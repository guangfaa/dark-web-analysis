"""       seed-based dark web spider      """

from scrapy_redis.spiders import RedisSpider
import pymongo
import re
import warnings
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.linkextractors import LinkExtractor
import redis
warnings.filterwarnings("ignore", category=ScrapyDeprecationWarning)


#建立数据库
client = pymongo.MongoClient("mongodb://192.168.31.7:27017/")
db = client['004db']           #建立数据库
links = db["links"]            #存储超链接
domain = db["domain"]          #存储域名
clearweb = db["clearweb"]      #存储明网地址
link = db["link"]              #存储url
#links.insert_one({"url_":"NULL","url":"http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address","content":"","status":True,"value":True})
links.insert_one({"url_":"NULL","url":"http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address","status":False,"value":True})
domain.insert_one({"url":'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address',"times":1})
links.create_index([("url_)", 1), ("url", 1)], unique=True)            #设置唯一索引
link.create_index([("url", 1)], unique=True)
clearweb.create_index([("url", 1)], unique=True)

class LizhiSpider(RedisSpider):    #将spider类继承改为RedisCrawlSpider
    name = "lizhi"
    redis_key = 'lizhi:start_urls'   #lpush一个地址
    r = redis.Redis(host='192.168.31.7', port=6379)

    # 插入 URL 到 Start URLs 集合
    #r.rpush('lizhi:start_urls', 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address/')
    r.rpush('lizhi:start_urls', 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address')
    

    
    def remove_right_part(self,string):
        if '?' in string:
            string = string.split('?')[0]
        if '#' in string:
            string = string.split('#')[0]
        return string
    
    def add_url(self, url, response):
        try:
            links.insert_one({"url_":response.request.url,"url":url , "status":False,"value":True})
            print ("[++]"+url)
            self.server.rpush(self.redis_key, url) 
        except:
            pass

        try:
            link.insert_one({"url":url})   #把link的url设置为唯一索引
            #计数，新建一个mongodb
            URL = url.split('.onion')[0]
            result = domain.find({"url": URL})
            #如果之前没有，插入
            if len(list(result)) > 0:
                result = domain.update_one(
                {"url": URL},
                {"$inc": {"times": 1}}
            )
            else:
                domain.insert_one({"url":URL,"times":1})
            
            #如果有，次数加一
        except:
            pass



    def parse(self, response):
        pattern = r'https?://\S+'
        link = LinkExtractor(allow=pattern)
        linkss = link.extract_links(response)       #使用LinkExtractor提取出页面中的链接

      
        u = { "url": response.request.url }
        newvalues = { "$set": { "status":True,"value":True} }
        x = links.update_one(u, newvalues)              #更新此次访问的URL的status和value

        if linkss:
            for link_one in linkss:
               
                url = link_one.url
                url = self.remove_right_part(url)

                index = url.find('.onion')
                if index == -1:   #明网地址
                    try:
                        
                        links.insert_one({"url_":response.request.url,"url":url , "status":False,"value":True})
                        clearweb.insert_one({"url":url, "status":False})
                        self.r.rpush('clearweb:start_urls', url)        #插入到clearweb clawer的redis
                    except:
                        pass
                    continue
                ex = url[:index]
                if len(ex)<56:
                    continue                 #失效暗网地址
                
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


      