import datetime
import re
import urllib.request
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver

driver_address = r'c:\chromedriver_win32\chromedriver.exe'


def get_driver(url):
    """
    웹 드라이버를 사용하여 매개변수인 url로 접속한 후 드라이버를 반환하는 함수
    :param url:
    :return: driver
    """
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


class RocketPunch:
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
                        .find_elements_by_tag_name('a')[-1].text)  # 검색결과 페이지 수
            for i in range(1, pages + 1):  # 페이지 수 만큼 반복
                self.driver.get(self.url + '&page=' + str(i))  # 각 페이지를 돌면서
                openings = self.driver.find_elements_by_class_name('company.item')  # 해당 페이지의 공고 리스트 수집
                [self.html_list.append(opening.get_attribute('innerHTML')) for opening in openings]
                # 공고 정보가 담긴 html 들을 리스트로 저장
        except:  # 검색 결과 페이지 수가 1개인 경우
            openings = self.driver.find_elements_by_class_name('company.item')
            if openings:  # 공고가 하나라도 있으면
                [self.html_list.append(opening.get_attribute('innerHTML')) for opening in openings]
                # 공고 정보 저장
        return self.html_list  # 공고 정보 리스트 반환

    def get_general_info(self):
        # HTML 리스트를 입력받아 그 안에서 회사명, 공고명, 공고URL 등을 추출하여 리턴하는 함수
        for html in self.html_list:  # 저장한 공고 정보 리스트 순회
            soup = BeautifulSoup(html, "html.parser")  # html을 bs4 객체로 변환
            name = soup.find('strong').getText()  # 회사 이름 찾기
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
                html = html.find(text=re.compile('자격|필수|basic|이런 분을|Requirement|선호하는 인재상|지원요건|Who You Are')) \
                    .parent.prettify()  # 채용 상세에서 '자격'의 부모 찾기
                html = BeautifulSoup(html, "lxml").text.split('\n')
                words = [x for x in html if len(x.strip()) > 0]  # 찾은 텍스트를 리스트로
                job_opening.save_data(words)  # 해당 채용공고에 저장
            except:
                # print(job_opening.company_name, job_opening.url, sep='\n')
                # traceback.print_exc()
                delete.append(job_opening)  # 자격, 필수 둘다 못찾으면 삭제 목록에 추가
        for i in delete:
            self.job_opening_list.remove(i)  # 삭제
        return self.job_opening_list  # 채용 공고 리스트 반환
