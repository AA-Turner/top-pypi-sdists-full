"""Wake envelopes must remain coherent when variable writers observe races."""

import pytest

from agentic_devtools.cli.ci.cooldown_document import _merge_wake_entry


@pytest.fixture
def entry():
    return {
        "version": 1,
        "identity": "first",
        "pr_number": 1,
        "head_sha": "abc",
        "event": "opened",
        "created_at": 100,
        "expires_at": 86500,
        "resume_at": 200,
        "status": "pending",
    }


class TestMergeWakeEntry:
    def test_same_generation_merges_deadlines_tombstones_and_unknown_metadata(self, entry):
        left = dict(entry, resume_at=300, status="delivered", custom={"old": True})
        right = dict(entry, resume_at=200, custom={"new": True})
        actual = _merge_wake_entry(left, right)
        assert actual == dict(left, custom={"old": True, "new": True})

    def test_different_generations_select_one_complete_envelope(self, entry):
        newer = dict(entry, identity="second", created_at=110, expires_at=86510, resume_at=300)
        assert _merge_wake_entry(entry, newer) == newer
        assert _merge_wake_entry(newer, entry) == newer
        delivered = dict(entry, status="delivered")
        assert _merge_wake_entry(delivered, newer) == delivered
        assert _merge_wake_entry(newer, delivered) == delivered

    def test_incomplete_unknown_record_is_not_assumed_to_be_a_known_envelope(self, entry):
        result = _merge_wake_entry({"version": 1, "identity": "partial"}, entry)
        assert result == entry

    @pytest.mark.parametrize(
        "overrides",
        [{"version": 9}, {"identity": None}, {"resume_at": []}, {"expires_at": True}],
    )
    def test_unknown_shapes_keep_existing_generic_metadata_semantics(self, entry, overrides):
        unknown = dict(entry, **overrides, custom={"future": True})
        result = _merge_wake_entry(entry, unknown)
        assert result["custom"] == {"future": True}
