"""Tests for monotonic cooldown write verification."""

from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.cooldown_document import _preserves_cooldown_records


class TestPreservesCooldownRecords:
    def test_requires_every_expected_deadline_without_shortening(self):
        expected = {"github:TOKEN": CooldownRecord(200)}
        assert _preserves_cooldown_records(expected, {"github:TOKEN": CooldownRecord(300)})
        assert not _preserves_cooldown_records(expected, {"github:TOKEN": CooldownRecord(100)})
        assert not _preserves_cooldown_records(expected, {})
        assert _preserves_cooldown_records({}, {})
