"""Clean runtime client — session management, chat, events, discovery.

No server lifecycle management, no subprocess spawning, no TUI concerns.
Connects to an already-running runtime server over HTTP + WebSocket.
"""

import asyncio
import contextlib
import contextvars
import ipaddress
import json
import os
import typing as t
from urllib.parse import quote, urlsplit, urlunsplit

import httpx
from loguru import logger
from websockets.exceptions import ConnectionClosed

from dreadnode.app.api.client import AuthenticationError
from dreadnode.app.client import models
from dreadnode.app.client.interactive import (
    TurnCancelledError,
    TurnFailedError,
    _RuntimeInteractiveTransport,
)
from dreadnode.app.client.transports import (
    StreamingASGITransport,
    _RuntimeSocketProtocol,
    _WebsocketsRuntimeSocket,
)
from dreadnode.app.env import read_env_with_deprecation
from dreadnode.app.server.runtime_credentials import read_runtime_token
from dreadnode.app.server.runtime_events import RuntimeEventEnvelope
from dreadnode.core.tls import cached_platform_ssl_context, format_tls_error

_SUBSCRIBE_RECONNECT_INITIAL_DELAY = 0.25
_SUBSCRIBE_RECONNECT_MAX_DELAY = 15.0

# Loopback polling budget, used while waiting on a local server to bind. The
# managed client retries every 100ms, so this only has to beat a live socket.
_LOCAL_HEALTH_TIMEOUT = 1.0
# Remote runtimes are reached across the customer's WAN and ingress, with a TLS
# handshake on the first request. The loopback budget above is not survivable
# there, and a timeout here surfaces as "could not connect" with no cause.
REMOTE_HEALTH_TIMEOUT_SECONDS = 15.0

__all__ = [
    "DEFAULT_MODEL",
    "DEFAULT_RUNTIME_URL",
    "RuntimeClient",
    "TurnCancelledError",
    "TurnFailedError",
]


def _default_runtime_url() -> str:
    """Resolve the runtime URL from env at call time.

    Precedence: ``DREADNODE_RUNTIME_URL`` > composed from ``DREADNODE_RUNTIME_HOST``
    + ``DREADNODE_RUNTIME_PORT`` (with legacy ``DREADNODE_SERVER_HOST`` / ``_PORT``
    accepted and warned) > ``http://127.0.0.1:8787``.
    """
    explicit_url = os.environ.get("DREADNODE_RUNTIME_URL")
    if explicit_url:
        return explicit_url
    host = read_env_with_deprecation("DREADNODE_RUNTIME_HOST", "DREADNODE_SERVER_HOST", "127.0.0.1")
    port = read_env_with_deprecation("DREADNODE_RUNTIME_PORT", "DREADNODE_SERVER_PORT", "8787")
    return f"http://{host}:{port}"


class _RuntimeTokenAuth(httpx.Auth):
    """Attach the runtime's bearer credential per request.

    SB-CRED-012: the credential never changes during the sandbox's life, so
    there is nothing to re-read and no retry to make — a 401 means the caller
    is genuinely not authorized. Resolution stays per-request only so a client
    built before the environment was populated still picks it up. A ``None``
    result sends the request unauthenticated, which is how a server with auth
    disabled behaves.
    """

    def __init__(self, resolve_token: "t.Callable[[], str | None]") -> None:
        self._resolve_token = resolve_token

    def auth_flow(
        self, request: httpx.Request
    ) -> "t.Generator[httpx.Request, httpx.Response, None]":
        token = self._resolve_token()
        if token:
            request.headers["Authorization"] = f"Bearer {token}"
        yield request


# Resolved at import; consumers that spawn the server subprocess need the
# decomposed host/port pair. Lazy per-instance resolution in ``RuntimeClient.__init__``
# still reads current env.
DEFAULT_RUNTIME_HOST = read_env_with_deprecation(
    "DREADNODE_RUNTIME_HOST", "DREADNODE_SERVER_HOST", "127.0.0.1"
)
DEFAULT_RUNTIME_PORT = int(
    read_env_with_deprecation("DREADNODE_RUNTIME_PORT", "DREADNODE_SERVER_PORT", "8787")
)
DEFAULT_RUNTIME_URL = _default_runtime_url()
DEFAULT_MODEL = "anthropic/claude-opus-4-6"

if t.TYPE_CHECKING:
    from dreadnode.app.api.models import HumanInputResponse


class RuntimeClient:
    """Client for interacting with a running Dreadnode runtime server.

    Provides session management, chat streaming, event subscription,
    and runtime discovery. Assumes the server is already running —
    use :class:`~dreadnode.app.client.managed_client.ManagedRuntimeClient`
    when you need to start or manage the server process.
    """

    def __init__(
        self,
        server_url: str | None = None,
        *,
        auth_token: str | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        default_notify_source: str | None = None,
        default_session_labels: dict[str, list[str]] | None = None,
        default_session_origin: str | None = None,
        default_session_group_id: str | None = None,
    ) -> None:
        # Resolve env lazily per instance so tests setting env after import still work.
        self.server_url = (server_url or _default_runtime_url()).rstrip("/")
        # A pinned token (explicitly passed, or set post-construction by
        # ManagedRuntimeClient once it owns the socket) is used verbatim.
        # Otherwise the runtime's own credential is read from the environment.
        self._auth_token = auth_token
        # Remote runtimes on self-hosted installs are fronted by the customer's
        # own certificate, frequently issued by an internal CA. httpx defaults to
        # the certifi bundle, which never contains one; the platform client uses
        # native trust (ENG-7742) and this client must match, or every runtime
        # fails TLS on an install whose platform connection works fine.
        # An injected transport owns its own trust decisions, so leave it alone.
        self._injected_transport = transport
        self._http_client = self._create_http_client(transport=transport)
        # Used as the fallback ``source`` on ``notify`` calls (CAP-WCLI-014).
        # Worker-hosted clients set this to ``capability.<name>``; standalone
        # clients leave it as None and must supply ``source`` explicitly.
        self._default_notify_source = default_notify_source

        # Reserved labels that this client stamps on every ``create_session``
        # call (CAP-WCLI-022). Worker-bound clients populate this with
        # ``worker:<name>``; standalone clients leave it empty.
        env_labels: dict[str, list[str]] = {}
        worker_name = os.environ.get("DREADNODE_WORKER_NAME", "").strip()
        if worker_name:
            env_labels["worker"] = [worker_name]
        capability = os.environ.get("DREADNODE_CAPABILITY_LABEL", "").strip()
        if capability:
            env_labels["capability"] = [capability]
        capability_version = os.environ.get("DREADNODE_CAPABILITY_VERSION", "").strip()
        if capability_version:
            env_labels["capability_version"] = [capability_version]
        source_labels = default_session_labels if default_session_labels is not None else env_labels
        self._default_session_labels = {key: list(values) for key, values in source_labels.items()}
        # SES-ORG-003: worker-bound clients set this to ``worker`` so the
        # platform stamps ``origin=worker`` on every session. Standalone
        # clients leave it ``None`` and the runtime's default ``user`` applies.
        self._default_session_origin = default_session_origin or (
            os.environ.get("DREADNODE_SESSION_ORIGIN", "").strip() or None
        )
        self._default_session_group_id = default_session_group_id or (
            os.environ.get("DREADNODE_SESSION_GROUP_ID", "").strip() or None
        )
        self._active_session_group_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
            f"dreadnode_active_session_group_id_{id(self)}",
            default=None,
        )
        self._started = False
        self._interactive_transport: _RuntimeInteractiveTransport | None = None

    def _create_http_client(
        self,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> httpx.AsyncClient:
        """Create an HTTP client with the runtime's shared trust and auth policy."""
        transport_kwargs: dict[str, t.Any] = (
            {"transport": transport}
            if transport is not None
            else {"verify": cached_platform_ssl_context()}
        )
        return httpx.AsyncClient(
            base_url=self.server_url,
            timeout=None,  # noqa: S113 - long-lived runtime client intentionally disables global timeout
            auth=_RuntimeTokenAuth(self._current_token),
            **transport_kwargs,
        )

    def _current_token(self) -> str | None:
        """The bearer to present: the pinned one, else the runtime's own."""
        if self._auth_token is not None:
            return self._auth_token
        return read_runtime_token()

    def _build_auth_headers(self) -> dict[str, str]:
        token = self._current_token()
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    def _interactive_websocket_url(self) -> str:
        parsed = urlsplit(self.server_url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        return urlunsplit((scheme, parsed.netloc, "/api/ws", "", ""))

    def _health_timeout(self) -> float:
        """Pick the health budget from the destination, not the call site.

        A standalone worker connects to a loopback runtime through this same
        base ``start()``, and should fail fast rather than wait out a budget
        sized for a customer's WAN.
        """
        host = urlsplit(self.server_url).hostname or ""
        if host == "localhost" or host.endswith(".localhost"):
            return _LOCAL_HEALTH_TIMEOUT
        try:
            is_loopback = ipaddress.ip_address(host).is_loopback
        except ValueError:
            is_loopback = False
        return _LOCAL_HEALTH_TIMEOUT if is_loopback else REMOTE_HEALTH_TIMEOUT_SECONDS

    def _get_interactive_transport(self) -> _RuntimeInteractiveTransport:
        if self._interactive_transport is None:
            self._interactive_transport = _RuntimeInteractiveTransport(self)
        return self._interactive_transport

    @property
    def is_started(self) -> bool:
        """Whether the client has verified server connectivity."""
        return self._started

    async def start(self) -> None:
        """Verify the server is reachable.

        Subclasses override this to add server lifecycle management
        (e.g., auto-starting an in-process or subprocess server).
        """
        if self._started:
            return
        await self._probe_health(self._health_timeout())
        self._started = True

    async def close(self) -> None:
        """Close network resources (HTTP client and interactive transport)."""
        interactive = self._interactive_transport
        self._interactive_transport = None
        if interactive is not None:
            await interactive.close()
        await self._http_client.aclose()

    def _connect_error(self, cause: BaseException | str) -> RuntimeError:
        """Build a connect failure that names the underlying cause.

        The bare "could not connect" text this replaces was indistinguishable
        across DNS, TLS, routing and auth failures, which left both operators
        and support guessing at a self-hosted install.
        """
        detail = (
            f"{type(cause).__name__}: {cause}" if isinstance(cause, BaseException) else str(cause)
        )
        message = f"Could not connect to Dreadnode runtime server at {self.server_url} ({detail})"
        tls_hint = format_tls_error(cause)
        return RuntimeError(f"{message}\n\n{tls_hint}" if tls_hint else message)

    async def _probe_health(
        self,
        timeout: float,  # noqa: ASYNC109 - httpx owns the deadline
    ) -> None:
        """Verify ``/api/health``, raising a described failure on any error."""
        try:
            response = await self._http_client.get("/api/health", timeout=timeout)
        except httpx.HTTPError as exc:
            logger.debug("Health check failed | url={} | error={}", self.server_url, exc)
            raise self._connect_error(exc) from exc
        if response.status_code != 200:
            logger.debug("Health check | status={} | healthy=False", response.status_code)
            raise self._connect_error(f"/api/health returned HTTP {response.status_code}")
        logger.debug("Health check | status={} | healthy=True", response.status_code)

    async def _is_healthy(
        self,
        timeout: float = _LOCAL_HEALTH_TIMEOUT,  # noqa: ASYNC109 - httpx owns the deadline
    ) -> bool:
        try:
            await self._probe_health(timeout)
        except RuntimeError as exc:
            logger.debug("Health check failed | error={}", exc)
            return False
        return True

    # ── Runtime discovery ─────────────────────────────────────────

    async def fetch_runtime_info(self) -> models.RuntimeInfo:
        """Fetch runtime metadata from the connected server."""
        logger.debug("Fetching runtime info")
        await self.start()
        response = await self._http_client.get("/api/runtime")
        response.raise_for_status()
        info = models.RuntimeInfo.from_dict(response.json())
        logger.debug(
            "Runtime info | status={} | version={} | capabilities={}",
            info.status,
            info.version,
            len(info.capabilities),
        )
        return info

    async def fetch_tools(self) -> list[models.ToolInfo]:
        """Fetch available tools from runtime."""
        logger.debug("Fetching tools")
        await self.start()
        resp = await self._http_client.get("/api/tools")
        resp.raise_for_status()
        tools = [models.ToolInfo.from_dict(t) for t in resp.json().get("tools", [])]
        logger.debug("Fetched tools | count={}", len(tools))
        return tools

    async def fetch_skills(self) -> list[models.SkillInfo]:
        """Fetch available skills from runtime."""
        logger.debug("Fetching skills")
        await self.start()
        resp = await self._http_client.get("/api/skills")
        resp.raise_for_status()
        skills = [models.SkillInfo.from_dict(s) for s in resp.json().get("skills", [])]
        logger.debug("Fetched skills | count={}", len(skills))
        return skills

    async def fetch_mcp_detail(self, capability: str, server_name: str) -> dict[str, t.Any]:
        """Fetch full detail for an MCP server."""
        logger.debug("Fetching MCP detail | server={}:{}", capability, server_name)
        await self.start()
        resp = await self._http_client.get(f"/api/mcp/{capability}/{server_name}")
        resp.raise_for_status()
        data = resp.json()
        logger.debug(
            "Fetched MCP detail | server={}:{} | tools={}",
            capability,
            server_name,
            data.get("tool_count", 0),
        )
        return data

    async def reconnect_mcp_server(self, capability: str, server_name: str) -> dict[str, t.Any]:
        """Reconnect an MCP server and return updated detail."""
        logger.debug("Reconnecting MCP server | server={}:{}", capability, server_name)
        await self.start()
        resp = await self._http_client.post(f"/api/mcp/{capability}/{server_name}/reconnect")
        resp.raise_for_status()
        data = resp.json()
        logger.debug(
            "MCP reconnect complete | server={}:{} | status={}",
            capability,
            server_name,
            data.get("status"),
        )
        return data

    async def reauthenticate_mcp_server(
        self, capability: str, server_name: str
    ) -> dict[str, t.Any]:
        """Clear stored OAuth creds for an MCP server and trigger fresh auth.

        Only applies to streamable-HTTP servers with ``auth: oauth`` declared
        (CAP-MCP-011) — the platform returns 404 for stdio or non-OAuth HTTP.
        """
        logger.debug("Re-authenticating MCP server | server={}:{}", capability, server_name)
        await self.start()
        resp = await self._http_client.post(f"/api/mcp/{capability}/{server_name}/reauthenticate")
        resp.raise_for_status()
        data = resp.json()
        logger.debug(
            "MCP reauthenticate complete | server={}:{} | status={}",
            capability,
            server_name,
            data.get("status"),
        )
        return data

    async def fetch_worker_detail(self, capability: str, worker_name: str) -> dict[str, t.Any]:
        """Fetch full detail for a capability worker."""
        logger.debug("Fetching worker detail | worker={}:{}", capability, worker_name)
        await self.start()
        resp = await self._http_client.get(f"/api/workers/{capability}/{worker_name}")
        resp.raise_for_status()
        data = resp.json()
        logger.debug(
            "Fetched worker detail | worker={}:{} | state={}",
            capability,
            worker_name,
            data.get("state"),
        )
        return data

    async def restart_worker(self, capability: str, worker_name: str) -> dict[str, t.Any]:
        """Restart a capability worker and return updated detail."""
        logger.debug("Restarting worker | worker={}:{}", capability, worker_name)
        await self.start()
        resp = await self._http_client.post(f"/api/workers/{capability}/{worker_name}/restart")
        resp.raise_for_status()
        data = resp.json()
        logger.debug(
            "Worker restart complete | worker={}:{} | state={}",
            capability,
            worker_name,
            data.get("state"),
        )
        return data

    async def fetch_skill_content(self, name: str) -> str:
        """Fetch rendered skill content by name."""
        logger.debug("Fetching skill content | name={}", name)
        await self.start()
        resp = await self._http_client.get(f"/api/skills/{name}")
        resp.raise_for_status()
        data = resp.json()
        return str(data.get("rendered", "") or data.get("instructions", ""))

    async def reload_capabilities(self) -> models.RuntimeInfo:
        """Tell the server to re-discover capabilities and return updated runtime info."""
        logger.info("Reloading capabilities")
        await self.start()
        response = await self._http_client.post("/api/reload")
        response.raise_for_status()
        info = models.RuntimeInfo.from_dict(response.json())
        logger.info("Capabilities reloaded | count={}", len(info.capabilities))
        return info

    # ── Session management ────────────────────────────────────────

    async def list_sessions(self, *, include_platform: bool = False) -> list[models.SessionInfo]:
        """List in-process sessions from the connected server (the boot/swap fast path).

        Returns only sessions the runtime knows about in memory. ``include_platform``
        is preserved for callers that don't yet differentiate the two paths — when
        true, the runtime falls back to delegating to ``browse_sessions(page=1, limit=100)``
        and returns the flat ``sessions`` list. New code wanting paginated platform
        history should call :meth:`browse_sessions` directly so it gets the
        envelope (``total``, ``page``, etc.).
        """
        logger.debug("Listing sessions | include_platform={}", include_platform)
        await self.start()
        if include_platform:
            envelope = await self.browse_sessions(page=1, limit=100)
            return list(envelope.sessions)
        response = await self._http_client.get("/api/sessions")
        response.raise_for_status()
        sessions = [models.SessionInfo.from_dict(item) for item in response.json()]
        logger.debug("Listed sessions | count={}", len(sessions))
        return sessions

    async def browse_sessions(
        self,
        *,
        page: int = 1,
        limit: int = 20,
        sort_by: t.Literal[
            "updated_at", "last_message_at", "created_at", "message_count"
        ] = "updated_at",
        sort_dir: t.Literal["asc", "desc"] = "desc",
        archived: t.Literal["active", "inactive", "archived", "any"] = "active",
        label: list[str] | None = None,
        user_id: str | None = None,
        project_id: list[str] | None = None,
        origin: list[str] | None = None,
        search: str | None = None,
        include_workload_sessions: bool = False,
    ) -> models.SessionListResult:
        """Paginated browse of platform-persisted sessions for this workspace.

        Pass-through for the platform's ``GET /sessions`` query shape — the
        runtime forwards every kwarg as a query param and returns the
        platform's paginated envelope verbatim. In-process sessions are
        not merged on this path; the table view trusts that
        ``_register_session_with_platform`` syncs new sessions within a
        turn. Use :meth:`list_sessions` for live in-process state.

        ``include_workload_sessions`` (SES-LST-009) defaults to ``False``
        so the table view hides eval (and future optimization / training
        / world) runs. Callers that want them — the agents page, analytics
        — pass ``True``.
        """
        logger.debug(
            "Browsing sessions | page={} limit={} sort={}:{}",
            page,
            limit,
            sort_by,
            sort_dir,
        )
        await self.start()
        # httpx serializes list values as repeated query params, matching
        # how the platform client wires `?label=` / `?project_id=`.
        params: dict[str, t.Any] = {
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_dir": sort_dir,
            "archived": archived,
            "include_workload_sessions": include_workload_sessions,
        }
        if user_id is not None:
            params["user_id"] = user_id
        if search:
            params["search"] = search
        if project_id:
            params["project_id"] = list(project_id)
        if origin:
            params["origin"] = list(origin)
        if label:
            params["label"] = list(label)
        response = await self._http_client.get("/api/sessions/browse", params=params)
        response.raise_for_status()
        envelope = models.SessionListResult.from_dict(response.json())
        logger.debug(
            "Browsed sessions | total={} page={}/{} returned={}",
            envelope.total,
            envelope.page,
            envelope.total_pages,
            len(envelope.sessions),
        )
        return envelope

    async def browse_session_facets(
        self,
        *,
        archived: t.Literal["active", "inactive", "archived", "any"] = "active",
        label: list[str] | None = None,
        user_id: str | None = None,
        project_id: list[str] | None = None,
        origin: list[str] | None = None,
        search: str | None = None,
        include_workload_sessions: bool = False,
    ) -> models.SessionFacets:
        """Per-key value counts for the sidebar facets on the table view.

        Parallels :meth:`browse_sessions` — takes the same filter set
        (minus pagination / sort) and returns a typed
        :class:`~dreadnode.app.client.models.SessionFacets` envelope.
        Keys with zero matches are omitted by the platform, so the result
        only carries the keys the caller can act on. Honors the same
        SES-LST-009 workload default as the list endpoint.
        """
        logger.debug("Browsing session facets | archived={}", archived)
        await self.start()
        params: dict[str, t.Any] = {
            "archived": archived,
            "include_workload_sessions": include_workload_sessions,
        }
        if user_id is not None:
            params["user_id"] = user_id
        if search:
            params["search"] = search
        if project_id:
            params["project_id"] = list(project_id)
        if origin:
            params["origin"] = list(origin)
        if label:
            params["label"] = list(label)
        response = await self._http_client.get("/api/sessions/facets", params=params)
        response.raise_for_status()
        facets = models.SessionFacets.from_dict(response.json())
        logger.debug("Browsed session facets | keys={}", len(facets.labels))
        return facets

    async def create_session(
        self,
        *,
        capability: str | None = None,
        agent: str | None = None,
        model: str | None = None,
        session_id: str | None = None,
        group_id: str | None = None,
        project: str | None = None,
        generate_params_extra: dict[str, t.Any] | None = None,
        policy: str | dict[str, t.Any] | None = None,
        labels: dict[str, list[str]] | None = None,
        origin: str | None = None,
        project_memory_scope_kind: str | None = None,
        enable_project_memory_preload: bool | None = None,
        project_memory_preload_limit: int | None = None,
    ) -> models.SessionInfo:
        """Create or resolve a session on the server.

        If *session_id* is provided and a session with that ID already
        exists, the call is idempotent and returns the existing session
        (CAP-WCLI-003).
        """
        logger.debug(
            "Creating session | agent={} | model={} | project={} | policy={} | session_id={}",
            agent,
            model,
            project,
            policy,
            session_id[:8] if session_id else None,
        )
        await self.start()
        payload: dict[str, t.Any] = {}
        if capability is not None:
            payload["capability"] = capability
        if agent is not None:
            payload["agent"] = agent
        if model is not None:
            payload["model"] = model
        if session_id is not None:
            payload["session_id"] = session_id
        resolved_group_id = (
            group_id or self._active_session_group_id.get() or self._default_session_group_id
        )
        if resolved_group_id is not None:
            payload["group_id"] = resolved_group_id
        if project is not None:
            payload["project"] = project
        if generate_params_extra is not None:
            payload["generate_params_extra"] = generate_params_extra
        if policy is not None:
            payload["policy"] = policy
        # Merge client-bound default labels (CAP-WCLI-022) with any explicit
        # per-call labels. Explicit values win on conflict.
        merged_labels: dict[str, list[str]] = {
            key: list(values) for key, values in self._default_session_labels.items()
        }
        if labels:
            for key, values in labels.items():
                merged_labels[key] = list(values)
        if merged_labels:
            payload["labels"] = merged_labels
        # SES-ORG-003: explicit per-call origin wins; otherwise fall back to
        # the client-bound default (worker-bound clients set this to
        # ``worker``). Standalone clients leave it unset so the runtime's
        # ``user`` default applies.
        resolved_origin = origin if origin is not None else self._default_session_origin
        if resolved_origin is not None:
            payload["origin"] = resolved_origin
        if project_memory_scope_kind is not None:
            payload["project_memory_scope_kind"] = project_memory_scope_kind
        if enable_project_memory_preload is not None:
            payload["enable_project_memory_preload"] = enable_project_memory_preload
        if project_memory_preload_limit is not None:
            payload["project_memory_preload_limit"] = project_memory_preload_limit
        response = await self._http_client.post("/api/sessions", json=payload)
        response.raise_for_status()
        session = models.SessionInfo.from_dict(response.json())
        logger.info(
            "Session created | session_id={} | capability={}",
            session.session_id[:8],
            session.capability,
        )
        return session

    @contextlib.asynccontextmanager
    async def workflow(
        self,
        title: str,
        *,
        kind: t.Literal["worker_run", "evaluation_item", "workflow"] = "workflow",
        project: str | None = None,
        capability: str | None = None,
        capability_version: str | None = None,
        worker: str | None = None,
        metadata: dict[str, t.Any] | None = None,
    ) -> t.AsyncIterator[str | None]:
        """Create a session group and attach child ``create_session`` calls to it.

        If the local runtime is not connected to the platform, the context still
        runs and yields ``None`` so capability logic does not fail just because
        grouping is unavailable.
        """
        await self.start()
        group_id: str | None = None
        resolved_capability = capability or (
            os.environ.get("DREADNODE_CAPABILITY_LABEL", "").strip() or None
        )
        resolved_capability_version = capability_version or (
            os.environ.get("DREADNODE_CAPABILITY_VERSION", "").strip() or None
        )
        resolved_worker = worker or (os.environ.get("DREADNODE_WORKER_NAME", "").strip() or None)
        try:
            payload: dict[str, t.Any] = {
                "kind": kind,
                "title": title,
                "project": project,
                "capability": resolved_capability,
                "capability_version": resolved_capability_version,
                "worker": resolved_worker,
                "metadata": metadata or {},
            }
            response = await self._http_client.post("/api/session-groups", json=payload)
            if response.status_code == 404:
                logger.debug("Workflow group skipped: platform sync unavailable")
            else:
                response.raise_for_status()
                group = response.json()
                raw_group_id = group.get("id")
                if raw_group_id is not None:
                    group_id = str(raw_group_id)
        except Exception:
            logger.opt(exception=True).warning("Failed to create workflow group '{}'", title)

        token = self._active_session_group_id.set(group_id)
        try:
            yield group_id
        except Exception:
            if group_id is not None:
                with contextlib.suppress(Exception):
                    await self._http_client.patch(
                        f"/api/session-groups/{group_id}",
                        json={"status": "failed"},
                    )
            raise
        else:
            if group_id is not None:
                with contextlib.suppress(Exception):
                    await self._http_client.patch(
                        f"/api/session-groups/{group_id}",
                        json={"status": "completed"},
                    )
        finally:
            self._active_session_group_id.reset(token)

    async def get_session(self, session_id: str) -> models.SessionInfo | None:
        """Fetch a single session by id, hydrating from the platform if needed.

        Returns ``None`` on 404 so callers can treat "not found" as a normal
        outcome (e.g. ``--resume`` against an unknown id).
        """
        logger.debug("Getting session | session_id={}", session_id[:8])
        await self.start()
        response = await self._http_client.get(f"/api/sessions/{session_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return models.SessionInfo.from_dict(response.json())

    async def set_session_title(self, session_id: str, title: str) -> None:
        """Persist a session title on the server."""
        logger.info("Setting session title | session_id={}", session_id[:8])
        await self.start()
        response = await self._http_client.post(
            f"/api/sessions/{session_id}/title",
            json={"title": title},
        )
        response.raise_for_status()

    async def set_session_policy(
        self,
        session_id: str,
        policy: str | dict[str, t.Any] | None,
    ) -> dict[str, t.Any]:
        """Swap a session's active policy mid-run.

        Returns the server response dict with ``policy_name``,
        ``policy_is_autonomous``, and ``policy_display_label``
        populated from the resolved policy class.
        """
        logger.info("Setting session policy | session_id={} policy={}", session_id[:8], policy)
        await self.start()
        response = await self._http_client.post(
            f"/api/sessions/{session_id}/policy",
            json={"policy": policy},
        )
        response.raise_for_status()
        return dict(response.json())

    async def compact_session(self, session_id: str, *, guidance: str = "") -> dict[str, t.Any]:
        """Request manual compaction of a session."""
        logger.info("Compacting session | session_id={}", session_id[:8])
        await self.start()
        payload: dict[str, t.Any] = {}
        if guidance:
            payload["guidance"] = guidance
        response = await self._http_client.post(
            f"/api/sessions/{session_id}/compact",
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def fetch_rewind_candidates(self, session_id: str) -> list[dict[str, t.Any]]:
        """Return user-message rewind targets for the picker.

        Returns an empty list when the runtime is not platform-synced —
        rewind is platform-only, so there's nothing to surface.
        """
        logger.debug("Fetching rewind candidates | session_id={}", session_id[:8])
        await self.start()
        response = await self._http_client.get(f"/api/sessions/{session_id}/rewind/candidates")
        response.raise_for_status()
        body = response.json()
        candidates = body.get("candidates") if isinstance(body, dict) else None
        if not isinstance(candidates, list):
            return []
        return [entry for entry in candidates if isinstance(entry, dict)]

    async def rewind_session(self, session_id: str, *, from_seq: int) -> dict[str, t.Any]:
        """Hard-truncate a session at the target user-message ``seq``.

        Returns ``{status, deleted_count, target_seq, restored_content}``
        on success. Caller must already have aborted any in-flight turn
        — the runtime refuses with ``status=skipped`` while busy.
        """
        logger.info(
            "Rewinding session | session_id={} from_seq={}",
            session_id[:8],
            from_seq,
        )
        await self.start()
        response = await self._http_client.post(
            f"/api/sessions/{session_id}/rewind",
            json={"from_seq": from_seq},
        )
        response.raise_for_status()
        return dict(response.json())

    async def fetch_session_messages(self, session_id: str) -> list[dict[str, t.Any]]:
        """Fetch conversation messages for a session."""
        logger.debug("Fetching session messages | session_id={}", session_id[:8])
        await self.start()
        response = await self._http_client.get(f"/api/sessions/{session_id}/messages")
        response.raise_for_status()
        messages = response.json()
        logger.debug(
            "Fetched session messages | session_id={} | count={}", session_id[:8], len(messages)
        )
        return messages

    async def delete_session(self, session_id: str) -> None:
        """Delete a server session."""
        logger.info("Deleting session | session_id={}", session_id[:8])
        await self.start()
        response = await self._http_client.delete(f"/api/sessions/{session_id}")
        response.raise_for_status()

    async def archive_session(self, session_id: str, *, archived: bool = True) -> None:
        """Toggle a session's archived state on the platform.

        ``archived=True`` archives; ``archived=False`` unarchives. Both
        endpoints are idempotent on the platform side, so the caller can
        use this to drive a one-key toggle without tracking prior state.
        """
        action = "archive" if archived else "unarchive"
        logger.info("{} session | session_id={}", action.capitalize(), session_id[:8])
        await self.start()
        response = await self._http_client.post(
            f"/api/sessions/{session_id}/{action}",
        )
        response.raise_for_status()

    async def freeze_session(self, session_id: str) -> None:
        """Freeze a session on the platform — terminal, idempotent.

        Frozen sessions can still be loaded for read; the platform rejects
        any new turns. There is no thaw — design the call site accordingly.
        """
        logger.info("Freezing session | session_id={}", session_id[:8])
        await self.start()
        response = await self._http_client.post(
            f"/api/sessions/{session_id}/freeze",
        )
        response.raise_for_status()

    # ── Turn execution ────────────────────────────────────────────

    async def cancel_session(self, session_id: str) -> None:
        """Cancel the active turn for a session."""
        await self.start()
        await self._get_interactive_transport().cancel_session(session_id)

    async def stream_chat(
        self,
        *,
        session_id: str,
        message: str,
        model: str | None = None,
        agent: str | None = None,
        reset: bool = False,
        generate_params_extra: dict[str, t.Any] | None = None,
    ) -> t.AsyncIterator[dict[str, t.Any]]:
        """Stream websocket chat events for one session turn."""
        logger.debug(
            "WS stream starting | session={} | model={} | agent={}", session_id[:8], model, agent
        )
        await self.start()
        event_count = 0
        transport = self._get_interactive_transport()
        async for event in transport.stream_chat(
            session_id=session_id,
            message=message,
            model=model,
            agent=agent,
            reset=reset,
            generate_params_extra=generate_params_extra,
        ):
            event_count += 1
            event_type = str(event.get("type", "")).lower()
            logger.debug("WS event | type={} | session={}", event_type, session_id[:8])
            yield event
        logger.debug("WS stream complete | session={} | events={}", session_id[:8], event_count)

    async def run_turn(
        self,
        *,
        session_id: str,
        message: str,
        model: str | None = None,
        agent: str | None = None,
        reset: bool = False,
        generate_params_extra: dict[str, t.Any] | None = None,
    ) -> dict[str, t.Any]:
        """Run a turn to completion and return the terminal ``turn.completed``
        payload (CAP-WEVT-007): ``response_text``, ``tool_calls``, ``usage``,
        ``duration_ms``, ``turn_id``.

        Use this when you want the final result without iterating individual
        agent events. For streaming UIs, use :meth:`stream_chat` instead.

        Raises :class:`TurnFailedError` on ``turn.failed`` (carrying the
        ``error_type``, ``partial_response``, and any attempted tool calls)
        and :class:`TurnCancelledError` on ``turn.cancelled``.
        """
        logger.debug(
            "WS run_turn | session={} | model={} | agent={}",
            session_id[:8],
            model,
            agent,
        )
        await self.start()
        return await self._get_interactive_transport().run_turn(
            session_id=session_id,
            message=message,
            model=model,
            agent=agent,
            reset=reset,
            generate_params_extra=generate_params_extra,
        )

    # ── Event subscription ────────────────────────────────────────

    async def subscribe_session(self, session_id: str) -> None:
        """Keep a session subscribed on the interactive websocket."""
        logger.debug("Subscribing to session stream | session={}", session_id[:8])
        await self.start()
        await self._get_interactive_transport().subscribe_session(session_id)

    async def unsubscribe_session(self, session_id: str) -> None:
        """Drop a session subscription from the interactive websocket."""
        logger.debug("Unsubscribing from session stream | session={}", session_id[:8])
        await self.start()
        await self._get_interactive_transport().unsubscribe_session(session_id)

    async def subscribe(self, *kinds: str) -> t.AsyncIterator[RuntimeEventEnvelope]:
        """Subscribe to runtime-bus events filtered by ``kinds`` (CAP-WCLI-018).

        Returns an async iterator yielding :class:`RuntimeEventEnvelope`
        values. ``kinds`` is variadic; passing none subscribes to every
        event. Session- and runtime-scope envelopes both flow through —
        consumers inspect ``session_id`` to distinguish (CAP-WEVT-002).

        The iterator yields events until the caller closes it
        (``aclose()`` or breaking out of ``async for``) or authentication
        is rejected. History is not replayed (CAP-WCLI-020).

        On transient transport loss the client reconnects with
        exponential backoff, reinstates the original ``kinds`` filter,
        and yields a synthetic ``transport.reconnected`` envelope before
        resuming (CAP-WCLI-021). Events published while disconnected
        are not replayed; subscribers that need durability own their
        own resync.

        Peer of :meth:`subscribe_session` (CAP-WCLI-011); independent
        from the interactive transport, so standalone worker processes
        can iterate the runtime bus without opening a session-control
        channel.
        """
        await self.start()

        first_connection = True
        backoff = _SUBSCRIBE_RECONNECT_INITIAL_DELAY
        while True:
            try:
                socket = await self._open_event_stream_socket(kinds)
            except AuthenticationError:
                raise
            except Exception as exc:
                if first_connection:
                    raise
                logger.debug(
                    "Runtime event stream reconnect failed | error={} | backoff={:.2f}s",
                    exc,
                    backoff,
                )
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, _SUBSCRIBE_RECONNECT_MAX_DELAY)
                continue

            logger.debug(
                "Runtime event stream opened | kinds={} | reconnect={}",
                sorted(kinds) or "*",
                not first_connection,
            )
            if not first_connection:
                yield RuntimeEventEnvelope(
                    seq=0,
                    kind="transport.reconnected",
                    payload={"kinds": sorted(kinds)},
                )
            first_connection = False
            backoff = _SUBSCRIBE_RECONNECT_INITIAL_DELAY

            try:
                while True:
                    try:
                        raw = await socket.recv_text()
                    except AuthenticationError:
                        raise
                    except (RuntimeError, ConnectionClosed, OSError) as exc:
                        # Transient transport loss — close this socket,
                        # reconnect, and yield ``transport.reconnected``.
                        logger.debug("Runtime event stream transient loss | error={}", exc)
                        break
                    envelope_data = json.loads(raw)
                    yield RuntimeEventEnvelope.model_validate(envelope_data)
            finally:
                with contextlib.suppress(Exception):
                    await socket.close()

    async def _open_event_stream_socket(
        self,
        kinds: tuple[str, ...],
    ) -> _RuntimeSocketProtocol:
        """Open a websocket against ``/api/ws/events`` with the kind filter."""
        parsed = urlsplit(self.server_url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        query = "&".join(f"kinds={quote(kind, safe='')}" for kind in kinds)
        url = urlunsplit((scheme, parsed.netloc, "/api/ws/events", query, ""))
        headers = self._build_auth_headers()

        http_transport = self._http_client._transport
        if isinstance(http_transport, StreamingASGITransport):
            return await http_transport.websocket_connect(url=url, headers=headers)
        # Only a caller-supplied transport has no websocket equivalent. httpx
        # always populates ``_transport``, so testing that attribute rejected
        # every real socket -- local subprocess included -- and left the TUI's
        # notify and component-state loops retrying a hard failure forever.
        if self._injected_transport is not None:
            raise RuntimeError(
                "Runtime event stream is unavailable with an injected HTTP transport"
            )

        from websockets.asyncio.client import connect

        # Match the HTTP client's trust store so a wss:// runtime behind an
        # internal CA does not fail after its https:// health check passed.
        # websockets rejects a context on ws:// and rejects None on wss://,
        # so this has to track the scheme exactly.
        connection = await connect(
            url,
            additional_headers=headers or None,
            ping_interval=20,
            ping_timeout=20,
            ssl=cached_platform_ssl_context() if scheme == "wss" else None,
        )
        return _WebsocketsRuntimeSocket(connection)

    async def publish(
        self,
        kind: str,
        payload: dict[str, t.Any] | None = None,
        *,
        session_id: str | None = None,
    ) -> dict[str, t.Any]:
        """Publish an event onto the runtime event bus (CAP-WCLI-013).

        When *session_id* is provided the event is session-scoped; otherwise
        it is runtime-scope. Subscribers matching the event's ``kind`` receive
        it regardless of scope (CAP-WEVT-002). Reserved-prefix kinds
        (``turn.``, ``prompt.``, ``session.``, ``transport.``,
        ``capabilities.``) are rejected at the server per CAP-WEVT-003.
        """
        body = {"kind": kind, "payload": payload or {}}
        await self.start()
        if session_id is not None:
            logger.debug("Publishing event | session={} | kind={}", session_id[:8], kind)
            response = await self._http_client.post(
                f"/api/sessions/{session_id}/events",
                json=body,
            )
        else:
            logger.debug("Publishing runtime-scope event | kind={}", kind)
            response = await self._http_client.post("/api/events", json=body)
        response.raise_for_status()
        return response.json()

    async def notify(
        self,
        title: str,
        *,
        body: str | None = None,
        severity: t.Literal["info", "warning", "error", "success"] = "info",
        source: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, t.Any]:
        """Publish a user-facing notification (CAP-WCLI-014, CAP-WEVT-004).

        Notifications are runtime-scope unless *session_id* is provided.
        *source* defaults to the client's configured
        ``default_notify_source`` — worker-hosted clients get
        ``capability.<name>``; standalone clients leave it empty unless
        the caller supplies one.
        """
        return await self.publish(
            kind="notify",
            payload={
                "source": source or self._default_notify_source or "",
                "title": title,
                "body": body,
                "severity": severity,
            },
            session_id=session_id,
        )

    # ── Prompt responses ──────────────────────────────────────────

    async def send_permission_response(
        self,
        session_id: str,
        request_id: str,
        decision: str,
    ) -> None:
        """Send a permission decision back to the server via the interactive websocket."""
        logger.debug(
            "Sending permission response | session={} | request_id={} | decision={}",
            session_id[:8],
            request_id,
            decision,
        )
        await self.start()
        await self._get_interactive_transport().send_permission_response(
            session_id,
            request_id,
            decision,
        )

    async def send_human_input_response(
        self,
        session_id: str,
        response: "HumanInputResponse",
    ) -> None:
        """Send a human input response back to the server via the interactive websocket."""
        logger.debug("Sending human input response | session={}", session_id[:8])
        await self.start()
        await self._get_interactive_transport().send_human_input_response(session_id, response)

    # ── File system & shell ───────────────────────────────────────

    async def list_files(
        self,
        path: str | None = None,
        depth: int = 10,
    ) -> list[dict[str, t.Any]]:
        """List files in a directory on the server."""
        logger.debug("Listing files | path={} | depth={}", path, depth)
        await self.start()
        params: dict[str, t.Any] = {"depth": depth}
        if path:
            params["path"] = path
        response = await self._http_client.get("/api/files", params=params)
        response.raise_for_status()
        return response.json().get("entries", [])

    async def read_file(self, path: str) -> str:
        """Read a file's content from the server."""
        logger.debug("Reading file | path={}", path)
        await self.start()
        response = await self._http_client.get("/api/files/read", params={"path": path})
        response.raise_for_status()
        return response.json().get("content", "")

    async def execute_shell(
        self,
        command: str,
        *,
        cwd: str | None = None,
        timeout: int = 30,  # noqa: ASYNC109
    ) -> dict[str, t.Any]:
        """Execute a shell command on the server."""
        logger.debug("Executing shell command | cwd={} | timeout={}", cwd, timeout)
        await self.start()
        response = await self._http_client.post(
            "/api/shell",
            params={"command": command, "timeout": timeout, **({"cwd": cwd} if cwd else {})},
        )
        response.raise_for_status()
        return response.json()
