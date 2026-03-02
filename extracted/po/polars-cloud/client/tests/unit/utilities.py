import time
from uuid import uuid4

import jwt


def access_token() -> str:
    """An access token that passes the validity check."""
    current_time = int(time.time())

    payload = {
        "iss": "http://localhost:3001",
        "sub": str(uuid4()),
        "exp": current_time + 1000,
        "iat": current_time - 1000,
        "given_name": "first_name",
        "family_name": "last_name",
        "email": "test@example.com",
        "email_verified": True,
        "name": "FirstName LastName",
        "encryption_key": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
    }

    return jwt.encode(payload, "SECRET", algorithm="HS256")
