from abc import abstractmethod
import re

from .idp_login import IdpLogin

class Authenticator:
    @abstractmethod
    def name(self) -> str:
        return None

    @abstractmethod
    def authenticate(self, idp_uri: str, app_host: str, username: str, password: str, verify: bool = True) -> IdpLogin:
        pass

    def extract(self, form: str, pattern: re.Pattern):
        value = None

        for l in form.split('\n'):
            # <input type="hidden" name="id_token" value="..."/>
            groups = re.match(pattern, l)
            if groups:
                value = groups[1]

        return value