"""Sanitized exception -> flow error-category classification.

Maps a caught exception to a ``(error_category, http_status)`` pair from the
closed ``flow_contract.CLIENT_FLOW_ERROR_CATEGORIES`` vocabulary, so failed
flow summaries carry enough context to diagnose server-side (motivating
incident: hours of ``cli.list_tools`` failures ingested as bare
``error_type: RuntimeError`` — support had to keep asking the customer for
local log files).

This module deliberately lives OUTSIDE the ``flow_*`` stdlib-only import
closure (cli/AGENTS.md): it needs ``httpx`` / ``mcp`` / ``fastmcp`` types,
which are excluded from the ``aiwatch`` PyInstaller bundle. It is imported
only by the ``runlayer run`` path (``main.py`` / ``middleware.py``), which
injects :func:`classify_exception` into ``flow_trace`` via
``set_error_classifier``.

SANITIZATION CONTRACT: the return value is a category string from the closed
vocabulary plus an optional integer HTTP status. Exception messages, URLs,
response bodies, and tokens NEVER enter the result.
"""

from __future__ import annotations

import asyncio
import socket
import ssl
import sys
from collections.abc import Iterator

import httpx

if sys.version_info >= (3, 11):
    import builtins

    _ExceptionGroup = builtins.BaseExceptionGroup
else:  # pragma: no cover - py3.10 backport (dep of anyio)
    from exceptiongroup import BaseExceptionGroup as _ExceptionGroup
from fastmcp.exceptions import FastMCPError
from mcp.client.auth import OAuthFlowError, OAuthRegistrationError, OAuthTokenError
from mcp.shared.exceptions import McpError

from runlayer_cli import oauth_guidance
from runlayer_cli.oauth import OAuthCallbackTimeoutError

# Total exceptions visited across group members and __cause__/__context__
# links — bounds pathological graphs while comfortably covering real anyio /
# fastmcp nesting (a few groups deep, a few links long).
_MAX_TRAVERSED_EXCEPTIONS = 32


def _iter_tree(exc: BaseException) -> Iterator[BaseException]:
    """Yield every non-group exception reachable from ``exc``, wrapper-first.

    Uniform traversal: ExceptionGroups are unwrapped into their member leaves
    and ``__cause__``/``__context__`` links are followed at ANY depth — a
    group can sit behind a cause (e.g. RuntimeError raised from an anyio task
    group's ExceptionGroup of transport errors) and a cause can sit behind a
    group member. Breadth-first, so wrappers classify before the exceptions
    they wrap; bounded and cycle-safe (visited set) against pathological
    graphs.
    """
    seen: set[int] = set()
    queue: list[BaseException] = [exc]
    visited = 0
    while queue and visited < _MAX_TRAVERSED_EXCEPTIONS:
        current = queue.pop(0)
        if id(current) in seen:
            continue
        seen.add(id(current))
        visited += 1
        links: list[BaseException] = []
        if isinstance(current, _ExceptionGroup):
            # The members are the real failures; the group itself is wrapping.
            links.extend(current.exceptions)
        else:
            yield current
        for link in (current.__cause__, current.__context__):
            if link is not None:
                links.append(link)
        queue.extend(link for link in links if id(link) not in seen)


def _status_category(status_code: int) -> str:
    if status_code == 401:
        return "http_401"
    if status_code == 403:
        return "http_403"
    if status_code == 404:
        return "http_404"
    if 400 <= status_code < 500:
        return "http_4xx"
    if 500 <= status_code < 600:
        return "http_5xx"
    return "other"


def _classify_single(exc: BaseException) -> tuple[str, int | None]:
    """Classify exactly one exception object (no chain or group walking)."""
    # OAuth first: these subclass generic errors (OAuthCallbackTimeoutError is
    # a TimeoutError) and the OAuth-specific category is the diagnostic one.
    if isinstance(exc, OAuthRegistrationError):
        # Only a 4xx is a *rejection* (configuration problem, Manual OAuth is
        # the fix — mirroring oauth_guidance/OAuth.async_auth_flow, which pass
        # 5xx through as likely-transient). 5xx classifies by status; a
        # message without the SDK's status shape stays "other" — the cause
        # chain may still surface the underlying HTTP error.
        status_code = oauth_guidance.registration_failure_status(str(exc))
        if status_code is None:
            return ("other", None)
        if 400 <= status_code < 500:
            return ("oauth_registration_rejected", status_code)
        return (_status_category(status_code), status_code)
    if isinstance(exc, OAuthCallbackTimeoutError):
        return ("oauth_flow_timeout", None)
    if isinstance(exc, OAuthFlowError | OAuthTokenError):
        return ("other", None)

    if isinstance(exc, httpx.HTTPStatusError):
        status_code = exc.response.status_code
        return (_status_category(status_code), status_code)

    if isinstance(exc, httpx.ConnectTimeout):
        return ("connect_timeout", None)
    if isinstance(exc, httpx.TimeoutException):
        return ("timeout", None)

    if isinstance(exc, socket.gaierror):
        return ("dns", None)
    if isinstance(exc, ssl.SSLError):
        return ("tls", None)

    if isinstance(exc, httpx.ConnectError | ConnectionError):
        return ("connect", None)
    if isinstance(exc, httpx.TransportError):
        # Remaining transport failures (ReadError, RemoteProtocolError, ...):
        # the upstream went away mid-exchange.
        return ("connect", None)
    if isinstance(exc, TimeoutError):
        return ("timeout", None)

    if isinstance(exc, McpError | FastMCPError):
        return ("mcp_protocol", None)

    # The CLI runs anyio on the asyncio backend only, so asyncio.CancelledError
    # is the cancellation class (anyio.get_cancelled_exc_class() needs a
    # running loop and this classifier must work from sync call sites too).
    if isinstance(exc, asyncio.CancelledError):
        return ("cancelled", None)

    return ("other", None)


def classify_exception(exc: BaseException) -> tuple[str, int | None]:
    """Classify ``exc`` into ``(error_category, http_status)``.

    Uniformly traverses (nested) ExceptionGroups and
    ``__cause__``/``__context__`` chains in any combination (``_iter_tree``).
    First pass scans every reachable exception for the OS-level root causes
    (DNS resolution, TLS handshake) — they carry the most diagnostic signal
    and would otherwise be shadowed by the generic ``connect`` of an
    httpx.ConnectError wrapper. Second pass runs the full classification
    wrapper-first, so e.g. a RuntimeError raised ``from`` an
    httpx.HTTPStatusError still classifies as ``http_*`` (and an
    OAuthRegistrationError wrapping an HTTP 403 keeps the more specific OAuth
    category). Always returns a category from
    ``CLIENT_FLOW_ERROR_CATEGORIES`` — the fallback is ``("other", None)``.
    Never raises and never includes message text.
    """
    try:
        nodes = list(_iter_tree(exc))
        for node in nodes:
            if isinstance(node, socket.gaierror):
                return ("dns", None)
            if isinstance(node, ssl.SSLError):
                return ("tls", None)
        result: tuple[str, int | None] = ("other", None)
        for node in nodes:
            category, http_status = _classify_single(node)
            if category != "other":
                return (category, http_status)
            if http_status is not None and result[1] is None:
                # "other" with a status (e.g. an unexpected HTTP 3xx): keep
                # the status as a fallback while scanning for something more
                # specific.
                result = (category, http_status)
        return result
    except Exception:
        return ("other", None)
