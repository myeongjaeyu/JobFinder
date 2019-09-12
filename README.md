# JobRequirementsAnalyzer
- 웹에서 채용공고를 수집하여 <자격 요건>과 <우대 사항> 등을 분석하여 그래프로 제공하는 서비스입니다.  

<br>

## 개발 동기
최근 취업 포트폴리오로 사용할 개인 프로젝트를 하려고 마음먹었습니다. 그런데 <br>

> 어떤 언어(기술)을 사용해야 취업에 도움이 될까 ?

와 같은 고민을 하게되었고, 고민 도중 채용 공고에 보면 <필수 요건> 혹은 <br>
<우대 요건> 같은 부분이 있다는걸 생각해냈습니다. <br>  
채용 정보 사이트에서 많이 찾고 있는 기술들을 사용하기로 마음먹고 정보를 모으기 시작했습니다.<br>

![채용공고 확대](https://user-images.githubusercontent.com/44807859/64788805-2eefbd00-d5ae-11e9-97e4-8cee68e43644.png)

<br>
엑셀을 이용해 채용공고를 10개쯤 수집했을 때.

> 내가 개발자(지망생)인데, 이걸 일일히 복사 붙여넣기를 하고 있어야 하나 ? 

라는 생각이 들었고, 채용공고를 수집해서 통계를 내주는 웹앱을 만들기로 결정했습니다.


## 개발 환경
![python3](https://user-images.githubusercontent.com/44807859/64787062-da970e00-d5aa-11e9-8799-3ed8432e27e5.png)
- python3 :
Selenium, Beautiful Soup과 같은 강력한 라이브러리들이 있어서
웹에서 채용공고 정보를 수집할 크롤러를 만들기 수월한 언어입니다.


![django](https://user-images.githubusercontent.com/44807859/64785931-60fe2080-d5a8-11e9-8311-3683f10cf73d.png)

- Django :
현재 취업 준비를 하는 상황에서 직접 사용하려고 만드는 프로젝트이기 때문에 
이미 사용해봐서 익숙하고 빠르게 웹앱을 만들 수 있는 강력한 웹 프레임워크인 Django를 사용했습니다.

![postgresql](https://user-images.githubusercontent.com/44807859/64786324-28ab1200-d5a9-11e9-9aaa-d283f9fa0ed7.png)

- postgresql :
*two scoops of django* 와 같은 Django 관력 서적과 스택오버플로우 등에서 
Django와 같이 사용하기 좋은 RDBS로 postgresql을 많이 뽑고 있습니다.

![AWS EC2](https://user-images.githubusercontent.com/44807859/64786336-2cd72f80-d5a9-11e9-8f41-62b8413660b1.png)

- AWS EC2 : 
윈도우에서도 배포를 할 수는 있지만 리눅스 환경에서 배포하는것 편하고 
컴퓨터를 계속 켜둘 수 없는 상황에서 가장 합리적인 선택이였습니다.
AWS를 경험해보고 싶다는것도 큰 이유였습니다.

![Amazon RDS](https://user-images.githubusercontent.com/44807859/64786335-2cd72f80-d5a9-11e9-8663-ad66f9061ce6.png)

- AWS RDS: 
AWS EC2를 선택한 것과 같이 컴퓨터를 계속 켜둘 수 없고 채용 공고를 전부 저장하는 것이 아니라 검색 키워드와 텍스트들만 저장할 것이기 때문에 무료로 사용할 수 있는 용량으로 충분하여 선택하였습니다.


## 프로젝트 설명

### 간단한 구조도

![프로젝트 구조2](https://user-images.githubusercontent.com/44807859/64790679-6e6bd880-d5b1-11e9-9ab7-f569ba325008.jpg)


### 개발 과정
##### 1. 크롤러
- 파이썬 requests 모듈을 사용하여 채용공고 정보들을 수집했고, 정보보호를 위해 채용공고 정보를 숨기는 사이트는 selenium을 통해 구글 크롬 웹드라이버로 직접 접속하도록 하여 채용공고들의 회사이름, 공고 타이틀, URL등을 긁어왔습니다.

- 수집한 채용 공고들을 순회하면서 텍스트를 전부 수집한 뒤 "필수 요건", "지원 자격", "우대 사항"을 비롯한 단어들로 텍스트를 검색하여 필요없는 텍스트를 삭제합니다.


##### 2. 분석기
- 필요 없는 텍스트를 삭제하고 나온 <필수 요건>, <우대 사항> 과 같은 텍스트들을 한글은 한국어 형태소 분석기 KoNLPy, 영문은 자연어 처리 패키지 nltk를 이용하여 조사와 같은 불용어를 제거하였습니다.

![카톡](https://user-images.githubusercontent.com/44807859/64793168-9c531c00-d5b5-11e9-9427-b6d9c092c0ac.png)

- 이 과정까지 진행한 후 테스트 결과 한글 제가 원하는 정보인 Tech Stack에 관련된 단어들은 80% 이상이 영문이라는걸 알았고 한글을 제거하기로 결정하였습니다.

- 한글과 불용어를 제거한 단어 리스트들을 자격 요건과 우대 사항으로 나눠서 저장한 뒤, 각각의 단어들의 빈도수를 계산하였습니다.

##### 3. 그래프

![필수요건](https://user-images.githubusercontent.com/44807859/64794216-25b71e00-d5b7-11e9-926c-888245618f36.PNG)
![2019-09Frontend2](https://user-images.githubusercontent.com/44807859/64794247-2f408600-d5b7-11e9-9a36-38cf0c12d86f.png)


- 처음에는 단어의 빈도 수와 퍼센테이지를 테이블 형태로 제공하려고 했으나, 좀 더 아름답고 효과적으로 정보를 제공하기 위해 빈도 수는 Var chart로 만들고 퍼센테이지는 Word Cloud를 그려서 제공하였습니다.


##### 4. Django 웹앱

- Models : 키워드, 날짜, 필수 요건 단어 리스트, 우대 요건 단어 리스트의 4가지 필드만 있는 간단한 모델입니다.<br>

- Templates : 프론트 페이지에선 Role 탭과 Skills 탭으로 구분되어 유의미한 채용 공고 수를 수집할 수 있는 키워드들만 버튼으로 제공합니다. 버튼을 클릭하면 해당 키워드의 통계를 그래프로 보여줍니다.<br>

- View : 사용자가 클릭한 버튼의 키워드와 해당 날짜로 DB를 검색하여 단어들을 가져오고 통계를 낸 뒤 그래프를 그려줍니다. 매달 15일에 자동으로 크롤러와 분석기를 실행하여 DB에 저장합니다.


##### 5. 배포

- AWS EC2 : AWS elastic beanstalk를 사용하여 쉽게 Django 앱을 구성해본적은 있었지만 
본격적으로 AWS를 사용해본것은 처음이였습니다. 
하지만 AWS 문서가 한글로 자세하게 구성되어 있어 EC2 인스턴스를 만드는 과정은 어렵지 않았습니다.<br>

- uWSGI + NGINX 배포 : 리눅스 환경에서 Django 웹앱을 배포해본 경험이 있었기 때문에 간단한 검색을 통해 쉽게 배포에 성공하였습니다.<br>

- AWS RDS : AWS RDS는 사용할 DB를 고르고 클릭만 하면 DB를 구성해주기 때문에 로컬에서 서버를 여는것만큼 쉬웠습니다.<br>

## RESTful API ?

- 프로젝트를 완성하고 테스트를 하던 도중 Backend와 Django 키워드에서 'RESTful' 이라는 단어가 엄청나게 높은 빈도수를 기록하는 것을 발견하였습니다.

- RESTful API에 대한 정의를 읽어봤지만 감이 안오던 도중 Django에는 RESTful API를 쉽게 구성할 수 있도록 해주는 django rest framework가 있다는걸 알게되었습니다.

### 실제로 구성해본 RESTful API의 위력

![API1](https://user-images.githubusercontent.com/44807859/64798219-9b25ed00-d5bd-11e9-9d55-b1efd443f26f.PNG)

![API2](https://user-images.githubusercontent.com/44807859/64798220-9b25ed00-d5bd-11e9-854d-7af8247bbc99.PNG)

- django rest framework를 이용하여 실제로 구현해보니 그 위력을 알게되었습니다.
- DB에 연결하지도 않았는데, 이런 간단한 코드만으로 데이터를 주고받을수있다니 ! 

# END
