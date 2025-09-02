import base64
import json
import re
import requests
from urllib.parse import urlparse, parse_qs

from adam.log import Log
from adam.sso.authenticator import Authenticator
from adam.sso.id_token import IdToken

from .idp_login import IdpLogin
from adam.config import Config

class AdException(Exception):
    pass

class AdAuthenticator(Authenticator):
    def name(self) -> str:
        return 'ActiveDirectory'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(AdAuthenticator, cls).__new__(cls)

        return cls.instance

    def authenticate(self, idp_uri: str, app_host: str, username: str, password: str) -> IdpLogin:
        parsed_url = urlparse(idp_uri)
        query_string = parsed_url.query
        params = parse_qs(query_string)
        state_token = params.get('state', [''])[0]
        redirect_url = params.get('redirect_uri', [''])[0]

        session = requests.Session()
        r = session.get(idp_uri)
        Config().debug(f'{r.status_code} {idp_uri}')

        config = self.validate_and_return_config(r)

        groups = re.match(r'(https://.*?/.*?)/.*', idp_uri)
        if not groups:
            raise AdException('Incorrect idp_uri configuration.')

        login_uri = f'{groups[1]}/login'
        body = {
            'login': username,
            'passwd': password,
            'ctx': config['sCtx'],
            'hpgrequestid': config['sessionId'],
            'flowToken': config['sFT']
        }
        r = session.post(login_uri, data=body, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        Config().debug(f'{r.status_code} {login_uri}')

        config = self.validate_and_return_config(r)

        groups = re.match(r'(https://.*?)/.*', idp_uri)
        if not groups:
            raise AdException('Incorrect idp_uri configuration.')

        kmsi_uri = f'{groups[1]}/kmsi'
        body = {
            'ctx': config['sCtx'],
            'hpgrequestid': config['sessionId'],
            'flowToken': config['sFT'],
        }
        r = session.post(kmsi_uri, data=body, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        Config().debug(f'{r.status_code} {kmsi_uri}')

        if (config := self.extract_config_object(r.text)):
            if 'sErrorCode' in config and config['sErrorCode'] == '50058':
                raise AdException('Invalid username/password.')
            elif 'strServiceExceptionMessage' in config:
                raise AdException(config['strServiceExceptionMessage'])
            else:
                Log.log_to_file(config)
                raise AdException('Unknown err.')

        id_token = self.extract(r.text, r'.*name=\"id_token\" value=\"(.*?)\".*')
        if not id_token:
            raise AdException('Invalid username/password.')

        parsed = self.parse_id_token(id_token)
        roles = parsed.groups
        roles.append(username)
        whitelisted = self.whitelisted_members()

        for role in roles:
            if role in whitelisted:
                return IdpLogin(redirect_url, id_token, state_token, username, idp_uri=idp_uri, id_token_obj=parsed, session=session)

        contact = Config().get('idps.ad.contact', 'Please contact ted.tran@c3.ai.')
        raise AdException(f'{username} is not whitelisted. {contact}')

    def validate_and_return_config(self, r: requests.Response):
        if r.status_code < 200 or r.status_code >= 300:
            Config().debug(r.text)

            return None

        return self.extract_config_object(r.text)

    def extract_config_object(self, text: str):
        for line in text.split('\n'):
            groups = re.match(r'.*\$Config=\s*(\{.*)', line)
            if groups:
                js = groups[1].replace(';', '')
                config = json.loads(js)

                return config

        return None

    def whitelisted_members(self) -> list[str]:
        members_f = Config().get('idps.ad.whitelist-file', '/kaqing/members')
        try:
            with open(members_f, 'r') as file:
                lines = file.readlines()
            lines = [line.strip() for line in lines]

            def is_non_comment(line: str):
                return not line.startswith('#')

            lines = list(filter(is_non_comment, lines))

            return [line.split('#')[0].strip(' ') for line in lines]
        except FileNotFoundError:
            pass

        return []

    def parse_id_token(self, id_token: str) -> IdToken:
        def decode_jwt_part(encoded_part):
            missing_padding = len(encoded_part) % 4
            if missing_padding:
                encoded_part += '=' * (4 - missing_padding)
            decoded_bytes = base64.urlsafe_b64decode(encoded_part)
            return json.loads(decoded_bytes.decode('utf-8'))

        parts = id_token.split('.')
        # header = decode_jwt_part(parts[0])
        data = decode_jwt_part(parts[1])
        # print('SEAN', payload)
        # {
        #     'aud': '00ff94a8-6b0a-4715-98e0-95490012d818',
        #     'iss': 'https://login.microsoftonline.com/53ad779a-93e7-485c-ba20-ac8290d7252b/v2.0',
        #     'iat': 1756138348,
        #     'nbf': 1756138348,
        #     'exp': 1756142248,
        #     'cc': 'CmCuOndNgXFbP/Vor0kv9fqd32LOv7kSHKStVrGPTXXnlPlSET3g4z23XjVZJW37F2Yy8d45MzZ6xA/XNbYGE3BHYAZFhfDKOp0ZbWZysqa2zqD3lpyXxnlEpzWkFY1SlDgSBWMzLmFpGhIKEFbS9ukejKFBi0QKCcPHh6MiEgoQb7gHorgqqEOuuPDIcSgHATICTkE4AUIJCQDvjjtx391I',
        #     'email': 'sean.ahn@c3.ai',
        #     'groups': [
        #         'e58ef97f-8622-47cc-93cd-0ec8e3df2b4e',
        #         '290214ec-2eaa-47bb-802c-70c2535bb7e7',
        #         '55cd2e92-c40d-4646-b837-c6fb6406013b',
        #         '9b715aa3-ec6c-44ad-be0c-a1d95045526d',
        #         '19a38c19-e4c3-4d7b-8bb0-4afe7f502a51',
        #         '5d891ce3-02d8-4d34-9748-9e711a3d54c5',
        #         '0626cb36-106c-4ab3-adcf-7ee8e3f05584',
        #         '6dfdfa3e-b225-4a74-a534-1cc963f78e08',
        #         'bfdcca4e-7212-4e73-9b8a-eecfd3a7797d',
        #         '6d050845-61c4-4072-acb1-9662d0c9faa0',
        #         'c4fbb32c-9892-4eb3-a829-b4eaaf71b4ef'
        #     ],
        #     'name': 'Sean Ahn',
        #     'nonce': 'V7DzmHtmhu3X3tzZmC55vMQ2WJtqXnW6wJpYb3Kfud8',
        #     'oid': '380029a1-0643-4764-b3b8-9bc02630af41',
        #     'preferred_username': 'sean.ahn@c3.ai',
        #     'rh': '1.ATcAmnetU-eTXEi6IKyCkNclK6iU_wAKaxVHmOCVSQAS2Bj1AJU3AA.',
        #     'sid': '007dea79-a65c-7911-5142-8ea1b9faa41a',
        #     'sub': 'd-iCznXBDo3HEV7UCGalCVFIG47dQl_SFCaQtN2yVQI',
        #     'tid': '53ad779a-93e7-485c-ba20-ac8290d7252b',
        #     'uti': 'b7gHorgqqEOuuPDIcSgHAQ',
        #     'ver': '2.0'
        # }

        return IdToken(
            data,
            data['email'],
            data['name'],
            groups=data['groups'] if 'groups' in data else [],
            iat=data['iat'] if 'iat' in data else 0,
            nbf=data['nbf'] if 'nbf' in data else 0,
            exp=data['exp'] if 'exp' in data else 0
        )