import re
import time
import wiringpi
from wiringpi import GPIO

from opigallus import *
from opigallus.display import ssd1306
from opigallus.draw import canvas
from PIL import ImageFont, ImageDraw
from subprocess import Popen, PIPE

FAN_PIN = 17

def getCmdOut(cmd=""):
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
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

def getCpuLoad():
    out = getCmdOut('cat /proc/loadavg')
    match = re.findall(r'\d*\.\d+|d+', out)
    if not match:
        return 0
    return match[0]

wiringpi.wiringPiSetup()
wiringpi.pinMode(FAN_PIN, GPIO.OUTPUT)
wiringpi.softPwmCreate(FAN_PIN, 0, 100)

disp = ssd1306(port=3, address=0x3c, width=128, height=64)
while True:
    if float(getCpuTemperature()) > 47 :
        wiringpi.softPwmWrite(FAN_PIN, 100)
    elif float(getCpuTemperature()) > 45 :
        wiringpi.softPwmWrite(FAN_PIN, 75)
    elif float(getCpuTemperature()) > 43 :
        wiringpi.softPwmWrite(FAN_PIN, 50)
    elif float(getCpuTemperature()) > 41 :
        wiringpi.softPwmWrite(FAN_PIN, 25)
    else :
        wiringpi.softPwmWrite(FAN_PIN, 0)

        
    
    time.sleep(0.25)
    
    with canvas(disp) as draw:
        font = ImageFont.load_default()
        font = ImageFont.truetype('/oled', size = 18) ## отсюда www.dafont.com/bitmap.php
        draw.rectangle((0,0,128,64), outline =0, fill=0)
        memory = getMemLoad()
        lines = [
            'CPU t:   {} °C'.format(getCpuTemperature()),
            'M:  {} / {} M'.format(memory['Used'], memory['Total']),
            'Load:  {} %'.format(getCpuLoad())
            ]        
        draw.text((0,0), lines[0], font=font, fill=255)
        draw.text((0,22), lines[1],font=font, fill=255)
        draw.text((0,44), lines[2],font=font, fill=255)


