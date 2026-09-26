from __future__ import annotations

import datetime
import uuid

from globus_sdk import GlobusError, Scope


class TokenValidationError(GlobusError):
    """The class of errors raised when a token fails validation."""


class IdentityValidationError(TokenValidationError):
    """
    The class of errors raised when a token response's identity is indeterminate or
    incorrect.
    """


class MissingIdentityError(IdentityValidationError, LookupError):
    """No identity info contained in a token response."""


class IdentityMismatchError(IdentityValidationError, ValueError):
    """The identity in a token response did not match the expected identity."""

    def __init__(
        self, message: str, stored_id: uuid.UUID | str, new_id: uuid.UUID | str
    ) -> None:
        super().__init__(message)
        self.message = message
        self.stored_id = stored_id
        self.new_id = new_id

    def __str__(self) -> str:
        return self.message

    def __reduce__(self) -> tuple[type, tuple[str, uuid.UUID | str, uuid.UUID | str]]:
        return (IdentityMismatchError, (self.message, self.stored_id, self.new_id))


class MissingTokenError(TokenValidationError, LookupError):
    """No token stored for a given resource server."""

    def __init__(self, message: str, resource_server: str) -> None:
        super().__init__(message)
        self.message = message
        self.resource_server = resource_server

    def __str__(self) -> str:
        return self.message

    def __reduce__(self) -> tuple[type, tuple[str, str]]:
        return (MissingTokenError, (self.message, self.resource_server))


class ExpiredTokenError(TokenValidationError, ValueError):
    """The token stored for a given resource server has expired."""

    def __init__(self, expires_at_seconds: int) -> None:
        expiration = datetime.datetime.fromtimestamp(expires_at_seconds)
        message = f"Token expired at {expiration.isoformat()}"

        super().__init__(message)

        self.message = message
        self.expiration = expiration
        self._expires_at_seconds = expires_at_seconds

    def __str__(self) -> str:
        return self.message

    def __reduce__(self) -> tuple[type, tuple[int]]:
        return (ExpiredTokenError, (self._expires_at_seconds,))


class UnmetScopeRequirementsError(TokenValidationError, ValueError):
    """The token stored for a given resource server is missing required scopes."""

    def __init__(
        self, message: str, scope_requirements: dict[str, list[Scope]]
    ) -> None:
        super().__init__(message)
        self.message = message
        # The full set of scope requirements which were evaluated.
        #   Notably this is not exclusively the unmet scope requirements.
        self.scope_requirements = scope_requirements

    def __str__(self) -> str:
        return self.message

    def __reduce__(self) -> tuple[type, tuple[str, dict[str, list[Scope]]]]:
        return (UnmetScopeRequirementsError, (self.message, self.scope_requirements))
