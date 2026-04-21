import os
import platform
from unittest import TestCase, mock

from launchable.utils.http_client import _HttpClient, _sanitize_headers
from launchable.version import __version__


class HttpClientTest(TestCase):
    @mock.patch.dict(
        os.environ,
        {"LAUNCHABLE_ORGANIZATION": "launchableinc", "LAUNCHABLE_WORKSPACE": "test"},
        clear=True,
    )
    def test_header(self):
        cli = _HttpClient("/test")
        self.assertEqual(cli._headers(True), {
            'Content-Encoding': 'gzip',
            'Content-Type': 'application/json',
            "User-Agent": "Launchable/{} (Python {}, {})".format(
                __version__,
                platform.python_version(),
                platform.platform(),
            ),
        })

        self.assertEqual(cli._headers(False), {
            'Content-Type': 'application/json',
            "User-Agent": "Launchable/{} (Python {}, {})".format(
                __version__,
                platform.python_version(),
                platform.platform(),
            ),
        })

        cli = _HttpClient("/test", test_runner="dummy")
        self.assertEqual(cli._headers(False), {
            'Content-Type': 'application/json',
            "User-Agent": "Launchable/{} (Python {}, {}) TestRunner/{}".format(
                __version__,
                platform.python_version(),
                platform.platform(),
                "dummy",
            ),
        })

    def test_sanitize_headers_with_bearer_token(self):
        headers = {
            'Authorization': 'Bearer v1:konboi/arm-testing:cfcxxxxxxxxxxxxxx',
            'Content-Type': 'application/json',
            'User-Agent': 'test-agent'
        }
        sanitized = _sanitize_headers(headers)

        # Original headers should not be modified
        self.assertEqual(headers['Authorization'], 'Bearer v1:konboi/arm-testing:cfcxxxxxxxxxxxxxx')

        # Sanitized headers should have token redacted
        self.assertEqual(sanitized['Authorization'], 'Bearer [REDACTED]')
        self.assertEqual(sanitized['Content-Type'], 'application/json')
        self.assertEqual(sanitized['User-Agent'], 'test-agent')

    def test_sanitize_headers_without_authorization(self):
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'test-agent'
        }
        sanitized = _sanitize_headers(headers)

        # All headers should remain unchanged
        self.assertEqual(sanitized, headers)

    def test_sanitize_headers_with_non_bearer_authorization(self):
        headers = {
            'Authorization': 'Basic dXNlcjpwYXNz',
            'Content-Type': 'application/json'
        }
        sanitized = _sanitize_headers(headers)

        # Non-Bearer authorization should remain unchanged
        self.assertEqual(sanitized['Authorization'], 'Basic dXNlcjpwYXNz')
