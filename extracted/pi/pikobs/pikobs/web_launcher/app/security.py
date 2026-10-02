from fastapi import Header, HTTPException
import hmac

from . import config


def require_token(x_pikobs_token: str = Header(default='')) -> None:
    expected = config.API_TOKEN
    if not expected:
        raise HTTPException(503, 'Pikobs Web API token is not configured')
    if not hmac.compare_digest(x_pikobs_token, expected):
        raise HTTPException(401, 'Invalid or missing Pikobs Web token')
