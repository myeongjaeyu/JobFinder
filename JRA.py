import collections
import datetime
import re
import urllib.request
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from selenium import webdriver

import graph
from filter import filter

# driver_address = r'/home/ubuntu/Downloads/geckodriver'
driver_address = r'c:\chromedriver_win32\chromedriver.exe'

def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')
    options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(driver_address, chrome_options=options)
    driver.get(url)
    driver.implicitly_wait(2)
    return driver


class JobOpening:
    def __init__(self, company_name, job_title, key_word, url):
        self.date = datetime.date.today().strftime('%Y-%m-%d')
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
        for i, a in enumerate(words):
            for b in words[i + 1:]:
                if a.casefold() == b.casefold():
                    words[i] = b
            if a not in stop_words:
                result.append(words[i])
        result = filter(result)
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
        self.statistics['qualifications'] = collections.Counter(self.texts['qualifications']).most_common()
        self.statistics['preferential_treatment'] = collections.Counter(
            self.texts['preferential_treatment']).most_common()
        return self.statistics


class RoketPunch():
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
        # print(len(self.job_opening_list))
        return self.job_opening_list  # 공고 객체 리스트 반환

    def get_requirements(self):
        # 채용공고 오브젝트를 입력받아 해당 URL로 접속한 후 자격요건등이 포함된 텍스트 뭉치를 저장하고 반환하는 함수
        delete = list()  # 지워야 할 공고들을 저장하는 리스트
        for job_opening in self.job_opening_list:  # 공고 리스트 순회
            html = urllib.request.urlopen(job_opening.url).read().decode("utf-8")  # 공고 접속
            html = BeautifulSoup(html, "html.parser")  # 채용상세를 bs4객체화
            try:
                html = html.find(text=re.compile('자격|필수|Qualifications|이런 분을|Requirement|선호하는 인재상|지원요건|Who You Are')) \
                    .parent.prettify()  # 채용 상세에서 '자격'의 부모 찾기
                html = BeautifulSoup(html, "lxml").text.split('\n')
                words = [x for x in html if len(x.strip()) > 0]  # 찾은 텍스트를 리스트로
                job_opening.save_data(words)  # 해당 채용공고에 저장
            except:
                # print(job_opening.company_name, job_opening.url, sep='\n')
                # traceback.print_exc()
                delete.append(job_opening)      # 자격, 필수 둘다 못찾으면 삭제 목록에 추가
        for i in delete:
            self.job_opening_list.remove(i)  # 삭제
        return self.job_opening_list  # 채용 공고 리스트 반환


def deduplication(job_opening_list):
    checker = dict()
    tmp = list()
    for job in job_opening_list:
        try:
            if checker[job.url]:
                continue
        except:
            checker[job.url] = True
            tmp.append(job)
            continue
    return tmp


def init():
    keylist = [('모바일 게임', 'Mobile Game'),
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
            rp = RoketPunch(key[0])
            rp2 = RoketPunch(key[1])
            rp.job_opening_list += rp2.job_opening_list
            rp.job_opening_list = list(dict.fromkeys(rp.job_opening_list))
            key = key[1].replace(" ", "")
        else:
            rp = RoketPunch(key)
        rp.job_opening_list = deduplication(rp.job_opening_list)
        count = len(rp.job_opening_list)
        if count < 20:
            continue
        print(key, count)
        words = Splitter(rp.job_opening_list).get_words()
        wq = words['qualifications']
        pt = words['preferential_treatment']

        requests.post('http://127.0.0.1:8000/API/', json=
        {
            "count": count,
            "keyword": key,
            "qualifications_words": wq,
            "preferential_treatment_words": pt,
        },
                      auth=('ymj', '66859060')
                      )
        url1 = '/assets/' + str(datetime.date.today())[:-3] + key + '1.png'
        url2 = '/assets/' + str(datetime.date.today())[:-3] + key + '2.png'
        graph.word_cloud(wq, url1)
        graph.word_cloud(pt, url2)

if __name__ == "__main__":
    init()
