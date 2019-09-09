import unittest
from konlpy.tag import Komoran
from konlpy.utils import pprint
import re
from konlpy.tag import Hannanum
import collections
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import urllib.request
import tmp
import plotly.graph_objects as go
import matplotlib
import requests


class MyTestCase(unittest.TestCase):
    def test_something(self):
        requests.post('http://127.0.0.1:8000/API/', json=
        {
            "count": 1231,
            "keyword": 'Django',
            "words": ['gasdf'] * 1000
        },
                      auth=('ymj', '66859060')
                      )


if __name__ == '__main__':
    unittest.main()



"""

            html = urllib.request.urlopen(job_opening.url).read().decode("utf-8")  # 공고 접속
            html = BeautifulSoup(html, "html.parser")  # 채용상세를 bs4객체화


        #JobRequirementAnalyzer.init()
        stop_words = list()
        sample = list()
        stop_words_re = list()
        with open('stop_words.txt') as file:
            for line in file.readlines():
                stop_words.append(line.strip().split('\t'))
        with open('sample.txt') as file:
            for line in file.readlines():
                if line != '\n':
                    sample.append(line.strip().split(' '))

        words = list()
        for text in sample:
            for i in text:
                i = re.sub('[^a-zA-Z]', ' ', i).split(' ')
                tmp = list()
                [tmp.append(x) for x in i if len(x) > 1]
                if tmp:
                    words.append(tmp)
        for i in words:
            print(i)




        words = list()
        for text in sample:
            for i in text:
                i = re.sub('[^a-zA-Z]', ' ', i).split(' ')
                tmp = list()
                [tmp.append(x) for x in i if len(x) > 1]
                if tmp:
                    words.append(tmp)
        for i in words:
            print(i)
"""