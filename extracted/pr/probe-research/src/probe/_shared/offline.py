"""Is this machine offline? Only when it had no network at all: the name did not
resolve, or the network or host was unreachable.

A refused or reset connection, a timeout, a TLS failure (a proxy that re-signs
it) or a reply that is not what was asked for is NOT offline: the network
answered, so whatever failed may be ours, and the watch still reports it
(2026-10-24 review: counting every no-HTTP-answer as offline hid a broken
corporate proxy and a server that hangs). What reads as offline here never
reaches the Probe team anyway: a report needs the same network.

`no_network(exc)` walks an error and what it was raised from; `no_network_text`
reads the one-line text a store kept of one (the tap journal's `http 0: ...`).
A text in another language reads as not offline, so it is reported.

Stdlib only (the service's start path).
"""

from __future__ import annotations

import errno
import re
import socket

_UNREACHABLE = frozenset(
    code for code in (getattr(errno, name, None) for name in (
        "ENETDOWN", "ENETUNREACH", "EHOSTDOWN", "EHOSTUNREACH",
        "WSAENETDOWN", "WSAENETUNREACH", "WSAEHOSTDOWN", "WSAEHOSTUNREACH"))
    if code is not None
)
#: The same failures as their system text: DNS on macOS, Linux and Windows,
#: then the unreachable network or host.
_NO_NETWORK_TEXT = re.compile(
    r"\bhttp 0:.*(?:"
    r"nodename nor servname provided|Name or service not known|Temporary failure in name resolution"
    r"|No address associated with hostname|getaddrinfo failed"
    r"|Network is unreachable|Network is down|No route to host|Host is down|host is unreachable"
    r"|unreachable network|unreachable host)",
    re.IGNORECASE,
)
_DEPTH = 8


def _group(exc: BaseException) -> bool:
    """An exception group: the builtin (3.11+) or the `exceptiongroup` backport
    anyio raises on 3.10 -- never any error that merely has `.exceptions`."""
    return any(cls.__name__ in ("BaseExceptionGroup", "ExceptionGroup") for cls in type(exc).__mro__)


def no_network(exc: BaseException | None, _depth: int = 0) -> bool:
    """`exc`, or an error it was raised from, is a name that did not resolve or
    an unreachable network or host."""
    seen = _depth
    while exc is not None and seen < _DEPTH:
        if isinstance(exc, socket.gaierror):
            return True
        members = getattr(exc, "exceptions", None) if _group(exc) else None
        if isinstance(members, (list, tuple)) and members:
            # anyio's every address tried: all of them had no network.
            return all(no_network(m, seen + 1) for m in members)
        reason = getattr(exc, "reason", None)
        if isinstance(reason, BaseException):
            exc = reason  # urllib's URLError keeps it here, not in __cause__
        elif isinstance(exc, OSError) and exc.errno is not None:
            # The socket error itself decides. Past it is only an earlier
            # attempt's error that a client's retry was raised while handling.
            return exc.errno in _UNREACHABLE
        else:
            # httpcore's pool re-raises its ConnectError `from None`, leaving the
            # socket error only as __context__ (the daemon's real chain); anyio's
            # "All connection attempts failed" (no errno) raises from its attempts.
            exc = exc.__cause__ or exc.__context__
        seen += 1
    return False


def no_network_text(text: object) -> bool:
    """The kept text of an error with no HTTP answer (`http 0: ...`) says no
    network (see `no_network`); an HTTP answer's text never does."""
    return isinstance(text, str) and _NO_NETWORK_TEXT.search(text) is not None
