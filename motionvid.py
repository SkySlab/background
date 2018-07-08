import smtplib, os, glob, time, datetime, urllib2, json, httplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders

time.sleep(5) # wait for 5 seconds to finish video encoding

# read and store our secret keys
with open('/home/pi/background/config.json') as config_file:
        user_config = json.load(config_file)
        wu_api = user_config['weather_underground_api']
        ts_api = user_config['thingspeak_api']
        google_key = user_config['google_application_key']
        location = user_config['location']
        fromaddr = user_config['fromaddr']
        toaddr = user_config['toaddr']
        google_login = user_config['google_login']

# get the ambient temperature
def getAmbient():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/' + location + '.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        currentTemp_c = parsed_json['current_observation']['temp_c']
        return(currentTemp_c)
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

cpu_temp = getTheCPUColour(float(getCPUtemperature())) + str(getCPUtemperature()) + "C"
Ambient = getTheColour(float(getAmbient())) + str(getAmbient()) + "C"

# define message parameters and create the container

msg = MIMEMultipart('alternative')

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Motion detected at " + time.strftime("%H:%M") + " on " + time.strftime("%d/%m/%Y")

html_1 = "<html><head></head><body> The camera has been activated.<br><br>"
html_2 = "I am currently " + cpu_temp + "</span> while the ambient temperature is " + Ambient + "</span>.</body></html>"

text = ""

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html_1 + html_2, 'html')

msg.attach(part1)
msg.attach(part2)

# get the picture and video path and name
last_photo_taken = sorted(glob.glob("/var/lib/motion/*.jpg"),key=os.path.getmtime)[-1]
photo_name = os.path.basename(last_photo_taken)
last_video_taken = sorted(glob.glob("/var/lib/motion/*.avi"),key=os.path.getmtime)[-1]
video_name = os.path.basename(last_video_taken)

# attach the video to the email
attachment = open(last_video_taken, "rb")
part = MIMEBase('application', "octet-steam")
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % video_name)
msg.attach(part)

# attach the preview image to the email

attachment = open(last_photo_taken, "rb")
img = MIMEImage(attachment.read())
img.add_header('Content-Disposition', "attachment; filename= %s" % photo_name)
attachment.close()
msg.attach(img)

# send the email

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(google_login, google_key)
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
