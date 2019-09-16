from rest_framework import serializers
from .models import KeywordData


class KeywordDataSerilalizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KeywordData
        fields = ['date', 'count', 'keyword', 'qualifications_words', 'preferential_treatment_words']