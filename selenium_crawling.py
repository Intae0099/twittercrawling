from selenium import webdriver
import time

#url 설정
url = 'https://twitter.com/elonmusk'
#크롬 드라이버 사용
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
time.sleep(3)

result = []

#for문의 숫자는 크롤링할 게시글 수 설정
for i in range(4):

    try:
        twitter = driver.find_element_by_xpath(
                f'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div/div[{i}]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span')
        result.append(twitter.text)
    except:
        pass

#로딩시간 기다려주기
time.sleep(3)

textresult = []

for p in result:
        textresult.append(p)

#출력
print(textresult)

"""
트윗별로 추출
print(textresult[1])
print("--------------")
strch = textresult[1].split()

print(strch)
"""
driver.close()
