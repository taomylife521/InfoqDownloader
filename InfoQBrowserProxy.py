from BrowserProxyFramework import BrowserProxyFramework
import json
import time
import pandas as pd
from ffmpy3 import FFmpeg
import os

detailList=[]
 #
class InfoQBrowserProxy(BrowserProxyFramework):

    def __init__(self):
       self.videoListfileName = 'VideoList.xlsx'
       self.fileName = 'VideoUrl.xlsx'
       self.videoinfos = {"uuid": [], "article_title": [], "duration": [], "views": [], "ppt_url": [], "超清": [], "高清": [],
              "标清": []}
       self.videoList = {"uuid": [], "article_title": []}
       super(InfoQBrowserProxy, self).__init__()
    def loadallresponsecomplete(self,entrys):
        #self.videoinfos.to_excel(self.fileName)#加载所有请求完成，写入excel数据
        pass

    def process_request(self, request, response):
        print(request)

    def process_response(self, response, request):
        if '/public/v1/article/getVideoList' in request['url']:#加载视频列表
            contents=response['content']['text']
            contentList = json.loads(contents)
            if contentList['code'] != 0:
                return
            for item in contentList['data']:
                #print('uuid:'+item['uuid']+',article_title:'+item['article_title']+",duration:"+item["duration"])
                self.writeVideoList(item)
                #self.run(self.load, "https://www.infoq.cn/video/"+item['uuid'])

            #self.videoinfos = pd.DataFrame(data=self.videoinfos, columns=self.videoinfos.keys())
            #self.videoinfos.to_excel(self.fileName)
        if 'public/v1/article/getDetail' in request['url']:
            try:
                contentDetail = response['content']['text']
                detail = json.loads(contentDetail)
                if detail['code'] != 0:
                    return
                detailList.append(detail['data'])

                if type(detail['data']) is list:
                    for item in detail['data']:
                        self.writeVideoInfos(item)
                else:
                    self.writeVideoInfos(detail['data'])
                #print('uuid:'+detail['data']['uuid']+',article_title:'+detail['data']['article_title'])#+",definition:"+item['data']["definition"]
                #print("捕获到:"+str(response['content']['text']))
            except KeyError:
                print('KeyError')
            except TypeError:
                print('TypeError')

    def load(self, url):
        self.browser.get(url)
        time.sleep(5)

    def loadList(self, url):
        self.browser.get(url)
        temp_height=0
        print("Start Scrolling Loading")
        while True:
            # 循环将滚动条下拉
            self.browser.execute_script("window.scrollBy(0,100)")
            # sleep一下让滚动条反应一下
            time.sleep(1)
            # 获取当前滚动条距离顶部的距离
            check_height = self.browser.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            # 如果两者相等说明到底了
            if check_height == temp_height:
                break
            temp_height = check_height
            print(check_height)
        print("Scrolling Loading Complete Start Click More-Button")
        moretext = self.browser.find_element_by_class_name('more-button').text
        while '没有更多了' not in moretext:
            try:
                self.browser.find_element_by_class_name('more-button').click()
                # sleep一下让滚动条反应一下
                time.sleep(2)
                moretext = self.browser.find_element_by_class_name('more-button').text
            except Exception:
                 break

        videos=self.browser.find_elements_by_class_name('video-item')
        for videoItem in videos:
            e=videoItem.find_element_by_class_name('com-article-title')
            self.videoList['uuid'].append(e.get_attribute('href'))
            self.videoList['article_title'].append(e.text)




        self.videoList = pd.DataFrame(data=self.videoList, columns=self.videoList.keys())
        self.videoList.to_excel(self.videoListfileName)
        print("All Load Complete")
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
        submit.click()
        time.sleep(3)
        #self.browser.get('https://www.infoq.cn/video/list')
        #cookie = self.browser.get_cookies()
        #print(cookie)

    def writeVideoInfos(self,data):

        # if not os.path.exists(fileName):
        #     f = open(fileName, 'w')
        #     f.close()
        #videoinfos = pd.read_excel(u'VideoUrl.xlsx', keep_default_na=False)
        if 'definition' not in data.keys():
            return
        uuid = data['uuid'] if 'uuid' in data.keys() else ''
        article_title = data['article_title'] if 'article_title' in data.keys() else ''
        duration = data['duration'] if 'duration' in data.keys() else ''
        views = data['views'] if 'views' in data.keys() else ''
        ppt_url = data['ppt_url'] if 'ppt_url' in data.keys() else ''
        self.videoinfos['uuid'].append(uuid)
        self.videoinfos['article_title'].append(article_title)
        #videoinfos['article_sharetitle'].append(data['article_sharetitle'])
        self.videoinfos['duration'].append(duration)
        self.videoinfos['views'].append(views)
        self.videoinfos['ppt_url'].append(ppt_url)
        if 'definition' not in data.keys():
            self.videoinfos['超清'].append('')
            self.videoinfos['高清'].append('')
            self.videoinfos['标清'].append('')
        else:
            for item in data['definition']:
                if item['type'] in 'hd':
                    self.videoinfos['超清'].append(item['url'])
                # else:
                #     self.videoinfos['超清'].append('')
                if item['type'] in 'sd':
                    self.videoinfos['高清'].append(item['url'])
                # else:
                #     self.videoinfos['高清'].append('')
                if item['type'] in 'ld':
                    self.videoinfos['标清'].append(item['url'])
                # else:
                #     self.videoinfos['标清'].append('')
        #self.videoinfos = pd.DataFrame(data=self.videoinfos, columns=self.videoinfos.keys())
        #return self.videoinfos

        # with open('data.txt', 'a+') as f:
        #     f.write('\n'+json.dumps(data))

    def writeVideoList(self, data):

        # if not os.path.exists(fileName):
        #     f = open(fileName, 'w')
        #     f.close()
        # videoinfos = pd.read_excel(u'VideoUrl.xlsx', keep_default_na=False)

        uuid = data['uuid'] if 'uuid' in data.keys() else ''
        article_title = data['article_title'] if 'article_title' in data.keys() else ''
        self.videoList['uuid'].append(uuid)
        self.videoList['article_title'].append(article_title)

    def ffmpeg_download(self,inputs_path, outputs_path):
        try:
            '''
            :param inputs_path: 输入的文件传入字典格式{文件：操作}
            :param outputs_path: 输出的文件传入字典格式{文件：操作}
            :return:
            '''
            a = FFmpeg(
                inputs={inputs_path: None},
                outputs={outputs_path: '-c copy',
                         }
            )
            print(a.cmd)
            a.run()
        except Exception:
            pass
    def StartDownload(self,url):
        # 1.加载列表
        # self.run(self.loadList, "https://www.infoq.cn/video/list")
        # 2.加载详情，读取列表excel
        # df = pd.read_excel(self.videoListfileName)  # 现在Excel表格与py代码放在一个文件夹里
        # for item in df.values:
        #     self.run(self.load, item[1])
        # print(self.videoinfos)
        # self.videoinfos = pd.DataFrame(data=self.videoinfos, columns=self.videoinfos.keys())
        # self.videoinfos.to_excel(self.fileName)
        # 3.下载视频
        df = pd.read_excel(self.fileName)  # 现在Excel表格与py代码放在一个文件夹里
        for item in df.values:
            title=item[2]
            hd=item[6]
            if(hd == None):
                continue
            print(title + ":" + hd)
            outputpath= "./Video/" + title + ".mp4"
            outputpath =outputpath.replace(" ", "").replace("|", "#")
            if not os.path.exists(outputpath):
                self.ffmpeg_download(inputs_path=hd,outputs_path=outputpath)
            print(outputpath+" DownLoad Sucess")

            #self.run(self.load, item[1])





