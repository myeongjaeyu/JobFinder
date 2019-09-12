import datetime
import os
import requests
from celery.schedules import crontab
from celery.task import periodic_task
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
import Analyzer
import Crawler
import graph
from Analyzer.models import KeywordData
from .serializers import KeywordDataSerilalizer


class KeywordDataViewSet(viewsets.ModelViewSet):
    queryset = KeywordData.objects.all()
    serializer_class = KeywordDataSerilalizer


@csrf_exempt
def index(request):
    keys = KeywordData.objects.values_list('keyword', flat=True)
    context = {'keys': keys}
    return render(request, 'Analyzer/index.html', context)


def results(request, keyword):
    today = datetime.date.today()
    year = today.year
    month = today.month
    data = KeywordData.objects.filter(keyword=keyword).filter(date__year=year).filter(date__month=month)
    qualifications_words = list(data.values_list('qualifications_words', flat=True)[0])
    preferential_treatment_words = list(data.values_list('preferential_treatment_words', flat=True)[0])
    counted_qualifications_words = graph.counting_frequency(qualifications_words)
    counted_preferential_treatment_words = graph.counting_frequency(preferential_treatment_words)
    var_chart1 = graph.draw_var_chart(counted_qualifications_words[:30])
    var_chart2 = graph.draw_var_chart(counted_preferential_treatment_words[:30])
    url1 = staticfiles_storage.url(str(today)[:-3] + keyword + '1.png')
    url2 = staticfiles_storage.url(str(today)[:-3] + keyword + '2.png')
    if not os.path.exists(os.getcwd() + url1):
        graph.word_cloud(data.qualifications_words, url1)
    if not os.path.exists(os.getcwd() + url2):
        graph.word_cloud(data.preferential_treatment_words, url2)
    context = {'var_chart1': var_chart1, 'var_chart2': var_chart2,
               'word_cloud1': url1, 'word_cloud2': url2,
               'keyword': keyword, 'month': str(today.strftime("%B")),
               'year': str(today.strftime("%Y")), 'count': data.get().count
               }
    return render(request, 'Analyzer/results.html', context)


@periodic_task(run_every=crontab(minute=0, hour=0, day_of_month=15))
def every_two_weeks():
    keylist = [
        ('모바일 게임', 'Mobile Game'),
        ('백엔드', 'Backend'), ('프론트엔드', 'Frontend'), ('풀스택', 'Fullstack'),
        ('안드로이드', 'Android'), ('아이폰', 'Iphone'),
        ('머신러닝', 'Machine learning'), ('인공지능', 'AI'), ('데이터 엔지니어', 'Data Engineer'),
        ('게임 클라이언트', 'Game Client'),
        ('게임 서버', 'Game Servser'), ('네트워크', 'Network'), ('시스템', 'System'), ('보안', 'Security'), 'QA',
        ('사물인터넷', 'IoT'), ('응용프로그램', 'Application'), ('블록체인', 'Blockchain'),
        'Django', 'Spring', 'Go', 'Android', 'Swift',
        'React', 'Vue', 'Angular', 'Flask', 'Ruby',
        'Node', 'NET', 'TensorFlow', 'Hadoop', 'Unreal',
        'Cry', 'Unity', 'SQL', 'NoSQL', 'AWS',
    ]
    for key in keylist:
        if type(key) == tuple:
            rp = Crawler.RocketPunch(key[0])
            rp2 = Crawler.RocketPunch(key[1])
            rp.job_opening_list += rp2.job_opening_list
            rp.job_opening_list = list(dict.fromkeys(rp.job_opening_list))
            key = key[1].replace(" ", "")
        else:
            rp = Crawler.RocketPunch(key)

        result = Analyzer(rp.job_opening_list)
        count = len(result.job_opening_list)
        if count < 20:
            continue
        print(key, count)
        words = result.words

        requests.post('http://127.0.0.1:8000/API/', json=
        {
            "count": count,
            "keyword": key,
            "basic_words": words['basic'],
            "additional_words": words['additional'],
        },
                      auth=('ymj', '66859060')
                      )
        url1 = '/assets/' + str(datetime.date.today())[:-3] + key + '1.png'
        url2 = '/assets/' + str(datetime.date.today())[:-3] + key + '2.png'
        graph.word_cloud(words['basic'], url1)
        graph.word_cloud(words['additional'], url2)
