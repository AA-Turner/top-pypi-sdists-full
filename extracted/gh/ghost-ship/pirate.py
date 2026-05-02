#!/usr/bin/env python

from os import environ
from sys import argv

NOMAD_ADDR = environ['NOMAD_ADDR']
MONGO_URL = environ['TYK_MONGO_URL']
CONSUL_ADDR = environ['CONSUL_ADDR']
TYK_ADDR = environ['TYK_ADDR']
TYK_TOKEN = environ['TYK_TOKEN']

VERSION = '0.2.5'

from ghost_ship.job import Job
from ghost_ship.exception import *
from ghost_ship import tyk
from getopt import getopt
import logging 

usage = """Usage:

* Init a service

  $ ghost-ship run service-name --scale=4

* scale service to 2 containers

  $ ghost-ship scale service-name 2
 
* Upgrade service to version v2

  $ ghost-ship upgrade service-name v2
 
"""


def run(service_name, version):
  Job(service_name).initilize(version)

def scale(service_name, count):
  try:
    Job(service_name).scale(int(count))
  except:
    logging.error('Count must be int')
    exit(1)

def upgrade(service_name, version):
  Job(service_name).upgrade(version)

def version():
  print 'Ghost ship v%s' % VERSION

job_commands = dict(run=run, upgrade=upgrade, scale=scale, version=version)

def do(command, args):
  if command != 'version':
    info() 
  job_commands[command](*args)  

def info():
  logging.info('NOMAD_ADDR: %s ' %NOMAD_ADDR)
  logging.info('TYK_MONGO_URL: %s ' % MONGO_URL)
  logging.info('CONSUL_ADDR: %s ' % CONSUL_ADDR)
  logging.info('TYK_ADDR: %s ' % TYK_ADDR)
  logging.info('TYK_TOKEN: %s ' % TYK_TOKEN)

def main():
  try:
    if len(argv) >= 2:
      do(argv[1], argv[2:])
    else:
      print usage
  except JobNotFound as e:
    logging.error('Job not found: %s', e)
    exit(1)
  except GroupNotFound as e:
    logging.error('Job Group is not found: %s', e)
    exit(1)
  except UpgradeFail as e:
    logging.error('Job upgrade fail: %s', e)
    exit(1)
  except TykServiceNotFound as e:
    logging.error('Tyk service is not found: %s', e)
    exit(1)
  except TykReloadFailed as e:
    logging.error('Tyk reload was failed: %s', e)
    exit(1)
  except JobTemplateIsNotFound as e:
    logging.error('Job template is not found: %s', e)
    exit(1)

if __name__ == '__main__':
  main()
