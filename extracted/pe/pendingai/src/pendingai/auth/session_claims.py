#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from pendingai import config
from pendingai.exceptions import AuthenticationError
from pendingai.utils.logger import Logger

logger = Logger().get_logger()


@dataclass
class SessionClaims:
    """
    Authenticated session jwt claims.
    """

    issuer: str
    subscriber: str
    audiences: list[str]
    issued_at: datetime
    expire_at: datetime
    client_id: str
    scopes: list[str]

    user_email: str
    user_org_id: str
    user_org_name: str

    @staticmethod
    def _parse_datetime_claim(claim: int) -> datetime:
        """
        Parsed claim timestamp in epoch integer format into local
        timezone-friendly datetime instance.
        """
        return datetime.fromtimestamp(claim, timezone.utc).astimezone(config.TZ_LOCAL)

    @classmethod
    def from_dict(cls, claims: dict) -> "SessionClaims":
        """
        Build session claims dataclass from a parsed set of jwt token
        claims; extract fields into expected data type and populate
        custom claim fields; all claims are required.
        """
        required_claims: list[str] = [
            "iss",
            "sub",
            "aud",
            "iat",
            "exp",
            "azp",
            "scope",
            "https://pending.ai/claims/email",
            "https://pending.ai/claims/org_id",
            "https://pending.ai/claims/org_name",
        ]
        missing: list[str] = [x for x in required_claims if x not in claims.keys()]
        if len(missing) > 0:
            logger.warning(f"Required session claims missing from token: {missing}")
            raise AuthenticationError(
                "Authentication session contains malformed data. "
                "Reset the session by logging in. If the problem "
                "continues contact support via email at "
                "'support@pending.ai'."
            )

        try:
            return cls(
                issuer=claims["iss"],
                subscriber=claims["sub"],
                audiences=claims["aud"],
                issued_at=cls._parse_datetime_claim(claims["iat"]),
                expire_at=cls._parse_datetime_claim(claims["exp"]),
                client_id=claims["azp"],
                scopes=claims["scope"].split(),
                user_email=claims["https://pending.ai/claims/email"],
                user_org_id=claims["https://pending.ai/claims/org_id"],
                user_org_name=claims["https://pending.ai/claims/org_name"],
            )
        except Exception as e:
            logger.critical("Malformed parsing of session claims", exc_info=e)
            raise AuthenticationError(
                "Failed to read authenticated session info. Reset the "
                "session by logging in. If the problem continues "
                "contact support via email at 'support@pending.ai'."
            ) from e
