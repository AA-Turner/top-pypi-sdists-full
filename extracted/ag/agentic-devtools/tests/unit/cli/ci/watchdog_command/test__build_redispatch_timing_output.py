"""Tests for _build_redispatch_timing_output()."""

from datetime import UTC, datetime

from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.watchdog_command import _build_redispatch_timing_output


def test_sets_cooldown_wait_from_latest_run() -> None:
    now = datetime(2026, 7, 27, 10, 0, 0, tzinfo=UTC)
    latest_run = {"status": "completed", "conclusion": "success", "updated_at": "2026-07-27T09:59:10Z"}

    output = _build_redispatch_timing_output(latest_run, None, now)

    assert output["sleep_seconds"] == 15
    assert output["throttle_reason"] == "cooldown"


def test_keeps_existing_sleep_when_provider_wait_is_shorter() -> None:
    now = datetime(2026, 7, 27, 10, 0, 0, tzinfo=UTC)
    latest_run = {"status": "completed", "conclusion": "success", "updated_at": "2026-07-27T09:59:10Z"}
    paused = ("github:SPECKIT_PR_TOKEN", CooldownRecord(resume_at=now.timestamp() + 10, updated_at=100))

    output = _build_redispatch_timing_output(latest_run, paused, now)

    assert output["sleep_seconds"] == 15
    assert output["throttle_reason"] == "cooldown"
