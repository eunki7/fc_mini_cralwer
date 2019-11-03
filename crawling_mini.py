from time import sleep
from bs4 import BeautifulSoup
import requests
import time
import csv

# Atom 에디터일 경우 아래 4줄 주석 해제
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# 미니 프로젝트 예제 소스

# 본 소스코드는 미니 프로젝트의 예시입니다.
# 사이트는 ★본인이 원하는 사이트★를 대상으로 합니다.
# ★★크롤링 대상 사이트의 서버 부하 등 문제를 야기해서는 안됩니다.★★
# 크롤링 대상 사이트의 Dom 구조가 변경되어서 작동이 되지 않을 수 있습니다.


# 클래스 형태로 크롤러를 제작합니다.
# 각 기능별로 상세하게 메소드로 분리 후 역할에 맞게 작성합니다.
# 본인이 크롤링 하고 싶은 사이트로 변경해서 작성 부탁드립니다.

# 아래 예제는 다음 뉴스 사이트를 대상으로 작성했습니다.
# 어렵지 않은 예제 소스이니 크롤링 기초 과정을 수강 후 매우 쉽게 작성 가능합니다.
# 단편성 크롤링이 아닌 페이지 내 이동 규칙을 적용해서 소스코드 작성을 부탁드립니다.
# 크롤링 결과는 본인이 원하는 파일 포멧(CSV, TXT, JSON)등으로 꼭 저장해 봅니다.
# ★예외 처리는 최소화★로 작성했습니다.
# 특히 ★마지막 페이지가 없는 경우★는 조건문으로 처리를 꼭 해주셔야 합니다.
class DaumArticleCrawler(object):
    # 초기화
    def __init__(self):
        # 다음뉴스의 IT 섹션의 기사를 대상으로 합니다.
        self.target_url = 'https://news.daum.net/breakingnews/digital?page='
        # 크롤링 페이지 범위를 지정합니다.
        # 기본값은 1 ~ 10 (총 10페이지)
        self.range = {'s_page': 1, 'e_page': 10}
    
    
    # 범위 지정
    def set_page_range(self, s_page, e_page):
        self.range['s_page'] = s_page
        self.range['e_page'] = e_page
    
    
    # 크롤링
    @staticmethod
    def crawling(self):
        # 수집 데이터 전체 저장
        article_list = []
        # 시작페이지 -> 끝 페이지
        for number in range(self.range['s_page'], self.range['e_page'] + 1):
            # 페이지 URL 완성
            URL = self.target_url + str(number)
            
            # URL 확인
            # print(URL)
            
            # 실제 요청
            response = requests.get(URL)
            # 크롤링 딜레이(반드시 작성 1초 이상 권장)
            time.sleep(0.5)
            
            # 수신 데이터 확인(주석 해제 후 확인)
            # 수신 헤더 정보
            # print(response.headers)
            # 수신 인코딩 정보
            # print(response.encoding)
            # 수신 데이터 수신 OK
            # print(response.ok)
            # 수신 컨텐츠 정보
            # print(response.content)
            # 수신 텍스트
            # print(response.text)
            
            # bs4 선언 및 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 이 부분에서 본인이 원하는 내용을 파싱
            # 본 예제에서는 간단하게 제목, 본문 미리보기 파싱
            # 신문 본문 클릭 후 상세 내용도 직접 구현해 보세요.
            
            # 기사 본문 전체 영역
            article_body = soup.select('div.box_etc > ul.list_news2 > li')
            
            # 각 부분 파싱
            for body in article_body:
                # 신문사
                paper_info = body.select_one('span.info_news').text.strip()
                # 기사 제목
                title = body.select_one('strong.tit_thumb > a.link_txt').text.strip()
                # 기사 본문(미리보기)
                content = body.select_one('span.link_txt').text.strip()
                
                article_list.append((paper_info, title, content))
        
        # CSV 파일 저장
        self.export_csv(article_list)
    
    
    # 파일 저장
    def export_csv(self, args):
        # CSV 파일 쓰기
        # 관리자 권한 확인(윈도우), 본인이 원하는 경로 및 파일명 지정
        with open('./result_article.csv', 'w', encoding='utf-8') as f:
             # Writer 객체 생성 
             wt = csv.writer(f)
             # Tuple to Csv
             for c in args:
                 wt.writerow(c)
    
    
    # 시작
    def start(self):
        DaumArticleCrawler.crawling(self)


if __name__ == "__main__":
    # 클래스 생성
    crawler = DaumArticleCrawler()
    # 크롤링 페이지 범위 설정
    crawler.set_page_range(1,25)
    # 크롤링 시작
    crawler.start()