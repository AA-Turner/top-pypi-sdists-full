"""the hosted ASGI app: /healthz, OAuth discovery, 401s with a logged reason, streamable HTTP mounted."""

from __future__ import annotations
import json
import logging
import os
import re
from typing import Any

import anyio
import anyio.to_thread
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from ...foundation.compat.compat import StrEnum
from ...foundation.request_identity.request_identity import (
    CLIENT_KIND_HEADER,
    CLIENT_VERSION_HEADER,
    client_headers_scope,
    client_version_headers)
from ...sdk.settings import workspace_limit
from ..delivery import accounting
from ...foundation.token_budget.token_budget import TokenizerUnavailable, count_tokens
from probe.mcp.server.auth import (
    _PROTECTED_RESOURCE_PATH,
    _oauth_discovery,
    _upstream_rejects,
    identity_for_token,
)
from probe.mcp.server.pool import _client_headers_var, _env, _token_var
from probe.mcp.server.server import create_server


async def _send_json(
    send: Any, status: int, body: bytes, *, extra_headers: list | None = None
) -> None:
    headers = [(b"content-type", b"application/json")] + (extra_headers or [])
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body})


#: What the Claude Code plugin's `bin/probe-mcp-headers` sends when the computer
#: holds no Probe token. It never sends nothing: a bare request draws the OAuth
#: challenge, and Claude Code then shows "Needs authentication" and skips this
#: server in every new session for 15 minutes. This placeholder is refused like
#: a bad token ("Failed to connect", no OAuth), without asking the API.
NO_TOKEN_PLACEHOLDER = "probe-no-token"


class Unauthorized(StrEnum):
    """Why the edge refused a request (logged; the body's `error` stays `invalid_token`)."""

    #: No bearer token at all: an OAuth client before it signs in, or an old helper.
    MISSING = "missing"
    #: The plugin helper found no token on the computer (NO_TOKEN_PLACEHOLDER).
    NO_TOKEN_ON_DEVICE = "no_token_on_device"
    #: A token the API refused: revoked, rotated, expired or never valid.
    REJECTED = "rejected"


def _unauthorized_body(reason: Unauthorized) -> bytes:
    if reason is Unauthorized.NO_TOKEN_ON_DEVICE:
        from ...sdk.session_marker import WIZARD_HINT

        return json.dumps(
            {"error": "invalid_token", "error_description": f"no Probe token on this computer: {WIZARD_HINT}"}
        ).encode()
    return b'{"error":"invalid_token"}'


#: A User-Agent's leading `product/version`, the only part of that caller-chosen
#: text a refusal log keeps: anything else (a pasted credential included) is "other".
_USER_AGENT_PRODUCT = re.compile(r"[A-Za-z][A-Za-z0-9._-]{0,40}/[0-9][0-9A-Za-z._+-]{0,30}")


def _user_agent_product(raw: bytes) -> str:
    text = raw.decode("ascii", "replace").split(" ", 1)[0]
    if not text:
        return "-"
    return text if _USER_AGENT_PRODUCT.fullmatch(text) else "other"


def _auth_logger() -> logging.Logger:
    """The refusal log, one plain line per 401. Not `_logger`: the hosted server's
    root handler (FastMCP's RichHandler) wraps at 80 columns, which splits a line
    so a search for `reason=` never shows the client beside it."""
    log = logging.getLogger("probe.mcp.auth")
    # Probe's own handler, found by its mark: a handler someone else added first
    # (a dictConfig, a test's capture) must not stop the plain line or let it
    # propagate into the wrapping root handler as well.
    if not any(getattr(handler, "_probe_auth_log", False) for handler in log.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        handler._probe_auth_log = True  # type: ignore[attr-defined]
        log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False
    return log


def with_auth_and_health(inner: Any, *, mcp_path: str = "/mcp", token_rejected: Any = None) -> Any:
    """Wrap an ASGI app: answer ``GET /healthz``; when OAuth discovery is on, serve
    the RFC 9728 protected-resource metadata and return a ``WWW-Authenticate``
    challenge for an unauthenticated MCP request (so clients auto-discover the
    authorization server). Otherwise copy the request's Bearer token into
    ``_token_var`` for the request (the per-request service picks it up).
    Non-HTTP scopes (lifespan) pass straight through.

    A *present but invalid* token is rejected here too, with the same 401 challenge.
    It has to happen at the edge: an MCP tool error is protocol-level and always
    rides inside an HTTP 200, so a stale token would otherwise load its tools and
    fail every call. The 401 is also what makes a client re-run its credential
    helper and retry (Claude Code >= 2.1.193), which is what lets a rotated token
    heal without a restart. That is a different floor from the plugin's own helper,
    which needs >= 2.1.195 for ``${CLAUDE_PLUGIN_ROOT}`` to interpolate.
    ``token_rejected`` is injectable for tests; ``PROBE_MCP_VERIFY_TOKEN=0`` turns
    the check off.
    """

    discovery = _oauth_discovery()
    if token_rejected is None and _env("MCP_VERIFY_TOKEN", "1") == "1":
        token_rejected = _upstream_rejects

    challenge = None
    if discovery:
        challenge = (
            'Bearer realm="research", '
            f'resource_metadata="{discovery["resource"]}{_PROTECTED_RESOURCE_PATH}", '
            'scope="research:read"'
        ).encode()
    auth_log = _auth_logger()

    async def _unauthorized(
        send: Any, reason: Unauthorized, client_headers: dict, agent: str | None, user_agent: bytes
    ) -> None:
        # Why, and from which client: a missing token and a refused one used to be
        # one indistinguishable `401 invalid_token`. Only values already validated
        # (client kind/version, a known agent) or reduced to `product/version`;
        # never the token, never other caller text.
        auth_log.info(
            "mcp 401 reason=%s client=%s/%s agent=%s user_agent=%s",
            reason.value,
            client_headers.get(CLIENT_KIND_HEADER) or "-",
            client_headers.get(CLIENT_VERSION_HEADER) or "-",
            agent or "-",
            _user_agent_product(user_agent),
        )
        extra = None
        if challenge and reason is Unauthorized.NO_TOKEN_ON_DEVICE:
            # Our own helper's placeholder: no sign-in to discover, so no
            # resource_metadata for a client to start one from.
            extra = [(b"www-authenticate", b'Bearer realm="research", error="invalid_token"')]
        elif challenge:
            extra = [(b"www-authenticate", challenge)]
        await _send_json(send, 401, _unauthorized_body(reason), extra_headers=extra)

    async def app(scope: dict, receive: Any, send: Any) -> None:
        if scope.get("type") != "http":
            await inner(scope, receive, send)
            return
        path = scope.get("path")
        if path == "/healthz":
            try:
                # Cold asset validation stays off the event loop and outside
                # the tool admission pool, so a saturated reader remains live.
                await anyio.to_thread.run_sync(count_tokens, "")
            except TokenizerUnavailable:
                await _send_json(send, 503, b'{"error":"mcp_tokenizer_unavailable"}')
                return
            await _send_json(send, 200, b'{"status":"ok"}')
            return
        if discovery and path == _PROTECTED_RESOURCE_PATH:
            body = json.dumps(
                {
                    "resource": discovery["resource"],
                    "authorization_servers": discovery["authorization_servers"],
                    "scopes_supported": ["research:read"],
                    "bearer_methods_supported": ["header"],
                }
            ).encode()
            await _send_json(send, 200, body)
            return
        headers = dict(scope.get("headers") or [])
        raw = headers.get(b"authorization", b"")
        try:
            # ASCII: every token any issuer mints is, and a non-ASCII one would
            # raise inside the API check (httpx cannot send it): a 500, not a 401.
            token = raw[7:].decode("ascii").strip() or None if raw[:7].lower() == b"bearer " else None
            undecodable = False
        except UnicodeDecodeError:
            # Not a token any issuer minted: refused at the edge, never a 500.
            token, undecodable = None, True
        try:
            client_kind = headers.get(CLIENT_KIND_HEADER.lower().encode(), b"").decode("ascii")
            client_version = headers.get(
                CLIENT_VERSION_HEADER.lower().encode(),
                b"",
            ).decode("ascii")
        except UnicodeDecodeError:
            client_headers = {}
        else:
            client_headers = client_version_headers(client_kind, client_version)
        # The CALLER's workspace limit (their computer's `probe workspace limit`),
        # forwarded as it came on every API call made for this request: the API
        # narrows those reads. `{}` -- they sent none -- is bound too, so this pod
        # never lends a request a limit of its own. The token check below (`/v1/me`)
        # does not carry it: a limit is never a reason to refuse a key.
        forwarded_limit = workspace_limit.forward_from(headers)
        client_headers_reset = _client_headers_var.set(client_headers)
        # Per-request accounting holder. Bound for EVERY hosted request, but only
        # emitted for ones that actually ran a tool (see accounting.emit) -- so
        # /healthz, the OAuth metadata path and unauthorized requests all return
        # before a tool runs and produce nothing.
        agent, agent_session = accounting.agent_from_headers(headers)
        acct = accounting.begin_request(
            agent,
            agent_session,
            client_headers,
            hide_session_work=accounting.hide_session_work_from_headers(headers),
        )
        # Bind the CALLER's pair as the outbound identity for this request, so
        # backend calls made while serving it report the caller's client rather
        # than the memoized transport's (which, hosted, is our own deployed
        # version). Binding `{}` is deliberate and not the same as leaving it
        # unset: a caller that reported nothing must reach the backend with no
        # version, never with ours.
        with client_headers_scope(client_headers), workspace_limit.forwarded_scope(forwarded_limit):
            try:
                if path.startswith(mcp_path):
                    refused = None
                    if undecodable:
                        refused = Unauthorized.REJECTED
                    elif discovery and token is None:
                        refused = Unauthorized.MISSING
                    elif token == NO_TOKEN_PLACEHOLDER:
                        refused = Unauthorized.NO_TOKEN_ON_DEVICE
                    elif token and token_rejected is not None and await token_rejected(token):
                        refused = Unauthorized.REJECTED
                    if refused is not None:
                        await _unauthorized(send, refused, client_headers, agent, headers.get(b"user-agent", b""))
                        return
                # Identity is read HERE, not at emit time. The accept cache has a
                # short TTL and emit runs after the tool body: any call that outlives
                # the TTL would otherwise emit as an unidentified caller despite
                # having authenticated perfectly well.
                acct["identity"] = identity_for_token(token)
                limited_to = workspace_limit.as_uuid(forwarded_limit.get(workspace_limit.LIMIT_HEADER))
                if limited_to and isinstance(acct["identity"], dict):
                    # This request's copy: the cached identity is per token.
                    acct["identity"] = {**acct["identity"], "workspace_id": limited_to}
                token_reset = _token_var.set(token)
                try:
                    await inner(scope, receive, accounting.counting_send(acct, send))
                finally:
                    _token_var.reset(token_reset)
            finally:
                # In `finally` so a client that disconnects mid-response still
                # records what we actually put on the wire. identity_for_token
                # reads the cache _upstream_rejects just populated.
                accounting.emit(acct, acct.get("identity"))
                accounting.end_request(acct)
                _client_headers_var.reset(client_headers_reset)

    return app


def http_app(mcp: FastMCP | None = None, *, path: str = "/mcp") -> Any:
    """The hosted ASGI app: FastMCP streamable-HTTP mounted at ``path``, wrapped with
    per-request auth + a health endpoint.

    DNS-rebinding protection (which rejects a non-localhost Host header) is OFF by
    default: this runs behind an authenticated reverse proxy (ingress + per-request
    Bearer token), so the browser-local-server threat it guards against does not apply.
    Set ``PROBE_MCP_DNS_REBIND_PROTECT=1`` (+ ``PROBE_MCP_ALLOWED_HOSTS=a,b``) to re-enable."""
    # Multi-tenant: the SDK scrubber's cache (plan (k)) would hold one tenant's
    # raw strings and time-leak them to the next. Off for the process's life.
    from probe.sdk import redaction as _redaction

    _redaction.forbid_scrub_cache()
    if mcp is None:
        protect = _env("MCP_DNS_REBIND_PROTECT", "0") == "1"
        hosts = [h.strip() for h in (_env("MCP_ALLOWED_HOSTS") or "").split(",") if h.strip()]
        security = TransportSecuritySettings(
            enable_dns_rebinding_protection=protect,
            allowed_hosts=hosts or ["*"],
            allowed_origins=["*"],
        )
        mcp = create_server(transport_security=security)
    mcp.settings.streamable_http_path = path
    # Response accounting depends on this. Stateless mode starts the MCP server task
    # from INSIDE each request task, so the worker thread's context copy still points
    # at that request's accounting holder. Stateful mode starts it once per SESSION at
    # initialize, so note_tool would forever mutate the first request's holder, every
    # later call would emit nothing, and no test would fail. One flag away from a
    # silent total loss of the metric, so assert it rather than remember it.
    if not mcp.settings.stateless_http:
        raise RuntimeError(
            "hosted MCP must run stateless_http=True: response accounting binds its "
            "per-request holder through the request task's context"
        )
    return with_auth_and_health(mcp.streamable_http_app(), mcp_path=path)


def main_http() -> None:
    import uvicorn

    uvicorn.run(
        http_app(),
        host=os.environ.get("HOST", "::"),
        port=int(os.environ.get("PORT", "8080")),
        # Nothing here reads the client address or scheme. Behind the hosted
        # pod's loopback TLS sidecar every peer is 127.0.0.1, which uvicorn
        # trusts by default and would then rewrite both from X-Forwarded-*.
        proxy_headers=False,
        # Above ingress-nginx's 60 s upstream keep-alive, so the proxy closes an
        # idle connection first. At uvicorn's 5 s default the two race, and the
        # proxy can send a request down a socket this end is closing (502).
        timeout_keep_alive=75,
    )
