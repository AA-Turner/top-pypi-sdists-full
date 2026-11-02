"""Tests for _evict_oldest."""

from __future__ import annotations

from agentic_devtools.cli.github.issue_dedup_integration import (
    LEDGER_MAX_ENTRIES,
    _evict_oldest,
)


class TestEvictOldest:
    """Tests for _evict_oldest."""

    def test_under_limit_returns_unchanged(self) -> None:
        """Under limit: dict returned as-is."""
        entries = {"sig1": {"created_utc": "2024-01-01T00:00:00Z", "issue_number": 1}}
        result = _evict_oldest(entries)
        assert result == entries

    def test_at_limit_returns_unchanged(self) -> None:
        """At exactly LEDGER_MAX_ENTRIES: no eviction."""
        entries = {
            f"sig{i:04d}": {"created_utc": f"2024-01-01T{i // 60:02d}:{i % 60:02d}:00Z", "issue_number": i}
            for i in range(LEDGER_MAX_ENTRIES)
        }
        result = _evict_oldest(entries)
        assert len(result) == LEDGER_MAX_ENTRIES

    def test_over_limit_evicts_oldest(self) -> None:
        """Over limit: oldest by created_utc is evicted."""
        entries = {
            f"sig{i:04d}": {"created_utc": f"2024-01-{i + 1:02d}T00:00:00Z", "issue_number": i}
            for i in range(LEDGER_MAX_ENTRIES + 1)
        }
        result = _evict_oldest(entries)
        assert len(result) == LEDGER_MAX_ENTRIES
        # sig0000 has the oldest timestamp (Jan 1) and should be evicted
        assert "sig0000" not in result

    def test_tie_breaking_by_lexicographic_key(self) -> None:
        """When timestamps are equal, evicts by ascending lexicographic key."""
        entries = {
            f"sig{i:04d}": {"created_utc": "2024-01-01T00:00:00Z", "issue_number": i}
            for i in range(LEDGER_MAX_ENTRIES + 2)
        }
        result = _evict_oldest(entries)
        assert len(result) == LEDGER_MAX_ENTRIES
        # sig0000 and sig0001 have the smallest lexicographic keys (same timestamp)
        assert "sig0000" not in result
        assert "sig0001" not in result

    def test_null_created_utc_does_not_raise(self) -> None:
        """Entries with null created_utc sort stably without raising TypeError."""
        entries = {f"sig{i:04d}": {"created_utc": None, "issue_number": i} for i in range(LEDGER_MAX_ENTRIES + 1)}
        result = _evict_oldest(entries)
        assert len(result) == LEDGER_MAX_ENTRIES

    def test_numeric_created_utc_does_not_raise(self) -> None:
        """Entries with numeric created_utc (corrupted) sort stably without TypeError."""
        entries = {f"sig{i:04d}": {"created_utc": i, "issue_number": i} for i in range(LEDGER_MAX_ENTRIES + 1)}
        result = _evict_oldest(entries)
        assert len(result) == LEDGER_MAX_ENTRIES

    def test_non_dict_entry_value_does_not_raise(self) -> None:
        """Entries whose value is not a dict (corrupted) sort stably without TypeError."""
        # Mix normal dict entries with non-dict values (strings) to exceed the cap
        entries: dict = {
            f"sig{i:04d}": {"created_utc": f"2024-01-{i + 1:02d}T00:00:00Z", "issue_number": i}
            for i in range(LEDGER_MAX_ENTRIES)
        }
        # Add one non-dict entry to push over the cap — exercises the else branch in sort_key
        entries["sig_bad"] = "not-a-dict"
        result = _evict_oldest(entries)
        assert len(result) == LEDGER_MAX_ENTRIES
