import requests
import json
from bs4 import BeautifulSoup

baseUrl="https://www.infoq.cn"
size=12
videoListUrl = baseUrl+"/public/v1/article/getVideoList"
videoDetailUrl=baseUrl+"/public/v1/article/getDetail"
cookies = {
        'LF_ID': '1589160741648-6915890-8278982',
        '_ga': 'GA1.2.1494193241.1589160742',
        'TARGET': '5dbf4-bf48ab1-3e8ee7e-b305d5a',
        '_itt': '1',
        'GCID': 'e6e944d-0112ea2-4029236-f842d5b',
        'GRID': 'e6e944d-0112ea2-4029236-f842d5b',
        '_gid': 'GA1.2.215464015.1594624593',
        'Hm_lvt_094d2af1d9a57fd9249b3fa259428445': '1594432002,1594624593,1594710547,1594719272',
        '_gat': '1',
        'Hm_lpvt_094d2af1d9a57fd9249b3fa259428445': '1594721165',
        'SERVERID': '3431a294a18c59fc8f5805662e2bd51e^|1594721164^|1594719270',
    }

headers = {
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Origin': 'https://www.infoq.cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    #'Referer': 'https://www.infoq.cn/video/list',
    'Referer': 'https://www.infoq.cn/video/8g55QaWlyHh5KlViTGgu',
    'Connection': 'keep-alive',
}
def ExtractVideoUrl():
    data = {'size' : '12'}
    #headers = {'content-type': 'application/json' }
    #session=requests.get(baseUrl)
   # result = requests.post(url=videoListUrl,data=data,headers=headers)
    response = requests.post('https://www.infoq.cn/public/v1/article/getVideoList', headers=headers, cookies=cookies, data=data)
    videoJsonList=response.json()
    for inx,videoItem in enumerate(videoJsonList["data"]):
        print(str(inx)+":"+videoItem["article_title"] +",uuid:"+videoItem["uuid"]+",score:"+str(videoItem["score"]))

def GetVideoDetail():
    data = {'uuid': '8g55QaWlyHh5KlViTGgu'}
    detailResult=requests.post(videoDetailUrl,cookies=cookies,headers=headers,data=data)
    print(detailResult.json())

if __name__ == '__main__':
    #ExtractVideoUrl()
    GetVideoDetail()
    # print(__name__)



