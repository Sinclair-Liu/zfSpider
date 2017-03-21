#author=刘宗汉
from urllib import request
import http.cookiejar
import gzip
import re

#根据分析得知登陆url
baseurl = 'http://xuanke.cufe.edu.cn/xtgl/login_login.html?yhm=%s&mm=%s&yzm='
url = 'http://xuanke.cufe.edu.cn/xtgl/login_login.html?yhm=2015312253&mm=******&yzm='
#username = input('输入用户名：')
#password = input('输入密码：')
#url = baseurl % (username,password)
#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = http.cookiejar.LWPCookieJar()
cookie_support = request.HTTPCookieProcessor(cj)
opener = request.build_opener(cookie_support, request.HTTPHandler)
request.install_opener(opener)
#打开页面，获取cookie
page = request.urlopen(url).read()
#发现页面为gzip压缩，需要先解压
page = gzip.decompress(page).decode("utf-8")
#cbaseurl = 'http://xuanke.cufe.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdmKey=N2151&sessionUserKey=%s&xnm=%s&xqm=%s'
#curl = 'http://xuanke.cufe.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdmKey=N2151&sessionUserKey=2015312253&xnm=2016&xqm=12'
#xnm = input('输入学年：')
#xqm = input('输入学期：')
#curl = cbaseurl % (username,xnm,xqm)
curl = 'http://xuanke.cufe.edu.cn/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=2015312253&xnm=2016&xqm=3&_search=false&nd=1490101123899&queryModel.showCount=15&queryModel.currentPage=1&queryModel.sortName=&queryModel.sortOrder=asc&time=0'
content = request.urlopen(curl).read().decode('utf-8')
print(content)