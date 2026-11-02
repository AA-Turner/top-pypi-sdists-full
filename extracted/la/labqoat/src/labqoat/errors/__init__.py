"""Labqoat error types."""

from __future__ import annotations

from labqoat.errors.api_error import ApiError
from labqoat.errors.authentication_error import AuthenticationError
from labqoat.errors.revision_conflict_error import RevisionConflictError
from labqoat.errors.transport_error import TransportError

__all__ = ["ApiError", "AuthenticationError", "RevisionConflictError", "TransportError"]
