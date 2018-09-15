from app.mylogging import MyLogger
from app.SubScraper import gomSubScraper
from app.EmotionClassifier import emotion_classify


subScrapDataLogFile = 'log/subScrapData.log'
subScrapDataLogger = MyLogger(subScrapDataLogFile)

import os
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

from search.models import Sub

gomSubScraper = gomSubScraper()
ec = emotion_classify()

if __name__=='__main__':
    gomLastPage = gomSubScraper.getLastPage()
    for page in range(1, gomLastPage + 1):
        sortSmiDictList = gomSubScraper.getSortSmiList(str(page))

        for sortSmiDict in sortSmiDictList:
            try:
                smiFileName = list(sortSmiDict.keys())[0]
                smiList = list(sortSmiDict.values())[0]
                for enSmi, korSmi in smiList:
                    try:
                        emotion = ec.classify_text(enSmi)
                        subScrapDataLogger.info(smiFileName + enSmi+ korSmi + emotion)
                        Sub(smi_filename=smiFileName, eng_sentence=enSmi, kor_sentence=korSmi, emotion=emotion).save()
                    except Exception as e:
                        subScrapDataLogger.error(e)
                        continue
            except Exception as e:
                subScrapDataLogger.error(e)
                continue
