from datetime import datetime, timedelta, timezone

import jwt

from connector.generated import JWTCredential


def sign_jwt(credentials: JWTCredential, expiration_minutes: int = 20) -> str:
    # modify the claims to include the current `iat` and `exp` expiration time in UNIX time (seconds since the Unix epoch)
    now = datetime.now(timezone.utc)
    expiration_time = now + timedelta(minutes=expiration_minutes)
    credentials.claims.iat = int(now.timestamp())
    credentials.claims.exp = int(expiration_time.timestamp())
    token = jwt.encode(
        payload=credentials.claims.to_dict(),
        key=credentials.secret,
        headers=credentials.headers.to_dict(),
    )
    return token
