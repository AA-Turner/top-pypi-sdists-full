#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025

"""Unit tests for HTTP retry mechanics."""

# fmt: off
import threading
from unittest.mock import patch

import pytest
import requests

from streamsets.sdk.retry import (
    DEFAULT_RETRY_SETTINGS, JITTER_FACTOR, MAX_DELAY, HTTPRetryError, RetryConfig, RetrySettings, http_retry,
    no_retry_on_http_error, retry_on_http_error,
)

# fmt: on


class MockResponse:
    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text


class MockHTTPError(requests.exceptions.HTTPError):
    """Mock HTTPError for testing."""

    def __init__(self, status_code):
        self.response = MockResponse(status_code)
        super().__init__(f"HTTP {status_code}", response=self.response)


class MockConnectionError(requests.exceptions.ConnectionError):
    """Mock ConnectionError for testing."""

    pass


class MockClient:
    def __init__(self):
        self.call_count = 0
        self.responses = []

    def reset(self):
        self.call_count = 0
        self.responses = []

    @http_retry()
    def make_request(self):
        self.call_count += 1
        if self.responses:
            response_or_exception = self.responses.pop(0)
            if isinstance(response_or_exception, Exception):
                raise response_or_exception
            return response_or_exception
        return MockResponse(200, "success")


def setup_function():
    RetryConfig.reset()


def teardown_function():
    RetryConfig.reset()


# =====================
# RetrySettings Tests
# =====================
def test_valid_settings():
    settings = RetrySettings(max_attempts=5, max_time=60.0, init_delay=1.0, exp_factor=2.0, jitter=True)
    assert settings.max_attempts == 5
    assert settings.max_time == 60.0


def test_default_settings():
    settings = RetrySettings()
    assert settings.max_attempts == 3
    assert settings.init_delay == 1.0


def test_invalid_max_attempts():
    with pytest.raises(ValueError):
        RetrySettings(max_attempts=0)
    with pytest.raises(ValueError):
        RetrySettings(max_attempts=100)


# =====================
# RetryConfig Tests
# =====================
def test_default_config():
    assert RetryConfig.default == DEFAULT_RETRY_SETTINGS


def test_is_retryable_status():
    assert RetryConfig.is_retryable_status(429) is True
    assert RetryConfig.is_retryable_status(500) is True
    assert RetryConfig.is_retryable_status(404) is False


def test_set_default():
    new_default = RetrySettings(max_attempts=10)
    RetryConfig.set(default=new_default)
    assert RetryConfig.default.max_attempts == 10


def test_disable_enable():
    RetryConfig.disable()
    assert RetryConfig.default.max_attempts == 1
    RetryConfig.enable(use_defaults=True)
    assert RetryConfig.default == DEFAULT_RETRY_SETTINGS


def test_add_configs_and_codes():
    RetryConfig.reset()

    new_config = RetrySettings(max_attempts=7, exp_factor=1.8)
    RetryConfig.add(status_configs={408: new_config}, retryable_status_codes={408, 409})

    assert 408 in RetryConfig.status_configs
    assert RetryConfig.status_configs[408].max_attempts == 7
    assert 408 in RetryConfig.retryable_status_codes
    assert 409 in RetryConfig.retryable_status_codes


def test_add_updates_existing_status_config():
    RetryConfig.reset()

    assert RetryConfig.status_configs[429].max_attempts == 10
    new_config = RetrySettings(max_attempts=20, init_delay=3.0)
    RetryConfig.add(status_configs={429: new_config})

    assert RetryConfig.status_configs[429].max_attempts == 20
    assert RetryConfig.status_configs[429].init_delay == 3.0


def test_add_invalid_type_raises_error():
    """Test that add() validates argument types."""
    RetryConfig.reset()

    with pytest.raises(ValueError, match="must be a dictionary"):
        RetryConfig.add(status_configs=[404])

    with pytest.raises(ValueError, match="must be a set"):
        RetryConfig.add(retryable_status_codes=[404, 405])


def test_remove_both_configs_and_codes():
    RetryConfig.reset()

    assert 429 in RetryConfig.status_configs
    assert 500 in RetryConfig.retryable_status_codes

    RetryConfig.remove(status_configs={429}, retryable_status_codes={500})

    assert 429 not in RetryConfig.status_configs
    assert 500 not in RetryConfig.retryable_status_codes


# =====================
# Basic Retry Tests
# =====================
@patch('time.sleep', return_value=None)
def test_successful_request_no_retry(mock_sleep):
    RetryConfig.reset()
    client = MockClient()
    client.responses = [MockResponse(200, "success")]
    response = client.make_request()
    assert response.status_code == 200
    assert client.call_count == 1
    mock_sleep.assert_not_called()


@patch('time.sleep', return_value=None)
def test_retry_on_500_error(mock_sleep):
    RetryConfig.reset()
    client = MockClient()
    client.responses = [MockResponse(500), MockResponse(500), MockResponse(200)]
    response = client.make_request()
    assert response.status_code == 200
    assert client.call_count == 3


@patch('time.sleep', return_value=None)
def test_retry_on_429_rate_limit(mock_sleep):
    RetryConfig.reset()
    client = MockClient()
    client.responses = [MockResponse(429), MockResponse(429), MockResponse(200)]
    response = client.make_request()
    assert response.status_code == 200
    assert client.call_count == 3


@patch('time.sleep', return_value=None)
def test_max_retries_exceeded(mock_sleep):
    RetryConfig.reset()
    client = MockClient()
    client.responses = [MockResponse(500)] * 10
    with pytest.raises(HTTPRetryError) as exc_info:
        client.make_request()
    error = exc_info.value
    assert "Max retries" in str(error)
    assert error.last_response.status_code == 500
    assert error.attempts_made == 3


@patch('time.sleep', return_value=None)
def test_non_retryable_status_code(mock_sleep):
    RetryConfig.reset()
    client = MockClient()
    client.responses = [MockResponse(404)]
    response = client.make_request()
    assert response.status_code == 404
    assert client.call_count == 1
    mock_sleep.assert_not_called()


@patch('time.sleep', return_value=None)
def test_add_retryable_code_enables_retry(mock_sleep):
    RetryConfig.reset()
    RetryConfig.add(retryable_status_codes={404})
    client = MockClient()
    client.responses = [MockResponse(404), MockResponse(404), MockResponse(200)]

    response = client.make_request()
    assert response.status_code == 200
    assert client.call_count == 3


@patch('time.sleep', return_value=None)
def test_remove_retryable_code_disables_retry(mock_sleep):
    RetryConfig.reset()
    RetryConfig.remove(status_configs={500}, retryable_status_codes={500})
    client = MockClient()
    client.responses = [MockResponse(500), MockResponse(200)]
    response = client.make_request()
    assert response.status_code == 500
    assert client.call_count == 1


# =========================
# Exception Handling Tests
# =========================
@patch('time.sleep', return_value=None)
def test_connection_error_retry(mock_sleep):
    RetryConfig.reset()
    client = MockClient()
    client.responses = [MockConnectionError(), MockConnectionError(), MockResponse(200)]
    response = client.make_request()
    assert response.status_code == 200
    assert client.call_count == 3
    assert mock_sleep.call_count == 2


@patch('time.sleep', return_value=None)
def test_http_exception_with_status_code(mock_sleep):
    RetryConfig.reset()
    client = MockClient()
    client.responses = [MockHTTPError(500), MockHTTPError(500), MockResponse(200)]
    response = client.make_request()
    assert response.status_code == 200
    assert client.call_count == 3


@patch('time.sleep', return_value=None)
def test_http_error_404_not_retried_by_default(mock_sleep):
    RetryConfig.reset()
    client = MockClient()
    client.responses = [MockHTTPError(404)]

    with pytest.raises(requests.exceptions.HTTPError):
        client.make_request()

    assert client.call_count == 1
    mock_sleep.assert_not_called()


@patch('time.sleep', return_value=None)
def test_http_error_404_retried_when_configured(mock_sleep):
    RetryConfig.set(status_configs={404: RetrySettings(max_attempts=3, init_delay=1.0, exp_factor=2.0)})

    client = MockClient()
    client.responses = [MockHTTPError(404), MockHTTPError(404), MockResponse(200)]

    response = client.make_request()

    assert response.status_code == 200
    assert client.call_count == 3
    assert mock_sleep.call_count == 2


@patch('time.sleep', return_value=None)
def test_http_retry_error(mock_sleep):
    RetryConfig.set(status_configs={500: RetrySettings(max_attempts=3)})
    client = MockClient()
    client.responses = [MockHTTPError(500)] * 5  # More than max_attempts

    with pytest.raises(HTTPRetryError) as exc_info:
        client.make_request()

    assert exc_info.value.attempts_made == 3


@pytest.mark.parametrize(
    "exception_class,exception_msg",
    [
        (ValueError, "Invalid input"),
        (AttributeError, "'NoneType' object has no attribute 'x'"),
        (TypeError, "unsupported operand type"),
        (KeyError, "missing key"),
        (IndexError, "list index out of range"),
    ],
)
def test_non_requests_exceptions_not_retried(exception_class, exception_msg):
    RetryConfig.reset()
    client = MockClient()
    client.responses = [exception_class(exception_msg)]

    with pytest.raises(exception_class, match=exception_msg):
        client.make_request()

    assert client.call_count == 1


# =========================
# Context Manager Tests
# =========================
@patch('time.sleep', return_value=None)
def test_retry_with_only_status_codes(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(429), MockResponse(200)]
    with retry_on_http_error(RetrySettings(max_attempts=5), only_status_codes={429}):
        response = client.make_request()
    assert response.status_code == 200
    assert client.call_count == 2


@patch('time.sleep', return_value=None)
def test_only_status_codes_excludes_others(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(429), MockResponse(500), MockResponse(200)]
    with retry_on_http_error(RetrySettings(max_attempts=5), only_status_codes={429}):
        response = client.make_request()
    assert response.status_code == 500
    assert client.call_count == 2


@patch('time.sleep', return_value=None)
def test_skip_status_codes(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(501), MockResponse(500), MockResponse(200)]
    with retry_on_http_error(RetrySettings(max_attempts=5), skip_status_codes={500}):
        response = client.make_request()
    assert response.status_code == 500
    assert client.call_count == 2


@patch('time.sleep', return_value=None)
def test_no_retry_context(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(500)]
    with no_retry_on_http_error():
        response = client.make_request()
    assert response.status_code == 500
    assert client.call_count == 1


def test_cannot_use_both_filters():
    with pytest.raises(ValueError, match="Cannot specify both"):
        with retry_on_http_error(RetrySettings(max_attempts=5), only_status_codes={429}, skip_status_codes={500}):
            pass


# =========================
# Edge Cases Tests
# =========================
@patch('time.sleep', return_value=None)
def test_nested_context_managers(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(429), MockResponse(200)]
    with retry_on_http_error(RetrySettings(max_attempts=10)):
        with retry_on_http_error(RetrySettings(max_attempts=2), only_status_codes={429}):
            response = client.make_request()
    assert response.status_code == 200


@patch('time.sleep', return_value=None)
def test_2xx_never_retries(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(201)]
    response = client.make_request()
    assert response.status_code == 201
    assert client.call_count == 1


@patch('time.sleep', return_value=None)
def test_3xx_never_retries(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(301)]
    response = client.make_request()
    assert response.status_code == 301
    assert client.call_count == 1


@patch('time.sleep', return_value=None)
def test_all_4xx_retry_with_override(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(404), MockResponse(200)]
    with retry_on_http_error(RetrySettings(max_attempts=5)):
        response = client.make_request()
    assert response.status_code == 200
    assert client.call_count == 2


def test_config_thread_safety():
    errors = []

    def modify_config():
        try:
            for _ in range(10):
                RetryConfig.set(default=RetrySettings(max_attempts=5))
                RetryConfig.reset()
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=modify_config) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(errors) == 0


# =========================================
# Exponential Backoff, Jitter, MaxCap Tests
# =========================================
@patch('time.sleep', return_value=None)
def test_exponential_backoff_called(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(500), MockResponse(500), MockResponse(200)]
    client.make_request()
    assert mock_sleep.call_count == 2


@patch('time.sleep', return_value=None)
def test_exponential_backoff_values(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(500), MockResponse(500), MockResponse(500), MockResponse(200)]

    settings = RetrySettings(max_attempts=4, init_delay=2.0, exp_factor=2.0, jitter=False)
    with retry_on_http_error(settings):
        response = client.make_request()

    assert response.status_code == 200
    assert mock_sleep.call_count == 3

    calls = [call[0][0] for call in mock_sleep.call_args_list]
    assert calls == [2.0, 4.0, 8.0]


@patch('time.sleep', return_value=None)
def test_jitter_adds_randomness(mock_sleep):
    """Verify jitter adds randomness based on JITTER_FACTOR."""
    client = MockClient()
    client.responses = [MockResponse(500), MockResponse(500), MockResponse(200)]

    settings = RetrySettings(max_attempts=3, init_delay=1.0, exp_factor=2.0, jitter=True)
    with retry_on_http_error(settings):
        client.make_request()

    assert mock_sleep.call_count == 2

    calls = [call[0][0] for call in mock_sleep.call_args_list]
    assert 1 * (1 - JITTER_FACTOR) <= calls[0] <= 1 * (1 + JITTER_FACTOR)
    assert 2 * (1 - JITTER_FACTOR) <= calls[1] <= 2 * (1 + JITTER_FACTOR)


@patch('time.sleep', return_value=None)
def test_max_delay_cap(mock_sleep):
    client = MockClient()
    client.responses = [MockResponse(500)] * 10 + [MockResponse(200)]

    settings = RetrySettings(max_attempts=11, init_delay=10.0, exp_factor=3.0, jitter=False)
    with retry_on_http_error(settings):
        client.make_request()

    calls = [call[0][0] for call in mock_sleep.call_args_list]
    assert all(delay <= MAX_DELAY for delay in calls)
