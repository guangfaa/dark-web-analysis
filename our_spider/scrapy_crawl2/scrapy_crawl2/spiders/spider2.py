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
db = client['3our_spider_db']
# 存储暗网页面
link = db["link"]          
# 存储暗网网站
domain = db["domain"]  

     
#mongo
all = db["all"]   
         
link.create_index([("url", 1)], unique=True)
all.create_index([("url1", 1), ("url2", 1)], unique=True)  



class Spider2Spider(RedisSpider):
    name = "spider2"
    redis_key = 'spider2:start_urls'   
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
    kinds_list = ["privacytools","breachlinks","passfiles","spyusers","torusers","onlinedata","webransom","darkpirate","encryptedlinks","hiddenservice","hiddencontact","market","ransom","sale","onlinecrime","tradecrime","cashusers","proxyfiles","salesite","tradepass","securevpn","tradeshare","passservice","identity","servicegoods","piratetools","safebank","sharegoods","onlineblackmail","safetrade","webanonymous","hostservice","systemsite","copytools","payservice","hiddenfile","buysystem","hiddensafe","tracksystem","onlineid","cashsite","netsystem","securekey","id","torlinks","crimetools","onlineransom","safepay","tradeillegal","webhost","securelock","contactmarket","emailservice","onlinedrug","drugmarket","anonfiles","securecloud","darkwallet","buymarket","illegalbitcoin","spytools","illegalweb","onlinefraud","illegalonline","encrypted","cryptocloud","cloudsystem","hiddenserver","contactsite","hiddenmoney","cryptopayment","illegalservice","onlinetrack","netfiles","hiddendark","darkcontact","cryptosystem","onlinecloud","tradeweb","attackservice","codefiles","darkpayment","safeonline","marketfiles","privacymarket","securetor","attacklinks","webmail","emailtools","onlinegoods","chatsystem","moneygoods","blackmaillinks","fraudsystem","ransomfiles","webemail","torservice","darkproxy","tradebitcoin","webvpn","nettools","goodsusers","cryptotheft","drugfiles","filesystem","webtrack","blackmailmarket","shopservice","vpnusers","cryptoidentity","anonusers","tradeblackmail","cryptotrack","darkprivacy","cryptosecure","websystem","cryptoscam","webshop","hacksystem","moneyusers","illegalid","hiddencrypto","hiddenvpn","illegaltools","contacttools","webgoods","secureuser","sell","paymentsite","hiddenanon","hiddenemail","websafe","illegalblackmail","piratelinks","illegalsell","tradetools","webstore","paymenttools","onlinelink","storesystem","cryptodata","cryptochat","illegalblock","shareusers","illegalcash","pirateusers","hiddenblackmail","shoplinks","privacy","accountfiles","linktools","hiddendrug","illegalidentity","hostlinks","tradeuser","key","cryptoserver","cryptomarket","cashsystem","hiddengoods","blackmailsystem","mailsite","ransomtools","accountservice","illegalprivacy","emailusers","netservice","file","onlineencrypted","serversite","webillegal","darkattack","shoptools","paymentservice","blackmailusers","serviceusers","onlinetrade","exchangeusers","fraudmarket","theftsystem","datalinks","hidesite","safechat","salemarket","hosttools","tradeidentity","tradelog","sharemarket","tradedark","buyservice","cloudusers","accessmarket","webexchange","crimefiles","illegalfile","chat","onlinepayment","onlinecoin","moneyfiles","bitcoinsystem","illegalcard","safehack","pirateservice","cryptogoods","webusers","illegalaccess","idfiles","paymarket","keymarket","tradepirate","tradestolen","safelinks","cryptotrade","onlinescam","darktrade","illegaltor","serversystem","scamsite","keysystem","breachtools","tradetrace","shopusers","safenet","webtor","webbitcoin","tradehost","tradeexchange","paysystem","softwaretools","proxysite","proxylinks","hiddenpay","darkstore","accessfiles","usergoods","moneysystem","anonymousmarket","scamtools","anonymoussystem","logsystem","emailgoods","onlinebreach","codesite","cryptocode","payusers","cryptomail","spylinks","cryptomoney","hiddencrime","securecard","spygoods","cryptoencrypted","anonymoususers","securecontact","idlinks","webcopy","tradecash","softwarefiles","webid","accountmarket","safeprivacy","anonymousfiles","securefraud","payment","netmarket","datamarket","blocklinks","logsite","darksystem","shopgoods","sellmarket","cryptovpn","hiddencard","scamgoods","theftmarket","keygoods","tradewallet","weblink","toolstools","safeexchange","cashfiles","hiddenwallet","illegaldata","vpnsystem","linkfiles","stolenusers","passtools","darktrace","tradecontact","webbank","darkmoney","cryptocopy","exchangefiles","ransomservice","illegalwallet","onlineblock","safeencrypted","coinlinks","illegal","servicesystem","darkblackmail","securedrug","safelink","toolssite","chatsite","lock","onlineshop","datafiles","tracktools","blockusers","exchangesite","bitcoin","onlineanonymous","walletusers","keyfiles","webcash","onlinespy","safesite","safe","onlinelinks","paysite","fake","websale","illegalencrypted","webpayment","onlinestore","tradescam","paylinks","securesecure","trademail","tracegoods","banklinks","tradetheft","onlinekey","darkanon","goodslinks","hiddensite","piratesite","darkvpn","coinservice","fraudtools","faketools","serverlinks","webcrypto","bankgoods","secureleak","cryptofake","secureid","drug","mailservice","passusers","accesstools","tradebank","theftservice","store","idmarket","servicemarket","linkservice","safeserver","tradelock","track","linksystem","webhidden","cryptolinks","tradeleak","secureonline","fraud","sharesite","cashtools","hiddencash","illegalmoney","toolsservice","safetheft","fakesite","stolenfiles","storeservice","walletsite","anonymouslinks","tradeencrypted","coinsystem","identitytools","securesite","money","securehack","ransomusers","darklinks","codemarket","accessservice","securepayment","cryptoillegal","webmoney","trace","account","safesoftware","illegalcrypto","moneysite","tradefiles","illegalsystem","passgoods","securefile","paymentusers","blackmailtools","ransomsite","darkuser","cryptotor","logservice","blackmailgoods","onlinestolen","darksale","exchangegoods","hiddennet","shop","securesell","servicesite","safebitcoin","keysite","identitysite","illegalransom","safetrace","hiddenhost","usersite","safeillegal","onlinetor","safegoods","druggoods","safecloud","webencrypted","leaktools","piratemarket","tradeattack","onlinehidden","dark","traceusers","safecrypto","exchangelinks","darkfake","tortools","attacktools","illegalfraud","darktrack","encryptedmarket","link","webhack","onlineaccess","toolsmarket","secureproxy","system","buysite","privacyfiles","darkcard","darkid","trackusers","hiddenexchange","cryptoservice","secureemail","fakelinks","darkstolen","illegalcode","softwaregoods","banktools","blackmail","keytools","safepayment","scammarket","blockfiles","tradesecure","vpn","shopfiles","cryptohack","webwallet","moneytools","onlinebank","safesystem","tradeaccount","theftgoods","fraudsite","safepass","drugtools","hiddentor","tradepay","onlineservice","onlineattack","onlinepass","codegoods","datausers","saferansom","onlineillegal","hiddenmarket","safeuser","privacygoods","contactusers","theft","webtrace","darkpay","tracesystem","cryptolog","mailfiles","safeanon","fakesystem","trackfiles","drugservice","cryptokey","proxymarket","vpnfiles","usersystem","accessgoods","hidegoods","illegalbuy","banksite","ransomlinks","accesssite","onlineonline","darkgoods","spysystem","tradefake","hiddenhidden","illegalserver","crimeusers","servermarket","hiddenid","torsystem","securepay","tradesale","toolslinks","anonservice","datasite","cryptohide","linkgoods","cryptoonline","onlinesystem","anonsystem","softwarelinks","tracefiles","buygoods","cloudmarket","buytools","darkonline","piratefiles","safedrug","secureexchange","illegalillegal","systemmarket","paygoods","paytools","darkanonymous","secureusers","scamusers","darkchat","servicefiles","illegalhost","tracemarket","safeemail","darknet","encryptedtools","sellusers","cryptodrug","hiddenpayment","bankservice","webaccount","locktools","filesite","fakefiles","anonymoussite","privacylinks","tradekey","hidemarket","walletfiles","theftusers","datagoods","cryptoblackmail","cryptobank","saleusers","securebreach","crypto","webshare","drugsite","tradecode","bitcointools","theftsite","hackgoods","systemgoods","blockmarket","toolssystem","bitcoinmarket","tradeproxy","hiddenbuy","attackfiles","secureaccess","filemarket","illegalproxy","fraudlinks","cryptosoftware","hiddenaccount","safecode","darkservice","host","darksoftware","hiddendata","securepirate","hiddenfraud","usermarket","hiddenspy","accesslinks","paymentlinks","bitcoinfiles","secureanon","payfiles","illegalsafe","webcard","coinfiles","onlinehost","tradedrug","safesell","safeidentity","moneymarket","code","cryptofile","illegalstolen","illegalchat","darkencrypted","safedark","buyusers","bank","securebuy","tradevpn","logusers","piratesystem","secureransom","lockfiles","hiddenshop","linklinks","securelog","breachsystem","darkweb","breach","blackmailservice","onlinetheft","servergoods","accountgoods","hiddenlog","salelinks","illegalspy","hiddenmail","vpnsite","illegalshop","hiddenprivacy","illegalattack","hiddenweb","securecrypto","hiddensecure","safebreach","bankfiles","blackmailsite","fraudusers","servertools","cryptofraud","tradesystem","illegalexchange","safetor","exchangesystem","blocktools","crimelinks","bitcoinlinks","copylinks","weblinks","hostmarket","cashlinks","paymentgoods","safefiles","darkcrime","securecrime","moneyservice","attackgoods","cashmarket","storelinks","hacktools","toolsfiles","keyservice","vpngoods","secure","marketusers","illegaluser","bitcoinservice","darkhide","softwaremarket","trademarket","tracesite","idtools","copyservice","breachusers","hiddenlock","securetheft","onlineprivacy","illegalmail","safeaccount","stolenlinks","onlinemoney","spysite","hiddenfiles","securebitcoin","accesssystem","server","websoftware","keylinks","leakfiles","webfiles","bitcoinusers","safeanonymous","encryptedservice","loggoods","sellsite","safesafe","stolen","contactsystem","proxyservice","identitysystem","illegaltrade","illegaltrace","onlinelog","tradedata","traderansom","safedata","tradechat","trackgoods","sellservice","cryptoshare","darkfraud","linkusers","cardlinks","onlineuser","netusers","onlinesoftware","cryptobitcoin","hide","hideusers","maillinks","webattack","codeusers","contactfiles","exchange","securesafe","hiddenkey","crime","cloudsite","webproxy","onlinesell","softwareservice","goods","onlinehack","hiddenleak","salesystem","hiddenanonymous","illegalcontact","userservice","datatools","hackfiles","illegalusers","lockservice","hiddenpass","anon","illegallock","shopmarket","cryptoanon","onlinewallet","weblog","buy","softwaresystem","bitcoinsite","securelink","webdark","illegallinks","stolensystem","chatmarket","userusers","illegallog","onlinehide","onlinevpn","wallettools","anonlinks","illegalnet","illegalanon","webspy","securesale","codelinks","sharetools","storefiles","ransomgoods","exchangemarket","securefiles","cryptohidden","tradehide","cryptostolen","website","securesystem","keyusers","hostfiles","scamsystem","serverservice","onlinechat","crimesite","encryptedusers","sellsystem","securehidden","illegalhack","cloudfiles","secureblock","illegalmarket","safesecure","tormarket","tradespy","emailsite","hidelinks","webonline","buyfiles","spyservice","contact","cryptocontact","illegalshare","hiddenidentity","securefake","cryptoblock","paymentfiles","cryptoransom","filegoods","attackmarket","sellfiles","onlinemail","blocksystem","systemservice","storemarket","secureweb","userlinks","darkdark","identityservice","onlinesecure","cryptopay","webtrade","securetrace","idservice","ransomsystem","onlineidentity","accountlinks","fileusers","illegaltheft","pirate","cryptoleak","codeservice","fakeusers","breachservice","passsystem","thefttools","cryptoweb","cryptopirate","cryptosafe","leaklinks","safecontact","cryptosale","darkemail","webfraud","hostusers","contactservice","hacklinks","hiddenonline","darkcash","idgoods","copysite","systemtools","illegaldark","blockgoods","passmarket","securemarket","fraudfiles","chattools","breachfiles","illegalfiles","cryptoexchange","cryptospy","privacyservice","anongoods","hiddenstolen","fakeservice","cryptopass","encryptedsystem","cardsite","securenet","illegalfake","logtools","walletgoods","cryptoaccess","secureattack","spy","darkspy","scam","securespy","darkfile","scamfiles","safecopy","usertools","crimemarket","darkbank","darkusers","blackmailfiles","tradeid","webblock","hidetools","webnet","fraudservice","loglinks","safevpn","encryptedfiles","cryptoemail","hiddenfake","pirategoods","bankusers","serviceservice","onlinepay","weblock","cryptoid","selltools","onlineshare","sharefiles","attackusers","leakservice","tradecopy","mail","stolenservice","scamlinks","safefake","cryptolock","webcontact","tradegoods","emaillinks","illegalcrime","darkfiles","tradesite","bankmarket","safemarket","cryptoaccount","crimegoods","tradefile","lockmarket","darksite","exchangetools","tradeonline","safefraud","darkhidden","onlineexchange","systemlinks","safehost","breachmarket","stolentools","safekey","webscam","securemoney","hiddenencrypted","hiddenproxy","hackservice","onlinefile","darksecure","illegalstore","datasystem","hostgoods","tradelink","onlinesale","cloudlinks","safemail","shopsite","hiddencoin","hiddenpirate","securescam","tradeblock","darkexchange","tradeanon","secureencrypted","copyusers","safecoin","blocksite","securecoin","toolsusers","markettools","drugusers","tradepayment","walletlinks","privacyusers","mailsystem","cryptocrime","software","hiddensoftware","goodsfiles","codesystem","onlinemarket","safespy","darklog","tradecard","spyfiles","safemoney","chatusers","darkbitcoin","safetools","darkhost","safeshare","hiddenblock","cardtools","darktools","illegalpay","log","marketsite","hidefiles","saletools","traceservice","selllinks","theftlinks","onlinefiles","darkcrypto","illegalbank","tradehidden","darkdrug","mailmarket","systemfiles","encryptedsite","cryptocrypto","webkey","safeattack","contactlinks","share","tradeprivacy","tradehack","illegalpass","cashgoods","tor","filelinks","marketsystem","secureserver","webpay","cryptoshop","hackmarket","securecash","web","locksystem","leakgoods","lockusers","linksite","cash","onlinebuy","darkmail","netlinks","accountsite","securechat","safebuy","darkpass","tracetools","banksystem","online","darkleak","secureaccount","torgoods","serverusers","marketmarket","hiddenuser","darkbreach","anonymous","identityusers","tradefraud","hiddencloud","privacysite","safeblackmail","onlinecopy","onlinecrypto","data","webcoin","userfiles","illegalleak","sharesystem","darktheft","secureanonymous","tradesoftware","netsite","securedark","torsite","leakmarket","stolenmarket","webblackmail","darkaccount","darksafe","moneylinks","darkdata","darkillegal","cryptocoin","safelock","goodsservice","safehidden","securebank","securehide","hostsystem","onlinebitcoin","hiddenbank","tradecoin","webhide","onlineleak","shareservice","webchat","theftfiles","hiddentools","cryptouser","spymarket","onlinetrace","hiddenillegal","logfiles","identitygoods","tradecrypto","toolsgoods","tradesell","hiddenhack","walletmarket","darkshare","darkcoin","tradeaccess","websecure","cryptowallet","webserver","onlinecash","safeproxy","hiddenshare","walletsystem","systemsystem","cloud","hiddencode","storeusers","anonymousservice","hiddenattack","wallet","safeusers","chatlinks","tradelinks","cloudtools","proxy","webweb","idusers","securehost","webcode","cashservice","mailusers","illegalsale","contactgoods","tradebreach","hiddenaccess","copy","goodsgoods","securedata","safeid","cryptosell","hiddenhide","cardusers","anonymoustools","hiddensystem","webpass","identitymarket","safescam","accountsystem","safecrime","softwaresite","ransommarket","lockgoods","hiddenstore","saleservice","webtheft","storetools","sharelinks","emailmarket","securetrack","hostsite","hiddenscam","onlinenet","anonymousgoods","vpntools","chatgoods","safewallet","breachsite","illegalpirate","cointools","cryptodark","systemusers","linkmarket","cardfiles","onlineproxy","trademoney","secureshop","coinusers","netgoods","illegalgoods","tradestore","tools","tradebuy","passsite","email","goodsmarket","trackservice","chatservice","paymentmarket","servicelinks","tradecloud","leaksite","serverfiles","onlinedark","hidden","webservice","illegalbreach","onlinetools","safeaccess","onlinesite","hiddentrade","darksell","safelog","proxyusers","fakemarket","securesoftware","hiddenlinks","darkserver","webbreach","safetrack","marketlinks","marketgoods","stolengoods","encryptedgoods","proxysystem","vpnlinks","tradeusers","torfiles","anontools","storesite","webaccess","onlinefake","tradeanonymous","tradetrack","webdata","coin","onlinecard","websell","emailfiles","cryptobreach","exchangeservice","secureprivacy","webfake","secureidentity","safesale","webtools","onlineaccount","hiddenransom","tracklinks","tradesafe","hiddenbitcoin","darklock","safefile","hiddencopy","card","safeservice","webpirate","emailsystem","vpnmarket","securestolen","securestore","illegaltrack","illegalsite","webanon","cryptotrace","tradeshop","webstolen","tradeserver","tradenet","copymarket","copygoods","darkshop","goodstools","secureillegal","crimesystem","sellgoods","hacksite","coinsite","anonmarket","webprivacy","attacksite","darkblock","hiddenchat","copysystem","securegoods","pay","safecard","identityfiles","hidesystem","net","hackusers","illegalcoin","cardservice","securepass","cryptoattack","securetools","securewallet","illegalscam","service","webcrime","dataservice","marketservice","tradeservice","accountusers","buylinks","darkmarket","cryptotools","webfile","secureservice","webbuy","darkcopy","cryptostore","illegalsecure","mailgoods","trade","darkhack","onlineweb","attacksystem","webcloud","scamservice","tracksite","drugsystem","cardmarket","illegalhidden","salegoods","cryptocash","illegalvpn","filefiles","servicetools","hiddensell","illegalhide","anonsite","darkaccess","safestore","onlinecode","identitylinks","securetrade","cryptousers","secureshare","securecopy","leaksystem","chatfiles","shopsystem","securelinks","safeleak","breachgoods","illegalsoftware","mailtools","tradeemail","idsite","illegalkey","blockservice","safeshop","vpnservice","illegalanonymous","fraudgoods","walletservice","illegalemail","onlineemail","tradetrade","cryptosite","leakusers","darkkey","proxygoods","accessusers","darktor","hiddenlink","idsystem","illegalcopy","illegalcloud","darkidentity","illegalaccount","safepirate","cardgoods","goodssystem","salefiles","onlineusers","user","passlinks","fileservice","onlinecontact","hack","block","trackmarket","securemail","codetools","filetools","cryptohost","pass","hiddenusers","cryptoprivacy","webleak","safeblock","secureblackmail","cryptolink","illegaldrug","cryptofiles","illegalpayment","darkbuy","leak","safestolen","cardsystem","darkcode","cryptocard","crimeservice","accounttools","darkransom","onlinesafe","hideservice","cryptonet","onlinepirate","hiddenbreach","webuser","webidentity","onlineserver","locksite","softwareusers","cloudservice","tracelinks","webdrug","safehide","proxytools","illegallink","webmarket","coingoods","onlineanon","darkcloud","hiddentrace","hiddentheft","safeweb","tradetor","cloudgoods","coinmarket","privacysystem","safecash","onlinelock","logmarket","cryptoproxy","hiddensale","locklinks","storegoods","cryptoanonymous","darkscam","bitcoingoods","stolensite","hiddentrack","attack","paymentsystem","goodssite","securecode","darklink","druglinks","cryptobuy","access","fakegoods","copyfiles","dark","web","market","trade","money","bitcoin","crypto","data","hack","crime","illegal","fraud","wallet","card","scam","drug","trade","vpn","spy","secure","hidden","goods","id","ransom","file","key","code","user","chat","proxy","service","host","buy","sell","link","block","theft","cash","mail","email","account","fake","stolen","sale","server","tools","attack","access","anon","payment","pirate","net","privacy","safe","lock","breach","leak","copy","store","system","software","online","share","cloud","file","exchange","blackmail","identity","tor","encrypted","contact","user","trade","pass","coin","log","secure","code","track","anonymous","trace","hide","bank","cash","shop","money","pay","dark","web","market","trade","money","bitcoin","crypto","data","hack","crime","illegal","fraud","wallet","card","scam","drug","trade","vpn","spy","secure","hidden","goods","id","ransom","file","key","code","user","chat","proxy","service","host","buy","sell","link","block","theft","cash","mail","email","account","fake","stolen","sale","server","tools","attack","access","anon","payment","pirate","net","privacy","safe","lock","breach","leak","copy","store","system","software","online","share","cloud","file","exchange","blackmail","identity","tor","encrypted","contact","user","trade","pass","coin","log","secure","code","track","anonymous","trace","hide","bank","cash","shop","money","pay","dark","web","market","trade","money","bitcoin","crypto","data","hack","crime","illegal","fraud","wallet","card","scam","drug","trade","vpn","spy","secure","hidden","goods","id","ransom","file","key","code","user","chat","proxy","service","host","buy","sell","link","block","theft","cash","mail","email","account","fake","stolen","sale","server","tools","attack","access","anon","payment","pirate","net","privacy","safe","lock","breach","leak","copy","store","system","software","online","share","cloud","file","exchange","blackmail","identity","tor","encrypted","contact","user","trade","pass","coin","log","secure","code","track","anonymous","trace","hide","bank","cash","shop","money","pay","dark","web","market","trade","money","bitcoin","crypto","data","hack","crime","illegal","fraud","wallet","card","scam","drug","trade","vpn","spy","secure","hidden","goods","id","ransom","file","key","code","user","chat","proxy","service","host","buy","sell","link","block","theft","cash","mail","email","account","fake","stolen","sale","server","tools","attack","access","anon","payment","pirate","net","privacy","safe","lock","breach","leak","copy","store","system","software","online","share","cloud","file","exchange","blackmail","identity","tor","encrypted","contact","user","trade","pass","coin","log","secure","code","track","anonymous","trace","hide","bank","cash","shop","money","pay","dark","web","market","trade","money","bitcoin","crypto","data","hack","crime","illegal","fraud","wallet","card","scam","drug","trade","vpn","spy","secure","hidden","goods","id","ransom","file","key","code","user","chat","proxy","service","host","buy","sell","link","block","theft","cash","mail","email","account","fake","stolen","sale","server","tools","attack","access","anon","payment","pirate","net","privacy","safe","lock","breach","leak","copy","store","system","software","online","share","cloud","file","exchange","blackmail","identity","tor","encrypted","contact","user","trade","pass","coin","log","secure","code","track","anonymous","trace","hide","bank","cash","shop","money","pay","dark","web","market","trade","money","bitcoin","crypto","data","hack","crime","illegal","fraud","wallet","card","scam","drug","trade","vpn","spy","secure","hidden","goods","id","ransom","file","key","code","user","chat","proxy","service","host","buy","sell","link","block","theft","cash","mail","email","account","fake","stolen","sale","server","tools","attack","access","anon","payment","pirate","net","privacy","safe","lock","breach","leak","copy","store","system","software","online","share","cloud","file","exchange","blackmail","identity","tor","encrypted","contact","user","trade","pass","coin","log","secure","code","track","anonymous","trace","hide","bank","cash","shop","money","pay","dark","web","market","trade","money","bitcoin","crypto","data","hack","crime","illegal","fraud","wallet","card","scam","drug","trade","vpn","spy","secure","hidden","goods"]

    
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
                self.r.rpush('Spider:start_urls', url)
                self.r.rpush('spider3:start_urls', self.base3+"\""+str(url)+"\""+"&first=1")
        except:
            pass


    # for i in kinds_list:
    #     url = base1+i+base2+str(current_page)
    #     list_num+=1
    #     r.rpush(redis_key, url)
    #     print(url)


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
                try:
                    all.insert_one({"url1":self.engine_url,"type1":"dark","url2":url,"type2":"dark","edge":"hyperlink"})
                    print ("[++][++]"+url)
                except:
                    continue
                # self.add_url(url, response)
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
        if "=1" == response.request.url[-2:]:
            match = re.search(r'Term frequencies:\s*<b>\w+</b>:\s*&nbsp;([\d,]+)', response.text)
            if match:
                number = int("".join(match.group(1).split(",")))
                total_pages = min(int(number / 10), 4000)
                page = 1
                for i in range(total_pages):
                    page +=1
                    new_url = response.request.url[:-1] + str(page)
                    self.server.rpush(self.redis_key, new_url)
            else:
                print("No match found.")


