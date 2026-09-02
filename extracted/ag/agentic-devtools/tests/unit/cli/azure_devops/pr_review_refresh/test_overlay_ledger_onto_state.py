"""Tests for overlay_ledger_onto_state."""

from types import SimpleNamespace

from agentic_devtools.cli.azure_devops.pr_review_refresh import overlay_ledger_onto_state


def _state(files):
    return SimpleNamespace(files=files)


def _fe(status="unreviewed", summary=None):
    return SimpleNamespace(status=status, summary=summary)


def _entry(**overrides):
    entry = {"status": "complete", "outcome": "approve", "filePath": "/src/a.ts", "summary": "ok"}
    entry.update(overrides)
    return entry


class TestOverlayLedgerOntoState:
    def test_approve_sets_approved_and_summary(self):
        fe = _fe()
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": _entry()})
        assert fe.status == "approved"
        assert fe.summary == "ok"

    def test_request_changes_sets_needs_work(self):
        fe = _fe()
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": _entry(outcome="request-changes")})
        assert fe.status == "needs-work"

    def test_request_changes_with_suggestion_sets_needs_work(self):
        fe = _fe()
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": _entry(outcome="request-changes-with-suggestion")})
        assert fe.status == "needs-work"

    def test_non_complete_is_skipped(self):
        fe = _fe(status="unreviewed")
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": _entry(status="needs-info")})
        assert fe.status == "unreviewed"

    def test_missing_file_path_is_skipped(self):
        fe = _fe()
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": _entry(filePath=None)})
        assert fe.status == "unreviewed"

    def test_blank_file_path_is_skipped(self):
        fe = _fe()
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": _entry(filePath="")})
        assert fe.status == "unreviewed"

    def test_file_not_in_state_is_skipped(self):
        # No matching FileEntry — must not raise.
        overlay_ledger_onto_state(_state({}), {"k": _entry(filePath="/other.ts")})

    def test_missing_summary_preserves_existing(self):
        fe = _fe(summary="old")
        entry = _entry()
        del entry["summary"]
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": entry})
        assert fe.status == "approved"
        assert fe.summary == "old"

    def test_none_summary_preserves_existing(self):
        fe = _fe(summary="old")
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": _entry(summary=None)})
        assert fe.summary == "old"

    def test_empty_string_summary_updates_entry(self):
        """Empty-string summary must win (latest-attempt semantics)."""
        fe = _fe(summary="old")
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": _entry(summary="")})
        assert fe.status == "approved"
        assert fe.summary == ""

    def test_unknown_outcome_is_skipped(self):
        fe = _fe(status="unreviewed", summary="old")
        overlay_ledger_onto_state(_state({"/src/a.ts": fe}), {"k": _entry(outcome="unknown")})
        assert fe.status == "unreviewed"
        assert fe.summary == "old"
