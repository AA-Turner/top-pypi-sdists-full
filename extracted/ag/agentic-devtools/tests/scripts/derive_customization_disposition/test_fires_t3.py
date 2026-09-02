"""Tests for fires_t3 in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive, unit


def test_two_numbered_steps_fire() -> None:
    """T3's first limb is two or more numbered steps."""
    assert derive.fires_t3(unit(body="1. Do this.\n2. Then that.\n")) is True


def test_two_distinct_commands_fire() -> None:
    """T3's second limb is two or more distinct commands, however they are named."""
    body = "Run `agdt-set key value` first.\n\n```bash\nagdt-run-setup\n```\n"
    assert derive.fires_t3(unit(body=body)) is True


def test_one_step_and_one_command_does_not_fire() -> None:
    """A single instruction is not an ordered procedure."""
    assert derive.fires_t3(unit(body="1. Run `agdt-set key value`.\n")) is False
