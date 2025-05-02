#!/usr/bin/env python
#234567891123456789212345678931234567894123456789512345678961234567897123456789
# encoding: utf-8


from pytz import reference
import time
import colorlog
import datetime
import logging
import os
import sys

# get root logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# console handler gets all log entries
ch = logging.StreamHandler() # defaults to sys.stderr

log.addHandler(ch)


formatstr = '%(asctime)s.%(msecs)03d [%(levelname)-.4s] %(message)s'
datefmt = '%Y-%m-%dT%H:%M:%S'

localtime = reference.LocalTimezone()
if localtime.tzname(datetime.datetime.now()) == 'UTC':
    # UTC time, just append Z
    formatstr = '%(asctime)s.%(msecs)03dZ [%(levelname)-.4s] %(message)s'
else:
    # not UTC, append offset of local system time
    minute = (time.localtime().tm_gmtoff / 60) % 60
    hour = ((time.localtime().tm_gmtoff / 60) - minute) / 60
    utcoffset = "%.2d%.2d" %(hour, minute)
    if utcoffset[0] != '-':
        utcoffset = '+' + utcoffset
    formatstr = '%(asctime)s.%(msecs)03d' + utcoffset + ' [%(levelname)-.4s] %(message)s'

colorFormatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s' + formatstr, datefmt=datefmt
)

formatter = logging.Formatter(
    fmt=formatstr,
    datefmt=datefmt
)

log.notice = log.info

if sys.stdout.isatty():
    ch.setFormatter(colorFormatter)
else:
    ch.setFormatter(formatter)

# log to syslog if env var is setup
if os.environ.get('LOG_TO_SYSLOG',False):

    # default to UDP if no socket found
    address = ('localhost', 514)

    from logging.handlers import SysLogHandler

    locations = [
        "/var/run/syslog",  # osx
        "/dev/log",         # linux
        "/var/run/log"      # freebsd
    ]

    for p in locations:
        if os.path.exists(p):
            address = p

    slh = SysLogHandler(address=address)
    syslogFormatter = logging.Formatter('%(message)s')
    slh.setFormatter(syslogFormatter)
    log.addHandler(slh)

def panic(msg):
    log.critical(msg)
    sys.exit(1)

log.panic = panic
log.die = panic
