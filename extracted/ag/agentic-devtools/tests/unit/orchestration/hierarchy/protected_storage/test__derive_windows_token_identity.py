"""Tests for _derive_windows_token_identity."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import _derive_windows_token_identity


def _success_side_effect(expected_size: int = 16):  # type: ignore[no-untyped-def]
    def _get_token_information(_token, _token_class, buffer, _length, required_ptr):
        required_ptr._obj.value = expected_size
        return 0 if buffer is None else 1

    return _get_token_information


def _set_sid_value(_sid, sid_ptr) -> int:  # type: ignore[no-untyped-def]
    sid_ptr._obj.value = "S-1-5-21-123"
    return 1


def test_derive_windows_token_identity_returns_sid_string() -> None:
    """A successful token lookup returns the stable SID identity."""
    kernel32 = MagicMock()
    advapi32 = MagicMock()
    kernel32.GetCurrentProcess.return_value = object()
    advapi32.OpenProcessToken.return_value = 1
    advapi32.GetTokenInformation.side_effect = _success_side_effect()
    advapi32.ConvertSidToStringSidW.side_effect = _set_sid_value

    fake_token_user = SimpleNamespace(contents=SimpleNamespace(User=SimpleNamespace(Sid=object())))
    with patch("ctypes.WinDLL", side_effect=[kernel32, advapi32], create=True):
        with patch("ctypes.cast", return_value=fake_token_user):
            assert _derive_windows_token_identity() == "sid:S-1-5-21-123"

    kernel32.LocalFree.assert_called_once()
    kernel32.CloseHandle.assert_called_once()


def test_derive_windows_token_identity_raises_when_open_process_token_fails() -> None:
    """The helper fails closed when the current process token cannot be opened."""
    kernel32 = MagicMock()
    advapi32 = MagicMock()
    kernel32.GetCurrentProcess.return_value = object()
    advapi32.OpenProcessToken.return_value = 0

    with patch("ctypes.WinDLL", side_effect=[kernel32, advapi32], create=True):
        with pytest.raises(OSError, match="OpenProcessToken failed"):
            _derive_windows_token_identity()


def test_derive_windows_token_identity_raises_when_token_size_is_missing() -> None:
    """A zero-sized token-user payload is rejected."""
    kernel32 = MagicMock()
    advapi32 = MagicMock()
    kernel32.GetCurrentProcess.return_value = object()
    advapi32.OpenProcessToken.return_value = 1
    advapi32.GetTokenInformation.side_effect = lambda *_args: 0

    with patch("ctypes.WinDLL", side_effect=[kernel32, advapi32], create=True):
        with pytest.raises(OSError, match="no token-user payload"):
            _derive_windows_token_identity()

    kernel32.CloseHandle.assert_called_once()


def test_derive_windows_token_identity_raises_when_token_lookup_second_call_fails() -> None:
    """The helper rejects a token-user lookup that fails after sizing the buffer."""
    kernel32 = MagicMock()
    advapi32 = MagicMock()
    kernel32.GetCurrentProcess.return_value = object()
    advapi32.OpenProcessToken.return_value = 1

    def _get_token_information(_token, _token_class, buffer, _length, required_ptr):  # type: ignore[no-untyped-def]
        required_ptr._obj.value = 16
        return 0 if buffer is None else 0

    advapi32.GetTokenInformation.side_effect = _get_token_information

    with patch("ctypes.WinDLL", side_effect=[kernel32, advapi32], create=True):
        with pytest.raises(OSError, match="GetTokenInformation failed"):
            _derive_windows_token_identity()

    kernel32.CloseHandle.assert_called_once()


def test_derive_windows_token_identity_raises_when_sid_conversion_fails() -> None:
    """The helper rejects a token whose SID cannot be converted to a string."""
    kernel32 = MagicMock()
    advapi32 = MagicMock()
    kernel32.GetCurrentProcess.return_value = object()
    advapi32.OpenProcessToken.return_value = 1
    advapi32.GetTokenInformation.side_effect = _success_side_effect()
    advapi32.ConvertSidToStringSidW.return_value = 0

    fake_token_user = SimpleNamespace(contents=SimpleNamespace(User=SimpleNamespace(Sid=object())))
    with patch("ctypes.WinDLL", side_effect=[kernel32, advapi32], create=True):
        with patch("ctypes.cast", return_value=fake_token_user):
            with pytest.raises(OSError, match="ConvertSidToStringSidW failed"):
                _derive_windows_token_identity()

    kernel32.CloseHandle.assert_called_once()


def test_derive_windows_token_identity_raises_when_sid_conversion_returns_empty_value() -> None:
    """An empty converted SID is rejected as an untrusted identity."""
    kernel32 = MagicMock()
    advapi32 = MagicMock()
    kernel32.GetCurrentProcess.return_value = object()
    advapi32.OpenProcessToken.return_value = 1
    advapi32.GetTokenInformation.side_effect = _success_side_effect()
    advapi32.ConvertSidToStringSidW.side_effect = lambda _sid, _sid_ptr: 1

    fake_token_user = SimpleNamespace(contents=SimpleNamespace(User=SimpleNamespace(Sid=object())))
    with patch("ctypes.WinDLL", side_effect=[kernel32, advapi32], create=True):
        with patch("ctypes.cast", return_value=fake_token_user):
            with pytest.raises(OSError, match="returned an empty SID"):
                _derive_windows_token_identity()

    kernel32.LocalFree.assert_called_once()
    kernel32.CloseHandle.assert_called_once()
