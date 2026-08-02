"""Tests for the wrapped requests module."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch
from requests.exceptions import ProxyError

from coze_workload_identity._debug import _reset_coze_debug_for_tests
from coze_workload_identity import requests as sdk_requests


class TestConfiguredRequests(unittest.TestCase):
    def setUp(self):
        _reset_coze_debug_for_tests()
        self._tmp_dir = tempfile.TemporaryDirectory()
        self.ca_path = os.path.join(self._tmp_dir.name, "coze-ca.pem")
        with open(self.ca_path, "w", encoding="utf-8") as f:
            f.write("test ca")

    def tearDown(self):
        for key in [
            "COZE_SKILL_PROXY_DOMAIN",
            "COZE_OUTBOUND_AUTH_PROXY",
            "identity_ticket",
            "REQUESTS_CA_BUNDLE",
            "CURL_CA_BUNDLE",
            "SSL_CERT_FILE",
            "COZE_OUTBOUND_AUTH_PROXY_CA_PATH",
            "COZE_OUTBOUND_AUTH_PROXY_CA",
        ]:
            os.environ.pop(key, None)
        self._tmp_dir.cleanup()
        _reset_coze_debug_for_tests()

    def test_session_uses_ca_bundle_without_debug_output_by_default(self):
        os.environ["COZE_SKILL_PROXY_DOMAIN"] = "https://proxy.example.com:443"
        os.environ["identity_ticket"] = "ticket_123"
        os.environ["REQUESTS_CA_BUNDLE"] = "/parent/requests-ca.pem"
        os.environ["CURL_CA_BUNDLE"] = "/parent/curl-ca.pem"
        os.environ["SSL_CERT_FILE"] = "/parent/ssl-ca.pem"
        os.environ["COZE_OUTBOUND_AUTH_PROXY_CA_PATH"] = self.ca_path

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            session = sdk_requests.session()

        self.assertFalse(session.trust_env)
        self.assertEqual(session.verify, self.ca_path)
        self.assertIsNone(session.cert)
        self.assertEqual(stdout.getvalue(), "")

    def test_session_prints_proxy_url_when_coze_debug_arg_is_present(self):
        os.environ["COZE_SKILL_PROXY_DOMAIN"] = "https://proxy.example.com:443"
        os.environ["identity_ticket"] = "ticket_123"
        os.environ["COZE_OUTBOUND_AUTH_PROXY_CA_PATH"] = self.ca_path

        with patch("sys.argv", ["tool.py", "--coze-debug", "query"]):
            _reset_coze_debug_for_tests()
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                sdk_requests.session()

            self.assertIn(
                "Configured proxy_url: https://space:ticket_123@proxy.example.com:443",
                stdout.getvalue(),
            )
            self.assertEqual(["tool.py", "query"], __import__("sys").argv)

    def test_request_discards_explicit_certificate_arguments(self):
        os.environ["COZE_SKILL_PROXY_DOMAIN"] = "https://proxy.example.com:443"
        os.environ["identity_ticket"] = "ticket_123"
        os.environ["COZE_OUTBOUND_AUTH_PROXY_CA_PATH"] = self.ca_path
        session = sdk_requests.session()
        session.verify = "/session/ca.pem"
        session.cert = "/session/client.pem"

        with patch("requests.sessions.Session.request", return_value=Mock()) as mock_request:
            session.request(
                "GET",
                "https://example.test",
                verify="/caller/ca.pem",
                cert="/caller/client.pem",
            )

        request_kwargs = mock_request.call_args.kwargs
        self.assertNotIn("verify", request_kwargs)
        self.assertNotIn("cert", request_kwargs)
        self.assertNotIn("x-tt-env", request_kwargs["headers"])
        self.assertNotIn("x-use-ppe", request_kwargs["headers"])
        self.assertEqual(session.verify, self.ca_path)
        self.assertIsNone(session.cert)

    def test_request_preserves_existing_headers_without_ppe_headers(self):
        os.environ["COZE_SKILL_PROXY_DOMAIN"] = "https://proxy.example.com:443"
        os.environ["identity_ticket"] = "ticket_123"
        os.environ["COZE_OUTBOUND_AUTH_PROXY_CA_PATH"] = self.ca_path
        session = sdk_requests.session()

        with patch("requests.sessions.Session.request", return_value=Mock()) as mock_request:
            session.request(
                "GET",
                "https://example.test",
                headers={"X-Caller": "caller-header"},
            )

        request_headers = mock_request.call_args.kwargs["headers"]
        self.assertEqual(request_headers["X-Caller"], "caller-header")
        self.assertNotIn("x-tt-env", request_headers)
        self.assertNotIn("x-use-ppe", request_headers)

    def test_request_debug_output_is_silent_by_default(self):
        os.environ["COZE_SKILL_PROXY_DOMAIN"] = "https://proxy.example.com:443"
        os.environ["identity_ticket"] = "ticket_123"
        os.environ["COZE_OUTBOUND_AUTH_PROXY_CA_PATH"] = self.ca_path
        session = sdk_requests.session()

        prepared_request = Mock()
        prepared_request.method = "POST"
        prepared_request.url = "https://example.test/api"
        prepared_request.headers = {"X-Request": "request-header"}
        prepared_request.body = b'{"query": "weather"}'

        response = Mock()
        response.request = prepared_request
        response.status_code = 200
        response.headers = {"X-Response": "response-header"}

        with patch(
            "requests.sessions.Session.request",
            return_value=response,
        ):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                session.request("POST", "https://example.test/api")

        console_output = stdout.getvalue()
        self.assertEqual(console_output, "")

    def test_request_prints_actual_request_and_response_details_with_debug_arg(self):
        os.environ["COZE_SKILL_PROXY_DOMAIN"] = "https://proxy.example.com:443"
        os.environ["identity_ticket"] = "ticket_123"
        os.environ["COZE_OUTBOUND_AUTH_PROXY_CA_PATH"] = self.ca_path
        with patch("sys.argv", ["tool.py", "--coze-debug"]):
            _reset_coze_debug_for_tests()
            with redirect_stdout(io.StringIO()):
                session = sdk_requests.session()

        prepared_request = Mock()
        prepared_request.method = "POST"
        prepared_request.url = "https://example.test/api"
        prepared_request.headers = {"X-Request": "request-header"}
        prepared_request.body = b'{"query": "weather"}'

        response = Mock()
        response.request = prepared_request
        response.status_code = 200
        response.headers = {"X-Response": "response-header"}

        with patch(
            "requests.sessions.Session.request",
            return_value=response,
        ):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                session.request("POST", "https://example.test/api")

        console_output = stdout.getvalue()
        self.assertIn("Configured request", console_output)
        self.assertIn("X-Request", console_output)
        self.assertIn('{"query": "weather"}', console_output)
        self.assertIn("Configured response", console_output)
        self.assertIn("X-Response", console_output)

    def test_request_prints_request_details_when_request_fails(self):
        os.environ["COZE_SKILL_PROXY_DOMAIN"] = "https://proxy.example.com:443"
        os.environ["identity_ticket"] = "ticket_123"
        os.environ["COZE_OUTBOUND_AUTH_PROXY_CA_PATH"] = self.ca_path
        with patch("sys.argv", ["tool.py", "--coze-debug"]):
            _reset_coze_debug_for_tests()
            with redirect_stdout(io.StringIO()):
                session = sdk_requests.session()

        prepared_request = Mock()
        prepared_request.method = "POST"
        prepared_request.url = "https://example.test/api"
        prepared_request.headers = {"X-Request": "request-header"}
        prepared_request.body = b'{"query": "weather"}'
        error = ProxyError("proxy failed", request=prepared_request)

        with patch(
            "requests.sessions.Session.request",
            side_effect=error,
        ):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                with self.assertRaises(ProxyError):
                    session.request("POST", "https://example.test/api")

        console_output = stdout.getvalue()
        self.assertIn("Configured request", console_output)
        self.assertIn("X-Request", console_output)
        self.assertIn('{"query": "weather"}', console_output)
        self.assertIn("Configured request failed", console_output)
        self.assertIn("proxy failed", console_output)


if __name__ == "__main__":
    unittest.main()
