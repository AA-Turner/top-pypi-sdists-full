import datetime as dt
import ipaddress
import os
import ssl
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterator
from unittest.mock import MagicMock, patch

import httpx
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

import truststore

from runlayer_cli import tls

# truststore.SSLContext subclasses the original ssl.SSLContext at class-def
# time — so __bases__[0] always points to the un-injected stdlib class, even
# after some other test has triggered truststore.inject_into_ssl() (which
# would otherwise return a client-only truststore.SSLContext from
# `ssl.SSLContext(PROTOCOL_TLS_SERVER)` and break wrap_socket(server_side=True)).
_REAL_SSL_CONTEXT: type[ssl.SSLContext] = truststore.SSLContext.__bases__[0]


class _QuietThreadingHTTPServer(ThreadingHTTPServer):
    def handle_error(self, request: object, client_address: object) -> None:
        pass


class _OkHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = b'{"ok": true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        pass


@contextmanager
def _https_server(cert_path: Path, key_path: Path) -> Iterator[str]:
    server = _QuietThreadingHTTPServer(("127.0.0.1", 0), _OkHandler)
    context = _REAL_SSL_CONTEXT(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    server.socket = context.wrap_socket(server.socket, server_side=True)

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"https://localhost:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _write_private_ca_server_certs(tmp_path: Path) -> tuple[Path, Path, Path]:
    now = dt.datetime.now(dt.UTC)
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ca_name = x509.Name(
        [x509.NameAttribute(NameOID.COMMON_NAME, "Runlayer Test Root CA")]
    )
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(ca_name)
        .issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - dt.timedelta(minutes=1))
        .not_valid_after(now + dt.timedelta(days=1))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256())
    )

    server_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    server_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    server_cert = (
        x509.CertificateBuilder()
        .subject_name(server_name)
        .issuer_name(ca_name)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - dt.timedelta(minutes=1))
        .not_valid_after(now + dt.timedelta(days=1))
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    x509.DNSName("localhost"),
                    x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
                ]
            ),
            critical=False,
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
            critical=False,
        )
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256())
    )

    ca_path = tmp_path / "ca.pem"
    cert_path = tmp_path / "server.pem"
    key_path = tmp_path / "server-key.pem"
    ca_path.write_bytes(ca_cert.public_bytes(serialization.Encoding.PEM))
    cert_path.write_bytes(server_cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(
        server_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    return ca_path, cert_path, key_path


def test_ca_bundle_prefers_runlayer_env(monkeypatch):
    monkeypatch.setenv("SSL_CERT_FILE", "/tmp/ssl.pem")
    monkeypatch.setenv("RUNLAYER_CA_BUNDLE", "/tmp/runlayer.pem")

    assert tls.get_ca_bundle_path() == "/tmp/runlayer.pem"


def test_ca_bundle_falls_back_to_ssl_cert_file(monkeypatch):
    monkeypatch.delenv("RUNLAYER_CA_BUNDLE", raising=False)
    monkeypatch.setenv("SSL_CERT_FILE", "/tmp/ssl.pem")
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", "/tmp/requests.pem")

    assert tls.get_ca_bundle_path() == "/tmp/ssl.pem"


def test_ca_bundle_falls_back_to_requests_ca_bundle(monkeypatch):
    monkeypatch.delenv("RUNLAYER_CA_BUNDLE", raising=False)
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", "/tmp/requests.pem")

    assert tls.get_ca_bundle_path() == "/tmp/requests.pem"


def test_ca_bundle_dir_uses_ssl_cert_dir(monkeypatch):
    monkeypatch.setenv("SSL_CERT_DIR", "/tmp/certs")

    assert tls.get_ca_bundle_dir() == "/tmp/certs"


def test_set_ca_bundle_path_sets_runlayer_env(monkeypatch):
    monkeypatch.delenv("RUNLAYER_CA_BUNDLE", raising=False)

    tls.set_ca_bundle_path("/tmp/debug.pem")

    assert tls.get_ca_bundle_path() == "/tmp/debug.pem"
    os.environ.pop("RUNLAYER_CA_BUNDLE", None)


def test_build_verify_uses_system_trust_and_extra_bundle(monkeypatch):
    context = MagicMock(spec=ssl.SSLContext)
    monkeypatch.setenv("RUNLAYER_CA_BUNDLE", "/tmp/runlayer.pem")
    monkeypatch.setenv("SSL_CERT_DIR", "/tmp/certs")

    with patch("runlayer_cli.tls.truststore.SSLContext", return_value=context) as ctor:
        result = tls.build_verify()

    ctor.assert_called_once_with(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations.assert_called_once_with(
        cafile="/tmp/runlayer.pem", capath="/tmp/certs"
    )
    assert result is context


def test_build_verify_ignores_missing_ca_bundle(monkeypatch):
    context = MagicMock(spec=ssl.SSLContext)
    context.load_verify_locations.side_effect = FileNotFoundError("/tmp/missing.pem")
    monkeypatch.delenv("RUNLAYER_CA_BUNDLE", raising=False)
    monkeypatch.setenv("SSL_CERT_FILE", "/tmp/missing.pem")

    with (
        patch("runlayer_cli.tls.truststore.SSLContext", return_value=context),
        pytest.warns(RuntimeWarning, match="Ignoring invalid TLS CA bundle"),
    ):
        result = tls.build_verify()

    context.load_verify_locations.assert_called_once_with(
        cafile="/tmp/missing.pem", capath=None
    )
    assert result is context


def test_http_client_sets_verify_context():
    context = MagicMock(spec=ssl.SSLContext)

    with (
        patch("runlayer_cli.tls.build_verify", return_value=context),
        patch("runlayer_cli.tls.httpx.Client") as client_cls,
    ):
        tls.http_client(headers={"User-Agent": "Runlayer CLI"})

    assert client_cls.call_args.kwargs["verify"] is context
    assert client_cls.call_args.kwargs["headers"] == {"User-Agent": "Runlayer CLI"}


def test_async_http_client_sets_verify_context():
    context = MagicMock(spec=ssl.SSLContext)

    with (
        patch("runlayer_cli.tls.build_verify", return_value=context),
        patch("runlayer_cli.tls.httpx.AsyncClient") as client_cls,
    ):
        tls.async_http_client(headers={"User-Agent": "Runlayer CLI"})

    assert client_cls.call_args.kwargs["verify"] is context
    assert client_cls.call_args.kwargs["headers"] == {"User-Agent": "Runlayer CLI"}


def test_async_http_client_preserves_mcp_default_timeout():
    from mcp.shared._httpx_utils import (
        MCP_DEFAULT_SSE_READ_TIMEOUT,
        MCP_DEFAULT_TIMEOUT,
    )

    with (
        patch("runlayer_cli.tls.build_verify"),
        patch("runlayer_cli.tls.httpx.AsyncClient") as client_cls,
    ):
        tls.async_http_client()

    timeout = client_cls.call_args.kwargs["timeout"]
    assert timeout.connect == MCP_DEFAULT_TIMEOUT
    assert timeout.read == MCP_DEFAULT_SSE_READ_TIMEOUT


def test_async_http_client_uses_explicit_timeout():
    explicit_timeout = httpx.Timeout(10.0, read=20.0)

    with (
        patch("runlayer_cli.tls.build_verify"),
        patch("runlayer_cli.tls.httpx.AsyncClient") as client_cls,
    ):
        tls.async_http_client(timeout=explicit_timeout)

    assert client_cls.call_args.kwargs["timeout"] is explicit_timeout


def test_http_client_trusts_private_ca_bundle(monkeypatch, tmp_path):
    ca_path, cert_path, key_path = _write_private_ca_server_certs(tmp_path)
    monkeypatch.delenv("RUNLAYER_CA_BUNDLE", raising=False)
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)
    monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

    with _https_server(cert_path, key_path) as url:
        with pytest.raises(httpx.ConnectError):
            with tls.http_client(timeout=2, trust_env=False) as client:
                client.get(url)

        monkeypatch.setenv("RUNLAYER_CA_BUNDLE", str(ca_path))
        with tls.http_client(timeout=2, trust_env=False) as client:
            response = client.get(url)

    assert response.json() == {"ok": True}
