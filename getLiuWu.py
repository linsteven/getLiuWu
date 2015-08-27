#coding=utf-8
import getLiu
import getWu
import time

sendedLst = getLiu.init()
while(True) :
  getLiu.runOnce(sendedLst)
  time.sleep(5)
  print 'one cycle'
