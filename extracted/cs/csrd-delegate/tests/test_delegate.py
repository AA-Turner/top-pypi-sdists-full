"""Tests for csrd.delegate retry profiles and BaseDelegate helpers."""

from csrd.delegate._base_delegate import BaseDelegate
from csrd.delegate._retry import RETRY_PROFILES


class TestRetryProfiles:
    def test_no_retry_profile(self):
        profile = RETRY_PROFILES["no_retry"]
        assert profile["retry_enabled"] is False

    def test_conservative_profile(self):
        profile = RETRY_PROFILES["conservative"]
        assert profile["retry_enabled"] is True
        assert profile["retry_attempts"] == 2
        assert profile["retry_backoff"] == 0.5

    def test_aggressive_profile(self):
        profile = RETRY_PROFILES["aggressive"]
        assert profile["retry_enabled"] is True
        assert profile["retry_attempts"] == 5

    def test_resilient_profile(self):
        profile = RETRY_PROFILES["resilient"]
        assert profile["retry_enabled"] is True
        assert profile["retry_attempts"] == 7


class TestBaseDelegateHelpers:
    def test_normalize_headers(self):
        headers = {
            "Content-Type": "application/json",
            "X-Custom": "value",
            "content-type": "text/html",
        }
        result = BaseDelegate._normalize_headers(headers)
        # First occurrence wins
        assert result["content-type"] == "application/json"
        assert result["x-custom"] == "value"

    def test_filter_headers(self):
        delegate = BaseDelegate("http://localhost", header_filter_list=["host", "x-secret"])
        headers = {"host": "localhost", "x-secret": "hidden", "x-public": "visible"}
        result = delegate._filter_headers(headers)
        assert "host" not in result
        assert "x-secret" not in result
        assert result["x-public"] == "visible"

    def test_filter_headers_default_removes_host(self):
        delegate = BaseDelegate("http://localhost")
        headers = {"host": "example.com", "accept": "application/json"}
        result = delegate._filter_headers(headers)
        assert "host" not in result
        assert result["accept"] == "application/json"

    def test_ignore_incoming_headers(self):
        delegate = BaseDelegate("http://localhost", ignore_incoming_headers=True)
        assert delegate._headers == {}

    def test_filter_method_kwargs(self):
        def sample_method(url, headers=None, timeout=None):
            pass

        result = BaseDelegate._filter_method_kwargs(
            sample_method,
            url="/test",
            headers={"x": "y"},
            timeout=10,
            unknown_param="ignored",
            none_param=None,
        )
        assert "url" in result
        assert "headers" in result
        assert "timeout" in result
        assert "unknown_param" not in result
        assert "none_param" not in result

    def test_retry_profile_configuration(self):
        delegate = BaseDelegate("http://localhost", retry_profile="conservative")
        assert delegate._retry_enabled is True
        assert delegate._retry_profile == "conservative"

    def test_no_retry_by_default(self):
        delegate = BaseDelegate("http://localhost")
        assert delegate._retry_enabled is False

    def test_parse_status_code_success(self):
        from unittest.mock import MagicMock

        response = MagicMock()
        response.status_code = 200
        result = BaseDelegate._parse_status_code(response)
        assert result is response

    def test_parse_status_code_with_handler(self):
        from unittest.mock import MagicMock

        response = MagicMock()
        response.status_code = 404
        custom_response = MagicMock()
        handlers = {404: lambda r: custom_response}
        result = BaseDelegate._parse_status_code(response, response_handlers=handlers)
        assert result is custom_response
