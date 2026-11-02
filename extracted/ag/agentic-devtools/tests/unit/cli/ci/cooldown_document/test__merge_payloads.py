"""Tests for loss-resistant document merging."""

import pytest

from agentic_devtools.cli.ci.cooldown_document import _merge_payloads
from agentic_devtools.cli.shared.retry import DEFAULT_RATE_LIMIT_MAX_DELAY


class TestMergePayloads:
    @pytest.mark.parametrize(
        "stored",
        [
            1e300,
            True,
            False,
            None,
            "300",
            {},
            [],
            float("nan"),
            float("inf"),
            float("-inf"),
            -1,
            100,
            101 + DEFAULT_RATE_LIMIT_MAX_DELAY,
            10**400,
        ],
    )
    def test_active_canonical_replaces_only_matching_invalid_deadline(self, stored):
        left = {
            "github:TOKEN": {"resume_at": stored, "expires_at": 1e300, "custom": {"resume_at": 1e300}},
            "github:OTHER": {"resume_at": 1e300},
        }
        right = {"github:TOKEN": {"resume_at": 200, "expires_at": 300, "new": True}}
        result = _merge_payloads(left, right, _path=("provider_cooldowns",), now=100)
        assert result == {
            "github:TOKEN": {
                "resume_at": 200,
                "expires_at": 1e300,
                "custom": {"resume_at": 1e300},
                "new": True,
            },
            "github:OTHER": {"resume_at": 1e300},
        }
        assert left["github:TOKEN"]["resume_at"] is stored

    @pytest.mark.parametrize("stored", [1e300, 300, None, {}])
    @pytest.mark.parametrize(
        "incoming",
        [
            1e300,
            True,
            None,
            "400",
            {},
            [],
            float("nan"),
            float("inf"),
            -1,
            100,
            101 + DEFAULT_RATE_LIMIT_MAX_DELAY,
        ],
    )
    def test_invalid_canonical_leaves_stored_deadline_unchanged(self, stored, incoming):
        result = _merge_payloads(
            {"github:TOKEN": {"resume_at": stored}},
            {"github:TOKEN": {"resume_at": incoming}},
            _path=("provider_cooldowns",),
            now=100,
        )
        assert result["github:TOKEN"]["resume_at"] is stored

    @pytest.mark.parametrize(
        "stored,incoming",
        [(300, 200), (200, 300), (300, 300), (200, 100 + DEFAULT_RATE_LIMIT_MAX_DELAY)],
    )
    def test_valid_deadlines_keep_the_later_value(self, stored, incoming):
        result = _merge_payloads(
            {"github:TOKEN": {"resume_at": stored}},
            {"github:TOKEN": {"resume_at": incoming}},
            _path=("provider_cooldowns",),
            now=100,
        )
        assert result["github:TOKEN"]["resume_at"] == max(stored, incoming)

    @pytest.mark.parametrize("options", [{"now": 100}, {"_path": ("other",), "now": 100}])
    def test_time_alone_does_not_enable_cooldown_repair(self, options):
        left = {"provider_cooldowns": {"github:TOKEN": {"resume_at": 1e300}}}
        right = {"provider_cooldowns": {"github:TOKEN": {"resume_at": 200}}}
        assert _merge_payloads(left, right, **options) == left

    @pytest.mark.parametrize("path", [(), ("provider_cooldowns",)])
    def test_generic_merge_retains_numeric_maximum_without_time_opt_in(self, path):
        left = {"github:TOKEN": {"resume_at": 1e300, "expires_at": 1e300, "custom": True}}
        right = {"github:TOKEN": {"resume_at": 200, "expires_at": 300}}
        assert _merge_payloads(left, right, _path=path) == left

    def test_default_whole_document_merge_does_not_repair_cooldowns(self):
        left = {"provider_cooldowns": {"github:TOKEN": {"resume_at": 1e300}}}
        right = {"provider_cooldowns": {"github:TOKEN": {"resume_at": 200}}}
        assert _merge_payloads(left, right) == left

    def test_concurrent_wake_generations_keep_a_coherent_identity_and_ttl(self):
        older = {
            "version": 1,
            "identity": "old",
            "pr_number": 1,
            "head_sha": "abc",
            "event": "opened",
            "created_at": 100,
            "expires_at": 86500,
            "resume_at": 300,
            "status": "pending",
            "old_meta": True,
        }
        newer = dict(older, identity="new", created_at=110, expires_at=86510, resume_at=200, new_meta=True)
        left = {"dispatcher_wakes": {"version": 1, "entries": {"key": newer}}}
        right = {"dispatcher_wakes": {"version": 1, "entries": {"key": older}}}
        merged = _merge_payloads(left, right)["dispatcher_wakes"]["entries"]["key"]
        assert merged["identity"] == "old"
        assert merged["created_at"] == 100
        assert merged["expires_at"] == 86500
        assert merged["resume_at"] == 300
        assert merged["old_meta"] is True and merged["new_meta"] is True

    def test_unions_nested_fields_and_preserves_tombstones_and_longest_deadlines(self):
        left = {"entries": {"a": {"status": "delivered", "resume_at": 300, "expires_at": 400, "old": 1}}}
        right = {"entries": {"a": {"status": "pending", "resume_at": 200, "expires_at": 350, "new": 2}}}
        assert _merge_payloads(left, right) == {
            "entries": {"a": {"status": "delivered", "resume_at": 300, "expires_at": 400, "old": 1, "new": 2}}
        }
        assert left["entries"]["a"] == {"status": "delivered", "resume_at": 300, "expires_at": 400, "old": 1}

    def test_unknown_values_and_boolean_deadlines_do_not_crash(self):
        assert _merge_payloads({"resume_at": True}, {"resume_at": 3}) == {"resume_at": 3}
        assert _merge_payloads({"expires_at": 3}, {"expires_at": False}) == {"expires_at": False}
        assert _merge_payloads({"x": []}, {"x": {"new": 1}}) == {"x": {"new": 1}}
