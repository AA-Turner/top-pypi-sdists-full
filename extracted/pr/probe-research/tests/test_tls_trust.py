"""TLS trust: one CA decision for every connection the agent opens (plan item (l), D21).

Before `probe.sdk.tls`, httpx (every SDK write) trusted SSL_CERT_FILE/SSL_CERT_DIR
else certifi, and urllib (telemetry) trusted the OS store. Behind a TLS-re-signing
proxy, telemetry reported a healthy SDK while every write failed verification, and
REQUESTS_CA_BUNDLE -- the variable the researcher had already set -- did nothing.

The end-to-end tests here stand up a real HTTPS server whose certificate is signed
by a CA generated in the test, so they prove the handshake, not a mock of it.
"""

from __future__ import annotations

import ast
import datetime
import http.server
import ipaddress
import json
import os
import shutil
import signal
import ssl
import subprocess
import threading
import time
import urllib.error
import warnings
from pathlib import Path

import certifi
import httpx
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

from probe.cli import telemetry as cli_telemetry
from probe.sdk import _telemetry_core as core
from probe.sdk import errors, tls
from probe.sdk.config import Settings
from probe.sdk.transport import Transport

_SRC = Path(__file__).resolve().parent.parent / "src" / "probe"


# -- fixtures ------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clean_trust(monkeypatch):
    """No ambient bundle variable, no cached context, no remembered warning."""
    for name in ("SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(tls, "_cached", None)
    monkeypatch.setattr(tls, "_warned", set())


def _name(common_name: str) -> x509.Name:
    return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])


def _write_pem(path: Path, cert: x509.Certificate) -> Path:
    path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    return path


class _CA:
    """A root CA with the extensions Python 3.13's VERIFY_X509_STRICT demands."""

    def __init__(self, common_name: str):
        self.key = ec.generate_private_key(ec.SECP256R1())
        now = datetime.datetime.now(datetime.timezone.utc)
        ski = x509.SubjectKeyIdentifier.from_public_key(self.key.public_key())
        self.cert = (
            x509.CertificateBuilder()
            .subject_name(_name(common_name))
            .issuer_name(_name(common_name))
            .public_key(self.key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(minutes=5))
            .not_valid_after(now + datetime.timedelta(days=1))
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True, content_commitment=False, key_encipherment=False,
                    data_encipherment=False, key_agreement=False, key_cert_sign=True,
                    crl_sign=True, encipher_only=False, decipher_only=False,
                ),
                critical=True,
            )
            .add_extension(ski, critical=False)
            .sign(self.key, hashes.SHA256())
        )
        self.common_name = common_name

    def issue_server(self, directory: Path) -> tuple[Path, Path]:
        """A leaf for 127.0.0.1 / localhost; returns (cert chain path, key path)."""
        key = ec.generate_private_key(ec.SECP256R1())
        now = datetime.datetime.now(datetime.timezone.utc)
        ca_ski = self.cert.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value
        cert = (
            x509.CertificateBuilder()
            .subject_name(_name("probe-tls-test-server"))
            .issuer_name(self.cert.subject)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(minutes=5))
            .not_valid_after(now + datetime.timedelta(days=1))
            .add_extension(
                x509.SubjectAlternativeName(
                    [x509.DNSName("localhost"), x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]
                ),
                critical=False,
            )
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True, content_commitment=False, key_encipherment=False,
                    data_encipherment=False, key_agreement=False, key_cert_sign=False,
                    crl_sign=False, encipher_only=False, decipher_only=False,
                ),
                critical=True,
            )
            .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
            .add_extension(
                x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(ca_ski),
                critical=False,
            )
            .add_extension(
                x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False
            )
            .sign(self.key, hashes.SHA256())
        )
        cert_path = _write_pem(directory / "server.pem", cert)
        key_path = directory / "server.key"
        key_path.write_bytes(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        )
        return cert_path, key_path


@pytest.fixture()
def bundles(tmp_path):
    """Three distinct CA bundles, so which one a context loaded is observable."""
    out = {}
    for label in ("ssl_cert_file", "requests", "curl"):
        ca = _CA(f"probe-test-ca-{label}")
        out[label] = (_write_pem(tmp_path / f"{label}.pem", ca.cert), ca.common_name)
    return out


class _Handler(http.server.BaseHTTPRequestHandler):
    received: list[tuple[str, str]] = []

    def _answer(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        type(self).received.append((self.command, self.path))
        body = json.dumps({"ok": True, "user_id": "u-1"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_GET = _answer
    do_POST = _answer

    def log_message(self, *args) -> None:  # keep test output clean
        pass


@pytest.fixture()
def https_server(tmp_path):
    """A real HTTPS server on 127.0.0.1 signed by a CA made for this test only."""
    ca = _CA("probe-test-proxy-ca")
    ca_path = _write_pem(tmp_path / "proxy-ca.pem", ca.cert)
    cert_path, key_path = ca.issue_server(tmp_path)
    server_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    server_ctx.load_cert_chain(cert_path, key_path)

    class Handler(_Handler):
        received: list[tuple[str, str]] = []

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.socket = server_ctx.wrap_socket(server.socket, server_side=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield {
            "url": f"https://127.0.0.1:{server.server_address[1]}",
            "ca": ca,
            "ca_path": ca_path,
            "received": Handler.received,
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _subjects(context: ssl.SSLContext) -> set[str]:
    names = set()
    for cert in context.get_ca_certs():
        for rdn in cert.get("subject", ()):
            for key, value in rdn:
                if key == "commonName":
                    names.add(value)
    return names


def _certifi_count() -> int:
    return ssl.create_default_context(cafile=certifi.where()).cert_store_stats()["x509_ca"]


def _hashed_dir(directory: Path, *pems: Path) -> Path:
    """An OpenSSL `capath`: each CA under its subject hash, as `c_rehash` lays it out."""
    directory.mkdir()
    for pem in pems:
        subject_hash = subprocess.run(
            ["openssl", "x509", "-noout", "-subject_hash", "-in", str(pem)],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        shutil.copy(pem, directory / f"{subject_hash}.0")
    return directory


def _builtin_paths(monkeypatch, *, cafile: object = None, capath: object = None) -> None:
    """Stand-ins for OpenSSL's compiled-in locations, so a test controls the 'OS store'."""
    real = ssl.get_default_verify_paths()
    fake = real._replace(
        openssl_cafile=str(cafile) if cafile else None,
        openssl_capath=str(capath) if capath else None,
    )
    monkeypatch.setattr(tls.ssl, "get_default_verify_paths", lambda: fake)


def _handshake(url: str) -> None:
    with httpx.Client(verify=tls.ssl_context()) as client:
        assert client.get(url + "/probe").status_code == 200


needs_openssl = pytest.mark.skipif(
    shutil.which("openssl") is None, reason="needs `openssl` to hash a CA dir"
)


# -- precedence ----------------------------------------------------------------


def test_ssl_cert_file_replaces_the_defaults_and_outranks_the_bundles(monkeypatch, bundles):
    monkeypatch.setenv("SSL_CERT_FILE", str(bundles["ssl_cert_file"][0]))
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(bundles["requests"][0]))
    monkeypatch.setenv("CURL_CA_BUNDLE", str(bundles["curl"][0]))

    context = tls.ssl_context()

    # OpenSSL's own variable REPLACES the defaults, as httpx always read it: exactly
    # that bundle, none of certifi's ~150 roots, and neither lower tier.
    assert _subjects(context) == {bundles["ssl_cert_file"][1]}
    assert context.cert_store_stats()["x509_ca"] == 1
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname


@pytest.mark.parametrize(
    ("set_vars", "added", "absent"),
    [
        (("REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"), "requests", "curl"),
        (("CURL_CA_BUNDLE",), "curl", "requests"),
    ],
)
def test_requests_and_curl_bundles_are_added_to_the_defaults(
    monkeypatch, bundles, set_vars, added, absent
):
    by_var = {"REQUESTS_CA_BUNDLE": "requests", "CURL_CA_BUNDLE": "curl"}
    for var in set_vars:
        monkeypatch.setenv(var, str(bundles[by_var[var]][0]))

    context = tls.ssl_context()

    subjects = _subjects(context)
    assert bundles[added][1] in subjects
    assert bundles[absent][1] not in subjects  # REQUESTS_CA_BUNDLE outranks CURL_CA_BUNDLE
    # ON TOP of the defaults, never instead of them: certifi's roots are all still here.
    assert context.cert_store_stats()["x509_ca"] >= _certifi_count() + 1
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname


@pytest.mark.parametrize("variable", ["REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"])
def test_a_bundle_set_for_another_tool_never_costs_probe_its_public_roots(
    monkeypatch, bundles, https_server, variable
):
    """The regression the replace rule caused: a shell profile exporting a bundle with
    ONE unrelated internal root made every Probe connection fail, where the release
    before connected fine. The test server's CA stands in for the public roots
    (certifi), so this is a real handshake with no call leaving the machine."""
    monkeypatch.setattr(certifi, "where", lambda: str(https_server["ca_path"]))
    _handshake(https_server["url"])  # control: the 'public' root verifies

    monkeypatch.setenv(variable, str(bundles["requests"][0]))  # one unrelated root
    _handshake(https_server["url"])
    assert bundles["requests"][1] in _subjects(tls.ssl_context())


@needs_openssl
def test_ssl_cert_file_alone_keeps_the_builtin_certificate_folder(
    monkeypatch, bundles, https_server, tmp_path
):
    """`set_default_verify_paths` semantics: a variable replaces only ITS half of the
    pair. urllib on main kept OpenSSL's built-in folder under SSL_CERT_FILE alone."""
    folder = _hashed_dir(tmp_path / "builtin-certs", https_server["ca_path"])
    _builtin_paths(monkeypatch, capath=folder)
    monkeypatch.setenv("SSL_CERT_FILE", str(bundles["ssl_cert_file"][0]))  # unrelated root

    _handshake(https_server["url"])  # verified through the built-in folder

    # Control: with SSL_CERT_DIR set too, the pair replaces both halves.
    empty = tmp_path / "empty-certs"
    empty.mkdir()
    monkeypatch.setenv("SSL_CERT_DIR", str(empty))
    with pytest.raises(httpx.ConnectError, match="CERTIFICATE_VERIFY_FAILED"):
        _handshake(https_server["url"])


def test_ssl_cert_dir_alone_keeps_the_builtin_certificate_file(monkeypatch, bundles, tmp_path):
    builtin_file, builtin_cn = bundles["curl"]  # stands in for the OS's built-in file
    _builtin_paths(monkeypatch, cafile=builtin_file)
    empty = tmp_path / "certs.d"
    empty.mkdir()
    monkeypatch.setenv("SSL_CERT_DIR", str(empty))
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(bundles["requests"][0]))

    context = tls.ssl_context()

    # The built-in file, and REQUESTS_CA_BUNDLE never consulted: tier 1 was usable.
    assert _subjects(context) == {builtin_cn}


def test_no_variable_means_os_defaults_plus_certifi(monkeypatch):
    context = tls.ssl_context()
    assert context.cert_store_stats()["x509_ca"] >= _certifi_count()
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname


def test_the_context_is_built_once_per_process_and_rebuilt_when_a_variable_moves(
    monkeypatch, bundles
):
    first = tls.ssl_context()
    assert tls.ssl_context() is first
    monkeypatch.setenv("CURL_CA_BUNDLE", str(bundles["curl"][0]))
    moved = tls.ssl_context()
    assert moved is not first
    assert bundles["curl"][1] in _subjects(moved)


# -- an unusable path warns once, falls back, never raises -----------------------


def test_a_missing_path_warns_once_and_falls_to_the_next_tier(monkeypatch, bundles, tmp_path):
    missing = str(tmp_path / "nope.pem")
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", missing)
    monkeypatch.setenv("CURL_CA_BUNDLE", str(bundles["curl"][0]))

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        context = tls.ssl_context()
        tls.ssl_context()  # cached: no second warning
        monkeypatch.setattr(tls, "_cached", None)
        tls.ssl_context()  # rebuilt: still no second warning for the same path

    messages = [str(w.message) for w in caught]
    assert len(messages) == 1, messages
    assert "REQUESTS_CA_BUNDLE" in messages[0] and missing in messages[0]
    assert "Restart the process" in messages[0]  # the file is read once per process
    assert bundles["curl"][1] in _subjects(context)


def test_warnings_are_emitted_after_the_lock_is_released(monkeypatch, tmp_path):
    """A warnings hook that builds a client of its own must not deadlock on the lock."""
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(tmp_path / "missing.pem"))
    held: list[bool] = []

    def hook(message, category, filename, lineno, file=None, line=None):
        held.append(tls._lock.locked())

    with warnings.catch_warnings():
        warnings.simplefilter("always")
        warnings.showwarning = hook
        tls.ssl_context()
    assert held == [False]


def test_a_file_holding_no_certificate_warns_and_falls_back_to_the_defaults(
    monkeypatch, tmp_path
):
    garbage = tmp_path / "not-a-bundle.pem"
    garbage.write_text("this is not a certificate\n")
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(garbage))

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        context = tls.ssl_context()

    assert len(caught) == 1 and "no usable certificate" in str(caught[0].message)
    assert context.cert_store_stats()["x509_ca"] >= _certifi_count()


def test_bad_paths_never_raise_even_when_warnings_are_errors(monkeypatch, tmp_path):
    for name in ("SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"):
        monkeypatch.setenv(name, str(tmp_path / f"missing-{name}"))
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # what `-W error` harnesses do
        context = tls.ssl_context()
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.cert_store_stats()["x509_ca"] >= _certifi_count()


def test_a_typod_ssl_cert_file_does_not_empty_the_os_store(monkeypatch, bundles, tmp_path):
    """OpenSSL's default loader reads SSL_CERT_FILE itself, IN PLACE of its compiled
    path. So a missing SSL_CERT_FILE would silently drop the OS bundle from the
    fallback unless the compiled path is loaded by name."""
    os_bundle, os_cn = bundles["curl"]  # stands in for the OS's compiled cafile
    _builtin_paths(monkeypatch, cafile=os_bundle)
    monkeypatch.setenv("SSL_CERT_FILE", str(tmp_path / "typo.pem"))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        context = tls.ssl_context()
    assert os_cn in _subjects(context)
    assert context.cert_store_stats()["x509_ca"] >= _certifi_count()


@pytest.mark.skipif(not hasattr(os, "fork"), reason="POSIX fork only")
def test_a_fork_while_the_context_is_being_built_does_not_hang_the_child():
    """A DataLoader worker forked mid-build inherits a HELD lock; its first client
    would wait on it forever unless the child gets a fresh one."""
    tls._lock.acquire()  # stands in for another thread mid-build at fork time
    try:
        pid = os.fork()
        if pid == 0:  # child: never return into pytest
            try:
                tls.ssl_context()
                os._exit(0)
            except BaseException:  # noqa: BLE001
                os._exit(1)
    finally:
        tls._lock.release()
    deadline = time.monotonic() + 10
    while True:
        done, status = os.waitpid(pid, os.WNOHANG)
        if done:
            break
        if time.monotonic() > deadline:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
            pytest.fail("the forked child hung on the inherited TLS lock")
        time.sleep(0.05)
    assert os.waitstatus_to_exitcode(status) == 0


# -- the real handshake ------------------------------------------------------------


def test_transport_uses_the_shared_context():
    transport = Transport(Settings(base_url="https://127.0.0.1:9", token="t"), max_retries=0)
    try:
        pool = transport._client._transport._pool  # httpx -> httpcore pool
        assert pool._ssl_context is tls.ssl_context()
    finally:
        transport.close()


def test_a_private_ca_fails_without_the_bundle_and_works_with_requests_ca_bundle(
    monkeypatch, https_server
):
    settings = Settings(base_url=https_server["url"], token="probe_pat_test")

    # Negative control: the server's CA is in no default store.
    with Transport(settings, max_retries=0) as transport:
        with pytest.raises(errors.TransportError) as refused:
            transport.get("/v1/me")
    assert "CERTIFICATE_VERIFY_FAILED" in repr(refused.value.__cause__)

    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(https_server["ca_path"]))
    with Transport(settings, max_retries=0) as transport:
        assert transport.get("/v1/me") == {"ok": True, "user_id": "u-1"}
    assert ("GET", "/v1/me") in https_server["received"]


@needs_openssl
def test_a_bundle_directory_is_used_as_capath(monkeypatch, https_server, tmp_path):
    monkeypatch.setenv(
        "REQUESTS_CA_BUNDLE", str(_hashed_dir(tmp_path / "ca.d", https_server["ca_path"]))
    )
    _handshake(https_server["url"])


def test_the_urllib_telemetry_path_uses_the_same_trust(monkeypatch, https_server):
    """Telemetry and SDK writes must agree about a proxy's certificate."""
    monkeypatch.setattr(core, "POSTHOG_HOST", https_server["url"])
    batch = [{"event": "tls.test", "distinct_id": "d", "properties": {}}]

    # Negative control: urllib's own default store refuses the private CA.
    with pytest.raises(urllib.error.URLError) as refused:
        core.post_batch(batch)
    assert isinstance(refused.value.reason, ssl.SSLCertVerificationError)

    # The CLI's sender path, with the bundle set, goes through.
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(https_server["ca_path"]))
    cli_telemetry._post_batch(batch)
    assert ("POST", "/batch/") in https_server["received"]


def test_resolve_identity_hands_its_context_to_urlopen(monkeypatch):
    seen: list[object] = []

    def fake_urlopen(req, timeout=None, context=None):
        seen.append(context)
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(core.urllib.request, "urlopen", fake_urlopen)
    shared = tls.ssl_context()
    core.resolve_identity({"token": "tok", "base_url": core.DEFAULT_BASE}, context=shared)
    assert seen == [shared]


# -- every client in the package takes the shared trust ------------------------------

#: httpx entry points that open connections. A new one belongs here.
_HTTPX_CALLS = {"Client", "AsyncClient", "get", "post", "put", "patch", "delete", "head",
                "request", "stream", "options"}


def _call_name(node: ast.Call) -> tuple[str | None, str | None]:
    func = node.func
    if isinstance(func, ast.Attribute):
        owner = func.value
        owner_name = owner.id if isinstance(owner, ast.Name) else (
            owner.attr if isinstance(owner, ast.Attribute) else None
        )
        return owner_name, func.attr
    if isinstance(func, ast.Name):
        return None, func.id
    return None, None


def _violations(tree: ast.AST, rel: str) -> list[str]:
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        owner, name = _call_name(node)
        keywords = {kw.arg for kw in node.keywords}
        where = f"{rel}:{node.lineno}"
        if owner == "httpx" and name in _HTTPX_CALLS and "verify" not in keywords:
            found.append(f"{where} httpx.{name}(...) without verify=")
        # The context is shared, and httpcore writes each connection's ALPN list
        # onto it: an HTTP/2 client would rewrite it under every HTTP/1.1 one.
        if owner == "httpx" and "http2" in keywords:
            found.append(f"{where} httpx.{name}(http2=...) on the shared TLS context")
        # urllib, and the vendored stdlib-only helpers that forward a context
        # to it (they cannot import probe.sdk.tls; their CLI callers pass it).
        forwards = (
            name == "urlopen"
            or (owner == "core" and name in {"resolve_identity", "post_batch"})
            or (owner == "version_policy" and name in {"fetch", "refresh"})
            or (owner is None and name == "Wire")
        )
        if forwards and "context" not in keywords:
            found.append(f"{where} {name}(...) without context=")
    return found


def test_every_client_in_the_package_is_handed_the_shared_trust():
    missing: list[str] = []
    for path in sorted(_SRC.rglob("*.py")):
        rel = path.relative_to(_SRC).as_posix()
        missing += _violations(ast.parse(path.read_text(encoding="utf-8")), rel)
    assert not missing, (
        "every connection must use probe.sdk.tls.ssl_context() (plan item (l)):\n  "
        + "\n  ".join(missing)
    )


def test_the_guard_catches_what_it_is_for():
    """Negative control: the guard above is only evidence if it can fail."""
    snippet = (
        "import httpx, urllib.request\n"
        "httpx.Client(base_url='x')\n"
        "httpx.AsyncClient(verify=ctx, http2=True)\n"
        "urllib.request.urlopen(req, timeout=1)\n"
        "version_policy.refresh()\n"
        "Wire(base, token, source)\n"
        "httpx.Client(verify=ctx)\n"
        "urllib.request.urlopen(req, context=ctx)\n"
    )
    found = _violations(ast.parse(snippet), "snippet.py")
    assert found == [
        "snippet.py:2 httpx.Client(...) without verify=",
        "snippet.py:3 httpx.AsyncClient(http2=...) on the shared TLS context",
        "snippet.py:4 urlopen(...) without context=",
        "snippet.py:5 refresh(...) without context=",
        "snippet.py:6 Wire(...) without context=",
    ], found


def test_the_shared_module_is_stdlib_only():
    """Enqueue paths and urllib callers import it without an HTTP client."""
    tree = ast.parse((_SRC / "sdk" / "tls.py").read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    assert imported <= {"__future__", "os", "ssl", "threading", "certifi"}, imported
    assert os.path.basename(certifi.where()).endswith(".pem")
