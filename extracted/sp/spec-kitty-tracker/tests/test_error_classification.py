from spec_kitty_tracker import FailureClass, classify_http_status
from spec_kitty_tracker.errors import ConnectorRequestError


def test_http_status_classification_matrix() -> None:
    assert classify_http_status(429) == FailureClass.RATE_LIMIT
    assert classify_http_status(503) == FailureClass.TRANSIENT
    assert classify_http_status(401) == FailureClass.AUTHENTICATION
    assert classify_http_status(403) == FailureClass.PERMISSION
    assert classify_http_status(404) == FailureClass.NOT_FOUND
    assert classify_http_status(422) == FailureClass.VALIDATION
    assert classify_http_status(418) == FailureClass.NON_RETRYABLE


def test_connector_request_error_infers_failure_class_from_status() -> None:
    err = ConnectorRequestError("upstream unavailable", status_code=503)
    assert err.failure_class == FailureClass.TRANSIENT
    assert err.is_retryable is True


def test_connector_request_error_carries_rate_limit_hint() -> None:
    err = ConnectorRequestError(
        "too many requests",
        status_code=429,
        retry_after_seconds=60,
    )
    assert err.failure_class == FailureClass.RATE_LIMIT
    assert err.retry_after_seconds == 60
    assert err.is_retryable is True


def test_connector_request_error_non_retryable_default() -> None:
    err = ConnectorRequestError("bad payload")
    assert err.failure_class == FailureClass.NON_RETRYABLE
    assert err.is_retryable is False
