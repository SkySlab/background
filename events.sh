#! /bin/bash

EVENTS_FILE=/home/pi/background/eventscounter.txt

EVENTS_COUNTER=$(/bin/cat $EVENTS_FILE)

((EVENTS_COUNTER++))

echo $EVENTS_COUNTER > $EVENTS_FILE
