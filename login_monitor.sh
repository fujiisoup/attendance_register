LOGFILE=~/automation/login_logout.csv

dbus-monitor --session "type='signal',interface='org.gnome.ScreenSaver'" |
  while read x; do
    case "$x" in 
      *"boolean true"*) 
        echo SCREEN_LOCKED "$(date +%Y%m%d%H%M%S)" >> $LOGFILE
        python send_login_log.py kyoto-u.account false
      ;;
      *"boolean false"*) echo SCREEN_UNLOCKED "$(date +%Y%m%d%H%M%S)" >> $LOGFILE;;
    esac
  done