#coding=utf-8
import getLiu
import getWu
import time
import sendWu
import getTodayUrl


startLiuHour = 8
stopLiuHour = 21
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
      h = time.localtime().tm_hour
      m = time.localtime().tm_min
      logFile = open('./log/getBoth_' + date + '.log','a')
      logFile.write(str(h) + ':' + str(m) + '\n')
      if h == startWuHour and enterWu is False :
        enterWu = True
        logFile.write('\n\n\nEnterWu\n\n')
        sendWu.informMyself('开始wu2198')
      if enterWu :
        getWu.runOnce(url, date, wuSendedLst, latestDeal, oldLst)
      if not wuIsMid and h == midWuHour and m == midWuMinute :
        getWu.runEnd(url)
        wuIsMid = True
      if not wuIsEnd and h == stopWuHour and m == stopWuMinute :
        enterWu = False
        getWu.runEnd(url)
        wuIsEnd = True
        sendWu.informMyself('结束wu2198')
      if h == stopLiuHour : # 22
        enterLiu = False
        sendWu.informMyself('结束大刘')
      logFile.close()

  time.sleep(300)

