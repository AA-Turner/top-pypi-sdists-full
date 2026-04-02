"""Tests for connector_sdk_types.errors (codes + classification)."""

from connector_sdk_types.errors import (
    CODE_CATEGORY_MAP,
    CODE_FAULT_MAP,
    DEPRECATED_CODE_REDIRECTS,
    REFRESHABLE_CODES,
    RETRYABLE_CODES,
    ConnectorErrorCategory,
    ConnectorErrorCode,
    ConnectorErrorFault,
)
from connector_sdk_types.generated.models.error_code import ErrorCode


def test_all_sdk_error_codes_in_fault_map():
    """Every ConnectorErrorCode must have a fault mapping."""
    missing = [code for code in ConnectorErrorCode if code not in CODE_FAULT_MAP]
    assert not missing, f"Missing fault mapping for: {missing}"


def test_all_sdk_error_codes_in_category_map():
    """Every ConnectorErrorCode must have a category mapping."""
    missing = [code for code in ConnectorErrorCode if code not in CODE_CATEGORY_MAP]
    assert not missing, f"Missing category mapping for: {missing}"


def test_fault_and_category_maps_same_key_set():
    assert set(CODE_FAULT_MAP) == set(CODE_CATEGORY_MAP)


# DEPRECATED_CODE_REDIRECTS


def test_all_error_codes_covered_in_redirects():
    """Every deprecated ErrorCode value must have a redirect entry."""
    missing = [code for code in ErrorCode if code.value not in DEPRECATED_CODE_REDIRECTS]
    assert not missing, f"Missing redirect for deprecated codes: {missing}"


def test_redirects_map_to_sdk_error_codes():
    """All redirect values must be valid ConnectorErrorCode instances."""
    for key, value in DEPRECATED_CODE_REDIRECTS.items():
        assert isinstance(
            value, ConnectorErrorCode
        ), f"{key!r} → {value!r} is not an ConnectorErrorCode"


def test_api_error_redirects_to_invalid_response():
    assert DEPRECATED_CODE_REDIRECTS["api_error"] == ConnectorErrorCode.INVALID_RESPONSE


def test_client_call_error_redirects_to_invalid_response():
    assert DEPRECATED_CODE_REDIRECTS["client_call_error"] == ConnectorErrorCode.INVALID_RESPONSE


def test_unauthenticated_redirects_to_unauthorized():
    assert DEPRECATED_CODE_REDIRECTS["unauthenticated"] == ConnectorErrorCode.UNAUTHORIZED


def test_not_implemented_redirects_to_unsupported_operation():
    assert DEPRECATED_CODE_REDIRECTS["not_implemented"] == ConnectorErrorCode.UNSUPPORTED_OPERATION


def test_unexpected_error_redirects_to_internal_error():
    assert DEPRECATED_CODE_REDIRECTS["unexpected_error"] == ConnectorErrorCode.INTERNAL_ERROR


def test_codes_that_exist_in_both_pass_through():
    """Codes present in both ErrorCode and ConnectorErrorCode redirect to their ConnectorErrorCode equivalent."""
    passthrough = ["rate_limit", "bad_request", "not_found", "permission_denied"]
    for val in passthrough:
        assert DEPRECATED_CODE_REDIRECTS[val] == ConnectorErrorCode(val), val


# Behavioural frozensets


def test_refreshable_not_in_retryable():
    """Auth codes should not be in the plain-retry set."""
    overlap = REFRESHABLE_CODES.intersection(RETRYABLE_CODES)
    assert not overlap, f"Unexpected overlap: {overlap}"


def test_throttle_not_in_retryable():
    """Rate-limit code should use throttled retry, not plain retry."""
    assert ConnectorErrorCode.RATE_LIMIT not in RETRYABLE_CODES


# Consistency invariants


def test_retryable_codes_all_have_transient_or_internal_category():
    """Everything marked retryable should be TRANSIENT or INTERNAL — never CLIENT or AUTH."""
    for code in RETRYABLE_CODES:
        if not isinstance(code, ConnectorErrorCode):
            continue
        cat = CODE_CATEGORY_MAP.get(code)
        assert cat in (
            ConnectorErrorCategory.TRANSIENT,
            ConnectorErrorCategory.INTERNAL,
        ), f"{code} is retryable but has category {cat}"


def test_refreshable_codes_all_have_authentication_category():
    for code in REFRESHABLE_CODES:
        cat = CODE_CATEGORY_MAP.get(code)
        assert (
            cat == ConnectorErrorCategory.AUTHENTICATION
        ), f"{code} is refreshable but has category {cat}"


def test_client_fault_codes_have_client_category():
    """All CALLER-fault codes should be CLIENT category."""
    for code, fault in CODE_FAULT_MAP.items():
        if fault == ConnectorErrorFault.CALLER:
            assert (
                CODE_CATEGORY_MAP[code] == ConnectorErrorCategory.CLIENT
            ), f"{code} is CALLER fault but has category {CODE_CATEGORY_MAP[code]}"


# Cross-enum str equality (caller-side list checks)
#
# The monorepo holds its retry/refresh lists as ErrorCode members.
# After the SDK update, error.error_code is always ConnectorErrorCode (via _coerce_error_code).


def test_sdk_error_code_equals_error_code_same_string_value():
    """ConnectorErrorCode and ErrorCode with the same string value compare equal."""
    assert ConnectorErrorCode.UNAUTHORIZED == ErrorCode.UNAUTHORIZED
    assert ConnectorErrorCode.AUTHENTICATION_EXPIRED == ErrorCode.AUTHENTICATION_EXPIRED
    assert ConnectorErrorCode.CREDS_REVOKED == ErrorCode.CREDS_REVOKED
    assert ConnectorErrorCode.RATE_LIMIT == ErrorCode.RATE_LIMIT
    assert ConnectorErrorCode.BAD_GATEWAY == ErrorCode.BAD_GATEWAY
    assert ConnectorErrorCode.INTERNAL_ERROR == ErrorCode.INTERNAL_ERROR


def test_sdk_error_code_not_equal_to_different_error_code():
    """ConnectorErrorCode does NOT match an ErrorCode with a different string value."""
    assert ConnectorErrorCode.UNAUTHORIZED != ErrorCode.PERMISSION_DENIED
    assert ConnectorErrorCode.INTERNAL_ERROR != ErrorCode.RATE_LIMIT


def test_sdk_error_code_in_refresh_credentials_list():
    """Simulates the caller-side check: error.error_code in ERROR_CODES_THAT_SHOULD_REFRESH_CREDENTIALS."""
    error_codes_that_should_refresh_credentials = [
        ErrorCode.AUTHENTICATION_EXPIRED,
        ErrorCode.UNAUTHORIZED,
        ErrorCode.CREDS_REVOKED,
    ]
    assert ConnectorErrorCode.AUTHENTICATION_EXPIRED in error_codes_that_should_refresh_credentials
    assert ConnectorErrorCode.UNAUTHORIZED in error_codes_that_should_refresh_credentials
    assert ConnectorErrorCode.CREDS_REVOKED in error_codes_that_should_refresh_credentials
    # negative
    assert ConnectorErrorCode.RATE_LIMIT not in error_codes_that_should_refresh_credentials


def test_sdk_error_code_in_throttle_and_retry_list():
    """Simulates the caller-side check: error.error_code in ERROR_CODES_THAT_SHOULD_THROTTLE_AND_RETRY."""
    error_codes_that_should_throttle_and_retry = [ErrorCode.RATE_LIMIT]
    assert ConnectorErrorCode.RATE_LIMIT in error_codes_that_should_throttle_and_retry
    assert ConnectorErrorCode.BAD_GATEWAY not in error_codes_that_should_throttle_and_retry


def test_sdk_error_code_in_retry_without_throttling_list():
    """Simulates: error.error_code in ERROR_CODES_THAT_SHOULD_BE_RETRIED_WITHOUT_THROTTLING."""
    error_codes_that_should_be_retried_without_throttling = [
        ErrorCode.UNEXPECTED_ERROR,  # deprecated — redirects to INTERNAL_ERROR
        ErrorCode.BAD_GATEWAY,
        ErrorCode.REQUEST_TIMEOUT,
        ErrorCode.CONNECTION_TIMEOUT,
        ErrorCode.CONNECTION_REJECTED,
        ErrorCode.INTERNAL_ERROR,
    ]
    assert ConnectorErrorCode.BAD_GATEWAY in error_codes_that_should_be_retried_without_throttling
    assert (
        ConnectorErrorCode.REQUEST_TIMEOUT in error_codes_that_should_be_retried_without_throttling
    )
    assert (
        ConnectorErrorCode.CONNECTION_TIMEOUT
        in error_codes_that_should_be_retried_without_throttling
    )
    assert (
        ConnectorErrorCode.CONNECTION_REJECTED
        in error_codes_that_should_be_retried_without_throttling
    )
    assert (
        ConnectorErrorCode.INTERNAL_ERROR in error_codes_that_should_be_retried_without_throttling
    )
    # negative
    assert (
        ConnectorErrorCode.PERMISSION_DENIED
        not in error_codes_that_should_be_retried_without_throttling
    )


def test_unexpected_error_redirect_preserves_retry_behaviour():
    """
    UNEXPECTED_ERROR (deprecated) redirects to INTERNAL_ERROR via _coerce_error_code.
    The caller's list contains both ErrorCode.UNEXPECTED_ERROR and ErrorCode.INTERNAL_ERROR,
    so INTERNAL_ERROR still matches and the retry is triggered — behaviour is preserved.
    """
    error_codes_that_should_be_retried_without_throttling = [
        ErrorCode.UNEXPECTED_ERROR,
        ErrorCode.BAD_GATEWAY,
        ErrorCode.REQUEST_TIMEOUT,
        ErrorCode.CONNECTION_TIMEOUT,
        ErrorCode.CONNECTION_REJECTED,
        ErrorCode.INTERNAL_ERROR,
    ]
    redirected = DEPRECATED_CODE_REDIRECTS["unexpected_error"]
    assert redirected == ConnectorErrorCode.INTERNAL_ERROR
    # The redirected code must still hit the retry list
    assert redirected in error_codes_that_should_be_retried_without_throttling


def test_error_model_coercion_produces_sdk_error_code_that_matches_error_code_list():
    """
    End-to-end: ErrorResponse.model_validate() with a deprecated string value produces an
    error_code that is still found in the caller's ErrorCode-based lists.
    """
    from connector_sdk_types.generated import ErrorResponse

    error_codes_that_should_refresh_credentials = [
        ErrorCode.AUTHENTICATION_EXPIRED,
        ErrorCode.UNAUTHORIZED,
        ErrorCode.CREDS_REVOKED,
    ]

    raw = {
        "is_error": True,
        "error": {
            "message": "token expired",
            "error_code": "authentication_expired",
            "app_id": "myapp",
        },
    }
    response = ErrorResponse.model_validate(raw)
    assert isinstance(response.error.error_code, ConnectorErrorCode)
    assert response.error.error_code in error_codes_that_should_refresh_credentials
