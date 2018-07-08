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
