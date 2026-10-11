"""Tests for dealcloud_sdk.constants (field types and env names)."""

import pytest

from dealcloud_sdk.constants.field_types import (
    TEXT,
    CHOICE,
    REFERENCE,
    FIELD_TYPE_NAMES,
    FIELD_TYPE_IDS,
    get_field_type_name,
    get_field_type_id,
)


class TestFieldTypes:
    """Tests for field type constants and helpers."""

    def test_get_field_type_name_known(self):
        assert get_field_type_name(TEXT) == "Text"
        assert get_field_type_name(CHOICE) == "Choice"
        assert get_field_type_name(REFERENCE) == "Reference"
        assert get_field_type_name(1) == "Text"
        assert get_field_type_name(5) == "Reference"

    def test_get_field_type_name_unknown_returns_fallback(self):
        assert get_field_type_name(999) == "Unknown(999)"
        assert get_field_type_name(-1) == "Unknown(-1)"

    def test_get_field_type_id_known(self):
        assert get_field_type_id("Text") == 1
        assert get_field_type_id("Choice") == 2
        assert get_field_type_id("Reference") == 5

    def test_get_field_type_id_unknown_returns_minus_one(self):
        assert get_field_type_id("UnknownType") == -1
        assert get_field_type_id("") == -1

    def test_field_type_names_consistency(self):
        for fid, name in FIELD_TYPE_NAMES.items():
            assert get_field_type_id(name) == fid
            assert get_field_type_name(fid) == name


class TestFieldTypeNames:
    """Tests for FIELD_TYPE_NAMES and get_field_type_name."""

    def test_field_type_names_contains_all_types(self):
        """FIELD_TYPE_NAMES contains all expected field types."""
        from dealcloud_sdk.constants import field_types

        expected_types = [
            field_types.TEXT, field_types.CHOICE, field_types.NUMBER,
            field_types.DATE, field_types.REFERENCE, field_types.BOOLEAN,
            field_types.USER, field_types.BINARY, field_types.ENTRY_LIST_ID,
            field_types.COUNTER, field_types.IMAGE, field_types.DATA_SOURCE,
            field_types.CURRENCY,
        ]
        for ft in expected_types:
            assert ft in FIELD_TYPE_NAMES

    def test_get_field_type_name_returns_correct_names(self):
        """get_field_type_name returns correct human-readable names."""
        from dealcloud_sdk.constants import field_types

        assert get_field_type_name(field_types.TEXT) == "Text"
        assert get_field_type_name(field_types.CHOICE) == "Choice"
        assert get_field_type_name(field_types.REFERENCE) == "Reference"
        assert get_field_type_name(field_types.CURRENCY) == "Currency"

    def test_get_field_type_name_unknown_type(self):
        """get_field_type_name handles unknown types gracefully."""
        result = get_field_type_name(99999)
        assert "Unknown" in result
        assert "99999" in result


class TestGetFieldTypeId:
    """Tests for get_field_type_id function."""

    def test_get_field_type_id_returns_correct_ids(self):
        """get_field_type_id returns correct IDs."""
        from dealcloud_sdk.constants import field_types

        assert get_field_type_id("Text") == field_types.TEXT
        assert get_field_type_id("Choice") == field_types.CHOICE
        assert get_field_type_id("Reference") == field_types.REFERENCE

    def test_get_field_type_id_unknown_name(self):
        """get_field_type_id returns -1 for unknown names."""
        assert get_field_type_id("NonExistentType") == -1
