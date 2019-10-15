from Analyser import Analyzer
import Crawler

def every_month():
    """
        매달 15일에 Crawler, Analyser, graph 모듈을 사용하여 비즈니스 로직을 수행하고 데이터와
        워드 클라우드 이미지를 저장하는 함수.
        :return:
        """
    keyword_list = [
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
    for key in keyword_list:
        # 키워드가 (한글, 영어)로 형식으로 되어있으면
        if isinstance(key, tuple):
            rp = Crawler.RocketPunch(key[0])
            rp2 = Crawler.RocketPunch(key[1])
            # 검색 결과를 합친다.
            rp.job_opening_list += rp2.job_opening_list
            rp.job_opening_list = list(dict.fromkeys(rp.job_opening_list))
            key = key[1].replace(" ", "")
        else:
            rp = Crawler.RocketPunch(key)
        # 수집한 채용공고를 분석기에 넣어서 분석한다.
        result = Analyzer(rp.job_opening_list)
        count = len(result.job_opening_list)
        # 수집한 채용공고가 20개 이하면 통계를 낼만큼 충분한 표본을 확보하지 못하였으므로 저장하지 않는다.
        if count < 20:
            print(key, count)
            continue
        # 분석기로 분석한 단어들을 rest api를 통해 저장한다.
        words = result.words
        requests.post('http://127.0.0.1:8000/API/', json={
            "count": count,
            "keyword": key,
            "basic_words": words['basic'],
            "additional_words": words['additional'],
        },
                      auth=('ymj', '66859060')
                      )
        # 워드 클라우드 이미지를 static root에 저장한다
        url1 = '/assets/' + str(datetime.date.today())[:-3] + key + '1.png'
        url2 = '/assets/' + str(datetime.date.today())[:-3] + key + '2.png'
        graph.word_cloud(words['basic'], url1)
        graph.word_cloud(words['additional'], url2)
