"""Tests for dealcloud_sdk.data.models (ReferenceCache, BatchResult, ModifiedEntry, DeltaSyncResult, ReferenceFormat)."""

from datetime import datetime

import pytest

from dealcloud_sdk.data.models import (
    ReferenceFormat,
    ReferenceCache,
    BatchResult,
    ModifiedEntry,
    DeltaSyncResult,
)


class TestReferenceFormat:
    """Tests for ReferenceFormat enum."""

    def test_id_value(self):
        assert ReferenceFormat.ID.value == "id"

    def test_name_value(self):
        assert ReferenceFormat.NAME.value == "name"

    def test_members(self):
        assert list(ReferenceFormat) == [ReferenceFormat.ID, ReferenceFormat.NAME]


class TestReferenceCache:
    """Tests for ReferenceCache."""

    def test_get_miss_returns_none(self):
        cache = ReferenceCache()
        assert cache.get("Company", 1) is None

    def test_set_and_get(self):
        cache = ReferenceCache()
        cache.set("Company", 1, "Acme Corp")
        assert cache.get("Company", 1) == "Acme Corp"

    def test_get_updates_access_order(self):
        cache = ReferenceCache(max_entries=2)
        cache.set("Obj", 1, "A")
        cache.set("Obj", 2, "B")
        _ = cache.get("Obj", 1)  # move 1 to end of access order
        cache.set("Obj", 3, "C")  # evict oldest (2)
        assert cache.get("Obj", 2) is None
        assert cache.get("Obj", 1) == "A"
        assert cache.get("Obj", 3) == "C"

    def test_bulk_set(self):
        cache = ReferenceCache()
        cache.bulk_set("Company", {1: "Acme", 2: "Beta", 3: "Gamma"})
        assert cache.get("Company", 1) == "Acme"
        assert cache.get("Company", 2) == "Beta"
        assert cache.get("Company", 3) == "Gamma"

    def test_eviction_when_at_capacity(self):
        cache = ReferenceCache(max_entries=3)
        cache.set("Obj", 1, "A")
        cache.set("Obj", 2, "B")
        cache.set("Obj", 3, "C")
        assert cache.size == 3
        cache.set("Obj", 4, "D")  # should evict oldest (1)
        assert cache.size == 3
        assert cache.get("Obj", 1) is None
        assert cache.get("Obj", 2) == "B"
        assert cache.get("Obj", 3) == "C"
        assert cache.get("Obj", 4) == "D"

    def test_get_missing(self):
        cache = ReferenceCache()
        cache.set("Company", 1, "Acme")
        missing = cache.get_missing("Company", [1, 2, 3])
        assert missing == [2, 3]

    def test_get_missing_empty(self):
        cache = ReferenceCache()
        cache.set("Company", 1, "A")
        assert cache.get_missing("Company", [1]) == []

    def test_clear(self):
        cache = ReferenceCache()
        cache.set("Company", 1, "A")
        cache.clear()
        assert cache.size == 0
        assert cache.get("Company", 1) is None

    def test_size_property(self):
        cache = ReferenceCache()
        assert cache.size == 0
        cache.set("Obj", 1, "A")
        assert cache.size == 1

    def test_hit_rate_info(self):
        cache = ReferenceCache(max_entries=10)
        cache.set("Obj", 1, "A")
        assert "1/10" in cache.hit_rate_info
        assert "Cache size" in cache.hit_rate_info

    def test_object_id_as_int_normalized(self):
        cache = ReferenceCache()
        cache.set(100, 1, "Name")  # object_id as int
        assert cache.get(100, 1) == "Name"
        assert cache.get("100", 1) == "Name"

    def test_set_existing_key_updates_and_moves_in_access_order(self):
        cache = ReferenceCache()
        cache.set("Obj", 1, "A")
        cache.set("Obj", 1, "A-updated")  # same key: hits "key in _access_order" in set()
        assert cache.get("Obj", 1) == "A-updated"
        assert cache.size == 1


class TestBatchResult:
    """Tests for BatchResult."""

    def test_defaults(self):
        r = BatchResult()
        assert r.results == []
        assert r.errors == []
        assert r.total_requested == 0
        assert r.total_succeeded == 0
        assert r.total_failed == 0

    def test_construct_with_values(self):
        r = BatchResult(
            results=[{"id": 1}],
            errors=[{"id": 2, "error": "fail"}],
            total_requested=2,
            total_succeeded=1,
            total_failed=1,
        )
        assert r.has_errors is True
        assert r.success_rate == 50.0

    def test_has_errors_false(self):
        r = BatchResult(errors=[], total_requested=1, total_succeeded=1)
        assert r.has_errors is False

    def test_success_rate_zero_requested(self):
        r = BatchResult(total_requested=0)
        assert r.success_rate == 100.0


class TestModifiedEntry:
    """Tests for ModifiedEntry."""

    def test_from_api_lowercase_keys(self):
        data = {
            "entryId": 42,
            "modifiedDate": "2024-01-15T10:30:00Z",
            "isDeleted": False,
        }
        entry = ModifiedEntry.from_api(data)
        assert entry.entry_id == 42
        assert entry.modified_date.year == 2024
        assert entry.modified_date.month == 1
        assert entry.modified_date.day == 15
        assert entry.is_deleted is False

    def test_from_api_pascal_case_keys(self):
        data = {
            "EntryId": 99,
            "ModifiedDate": "2024-06-01T12:00:00Z",
            "IsDeleted": True,
        }
        entry = ModifiedEntry.from_api(data)
        assert entry.entry_id == 99
        assert entry.is_deleted is True

    def test_from_api_datetime_object(self):
        dt = datetime(2024, 3, 1, 14, 0, 0)
        data = {"entryId": 1, "modifiedDate": dt, "isDeleted": False}
        entry = ModifiedEntry.from_api(data)
        assert entry.modified_date == dt

    def test_direct_construction(self):
        dt = datetime(2024, 1, 1)
        entry = ModifiedEntry(entry_id=10, modified_date=dt, is_deleted=False)
        assert entry.entry_id == 10
        assert entry.modified_date == dt
        assert entry.is_deleted is False


class TestDeltaSyncResult:
    """Tests for DeltaSyncResult."""

    def test_defaults(self):
        r = DeltaSyncResult()
        assert r.modified_ids == []
        assert r.deleted_ids == []
        assert r.modified_data is None
        assert r.modified_since is None
        assert r.total_changes == 0
        assert r.has_modifications is False
        assert r.has_deletions is False

    def test_total_changes(self):
        r = DeltaSyncResult(modified_ids=[1, 2], deleted_ids=[3])
        assert r.total_changes == 3

    def test_has_modifications(self):
        r = DeltaSyncResult(modified_ids=[1])
        assert r.has_modifications is True
        r2 = DeltaSyncResult(modified_ids=[], deleted_ids=[1])
        assert r2.has_modifications is False

    def test_has_deletions(self):
        r = DeltaSyncResult(deleted_ids=[1, 2])
        assert r.has_deletions is True
        r2 = DeltaSyncResult(modified_ids=[1], deleted_ids=[])
        assert r2.has_deletions is False

    def test_construct_with_modified_data(self):
        r = DeltaSyncResult(
            modified_ids=[1],
            modified_data=[{"EntryId": 1, "Name": "Test"}],
            modified_since=datetime(2024, 1, 1),
        )
        assert r.modified_data == [{"EntryId": 1, "Name": "Test"}]
        assert r.modified_since.year == 2024
