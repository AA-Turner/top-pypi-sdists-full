"""Tests for the hook's lazy-enrollment fallback in relay._load_credentials.

When no user secret is found locally but MDM has pushed an EnrollmentKey,
the hook attempts a one-shot exchange against /api/v1/mdm/enroll on the
first hook fire and persists the resulting per-user API key via
``Config.set_host_credentials``. Repeated fires within 60s skip the
exchange (cooldown touch file).
"""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import patch

import pytest

from runlayer_cli.config import Config
from runlayer_cli.enrollment import EnrollmentError, EnrollmentResult
from runlayer_cli.hook import relay


def _ok_result(
    api_key: str = "rl_user_xyz",
    username: str = "",
    device_name: str = "",
) -> EnrollmentResult:
    return EnrollmentResult(api_key=api_key, username=username, device_name=device_name)


@pytest.fixture
def fake_runlayer_dir(tmp_path: Path, monkeypatch):
    """Redirect get_runlayer_dir to a tmp dir for the cooldown touch file."""
    state_dir = tmp_path / ".runlayer"
    state_dir.mkdir()
    monkeypatch.setattr(relay, "get_runlayer_dir", lambda: state_dir)
    return state_dir


def test_lazy_enrollment_persists_user_secret_on_first_fire(
    fake_runlayer_dir: Path,
):
    """No prior secret + MDM enrollment_key → exchange + persist."""
    host = "https://t.example.com"
    api_key = "rl_user_xyz"

    cfg = Config(default_host=host)
    saved_credentials: dict[str, str] = {}

    def _fake_set(self_cfg: Config, url: str, secret: str) -> bool:
        saved_credentials[url] = secret
        return True

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={
                "host": host,
                "enrollment_key": "rl_enroll_abc",
                "username": "u@example.com",
                "device_name": "Mac-1",
            },
        ),
        patch.object(
            relay,
            "exchange_enrollment_key",
            return_value=_ok_result(api_key, "u@example.com", "Mac-1"),
        ) as mock_exchange,
        patch.object(relay, "save_config", lambda *_: None),
        patch.object(relay, "write_enrollment_marker") as mock_marker,
        patch.object(Config, "set_host_credentials", _fake_set),
    ):
        got_host, got_secret = relay._load_credentials()

    assert got_host == host
    assert got_secret == api_key
    assert saved_credentials.get(host) == api_key
    mock_exchange.assert_called_once_with(
        host=host,
        enrollment_key="rl_enroll_abc",
        username="u@example.com",
        device_name="Mac-1",
    )
    # Cooldown touch file written.
    assert (fake_runlayer_dir / ".enrollment-attempt").exists()
    # Gate witness dropped so a subsequent bootstrap LaunchDaemon cycle
    # sees this user as enrolled.
    mock_marker.assert_called_once_with(host)


def test_lazy_enrollment_passes_raw_managed_values_to_exchange(
    fake_runlayer_dir: Path,
):
    """``Username`` / ``DeviceName`` absent from MDM → raw ``None`` reaches
    ``exchange_enrollment_key``, which owns env/OS fallback resolution."""
    cfg = Config(default_host="https://t.example.com")

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={
                "host": "https://t.example.com",
                "enrollment_key": "rl_enroll_abc",
            },
        ),
        patch.object(
            relay,
            "exchange_enrollment_key",
            return_value=_ok_result("k", "osuser", "oshost"),
        ) as mock_ex,
        patch.object(relay, "save_config", lambda *_: None),
        patch.object(Config, "set_host_credentials", lambda *_args, **_kw: True),
    ):
        relay._load_credentials()

    mock_ex.assert_called_once_with(
        host="https://t.example.com",
        enrollment_key="rl_enroll_abc",
        username=None,
        device_name=None,
    )


def test_lazy_enrollment_no_enrollment_key_raises(fake_runlayer_dir: Path):
    """No prior secret AND no enrollment key → fail closed (RelayError(1))."""
    cfg = Config(default_host="https://t.example.com")

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay, "read_managed_config", return_value={"host": "https://t.example.com"}
        ),
        patch.object(relay, "exchange_enrollment_key") as mock_ex,
    ):
        with pytest.raises(relay.RelayError) as exc:
            relay._load_credentials()

    assert exc.value.exit_code == 1
    mock_ex.assert_not_called()
    # Did NOT touch cooldown file (nothing was attempted).
    assert not (fake_runlayer_dir / ".enrollment-attempt").exists()


def test_lazy_enrollment_cooldown_skips_exchange(fake_runlayer_dir: Path):
    """Recent attempt → skip the exchange, fail closed."""
    cooldown_file = fake_runlayer_dir / ".enrollment-attempt"
    cooldown_file.touch()
    cfg = Config(default_host="https://t.example.com")

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={
                "host": "https://t.example.com",
                "enrollment_key": "rl_enroll_abc",
            },
        ),
        patch.object(relay, "exchange_enrollment_key") as mock_ex,
    ):
        with pytest.raises(relay.RelayError):
            relay._load_credentials()
        mock_ex.assert_not_called()


def test_lazy_enrollment_cooldown_expires_after_window(fake_runlayer_dir: Path):
    """Stale touch file (>60s) → enrollment is retried."""
    cooldown_file = fake_runlayer_dir / ".enrollment-attempt"
    cooldown_file.touch()
    old_mtime = time.time() - 120
    import os

    os.utime(cooldown_file, (old_mtime, old_mtime))

    cfg = Config(default_host="https://t.example.com")

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={
                "host": "https://t.example.com",
                "enrollment_key": "rl_enroll_abc",
            },
        ),
        patch.object(
            relay, "exchange_enrollment_key", return_value=_ok_result("k")
        ) as mock_ex,
        patch.object(relay, "save_config", lambda *_: None),
        patch.object(Config, "set_host_credentials", lambda *a, **k: True),
    ):
        host_, secret_ = relay._load_credentials()

    assert secret_ == "k"
    mock_ex.assert_called_once()


def test_lazy_enrollment_failure_falls_through_to_relay_error(
    fake_runlayer_dir: Path,
):
    """Exchange failure → fail closed (caller sees RelayError(1))."""
    cfg = Config(default_host="https://t.example.com")

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={
                "host": "https://t.example.com",
                "enrollment_key": "rl_enroll_abc",
            },
        ),
        patch.object(
            relay,
            "exchange_enrollment_key",
            side_effect=EnrollmentError("server down", status_code=503),
        ),
    ):
        with pytest.raises(relay.RelayError) as exc:
            relay._load_credentials()

    assert exc.value.exit_code == 1


def test_lazy_enrollment_emits_fallback_warning_event(fake_runlayer_dir: Path):
    """Successful lazy enrollment must POST aiwatch.lazy_enrollment_fallback_hit.

    The enroll LaunchAgent + bootstrap LaunchDaemon (macOS) / Intune
    Remediation (Windows) is supposed to handle enroll-before-first-hook
    in normal operation; hitting this fallback means bootstrap didn't run
    (or didn't run as the right user). The
    structured warning event lets the backend surface that in the operator
    dashboard.
    """
    host = "https://t.example.com"
    cfg = Config(default_host=host)

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={
                "host": host,
                "enrollment_key": "rl_enroll_abc",
                "username": "u@example.com",
                "device_name": "Mac-1",
            },
        ),
        patch.object(
            relay,
            "exchange_enrollment_key",
            return_value=_ok_result("rl_user_key", "u@example.com", "Mac-1"),
        ),
        patch.object(relay, "save_config", lambda *_: None),
        patch.object(Config, "set_host_credentials", lambda *_args, **_kw: True),
        patch.object(relay, "forward_event") as mock_forward,
    ):
        relay._load_credentials()

    mock_forward.assert_called_once()
    kwargs = mock_forward.call_args.kwargs
    assert kwargs["client_name"] == "aiwatch_hook"
    assert kwargs["event_name"] == "aiwatch.lazy_enrollment_fallback_hit"
    payload = kwargs["payload"]
    assert payload["host"] == host
    assert payload["username"] == "u@example.com"
    assert payload["device_name"] == "Mac-1"


def test_lazy_enrollment_warning_event_failure_does_not_break_enrollment(
    fake_runlayer_dir: Path,
):
    """The fallback warning is best-effort — its failure must not prevent us
    from returning the freshly-minted user API key."""
    host = "https://t.example.com"
    cfg = Config(default_host=host)

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={
                "host": host,
                "enrollment_key": "rl_enroll_abc",
            },
        ),
        patch.object(
            relay,
            "exchange_enrollment_key",
            return_value=_ok_result("rl_user_key"),
        ),
        patch.object(relay, "save_config", lambda *_: None),
        patch.object(Config, "set_host_credentials", lambda *_args, **_kw: True),
        patch.object(
            relay,
            "forward_event",
            side_effect=RuntimeError("relay endpoint unreachable"),
        ),
    ):
        host_, secret_ = relay._load_credentials()

    assert host_ == host
    assert secret_ == "rl_user_key"


def test_load_credentials_normalizes_mdm_host_with_trailing_slash(
    fake_runlayer_dir: Path,
):
    """MDM ``Host`` with trailing slash must be normalized before relay POST.

    Regression: ``config.default_host`` is normalized at write time via
    ``set_host_credentials``; the MDM-host fallback inherits no such guarantee
    and a tenant ``Host`` value of ``https://tenant.example.com/`` would let
    ``_post`` build ``https://tenant.example.com//api/v1/hooks/cursor`` (double
    slash). Mirrors ``enrollment.resolve_host`` which ``normalize_url``s every
    source.
    """
    host_with_slash = "https://tenant.example.com/"
    host_normalized = "https://tenant.example.com"
    api_key = "rl_user_xyz"

    cfg = Config()

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={"host": host_with_slash},
        ),
        patch.object(Config, "get_secret_for_host", lambda _self, _url: api_key),
    ):
        got_host, got_secret = relay._load_credentials()

    assert got_host == host_normalized
    assert got_secret == api_key


def test_lazy_enrollment_normalizes_mdm_host_with_trailing_slash(
    fake_runlayer_dir: Path,
):
    """MDM-driven lazy enrollment must exchange against the normalized host.

    Without normalization, ``exchange_enrollment_key`` and downstream
    ``_post`` calls would both see the trailing slash, producing
    ``https://t.example.com//api/v1/mdm/enroll`` style URLs.
    """
    host_with_slash = "https://t.example.com/"
    host_normalized = "https://t.example.com"
    cfg = Config()

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={
                "host": host_with_slash,
                "enrollment_key": "rl_enroll_abc",
            },
        ),
        patch.object(
            relay,
            "exchange_enrollment_key",
            return_value=_ok_result("rl_user_key"),
        ) as mock_ex,
        patch.object(relay, "save_config", lambda *_: None),
        patch.object(Config, "set_host_credentials", lambda *_a, **_kw: True),
    ):
        got_host, got_secret = relay._load_credentials()

    assert got_host == host_normalized
    assert got_secret == "rl_user_key"
    assert mock_ex.call_args.kwargs["host"] == host_normalized


def test_lazy_enrollment_no_recursion_when_disk_writes_fail(
    fake_runlayer_dir: Path,
):
    """Regression: forward_event -> _load_credentials must not re-enter
    _try_lazy_enrollment, even when both `save_config` and
    `_touch_enrollment_attempt` fail (shared filesystem failure domain
    with the cooldown touch file) and the keyring write also no-ops.

    Without the in-memory guard, a read-only `~/.runlayer/` directory plus a
    failing keyring would cause the post-success warning event to recurse
    and re-run the network exchange + warning forever (stack overflow).
    """
    host = "https://t.example.com"
    cfg = Config(default_host=host)
    exchange_calls = 0

    def _counting_exchange(**_kwargs):
        nonlocal exchange_calls
        exchange_calls += 1
        return _ok_result("rl_user_key")

    def _real_forward_event(**_kwargs):
        # Mirror _forward_post: re-resolve credentials. Without the guard
        # this re-enters _try_lazy_enrollment and bumps exchange_calls.
        try:
            relay._load_credentials()
        except relay.RelayError:
            pass

    with (
        patch.object(relay, "load_config", return_value=cfg),
        patch.object(
            relay,
            "read_managed_config",
            return_value={
                "host": host,
                "enrollment_key": "rl_enroll_abc",
            },
        ),
        patch.object(relay, "exchange_enrollment_key", side_effect=_counting_exchange),
        patch.object(relay, "save_config", side_effect=OSError("read-only fs")),
        patch.object(relay, "_touch_enrollment_attempt", lambda: None),
        patch.object(Config, "set_host_credentials", lambda *_a, **_kw: False),
        patch.object(relay, "forward_event", side_effect=_real_forward_event),
    ):
        host_, secret_ = relay._load_credentials()

    assert host_ == host
    assert secret_ == "rl_user_key"
    assert exchange_calls == 1
    assert relay._lazy_enrollment_in_progress is False
