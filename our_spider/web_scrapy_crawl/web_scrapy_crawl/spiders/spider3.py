# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import pymongo
import re
from scrapy.linkextractors import LinkExtractor
import redis
from bs4 import BeautifulSoup
import base64
from scrapy_redis.spiders import RedisSpider
import warnings
from scrapy.exceptions import ScrapyDeprecationWarning
warnings.filterwarnings("ignore", category=ScrapyDeprecationWarning)

client = pymongo.MongoClient("mongodb://192.168.31.7:27017/")
# 建立数据库
client = pymongo.MongoClient("mongodb://192.168.31.7:27017/")
# 建立数据库
# 建立数据库
db = client['3our_spider_db']
# 存储暗网页面
link = db["link"]          
# 存储暗网网站
domain = db["domain"]
#mongo
all = db["all"]     
link.create_index([("url", 1)], unique=True)
all.create_index([("url1", 1), ("url2", 1)], unique=True)   

class Spider3Spider(RedisSpider):
    name = "spider3"
    redis_key = 'spider3:start_urls'   #lpush一个地址
    r = redis.Redis(host='192.168.31.7', port=6379)
    # a = "https://cn.bing.com/search?q=%22http://megalzwink435kangsseahebpbp3teedi4jjt64ne2g6d3oqy3qlweid.onion%22&first=1"
    def add_10_to_number_in_string(self,input_string):
    # 使用正则表达式提取字符串中的数字部分
        match = re.search(r'\d+$', input_string)
        if match:
            number = int(match.group())
            new_number = number + 10
            new_number_str = str(new_number)
            new_string = re.sub(r'\d+$', new_number_str, input_string)
            return new_string
        else:
            # 如果没有找到数字部分，直接返回原始字符串
            return input_string

    def parse(self, response):
        #pattern = r"約\s*(\d+)\s*項搜尋結果|找到约\s*(\d+)\s*条结果|约\s*(\d+)\s*个结果"
        pattern = r"约\s*(\d+)\s*个结果|About\s*(\d+)\s*results|of\s*(\d+)\s*results"
        match = re.search(pattern, response.text.replace(',', ''))

        # 指定保存文件的名称
        # file_name = 'output.txt'
        # with open(file_name, 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        if match :
            number = match.group(1) or match.group(2) or match.group(3)
            print("在明网中找到的结果数目:", number)
            soup = BeautifulSoup(response.text, 'html.parser')
            h2_tags = soup.find_all('h2')
            for h2 in h2_tags:
                a_tag = h2.find('a')  # 查找 <h2> 中的 <a> 标签
                if a_tag and 'href' in a_tag.attrs:  # 确保 <a> 标签存在且有 href 属性
                    print(a_tag['href'])
                    if "www.bing.com" in a_tag['href']:
                        pattern = r'aHR0[^&]*'
                        match = re.search(pattern,a_tag['href'])
                        if match:
                            enc = 'aHR0' + match.group(1)
                            if len(enc) % 4 == 1:
                                enc += '='
                            elif len(enc) % 4 == 2:
                                enc += '=='
                            elif len(enc) % 4 == 3:
                                enc += '==='
                            url = base64.b64decode(enc).decode()
                    else:
                        url = a_tag['href']

                    try:
                        match = re.search('%22(.*?)%22', response.request.meta["originalurl"])
                        dark_url = match.group(1)     #当前url
                        all.insert_one({"url1":url,"type1":"surface","url2":dark_url,"type2":"dark","edge":"hyperlink"})
                        print('!!!!!!!!!')
                        self.r.rpush('clearweb:start_urls', url)
                    except:
                        print('#################')
                        pass
                next_url = self.add_10_to_number_in_string(response.request.url)
                self.r.lpush('spider3:start_urls', next_url)

        else:
            print("_________在明网中找到的结果数目:0")
            pass