import configparser
import sys
import os
from os.path import expanduser

ACCESS_TOKEN = 'accessToken'
REFRESH_TOKEN = 'refreshToken'
VOLUME = 'volume'
DEVICE_NAME = 'deviceName'
CLIENT_SECRET = 'clientSecret'
CLIENT_ID = 'clientId'

TOKEN_SECTION = 'token'
APP_SECTION = 'app'

CONFIG_FILE_PATH = '~/.config/spotipy-cli/spotipy-clirc'


class Config:
    configLocation = expanduser(CONFIG_FILE_PATH)
    clientId = ''
    clientSecret = ''

    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read(self.configLocation)
        if len(parser.sections()) == 0:
            parser.add_section(APP_SECTION)
            sys.stdout.write("No configuration found. Follow the instructions at "
                             "https://developer.spotify.com/documentation/general/guides/app-settings/ and provide "
                             "obtained values. Set the redirect URL to http://localhost:9999/callback\n")
            parser[APP_SECTION][CLIENT_ID] = input("Client ID: ")
            parser[APP_SECTION][CLIENT_SECRET] = input("Client Secret: ")
            parser[APP_SECTION][DEVICE_NAME] = input("Name of the device to control: ")
            parser[APP_SECTION][VOLUME] = input("Set volume to: ")
            parser.add_section(TOKEN_SECTION)
            path = os.path.dirname(self.configLocation)
            os.makedirs(path, exist_ok=True)
            with open(self.configLocation, 'w') as configfile:
                parser.write(configfile)

        try:
            self.refreshToken = parser[TOKEN_SECTION][REFRESH_TOKEN]
            self.accessToken = parser[TOKEN_SECTION][ACCESS_TOKEN]
        except KeyError:
            pass

        try:
            self.clientId = parser[APP_SECTION][CLIENT_ID]
            self.clientSecret = parser[APP_SECTION][CLIENT_SECRET]
            self.deviceName = parser[APP_SECTION][DEVICE_NAME]
            self.volume = parser[APP_SECTION][VOLUME]
        except KeyError:
            sys.stderr.write('Invalid config file found: {}\n'.format(self.configLocation))
            sys.exit()

    def store_token(self, token_type, token):
        self.__store_config(TOKEN_SECTION, token_type, token)

        if token_type == REFRESH_TOKEN:
            self.refreshToken = token
        elif token_type == ACCESS_TOKEN:
            self.accessToken = token

    def __store_config(self, section, config, value):
        parser = configparser.ConfigParser()
        parser.read(self.configLocation)
        if not parser.has_section(section):
            parser.add_section(section)
        parser[section][config] = value
        with open(self.configLocation, 'w') as configfile:
            parser.write(configfile)
