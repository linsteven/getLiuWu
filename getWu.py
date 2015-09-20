#coding=utf-8
import sys
import urllib
import re
import time
import sendWu
import getTodayUrl
import socket

socket.setdefaulttimeout(5)

def getMesg(url) :
  html = ''
  lst = list()
  try :
    page = urllib.urlopen(url)
    html = page.read()
  except IOError,e :
    errno,errstr = sys.exc_info()[:2]
    logfile = open('./log/getWu_error.log', 'a')
    if errno == socket.timeout:
      logfile.write('There was a timeout\n')
    else :
      logfile.write('Some other socket error\n')
      
  if html == '':
    return lst
  lines = html.split('\n')
  start = 0
  end = 0
  findStart = False
  findEnd = False
  count = 0
  divCount = 0
  for line in lines :
    #if line == '</DIV>' : divCount += 1
    if findStart == False and line.startswith('<p>') :
      findStart = True
      start = count
    if findEnd == False and ('<!-- 正文结束 -->' in line ) : #line.startswith('<div>15') :
      findEnd = True
      end = count
      break
    count += 1
  for i in range(start,end+1) :
    lines[i] = lines[i].replace('&nbsp;',' ')
    lines[i] = lines[i].replace('---&gt;','')
    lines[i], num = re.subn(ur"<((?!>).)*>", "", lines[i])
    lines[i] = lines[i].strip(' ') 
    lines[i] = lines[i].replace('&lt;&lt;','<<')
    lines[i] = lines[i].replace('&gt;&gt;','>>')
    lines[i] = lines[i].replace('&#9733;','')
    lines[i] = lines[i].replace('&amp;','&')
    #if time and the content are placed seperately in two lines, then put time
    # in the content's line
    if re.match(ur"^\d{1,2}:\d{2}$", lines[i]) :
      lines[i+1] = lines[i] + " " + lines[i+1]
      lines[i] = ''
    if (not re.match(ur"^\d{1,2}:\d{2}", lines[i]))  and ( not re.match(r"^\d{1}\.", lines[i])) :
      lines[i] = ''
    if lines[i] != '' :
      lst.append(lines[i])
  return lst

def isDeal(line) :
  if (re.match(r"^.*买进\d{1,2}%", line) or
      re.match(r"^.*兑现\d{1,2}%", line) or
      re.match(r"^.*T出\d{1,2}%", line)  or
      re.match(r"^.*砍掉\d{1,2}%", line) or
      re.match(r"^.*出掉\d{1,2}%", line) or
      re.match(r"^.*减掉\d{1,2}%", line) or
      re.match(r"^.*减出\d{1,2}%", line) or
      re.match(r"^.*挂中\d{1,2}%", line) or
      re.match(r"^.*成交\d{1,2}%", line) or
      re.match(r"^.*回补\d{1,2}%", line) ):
    return True
  return False

def sendEmail(newLst, latestDeal = '', subject = '今日及时分析_wu2198') :
  content = ''
  if subject == '上午直播_wu2198' :
    content = '上午分析:\n\n'
  elif subject == '今日直播_wu2198' :
    content = '今日分析:\n\n'
  else:
    content = '新交易：' + latestDeal + ' \n\n' + '及时分析: ' + '\n\n' 
  for line in newLst :
    line = line.replace(' ', '  ') #扩大时间和内容间距离
    content += line + '\n\n'
  sendWu.send(subject, content)

def output(newLst, deaLst, latestDeal, refreshTime) :
  sep1 = '\n' + '-' * 25
  sep2 = '\n' + '=' * 25
  #今日分析
  print '今日分析：\n'
  for line in newLst :
   print line
  print sep1
  #today's deals
  print '今日交易：'
  for line in deaLst : 
    print line
  print sep1
  print '\n最新交易: ' + latestDeal
  print sep1
  print refreshTime
  print sep2

def init(date) :
  sendedFile = open('./tmp/sendedWu_' + date + '.txt','a')
  sendedFile.close()
  sendedFile = open('./tmp/sendedWu_' + date + '.txt','r')
  lines = sendedFile.readlines()
  sendedFile.close()
  length = len(lines)
  wuSendedLst = list()
  for i in range(length) :
    wuSendedLst.append(lines[i].strip('\n'))
  return wuSendedLst

def runEnd(url):
  if url == '' :
    return
  newLst = getMesg(url)
  h = time.localtime().tm_hour
  if h == 11 :
    sendEmail(newLst,'', '上午直播_wu2198')
  else :
    sendEmail(newLst,'', '今日直播_wu2198')

def runOnce(url, date, wuSendedLst, latestDeal , oldLst ) :
  if url == '':
    return
  logFile = open('./log/getWu_' + date + '.log', 'a')
  newLst = getMesg(url)
  if True: #len(newLst) > len(oldLst) :
    newLen = len(newLst)
    getNew = False
    for i in range(0, newLen) :
      if '目前中短线仓位' in newLst[i] :
        linenum = 0 
        #if several deals occur at the same time, set the subject be the last deal
        latestDeal = ''
        for j in range(i-3,i) :
          logFile.write(newLst[j] + '\n')
          if re.match(r"^.*\d{1,2}%", newLst[j]) and newLst[j] not in wuSendedLst:
            linenum = j
            getNew = True
            wuSendedLst.append(newLst[j])
            latestDeal = latestDeal + newLst[j] + '\n'
            sendedFile = open('./tmp/sendedWu_' + date + '.txt','a')
            sendedFile.write(newLst[j] + '\n')
            sendedFile.close()
            logFile.write('New deal: ' + newLst[j] + '\n')
        logFile.write('linenum = ' + str(linenum) + '\n')
        if linenum != 0 :
          ops = newLst[linenum].split(' ')
          if len(ops) > 1 :
            subject = ops[1]
            sendEmail( newLst, latestDeal, ops[1])

  refreshTime =  "\n更新时间: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
  logFile.write(refreshTime + '')
  logFile.write('-----------------\n')
  #output(newLst, wuSendedLst, latestDeal, refreshTime) 
  logFile.close()
  

def run():
  #url = getTodayUrl.getUrl()  #url of wu's blog
  url = 'http://blog.sina.com.cn/s/blog_48874cec0102vx4s.html'
  if url == '' :
    return
  latestDeal = '暂无'
  oldLst = list()
  date = time.strftime('%Y%m%d', time.localtime(time.time()))
  wuSendedLst = init(date) # deaLst
  while True :
    runOnce(url, date, wuSendedLst, latestDeal, oldLst)
    time.sleep(10)

#run()

