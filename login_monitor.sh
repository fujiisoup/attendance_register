#!/bin/bash

LOGFILE=login_logout.csv
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

# exit if another instance of this script is running
for pid in $(pidof -x `basename $0`); do
   [ $pid != $$ ] && { exit 1; }
done

dbus-monitor --session "type='signal',interface='org.gnome.ScreenSaver'" |
  while read x; do
    case "$x" in 
      *"boolean true"*) 
        echo SCREEN_LOCKED "$(date +%Y%m%d%H%M%S)" >> $LOGFILE;;
      *"boolean false"*) 
        echo SCREEN_UNLOCKED "$(date +%Y%m%d%H%M%S)" >> $LOGFILE
        python send_login_log.py 'login_logout.csv' 'kyoto-u.account' 'false'
      ;;
    esac
    sleep 1
  done
