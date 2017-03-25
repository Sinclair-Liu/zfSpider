#author=刘宗汉
from urllib import request
import http.cookiejar
import gzip
import json
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import pickle

def start():
    score_info = ['',]
    file = open('score.pkl','wb')
    pickle.dump(score_info, file)
    file.close()

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def getScore():
    #根据分析得知登陆url
    #baseurl = 'http://xuanke.cufe.edu.cn/xtgl/login_login.html?yhm=%s&mm=%s&yzm='
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
    string = ""
    for i in list:
        if i['kcxzmc'] != '非授课':
            message = i['kcmc'] + ' 学分：' + i['xf'] + ' 成绩：' + i['cj'] + ' 绩点：' + i['jd']
            string += (message + "\n")
        if i['kcxzmc'] == '必修课' or i['kcxzmc'] == '限选课':
            xf += float(i['xf'])
            if i['cj'] == 'A':
                i['cj'] = 94
            cj += float(i['cj'])*float(i['xf'])
            jd += float(i['jd'])*float(i['xf'])
    string += ('加权学分平均分：%s\n' % (cj/xf))
    string += ('平均绩点：%s\n' % (jd/xf))
    file = open('score.pkl','rb')
    score_info = pickle.load(file)
    file.close()
    if string == score_info[0]:
        pass
    else:
        score_info[0] = string
        file = open('score.pkl','wb')
        pickle.dump(score_info, file)
        file.close()
        from_addr = "sinclair_liu@sina.com"
        password = "xxxxxx"
        to_addr = "nxp_nihao@163.com"
        smtp_server = "smtp.sina.com"
        msg = MIMEText(string, 'plain', 'utf-8')
        msg['From'] = _format_addr('云主机<%s>' % from_addr)
        msg['To'] = _format_addr('刘宗汉 <%s>' % to_addr)
        msg['Subject'] = Header('成绩', 'utf-8').encode()
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

def menu():
    dict = {0:start,1:getScore}
    #dict[0]()
    dict[1]()
if __name__ == '__main__':
    menu()
