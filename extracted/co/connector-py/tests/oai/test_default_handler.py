"""Unit tests for the DefaultHandler class in connector.oai.errors."""

from unittest.mock import MagicMock, patch

import httpx
from connector.oai.errors import (
    ConnectorError,
    DefaultHandler,
    HTTPHandler,
    NetworkError,
    handle_exception,
)
from connector_sdk_types.errors import ConnectorErrorCode
from connector_sdk_types.generated import Error, ErrorCode, ErrorResponse


def _make_response() -> ErrorResponse:
    return ErrorResponse(
        is_error=True,
        error=Error(message="initial", error_code=ConnectorErrorCode.INTERNAL_ERROR, app_id="test"),
    )


# _extract_status_code


def test_extract_status_code_from_response_attr():
    e = MagicMock(spec=[])
    e.response = MagicMock(spec=[])
    e.response.status_code = 404
    assert DefaultHandler._extract_status_code(e) == 404


def test_extract_status_code_from_code_attr():
    e = MagicMock(spec=[])
    e.code = 500
    assert DefaultHandler._extract_status_code(e) == 500


def test_extract_status_code_code_overrides_response():
    """e.code takes precedence over e.response.status_code."""
    e = MagicMock(spec=[])
    e.response = MagicMock(spec=[])
    e.response.status_code = 404
    e.code = 503
    assert DefaultHandler._extract_status_code(e) == 503


def test_extract_status_code_non_int_returns_none():
    e = MagicMock(spec=[])
    e.code = "not-an-int"
    assert DefaultHandler._extract_status_code(e) is None


def test_extract_status_code_plain_exception():
    assert DefaultHandler._extract_status_code(Exception("plain")) is None


# _extract_error_message


def test_extract_error_message_json_with_url():
    mock_resp = MagicMock(spec=[])
    mock_resp.json = MagicMock(return_value={"error": "not found"})
    mock_resp.url = "https://api.example.com/users?q=1"
    e = MagicMock(spec=[])
    e.response = mock_resp
    result = DefaultHandler._extract_error_message(e, 404)
    assert result and "[404]" in result
    assert "https://api.example.com/users" in result
    assert "?" not in result  # query params stripped


def test_extract_error_message_json_empty_dict_skipped():
    """Empty dict from .json() falls through to exception path."""
    mock_resp = MagicMock(spec=[])
    mock_resp.json = MagicMock(return_value={})
    mock_resp.text = "raw text fallback"
    mock_resp.url = "https://api.example.com/foo"
    mock_resp.status_code = 400
    e = MagicMock(spec=[])
    e.response = mock_resp
    result = DefaultHandler._extract_error_message(e, 400)
    # Empty dict is falsy → falls through to text fallback
    assert result is None or "raw text fallback" in result


def test_extract_error_message_json_without_url():
    mock_resp = MagicMock(spec=["json"])
    mock_resp.json = MagicMock(return_value={"msg": "err"})
    e = MagicMock(spec=[])
    e.response = mock_resp
    result = DefaultHandler._extract_error_message(e, 422)
    assert result and "[422]" in result
    assert "err" in result


def test_extract_error_message_fallback_to_text_with_url():
    mock_resp = MagicMock(spec=[])
    mock_resp.json = MagicMock(side_effect=Exception("no json"))
    mock_resp.text = "plain response body"
    mock_resp.headers = {"content-type": "text/plain"}
    mock_resp.url = "https://api.example.com/foo"
    mock_resp.status_code = 503
    e = MagicMock(spec=[])
    e.response = mock_resp
    result = DefaultHandler._extract_error_message(e, 503)
    assert result and "plain response body" in result
    assert "[503]" in result


def test_extract_error_message_fallback_empty_text_returns_none():
    mock_resp = MagicMock(spec=[])
    mock_resp.json = MagicMock(side_effect=Exception("no json"))
    mock_resp.text = ""
    mock_resp.headers = {"content-type": "text/plain"}
    mock_resp.url = "https://api.example.com/foo"
    mock_resp.status_code = 503
    e = MagicMock(spec=[])
    e.response = mock_resp
    result = DefaultHandler._extract_error_message(e, 503)
    assert result is None


def test_extract_error_message_html_response_body_is_omitted():
    mock_resp = MagicMock(spec=[])
    mock_resp.json = MagicMock(side_effect=Exception("no json"))
    mock_resp.text = "<!DOCTYPE html><html><body>Gateway Timeout</body></html>"
    mock_resp.headers = {"content-type": "text/html; charset=utf-8"}
    mock_resp.url = "https://api.example.com/foo"
    mock_resp.status_code = 504
    e = MagicMock(spec=[])
    e.response = mock_resp
    result = DefaultHandler._extract_error_message(e, 504)
    assert result is not None
    assert "Upstream HTML error response." in result
    assert "<!DOCTYPE html>" not in result


def test_extract_error_message_html_like_body_without_content_type_is_omitted():
    mock_resp = MagicMock(spec=[])
    mock_resp.json = MagicMock(side_effect=Exception("no json"))
    mock_resp.text = "   <html><body>Gateway Timeout</body></html>"
    mock_resp.headers = {}
    mock_resp.url = "https://api.example.com/foo"
    mock_resp.status_code = 504
    e = MagicMock(spec=[])
    e.response = mock_resp
    result = DefaultHandler._extract_error_message(e, 504)
    assert result is not None
    assert "Upstream HTML error response." in result
    assert "<html>" not in result.lower()


def test_extract_error_message_long_text_response_is_truncated():
    mock_resp = MagicMock(spec=[])
    mock_resp.json = MagicMock(side_effect=Exception("no json"))
    mock_resp.text = "x" * 2000
    mock_resp.headers = {"content-type": "text/plain"}
    mock_resp.url = "https://api.example.com/foo"
    mock_resp.status_code = 500
    e = MagicMock(spec=[])
    e.response = mock_resp
    result = DefaultHandler._extract_error_message(e, 500)
    assert result is not None
    assert "...(truncated)" in result
    assert len(result) < 1000  # includes status/url prefix


def test_extract_error_message_fallback_to_str_e():
    """No response attribute → fall back to str(e)."""
    e = Exception("plain error message")
    result = DefaultHandler._extract_error_message(e, None)
    assert result == "plain error message"


def test_extract_error_message_fallback_uses_message_attr():
    """Exception with .message attr uses it over str(e)."""

    class CustomError(Exception):
        message = "custom message attr"

    e = CustomError()
    result = DefaultHandler._extract_error_message(e, None)
    assert result == "custom message attr"


# _populate_base_error_info


def test_populate_base_error_info_with_message():
    resp = _make_response()
    e = Exception("original")
    DefaultHandler._populate_base_error_info(resp, e, lambda _: None, 404, "override message")
    assert resp.error.message == "override message"
    assert resp.error.status_code == 404
    assert resp.error.raised_in and "tests" in resp.error.raised_in
    assert resp.error.raised_by == "Exception"


def test_populate_base_error_info_no_message_uses_str_e():
    resp = _make_response()
    e = Exception("fallback from str")
    DefaultHandler._populate_base_error_info(resp, e, lambda _: None, None, None)
    assert resp.error.message == "fallback from str"


def test_populate_base_error_info_no_message_uses_message_attr():
    resp = _make_response()

    class CustomErr(Exception):
        message = "from message attr"

    e = CustomErr()
    DefaultHandler._populate_base_error_info(resp, e, lambda _: None, None, None)
    assert resp.error.message == "from message attr"


def test_populate_base_error_info_empty_str_exception_gets_fallback():
    resp = _make_response()

    class EmptyMessageError(Exception):
        def __str__(self) -> str:
            return ""

    e = EmptyMessageError()
    DefaultHandler._populate_base_error_info(resp, e, lambda _: None, None, None)
    assert resp.error.message == "EmptyMessageError: (no message)"


def test_handle_exception_logger_empty_exception_message_not_blank():
    class EmptyMessageError(Exception):
        def __str__(self) -> str:
            return ""

    e = EmptyMessageError()
    with patch("connector.oai.errors.base.error_logger.error") as mock_error:
        handle_exception(e, [], lambda _: None, "my_app")
    line = _render_error_log_call(mock_error)
    assert ": EmptyMessageError: (no message) | " in line


# _handle_connector_error


def test_handle_connector_error_sdk_code_passthrough():
    resp = _make_response()
    e = ConnectorError(message="rate limited", error_code=ConnectorErrorCode.RATE_LIMIT)
    DefaultHandler._handle_connector_error(resp, e)
    assert resp.error.error_code == ConnectorErrorCode.RATE_LIMIT


def test_handle_connector_error_deprecated_api_error():
    resp = _make_response()
    e = ConnectorError(message="api error", error_code=ErrorCode.API_ERROR)
    DefaultHandler._handle_connector_error(resp, e)
    assert resp.error.error_code == ConnectorErrorCode.INVALID_RESPONSE


def test_handle_connector_error_deprecated_client_call_error():
    resp = _make_response()
    e = ConnectorError(message="client call", error_code=ErrorCode.CLIENT_CALL_ERROR)
    DefaultHandler._handle_connector_error(resp, e)
    assert resp.error.error_code == ConnectorErrorCode.INVALID_RESPONSE


def test_handle_connector_error_deprecated_unauthenticated():
    resp = _make_response()
    e = ConnectorError(message="unauth", error_code=ErrorCode.UNAUTHENTICATED)
    DefaultHandler._handle_connector_error(resp, e)
    assert resp.error.error_code == ConnectorErrorCode.UNAUTHORIZED


def test_handle_connector_error_app_error_code_set():
    resp = _make_response()
    e = ConnectorError(
        message="not found", error_code=ConnectorErrorCode.NOT_FOUND, app_error_code="myapp.404"
    )
    DefaultHandler._handle_connector_error(resp, e)
    assert resp.error.app_error_code == "myapp.404"


def test_handle_connector_error_no_app_error_code():
    resp = _make_response()
    e = ConnectorError(message="err", error_code=ConnectorErrorCode.INTERNAL_ERROR)
    DefaultHandler._handle_connector_error(resp, e)
    assert resp.error.app_error_code is None


# handle_exception


def test_handle_exception_connector_error_skips_handler_loop():
    """ConnectorError bypasses exception_handlers list."""
    from connector.oai.errors import HTTPHandler

    handler_called = []

    class SpyHandler(HTTPHandler):
        @staticmethod
        def handle(e, original_func, response, error_code=None):
            handler_called.append(True)
            return HTTPHandler.handle(e, original_func, response, error_code)

    e = ConnectorError(message="permission denied", error_code=ConnectorErrorCode.PERMISSION_DENIED)
    resp = handle_exception(e, [(ConnectorError, SpyHandler, None)], lambda _: None, "test_app")
    assert not handler_called, "Handler loop should be skipped for ConnectorError"
    assert resp.error.error_code == ConnectorErrorCode.PERMISSION_DENIED


def test_handle_exception_uses_matching_handler():
    """Non-ConnectorError uses the matching handler from exception_classes."""
    # Build a minimal HTTPStatusError with a mocked response
    mock_request = httpx.Request("GET", "https://example.com/")
    mock_response = httpx.Response(status_code=503, request=mock_request)
    e = httpx.HTTPStatusError("503", request=mock_request, response=mock_response)

    # The DefaultHandler sets status_code from e.response; HTTPHandler maps it
    resp = handle_exception(
        e, [(httpx.HTTPStatusError, HTTPHandler, None)], lambda _: None, "test_app"
    )
    assert resp.error.error_code == ConnectorErrorCode.SERVICE_ERROR


def test_handle_exception_maps_connect_timeout_to_connection_timeout():
    req = httpx.Request("GET", "https://example.com/")
    e = httpx.ConnectTimeout("connect timeout", request=req)
    resp = handle_exception(
        e, [(httpx.HTTPStatusError, HTTPHandler, None)], lambda _: None, "test_app"
    )
    assert resp.error.error_code == ConnectorErrorCode.CONNECTION_TIMEOUT


def test_handle_exception_maps_read_timeout_to_request_timeout():
    req = httpx.Request("GET", "https://example.com/")
    e = httpx.ReadTimeout("read timeout", request=req)
    resp = handle_exception(
        e, [(httpx.HTTPStatusError, HTTPHandler, None)], lambda _: None, "test_app"
    )
    assert resp.error.error_code == ConnectorErrorCode.REQUEST_TIMEOUT


def test_handle_exception_maps_read_error_to_connection_closed():
    req = httpx.Request("GET", "https://example.com/")
    e = httpx.ReadError("read error", request=req)
    resp = handle_exception(
        e, [(httpx.HTTPStatusError, HTTPHandler, None)], lambda _: None, "test_app"
    )
    assert resp.error.error_code == ConnectorErrorCode.CONNECTION_CLOSED


def test_handle_exception_maps_remote_protocol_error_to_connection_closed():
    req = httpx.Request("GET", "https://example.com/")
    e = httpx.RemoteProtocolError("peer closed connection", request=req)
    resp = handle_exception(
        e, [(httpx.HTTPStatusError, HTTPHandler, None)], lambda _: None, "test_app"
    )
    assert resp.error.error_code == ConnectorErrorCode.CONNECTION_CLOSED


def _render_error_log_call(mock_error: MagicMock) -> str:
    """Rebuild the formatted line from ``error_logger.error(fmt, *args, exc_info=True)``."""
    args, kwargs = mock_error.call_args
    assert kwargs.get("exc_info") is True
    fmt, *values = args
    return fmt % tuple(values)


def test_handle_exception_logger_includes_pipe_metadata_for_connector_error():
    """handle_exception logs one line with app/code, message, and pipe-separated metadata."""
    e = NetworkError(message="boom")

    with patch("connector.oai.errors.base.error_logger.error") as mock_error:
        handle_exception(e, [], lambda _: None, "test_app")

    mock_error.assert_called_once()
    line = _render_error_log_call(mock_error)

    assert line.startswith("test_app/")
    assert "connection_timeout" in line
    assert ": boom | " in line
    assert "error_fault=infrastructure" in line
    assert "error_category=transient" in line
    assert "error_retryable=True" in line
    assert "error_throttled=False" in line
    assert "error_refreshable=False" in line
    assert "error_hint=Please retry the request." in line


def test_handle_exception_logger_http_error_includes_pipe_metadata_and_exc_info():
    """Non-ConnectorError path still logs resolved error_code metadata on the same line."""
    mock_request = httpx.Request("GET", "https://example.com/")
    mock_response = httpx.Response(status_code=503, request=mock_request)
    e = httpx.HTTPStatusError("503", request=mock_request, response=mock_response)

    with patch("connector.oai.errors.base.error_logger.error") as mock_error:
        handle_exception(
            e, [(httpx.HTTPStatusError, HTTPHandler, None)], lambda _: None, "salesforce"
        )

    mock_error.assert_called_once()
    line = _render_error_log_call(mock_error)

    assert "salesforce/" in line
    assert "service_error" in line
    assert " | error_fault=upstream" in line
    assert "error_category=transient" in line
    assert line.endswith("error_hint=")


def test_handle_exception_logger_plain_exception_uses_internal_error_metadata():
    """Plain exceptions resolve to INTERNAL_ERROR; metadata is still appended after the pipe."""
    e = ValueError("plain failure")

    with patch("connector.oai.errors.base.error_logger.error") as mock_error:
        handle_exception(e, [], lambda _: None, "my_app")

    line = _render_error_log_call(mock_error)
    assert "my_app/" in line
    assert "internal_error" in line
    assert "plain failure" in line
    assert "error_fault=connector" in line
    assert "error_category=internal" in line
    assert line.endswith("error_hint=")
