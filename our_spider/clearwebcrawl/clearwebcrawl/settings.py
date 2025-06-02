# Scrapy settings for clearwebcrawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

BOT_NAME = "clearwebcrawl"

SPIDER_MODULES = ["clearwebcrawl.spiders"]
NEWSPIDER_MODULE = "clearwebcrawl.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "clearwebcrawl (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16
DOWNLOAD_TIMEOUT = 40

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = random.randint(1,5)
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "USER_AGENT" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",

    #"Cookie":"OTZ=7455231_24_24__24_; AEC=Ae3NU9Ps5-dRLN8MwsxQxWn2CEX3ie0zC7q2Pvy925YLzuqPlaBFFsSuhA; NID=512=fxSZBnglGaw8HM3emmzgBlMqqd1eWVGLyZ1lBI_zRQPTw6vpQCw-wzrNyvW8KWVedgUWyI2H9huMZFYDXJ5gP5uZS_rN8v5kXSaePQc3Pc5YtYPQIg8yvGpTO5jKr8cfCzSW0hs_yyyC1WT6Ort9HYBvgXJhULNJ0cMFP070hPC9nuM8FLJHGvxLV_fIJyCFEHV8gsP0qo5LSyp9ocvuPjv2n9U0x_Mc8xSveKvfNP2asaK1; 1P_JAR=2024-03-09-03; GOOGLE_ABUSE_EXEMPTION=ID=2228989816913461:TM=1709954182:C=r:IP=165.154.21.45-:S=nKBo4lQNM6IpWb6tEjaT6D8; DV=w3JJMLr4O48Y0J-HU_sc0edCKGMT4hg"
    "Cookie":"MUID=13B549563C906C3D25E35A943DF66D98; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=17D59F3D5E1B4AC98035F4B558636AEF&dmnchg=1; MUIDB=13B549563C906C3D25E35A943DF66D98; _uetvid=26de0cd08aa811ee8554d126447952d1; MSPTC=IxDjgcx4WGJ68zJG9hRbISnzNPt1rnCF8N1gb2iWPnI; MMCASM=ID=E840D3CDB1594D3CAD34E78899387E68; _UR=QS=0&TQS=0&cdxcls=0; MicrosoftApplicationsTelemetryDeviceId=94e34bf0-63f4-4b75-8a64-f3f612622551; _FP=hta=off; mapc=rm=0; ANIMIA=FRE=1; EDGSRCHHPGUSR=CIBV=1.1678.1; _tarLang=default=zh-Hans; _TTSS_OUT=hist=WyJlbiIsInpoLUhhbnMiXQ==; _TTSS_IN=hist=WyJ6aC1IYW5zIiwiZnIiLCJlbiIsImF1dG8tZGV0ZWN0Il0=&isADRU=1; SRCHS=PC=NMTS; _Rwho=u=d&ts=2024-05-10; _SS=PC=NMTS&SID=22BB3CEDD18E6CEC113F2896D0CD6DA4&R=200&RB=0&GB=0&RG=200&RP=200; BFPRResults=FirstPageUrls=3392BA6218FCBEF26F31BFEFF12F7499%2C8406BB1A858CAB9CF5F6AE8CC7233192%2C08E077E18BED30B86493404BEE267D3C%2C50ED98EFD67CC27E01FE3B83380C35DD%2C6BA510246938F295F2116484653FFB42%2C167C7D81CCD15DF442F7B2F025795297%2C445E687E3387F63C54A185DC76B104C3%2C163B9A27EB5686B75826CB3F9D250DFC%2CCED7534AFF08AFDC34061CDCCC54F836%2C967B2DD76809D3CF1DFA29D974FD15A1&FPIG=679A8C8166F44CA08CBEC3CAAFB66E18; USRLOC=HS=1&ELOC=LAT=39.77325439453125|LON=116.36433410644531|N=%E5%A4%A7%E5%85%B4%E5%8C%BA%EF%BC%8C%E5%8C%97%E4%BA%AC%E5%B8%82|ELT=2|&CLOC=LAT=39.77325251529622|LON=116.36433728166332|A=733.4464586120832|TS=240513004735|SRC=W&BID=MjQwNTEzMDg0NzM0X2MxOGNhZDYxOGNjZTcyYWFkNTMzZmZhZDJlMDdmYzdkYjhjZDExMDc2OTIyZTUzNjFmNDBkNWVjMjAwZTZjNmE=; ABDEF=V=13&ABDV=13&MRNB=1715562554568&MRB=0; SRCHUSR=DOB=20231107&T=1715564907000; _HPVN=CS=eyJQbiI6eyJDbiI6NywiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6NywiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6NywiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNC0wNS0xM1QwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoxNiwiVG9ibiI6MH0=; ai_session=x1xHjmtPqixcn4bD7OK2WI|1715565072037|1715566506842; _EDGE_S=SID=22BB3CEDD18E6CEC113F2896D0CD6DA4&mkt=zh-cn; GC=M4OfIhkNQAPHV9TcfSFkcuTbV9Skj1t0z7qZpxu3t6NJUWpSBmOY47gtQO1u7_eDU7G2nhh4JG2rZCCI45pE3A; _RwBf=r=0&ilt=2180&ihpd=3&ispd=19&rc=200&rb=0&gb=0&rg=200&pc=200&mtu=0&rbb=0&g=0&cid=&clo=0&v=22&l=2024-05-12T07:00:00.0000000Z&lft=2024-05-04T00:00:00.0000000-07:00&aof=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2024-05-13T02:21:16.7210190+00:00&rwred=0&wls=&wlb=&lka=0&lkt=0&aad=0&TH=&ccp=&wle=&ard=0001-01-01T00:00:00.0000000&rwdbt=0001-01-01T00:00:00.0000000&rwflt=0001-01-01T00:00:00.0000000&cpt=; ipv6=hit=1715570477846; SRCHHPGUSR=SRCHLANG=zh-Hans&PV=15.0.0&BZA=0&BRW=W&BRH=S&CW=1432&CH=150&SCW=1417&SCH=2454&DPR=1.5&UTC=480&DM=1&EXLTT=31&HV=1715566877&WTS=63851161707&PRVCW=1432&PRVCH=838&IG=F343534D6200403892830DD681631133&CIBV=1.1732.0&PR=1.5&THEME=1&EXLKNT=1&LSL=0&VSRO=1&BCML=1&BCTTSOS=110&AS=1&ADLT=OFF&NNT=1&HAP=0&CHTRSP=1"
    # "Cookie":"OTZ=7455231_24_24__24_; AEC=Ae3NU9Ps5-dRLN8MwsxQxWn2CEX3ie0zC7q2Pvy925YLzuqPlaBFFsSuhA; NID=512=fxSZBnglGaw8HM3emmzgBlMqqd1eWVGLyZ1lBI_zRQPTw6vpQCw-wzrNyvW8KWVedgUWyI2H9huMZFYDXJ5gP5uZS_rN8v5kXSaePQc3Pc5YtYPQIg8yvGpTO5jKr8cfCzSW0hs_yyyC1WT6Ort9HYBvgXJhULNJ0cMFP070hPC9nuM8FLJHGvxLV_fIJyCFEHV8gsP0qo5LSyp9ocvuPjv2n9U0x_Mc8xSveKvfNP2asaK1; GOOGLE_ABUSE_EXEMPTION=ID=2fdab3095d5a5a43:TM=1709949895:C=r:IP=165.154.21.45-:S=myw4S6jvSkIKbs573LN9-FM; 1P_JAR=2024-03-09-02; DV=w3JJMLr4O48Y0J-HU_sc0edCWUwP4hg"
    #"Cookie":"HSID=Au8uEA5smpcqs0jVR; SSID=AhuZ5E92DWLwMiF3I; APISID=x3bQ2z7hM2St1hsD/Aux1FaVl4HMFIibFs; SAPISID=cO8S-xOSVlNt7D1F/AF2C04hp3IrAOZ5c2; __Secure-1PAPISID=cO8S-xOSVlNt7D1F/AF2C04hp3IrAOZ5c2; __Secure-3PAPISID=cO8S-xOSVlNt7D1F/AF2C04hp3IrAOZ5c2; SEARCH_SAMESITE=CgQI6ZkB; SID=g.a000gwjcPEeBtAgQXf7ufWSn5PZ9tGZRSQtreT9NPL9zcWoCmj6xGHUnYssthL_Rg85ZK7eZLAACgYKAUwSAQASFQHGX2MiKGqOljS3IPaUS8QLoiq7CxoVAUF8yKrrbhbVQOYzlBebXqeRmFAb0076; __Secure-1PSID=g.a000gwjcPEeBtAgQXf7ufWSn5PZ9tGZRSQtreT9NPL9zcWoCmj6x4A1ncDOKU2A2MMVaOKet4gACgYKAf0SAQASFQHGX2Migkv23Bvy3UskoAGxhLNW7BoVAUF8yKrdBmxUh142J9LE_-j201_o0076; __Secure-3PSID=g.a000gwjcPEeBtAgQXf7ufWSn5PZ9tGZRSQtreT9NPL9zcWoCmj6x-DKFdkUc7qr6LGkX9Ph8VQACgYKAdgSAQASFQHGX2Miwr6F8tHaVNMt00kkDSW95RoVAUF8yKqceRMLyEzH9PDjn-cfx9qy0076; AEC=Ae3NU9MK1nm-DlTWO-WBGW0jVt5laDWDzsx7iLRPA74FC2XerDXsxG6Lmr8; __Secure-1PSIDTS=sidts-CjEBYfD7Z7RyEaC4lV8j-Dtq29GBmVoSJm23PJbX8OnL6acmZ-Dz0Jt6tR9MffGIUhfeEAA; __Secure-3PSIDTS=sidts-CjEBYfD7Z7RyEaC4lV8j-Dtq29GBmVoSJm23PJbX8OnL6acmZ-Dz0Jt6tR9MffGIUhfeEAA; 1P_JAR=2024-03-09-02; GOOGLE_ABUSE_EXEMPTION=ID=9858dd1a353332f5:TM=1709950049:C=r:IP=165.154.21.45-:S=jbf3i8wChXufKM9pRUchYh4; NID=512=mWok8zlOY7aYYun6aBWeFyvwdPVqwTIQcM-ry1pzj9KeFCKTa33aYCJF2hOu95lE845dp7So5VZsvC_kt8yxuEeRujlIy_Pq7uOQfyMJaBdQ2hOYUgC_CuSCSa8Sr3XEgfJyxvMGtrkERrtyYF1fPQAhvklu8eX1yJlVQdecjYtPfKQZfCwq__wwy4X2GXFZlcymowQwqmnl4_Pfe0GjbUWX-uZQpWm9Jci58aW2LKsUbmD6qRn5fAXDAUhn9WnT2zWNr43Iss3-tSgH_okh8pgDqCYiSaF0MxRXcb3fojmt; SIDCC=AKEyXzXf0oqdfsJc_7E1s89MwAFF_6L3UQbELzg_8Ywtwyd3gY4hCI8B1oqIwbLv6ICn45I4Cg; __Secure-1PSIDCC=AKEyXzUxqH7JaHKDg7u_yLliReeNbp4kmn9xOic-EfkMRgc9igWxlsZv8_9EQvMFiMle2cKC8iE; __Secure-3PSIDCC=AKEyXzVsHmwNJeFs8fiZewsQv2djV8mp6yjvkHjLu5QHlF4j1z8AkbnAGj0m4eLb4dKO3Og216Y"
}
# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "clearwebcrawl.middlewares.ClearwebcrawlSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "clearwebcrawl.middlewares.ClearwebcrawlDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "clearwebcrawl.pipelines.ClearwebcrawlPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# redis配置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True
REDIS_HOST = '192.168.31.7'
REDIS_PORT = 6379
#REDIS_START_URLS_AS_SET = True
REDIS_START_URLS_AS_LIST = True


RETRY_TIMES = 2