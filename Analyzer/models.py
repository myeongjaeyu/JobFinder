from django.db import models
from django.contrib.postgres.fields import ArrayField


class KeywordData(models.Model):
    date = models.DateField(auto_now=True)
    count = models.IntegerField(null=False)
    keyword = models.CharField(max_length=50, primary_key=True)
    qualifications_words = ArrayField(models.CharField(max_length=50), null=True)
    preferential_treatment_words = ArrayField(models.CharField(max_length=50), null=True)

# Create your models here.