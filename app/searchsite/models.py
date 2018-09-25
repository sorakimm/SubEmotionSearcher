from django.db import models
from django.utils import timezone
from searchsite.search.search import SubIndex

# Create your models here.

class Sub(models.Model):
    smi_filename = models.CharField(max_length=200)  # Field name made lowercase.
    eng_sentence = models.CharField(max_length=500)  # Field name made lowercase.
    kor_sentence = models.CharField(max_length=500)  # Field name made lowercase.
    emotion = models.CharField(max_length=45, blank=True, null=True)
    crawled_date = models.DateField(default=timezone.now)

    def indexing(self):
        obj = SubIndex(
            meta={'id': self.id},
            smi_filename=self.smi_filename,
            eng_sentence=self.eng_sentence,
            kor_sentence=self.kor_sentence,
            emotion=self.emotion,
            crawled_date=self.crawled_date
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    def __str__(self):
        return self.smi_filename
