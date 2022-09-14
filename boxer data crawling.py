# 필요한 모듈을 임포트 합니다
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#현재 설치되어있는 Chrome 버전과 동일한 Chromedriver을 다운받습니다
driver = webdriver.Chrome('./chromedriver.exe')
driver.get("https://boxrec.com/en/login?error=limit")
time.sleep(3)

#로그인 합니다
driver.find_element_by_xpath('//*[@id="username"]').send_keys('bigdataboxing@ruu.kr')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('Bigdata12')
driver.find_element_by_xpath('//*[@id="pageOuter"]/div/div[2]/form/div[4]/button').click()
time.sleep(4)

#월드 랭킹으로 이동합니다
driver.get("https://boxrec.com/en/ratings?sex=M")
time.sleep(4)

#세계 랭킹 페이지를 이동합니다.
#페이지는 1페이지부터 200 페이지까지로 제한합니다.
for page in range(2,4):

    # 현 페이지의 가장 상단에 위치한 선수부터 최하단의 선수의 페이지까지 이동합니다.
    # 한 페이지에 50명의 선수가 있습니다.
    for count in range(2):
        boxerN = int(count)
        boxerRanking = ('//*[@id="se' + str(boxerN) + '"]/td[2]/a')
        driver.find_element_by_xpath(boxerRanking).click()

        #추가 필요: 현 페이지 복서의 데이터를 csv 형태로 저장합니다.
        #저장할 데이터:

        #이전 페이지로 이동합니다.
        time.sleep(1)
        driver.back()

    #다음 페이지로 이동합니다.
    driver.find_element_by_xpath('// *[ @ id = "pageOuter"] / div / div[9] / div[1] / input').send_keys(page)
    driver.find_element_by_xpath('// *[ @ id = "pageOuter"] / div / div[9] / div[1] / input').send_keys(Keys.ENTER)
