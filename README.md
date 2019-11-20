# Automatic attendance logging for Kyoto university

With this script, the attendance logging is automatically made based on
+ arrival will be registered when unlock the screen of your computer for the first time in each day
+ departure time will be registered when you lock the screen last time in each day

## Limitation

This script only works in ubuntu/debian computers and only in KUINS network.

This script cannot know when is the last screen lock until the end of the day.
Therefore, this cannot click the `depature` botton.
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
4. Register this script in your startup, e.g., `.profile`.

I added the following line to `.profile`,
```
bash ~/automation/login_monitor.sh &
```
(I put these script in `~/automation/`)
