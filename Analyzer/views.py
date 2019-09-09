from Analyzer.models import KeywordData
from rest_framework import viewsets
from .serializers import KeywordDataSerilalizer
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.storage import staticfiles_storage
import os
import graph


@csrf_exempt
def index(request):
    keys = KeywordData.objects.values_list('keyword', flat=True)
    context = {'keys': keys}
    return render(request, 'Analyzer/index.html', context)


def results(request, keyword):
    data = get_object_or_404(KeywordData, pk=keyword)
    qualifications_words = data.qualifications_words
    preferential_treatment_words = data.preferential_treatment_words
    counted_qualifications_words = graph.counting_frequency(qualifications_words)
    counted_preferential_treatment_words = graph.counting_frequency(preferential_treatment_words)
    var_chart1 = graph.draw_var_chart(counted_qualifications_words[:30])
    var_chart2 = graph.draw_var_chart(counted_preferential_treatment_words[:30])
    url1 = staticfiles_storage.url(str(data.date)[:-3] + data.keyword + '1.png')
    url2 = staticfiles_storage.url(str(data.date)[:-3] + data.keyword + '2.png')
    if not os.path.exists(os.getcwd() + url1):
        graph.word_cloud(data.qualifications_words, url1)
    if not os.path.exists(os.getcwd() + url2):
        graph.word_cloud(data.preferential_treatment_words, url2)
    context = {'var_chart1': var_chart1, 'var_chart2': var_chart2,
               'word_cloud1': url1, 'word_cloud2': url2}
    return render(request, 'Analyzer/results.html', context)


class KeywordDataViewSet(viewsets.ModelViewSet):
    queryset = KeywordData.objects.all()
    serializer_class = KeywordDataSerilalizer
