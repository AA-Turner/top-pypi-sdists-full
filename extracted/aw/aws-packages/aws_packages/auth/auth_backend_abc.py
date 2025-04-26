from abc import ABCMeta, abstractmethod

from aws_packages.auth.models import AuthenticationRequest, User


class AuthBackendBase(metaclass=ABCMeta):
    """Base class for authentication backends"""

    @abstractmethod
    def authenticate(self, request: AuthenticationRequest) -> User:
        """Authenticate the request and returns an authenticated User"""
        pass

    @abstractmethod
    def authenticate_with_token(self, token: str) -> bool:
        """Authenticate user using jwt token and return status"""
        pass

    @abstractmethod
    def get_access_token(self, user: User) -> str:
        """Get the access for the given user"""
        pass

    @abstractmethod
    def get_refresh_token(self, user: User, token: str) -> str:
        """Get the refresh token for the given user"""
        pass
