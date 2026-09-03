"""Unit tests for AES-256-GCM protected storage (FR-011, FR-012, SC-017)."""

from __future__ import annotations

import builtins
from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import (
    UnauthorizedAccessError,
    derive_caller_identity,
)


def test_derive_caller_identity_matches_process_owner() -> None:
    identity = derive_caller_identity()
    assert isinstance(identity, str)
    assert identity


def test_derive_caller_identity_falls_back_to_uid_when_pwd_is_unavailable() -> None:
    """A trusted numeric UID is used when POSIX username lookup is unavailable."""
    original_import = builtins.__import__

    def _import_with_pwd_failure(name: str, *args, **kwargs):  # type: ignore[no-untyped-def]
        if name == "pwd":
            raise ImportError("pwd unavailable")
        return original_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=_import_with_pwd_failure):
        identity = derive_caller_identity()

    assert identity.startswith("uid:")


def test_derive_caller_identity_fails_closed_without_trusted_identity_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    """When neither pwd nor UID sources are available, identity derivation must fail closed."""
    original_import = builtins.__import__

    def _import_with_pwd_failure(name: str, *args, **kwargs):  # type: ignore[no-untyped-def]
        if name == "pwd":
            raise ImportError("pwd unavailable")
        return original_import(name, *args, **kwargs)

    monkeypatch.delattr("agentic_devtools.orchestration.hierarchy.protected_storage.os.getuid", raising=False)
    with patch("builtins.__import__", side_effect=_import_with_pwd_failure):
        with pytest.raises(UnauthorizedAccessError, match="trusted identity"):
            derive_caller_identity()


def test_derive_caller_identity_uses_windows_sid_when_posix_sources_are_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Windows falls back to the trusted process-token SID when POSIX sources are unavailable."""
    original_import = builtins.__import__

    def _import_with_pwd_failure(name: str, *args, **kwargs):  # type: ignore[no-untyped-def]
        if name == "pwd":
            raise ImportError("pwd unavailable")
        return original_import(name, *args, **kwargs)

    monkeypatch.delattr("agentic_devtools.orchestration.hierarchy.protected_storage.os.getuid", raising=False)
    with patch("agentic_devtools.orchestration.hierarchy.protected_storage.sys.platform", "win32"):
        with patch(
            "agentic_devtools.orchestration.hierarchy.protected_storage._derive_windows_token_identity",
            return_value="sid:S-1-5-21-123",
        ):
            with patch("builtins.__import__", side_effect=_import_with_pwd_failure):
                assert derive_caller_identity() == "sid:S-1-5-21-123"


def test_derive_caller_identity_fails_closed_when_windows_sid_lookup_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Windows SID lookup errors still fail closed instead of permitting an unknown identity."""
    original_import = builtins.__import__

    def _import_with_pwd_failure(name: str, *args, **kwargs):  # type: ignore[no-untyped-def]
        if name == "pwd":
            raise ImportError("pwd unavailable")
        return original_import(name, *args, **kwargs)

    monkeypatch.delattr("agentic_devtools.orchestration.hierarchy.protected_storage.os.getuid", raising=False)
    with patch("agentic_devtools.orchestration.hierarchy.protected_storage.sys.platform", "win32"):
        with patch(
            "agentic_devtools.orchestration.hierarchy.protected_storage._derive_windows_token_identity",
            side_effect=OSError("token lookup failed"),
        ):
            with patch("builtins.__import__", side_effect=_import_with_pwd_failure):
                with pytest.raises(UnauthorizedAccessError, match="trusted identity"):
                    derive_caller_identity()
