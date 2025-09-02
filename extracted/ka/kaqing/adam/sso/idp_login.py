import base64
import json
from urllib.parse import parse_qs, urlparse
import requests

from adam.sso.id_token import IdToken

class IdpLogin:
    def __init__(self, app_login_url: str, id_token: str, state: str, user: str = None, idp_uri: str = None, id_token_obj: IdToken = None, session: requests.Session = None):
        self.app_login_url = app_login_url
        self.id_token = id_token
        self.state = state
        self.user = user
        self.idp_uri = idp_uri
        self.id_token_obj = id_token_obj
        self.session = session

    def deser(idp_token: str):
        j = json.loads(base64.b64decode(idp_token.encode('utf-8')))

        return IdpLogin(
            j['r'],
            j['id_token'],
            j['state'],
            idp_uri=j['idp_uri'] if 'idp_uri' in j else None,
            id_token_obj=IdToken.from_dict(j['id_token_obj']))

    def ser(self):
        return base64.b64encode(json.dumps({
            'r': self.app_login_url,
            'id_token': self.id_token,
            'state': self.state,
            'idp_uri': self.idp_uri,
            'id_token_obj': self.id_token_obj.to_dict() if self.id_token_obj else None
        }).encode('utf-8')).decode('utf-8')

    def create_from_idp_uri(idp_uri: str):
        parsed_url = urlparse(idp_uri)
        query_string = parsed_url.query
        params = parse_qs(query_string)
        state_token = params.get('state', [''])[0]
        redirect_url = params.get('redirect_uri', [''])[0]

        return IdpLogin(app_login_url=redirect_url, id_token=None, state=state_token, idp_uri=idp_uri)

    def shell_user(self):
        if not self.user:
            return None

        return self.user.split('@')[0].replace('.', '')