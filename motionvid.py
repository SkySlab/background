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
        location = user_config['location'] + ".json"
        fromaddr = user_config['fromaddr']
        toaddr = user_config['toaddr']
        google_login = user_config['google_login']

# get the ambient temperature
def getAmbient():
        f = urllib2.urlopen('http://api.wunderground.com/api/' + wu_api + '/conditions/forecast/q/' + location)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        currentTemp_c = parsed_json['current_observation']['temp_c']
        return(currentTemp_c)
        f.close()

# define message parameters and create the container

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Motion Cam Activated"
body = "Video of Motion Detected"
msg.attach(MIMEText(body, 'plain'))

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
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
