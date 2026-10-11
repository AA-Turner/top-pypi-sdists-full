"""Tests for opt-in error enrichment utilities."""

from __future__ import annotations

from dealcloud_sdk.models.schema import Field
from dealcloud_sdk.utils.error_enrichment import (
    build_field_lookup,
    enrich_row_errors,
    field_lookup_from_fields,
    format_error_message_english,
    format_error_with_metadata,
    format_row_error_message_english,
    format_row_error_with_metadata,
    iter_row_error_items,
)
from dealcloud_sdk.utils.process_response_errors import _errors_from_cell_item


class TestFieldLookup:
    def test_from_field_map(self):
        field_map = {
            "Company": {
                "Revenue": {
                    "id": 2060083,
                    "name": "Revenue",
                    "apiName": "Revenue",
                    "type": "Currency",
                },
            }
        }
        lookup = build_field_lookup(field_map, "Company")
        assert lookup[2060083] == {"name": "Revenue", "apiName": "Revenue"}

    def test_from_fields(self):
        fields = [
            Field(id=10, name="Name", apiName="CompanyName"),
            Field(id=20, name="Revenue", apiName="Revenue"),
        ]
        lookup = field_lookup_from_fields(fields)
        assert lookup[10]["name"] == "Name"
        assert lookup[10]["apiName"] == "CompanyName"


class TestIterRowErrorItems:
    def test_rows_errors_array(self):
        error_row = {
            "EntryId": 1001,
            "Errors": [
                {
                    "fieldId": 10,
                    "field": "0",
                    "code": 400,
                    "description": "Invalid value",
                }
            ],
        }
        items = iter_row_error_items(error_row)
        assert len(items) == 1
        assert items[0]["fieldId"] == 10

    def test_cells_nested_shape(self):
        error_row = {
            "entryId": -1,
            "fieldId": 2060083,
            "error": {
                "field": "0",
                "code": 5010,
                "description": "Can't change value in calculated or smart field.",
            },
        }
        items = iter_row_error_items(error_row)
        assert items[0]["fieldId"] == 2060083
        assert items[0]["code"] == 5010

    def test_errors_from_cell_item_includes_field_id(self):
        cell_item = {
            "entryId": -1,
            "fieldId": 99,
            "error": {"code": 5010, "description": "blocked", "field": "0"},
        }
        items = _errors_from_cell_item(cell_item)
        assert items[0]["fieldId"] == 99


class TestEnrichRowErrors:
    def test_nested_error_shape(self):
        error_row = {
            "entryId": -1,
            "fieldId": 2060083,
            "error": {
                "field": "0",
                "code": 5010,
                "description": "Can't change value in calculated or smart field.",
            },
        }
        lookup = {2060083: {"name": "Revenue", "apiName": "Revenue"}}
        items = enrich_row_errors(error_row, lookup, object_name="Company")
        assert len(items) == 1
        assert items[0]["fieldName"] == "Revenue"
        assert items[0]["apiName"] == "Revenue"
        assert items[0]["fieldId"] == 2060083
        assert items[0]["entryId"] == -1
        assert items[0]["objectName"] == "Company"

    def test_unknown_field_id(self):
        error_row = {
            "EntryId": 1,
            "Errors": [{"fieldId": 999, "code": 1, "description": "bad"}],
        }
        items = enrich_row_errors(error_row, {}, object_name="Company")
        assert items[0]["fieldName"] is None
        assert items[0]["apiName"] is None


class TestFormatErrorWithMetadata:
    def test_includes_field_name_api_name_and_field_id(self):
        item = {
            "entryId": 42,
            "fieldId": 2060083,
            "fieldName": "Revenue",
            "apiName": "Revenue",
            "description": "Can't change value in calculated or smart field.",
            "objectName": "Company",
        }
        message = format_error_with_metadata(item)
        assert "EntryId 42" in message
        assert "Can't change value in calculated or smart field." in message
        assert "[Company, fieldName Revenue, apiName Revenue, fieldId 2060083]" in message
        assert "objectName" not in message
        assert "(code" not in message

    def test_row_wrapper(self):
        error_row = {
            "entryId": 42,
            "fieldId": 2060083,
            "error": {
                "field": "0",
                "code": 5010,
                "description": "Can't change value in calculated or smart field.",
            },
        }
        lookup = {2060083: {"name": "Revenue", "apiName": "Revenue"}}
        message = format_row_error_with_metadata(
            error_row, field_lookup=lookup, object_name="Company"
        )
        assert "[Company, fieldName Revenue, apiName Revenue, fieldId 2060083]" in message


class TestFormatErrorMessageEnglish:
    def test_english_only(self):
        item = {
            "entryId": 42,
            "fieldId": 2060083,
            "fieldName": "Revenue",
            "apiName": "Revenue",
            "description": "Can't change value in calculated or smart field.",
            "objectName": "Company",
        }
        message = format_error_message_english(item)
        assert "Revenue" in message
        assert "Company" in message
        assert "2060083" not in message
        assert "EntryId" not in message
        assert "apiName" not in message

    def test_row_wrapper(self):
        error_row = {
            "entryId": 42,
            "fieldId": 2060083,
            "error": {
                "code": 5010,
                "description": "Can't change value in calculated or smart field.",
            },
        }
        lookup = {2060083: {"name": "Revenue", "apiName": "Revenue"}}
        message = format_row_error_message_english(
            error_row, field_lookup=lookup, object_name="Company"
        )
        assert "The Revenue field on Company could not be updated" in message
