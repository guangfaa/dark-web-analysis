"""       seed-based dark web spider      """

from scrapy_redis.spiders import RedisSpider
import pymongo
import re
import warnings
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.linkextractors import LinkExtractor
import redis
from datetime import datetime


warnings.filterwarnings("ignore", category=ScrapyDeprecationWarning)
# 建立数据库
client = pymongo.MongoClient("mongodb://192.168.31.7:27017/")
# 建立数据库
db = client['2seed_surface_db']           
# 存储暗网页面
link = db["link"]          
# 存储暗网网站  
domain = db["domain"]         
# 存储明网地址 
clearweb = db["clearweb"]      
# 存储暗网超链接
links = db["links"]           
# 暗网到明网
dark_surface = db["dark_surface"]                
# 明网到暗网
surface_dark = db["surface_dark"]               

# def read_seed_nodes(file_path):
#     with open(file_path, 'r') as file:
#         seeds = file.readlines()
#     return [seed.strip() for seed in seeds]

# for s in read_seed_nodes("/public/home/lizhihao/experiment/seed_based/seed_based/seed.txt"):
#     links.insert_one({"url_":"NULL","url":s})
#     domain.insert_one({"url":s,"times":1})
#     link.insert_one({"url":s,"status":0,"value":0})
# 设置唯一索引
links.create_index([("url_", 1), ("url", 1)], unique=True)            
link.create_index([("url", 1)], unique=True)
clearweb.create_index([("url", 1)], unique=True)
dark_surface.create_index([("dark", 1), ("surface", 1)], unique=True)  
surface_dark.create_index([("surface", 1), ("dark", 1)], unique=True)  




# 将spider类继承改为RedisCrawlSpider
class LizhiSpider(RedisSpider):    
    name = "seed-ss"
    redis_key = 'seed-ss:start_urls'  
    r = redis.Redis(host='192.168.31.7', port=6379)
    start_time = datetime.now()
    print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 插入 URL 到 Start URLs 集合
    # r.rpush('lizhi:start_urls', 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address/')
    # for s in read_seed_nodes("/public/home/lizhihao/experiment/seed_based/seed_based/seed.txt"):
        # r.rpush('seed-ss:start_urls', s)
    
    base2 = "https://cn.bing.com/search?q="
    
    def remove_right_part(self,string):
        # 去掉最后一个/
        if string[-1] == "/":    
            a = string.rfind("/")
            string = string[:a]
        if '?' in string:
            string = string.split('?')[0]
        if '#' in string:
            string = string.split('#')[0]
        return string
    
    def add_url(self, url, response):
        try:
            self.server.rpush(self.redis_key, url) 
            self.r.rpush('spider3-ss:start_urls', self.base2+"\""+str(url)+"\""+"&first=1")
        except:
            pass

        try:
            link.insert_one({"url":url,"status":0,"value":0})   
        except:
            pass

    def parse(self, response):
        if response.status == 200:
            pattern = r'https?://\S+'
            Link = LinkExtractor(allow=pattern)
            iframe_links = response.xpath('//iframe/@src').getall()
            # 使用LinkExtractor提取出页面中的链接
            linkss = Link.extract_links(response)       
            # print(self.remove_right_part(response.request.url))
            u = { "url": response.request.meta["originalurl"] }
            newvalues = { "$set": { "status":True,"value":True} }
            # 更新此次访问的URL的status和value
            x = link.update_one(u, newvalues)     
            link_all = []
            if linkss:
                for link_one in linkss:
                    link_all.append(link_one.url)
            if iframe_links:
                link_all.extend(iframe_links)

            if link_all:
                for url in link_all:
                    url = self.remove_right_part(url)
                    
                    index = url.find('.onion')
                    # 明网地址
                    if index == -1:   
                        try:
                            print(url)
                            dark_surface.insert_one({"dark":response.request.meta["originalurl"],"surface":url})
                            clearweb.insert_one({"url":url, "status":False})
                            # 插入到clearweb clawer的redis
                            self.r.rpush('clearweb-ss:start_urls', url)
                            continue #新加的        
                        except:
                            continue
                    ex = url[:index]
                    if len(ex) < 56:
                        # 失效暗网地址
                        continue                 
                    if url[-1] == "/":    
                        # 去掉最后一个/
                        a = url.rfind("/")
                        url = url[:a]
                    try:
                        links.insert_one({"url_":response.request.meta["originalurl"],"url":url})
                        print ("[++]"+url)
                    except:
                        continue

                    if ex.count(".") >= 1:
                        # 主域
                        match1 = re.search(r"(https?://).*", url) 
                        extracted1 = match1.group(1)   
                        match = re.search(r"(.{56}\.onion)", url)         
                        extracted2 = match.group(1)     #超链接直插入一个 
                                                        #线程64  
                                                        #重定向
                        
                        # 获取主域名extracted
                        extracted = extracted1 + extracted2     
                        # 尝试插入主域名
                        self.add_url(extracted, response)     
                    for i in range(url.count('/') - 1):
                        url_now = '/'.join(url.split('/')[:i+3])   
                        self.add_url(url_now, response)
        else:
            pass