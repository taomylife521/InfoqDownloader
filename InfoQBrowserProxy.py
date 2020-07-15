from BrowserProxyFramework import BrowserProxyFramework
import json
import time


class InfoQBrowserProxy(BrowserProxyFramework):

    #def __init__(self):
       # Login(self)

    def process_request(self, request, response):
        print(request)

    def process_response(self, response, request):
        if '/public/v1/article/getVideoList' in request['url']:
            contents=response['content']['text']
            contentList = json.loads(contents)
            if contentList['code'] != 0:
                return
            for item in contentList['data']:
                print('uuid:'+item['uuid']+',article_title:'+item['article_title']+",duration:"+item["duration"])
                self.run(self.load, "https://www.infoq.cn/video/"+item['uuid'])
        if 'public/v1/article/getDetail' in request['url']:
            contentDetail = response['content']['text']
            detail = json.loads(contentDetail)
            print('uuid:'+item['data']['uuid']+',article_title:'+item['data']['article_title'])#+",definition:"+item['data']["definition"]
            #print("捕获到:"+str(response['content']['text']))

    def load(self, url):
        self.browser.get(url)

    def loadList(self, url):
        self.browser.get(url)
        # temp_height=0
        # while True:
        #     # 循环将滚动条下拉
        #     self.browser.execute_script("window.scrollBy(0,500)")
        #     # sleep一下让滚动条反应一下
        #     time.sleep(5)
        #     # 获取当前滚动条距离顶部的距离
        #     check_height = self.browser.execute_script(
        #         "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        #     # 如果两者相等说明到底了
        #     if check_height == temp_height:
        #         break
        #     temp_height = check_height
        #     print(check_height)
        #
        # moretext = self.browser.find_element_by_class_name('more-button').text
        # while '没有更多了' not in moretext:
        #     self.browser.find_element_by_class_name('more-button').click()
        #     # sleep一下让滚动条反应一下
        #     time.sleep(5)
        #     moretext = self.browser.find_element_by_class_name('more-button').text
        time.sleep(3)

    def Login(self,username,pwd):
        self.browser.get('https://account.geekbang.org/infoq/signin')
        #time.sleep(1)
        account = self.browser.find_element_by_name('cellphone')
        password = self.browser.find_element_by_name('password')
        submit = self.browser.find_element_by_class_name('_3onsJjulw_ZjgvJO5gfULb_0')

        account.clear()
        password.clear()
        account.send_keys(username)
        password.send_keys(pwd)

        #self.browser.get('https://www.infoq.cn/video/list')
        #cookie = self.browser.get_cookies()
        #print(cookie)

    def StartDownload(self,url):
        self.run(self.loadList, "https://www.infoq.cn/video/list")



