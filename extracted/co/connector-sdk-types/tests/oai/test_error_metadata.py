"""
Tests for ConnectorErrorMetadata
"""

import pytest
from connector_sdk_types.errors import (
    CODE_CATEGORY_MAP,
    CODE_FAULT_MAP,
    REFRESHABLE_CODES,
    RETRYABLE_CODES,
    THROTTLE_AND_RETRY_CODES,
    ConnectorErrorCategory,
    ConnectorErrorCode,
    ConnectorErrorFault,
    ConnectorErrorMetadata,
    build_metadata,
)
from connector_sdk_types.generated.models.error_code import ErrorCode

# build_metadata — field derivation


@pytest.mark.parametrize("code", list(ConnectorErrorCode))
def test_build_metadata_fault_matches_map(code):
    meta = build_metadata(code)
    assert meta.fault == CODE_FAULT_MAP[code]


@pytest.mark.parametrize("code", list(ConnectorErrorCode))
def test_build_metadata_category_matches_map(code):
    meta = build_metadata(code)
    assert meta.category == CODE_CATEGORY_MAP[code]


@pytest.mark.parametrize("code", list(ConnectorErrorCode))
def test_build_metadata_retryable_consistent_with_frozensets(code):
    meta = build_metadata(code)
    expected = code in RETRYABLE_CODES or code in THROTTLE_AND_RETRY_CODES
    assert meta.retryable == expected, f"{code}: retryable mismatch"


@pytest.mark.parametrize("code", list(ConnectorErrorCode))
def test_build_metadata_throttled_consistent_with_frozenset(code):
    meta = build_metadata(code)
    assert meta.throttled == (code in THROTTLE_AND_RETRY_CODES), f"{code}: throttled mismatch"


@pytest.mark.parametrize("code", list(ConnectorErrorCode))
def test_build_metadata_refreshable_consistent_with_frozenset(code):
    meta = build_metadata(code)
    assert meta.refreshable == (code in REFRESHABLE_CODES), f"{code}: refreshable mismatch"


def test_build_metadata_hint_passed_through():
    meta = build_metadata(ConnectorErrorCode.RATE_LIMIT, hint="Retry after 30s")
    assert meta.hint == "Retry after 30s"


def test_build_metadata_hint_defaults_to_none():
    meta = build_metadata(ConnectorErrorCode.NOT_FOUND)
    assert meta.hint is None


# Behavior checks


def test_rate_limit_is_retryable_and_throttled():
    meta = build_metadata(ConnectorErrorCode.RATE_LIMIT)
    assert meta.retryable is True
    assert meta.throttled is True
    assert meta.refreshable is False


def test_bad_gateway_is_retryable_not_throttled():
    meta = build_metadata(ConnectorErrorCode.BAD_GATEWAY)
    assert meta.retryable is True
    assert meta.throttled is False


def test_authentication_expired_is_refreshable_not_retryable():
    meta = build_metadata(ConnectorErrorCode.AUTHENTICATION_EXPIRED)
    assert meta.refreshable is True
    assert meta.retryable is False
    assert meta.throttled is False


def test_permission_denied_not_retryable_not_refreshable():
    meta = build_metadata(ConnectorErrorCode.PERMISSION_DENIED)
    assert meta.retryable is False
    assert meta.refreshable is False


def test_not_found_has_caller_fault_and_client_category():
    meta = build_metadata(ConnectorErrorCode.NOT_FOUND)
    assert meta.fault == ConnectorErrorFault.CALLER
    assert meta.category == ConnectorErrorCategory.CLIENT


def test_connection_timeout_has_infrastructure_fault():
    meta = build_metadata(ConnectorErrorCode.CONNECTION_TIMEOUT)
    assert meta.fault == ConnectorErrorFault.INFRASTRUCTURE
    assert meta.retryable is True


# ConnectorErrorMetadata is a proper Pydantic model


def test_metadata_serialises_to_dict():
    meta = build_metadata(ConnectorErrorCode.RATE_LIMIT, hint="retry")
    d = meta.model_dump()
    assert d["fault"] == ConnectorErrorFault.UPSTREAM
    assert "retryable" in d
    assert "throttled" in d
    assert "refreshable" in d
    assert d["hint"] == "retry"


def test_metadata_is_connector_error_metadata_instance():
    meta = build_metadata(ConnectorErrorCode.INTERNAL_ERROR)
    assert isinstance(meta, ConnectorErrorMetadata)


# ConnectorError.get_error_metadata() integration


def test_connector_error_get_metadata_uses_default_code():
    from connector.oai.errors import ConnectorError

    e = ConnectorError(error_code=ConnectorErrorCode.RATE_LIMIT)
    meta = e.get_error_metadata()
    assert meta.throttled is True
    assert meta.retryable is True
    assert meta.fault == ConnectorErrorFault.UPSTREAM


def test_connector_error_get_metadata_passes_hint():
    from connector.oai.errors import RateLimitError

    e = RateLimitError(hint="retry after 60s")
    meta = e.get_error_metadata()
    assert meta.hint == "retry after 60s"


def test_connector_error_subclass_default_hint_flows_to_metadata():
    from connector.oai.errors import CredentialsRevokedError

    e = CredentialsRevokedError()
    meta = e.get_error_metadata()
    assert meta.hint is not None  # DEFAULT_HINT is set on CredentialsRevokedError
    assert meta.refreshable is True


def test_connector_error_get_metadata_resolves_deprecated_code():
    from connector.oai.errors import ConnectorError

    e = ConnectorError(error_code=ErrorCode.API_ERROR)  # deprecated → INVALID_RESPONSE
    meta = e.get_error_metadata()
    assert meta.fault == ConnectorErrorFault.CONNECTOR
    assert meta.category == ConnectorErrorCategory.INTERNAL
    assert meta.retryable is False


# handle_exception auto-populates error_metadata


def test_handle_exception_populates_metadata_for_connector_error():
    from connector.oai.errors import NotFoundError, handle_exception

    e = NotFoundError(message="user 42 not found")
    resp = handle_exception(e, [], lambda _: None, "test_app")
    assert resp.error.error_metadata is not None
    assert resp.error.error_metadata.fault == ConnectorErrorFault.CALLER
    assert resp.error.error_metadata.retryable is False


def test_handle_exception_populates_metadata_for_non_connector_error():
    import httpx
    from connector.oai.errors import HTTPHandler, handle_exception

    req = httpx.Request("GET", "https://example.com/")
    resp_http = httpx.Response(status_code=429, request=req)
    e = httpx.HTTPStatusError("429", request=req, response=resp_http)

    resp = handle_exception(
        e, [(httpx.HTTPStatusError, HTTPHandler, None)], lambda _: None, "test_app"
    )
    assert resp.error.error_metadata is not None
    assert resp.error.error_metadata.throttled is True
    assert resp.error.error_metadata.retryable is True


def test_handle_exception_metadata_hint_is_none_for_raw_exceptions():
    import httpx
    from connector.oai.errors import HTTPHandler, handle_exception

    req = httpx.Request("GET", "https://example.com/")
    resp_http = httpx.Response(status_code=503, request=req)
    e = httpx.HTTPStatusError("503", request=req, response=resp_http)

    resp = handle_exception(
        e, [(httpx.HTTPStatusError, HTTPHandler, None)], lambda _: None, "test_app"
    )
    assert resp.error.error_metadata is not None
    assert resp.error.error_metadata.hint is None


def test_error_metadata_appears_in_serialised_error_response():
    from connector.oai.errors import AuthenticationExpiredError, handle_exception

    e = AuthenticationExpiredError()
    resp = handle_exception(e, [], lambda _: None, "test_app")
    serialised = resp.error.to_dict()
    assert "error_metadata" in serialised
    meta = serialised["error_metadata"]
    assert meta["refreshable"] is True
    assert meta["retryable"] is False
