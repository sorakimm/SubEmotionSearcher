from django.db import models

# Create your models here.
class Sub(models.Model):
    smi_filename = models.CharField(db_column='smiFileName', max_length=200)  # Field name made lowercase.
    eng_sentence = models.CharField(db_column='engSentence', max_length=500)  # Field name made lowercase.
    kor_sentence = models.CharField(db_column='korSentence', max_length=500)  # Field name made lowercase.
    emotion = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.smi_filename
