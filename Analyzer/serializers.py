from rest_framework import serializers
from .models import KeywordData
from django.contrib.auth.models import User


class KeywordDataSerilalizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KeywordData
        fields = ['date', 'count', 'keyword', 'qualifications_words', 'preferential_treatment_words']