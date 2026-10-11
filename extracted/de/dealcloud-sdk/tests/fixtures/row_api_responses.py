"""Canned DealCloud Rows API response bodies for mock contract tests."""

from __future__ import annotations

ROW_OK: dict = {"EntryId": 100, "Name": "Acme"}

ROW_ERROR_5009: dict = {
    "EntryId": 200,
    "Formula": "duplicate formula",
    "Errors": [
        {
            "field": "Formula",
            "code": 5009,
            "description": "Value is not unique",
        }
    ],
}

MIXED_BATCH: list[dict] = [ROW_OK, ROW_ERROR_5009]
ALL_ERRORS_BATCH: list[dict] = [ROW_ERROR_5009]
ALL_OK_BATCH: list[dict] = [ROW_OK]

# Insert responses use negative EntryId on error rows for correlation (-1 → index 0).
INSERT_ROW_OK: dict = {"EntryId": 1001, "Name": "Acme"}
INSERT_ROW_ERROR: dict = {
    "EntryId": -2,
    "Name": "b",
    "Errors": [
        {
            "field": "Formula",
            "code": 5009,
            "description": "Value is not unique",
        }
    ],
}
INSERT_MIXED_BATCH: list[dict] = [INSERT_ROW_OK, INSERT_ROW_ERROR]

# SDK parallel_put / parallel_post return nested lists (one inner list per HTTP payload).
PARALLEL_PUT_MIXED = [MIXED_BATCH]
PARALLEL_POST_MIXED = [MIXED_BATCH]
PARALLEL_PUT_ALL_OK = [ALL_OK_BATCH]
PARALLEL_POST_ALL_OK = [ALL_OK_BATCH]
PARALLEL_PUT_ALL_ERRORS = [ALL_ERRORS_BATCH]

# COLLECT mode: (nested batch results, transport_errors)
COLLECT_PUT_MIXED = ([MIXED_BATCH], [])
COLLECT_POST_MIXED = ([MIXED_BATCH], [])
COLLECT_DELETE_MIXED = ([MIXED_BATCH], [])

SCHEMA_FIELDS_GET_RESPONSE = [
    {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
    {"apiName": "Formula", "name": "Formula", "fieldType": 1, "id": 11, "entryListId": 100},
]
