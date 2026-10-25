"""`probe._shared.offline`: no network at all, never a failure that answered.

2026-10-24 review: counting every connection that got no HTTP answer as
"offline" hid a corporate proxy re-signing TLS and a server hanging past the
client's timeout from the Probe team. Only a name that did not resolve or an
unreachable network or host is the laptop's."""

from __future__ import annotations

import builtins
import errno
import os
import socket
import ssl
import urllib.error

import pytest

from probe._shared import offline


def _from(exc: BaseException, cause: BaseException) -> BaseException:
    exc.__cause__ = cause
    return exc


def _daemon_chain(root: BaseException) -> BaseException:
    """The daemon's real chain, raised the way the libraries raise it (review:
    hand-set causes passed while the real path never matched): httpcore maps
    the socket error `from` it, its pool re-raises that `from None` (the socket
    error left only as __context__), then httpx, openai and pydantic_ai each
    raise their own `from` the one before."""
    class HttpcoreConnectError(Exception): ...
    class HttpxConnectError(Exception): ...
    class ModelAPIError(Exception): ...

    try:
        try:
            try:
                try:
                    raise root
                except OSError as exc:
                    raise HttpcoreConnectError(str(exc)) from exc
            except HttpcoreConnectError as exc:
                raise exc from None
        except HttpcoreConnectError as exc:
            raise HttpxConnectError(str(exc)) from exc
    except HttpxConnectError as exc:
        try:
            raise ModelAPIError("Connection error.") from exc
        except ModelAPIError as model:
            return model


@pytest.mark.parametrize("exc, expected", [
    (urllib.error.URLError(socket.gaierror(8, "nodename nor servname provided, or not known")), True),
    (urllib.error.URLError(OSError(errno.ENETUNREACH, "Network is unreachable")), True),
    (_from(RuntimeError("Connection error."), OSError(errno.EHOSTUNREACH, "No route to host")), True),
    (_from(RuntimeError("Connection error."), _from(OSError("connect"), socket.gaierror(-2, "Name or service not known"))),
     True),
    (urllib.error.URLError(ConnectionRefusedError(errno.ECONNREFUSED, "Connection refused")), False),
    (ConnectionResetError(errno.ECONNRESET, "Connection reset by peer"), False),
    (TimeoutError("timed out"), False),
    (urllib.error.URLError(ssl.SSLCertVerificationError(1, "CERTIFICATE_VERIFY_FAILED")), False),
    (ValueError("not a manifest"), False),
    (None, False),
], ids=["dns", "net-unreachable", "host-unreachable-cause", "dns-deep", "refused", "reset", "timeout", "tls",
        "bad-body", "none"])
def test_only_no_network_at_all_is_offline(exc, expected):
    assert offline.no_network(exc) is expected


@pytest.mark.parametrize("root, expected", [
    (socket.gaierror(8, "nodename nor servname provided, or not known"), True),
    (OSError(errno.ENETUNREACH, "Network is unreachable"), True),
    (ConnectionRefusedError(errno.ECONNREFUSED, "Connection refused"), False),
], ids=["dns", "net-unreachable", "refused"])
def test_the_daemon_s_real_chain_reaches_its_socket_error(root, expected):
    chained = _daemon_chain(root)
    assert chained.__cause__ is not None and offline.no_network(chained) is expected


def test_a_retry_s_refused_connection_is_not_its_earlier_attempt_s_dns_failure():
    """A client retries inside its `except`, so attempt 2's refused connection
    carries attempt 1's DNS failure as __context__: the refusal decides."""
    try:
        try:
            raise socket.gaierror(8, "nodename nor servname provided")
        except OSError:
            raise ConnectionRefusedError(errno.ECONNREFUSED, "Connection refused")
    except ConnectionRefusedError as refused:
        assert refused.__context__ is not None and offline.no_network(refused) is False


@pytest.mark.parametrize("attempts, expected", [
    ([errno.ENETUNREACH], True),
    ([errno.ENETUNREACH, errno.EHOSTUNREACH], True),
    ([errno.ENETUNREACH, errno.ECONNREFUSED], False),
], ids=["one-address", "all-unreachable", "one-refused"])
def test_anyio_s_all_attempts_failed_reads_its_attempts(attempts, expected):
    group = getattr(builtins, "ExceptionGroup", None)
    if group is None:
        pytest.skip("no builtin ExceptionGroup before Python 3.11")
    errors = [OSError(code, os.strerror(code)) for code in attempts]
    cause = errors[0] if len(errors) == 1 else group("multiple connection attempts failed", errors)
    try:
        raise OSError("All connection attempts failed") from cause
    except OSError as exc:
        assert offline.no_network(exc) is expected


@pytest.mark.parametrize("text, expected", [
    ("http 0: <urlopen error [Errno 8] nodename nor servname provided, or not known>", True),
    ("http 0: <urlopen error [Errno -2] Name or service not known>", True),
    ("http 0: <urlopen error [Errno -3] Temporary failure in name resolution>", True),
    ("http 0: <urlopen error [Errno 11001] getaddrinfo failed>", True),
    ("http 0: <urlopen error [Errno 51] Network is unreachable>", True),
    ("http 0: <urlopen error [Errno 65] No route to host>", True),
    ("http 0: <urlopen error [WinError 10051] A socket operation was attempted to an unreachable network>", True),
    ("http 0: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed>", False),
    ("http 0: <urlopen error timed out>", False),
    ("http 0: <urlopen error [Errno 61] Connection refused>", False),
    ("stream receipts unavailable (http 0); nothing newly staged", False),
    ("http 503: transcript delivery pending", False),
    # An HTTP answer is never offline, whatever its detail says (review).
    ("http 502: upstream: Temporary failure in name resolution", False),
    (None, False),
])
def test_a_kept_error_text_is_offline_only_for_no_network(text, expected):
    assert offline.no_network_text(text) is expected
