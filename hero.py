# 첫번째 블럭
# 필요한 모듈을 임포트 합니다
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import warnings  # 경고를 무시합니다.

warnings.filterwarnings('ignore')

page_num = input('몇 페이지부터 시작할까요? : ')
end_page = input('몇 페이지까지 크롤링할까요? : ')

# 결과를 저장할 데이터프레임
df_player_info = pd.DataFrame()
df_match_history = pd.DataFrame()

# 현재 설치되어있는 Chrome 버전과 동일한 Chromedriver을 다운받습니다
driver = webdriver.Chrome('C:/Users/jeong/PycharmProjects/pythonProject/chromedriver.exe')
driver.implicitly_wait(5)  # 로딩이 다 다음 페이지로 넘어갑니다
driver.get("https://boxrec.com/en/login?error=limit")

# 로그인 합니다
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys('bigdataboxing@ruu.kr')
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('Bigdata12')
driver.find_element(By.XPATH, '//*[@id="pageOuter"]/div/div[2]/form/div[4]/button').click()

# 월드 랭킹으로 이동합니다
timesFifty = (int(page_num) - 1) * 50  # 50페이지씩 이동하는 변수
pageOne = str('https://boxrec.com/en/ratings?sex=M&offset=' + str(timesFifty))
driver.get(pageOne)

# df = pd.DataFrame(columns=['name','division', 'rating', 'bouts', 'rounds', 'KOs', 'career', 'debut', 'vada', 'titles', 'ID#', 'birth name', 'sex', 'alias', 'age', 'nationality', 'stance', 'height', 'reach', 'residence', 'birth place'])

currentURL = str(driver.current_url)
captcha = str('https://boxrec.com/recaptcha')
try:
    # 페이지는 1페이지부터 150 페이지까지로 제한합니다. (7450)
    while timesFifty <= (int(end_page) - 1) * 50 and currentURL != captcha:
        # 현 페이지의 가장 상단에 위치한 선수부터 최하단의 선수의 페이지까지 이동합니다.
        # 한 페이지에 50명의 선수가 있습니다. (50)
        for count in range(50):
            if currentURL != captcha:
                dict_player_info = {}  # 선수 데이터가 들어가는 공 리스트

                boxerN = int(count)
                boxerRanking = str('// *[ @ id = "se' + str(boxerN) + '"] / td[2] / a')
                driver.find_element(By.XPATH, boxerRanking).click()

                if currentURL != captcha:

                    ### 현 페이지 복서의 데이터를 dict 형태로 저장합니다.
                    # 저장할 데이터: 이름 / ID / division / bouts / rounds / KOs / career / titles / age / nationality / stance / height / reach / residence / birth / place
                    # name은 모든 선수들의 페이지에서 동일하기 때문에 별도로 뽑아서 dict에 저장

                    name = driver.find_element(By.XPATH,
                                               '//*[@id="pageOuter"]/div/div[4]/div[2]/table/tbody/tr[1]/td/h1')
                    dict_player_info['name'] = name.text

                    # 선수들 페이지를 보면 왼쪽, 오른쪽 정보로 나뉘어져 있는걸 볼 수 있는데, 이는 div[{i}]로 구분할 수 있음. -> 왼쪽 테이블 div[3], 오른쪽 테이블 div[4]
                    # 선수들 정보를 보면 division heavy 처럼 Label Value 의 형식으로 이루어져 있는걸 볼 수 있음 -> 이를 Label, value로 구분지어서 dict의 key:value로 받아옴
                    # 선수들 정보들을 구분짓는 기준은 tr[{j}]로 확인가능. 따라서 for문으로 1~11 (1등 선수의 최대 번호가 11번에서 끝남) 까지 반복문을 돌림
                    # 선수들마다 정보의 개수 (= Dict의 길이)가 다르기 때문에 try, except 구문으로 길이가 같지 않아도 dict에 저장할 수 있도록 맞춰줌
                    # e.g) 1등 선수는 tr이 1`~11까지 존재, 500등 선수는 tr이 1~9번까지 존재
                    # DataFrame은 Column명과 Dict의 Key값을 기준으로 동일하면 해당 value를 채워넣는 식으로 생성 -> Dict의 길이만 다르지 Key의 명칭들은 다 같기 때문에

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

                    #                 print(dict_player_info) # dict_player_info 확인차 한번 출력
                    df_player_info = df_player_info.append(dict_player_info,
                                                           ignore_index=True)  # 데이터프레임에 dict_player_info 추가

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
                        #                     print(dict_match_history) # 확인용
                        except:
                            continue

                    driver.back()

                else:  # 캡챠가 나왔을 때 바로 전 페이지 URL / 페이지 # / 선수 # / 선수 이름을 프린트합니다
                    print('프로그램이 Google captcha에 의해 종료되었습니다.')
                    print('종료된 페이지:' + str((timesFifty // 50) + 1))
                    print(df_player_info.tail())
                    print(df_match_history.tail())
                    df_player_info.to_csv('player_info1.csv', encoding='utf-8', index=False)
                    df_match_history.to_csv('match_history1.csv', encoding='utf-8', index=False)


            else:  # 캡챠가 나왔을 때 바로 전 페이지 URL / 페이지 # / 선수 # / 선수 이름을 프린트합니다
                print('프로그램이 Google captcha에 의해 종료되었습니다.')
                print('종료된 페이지:' + str((timesFifty // 50) + 1))
                print(df_player_info.tail())
                print(df_match_history.tail())
                df_player_info.to_csv('player_info1.csv', encoding='utf-8', index=False)
                df_match_history.to_csv('match_history1.csv', encoding='utf-8', index=False)

                # 다음 페이지로 이동합니다.
        timesFifty += 50
        world_ranking_page = str('https://boxrec.com/en/ratings?sex=M&offset=' + str(timesFifty))
        driver.get(world_ranking_page)

    else:  # 캡챠가 나왔을 때 바로 전 페이지 URL / 페이지 # / 선수 # / 선수 이름을 프린트합니다
        print('프로그램이 Google captcha에 의해 종료되었습니다.')
        print('종료된 페이지:' + str((timesFifty // 50) + 1))
        print(df_player_info.tail())
        print(df_match_history.tail())
        df_player_info.to_csv('player_info1.csv', encoding='utf-8', index=False)
        df_match_history.to_csv('match_history1.csv', encoding='utf-8', index=False)

    print("드디어 완료")

except Exception as e:
    print(df_player_info.tail())
    print(df_match_history.tail())
    print("비정상적인 종료")
    print('오류종류 : {}'.format(e), '\n')
    print('종료된 페이지:' + str((timesFifty // 50) + 1))
    print('다시시작해야 할 index : {}'.format(count))
    df_player_info.to_csv('player_info1.csv', encoding='utf-8', index=False)
    df_match_history.to_csv('match_history1.csv', encoding='utf-8', index=False)
