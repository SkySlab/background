login as: pi
pi@192.168.0.90's password:
Linux DrivewaySecurityPi 4.14.50+ #1122 Tue Jun 19 12:21:21 BST 2018 armv6l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jul  7 20:14:23 2018 from 192.168.0.122
pi@DrivewaySecurityPi:~ $ ls
background  PiJuice  pijuice_config.JSON.old
pi@DrivewaySecurityPi:~ $ cd background/
pi@DrivewaySecurityPi:~/background $ ls
cleandir.sh  motionalert.py  motionvid.py  motionvid.py.old  noticeshutdown.py  noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ nano config.json
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 44, in <module>
    forecast_text = forecast.text
AttributeError: 'list' object has no attribute 'text'
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
  File "./noticeup.py", line 45
    f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
    ^
IndentationError: expected an indented block
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
  File "./noticeup.py", line 45
    f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
    ^
IndentationError: expected an indented block
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 75, in <module>
    body2 = "I am currently " + cpu_temp + "while the ambient temperature is " + Ambient + "\n\n"
TypeError: cannot concatenate 'str' and 'float' objects
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 75, in <module>
    body2 = "I am currently ", cpu_temp + "while the ambient temperature is " + Ambient + "\n\n"
TypeError: cannot concatenate 'str' and 'float' objects
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 76, in <module>
    body3 = " while the ambient temperature is " + Ambient + "\n\n"
TypeError: cannot concatenate 'str' and 'float' objects
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 77, in <module>
    body = body1 + body2 + body3
TypeError: coercing to Unicode: need string or buffer, tuple found
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 59, in <module>
    cpu_temp = str.getCPUtemperature()
AttributeError: type object 'str' has no attribute 'getCPUtemperature'
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ sudo nano /etc/rc.local
pi@DrivewaySecurityPi:~/background $ ls
cleandir.sh  config.json  motionalert.py  motionvid.py  motionvid.py.old  noticeshutdown.py  noticeup.py
pi@DrivewaySecurityPi:~/background $ cat noticeup.py
import smtplib, os, glob, time, datetime, urllib2, json, httplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders
from weather import Weather, Unit

# Import weather_underground and Thingspeak keys
with open('/home/pi/background/config.json') as config_file:
        user_config = json.load(config_file)
        wu_api = user_config['weather_underground_api']
        ts_api = user_config['thingspeak_api']

# get the current temperature
def getAmbient():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        currentTemp_c = parsed_json['current_observation']['temp_c']
        return(currentTemp_c)
        f.close()

#get the forecast for today
def getForecastToday():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        todayCondition = parsed_json['forecast']['txt_forecast']['forecastday'][0]['fcttext_metric']
        return(todayCondition)
        f.close()

# get the forecast for tonight
def getForecastTonight():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tonightCondition = parsed_json['forecast']['txt_forecast']['forecastday'][1]['fcttext_metric']
        return(tonightCondition)
        f.close()

# get the forecast for tomorrow
def getForecastTomorrow():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tomorrowCondition = parsed_json['forecast']['txt_forecast']['forecastday'][2]['fcttext_metric']
        return(tomorrowCondition)
        f.close()

# get my own temperature
def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))

# define message parameters and create the container

cpu_temp = str(getCPUtemperature()) + " C"
Ambient = str(getAmbient()) + " C"
forecastToday = getForecastToday()
forecastTonight = getForecastTonight()
forecastTomorrow = getForecastTomorrow()
current_year = datetime.date.today().strftime("%Y")
month_of_year = datetime.date.today().strftime("%B")
day_of_month = datetime.date.today().strftime("%d")
day_of_week = datetime.date.today().strftime("%A")
fromaddr = "baileys2611@gmail.com"
toaddr = "baileys2611@gmail.com"
msg = MIMEMultipart()
msg['From'] = 'baileys2611@gmail.com'
msg['To'] = 'baileys2611@gmail.com'
msg['Subject'] = "Motion Cam Started"
body1 = "Good morning!<br><br>Today is " + day_of_week + ", " + day_of_month + " of " + month_of_year + " " + current_year + ".<br><br>The forecast for Canberra is:<br>Today : " + forecastToday + "<br>Tonight : " + forecastTonight + "<br>Tomorrow : " + forecastTomorrow + "<br><br>"
body2 = "I am currently " + cpu_temp + " while the ambient temperature is " + Ambient
body = body1 + body2
msg.attach(MIMEText(body, 'html'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('baileys2611@gmail.com', 'tlhmdllkhvbeffug')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ sudo nano /etc/rc.local
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
  File "./noticeup.py", line 82
    part1 = MIMEText(html_1, 'html'))
                                    ^
SyntaxError: invalid syntax
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ sudo service motion stop
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
42.2
42.2C
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
37.9
<type 'str'>
37.4C
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
37.4
<type 'str'>
^[[A37.4C
^[[A^[[A^[[A^[[A^[[A^[[A^[[A^[[Api@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 59, in <module>
    cpu_temp = int(getCPUtemperature())
ValueError: invalid literal for int() with base 10: '36.9'
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
37.4
<type 'float'>
36.9C
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
  File "./noticeup.py", line 87
    Ambient = get TheColour(Ambient) + str(getAmbient()) + "C"
                          ^
SyntaxError: invalid syntax
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 95, in <module>
    msg['Subject'] = "Motion Cam Started at " + str(datetime.now())
AttributeError: 'module' object has no attribute 'now'
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ cat noticeup.py
import smtplib, os, glob, time, datetime, urllib2, json, httplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders
from weather import Weather, Unit

# Import weather_underground and Thingspeak keys
with open('/home/pi/background/config.json') as config_file:
        user_config = json.load(config_file)
        wu_api = user_config['weather_underground_api']
        ts_api = user_config['thingspeak_api']

# get the current temperature
def getAmbient():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        currentTemp_c = parsed_json['current_observation']['temp_c']
        return(currentTemp_c)
        f.close()

#get the forecast for today
def getForecastToday():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        todayCondition = parsed_json['forecast']['txt_forecast']['forecastday'][0]['fcttext_metric']
        return(todayCondition)
        f.close()

# get the forecast for tonight
def getForecastTonight():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tonightCondition = parsed_json['forecast']['txt_forecast']['forecastday'][1]['fcttext_metric']
        return(tonightCondition)
        f.close()

# get the forecast for tomorrow
def getForecastTomorrow():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tomorrowCondition = parsed_json['forecast']['txt_forecast']['forecastday'][2]['fcttext_metric']
        return(tomorrowCondition)
        f.close()

# get my own temperature
def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))

# get our parts assigned to variables

cpu_temp = float(getCPUtemperature())
Ambient = float(getAmbient())
forecastToday = getForecastToday()
forecastTonight = getForecastTonight()
forecastTomorrow = getForecastTomorrow()
current_year = datetime.date.today().strftime("%Y")
month_of_year = datetime.date.today().strftime("%B")
day_of_month = datetime.date.today().strftime("%d")
day_of_week = datetime.date.today().strftime("%A")
fromaddr = "baileys2611@gmail.com"
toaddr = "baileys2611@gmail.com"

recipients = ['baileys2611@gmail.com', 'abailey73@gmail.com']

# colour the numbers dependant on value
def getTheColour(number):
        if (number <= 10):
                span_colour = "<span sytle=color:blue>"
        elif (number > 10) and (number <= 25):
                span_colour = "<span style=color:olive>"
        elif (number > 25) and (number <= 35):
                span_colour = "<span style=color:orange>"
        else:
                span_colour = "<span style=color:red>"
        return(span_colour)


# make the email

cpu_temp = getTheColour(cpu_temp) + str(getCPUtemperature()) + "C"
Ambient = getTheColour(Ambient) + str(getAmbient()) + "C"

msg = MIMEMultipart('alternative')

msg['From'] = 'baileys2611@gmail.com'
msg['To'] = ", ".join(recipients)
msg['Subject'] = "Motion Cam Started at " + time.strftime("%H:%M") + " on " + time.strftime("%d/%m/%Y")

html_1 = "<html><head></head><body>Good morning!<br><br>Today is " + day_of_week + ", " + day_of_month + " of " + month_of_year + " " + current_year + ".<br><br>The forecast for Canberra is:<br>Today : " + forecastToday + "<br>Tonight : " + forecastTonight + "<br>Tomorrow : " + forecastTomorrow + "<br><br>"
html_2 = "I am currently " + cpu_temp + "</span> while the ambient temperature is <span style=color:blue>" + Ambient + "</span>.</body></html>"

text = ""

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html_1 + html_2, 'html')

msg.attach(part1)
msg.attach(part2)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('baileys2611@gmail.com', 'tlhmdllkhvbeffug')
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
  File "./noticeup.py", line 47
    def getTomorrowsHigh():
      ^
IndentationError: expected an indented block
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 112, in <module>
    html_1 = "<html><head></head><body>Good morning!<br><br>Today is " + day_of_week + ", " + day_of_month + " of " + month_of_year + " " + current_year + ".<br><br>The forecast for Canberra is:<br>Today : " + getTodaysColour + forecastToday + "</span><br>Tonight : " + forecastTonight + "<br>Tomorrow : " + forecastTomorrow + "<br><br>"
TypeError: cannot concatenate 'str' and 'function' objects
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 112, in <module>
    html_1 = "<html><head></head><body>Good morning!<br><br>Today is " + day_of_week + ", " + day_of_month + " of " + month_of_year + " " + current_year + ".<br><br>The forecast for Canberra is:<br>Today : " + getTodaysColour() + forecastToday + "</span><br>Tonight : " + forecastTonight + "<br>Tomorrow : " + forecastTomorrow + "<br><br>"
  File "./noticeup.py", line 39, in getTodaysColour
    todayColour = str(getTheColour(float(parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['celcius'])))
KeyError: 'celcius'
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
Traceback (most recent call last):
  File "./noticeup.py", line 112, in <module>
    html_1 = "<html><head></head><body>Good morning!<br><br>Today is " + day_of_week + ", " + day_of_month + " of " + month_of_year + " " + current_year + ".<br><br>The forecast for Canberra is:<br>Today : " + getTodaysColour() + forecastToday + "</span><br>Tonight : " + forecastTonight + "<br>Tomorrow : " + forecastTomorrow + "<br><br>"
  File "./noticeup.py", line 39, in getTodaysColour
    todayColour = str(getTheColour(float(parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['celcius'])))
KeyError: 'celcius'
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
<span sytle=color:blue>
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
<span sytle=color:blue>
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeup.py
pi@DrivewaySecurityPi:~/background $ python ./noticeup.py
pi@DrivewaySecurityPi:~/background $ ls
cleandir.sh  config.json  motionalert.py  motionvid.py  motionvid.py.old  noticeshutdown.py  noticeup.py
pi@DrivewaySecurityPi:~/background $ rm noticeshutdown.py
pi@DrivewaySecurityPi:~/background $ ls
cleandir.sh  config.json  motionalert.py  motionvid.py  motionvid.py.old  noticeup.py
pi@DrivewaySecurityPi:~/background $ cp noticeup.py noticeshutdown.py
pi@DrivewaySecurityPi:~/background $ ls
cleandir.sh  config.json  motionalert.py  motionvid.py  motionvid.py.old  noticeshutdown.py  noticeup.py
pi@DrivewaySecurityPi:~/background $ nano noticeshutdown.py
pi@DrivewaySecurityPi:~/background $ python ./noticeshutdown.py
pi@DrivewaySecurityPi:~/background $ sudo crontab -e
No modification made
pi@DrivewaySecurityPi:~/background $ pwd
/home/pi/background
pi@DrivewaySecurityPi:~/background $ cat /etc/rc.local
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

sudo /usr/bin/python /home/pi/PiJuice/Software/Test/wakeup_enable.py
/usr/bin/python /home/pi/background/noticeup.py

exit 0
pi@DrivewaySecurityPi:~/background $ sudo crontab -e
crontab: installing new crontab
pi@DrivewaySecurityPi:~/background $ ls
cleandir.sh  config.json  motionalert.py  motionvid.py  motionvid.py.old  noticeshutdown.py  noticeup.py
pi@DrivewaySecurityPi:~/background $ nano config.json
pi@DrivewaySecurityPi:~/background $ nano motionvid.py
pi@DrivewaySecurityPi:~/background $ cat noticeup.py
import smtplib, os, glob, time, datetime, urllib2, json, httplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders
from weather import Weather, Unit

# Import weather_underground and Thingspeak keys
with open('/home/pi/background/config.json') as config_file:
        user_config = json.load(config_file)
        wu_api = user_config['weather_underground_api']
        ts_api = user_config['thingspeak_api']

# get the current temperature
def getAmbient():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        currentTemp_c = parsed_json['current_observation']['temp_c']
        return(currentTemp_c)
        f.close()

#get the forecast for today
def getForecastToday():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        todayCondition = parsed_json['forecast']['txt_forecast']['forecastday'][0]['fcttext_metric']
        return(todayCondition)
        f.close()

# get the maximum for today and set the colour
def getTodaysColour():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        todayColour = str(getTheColour(float(parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'])))
        return(todayColour)
        f.close()

# get the low for tonight and set the colour
def getTonightsColour():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tonightsColour = str(getTheColour(float(parsed_json['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'])))
        return(tonightsColour)
        f.close()

# get the high for tomorrow and set the colour
def getTomorrowsColour():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tomorrowsColour = str(getTheColour(float(parsed_json['forecast']['simpleforecast']['forecastday'][1]['high']['celsius'])))
        return(tomorrowsColour)
        f.close()

# get the forecast for tonight
def getForecastTonight():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tonightCondition = parsed_json['forecast']['txt_forecast']['forecastday'][1]['fcttext_metric']
        return(tonightCondition)
        f.close()

# get the forecast for tomorrow
def getForecastTomorrow():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tomorrowCondition = parsed_json['forecast']['txt_forecast']['forecastday'][2]['fcttext_metric']
        return(tomorrowCondition)
        f.close()

# get my own temperature
def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))

# colour the numbers dependant on value, used for forecast and ambient temperature.
# CPU temperature colour should be different as tolerance is different.
def getTheColour(number):
        if (number <= 10):
                span_colour = "<span style=color:blue>"
        elif (number > 10) and (number <= 25):
                span_colour = "<span style=color:olive>"
        elif (number > 25) and (number <= 35):
                span_colour = "<span style=color:orange>"
        else:
                span_colour = "<span style=color:red>"
import smtplib, os, glob, time, datetime, urllib2, json, httplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders
from weather import Weather, Unit

# Import weather_underground and Thingspeak keys
with open('/home/pi/background/config.json') as config_file:
        user_config = json.load(config_file)
        wu_api = user_config['weather_underground_api']
        ts_api = user_config['thingspeak_api']
        google_key = user_config['google_application_key']

# get the current temperature
def getAmbient():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        currentTemp_c = parsed_json['current_observation']['temp_c']
        return(currentTemp_c)
        f.close()

#get the forecast for today
def getForecastToday():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        todayCondition = parsed_json['forecast']['txt_forecast']['forecastday'][0]['fcttext_metric']
        return(todayCondition)
        f.close()

# get the maximum for today and set the colour
def getTodaysColour():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        todayColour = str(getTheColour(float(parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'])))
        return(todayColour)
        f.close()

# get the low for tonight and set the colour
def getTonightsColour():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tonightsColour = str(getTheColour(float(parsed_json['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'])))
        return(tonightsColour)
        f.close()

# get the high for tomorrow and set the colour
def getTomorrowsColour():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tomorrowsColour = str(getTheColour(float(parsed_json['forecast']['simpleforecast']['forecastday'][1]['high']['celsius'])))
        return(tomorrowsColour)
        f.close()

# get the forecast for tonight
def getForecastTonight():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tonightCondition = parsed_json['forecast']['txt_forecast']['forecastday'][1]['fcttext_metric']
        return(tonightCondition)
        f.close()

# get the forecast for tomorrow
def getForecastTomorrow():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/canberra.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        tomorrowCondition = parsed_json['forecast']['txt_forecast']['forecastday'][2]['fcttext_metric']
        return(tomorrowCondition)
        f.close()

# get my own temperature
def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))

# colour the numbers dependant on value, used for forecast and ambient temperature.
# CPU temperature colour should be different as tolerance is different.
def getTheColour(number):
        if (number <= 10):
                span_colour = "<span style=color:blue>"
        elif (number > 10) and (number <= 25):
                span_colour = "<span style=color:olive>"
        elif (number > 25) and (number <= 35):
                span_colour = "<span style=color:orange>"
        else:
                span_colour = "<span style=color:red>"
        return(span_colour)

# colour the number of the CPU temperature.
def getTheCPUColour(number):
        if (number <= 10):
                span_colour = "<span style=color:blue>"
        elif (number > 10) and (number <= 35):
                span_colour = "<span style=color:olive>"
        elif (number > 35) and (number <= 55):
                span_colour = "<span style=color:orange>"
        else:
                span_colour = "<span style=color:red>"
        return(span_colour)

# get our parts assigned to variables

cpu_temp = float(getCPUtemperature())
Ambient = float(getAmbient())
forecastToday = getForecastToday()
forecastTonight = getForecastTonight()
forecastTomorrow = getForecastTomorrow()
current_year = datetime.date.today().strftime("%Y")
month_of_year = datetime.date.today().strftime("%B")
day_of_month = datetime.date.today().strftime("%d")
day_of_week = datetime.date.today().strftime("%A")
fromaddr = "baileys2611@gmail.com"
toaddr = "baileys2611@gmail.com"

recipients = ['baileys2611@gmail.com', 'abailey73@gmail.com']

# make the email

cpu_temp = getTheCPUColour(cpu_temp) + str(getCPUtemperature()) + "C"
Ambient = getTheColour(Ambient) + str(getAmbient()) + "C"

msg = MIMEMultipart('alternative')

msg['From'] = 'baileys2611@gmail.com'
msg['To'] = ", ".join(recipients)
msg['Subject'] = "Motion Cam Started at " + time.strftime("%H:%M") + " on " + time.strftime("%d/%m/%Y")

html_1 = "<html><head></head><body>Good morning!<br><br>Today is " + day_of_week + ", " + day_of_month + " of " + month_of_year + " " + current_year + ".<br><br>"
html_1a = "The forecast for Canberra is:<br>Today : " + getTodaysColour() + forecastToday + "</span><br>Tonight : " + getTonightsColour() + forecastTonight + "</span><br>Tomorrow : " + getTomorrowsColour() + forecastTomorrow + "</span><br><br>"
html_2 = "I am currently " + cpu_temp + "</span> while the ambient temperature is " + Ambient + "</span>.</body></html>"

text = ""

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html_1 + html_1a + html_2, 'html')

msg.attach(part1)
msg.attach(part2)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('baileys2611@gmail.com', google_key)
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
