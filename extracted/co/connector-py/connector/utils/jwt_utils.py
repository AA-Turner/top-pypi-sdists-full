from datetime import datetime, timedelta, timezone

import jwt
from connector_sdk_types.generated import JWTCredential

from connector.oai.errors import InvalidConfigurationError


def sign_jwt(credentials: JWTCredential, expiration_minutes: int = 20) -> str:
    # modify the claims to include the current `iat` and `exp` expiration time in UNIX time (seconds since the Unix epoch)
    now = datetime.now(timezone.utc)
    expiration_time = now + timedelta(minutes=expiration_minutes)
    credentials.claims.iat = int(now.timestamp())
    credentials.claims.exp = int(expiration_time.timestamp())
    headers = credentials.headers.to_dict()
    # The base JWTHeaders schema requires `crit`, so it defaults to an empty list, but
    # PyJWT (>= 2.12.0) rejects an empty `crit` header per RFC 7515. Drop it when unused
    # so the signed token stays spec-compliant.
    if not headers.get("crit"):
        headers.pop("crit", None)
    try:
        token = jwt.encode(
            payload=credentials.claims.to_dict(),
            key=credentials.secret,
            headers=headers,
        )
    except Exception as e:
        raise InvalidConfigurationError(
            message=f"Failed to sign JWT: {e}",
        ) from e
    return token
