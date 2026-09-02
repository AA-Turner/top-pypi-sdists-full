"""Tests for merge_cooldown()."""

import json

from agentic_devtools.cli.ci.cooldown import CooldownRecord, merge_cooldown, serialize_cooldowns


class TestMergeCooldown:
    """merge_cooldown() preserves the later active record."""

    def test_adds_record_when_missing(self) -> None:
        merged = merge_cooldown(
            None,
            key="github:GH_TOKEN",
            record=CooldownRecord(200, source="retry-after", updated_at=30),
            now=100,
        )

        assert json.loads(merged)["provider_cooldowns"]["github:GH_TOKEN"]["resume_at"] == 200

    def test_does_not_shorten_active_record(self) -> None:
        later = CooldownRecord(300, updated_at=20)
        raw = serialize_cooldowns({"github:GH_TOKEN": later})

        merged = merge_cooldown(
            raw,
            key="github:GH_TOKEN",
            record=CooldownRecord(200, source="retry-after", updated_at=30),
            now=100,
        )

        assert json.loads(merged)["provider_cooldowns"]["github:GH_TOKEN"]["resume_at"] == 300
