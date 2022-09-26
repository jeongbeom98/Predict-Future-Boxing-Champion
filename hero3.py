# 두번째 블럭
# 첫번째 블럭에서 가져온 csv파일에다가 세번째 블럭에서 가져오는 선수들의 정보, 전적을 append 시켜주는 함수
# dict의 key와 csv파일의 컬럼을 자동으로 매칭시킴

import csv
from csv import writer

def appendNewData(csv_file, dict_data):
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        append_writer = csv.DictWriter(f, fieldnames = dict_data.keys())
        append_writer.writerow(dict_data)

# 세번째 블럭
# 반복해서 돌려야 하는 코드

# 필요한 모듈을 임포트 합니다
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import warnings  # 경고를 무시합니다.

warnings.filterwarnings('ignore')

page_num = input('몇 페이지에서 시작할까요? : ')
index_num = input('몇번째 선수부터 시작할까요? : ')
end_page = input('몇 페이지까지 크롤링할까요? : ')

#결과를 저장할 데이터프레임
df_player_info = pd.DataFrame()
df_match_history = pd.DataFrame()

# 현재 설치되어있는 Chrome 버전과 동일한 Chromedriver을 다운받습니다
driver = webdriver.Chrome('C:/Users/jeong/PycharmProjects/pythonProject/chromedriver.exe')
driver.implicitly_wait(7)  # 로딩이 다 다음 페이지로 넘어갑니다
driver.get("https://boxrec.com/en/login?error=limit")

# 로그인 합니다
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys('bigdataboxing@ruu.kr')
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('Bigdata12')
driver.find_element(By.XPATH, '//*[@id="pageOuter"]/div/div[2]/form/div[4]/button').click()

# 월드 랭킹으로 이동합니다
timesFifty = (int(page_num) - 1) * 50  # 50페이지씩 이동하는 변수
pageOne = str('https://boxrec.com/en/ratings?sex=M&offset=' + str(timesFifty))
driver.get(pageOne)
currentURL = str(driver.current_url)
captcha = str('https://boxrec.com/recaptcha')

try:
    # 페이지는 1페이지부터 150 페이지까지로 제한합니다. (7450)
    while timesFifty <= (int(end_page) - 1) * 50 and currentURL != captcha:
        # 현 페이지의 가장 상단에 위치한 선수부터 최하단의 선수의 페이지까지 이동합니다.
        # 한 페이지에 50명의 선수가 있습니다. (50)
        for count in range(int(index_num), 50):
            if currentURL != captcha:
                dict_player_info = {}  # 선수 데이터가 들어가는 공 리스트

                boxerN = int(count)
                boxerRanking = str('// *[ @ id = "se' + str(boxerN) + '"] / td[2] / a')
                driver.find_element(By.XPATH, boxerRanking).click()

                if currentURL != captcha:

                    name = driver.find_element(By.XPATH,
                                               '//*[@id="pageOuter"]/div/div[4]/div[2]/table/tbody/tr[1]/td/h1')
                    dict_player_info['name'] = name.text

                    for i in range(3, 5):
                        for j in range(1, 12):
                            try:
                                Label = driver.find_element(By.XPATH,
                                                            f'//*[@id="pageOuter"]/div/div[4]/div[2]/table/tbody/tr[2]/td[2]/div[{i}]/table/tbody/tr[{j}]/td[1]/b')
                                value = driver.find_element(By.XPATH,
                                                            f'//*[@id="pageOuter"]/div/div[4]/div[2]/table/tbody/tr[2]/td[2]/div[{i}]/table/tbody/tr[{j}]/td[2]')
                                dict_player_info[Label.text] = value.text
                                rating = driver.find_element(By.XPATH,
                                                             '//*[@id="pageOuter"]/div/div[4]/div[2]/table/tbody/tr[2]/td[2]/div[3]/table/tbody/tr[3]/td[2]/a')
                                dict_player_info['rating'] = rating.text
                            except Exception as e:
                                continue

                    # 데이터 전처리

                    # rating : rating에서 #을 제거
                    if 'rating' in dict_player_info.keys():
                        dict_player_info['rating'] = dict_player_info['rating'].lstrip('#')
                    else:
                        pass
                    # career는 경력으로 년수로 변환
                    if 'career' in dict_player_info.keys():
                        dict_player_info['career'] = int(dict_player_info['career'].split('-')[1]) - int(
                            dict_player_info['career'].split('-')[0])
                    else:
                        pass
                    # titles : 수상경력이 있는 선수들은 개수로 변환
                    if 'titles' in dict_player_info.keys():
                        dict_player_info['titles'] = len(dict_player_info['titles'].split('\n'))
                    else:
                        pass
                    # height, reach 는 cm인 값들만 뽑아옴
                    if 'height' in dict_player_info.keys():
                        dict_player_info['height'] = dict_player_info['height'].split('/')[1].strip()
                    else:
                        pass
                    if 'reach' in dict_player_info.keys():
                        dict_player_info['reach'] = dict_player_info['reach'].split('/')[1].strip()
                    else:
                        pass

                    df_player_info = df_player_info.append(dict_player_info,
                                                           ignore_index=True)  # 데이터프레임에 dict_player_info 추가

                    # dict_player_info의 값을 player_info.csv파일에 추가함

                    appendNewData('player_info1.csv', dict_player_info)

                    # 전적 데이터 크롤링

                    pattern = re.compile('\d{7}|\d{6}')  # 정규식을 활용해서 id값이 숫자로만 이뤄진 6~7자리 인 값들만 가져옴

                    html = driver.page_source  # selenium에서 html페이지를 가져오는 메소드
                    soup = BeautifulSoup(html, 'lxml')
                    history = soup.select(".dataTable > tbody")  # .dataTable => dataTable 클래스에서
                    # >tbody => 태그가 tbody인 값들만 가져옴

                    for i in range(len(history)):
                        id_num = pattern.findall(
                            history[i].attrs['id'])  # attrs 메소드를 사용해 bs4.element_result 타입인 history에서 id 값들을 가져오고
                        # 그 값들중 주어진 정규식 표현과 일치한 값들을 뽑아옴

                        # 날짜별로 구분된 id값들을 내가 원하는 정보의 XPATH에 format 형태로 대입하여 저장
                        # 아직 치워지지 않은 경기는 player_2가 없기때문에 오류 발생 일단 try,except구문으로 처리한 후 추후에 다시 고려
                        try:
                            date = driver.find_element(By.XPATH, '//*[@id={}]/td[2]/a'.format(*id_num))
                            player_1 = driver.find_element(By.XPATH,
                                                           '//*[@id="pageOuter"]/div/div[4]/div[2]/table/tbody/tr[1]/td/h1')
                            player_2 = driver.find_element(By.XPATH, '//*[@id={}]/td[6]/a'.format(*id_num))
                            match_result = driver.find_element(By.XPATH, '//*[@id={}]/td[10]/div'.format(*id_num))
                            rounds = driver.find_element(By.XPATH, '//*[@id={}]/td[11]'.format(*id_num))

                            # 데이터프레임을 더 간편하게 만들기 위해서 dict형식으로 저장
                            dict_match_history = {'date': date.text, 'player_1': player_1.text,
                                                  'player_2': player_2.text, 'match_result': match_result.text,
                                                  'match_rounds': rounds.text}

                            # 데이터프레임에 저장
                            df_match_history = df_match_history.append(dict_match_history, ignore_index=True)

                            # dict_match_history의 값을 match_history.csv파일에 추가함
                            appendNewData('match_history1.csv', dict_match_history)

                        except:
                            continue

                    driver.back()

                else:  # 캡챠가 나왔을 때 바로 전 페이지 URL / 페이지 # / 선수 # / 선수 이름을 프린트합니다
                    print('프로그램이 Google captcha에 의해 종료되었습니다.')
                    print('종료된 페이지:' + str((timesFifty // 50) + 1))
                    print(df_player_info.tail())
                    print(df_match_history.tail())


            else:  # 캡챠가 나왔을 때 바로 전 페이지 URL / 페이지 # / 선수 # / 선수 이름을 프린트합니다
                print('프로그램이 Google captcha에 의해 종료되었습니다.')
                print('종료된 페이지:' + str((timesFifty // 50) + 1))
                print(df_player_info.tail())
                print(df_match_history.tail())

        # 다음 페이지로 이동합니다.
        timesFifty += 50
        world_ranking_page = str('https://boxrec.com/en/ratings?sex=M&offset=' + str(timesFifty))
        driver.get(world_ranking_page)
        index_num = 0  # 새로운 페이지가 시작될때 index를 0으로 초기화

    else:  # 캡챠가 나왔을 때 바로 전 페이지 URL / 페이지 # / 선수 # / 선수 이름을 프린트합니다
        print('프로그램이 Google captcha에 의해 종료되었습니다.')
        print('종료된 페이지:' + str((timesFifty // 50) + 1))
        print(df_player_info.tail())
        print(df_match_history.tail())

    print("드디어 완료")

except Exception as e:
    print(df_player_info.tail())
    print(df_match_history.tail())
    print("비정상적인 종료")
    print('오류종류 : {}'.format(e), '\n')
    print('종료된 페이지:' + str((timesFifty // 50) + 1))
    print('다시시작해야 할 index : {}'.format(count))