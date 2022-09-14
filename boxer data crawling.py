# 필요한 모듈을 임포트 합니다
from selenium import webdriver
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
time.sleep(3)

#현 페이지의 가장 상단에 위치한 선수부터 최하단의 선수의 페이지까지 이동합니다.
#한 페이지에 50명의 선수가 있습니다.
#페이지는 1페이지부터 458 페이지까지로 제한합니다.
for count in range(50):
    boxerN = int(count)
    boxerRanking = ('//*[@id="se' + str(boxerN) + '"]/td[2]/a')
    driver.find_element_by_xpath(boxerRanking).click()
    
