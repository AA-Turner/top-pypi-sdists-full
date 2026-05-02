from configparser import ConfigParser

import os

_CFG_FILENAME = 'capstone.ini'

_DB_SECTION = 'database'
_DB_HOST_OPT = 'host'
_DB_PORT_OPT = 'port'
_DB_NAME_OPT = 'database'
_DB_USERNAME_OPT = 'user'
_DB_PASSWORD_OPT = 'password'

DB_HOST = None
DB_PORT = None
DB_NAME = None
DB_USERNAME = None
DB_PASSWORD = None

_AV_SECTION = 'alphavantage'
_AV_APIKEY_OPT = 'apikey'

AV_APIKEY = None


def load_config():

    global DB_HOST
    global DB_PORT
    global DB_NAME
    global DB_USERNAME
    global DB_PASSWORD

    global AV_APIKEY

    DB_HOST = '35.232.238.193'
    DB_PORT = '5432'
    DB_NAME = 'capstone'
    DB_USERNAME ='postgres'
    DB_PASSWORD = '12341234'

    AV_APIKEY = '4F9G7E51ZEMJ6L2B'
    '''
    parser = ConfigParser()

    full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), _CFG_FILENAME)

    print(__file__)
    print(full_path)

    parser.read(full_path)

    DB_HOST = parser.get(_DB_SECTION, _DB_HOST_OPT)
    DB_PORT = parser.get(_DB_SECTION, _DB_PORT_OPT)
    DB_NAME = parser.get(_DB_SECTION, _DB_NAME_OPT)
    DB_USERNAME = parser.get(_DB_SECTION, _DB_USERNAME_OPT)
    DB_PASSWORD = parser.get(_DB_SECTION, _DB_PASSWORD_OPT)

    AV_APIKEY = parser.get(_AV_SECTION, _AV_APIKEY_OPT)
    '''

def get_database_items():

    return {
        _DB_HOST_OPT: DB_HOST,
        _DB_PORT_OPT: DB_PORT,
        _DB_NAME_OPT: DB_NAME,
        _DB_USERNAME_OPT: DB_USERNAME,
        _DB_PASSWORD_OPT: DB_PASSWORD
    }


load_config()

