from django.contrib.postgres.fields import ArrayField
from django.db import models


class KeywordData(models.Model):
    date = models.DateField(auto_now=True)
    count = models.IntegerField(null=False)
    keyword = models.CharField(max_length=50, primary_key=True)
    basic_words = ArrayField(models.CharField(max_length=50), null=True)
    additional_words = ArrayField(models.CharField(max_length=50), null=True)

    class Meta:
        unique_together = (("date", "keyword"),)
