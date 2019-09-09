from selenium import webdriver
from bs4 import BeautifulSoup
import re
import traceback
from datetime import datetime
import collections
from nltk.corpus import stopwords
import plotly.graph_objects as go
import urllib.request
import matplotlib
import matplotlib.pyplot as plt
import squarify
from wordcloud import WordCloud
import requests
import datetime
import os
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.options import Options


driver_address = r'/home/ubuntu/Downloads/geckodriver'


def get_driver(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=driver_address)
    driver.get(url)
    driver.implicitly_wait(3)
    return driver


class JobOpening:
    def __init__(self, company_name, job_title, key_word, url):
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.company_name = company_name
        self.job_title = job_title
        self.key_word = key_word
        self.url = url
        self.texts = list()
        self.html = list()

    def save_data(self, texts):
        self.texts = texts


class Splitter:
    def __init__(self, job_opening_list):
        self.qualifications = list()
        self.preferential_treatment = list()
        self.words = dict()
        start_str = ['자격', '필수', '이런 분을', 'Qualifications', '선호하는 인재상', ' Requirement', '지원요건', 'Who You Are']
        for job in job_opening_list:
            start = None
            middle = None
            end = None
            for text in job.texts:
                if any(x in start_str for x in text):
                    start = job.texts.index(text) + 1
                if '우대' in text:
                    middle = job.texts.index(text)
                if '복지' in text or '혜택' in text or '채용' in text:
                    end = job.texts.index(text)
                    break
            if not middle:
                middle = job.texts.index(job.texts[-1]) + 1
            if not end:
                end = job.texts.index(job.texts[-1]) + 1
            [self.qualifications.append(x) for x in job.texts[start:middle]]
            [self.preferential_treatment.append(x) for x in job.texts[middle + 1:end]]
        self.words['qualifications'] = self.eng_split(self.qualifications)
        self.words['preferential_treatment'] = self.eng_split(self.preferential_treatment)

    def eng_split(self, texts):
        words = list()
        result = list()
        for text in texts:
            text = re.sub('[^a-zA-Z]', ' ', text).split(' ')
            [words.append(x) for x in text if len(x) > 1]
        stop_words = set(stopwords.words('english'))
        print(words, end='\n')
        for i, a in enumerate(words):
            for b in words[i + 1:]:
                if a.casefold() == b.casefold():
                    words[i] = b
            if a not in stop_words:
                result.append(words[i])
        print(result, end='\n')
        return result

    def get_words(self):
        return self.words


class Analyzer:
    def __init__(self, texts):
        self.texts = texts
        self.statistics = dict()
        self.qualifications = dict()
        self.preferential_treatment = dict()
        self.counting_frequency()

    def counting_frequency(self):
        self.statistics['qualifications'] = collections.Counter(self.texts['qualifications']).most_common(100)
        self.statistics['preferential_treatment'] = collections.Counter(self.texts['preferential_treatment']).most_common(100)
        return self.statistics


class KeyWordData:
    def __init__(self, job_opening_list):
        self.job_opening_list = job_opening_list
        self.splited_words = Splitter(self.job_opening_list).get_words()  # 문자열 리스트를 단어 리스트로 반환
        self.statistics = Analyzer(self.splited_words).counting_frequency()  # 단어 리스트를 통계로 반환
        """
        self.draw_var_chart(self.statistics['qualifications'][:30])
        self.draw_var_chart(self.statistics['preferential_treatment'][:30])
        self.draw_treemap(self.statistics['qualifications'][:30])
        self.draw_treemap(self.statistics['preferential_treatment'][:30])
        self.word_cloud(self.splited_words['qualifications'])
        self.word_cloud(self.splited_words['preferential_treatment'])
        """

    def draw_var_chart(self, data):
        x = list()
        y = list()
        width = list()
        for key, value in data:
            x.insert(0, value)
            y.insert(0, key)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x,
            y=y,
            text=x,
            textposition='outside',
            orientation='h',
            marker_color='#696969',
        ))
        fig.update_layout(
            autosize=False,
            height=1200,
            width=800,
            font=dict(
                size=14
            )
        )
        fig.update_xaxes(automargin=True)
        fig.update_yaxes(automargin=True)
        fig.show()

    def word_cloud(self, data):
        wordcloud = WordCloud(
            max_font_size=100,
            background_color="white",
            width=1200,
            height=800,
            colormap=matplotlib.cm.RdYlGn
        )
        wordcloud = wordcloud.generate(' '.join(data))

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def draw_treemap(self, data):
        fig = go.Figure()
        keys = list()
        values = list()
        for key, value in data:
            values.insert(0, value)
            keys.insert(0, key)

        x = 0.
        y = 0.
        width = 100.
        height = 100.

        normed = squarify.normalize_sizes(values, width, height)
        rects = squarify.squarify(normed, x, y, width, height)

        # Choose colors from http://colorbrewer2.org/ under "Export"
        color_brewer = ['#42926b', '#394b41', '#9cb0a4', ' #1d1d35',
                        '#0e8dbe', '#005b88', '#3784e1', '#cf634d'] * 10
        shapes = []
        annotations = []
        counter = 0

        for r, key, val, color in zip(rects, keys, values, color_brewer):
            shapes.append(
                dict(
                    type='rect',
                    x0=r['x'],
                    y0=r['y'],
                    x1=r['x'] + r['dx'],
                    y1=r['y'] + r['dy'],
                    line=dict(width=2),
                    fillcolor=color
                )
            )
            annotations.append(
                dict(
                    x=r['x'] + (r['dx'] / 2),
                    y=r['y'] + (r['dy'] / 2),
                    text=key,
                    showarrow=False
                )
            )

        # For hover text
        fig.add_trace(go.Scatter(
            x=[r['x'] + (r['dx'] / 2) for r in rects],
            y=[r['y'] + (r['dy'] / 2) for r in rects],
            text=[str(v) for v in keys],
            mode='lines+markers+text',
        ))

        fig.update_layout(
            height=700,
            width=700,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            shapes=shapes,
            annotations=annotations,
            hovermode='closest'
        )

        fig.show()


class JobInfoSite:
    def __init__(self, keyword):
        pass

    def search(self):
        pass

    def get_general_info(self):
        pass

    def get_requirements(self):
        pass


class RoketPunch(JobInfoSite):
    def __init__(self, keyword):
        self.keyword = keyword
        self.url = 'https://www.rocketpunch.com/jobs?keywords=' + self.keyword
        self.driver = get_driver(self.url)
        self.html_list = list()
        self.job_opening_list = list()
        self.search()
        self.get_general_info()
        self.get_requirements()

    def search(self):
        # 키워드를 입력받아 로켓펀치를 검색한 후 HTML 데이터를 리턴하는 함수
        try:
            pages = int(self.driver.find_element_by_class_name('tablet.computer.large.screen.widescreen.only') \
                        .find_elements_by_tag_name('a')[-1].text) # 검색결과 페이지 수
            for i in range(1, pages + 1): # 페이지 수 만큼 반복
                self.driver.get(self.url + '&page=' + str(i)) # 각 페이지를 돌면서
                openings = self.driver.find_elements_by_class_name('company.item') # 해당 페이지의 공고 리스트 수집
                [self.html_list.append(opening.get_attribute('innerHTML')) for opening in openings]
                # 공고 정보가 담긴 html 들을 리스트로 저장
        except: # 검색 결과 페이지 수가 1개인 경우
            openings = self.driver.find_elements_by_class_name('company.item')
            if openings: # 공고가 하나라도 있으면
                [self.html_list.append(opening.get_attribute('innerHTML')) for opening in openings]
                # 공고 정보 저장
        return self.html_list  # 공고 정보 리스트 반환

    def get_general_info(self):
        # HTML 리스트를 입력받아 그 안에서 회사명, 공고명, 공고URL 등을 추출하여 리턴하는 함수
        for html in self.html_list: # 저장한 공고 정보 리스트 순회
            soup = BeautifulSoup(html, "html.parser")  # html을 bs4 객체로 변환
            name = soup.find('strong').getText()       # 회사 이름 찾기
            job_title = soup.find('a', class_='job-title').getText()  # 공고 제목 찾기
            url = 'https://www.rocketpunch.com' + soup.find('a', class_='job-title')['href']  # 공고 url 찾기
            self.job_opening_list.append(JobOpening(name, job_title, self.keyword, url))  # 공고 객체를 만들어서 정보 저장
        print(len(self.job_opening_list))
        return self.job_opening_list  # 공고 객체 리스트 반환

    def get_requirements(self):
        # 채용공고 오브젝트를 입력받아 해당 URL로 접속한 후 자격요건등이 포함된 텍스트 뭉치를 저장하고 반환하는 함수
        delete = list()  # 지워야 할 공고들을 저장하는 리스트
        for job_opening in self.job_opening_list:  # 공고 리스트 순회
            html = urllib.request.urlopen(job_opening.url).read().decode("utf-8")  # 공고 접속
            html = BeautifulSoup(html, "html.parser")  # 채용상세를 bs4객체화
            try:
                html = html.find(text=re.compile('자격|필수|Qualifications|이런 분을|Requirement|선호하는 인재상|지원요건|Who You Are'))\
                    .parent.prettify()  # 채용 상세에서 '자격'의 부모 찾기
                html = BeautifulSoup(html, "lxml").text.split('\n')
                words = [x for x in html if len(x.strip()) > 0]  # 찾은 텍스트를 리스트로
                job_opening.save_data(words)  # 해당 채용공고에 저장
            except:
                print(job_opening.company_name, job_opening.url, sep='\n')
                traceback.print_exc()
                delete.append(job_opening)      # 자격, 필수 둘다 못찾으면 삭제 목록에 추가
        for i in delete:
            self.job_opening_list.remove(i)  # 삭제
        return self.job_opening_list  # 채용 공고 리스트 반환


def init():
    keylist = [
            'Django', 'Spring', 'Go', 'Android', 'Swift',
            'React', 'Vue', 'Angular', 'Flask', 'Ruby',
            'Node.js', '.NET', 'TensorFlow', 'Hadoop', 'Unreal Engine',
            'CryEngine', 'Unity', 'SQL', 'NoSQL', 'AWS',
            '백엔드', '프론트엔드', '풀스택', '안드로이드','아이폰',
            '머신러닝', '인공지능', '데이터 엔지니어', '모바일 게임', '게임 클라이언트',
            '게임 서버', '네트워크', '시스템', '인터넷 보안', 'QA',
            '사물인터넷', '응용프로그램', '블록체인']
    for key in keylist:
        rp = RoketPunch(key)
        words = KeyWordData(rp.job_opening_list).splited_words
        wq = words['qualifications']
        pt = words['preferential_treatment']
        count = len(rp.job_opening_list)
        requests.post('http://0:8080/API/', json=
        {
            "count": count,
            "keyword": key,
            "qualifications_words": wq,
            "preferential_treatment_words": pt,
        },
                      auth=('ymj', '66859060')
                      )
        url1 = os.getcwd() + '/assets/' + str(datetime.date.today)[:-3] + key + '1.png'
        url2 = os.getcwd() + '/assets/' + str(datetime.date.today)[:-3] + key + '2.png'
        graph.word_cloud(wq, url1)
        graph.word_cloud(pt, url2)

if __name__ == "__main__":
    init()
