# Background
Background tasks to perform in various raspberry pi configurations

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

```
05 08 * * * /bin/bash /home/pi/background/cleandir.sh > /dev/null 2>&1
30 07 * * * /usr/bin/python /home/pi/background/noticeup.py
30 20 * * * /usr/bin/python /home/pi/background/noticeshutdown.py
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

I have included an example motion.conf in the library which seems to work well.  It has to be located at /etc/motion/ and must be named motion.conf
