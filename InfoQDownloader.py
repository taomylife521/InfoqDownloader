import requests
import json
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import os
from requestium import Session, Keys
import time
import csv


from InfoQBrowserProxy import InfoQBrowserProxy

baseUrl="https://www.infoq.cn"
size=12
videoListUrl = baseUrl+"/public/v1/article/getVideoList"
videoDetailUrl=baseUrl+"/public/v1/article/getDetail"

# webdriver驱动地址根据实际修改
s = Session(webdriver_path='D:\soft\chromedriver_win32\chromedriver.exe',
            browser='chrome'  # ,
            )  # webdriver_options={'arguments': ['headless']}

# 创建一个requests session对象
session = requests.Session()
def ExtractVideoUrl(cookies):
    data = {'size' : '12'}
    #headers = {'content-type': 'application/json' }
    #session=requests.get(baseUrl)
   # result = requests.post(url=videoListUrl,data=data,headers=headers)
    response = session.post('https://www.infoq.cn/public/v1/article/getVideoList',cookies=cookies, data=data)
    videoJsonList=response.json()
    for inx,videoItem in enumerate(videoJsonList["data"]):
        print(str(inx)+":"+videoItem["article_title"] +",uuid:"+videoItem["uuid"]+",score:"+str(videoItem["score"]))

def GetVideoDetail():
    data = {'uuid': '8g55QaWlyHh5KlViTGgu'}
    detailResult=session.post(videoDetailUrl,data=data)
    print(detailResult.json())

def LoginInfoq():
    driver = webdriver.Chrome()
    if not os.path.exists("cookies.txt"):
        driver.get("https://account.geekbang.org/infoq/signin")
        time.sleep(5)

        account = driver.find_element_by_name('cellphone')
        password = driver.find_element_by_name('password')
        submit = driver.find_element_by_class_name('_3onsJjulw_ZjgvJO5gfULb_0')

        account.clear()
        password.clear()
        account.send_keys('13716910787')
        password.send_keys('soulcoder@')

        submit.click()
        time.sleep(5)

    with open("cookies.txt", "r") as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            # cookie.pop('domain')  # 如果报domain无效的错误
            driver.add_cookie(cookie)
    # cookie和前面一样的方式获取和保存

    driver.get('https://www.infoq.cn/video/list');
    cookies = driver.get_cookies()
    with open("cookies.txt", "w") as fp:
        json.dump(cookies, fp)
    # 把cookies设置到session中
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    ExtractVideoUrl(cookies)
    print(cookies)
    driver.close()


# 将cookie信息添加进requests组件中
def add_cookies(cookie, s):
    u"往session添加cookies"
    s.cookies.clear()
    c = requests.cookies.RequestsCookieJar()
    for i in cookie:  # 添加cookie到CookieJar
        # print(i)
        c.set(i["name"], i["value"])
    s.cookies.update(c)  # 更新session里的cookie
    print(s.cookies)
    return s


# 获取cookie信息
def getCookie():

    s.driver.get('https://account.geekbang.org/infoq/signin')
    time.sleep(1)
    account = s.driver.find_element_by_name('cellphone')
    password = s.driver.find_element_by_name('password')
    submit = s.driver.find_element_by_class_name('_3onsJjulw_ZjgvJO5gfULb_0')

    account.clear()
    password.clear()
    account.send_keys('13716910787')
    password.send_keys('soulcoder@')
    #s.driver.find_element_by_name('cellphone').clear()
    #s.driver.find_element_by_name('cellphone').send_keys('13716910787')
    #s.driver.find_element_by_name('password').clear()
    #s.driver.find_element_by_name('password').send_keys('soulcoder@')
    #s.driver.find_element_by_class_name('_3onsJjulw_ZjgvJO5gfULb_0').click()
    #time.sleep(3)
    #url = s.driver.current_url
    s.driver.get('https://www.infoq.cn/video/list');
    cookie = s.driver.get_cookies()
    print(cookie)
    jsonCookies = json.dumps(cookie)  # 转字符串

    return cookie

def ExtractUrl():
    session2 = requests.session()
    cookie = getCookie()
    # 为requests组件加入cookie信息
    add_cookies(cookie, session2)

    s.driver.get("https://www.infoq.cn/video/list")
    cookie = s.driver.get_cookies()
    add_cookies(cookie, session2)

    data = {'size': '12'}
    # 反爬破解机制，加入自己网页的user-agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','Referer': 'https://www.infoq.cn/video/list'}
    response = session2.post('https://www.infoq.cn/public/v1/article/getVideoList', headers=headers, data=data)
    videoJsonList = response.json()
    for inx, videoItem in enumerate(videoJsonList["data"]):
        print(str(inx) + ":" + videoItem["article_title"] + ",uuid:" + videoItem["uuid"] + ",score:" + str(
            videoItem["score"]))
    s.driver.get("https://www.infoq.cn/video/8g55QaWlyHh5KlViTGgu")
    cookie = s.driver.get_cookies()
    add_cookies(cookie, session2)
   #s.driver.close()

    detailheaders={
        #'Sec-Fetch-Mode': 'cors',
        #'Sec-Fetch-Site': 'same-origin',
        #'Origin': 'https://www.infoq.cn',
        #'Accept-Encoding': 'gzip, deflate, br',
        #'Accept-Language': 'zh-CN,zh;q=0.9',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        #'Content-Type': 'application/json',
        #'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.infoq.cn/video/8g55QaWlyHh5KlViTGgu'#,
        #'Connection': 'keep-alive',
        }
    detaildata = {'uuid': '8g55QaWlyHh5KlViTGgu'}
    detailResult = session2.post("https://www.infoq.cn/public/v1/article/getDetail",detailheaders=detailheaders, data=detaildata)
    print(detailResult.json())


if __name__ == '__main__':
    infoDownloader=InfoQBrowserProxy()
    #infoDownloader.Login('13716910787','soulcoder@')
    #infoDownloader.run(infoDownloader.load,"https://www.infoq.cn/video/list")
    infoDownloader.StartDownload("https://www.infoq.cn/video/list")

    #ExtractUrl()
    #LoginInfoq()
    #ExtractVideoUrl()
    #GetVideoDetail()
    # print(__name__)



