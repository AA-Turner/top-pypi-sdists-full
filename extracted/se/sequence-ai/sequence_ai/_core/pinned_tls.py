"""
The worker's certificate checked by the sha256 fingerprint the gateway pinned for it, not by a CA: the fingerprint
normalized fail-closed, and the SSLContext that refuses any other certificate on the worker's address - a connection
opened inside another TLS connection (through an HTTPS proxy) included. Stdlib `ssl` + `hashlib` only (no
`cryptography`, no `certifi`).

WHY its own module: direct.py had grown to 1966 lines, past the ~1500 a file may have
 
; how a worker's certificate is checked is one responsibility, the connection that uses it another.
"""

from __future__ import annotations

import hashlib
import hmac
import ssl
from typing import Any, Optional

from ..errors import CertPinError





_HEX = frozenset("0123456789abcdef")


def _sha256_hex(der: bytes) -> str:
    """The pinned-fingerprint algorithm, in one place so both ends compute it identically."""
    return hashlib.sha256(der).hexdigest()


def normalize_fingerprint(fingerprint: Optional[str]) -> str:
    """
    Return a bare lowercase sha256 hex digest, or raise — fail-closed.

    A pin the SDK cannot read is a pin it cannot enforce, and the safe answer to "I was given no
    usable fingerprint" is to refuse the connection, never to fall back to default-CA trust or
    `verify=False`. Empty, None, or anything that is not 64 hex characters (with optional colons
    or spaces, as `openssl x509 -fingerprint` prints them) is rejected here, before any socket
    is opened.
    """
    if not isinstance(fingerprint, str):
        raise CertPinError("no cert fingerprint to pin; refusing to connect")
    cleaned = fingerprint.strip().replace(":", "").replace(" ", "").lower()
    if len(cleaned) != 64 or any(c not in _HEX for c in cleaned):
        raise CertPinError("cert fingerprint is not a valid sha256 hex digest; refusing to connect")
    return cleaned


class _PinnedSSLObject(ssl.SSLObject):
    """
    The pin, for a connection opened inside another TLS connection - through an HTTPS proxy, which httpcore wraps with
    `wrap_bio`, not `wrap_socket` - checked as soon as its handshake completes, as `_PinnedSSLContext.wrap_socket`
    checks a direct one. Without it such a connection ran with `CERT_NONE` and no pin at all: whoever ran the proxy
    could present any certificate and read the direct secret.
    """

    def do_handshake(self) -> None:
        super().do_handshake()
        der = self.getpeercert(binary_form=True)
        if not der:
            raise CertPinError("worker presented no certificate; refusing to connect")
        if not hmac.compare_digest(_sha256_hex(der), self.context._pinned_fp):
            raise CertPinError("worker certificate does not match the pinned fingerprint")


class _PinnedSSLContext(ssl.SSLContext):
    """
    An SSLContext that verifies the peer by a pinned sha256 fingerprint, not by a CA.

    The handshake runs with `CERT_NONE` because the worker's self-signed cert has no chain to
    validate; the real check happens right after, on the DER bytes the server actually
    presented. Doing it in `wrap_socket` rather than once at setup is what makes it hold for
    every connection the pool opens, not just the first — a second connection that skipped the
    check would be the hole the pin exists to close.
    """

    _pinned_fp = ""

    sslobject_class = _PinnedSSLObject

    def wrap_socket(self, sock: Any, *args: Any, **kwargs: Any) -> Any:
        ssl_sock = super().wrap_socket(sock, *args, **kwargs)
        try:
            der = ssl_sock.getpeercert(binary_form=True)
        except Exception as exc:
            try:
                ssl_sock.close()
            finally:
                raise CertPinError("could not read the worker certificate to pin it") from exc
        if not der:
            ssl_sock.close()
            raise CertPinError("worker presented no certificate; refusing to connect")
        presented = _sha256_hex(der)
        if not hmac.compare_digest(presented, self._pinned_fp):
            ssl_sock.close()


            raise CertPinError("worker certificate does not match the pinned fingerprint")
        return ssl_sock


def build_pinned_ssl_context(fingerprint: Optional[str]) -> ssl.SSLContext:
    """
    Build an SSLContext pinned to `fingerprint`, or raise CertPinError (fail-closed).

    `check_hostname` is turned off before `verify_mode`, because setting `CERT_NONE` while
    hostname checking is still on raises — and hostname checking is meaningless for a bare-IP
    self-signed worker anyway. The fingerprint pin is the entirety of the trust decision.
    """
    pinned = normalize_fingerprint(fingerprint)
    ctx = _PinnedSSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx._pinned_fp = pinned
    return ctx
