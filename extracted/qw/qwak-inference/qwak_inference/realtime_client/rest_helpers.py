import socket
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import requests

from qwak_inference.configuration import Auth0Client, FrogMLAuthClient
from qwak_inference.configuration.account import UserAccountConfiguration
from qwak_inference.exceptions import QwakLoginException


def _get_authorization():
    user_account_configuration = UserAccountConfiguration()
    if issubclass(user_account_configuration._auth_client, Auth0Client):
        apikey: Optional[str] = user_account_configuration.get_user_apikey()
        auth_client = Auth0Client(api_key=apikey)
        tenant_id = None
    else:
        auth_client = FrogMLAuthClient()
        tenant_id = auth_client.get_tenant_id()

    return (
        f"Bearer {auth_client.get_token()}",
        auth_client.token_expiration(),
        tenant_id,
    )


@dataclass
class SocketConfiguration:
    tcp_keepalive: bool = True
    tcp_keepidle: int = 120
    tcp_keepintvl: int = 75
    tcp_keepcnt: int = 9


class SocketAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, *args, socket_params=None, **kwargs):
        self.socket_params = socket_params
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_params:
            kwargs["socket_options"] = self.socket_params
        super().init_poolmanager(*args, **kwargs)


# Configure only TCP attributes that are available in the OS
def validate_socket_config(socket_options):
    config = []
    for line in socket_options:
        if hasattr(socket, line[0]) and hasattr(socket, line[1]):
            config.append((getattr(socket, line[0]), getattr(socket, line[1]), line[2]))
    return config


class RestSession(requests.Session):
    def __init__(self, socket_configuration=SocketConfiguration()):
        super().__init__()
        self.headers.update({"Content-Type": "application/json"})
        socket_options = [
            ("SOL_SOCKET", "SO_KEEPALIVE", int(socket_configuration.tcp_keepalive)),
            ("SOL_TCP", "TCP_KEEPIDLE", socket_configuration.tcp_keepidle),
            ("SOL_TCP", "TCP_KEEPINTVL", socket_configuration.tcp_keepintvl),
            ("SOL_TCP", "TCP_KEEPCNT", socket_configuration.tcp_keepcnt),
        ]
        socket_options = validate_socket_config(socket_options)
        adapter = SocketAdapter(socket_params=socket_options)
        self.mount("https://", adapter)
        self.mount("http://", adapter)

    def prepare_request(self, request):
        if "Authorization" not in self.headers:
            self.prepare_request_token()
        else:
            if self.jwt_expiration and self.jwt_expiration <= datetime.now(
                timezone.utc
            ):
                self.prepare_request_token()

        return super().prepare_request(request)

    def prepare_request_token(self):
        auth_token, self.jwt_expiration, self.tenant_id = _get_authorization()
        self.headers["Authorization"] = auth_token

        if self.tenant_id:
            self.headers["X-JFrog-Tenant-Id"] = self.tenant_id
            if self.jwt_expiration and self.jwt_expiration <= datetime.now(
                timezone.utc
            ):
                raise QwakLoginException(
                    "JFrog access token has expired. Please generate a new access token in your JFrog Artifactory settings."
                )
