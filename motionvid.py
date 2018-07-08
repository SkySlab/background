import smtplib, os, glob, time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders

time.sleep(5) # wait for 5 seconds to finish video encoding

# define message parameters and create the container

fromaddr = "baileys2611@gmail.com"
toaddr = "baileys2611@gmail.com"
msg = MIMEMultipart()
msg['From'] = 'baileys2611@gmail.com'
msg['To'] = 'baileys2611@gmail.com'
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
server.login('baileys2611@gmail.com', 'tlhmdllkhvbeffug')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
