import datetime
import os
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render
from rest_framework import viewsets
import graph
from Analyzer.models import KeywordData
from .serializers import KeywordDataSerilalizer



#@csrf_exempt
def index(request):
    """
    채용공고 검색 키워드들을 목록으로 나타내주는 View
    :param request:
    :return:
    """
    keys = KeywordData.objects.values_list('keyword', flat=True)
    context = {'keys': keys}
    return render(request, 'Analyzer/index.html', context)


def results(request, keyword):
    """
    채용공고 수집 및 분석 결과를 그래프로 나타내주는 View
    :param request:
    :param keyword:
    :return:
    """
    # 오늘 날짜의 년, 월로 데이터를 찾는다.
    today = datetime.date.today()
    year = today.year
    month = today.month
    query = KeywordData.objects.filter(keyword=keyword).filter(date__year=year).filter(date__month=month)
    basic_words = list(query.values_list('qualifications_words', flat=True)[0])
    additional_words = list(query.values_list('additional_words', flat=True)[0])
    # Var 차트를 만들고
    var_chart1 = graph.draw_var_chart(basic_words)
    var_chart2 = graph.draw_var_chart(additional_words)
    # 생성된 워드 클라우드 이미지의 주소를 찾아서
    url1 = staticfiles_storage.url(str(today)[:-3] + keyword + '1.png')
    url2 = staticfiles_storage.url(str(today)[:-3] + keyword + '2.png')
    # 워드 클라우드 이미지가 존재하지 않으면 생성해준다.
    if not os.path.exists(os.getcwd() + url1):
        graph.word_cloud(query.basic_words, url1)
    if not os.path.exists(os.getcwd() + url2):
        graph.word_cloud(query.additional_words, url2)

    context = {'var_chart1': var_chart1, 'var_chart2': var_chart2,
               'word_cloud1': url1, 'word_cloud2': url2,
               'keyword': keyword, 'month': str(today.strftime("%B")),
               'year': str(today.strftime("%Y")), 'count': query.get().count
               }
    return render(request, 'Analyzer/results.html', context)


class KeywordDataViewSet(viewsets.ModelViewSet):
    """
    django rest framework 를 사용하기 위한 View
    """
    queryset = KeywordData.objects.all()
    serializer_class = KeywordDataSerilalizer
