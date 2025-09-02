"""Exceptions for crownstone cloud connection cloud"""
from __future__ import annotations

AuthError = {
    "LOGIN_FAILED": "Wrong email or password provided",
    "USERNAME_EMAIL_REQUIRED": "Email or password not provided",
    "LOGIN_FAILED_EMAIL_NOT_VERIFIED": "Email has not been verified, please do that first",
}

AbilityError = {
    "NOT_ENABLED": "This ability is not enabled. Use the Crownstone App to enable it.",
}


class CrownstoneException(Exception):
    """Raised when authentication with API ended in error"""

    def __init__(self, exception_type: str, message: str | None = None):
        super().__init__(exception_type, message)
        self.type = exception_type
        self.message = message


class CrownstoneAuthenticationError(CrownstoneException):
    """Raised when authentication with API ended in error"""


class CrownstoneUnknownError(Exception):
    """Raised when the error is not known / no data"""


class CrownstoneConnectionError(Exception):
    """Raised when a connection to the Crownstone Cloud can't be made."""


class CrownstoneAbilityError(CrownstoneException):
    """Raised when when e.g. dimming command is requested when it is not enabled."""


class CrownstoneNotFoundError(Exception):
    """Raised when searching for a Crownstone object, but it is not found."""
