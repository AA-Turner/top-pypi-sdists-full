"""Tests for dealcloud_sdk.data.references (reference field resolution and caching)."""

import pytest
from unittest.mock import MagicMock

from dealcloud_sdk.constants import field_types
from dealcloud_sdk.models.schema import Field
from dealcloud_sdk.data.models import ReferenceCache, ReferenceFormat
from dealcloud_sdk.data import references


class TestGetReferenceFields:
    """Tests for get_reference_fields."""

    def test_returns_only_reference_fields(self):
        """Only fields with fieldType REFERENCE are returned."""
        schema_client = MagicMock()
        schema_client.get_fields.return_value = [
            Field(apiName="Name", fieldType=field_types.TEXT),
            Field(apiName="PrimaryContact", fieldType=field_types.REFERENCE),
            Field(apiName="Status", fieldType=field_types.CHOICE),
            Field(apiName="Owner", fieldType=field_types.REFERENCE),
        ]
        result = references.get_reference_fields(schema_client, "Company")
        assert len(result) == 2
        assert result[0].apiName == "PrimaryContact"
        assert result[1].apiName == "Owner"
        schema_client.get_fields.assert_called_once_with("Company")

    def test_returns_empty_when_no_reference_fields(self):
        """Empty list when no REFERENCE fields."""
        schema_client = MagicMock()
        schema_client.get_fields.return_value = [
            Field(apiName="Name", fieldType=field_types.TEXT),
        ]
        result = references.get_reference_fields(schema_client, "Company")
        assert result == []


class TestFetchEntryNames:
    """Tests for fetch_entry_names."""

    def test_empty_entry_ids_returns_empty_dict(self):
        """Empty entry_ids returns {}."""
        data_client = MagicMock()
        result = references.fetch_entry_names(data_client, "Company", [])
        assert result == {}
        data_client.read_data.assert_not_called()

    def test_success_returns_entry_id_to_name_mapping(self):
        """Success returns dict entry_id -> name."""
        data_client = MagicMock()
        data_client.read_data.return_value = [
            {"EntryId": 1, "Name": "Company A"},
            {"EntryId": 2, "Name": "Company B"},
        ]
        result = references.fetch_entry_names(data_client, "Company", [1, 2])
        assert result == {1: "Company A", 2: "Company B"}
        data_client.read_data.assert_called_once()
        call_kw = data_client.read_data.call_args[1]
        assert call_kw["object_id"] == "Company"
        assert "EntryId in (1,2)" in call_kw["query"]
        assert call_kw["fields"] == ["EntryId", "Name"]
        assert call_kw["output"] == "list"

    def test_exception_returns_ids_as_fallback(self):
        """On exception returns entry_id -> str(entry_id) fallback."""
        data_client = MagicMock()
        data_client.read_data.side_effect = Exception("API error")
        result = references.fetch_entry_names(data_client, "Company", [1, 2])
        assert result == {1: "1", 2: "2"}

    def test_custom_name_field(self):
        """name_field is passed to read_data and used for display values."""
        data_client = MagicMock()
        data_client.read_data.return_value = [
            {"EntryId": 1, "Title": "CEO"},
        ]
        result = references.fetch_entry_names(
            data_client, "Role", [1], name_field="Title",
        )
        assert result == {1: "CEO"}
        assert data_client.read_data.call_args[1]["fields"] == ["EntryId", "Title"]

    def test_row_without_name_field_uses_entry_id_string(self):
        """When name column is absent, mapping uses str(EntryId) per row.get fallback."""
        data_client = MagicMock()
        data_client.read_data.return_value = [{"EntryId": 99}]
        result = references.fetch_entry_names(data_client, "X", [99])
        assert result == {99: "99"}


class TestResolveReferenceValue:
    """Tests for resolve_reference_value."""

    def test_none_returns_none(self):
        """None value returns None."""
        assert references.resolve_reference_value(None, ReferenceFormat.ID) is None

    def test_list_recurses(self):
        """List of values is resolved recursively."""
        cache = ReferenceCache()
        result = references.resolve_reference_value(
            [{"EntryId": 1, "Name": "A"}, {"EntryId": 2, "Name": "B"}],
            ReferenceFormat.ID,
            cache=cache,
        )
        assert result == [1, 2]

    def test_dict_id_format_returns_id(self):
        """Dict with reference_format ID returns id/entryId/EntryId."""
        assert references.resolve_reference_value(
            {"id": 10}, ReferenceFormat.ID
        ) == 10
        assert references.resolve_reference_value(
            {"entryId": 20}, ReferenceFormat.ID
        ) == 20
        assert references.resolve_reference_value(
            {"EntryId": 30}, ReferenceFormat.ID
        ) == 30

    def test_dict_name_format_embedded_name(self):
        """Dict with NAME format and embedded name returns name."""
        assert references.resolve_reference_value(
            {"EntryId": 1, "Name": "Acme"}, ReferenceFormat.NAME
        ) == "Acme"
        assert references.resolve_reference_value(
            {"EntryId": 1, "displayName": "Display"}, ReferenceFormat.NAME
        ) == "Display"
        assert references.resolve_reference_value(
            {"EntryId": 1, "name": "lower"}, ReferenceFormat.NAME
        ) == "lower"

    def test_dict_name_format_cache_hit(self):
        """Dict with NAME format uses cache when no embedded name."""
        cache = ReferenceCache()
        cache.set("Company", 1, "Cached Name")
        assert references.resolve_reference_value(
            {"EntryId": 1}, ReferenceFormat.NAME,
            target_object="Company", cache=cache,
        ) == "Cached Name"

    def test_dict_name_format_cache_miss_still_stringifies_id(self):
        """With cache + target_object, cache miss falls through to str(entry_id)."""
        cache = ReferenceCache()
        assert references.resolve_reference_value(
            {"EntryId": 5}, ReferenceFormat.NAME,
            target_object="Z", cache=cache,
        ) == "5"

    def test_dict_name_format_fallback_to_str_id(self):
        """Dict with NAME format and no cache returns str(entry_id)."""
        assert references.resolve_reference_value(
            {"EntryId": 1}, ReferenceFormat.NAME,
        ) == "1"

    def test_dict_id_format_missing_keys_returns_none(self):
        """Dict with no id keys for ID format returns None."""
        assert references.resolve_reference_value({}, ReferenceFormat.ID) is None

    def test_dict_name_format_empty_dict_returns_none(self):
        """Dict with NAME format and no id or name returns None."""
        assert references.resolve_reference_value({}, ReferenceFormat.NAME) is None

    def test_raw_int_id_format(self):
        """Raw int with ID format returns entry_id."""
        assert references.resolve_reference_value(42, ReferenceFormat.ID) == 42

    def test_raw_int_name_format_cache_hit(self):
        """Raw int with NAME format uses cache."""
        cache = ReferenceCache()
        cache.set("Company", 42, "The Company")
        assert references.resolve_reference_value(
            42, ReferenceFormat.NAME,
            target_object="Company", cache=cache,
        ) == "The Company"

    def test_raw_int_name_format_fallback(self):
        """Raw int with NAME format and no cache returns str(entry_id)."""
        assert references.resolve_reference_value(42, ReferenceFormat.NAME) == "42"

    def test_float_id_format_coerced_to_int(self):
        assert references.resolve_reference_value(3.0, ReferenceFormat.ID) == 3

    def test_float_name_format_cache_hit(self):
        cache = ReferenceCache()
        cache.set("T", 7, "Seven")
        assert references.resolve_reference_value(
            7.0, ReferenceFormat.NAME, target_object="T", cache=cache,
        ) == "Seven"

    def test_float_name_format_cache_miss_with_target(self):
        """Float NAME: cache lookup misses, falls back to str(int(value))."""
        cache = ReferenceCache()
        assert references.resolve_reference_value(
            4.0, ReferenceFormat.NAME, target_object="Z", cache=cache,
        ) == "4"

    def test_non_numeric_non_dict_passthrough(self):
        """Values that are not dict/list/int/float are returned unchanged."""
        assert references.resolve_reference_value("plain", ReferenceFormat.ID) == "plain"


class TestApplyReferenceFormat:
    """Tests for apply_reference_format."""

    def test_empty_rows_returns_rows_unchanged(self):
        """Empty rows returns rows unchanged."""
        data_client = MagicMock()
        assert references.apply_reference_format(
            data_client, [], "Company", ReferenceFormat.ID
        ) == []

    def test_no_ref_fields_returns_rows_unchanged(self):
        """No reference fields returns rows unchanged."""
        data_client = MagicMock()
        data_client.get_fields = MagicMock(return_value=[
            Field(apiName="Name", fieldType=field_types.TEXT),
        ])
        rows = [{"Name": "A", "EntryId": 1}]
        result = references.apply_reference_format(
            data_client, rows, "Company", ReferenceFormat.ID
        )
        assert result == rows

    def test_id_format_extracts_ids(self):
        """ID format extracts entry IDs from reference dicts."""
        data_client = MagicMock()
        data_client.get_fields = MagicMock(return_value=[
            Field(apiName="Contact", fieldType=field_types.REFERENCE, entryLists=[100]),
        ])
        rows = [{"EntryId": 1, "Contact": {"EntryId": 10, "Name": "John"}}]
        result = references.apply_reference_format(
            data_client, rows, "Company", ReferenceFormat.ID
        )
        assert result[0]["Contact"] == 10

    def test_name_format_with_cache_prefetches(self):
        """NAME format with cache calls prefetch and uses resolve_reference_value."""
        data_client = MagicMock()
        data_client.get_fields = MagicMock(return_value=[
            Field(apiName="Contact", fieldType=field_types.REFERENCE, entryLists=[100]),
        ])
        cache = ReferenceCache()
        cache.set("100", 10, "John Doe")
        rows = [{"EntryId": 1, "Contact": {"EntryId": 10}}]
        result = references.apply_reference_format(
            data_client, rows, "Company", ReferenceFormat.NAME, reference_cache=cache
        )
        assert result[0]["Contact"] == "John Doe"

    def test_name_format_without_cache_skips_prefetch(self):
        """NAME format with reference_cache=None does not call prefetch_reference_names."""
        data_client = MagicMock()
        data_client.get_fields = MagicMock(return_value=[
            Field(apiName="Contact", fieldType=field_types.REFERENCE, entryLists=[100]),
        ])
        rows = [{"EntryId": 1, "Contact": {"Name": "Embedded"}}]
        result = references.apply_reference_format(
            data_client, rows, "Company", ReferenceFormat.NAME, reference_cache=None,
        )
        assert result[0]["Contact"] == "Embedded"
        data_client.read_data.assert_not_called()

    def test_multi_entry_lists_uses_first_target_for_resolution(self):
        """When entryLists has multiple IDs, first is used as target object string."""
        data_client = MagicMock()
        data_client.get_fields = MagicMock(return_value=[
            Field(apiName="Contact", fieldType=field_types.REFERENCE, entryLists=[100, 200]),
        ])
        rows = [{"EntryId": 1, "Contact": {"EntryId": 10, "Name": "J"}}]
        result = references.apply_reference_format(
            data_client, rows, "Company", ReferenceFormat.ID,
        )
        assert result[0]["Contact"] == 10

    def test_empty_entry_lists_no_target_object_still_resolves_id(self):
        """Field with entryLists=[] has target None; ID format still extracts entry id."""
        data_client = MagicMock()
        data_client.get_fields = MagicMock(return_value=[
            Field(apiName="Loose", fieldType=field_types.REFERENCE, entryLists=[]),
        ])
        rows = [{"EntryId": 1, "Loose": {"EntryId": 9}}]
        result = references.apply_reference_format(
            data_client, rows, "Company", ReferenceFormat.ID,
        )
        assert result[0]["Loose"] == 9

    def test_row_without_some_reference_fields_unchanged_for_missing_keys(self):
        """Rows that omit a reference field are still returned; only present keys transform."""
        data_client = MagicMock()
        data_client.get_fields = MagicMock(return_value=[
            Field(apiName="A", fieldType=field_types.REFERENCE, entryLists=[1]),
            Field(apiName="B", fieldType=field_types.REFERENCE, entryLists=[2]),
        ])
        rows = [{"EntryId": 1, "A": {"EntryId": 5}}]
        result = references.apply_reference_format(
            data_client, rows, "Company", ReferenceFormat.ID,
        )
        assert result[0]["A"] == 5
        assert "B" not in result[0]


class TestPrefetchReferenceNames:
    """Tests for prefetch_reference_names."""

    def test_populates_cache_for_missing_ids(self):
        """Prefetch fetches names and populates cache."""
        data_client = MagicMock()
        data_client.read_data.return_value = [
            {"EntryId": 1, "Name": "Company One"},
            {"EntryId": 2, "Name": "Company Two"},
        ]
        cache = ReferenceCache()
        field_targets = {"PrimaryCompany": "Company"}
        rows = [
            {"EntryId": 1, "PrimaryCompany": 1},
            {"EntryId": 2, "PrimaryCompany": 2},
        ]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        assert cache.get("Company", 1) == "Company One"
        assert cache.get("Company", 2) == "Company Two"
        data_client.read_data.assert_called_once()

    def test_handles_dict_value_with_entry_id(self):
        """Prefetch extracts entry IDs from dict reference values."""
        data_client = MagicMock()
        data_client.read_data.return_value = [{"EntryId": 10, "Name": "Ten"}]
        cache = ReferenceCache()
        field_targets = {"Ref": "Obj"}
        rows = [{"EntryId": 1, "Ref": {"EntryId": 10}}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        assert cache.get("Obj", 10) == "Ten"

    def test_skips_falsy_reference_values(self):
        """Empty dict / missing values do not add IDs."""
        data_client = MagicMock()
        cache = ReferenceCache()
        field_targets = {"R": "O"}
        rows = [{"EntryId": 1, "R": {}}, {"EntryId": 2}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        data_client.read_data.assert_not_called()

    def test_skips_when_target_object_unresolved(self):
        """Reference field with no entryLists target does not collect IDs."""
        data_client = MagicMock()
        cache = ReferenceCache()
        field_targets = {"R": None}
        rows = [{"EntryId": 1, "R": 5}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        data_client.read_data.assert_not_called()

    def test_list_with_dict_and_raw_int_ids(self):
        """Multi-select references: mix of dict items and bare int IDs."""
        data_client = MagicMock()
        data_client.read_data.return_value = [
            {"EntryId": 1, "Name": "One"},
            {"EntryId": 2, "Name": "Two"},
        ]
        cache = ReferenceCache()
        field_targets = {"Tags": "TagObj"}
        rows = [{"EntryId": 1, "Tags": [{"id": 1}, 2]}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        assert cache.get("TagObj", 1) == "One"
        assert cache.get("TagObj", 2) == "Two"

    def test_raw_int_reference_value(self):
        """Single raw int reference value adds that ID."""
        data_client = MagicMock()
        data_client.read_data.return_value = [{"EntryId": 7, "Name": "Seven"}]
        cache = ReferenceCache()
        field_targets = {"Owner": "User"}
        rows = [{"EntryId": 1, "Owner": 7}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        assert cache.get("User", 7) == "Seven"

    def test_multi_target_entry_list_uses_first_for_id_collection(self):
        """field_targets may be a list; first element is the object key for prefetch."""
        data_client = MagicMock()
        data_client.read_data.return_value = [{"EntryId": 3, "Name": "Three"}]
        cache = ReferenceCache()
        field_targets = {"R": [300, 400]}
        rows = [{"EntryId": 1, "R": {"EntryId": 3}}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        assert cache.get("300", 3) == "Three"

    def test_prefetch_skips_fetch_when_all_ids_already_cached(self):
        """When get_missing is empty, fetch_entry_names is not called."""
        data_client = MagicMock()
        cache = ReferenceCache()
        cache.set("Obj", 1, "Already")
        field_targets = {"R": "Obj"}
        rows = [{"EntryId": 1, "R": 1}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        data_client.read_data.assert_not_called()

    def test_prefetch_list_ignores_non_id_items(self):
        """List entries that are not dict or int/float are skipped."""
        data_client = MagicMock()
        data_client.read_data.return_value = [
            {"EntryId": 1, "Name": "One"},
            {"EntryId": 2, "Name": "Two"},
        ]
        cache = ReferenceCache()
        field_targets = {"T": "O"}
        rows = [{"T": [{"id": 1}, "skipped-string", 2]}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        assert cache.get("O", 1) == "One"
        assert cache.get("O", 2) == "Two"

    def test_prefetch_list_dict_without_id_does_not_add(self):
        """Dict items in a multi-ref list with no id keys contribute nothing."""
        data_client = MagicMock()
        cache = ReferenceCache()
        field_targets = {"T": "O"}
        rows = [{"T": [{"label": "no-id"}, {"id": 3}]}]
        data_client.read_data.return_value = [{"EntryId": 3, "Name": "Three"}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        assert cache.get("O", 3) == "Three"

    def test_prefetch_single_dict_without_id_skips(self):
        """Top-level dict reference with no id/entryId keys adds no IDs."""
        data_client = MagicMock()
        cache = ReferenceCache()
        field_targets = {"R": "O"}
        rows = [{"R": {"label": "orphan"}}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        data_client.read_data.assert_not_called()

    def test_prefetch_string_value_does_not_match_numeric_branch(self):
        """Unexpected string reference value is ignored for ID collection."""
        data_client = MagicMock()
        cache = ReferenceCache()
        field_targets = {"R": "O"}
        rows = [{"R": "not-an-id"}]
        references.prefetch_reference_names(data_client, rows, field_targets, cache)
        data_client.read_data.assert_not_called()
