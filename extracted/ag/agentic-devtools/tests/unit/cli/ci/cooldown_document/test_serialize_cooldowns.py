"""Tests for backwards-compatible cooldown serialization."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.cooldown import CooldownRecord, merge_cooldown, parse_cooldowns
from agentic_devtools.cli.ci.cooldown_document import MAX_WAKE_DOCUMENT_BYTES, serialize_cooldowns
from agentic_devtools.cli.shared.retry import DEFAULT_RATE_LIMIT_MAX_DELAY


class TestSerializeCooldowns:
    @pytest.mark.parametrize("stored,expected", [(1e300, 200), (150, 200), (300, 300)])
    def test_repairs_only_matching_deadline_and_preserves_metadata(self, stored, expected):
        payload = {
            "version": 8,
            "custom": {"enabled": True},
            "provider_cooldowns": {
                "github:TOKEN": {"resume_at": stored, "expires_at": 1e300, "custom": {"keep": True}},
                "github:OTHER": {"resume_at": 1e300, "custom": False},
                "azure:TOKEN": {"resume_at": "invalid"},
                "future": None,
            },
        }
        result = json.loads(
            serialize_cooldowns({"github:TOKEN": CooldownRecord(200)}, raw=json.dumps(payload), now=100)
        )
        assert result["provider_cooldowns"]["github:TOKEN"]["resume_at"] == expected
        assert result["provider_cooldowns"]["github:TOKEN"]["expires_at"] == 1e300
        assert result["provider_cooldowns"]["github:TOKEN"]["custom"] == {"keep": True}
        for key in ("github:OTHER", "azure:TOKEN", "future"):
            assert result["provider_cooldowns"][key] == payload["provider_cooldowns"][key]
        assert result["version"] == 8
        assert result["custom"] == {"enabled": True}
        assert parse_cooldowns(json.dumps(result), now=100)["github:TOKEN"].resume_at == expected

    @pytest.mark.parametrize("stored", [1e300, 300])
    @pytest.mark.parametrize("incoming", [100, 90, 1e300, True, None, "200", float("inf"), float("nan")])
    def test_invalid_canonical_deadline_does_not_replace_stored_state(self, stored, incoming):
        result = json.loads(
            serialize_cooldowns(
                {"github:TOKEN": CooldownRecord(incoming)},
                raw=json.dumps({"provider_cooldowns": {"github:TOKEN": {"resume_at": stored}}}),
                now=100,
            )
        )
        assert result["provider_cooldowns"]["github:TOKEN"]["resume_at"] == stored

    def test_new_expired_record_is_serialized_without_clamping(self):
        result = json.loads(serialize_cooldowns({"github:TOKEN": CooldownRecord(90)}, now=100))
        assert result["provider_cooldowns"]["github:TOKEN"]["resume_at"] == 90

    @pytest.mark.parametrize("explicit_now", [False, True])
    def test_serializer_reads_default_clock_once_and_reuses_explicit_time(self, explicit_now):
        deadline = 100 + DEFAULT_RATE_LIMIT_MAX_DELAY
        with patch(
            "agentic_devtools.cli.ci.cooldown_document.time.time", side_effect=[] if explicit_now else [100]
        ) as clock:
            result = serialize_cooldowns(
                {"github:TOKEN": CooldownRecord(deadline)},
                raw='{"provider_cooldowns":{"github:TOKEN":{"resume_at":1e300}}}',
                **({"now": 100} if explicit_now else {}),
            )
        assert clock.call_count == (0 if explicit_now else 1)
        assert parse_cooldowns(result, now=100)["github:TOKEN"].resume_at == deadline

    @pytest.mark.parametrize("explicit_now", [False, True])
    @pytest.mark.parametrize("stored", [1e300, 100 + DEFAULT_RATE_LIMIT_MAX_DELAY])
    @pytest.mark.parametrize("incoming", [200, 90])
    def test_merge_cooldown_shares_one_validation_time(self, explicit_now, stored, incoming):
        with patch("agentic_devtools.cli.ci.cooldown.time.time", side_effect=[] if explicit_now else [100]) as clock:
            result = merge_cooldown(
                json.dumps({"provider_cooldowns": {"github:TOKEN": {"resume_at": stored}}}),
                key="github:TOKEN",
                record=CooldownRecord(incoming),
                **({"now": 100} if explicit_now else {}),
            )
        assert clock.call_count == (0 if explicit_now else 1)
        expected = stored if incoming == 90 or stored != 1e300 else incoming
        assert json.loads(result)["provider_cooldowns"]["github:TOKEN"]["resume_at"] == expected

    def test_unknown_and_legacy_metadata_are_retained(self):
        result = json.loads(
            serialize_cooldowns(
                {"github:TOKEN": CooldownRecord(200)},
                raw='{"version":8,"provider_cooldowns":{"future":null,"github:TOKEN":{"custom":true}}}',
            )
        )
        assert result["version"] == 8
        assert result["provider_cooldowns"]["future"] is None
        assert result["provider_cooldowns"]["github:TOKEN"]["custom"] is True

    def test_future_cooldown_schema_is_not_overwritten(self):
        with pytest.raises(ValueError):
            serialize_cooldowns({}, raw='{"provider_cooldowns":[]}')

    def test_known_wake_document_byte_limit_applies_before_serialization_returns(self):
        raw = json.dumps(
            {
                "dispatcher_wakes": {"version": 1, "entries": {}},
                "legacy": "x" * MAX_WAKE_DOCUMENT_BYTES,
            }
        )
        with pytest.raises(ValueError, match="size"):
            serialize_cooldowns({}, raw=raw)
