"""Unit tests for dealcloud_sdk.constants.user_activity helpers."""

import pytest

from dealcloud_sdk.constants import user_activity as ua


def test_get_activity_type_name_unknown_returns_str_id():
    assert ua.get_activity_type_name(999) == "999"


def test_get_activity_type_id_valid_and_invalid():
    assert ua.get_activity_type_id("Login Successful") == 1
    with pytest.raises(ValueError, match="Unknown activity type name"):
        ua.get_activity_type_id("Not A Real Activity")


def test_get_source_type_name_unknown():
    assert ua.get_source_type_name(42) == "42"


def test_get_source_type_id_valid_and_invalid():
    assert ua.get_source_type_id("Web UI") == 1
    with pytest.raises(ValueError, match="Unknown source type name"):
        ua.get_source_type_id("Invalid Source")


def test_get_export_data_type_name_unknown():
    assert ua.get_export_data_type_name(99) == "99"


def test_get_export_data_type_id_valid_and_invalid():
    assert ua.get_export_data_type_id("Export Image") == 2
    with pytest.raises(ValueError, match="Unknown export data type name"):
        ua.get_export_data_type_id("Nope")


def test_getters_return_copies_or_fresh_dicts():
    d1 = ua.get_activity_types()
    d1[1] = "mutated"
    d2 = ua.get_activity_types()
    assert d2[1] == "Login Successful"


def test_type_ids_list_helpers_return_tuples():
    assert ua.get_activity_type_ids()[0] == (1, "Login Successful")
    assert ua.get_source_type_ids()[0] == (1, "Web UI")
    assert ua.get_export_data_type_ids()[0] == (0, "Export Data")
