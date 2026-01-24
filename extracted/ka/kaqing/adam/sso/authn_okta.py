import json
import jwt
import requests
from urllib.parse import urlparse, parse_qs, unquote

from adam.sso.authenticator import Authenticator
from adam.sso.id_token import IdToken

from .idp_login import IdpLogin
from adam.config import Config
from adam.utils import debug, log2, log_exc

class OktaException(Exception):
    pass

class OktaAuthenticator(Authenticator):
    def name(self) -> str:
        return 'Okta'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(OktaAuthenticator, cls).__new__(cls)

        return cls.instance

    def authenticate(self, idp_uri: str, app_host: str, username: str, password: str, verify: bool) -> IdpLogin:
        parsed_url = urlparse(idp_uri)
        query_string = parsed_url.query
        params = parse_qs(query_string)
        state_token = params.get('state', [''])[0]
        redirect_url = params.get('redirect_uri', [''])[0]

        okta_host = parsed_url.hostname

        authn_uri = f"https://{okta_host}/api/v1/authn"
        payload = {
            "username": username,
            "password": password,
            "options": {
                "warnBeforePasswordExpired": True,
                "multiOptionalFactorEnroll": False
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        session = requests.Session()
        response = session.post(authn_uri, headers=headers, data=json.dumps(payload))
        debug(f'{response.status_code} {authn_uri}')
        auth_response = response.json()

        if 'sessionToken' not in auth_response:
            raise OktaException('Invalid username/password.')

        session_token = auth_response['sessionToken']

        url = f'{idp_uri}&sessionToken={session_token}'
        r = session.get(url)
        debug(f'{r.status_code} {url}')

        id_token = OktaAuthenticator().extract(r.text, r'.*name=\"id_token\" value=\"(.*?)\".*')
        if not id_token:
            err = OktaAuthenticator().extract(r.text, r'.*name=\"error_description\" value=\"(.*?)\".*')
            if err:
                log2(unquote(err).replace('&#x20;', ' '))
            else:
                log2('id_token not found\n' + r.text)

            raise OktaException('Invalid username/password.')

        if not verify:
            # just relay id_token, it will be verified by SP
            return IdpLogin(redirect_url, id_token, state_token, username, idp_uri=idp_uri, id_token_obj=None, session=session)

        if group := Config().get('app.login.admin-group', '{host}/C3.ClusterAdmin').replace('{host}', app_host):
            parsed = OktaAuthenticator.parse_id_token(okta_host, id_token)
            if group not in parsed.groups:
                tks = group.split('/')
                group = tks[len(tks) - 1]
                log2(f'{username} is not a member of {group}.')

                raise OktaException("You are not part of admin group.")

        return IdpLogin(redirect_url, id_token, state_token, username, idp_uri=idp_uri, id_token_obj=parsed, session=session)

    def parse_id_token(idp_host, id_token) -> IdToken:
        data: dict[str, any] = []

        if not jwt.algorithms.has_crypto:
            log2("No crypto support for JWT, please install the cryptography dependency")

            return None

        jwks_url = Config().get('idps.okta.jwks-uri', 'https://c3energy.okta.com/oauth2/v1/keys')
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