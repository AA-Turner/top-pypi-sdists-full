from typing import Optional, Literal

from openapi_client import ProtoLLMVectorDBConnAuth


class ConnectionAuthUserPass(object):
    username: str
    password: str
    def __init__(self, username, password):
        self.username = username
        self.password = password

class ConnectionAuthBearer(object):
    token: str
    def __init__(self, token):
        self.token = token

class ConnectionAuthHeader(object):
    header_key: str
    header_value: str
    def __init__(self, header_key, header_value):
        self.header_key = header_key
        self.header_value = header_value

class ConnectionAuth(object):
    auth_type: Literal["userpass", "bearer", "header", "none"]
    userpass: Optional[ConnectionAuthUserPass]
    bearer: Optional[ConnectionAuthBearer]
    header: Optional[ConnectionAuthHeader]

    def __init__(self, auth: ProtoLLMVectorDBConnAuth):
        if auth.type == "none":
            self.auth_type = "none"
        elif auth.type == "userpass":
            self.auth_type = "userpass"
            self.userpass = ConnectionAuthUserPass(auth.username, auth.password)
        elif auth.type == "bearer":
            self.auth_type = "bearer"
            self.bearer = ConnectionAuthBearer(auth.token)
        elif auth.type == "header":
            self.auth_type = "header"
            self.header = ConnectionAuthHeader(auth.header_key, auth.header_value)