import scrapy
import pymongo
from scrapy_redis.spiders import RedisSpider
import redis
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import ScrapyDeprecationWarning
import warnings
warnings.filterwarnings("ignore", category=ScrapyDeprecationWarning)
import re
client = pymongo.MongoClient("mongodb://192.168.31.7:27017/")
db = client['3our_spider_db']           
# 存储暗网页面
# 存储暗网页面
link = db["link"]          
# 存储暗网网站
domain = db["domain"]  
#mongo
all = db["all"]           

link.create_index([("url", 1)], unique=True)
all.create_index([("url1", 1), ("url2", 1)], unique=True)  

class ClearwebSpider(RedisSpider):
    name = "clearweb"
    redis_key = 'clearweb:start_urls'   #lpush一个地址
    r = redis.Redis(host='192.168.31.7', port=6379)
    base3 = "https://cn.bing.com/search?q="
    

    def remove_right_part(self,string):
        if '?' in string:
            string = string.split('?')[0]
        if '#' in string:
            string = string.split('#')[0]
        return string
    def find_and_process(self,domain2):
        # 查询字段 a 中与 b_value 相同的文档
        documents = list(domain.find({'a': domain2}))


        # 获取相应的 number 字段的值
        number_values = [doc['number'] for doc in documents]
        if number_values != []:
            number_values = number_values[0]  # 提取第一个数值
            print(number_values)
        else:
            number_values = -1


        if number_values > 20:
            print('找到的数量大于 20，返回 0，进行下一步处理。')
            return 0  # 返回 0 以进行下一步处理
        elif 0 < number_values <= 20:
            # 如果数量在 1 到 20 之间，更新计数
            domain.update_one({'a': domain2}, {'$inc': {'number': 1}})
            print(f'找到的 number 值：{number_values}，计数加 1。')
        else:
            # 如果没有找到相应的文档，则插入新文档
            domain.insert_one({'a': domain2, 'number': 1})
            print(f'没有找到相应的文档，已插入新文档：{{"a": "{domain2}", "number": 1}}。')


    def add_url(self, url, response):
        try:
            link.insert_one({"url":url})
            match = re.search(r"(.{56}\.onion)", url)
            domain2 = match.group(1)
            result = self.find_and_process(domain2)
            if result == 0:
                return
            else:
                self.server.rpush('Spider:start_urls', url) 
                self.r.rpush('spider3:start_urls', self.base2+"\""+str(url)+"\""+"&first=1")
        except:
            pass

    def parse(self, response):
        # u = { "url": response.request.meta["originalurl"] }
        # newvalues = { "$set": { "status":True} } 明网标记为有效
        # x = clearweb.update_one(u, newvalues)
        pattern = r'https?://\S+'
        link = LinkExtractor(allow=pattern)
        linkss = link.extract_links(response)
        
        if linkss:
                for link_one in linkss:
                    url = link_one.url
                    url = self.remove_right_part(url)
                    index = url.find('.onion')
                    if index == -1:   #明网地址
                        continue
                    ex = url[:index]
                    if len(ex)<56:
                        continue                 #失效暗网地址
                    if url[-1] == "/":    #去掉最后一个/
                        a = url.rfind("/")
                        url = url[:a]
                    try:
                        all.insert_one({"url1":response.request.meta["originalurl"],"type1":"surface","url2":url,"type2":"dark","edge":"hyperlink"})
                        print ("[++]"+url)
                    except:
                        continue
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
        else:
            try:
                all.insert_one({"url1":response.request.meta["originalurl"],"type1":"surface","url2":1,"type2":"","edge":""})
                print ("[++]"+url)
            except:
                pass






        
