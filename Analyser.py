import collections
import json
import re

from nltk.corpus import stopwords


class Analyzer:
    def __init__(self, job_opening_list):
        with open('words.json', 'r') as f:
            file = json.loads(f.read())
        self.file = file
        self.job_opening_list = job_opening_list
        self.deduplication()
        self.lines = self.line_splitter()
        self.words = dict()
        self.words['basic'] = self.word_splitter(self.lines['basic'])
        self.words['additional'] = self.word_splitter(self.lines['additional'])
        self.frequency = self.counting_frequency()

    def deduplication(self):
        """
        수집한 채용공고의 중복을 제거해주는 함수
        :return:
        """
        checker = dict()
        tmp = list()
        for job in self.job_opening_list:
            try:
                if checker[job.url]:
                    continue
            except KeyError:
                checker[job.url] = True
                tmp.append(job)
                continue
        self.job_opening_list = tmp

    def line_splitter(self):
        """
        채용공고에서 추출한 텍스트에서 '자격요건'과 '우대사항'을 분리해주는 함수
        :return:
        """
        # '자격', '필수' 같이 '자격요건' 항목으로 쓰일만한 단어들을 찾아서
        # '우대' 같은 단어가 나올때까지 '자격 요건'으로 집어넣고,
        # 우대사항부터 끝까지 혹은 '복지', '혜택'과 같은 다른 항목으로 넘어갈때까지
        # '우대 사항'으로 집어넣는다.
        start_str = self.file["start_str"]
        middle_str = self.file["middle_str"]
        end_str = self.file["end_str"]
        for job in self.job_opening_list:
            start = None
            middle = None
            end = None
            for text in job.texts:
                if any(x in start_str for x in text):
                    start = job.texts.index(text) + 1
                if any(x in middle_str for x in text):
                    middle = job.texts.index(text)
                if any(x in end_str for x in text):
                    end = job.texts.index(text)
                    break
            if not middle:
                middle = job.texts.index(job.texts[-1]) + 1
            if not end:
                end = job.texts.index(job.texts[-1]) + 1
            [self.lines['basic'].append(x) for x in job.texts[start:middle]]
            [self.lines['additional'].append(x) for x in job.texts[middle + 1:end]]
        return self.lines

    def word_splitter(self, lines):
        """
        추출한 '자격 요건'과 '우대 사항'에서 한글을 전부 제거하고
        남은 영문에서 불용어를 제거해 의미 있는 단어만 뽑아서 리스트로 반환하는 함수
        :param lines:
        :return:
        """
        words = list()
        result = list()
        for line in lines:
            line = re.sub('[^a-zA-Z]', ' ', line).split(' ')
            [words.append(x) for x in line if len(x) > 1]
        stop_words = set(stopwords.words('english'))
        # 똑같은 단어인데 대소문자만 다른 단어들을 통일시켜준다.
        for i, a in enumerate(words):
            for b in words[i + 1:]:
                if a.casefold() == b.casefold():
                    words[i] = b
            if a not in stop_words:
                result.append(words[i])
        return self.word_filter(result)

    def counting_frequency(self):
        """
        각 단어들의 빈도를 카운팅해주는 함수
        :return:
        """
        self.frequency['basic'] = collections.Counter(self.texts['basic']).most_common()
        self.frequency['additional'] = collections.Counter(
            self.texts['additional']).most_common()
        return self.frequency

    def word_filter(self, words):
        """
        자주 나오는 단어중에서 쓸모없는 단어를 제거하고
        분리된 복합어를 합쳐주는 함수
        :param words:
        :return:
        """
        remove_list = self.file["remove"]
        compound_keys = self.file["compound_key"]
        compound_values = self.file["compound_value"]
        compound_words = dict()
        for k, v in zip(compound_keys, compound_values):
            compound_words[k] = v
        for i, word in enumerate(words):
            word = word.lower()
            if word in remove_list:
                words[i] = ''
            elif word in compound_keys:
                words[i] = compound_words[word]
        new_list = [x for x in words if x]
        return new_list
