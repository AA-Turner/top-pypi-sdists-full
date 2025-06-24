from fastapi import Security
from fastapi.requests import Request
from fastapi.security import HTTPAuthorizationCredentials
from maleo_foundation.authentication import Authentication
from maleo_foundation.authorization import TOKEN_SCHEME, Authorization

class AuthDependencies:
    @staticmethod
    def authentication(
        request: Request
    ) -> Authentication:
        return Authentication(
            credentials=request.auth,
            user=request.user
        )

    @staticmethod
    def authorization(
        token: HTTPAuthorizationCredentials = Security(TOKEN_SCHEME)
    ) -> Authorization:
        return Authorization(
            scheme=token.scheme,
            credentials=token.credentials
        )