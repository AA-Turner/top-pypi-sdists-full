"""Tests for DealCloud utilities."""

import pytest
import pandas as pd
import numpy as np

from dealcloud_sdk import ErrorHandling
from dealcloud_sdk.utils.data_utils import (
    flatten_nested_list,
    format_data,
    divide_pages,
    calculate_pagination,
    query_by_entry_id,
    rows_query_payload_builder,
    generate_page_offsets,
)
from dealcloud_sdk.utils.resolve_references import resolve_object
from dealcloud_sdk.utils.process_response_errors import (
    DealCloudApiError,
    DealCloudValidationError,
    DealCloudRateLimitError,
    DealCloudAuthError,
    process_errors,
    handle_http_error,
    transform_http_error,
)


class TestErrorHandling:
    """Tests for ErrorHandling enum (string values must match intapp-rest-client)."""

    def test_error_handling_values(self):
        """ErrorHandling string values are the API contract for error_handling=... kwargs."""
        assert ErrorHandling.FAIL_FAST.value == "fail_fast"
        assert ErrorHandling.COLLECT.value == "collect"
        assert ErrorHandling.LOG_ONLY.value == "log_only"


class TestDataUtils:
    """Tests for data utility functions."""
    
    def test_flatten_nested_list(self):
        """Test flatten_nested_list."""
        nested = [[1, 2], [3, 4], [5]]
        result = flatten_nested_list(nested)
        assert result == [1, 2, 3, 4, 5]
    
    def test_flatten_nested_list_empty(self):
        """Test flatten_nested_list with empty list."""
        result = flatten_nested_list([])
        assert result == []
    
    def test_format_data_from_list(self):
        """Test format_data with list input."""
        data = [
            {"Name": "Company A", "Status": "Active"},
            {"Name": "Company B", "Status": "Inactive"},
        ]
        result_data, columns = format_data(data)
        assert result_data == data
        assert columns == {"Name", "Status"}
    
    def test_format_data_from_dataframe(self):
        """Test format_data with DataFrame input."""
        df = pd.DataFrame({
            "Name": ["Company A", "Company B"],
            "Status": ["Active", None],
        })
        result_data, columns = format_data(df)
        assert len(result_data) == 2
        assert result_data[1]["Status"] is None
        assert columns == {"Name", "Status"}
    
    def test_divide_pages(self):
        """Test divide_pages generator."""
        items = list(range(10))
        pages = list(divide_pages(items, 3))
        assert len(pages) == 4
        assert pages[0] == [0, 1, 2]
        assert pages[1] == [3, 4, 5]
        assert pages[2] == [6, 7, 8]
        assert pages[3] == [9]
    
    def test_calculate_pagination_no_pagination_needed(self):
        """Test calculate_pagination when data fits in single page."""
        rows = [{"A": 1, "B": 2}] * 10
        columns = {"A", "B"}
        result = calculate_pagination(rows, columns, cell_pagination_limit=100)
        assert len(result) == 1
        assert result[0] == rows
    
    def test_calculate_pagination_needed(self):
        """Test calculate_pagination when pagination is needed."""
        rows = [{"A": 1, "B": 2}] * 100
        columns = {"A", "B"}
        result = calculate_pagination(rows, columns, cell_pagination_limit=50)
        assert len(result) > 1
    
    def test_query_by_entry_id(self):
        """Test query_by_entry_id builds DealCloud entryId filter."""
        assert query_by_entry_id(4224866) == "{entryid: 4224866}"
        assert query_by_entry_id(1) == "{entryid: 1}"

    def test_rows_query_payload_builder_basic(self):
        """Test rows_query_payload_builder with basic query."""
        payload = rows_query_payload_builder("Name = 'Test'")
        assert payload == {"query": "Name = 'Test'", "wrapIntoArrays": True}
    
    def test_rows_query_payload_builder_with_options(self):
        """Test rows_query_payload_builder with all options."""
        payload = rows_query_payload_builder(
            query="Name = 'Test'",
            fields=["Name", "Status"],
            limit=100,
            skip=50,
        )
        assert payload["query"] == "Name = 'Test'"
        assert payload["fields"] == ["Name", "Status"]
        assert payload["limit"] == 100
        assert payload["skip"] == 50
    
    def test_generate_page_offsets(self):
        """Test generate_page_offsets."""
        offsets = generate_page_offsets(page_size=100, max_parallel_pages=5)
        assert offsets == [0, 100, 200, 300, 400]


class TestResolveReferences:
    """Tests for reference resolution."""
    
    def test_resolve_object_by_id(self):
        """Test resolve_object with id."""
        data = {"id": 123, "name": "Test Company"}
        result = resolve_object(data, "id")
        assert result == 123
    
    def test_resolve_object_by_name(self):
        """Test resolve_object with name."""
        data = {"id": 123, "name": "Test Company"}
        result = resolve_object(data, "name")
        assert result == "Test Company"
    
    def test_resolve_object_missing_key(self):
        """Test resolve_object with missing key returns dict."""
        data = {"id": 123, "name": "Test Company"}
        result = resolve_object(data, "missing")
        assert result == data
    
    def test_resolve_object_non_dict(self):
        """Test resolve_object with non-dict input."""
        result = resolve_object("not a dict", "id")
        assert result == "not a dict"


class TestProcessResponseErrors:
    """Tests for error processing."""
    
    def test_process_errors_with_errors(self):
        """Test process_errors with error responses."""
        response = [
            {"EntryId": 1, "Success": True},
            {"EntryId": -1, "Errors": [{"field": "Name", "code": 5006, "description": "Required"}]},
        ]
        errors = process_errors(response, raise_on_row_errors=False)
        assert len(errors) == 1
    
    def test_process_errors_raises_on_raise_on_row_errors(self):
        """Test process_errors raises when raise_on_row_errors=True."""
        response = [
            {"EntryId": -1, "Errors": [{"field": "Name", "code": 5006, "description": "Required"}]},
        ]
        with pytest.raises(DealCloudValidationError) as exc_info:
            process_errors(response, raise_on_row_errors=True)
        assert len(exc_info.value.errors) == 1
    
    def test_process_errors_no_errors(self):
        """Test process_errors with no errors."""
        response = [
            {"EntryId": 1, "Success": True},
            {"EntryId": 2, "Success": True},
        ]
        errors = process_errors(response, raise_on_row_errors=False)
        assert len(errors) == 0
    
    def test_handle_http_error_400(self):
        """Test handle_http_error for 400."""
        with pytest.raises(DealCloudValidationError) as exc_info:
            handle_http_error(400, {"errors": ["Invalid field"]}, {})
        assert exc_info.value.status_code == 400
    
    def test_handle_http_error_401(self):
        """Test handle_http_error for 401."""
        with pytest.raises(DealCloudAuthError) as exc_info:
            handle_http_error(401, {}, {})
        assert exc_info.value.status_code == 401
    
    def test_handle_http_error_403(self):
        """Test handle_http_error for 403."""
        with pytest.raises(DealCloudAuthError) as exc_info:
            handle_http_error(403, {}, {})
        assert exc_info.value.status_code == 403
    
    def test_handle_http_error_404(self):
        """Test handle_http_error for 404."""
        with pytest.raises(DealCloudApiError) as exc_info:
            handle_http_error(404, {}, {})
        assert exc_info.value.status_code == 404
    
    def test_handle_http_error_429_with_retry_after(self):
        """Test handle_http_error for 429 with Retry-After header."""
        with pytest.raises(DealCloudRateLimitError) as exc_info:
            handle_http_error(429, {}, {"Retry-After": "60"})
        assert exc_info.value.retry_after == 60
    
    def test_handle_http_error_500(self):
        """Test handle_http_error for 500."""
        with pytest.raises(DealCloudApiError) as exc_info:
            handle_http_error(500, {"error": "Server error"}, {})
        assert exc_info.value.status_code == 500

    def test_handle_http_error_400_with_errors_array_and_error_code(self):
        """Test handle_http_error 400 with errors array containing message and errorCode."""
        with pytest.raises(DealCloudValidationError) as exc_info:
            handle_http_error(
                400,
                {"errors": [{"message": "Invalid field", "errorCode": "VALIDATION_001"}]},
                {},
            )
        assert exc_info.value.status_code == 400
        assert "VALIDATION_001" in str(exc_info.value)

    def test_handle_http_error_with_non_dict_response_body(self):
        """Test handle_http_error when response_body is not a dict (e.g. string)."""
        with pytest.raises(DealCloudApiError) as exc_info:
            handle_http_error(502, "Gateway error string", {})
        assert exc_info.value.status_code == 502
        assert "Gateway error string" in str(exc_info.value)

    def test_handle_http_error_400_errors_dict_with_empty_message_skipped(self):
        """Dict errors with empty message do not append to error_details (inner if msg)."""
        with pytest.raises(DealCloudValidationError) as exc_info:
            handle_http_error(
                400,
                {"errors": [{"message": "", "errorCode": "X"}, {"message": "Bad", "errorCode": ""}]},
                {},
            )
        assert "Bad" in str(exc_info.value)

    def test_handle_http_error_non_dict_falsy_body_skips_elif(self):
        """Non-dict falsy body skips elif response_body branch before status handling."""
        with pytest.raises(DealCloudApiError) as exc_info:
            handle_http_error(503, None, {})
        assert exc_info.value.status_code == 503

    def test_transform_http_error_raises_dealcloud_exception(self):
        """Test transform_http_error converts HttpError to DealCloud exception."""
        from unittest.mock import MagicMock
        mock_http_error = MagicMock()
        mock_http_error.status_code = 404
        mock_http_error.full_response_body = None
        mock_http_error.response_body = {"message": "Not found"}
        mock_http_error.headers = {}
        mock_http_error.request_id = "req-123"
        with pytest.raises(DealCloudApiError) as exc_info:
            transform_http_error(mock_http_error)
        assert exc_info.value.status_code == 404

    def test_transform_http_error_429_raises_dealcloud_rate_limit_error_with_retry_after(self):
        """Test transform_http_error converts HttpError 429 to DealCloudRateLimitError with Retry-After."""
        from unittest.mock import MagicMock
        mock_http_error = MagicMock()
        mock_http_error.status_code = 429
        mock_http_error.full_response_body = None
        mock_http_error.response_body = {"message": "Too many requests"}
        mock_http_error.headers = {"Retry-After": "60"}
        mock_http_error.request_id = "req-456"
        with pytest.raises(DealCloudRateLimitError) as exc_info:
            transform_http_error(mock_http_error)
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 60

    def test_transform_http_error_429_without_retry_after(self):
        """Test transform_http_error 429 without Retry-After header yields retry_after=None."""
        from unittest.mock import MagicMock
        mock_http_error = MagicMock()
        mock_http_error.status_code = 429
        mock_http_error.full_response_body = None
        mock_http_error.response_body = {}
        mock_http_error.headers = {}
        mock_http_error.request_id = "req-789"
        with pytest.raises(DealCloudRateLimitError) as exc_info:
            transform_http_error(mock_http_error)
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after is None

    def test_with_error_handling_decorator_transforms_http_error(self):
        """Test with_error_handling decorator calls transform on HttpError."""
        from dealcloud_sdk.utils.process_response_errors import with_error_handling
        from intapp_rest_client.exceptions import HttpError

        @with_error_handling
        def failing_func():
            raise HttpError(
                403,
                "Forbidden",
                response_body={},
                headers={},
                request_id="req-123",
            )

        with pytest.raises(DealCloudAuthError):
            failing_func()


class TestExceptions:
    """Tests for exception classes."""
    
    def test_dealcloud_api_error(self):
        """Test DealCloudApiError."""
        error = DealCloudApiError("Test error", status_code=500, errors=["Error 1"])
        assert error.message == "Test error"
        assert error.status_code == 500
        assert error.errors == ["Error 1"]
    
    def test_dealcloud_validation_error(self):
        """Test DealCloudValidationError."""
        error = DealCloudValidationError("Validation failed", errors=["Field required"])
        assert "Validation failed" in str(error)
        assert error.errors == ["Field required"]
    
    def test_dealcloud_rate_limit_error(self):
        """Test DealCloudRateLimitError."""
        error = DealCloudRateLimitError("Rate limited", retry_after=60)
        assert error.status_code == 429
        assert error.retry_after == 60
    
    def test_dealcloud_auth_error(self):
        """Test DealCloudAuthError."""
        error = DealCloudAuthError("Unauthorized", status_code=401)
        assert error.status_code == 401


