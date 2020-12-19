

import json
import sys
import datetime 
import glob
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
import html2text

import logging
import os
import base64
import random

#-------------Output Logger
# create logger
logger = logging.getLogger(os.path.basename(__file__))
#logger.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)
ch.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh = logging.FileHandler('pyAutomail.log')
fh.setLevel(logging.ERROR)

# create formatter and add it to the handlers
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
#-------------Output Logger


# checking for prime
def is_prime(n):
   if n <= 1:
      return False
   else:
      for i in range(2, n):
         # checking for factor
         if n % i == 0:
            # return False
            return False
      # returning True
   return True

def birthdayMail(event):
  msg = EmailMessage()
 # image_cid = make_msgid()

  file = open(event['content'],'r', encoding='utf8')
  html = file.read()
  file.close()
  basepath = './hb/'
  search =  os.path.join(basepath,'*.jpg')
  xglob = glob.glob(search)
  filename = random.choices(xglob, k=1) # select random image
  image = open(filename[0], 'rb') #open binary file in read mode

  # know the Content-Type of the image
  maintype, subtype = mimetypes.guess_type(image.name)[0].split('/')

  image_read = image.read()
  image.close()
  image_64_encode = base64.b64encode(image_read)
#      <img src="data:{maintype}/{subtype};base64,{imgbase64}" />

  search =  os.path.join(basepath,'*.txt')
  xglob = glob.glob(search)
  filename = random.choices(xglob, k=1) # select random image
  happybirthday_file = open(filename[0], 'r', encoding='utf8') #open binary file in read mode
  happybirthday = happybirthday_file.read()
  happybirthday_file.close()

  today = datetime.date.today()
  date_event=datetime.datetime.strptime(event['date'], "%d.%m.%Y")
  birthday=datetime.date(date_event.year,date_event.month,date_event.day)
  alter =  today.year-birthday.year
  logger.debug("Alter: {}, Primzahl: {}, Runder? {}".format(alter,is_prime(alter),alter%10==0))
  if (is_prime(alter)):
    happybirthday = "\n<p>{} ist eine Primzahl - ein Grund zu feiern! </p>\n".format(alter) + happybirthday
  if(alter%10==0):
    happybirthday = "\n<p>Zum Runden {}. Geburtstag:</p>\n".format(alter) + happybirthday
  
  # image_cid=image_cid[1:-1]
  # ,imgbase64=image_64_encode.decode('utf-8')
  message=html.format(anrede=event['anrede'],happybirthday=happybirthday,maintype=maintype, subtype=subtype, imgbase64=image_64_encode.decode('utf-8'),gruss=event['gruss'])
  text_maker = html2text.HTML2Text()
  text_maker.ignore_images = True
  msg.set_content(text_maker.handle(message))
  msg.add_alternative(message, subtype='html')
  
  # attach it
  msg.add_attachment(image_read, 
                  maintype=maintype, 
                  subtype=subtype, 
                  filename='happy-birthday.jpg')

  logger.info("Folgende Mail wurde versandt Subject: '{}' Intervall: '{}', Datum: '{}'".format(event['subject'], event['intervall'], event['date']))
  msg['Subject'] = event['subject']
  msg['From'] = event['from']
  msg['To'] = event['to']
  return msg

def simpleMail(event):
  file = open(event['content'],'r', encoding='utf8')
  mailtext = file.read()
  file.close()
  msg = MIMEText(mailtext,_charset='utf-8')
  logger.info("Folgende Mail wurde versandt Subject: '{}' Intervall: '{}', Datum: '{}'".format(event['subject'], event['intervall'], event['date']))
  msg['Subject'] = event['subject']
  msg['From'] = event['from']
  msg['To'] = event['to']
  return msg



#read config
with open('config.json') as f:
  config_ = json.load(f)
  # if json isn't formated well abstract errors occur. Not that nice....

for event in config_['events']:
  logger.debug("Event: {}".format(event))

#check date against send-intervall
  today = datetime.date.today()
  date_event=datetime.datetime.strptime(event['date'], "%d.%m.%Y")
  logger.debug("Event, heute: {}".format((date_event, today)))
  # switch for bool-check
  test = { 
    'yearly': bool(today.day == date_event.day and today.month == date_event.month),
    'monthly':  bool(today.day == date_event.day),
    'daily': True # assuming running only once a day.
  }
  logger.debug("Prüfung auf bool: {},{}".format(event['intervall'],dict[event['intervall']]))
  if (test[event['intervall']]):
    msg = getattr(sys.modules[__name__], event['action'])(event)
   # msg = simpleMail(event)
    sender = event['from']
    receivers=event['to']
    port = config_['email']['port']
    password = config_['email']['password']
    # ssl send mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config_['email']['host'], port, context = context) as server:
        server.login(config_['email']['login'],password)
        server.sendmail(sender,receivers,msg.as_string())
        logger.debug("Email: {}".format((msg)))
