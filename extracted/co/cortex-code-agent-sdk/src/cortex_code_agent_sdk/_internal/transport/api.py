"""Direct Agent API transport for Cortex Code SDK."""

from __future__ import annotations

import asyncio
import json
import os
import re
import socket
import time
import uuid
from collections.abc import AsyncIterator, Mapping
from contextlib import suppress
from typing import Any

from ...types import (
    AgentApiOptions,
    AgentApiVStage,
    CortexCodeAgentOptions,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)
from . import Transport
from .api_support.connection import (
    _http_request,
    _http_stream_request,
    _resolve_connection,
)
from .api_support.messages import _to_api_assistant_content_block, _to_api_user_message
from .api_support.options import should_use_api_mode, validate_api_mode_options
from .api_support.settings import (
    _resolve_system_prompts,
    _sandbox_enabled,
)
from .api_support.tools import (
    _display_tool_name,
    _local_tool_execution_error,
    _normalize_tool_name,
    _permission_input_for_tool,
)
from .api_support.trace import _ApiTraceSink, _create_api_trace_sink
from .api_support.types import (
    DEFAULT_MODEL,
    DEFAULT_TOOLS,
    MAX_API_ROUND_TRIPS,
    SDK_ENTRYPOINT,
    _DirectConnection,
    _StreamResponse,
    _ToolUseData,
)
from .api_support.utils import _add_usage, _empty_usage
from .api_support.wire import (
    _parse_agent_run_cancel_response,
    _parse_agent_run_start_response,
    _parse_artifact_creation_response,
    _parse_latest_thread_message_id,
    _parse_response_body,
    _parse_thread_creation_response,
)

__all__ = ["AgentApiTransport", "should_use_api_mode", "validate_api_mode_options"]

API_AGENT_VERSION = "async-api"
SANDBOX_SQL_PROMPT = (
    "IMPORTANT: You are running in Snowflake sandbox mode. When using "
    "sql_execute, do NOT specify a connection parameter."
)
DISABLED_SERVER_TOOLS = [
    "system_instructions",
    "system_sql_reflection",
    "system_todo_write",
    "server_skill",
]
MAX_AUTH_REFRESH_RETRIES = 1
AUTH_EXPIRED_CODE_RE = re.compile(
    r"\b(?:390100|390103|390104|390111|390112|390114|390195|390303|390318|"
    r"394400|394401|394402|394407|407002)\b"
)
FORK_ARTIFACT_TITLE = "Forked conversation"


def _serialize_v_stage(v_stage: AgentApiVStage) -> dict[str, Any]:
    data: dict[str, Any] = {
        "stage_name": v_stage.stage_name,
        "mount_path": v_stage.mount_path,
    }
    optional_fields = {
        "vstage_namespace": v_stage.vstage_namespace,
        "vstage_version": v_stage.vstage_version,
        "is_vstage": v_stage.is_vstage,
        "readonly": v_stage.readonly,
        "encryption_type": v_stage.encryption_type,
    }
    data.update(
        {key: value for key, value in optional_fields.items() if value is not None}
    )
    return data


def _is_empty_stream_response(response: _StreamResponse) -> bool:
    return (
        not response.text.strip()
        and not response.thinking.strip()
        and not response.content
        and not response.tool_uses
        and not response.tool_results
    )


def _is_auth_expired_body(body: str | None) -> bool:
    if not body:
        return False
    return AUTH_EXPIRED_CODE_RE.search(body) is not None


class AgentApiTransport(Transport):
    """Transport that runs turns through Cortex Agent API instead of the CLI."""

    def __init__(self, options: CortexCodeAgentOptions):
        self._options = options
        self._session_id = options.session_id or ""
        self._api_options = options.api or AgentApiOptions()
        self._parent_message_id = self._api_options.parent_message_id
        self._created_thread = False
        self._active_run_id: str | None = None
        self._connection: _DirectConnection | None = None
        self._queue: asyncio.Queue[dict[str, Any] | None] | None = None
        self._messages: list[dict[str, Any]] = []
        self._ready = False
        self._closed = False
        self._run_lock = asyncio.Lock()
        self._run_task: asyncio.Task[None] | None = None
        self._active_run_interrupted = False
        self._active_stream_response: Any | None = None
        self._turn_count = 0
        self._result_text = ""
        self._aggregate_usage = _empty_usage()
        self._trace: _ApiTraceSink | None = _create_api_trace_sink(
            {
                **os.environ,
                **options.env,
            }
        )

    @property
    def pid(self) -> int | None:
        return None

    async def connect(self) -> None:
        if self._ready:
            return
        validate_api_mode_options(self._options)
        self._queue = asyncio.Queue()
        self._connection = _resolve_connection(self._options)
        if self._options.fork_session:
            await self._fork_thread()
        elif not self._session_id:
            await self._create_thread()
        elif self._parent_message_id is None:
            await self._resolve_parent_message_id_for_existing_thread()
        self._ready = True
        await self._put(self._build_init_message())

    async def write(self, data: str) -> None:
        if not self._ready:
            raise RuntimeError("API transport is not connected")
        for raw_line in data.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            message = json.loads(line)
            if message.get("type") == "control_request":
                await self._handle_control_request(message)
            elif message.get("type") == "user":
                self._messages.append(_to_api_user_message(message))
                if self._run_task is None or self._run_task.done():
                    self._run_task = asyncio.create_task(self._run_until_done())
            elif message.get("type") == "control_response":
                continue

    async def read_messages(self) -> AsyncIterator[dict[str, Any]]:
        if self._queue is None:
            self._queue = asyncio.Queue()
        while True:
            item = await self._queue.get()
            if item is None:
                break
            yield item

    async def close(self) -> None:
        self._closed = True
        if self._run_task is not None and not self._run_task.done():
            self._run_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._run_task
        if (
            self._api_options.delete_thread_on_close
            and self._created_thread
            and self._session_id
        ):
            with suppress(Exception):
                await self._delete_thread()
        if self._connection is not None and self._connection.close is not None:
            with suppress(Exception):
                self._connection.close()
        self._connection = None
        self._ready = False
        await self._put(None)

    def is_ready(self) -> bool:
        return self._ready

    async def end_input(self) -> None:
        # The Agent API request has already completed by the time Query calls
        # this for one-shot prompts; keep the transport open until close().
        return

    async def _handle_control_request(self, message: dict[str, Any]) -> None:
        request_id = str(message.get("request_id", ""))
        request = message.get("request", {})
        subtype = request.get("subtype")
        if subtype == "initialize":
            await self._control_success(request_id, self._initialization_response())
        elif subtype == "set_model":
            model = request.get("model")
            if isinstance(model, str) or model is None:
                self._options.model = model
            await self._control_success(request_id, {})
        elif subtype == "interrupt":
            if self._active_run_id is not None or (
                self._run_task is not None and not self._run_task.done()
            ):
                self._active_run_interrupted = True
            await self._cancel_active_run()
            await self._control_success(request_id, {})
        elif subtype == "set_permission_mode":
            await self._control_error(
                request_id,
                'API mode does not support permission_mode; use mode="cli" '
                "for plan and permission-mode controls",
            )
        elif isinstance(subtype, str) and subtype.startswith("mcp_"):
            await self._control_error(
                request_id,
                'API mode does not support MCP; use mode="cli" for MCP server controls',
            )
        else:
            await self._control_error(
                request_id,
                f"API mode does not support control request: {subtype}",
            )

    async def _control_success(self, request_id: str, response: dict[str, Any]) -> None:
        await self._put(
            {
                "type": "control_response",
                "response": {
                    "subtype": "success",
                    "request_id": request_id,
                    "response": response,
                },
            }
        )

    async def _control_error(self, request_id: str, error: str) -> None:
        await self._put(
            {
                "type": "control_response",
                "response": {
                    "subtype": "error",
                    "request_id": request_id,
                    "error": error,
                },
            }
        )

    async def _run_until_done(self) -> None:
        async with self._run_lock:
            started_at = time.monotonic()
            iterations = 0
            self._turn_count = 0
            self._result_text = ""
            self._aggregate_usage = _empty_usage()
            self._active_run_interrupted = False
            try:
                while not self._closed and iterations < MAX_API_ROUND_TRIPS:
                    iterations += 1
                    self._turn_count += 1
                    response = await self._call_agent_api()
                    if self._active_run_interrupted:
                        await self._put(
                            self._build_error_result(
                                started_at,
                                "error_during_execution",
                                ["Interrupted"],
                            )
                        )
                        return

                    assistant_message_id: str | None = None
                    for metadata in reversed(response.metadata):
                        if metadata.get("role") == "assistant":
                            assistant_message_id = metadata.get("message_id")
                            self._parent_message_id = assistant_message_id
                            break

                    _add_usage(self._aggregate_usage, response.usage)

                    if response.content:
                        if not assistant_message_id:
                            raise RuntimeError(
                                "API mode response missing assistant message_id metadata"
                            )
                        assistant = self._build_assistant_message(
                            response.content,
                            assistant_message_id,
                        )
                        await self._put(assistant)
                        self._messages.append(
                            {
                                "role": "assistant",
                                "content": [
                                    _to_api_assistant_content_block(block)
                                    for block in response.content
                                ],
                            }
                        )

                    if response.text:
                        self._result_text += response.text

                    if not response.tool_uses and not response.tool_results:
                        await self._put(self._build_success_result(started_at))
                        return

                    server_result_ids = {
                        tool_result.tool_use_id for tool_result in response.tool_results
                    }
                    tool_result_blocks: list[dict[str, Any]] = []
                    for tool_result in response.tool_results:
                        await self._put(
                            self._build_synthetic_tool_result_event(
                                tool_result.tool_use_id,
                                tool_result.content,
                                tool_result.is_error,
                            )
                        )

                    for tool_use in response.tool_uses:
                        if tool_use.id in server_result_ids:
                            continue
                        if tool_use.permission and tool_use.permission.get("options"):
                            decision = await self._resolve_server_permission(tool_use)
                            tool_result_blocks.append(
                                {
                                    "type": "permission_decision",
                                    "permission_decision": decision,
                                }
                            )
                            denied = decision["decision"] == "None"
                            reason = decision.get("reason", "user denied")
                            await self._put(
                                self._build_synthetic_tool_result_event(
                                    tool_use.id,
                                    f"(permission denied: {reason})"
                                    if denied
                                    else f"(permission granted: {decision['decision']})",
                                    denied,
                                )
                            )
                            continue

                        if tool_use.client_side_execute is False:
                            continue

                        result = _local_tool_execution_error(tool_use)
                        tool_result_blocks.append(
                            {
                                "type": "tool_result",
                                "tool_result": {
                                    "name": tool_use.name,
                                    "tool_use_id": tool_use.id,
                                    "status": "error",
                                    "content": [
                                        {"type": "text", "text": result["content"]}
                                    ],
                                },
                            }
                        )
                        await self._put(
                            self._build_synthetic_tool_result_event(
                                tool_use.id,
                                result["content"],
                                True,
                            )
                        )

                    if not tool_result_blocks:
                        await self._put(self._build_success_result(started_at))
                        return
                    self._messages.append(
                        {"role": "user", "content": tool_result_blocks}
                    )

                await self._put(
                    self._build_error_result(
                        started_at,
                        "error_during_execution",
                        [
                            "API mode exceeded internal round-trip limit "
                            f"({MAX_API_ROUND_TRIPS})"
                        ],
                    )
                )
            except asyncio.CancelledError:
                await self._put(
                    self._build_error_result(
                        started_at,
                        "error_during_execution",
                        ["Interrupted"],
                    )
                )
                raise
            except Exception as exc:
                await self._put(
                    self._build_error_result(
                        started_at,
                        "error_during_execution",
                        [str(exc)],
                    )
                )

    async def _call_agent_api(self, auth_retry_count: int = 0) -> _StreamResponse:
        if self._connection is None:
            raise RuntimeError("API transport is not connected")
        headers = self._build_headers()
        request_data = self._build_request_data()
        body = json.dumps(request_data).encode()
        self._trace_json(
            "agent-run-start-request",
            {
                "method": "POST",
                "url": self._connection.agent_url,
                "body": request_data,
            },
        )
        response = await asyncio.to_thread(
            _http_request,
            self._connection.agent_url,
            "POST",
            headers,
            body,
        )
        self._trace_json(
            "agent-run-start-response",
            {
                "method": "POST",
                "url": self._connection.agent_url,
                "status": response.status,
                "reason": response.reason,
                "body": response.body,
            },
        )
        if response.status < 200 or response.status >= 300:
            if await self._refresh_auth_and_retry(
                "agent_api_start_auth_expired",
                auth_retry_count,
                response.status,
                response.body,
            ):
                return await self._call_agent_api(auth_retry_count + 1)
            raise RuntimeError(
                f"Agent API request failed ({response.status}): "
                f"{response.body or response.reason}"
            )
        run_id, _user_message_id = _parse_agent_run_start_response(response.body)
        if not run_id:
            raise RuntimeError(
                f"Agent API start response missing run_id: {response.body}"
            )
        self._active_run_id = run_id
        try:
            stream_url = self._agent_run_stream_url(run_id)
            self._trace_json(
                "agent-run-stream-request",
                {
                    "method": "GET",
                    "url": stream_url,
                },
            )
            stream_response = await asyncio.to_thread(
                _http_stream_request,
                stream_url,
                self._build_stream_headers(),
                lambda: self._active_run_interrupted,
                self._set_active_stream_response,
            )
            self._trace_json(
                "agent-run-stream-response",
                {
                    "method": "GET",
                    "url": stream_url,
                    "status": stream_response.status,
                    "reason": stream_response.reason,
                    **(
                        {"body": stream_response.body}
                        if stream_response.status < 200 or stream_response.status >= 300
                        else {}
                    ),
                },
            )
            if stream_response.status < 200 or stream_response.status >= 300:
                if await self._refresh_auth_and_retry(
                    "agent_run_stream_auth_expired",
                    auth_retry_count,
                    stream_response.status,
                    stream_response.body,
                ):
                    return await self._call_agent_api(auth_retry_count + 1)
                raise RuntimeError(
                    f"Agent run stream failed ({stream_response.status}): "
                    f"{stream_response.body or stream_response.reason}"
                )
            try:
                parsed = _parse_response_body(
                    stream_response.body,
                    self._options.include_partial_messages,
                    self._handle_stream_metadata,
                )
            except RuntimeError as exc:
                if await self._refresh_auth_and_retry(
                    "agent_run_stream_auth_expired",
                    auth_retry_count,
                    None,
                    str(exc),
                ):
                    return await self._call_agent_api(auth_retry_count + 1)
                raise
            self._trace_text("agent-run-stream", "sse", parsed.raw_body or "")
            if _is_empty_stream_response(parsed) and await self._refresh_auth_and_retry(
                "agent_run_stream_auth_expired",
                auth_retry_count,
                None,
                parsed.raw_body,
            ):
                return await self._call_agent_api(auth_retry_count + 1)
            if self._options.include_partial_messages:
                for event in parsed.partial_events or []:
                    await self._put(
                        {
                            "type": "stream_event",
                            "event": event,
                            "parent_tool_use_id": None,
                            "uuid": str(uuid.uuid4()),
                            "session_id": self._session_id,
                        }
                    )
            return parsed
        finally:
            self._active_run_id = None

    def _trace_json(self, label: str, data: Mapping[str, Any]) -> None:
        if self._trace is not None:
            self._trace.write_json(label, data)

    def _trace_text(self, label: str, extension: str, data: str) -> None:
        if self._trace is not None:
            self._trace.write_text(label, extension, data)

    async def _refresh_auth_and_retry(
        self,
        reason: str,
        auth_retry_count: int,
        status: int | None,
        body: str | None,
    ) -> bool:
        if auth_retry_count >= MAX_AUTH_REFRESH_RETRIES:
            return False
        if status != 401 and not _is_auth_expired_body(body):
            return False
        if self._connection is None or self._connection.refresh is None:
            raise RuntimeError(
                "Snowflake authentication expired and this API mode connection "
                "cannot refresh automatically. Configure API mode with a "
                "Snowflake connection profile or api.token_provider."
            )
        await asyncio.to_thread(self._connection.refresh, reason)
        return True

    def _agent_run_stream_url(self, run_id: str) -> str:
        if self._connection is None:
            raise RuntimeError("API transport is not connected")
        return (
            f"{self._connection.protocol}://{self._connection.rest_url}"
            f"/api/v2/cortex/agent/runs/{run_id}"
        )

    async def _cancel_active_run(self) -> None:
        if self._connection is None or not self._active_run_id:
            return
        cancel_url = f"{self._agent_run_stream_url(self._active_run_id)}/cancel"
        self._trace_json(
            "agent-run-cancel-request",
            {
                "method": "POST",
                "url": cancel_url,
                "body": {},
            },
        )
        response = await asyncio.to_thread(
            _http_request,
            cancel_url,
            "POST",
            self._build_headers(),
            b"{}",
        )
        self._trace_json(
            "agent-run-cancel-response",
            {
                "method": "POST",
                "url": cancel_url,
                "status": response.status,
                "reason": response.reason,
                "body": response.body,
            },
        )
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(
                f"Agent run cancel failed ({response.status}): "
                f"{response.body or response.reason}"
            )
        assistant_message_id = _parse_agent_run_cancel_response(response.body)
        if assistant_message_id:
            self._parent_message_id = assistant_message_id
        self._close_active_stream_response()

    def _set_active_stream_response(self, response: Any | None) -> None:
        self._active_stream_response = response

    def _close_active_stream_response(self) -> None:
        response = self._active_stream_response
        if response is None:
            return
        fp = getattr(response, "fp", None)
        raw = getattr(fp, "raw", None)
        sock = getattr(raw, "_sock", None)
        if sock is not None:
            with suppress(Exception):
                sock.shutdown(socket.SHUT_RDWR)
            with suppress(Exception):
                sock.close()
        with suppress(Exception):
            response.close()

    def _handle_stream_metadata(self, metadata: dict[str, str]) -> None:
        if metadata.get("role") == "assistant" and metadata.get("message_id"):
            self._parent_message_id = metadata["message_id"]

    def _build_headers(self) -> dict[str, str]:
        if self._connection is None:
            raise RuntimeError("API transport is not connected")
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f'Snowflake Token="{self._connection.token}"',
            "User-Agent": "cortex_code_sdk/1.0.0",
        }

    def _build_stream_headers(self) -> dict[str, str]:
        if self._connection is None:
            raise RuntimeError("API transport is not connected")
        return {
            "Accept": "text/event-stream",
            "Authorization": f'Snowflake Token="{self._connection.token}"',
            "User-Agent": "cortex_code_sdk/1.0.0",
        }

    def _build_request_data(self) -> dict[str, Any]:
        if self._connection is None:
            raise RuntimeError("API transport is not connected")
        model = self._options.model or DEFAULT_MODEL
        tools = self._build_tools()
        experimental = self._build_experimental_settings(tools)
        messages = self._messages_for_request()
        request: dict[str, Any] = {
            "messages": messages,
            "model": model,
            "stream": False,
            "background": True,
            "origin_application": "coding_agent",
        }
        request["thread_id"] = self._session_id
        request["parent_message_id"] = self._parent_message_id or "0"

        if tools:
            request["tools"] = tools
            request["tool_choice"] = {"type": "auto"}
        request["experimental"] = experimental
        return request

    def _messages_for_request(self) -> list[dict[str, Any]]:
        if self._connection is None or not self._session_id:
            return self._messages
        return self._messages[-1:] if self._messages else []

    def _build_experimental_settings(
        self, tools: list[dict[str, Any]]
    ) -> dict[str, Any]:
        sandbox_enabled = _sandbox_enabled(self._options)
        sandbox_tools = self._sandbox_tools_setting(tools) if sandbox_enabled else None
        system_prompt, append_system_prompt = _resolve_system_prompts(self._options)

        experimental: dict[str, Any] = {
            "UseLegacyAnswersToolNames": False,
            "ResponseSchemaVersion": "v2",
            "EnableSingleAgentOrchestration": True,
            "EnableFunctionCallAPIForPlanning": True,
            "ReasoningAgentFlowType": "simple",
            "CodingAgent": self._build_coding_agent_settings(
                sandbox_enabled,
                sandbox_tools,
                system_prompt,
                append_system_prompt,
            ),
        }
        if self._options.effort:
            experimental["ThinkingEffort"] = self._options.effort
        if sandbox_enabled:
            experimental["CocoSandboxTools"] = sandbox_tools
        if self._api_options.v_stages:
            experimental["VStages"] = [
                _serialize_v_stage(v_stage) for v_stage in self._api_options.v_stages
            ]
        return experimental

    def _build_coding_agent_settings(
        self,
        sandbox_enabled: bool,
        sandbox_tools: str | None,
        system_prompt: str,
        append_system_prompt: str | None,
    ) -> dict[str, Any]:
        coding_agent: dict[str, Any] = {
            "UserID": self._connection.user if self._connection else "unknown",
            "SessionID": self._session_id,
            "Temperature": 1,
            "SystemPromptInternal": self._build_system_prompt_internal(
                sandbox_enabled,
                system_prompt,
                append_system_prompt,
            ),
            "SummarizationTriggerThreshold": 0.95,
            "PrivateMode": False,
            "OriginApplication": "cortex-code-cli",
            "OriginApplicationVersion": API_AGENT_VERSION,
            "Entrypoint": SDK_ENTRYPOINT,
            "SessionAccountLocators": [],
            "DisabledServerTools": DISABLED_SERVER_TOOLS,
        }

        if sandbox_enabled:
            coding_agent["SandboxEnable"] = True
            coding_agent["SandboxTools"] = sandbox_tools
            coding_agent["HeadlessSandboxClient"] = True

        return coding_agent

    def _build_system_prompt_internal(
        self,
        sandbox_enabled: bool,
        system_prompt: str,
        append_system_prompt: str | None,
    ) -> dict[str, Any]:
        client_prompt = self._client_prompt_for_request(
            sandbox_enabled,
            append_system_prompt,
        )
        working_directory = "/workspace" if sandbox_enabled else ""

        return {
            "Prompt": system_prompt,
            "Attributes": {
                "WorkingDirectory": working_directory,
                "AgentVersion": API_AGENT_VERSION,
                "AgentVersionLabel": API_AGENT_VERSION,
                "SnovaVersion": API_AGENT_VERSION,
                "AgentIdentity": "Cortex Code",
                "AgentDescription": "Cortex Code Agent SDK",
                "HelpInstructions": "",
                **({"ClientSystemPromptStr": client_prompt} if client_prompt else {}),
            },
            "FullOverride": bool(system_prompt),
        }

    def _client_prompt_for_request(
        self,
        sandbox_enabled: bool,
        append_system_prompt: str | None,
    ) -> str | None:
        parts = [
            append_system_prompt,
            SANDBOX_SQL_PROMPT if sandbox_enabled else None,
        ]
        return "\n\n".join(part for part in parts if isinstance(part, str) and part)

    def _build_tools(self) -> list[dict[str, Any]]:
        if not _sandbox_enabled(self._options):
            return []
        disallowed = {
            _normalize_tool_name(name) for name in self._options.disallowed_tools
        }
        return [
            {"tool_spec": {"type": name, "name": name}}
            for name in DEFAULT_TOOLS
            if _normalize_tool_name(name) not in disallowed
        ]

    def _sandbox_tools_setting(self, tools: list[dict[str, Any]]) -> str:
        if not self._options.disallowed_tools:
            return "*"
        names = [
            str(tool["tool_spec"]["name"])
            for tool in tools
            if isinstance(tool.get("tool_spec"), dict)
            and isinstance(tool["tool_spec"].get("name"), str)
            and tool["tool_spec"]["name"]
        ]
        return ",".join(names)

    async def _resolve_server_permission(
        self, tool_use: _ToolUseData
    ) -> dict[str, Any]:
        options = tool_use.permission["options"] if tool_use.permission else []
        deny_option = next(
            (
                option
                for option in options
                if option.lower() in {"none", "deny", "reject"}
            ),
            "None",
        )
        selected_decision = deny_option
        allowed = False
        reason: str | None = None

        if self._options.can_use_tool is not None:
            result = await self._options.can_use_tool(
                _display_tool_name(tool_use.name),
                {**_permission_input_for_tool(tool_use), "options": options},
                ToolPermissionContext(
                    signal=None,
                    suggestions=[],
                    blocked_path=None,
                    decision_reason=None,
                    tool_use_id=tool_use.id,
                    agent_id=None,
                ),
            )
            allowed = isinstance(result, PermissionResultAllow)
            if isinstance(result, PermissionResultDeny):
                reason = result.message
                selected_decision = deny_option
            elif isinstance(result, PermissionResultAllow):
                requested_decision = (
                    result.updated_input.get("decision")
                    if result.updated_input is not None
                    else None
                )
                if (
                    isinstance(requested_decision, str)
                    and requested_decision in options
                ):
                    selected_decision = requested_decision
                else:
                    allowed = False
                    selected_decision = deny_option

        return {
            "tool_use_id": tool_use.id,
            "decision": selected_decision if allowed else deny_option,
            **({"reason": reason} if reason else {}),
        }

    async def _fork_thread(self) -> None:
        source_thread_id = self._session_id
        if not source_thread_id:
            raise RuntimeError(
                "API mode fork_session requires session_id with the source Agent API thread ID"
            )
        artifact_id = await self._create_thread_artifact(
            source_thread_id,
            self._options.resume_session_at,
        )
        await self._create_thread(artifact_id)

    async def _create_thread_artifact(
        self, source_thread_id: str, source_message_id: str | None
    ) -> str:
        if self._connection is None:
            raise RuntimeError("API transport is not connected")
        url = (
            f"{self._connection.protocol}://{self._connection.rest_url}"
            "/api/v2/si/artifacts"
        )
        artifact: dict[str, Any] = {
            "type": "thread",
            "source_thread_id": source_thread_id,
            "spec": "{}",
            "data": "{}",
            "sql": "-- thread forked from Cortex Code SDK",
            "title": FORK_ARTIFACT_TITLE,
        }
        if source_message_id:
            artifact["source_message_id"] = source_message_id
        response = await asyncio.to_thread(
            _http_request,
            url,
            "POST",
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f'Snowflake Token="{self._connection.token}"',
            },
            json.dumps({"artifact": artifact}).encode(),
        )
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(
                f"Thread artifact creation failed ({response.status}): "
                f"{response.body or response.reason}"
            )
        artifact_id = _parse_artifact_creation_response(response.body)
        if not artifact_id:
            raise RuntimeError(
                f"Thread artifact creation response missing id: {response.body}"
            )
        return artifact_id

    async def _create_thread(self, artifact_id: str | None = None) -> None:
        if self._connection is None:
            return
        url = (
            f"{self._connection.protocol}://{self._connection.rest_url}"
            "/api/v2/cortex/threads"
        )
        request_body: dict[str, Any] = {"origin_application": "coding_agent"}
        if artifact_id:
            request_body["artifact_reference_ids"] = [artifact_id]
        response = await asyncio.to_thread(
            _http_request,
            url,
            "POST",
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f'Snowflake Token="{self._connection.token}"',
            },
            json.dumps(request_body).encode(),
        )
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(
                f"Thread creation failed ({response.status}): "
                f"{response.body or response.reason}"
            )
        thread_id, artifact_message_id = _parse_thread_creation_response(response.body)
        if not thread_id:
            raise RuntimeError(
                f"Thread creation response missing thread_id: {response.body}"
            )
        self._session_id = thread_id
        self._parent_message_id = artifact_message_id or self._parent_message_id
        self._created_thread = True

    async def _delete_thread(self) -> None:
        if self._connection is None or not self._session_id:
            return
        url = (
            f"{self._connection.protocol}://{self._connection.rest_url}"
            f"/api/v2/cortex/threads/{self._session_id}"
        )
        await asyncio.to_thread(
            _http_request,
            url,
            "DELETE",
            {
                "Accept": "application/json",
                "Authorization": f'Snowflake Token="{self._connection.token}"',
            },
            None,
        )

    async def _resolve_parent_message_id_for_existing_thread(
        self, auth_retry_count: int = 0
    ) -> None:
        if self._connection is None or not self._session_id:
            return
        url = (
            f"{self._connection.protocol}://{self._connection.rest_url}"
            f"/api/v2/cortex/threads/{self._session_id}"
        )
        self._trace_json(
            "thread-describe-request",
            {
                "method": "GET",
                "url": url,
                "threadId": self._session_id,
            },
        )
        response = await asyncio.to_thread(
            _http_request,
            url,
            "GET",
            {
                "Accept": "application/json",
                "Authorization": f'Snowflake Token="{self._connection.token}"',
            },
            None,
        )
        self._trace_json(
            "thread-describe-response",
            {
                "method": "GET",
                "url": url,
                "status": response.status,
                "reason": response.reason,
                "body": response.body,
            },
        )
        if await self._refresh_auth_and_retry(
            "thread_describe_auth_expired",
            auth_retry_count,
            response.status,
            response.body,
        ):
            await self._resolve_parent_message_id_for_existing_thread(
                auth_retry_count + 1
            )
            return
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(
                f"Thread describe failed ({response.status}): "
                f"{response.body or response.reason}"
            )
        latest_message_id = _parse_latest_thread_message_id(response.body)
        if latest_message_id is None:
            raise RuntimeError(
                f"Thread describe response for {self._session_id} did not include "
                "a timestamped latest assistant message id. Pass "
                "api.parent_message_id to choose the resume point explicitly."
            )
        self._parent_message_id = latest_message_id

    def _build_init_message(self) -> dict[str, Any]:
        return {
            "type": "system",
            "subtype": "init",
            "session_id": self._session_id,
            "uuid": str(uuid.uuid4()),
            "claude_code_version": "async-api",
            "cwd": "/workspace" if _sandbox_enabled(self._options) else "",
            "model": self._options.model or DEFAULT_MODEL,
            "tools": [
                tool["tool_spec"]["name"]
                for tool in self._build_tools()
                if isinstance(tool.get("tool_spec"), dict)
            ],
            "mcp_servers": [],
            "permissionMode": "default",
            "apiKeySource": (
                "simulator"
                if self._connection is not None and self._connection.is_local
                else "snowflake"
            ),
            "slash_commands": [],
            "output_style": "concise",
            "skills": [],
            "plugins": [],
        }

    def _initialization_response(self) -> dict[str, Any]:
        model = self._options.model or DEFAULT_MODEL
        return {
            "commands": [],
            "agents": [],
            "output_style": "concise",
            "models": [
                {
                    "value": model,
                    "displayName": model,
                    "description": "Configured model",
                }
            ],
            "account": {
                "apiKeySource": (
                    "simulator"
                    if self._connection is not None and self._connection.is_local
                    else "snowflake"
                ),
                "tokenSource": (
                    "simulator"
                    if self._connection is not None and self._connection.is_local
                    else "connection"
                ),
            },
        }

    def _build_assistant_message(
        self, content: list[dict[str, Any]], message_id: str
    ) -> dict[str, Any]:
        return {
            "type": "assistant",
            "content": content,
            "session_id": self._session_id,
            "parent_tool_use_id": None,
            "uuid": str(uuid.uuid4()),
            "message": {
                "id": message_id,
                "type": "message",
                "role": "assistant",
                "content": content,
                "model": self._options.model or DEFAULT_MODEL,
                "stop_reason": None,
                "stop_sequence": None,
                "usage": _empty_usage(),
            },
        }

    def _build_success_result(self, started_at: float) -> dict[str, Any]:
        structured_output = self._parse_structured_output()
        result: dict[str, Any] = {
            "type": "result",
            "subtype": "success",
            "session_id": self._session_id,
            "uuid": str(uuid.uuid4()),
            "duration_ms": int((time.monotonic() - started_at) * 1000),
            "is_error": False,
            "num_turns": self._turn_count,
            "result": (
                "Structured output provided successfully"
                if structured_output is not None
                else self._result_text
            ),
            "usage": dict(self._aggregate_usage),
            "modelUsage": {},
            "permission_denials": [],
        }
        if structured_output is not None:
            result["structured_output"] = structured_output
        return result

    def _build_error_result(
        self, started_at: float, subtype: str, errors: list[str]
    ) -> dict[str, Any]:
        return {
            "type": "result",
            "subtype": subtype,
            "session_id": self._session_id,
            "uuid": str(uuid.uuid4()),
            "duration_ms": int((time.monotonic() - started_at) * 1000),
            "is_error": True,
            "num_turns": self._turn_count,
            "usage": dict(self._aggregate_usage),
            "modelUsage": {},
            "permission_denials": [],
            "errors": errors,
        }

    def _build_synthetic_tool_result_event(
        self, tool_use_id: str, content: str, is_error: bool = False
    ) -> dict[str, Any]:
        block: dict[str, Any] = {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "content": content,
        }
        if is_error:
            block["is_error"] = True
        return {
            "type": "user",
            "session_id": self._session_id,
            "uuid": str(uuid.uuid4()),
            "parent_tool_use_id": None,
            "isSynthetic": True,
            "message": {"role": "user", "content": [block]},
        }

    def _parse_structured_output(self) -> Any:
        if not self._options.output_format:
            return None
        try:
            return json.loads(self._result_text.strip())
        except json.JSONDecodeError:
            return None

    async def _put(self, item: dict[str, Any] | None) -> None:
        if self._queue is None:
            self._queue = asyncio.Queue()
        await self._queue.put(item)
