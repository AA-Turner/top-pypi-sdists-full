"""Basic on_message middleware for MCP CLI with OAuth support."""

import inspect
import sys
from typing import Any, cast

import anyio
from anyio.abc import TaskGroup
import httpx
from fastmcp import Client
from fastmcp.server.middleware.middleware import Middleware, MiddlewareContext, CallNext
import structlog
import mcp.types as mt
from runlayer_cli import flow_trace, oauth_guidance
from runlayer_cli.api import RunlayerClient
from runlayer_cli.error_classification import classify_exception
from runlayer_cli.sync import sync_local_capabilities

from fastmcp.server.proxy import FastMCPProxy
from fastmcp.tools.tool import ToolResult
from fastmcp.server.proxy import ProxyTool
from runlayer_cli.models import ServerDetails
from runlayer_cli.models_mcp import PostRequest, PreRequest, UpstreamError

if sys.version_info >= (3, 11):
    import builtins

    _ExceptionGroup = builtins.BaseExceptionGroup
else:  # pragma: no cover - py3.10 backport (dep of anyio)
    from exceptiongroup import BaseExceptionGroup as _ExceptionGroup

logger = structlog.get_logger()

# Connection errors that indicate the upstream target is not reachable.
# httpx.TransportError covers ConnectError/ReadError/ReadTimeout/etc; a hung
# upstream (VPN down, DNS blackhole) surfaces as a timeout, not a connect error.
_UPSTREAM_CONNECTION_ERRORS = (
    httpx.TransportError,
    ConnectionError,
    TimeoutError,
)

# Upper bound on the upstream tools/list round-trip so a blackholed target
# can't hang the client forever. tools/call is intentionally unbounded
# (long-running tools are legitimate).
_LIST_TOOLS_UPSTREAM_TIMEOUT_SECONDS = 30.0

# Upper bound on the detached first upstream connect. Generous because a cold
# remote connect may wait on a human finishing a browser OAuth login; bounded
# so a dead upstream releases the callback port instead of holding it forever.
_FIRST_CONNECT_TIMEOUT_SECONDS = 300.0

# Transports whose first connect may run a browser OAuth flow.
_OAUTH_TRANSPORT_TYPES = frozenset({"sse", "streaming-http"})

# Requests the proxy forwards upstream, so they wait on the detached first
# connect. fastmcp routes initialize (and ping) through on_request too; those
# must answer before any login completes. tools/list waits inside its own
# upstream bound in on_list_tools instead.
_FIRST_CONNECT_GATED_METHODS = frozenset(
    {
        "prompts/list",
        "prompts/get",
        "resources/list",
        "resources/templates/list",
        "resources/read",
        "tools/call",
    }
)

_RUNLAYER_INJECTED_SESSION_ID_ARG = "_runlayer_session_id"

# Upper bound on one background capability-sync attempt. Generous because
# introspection may legitimately wait on a human (Xcode mcpbridge's Allow
# dialog gates the first upstream request), but bounded so a dead upstream
# can't leave the sync marked in-flight forever, which would block retries.
_BACKGROUND_SYNC_TIMEOUT_SECONDS = 300.0


def _normalize_transport_config(value: dict[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    normalized: dict[str, Any] = {}
    for key, item in value.items():
        if isinstance(item, dict):
            nested = _normalize_transport_config(item)
            if nested:
                normalized[key] = nested
        else:
            normalized[key] = item
    return normalized


def _same_capability_source(left: ServerDetails, right: ServerDetails) -> bool:
    return (
        left.url,
        left.transport_type,
        _normalize_transport_config(left.transport_config),
        left.deployment_mode,
    ) == (
        right.url,
        right.transport_type,
        _normalize_transport_config(right.transport_config),
        right.deployment_mode,
    )


def _unreachable_error(exc: BaseException) -> BaseException | None:
    """Return the underlying connection error if `exc` means upstream unreachable.

    anyio task groups (used by fastmcp transports) can wrap transport errors in
    (nested) ExceptionGroups that a plain `except` tuple never matches, so
    unwrap them recursively.
    """
    if isinstance(exc, _UPSTREAM_CONNECTION_ERRORS):
        return exc
    if isinstance(exc, _ExceptionGroup):
        for inner in exc.exceptions:
            found = _unreachable_error(inner)
            if found is not None:
                return found
    return None


def _session_id_from_call_params(params: mt.CallToolRequestParams) -> str | None:
    arguments = getattr(params, "arguments", None)
    if not isinstance(arguments, dict):
        return None
    value = arguments.get(_RUNLAYER_INJECTED_SESSION_ID_ARG)
    return value if isinstance(value, str) and value else None


class RunlayerMiddleware(Middleware):
    def __init__(
        self,
        runlayer_api_client: RunlayerClient,
        proxy: FastMCPProxy | None,
        server: ServerDetails,
    ):
        self.runlayer_api_client = runlayer_api_client
        self.server = server
        self.proxy = proxy
        # Sync needs a live upstream session, so it fires after the first
        # successful tools/list for every transport: startup sync returned
        # empty capabilities for SSE/streaming-http (no connection before the
        # event loop) and raced local approval prompts for stdio (Xcode
        # mcpbridge), blocking serving.
        self.sync_done = not self.server.sync_required
        # Task group for running sync without delaying the tools/list
        # response (set by main once the event loop is up). Servers that
        # never answer resources/prompts (Xcode mcpbridge) hang introspection
        # ~30s per call; inline sync made clients kill the connection.
        self.background_tasks: TaskGroup | None = None
        self._sync_in_flight = False
        # Set once the detached first upstream connect has finished (any
        # outcome); None until the first request asks for it.
        self._first_connect: anyio.Event | None = None

    def _handle_upstream_unreachable(
        self,
        unreachable: BaseException,
        *,
        payload: PreRequest,
        correlation_id: str,
        log_event: str,
        post_result: list[mt.ContentBlock]
        | tuple[list[mt.ContentBlock], dict[str, Any]]
        | list[mt.Tool]
        | mt.CallToolResult
        | None,
        tool: str | None = None,
        inject_synthetic_tool_on_policy_block: bool = False,
    ) -> None:
        """Shared graceful branch for an unreachable upstream.

        The caller returns an in-band error result (no exception propagates),
        so mark the flow here to record status="error", and post the error to
        the backend for the audit trail.

        When the timeout fired while a browser OAuth login was still waiting
        on its localhost callback (IdP rejecting the redirect URI shows an
        error page in the browser and the CLI just times out), replace the
        bare timeout with actionable callback-port guidance in both the log
        file and the audited upstream error.
        """
        # In-band error result: no exception propagates through flow(), so
        # classify here (sanitized category + optional status, never text).
        category, http_status = classify_exception(unreachable)
        flow_trace.mark_error(
            type(unreachable).__name__, category=category, http_status=http_status
        )
        error_message = str(unreachable)
        oauth_port = oauth_guidance.pending_oauth_flow_port()
        if oauth_port is not None and isinstance(
            unreachable, (TimeoutError, httpx.TimeoutException)
        ):
            guidance = oauth_guidance.oauth_pending_timeout_message(oauth_port)
            error_message = f"{error_message} {guidance}".strip()
            logger.error(
                "upstream_timeout_while_oauth_login_pending",
                server_name=self.server.name,
                oauth_callback_port=oauth_port,
                guidance=guidance,
            )
        logger.warning(
            log_event,
            server_name=self.server.name,
            error_type=type(unreachable).__name__,
            **({"tool": tool} if tool is not None else {}),
        )
        try:
            post_payload = PostRequest(
                result=post_result,
                **(payload.model_dump() or {}),
                correlation_id=correlation_id,
                inject_synthetic_tool_on_policy_block=inject_synthetic_tool_on_policy_block,
                upstream_error=UpstreamError(
                    type=type(unreachable).__name__, message=error_message
                ),
            )
            with flow_trace.step("post", kind="http"):
                self.runlayer_api_client.post(self.server.id, post_payload)
        except Exception:
            logger.warning("post_after_upstream_error_failed", exc_info=True)

    async def _sync_capabilities(self) -> None:
        for attempt in range(2):
            try:
                assert self.proxy is not None
                await sync_local_capabilities(
                    self.runlayer_api_client,
                    self.proxy,
                    self.server.id,
                    server_version=self.server.version,
                )
                self.sync_done = True
                logger.debug(
                    "capabilities_synced_via_middleware", server_id=self.server.id
                )
                return
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code != httpx.codes.CONFLICT or attempt == 1:
                    logger.warning("capabilities_sync_failed", exc_info=True)
                    return
                try:
                    current_server = self.runlayer_api_client.get_server_details(
                        self.server.id
                    )
                    if current_server.version is not None and _same_capability_source(
                        self.server, current_server
                    ):
                        self.server.version = current_server.version
                        logger.info(
                            "capabilities_sync_version_refreshed",
                            server_id=self.server.id,
                            server_version=current_server.version,
                        )
                        continue
                    else:
                        self.sync_done = True
                        logger.info(
                            "capabilities_sync_skipped_for_stale_server_config",
                            server_id=self.server.id,
                            server_version=self.server.version,
                        )
                except Exception:
                    logger.warning(
                        "capabilities_sync_version_refresh_failed", exc_info=True
                    )
                return
            except Exception:
                logger.warning("capabilities_sync_failed", exc_info=True)
                return

    async def maybe_start_sync(self) -> None:
        """Kick capability sync in the background (no-op if done/in flight).

        Called eagerly at startup and again on every tools/list until a sync
        succeeds: clients cache tools/list across reconnects, so the list
        hook alone may never fire again after the first successful session.
        """
        if self.sync_done or self._sync_in_flight:
            return
        self._sync_in_flight = True
        if self.background_tasks is None:
            # No task group -> the verified-local path (run_verified_proxy
            # never sets one): keep its pre-existing inline sync behavior.
            # Those upstreams are local HTTP servers that answer
            # resources/prompts promptly.
            try:
                await self._sync_capabilities()
            finally:
                self._sync_in_flight = False
            return
        self.background_tasks.start_soon(self._run_background_sync)

    async def _run_background_sync(self) -> None:
        # start_soon inherits contextvars: when spawned from on_list_tools the
        # active cli.list_tools flow would swallow the sync's flow steps
        # (operation() is re-entrant). Reset our task-local copy so sync emits
        # its own cli.sync_capabilities flow; the caller's flow is unaffected.
        flow_trace.reset_flow()
        try:
            with anyio.move_on_after(_BACKGROUND_SYNC_TIMEOUT_SECONDS) as scope:
                await self._sync_capabilities()
            if scope.cancel_called:
                logger.warning(
                    "capabilities_sync_timed_out",
                    server_id=self.server.id,
                    timeout_seconds=_BACKGROUND_SYNC_TIMEOUT_SECONDS,
                )
        finally:
            self._sync_in_flight = False

    async def _await_first_upstream_connect(self) -> None:
        """Run the first remote connect outside the request that triggered it.

        A cold connect may wait on a human finishing a browser OAuth login.
        Clients cancel their initial requests after ~30s (Claude Desktop) and
        tools/list is bounded the same way; when the request owns the connect,
        that cancellation tears the OAuth flow down and a login finished
        seconds later lands on nothing. Detaching the connect into the
        background task group gives the login the OAuth timeout instead. The
        tokens persist to disk, so the request (or the client's next attempt)
        connects with them.
        """
        if self._first_connect is None:
            self._first_connect = anyio.Event()
            if (
                self.background_tasks is None
                or self.proxy is None
                or self.server.transport_type not in _OAUTH_TRANSPORT_TYPES
            ):
                self._first_connect.set()
            else:
                self.background_tasks.start_soon(self._run_first_upstream_connect)
        await self._first_connect.wait()

    async def _run_first_upstream_connect(self) -> None:
        """Open the shared upstream client once and hold it for the process.

        The proxy reuses a single client (``reuse_client_factory``); its
        reentrant session must be opened exactly once and never reopened. This
        SDK version wedges on a task-affine OAuth lock if a session is closed
        and reconnected, so we do not open-then-close a warm session. Instead
        we enter the shared client here (running the OAuth flow) and keep it
        open with an idle wait; requests reuse it by re-entering (nesting),
        and process teardown closes it once via the finally.
        """
        assert self.proxy is not None
        assert self._first_connect is not None
        flow_trace.reset_flow()
        client = self.proxy.client_factory()
        if inspect.isawaitable(client):
            client = await client
        client = cast(Client, client)
        try:
            # Bound only the connect (the OAuth login), not the idle hold.
            with anyio.fail_after(_FIRST_CONNECT_TIMEOUT_SECONDS):
                await client.__aenter__()
        except TimeoutError:
            logger.warning(
                "first_upstream_connect_timed_out",
                server_id=self.server.id,
                timeout_seconds=_FIRST_CONNECT_TIMEOUT_SECONDS,
            )
            self._first_connect.set()
            return
        except Exception:
            # A failed first connect leaves no session; a later request opens
            # its own and surfaces the error. (Not a reconnect of a live one.)
            logger.debug("first_upstream_connect_failed", exc_info=True)
            self._first_connect.set()
            return
        self._first_connect.set()
        try:
            # Hold the session open (nesting stays >=1) until teardown cancels
            # the background task group.
            await anyio.sleep_forever()
        finally:
            with anyio.CancelScope(shield=True):
                try:
                    await client.__aexit__(None, None, None)
                except Exception:
                    logger.debug("first_upstream_client_close_failed", exc_info=True)

    async def on_request(
        self,
        context: MiddlewareContext[mt.Request[Any, Any]],
        call_next: CallNext[mt.Request[Any, Any], Any],
    ) -> Any:
        if context.method in _FIRST_CONNECT_GATED_METHODS:
            await self._await_first_upstream_connect()
        return await call_next(context)

    @flow_trace.operation("cli.call_tool")
    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        flow_trace.set_session_id(_session_id_from_call_params(context.message))
        payload = PreRequest(method="tools/call", params=context.message.model_dump())

        with flow_trace.step("pre", kind="http"):
            pre_response = self.runlayer_api_client.pre(self.server.id, payload)
        if pre_response.status_code != 200:
            raise Exception(pre_response.json())

        pre_json = pre_response.json()
        correlation_id = pre_json["correlation_id"]
        quick_tool_result = pre_json.get("quick_tool_result")
        if quick_tool_result:
            return ToolResult(content=quick_tool_result)

        # Input masking: apply masked arguments from the pre scan before the
        # call reaches the upstream MCP server. Mirrors the hosted proxy, which
        # executes upstream with the masked `tool_arguments` from
        # `pre_on_call_tool`. Also refresh `payload.params` so the post audit
        # records the masked arguments (pre already does).
        modified_args = pre_json.get("modified_args")
        if isinstance(modified_args, dict):
            context.message.arguments = modified_args
            payload.params = context.message.model_dump()

        try:
            async with flow_trace.step("upstream", kind="remote"):
                result = await call_next(context)
        except Exception as exc:
            unreachable = _unreachable_error(exc)
            if unreachable is None:
                raise
            error_result = ToolResult(
                content=f"{self.server.name} is not running. "
                f"Please start the application and try again."
            )
            self._handle_upstream_unreachable(
                unreachable,
                payload=payload,
                correlation_id=correlation_id,
                log_event="upstream_unreachable",
                post_result=error_result.to_mcp_result(),
                tool=context.message.name,
            )
            return error_result

        post_payload = PostRequest(
            result=result.to_mcp_result(),
            **(payload.model_dump() or {}),
            correlation_id=correlation_id,
        )

        with flow_trace.step("post", kind="http"):
            post_response = self.runlayer_api_client.post(self.server.id, post_payload)
        if post_response.status_code != 200:
            raise Exception(post_response.json())

        # Output masking: apply the masked result the backend produced (PII
        # MASK / hidden-ascii redaction) so the MCP client receives the redacted
        # output instead of the raw upstream payload.
        post_json = post_response.json()
        if isinstance(post_json, dict):
            modified_output = post_json.get("modified_output")
            if isinstance(modified_output, dict):
                modified = mt.CallToolResult.model_validate(modified_output)
                result.content = modified.content
                # `structuredContent` (camelCase, mcp.types) ↔ `structured_content`
                # (snake_case, fastmcp) mirrors fastmcp's own `ToolResult.to_mcp_result`.
                result.structured_content = modified.structuredContent

        return result

    @flow_trace.operation("cli.list_tools")
    async def on_list_tools(  # type: ignore
        self,
        context: MiddlewareContext[mt.ListToolsRequest],
        call_next: CallNext[mt.ListToolsRequest, list[mt.Tool]],
    ) -> list[ProxyTool]:
        payload = PreRequest(method="tools/list", params=None)

        with flow_trace.step("pre", kind="http"):
            pre_response = self.runlayer_api_client.pre(self.server.id, payload)
        if pre_response.status_code != 200:
            raise Exception(pre_response.json())

        correlation_id = pre_response.json()["correlation_id"]

        try:
            async with flow_trace.step("upstream", kind="remote"):
                with anyio.fail_after(_LIST_TOOLS_UPSTREAM_TIMEOUT_SECONDS):
                    await self._await_first_upstream_connect()
                    result = await call_next(context)
        except Exception as exc:
            unreachable = _unreachable_error(exc)
            if unreachable is None:
                raise
            self._handle_upstream_unreachable(
                unreachable,
                payload=payload,
                correlation_id=correlation_id,
                log_event="upstream_unreachable_on_list_tools",
                post_result=[],
                inject_synthetic_tool_on_policy_block=True,
            )
            return []

        await self.maybe_start_sync()

        post_payload = PostRequest(
            result=[t.to_mcp_tool() for t in result],  # type: ignore
            **(payload.model_dump() or {}),
            correlation_id=correlation_id,
            inject_synthetic_tool_on_policy_block=True,
        )

        with flow_trace.step("post", kind="http"):
            post_response = self.runlayer_api_client.post(self.server.id, post_payload)
        if post_response.status_code != 200:
            raise Exception(post_response.json())

        assert self.proxy is not None
        filtered_result = [
            ProxyTool.from_mcp_tool(self.proxy, mt.Tool.model_validate(t))  # type: ignore
            for t in post_response.json()
        ]

        return filtered_result
