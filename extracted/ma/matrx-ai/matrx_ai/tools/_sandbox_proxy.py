"""Sandbox proxy — routes filesystem and shell tool calls to a remote sandbox.

When a chat turn is bound to a Matrx Sandbox (the user picked one in the
editor), the matrx-ai filesystem and shell tools should target THAT
container's filesystem, not the host process aidream itself runs on.
This module is the bridge.

How the binding flows
---------------------
The host (aidream) puts a small dict on ``AppContext.metadata`` under the
key ``"active_sandbox"`` for any request that should target a sandbox::

    metadata["active_sandbox"] = {
        "sandbox_id":  "sbx-abc123",          # informational
        "base_url":    "https://orchestrator.dev.codematrx.com/sandboxes/sbx-abc123",
        "access_token": "xxx",                 # X-Sandbox-Access-Token (HMAC-bound)
        "root_path":   "/home/agent",          # advertised workspace root
    }

The structured proxy endpoints live at ``{base_url}/fs/...`` and
``{base_url}/exec`` on the orchestrator. The orchestrator forwards them
into the in-container ``matrx_agent`` daemon — the same path the
``/sandboxes/{id}/fs/list`` admin route uses, so tool views and admin
views are guaranteed to be looking at the same filesystem.

When ``active_sandbox`` is absent, ``get_active_sandbox()`` returns
``None`` and the calling tool falls back to its existing local
implementation (multi-tenant ``/tmp/workspaces/<uid>/<pid>`` layout).
That's the rule that keeps non-sandbox chats working unchanged.

Design notes
------------
- Pure ``httpx``; no aidream imports — package independence preserved.
- One ``httpx.AsyncClient`` per call; we don't hold a long-lived client
  here because the binding can change between turns.
- Errors translate to the ``ToolError`` shape the rest of the package
  uses, so callers can build a ``ToolResult(success=False, error=...)``
  directly without re-mapping HTTP statuses.
- ``shell_execute`` returns a normalized ``{exit_code, stdout, stderr,
  cwd}`` dict matching the orchestrator's ``ExecResponse`` 1:1.
"""

from __future__ import annotations

import asyncio
import base64
import binascii
import logging
from dataclasses import dataclass
from typing import Any, Literal

import httpx

logger = logging.getLogger(__name__)

# How long we'll wait on any single sandbox call. Generous because shell
# commands can legitimately take a while; the caller can override per call.
DEFAULT_TIMEOUT_SECONDS = 60.0

# Zero-drift migrations: when a box is being swapped onto a new image, the
# orchestrator returns 503 {"detail": {"status": "migrating"}} with Retry-After
# for the few seconds of the cutover. We retry transparently so the agent's tool
# call lands on the new container (same sandbox_id/binding) instead of erroring —
# no agent confusion, the whole point of the safe-swap design.
# A migration locks the box for its whole swap (build + cutover), which can run
# ~60-120s on a heavy image. Retry long enough to outlast that so the agent's
# tool call waits the migration out and lands on the new container, rather than
# giving up mid-swap. ~50 attempts x up to 5s ≈ several minutes of headroom.
_MIGRATING_MAX_ATTEMPTS = 50
_MIGRATING_MAX_DELAY = 5.0        # cap any single Retry-After backoff


@dataclass(frozen=True)
class SandboxBinding:
    sandbox_id: str
    base_url: str          # ends WITHOUT trailing slash
    access_token: str
    root_path: str = "/home/agent"
    target_kind: Literal["sandbox", "local_machine"] = "sandbox"


@dataclass(frozen=True)
class SandboxReadResult:
    """One bounded daemon read, normalized across daemon generations."""

    content: str
    size: int
    offset: int
    limit: int
    next_offset: int
    truncated: bool
    server_bounded: bool


def get_active_sandbox() -> SandboxBinding | None:
    """Read the active sandbox binding off the request's AppContext.

    Returns ``None`` when no AppContext is set (tests, batch runs) or when
    the request isn't bound to a sandbox. Callers are expected to fall
    through to their local implementation in that case.
    """
    try:
        from matrx_connect import try_get_app_context
    except Exception:
        return None

    ctx = try_get_app_context()
    if ctx is None:
        return None

    raw = ctx.metadata.get("active_sandbox") if ctx.metadata else None
    if not raw or not isinstance(raw, dict):
        return None

    sandbox_id = raw.get("sandbox_id") or ""
    base_url = (raw.get("base_url") or "").rstrip("/")
    access_token = raw.get("access_token") or ""
    if not sandbox_id or not base_url or not access_token:
        return None
    target_kind = "local_machine" if raw.get("target_kind") == "local_machine" else "sandbox"
    root_path = raw.get("root_path")
    if target_kind == "local_machine" and (
        not isinstance(root_path, str) or not root_path.strip()
    ):
        # Never reinterpret a Windows/Linux/macOS desktop through the cloud
        # server's default POSIX sandbox root.
        return None

    return SandboxBinding(
        sandbox_id=sandbox_id,
        base_url=base_url,
        access_token=access_token,
        root_path=root_path.strip() if isinstance(root_path, str) and root_path.strip() else "/home/agent",
        target_kind=target_kind,
    )


# ── Helpers ────────────────────────────────────────────────────────────────

# Fresh tokens re-minted mid-loop, keyed by orchestrator sandbox_id. A sandbox
# access token is short-lived (≤15 min); when one expires mid-loop we re-mint via
# the host seam and cache it here so EVERY subsequent tool call in the loop uses
# the fresh token, not just the retried one. Keyed by sandbox_id (a token is
# valid for the box regardless of which conversation/request drives it).
_TOKEN_OVERRIDES: dict[str, str] = {}


def _headers(binding: SandboxBinding) -> dict[str, str]:
    return {
        "X-Sandbox-Access-Token": _TOKEN_OVERRIDES.get(binding.sandbox_id) or binding.access_token,
        "Content-Type": "application/json",
    }


async def _remint_token(binding: SandboxBinding) -> str | None:
    """Re-issue a fresh sandbox token via the host-injected minter, or None.

    Called when a proxied call 401/403s — the client-minted token has expired
    (loop outlived its ≤15-min TTL, or the client disconnected and can't
    refresh). Minting is host-owned (orchestrator master key); a bare matrx-ai
    install has no minter and simply can't refresh (auth error surfaces as-is).
    """
    from matrx_ai._ext import get_sandbox_token_minter

    minter = get_sandbox_token_minter()
    if minter is None:
        logger.warning(
            "sandbox %s token rejected (401/403) and no token minter configured — "
            "cannot refresh; surfacing auth error",
            binding.sandbox_id,
        )
        return None
    try:
        fresh = await minter(sandbox_id=binding.sandbox_id, base_url=binding.base_url)
    except Exception as exc:
        logger.warning("sandbox %s token re-mint raised: %s", binding.sandbox_id, exc)
        return None
    if fresh:
        _TOKEN_OVERRIDES[binding.sandbox_id] = fresh
        logger.info("sandbox %s token re-minted mid-loop after 401/403", binding.sandbox_id)
        return fresh
    logger.warning(
        "sandbox %s token re-mint returned nothing — box gone OR the host's "
        "orchestrator credentials are misconfigured (check the host's "
        "[sandbox-autobind] logs before declaring the box dead)",
        binding.sandbox_id,
    )
    return None


class SandboxProxyError(RuntimeError):
    """Raised when a sandbox call returns a non-2xx response.

    Attributes mirror what tool implementations need to build a
    ``ToolError`` without re-parsing the HTTP layer.
    """

    def __init__(self, message: str, *, status: int | None = None, error_type: str = "sandbox_error"):
        super().__init__(message)
        self.status = status
        self.error_type = error_type


def _is_migrating(resp: httpx.Response) -> bool:
    """True when a 503 is the orchestrator signalling an in-progress image swap."""
    try:
        body = resp.json()
    except Exception:
        return "migrating" in (resp.text or "").lower()
    detail = body.get("detail") if isinstance(body, dict) else None
    if isinstance(detail, dict):
        return detail.get("status") == "migrating"
    return isinstance(detail, str) and "migrating" in detail.lower()


def _retry_after_seconds(resp: httpx.Response, *, default: float) -> float:
    raw = resp.headers.get("Retry-After")
    if raw:
        try:
            return float(raw)
        except ValueError:
            pass
    return default


async def _request(
    binding: SandboxBinding,
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json: Any = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> httpx.Response:
    url = f"{binding.base_url}{path}"
    attempt = 0
    reminted = False
    while True:
        attempt += 1
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.request(method, url, params=params, json=json, headers=_headers(binding))
        except httpx.TimeoutException as exc:
            raise SandboxProxyError(
                f"Sandbox call timed out after {timeout}s",
                error_type="timeout",
            ) from exc
        except httpx.RequestError as exc:
            raise SandboxProxyError(
                f"Sandbox unreachable: {exc}",
                error_type="unreachable",
            ) from exc

        # Transparent retry while the box is mid-migration (image swap). Same
        # sandbox_id + binding survive the swap, so retrying lands on the new
        # container with no agent-visible error.
        if resp.status_code == 503 and _is_migrating(resp) and attempt < _MIGRATING_MAX_ATTEMPTS:
            delay = min(_retry_after_seconds(resp, default=3.0), _MIGRATING_MAX_DELAY)
            logger.info("sandbox %s migrating — retry %d in %.1fs", binding.sandbox_id, attempt, delay)
            await asyncio.sleep(delay)
            continue

        # Token expired mid-loop → re-mint ONCE (server-side, independent of the
        # client's token TTL and connectivity) and retry, so a long coding loop
        # or a disconnected client never surfaces a hard mid-task auth error.
        # The re-minted token is cached for every subsequent call this loop.
        if resp.status_code in (401, 403) and not reminted:
            reminted = True
            if await _remint_token(binding) is not None:
                continue
        break

    if resp.status_code == 404:
        raise SandboxProxyError(
            f"Not found: {path}",
            status=404,
            error_type="not_found",
        )
    if resp.status_code in (401, 403):
        raise SandboxProxyError(
            f"Sandbox auth rejected ({resp.status_code}): {resp.text[:200]}",
            status=resp.status_code,
            error_type="auth",
        )
    if resp.status_code >= 400:
        raise SandboxProxyError(
            f"Sandbox call failed ({resp.status_code}): {resp.text[:300]}",
            status=resp.status_code,
            error_type="upstream_error",
        )
    return resp


# ── Filesystem operations ──────────────────────────────────────────────────

async def fs_list(
    binding: SandboxBinding,
    path: str,
    *,
    recursive: bool = False,
    depth: int = 1,
    pattern: str | None = None,
    limit: int = 500,
    page_token: str | None = None,
) -> dict[str, Any]:
    """List a directory inside the sandbox.

    New daemons filter and paginate server-side. Older targets ignore unknown
    query fields (or may reject them with 422); both cases remain readable and
    are identified by the absence of pagination metadata in their response.
    """
    legacy_params: dict[str, Any] = {
        "path": path,
        "recursive": "true" if recursive else "false",
        "depth": depth,
    }
    params = {
        **legacy_params,
        "limit": limit,
    }
    if pattern:
        params["pattern"] = pattern
    if page_token:
        params["pageToken"] = page_token
    try:
        resp = await _request(binding, "GET", "/fs/list", params=params)
    except SandboxProxyError as exc:
        if exc.status != 422:
            raise
        resp = await _request(binding, "GET", "/fs/list", params=legacy_params)
    return resp.json()


async def fs_stat(binding: SandboxBinding, path: str) -> dict[str, Any]:
    resp = await _request(binding, "GET", "/fs/stat", params={"path": path})
    return resp.json()


async def fs_read(
    binding: SandboxBinding,
    path: str,
    *,
    encoding: Literal["utf8", "base64"] = "utf8",
    offset: int = 0,
    limit: int = 1_048_576,
) -> SandboxReadResult:
    """Read one bounded page, falling back cleanly for older targets.

    Upgraded daemons expose authoritative continuation metadata in headers.
    Older FastAPI targets silently ignore the new query fields and return the
    whole file; only that compatibility path performs a client-side slice.
    """
    legacy_params = {"path": path, "encoding": encoding}
    try:
        resp = await _request(
            binding,
            "GET",
            "/fs/read",
            params={**legacy_params, "offset": offset, "limit": limit},
        )
    except SandboxProxyError as exc:
        if exc.status != 422:
            raise
        resp = await _request(binding, "GET", "/fs/read", params=legacy_params)

    size_header = resp.headers.get("X-Matrx-File-Size")
    if size_header is not None:
        try:
            size = int(size_header)
            next_offset = int(resp.headers["X-Matrx-Next-Offset"])
            truncated = resp.headers["X-Matrx-Truncated"].lower() == "true"
        except (KeyError, ValueError) as exc:
            raise SandboxProxyError(
                "Sandbox returned malformed bounded-read metadata",
                error_type="protocol_error",
            ) from exc
        return SandboxReadResult(
            content=resp.text,
            size=size,
            offset=offset,
            limit=limit,
            next_offset=next_offset,
            truncated=truncated,
            server_bounded=True,
        )

    if encoding == "base64":
        try:
            full_bytes = base64.b64decode(resp.text, validate=True)
        except (ValueError, binascii.Error) as exc:
            raise SandboxProxyError(
                "Legacy sandbox returned invalid base64 content",
                error_type="protocol_error",
            ) from exc
        selected = full_bytes[offset : offset + limit]
        content = base64.b64encode(selected).decode("ascii")
        size = len(full_bytes)
        next_offset = offset + len(selected)
        truncated = next_offset < size
    else:
        full_text = resp.text
        selected_text = full_text[offset : offset + limit]
        content = selected_text
        size = len(full_text.encode("utf-8"))
        next_offset = offset + len(selected_text)
        truncated = next_offset < len(full_text)

    return SandboxReadResult(
        content=content,
        size=size,
        offset=offset,
        limit=limit,
        next_offset=next_offset,
        truncated=truncated,
        server_bounded=False,
    )


async def fs_write(
    binding: SandboxBinding,
    path: str,
    content: str,
    *,
    encoding: Literal["utf8", "base64"] = "utf8",
    create_parents: bool = True,
    mode: int | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "path": path,
        "content": content,
        "encoding": encoding,
        "create_parents": create_parents,
    }
    if mode is not None:
        body["mode"] = mode
    resp = await _request(binding, "PUT", "/fs/write", json=body)
    return resp.json()


async def fs_mkdir(
    binding: SandboxBinding,
    path: str,
    *,
    parents: bool = True,
) -> dict[str, Any]:
    resp = await _request(binding, "POST", "/fs/mkdir", json={"path": path, "parents": parents})
    return resp.json()


async def fs_patch(
    binding: SandboxBinding,
    path: str,
    edits: list[dict[str, str]],
    *,
    create_if_missing: bool = False,
) -> dict[str, Any]:
    """Apply 1+ search-and-replace edits to a file.

    ``edits`` is a list of ``{"old_text": str, "new_text": str, "replace_all": bool}``.
    The daemon matches ``old_text`` exactly and substitutes ``new_text`` in
    order — identical semantics to the tool's local implementation.
    """
    resp = await _request(
        binding, "POST", "/fs/patch",
        json={"path": path, "edits": edits, "create_if_missing": create_if_missing},
    )
    return resp.json()


async def fs_search(
    binding: SandboxBinding,
    pattern: str,
    *,
    path: str | None = None,
    content_search: bool = False,
    max_results: int = 100,
    case_sensitive: bool = False,
    regex: bool = True,
) -> dict[str, Any]:
    """Search inside the sandbox.

    Routes to the matrx_agent's ripgrep-backed ``/search/content`` (when
    ``content_search=True``) or fd-backed ``/search/paths`` (default).
    Returns the matrx_agent response verbatim — ``{results: [...]}``.
    """
    cwd = path or binding.root_path
    if content_search:
        body: dict[str, Any] = {
            "query": pattern,
            "cwd": cwd,
            "regex": regex,
            "case_sensitive": case_sensitive,
            "max_results": max_results,
        }
        resp = await _request(binding, "POST", "/search/content", json=body)
    else:
        body = {
            "pattern": pattern,
            "cwd": cwd,
            "max_results": max_results,
        }
        resp = await _request(binding, "POST", "/search/paths", json=body)
    data = resp.json()
    # Unify the two daemon endpoints behind the {"results": [...]} shape this
    # function's contract promises (and that the fs_search tool consumer reads).
    # /search/content already returns {"results": [...]} (match objects), but
    # /search/paths returns {"paths": [...]} (path strings) — passing that
    # through verbatim made every sandbox-bound PATH search silently return
    # zero results, since the consumer only reads `results`. Same client/daemon
    # contract-drift class as the /fs/patch fix; normalize at this seam.
    if isinstance(data, dict) and "results" not in data and "paths" in data:
        data = {**data, "results": data["paths"]}
    return data


# ── Shell ──────────────────────────────────────────────────────────────────

async def exec_command(
    binding: SandboxBinding,
    command: str,
    *,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    stdin: str | None = None,
    timeout: int = 60,
    user: str = "agent",
) -> dict[str, Any]:
    """Run a shell command inside the sandbox via the orchestrator's ``/exec``.

    Returns ``{exit_code: int, stdout: str, stderr: str, cwd: str}`` matching
    the orchestrator's ``ExecResponse`` shape 1:1.
    """
    body: dict[str, Any] = {"command": command, "timeout": timeout, "user": user}
    if cwd is not None:
        body["cwd"] = cwd
    if env:
        body["env"] = env
    if stdin is not None:
        body["stdin"] = stdin
    # Give the HTTP layer a few extra seconds beyond the command timeout so
    # graceful timeouts surface as ExecResponse, not as our own HTTP timeout.
    resp = await _request(binding, "POST", "/exec", json=body, timeout=float(timeout) + 10.0)
    return resp.json()


__all__ = [
    "SandboxBinding",
    "SandboxReadResult",
    "SandboxProxyError",
    "get_active_sandbox",
    "fs_list",
    "fs_stat",
    "fs_read",
    "fs_write",
    "fs_mkdir",
    "fs_patch",
    "fs_search",
    "exec_command",
]
