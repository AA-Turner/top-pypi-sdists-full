"""
Parametrized unit tests for ``dealcloud_sdk.utils.process_response_errors``.

Consolidates the HTTP status → exception mapping and a few edge cases so
regressions are visible in one module (supplements ``test_utils.TestProcessResponseErrors``
and ``test_http_error_propagation``).
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from intapp_rest_client.exceptions import HttpError

from dealcloud_sdk.utils.process_response_errors import (
    DealCloudApiError,
    DealCloudAuthError,
    DealCloudRateLimitError,
    DealCloudValidationError,
    finalize_list_response,
    handle_http_error,
    process_errors,
    split_cell_store_results,
    split_row_results,
    transform_http_error,
    with_error_handling,
)


@pytest.mark.parametrize(
    ("status", "body", "headers", "exc_type", "extra_check"),
    [
        (
            400,
            {"message": "bad", "errors": [{"message": "field", "errorCode": "E1"}]},
            {},
            DealCloudValidationError,
            lambda e: e.status_code == 400 and "field" in str(e),
        ),
        (401, {"message": "no token"}, {}, DealCloudAuthError, lambda e: e.status_code == 401),
        (403, {"message": "nope"}, {}, DealCloudAuthError, lambda e: e.status_code == 403),
        (404, {"message": "gone"}, {}, DealCloudApiError, lambda e: e.status_code == 404),
        (
            429,
            {"message": "slow"},
            {"Retry-After": "42"},
            DealCloudRateLimitError,
            lambda e: e.retry_after == 42,
        ),
        (502, {"message": "gw"}, {}, DealCloudApiError, lambda e: e.status_code == 502),
        (503, None, {}, DealCloudApiError, lambda e: e.status_code == 503),
    ],
)
def test_handle_http_error_status_matrix(status, body, headers, exc_type, extra_check):
    with pytest.raises(exc_type) as ei:
        handle_http_error(status, body, headers)
    assert extra_check(ei.value)


def test_handle_http_error_400_error_dict_message_without_code_appends_msg_only():
    """Inner branch ``if code else msg`` when ``errorCode`` is missing."""
    with pytest.raises(DealCloudValidationError) as ei:
        handle_http_error(400, {"errors": [{"message": "only msg"}]}, {})
    assert "only msg" in str(ei.value)


def test_handle_http_error_errors_array_skips_non_dict_entries():
    """Non-dict elements in ``errors`` are skipped (no crash)."""
    with pytest.raises(DealCloudValidationError):
        handle_http_error(400, {"errors": ["not-a-dict", {"message": "ok", "errorCode": ""}]}, {})
    # Still raises 400; second entry contributes
    with pytest.raises(DealCloudValidationError) as ei:
        handle_http_error(400, {"errors": [None, {"message": "x"}]}, {})
    assert "x" in str(ei.value)


def test_transform_http_error_prefers_full_response_body():
    """``full_response_body`` wins over ``response_body`` when both set."""
    err = MagicMock(spec=HttpError)
    err.status_code = 404
    err.full_response_body = {"message": "from full"}
    err.response_body = {"message": "from partial"}
    err.headers = {}
    err.request_id = "rid"

    with pytest.raises(DealCloudApiError) as ei:
        transform_http_error(err)
    assert "from full" in ei.value.message


def test_transform_http_error_falls_back_to_response_body():
    err = MagicMock(spec=HttpError)
    err.status_code = 400
    err.full_response_body = None
    err.response_body = {"message": "partial only"}
    err.headers = {}
    err.request_id = "rid"

    with pytest.raises(DealCloudValidationError) as ei:
        transform_http_error(err)
    assert "partial only" in str(ei.value)


def test_transform_http_error_real_http_error_instance():
    """Use a real ``HttpError`` (not MagicMock) for ``transform_http_error``."""
    err = HttpError(
        404,
        "nf",
        {"message": "missing"},
        {},
        request_id="r1",
    )
    with pytest.raises(DealCloudApiError) as ei:
        transform_http_error(err)
    assert ei.value.status_code == 404


def test_with_error_handling_returns_value_when_no_http_error():
    @with_error_handling
    def ok():
        return {"ok": True}

    assert ok() == {"ok": True}


def test_process_errors_raise_true_aggregates_multiple_rows():
    response = [
        {"EntryId": 1, "Errors": [{"field": "A"}]},
        {"EntryId": 2, "Errors": [{"field": "B"}]},
    ]
    with pytest.raises(DealCloudValidationError) as ei:
        process_errors(response, raise_on_row_errors=True)
    assert len(ei.value.errors) == 2
    assert len(ei.value.row_errors) == 2
    assert ei.value.row_errors[0]["EntryId"] == 1


def test_process_errors_raise_on_row_errors_attaches_row_errors():
    response = [{"EntryId": 99, "Errors": [{"field": "Formula", "code": 5009}]}]
    with pytest.raises(DealCloudValidationError) as ei:
        process_errors(response, raise_on_row_errors=True)
    assert ei.value.row_errors == response


def test_split_row_results_partitions_ok_and_error_rows():
    response = [
        {"EntryId": 1, "Name": "ok"},
        {"EntryId": 2, "Errors": [{"field": "X"}]},
    ]
    ok_rows, error_rows = split_row_results(response)
    assert len(ok_rows) == 1
    assert len(error_rows) == 1
    assert ok_rows[0]["EntryId"] == 1
    assert error_rows[0]["EntryId"] == 2


def test_split_cell_store_results_partitions_per_field_errors():
    """Cells store API returns per-field items with nested ``error``, not top-level Errors."""
    response = [
        {"entryId": -1, "fieldId": 1, "value": "dup", "error": {"code": 5009, "description": "not unique"}},
        {"entryId": -1, "fieldId": 2, "value": "1997"},
        {"entryId": -2, "fieldId": 1, "value": "ok"},
        {"entryId": -2, "fieldId": 2, "value": "1997"},
        {"entryId": -2, "fieldId": 3, "value": 500000},
    ]
    ok_cells, error_rows = split_cell_store_results(response, is_create=True)
    assert len(ok_cells) == 0
    assert len(error_rows) == 2
    by_entry = {row["EntryId"]: row for row in error_rows}
    assert by_entry[-1]["Errors"][0]["code"] == 5009
    assert by_entry[-2]["Errors"][0]["description"] == "entry not committed (batch all-or-none)"


def test_split_cell_store_results_committed_create_has_positive_row_id():
    response = [
        {"entryId": -1, "fieldId": 1, "rowId": 1001, "value": "ok"},
        {"entryId": -1, "fieldId": 2, "rowId": 1001, "value": 1997},
    ]
    ok_cells, error_rows = split_cell_store_results(response, is_create=True)
    assert len(ok_cells) == 2
    assert error_rows == []


def test_process_errors_raise_false_no_raise_when_empty_errors_list():
    response = [{"EntryId": 1, "Success": True}]
    assert process_errors(response, raise_on_row_errors=True) == []


def test_finalize_list_response_returns_all_rows_and_error_partition():
    response = [
        {"EntryId": 1, "Name": "ok"},
        {"EntryId": 2, "Errors": [{"field": "X", "code": 1}]},
    ]
    all_rows, row_errors = finalize_list_response(response)
    assert all_rows is response
    assert len(row_errors) == 1
    assert row_errors[0]["EntryId"] == 2
