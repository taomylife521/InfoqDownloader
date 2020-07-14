import requests
import json
from bs4 import BeautifulSoup

baseUrl="https://www.infoq.cn"
size=12
videoListUrl = baseUrl+"/public/v1/article/getVideoList"
videoDetailUrl=baseUrl+"/public/v1/article/getDetail"
def ExtractVideoUrl():
    data = {'size' : '12'}
    headers = {'content-type': 'application/json' }
    session=requests.get(baseUrl)
    result = session.post(url=videoListUrl,data=data,headers=headers)
    print(result)

if __name__ == '__main__':
    ExtractVideoUrl()
    # print(__name__)



