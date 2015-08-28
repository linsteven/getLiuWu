#coding: utf-8
import sys
import urllib
import re
import time
import codecs
import sendLiu

def getHtml(url) :
  page = urllib.urlopen(url)
  html = page.read()
  return html

def getWeibo() :
  weibos = getHtml('http://www.imaibo.net/index.php?app=home&mod=Space&act=getSpaceWeibo300&uid=1954702')
  lines = weibos.split('\u')
  content = ''
  for word in lines : #转unicode为中文
    if len(word) == 4 :
      content += unichr(int(word,16))
    elif re.match(r"^[a-f0-9]{4}", word) :
      word = word.replace('\/', '/')
      word = word.replace('''\\\"''','''"''')
      content += unichr(int(word[:4],16)) + word[4:]
    else :
      content += word

  #f = codecs.open('1.txt', 'w', 'utf-8')
  #f.close()
  #f = codecs.open('1.txt', 'a', 'utf-8')
  weiboLst = list()
  for line in content.split('</div>') :
    if len(line) > 0 :
      #f.write(line)
      if u'刘鹏程SaiL直播' in line : #or re.match(r"^.*\d{2}:\d{2}.*$", line) :
        pos = line.find(u'[刘鹏程SaiL直播]')
        line = line[pos:]
        pos = line.find(u'[刘鹏程SaiL直播]', 1,-1)
        if pos > 0 : # if the line contains '展开更多', remove the less one
          line = line[:pos]
        #line = line.replace('</a>','')
        line, num = re.subn(ur"<((?!>).)*>", "", line)
        #line, num = re.subn(r'<a href.*_blank\'>','',line)
        #line, num = re.subn(r'<a target.*class\">','',line)
        #line, num = re.subn(r'<a target.*portfolio\/\d{2,6}\">','',line)
        #line, num = re.subn(r'<.*>','',line) # this line must be the last
        weiboLst.append(line)
        #f.write(line + '\n')
      elif re.match(ur"^.*\d{2}:\d{2}.*$", line) or re.match(ur"^.*\d{1,2}分钟.*$", line)  or re.match(ur"^.*\d{1,2}秒.*$", line) :
        if u'原文评论' in line : #1、获取原文链接，以获取评论内容 2、获取时间
          pos = line.find('<cite><a href')
          line = line[pos + 5:]
          pleft = line.find('http')
          pright = line.find('\"target')
          url = line[pleft:pright]
          #print url
          pos = line.find('blank\">')
          line = line[pos+7:]
          ctime, num = re.subn(r'<.*>','',line) # this line must be the last
          weiboLst.append(ctime) #暂时忽略url
          #f.write('url : ' + url + '  time : ' + ctime + '\n')
        else : 
          pos = line.find(u'评论')
          line = line[pos:]
          pos = line.find('blank\">')
          line = line[pos+7:]
          ctime, num = re.subn(r'<.*>','',line) # this line must be the last
          weiboLst.append(ctime)
          #f.write('time: ' + ctime + '\n')
          #pos = line.find(u'分')#(u'月' || u'今天' || u'分钟')
      elif u"回复" in line : #当回复置顶时，不会有[刘鹏程SaiL直播], 需特殊处理
        pos1 = line.find(u'回复')
        tmp = line[pos1+1:]
        pos2 = tmp.find(u'回复')
        if pos2 > 0 :
          line = line[:pos2]
        line = line[pos1:]
        line = u'[刘鹏程SaiL直播]' + line
        line, num = re.subn(ur"<((?!>).)*>", "", line)
        #line = line.replace('</a>','')
        #pat = re.compile(ur"\$.{3,4}\(\d{6}\)\$")
        #stocks = re.findall(pat,line)  #some errors
        #line, num = re.subn(r'<a target.*class\">','',line)
        #line, num = re.subn(r'<img.*$','',line)  #针对最后有表情，，，要改
        #line, num = re.subn(r'<a href.*_blank\'>','',line)
        #for st in stocks :
         # line += st + ' '
        #print line
        weiboLst.append(line)
        #f.write(line + '\n')
  #f.close()
  #weiboLst中是微博内容及其时间，需要将其组合
  return weiboLst

def combine() :
  lst = getWeibo()
  weibos = list()
  length = len(lst)
  #pos = lst[0].find(u'直播]')
  pos = 11 # pos+3 == 11
  for i in range(length) :
    if u'[刘鹏程' in lst[i] :
      weibo = lst[i]
      if u'[刘鹏程' in lst[i+1] :
        lst[i+1] = lst[i+1][11:]#去头部
        weibo += '(' + lst[i+2] + ')'
        weibo += u'//原文: ' + lst[i+1]
        weibo += '(' + lst[i+3] + ')'
        i += 3
      else : #没有原文，非转发，单条微博
        weibo += '(' + lst[i+1] + ')'
        i += 1
      print i, weibo
      weibos.append(weibo)
  return weibos

def getNewWeibo(sendedLst) :
  lst = getWeibo()
  length = len(lst)
  pos = 11 # pos+3 == 11
  weibo = ''
  hasNew = False
  cur = ''
  for i in range(12 if length > 12 else length):
    if u'[刘鹏程' in lst[i] :
      cur = lst[i]
      weibo = ''
      if u'[刘鹏程' in lst[i+1] :
        #if u'刚刚' in lst[i+3] or u'1分钟' in lst[i+3] :
        lst[i+1] = lst[i+1][11:]#去头部
        weibo += lst[i] + '(' + lst[i+3] + ')'
        weibo += u'//原文: ' + lst[i+1]
        weibo += '(' + lst[i+2] + ')'
        i += 3
      else : #没有原文，非转发，单条微博
        #if u'刚刚' in lst[i+1] or u'1分钟' in lst[i+1] :
        weibo += lst[i] + '(' + lst[i+1] + ')'
        i += 1
      if cur not in sendedLst :
        #更新sendedLst，并保持不是很大,10--20
        hasNew = True
        sendedLst.insert(0, cur)
        if len(sendedLst) >= 20 :
          for k in range(10) :
            sendedLst.pop()
        #更新本地文件
        date = time.strftime('%Y%m%d',time.localtime(time.time()))
        sendedFile = open('./tmp/sendedLiu_' + date + '.txt','a')
        sendedFile.write(cur + '\n')
        sendedFile.close()
        break  #一次假设只有一条更新，即10秒内大刘不会发两条微博
  if hasNew and '秒前' in weibo: # 满足刚刚更新的放进，不满足则添加进sended 文件
    return weibo
  else :
    return ''

#weibos = getWeibo()
#如何确认是新消息，
# 思路1： 根据时间标签判断，简单高效
# 思路2： 根据内容判断，是否曾出现过该消息
#暂时从简处理，行不通
#假设抓取‘1分钟前’，而按10秒的频率检查更新，则满足1分钟的会发多次，因此根据内容复杂但行的通。除非能1分钟更新一次，显然不符合实时性的要求，故还是采取思路2
#新思路：按时间标签，发送过保存一个今天已发送列表，检查到符合标签的看是否在已发送列表中，在就不发送，不在就发送并添加


#主程序run()思路逻辑：
#程序会在服务器不停的运行，后期会写一个监控程序，监测getDaliu以及getWu是否在运行
#1、打开程序，读取文件sended_08.txt，（08表示月份）初始化sendedLst，最多append10个，最少0个。
#2、每隔10s获取一次数据，分析是否有更新，有则发送，并更新sendedLst以及文件sended_08.txt

def init(date) :
  reload(sys)
  sys.setdefaultencoding('utf8') #'ascii' codec can't decode byte 0xe5 in position
  #date = time.strftime('%Y%m%d',time.localtime(time.time()))
  sendedFile = open('./tmp/sendedLiu_' + date + '.txt','a')
  sendedFile.close()
  sendedFile = open('./tmp/sendedLiu_' + date + '.txt','r')
  lines = sendedFile.readlines()
  sendedFile.close()
  length = len(lines)
  sendedLst = list()
  for i in range(length) :
    sendedLst.append(lines[i].strip('\n'))
  return sendedLst

def runOnce(sendedLst, date) :
  logfile = open('./log/getLiu_' + date + '.log', 'a')
  weibo = getNewWeibo(sendedLst)
  curtime = time.strftime('%H:%M:%S',time.localtime(time.time()))
  logfile.write('get New ok!' + curtime + '\n')
  if len(weibo) > 0 :
    #print 'New weibo: ' + weibo
    logfile.write('New weibo :' + weibo + '\n' + date + ' ' + curtime + '\n')
    sendLiu.send('大刘微博直播', weibo) 
  else :
    logfile.write('None!\n' + date + ' ' + curtime + '\n')
  logfile.close()
  #time.sleep(3)

def run() :
  sendedLst = init()
  while True : #无限循环
    runOnce(sendedLst)


#run()

