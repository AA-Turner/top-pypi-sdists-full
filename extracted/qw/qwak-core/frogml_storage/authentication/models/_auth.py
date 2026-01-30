from typing import Any

from requests import PreparedRequest
from requests.auth import AuthBase


class BearerAuth(AuthBase):
    def __init__(self, token: str):
        self.token: str = token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BearerAuth):
            return False

        return self.token == other.token


class EmptyAuth(AuthBase):
    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        return r
