import asyncio
import atexit
import threading
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, ClassVar, Literal, Optional, Union, overload

import aiohttp
from openreward.api._session.http import (
    RetryPolicy,
    _RemoteSSEError,
    _raise_for_status,
    request_retryable,
    resumable_sse,
    set_retry_policy,
)
from openreward.api._session.ping import ErrorResponse
from openreward.api._session.session import BaseAsyncSession, SessionKind, SessionTerminatedError
from openreward.api.errors import ToolCallError, ToolCallErrorReason, ToolFailed

BuiltinToolset = Literal["backsearch", "claude-code", "codex", "gemini-cli", "hermes", "openclaw"]
_VALID_BUILTIN_TOOLSETS = {"backsearch", "claude-code", "codex", "gemini-cli", "hermes", "openclaw"}
from .types import (
    ImageBlock,
    JSONObject,
    JSONValue,
    Mapping,
    Provider,
    ResponseChars,
    Server,
    Task,
    TaskDifficulty,
    TerminalToolSpec,
    TextBlock,
    ToolOutput,
    ToolSpec,
)
from openreward.models import TrainingStage
from openreward.api.sandboxes.secrets import build_secrets_header, augment_secrets_with_api_key

GOOGLE_UNSUPPORTED_SCHEMA_KEYS = {
    "additionalProperties",      # JSON Schema
    "additional_properties",     # sometimes appears already converted
    "title",                     # you already strip, but keep it here too
    "default",                   # often unsupported in function schemas
    "examples",
    "example",
    "patternProperties",
    "oneOf",
    "allOf",
    "anyOf",
    "not",
}

OPENAI_UNSUPPORTED_SCHEMA_KEYS = {
    "additionalProperties",
    "patternProperties",
    "oneOf",
    "allOf",
    "anyOf",
    "not",
}

def _sanitize_google_schema(x: Any) -> Any:
    """Recursively remove schema keys that Gemini/Google function calling rejects."""
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            if k in GOOGLE_UNSUPPORTED_SCHEMA_KEYS:
                continue
            if k == "$ref":
                k = "ref"
            elif k == "$defs":
                k = "defs"
            out[k] = _sanitize_google_schema(v)
        return out
    if isinstance(x, list):
        return [_sanitize_google_schema(i) for i in x]
    return x

def _fix_array_schemas(obj: Any) -> Any:
    """Recursively add missing 'items' to array schemas (required by OpenAI)."""
    if isinstance(obj, list):
        return [_fix_array_schemas(v) for v in obj]
    if not isinstance(obj, dict):
        return obj
    obj = {k: _fix_array_schemas(v) for k, v in obj.items()}
    t = obj.get("type")
    is_array = t == "array" or (isinstance(t, list) and "array" in t)
    if is_array and "items" not in obj:
        obj["items"] = {}
    return obj

def _sanitize_openai_schema(x: Any) -> Any:
    """
    Recursively sanitize schema for OpenAI function calling.

    - Collapses anyOf/oneOf/allOf into a single option (first non-null for
      anyOf, first entry otherwise) while preserving sibling metadata such as
      description/default/title on the enclosing schema.
    - Removes unsupported keywords (additionalProperties, patternProperties,
      not, etc.)
    - Ensures array types have 'items' field
    """
    if isinstance(x, dict):
        for key in ("anyOf", "oneOf", "allOf"):
            if key not in x:
                continue
            options = x[key]
            if not options:
                continue
            chosen = None
            if key == "anyOf":
                for option in options:
                    if not (isinstance(option, dict) and option.get("type") == "null"):
                        chosen = option
                        break
            if chosen is None:
                chosen = options[0]
            siblings = {k: v for k, v in x.items() if k != key}
            if isinstance(chosen, dict):
                merged = {**siblings, **chosen}
            else:
                return _sanitize_openai_schema(chosen)
            return _sanitize_openai_schema(merged)

        out = {}
        for k, v in x.items():
            if k in OPENAI_UNSUPPORTED_SCHEMA_KEYS:
                continue
            out[k] = _sanitize_openai_schema(v)

        if out.get("type") == "array" and "items" not in out:
            out["items"] = {}

        return out

    if isinstance(x, list):
        return [_sanitize_openai_schema(i) for i in x]

    return x

def _strip_titles(value: Any) -> Any:
    """Recursively remove JSON schema `title` keys."""
    if isinstance(value, dict):
        return {
            k: _strip_titles(v)
            for k, v in value.items()
            if k != "title"
        }
    if isinstance(value, list):
        return [_strip_titles(item) for item in value]
    return value


def sanitize_tool_schema(
    schema: Optional[Mapping[str, Any]],
    provider: Provider,
) -> dict[str, Any]:
    """Sanitize a JSON Schema for a given provider's function-calling API.

    Strips ``title`` keys and applies provider-specific fixups:

    - ``openai``/``openrouter``: collapse anyOf/oneOf/allOf, drop unsupported
      keywords (``additionalProperties``, ``patternProperties``, ``not``), and
      default missing ``items`` on array types.
    - ``anthropic``: strip titles only (Anthropic accepts standard JSON Schema).
    - ``google``: drop Gemini-unsupported keys and rename ``$ref``/``$defs``.

    Returns ``{}`` when ``schema`` is ``None`` or empty, so callers can safely
    spread the result (``ToolParams(**sanitize_tool_schema(...))``).
    """
    if not schema:
        return {}
    stripped = _strip_titles(schema)
    if provider in ("openai", "openrouter"):
        return _fix_array_schemas(_sanitize_openai_schema(stripped))
    if provider == "anthropic":
        return stripped
    if provider == "google":
        return _sanitize_google_schema(stripped)
    raise ValueError(f"Invalid provider: {provider!r}")


def parse_terminal_tool(res: Mapping[str, Any]) -> Optional[TerminalToolSpec]:
    """Read the terminal-tool descriptor out of a ``/tools`` response.

    Returns None both when the environment has no ``@terminal`` tool and when
    the env server predates the field.
    """
    raw = res.get("terminal_tool")
    if not raw:
        return None
    return TerminalToolSpec(
        name=raw["name"],
        arg=raw.get("arg"),
        description=raw.get("description", ""),
    )


@overload
def convert_tool_response(res: Mapping[str, Any], format: None = None) -> list[ToolSpec]: ...

@overload
def convert_tool_response(res: Mapping[str, Any], format: Provider = ...) -> list[dict[str, Any]]: ...

def convert_tool_response(
    res: Mapping[str, Any],
    format: Optional[Provider] = None,
) -> Union[list[ToolSpec], list[dict[str, Any]]]:
    if format is None:
        return [ToolSpec(**tool) for tool in res["tools"]]

    if format not in ("openai", "openrouter", "anthropic", "google"):
        raise ValueError(f"Invalid format: {format!r}")

    out: list[dict[str, Any]] = []
    for tool in res["tools"]:
        raw_schema = tool.get("input_schema")
        sanitized = sanitize_tool_schema(raw_schema, format)
        meta = {
            k: _strip_titles(v)
            for k, v in tool.items()
            if k not in {"input_schema", "title"}
        }

        if format == "openai":
            out.append({
                "type": "function",
                **meta,
                "parameters": sanitized if raw_schema else None,
            })
        elif format == "openrouter":
            out.append({
                "type": "function",
                "function": meta,
                "parameters": sanitized if raw_schema else None,
            })
        elif format == "anthropic":
            out.append({
                "type": "custom",
                **meta,
                "input_schema": sanitized if raw_schema else {"type": "object", "properties": {}},
            })
        else:  # google
            out.append({
                **meta,
                "parameters": sanitized if raw_schema else None,
            })

    return out

def _validate_toolset_name(toolset: Optional[str]) -> Optional[str]:
    """Validate that *toolset* is a known built-in toolset name."""
    if toolset is None:
        return None
    if toolset not in _VALID_BUILTIN_TOOLSETS:
        raise ValueError(
            f"Unknown toolset {toolset!r}; "
            f"valid options: {sorted(_VALID_BUILTIN_TOOLSETS)}"
        )
    return toolset


_VALID_REASONS: set[str] = {"not_found", "name_collision", "input_validation", "bad_input_shape"}


def _infer_invalid_reason(error: str) -> ToolCallErrorReason:
    """Fallback for servers that don't populate RunToolError.reason.

    The reason field shipped alongside this client; older servers return
    only the human message. Match on the known prefixes so we still emit
    a useful discriminator. Defaults to 'not_found' when nothing matches.
    """
    if error.startswith("Tool name collision"):
        return "name_collision"
    if error.startswith("Tool input validation error"):
        return "input_validation"
    if "is not a valid tool" in error:
        return "not_found"
    return "not_found"


@asynccontextmanager
async def matrix_sid_provider(client: aiohttp.ClientSession, server_name: str, token: Optional[str]) -> AsyncGenerator[str, None]:
    """Ephemeral SID provider using SSE-based /create_session, cleanup via /delete."""
    sid: Optional[str] = None

    def on_event(event: str, data: str) -> None:
        nonlocal sid
        if event == "task_id":
            sid = data.strip()

    await resumable_sse(
        client,
        "/create_session",
        token=token,
        deployment=server_name,
        max_retries=3,
        on_event=on_event,
    )

    assert sid is not None, "No SID returned from /create_session"
    try:
        yield sid
    finally:
        try:
            await request_retryable(client, "POST", "/delete_session", sid=sid, expect_json=False, token=token)
        except Exception:
            pass


class AsyncSession(BaseAsyncSession):
    _session_kind: ClassVar[SessionKind] = "environment"
    _retry_policy: ClassVar[RetryPolicy] = "env-server"

    def __init__(
        self,
        env: "AsyncEnvironment",
        task: Optional[Task] = None,
        secrets: Optional[Mapping[str, Union[str, tuple[str, list[str]]]]] = None,
        api_key: Optional[str] = None,
        split: Optional[str] = None,
        index: Optional[int] = None,
        toolset_name: Optional[str] = None,
        env_overrides: Optional[Mapping[str, str]] = None,
    ):
        has_task = task is not None
        has_index = split is not None and index is not None
        if has_task == has_index:
            raise ValueError("Provide either task or both split and index, not both/neither")
        if (split is None) != (index is None):
            raise ValueError("split and index must both be provided together")

        secrets = augment_secrets_with_api_key(
            secrets, api_key,
            base_url=str(env.client._base_url),
            api_base_url=str(env.api_client._base_url) if env.api_client else None,
        )

        creation_headers: Optional[dict[str, str]] = None
        if secrets:
            creation_headers = {"X-Secrets": build_secrets_header(secrets)}

        creation_payload: dict[str, Any] = {}
        if env_overrides:
            creation_payload["env"] = dict(env_overrides)

        super().__init__(
            base_url=str(env.client._base_url),
            api_key=api_key,
            creation_endpoint="/create_session",
            creation_payload=creation_payload,
            deployment=env.deployment_name,
            client=env.client,
            creation_headers=creation_headers,
        )

        self._secrets_headers = creation_headers
        self.env = env
        self.task = task
        self.split = split
        self.index = index
        self.toolset_name = toolset_name

        self._has_task_tools: bool = True
        self._terminal_tool: Optional[TerminalToolSpec] = None
        self._terminal_tool_fetched: bool = False

    def _env_path(self, suffix: str) -> str:
        """Build URL path, matching AsyncEnvironment's routing pattern.

        When variant is None, uses bare path (redirect middleware handles it).
        When variant is set, prefixes with the variant name.
        """
        if self.env.variant is None:
            return suffix
        return f"/{self.env.variant}{suffix}"

    async def _post_create(self) -> None:
        """POST /create with task payload after SID is obtained."""
        create_payload: dict[str, Any] = {}
        if self.task is not None:
            create_payload["task_spec"] = self.task.task_spec
            create_payload["env_name"] = self.task.environment_name
        else:
            create_payload["split"] = self.split
            create_payload["index"] = self.index
            if self.env.variant is not None:
                create_payload["env_name"] = self.env.variant
        if self.toolset_name is not None:
            create_payload["toolset_name"] = self.toolset_name

        await request_retryable(
            self.client,
            "POST",
            "/create",
            expect_json=True,
            sid=self.sid,
            deployment=self.deployment,
            json=create_payload,
            token=self.api_key,
            extra_headers=self._secrets_headers,
        )

    async def _pre_delete(self) -> None:
        """POST /delete to tear down the environment on the server."""
        if self.sid:
            await request_retryable(
                self.client,
                "POST",
                "/delete",
                expect_json=False,
                sid=self.sid,
                token=self.api_key,
                )

    async def version(self) -> dict[str, Optional[str]]:
        return await self._run_or_die(
            request_retryable(
                self.client,
                "GET",
                "/version",
                expect_json=True,
                sid=self.sid,
                deployment=self.deployment,
                token=self.api_key,
                )
        )

    async def get_prompt(self) -> list[Union[TextBlock, ImageBlock]]:
        res = await self._run_or_die(
            request_retryable(
                self.client,
                "GET",
                self._env_path("/prompt"),
                expect_json=True,
                sid=self.sid,
                deployment=self.deployment,
                token=self.api_key,
                )
        )
        blocks: list[Union[TextBlock, ImageBlock]] = []
        for block in res:
            if block["type"] == "text":
                blocks.append(TextBlock(text=block["text"], detail=block["detail"]))
            elif block["type"] == "image":
                blocks.append(ImageBlock(mimeType=block["mimeType"], detail=block["detail"], data=block["data"]))
        return blocks

    @overload
    async def list_tools(self, format: None = None) -> list[ToolSpec]: ...

    @overload
    async def list_tools(self, format: Provider) -> list[dict]: ...

    async def list_tools(self, format: Optional[Provider] = None) -> Union[list[ToolSpec], list[dict]]:
        if self._has_task_tools:
            try:
                res = await self._run_or_die(
                    request_retryable(
                        self.client,
                        "GET",
                        self._env_path("/task_tools"),
                        expect_json=True,
                        sid=self.sid,
                        deployment=self.deployment,
                        token=self.api_key,
                                )
                )
                self._terminal_tool = parse_terminal_tool(res)
                return convert_tool_response(res, format=format)
            except aiohttp.ClientResponseError as e:
                if e.status == 404:
                    self._has_task_tools = False
                else:
                    raise
        res = await self._run_or_die(
            request_retryable(
                self.client,
                "GET",
                self._env_path("/tools"),
                expect_json=True,
                sid=self.sid,
                deployment=self.deployment,
                token=self.api_key,
                )
        )
        self._terminal_tool = parse_terminal_tool(res)
        return convert_tool_response(res, format=format)

    async def terminal_tool(self) -> Optional[TerminalToolSpec]:
        """The environment's terminal tool, or None if it has none.

        Fetches the tool list on first use and caches the result for the
        lifetime of the session (an environment's terminal tool is static).
        """
        if not self._terminal_tool_fetched:
            await self.list_tools()
            self._terminal_tool_fetched = True
        return self._terminal_tool

    async def is_assistant_message_final(self) -> bool:
        """True when a plain assistant message should end the rollout.

        Environments that declare a ``@terminal`` tool expect the model to
        write its answer as an ordinary message rather than call a submit-style
        tool. When this returns True, a harness that receives an assistant
        message with no tool calls should pass its text to
        :meth:`call_terminal_tool` and stop.
        """
        return (await self.terminal_tool()) is not None

    async def call_terminal_tool(self, message: str = "") -> ToolOutput:
        """Call the environment's terminal tool with *message*.

        A terminal tool that takes no arguments is called with none, and
        *message* is ignored. Raises ``ToolCallError`` if the environment has
        no terminal tool.
        """
        term = await self.terminal_tool()
        if term is None:
            raise ToolCallError(
                reason="not_found",
                detail=f"Environment {self.deployment!r} has no @terminal tool",
            )
        return await self.call_tool(term.name, {} if term.arg is None else {term.arg: message})

    async def call_tool(self, tool_name: str, input: JSONObject = {}) -> ToolOutput:
        if not isinstance(input, Mapping):
            raise ToolCallError(
                reason="bad_input_shape",
                detail=f"Tool input must be a dictionary, got {type(input).__name__}",
            )

        if not all(isinstance(k, str) for k in input.keys()):
            non_string_keys = [k for k in input.keys() if not isinstance(k, str)]
            raise ToolCallError(
                reason="bad_input_shape",
                detail=f"All keys in tool input must be strings. Found non-string keys: {non_string_keys}",
            )

        try:
            res = await self._run_or_die(
                resumable_sse(
                    self.client,
                    self._env_path("/call"),
                    sid=self.sid,
                    deployment=self.deployment,
                    token=self.api_key,
                    json={"name": tool_name, "input": input},
                    max_retries=5,
                )
            )
        except _RemoteSSEError as e:
            # The server's @tool raised, or returned a non-ToolOutput.
            # Tools are expected to handle their own retrying; any
            # escaped exception terminates the rollout — mark the
            # session dead so subsequent calls raise SessionDead.
            self._mark_dead(ErrorResponse(type="error", message=str(e)))
            raise ToolFailed(str(e)) from e

        if res["ok"]:
            blocks: list[Union[TextBlock, ImageBlock]] = []
            for block in res["output"]["blocks"]:
                if block["type"] == "text":
                    blocks.append(TextBlock(
                        text=block["text"],
                        detail=block["detail"]
                    ))
                elif block["type"] == "image":
                    blocks.append(ImageBlock(
                        mimeType=block["mimeType"],
                        detail=block["detail"],
                        data=block["data"]
                    ))
            return ToolOutput(
                blocks=blocks,
                metadata=res["output"]["metadata"],
                reward=res["output"]["reward"],
                finished=res["output"]["finished"]
            )

        server_reason = res.get("reason")
        reason: ToolCallErrorReason
        if server_reason in _VALID_REASONS:
            reason = server_reason  # type: ignore[assignment]
        else:
            reason = _infer_invalid_reason(res["error"])
        raise ToolCallError(reason=reason, detail=res["error"])


class AsyncEnvironment:

    def __init__(
        self,
        namespace: Optional[str],
        name: str,
        variant: Optional[str],
        client: aiohttp.ClientSession,
        api_key: Optional[str],
        api_client: Optional[aiohttp.ClientSession] = None,
    ) -> None:

        self.server = name
        self.namespace = namespace
        self.name = name
        self.variant = variant
        self.client = client
        self.api_key = api_key
        self.api_client = api_client

    @property
    def deployment_name(self) -> str:
        if self.namespace is None:
            return self.name
        else:
            return f"{self.namespace}/{self.name}"

    async def list_splits(self) -> list[str]:
        async with matrix_sid_provider(self.client, self.deployment_name, self.api_key) as sid:
            path = "/splits" if self.variant is None else f"/{self.variant}/splits"
            res = await request_retryable(self.client, "GET", path, expect_json=True, sid=sid, deployment=self.deployment_name, token=self.api_key)
            return [s["name"] for s in res]

    async def list_tasks(self, split: str) -> list[Task]:
        async with matrix_sid_provider(self.client, self.deployment_name, self.api_key) as sid:
            path = "/tasks" if self.variant is None else f"/{self.variant}/tasks"
            res = await request_retryable(self.client, "POST", path, expect_json=True, sid=sid, deployment=self.deployment_name, json={"split": split}, token=self.api_key)
            return [Task(server_name=self.server, environment_name=res["env_name"], task_spec=task, namespace=self.namespace) for task in res["tasks"]]

    async def num_tasks(self, split: str) -> int:
        """Get the number of tasks for a given split."""
        async with matrix_sid_provider(self.client, self.deployment_name, self.api_key) as sid:
            path = "/num_tasks" if self.variant is None else f"/{self.variant}/num_tasks"
            res = await request_retryable(self.client, "POST", path, expect_json=True, sid=sid, deployment=self.deployment_name, json={"split": split}, token=self.api_key)
            return res["num_tasks"]

    async def get_task(self, split: str, index: int) -> Task:
        """Get a single task by split and index."""
        async with matrix_sid_provider(self.client, self.deployment_name, self.api_key) as sid:
            path = "/task" if self.variant is None else f"/{self.variant}/task"
            res = await request_retryable(self.client, "POST", path, expect_json=True, sid=sid, deployment=self.deployment_name, json={"split": split, "index": index}, token=self.api_key)
            return Task(server_name=self.server, environment_name=res["env_name"], task_spec=res["task"], namespace=self.namespace)

    async def get_task_range(self, split: str, start: Optional[int] = None, stop: Optional[int] = None) -> list[Task]:
        """Get tasks for indices in range(start, stop). Supports negative and None indices."""
        async with matrix_sid_provider(self.client, self.deployment_name, self.api_key) as sid:
            path = "/task_range" if self.variant is None else f"/{self.variant}/task_range"
            payload: dict[str, Any] = {"split": split}
            if start is not None:
                payload["start"] = start
            if stop is not None:
                payload["stop"] = stop
            res = await request_retryable(self.client, "POST", path, expect_json=True, sid=sid, deployment=self.deployment_name, json=payload, token=self.api_key)
            return [Task(server_name=self.server, environment_name=res["env_name"], task_spec=task, namespace=self.namespace) for task in res["tasks"]]

    async def list_tools(self, format: Optional[Provider] = None) -> Union[list[ToolSpec], list[dict]]:
        return convert_tool_response(await self._tools_response(), format=format)

    async def _tools_response(self) -> Mapping[str, Any]:
        path = "/tools" if self.variant is None else f"/{self.variant}/tools"
        async with matrix_sid_provider(self.client, self.deployment_name, self.api_key) as sid:
            return await request_retryable(self.client, "GET", path, expect_json=True, sid=sid, deployment=self.deployment_name, token=self.api_key)

    async def terminal_tool(self) -> Optional[TerminalToolSpec]:
        """The environment's ``@terminal`` tool, or None if it has none."""
        return parse_terminal_tool(await self._tools_response())

    async def is_assistant_message_final(self) -> bool:
        """True when a plain assistant message ends a rollout in this environment.

        See :meth:`AsyncSession.is_assistant_message_final`; prefer the session
        method inside a rollout, since it reuses the session's cached tool list
        and accounts for any session toolset.
        """
        return (await self.terminal_tool()) is not None

    async def get_prompt(self, task: Task) -> str:
        async with matrix_sid_provider(self.client, task.deployment_name, self.api_key) as sid:
            path = "/prompt" if self.variant is None else f"/{self.variant}/prompt"
            res = await request_retryable(self.client, "GET", path, expect_json=True, sid=sid, deployment=task.deployment_name, token=self.api_key)
            return res

    def session(
        self,
        task: Optional[Task] = None,
        secrets: Optional[Mapping[str, Union[str, tuple[str, list[str]]]]] = None,
        *,
        split: Optional[str] = None,
        index: Optional[int] = None,
        toolset: Optional[BuiltinToolset] = None,
        env_overrides: Optional[Mapping[str, str]] = None,
    ) -> AsyncSession:
        """Create a session from a Task object or from split/index.

        ``toolset`` is the name of a built-in toolset (e.g. ``"claude-code"``
        or ``"codex"``). The session forwards the name to the server, which
        instantiates the toolset bound to the per-session environment. Tools
        defined on the bound toolset override any same-named tool from the
        environment or its declared toolsets.

        ``env_overrides`` overrides environment variables on the main
        container at session-create time. Owners of the environment may
        override any key; other callers are restricted to
        ``OPENAI_BASE_URL``, ``OPENAI_API_KEY``, ``ANTHROPIC_BASE_URL``,
        ``ANTHROPIC_API_KEY`` and get a 400 for any other key.
        """
        toolset_name = _validate_toolset_name(toolset)
        return AsyncSession(
            self,
            task=task,
            secrets=secrets,
            api_key=self.api_key,
            split=split,
            index=index,
            toolset_name=toolset_name,
            env_overrides=env_overrides,
        )

    async def list_required_secrets(self) -> list[str]:
        """Get the list of secret keys required by this environment."""
        if self.api_client is None:
            raise RuntimeError("API base URL not configured; cannot fetch required secrets")
        owner = self.namespace or ""
        path = f"/v1/environments/{owner}/{self.name}/required-secrets"
        headers: dict[str, str] = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        async with self.api_client.get(path, headers=headers) as resp:
            await _raise_for_status(resp)
            data = await resp.json()
            return data["secrets"]

    async def get_task_difficulty(
        self,
        *,
        split: Optional[str] = None,
        model_name: Optional[str] = None,
        min_model_params: Optional[int] = None,
        max_model_params: Optional[int] = None,
        training_stage: Optional[TrainingStage] = None,
    ) -> list[TaskDifficulty]:
        """Get per-task difficulty (avg/min/max reward + rollout count) and
        response-length stats for this environment.

        Aggregates the rewards of logged rollouts (see
        :class:`~openreward.api.rollouts.rollout.RolloutAPI`), grouped by
        ``(split, variant, task_index)``. Each group also carries
        ``response_chars`` — character-length percentiles of model-generated
        content (assistant + tool-call args + reasoning), summed per rollout
        then taken across the group's rollouts (see
        :class:`~openreward.api.environments.types.ResponseChars`). The data is
        served from a materialized view, so freshness depends on its
        server-side refresh.

        When this environment was obtained with a ``variant`` (e.g.
        ``client.environments.get("owner/name", variant="v1")``), results are
        scoped to that variant — mirroring :meth:`list_tasks`. An environment
        without a variant returns rows across all variants.

        Args:
            split: Restrict to a single split. ``None`` aggregates across all
                splits (each split is returned as its own rows).
            model_name: Restrict to rollouts logged under this model name.
            min_model_params: Restrict to rollouts whose ``model_params`` is at
                least this value.
            max_model_params: Restrict to rollouts whose ``model_params`` is at
                most this value.
            training_stage: Restrict to ``"pretrained"``, ``"sft"`` or ``"rl"``.

        Returns:
            A list of :class:`~openreward.api.environments.types.TaskDifficulty`,
            one per ``(split, variant, task_index)`` group, ordered by split
            (nulls first), variant (nulls first), then task index.
        """
        if self.api_client is None:
            raise RuntimeError("API base URL not configured; cannot fetch task difficulty")
        if not self.namespace:
            raise ValueError(
                "Task difficulty is keyed by environment owner; "
                f"environment {self.name!r} has no namespace. Reference it as "
                '"owner/name" (e.g. client.environments.get("owner/name")).'
            )
        path = f"/v1/environments/{self.namespace}/{self.name}/task-difficulty"
        headers: dict[str, str] = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        params: dict[str, str] = {}
        if self.variant is not None:
            params["variant"] = self.variant
        if split is not None:
            params["split"] = split
        if model_name is not None:
            params["model_name"] = model_name
        if min_model_params is not None:
            params["min_model_params"] = str(min_model_params)
        if max_model_params is not None:
            params["max_model_params"] = str(max_model_params)
        if training_stage is not None:
            params["training_stage"] = training_stage
        async with self.api_client.get(path, headers=headers, params=params) as resp:
            await _raise_for_status(resp)
            data = await resp.json()
        return [
            TaskDifficulty(
                task_index=t["task_index"],
                avg_reward=t["avg_reward"],
                min_reward=t["min_reward"],
                max_reward=t["max_reward"],
                num_rollouts=t["num_rollouts"],
                response_chars=ResponseChars(**t["response_chars"]),
                split=t["split"],
                variant=t["variant"],
            )
            for t in data["tasks"]
        ]


class AsyncEnvironmentsAPI:

    def __init__(
        self,
        base_url: str,
        api_key: str,
        api_base_url: Optional[str] = None,
    ):
        self.api_key = api_key

        self.base_url = base_url
        self.api_base_url = api_base_url
        self.timeout = aiohttp.ClientTimeout(total=None)

        # Lazily initialized - connector requires a running event loop
        self._connector: Optional[aiohttp.TCPConnector] = None
        self._clients: dict[str, aiohttp.ClientSession] = {}

    def _get_connector(self) -> aiohttp.TCPConnector:
        """Lazily create the connector when inside a running event loop."""
        if self._connector is None or self._connector.closed:
            self._connector = aiohttp.TCPConnector(limit=1_000_000)
        return self._connector

    def get(self, name: str, variant: Optional[str] = None, base_url: Optional[str] = None) -> AsyncEnvironment:

        parts = name.split("/", maxsplit=1)
        namespace = None
        if len(parts) == 1:
            env_name = parts[0]
        elif len(parts) == 2:
            namespace, env_name = parts
        else:
            raise RuntimeError("impossible")

        if namespace and self.api_key is None:
            raise ValueError(f"Expected api_key to be passed when accessing remote environment")

        if base_url is None:
            base_url = self.base_url

        if base_url not in self._clients:
            self._clients[base_url] = aiohttp.ClientSession(
                base_url=base_url,
                timeout=self.timeout,
                connector=self._get_connector(),
                trust_env=True,
            )
            # base_url here is the env-server host (sessions.openreward.ai
            # or equivalent). Tag so the SDK uses the narrow retry policy
            # — env-server 500s come from ErrorHandlingMiddleware catching
            # an unhandled user-code exception and won't recover on retry.
            set_retry_policy(self._clients[base_url], "env-server")
        client = self._clients[base_url]

        api_client = None
        if self.api_base_url:
            if self.api_base_url not in self._clients:
                self._clients[self.api_base_url] = aiohttp.ClientSession(
                    base_url=self.api_base_url,
                    timeout=self.timeout,
                    connector=self._get_connector(),
                    trust_env=True,
                )
                # Platform API. Default "api" retry policy already applies;
                # left untagged for clarity.
            api_client = self._clients[self.api_base_url]

        return AsyncEnvironment(
            namespace=namespace,
            name=env_name,
            variant=variant,
            client=client,
            api_key=self.api_key,
            api_client=api_client,
        )

    async def aclose(self) -> None:
        """Close all aiohttp sessions and the shared connector.

        Sleeps briefly after closing to let aiohttp's connector finish its
        graceful-shutdown task (``_wait_for_close``). Without this, the task
        can be left pending when the event loop tears down, producing an
        ``ERROR Task was destroyed but it is pending!`` log at exit.
        """
        for client in self._clients.values():
            if not client.closed:
                await client.close()
        self._clients.clear()
        if self._connector is not None and not self._connector.closed:
            await self._connector.close()
            self._connector = None
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.25)

    async def __aenter__(self) -> "AsyncEnvironmentsAPI":
        return self

    async def __aexit__(self, *exc) -> None:
        await self.aclose()


class Session:
    """Synchronous wrapper around AsyncSession."""

    def __init__(self, async_session: AsyncSession, loop: asyncio.AbstractEventLoop):
        self._async = async_session
        self._loop = loop

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    @property
    def sid(self) -> Optional[str]:
        return self._async.sid

    @property
    def task(self) -> Optional[Task]:
        return self._async.task

    def __enter__(self) -> "Session":
        self._run(self._async.__aenter__())
        return self

    def __exit__(self, *exc):
        self._run(self._async.__aexit__(*exc))

    def version(self) -> dict[str, Optional[str]]:
        return self._run(self._async.version())

    def get_prompt(self) -> list[Union[TextBlock, ImageBlock]]:
        return self._run(self._async.get_prompt())

    @overload
    def list_tools(self, format: None = None) -> list[ToolSpec]: ...

    @overload
    def list_tools(self, format: Provider) -> list[dict]: ...

    def list_tools(self, format: Optional[Provider] = None) -> Union[list[ToolSpec], list[dict]]:
        return self._run(self._async.list_tools(format))

    def terminal_tool(self) -> Optional[TerminalToolSpec]:
        """The environment's terminal tool, or None if it has none."""
        return self._run(self._async.terminal_tool())

    def is_assistant_message_final(self) -> bool:
        """True when a plain assistant message should end the rollout.

        See :meth:`AsyncSession.is_assistant_message_final`.
        """
        return self._run(self._async.is_assistant_message_final())

    def call_terminal_tool(self, message: str = "") -> ToolOutput:
        """Call the environment's terminal tool with *message*."""
        return self._run(self._async.call_terminal_tool(message))

    def call_tool(self, tool_name: str, input: JSONObject = {}) -> ToolOutput:
        return self._run(self._async.call_tool(tool_name, input))


class Environment:
    """Synchronous wrapper around AsyncEnvironment."""

    def __init__(self, async_env: AsyncEnvironment, loop: asyncio.AbstractEventLoop):
        self._async = async_env
        self._loop = loop

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    @property
    def server(self) -> str:
        return self._async.server

    @property
    def namespace(self) -> Optional[str]:
        return self._async.namespace

    @property
    def name(self) -> str:
        return self._async.name

    @property
    def variant(self) -> Optional[str]:
        return self._async.variant

    @property
    def deployment_name(self) -> str:
        return self._async.deployment_name

    def list_splits(self) -> list[str]:
        return self._run(self._async.list_splits())

    def list_tasks(self, split: str) -> list[Task]:
        return self._run(self._async.list_tasks(split))

    def num_tasks(self, split: str) -> int:
        """Get the number of tasks for a given split."""
        return self._run(self._async.num_tasks(split))

    def get_task(self, split: str, index: int) -> Task:
        """Get a single task by split and index."""
        return self._run(self._async.get_task(split, index))

    def get_task_range(self, split: str, start: Optional[int] = None, stop: Optional[int] = None) -> list[Task]:
        """Get tasks for indices in range(start, stop). Supports negative and None indices."""
        return self._run(self._async.get_task_range(split, start, stop))

    @overload
    def list_tools(self, format: None = None) -> list[ToolSpec]: ...

    @overload
    def list_tools(self, format: Provider) -> list[dict]: ...

    def list_tools(self, format: Optional[Provider] = None) -> Union[list[ToolSpec], list[dict]]:
        return self._run(self._async.list_tools(format))

    def terminal_tool(self) -> Optional[TerminalToolSpec]:
        """The environment's ``@terminal`` tool, or None if it has none."""
        return self._run(self._async.terminal_tool())

    def is_assistant_message_final(self) -> bool:
        """True when a plain assistant message ends a rollout in this environment."""
        return self._run(self._async.is_assistant_message_final())

    def get_prompt(self, task: Task) -> str:
        return self._run(self._async.get_prompt(task))

    def session(
        self,
        task: Optional[Task] = None,
        secrets: Optional[Mapping[str, Union[str, tuple[str, list[str]]]]] = None,
        *,
        split: Optional[str] = None,
        index: Optional[int] = None,
        toolset: Optional[BuiltinToolset] = None,
        env_overrides: Optional[Mapping[str, str]] = None,
    ) -> Session:
        """Create a session from a Task object or from split/index.

        See :meth:`AsyncEnvironment.session` for the ``toolset`` and
        ``env_overrides`` parameters.
        """
        async_session = self._async.session(
            task=task,
            secrets=secrets,
            split=split,
            index=index,
            toolset=toolset,
            env_overrides=env_overrides,
        )
        return Session(async_session, self._loop)

    def list_required_secrets(self) -> list[str]:
        """Get the list of secret keys required by this environment."""
        return self._run(self._async.list_required_secrets())

    def get_task_difficulty(
        self,
        *,
        split: Optional[str] = None,
        model_name: Optional[str] = None,
        min_model_params: Optional[int] = None,
        max_model_params: Optional[int] = None,
        training_stage: Optional[TrainingStage] = None,
    ) -> list[TaskDifficulty]:
        """Get per-task difficulty for this environment.

        See :meth:`AsyncEnvironment.get_task_difficulty`.
        """
        return self._run(self._async.get_task_difficulty(
            split=split,
            model_name=model_name,
            min_model_params=min_model_params,
            max_model_params=max_model_params,
            training_stage=training_stage,
        ))


class EnvironmentsAPI:
    """Synchronous wrapper around AsyncEnvironmentsAPI.

    The event loop runs in a background daemon thread so that the ping
    task stays alive between synchronous calls.
    """

    def __init__(self, base_url: str, api_key: str, api_base_url: Optional[str] = None):
        self._loop = asyncio.new_event_loop()
        self._loop_thread = threading.Thread(
            target=self._loop.run_forever, daemon=True
        )
        self._loop_thread.start()
        self._async = AsyncEnvironmentsAPI(base_url, api_key, api_base_url=api_base_url)
        self._closed = False
        atexit.register(self._atexit_handler)

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    def get(self, name: str, variant: Optional[str] = None, base_url: Optional[str] = None) -> Environment:
        async def _get():
            return self._async.get(name, variant, base_url)
        async_env = self._run(_get())
        return Environment(async_env, self._loop)

    def close(self):
        """Clean up resources. Idempotent."""
        if self._closed:
            return
        self._closed = True
        if not self._loop.is_running():
            return
        try:
            self._run(self._async.aclose())
            self._run(self._loop.shutdown_asyncgens())
        except Exception:
            pass
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._loop_thread.join(timeout=5)
        if not self._loop.is_closed():
            self._loop.close()

    def _atexit_handler(self):
        try:
            self.close()
        except Exception:
            pass

    def __enter__(self) -> "EnvironmentsAPI":
        return self

    def __exit__(self, *exc):
        self.close()
