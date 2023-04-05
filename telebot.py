import telepot
import time,datetime
import re
from telepot.loop import MessageLoop
from subprocess import Popen, PIPE
import cv2
import configparser
import numpy as np
import copy

##BOT_TOKEN="5982985448:AAHJXSXB7xMP_LVS3YFBrNz1_bV1rnhTFhk"
##CHAT_ID="1846666955"
##CHAT_ID_GROUP ="-856193605"

config = configparser.ConfigParser()
config.read('resourses/bot_settings.ini')

BOT_TOKEN =  config['Telegram']['Bot_token']
CHAT_ID = config['Telegram']['Chat_ID']
CHAT_ID_GROUP = config['Telegram']['Chat_ID_group']
TRUSTED_USERS = config['Telegram']['Trusted_users_ID']


def getImage():        
        ret, frame = cap.read()
        cv2.imwrite('img1.png', frame)
        
##def getVideo(_length = 1):


def getCmdOut(cmd=''):
        process = Popen(cmd, shell=True,stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        if process.returncode:
                return False
        return out.decode("utf-8")

def temperatureFormat(_str=''):
    return '{:.2f}'.format(int(_str)/1000)

def getCpuTemperature():
    out = [0, 0, 0, 0]
    out[0] = getCmdOut('cat /sys/class/thermal/thermal_zone0/temp')
    out[1] = getCmdOut('cat /sys/class/thermal/thermal_zone1/temp')
    out[2] = getCmdOut('cat /sys/class/thermal/thermal_zone2/temp')
    out[3] = getCmdOut('cat /sys/class/thermal/thermal_zone3/temp')
    match = re.match(r'^[0-9]+', max(out))
    if not match:
        return 0
    return temperatureFormat(match.group())

def getMemLoad():
    result = {'Total': 0,'Used': 0, 'Free': 0}
    out = getCmdOut('free -tm')
    match = re.search(r'^Mem:\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)',out, re.MULTILINE)
    if not match:
        return result
    return {
        'Total' : match.groups()[0],
        'Used' : match.groups()[1],
        'Free' : match.groups()[2]
        }

def getDiskSpace():
    result = {'Total': 0,'Used': 0, 'Free': 0}
    out = getCmdOut('df -H | grep ^/dev')
    match = re.search(r'(?:(\d+|\d+[.,]\d+))G\s+(?:(\d+|\d+[,.]\d+))G\s+(?:(\d+|\d+[,.]\d+))G',out, re.MULTILINE)

    if not match:
        return result
    return {
        'Total' : match.groups()[0],
        'Used' : match.groups()[1],
        'Free' : match.groups()[2]
        }
        

def getCpuLoad():
    out = getCmdOut('cat /proc/loadavg')
    match = re.findall(r'\d*\.\d+|d+', out)
    if not match:
        return 0
    return match[0]

def getIpAddr():
        out = getCmdOut('ifconfig wlan0')
        match = re.search('\d+\.\d+\.\d+\.\d+', out)
        if not match:
                return 0
        return match[0]
        
def getTimeDate():
        _time = datetime.datetime.now()
        _str = ''
        _str = _str + str(_time.day) + '/'
        _str = _str + str(_time.month) + '/'
        _str = _str + str(_time.year)  + '  '  
        _str = _str + str(_time.hour) + ':'        
        _str = _str + str(_time.minute) + ':'
        _str = _str + str(_time.second)
        return _str
        
def getStatus():
        _time = datetime.datetime.now()
        _memory = getMemLoad()
        _cpu = getCpuLoad()
        _ip = getIpAddr()
        _freeSpace = getDiskSpace()
        
        _str = 'Текущее время :  '
        _str = _str + getTimeDate() + '\n'

        _str = _str + 'Темпертура процессора : '
        _str = _str + getCpuTemperature() + '°C\n'
        
        _str = _str + 'Использовано памяти : '
        _str = _str + '{} / {} Mb'.format(_memory['Used'], _memory['Total'])  + '\n'
        _str = _str + 'Зарузка ЦПУ : '
        _str = _str + _cpu + ' %\n'
        _str = _str + 'Место на диске : '
        _str = _str + '{} / {} Gb'.format(_freeSpace['Used'], _freeSpace['Total'])  + '\n'
        _str = _str + 'IP адрес : '
        _str = _str + _ip + '\n'     

        return _str
        

def action(msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        from_id = msg['from']['id']
        if TRUSTED_USERS.find(str(from_id)) == -1:
                bot.sendMessage(chat_id, "Неправельный пользователь!")
                return
        
        if command.find('/help') != -1 :

                answer = "/help - помощь\n"
                answer = answer + "/getimage - запрос картинки\n"
                answer = answer + "/status - состоние OPI\n"
                answer = answer + "\n"
                bot.sendMessage(chat_id, answer)
                
        elif command.find('/getimage') != -1 :
                getImage()
                image = open('img1.png', 'rb')
                bot.sendPhoto(chat_id, image)
                
        elif command.find('/getvideo') != -1 :                
                answer = 'Видосики не работат.\n'
                answer = answer + 'Спасибо за понимание.'
                bot.sendMessage(chat_id, answer)
                
        elif command.find('/status') != -1 :
                answer = getStatus()
                bot.sendMessage(chat_id, answer)
        else:
                answer = 'Нет такой команды.\n'
                answer = answer + '/help - помощь'
                bot.sendMessage(chat_id, answer)

                
bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot, action).run_as_thread()

bot.sendMessage(CHAT_ID_GROUP, 'OrangePi Запущен в {}'.format(getTimeDate()))

#---end bot start moving---

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
cap.set(cv2.CAP_PROP_FOURCC, fourcc)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
codec = cv2.VideoWriter_fourcc(*'MJPG')



ret, frame1 = cap.read()
ret, frame2 = cap.read()

movingDetected = False
messageSended = False
videoNum = 0

timeLastSend = time.time()

while(1):        
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations = 3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
                (x, y, h, w) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) < 2000:
                        continue
                frame = copy.deepcopy(frame2)
                cv2.rectangle(frame, (x, y), (x+h, y+w), (0, 255, 0), 2)
                movingDetected = True



        if len(contours) == 0 :
                movingDetected = False
                messageSended = False
        if (movingDetected and not messageSended and (time.time() - timeLastSend > 100)):
                cv2.imwrite('img_md.png', frame)
                image = open('img_md.png', 'rb')
                bot.sendPhoto(CHAT_ID_GROUP, image)
                messageSended = True 
                
        
        cv2.imshow('frame1', frame2)
        frame1 = frame2
        ret, frame2 = cap.read()

        k = cv2.waitKey(5) & 0xff
        if k == 27:
                break
        prvs = next
cap.release()
cv2.destroyAllWindows()


        
