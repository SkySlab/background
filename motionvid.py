import sys, smtplib, os, glob, time, datetime, urllib, urllib2, json, httplib, subprocess, shutil, paramiko
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders

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
        daily_counter_location = user_config['daily_counter_location']
        global_counter_location = user_config['global_counter_location']
        maximum_counter_location = user_config['max_counter_location']

# post to thingspeak
def post_ts():
        params = urllib.urlencode({'field1': daily_events, 'field2': getCPUtemperature(), 'field3': getAmbient(), 'key':ts_api})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

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

# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

cpu_temp = getTheCPUColour(float(getCPUtemperature())) + str(getCPUtemperature()) + "C"
Ambient = getTheColour(float(getAmbient())) + str(getAmbient()) + "C"

# read and increment the daily counter
def get_daily_events_value(filename=daily_counter_location):
    with open(filename, "r+") as f:
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        f.close()
    return val

# read and increment the global counter
def get_global_events_value(filename=global_counter_location):
    with open(filename, "r+") as f:
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        f.close()
    return val

# read and check the maximum daily events, update if this number of daily events is greater
# than the maximum daily events to date.
def get_max_events_value(maxfilename=maximum_counter_location, dailyfilename=daily_counter_location):
    with open(maxfilename, "r+") as a, open(dailyfilename, "r+") as b:
                maxval = int(a.read() or 0)
                dailyval = int(b.read() or 0)
                if (maxval > dailyval):
                        b.close()
                        a.close()
                        return maxval
                else:
                        maxval = dailyval
                        a.seek(0)
                        a.truncate()
                        a.write(str(maxval))
                        b.close()
                        a.close()
                        return dailyval

# Disk information
DISK_stats = getDiskSpace()
DISK_free = DISK_stats[2]

# define message parameters and create the container

daily_events = get_daily_events_value()
global_events = get_global_events_value()
maximum_events = get_max_events_value()

msg = MIMEMultipart('alternative')

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Motion detected at " + time.strftime("%H:%M") + " on " + time.strftime("%d/%m/%Y")

html_1 = "<html><head></head><body>"
html_1a = "The camera has been activated.<br><br>"
html_2 = "I am currently " + cpu_temp + "</span> while the ambient temperature is " + Ambient + "</span>.  I have " + DISK_free + " disk space remaining.<br><br>"
html_3 = "There have been " + str(daily_events) + " events today and " + str(global_events) + " events over the life of this camera. The maximum number of events in any day so far has been " + str(maximum_events) + ", which was on " + str(time.ctime(os.path.getmtime(maximum_counter_location))) + "."
html_3a = "<br><br>"
html_4 = "</body></html>"

text = ""

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html_1 + html_1a + html_2 + html_3 + html_3a + html_4, 'html')

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

# post to thingspeak
post_ts()

# now that the email is sent, stats updated, this portion of the script will place the
# updated files on to a server so that last known movements can be monitored

shutil.copy2(last_photo_taken, '/var/lib/motion/drivewaystill.jpg')
shutil.copy2(last_video_taken, '/var/lib/motion/drivewayvideo.avi')

ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect('192.168.0.124', username='admin', password='qx6&68#XER#e')
sftp = ssh.open_sftp()
sftp.put('/var/lib/motion/drivewaystill.jpg', '/share/Web/skyslab/stills/drivewaystill.jpg')
sftp.close()
ssh.close()

ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect('192.168.0.124', username='admin', password='qx6&68#XER#e')
sftp = ssh.open_sftp()
sftp.put('/var/lib/motion/drivewayvideo.avi', '/share/Web/skyslab/stills/drivewayvideo.avi')
sftp.close()
ssh.close()

# make sure that the python process exits and prevents handing processes if ther are errors
sys.exit(0)
