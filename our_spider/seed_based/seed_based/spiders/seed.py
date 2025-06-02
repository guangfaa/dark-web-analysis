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
db = client['3our_spider_db']
# 存储暗网页面
link = db["link"]          
# 存储暗网网站
domain = db["domain"]  

     
#mongo
all = db["all"]        

def read_seed_nodes(file_path):
    with open(file_path, 'r') as file:
        seeds = file.readlines()
    return [seed.strip() for seed in seeds]

# for s in read_seed_nodes("/public/home/lizhihao/experiment/our_spider/seed_based/seed_based/seed.txt"):
#     # domain.insert_one({"url":s,"times":1})
#     link.insert_one({"url":s})
# 设置唯一索引

link.create_index([("url", 1)], unique=True)
all.create_index([("url1", 1), ("url2", 1)], unique=True)  

# 将spider类继承改为RedisCrawlSpider
class LizhiSpider(RedisSpider):    
    name = "seed"
    redis_key = 'lizhi:start_urls'  
    r = redis.Redis(host='192.168.31.7', port=6379)
    # start_time = datetime.now()
    # print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 插入 URL 到 Start URLs 集合
    # r.rpush('lizhi:start_urls', 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address/')
    # for s in read_seed_nodes("/public/home/lizhihao/experiment/our_spider/seed_based/seed_based/seed.txt"):
    #     r.rpush('lizhi:start_urls', s)
    
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
                self.server.rpush(self.redis_key, url)
                self.r.rpush('spider3:start_urls', self.base2+"\""+str(url)+"\""+"&first=1")
        except:
            pass
        # try:
        #     self.server.rpush(self.redis_key, url)
        #     self.r.rpush('spider3:start_urls', self.base2+"\""+str(url)+"\""+"&first=1")
        # except:
        #     pass

    def parse(self, response):
        request_url = self.remove_right_part(response.url)
        if response.status == 200:
            pattern = r'https?://\S+'
            Link = LinkExtractor(allow=pattern)
            iframe_links = response.xpath('//iframe/@src').getall()
            # 使用LinkExtractor提取出页面中的链接
            linkss = Link.extract_links(response)       
            # u = { "url": request_url }
            # newvalues = { "$set": { "status":True,"value":True} }
            # # 更新此次访问的URL的status和value
            # x = link.update_one(u, newvalues)
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
                            all.insert_one({"url1":request_url,"type1":"dark","url2":url,"type2":"surface","edge":"hyperlink"})
                            # 插入到clearweb clawer的redis
                            self.r.rpush('clearweb:start_urls', url)
                            continue     #后面的改！！！！！！！！！！！！！！！！！！！！！！
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

                    # if response.request.meta["originalurl"] != self.remove_right_part(response.url):
                    #     # 发生重定向
                    #     try:
                    #         redirect.insert_one({"url_":response.request.meta["originalurl"],"url":self.remove_right_part(response.url)})
                    #     except:
                    #         continue
                    try:
                        all.insert_one({"url1":request_url,"type1":"dark","url2":url,"type2":"dark","edge":"hyperlink"})
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
                try:
                    all.insert_one({"url1":request_url,"type1":"dark","url2":1,"type2":"","edge":""})
                except:
                    pass
        else:
            pass