# Background
These scripts perform various background tasks using a Raspberry pi installed with Motion for security camera monitoring.  Tested with a Raspberry pi 1.2 B and B+, 3B and B+.  Tasks include:
1. Send an email when starting with the local weather conditions for today, tonight and tomorrow.
2. Record a picture, video on detecting motion and then send an email notification with the picture and video attached (along with local environmental conditions and some statistics).
3. Clean out the directory that stores the video and picture files each morning (allowing recovery overnight but need to recover disk space for continued operation).
4. Shut down the motion service at 20.00 each night, sending an email before shutting down with environmental conditions and statistics for the day.

## Configuration for motion and security camera
Each shell script has to be given executable permission:
```
chmod +777 *.sh
```

### Rc.local 
This has to be modified to reset the counter on startup and run the startup python script:
```
sudo /usr/bin/python /home/pi/background/noticeup.py
echo 0 > /home/pi/background/dailycountervalue.dat
```

### Cron 
Cron calls startup and shutdown scripts to start and stop  the motion service.  Here is an example that will:
1. At 08.05, call the cleandir script (which just cleans out the files in a directory).
2. At 07.30, call the noticeup.py script starting the motion service, sending an email with today's weather and some stats. 
3. At 20.30, call the notiiceshutdown.py script, stopping the motion service, sending an email stating as such with some weather stuff and stats.

Because I'm having 'issues' trying to get the autobrightness working to take into account the fluctuation of light during the day, I have to add a line that restarts motion frequently during the day.

```
05 08 * * * /bin/bash /home/pi/background/cleandir.sh > /dev/null 2>&1
30 07 * * * /usr/bin/python /home/pi/background/noticeup.py
30 20 * * * /usr/bin/python /home/pi/background/noticeshutdown.py
00 09,10,12,14,16,17,18,19 * * * sudo service motion restart
```

...and if you're using the weaved connected service (from remot3.it) then include
```
@reboot /usr/bin/wevedstart.sh
```

### Config.json
The config.json file needs to be edited with user keys, logon for google, location, email addresses both to and from.  Location needs to correspond to WeatherUnderground location names as all the forecast and temperature data (other than CPU temperature) is called using the WeatherUnderground API.

### Motion.conf
The Motion configuration file must be edited to include actions triggered after an event has occurred.  Motion.conf file is located at /etc/motion/motion.conf (for version 4 of motion that is) and the following configuration items are required:
```
target_dir /var/lib/motion
on_movie_end python /home/pi/background/motionvid.py
```

I have included an example motion.conf in the library which seems to work well.  It has to be located at /etc/motion/ and must be named motion.conf.  I've also had some permissions issues WRT writing and reading files, so choose the most appropriate method desired to make sure that the motion user has access to /var/lib/motion and /home/pi/background and /etc/motion (where the config file needs to reside).

### SCP and paramiko
Still to get this working.  The problem is how to run a script in motion as another user.  The motion user is installed by default and it does not have an ssh key associated with the scp function, so this needs to be sorted somehow and until I find a solution this needs to be commented out.

These need to be installed for ssh transfer to work.
```
sudo apt-get install libffi-dev
sudo pip install scp
```

Don't forget to ssh into the server (as root!) at least once before you try to scp any files or the scripts will fail as the known-hosts file gets updated after ssh-ing to the server in question.

### Install Motion and some other useful stuff

The steps:

1. Pre-set the Rpi to install motion and recognise the raspi-camera as a usb camera.
```
sudo apt-get update
sudo apt-get upgrade
sudo rpi-update
sudo apt-get install motion -y
sudo modprobe bcm2835-v4l2
```
reboot
```
sudo apt-get install htop
```

2. Install weavedconnect from Remot3.it.

```
sudo apt-get install weavedconnectd
sudo weavedinstaller
```
Then set the ssh port as default and 8081 port as http server.

3. Modify Motion.conf.
4. Install python and packages
```
sudo apt-get install python
sudo apt-get install python-pip
```

5. Install the scripts
6. Make the motion log directory
```
sudo mkdir /var/log/motion
```
7. Start motion once using the config file
```
sudo motion -c /etc/motion/motion.conf
```
8. Add the motion user to the correct permissions to allow creating and deleting files.
9. Modify /etc/rc.local
9. Install sudo crontab
