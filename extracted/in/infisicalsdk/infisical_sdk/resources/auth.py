from infisical_sdk.infisical_requests import InfisicalRequests
from infisical_sdk.resources.auth_methods import AWSAuth
from infisical_sdk.resources.auth_methods import UniversalAuth

from typing import Callable
class Auth:
    def __init__(self, requests: InfisicalRequests, setToken: Callable[[str], None]):
        self.requests = requests
        self.aws_auth = AWSAuth(requests, setToken)
        self.universal_auth = UniversalAuth(requests, setToken)