import scrapy
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider
import pymongo
import redis
import re
import warnings
from scrapy.exceptions import ScrapyDeprecationWarning
warnings.filterwarnings("ignore", category=ScrapyDeprecationWarning)

client = pymongo.MongoClient("mongodb://192.168.31.7:27017/")
db = client['001db']
links = db["links"]
#domain = db["domain"]

links.create_index([("url", 1)], unique=True)#设置URL为唯一索引，防止插入重复的URL



#class Spider2Spider(scrapy.Spider):
class Spider2Spider(RedisSpider):
    name = "spider2"

    redis_key = 'search_engine:start_urls'   #lpush一个地址
    r = redis.Redis(host='localhost', port=6379)
    
    current_page = 1      #起始页面
    list_num = 0          #起始列表位置
    #a="http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P=girl&[=8"
    engine_url = "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion"
    base1="http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P="
    base2="&[="
    
    kinds_list = ["market","financial","communication","service","wiki","social","adult","drug","game","money","bitcoin","man","leak","engine","vpn","e-mail","card","electronics","Betting","Escrow","Forums","book"]

    def remove_right_part(self,string):
        if '?' in string:
            string = string.split('?')[0]
        if '#' in string:
            string = string.split('#')[0]
        return string
    def add_url(self, url, response):
        try:
            links.insert_one({"url_":self.engine_url,"url":url, "content":"" , "status":False,"value":True})
            print ("[++][++]"+url)
            self.server.rpush(self.redis_key, url)
        except:
            pass

    def start_requests(self):
        for i in self.kinds_list:
            url = self.base1+i+self.base2+str(self.current_page)
            self.list_num+=1
            yield Request(url)


    def parse(self, response):
        
        pattern = r'https?://\S+'
        link = LinkExtractor(allow=pattern)
        linkss = link.extract_links(response)
        if linkss:
            for link_one in linkss:
                
                url = link_one.url
                url = self.remove_right_part(url)

                index = url.find('.onion')
                if index == -1:   #明网地址
                    try:
                        links.insert_one({"url_":self.engine_url,"url":url, "content":"" , "status":False,"value":True})
                    except:
                        pass
                    continue
                ex = url[:index]
                if len(ex)<56:
                    continue
                
                if url[-1] == "/":    #去掉最后一个/
                    a = url.rfind("/")
                    url = url[:a]
                if ex.count(".")>=1:
                    #主域
                    match1 = re.search(r"(https?://).*", url) 
                    extracted1 = match1.group(1)   
                    match = re.search(r"(.{56}\.onion)", url)         
                    extracted2 = match.group(1)
                    extracted = extracted1+extracted2     #获取主域名extracted
                    self.add_url(extracted, response)     #尝试插入主域名
                for i in range(url.count('/')-1):
                    url_now = '/'.join(url.split('/')[:i+3])   
                    self.add_url(url_now, response)
        if "&[=1" in response.request.url:
            match = re.search(r'Term frequencies:\s*\w+:\s*([\d,]+)', response)
            if match:
                number = int(match.group(1))
                page = 1
                for i in range(int(number/10)):
                    page +=1
                    new_url = response.request.url[:-1] + str(page)
                    self.server.rpush(self.redis_key, new_url)
            else:
                print("No match found.")


