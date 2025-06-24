from fastapi import FastAPI
from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from typing import Tuple
from maleo_foundation.authentication import Token, Credentials, User
from maleo_foundation.enums import BaseEnums
from maleo_foundation.client.manager import MaleoFoundationClientManager
from maleo_foundation.models.schemas import BaseGeneralSchemas
from maleo_foundation.models.transfers.parameters.token \
    import MaleoFoundationTokenParametersTransfers
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_foundation.utils.logging import MiddlewareLogger

class Backend(AuthenticationBackend):
    def __init__(
        self,
        keys: BaseGeneralSchemas.RSAKeys,
        logger: MiddlewareLogger,
        maleo_foundation: MaleoFoundationClientManager
    ):
        super().__init__()
        self._keys = keys
        self._logger = logger
        self._maleo_foundation = maleo_foundation

    async def authenticate(
        self,
        conn: HTTPConnection
    ) -> Tuple[Credentials, User]:
        if "Authorization" in conn.headers:
            auth = conn.headers["Authorization"]
            parts = auth.split()
            if len(parts) != 2 or parts[0] != "Bearer":
                raise AuthenticationError("Invalid Authorization header format")
            scheme, token = parts
            if scheme != 'Bearer':
                raise AuthenticationError("Authorization scheme must be Bearer token")

            #* Decode token
            decode_token_parameters = (
                MaleoFoundationTokenParametersTransfers
                .Decode(key=self._keys.public, token=token)
            )
            decode_token_result = (
                self._maleo_foundation.services.token
                .decode(parameters=decode_token_parameters)
            )
            if decode_token_result.success:
                type = BaseEnums.TokenType.ACCESS
                payload = decode_token_result.data
                token = Token(
                    type=type,
                    payload=payload
                )
                return (
                    Credentials(
                        token=token,
                        scopes=["authenticated", payload.sr]
                    ),
                    User(
                        authenticated=True,
                        username=payload.u_u,
                        email=payload.u_e
                    )
                )

        if "token" in conn.cookies:
            token = conn.cookies["token"]
            #* Decode token
            decode_token_parameters = (
                MaleoFoundationTokenParametersTransfers
                .Decode(key=self._keys.public, token=token)
            )
            decode_token_result = (
                self._maleo_foundation.services.token
                .decode(parameters=decode_token_parameters)
            )
            if decode_token_result.success:
                type = BaseEnums.TokenType.REFRESH
                payload = decode_token_result.data
                token = Token(
                    type=type,
                    payload=payload
                )
                return (
                    Credentials(
                        token=token,
                        scopes=["authenticated", payload.sr]
                    ),
                    User(
                        authenticated=True,
                        username=payload.u_u,
                        email=payload.u_e
                    )
                )

        return Credentials(), User(authenticated=False)

def add_authentication_middleware(
    app: FastAPI,
    keys: BaseGeneralSchemas.RSAKeys,
    logger: MiddlewareLogger,
    maleo_foundation: MaleoFoundationClientManager
) -> None:
    """
    Adds Authentication middleware to the FastAPI application.

    Args:
        app: FastAPI
            The FastAPI application instance to which the middleware will be added.

        logger: MiddlewareLogger
            Authentication middleware logger to be used.

        key: str
            Public key to be used for token decoding.

    Returns:
        None: The function modifies the FastAPI app by adding Base middleware.

    Note:
        FastAPI applies middleware in reverse order of registration, so this middleware
        will execute after any middleware added subsequently.

    Example:
    ```python
    add_authentication_middleware(app=app, limit=10, window=1, cleanup_interval=60, ip_timeout=300)
    ```
    """
    app.add_middleware(
        AuthenticationMiddleware,
        backend=Backend(keys, logger, maleo_foundation),
        on_error=BaseExceptions.authentication_error_handler
    )