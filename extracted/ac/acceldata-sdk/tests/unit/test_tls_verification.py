"""Regression tests for TLS verification on the Torch HTTP client.

Certificates and keys exist only inside a temporary directory and are deleted
when the test finishes. The HTTPS peer listens on 127.0.0.1. Credentials are
synthetic.
"""
import inspect
import os
import ssl
import subprocess
import threading
import unittest
import warnings
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory

import requests
from urllib3.exceptions import InsecureRequestWarning

from acceldata_sdk.torch_client import TorchClient
from acceldata_sdk.torch_http_client import TorchHttpClient, _HEADERS

_ACCESS_HEADER = "accessKey"
_SECRET_HEADER = "secretKey"
_LOOPBACK = "127.0.0.1"


class _RecordingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._record()

    def do_POST(self):
        self._record()

    def do_PUT(self):
        self._record()

    def do_DELETE(self):
        self._record()

    def _record(self):
        self.server.captured.append(
            {
                _ACCESS_HEADER: self.headers.get(_ACCESS_HEADER),
                _SECRET_HEADER: self.headers.get(_SECRET_HEADER),
                "path": self.path,
            }
        )
        body = b'{"status":"ok"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return


def _openssl(directory, *args):
    completed = subprocess.run(
        ["openssl", *args],
        cwd=directory,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "openssl failed: {}\n{}".format(" ".join(args), completed.stderr)
        )


def _openssl_config(directory, name, common_name, is_ca):
    path = os.path.join(directory, name)
    basic = "CA:TRUE" if is_ca else "CA:FALSE"
    Path(path).write_text(
        "\n".join(
            [
                "[req]",
                "distinguished_name = dn",
                "x509_extensions = ext",
                "req_extensions = ext",
                "prompt = no",
                "[dn]",
                "CN = {}".format(common_name),
                "[ext]",
                "subjectAltName = DNS:localhost,IP:127.0.0.1",
                "basicConstraints = critical,{}".format(basic),
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def _make_self_signed(directory):
    config = _openssl_config(directory, "self.cnf", _LOOPBACK, is_ca=False)
    _openssl(
        directory,
        "req",
        "-x509",
        "-newkey",
        "rsa:2048",
        "-keyout",
        "self.key",
        "-out",
        "self.crt",
        "-days",
        "2",
        "-nodes",
        "-config",
        config,
        "-extensions",
        "ext",
    )
    return os.path.join(directory, "self.crt"), os.path.join(directory, "self.key")


def _make_private_ca_material(directory):
    ca_config = _openssl_config(directory, "ca.cnf", "Acceldata SDK Test CA", is_ca=True)
    server_config = _openssl_config(directory, "server.cnf", _LOOPBACK, is_ca=False)
    _openssl(
        directory,
        "req",
        "-x509",
        "-newkey",
        "rsa:2048",
        "-keyout",
        "ca.key",
        "-out",
        "ca.crt",
        "-days",
        "2",
        "-nodes",
        "-config",
        ca_config,
        "-extensions",
        "ext",
    )
    _openssl(
        directory,
        "req",
        "-newkey",
        "rsa:2048",
        "-keyout",
        "server.key",
        "-out",
        "server.csr",
        "-nodes",
        "-config",
        server_config,
        "-reqexts",
        "ext",
    )
    _openssl(
        directory,
        "x509",
        "-req",
        "-in",
        "server.csr",
        "-CA",
        "ca.crt",
        "-CAkey",
        "ca.key",
        "-CAcreateserial",
        "-out",
        "server.crt",
        "-days",
        "2",
        "-extfile",
        server_config,
        "-extensions",
        "ext",
    )
    return (
        os.path.join(directory, "ca.crt"),
        os.path.join(directory, "server.crt"),
        os.path.join(directory, "server.key"),
    )


def _start_https_server(certfile, keyfile):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    server = ThreadingHTTPServer((_LOOPBACK, 0), _RecordingHandler)
    server.captured = []
    server.socket = context.wrap_socket(server.socket, server_side=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _stop_https_server(server, thread):
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)


def _client(verify_ssl, access_key, secret_key):
    return TorchHttpClient(
        url="https://{}".format(_LOOPBACK),
        access_key=access_key,
        secret_key=secret_key,
        torch_connection_timeout_ms=3000,
        torch_read_timeout_ms=3000,
        verify_ssl=verify_ssl,
    )


class TlsVerificationTests(unittest.TestCase):
    def setUp(self):
        _HEADERS[_ACCESS_HEADER] = None
        _HEADERS[_SECRET_HEADER] = None
        _HEADERS["Content-Type"] = "application/json"

    def tearDown(self):
        _HEADERS[_ACCESS_HEADER] = None
        _HEADERS[_SECRET_HEADER] = None
        _HEADERS["Content-Type"] = "application/json"

    def test_default_verify_ssl_uses_requests_verification(self):
        client = _client(True, "SYNTHETIC_ACCESS", "SYNTHETIC_SECRET")
        self.assertIs(client._verify_ssl, True)
        public = TorchClient(
            url="https://{}".format(_LOOPBACK),
            access_key="SYNTHETIC_ACCESS",
            secret_key="SYNTHETIC_SECRET",
        )
        self.assertIs(public.client._verify_ssl, True)

    def test_verify_ssl_rejects_unsupported_values(self):
        with self.assertRaises(TypeError):
            _client(1, "SYNTHETIC_ACCESS", "SYNTHETIC_SECRET")

    def test_request_paths_do_not_disable_verification(self):
        source = Path(inspect.getfile(TorchHttpClient)).read_text(encoding="utf-8")
        self.assertNotIn("verify=False", source)
        self.assertNotIn("disable_warnings", source)
        self.assertNotIn("InsecureRequestWarning", source)

    def test_self_signed_peer_is_rejected_before_credentials_are_sent(self):
        access_key = "SYNTHETIC_ACCESS_SELFSIGNED"
        secret_key = "SYNTHETIC_SECRET_SELFSIGNED"
        with TemporaryDirectory() as directory:
            certfile, keyfile = _make_self_signed(directory)
            server, thread = _start_https_server(certfile, keyfile)
            try:
                port = server.server_address[1]
                client = _client(True, access_key, secret_key)
                with self.assertRaises(requests.exceptions.SSLError):
                    client._get("https://{}:{}/health".format(_LOOPBACK, port))
                self.assertEqual(server.captured, [])
            finally:
                _stop_https_server(server, thread)

    def test_explicit_verify_ssl_false_reaches_self_signed_peer(self):
        access_key = "SYNTHETIC_ACCESS_DISABLED"
        secret_key = "SYNTHETIC_SECRET_DISABLED"
        with TemporaryDirectory() as directory:
            certfile, keyfile = _make_self_signed(directory)
            server, thread = _start_https_server(certfile, keyfile)
            try:
                port = server.server_address[1]
                public = TorchClient(
                    url="https://{}".format(_LOOPBACK),
                    access_key=access_key,
                    secret_key=secret_key,
                    torch_connection_timeout_ms=3000,
                    torch_read_timeout_ms=3000,
                    verify_ssl=False,
                )
                self.assertIs(public.client._verify_ssl, False)
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always")
                    body = public.client._get(
                        "https://{}:{}/health".format(_LOOPBACK, port)
                    )
                self.assertEqual(body, {"status": "ok"})
                self.assertEqual(len(server.captured), 1)
                self.assertEqual(server.captured[0][_ACCESS_HEADER], access_key)
                self.assertEqual(server.captured[0][_SECRET_HEADER], secret_key)
                self.assertTrue(
                    any(issubclass(item.category, InsecureRequestWarning) for item in caught)
                )
            finally:
                _stop_https_server(server, thread)

    def test_private_ca_succeeds_only_after_ca_bundle_is_configured(self):
        with TemporaryDirectory() as directory:
            ca_file, certfile, keyfile = _make_private_ca_material(directory)
            server, thread = _start_https_server(certfile, keyfile)
            try:
                port = server.server_address[1]
                url = "https://{}:{}/health".format(_LOOPBACK, port)

                untrusted_access = "SYNTHETIC_ACCESS_UNTRUSTED"
                untrusted_secret = "SYNTHETIC_SECRET_UNTRUSTED"
                untrusted = _client(True, untrusted_access, untrusted_secret)
                with self.assertRaises(requests.exceptions.SSLError):
                    untrusted._get(url)
                self.assertEqual(server.captured, [])

                trusted_access = "SYNTHETIC_ACCESS_BUNDLE"
                trusted_secret = "SYNTHETIC_SECRET_BUNDLE"
                trusted = _client(ca_file, trusted_access, trusted_secret)
                body = trusted._get(url)
                self.assertEqual(body, {"status": "ok"})
                self.assertEqual(len(server.captured), 1)
                self.assertEqual(server.captured[0][_ACCESS_HEADER], trusted_access)
                self.assertEqual(server.captured[0][_SECRET_HEADER], trusted_secret)
                self.assertNotEqual(server.captured[0][_ACCESS_HEADER], untrusted_access)
                self.assertNotEqual(server.captured[0][_SECRET_HEADER], untrusted_secret)
            finally:
                _stop_https_server(server, thread)

    def test_private_ca_succeeds_with_explicit_ssl_context(self):
        access_key = "SYNTHETIC_ACCESS_CONTEXT"
        secret_key = "SYNTHETIC_SECRET_CONTEXT"
        with TemporaryDirectory() as directory:
            ca_file, certfile, keyfile = _make_private_ca_material(directory)
            context = ssl.create_default_context()
            context.load_verify_locations(cafile=ca_file)
            server, thread = _start_https_server(certfile, keyfile)
            try:
                port = server.server_address[1]
                client = _client(context, access_key, secret_key)
                body = client._get("https://{}:{}/health".format(_LOOPBACK, port))
                self.assertEqual(body, {"status": "ok"})
                self.assertEqual(len(server.captured), 1)
                self.assertEqual(server.captured[0][_ACCESS_HEADER], access_key)
                self.assertEqual(server.captured[0][_SECRET_HEADER], secret_key)
            finally:
                _stop_https_server(server, thread)


if __name__ == "__main__":
    unittest.main()
