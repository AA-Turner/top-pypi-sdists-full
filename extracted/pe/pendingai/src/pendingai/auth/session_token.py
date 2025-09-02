#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import jwt

from pendingai import config
from pendingai.auth.session_claims import SessionClaims
from pendingai.exceptions import AuthenticationError


@dataclass
class SessionToken:
    """
    Authentication session token.
    """

    access_token: str
    refresh_token: str | None = None
    id_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None
    scope: str | None = None

    def __post_init__(self) -> None:
        if self.is_expired():
            raise AuthenticationError("Authentication session token is expired.")

    @staticmethod
    def _decode(token: str) -> dict:
        """
        Decode a jwt token and return extracted claims.
        """
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError:
            raise AuthenticationError(f"Invalid session token: '{token}'.")

    @property
    def claims(self) -> SessionClaims:
        """
        Extract and coerce jwt access token claims.
        """
        return SessionClaims.from_dict(self._decode(self.access_token))

    def is_expired(self) -> bool:
        """
        Check if the session token is expired.
        """
        return self.claims.expire_at < datetime.now(config.TZ_LOCAL)
