# 필요한 모듈을 임포트 합니다
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import warnings # 경고를 무시합니다.
import pandas as pd
from selenium.webdriver.common.by import By
warnings.filterwarnings('ignore')

#현재 설치되어있는 Chrome 버전과 동일한 Chromedriver을 다운받습니다
driver = webdriver.Chrome('C:/Users/jeong/PycharmProjects/pythonProject/chromedriver.exe')
driver.implicitly_wait(5) #로딩이 다 다음 페이지로 넘어갑니다
driver.get("https://boxrec.com/en/login?error=limit")

#로그인 합니다
driver.find_element_by_xpath('//*[@id="username"]').send_keys('bigdataboxing@ruu.kr')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('Bigdata12')
driver.find_element_by_xpath('//*[@id="pageOuter"]/div/div[2]/form/div[4]/button').click()

#월드 랭킹으로 이동합니다
timesFifty = int(0) #50페이지씩 이동하는 변수
pageOne = str('https://boxrec.com/en/ratings?sex=M&offset=' + str(timesFifty))
driver.get(pageOne)

df = pd.DataFrame(columns=['name','division', 'rating', 'bouts', 'rounds', 'KOs', 'career', 'debut', 'vada', 'titles', 'ID#', 'birth name', 'sex', 'alias', 'age', 'nationality', 'stance', 'height', 'reach', 'residence', 'birth place'])

currentURL = str(driver.current_url)
captcha = str('https://boxrec.com/recaptcha')
try:
    #페이지는 1페이지부터 150 페이지까지로 제한합니다. (7450)
    while timesFifty <= int(7450) and currentURL != captcha:
        # 현 페이지의 가장 상단에 위치한 선수부터 최하단의 선수의 페이지까지 이동합니다.
        # 한 페이지에 50명의 선수가 있습니다. (50)
        for count in range(50):
            if currentURL != captcha:
                dict_player_info = {}  # 선수 데이터가 들어가는 공 리스트

                boxerN = int(count)
                boxerRanking = str('// *[ @ id = "se' + str(boxerN) + '"] / td[2] / a')
                driver.find_element_by_xpath(boxerRanking).click()
                if currentURL != captcha:

                    ### 현 페이지 복서의 데이터를 dict 형태로 저장합니다.
                    # 저장할 데이터: 이름 / ID / division / bouts / rounds / KOs / career / titles / age / nationality / stance / height / reach / residence / birth / place
                    # name은 모든 선수들의 페이지에서 동일하기 때문에 별도로 뽑아서 dict에 저장

                    name = driver.find_element(By.XPATH, '//*[@id="pageOuter"]/div/div[4]/div[2]/table/tbody/tr[1]/td/h1')
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

                    print(dict_player_info)
                    df = df.append(dict_player_info, ignore_index=True)
                    driver.back()

                else:  # 캡챠가 나왔을 때 바로 전 페이지 URL / 페이지 # / 선수 # / 선수 이름을 프린트합니다
                    print('프로그램이 Google captcha에 의해 종료되었습니다.')
                    print('종료된 페이지:' + str((timesFifty // 50) + 1))
                print(df)
            else:  # 캡챠가 나왔을 때 바로 전 페이지 URL / 페이지 # / 선수 # / 선수 이름을 프린트합니다
                print('프로그램이 Google captcha에 의해 종료되었습니다.')
                print('종료된 페이지:' + str((timesFifty // 50) + 1))
            print(df)
        # 다음 페이지로 이동합니다.
        timesFifty += 50
        world_ranking_page = str('https://boxrec.com/en/ratings?sex=M&offset=' + str(timesFifty))
        driver.get(world_ranking_page)

    else: # 캡챠가 나왔을 때 바로 전 페이지 URL / 페이지 # / 선수 # / 선수 이름을 프린트합니다
        print('프로그램이 Google captcha에 의해 종료되었습니다.')
        print('종료된 페이지:' + str((timesFifty // 50) + 1))
    df.to_csv('boxing_Test.csv', encoding='utf-8', index=False)
    print("완료")
except:
    print(df)
    df.to_csv('boxing_Test.csv', encoding='utf-8', index=False)
    print("비정상적인 종료")
    print('종료된 페이지:' + str((timesFifty // 50) + 1))
