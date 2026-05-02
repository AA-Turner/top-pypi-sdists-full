"""
Tests for the typed ConnectorError hierarchy introduced in Step 2 of the
exception class system overhaul.

Coverage:
- ConnectorError class-var defaults and optional-arg behaviour
- Each typed subclass carries the correct DEFAULT_CODE
- Subclasses are proper ConnectorError instances (isinstance checks)
- Raising without any arguments uses class defaults
- Raising with explicit overrides uses provided values
- DefaultHandler handles typed subclasses the same as plain ConnectorError
"""

import pytest
from connector.oai.errors import (
    AuthenticationError,
    AuthenticationExpiredError,
    AuthorizationError,
    ClientError,
    ConflictError,
    ConnectionClosedError,
    ConnectionRejectedError,
    ConnectorError,
    CredentialsRevokedError,
    DefaultHandler,
    InternalError,
    InvalidPageTokenError,
    InvalidResponseError,
    InvalidValueError,
    MissingParameterError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    RequestTimeoutError,
    TransientError,
    UnknownValueError,
    UnsupportedOperationError,
    UpstreamError,
)
from connector_sdk_types.errors import ConnectorErrorCode
from connector_sdk_types.generated import Error, ErrorResponse

# Helpers


def _make_response() -> ErrorResponse:
    return ErrorResponse(
        is_error=True,
        error=Error(message="initial", error_code=ConnectorErrorCode.INTERNAL_ERROR, app_id="test"),
    )


# ConnectorError


def test_connector_error_defaults_when_no_args():
    e = ConnectorError()
    assert e.error_code == ConnectorErrorCode.INTERNAL_ERROR
    assert e.message == ConnectorError.DEFAULT_MESSAGE
    assert e.app_error_code is None


def test_connector_error_explicit_args_override_defaults():
    e = ConnectorError(message="custom msg", error_code=ConnectorErrorCode.NOT_FOUND)
    assert e.error_code == ConnectorErrorCode.NOT_FOUND
    assert e.message == "custom msg"


def test_connector_error_str_returns_message():
    e = ConnectorError(message="hello world")
    assert str(e) == "hello world"


def test_connector_error_str_returns_default_message_when_no_message():
    e = ConnectorError()
    assert str(e) == ConnectorError.DEFAULT_MESSAGE


# Default codes


@pytest.mark.parametrize(
    "cls, expected_code",
    [
        (AuthenticationError, ConnectorErrorCode.UNAUTHORIZED),
        (AuthenticationExpiredError, ConnectorErrorCode.AUTHENTICATION_EXPIRED),
        (CredentialsRevokedError, ConnectorErrorCode.CREDS_REVOKED),
        (AuthorizationError, ConnectorErrorCode.PERMISSION_DENIED),
        (TransientError, ConnectorErrorCode.SERVICE_ERROR),
        (RateLimitError, ConnectorErrorCode.RATE_LIMIT),
        (UpstreamError, ConnectorErrorCode.BAD_GATEWAY),
        (NetworkError, ConnectorErrorCode.CONNECTION_TIMEOUT),
        (ConnectionRejectedError, ConnectorErrorCode.CONNECTION_REJECTED),
        (ConnectionClosedError, ConnectorErrorCode.CONNECTION_CLOSED),
        (RequestTimeoutError, ConnectorErrorCode.REQUEST_TIMEOUT),
        (ClientError, ConnectorErrorCode.BAD_REQUEST),
        (NotFoundError, ConnectorErrorCode.NOT_FOUND),
        (InvalidValueError, ConnectorErrorCode.INVALID_VALUE),
        (UnknownValueError, ConnectorErrorCode.UNKNOWN_VALUE),
        (InvalidPageTokenError, ConnectorErrorCode.INVALID_PAGE_TOKEN),
        (MissingParameterError, ConnectorErrorCode.INTEGRATION_MISSING_PARAMETER),
        (ConflictError, ConnectorErrorCode.CONFLICT),
        (InternalError, ConnectorErrorCode.INTERNAL_ERROR),
        (InvalidResponseError, ConnectorErrorCode.INVALID_RESPONSE),
        (UnsupportedOperationError, ConnectorErrorCode.UNSUPPORTED_OPERATION),
    ],
)
def test_typed_error_default_code(cls, expected_code):
    """Every typed exception carries the correct DEFAULT_CODE when raised without args."""
    e = cls()
    assert e.error_code == expected_code, f"{cls.__name__} has wrong default code"


# Custom message/code override


def test_typed_error_accepts_custom_message():
    e = RateLimitError(message="Slack throttled us")
    assert e.message == "Slack throttled us"
    assert e.error_code == ConnectorErrorCode.RATE_LIMIT  # default code unchanged


def test_typed_error_accepts_custom_code_override():
    e = NetworkError(error_code=ConnectorErrorCode.CONNECTION_CLOSED)
    assert e.error_code == ConnectorErrorCode.CONNECTION_CLOSED


def test_typed_error_accepts_app_error_code():
    e = NotFoundError(app_error_code="sf.404")
    assert e.app_error_code == "sf.404"
    assert e.error_code == ConnectorErrorCode.NOT_FOUND


# isinstance checks


def test_all_typed_errors_are_connector_errors():
    classes = [
        AuthenticationError,
        AuthenticationExpiredError,
        CredentialsRevokedError,
        AuthorizationError,
        TransientError,
        RateLimitError,
        UpstreamError,
        NetworkError,
        ConnectionRejectedError,
        ConnectionClosedError,
        RequestTimeoutError,
        ClientError,
        NotFoundError,
        InvalidValueError,
        UnknownValueError,
        InvalidPageTokenError,
        MissingParameterError,
        ConflictError,
        InternalError,
        InvalidResponseError,
        UnsupportedOperationError,
    ]
    for cls in classes:
        e = cls()
        assert isinstance(e, ConnectorError), f"{cls.__name__} is not a ConnectorError"
        assert isinstance(e, Exception), f"{cls.__name__} is not an Exception"


def test_auth_subclasses_are_authentication_errors():
    assert isinstance(AuthenticationExpiredError(), AuthenticationError)
    assert isinstance(CredentialsRevokedError(), AuthenticationError)


def test_network_subclasses_are_network_errors():
    assert isinstance(ConnectionRejectedError(), NetworkError)
    assert isinstance(ConnectionClosedError(), NetworkError)
    assert isinstance(RequestTimeoutError(), NetworkError)


def test_network_is_transient():
    assert isinstance(NetworkError(), TransientError)
    assert isinstance(RateLimitError(), TransientError)
    assert isinstance(UpstreamError(), TransientError)


def test_client_subclasses_are_client_errors():
    assert isinstance(NotFoundError(), ClientError)
    assert isinstance(InvalidValueError(), ClientError)
    assert isinstance(UnknownValueError(), ClientError)
    assert isinstance(InvalidPageTokenError(), ClientError)
    assert isinstance(MissingParameterError(), ClientError)
    assert isinstance(ConflictError(), ClientError)


def test_internal_subclasses_are_internal_errors():
    assert isinstance(InvalidResponseError(), InternalError)
    assert isinstance(UnsupportedOperationError(), InternalError)


# DefaultHandler


def test_default_handler_handles_typed_auth_error():
    resp = _make_response()
    e = AuthenticationExpiredError(message="token expired")
    DefaultHandler._handle_connector_error(resp, e)
    assert resp.error.error_code == ConnectorErrorCode.AUTHENTICATION_EXPIRED


def test_default_handler_handles_typed_rate_limit_error():
    resp = _make_response()
    e = RateLimitError()
    DefaultHandler._handle_connector_error(resp, e)
    assert resp.error.error_code == ConnectorErrorCode.RATE_LIMIT


def test_default_handler_handles_typed_not_found_error():
    resp = _make_response()
    e = NotFoundError(message="user 123 not found", app_error_code="myapp.usr.404")
    DefaultHandler._handle_connector_error(resp, e)
    assert resp.error.error_code == ConnectorErrorCode.NOT_FOUND
    assert resp.error.app_error_code == "myapp.usr.404"


def test_default_handler_isinstance_check_catches_typed_subclass():
    """DefaultHandler dispatches on isinstance(e, ConnectorError), so subclasses are handled."""
    resp = _make_response()
    e = CredentialsRevokedError()
    resp = DefaultHandler.handle(e, lambda _: None, resp)
    assert resp.error.error_code == ConnectorErrorCode.CREDS_REVOKED


# ConnectorErrorCode coverage


def test_every_sdk_error_code_covered_by_a_typed_class():
    """
    Ensure no ConnectorErrorCode is left without a typed exception class.
    This acts as a guard against new codes being added to ConnectorErrorCode
    without a corresponding class being created here.
    """
    all_classes = [
        AuthenticationError,
        AuthenticationExpiredError,
        CredentialsRevokedError,
        AuthorizationError,
        TransientError,
        RateLimitError,
        UpstreamError,
        NetworkError,
        ConnectionRejectedError,
        ConnectionClosedError,
        RequestTimeoutError,
        ClientError,
        NotFoundError,
        InvalidValueError,
        UnknownValueError,
        InvalidPageTokenError,
        MissingParameterError,
        ConflictError,
        InternalError,
        InvalidResponseError,
        UnsupportedOperationError,
    ]
    covered_codes = {cls.DEFAULT_CODE for cls in all_classes}
    missing = [code for code in ConnectorErrorCode if code not in covered_codes]
    assert not missing, (
        f"The following ConnectorErrorCodes have no typed exception class: {missing}. "
        "Add a class for each new code."
    )
