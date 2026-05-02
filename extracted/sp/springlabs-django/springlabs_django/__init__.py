import logging

__version__ = "0.3.5"
DEBUG = True

PROJECT_NAME = "Springlabs Django Manager"
PROJECT_PACKAGE = "springlabs_django"
CONFIG_JSON = "springlabs_django.json"
LOG_NAME = "../springlabs_django.log"

format_log = '[%(asctime)s] [%(levelname)s] :: (%(process)d) :: (%(filename)s - %(funcName)s - %(lineno)d ) :: %(message)s'

logging.basicConfig(filename=LOG_NAME,
    format=format_log,
    level = logging.INFO if DEBUG == False else logging.DEBUG)
