import os
from urllib.parse import urlparse

from adam.sso import authn_okta
from adam.sso.authenticator import Authenticator
from adam.sso.authn_ad import AdAuthenticator
from adam.sso.sso_config import SsoConfig
from .idp_login import IdpLogin

class IdpNotSupportedException(Exception):
    pass

class IdpSession:
    def create(email: str, client_id: str, app_host: str, idp_uri: str = None) -> 'IdpSession':
        if not idp_uri:
            idp_uri = SsoConfig().find_idp_uri(email, client_id, app_host)

        return IdpSession(idp_uri, IdpSession._authenticator(idp_uri))

    def __init__(self, idp_uri: str, authenticator: Authenticator):
        self.idp_uri = idp_uri
        self.authenticator = authenticator

    def idp_host(self):
        return urlparse(self.idp_uri).hostname

    def _authenticator(idp_uri) -> Authenticator:
        idp = urlparse(idp_uri).hostname

        if 'okta' in idp.lower():
            return authn_okta.OktaAuthenticator()
        elif 'microsoftonline' in idp.lower():
            return AdAuthenticator()

        raise IdpNotSupportedException(f'{idp} is not supported; only okta and ad are supported.')

    def login_from_env_var(self) -> IdpLogin:
        if idp_token := os.getenv('IDP_TOKEN'):
            return self.login_from_token(idp_token)

        return None

    def login_from_token(self, idp_token: str) -> IdpLogin:
        l0: IdpLogin = IdpLogin.deser(idp_token)
        l1: IdpLogin = self.get_idp_login()
        # if l0.app_login_url == l1.app_login_url:
        if l0.state != 'EMPTY':
            return l0

        l0.state = l1.state

        return l0

    def get_idp_login(self) -> IdpLogin:
        return IdpLogin.create_from_idp_uri(self.idp_uri)