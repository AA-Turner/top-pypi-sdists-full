import json
import re
import jwt
import requests
from urllib.parse import urlparse, parse_qs

from adam.log import Log
from adam.sso.authenticator import Authenticator
from adam.sso.id_token import IdToken
from adam.utils import debug, log_exc
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

    def authenticate(self, idp_uri: str, app_host: str, username: str, password: str, verify: bool) -> IdpLogin:
        parsed_url = urlparse(idp_uri)
        query_string = parsed_url.query
        params = parse_qs(query_string)
        state_token = params.get('state', [''])[0]
        redirect_url = params.get('redirect_uri', [''])[0]

        session = requests.Session()
        r = session.get(idp_uri)
        debug(f'{r.status_code} {idp_uri}')

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
        debug(f'{r.status_code} {login_uri}')

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
        debug(f'{r.status_code} {kmsi_uri}')

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

        if not verify:
            return IdpLogin(redirect_url, id_token, state_token, username, idp_uri=idp_uri, id_token_obj=None, session=session)

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
            debug(r.text)

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
        jwks_url = Config().get('idps.ad.jwks-uri', '')
        with log_exc():
            jwks_client = jwt.PyJWKClient(jwks_url, cache_jwk_set=True, lifespan=360)
            signing_key = jwks_client.get_signing_key_from_jwt(id_token)
            data = jwt.decode(
                id_token,
                signing_key.key,
                algorithms=["RS256"],
                options={
                    "verify_signature": True,
                    "verify_exp": False,
                    "verify_nbf": True,
                    "verify_iat": True,
                    "verify_aud": False,
                    "verify_iss": False,
                },
            )
            return IdToken(
                data,
                data['email'],
                data['name'],
                groups=data['groups'] if 'groups' in data else [],
                iat=data['iat'] if 'iat' in data else 0,
                nbf=data['nbf'] if 'nbf' in data else 0,
                exp=data['exp'] if 'exp' in data else 0
            )

        return None