import pytest

from pipebio.pipebio_client import PipebioClient


class TestPipeBioClient:

    def test_valid_url_no_slash(self):
        assert PipebioClient.sanitize_baseurl("https://example.com") == "https://example.com"

    def test_valid_url_with_trailing_slash(self):
        assert PipebioClient.sanitize_baseurl("https://example.com/") == "https://example.com"

    def test_valid_url_with_whitespace(self):
        assert PipebioClient.sanitize_baseurl("  https://example.com/  ") == "https://example.com"

    def test_url_that_is_only_https(self):
        assert PipebioClient.sanitize_baseurl("https://") == "https://"

    def test_invalid_http_url(self):
        with pytest.raises(ValueError, match="must start with 'https://'"):
            PipebioClient.sanitize_baseurl("http://example.com")

    def test_missing_protocol(self):
        with pytest.raises(ValueError, match="must start with 'https://'"):
            PipebioClient.sanitize_baseurl("example.com")

    def test_empty_string(self):
        with pytest.raises(ValueError, match="must start with 'https://'"):
            PipebioClient.sanitize_baseurl("")

    def test_whitespace_only(self):
        with pytest.raises(ValueError, match="must start with 'https://'"):
            PipebioClient.sanitize_baseurl("   ")
