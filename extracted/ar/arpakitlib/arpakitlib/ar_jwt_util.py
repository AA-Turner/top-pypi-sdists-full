# arpakit

from typing import Any, Optional

import jwt
from jwt import PyJWTError

from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def encode_jwt_token(
        *,
        jwt_payload: dict[str, Any],
        jwt_secret: str
) -> str:
    raise_for_type(jwt_secret, str)
    return jwt.encode(jwt_payload, jwt_secret, algorithm="HS256")


def decode_jwt_token(
        *,
        jwt_token: str,
        jwt_secret: str
) -> Optional[dict[str, Any]]:
    raise_for_type(jwt_token, str)
    raise_for_type(jwt_secret, str)
    try:
        return jwt.decode(jwt_token, jwt_secret, algorithms=["HS256"])
    except PyJWTError:
        return None


def __example():
    pass


if __name__ == '__main__':
    __example()
