"""Unit tests for dealcloud_sdk.data.read module (view validation, list_configured_views, get_*_fields)."""

import pytest
from unittest.mock import MagicMock, patch

from dealcloud_sdk.data.read import (
    _validate_and_resolve_view_id,
    list_configured_views,
    resolve_view,
    resolve_view_display_name,
    get_choice_reference_fields,
    get_reference_fields,
)
from dealcloud_sdk.models.data import Rows
from dealcloud_sdk.models.schema import Field


class TestValidateAndResolveViewId:
    """Tests for _validate_and_resolve_view_id (include_nulls=False for views)."""

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_integer_view_id_validates_and_returns_include_nulls_false(self, mock_list_views):
        """Integer view_id validates against list_configured_views and returns include_nulls=False."""
        self_mock = MagicMock()
        mock_list_views.return_value.rows = [{"id": 12345, "name": "My View"}]

        resolved_id, include_nulls = _validate_and_resolve_view_id(self_mock, 12345)

        assert resolved_id == 12345
        assert include_nulls is False
        mock_list_views.assert_called_once_with(self_mock)

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_integer_view_id_not_found_raises_attribute_error(self, mock_list_views):
        """Unknown integer view_id raises AttributeError (wrapped from resolve_view)."""
        self_mock = MagicMock()
        mock_list_views.return_value.rows = [{"id": 999, "name": "Other"}]

        with pytest.raises(AttributeError) as exc_info:
            _validate_and_resolve_view_id(self_mock, 12345)

        assert "12345" in str(exc_info.value)
        mock_list_views.assert_called_once_with(self_mock)

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_string_view_id_resolves_and_returns_include_nulls_false(self, mock_list_views):
        """String view_id resolves name to ID and returns include_nulls=False."""
        self_mock = MagicMock()
        mock_list_views.return_value.rows = [
            {"id": 100, "name": "My View"},
        ]

        resolved_id, include_nulls = _validate_and_resolve_view_id(self_mock, "My View")

        assert resolved_id == 100
        assert include_nulls is False
        mock_list_views.assert_called_once_with(self_mock)

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_string_view_not_found_raises(self, mock_list_views):
        """String view_id with no matching view raises AttributeError."""
        self_mock = MagicMock()
        mock_list_views.return_value.rows = []

        with pytest.raises(AttributeError) as exc_info:
            _validate_and_resolve_view_id(self_mock, "Nonexistent View")

        assert "not found" in str(exc_info.value)
        mock_list_views.assert_called_once_with(self_mock)

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_string_view_multiple_matches_raises(self, mock_list_views):
        """String view_id with multiple matching names raises AttributeError."""
        self_mock = MagicMock()
        mock_list_views.return_value.rows = [
            {"id": 1, "name": "Dup View"},
            {"id": 2, "name": "Dup View"},
        ]

        with pytest.raises(AttributeError) as exc_info:
            _validate_and_resolve_view_id(self_mock, "Dup View")

        assert "Multiple views" in str(exc_info.value)
        mock_list_views.assert_called_once_with(self_mock)


class TestResolveView:
    """Tests for resolve_view."""

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_resolve_by_integer_id(self, mock_list_views):
        self_mock = MagicMock()
        row = {"id": 55, "name": "V", "primaryLists": [{"name": "Company"}]}
        mock_list_views.return_value.rows = [row]

        assert resolve_view(self_mock, 55) == row

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_resolve_by_name(self, mock_list_views):
        self_mock = MagicMock()
        row = {"id": 100, "name": "My View"}
        mock_list_views.return_value.rows = [row]

        assert resolve_view(self_mock, "My View") == row

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_resolve_integer_id_not_found_raises(self, mock_list_views):
        self_mock = MagicMock()
        mock_list_views.return_value.rows = []

        with pytest.raises(ValueError, match="View 999 not found"):
            resolve_view(self_mock, 999)

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_resolve_name_not_found_raises(self, mock_list_views):
        self_mock = MagicMock()
        mock_list_views.return_value.rows = []

        with pytest.raises(ValueError, match="View 'Missing' not found"):
            resolve_view(self_mock, "Missing")

    @patch('dealcloud_sdk.data.read.list_configured_views')
    def test_resolve_duplicate_names_raises(self, mock_list_views):
        self_mock = MagicMock()
        mock_list_views.return_value.rows = [
            {"id": 1, "name": "Dup"},
            {"id": 2, "name": "Dup"},
        ]

        with pytest.raises(ValueError, match="Multiple views named 'Dup'"):
            resolve_view(self_mock, "Dup")


class TestResolveViewDisplayName:
    """Tests for resolve_view_display_name."""

    @patch('dealcloud_sdk.data.read.resolve_view')
    def test_returns_name_when_present(self, mock_resolve):
        self_mock = MagicMock()
        mock_resolve.return_value = {"id": 55, "name": "My View"}

        assert resolve_view_display_name(self_mock, 55) == "My View"
        mock_resolve.assert_called_once_with(self_mock, 55)

    @patch('dealcloud_sdk.data.read.resolve_view')
    def test_returns_id_string_when_name_missing(self, mock_resolve):
        self_mock = MagicMock()
        mock_resolve.return_value = {"id": 55}

        assert resolve_view_display_name(self_mock, 55) == "55"


class TestListConfiguredViews:
    """Tests for list_configured_views (read module)."""

    def test_list_configured_views_returns_rows(self):
        self_mock = MagicMock()
        self_mock._views_url = "https://test.dealcloud.com/api/rest/v4/data/rows/view"
        self_mock._client.get.return_value = {"totalRecords": 2, "rows": [{"id": 1}, {"id": 2}]}

        result = list_configured_views(self_mock)

        assert isinstance(result, Rows)
        assert result.totalRecords == 2
        assert len(result.rows) == 2
        self_mock._client.get.assert_called_once_with("https://test.dealcloud.com/api/rest/v4/data/rows/view")

    def test_list_configured_views_with_is_private(self):
        self_mock = MagicMock()
        self_mock._views_url = "https://test.dealcloud.com/api/rest/v4/data/rows/view"
        self_mock._client.get.return_value = {"totalRecords": 0, "rows": []}

        list_configured_views(self_mock, is_private=True)

        self_mock._client.get.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/data/rows/view?isprivate=true"
        )


class TestGetChoiceReferenceFields:
    """Tests for get_choice_reference_fields (read module)."""

    def test_get_choice_reference_fields_filters_by_type(self):
        self_mock = MagicMock()
        self_mock.get_fields.return_value = [
            Field(apiName="Name", fieldType=1, id=1, entryListId=100),  # TEXT
            Field(apiName="Status", fieldType=2, id=2, entryListId=100),  # CHOICE
            Field(apiName="Contact", fieldType=5, id=3, entryListId=100),  # REFERENCE
            Field(apiName="Owner", fieldType=7, id=4, entryListId=100),  # USER
        ]

        result = get_choice_reference_fields(self_mock, "Company")

        assert len(result) == 3  # CHOICE, REFERENCE, USER
        api_names = {f.apiName for f in result}
        assert "Status" in api_names
        assert "Contact" in api_names
        assert "Owner" in api_names
        assert "Name" not in api_names


class TestGetReferenceFields:
    """Tests for get_reference_fields (read module) - delegates to references.get_reference_fields."""

    @patch('dealcloud_sdk.data.read.references.get_reference_fields')
    def test_get_reference_fields_delegates_to_references(self, mock_ref_get):
        mock_ref_get.return_value = [
            Field(apiName="PrimaryContact", fieldType=5, id=10, entryListId=100),
        ]
        self_mock = MagicMock()

        result = get_reference_fields(self_mock, "Company")

        assert len(result) == 1
        assert result[0].apiName == "PrimaryContact"
        mock_ref_get.assert_called_once_with(self_mock, "Company")
