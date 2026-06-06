"""Tests for the ``aiwatch enroll`` typer subcommand.

Mirrors the operator-facing ``runlayer credentials enroll`` behavior but with
MDM-fallback resolution (host + enrollment key + optional username /
device-name pulled from ``mdm_config.read_managed_config()`` when CLI flags /
env vars are absent) and idempotent short-circuit when a credential already
exists.
"""

from __future__ import annotations

from unittest.mock import patch

from typer.testing import CliRunner

from runlayer_cli.aiwatch import app as aiwatch_app
from runlayer_cli.config import Config
from runlayer_cli.enrollment import EnrollmentResult

runner = CliRunner()


def _ok_result(api_key: str = "rl_user_new") -> EnrollmentResult:
    return EnrollmentResult(
        api_key=api_key, username="u@example.com", device_name="Mac-1"
    )


def _config(default_host: str = "https://t.example.com") -> Config:
    return Config(default_host=default_host)


def _config_with_secret(host: str, secret: str = "rl_user_existing") -> Config:
    return Config(
        default_host=host,
        hosts={
            "t.example.com": {"url": host, "secret": secret},
        },
    )


# ── happy path ───────────────────────────────────────────────────────


def test_enroll_uses_mdm_host_when_no_flag(tmp_path):
    config = _config(default_host="")
    config.default_host = None

    with (
        patch("runlayer_cli.commands.enroll.load_config", return_value=Config()),
        patch("runlayer_cli.enrollment.load_config", return_value=Config()),
        patch(
            "runlayer_cli.enrollment.read_managed_config",
            return_value={
                "host": "https://mdm.example.com",
                "enrollment_key": "rl_enroll_abc",
                "username": "u@example.com",
                "device_name": "Mac-1",
            },
        ),
        patch(
            "runlayer_cli.commands.enroll.exchange_enrollment_key",
            return_value=_ok_result(),
        ) as mock_ex,
        patch("runlayer_cli.commands.enroll.save_config") as mock_save,
        patch("runlayer_cli.commands.enroll.write_enrollment_marker") as mock_marker,
        patch.object(Config, "set_host_credentials", return_value=False),
    ):
        result = runner.invoke(aiwatch_app, ["enroll"])

    assert result.exit_code == 0, result.output
    assert "Enrollment successful" in result.output
    mock_ex.assert_called_once_with(
        host="https://mdm.example.com",
        enrollment_key="rl_enroll_abc",
        username="u@example.com",
        device_name="Mac-1",
    )
    mock_save.assert_called_once()
    mock_marker.assert_called_once_with("https://mdm.example.com")


def test_enroll_explicit_flags_override_mdm():
    with (
        patch("runlayer_cli.commands.enroll.load_config", return_value=Config()),
        patch("runlayer_cli.enrollment.load_config", return_value=Config()),
        patch(
            "runlayer_cli.enrollment.read_managed_config",
            return_value={
                "host": "https://mdm.example.com",
                "enrollment_key": "rl_enroll_mdm",
                "username": "mdm@example.com",
                "device_name": "MDM-Mac",
            },
        ),
        patch(
            "runlayer_cli.commands.enroll.exchange_enrollment_key",
            return_value=_ok_result(),
        ) as mock_ex,
        patch("runlayer_cli.commands.enroll.save_config"),
        patch.object(Config, "set_host_credentials", return_value=False),
    ):
        result = runner.invoke(
            aiwatch_app,
            [
                "enroll",
                "--host",
                "https://explicit.example.com",
                "--enrollment-key",
                "rl_enroll_explicit",
                "--username",
                "alice",
                "--device-name",
                "alice-laptop",
            ],
        )

    assert result.exit_code == 0, result.output
    mock_ex.assert_called_once_with(
        host="https://explicit.example.com",
        enrollment_key="rl_enroll_explicit",
        username="alice",
        device_name="alice-laptop",
    )


# ── idempotent short-circuit ─────────────────────────────────────────


def test_enroll_already_enrolled_skips_exchange():
    config = _config_with_secret("https://t.example.com")
    with (
        patch("runlayer_cli.commands.enroll.load_config", return_value=config),
        patch("runlayer_cli.enrollment.load_config", return_value=config),
        patch(
            "runlayer_cli.enrollment.read_managed_config",
            return_value={"enrollment_key": "rl_enroll_abc"},
        ),
        patch("runlayer_cli.commands.enroll.exchange_enrollment_key") as mock_ex,
        patch("runlayer_cli.commands.enroll.write_enrollment_marker") as mock_marker,
    ):
        result = runner.invoke(aiwatch_app, ["enroll"])

    assert result.exit_code == 0, result.output
    assert "Already enrolled" in result.output
    mock_ex.assert_not_called()
    # Self-migration: short-circuit still refreshes marker for pre-marker
    # enrollments so the bootstrap gate stops false-failing.
    mock_marker.assert_called_once_with("https://t.example.com")


def test_enroll_force_reruns_when_already_enrolled():
    config = _config_with_secret("https://t.example.com")
    with (
        patch("runlayer_cli.commands.enroll.load_config", return_value=config),
        patch("runlayer_cli.enrollment.load_config", return_value=config),
        patch(
            "runlayer_cli.enrollment.read_managed_config",
            return_value={"enrollment_key": "rl_enroll_abc"},
        ),
        patch(
            "runlayer_cli.commands.enroll.exchange_enrollment_key",
            return_value=_ok_result("rl_user_renewed"),
        ) as mock_ex,
        patch("runlayer_cli.commands.enroll.save_config"),
        patch("runlayer_cli.commands.enroll.write_enrollment_marker") as mock_marker,
        patch.object(Config, "set_host_credentials", return_value=False),
    ):
        result = runner.invoke(aiwatch_app, ["enroll", "--force"])

    assert result.exit_code == 0, result.output
    assert "Enrollment successful" in result.output
    mock_ex.assert_called_once()
    mock_marker.assert_called_once_with("https://t.example.com")


# ── missing inputs ───────────────────────────────────────────────────


def test_enroll_missing_host_exits_2(monkeypatch):
    monkeypatch.delenv("RUNLAYER_HOST", raising=False)
    with (
        patch("runlayer_cli.commands.enroll.load_config", return_value=Config()),
        patch("runlayer_cli.enrollment.load_config", return_value=Config()),
        patch(
            "runlayer_cli.enrollment.read_managed_config",
            return_value={},
        ),
    ):
        result = runner.invoke(aiwatch_app, ["enroll"])

    assert result.exit_code == 2, result.output
    assert "no host" in result.output


def test_enroll_missing_enrollment_key_exits_2(monkeypatch):
    monkeypatch.delenv("RUNLAYER_ENROLLMENT_API_KEY", raising=False)
    with (
        patch(
            "runlayer_cli.commands.enroll.load_config",
            return_value=_config(),
        ),
        patch(
            "runlayer_cli.enrollment.load_config",
            return_value=_config(),
        ),
        patch(
            "runlayer_cli.enrollment.read_managed_config",
            return_value={},
        ),
    ):
        result = runner.invoke(aiwatch_app, ["enroll"])

    assert result.exit_code == 2, result.output
    assert "no enrollment key" in result.output


# ── enrollment endpoint failure ──────────────────────────────────────


def test_enroll_endpoint_failure_exits_1():
    from runlayer_cli.enrollment import EnrollmentError

    with (
        patch(
            "runlayer_cli.commands.enroll.load_config",
            return_value=_config(),
        ),
        patch(
            "runlayer_cli.enrollment.load_config",
            return_value=_config(),
        ),
        patch(
            "runlayer_cli.enrollment.read_managed_config",
            return_value={"enrollment_key": "rl_enroll_abc"},
        ),
        patch(
            "runlayer_cli.commands.enroll.exchange_enrollment_key",
            side_effect=EnrollmentError("server down", status_code=503),
        ),
    ):
        result = runner.invoke(aiwatch_app, ["enroll"])

    assert result.exit_code == 1, result.output
    assert "server down" in result.output
