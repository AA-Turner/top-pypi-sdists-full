from contextlib import suppress
from datetime import UTC, datetime

from django.utils import timezone
from jwt import decode as jwt_decode
from jwt.exceptions import DecodeError


def is_expired(token: str, exp_key: str = "exp") -> bool:
    with suppress(DecodeError, KeyError, ValueError):
        expiry_ts = int(jwt_decode(token, options={"verify_signature": False})[exp_key])
        expiry_datetime = datetime.fromtimestamp(expiry_ts, UTC)
        return expiry_datetime < timezone.now()
    return True
