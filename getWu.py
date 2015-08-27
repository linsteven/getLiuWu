#coding=utf-8
import urllib
import re
import time
import sendWu
import getTodayUrl

def getMesg(url) :
  page = urllib.urlopen(url)
  html = page.read()
  lines = html.split('\n')
  lst = list()
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
    lines[i] = lines[i].replace('<div>','')
    lines[i] = lines[i].replace('</DIV>','')
    lines[i] = lines[i].replace('&nbsp;<wbr>',' ')
    lines[i] = lines[i].replace('---&gt;','')
    lines[i] = lines[i].replace('<p>','')
    lines[i] = lines[i].replace('</P>','')
    lines[i] = lines[i].replace('<span>','')
    lines[i] = lines[i].replace('</SPAN>','')
    lines[i] = lines[i].strip(' ') 
    #clear the line contains a url which links to a new article,
    #such as: 14:15 最新<<券商股中线有涨35%潜力>>
    if 'HREF' in lines[i] : 
      lines[i] = '' 
    if '/>' in lines[i] :  #delete the "<img  .... />"
      lines[i], number = re.subn(ur"<.*/>", '', lines[i])
    #if time and the content are placed seperately in two lines, then put time
    # in the content's line
    if re.match(ur"^\d{1,2}:\d{2}$", lines[i]) :
      lines[i+1] = lines[i] + " " + lines[i+1]
      lines[i] = ''
    if (not re.match(ur"^\d{1,2}:\d{2}", lines[i]))  and ( not re.match(r"^\d{1}\.", lines[i])) :
      lines[i] = ''
    if lines[i] != '' :
      lst.append(lines[i])
    #print lines[i]
    #lst.append(lines[i])
  return lst

def isDeal(line) :
  #if ("买进" in line or 
  #    "兑现" in line or 
  #    "T出"  in line or
  #    "砍掉" in line or
  #    "出掉" in line or
  #    "减掉" in line or
  #    "挂中" in line or
  #    "成交" in line or
  #    "回补" in line) and '%' in line :#or "T出" or "买进" in line : #挂单
  if (re.match(r"^.*买进\d{1,2}%", line) or
      re.match(r"^.*兑现\d{1,2}%", line) or
      re.match(r"^.*T出\d{1,2}%", line)  or
      re.match(r"^.*砍掉\d{1,2}%", line) or
      re.match(r"^.*出掉\d{1,2}%", line) or
      re.match(r"^.*减掉\d{1,2}%", line) or
      re.match(r"^.*挂中\d{1,2}%", line) or
      re.match(r"^.*成交\d{1,2}%", line) or
      re.match(r"^.*回补\d{1,2}%", line) ):
    return True
  return False

def sendEmail(latestDeal, newLst, subject = '今日及时分析_wu2198') :
  content = '新交易：' + latestDeal + ' \n' + '及时分析: ' + '\n' 
  for line in newLst :
    line = line.replace(' ', '  ') #扩大时间和内容间距离
    content += line + '\n'
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

def run():
  url = getTodayUrl.getUrl()
  latestDeal = '暂无'
  oldLst = list()
  deaLst = list()
  newLst = getMesg(url)
  findDeal = False
  date = time.strftime('%Y%m%d', time.localtime(time.time()))
  
  while True :
    logFile = open('./log/getWu_' + date + '.log', 'a')
    newLst = getMesg(url)
    if len(newLst) > len(oldLst) :
      oldlen = len(oldLst)
      newlen = len(newLst)
      #logFile.write('oldlen = ' + str(oldlen) + ' newlen = ' + str(newlen))
      oldLst = newLst
      getNew = False
      for i in range(oldlen-1, newlen-1) :
        mesg = newLst[i]
        logFile.write('\n\nNew Message : ' + mesg + '\n')
        if isDeal(mesg) :
          getNew = True
          latestDeal = mesg
          deaLst.append(mesg)
          logFile.write('New deal: ' + mesg + '\n')
          ops = latestDeal.split(' ')
          logFile.write('ops length = ' + str(len(ops)))
          logFile.writelines(ops)
          for op in ops :
            print 'op: ' + op
          #if len(ops) > 1 :
      if getNew :
        sendEmail(latestDeal, oldLst, ops[1])
    
    diff = 0
    if latestDeal != '暂无' :
      strs = latestDeal.split(' ')
      times = strs[0].split(':')
      hour =  time.localtime().tm_hour
      minute = time.localtime().tm_min
      diff = hour * 60 + minute - int(times[0]) * 60 - int(times[1])
    if diff > 30 :
      latestDeal = '暂无' #only show the deal in 30 minutes
    #refresh time
    refreshTime =  "\n更新时间: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    output(newLst, deaLst, latestDeal, refreshTime)
    logFile.write(refreshTime + '')
    logFile.write('-----------------\n')
    #time.sleep(10)
  logFile.close()

#run()
