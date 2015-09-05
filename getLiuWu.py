#coding=utf-8
import getLiu
import getWu
import time
import sendWu
import getTodayUrl


startLiuHour = 7
stopLiuHour = 19
startWuHour = 9
midWuHour = 11
midWuMinute = 40
stopWuHour = 15
stopWuMinute = 10

sendWu.informMyself('程序启动')
while True :
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('./log/getBoth_' + date + '.log','a')
  hour = time.localtime().tm_hour
  minute = time.localtime().tm_min
  logFile.write(str(hour) + ':' + str(minute) + '\n')
  #print str(hour) + ':' + str(minute)
  #print 'in first while'
  logFile.write('in 1st while\n')
  logFile.close()
  enterLiu = False
  if hour == startLiuHour :
    enterLiu = True
    logFile = open('./log/getBoth_' + date + '.log','a')
    logFile.write('\n\n\nEnterLiu\n\n')
    logFile.close()
    #print 'enter liu'
    sendWu.informMyself('开始大刘')
    #init getLiu
    liuSendedLst = getLiu.init(date)
    #init getWu
    url = getTodayUrl.getUrl()
    wuSendedLst = getWu.init(date)
    latestDeal = '暂无'
    oldLst = list()
    enterWu = False
    wuIsEnd = False
    wuIsMid = False

    while(enterLiu) :
      getLiu.runOnce(liuSendedLst, date)
      if enterWu :
        time.sleep(3)
      else :
        time.sleep(8)
      h = time.localtime().tm_hour
      m = time.localtime().tm_min
      logFile = open('./log/getBoth_' + date + '.log','a')
      logFile.write(str(h) + ':' + str(m) + '\n')
      #print str(h) + ':' + str(m) + '\n'
      logFile.write('in 2nd while\n')
      if h == startWuHour and enterWu is False :
        enterWu = True
        logFile.write('\n\n\nEnterWu\n\n')
        #sendWu.informMyself('开始wu2198')
      #print '1'
      logFile.write('1\n')
      if enterWu :
        getWu.runOnce(url, date, wuSendedLst, latestDeal, oldLst)
        time.sleep(3)
      #print '2'
      logFile.write('2\n')
      if not wuIsMid and h == midWuHour and m == midWuMinute :
        getWu.runEnd(url)
        wuIsMid = True
      if not wuIsEnd and h == stopWuHour and m == stopWuMinute :
        enterWu = False
        getWu.runEnd(url)
        wuIsEnd = True
        sendWu.informMyself('结束wu2198')
      #print 3
      logFile.write('3\n')
      if h == stopLiuHour : # 22
        enterLiu = False
        sendWu.informMyself('结束大刘')
      #print 4
      logFile.write('4\n')
      logFile.close()
    
  time.sleep(300)

#sendedLst = getLiu.init()
#while(True) :
#  getLiu.runOnce(sendedLst)
#  time.sleep(5)
 # print 'one cycle'
