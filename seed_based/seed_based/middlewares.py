# Define here the models for your spider middleware

from scrapy import signals

from stem.control import Controller
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from fake_useragent import UserAgent
import random
import time
from toripchanger import TorIpChanger
from scrapy import Request
import pymongo
import redis
import re

from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError


redis_key = 'seed-s:start_urls'   
r = redis.Redis(host='192.168.31.7', port=6379)

class ScrapyCrawlSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapyCrawlDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# A Tor IP will be reused only after 10 different IPs were used.
# ip_changer = TorIpChanger(reuse_threshold=10)


#更新tor链路，只是请求，没有强制换链路（new ip）
# def new_tor_identity():
#     time.sleep(random.uniform(0.5,1.5 ))
#     with Controller.from_port(port=9051) as controller:
#         controller.authenticate(password='1234')
#         controller.signal(Signal.NEWNYM)
#         time.sleep(5)


    
class ProxyMiddleware(HttpProxyMiddleware):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def remove_right_part(self,string):
        if '?' in string:
            string = string.split('?')[0]
        if '#' in string:
            string = string.split('#')[0]
        return string
    def process_response(self, request, response, spider):
        print("%s!!!!!!!%s!!!!!!!!!!status!!!!!!!!!%s!!!!!!!%s"%(response.status,response.status,response.status,response.status))
        
        url = request.meta["originalurl"]
        if response.status != 200:   # 处理在(!=200)中出现的状态码
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        
            print(request.meta["originalurl"])
            match = re.search(r'retry=(\d+)', request.meta["originalurl"])
            if match:
                retry_time = int(match.group(1))
            else:
                retry_time = 0
            retry_time = retry_time + 1
            max_retries = 2

            url = self.remove_right_part(url)
            if retry_time <= max_retries:
                print(f'Retrying {url} (retey {retry_time})')

                r.lpush('seed-s:start_urls',url+f'?retry={retry_time}')

            else:
                print("""
                    ~~~~~~~~~~~~~~%s~~~~~~%s~~~~~~~~~~~~~~
                    """%(response.status,response.status))
                url = request.meta["originalurl"]
                url = self.remove_right_part(url)
                client = pymongo.MongoClient("mongodb://192.168.31.7:27017/")
                db = client['seed_base_db']
                link = db["link"]
                u = { "url": url }
                diedvalues = { "$set": {"status":True,"value":False} }
                x = link.update_one(u, diedvalues)

        return response
    def process_exception(self,request,exception,spider):
        #捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            #在日志中打印异常类型
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Got exception: %s' % (exception))
            #随意封装一个response，返回给spider
            url = request.meta["originalurl"]
            client = pymongo.MongoClient("mongodb://192.168.31.7:27017/")
            db = client['seed_base_db']
            link = db["link"]
            u = { "url": url }
            diedvalues = { "$set": {"status":True,"value":False} }
            x = link.update_one(u, diedvalues)
        #打印出未捕获到的异常
        print('not contained exception: %s'%exception)


    def process_request(self, request, spider):
        # Set the Proxy
        request.meta['proxy'] = 'http://127.0.0.1:8118' 
        
        #UA反反爬
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random
        # new_tor_identity() # A new identity for each request
        time.sleep(random.uniform(1, 2))


