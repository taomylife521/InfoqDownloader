from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from browsermobproxy import Server
import time
import json

class BrowserProxyFramework(object):

    def __init__(self):
        self.server = Server('browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat')
        self.server.start()
        self.proxy = self.server.create_proxy()
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
        self.browser = webdriver.Chrome(options=chrome_options)

    def process_request(self, request, response):
        pass

    def process_response(self, response, request):
        pass

    def loadallresponsecomplete(self, entrys):
        pass

    def run(self, func, *args):
        self.proxy.new_har(options={
            'captureContent': True,
            'captureHeaders': True
        })
        func(*args)
        result = self.proxy.har
        #print(result)
        for entry in result['log']['entries']:
            request = entry['request']
            response = entry['response']
            self.process_request(request, response)
            self.process_response(response, request)
        self.loadallresponsecomplete(result['log']['entries'])
    def __del__(self):
        self.proxy.close()
        self.browser.close()




if __name__ == '__main__':
    f = MovieFramework()
    for page in range(1, 5):
        url = f'https://dynamic2.scrape.center/page/{page}'
        f.run(f.load, url)