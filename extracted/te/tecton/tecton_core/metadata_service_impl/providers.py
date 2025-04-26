from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Optional


class AuthProvider(ABC):
    """Base library class that provide authentication."""

    @abstractmethod
    def get_auth_header(self) -> Optional[str]:
        msg = "AuthProvider.get_auth_header() is not implemented"
        raise NotImplementedError(msg)


class RequestProvider(ABC):
    """Base library class that provide request headers and url."""

    def __init__(self, auth_provider: AuthProvider) -> None:
        self.auth_provider = auth_provider

    @abstractmethod
    def request_headers(self) -> Dict[str, str]:
        msg = "RequestProvider.request_headers() is not implemented"
        raise NotImplementedError(msg)

    @abstractmethod
    def request_url(self) -> str:
        msg = "RequestProvider.request_url() is not implemented"
        raise NotImplementedError(msg)
