import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

from textblob.classifiers import NaiveBayesClassifier
import pandas as pd

from searchsite.crawl.mylogging import MyLogger

import os

emotionClassifyLogFile = 'log/emotionClassify.log'
emotionClassifyLogger = MyLogger(emotionClassifyLogFile)


dataFrame2 = '''On days when I feel close to my partner and other friends.   
When I feel at peace with myself and also experience a close  
contact with people whom I regard greatly.'''


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

class emotion_classify:
    def __init__(self):
        emotionClassifyLogger.debug("emo_classify init")
        cwd = os.getcwd()+'\\searchsite\\crawl'
        self.df = pd.read_csv(os.path.join(cwd, 'ISEAR.csv'))
        self.a = pd.Series(self.df['joy'])
        self.b = pd.Series(self.df[dataFrame2])
        self.new_df = pd.DataFrame({'Text': self.b, 'Emotion': self.a})

        self.stop = set(stopwords.words('english'))
        self.exclude = set(string.punctuation)
        self.lemma = WordNetLemmatizer()

        self.negative = ['not', 'neither', 'nor', 'but', 'however', 'although', 'nonetheless', 'despite', 'except',
                         'even though', 'yet']

        self.em_list = []
        self.text_list = []

        self.train = []

        self.sum_text_list = []

        self.e_score_dict = {}

        self.main()


    def clean(self, doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in self.stop if i not in self.negative])
        punc_free = "".join([ch for ch in stop_free if ch not in self.exclude])
        normalized = " ".join([self.lemma.lemmatize(word) for word in punc_free.split()])
        return normalized


    def iterate_clean(self):
        emotionClassifyLogger.debug("emo_iterate_clean")
        for i in range(self.df.shape[0]):
            self.new_df.loc[i]['Text'] = self.clean(self.new_df.loc[i]['Text'])


    def iterate_pop_text(self):
        emotionClassifyLogger.debug("emo_iter_pop_text")
        for i in range(self.new_df.shape[0]):
            self.text_list.append(self.new_df.loc[i]['Text'])


    def iterate_pop_emotion(self):
        emotionClassifyLogger.debug("emo_iterate_pop_emotion")
        for i in range(self.new_df.shape[0]):
            self.em_list.append(self.new_df.loc[i]['Emotion'])


    def create_train(self):
        emotionClassifyLogger.debug("emo_create_train")
        for i in range(self.new_df.shape[0]):
            self.train.append([self.text_list[i], self.em_list[i]])

    def classify_text(self, _smi):
        emotionClassifyLogger.info("emo_classify_text")
        cl = NaiveBayesClassifier(self.train)
        result = cl.classify(_smi)
        return result


    def main(self):
        emotionClassifyLogger.info("emo_main")
        self.iterate_clean()
        self.iterate_pop_emotion()
        self.iterate_pop_text()
        self.create_train()


