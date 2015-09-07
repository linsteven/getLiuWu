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
   #print 'wuget 1'
    page = urllib.urlopen(url)
   #print 'wuget 2'
    html = page.read()
   #print 'wuget 3'
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
    if findStart == False and line.startswith('<div>9') :
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
  if subject == '今日及时分析_wu2198' :
    content = '今日分析:\n'
  else :
    content = '新交易：' + latestDeal + ' \n\n' + '及时分析: ' + '\n' 
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
  sendEmail(newLst)

def runOnce(url, date, wuSendedLst, latestDeal , oldLst ) :
  if url == '':
    return
  logFile = open('./log/getWu_' + date + '.log', 'a')
  newLst = getMesg(url)
  if len(newLst) > len(oldLst) :
    oldLen = len(oldLst)
    newLen = len(newLst)
    for kk in range(oldLen,newLen) :
      oldLst.append(newLst[kk])
    #oldLst = newLst
    getNew = False
    subject = 'wu2198直播更新'
    for i in range(oldLen, newLen) :
      #mesg = newLst[i]
      #print newLst[i]
      #if isDeal(mesg) and mesg not in wuSendedLst : 
      #  #can get the deal as soon as possible
      #  getNew = True
      #  latestDeal = mesg
      #  wuSendedLst.append(mesg)
      #  sendedFile = open('./tmp/sendedWu_' + date + '.txt','a')
      #  sendedFile.write(mesg + '\n')
      #  sendedFile.close()
      #  logFile.write('New deal: ' + mesg + '\n')
      #  ops = latestDeal.split(' ')
      #  if len(ops) > 1 :
      #    subject = ops[1]
      #  #break
      if '目前中短线仓位' in newLst[i] :
        linenum = 0 
        #if several deals occur at the same time, set the subject be the last deal
        latestDeal = ''
        for j in range(i-3,i) :
          if re.match(r"^.*\d{1,2}%", newLst[j]) and newLst[j] not in wuSendedLst:
            linenum = j
            getNew = True
            wuSendedLst.append(newLst[j])
            latestDeal = latestDeal + newLst[j] + '\n'
            sendedFile = open('./tmp/sendedWu_' + date + '.txt','a')
            sendedFile.write(newLst[j] + '\n')
            sendedFile.close()
            logFile.write('New deal: ' + newLst[j] + '\n')
        if linenum != 0 :
          ops = newLst[linenum].split(' ')
          if len(ops) > 1 :
            subject = ops[1]
            sendEmail( oldLst, latestDeal, ops[1])
        #break


  #diff = 0
  #if latestDeal != '暂无' :
  #  strs = latestDeal.split(' ')
  #  times = strs[0].split(':')
  #  hour =  time.localtime().tm_hour
  #  minute = time.localtime().tm_min
  #  diff = 50
  #  #diff = hour * 60 + minute - int(times[0]) * 60 - int(times[1])
  #if diff > 30 :
  #  latestDeal = '暂无' #only show the deal in 30 minutes
  #refresh time
  refreshTime =  "\n更新时间: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
  logFile.write(refreshTime + '')
  logFile.write('-----------------\n')
  #time.sleep(10)
  #output(newLst, wuSendedLst, latestDeal, refreshTime) 
  logFile.close()
  

def run():
  url = getTodayUrl.getUrl()  #url of wu's blog
  #url = 'http://blog.sina.com.cn/s/blog_48874cec0102vwv6.html'
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

