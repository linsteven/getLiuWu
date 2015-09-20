#coding: utf-8
import smtplib
import base64
import time
import random
import re

from email.mime.text import MIMEText
from email.header import Header


def send(strSubject, content) :
#strSubject = '测试邮件功能'
#content = 'this is a test'
#if True :
  smtpserver = 'smtp.163.com'
  username = 'linsgrabstock@163.com'
  password = 'tzyukwjbfbvanltm'
  username = base64.encodestring(username).strip() 
  password = base64.encodestring(password).strip() 
  date = time.strftime('%Y%m%d', time.localtime(time.time()))
  userFile = open('userlistLiu.txt','r')
  #userFile = open('userlist.txt','r')
  emails = userFile.readlines()
  logFile = open('./log/sendemail_' + date +'.log','a') #write only ,append
  logFile.write('\n\n-----------------\nLiu Send Content: \n' + content + '\n')
  mesg = '\n\n' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())
  smtp = smtplib.SMTP()
  #print 'try connect'
  try :
    smtp.connect("smtp.163.com: 25")
    mesg += '\n' + str(smtp.docmd('helo', 'linsgrabstock@163.com') ) 
    mesg += '\n' + str(smtp.docmd('auth login'))
    mesg += '\n' + str(smtp.docmd(username))
    mesg += '\n' + str(smtp.docmd(password))
    mesg += '\n' + str(smtp.docmd('mail from:','<linsgrabstock@163.com>'))
    for usermail in emails :
      usermail = usermail.strip()
      #if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",  email) != None :
      #  print 'yes'
      usermail = '<' + usermail + '>'
      mesg += '\n' + str(smtp.docmd('rcpt to:', usermail))
      mesg += '\n' + 'send to ' + usermail 
    mesg += '\n' + str(smtp.docmd('data'))
    mesg += '\n' + str(smtp.docmd('from: linsgrabstock@163.com\r\n' + 
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

def test() : #testAmount
  count = 0
  while True :
   send('测试邮箱容量' + str(count), 'this is a simple test. No.' + str(count))
   count += 1
   if count >100 :
     break
   #print 'count = ' + str(count)
   #print time.localtime().tm_hour, ':', time.localtime().tm_min
   #print '\n\n'
   time.sleep(random.randint(5,20))

#test()

