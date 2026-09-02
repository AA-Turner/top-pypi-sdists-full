"""`runlayer doctor` - read-only OAuth/connectivity preflight for MCP servers.

One command that runs the checks a customer would otherwise burn hours
discovering one at a time: unreachable upstream URL, RFC 8707 `resource`
mismatch (aborts our OAuth silently), IdPs that reject dynamic client
registration (e.g. Okta 403 E0000005) without a pre-registered manual
client, missing scopes, and OAuth callback-port mismatches against IdPs
with exact redirect-URI matching.

Read-only: no token minting, no browser flow, no client registration. The
only POST is the MCP `initialize` handshake mirror of
StreamableHttpTransport, needed because POST-only servers 405 the GET and
advertise their OAuth challenge on the protocol POST.

Heavy/async dependencies (`anyio`, `runlayer_cli.oauth` which imports
`mcp`) are imported lazily inside functions so importing this module stays
cheap and never drags `mcp`/`anyio` into unrelated closures.
"""

from __future__ import annotations

import json
import socket
import sys
from dataclasses import dataclass
from typing import Any, Callable, Literal, Optional
from urllib.parse import urljoin, urlparse, urlsplit, urlunsplit

import httpx
from pydantic import ValidationError
import typer

from runlayer_cli.api import USER_AGENT, RunlayerClient
from runlayer_cli.config import resolve_credentials, set_credentials_in_context
from runlayer_cli.models import ServerDetails
from runlayer_cli.uuid_utils import is_uuid

_HTTP_TIMEOUT_SECONDS = 10.0
# Auth methods that require a client secret at the token endpoint.
_CONFIDENTIAL_AUTH_METHODS = {"client_secret_post", "client_secret_basic"}

Status = Literal["ok", "warn", "fail", "skip"]


def _supports_unicode() -> bool:
    try:
        "✅⚠️❌➖".encode(sys.stdout.encoding or "ascii")
        return True
    except (UnicodeEncodeError, LookupError, AttributeError):
        return False


_UNICODE_ICONS: dict[Status, str] = {
    "ok": "✅",
    "warn": "⚠️",
    "fail": "❌",
    "skip": "➖",
}
_ASCII_ICONS: dict[Status, str] = {
    "ok": "[ok]",
    "warn": "[warn]",
    "fail": "[error]",
    "skip": "[skip]",
}

# Common punctuation in check text that an ASCII-only console can't encode.
_ASCII_PUNCTUATION = str.maketrans(
    {
        "—": "-",
        "–": "-",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "…": "...",
        "→": "->",
    }
)


def _to_ascii(text: str) -> str:
    """Best-effort ASCII rendering: map common punctuation, replace the rest."""
    return text.translate(_ASCII_PUNCTUATION).encode("ascii", "replace").decode("ascii")


@dataclass
class CheckResult:
    status: Status
    title: str
    detail: str
    remedy: str | None = None


def _sanitize_unparseable_url(url: str) -> str:
    """Textual fallback when ``urlsplit`` rejects the URL entirely.

    Never returns the raw input — a malformed URL (the very thing the
    malformed-URL diagnostic prints) can still embed userinfo and query
    secrets. Truncate at the first ``?``/``#``, strip any
    ``scheme://userinfo@`` segment, cap the length.
    """
    text = url
    for separator in ("?", "#"):
        pos = text.find(separator)
        if pos != -1:
            text = text[:pos]
    scheme_end = text.find("://")
    if scheme_end != -1:
        rest = text[scheme_end + 3 :]
        path_start = rest.find("/")
        authority = rest if path_start == -1 else rest[:path_start]
        if "@" in authority:
            authority = authority.rsplit("@", 1)[-1]
        tail = "" if path_start == -1 else rest[path_start:]
        text = text[: scheme_end + 3] + authority + tail
    return text[:200]


def _redact_query_component(pair: str) -> str:
    """Mask a query component, keeping only a plausible key.

    A padded opaque token (`c2VjcmV0==`) splits into a "key" and an empty
    value, so the keyed branch alone would print the secret and mask
    nothing. Anything whose value side is empty or pure `=` padding is
    treated as opaque and masked whole.
    """
    if not pair:
        return pair
    key, sep, value = pair.partition("=")
    if not sep or value.strip("=") == "":
        return "***"
    return f"{key}=***"


def redact_url(url: str) -> str:
    """Display-safe URL: no userinfo, masked query values, no fragment.

    Catalog servers embed credentials in URLs (query tokens like Tinybird's
    ``?token=...``, basic-auth userinfo), and doctor output is destined for
    support tickets. Query KEYS survive so the shape stays diagnosable.
    Display only — comparisons and requests always use the raw URL.
    """
    try:
        parts = urlsplit(url)
    except ValueError:
        return _sanitize_unparseable_url(url)
    netloc = parts.netloc.rsplit("@", 1)[-1]
    query = ""
    if parts.query:
        # Keyless components (`?SECRET_TOKEN`) are masked wholesale — a
        # bare value is as much a credential as a keyed one.
        query = "&".join(
            _redact_query_component(pair) for pair in parts.query.split("&")
        )
    return urlunsplit((parts.scheme, netloc, parts.path, query, ""))


def base_url_of(url: str) -> str:
    """scheme://netloc/path — the value the PRM `resource` must equal.

    Mirrors ``oauth.FileTokenStorage.get_base_url`` so doctor compares the
    exact string the OAuth flow will validate per RFC 8707.
    """
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def prm_candidates(server_url: str) -> list[str]:
    """RFC 9728 protected-resource-metadata URLs: path-appended, then root."""
    parsed = urlparse(server_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    path = parsed.path.rstrip("/")
    candidates = []
    if path:
        candidates.append(f"{origin}/.well-known/oauth-protected-resource{path}")
    candidates.append(f"{origin}/.well-known/oauth-protected-resource")
    return candidates


def as_metadata_candidates(issuer: str) -> list[str]:
    """RFC 8414 / OIDC discovery URLs for an authorization-server issuer."""
    parsed = urlparse(issuer)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    path = parsed.path.rstrip("/")
    raw = [
        f"{origin}/.well-known/oauth-authorization-server{path}",
        # Some IdPs (Okta org AS among them) only answer the path-suffixed
        # form {issuer}/.well-known/oauth-authorization-server.
        f"{origin}{path}/.well-known/oauth-authorization-server",
        f"{origin}/.well-known/openid-configuration{path}",
        f"{origin}{path}/.well-known/openid-configuration",
    ]
    candidates: list[str] = []
    for url in raw:
        if url not in candidates:
            candidates.append(url)
    return candidates


def effective_callback_port(
    server: ServerDetails,
    flag_port: int | None,
    cached_port: int | None,
) -> tuple[int | None, str]:
    """(port, source) with the same precedence `runlayer run` applies.

    Server-configured port only counts under manual OAuth (mirrors
    ``main._oauth_for_server``); the field may be absent on older backends,
    which the model defaults to ``None``.
    """
    manual = server.requires_manual_oauth_setup
    server_port = (
        getattr(server, "manual_oauth_callback_port", None) if manual else None
    )
    if flag_port:
        return flag_port, "--oauth-callback-port flag"
    if server_port:
        return server_port, "server-configured callback port"
    if cached_port:
        return cached_port, "cached from a previous OAuth run"
    return None, "random free port chosen at OAuth time"


def _cached_callback_port(server_url: str) -> int | None:
    """Callback port cached by a previous OAuth run, if any."""
    try:
        # Lazy: oauth.py imports `mcp`, which must not load at module import.
        from runlayer_cli.oauth import FileTokenStorage  # noqa: PLC0415

        return FileTokenStorage(server_url=base_url_of(server_url)).get_callback_port()
    except Exception:  # noqa: BLE001 - cache probe is best-effort
        return None


# Request-construction failures (a malformed advertised/derived URL, e.g. a
# nonnumeric port) are NOT httpx.HTTPError and would escape as tracebacks.
_REQUEST_ERRORS = (httpx.HTTPError, httpx.InvalidURL, httpx.UnsupportedProtocol)


def _url_wellformed(url: str) -> bool:
    """Whether this URL is usable by both the request layer and our parsing.

    httpx and urllib disagree on some references: httpx.URL accepts an
    unclosed IPv6 literal like "https://[bad" that urlparse raises
    ValueError on. Both must succeed, or a URL that passes this guard
    still explodes in a later parse.
    """
    try:
        httpx.URL(url)
        urlparse(url)
    except (httpx.InvalidURL, TypeError, ValueError):
        return False
    return True


def _resolve_advertised_url(advertised: str | None, server_url: str) -> str | None:
    """Absolute advertised PRM URL; relative references join the MCP URL.

    Mirrors the backend wire-discovery pin (test_wire_discovery relative
    resource_metadata tests): the challenge may advertise a relative
    location and the PRM document may exist ONLY there — dropping it
    would fall through to well-known guessing and find nothing.
    """
    if advertised is None:
        return None
    # urlparse/urljoin raise on some hostile references (e.g. an unclosed
    # IPv6 literal "https://[bad"). Returning the raw value keeps it on the
    # malformed-URL path in discover_prm rather than escaping as a traceback.
    try:
        parsed = urlparse(advertised)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return advertised
        return urljoin(server_url, advertised)
    except ValueError:
        return advertised


def _usable_endpoint_url(value: str) -> bool:
    """Whether an AS metadata endpoint value is an absolute http(s) URL.

    Presence isn't usability: httpx happily parses relative strings like
    "not-a-url", but the runtime cannot call them.
    """
    if not _url_wellformed(value):
        return False
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


async def _fetch_json(client: httpx.AsyncClient, url: str) -> dict[str, Any] | None:
    """GET url; return the JSON object on 200, else None. Never raises."""
    try:
        response = await client.get(url)
    except _REQUEST_ERRORS:
        return None
    if response.status_code != 200:
        return None
    try:
        payload = response.json()
    except ValueError:
        return None
    return payload if isinstance(payload, dict) else None


def resource_metadata_from_www_authenticate(header: str | None) -> str | None:
    """`resource_metadata` URL from a WWW-Authenticate challenge, if any.

    The real discovery flow consumes this advertised URL from the upstream
    401 before falling back to well-known paths, so doctor must too.
    """
    if not header:
        return None
    marker = "resource_metadata="
    idx = header.lower().find(marker)
    if idx == -1:
        return None
    value = header[idx + len(marker) :].strip()
    if value.startswith('"'):
        end = value.find('"', 1)
        return value[1:end] if end > 1 else None
    for separator in (",", " "):
        pos = value.find(separator)
        if pos != -1:
            value = value[:pos]
    return value or None


# Mirrors StreamableHttpTransport's protocol handshake: POST-only servers
# (Runlayer's own backend proxy among them) reject GET with 405 and only
# advertise `WWW-Authenticate: resource_metadata=...` on this POST.
def _mcp_initialize_body() -> dict[str, Any]:
    """The handshake StreamableHttpTransport would send.

    The protocol version comes from the installed SDK rather than a
    literal: a pinned legacy version drifts as the dependency moves and
    makes doctor fail servers that `runlayer run` initializes fine.
    """
    from mcp.types import (  # noqa: PLC0415 - lazy; module top stays mcp-free
        LATEST_PROTOCOL_VERSION,
    )

    return {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": LATEST_PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": USER_AGENT, "version": "doctor"},
        },
    }


_MCP_INITIALIZE_ID = 0
_MCP_ACCEPT_HEADER = "application/json, text/event-stream"


async def _streamed_head(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
) -> tuple[int, str | None, str]:
    """(status, WWW-Authenticate, Content-Type) — headers only, no body.

    SSE endpoints answer with a ``text/event-stream`` body that never
    ends; a buffered request would sit on it until the read timeout and
    report a live server as unreachable. Receipt of the response HEADERS
    is the reachability signal, so stream and close immediately.
    """
    # build_request can raise on a malformed stored URL; callers treat
    # _REQUEST_ERRORS as an unreachable verdict rather than a traceback.
    request = client.build_request(method, url, headers=headers, json=json_body)
    response = await client.send(request, stream=True)
    try:
        return (
            response.status_code,
            response.headers.get("www-authenticate"),
            response.headers.get("content-type", ""),
        )
    finally:
        await response.aclose()


# Bounded 2xx body read: large enough for any real initialize reply
# (validated replies can exceed 4KiB), small enough that an SSE stream
# can't hold us; we stop as soon as a COMPLETE document/frame arrives.
_INIT_BODY_SAMPLE_CAP = 65536
_INIT_BODY_READ_TIMEOUT_SECONDS = 3.0


@dataclass
class InitializeProbe:
    """Outcome of a bounded-body probe (initialize POST or SSE GET)."""

    status: int
    challenge: str | None
    content_type: str
    body_sample: bytes
    read_timed_out: bool
    over_cap: bool = False
    session_id: str | None = None


def _first_sse_event(sample: bytes) -> tuple[str, str] | None:
    """(name, data) of the first complete, non-comment SSE event, if any.

    Comment-only blocks (``: ping`` keep-alives) dispatch nothing per the
    SSE spec and are skipped. Default event name is ``message``; multiple
    ``data:`` lines join with newlines per the spec.
    """
    text = sample.decode("utf-8", "replace").replace("\r\n", "\n")
    blocks = text.split("\n\n")
    # The final element is an incomplete block (or empty at a boundary).
    for block in blocks[:-1]:
        fields = [
            line
            for line in block.splitlines()
            if line.strip() and not line.startswith(":")
        ]
        if not fields:
            continue
        name = "message"
        data_lines: list[str] = []
        for line in fields:
            if line.startswith("event:"):
                name = line[len("event:") :].strip()
            elif line.startswith("data:"):
                data_lines.append(line[len("data:") :].lstrip(" "))
        return name, "\n".join(data_lines)
    return None


def _first_sse_event_name(sample: bytes) -> str | None:
    event = _first_sse_event(sample)
    return event[0] if event is not None else None


def _sse_endpoint_data_usable(data: str, sse_url: str) -> bool:
    """Mirror what the mcp sse client accepts for the `endpoint` event.

    It resolves ``urljoin(url, data)`` and requires the result's scheme
    and netloc to equal the connection URL's — nothing more, so nothing
    more is enforced here (plus non-empty: an empty reference is never a
    usable POST target).
    """
    if not data.strip():
        return False
    try:
        joined = urljoin(sse_url, data)
        if not _usable_endpoint_url(joined):
            return False
        connection = urlparse(sse_url)
        endpoint = urlparse(joined)
    except ValueError:
        # urllib itself rejects the reference (e.g. bad IPv6 bracket).
        return False
    return connection.scheme == endpoint.scheme and connection.netloc == endpoint.netloc


def _sample_complete(sample: bytes, media_type: str) -> bool:
    """Whether the sample already holds a complete document/frame."""
    if media_type == "text/event-stream":
        return _first_sse_event_name(sample) is not None
    try:
        json.loads(sample.decode("utf-8", "replace"))
    except ValueError:
        return False
    return True


async def _bounded_probe(
    client: httpx.AsyncClient, request: httpx.Request
) -> InitializeProbe:
    """Send and read a BOUNDED 2xx body; raises on transport errors.

    Reads until a complete JSON document / SSE event, the byte cap, or
    the short timeout — never the whole stream. Non-2xx stays
    header-only.
    """
    response = await client.send(request, stream=True)
    try:
        sample = b""
        timed_out = False
        over_cap = False
        if 200 <= response.status_code < 300:
            media_type = (
                response.headers.get("content-type", "").split(";")[0].strip().lower()
            )
            import anyio  # noqa: PLC0415 - lazy so module top stays anyio-free

            try:
                with anyio.fail_after(_INIT_BODY_READ_TIMEOUT_SECONDS):
                    async for chunk in response.aiter_bytes():
                        sample += chunk
                        # Cap first: a single chunk can be both complete and
                        # oversized, and the body is truncated to the cap
                        # below — breaking on "complete" would hand the
                        # classifier a mid-document slice and hard-fail a
                        # working endpoint instead of warning about size.
                        if len(sample) >= _INIT_BODY_SAMPLE_CAP:
                            over_cap = True
                            break
                        if _sample_complete(sample, media_type):
                            break
            except TimeoutError:
                timed_out = True
            except httpx.HTTPError:
                pass
        return InitializeProbe(
            status=response.status_code,
            challenge=response.headers.get("www-authenticate"),
            content_type=response.headers.get("content-type", ""),
            body_sample=sample[:_INIT_BODY_SAMPLE_CAP],
            read_timed_out=timed_out,
            over_cap=over_cap,
            session_id=response.headers.get("mcp-session-id"),
        )
    finally:
        await response.aclose()


async def _initialize_probe(
    client: httpx.AsyncClient,
    url: str,
    identity_headers: dict[str, str] | None = None,
) -> InitializeProbe | None:
    """POST shaped like the real transport's MCP initialize. Never raises."""
    headers = {"Accept": _MCP_ACCEPT_HEADER, **(identity_headers or {})}
    try:
        request = client.build_request(
            "POST", url, headers=headers, json=_mcp_initialize_body()
        )
        probe = await _bounded_probe(client, request)
    except _REQUEST_ERRORS:
        return None
    # A stateful Streamable HTTP server allocates a session for this
    # initialize; doctor never uses it, so release it rather than leaving
    # abandoned sessions to accumulate across runs. Best-effort: a server
    # that doesn't support DELETE termination just 405s.
    if probe.session_id:
        try:
            from mcp.types import (  # noqa: PLC0415 - lazy, as elsewhere
                LATEST_PROTOCOL_VERSION,
            )

            await client.request(
                "DELETE",
                url,
                headers={
                    **headers,
                    "Mcp-Session-Id": probe.session_id,
                    # Streamable HTTP treats a missing MCP-Protocol-Version
                    # as the legacy default and can reject the termination.
                    "MCP-Protocol-Version": LATEST_PROTOCOL_VERSION,
                },
            )
        except _REQUEST_ERRORS:
            pass
    return probe


def _probe_rank(status: int) -> int:
    """How strongly a probe status evidences a live, working endpoint.

    401 outranks 2xx so an auth-required POST overrides a challenge-less
    GET 200; both outrank 404/5xx (path/upstream trouble) and 405 (wrong
    method for this server, no signal at all).
    """
    if status == 401:
        return 4
    if 200 <= status < 300:
        return 3
    if status == 405:
        return 0
    if status == 404 or status >= 500:
        return 1
    return 2


_REACHABILITY_TITLE = "Upstream reachability"


def _classify_initialize_reply(
    sample: bytes, media_type: str
) -> tuple[Literal["ok", "error", "invalid", "empty", "incomplete"], str]:
    """Validate the bounded initialize reply sample as real JSON-RPC.

    A byte-substring check would pass JSON-RPC errors, wrong ids, and
    garbage containing the literal. The sample must parse as JSON (after
    extracting the first SSE ``data:`` frame for event streams), carry
    ``jsonrpc == "2.0"``, echo the request id, and hold a ``result``. A
    JSON-RPC ``error`` is classified separately so it can be quoted.
    """
    text = sample.decode("utf-8", "replace")
    if media_type == "text/event-stream":
        # Same SSE field semantics as _first_sse_event: multiple `data:`
        # lines join with newlines; a reply split across lines is valid.
        event = _first_sse_event(sample)
        if event is None:
            return "empty", ""
        text = event[1]
    if not text.strip():
        return "empty", ""
    try:
        payload = json.loads(text)
    except ValueError:
        return "invalid", ""
    if not isinstance(payload, dict):
        return "invalid", ""
    if payload.get("jsonrpc") != "2.0":
        return "invalid", ""
    if payload.get("id") != _MCP_INITIALIZE_ID:
        return "invalid", ""
    error = payload.get("error")
    if error is not None:
        code = error.get("code") if isinstance(error, dict) else None
        message = error.get("message") if isinstance(error, dict) else str(error)
        return "error", f"code={code}, message='{str(message)[:120]}'"
    result = payload.get("result")
    if not isinstance(result, dict):
        return "invalid", ""
    # Validate with the SDK's own InitializeResult rather than hand-rolled
    # shape checks: it is the model the runtime parses with, so doctor
    # can't drift from it (and nested schemas like ServerCapabilities are
    # covered for free). Deliberately NOT a supported-version check — the
    # model accepts any protocolVersion string, and pinning a version set
    # here would fail servers the CLI it ships with can actually negotiate.
    from mcp.types import (  # noqa: PLC0415 - lazy; module top stays mcp-free
        InitializeResult,
    )
    from pydantic import ValidationError  # noqa: PLC0415 - lazy with the above

    try:
        InitializeResult.model_validate(result)
    except ValidationError as exc:
        first = exc.errors()[0]
        field = ".".join(str(part) for part in first.get("loc", ())) or "result"
        return "incomplete", f"{field} ({str(first.get('msg', ''))[:80]})"
    return "ok", ""


def _mcp_speak_verdict(
    probe: InitializeProbe, probe_text: str, display_url: str, title: str
) -> CheckResult:
    """Is a 2xx initialize response actually MCP? Content-Type + sample.

    Any web handler can 200 an unknown POST with an HTML page; discarding
    the body would pass it. The bounded first chunk must be a valid
    JSON-RPC initialize reply (or an SSE ``data:`` frame containing one).
    A read timeout on an open event-stream without a complete frame is
    pass-with-note — the frame may simply not have arrived within the
    bounded read.
    """
    content_type = probe.content_type.split(";")[0].strip().lower()
    if content_type not in ("application/json", "text/event-stream"):
        return CheckResult(
            "fail",
            title,
            f"endpoint answered the initialize POST at {display_url} but is "
            f"not speaking MCP (Content-Type: {content_type or 'missing'})",
            "verify the URL is the vendor's MCP endpoint, not a web page",
        )
    kind, described = _classify_initialize_reply(probe.body_sample, content_type)
    if kind == "ok":
        return CheckResult("ok", title, probe_text)
    if kind == "error":
        return CheckResult(
            "fail",
            title,
            f"endpoint answered the initialize POST at {display_url} with a "
            f"JSON-RPC error ({described})",
            "the endpoint rejected the initialize; verify the URL, "
            "transport, and upstream configuration",
        )
    if kind == "incomplete":
        return CheckResult(
            "fail",
            title,
            f"endpoint answered the initialize POST at {display_url} but "
            f"the result is not a valid MCP InitializeResult: {described}",
            "verify the URL is the vendor's MCP endpoint and the upstream "
            "speaks the MCP protocol version",
        )
    if probe.over_cap:
        # Genuinely hit the cap without a complete document — ambiguous,
        # not provably invalid.
        return CheckResult(
            "warn",
            title,
            f"{probe_text} — initialize reply exceeds "
            f"{_INIT_BODY_SAMPLE_CAP} bytes without a complete JSON "
            "document; cannot validate the reply",
            "the endpoint may still work; verify it manually if `runlayer "
            "run` misbehaves",
        )
    if content_type == "text/event-stream" and probe.read_timed_out:
        return CheckResult(
            "ok",
            title,
            f"{probe_text} (event-stream open; no complete initialize frame "
            "observed within the bounded read)",
        )
    return CheckResult(
        "fail",
        title,
        f"endpoint answered the initialize POST at {display_url} with "
        f"{content_type} but the response is not a JSON-RPC initialize reply",
        "verify the URL is the vendor's MCP endpoint",
    )


def _streaming_http_verdict(
    get_status: int | str,
    post_result: InitializeProbe | None,
    display_url: str,
    title: str = _REACHABILITY_TITLE,
) -> CheckResult:
    """Decision table for streaming-http: the initialize POST decides.

    Passing outcomes are the closed set {2xx-speaking-MCP, 401};
    everything else is a failure (5xx/timeouts soften to warnings as
    likely-transient). The GET status is supplementary detail only —
    ``"failed"`` when the GET raised without preempting the POST.
    """
    if post_result is None:
        return CheckResult(
            "warn",
            title,
            f"HTTP {get_status} from the GET at {display_url}, but the MCP "
            "initialize POST failed (timeout or network error) — Streamable "
            "HTTP connects via POST",
            "retry; if it persists, the endpoint likely cannot serve the "
            "MCP protocol over POST",
        )
    post_status = post_result.status
    probe = (
        f"HTTP {post_status} from the MCP initialize POST at {display_url} "
        f"(GET {get_status}, MCP initialize POST {post_status})"
    )
    if 200 <= post_status < 300:
        return _mcp_speak_verdict(post_result, probe, display_url, title)
    if post_status == 401:
        return CheckResult(
            "ok",
            title,
            f"{probe} (auth required — expected for OAuth-protected servers)",
        )
    if post_status == 405 and get_status == 405:
        return CheckResult(
            "fail",
            title,
            f"GET 405, MCP initialize POST 405 at {display_url} — endpoint "
            "answers neither GET nor MCP initialize POST — likely wrong "
            "path or stale URL",
            "verify the server URL in server settings matches the vendor's "
            "current MCP endpoint",
        )
    if post_status == 405:
        get_succeeded = isinstance(get_status, int) and (
            200 <= get_status < 300 or get_status == 401
        )
        if get_succeeded:
            # The classic misconfig: SSE endpoint stored as Streaming
            # HTTP. Diagnosed only when the GET actually SUCCEEDED —
            # "URL answers GET" must be true before suggesting SSE.
            return CheckResult(
                "fail",
                title,
                f"GET {get_status} but MCP initialize POST 405 at "
                f"{display_url} — URL answers GET but not MCP initialize "
                "POST — is this an SSE endpoint configured as Streaming "
                "HTTP?",
                "if the vendor endpoint is SSE, switch the server's "
                "transport to SSE, or use the vendor's streamable-http URL",
            )
        get_desc = f"GET {get_status}" if isinstance(get_status, int) else "GET failed"
        return CheckResult(
            "fail",
            title,
            f"endpoint rejects the MCP initialize POST (405) and "
            f"{get_desc} at {display_url} — likely wrong URL or stale "
            "endpoint",
            "verify the server URL in server settings matches the vendor's "
            "current MCP endpoint",
        )
    if post_status == 403:
        return CheckResult(
            "fail",
            title,
            f"{probe} — upstream refused the MCP initialize (HTTP 403) — "
            "endpoint reachable but rejects this client",
            "check upstream access controls (IP allowlists, org policies); "
            "the runtime will hit the same rejection",
        )
    if post_status == 404:
        return CheckResult(
            "fail",
            title,
            f"{probe} — the MCP path may be stale or wrong",
            "verify the server URL in server settings matches the vendor's "
            "current MCP endpoint",
        )
    if post_status >= 500:
        return CheckResult(
            "warn",
            title,
            f"{probe} — upstream is erroring",
            "the host is reachable; retry later or contact the upstream vendor",
        )
    return CheckResult(
        "fail",
        title,
        f"{probe} — unexpected response to the MCP initialize",
        "the endpoint does not speak the MCP protocol here; verify the "
        "server URL and transport in server settings",
    )


def _sse_verdict(
    get_probe: InitializeProbe,
    sse_url: str,
    display_url: str,
    title: str = _REACHABILITY_TITLE,
) -> CheckResult:
    """Decision table for sse: the streamed GET decides.

    Passing outcomes are the closed set {2xx event-stream carrying the
    MCP ``endpoint`` event, 401}; everything else is a failure (5xx
    softens to a warning as likely-transient). Symmetric with the
    streaming-http MCP-speak check: a 2xx that isn't an event stream is
    any web page, and an event stream without the ``endpoint`` event can
    be any feed.
    """
    get_status = get_probe.status
    content_type = get_probe.content_type
    body_sample = get_probe.body_sample
    read_timed_out = get_probe.read_timed_out
    probe = f"HTTP {get_status} from the streamed GET at {display_url}"
    if 200 <= get_status < 300:
        media_type = content_type.split(";")[0].strip().lower()
        if media_type != "text/event-stream":
            return CheckResult(
                "fail",
                title,
                f"{probe} — URL answered GET but is not an event stream "
                f"(Content-Type: {media_type or 'missing'}) — is this "
                "actually an SSE MCP endpoint?",
                "verify the URL is the vendor's SSE endpoint; if it is "
                "Streamable HTTP, switch the server's transport",
            )
        # text/event-stream alone can be any feed: SSETransport needs the
        # MCP `endpoint` event (mcp SDK sse server's first event) to learn
        # its POST URL.
        event = _first_sse_event(body_sample)
        first_event = event[0] if event is not None else None
        if event is not None and first_event == "endpoint":
            if not _sse_endpoint_data_usable(event[1], sse_url):
                return CheckResult(
                    "fail",
                    title,
                    f"{probe} — endpoint event carries an unusable POST URL "
                    f"('{redact_url(event[1])[:120]}') — the transport "
                    "cannot post messages",
                    "the server's SSE endpoint event is malformed; report "
                    "it to the upstream vendor",
                )
            return CheckResult("ok", title, f"{probe} (MCP endpoint event received)")
        if first_event is not None:
            return CheckResult(
                "fail",
                title,
                f"{probe} — stream connected but the first event is "
                f"'{first_event}', not the MCP endpoint event — is this an "
                "unrelated event feed?",
                "verify the URL is the vendor's MCP SSE endpoint",
            )
        if read_timed_out:
            # Stream open, nothing dispatched within the bounded read —
            # ambiguous rather than provably wrong (a 401 was not
            # available to confirm auth-gating either).
            return CheckResult(
                "ok",
                title,
                f"{probe} (event-stream open; no MCP endpoint event "
                "observed within the bounded read — cannot fully confirm "
                "this is an MCP SSE server)",
            )
        return CheckResult(
            "warn",
            title,
            f"{probe} — stream connected but no MCP endpoint event received",
            "verify the URL is the vendor's MCP SSE endpoint",
        )
    if get_status == 401:
        return CheckResult(
            "ok",
            title,
            f"{probe} (auth required — expected for OAuth-protected servers)",
        )
    if get_status == 405:
        return CheckResult(
            "fail",
            title,
            f"{probe} — URL rejects GET — is this a Streaming HTTP "
            "endpoint configured as SSE?",
            "if the vendor endpoint is Streamable HTTP, switch the "
            "server's transport to streaming-http, or use the vendor's "
            "SSE URL",
        )
    if get_status == 404:
        return CheckResult(
            "fail",
            title,
            f"{probe} — the MCP path may be stale or wrong",
            "verify the server URL in server settings matches the vendor's "
            "current MCP endpoint",
        )
    if get_status >= 500:
        return CheckResult(
            "warn",
            title,
            f"{probe} — upstream is erroring",
            "the host is reachable; retry later or contact the upstream vendor",
        )
    return CheckResult(
        "fail",
        title,
        f"{probe} — unexpected response for an SSE endpoint",
        "verify the server URL and transport in server settings",
    )


async def check_reachability(
    client: httpx.AsyncClient,
    url: str,
    identity_headers: dict[str, str] | None = None,
    transport_type: str = "streaming-http",
) -> tuple[CheckResult, str | None]:
    """(result, advertised resource_metadata URL from the OAuth challenge).

    One explicit decision per transport: ``streaming-http`` always runs
    the initialize POST and its outcome IS the verdict (the GET only
    supplies supplementary detail and challenge harvest); ``sse`` is
    decided by the streamed GET, with the POST used at most to harvest a
    missing challenge. Unknown transports fall back to best-evidence
    ranking across both probes.

    ``identity_headers`` (the identity-forward bundle) apply per-request
    here ONLY — like `runlayer run`, which attaches the bundle to the MCP
    transport for ``server.url`` and nowhere else. The shared client must
    stay identity-free so discovery/metadata fetches (PRM, authorization
    server) never leak ``X-Runlayer-Identity-Token`` or user/org PII to
    the IdP or an advertised PRM host.
    """
    title = _REACHABILITY_TITLE
    display_url = redact_url(url)

    if transport_type == "sse":
        # Mirror httpx-sse's aconnect_sse (what SSETransport rides on):
        # it sends `Accept: text/event-stream`, and content-negotiating
        # servers only serve the event stream when asked for it — a
        # generic */* GET would fetch HTML and false-fail the gate. The
        # bounded body read captures the first event so the verdict can
        # require the MCP `endpoint` event.
        sse_headers = {
            **(identity_headers or {}),
            "Accept": "text/event-stream",
        }
        try:
            get_request = client.build_request("GET", url, headers=sse_headers)
            get_probe = await _bounded_probe(client, get_request)
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            return CheckResult(
                "fail",
                title,
                f"{display_url} — host unreachable from this machine (VPN?): {exc}",
                "connect to the VPN / network that can reach the upstream, "
                "or fix the server URL in server settings",
            ), None
        except _REQUEST_ERRORS as exc:
            return CheckResult(
                "fail",
                title,
                f"{display_url} — request failed: {exc}",
                "verify the server URL and local network/TLS configuration",
            ), None
        advertised_prm_url = resource_metadata_from_www_authenticate(
            get_probe.challenge
        )
        # Harvest-only POST: an OAuth-protected SSE server may publish
        # resource_metadata only on the protocol POST.
        if advertised_prm_url is None and get_probe.status == 401:
            post_result = await _initialize_probe(client, url, identity_headers)
            if post_result is not None:
                advertised_prm_url = resource_metadata_from_www_authenticate(
                    post_result.challenge
                )
        return _sse_verdict(get_probe, url, display_url), advertised_prm_url

    status = -1
    challenge: str | None = None
    get_exc: Exception | None = None
    get_unreachable = False
    try:
        status, challenge, _content_type = await _streamed_head(
            client, "GET", url, headers=identity_headers
        )
    except (httpx.ConnectError, httpx.TimeoutException) as exc:
        get_exc = exc
        get_unreachable = True
    except _REQUEST_ERRORS as exc:
        get_exc = exc
    if get_exc is not None and transport_type != "streaming-http":
        # The GET is half the evidence for unknown transports; its
        # failure ends the check.
        if get_unreachable:
            return CheckResult(
                "fail",
                title,
                f"{display_url} — host unreachable from this machine (VPN?): {get_exc}",
                "connect to the VPN / network that can reach the upstream, "
                "or fix the server URL in server settings",
            ), None
        return CheckResult(
            "fail",
            title,
            f"{display_url} — request failed: {get_exc}",
            "verify the server URL and local network/TLS configuration",
        ), None
    advertised_prm_url = resource_metadata_from_www_authenticate(challenge)

    if transport_type == "streaming-http":
        # The POST always runs and always decides — a GET 401 with a
        # usable challenge is harvest material, never a verdict, and a
        # GET that reset/timed out is supplementary detail only: the POST
        # is the operation the runtime actually performs.
        post_result = await _initialize_probe(client, url, identity_headers)
        if post_result is None and get_exc is not None:
            if get_unreachable:
                return CheckResult(
                    "fail",
                    title,
                    f"{display_url} — host unreachable from this machine "
                    f"(VPN?): GET and MCP initialize POST both failed "
                    f"({get_exc})",
                    "connect to the VPN / network that can reach the "
                    "upstream, or fix the server URL in server settings",
                ), None
            return CheckResult(
                "fail",
                title,
                f"{display_url} — request failed: GET and MCP initialize "
                f"POST both failed ({get_exc})",
                "verify the server URL and local network/TLS configuration",
            ), None
        if post_result is not None and advertised_prm_url is None:
            advertised_prm_url = resource_metadata_from_www_authenticate(
                post_result.challenge
            )
        get_display: int | str = "failed" if get_exc is not None else status
        return _streaming_http_verdict(
            get_display, post_result, display_url
        ), advertised_prm_url

    # Unknown transport: best evidence across both probes.
    probe = f"HTTP {status} from {display_url}"
    if advertised_prm_url is None or status != 401:
        get_status = status
        post_result = await _initialize_probe(client, url, identity_headers)
        if post_result is not None:
            post_status = post_result.status
            if advertised_prm_url is None:
                advertised_prm_url = resource_metadata_from_www_authenticate(
                    post_result.challenge
                )
            decided = "GET"
            if _probe_rank(post_status) > _probe_rank(get_status):
                decided = "MCP initialize POST"
                status = post_status
            probe = (
                f"HTTP {status} from the {decided} at {display_url} "
                f"(GET {get_status}, MCP initialize POST {post_status})"
            )
    if status == 404:
        return CheckResult(
            "warn",
            title,
            f"{probe} — the MCP path may be stale or wrong",
            "verify the server URL in server settings matches the vendor's "
            "current MCP endpoint",
        ), advertised_prm_url
    if status >= 500:
        return CheckResult(
            "warn",
            title,
            f"{probe} — upstream is erroring",
            "the host is reachable; retry later or contact the upstream vendor",
        ), advertised_prm_url
    if status == 401:
        return CheckResult(
            "ok",
            title,
            f"{probe} (auth required — expected for OAuth-protected servers)",
        ), advertised_prm_url
    return CheckResult("ok", title, probe), advertised_prm_url


async def discover_prm(
    client: httpx.AsyncClient,
    server_url: str,
    advertised_url: str | None = None,
) -> tuple[dict[str, Any] | None, CheckResult]:
    title = "Protected-resource metadata (RFC 9728)"
    if advertised_url and not _url_wellformed(advertised_url):
        # The real discovery flow consumes this URL first; a malformed one
        # is a check failure, not a traceback.
        return None, CheckResult(
            "fail",
            title,
            f"advertised metadata URL is malformed: {redact_url(advertised_url)}",
            "the upstream's WWW-Authenticate resource_metadata value is "
            "invalid; report it to the upstream vendor",
        )
    candidates: list[tuple[str, str]] = []
    if advertised_url:
        candidates.append((advertised_url, "advertised via WWW-Authenticate"))
    for candidate in prm_candidates(server_url):
        if candidate != advertised_url:
            candidates.append((candidate, "well-known path"))
    rejected: list[str] = []
    for candidate, source in candidates:
        payload = await _fetch_json(client, candidate)
        if payload is None:
            continue
        # Mirror the backend wire pin (test_invalid_prm_document_continues_
        # ladder): a 200 document failing schema validation — no non-empty
        # authorization_servers — is skipped WITHOUT aborting; remaining
        # PRM URLs are tried and discovery falls back to the RS origin.
        # Elements must be usable URLs too: the runtime's typed
        # handle_protected_resource_response rejects invalid entries and
        # continues the ladder, so a doc advertising "not-a-url" must not
        # be selected over a later valid candidate. Rejections are kept so
        # that when NOTHING validates we can still say why, instead of
        # degrading to a bare "not found".
        servers = payload.get("authorization_servers")
        if not (isinstance(servers, list) and len(servers) >= 1):
            rejected.append(f"{redact_url(candidate)} (no authorization_servers)")
            continue
        unusable = [
            entry
            for entry in servers
            if not (isinstance(entry, str) and _usable_endpoint_url(entry))
        ]
        if unusable:
            rejected.append(
                f"{redact_url(candidate)} (authorization_servers entry is not "
                f"an absolute http(s) URL: {redact_url(str(unusable[0]))})"
            )
            continue
        return payload, CheckResult(
            "ok", title, f"found at {redact_url(candidate)} ({source})"
        )
    if rejected:
        return None, CheckResult(
            "fail",
            title,
            "no usable protected-resource metadata — rejected: " + "; ".join(rejected),
            "fix the metadata document the upstream serves, or report it to "
            "the upstream vendor",
        )
    return None, CheckResult(
        "warn",
        title,
        "no protected-resource metadata found (advertised, path-appended, or root)"
        if advertised_url
        else "no protected-resource metadata found (path-appended or root)",
        "server may not use OAuth or predates RFC 9728; discovery falls "
        "back to the server origin",
    )


def check_resource_match(prm: dict[str, Any], configured_base: str) -> CheckResult:
    """RFC 8707: `resource` must EXACTLY equal the configured URL.

    The MCP SDK validates this and a mismatch silently aborts the whole
    OAuth flow, so surface both strings verbatim.
    """
    title = "PRM `resource` matches configured URL (RFC 8707)"
    resource = prm.get("resource")
    if not isinstance(resource, str) or not resource:
        return CheckResult(
            "warn",
            title,
            "PRM has no `resource` field",
            "ask the upstream vendor to publish `resource`; the OAuth flow "
            "may still work but cannot be validated here",
        )
    if resource != configured_base:
        return CheckResult(
            "fail",
            title,
            f"MISMATCH — PRM resource='{redact_url(resource)}' vs configured "
            f"URL='{redact_url(configured_base)}' (OAuth aborts silently on "
            "mismatch)",
            "update the server URL in server settings to exactly match the "
            "PRM `resource` value (scheme, host, path, trailing slash)",
        )
    return CheckResult("ok", title, f"'{redact_url(resource)}' matches exactly")


def issuer_from_prm(prm: dict[str, Any] | None, server_url: str) -> tuple[str, bool]:
    """(issuer, from_prm). Falls back to the server origin when PRM is absent."""
    if prm is not None:
        servers = prm.get("authorization_servers")
        if isinstance(servers, list) and servers and isinstance(servers[0], str):
            return servers[0], True
    parsed = urlparse(server_url)
    return f"{parsed.scheme}://{parsed.netloc}", False


def _issuer_matches(doc_issuer: str, expected: str) -> bool:
    """RFC 8414: the declared issuer must EQUAL the discovery target.

    Simple string comparison per the RFC — no slash normalization: the
    runtime's typed parsing rejects `.../tenant` vs `.../tenant/`, and
    any prefix acceptance would pass cross-tenant documents.
    """
    return doc_issuer == expected


def _as_metadata_valid(payload: dict[str, Any], expected_issuer: str) -> bool:
    """Candidate-selection validity, mirroring the backend wire pin.

    test_asm_recoverable_failures_continue_to_next_url: a 200 with an
    invalid document shape moves on to the next ladder URL — so `issuer`
    and both runtime-required endpoints are validated BEFORE a candidate
    is selected, not after. A usable-but-wrong issuer is equally invalid
    for selection: it must not preempt a later candidate that declares the
    expected one.
    """
    doc_issuer = payload.get("issuer")
    if not (isinstance(doc_issuer, str) and _usable_endpoint_url(doc_issuer)):
        return False
    if not _issuer_matches(doc_issuer, expected_issuer):
        return False
    for name in ("authorization_endpoint", "token_endpoint"):
        value = payload.get(name)
        if not (isinstance(value, str) and value and _usable_endpoint_url(value)):
            return False
    # Finally the runtime's own model: a malformed OPTIONAL field (e.g.
    # token_endpoint_auth_methods_supported as a string) makes the real
    # OAuth flow reject this document and move on, so it must not be
    # selected here either.
    from mcp.shared.auth import (  # noqa: PLC0415 - lazy; module top stays mcp-free
        OAuthMetadata,
    )
    from pydantic import ValidationError  # noqa: PLC0415 - lazy with the above

    try:
        OAuthMetadata.model_validate(payload)
    except ValidationError:
        return False
    return True


async def discover_as_metadata(
    client: httpx.AsyncClient, issuer: str
) -> tuple[dict[str, Any] | None, str | None]:
    for candidate in as_metadata_candidates(issuer):
        payload = await _fetch_json(client, candidate)
        if payload is None:
            continue
        if not _as_metadata_valid(payload, issuer):
            # Invalid shape or a mismatched issuer must not stop discovery;
            # try the next well-known location.
            continue
        return payload, candidate
    return None, None


def check_registration_endpoint(
    as_metadata: dict[str, Any] | None,
    found_url: str | None,
    issuer: str,
    server: ServerDetails,
) -> CheckResult:
    title = "Authorization server metadata"
    found_url = redact_url(found_url) if found_url is not None else None
    # A manual client only takes effect when the flag is on — mirrors
    # `main._oauth_for_server`, which ignores the id otherwise.
    has_client_id = bool(server.manual_oauth_client_id)
    active_manual = server.requires_manual_oauth_setup and has_client_id
    if as_metadata is None:
        return CheckResult(
            "warn",
            title,
            f"could not fetch authorization-server metadata for {redact_url(issuer)}",
            "verify the authorization server is reachable from this machine; "
            "OAuth discovery will likely fail the same way",
        )
    # The authorization-code flow needs both endpoints at runtime, whether
    # the client came from DCR or manual configuration — metadata missing
    # either one is a hard failure, not a pass. Presence isn't usability:
    # a present-but-unusable value (relative, non-http, unparseable) fails
    # naming the field and its (redacted) value.
    missing_endpoints: list[str] = []
    unusable_endpoints: list[tuple[str, str]] = []
    for name in ("authorization_endpoint", "token_endpoint"):
        value = as_metadata.get(name)
        if not (isinstance(value, str) and value):
            missing_endpoints.append(name)
        elif not _usable_endpoint_url(value):
            unusable_endpoints.append((name, value))
    if missing_endpoints:
        return CheckResult(
            "fail",
            title,
            f"found at {found_url}; metadata is missing "
            f"{' and '.join(missing_endpoints)} — the authorization-code "
            "flow cannot run",
            "the authorization server's metadata is incomplete; verify the "
            "issuer URL or contact the IdP administrator",
        )
    if unusable_endpoints:
        described = "; ".join(
            f"{name}='{redact_url(value)}'" for name, value in unusable_endpoints
        )
        return CheckResult(
            "fail",
            title,
            f"found at {found_url}; metadata has endpoint URL(s) that are "
            f"not usable absolute http(s) URLs: {described} — the "
            "authorization-code flow cannot run",
            "the authorization server's metadata is broken; verify the "
            "issuer URL or contact the IdP administrator",
        )
    doc_issuer = as_metadata.get("issuer")
    if (
        isinstance(doc_issuer, str)
        and doc_issuer
        and not _issuer_matches(doc_issuer, issuer)
    ):
        # Discovery only surfaces docs WITH a usable issuer; one that
        # doesn't correspond to the discovered AS is a misconfiguration
        # the runtime's typed parsing would also reject.
        return CheckResult(
            "fail",
            title,
            f"found at {found_url}; metadata issuer "
            f"'{redact_url(doc_issuer)}' does not match the discovered "
            f"authorization server '{redact_url(issuer)}'",
            "the authorization server's issuer is misconfigured; verify "
            "the issuer URL or contact the IdP administrator",
        )
    registration = as_metadata.get("registration_endpoint")
    if (
        isinstance(registration, str)
        and registration
        and not _usable_endpoint_url(registration)
        and not active_manual
    ):
        # The DCR path would rely on this endpoint; an unusable value is
        # its own finding, not a generic "no registration_endpoint".
        return CheckResult(
            "fail",
            title,
            f"found at {found_url}; registration_endpoint is not a usable "
            f"absolute http(s) URL: '{redact_url(registration)}'",
            "the IdP's metadata is broken — configure Manual OAuth in "
            "server settings or contact the IdP administrator",
        )
    if isinstance(registration, str) and registration:
        detail = (
            f"found at {found_url}; registration_endpoint present "
            "(dynamic client registration advertised)"
        )
        if active_manual:
            detail += " — manual OAuth client configured, DCR will be skipped"
        return CheckResult(
            "ok",
            title,
            detail,
            None
            if active_manual
            else "note: some IdPs (e.g. Okta, 403 E0000005) advertise this "
            "endpoint but reject registration by policy — if OAuth fails "
            "there, configure Manual OAuth in server settings",
        )
    if active_manual:
        return CheckResult(
            "ok",
            title,
            f"found at {found_url}; no registration_endpoint, but a manual "
            "OAuth client is configured",
        )
    if has_client_id:
        # Precisely the customer state that motivated this command: the
        # credentials exist but `runlayer run` will still attempt DCR.
        return CheckResult(
            "fail",
            title,
            f"found at {found_url}; no registration_endpoint, and the "
            "configured manual client credentials are IGNORED because "
            "registration is not set to manual",
            "enable Manual OAuth in server settings so the configured "
            "client is actually used",
        )
    return CheckResult(
        "fail",
        title,
        f"found at {found_url}; no registration_endpoint and no manual "
        "client configured",
        "IdP likely requires a pre-registered client; configure Manual "
        "OAuth in server settings",
    )


def manual_oauth_checks(
    server: ServerDetails,
    prm: dict[str, Any] | None,
    as_metadata: dict[str, Any] | None = None,
) -> list[CheckResult]:
    results: list[CheckResult] = []
    manual = server.requires_manual_oauth_setup
    client_id = server.manual_oauth_client_id or None
    # Empty string classifies as absent, matching the backend/oauth.py rule.
    secret = server.manual_oauth_client_secret or None

    title = "Manual OAuth configuration"
    if manual and client_id is None:
        results.append(
            CheckResult(
                "fail",
                title,
                "Manual OAuth is required but no client ID is configured",
                "add the pre-registered client ID (and secret if "
                "confidential) in server settings",
            )
        )
    elif manual:
        results.append(
            CheckResult("ok", title, f"manual client '{client_id}' configured")
        )
    elif client_id is not None:
        results.append(
            CheckResult(
                "warn",
                title,
                "a manual client ID is configured but 'requires manual OAuth "
                "setup' is off — the manual client is IGNORED",
                "enable manual OAuth setup in server settings if the IdP "
                "rejects dynamic registration",
            )
        )
    else:
        results.append(
            CheckResult(
                "ok", title, "not required (dynamic registration / broker flow)"
            )
        )

    if manual:
        advertised: list[str] = []
        if prm is not None:
            raw = prm.get("scopes_supported")
            if isinstance(raw, list):
                advertised = [s for s in raw if isinstance(s, str)]
        configured = set((server.manual_oauth_scopes or "").split())
        scope_title = "OAuth scopes"
        if advertised:
            # scopes_supported is what the resource supports, not what every
            # client must request — a least-privilege subset is valid.
            if not configured:
                results.append(
                    CheckResult(
                        "warn",
                        scope_title,
                        "no scopes configured; the server advertises: "
                        + ", ".join(advertised),
                        "if OAuth or tool calls fail with permission errors, "
                        "configure the scopes this server requires",
                    )
                )
            else:
                unsupported = [s for s in sorted(configured) if s not in advertised]
                if unsupported:
                    results.append(
                        CheckResult(
                            "warn",
                            scope_title,
                            "configured but not in the server's advertised "
                            "scopes_supported: " + ", ".join(unsupported),
                            "verify these scopes are valid for this server — "
                            "the IdP may reject the authorization request",
                        )
                    )
                else:
                    unrequested = [s for s in advertised if s not in configured]
                    detail = (
                        "configured scopes are a subset of the advertised "
                        "scopes_supported"
                    )
                    if unrequested:
                        detail += f" (not requested: {', '.join(unrequested)})"
                    results.append(CheckResult("ok", scope_title, detail))
        else:
            results.append(
                CheckResult(
                    "ok",
                    scope_title,
                    f"configured: '{server.manual_oauth_scopes or '(none)'}'; "
                    "server advertises no scopes_supported to compare against",
                )
            )

    if manual and client_id is not None:
        # Derive the EFFECTIVE auth method with the same rule as runtime
        # (OAuth.__init__): an absent/empty secret overrides any stored
        # confidential preference to "none" — the public PKCE path;
        # otherwise the stored preference or the client_secret_post default.
        method = server.preferred_token_endpoint_auth_method
        secret_title = "Client secret vs token auth method"
        if secret is None:
            resolved_method = "none"
            if method in _CONFIDENTIAL_AUTH_METHODS:
                results.append(
                    CheckResult(
                        "warn",
                        secret_title,
                        f"no client secret configured; stored confidential auth "
                        f"method '{method}' is overridden to 'none' at runtime "
                        "(public PKCE client)",
                        "if the IdP client is actually confidential, add the "
                        "client secret in server settings; if it is public, this "
                        "works as-is and the stored method is just stale",
                    )
                )
            else:
                results.append(
                    CheckResult(
                        "ok",
                        secret_title,
                        "public client (no secret; token auth resolves to 'none')",
                    )
                )
        else:
            resolved_method = method or "client_secret_post"
            results.append(
                CheckResult(
                    "ok",
                    secret_title,
                    "confidential client (secret configured, auth method "
                    f"'{resolved_method}')",
                )
            )
        # Validate the RESOLVED method — whatever branch produced it — against
        # what the authorization server advertises. A secretless client
        # resolving to "none" against an AS that only supports confidential
        # methods fails token exchange just as surely as the reverse.
        supported = (
            as_metadata.get("token_endpoint_auth_methods_supported")
            if as_metadata is not None
            else None
        )
        if isinstance(supported, list):
            supported_methods = [s for s in supported if isinstance(s, str)]
            method_title = "Token endpoint auth method support"
            if supported_methods and resolved_method not in supported_methods:
                # A definite incompatibility, not ambiguity: the token
                # exchange cannot succeed, so it must affect the exit code.
                results.append(
                    CheckResult(
                        "fail",
                        method_title,
                        f"runtime will use '{resolved_method}' but the "
                        "authorization server supports only: "
                        + ", ".join(supported_methods),
                        "set the token endpoint auth method (and client secret "
                        "if confidential) in server settings to one the "
                        "authorization server supports",
                    )
                )
            elif supported_methods:
                results.append(
                    CheckResult(
                        "ok",
                        method_title,
                        f"'{resolved_method}' is advertised in the "
                        "authorization server's "
                        "token_endpoint_auth_methods_supported",
                    )
                )
    return results


def _callback_port_available(port: int) -> bool:
    """Bind test mirroring ``oauth._ensure_callback_port_available``.

    Same rule as `runlayer run`: it refuses to start the OAuth callback
    listener when the fixed port is already owned by another process.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            probe.bind(("127.0.0.1", port))
            probe.listen(1)
        except OSError:
            return False
    return True


def callback_port_check(
    server: ServerDetails,
    flag_port: int | None,
    cached_port: int | None,
) -> CheckResult:
    """Exact-match redirect guidance applies to MANUAL clients only.

    On the DCR path OAuth registers the exact chosen redirect URI (port
    included) during registration, so exact matching is satisfied by
    construction — a random port there is normal, not a warning.
    """
    title = "OAuth callback port"
    active_manual = server.requires_manual_oauth_setup and bool(
        server.manual_oauth_client_id
    )
    port, source = effective_callback_port(server, flag_port, cached_port)
    if port is not None and not _callback_port_available(port):
        return CheckResult(
            "warn",
            title,
            f"effective port {port} ({source}) — callback port {port} is "
            "already in use — `runlayer run` will fail to open the OAuth "
            "callback listener",
            "close the conflicting process or choose another port "
            "(--oauth-callback-port)",
        )
    if port is not None and active_manual:
        return CheckResult(
            "ok",
            title,
            f"effective port {port} ({source}) — ensure "
            f"http://localhost:{port}/callback is registered in the IdP "
            "redirect-URI allowlist",
        )
    if port is not None:
        return CheckResult(
            "ok",
            title,
            f"effective port {port} ({source})",
        )
    if active_manual:
        return CheckResult(
            "warn",
            title,
            f"{source} — IdPs with exact redirect-URI matching (e.g. Okta) "
            "will reject an unregistered port",
            "pass --oauth-callback-port <port> or set a callback port in "
            "server settings, and register http://localhost:<port>/callback "
            "in the IdP",
        )
    return CheckResult(
        "ok",
        title,
        f"{source} — dynamic client registration registers the redirect "
        "URI (port included) automatically",
    )


def _default_client_factory(headers: dict[str, str]) -> httpx.AsyncClient:
    # Lazy: tls.async_http_client only imports mcp when no timeout is given,
    # so pass an explicit one.
    from runlayer_cli.tls import async_http_client  # noqa: PLC0415

    return async_http_client(
        headers=headers,
        timeout=httpx.Timeout(_HTTP_TIMEOUT_SECONDS),
    )


def _verified_local_config(server: ServerDetails) -> Any | None:
    """VerificationConfig when the catalog entry is verified-local.

    Mirrors ``main.run``: a ``catalog_entry_name`` match wins before the
    transport branch, and the CLI codesign-verifies and proxies to the
    desktop app's localhost port instead of using ``server.url``.
    """
    # Lazy: keep verified_local_proxy out of this module's import cost.
    from runlayer_cli.verified_local_proxy.config import (  # noqa: PLC0415
        VERIFICATION_CONFIGS,
    )

    return VERIFICATION_CONFIGS.get(server.catalog_entry_name or "")


def _verify_target_once(config: Any) -> None:
    """One-shot, read-only process/signature verification of the target.

    The real path runs the same ``verify_target`` before connecting and
    refuses unexpected listeners; doctor mirrors it without retries.
    """
    # Lazy: proxy.py drags fastmcp/mcp into the closure.
    from runlayer_cli.verified_local_proxy.proxy import (  # noqa: PLC0415
        verify_target,
    )

    verify_target(config, max_retries=1)


def _verification_unavailable(exc: Exception) -> bool:
    """Verification could not run at all — distinct from a rejection.

    ``get_verifier`` raises ``RuntimeError`` on unsupported platforms
    (type check suffices). ``WindowsVerifier`` raises a plain
    ``VerificationError`` before identifying ANY listener — only its
    "not yet implemented" message distinguishes it, so match that
    conservatively.
    """
    if isinstance(exc, RuntimeError):
        return True
    message = str(exc).lower()
    return "not yet implemented" in message or "not implemented" in message


def _verify_target_result(verifier: Callable[[], None], display_target: str):
    """Run the process/signature verifier and translate to a CheckResult."""
    title = "Verified-local process"
    from runlayer_cli.verified_local_proxy.exceptions import (  # noqa: PLC0415
        TargetNotRunningError,
    )

    try:
        verifier()
    except TargetNotRunningError as exc:
        return CheckResult(
            "fail",
            title,
            f"no process found listening at {display_target}: {exc}",
            "start the desktop application, then rerun",
        )
    except Exception as exc:  # noqa: BLE001 - any verifier error is a finding
        if _verification_unavailable(exc):
            # No listener was ever identified — accusing the app of being
            # an impostor here would be wrong. The HTTP verdict decides.
            return CheckResult(
                "warn",
                title,
                f"process verification unavailable on this platform "
                f"({exc}) — relying on the HTTP probe only",
            )
        return CheckResult(
            "fail",
            title,
            f"a process is listening at {display_target} but is not the "
            f"expected signed application: {exc}",
            "quit the unexpected process and start the genuine desktop "
            "application, then rerun",
        )
    return CheckResult(
        "ok",
        title,
        f"process listening at {display_target} matches the expected "
        "signed application",
    )


async def run_verified_local_checks(
    target_url: str,
    identity_headers: dict[str, str] | None = None,
    client_factory: Callable[[dict[str, str]], httpx.AsyncClient] | None = None,
    verifier: Callable[[], None] | None = None,
) -> list[CheckResult]:
    """Probe a verified-local desktop app target like the runtime would.

    The runtime verifies the listening process's code signature BEFORE
    connecting (``verify_target``) and then talks StreamableHttpTransport
    to ``/mcp`` with the identity-forward headers — so doctor does both:
    ``verifier`` (one-shot, read-only) plus the initialize-POST decision,
    with the same per-request identity headers as the ordinary upstream
    probe.
    """
    factory = client_factory or _default_client_factory
    title = "Verified-local target"
    display_target = redact_url(target_url)
    results: list[CheckResult] = []
    if verifier is not None:
        results.append(_verify_target_result(verifier, display_target))
    async with factory({"User-Agent": USER_AGENT}) as client:
        try:
            get_status, _challenge, _content_type = await _streamed_head(
                client, "GET", target_url, headers=identity_headers
            )
        except _REQUEST_ERRORS as exc:
            # These targets are StreamableHttpTransport endpoints: the POST
            # is what the runtime uses, so a failed preliminary GET must not
            # preempt it (mirrors check_reachability's streaming-http path).
            get_status = "failed"
            get_error = exc
        post_result = await _initialize_probe(client, target_url, identity_headers)
        if get_status == "failed" and post_result is None:
            results.append(
                CheckResult(
                    "fail",
                    title,
                    f"desktop app not reachable at {display_target}: {get_error}",
                    "start the desktop application (and enable its MCP "
                    "server), then rerun",
                )
            )
            return results
    verdict = _streaming_http_verdict(
        get_status, post_result, display_target, title=title
    )
    if verdict.status == "ok":
        verdict.detail += " — desktop app is listening"
    else:
        post_status = "no response" if post_result is None else post_result.status
        verdict = CheckResult(
            "fail",
            title,
            f"desktop app responded but its MCP endpoint is unavailable at "
            f"{display_target} (GET {get_status}, MCP initialize POST "
            f"{post_status})",
            "restart the desktop application and re-enable its MCP server, then rerun",
        )
    results.append(verdict)
    return results


def _identity_headers(server: ServerDetails) -> dict[str, str]:
    """The identity-forward bundle headers, for the upstream probes ONLY.

    Identity-gated upstreams reject an anonymous probe while `runlayer run`
    works, so the upstream probes must carry the same ``X-Runlayer-*``
    headers. They are per-request, never client-wide: `runlayer run`
    attaches the bundle only to the MCP transport for ``server.url``, and
    the bundle can carry ``X-Runlayer-Identity-Token`` (short-lived token
    plus user/org PII) that must not reach the IdP or a PRM host.
    """
    headers: dict[str, str] = {}
    # Lazy: identity_forward imports anyio at module top.
    from runlayer_cli.identity_forward import (  # noqa: PLC0415
        merge_bundle_into_headers,
    )

    merge_bundle_into_headers(headers, server.identity_forward)
    return headers


async def run_network_checks(
    server: ServerDetails,
    flag_port: int | None,
    client_factory: Callable[[dict[str, str]], httpx.AsyncClient] | None = None,
    cached_port_lookup: Callable[[str], int | None] | None = None,
) -> list[CheckResult]:
    """All checks after the server-details read. Read-only probes only."""
    factory = client_factory or _default_client_factory
    lookup = cached_port_lookup or _cached_callback_port
    results: list[CheckResult] = []
    prm: dict[str, Any] | None = None
    as_metadata: dict[str, Any] | None = None
    # The shared client stays identity-free; only the upstream reachability
    # probes attach the identity-forward bundle.
    async with factory({"User-Agent": USER_AGENT}) as client:
        reachability, advertised_prm_url = await check_reachability(
            client,
            server.url,
            _identity_headers(server),
            server.transport_type,
        )
        advertised_prm_url = _resolve_advertised_url(advertised_prm_url, server.url)
        results.append(reachability)
        if reachability.status == "fail":
            results.append(
                CheckResult(
                    "skip",
                    "Protected-resource metadata (RFC 9728)",
                    "skipped — upstream unreachable",
                )
            )
            results.append(
                CheckResult(
                    "skip",
                    "Authorization server metadata",
                    "skipped — upstream unreachable",
                )
            )
        else:
            prm, prm_result = await discover_prm(client, server.url, advertised_prm_url)
            if (
                prm is None
                and prm_result.status == "warn"
                and reachability.detail.find("401") != -1
            ):
                # The upstream demanded authentication but publishes no
                # protected-resource metadata anywhere: the OAuth flow has
                # nothing to discover, so this is broken, not merely absent.
                prm_result = CheckResult(
                    "fail",
                    prm_result.title,
                    prm_result.detail
                    + " — but the upstream answered 401, so OAuth cannot start",
                    "the upstream requires auth without publishing RFC 9728 "
                    "metadata; report it to the upstream vendor",
                )
            results.append(prm_result)
            if prm is not None:
                results.append(check_resource_match(prm, base_url_of(server.url)))
            issuer, from_prm = issuer_from_prm(prm, server.url)
            if from_prm and not _usable_endpoint_url(issuer):
                # An unusable issuer would silently drain into failed
                # discovery; name it instead of exiting 0.
                results.append(
                    CheckResult(
                        "fail",
                        "Authorization server metadata",
                        "PRM authorization_servers[0] is not a usable "
                        f"absolute http(s) URL: '{redact_url(issuer)}'",
                        "the resource's protected-resource metadata is "
                        "broken; report it to the upstream vendor",
                    )
                )
            else:
                as_metadata, found_url = await discover_as_metadata(client, issuer)
                registration_result = check_registration_endpoint(
                    as_metadata, found_url, issuer, server
                )
                if not from_prm and registration_result.status != "fail":
                    registration_result.detail += (
                        " (issuer guessed from server origin — no PRM)"
                    )
                results.append(registration_result)
    results.extend(manual_oauth_checks(server, prm, as_metadata))
    results.append(callback_port_check(server, flag_port, lookup(server.url)))
    return results


def print_results(results: list[CheckResult]) -> bool:
    """Print all results; True when every check passed (no ❌).

    Unicode support is resolved per call (not at import) and, on an
    ASCII-only stdout, the ENTIRE rendered line is sanitized — the check
    text carries em dashes and arrows, not just the icons.
    """
    unicode_ok = _supports_unicode()
    icons = _UNICODE_ICONS if unicode_ok else _ASCII_ICONS
    for result in results:
        line = f"{icons[result.status]} {result.title}: {result.detail}"
        remedy = f"   -> {result.remedy}" if result.remedy else None
        if not unicode_ok:
            line = _to_ascii(line)
            remedy = _to_ascii(remedy) if remedy is not None else None
        typer.echo(line)
        if remedy is not None:
            typer.echo(remedy)
    return all(result.status != "fail" for result in results)


def doctor(
    ctx: typer.Context,
    target: str = typer.Argument(
        ..., help="UUID or supported alias of the MCP server to check"
    ),
    secret: Optional[str] = typer.Option(
        None,
        "--secret",
        "-s",
        help="API secret for authentication (optional if logged in)",
    ),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        help="Runlayer host URL (required if not in config)",
    ),
    oauth_callback_port: Optional[int] = typer.Option(
        None,
        "--oauth-callback-port",
        envvar="RUNLAYER_OAUTH_CALLBACK_PORT",
        min=1,
        max=65535,
        help="Fixed localhost port the OAuth callback would use "
        "(same flag as `runlayer run`)",
    ),
) -> None:
    """Preflight OAuth/connectivity checks for an MCP server (read-only)."""
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)

    client = RunlayerClient(hostname=credentials["host"], secret=credentials["secret"])
    details_title = "Server details"
    try:
        server_id = target if is_uuid(target) else client.resolve_server_target(target)
        server = client.get_server_details(server_id)
    except httpx.HTTPStatusError as exc:
        print_results(
            [
                CheckResult(
                    "fail",
                    details_title,
                    f"GET /api/v1/local/... returned HTTP "
                    f"{exc.response.status_code} for '{target}'",
                    "check the server ID/alias and that your credentials "
                    "have access to this server",
                )
            ]
        )
        raise typer.Exit(1)
    except httpx.HTTPError as exc:
        print_results(
            [
                CheckResult(
                    "fail",
                    details_title,
                    "cannot reach Runlayer host "
                    f"{redact_url(credentials['host'])}: {exc}",
                    "check --host and your network connection",
                )
            ]
        )
        raise typer.Exit(1)
    except (ValidationError, ValueError) as exc:
        # A 200 whose body isn't JSON at all (captive portal, proxy error
        # page) or doesn't match ServerDetails (version skew) must read as
        # a diagnostic, not a traceback. ValueError covers json decoding;
        # ValidationError is a subclass but named for intent.
        print_results(
            [
                CheckResult(
                    "fail",
                    details_title,
                    f"unexpected server details response for '{target}': "
                    f"{str(exc)[:200]}",
                    "the Runlayer host may be a different version than this "
                    "CLI; upgrade the CLI or check --host",
                )
            ]
        )
        raise typer.Exit(1)

    results = [
        CheckResult(
            "ok",
            details_title,
            f"'{server.name}' — deployment_mode="
            f"{server.deployment_mode or 'unknown'}, "
            f"transport={server.transport_type}, url={redact_url(server.url)}",
        )
    ]
    verified_config = _verified_local_config(server)
    if verified_config is not None:
        # `runlayer run` never touches server.url for these: it verifies
        # the desktop app's code signature and proxies to its localhost
        # port. Probe that target instead; OAuth discovery does not apply.
        results.append(
            CheckResult(
                "skip",
                "OAuth preflight",
                "verified-local catalog entry — `runlayer run` "
                "codesign-verifies and proxies to the local desktop app; "
                "no OAuth flow to check",
            )
        )
        import anyio  # noqa: PLC0415 - lazy so this module stays anyio-free

        results.extend(
            anyio.run(
                run_verified_local_checks,
                verified_config.target_url,
                _identity_headers(server),
                None,
                lambda: _verify_target_once(verified_config),
            )
        )
        if not print_results(results):
            raise typer.Exit(1)
        raise typer.Exit(0)

    if server.transport_type == "stdio":
        results.append(
            CheckResult(
                "skip",
                "OAuth/connectivity preflight",
                "stdio transport — the CLI spawns a local process; there is "
                "no upstream URL or OAuth flow to check",
            )
        )
        print_results(results)
        raise typer.Exit(0)

    import anyio  # noqa: PLC0415 - lazy so this module stays anyio-free

    results.extend(anyio.run(run_network_checks, server, oauth_callback_port))
    passed = print_results(results)
    if not passed:
        raise typer.Exit(1)
