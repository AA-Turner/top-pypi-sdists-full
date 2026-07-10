import time
import typing
from dataclasses import dataclass
from functools import lru_cache

import jwt

from abstra_internals.environment import PROJECT_ID, PUBLIC_KEY
from abstra_internals.logger import AbstraLogger
from abstra_internals.utils.email import is_valid_email

USER_AUTH_HEADER_KEY = "Authorization"


@lru_cache(maxsize=10)
def _decode_jwt_cached(jwt_str: str, aud, skip_verify: bool):
    try:
        if not skip_verify and PUBLIC_KEY:
            return jwt.decode(
                jwt_str, key=PUBLIC_KEY, algorithms=["RS256"], audience=aud
            )
        if skip_verify:
            # Explicitly requested: skip audience validation too — editor JWTs
            # have a different audience (web-editor-{PROJECT_ID}) than user JWTs
            # (PROJECT_ID), and both should work for get_user() in development.
            return jwt.decode(
                jwt_str,
                options={"verify_signature": False, "verify_aud": False},
            )
        # PUBLIC_KEY is not set but skip_verify was not requested — still
        # validate audience and expiration. PyJWT silently disables every
        # other check when verify_signature is False, so both must be
        # re-enabled explicitly (used by _guard() to ensure correct JWT type).
        return jwt.decode(
            jwt_str,
            options={"verify_signature": False, "verify_aud": True, "verify_exp": True},
            audience=aud,
        )

    except jwt.ExpiredSignatureError:
        return None
    except Exception as e:
        AbstraLogger.capture_exception(e)
        return None


def decode_jwt(jwt_str: str, aud=PROJECT_ID, skip_verify: bool = False):
    claims = _decode_jwt_cached(jwt_str, aud, skip_verify)
    if claims is None:
        return None
    # The cache outlives token expiration: a token validated while still
    # valid would otherwise stay "valid" for the life of the process.
    exp = claims.get("exp")
    if not skip_verify and exp is not None and time.time() >= exp:
        return None
    return claims


@dataclass
class UserClaims:
    """The response from the authentication process

    Attributes:
      email (str): The email address of the user
      claims (dict): The claims from the JWT token
    """

    claims: typing.Dict[str, typing.Any]

    @property
    def email(self) -> str:
        return self.claims["email"]

    def add_roles(self, roles: typing.List[str]) -> None:
        self.claims["roles"] = roles

    @property
    def roles(self) -> typing.List[str]:
        return self.claims.get("roles", [])

    @classmethod
    def from_jwt(
        cls, jwt_str: str, skip_verify: bool = False
    ) -> typing.Optional["UserClaims"]:
        claims = decode_jwt(jwt_str, skip_verify=skip_verify)
        if claims is None:
            return None

        email = claims.get("email")
        if not is_valid_email(email):
            return None

        return cls(claims)

    def __getattr__(self, name):
        return self.claims.get(name)
