# Scrapy settings for seed_based project

BOT_NAME = "seed_based"

SPIDER_MODULES = ["seed_based.spiders"]
NEWSPIDER_MODULE = "seed_based.spiders"

# user-agent 不使用，已改为随机代理
USER_AGENT = "Mozilla/5.0"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# 下载延时
DOWNLOAD_DELAY = 1  
#DOWNLOAD_TIMEOUT = 80  # seconds

#动态改变访问目标网站的频率，利用一个随机值，将延迟时间设置为0.5-1.5之间的随机数*DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True 
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

#反爬，scrapy禁用cookie
COOKIES_ENABLED = False  

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

#设置request headers:反爬
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Enable or disable spider middlewares
#SPIDER_MIDDLEWARES = {
#    "seed_based.middlewares.ScrapyCrawlSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "seed_based.middlewares.ProxyMiddleware": 543,
    #'seed_based.middlewares.RetryFailedUrl': 400,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "seed_based.pipelines.ScrapyCrawlPipeline": 300,
    #'scrapy_redis.pipelines.RedisPipeline': 300 redis存储，不使用，存到mongodb中
}

# scrapy去重，存放到redis的dup中
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"   
# 提高Scrapy在异步处理方面的性能
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# redis配置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True
REDIS_HOST = '192.168.31.7'
REDIS_PORT = 6379
# REDIS_START_URLS_AS_SET = True
REDIS_START_URLS_AS_LIST = True

# 返回错误时重试次数
RETRY_ENABLED = False
HTTPERROR_ALLOW_ALL = True  # 允许所有 HTTP 错误
RETRY_TIMES = 2




