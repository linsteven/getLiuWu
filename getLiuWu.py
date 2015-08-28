#coding=utf-8
import getLiu
import getWu
import time
import sendWu
import getTodayUrl



sendWu.informMyself('程序启动')
while True :
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('./log/getBoth_' + date + '.log','a')
  hour = time.localtime().tm_hour
  minute = time.localtime().tm_min
  logFile.write(str(hour) + ':' + str(minute) + '\n')
  logFile.close()
  enterLiu = False
  if hour == 8 :
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
      if h == 9 and enterWu is False :
        enterWu = True
        logFile.write('\n\n\nEnterWu\n\n')
        sendWu.informMyself('开始wu2198')
      if enterWu :
        getWu.runOnce(url, date, wuSendedLst, latestDeal, oldLst)
        time.sleep(3)
      if h == 15 and m == 10 and not wuIsEnd:
        enterWu = False
        getWu.runEnd(url)
        wuIsEnd = True
      if h == 22 :
        enterLiu = False
      logFile.close()
    
  time.sleep(60)

#sendedLst = getLiu.init()
#while(True) :
#  getLiu.runOnce(sendedLst)
#  time.sleep(5)
 # print 'one cycle'
