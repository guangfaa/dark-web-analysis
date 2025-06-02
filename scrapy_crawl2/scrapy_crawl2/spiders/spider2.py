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
# 建立数据库
db = client['2seed_engine_db']           
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

links.create_index([("url_", 1), ("url", 1)], unique=True)            
link.create_index([("url", 1)], unique=True)
clearweb.create_index([("url", 1)], unique=True)
dark_surface.create_index([("dark", 1), ("surface", 1)], unique=True)  
surface_dark.create_index([("surface", 1), ("dark", 1)], unique=True)  

class Spider2Spider(RedisSpider):
    name = "spider2-e"
    redis_key = 'spider2-e:start_urls'   
    r = redis.Redis(host='192.168.31.7', port=6379)
    # 起始页面
    current_page = 1      
    # 起始列表位置
    list_num = 0          
    # a="http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P=girl&[=8"
    engine_url = "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion"
    base1="http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P="
    base2="&[="
    base3 = "https://cn.bing.com/search?q="
    kinds_list = ["market","financial","communication","service","wiki","social","adult","drug","game","money","bitcoin","man","leak","engine","vpn","e-mail","card","electronics","Betting","Escrow","Forums","book","battery","arson","murder","manslaughter","homicide","kidnapping","abduction","smuggling","trafficking","counterfeiting","forgery","bribery","corruption","cybercrime","phishing","hacking","ransomware","theft","blackmail","terrorism","vandalism","shoplifting","pickpocketing","mugging","looting","trespassing","poaching","espionage","tax","racketeering","crime","prostitution","solicitation","pimping","human","doxing", "ransom", "scam", "phreaking", "exploitation","pseudonym", "networks", "illegal", "transaction", "secrecy","censorship", "underground", "subculture", "darkweb", "hidden","anonymizer", "bypass", "untraceable", "smuggling", "privacy","stealth", "incognito", "ghosting", "shadow", "clandestine","hack", "exploit", "tunneling", "deanonymization", "tor","vpn", "payload", "payload", "cracking", "flooding","credential", "hijacking", "spoofing", "vulnerability", "confidentiality"]
    
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
            links.insert_one({"url_":self.engine_url,"url":url})
            print ("[++][++]"+url)
            self.r.rpush('Spider-e:start_urls', url)
            self.r.rpush('spider3-e:start_urls', self.base3+"\""+str(url)+"\""+"&first=1")
            #获取的地址在明网上查
        except:
            pass
        try:
            link.insert_one({"url":url,"status":0,"value":0})   
            # # 计数，新建一个mongodb
            # match = re.search(r"(.{56}\.onion)", url)         
            # URL = match.group(1)
            # result = domain.find({"url": URL})
            # # 如果之前没有，插入
            # if len(list(result)) > 0:
            #     result = domain.update_one(
            #     {"url": URL},
            #     {"$inc": {"times": 1}}
            # )
            # else:
            #     # 如果有，次数加一
            #     domain.insert_one({"url":URL,"times":1})
        except:
            pass


    # for i in kinds_list:
    #     url = base1+i+base2+str(current_page)
    #     list_num+=1
    #     r.rpush(redis_key, url)


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
                    continue
                ex = url[:index]
                if len(ex)<56:
                    continue
                
                if url[-1] == "/":    #去掉最后一个/
                    a = url.rfind("/")
                    url = url[:a]
                self.add_url(url, response)
                # if ex.count(".")>=1:
                #     #主域
                #     match1 = re.search(r"(https?://).*", url) 
                #     extracted1 = match1.group(1)   
                #     match = re.search(r"(.{56}\.onion)", url)         
                #     extracted2 = match.group(1)
                #     extracted = extracted1+extracted2     #获取主域名extracted
                #     self.add_url(extracted, response)     #尝试插入主域名
                # for i in range(url.count('/')-1):
                #     url_now = '/'.join(url.split('/')[:i+3])   
                #     self.add_url(url_now, response)
        if "=1" == response.request.url[-2:]:
            match = re.search(r'Term frequencies:\s*<b>\w+</b>:\s*&nbsp;([\d,]+)', response.text)
            if match:
                number = int("".join(match.group(1).split(",")))
                print(response.request.url,number)
                total_pages = min(int(number / 10), 4000)
                page = 1
                for i in range(total_pages):
                    print(i)
                    page +=1
                    new_url = response.request.url[:-1] + str(page)
                    self.server.rpush(self.redis_key, new_url)
            else:
                print("No match found.")


