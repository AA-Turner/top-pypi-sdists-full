"""Tests for the best-effort check-in step of ``aiwatch enroll``.

Lives apart from ``test_enroll_command.py`` (which autouse-mocks
``_submit_validation_checkins``) so the *real* ``_submit_validation_checkins``
runs and its best-effort contract is exercised end to end.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from runlayer_cli.aiwatch import app as aiwatch_app
from runlayer_cli.commands.enroll import _submit_validation_checkins
from runlayer_cli.config import Config
from runlayer_cli.enrollment import EnrollmentResult

runner = CliRunner()


@pytest.mark.parametrize(
    "failing",
    [
        "runlayer_cli.api.RunlayerClient",
        "runlayer_cli.aiwatch_checkin._make_device_context",
        "runlayer_cli.scan.device.get_installed_tools",
    ],
)
def test_submit_validation_checkins_swallows_unexpected_setup_error(failing: str):
    """Setup (client ctor, device context, tool enumeration) runs outside the
    per-check-in isolation in ``submit_validation_checkins``. As a documented
    best-effort step that runs *after* enrollment already succeeded, an
    unexpected blow-up there must be swallowed, not propagated to ``enroll()``.
    """
    targets = {
        "runlayer_cli.api.RunlayerClient": patch("runlayer_cli.api.RunlayerClient"),
        "runlayer_cli.aiwatch_checkin._make_device_context": patch(
            "runlayer_cli.aiwatch_checkin._make_device_context"
        ),
        "runlayer_cli.scan.device.get_installed_tools": patch(
            "runlayer_cli.scan.device.get_installed_tools"
        ),
    }
    with (
        targets["runlayer_cli.api.RunlayerClient"] as client,
        targets["runlayer_cli.aiwatch_checkin._make_device_context"] as ctx,
        targets["runlayer_cli.scan.device.get_installed_tools"] as tools,
        patch("runlayer_cli.aiwatch_checkin.submit_validation_checkins"),
    ):
        {
            "runlayer_cli.api.RunlayerClient": client,
            "runlayer_cli.aiwatch_checkin._make_device_context": ctx,
            "runlayer_cli.scan.device.get_installed_tools": tools,
        }[failing].side_effect = RuntimeError("boom")

        # Must not raise.
        _submit_validation_checkins("https://t.example.com", "rl_user_x")


def test_enroll_succeeds_when_checkin_setup_raises():
    """A post-enrollment check-in failure must not turn a completed enrollment
    into a traceback + non-zero exit (contrast scan, where check-ins run inside
    the general ``try/except``).
    """
    with (
        patch("runlayer_cli.commands.enroll.load_config", return_value=Config()),
        patch("runlayer_cli.enrollment.load_config", return_value=Config()),
        patch(
            "runlayer_cli.enrollment.read_managed_config",
            return_value={
                "host": "https://mdm.example.com",
                "enrollment_key": "rl_enroll_abc",
            },
        ),
        patch(
            "runlayer_cli.commands.enroll.exchange_enrollment_key",
            return_value=EnrollmentResult(
                api_key="rl_user_new", username="u@example.com", device_name="Mac-1"
            ),
        ),
        patch("runlayer_cli.config.save_config"),
        patch.object(Config, "set_host_credentials", return_value=False),
        patch("runlayer_cli.api.RunlayerClient"),
        patch("runlayer_cli.aiwatch_checkin._make_device_context", return_value={}),
        patch(
            "runlayer_cli.scan.device.get_installed_tools",
            side_effect=RuntimeError("device scan blew up"),
        ),
    ):
        result = runner.invoke(aiwatch_app, ["enroll"])

    assert result.exit_code == 0, result.output
    assert "Enrollment successful" in result.output
