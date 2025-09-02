import base64
import os
import re

from adam.config import Config

class IdpConfigurationException(Exception):
    pass

class SsoConfig:
    DEFAULT_IDP_URI = 'https://c3energy.okta.com/oauth2/v1/authorize?response_type=id_token&response_mode=form_post&client_id={client_id}&scope=openid+email+profile+groups&redirect_uri=https%3A%2F%2F{host}%2Fc3%2Fc3%2Foidc%2Flogin&nonce={nonce}&state=EMPTY'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(SsoConfig, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        if not hasattr(self, 'config'):
            self.config = Config().get('idps', {
                'ad': {
                    'email-pattern': '.*@c3.ai',
                    'uri': 'https://login.microsoftonline.com/53ad779a-93e7-485c-ba20-ac8290d7252b/oauth2/v2.0/authorize?response_type=id_token&response_mode=form_post&client_id=00ff94a8-6b0a-4715-98e0-95490012d818&scope=openid+email+profile&redirect_uri=https%3A%2F%2Fplat.c3ci.cloud%2Fc3%2Fc3%2Foidc%2Flogin&nonce={nonce}&state=EMPTY',
                    'contact': 'Please contact ted.tran@c3.ai.'
                },
                'okta': {
                    'default': True,
                    'email-pattern': '.*@c3iot.com',
                    'uri': SsoConfig.DEFAULT_IDP_URI
                }
            })

    def find_idp_uri(self, user_email: str, client_id: str, app_host: str) -> str:
        default: str = SsoConfig.DEFAULT_IDP_URI
        for k, v in self.config.items():
            if 'default' in v and v['default']:
                default = v['uri']
                break

        if not default:
            raise IdpConfigurationException('Please configure default idp.')

        def rpl(uri: str):
            return uri.replace('{client_id}', client_id).replace('{host}', app_host).replace('{nonce}', SsoConfig.generate_oauth_nonce())

        if not user_email:
            return rpl(default)

        for idp_name, conf in self.config.items():
            if 'email-pattern' in conf:
                groups = re.match(conf['email-pattern'], user_email)
                if groups:
                    return rpl(conf['uri'])

        return rpl(default)

    def generate_oauth_nonce():
        random_bytes = os.urandom(32)
        nonce = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
        nonce = nonce.rstrip('=')

        return nonce