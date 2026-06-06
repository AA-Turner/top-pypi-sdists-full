"""Unit tests for runlayer_cli.enrollment.exchange_enrollment_key."""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest

from runlayer_cli.enrollment import (
    ENROLLMENT_ENDPOINT_PATH,
    EnrollmentError,
    enrollment_marker_path,
    exchange_enrollment_key,
    resolve_enrollment_identity,
    write_enrollment_marker,
)


def _mock_response(*, status_code: int, body: object) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.json.return_value = body
    return response


def _patch_http_client(response: MagicMock | None, *, raises: Exception | None = None):
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    if raises is not None:
        mock_client.post.side_effect = raises
    else:
        mock_client.post.return_value = response
    return patch("runlayer_cli.enrollment.http_client", return_value=mock_client)


def test_exchange_enrollment_key_happy_path():
    response = _mock_response(status_code=200, body={"api_key": "rl_user_xyz"})
    with _patch_http_client(response):
        result = exchange_enrollment_key(
            host="https://t.example.com",
            enrollment_key="rl_enroll_abc",
            username="user@example.com",
            device_name="Test-Mac",
        )
    assert result.api_key == "rl_user_xyz"
    assert result.username == "user@example.com"
    assert result.device_name == "Test-Mac"


def test_exchange_enrollment_key_strips_trailing_slash_in_endpoint():
    response = _mock_response(status_code=200, body={"api_key": "rl_user_xyz"})
    with _patch_http_client(response) as mock_factory:
        exchange_enrollment_key(
            host="https://t.example.com/",
            enrollment_key="k",
            username=None,
            device_name=None,
        )
        client = mock_factory.return_value
        called_url = client.post.call_args[0][0]
        assert called_url == f"https://t.example.com{ENROLLMENT_ENDPOINT_PATH}"


def test_exchange_enrollment_key_resolves_blank_username_and_device_name(monkeypatch):
    """Backend ``MDMEnrollRequest`` requires both fields (test_enroll_missing_username →
    422). When callers pass ``None`` we must still POST an OS-resolved body, not ``{}``."""
    monkeypatch.delenv("ENROLLMENT_USERNAME", raising=False)
    monkeypatch.delenv("RUNLAYER_ENROLLMENT_USERNAME", raising=False)
    monkeypatch.delenv("ENROLLMENT_DEVICE_NAME", raising=False)
    monkeypatch.delenv("RUNLAYER_ENROLLMENT_DEVICE_NAME", raising=False)

    response = _mock_response(status_code=200, body={"api_key": "rl_user_xyz"})
    with (
        patch("runlayer_cli.enrollment.getpass.getuser", return_value="osuser"),
        patch("runlayer_cli.enrollment.socket.gethostname", return_value="oshost"),
        _patch_http_client(response) as mock_factory,
    ):
        exchange_enrollment_key(
            host="https://t.example.com",
            enrollment_key="k",
            username=None,
            device_name=None,
        )
        client = mock_factory.return_value
        body = client.post.call_args[1]["json"]
        assert body == {"username": "osuser", "device_name": "oshost"}


def test_exchange_enrollment_key_prefers_env_over_os_defaults(monkeypatch):
    monkeypatch.setenv("ENROLLMENT_USERNAME", "envuser")
    monkeypatch.setenv("ENROLLMENT_DEVICE_NAME", "envhost")

    response = _mock_response(status_code=200, body={"api_key": "rl_user_xyz"})
    with (
        patch("runlayer_cli.enrollment.getpass.getuser", return_value="osuser"),
        patch("runlayer_cli.enrollment.socket.gethostname", return_value="oshost"),
        _patch_http_client(response) as mock_factory,
    ):
        exchange_enrollment_key(
            host="https://t.example.com",
            enrollment_key="k",
            username=None,
            device_name=None,
        )
        body = mock_factory.return_value.post.call_args[1]["json"]
        assert body == {"username": "envuser", "device_name": "envhost"}


def test_exchange_enrollment_key_explicit_values_win_over_env_and_os(monkeypatch):
    monkeypatch.setenv("ENROLLMENT_USERNAME", "envuser")
    monkeypatch.setenv("ENROLLMENT_DEVICE_NAME", "envhost")

    response = _mock_response(status_code=200, body={"api_key": "rl_user_xyz"})
    with (
        patch("runlayer_cli.enrollment.getpass.getuser", return_value="osuser"),
        patch("runlayer_cli.enrollment.socket.gethostname", return_value="oshost"),
        _patch_http_client(response) as mock_factory,
    ):
        exchange_enrollment_key(
            host="https://t.example.com",
            enrollment_key="k",
            username="mdmuser",
            device_name="mdmhost",
        )
        body = mock_factory.return_value.post.call_args[1]["json"]
        assert body == {"username": "mdmuser", "device_name": "mdmhost"}


def test_exchange_enrollment_key_401_raises_with_status_code():
    response = _mock_response(status_code=401, body={"detail": "invalid key"})
    with _patch_http_client(response):
        with pytest.raises(EnrollmentError) as exc_info:
            exchange_enrollment_key(
                host="https://t.example.com",
                enrollment_key="bad",
                username=None,
                device_name=None,
            )
    assert exc_info.value.status_code == 401
    assert "invalid key" in str(exc_info.value)


def test_exchange_enrollment_key_5xx_raises():
    response = _mock_response(status_code=503, body={})
    with _patch_http_client(response):
        with pytest.raises(EnrollmentError) as exc_info:
            exchange_enrollment_key(
                host="https://t.example.com",
                enrollment_key="k",
                username=None,
                device_name=None,
            )
    assert exc_info.value.status_code == 503


def test_exchange_enrollment_key_missing_api_key_raises():
    response = _mock_response(status_code=200, body={"unexpected": "shape"})
    with _patch_http_client(response):
        with pytest.raises(EnrollmentError) as exc_info:
            exchange_enrollment_key(
                host="https://t.example.com",
                enrollment_key="k",
                username=None,
                device_name=None,
            )
    assert "api_key" in str(exc_info.value)
    # Malformed-but-HTTP-200 carries status_code=200 so the typer wrapper can
    # exit 1 (server reachable, response shape wrong) vs 2 (transport error).
    assert exc_info.value.status_code == 200


def test_resolve_enrollment_identity_passes_through_when_both_provided(monkeypatch):
    monkeypatch.setenv("ENROLLMENT_USERNAME", "envuser")
    monkeypatch.setenv("ENROLLMENT_DEVICE_NAME", "envhost")
    assert resolve_enrollment_identity("alice", "alice-mac") == ("alice", "alice-mac")


def test_resolve_enrollment_identity_falls_back_to_env_then_os(monkeypatch):
    monkeypatch.delenv("ENROLLMENT_USERNAME", raising=False)
    monkeypatch.delenv("RUNLAYER_ENROLLMENT_USERNAME", raising=False)
    monkeypatch.setenv("ENROLLMENT_DEVICE_NAME", "envhost")
    monkeypatch.delenv("RUNLAYER_ENROLLMENT_DEVICE_NAME", raising=False)

    with (
        patch("runlayer_cli.enrollment.getpass.getuser", return_value="osuser"),
        patch("runlayer_cli.enrollment.socket.gethostname", return_value="oshost"),
    ):
        assert resolve_enrollment_identity(None, None) == ("osuser", "envhost")


def test_resolve_enrollment_identity_runlayer_prefixed_env_vars_honored(monkeypatch):
    monkeypatch.delenv("ENROLLMENT_USERNAME", raising=False)
    monkeypatch.setenv("RUNLAYER_ENROLLMENT_USERNAME", "rl_envuser")
    monkeypatch.delenv("ENROLLMENT_DEVICE_NAME", raising=False)
    monkeypatch.setenv("RUNLAYER_ENROLLMENT_DEVICE_NAME", "rl_envhost")

    assert resolve_enrollment_identity(None, None) == ("rl_envuser", "rl_envhost")


def test_resolve_enrollment_identity_returns_empty_when_os_lookup_blows_up(monkeypatch):
    monkeypatch.delenv("ENROLLMENT_USERNAME", raising=False)
    monkeypatch.delenv("RUNLAYER_ENROLLMENT_USERNAME", raising=False)
    monkeypatch.delenv("ENROLLMENT_DEVICE_NAME", raising=False)
    monkeypatch.delenv("RUNLAYER_ENROLLMENT_DEVICE_NAME", raising=False)

    with (
        patch("runlayer_cli.enrollment.getpass.getuser", side_effect=OSError("no tty")),
        patch(
            "runlayer_cli.enrollment.socket.gethostname",
            side_effect=OSError("no host"),
        ),
    ):
        assert resolve_enrollment_identity(None, None) == ("", "")


def test_exchange_enrollment_key_transport_error_raises():
    with _patch_http_client(None, raises=httpx.ConnectError("no route")):
        with pytest.raises(EnrollmentError) as exc_info:
            exchange_enrollment_key(
                host="https://t.example.com",
                enrollment_key="k",
                username=None,
                device_name=None,
            )
    assert "no route" in str(exc_info.value)
    assert exc_info.value.status_code is None


class TestWriteEnrollmentMarker:
    def test_creates_marker_at_expected_path(self, tmp_path: Path, monkeypatch):
        monkeypatch.setattr(Path, "home", lambda: tmp_path)

        write_enrollment_marker("https://t.example.com")

        assert (tmp_path / ".runlayer" / ".enrolled-t.example.com").is_file()

    def test_creates_runlayer_dir_when_missing(self, tmp_path: Path, monkeypatch):
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        assert not (tmp_path / ".runlayer").exists()

        write_enrollment_marker("https://t.example.com")

        assert (tmp_path / ".runlayer").is_dir()

    def test_is_idempotent(self, tmp_path: Path, monkeypatch):
        monkeypatch.setattr(Path, "home", lambda: tmp_path)

        write_enrollment_marker("https://t.example.com")
        write_enrollment_marker("https://t.example.com")

        marker = tmp_path / ".runlayer" / ".enrolled-t.example.com"
        assert marker.is_file()

    def test_refreshes_mtime_on_recall(self, tmp_path: Path, monkeypatch):
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        marker = tmp_path / ".runlayer" / ".enrolled-t.example.com"
        marker.parent.mkdir(parents=True)
        marker.touch()
        stale = time.time() - 3600
        import os

        os.utime(marker, (stale, stale))

        write_enrollment_marker("https://t.example.com")

        assert marker.stat().st_mtime > stale + 60

    def test_swallows_oserror(self, tmp_path: Path, monkeypatch):
        # Point home at a path that cannot be created (file blocks the dir).
        blocked = tmp_path / "blocked"
        blocked.write_text("not a dir")
        monkeypatch.setattr(Path, "home", lambda: blocked)

        # Must not raise.
        write_enrollment_marker("https://t.example.com")

    def test_path_for_default_port_omits_port(self):
        path = enrollment_marker_path(
            "https://t.example.com:443", home=Path("/Users/alice")
        )
        assert path.name == ".enrolled-t.example.com"

    def test_path_for_custom_port_includes_port(self):
        path = enrollment_marker_path(
            "https://t.example.com:8443", home=Path("/Users/alice")
        )
        assert path.name == ".enrolled-t.example.com:8443"
