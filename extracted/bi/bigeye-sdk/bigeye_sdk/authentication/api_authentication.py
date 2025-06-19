from __future__ import annotations

import abc
import base64
import binascii
import configparser
import glob
import http.cookiejar
import json
import os
import sqlite3
import yaml
import sys
import tempfile
import urllib.parse
from os.path import exists
from pathlib import Path

import keyring
import lz4.block
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from pydantic.v1 import BaseModel
from pydantic.v1.dataclasses import dataclass
from requests.auth import HTTPBasicAuth

from bigeye_sdk.functions.aws import get_secret
from bigeye_sdk.authentication.enums import BrowserType, OperatingSystem
from bigeye_sdk.functions.file_functs import create_subdir_if_not_exists
from bigeye_sdk.exceptions import BrowserAuthException
from bigeye_sdk.log import get_logger
from bigeye_sdk.serializable import YamlSerializable

log = get_logger(__file__)

HOME_DIR = str(Path.home())
DEFAULT_CRED_FILE = os.path.join(HOME_DIR, '.bigeye', 'credentials.ini')
OLD_DEFAULT_CRED_FILE = os.path.join(HOME_DIR, '.bigeye', 'default_cred.json')



class AwsSecretIdentifier(BaseModel):
    secret_name: str
    aws_region: str


@dataclass
class ApiAuth(YamlSerializable):

    @abc.abstractmethod
    def get_auth_headers(self):
        pass

    @classmethod
    def load(cls, auth_file: str = None, workspace: str = 'DEFAULT') -> ApiAuth:
        auth_file = cls.find_user_credentials(auth_file)
        if os.path.isfile(auth_file):
            if auth_file.lower().endswith('.json'):
                return cls.load_from_json_file(auth_file)
            else:
                return cls.load_from_ini_file(auth_file,workspace)
        else:
            return cls.load_from_base64(auth_file)

    @classmethod
    def load_from_ini_file(cls, auth_file: str, workspace: str) -> ApiAuth:
        log.info(f'Loading API Conf: {auth_file}')
        cp = configparser.ConfigParser(default_section=None, interpolation=None)
        cp.read(auth_file)
        # Convert browser type to proper enum (config parser reads everything as strings)
        for key, value in cp[workspace].items():
            if key == 'browser':
                cp[workspace][key] = BrowserType[value]
        return cls.factory(cp[workspace])

    @classmethod
    def load_from_json_file(cls, file: str) -> ApiAuth:
        log.info(f'Loading API Conf: {file}')
        with open(file) as json_file:
            return cls.factory(yaml.safe_load(json_file))

    @classmethod
    def load_cred_from_aws_secret(cls, region_name: str, secret_name: str):
        log.info(f'Loading AWS Secret: {secret_name}')
        return cls.factory(get_secret(region_name=region_name,
                                              secret_name=secret_name))

    @classmethod
    def load_from_base64(cls, encoded: str):
        try:
            log.info("Loading API Conf")
            conf_dict = json.loads(base64.b64decode(encoded).decode('utf-8'))
            return cls.factory(conf_dict)
        except binascii.Error as e:
            log.error('Error decoding API configuration. Verify it is valid base64.')
            log.error(f'Error message: {e}')
            raise e
        
    @classmethod
    def save_as_file(cls, auth_filename: str, cred: ApiAuth, workspace: str) -> None:
        cp = configparser.ConfigParser(default_section=None, interpolation=None)
        if not auth_filename:
            auth_filename = cls.find_user_credentials(auth_filename)
        cp.read(auth_filename)
        cp[workspace] = cred.to_dict()
        with open(auth_filename, 'w+') as file:
            cp.write(file)

    @staticmethod
    def find_user_credentials(auth_filename: str) -> str:
        if auth_filename:
            return auth_filename
        elif 'BIGEYE_API_CRED_FILE' in os.environ:
            return os.environ['BIGEYE_API_CRED_FILE']
        elif os.path.exists(DEFAULT_CRED_FILE):
            return DEFAULT_CRED_FILE
        elif os.path.exists(OLD_DEFAULT_CRED_FILE):
            return OLD_DEFAULT_CRED_FILE
        else:
            create_subdir_if_not_exists(path=DEFAULT_CRED_FILE, includes_file=True)
            return DEFAULT_CRED_FILE

    @classmethod
    def find_and_parse_user_credentials(cls, auth_filename: str) -> configparser.ConfigParser:
        cp = configparser.ConfigParser(default_section=None, interpolation=None)
        cp.read(cls.find_user_credentials(auth_filename))
        return cp

    @staticmethod
    def factory(conf: dict) -> ApiAuth:
        ex: Exception

        for model_cls in [BasicAPIAuth, BrowserAPIAuth, APIKeyAuth]:
            try:
                return model_cls(**conf)
            except Exception as e:
                ex = e

        raise ex


@dataclass
class BasicAPIAuth(ApiAuth):
    """
    Credential models to bind required host and authentication details for data_modules runtimes.

    Attributes:
        base_url: str - the full url of the bigeye instance.
        user: str - the username to access bigeye.
        password: str - the user password to access bigeye.
    """
    base_url: str
    """Host URL for the Bigeye -- e.g. app.bigeye.com"""
    user: str
    """Basic Auth user for this host."""
    password: str
    """Basic Auth password for this host."""

    def get_auth_headers(self) -> dict:
        return {'auth': HTTPBasicAuth(self.user.lower(), self.password)}


@dataclass
class APIKeyAuth(ApiAuth):
    """
    Credential model for authenticating to Bigeye using a Personal API Key.

    Attributes:
        base_url: str - the full url of the bigeye instance.
        api_key: str - the full API Key provided by Bigeye.
    """
    base_url: str
    """Host URL for the Bigeye -- e.g. app.bigeye.com"""
    api_key: str
    """The full API Key provided by Bigeye"""

    def get_auth_headers(self) -> dict:
        auth_key: str = os.environ.get('BIGEYE_APIKEYAUTH_AUTH_HEADER_KEY', 'Authorization')
        return {auth_key: f'apikey {self.api_key}'}


@dataclass
class BrowserAPIAuth(ApiAuth):
    """
    Credential model to bind required host and auth details from browser cookies.

    Attributes:
        browser: BrowserType
        browser_profile_user_name: str - the username associated with the browser profile.
        base_url: str - the full url of the bigeye instance.
    """
    browser: BrowserType
    browser_profile_user_name: str = None
    base_url: str = "https://app.bigeye.com"

    def get_auth_headers(self) -> dict:
        return {'cookies': self.auth_factory().get_cookies()}

    def get_use_default_profile(self) -> bool:
        return False if self.browser_profile_user_name else True

    def get_domain_name(self) -> str:
        return self.base_url.split('//')[-1]

    def auth_factory(self) -> BrowserAuth:
        if self.browser == BrowserType.CHROME:
            return Chrome(api_conf=self)
        elif self.browser == BrowserType.CHROMIUM:
            return Chromium(api_conf=self)
        elif self.browser == BrowserType.FIREFOX:
            return Firefox(api_conf=self)


class BrowserAuth(abc.ABC):
    os: OperatingSystem

    def __init__(self):
        self.os = OperatingSystem.factory()

    @abc.abstractmethod
    def get_cookies(self):
        pass


class ChromiumBased(BrowserAuth):
    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16
    osx_user_cookie_file: str
    osx_local_state_file: str
    linux_user_cookie_file: str
    linux_local_state_file: str
    browser_profile_user_name: str
    browser: str
    domain_name: str
    _cookie_file: str = None
    _cookie_encryption_pass: str = None
    _iterations: int = None

    def __init__(self, api_conf: BrowserAPIAuth):
        super().__init__()
        self.browser_profile_user_name = api_conf.browser_profile_user_name
        self.browser = api_conf.browser.name
        self.domain_name = api_conf.get_domain_name()
        self._set_os_specific_attributes()

    def _set_os_specific_attributes(self):
        user_profile: str = self._get_user_profile()

        if self.os == OperatingSystem.MACOS:
            cookie_encryption_pass = keyring.get_password(
                f'{self.browser.capitalize()} Safe Storage', self.browser.capitalize()
            )
            self.cookie_encryption_pass = cookie_encryption_pass.encode('utf8')
            self.iterations = 1003
            self.cookie_file = os.path.expanduser(
                self.osx_user_cookie_file.format(user_profile=user_profile)
            )

            # If running Chromium on Linux
        elif self.os == OperatingSystem.LINUX:
            self.cookie_encryption_pass = self._get_linux_cookie_encrypt_pass()
            self.iterations = 1
            self.cookie_file = os.path.expanduser(
                self.linux_user_cookie_file.format(user_profile=user_profile)
            )
        else:
            raise BrowserAuthException("Invalid OS. Currently, only works on OSX or Linux.")

    def _get_user_profile(self):
        if self.os == OperatingSystem.MACOS:
            local_state = os.path.expanduser(self.osx_local_state_file)
        elif self.os == OperatingSystem.LINUX:
            local_state = os.path.expanduser(self.linux_local_state_file)
        else:
            raise BrowserAuthException("Invalid OS. Currently, only works on OSX or Linux.")

        log.info(f"Getting browser profile for user: {self.browser_profile_user_name}")

        with open(local_state) as json_file:
            profiles = json.load(json_file)['profile']['info_cache']
            user_profile = [k for k, v in profiles.items()
                            if v["user_name"] == self.browser_profile_user_name][0]

        return user_profile

    def _get_linux_cookie_encrypt_pass(self):
        """Retrieve password used to encrypt cookies from libsecret"""
        # https://github.com/n8henrie/pycookiecheat/issues/12
        my_pass = None

        import secretstorage
        connection = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(connection)
        secret = None

        # we should not look for secret with label. Sometimes label can be different. For example,
        # if Steam is installed before Chromium, Opera or Edge, it will show Steam Secret Storage as label.
        # Instead, we should look with schema and application
        secret = next(collection.search_items(
            {'xdg:schema': 'chrome_libsecret_os_crypt_password_v2',
             'application': self.browser.lower()}), None)

        if not secret:
            # trying os_crypt_v1
            secret = next(collection.search_items(
                {'xdg:schema': 'chrome_libsecret_os_crypt_password_v1',
                 'application': self.browser.lower()}), None)

        if secret:
            my_pass = secret.get_secret()

        connection.close()

        # Try to get pass from keyring, which should support KDE / KWallet
        if not my_pass:
            try:
                my_pass = keyring.get_password(
                    "{} Keys".format(self.browser.capitalize()),
                    "{} Safe Storage".format(self.browser.capitalize())
                ).encode('utf-8')
            except RuntimeError:
                pass
            except AttributeError:
                pass

        # try default peanuts password, probably won't work
        if not my_pass:
            my_pass = 'peanuts'.encode('utf-8')

        return my_pass

    def get_cookies(self):

        def chromium_decrypt(encrypted_value, cipher_key=None):

            # Encrypted cookies should be prefixed with 'v10' according to the
            # Chromium code. Strip it off.
            encrypted_value = encrypted_value[3:]

            # Strip padding by taking off number indicated by padding
            # e.g. if last is '\x0e' then ord('\x0e') == 14, so take off 14.
            # You'll need to change this function to use ord() for python2.
            def clean(x):
                return x[:-x[-1]].decode('utf8')

            cipher = AES.new(cipher_key, AES.MODE_CBC, IV=self.iv)
            decrypted = cipher.decrypt(encrypted_value)

            return clean(decrypted)

        key = PBKDF2(self.cookie_encryption_pass, self.salt, self.length, self.iterations)

        # Part of the domain name that will help the sqlite3 query pick it from the Chrome cookies
        domain = urllib.parse.urlparse(self.domain_name).netloc
        domain_no_sub = '.'.join(domain.split('.')[-2:])

        conn = sqlite3.connect(self.cookie_file)
        sql = 'select name, value, encrypted_value from cookies ' \
              'where host_key like "%{}%" and name = "rememberMe"'.format(domain)

        cookies = {}
        cookies_list = []

        with conn:
            for k, v, ev in conn.execute(sql):

                # if there is a not encrypted value or if the encrypted value
                # doesn't start with the 'v10' prefix, return v
                if v or ((ev[:3] != b'v10') and sys.platform == 'darwin'):
                    cookies_list.append((k, v))
                else:
                    decrypted_tuple = (k, chromium_decrypt(ev, cipher_key=key))
                    cookies_list.append(decrypted_tuple)
            cookies.update(cookies_list)

        return cookies


class Chrome(ChromiumBased):
    browser_profile_user_name: str = None
    browser: str = None
    domain_name: str = None
    osx_user_cookie_file: str = HOME_DIR + '/Library/Application Support/Google/Chrome/{user_profile}/Cookies'
    osx_local_state_file: str = f'{HOME_DIR}/Library/Application Support/Google/Chrome/Local State'
    linux_user_cookie_file: str = HOME_DIR + '/.config/google-chrome/{user_profile}/Cookies'
    linux_local_state_file: str = f'{HOME_DIR}/.config/google-chrome/Local State'


class Chromium(ChromiumBased):
    browser_profile_user_name: str = None
    browser: str = None
    domain_name: str = None
    osx_user_cookie_file: str = HOME_DIR + '/Library/Application Support/Chromium/{user_profile}/Cookies'
    osx_local_state_file: str = f'{HOME_DIR}/Library/Application Support/Chromium/Local State'
    linux_user_cookie_file: str = HOME_DIR + '/.config/chromium/{user_profile}/Cookies'
    linux_local_state_file: str = f'{HOME_DIR}/.config/chromium/Local State'


class Firefox(BrowserAuth):
    domain_name: str
    session_file: str = None
    session_file_lz4: str = None
    tmp_cookie_file: str = None
    osx_user_data_path: str = f'{HOME_DIR}/Library/Application Support/Firefox'
    linux_user_data_path: str = f'{HOME_DIR}/.mozilla/firefox'

    def __init__(self, api_conf: BrowserAPIAuth):
        super().__init__()
        self.domain_name = api_conf.get_domain_name()
        cookie_file = self.__find_cookie_file()
        self.__create_local_copy(cookie_file)
        self.session_file = os.path.join(
            os.path.dirname(cookie_file), 'sessionstore.js')
        self.session_file_lz4 = os.path.join(os.path.dirname(
            cookie_file), 'sessionstore-backups', 'recovery.jsonlz4')

    def _get_user_profile_path(self):
        if self.os == OperatingSystem.MACOS:
            local_state_path = os.path.expanduser(self.osx_user_data_path)
        elif self.os == OperatingSystem.LINUX:
            if exists(self.linux_user_data_path):
                local_state_path = os.path.expanduser(self.linux_user_data_path)
            elif exists(f'{HOME_DIR}/snap/firefox/common/.mozilla/firefox'):
                local_state_path = f'{HOME_DIR}/snap/firefox/common/.mozilla/firefox'
            else:
                raise BrowserAuthException(f'Cannot find cookie file.')
        else:
            raise BrowserAuthException(f'Unsupported operating system: {sys.platform}')

        config = configparser.ConfigParser()
        profiles_ini_path = glob.glob(os.path.join(
            local_state_path + '**', 'profiles.ini'))
        fallback_path = local_state_path + '**'

        if not profiles_ini_path:
            return fallback_path

        profiles_ini_path = profiles_ini_path[0]
        config.read(profiles_ini_path, encoding="utf8")

        profile_path = None
        for section in config.sections():
            if section.startswith('Install'):
                profile_path = config[section].get('Default')
                break
            # in ff 72.0.1, if both an Install section and one with Default=1 are present, the former takes precedence
            elif config[section].get('Default') == '1' and not profile_path:
                profile_path = config[section].get('Path')

        for section in config.sections():
            # the Install section has no relative/absolute info, so check the profiles
            if config[section].get('Path') == profile_path:
                absolute = config[section].get('IsRelative') == '0'
                return profile_path if absolute else os.path.join(os.path.dirname(profiles_ini_path), profile_path)

        return fallback_path

    def get_cookies(self):

        con = sqlite3.connect(self.tmp_cookie_file)
        cur = con.cursor()
        cur.execute('select host, path, isSecure, expiry, name, value, isHttpOnly from moz_cookies '
                    'where host like ? and name = "rememberMe"', ('%{}%'.format(self.domain_name),))

        cj = http.cookiejar.CookieJar()
        for item in cur.fetchall():
            host, path, secure, expires, name, value, http_only = item
            c = Firefox.__create_cookie(host, path, secure, expires, name, value, http_only)
            cj.set_cookie(c)
        con.close()

        self.__add_session_cookies(cj)
        self.__add_session_cookies_lz4(cj)

        return cj

    def __create_local_copy(self, cookie_file: str):
        """
        Make a local copy of the sqlite cookie database and return the new filename.
        This is necessary in case this database is still being written to while the user browses
        to avoid sqlite locking errors.
        """
        # check if cookie file exists
        if os.path.exists(cookie_file):
            # copy to random name in tmp folder
            self.tmp_cookie_file = tempfile.NamedTemporaryFile(suffix='.sqlite').name
            with open(self.tmp_cookie_file, 'wb') as tmp_file:
                with open(cookie_file, 'rb') as cf:
                    tmp_file.write(cf.read())
        else:
            raise BrowserAuthException(f'Can not find cookie file at: {cookie_file}')

    def __find_cookie_file(self):
        cookie_files = []

        cookie_files = glob.glob(os.path.join(self._get_user_profile_path(), 'cookies.sqlite')) \
                       or cookie_files

        if cookie_files:
            return cookie_files[0]
        else:
            raise BrowserAuthException('Failed to find Firefox cookie file')

    def __add_session_cookies(self, cj):
        if not os.path.exists(self.session_file):
            return
        try:
            with open(self.session_file, 'rb') as sf:
                json_data = json.loads(sf.read().decode())
        except ValueError as e:
            print('Error parsing firefox session JSON:', str(e))
        else:
            for window in json_data.get('windows', []):
                for cookie in window.get('cookies', []):
                    if self.domain_name == '' or self.domain_name in cookie.get('host', ''):
                        cj.set_cookie(Firefox.__create_session_cookie(cookie))

    def __add_session_cookies_lz4(self, cj):
        if not os.path.exists(self.session_file_lz4):
            return
        try:
            with open(self.session_file_lz4, 'rb') as file_obj:
                file_obj.read(8)
                json_data = json.loads(lz4.block.decompress(file_obj.read()))
        except ValueError as e:
            print('Error parsing firefox session JSON LZ4:', str(e))
        else:
            for cookie in json_data.get('cookies', []):
                if self.domain_name == '' or self.domain_name in cookie.get('host', ''):
                    cj.set_cookie(Firefox.__create_session_cookie(cookie))

    @staticmethod
    def __create_session_cookie(cookie_json):
        return Firefox.__create_cookie(cookie_json.get('host', ''), cookie_json.get('path', ''),
                                       cookie_json.get('secure', False), None,
                                       cookie_json.get('name', ''), cookie_json.get('value', ''),
                                       cookie_json.get('httponly', False))

    @staticmethod
    def __create_cookie(host, path, secure, expires, name, value, http_only):
        """Shortcut function to create a cookie"""
        # HTTPOnly flag goes in _rest, if present (see https://github.com/python/cpython/pull/17471/files#r511187060)
        return http.cookiejar.Cookie(0, name, value, None, False, host, host.startswith('.'), host.startswith('.'),
                                     path,
                                     True, secure, expires, False, None, None,
                                     {'HTTPOnly': ''} if http_only else {})
