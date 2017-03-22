#author=刘宗汉
from urllib import request
import http.cookiejar
import gzip
import json

def getScore():
    #根据分析得知登陆url
    baseurl = 'http://xuanke.cufe.edu.cn/xtgl/login_login.html?yhm=%s&mm=%s&yzm='
    url = 'http://xuanke.cufe.edu.cn/xtgl/login_login.html?yhm=2015312253&mm=xxxxxx&yzm='
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
    curl = 'http://xuanke.cufe.edu.cn/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=2015312253&xnm=&xqm=&_search=false&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=&queryModel.sortOrder=asc&time=0'
    #2016-2017学年的xnm为2016，全部为空
    #1学期的xqm为3，2学期为12，3学期为16，全部为空
    content = request.urlopen(curl).read().decode('utf-8')
    contentJson = json.loads(content)
    list = contentJson.get('items')
    xf = 0
    cj = 0
    jd = 0
    for i in list:
        if i['kcxzmc'] != '非授课':
            message = i['kcmc'] + ' 学分：' + i['xf'] + ' 成绩：' + i['cj'] + ' 绩点：' + i['jd']
            print(message)
        if i['kcxzmc'] == '必修课' or i['kcxzmc'] == '限选课':
            xf += float(i['xf'])
            if i['cj'] == 'A':
                i['cj'] = 94
            cj += float(i['cj'])*float(i['xf'])
            jd += float(i['jd'])*float(i['xf'])
    print('加权学分平均分：%s' % (cj/xf))
    print('平均绩点：%s' % (jd/xf))



def menu():
    dict = {1:getScore}
    dict[1]()
if __name__ == '__main__':
    menu()
