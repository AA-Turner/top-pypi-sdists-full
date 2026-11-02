"""Tests for verifying persisted cooldown records."""

from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.cooldown_document import _preserves_cooldown_records


def test_requires_every_expected_record_to_be_preserved_without_shortening() -> None:
    expected = {"github:TEAM": CooldownRecord(140)}

    assert _preserves_cooldown_records(expected, expected)
    assert _preserves_cooldown_records({}, {})
    assert not _preserves_cooldown_records(expected, {})
    assert not _preserves_cooldown_records(expected, {"github:TEAM": CooldownRecord(130)})
