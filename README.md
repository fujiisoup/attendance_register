# Automatic attendance logging for Kyoto university

This script enables the attendance logging automatically.

+ the time unlock your computer for the first time in each day is the *arrival time*
+ the time you lock the screen last time in each day is the *departure time*

## Limitation

This script only works in ubuntu/debian computers and only in KUINS network.  
Only one OS-dependent part is [login_monitor.sh](./login_monitor.sh), which detects the screen lock / unlock and start a python script [send_login_log.py](./send_login_log.py).  
The python script should work in any OS, but not the shell script. Any contribution is wellcome.

This script cannot know when is the last screen lock until the end of the day.
Therefore, this cannot click the *depature* botton in time.
Instead, it just adds a note for the departure time.

## Motivation

I hate to do such a silly stuff every day.
Let's automate.

## Installation

### Requirement
#### Python
1. selenium: `pip install selenium`
2. gecko driver for firefox: downlad driver from https://github.com/mozilla/geckodriver/releases and copy it under `/usr/local/bin/`

### Account information
3. put your account information in the same directory of the script  
This account file should be named as `kyoto-u.account`
The first line should be your SPS-ID, (e.g. taro123yamada) and the second line should be your password.

#### shell script
4. Register this script in your startup, e.g., `.bashrc`.  
Note that this script automatically terminates if another instance is already running.
Therefore it may be safer to execute this script every login.

I added the following line to `.bashrc`,
```
~/automation/login_monitor.sh &
```
(I put these scripts in `~/automation/`)
