#coding: utf-8
import smtplib
import base64
import time
import random
import re

from email.mime.text import MIMEText
from email.header import Header


def send(strSubject, content, opt = ''):
  sender = 'linsgrabstock@yeah.net'
  smtpserver = 'smtp.yeah.net'
  username = 'linsgrabstock@yeah.net'
  pwdFile = open('pwdWu.txt', 'r')
  password = pwdFile.readline().strip()
  pwdFile.close()
  username = base64.encodestring(username).strip() 
  password = base64.encodestring(password).strip() 
  date = time.strftime('%Y%m%d', time.localtime(time.time()))
  #userFile = open('userlistTest.txt','r')
  userFile = open('userlistWu.txt','r')
  mesg = '\nWu news\n\n'
  emails = userFile.readlines()
  userFile.close()
  logFile = open('./log/sendemail_' + date +'.log','a') #write only ,append
  logFile.write('\n\n-------------------\n Wu Send Content: \n' + content + '\n')
  mesg += '\n\n' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())
  smtp = smtplib.SMTP()
  try :
    smtp.connect("smtp.yeah.net: 25")
    mesg += '\n' + str(smtp.docmd('helo', 'linsgrabstock@yeah.net') ) 
    mesg += '\n' + str(smtp.docmd('auth login'))
    mesg += '\n' + str(smtp.docmd(username))
    mesg += '\n' + str(smtp.docmd(password))
    mesg += '\n' + str(smtp.docmd('mail from:','<linsgrabstock@yeah.net>'))
    if len(opt) == 0:
      for usermail in emails :
        usermail = usermail.strip()
        #if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",  email) != None :
        usermail = '<' + usermail + '>'
        mesg += '\n' + str(smtp.docmd('rcpt to:', usermail))
        mesg += '\n' + 'send to ' + usermail 
    else :
      usermail = '<1656758436@qq.com>'
      mesg +=  '\n' + str(smtp.docmd('rcpt to:', usermail))
      mesg += '\n' + 'send to ' + usermail 
    mesg += '\n' + str(smtp.docmd('data'))
    mesg += '\n' + str(smtp.docmd('from: linsgrabstock@yeah.net\r\n' + 
    'to: receiver@qq.com\r\n' + 
    'subject: ' + strSubject + '\r\n\r\n' + 
    #'subject: mail theme\r\n\r\n' + 
    content + '\r\n' + 
    #'rsrs \r\n' + 
    '.'))
    smtp.quit()
    #print mesg
    logFile.write(mesg)
    logFile.close()
    return True
  except Exception, e:
    mesg += 'exception :' + str(e)
    #print mesg
    logFile.write(mesg)
    logFile.close()
    return False

def informMyself(mesg) :
  send(mesg, mesg, 'send to myself')

def test() : #testAmount
  count = 0
  #while True :
  if True :
    send('大刘微博更新以及wu交易提醒','如果您收到，明天应该就能收到大刘更新及wu交易提醒邮件了。谢谢')
    count += 1

#test()

