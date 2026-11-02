"""SDK-owned authoring contracts for the Unified Harness runtime."""

from __future__ import annotations

import base64
import contextvars
import functools
import inspect
import ipaddress
import os
import posixpath
import warnings
from collections.abc import Callable, Mapping, Sequence
from copy import copy, deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Protocol, Self, cast
from uuid import uuid4

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    PrivateAttr,
    TypeAdapter,
    ValidationError,
    field_validator,
    model_validator,
)

from mistralai.vibe.harness.app_server.session import McpHttpSourceConfiguration, ToolModelAccess
from mistralai.vibe.harness.runtime.capabilities import (
    PostAgentTurnHookAccept,
    PostAgentTurnHookInvocation,
    PostLlmCallHookAccept,
    PostLlmCallHookInvocation,
    PostLlmCallHookReject,
    PostLlmCallHookRetry,
    PostToolCallHookContinue,
    PreAgentTurnHookContinue,
    PreAgentTurnHookInvocation,
    PreAgentTurnHookSkip,
    PreLlmCallHookContinue,
    PreLlmCallHookInvocation,
    PreLlmCallHookSkip,
    PreToolCallHookContinue,
    PreToolCallHookSkip,
)
from mistralai.vibe.harness.runtime.hosts.workflows import (
    FileSource,
    ResolvedFile,
    ResolvedFiles,
    WorkflowSandboxExecuteRequest,
    WorkflowSandboxExecuteResult,
    WorkflowSandboxReadFileRequest,
    WorkflowSandboxReadFileResult,
    WorkflowSandboxWriteFilesRequest,
    WorkflowSandboxWriteFilesResult,
    register_file_resolver,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_files import (
    inline_file_source,
    normalized_relative_path,
)
from mistralai.vibe_agents.sdk.app.config import MistralSandboxSettings
from mistralai.workflows.plugins.mistralai.connectors import decorator as connector_decorator

from . import connector_selection, hooks, session_input, stateful
from . import tool as tool_authoring
from . import types as authoring_types
from .errors import SdkError
from .sandbox_policy import (
    GitHubBinding,
    HeaderBinding,
    Network,
    NetworkMode,
    SandboxHeaderBinding,
    SandboxPolicy,
    WorkspaceHeaderBindings,
    network_blocks,
)
from .secrets import MistralSecret, SecretOrigin, validate_secret_name
from .skills import AllRegistrySkills, RegistrySkill, SandboxWorkspaceSkills

if TYPE_CHECKING:
    from .subagent import Subagent

_JSON_OBJECT = TypeAdapter(dict[str, JsonValue])
_JSON_VALUE: TypeAdapter[JsonValue] = TypeAdapter(JsonValue)

Depends = session_input.Depends
SessionInput = session_input.SessionInput

PermissionMode = authoring_types.PermissionMode
type HarnessTool = tool_authoring.PythonTool[..., Any] | tool_authoring.ClientToolDefinition[Any]
# What `tools=` takes: a plain function becomes a PythonTool, as if decorated with @agents.tool, and a
# client tool stands for its declaration.
type HarnessTools = Sequence[HarnessTool | tool_authoring.ClientTool[..., Any] | Callable[..., Any]]
type HarnessConnector = connector_decorator.ConnectorSlot | connector_selection.AllConnectors


def split_connectors(
    connectors: Sequence[HarnessConnector],
    *,
    owner: str = "Harness",
) -> tuple[tuple[connector_decorator.ConnectorSlot, ...], connector_selection.AllConnectors | None]:
    """Separate connectors named at build time from the run-time discovered set."""

    slots: list[connector_decorator.ConnectorSlot] = []
    discovery: connector_selection.AllConnectors | None = None
    for entry in connectors:
        if isinstance(entry, connector_selection.AllConnectors):
            if discovery is not None:
                raise ValueError(f"{owner} connectors accept at most one all_connectors() selection")
            discovery = entry
            continue
        if not isinstance(entry, connector_decorator.ConnectorSlot):
            raise TypeError(f"{owner} connectors must be agents.connector(...) or agents.all_connectors(...)")
        slots.append(entry)
    return tuple(slots), discovery


def split_skills(
    skills: Sequence[HarnessSkill | SandboxWorkspaceSkills | AllRegistrySkills],
) -> tuple[tuple[HarnessSkill, ...], tuple[SandboxWorkspaceSkills, ...], AllRegistrySkills | None]:
    """Separate explicit skills, sandbox search roots, and Registry discovery."""

    written: list[HarnessSkill] = []
    found: list[SandboxWorkspaceSkills] = []
    discovery: AllRegistrySkills | None = None
    for entry in skills:
        if isinstance(entry, AllRegistrySkills):
            if discovery is not None:
                raise ValueError("Harness skills accept at most one all_registry_skills() selection")
            discovery = entry
            continue
        if isinstance(entry, SandboxWorkspaceSkills):
            found.append(entry)
            continue
        if not isinstance(entry, LocalSkillBundle | RegistrySkill):
            raise TypeError(
                "Harness skills must be agents.LocalSkillBundle, agents.RegistrySkill, agents.SandboxWorkspaceSkills "
                "or agents.all_registry_skills()"
            )
        written.append(entry)
    return tuple(written), tuple(found), discovery


@dataclass(frozen=True, slots=True)
class CallbackSession:
    """Session identity available while a Unified Harness Hook runs."""

    id: str
    turn_id: str

    def __str__(self) -> str:
        return self.id


# Each sandbox driver maps this root to its own folder outside the workspace.
_HOOK_FILES_ROOT = "/hook-files"
_HOOK_FILES_RESOLVER = "agents-sdk-hook-files"


class _HookFileResolver:
    """Hand a sandbox driver the bytes a Hook is writing, from this process."""

    def __init__(self) -> None:
        self.pending: dict[str, ResolvedFile] = {}

    async def __call__(self, refs: JsonValue) -> ResolvedFiles:
        if not isinstance(refs, str) or (file := self.pending.get(refs)) is None:
            raise RuntimeError("the file a Hook is writing is not known to this process")
        return ResolvedFiles(files=(file,))


_hook_file_resolver = _HookFileResolver()


class _HookSandboxPort(Protocol):
    @property
    def workspace(self) -> str | None: ...

    async def execute(self, request: WorkflowSandboxExecuteRequest) -> WorkflowSandboxExecuteResult: ...

    async def read_file(self, request: WorkflowSandboxReadFileRequest) -> WorkflowSandboxReadFileResult: ...

    async def write_files(self, request: WorkflowSandboxWriteFilesRequest) -> WorkflowSandboxWriteFilesResult: ...


@dataclass(frozen=True, slots=True)
class SandboxExecutionResult:
    """Output of a command run in the current session sandbox."""

    exit_code: int
    stdout: str
    stderr: str


class HookSandbox:
    """Session sandbox operations available to an authored Hook."""

    def __init__(self) -> None:
        self._port: _HookSandboxPort | None = None
        self._inline_writes = False

    def bind(self, port: _HookSandboxPort, *, inline_writes: bool = False) -> None:
        """Bind the live sandbox.

        Set ``inline_writes`` when the Hook runs in Workflow code. The worker that writes the file
        does not share this process's memory, and a replay must see the same input, so
        ``write_file`` carries the content in the write request.
        """

        self._port = port
        self._inline_writes = inline_writes

    @property
    def is_executable(self) -> bool:
        return self._port is not None and self._port.workspace is not None

    @property
    def workspace(self) -> str | None:
        return self._port.workspace if self._port is not None else None

    async def execute(
        self,
        command: str,
        *,
        cwd: str | None = None,
        timeout_seconds: int | None = None,
        env: Mapping[str, str] | None = None,
    ) -> SandboxExecutionResult:
        """Run a command in the session sandbox at most once."""

        result = await self._execute(
            WorkflowSandboxExecuteRequest(
                command=command,
                operation_name="hook.execute",
                arguments={},
                cwd=cwd or self.workspace or "/workspace",
                timeout_seconds=timeout_seconds,
                retry_mode="at_most_once",
                env=dict(env or {}),
            )
        )
        return SandboxExecutionResult(result.exit_code, result.stdout, result.stderr)

    async def _execute(self, request: WorkflowSandboxExecuteRequest) -> WorkflowSandboxExecuteResult:
        return await self._require_port().execute(request)

    async def read_file(self, path: str, *, max_bytes: int = 1024 * 1024) -> bytes:
        """Read a whole file from the session sandbox.

        A relative ``path`` is resolved against the sandbox workspace. A file larger than
        ``max_bytes`` is never cut: every sandbox raises an error instead. A missing file raises
        ``FileNotFoundError``.
        """

        port = self._require_port()
        result = await port.read_file(
            WorkflowSandboxReadFileRequest(
                path=path if path.startswith("/") else f"{port.workspace}/{path}", max_bytes=max_bytes
            )
        )
        return base64.b64decode(result.content_base64)

    async def write_file(self, name: str, content: bytes) -> str:
        """Write ``content`` to a file outside the workspace and return its path in the sandbox.

        ``name`` is a relative path under the folder the sandbox keeps for Hook files. Writing the
        same ``name`` again replaces the file. Raise ``ValueError`` if ``name`` is absolute or
        leaves that folder. A served sandbox hook runs in Workflow code, where ``content`` must be
        UTF-8 text and the JSON-encoded request, path included, must fit in 1 MiB.
        """

        port = self._require_port()
        path = normalized_relative_path(name)
        if self._inline_writes:
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError as error:
                raise ValueError("A served sandbox hook can write only UTF-8 text with write_file") from error
            written = await port.write_files(
                WorkflowSandboxWriteFilesRequest(root=_HOOK_FILES_ROOT, source=inline_file_source(path, text))
            )
            return posixpath.join(written.root, path)
        key = uuid4().hex
        _hook_file_resolver.pending[key] = ResolvedFile(path=path, content=content)
        register_file_resolver(_HOOK_FILES_RESOLVER, _hook_file_resolver)
        try:
            written = await port.write_files(
                WorkflowSandboxWriteFilesRequest(
                    root=_HOOK_FILES_ROOT, source=FileSource(resolver=_HOOK_FILES_RESOLVER, refs=key)
                )
            )
        finally:
            del _hook_file_resolver.pending[key]
        return posixpath.join(written.root, path)

    def _require_port(self) -> _HookSandboxPort:
        if not self.is_executable or self._port is None:
            raise RuntimeError("The current session has no accessible executable sandbox")
        return self._port


class CallbackContext:
    """What a callback gets as `ctx`: the Session it runs in and the Session sandbox.

    The shared base: a Hook method gets a ``HookCallbackContext``, and a tool a ``ToolCallbackContext``.
    """

    def __init__(
        self,
        session: CallbackSession,
        sandbox: HookSandbox | None = None,
        *,
        _max_iterations: int | None = None,
    ) -> None:
        self._session = session
        self._sandbox = sandbox or HookSandbox()
        # The agent's max_iterations, which StructuredOutputHook reads. Private: not part of `ctx`'s API.
        self._max_iterations = _max_iterations

    @property
    def session(self) -> CallbackSession:
        return self._session

    @property
    def sandbox(self) -> HookSandbox:
        return self._sandbox


class HookCallbackContext(CallbackContext):
    """What a Hook method gets as `ctx`: the Session it runs in and the Session sandbox."""


# The ids of the context a direct call of a tool gets when it passes none.
_LOCAL = "local"


class ToolCallbackContext(CallbackContext):
    """What a tool gets as its first, positional-only parameter: the Session, its sandbox and the call.

    A tool takes it by type, under any name: ``def search(ctx: agents.ToolCallbackContext, /, query: str)``.
    The model never sees it. A direct call can pass ``ToolCallbackContext.local()``, or leave it out to
    get that local context.
    """

    def __init__(self, session: CallbackSession, sandbox: HookSandbox | None = None, *, tool_call_id: str) -> None:
        super().__init__(session, sandbox)
        self._tool_call_id = tool_call_id

    @property
    def tool_call_id(self) -> str:
        """The id of the model's call to the tool, as in the Session's tool call entry."""
        return self._tool_call_id

    @classmethod
    def local(cls) -> "ToolCallbackContext":
        """A context for a call outside any Session: every id is ``"local"`` and the sandbox is unbound."""
        return cls(CallbackSession(id=_LOCAL, turn_id=_LOCAL), tool_call_id=_LOCAL)


SKILL_ENTRY_FILE = "SKILL.md"


class LocalSkillFile(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str = Field(min_length=1)
    content_base64: str
    executable: bool = False

    @field_validator("content_base64")
    @classmethod
    def validate_content_base64(cls, value: str) -> str:
        try:
            base64.b64decode(value.encode("ascii"), validate=True)
        except (ValueError, UnicodeEncodeError) as exc:
            raise ValueError("content_base64 must be valid base64") from exc
        return value


# Windows has no executable bit: os.access(X_OK) is true for every file there, so a script is
# recognized by its shebang instead.
_HAS_EXECUTABLE_BIT = os.name != "nt"


def _is_executable(path: Path) -> bool:
    if _HAS_EXECUTABLE_BIT:
        return os.access(path, os.X_OK)
    with path.open("rb") as handle:
        return handle.read(2) == b"#!"


class LocalSkillBundle(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    files: list[LocalSkillFile] = Field(default_factory=list)

    @classmethod
    def from_directory(cls, path: str | Path) -> Self:
        """Bundle a skill directory: its SKILL.md and every asset beside it."""

        root = Path(path)
        if not (root / SKILL_ENTRY_FILE).is_file():
            raise ValueError(f"{root} is not a skill directory: it has no {SKILL_ENTRY_FILE}.")
        files: list[LocalSkillFile] = []
        for entry in sorted(root.rglob("*")):
            if entry.is_dir():
                continue
            if entry.is_symlink() or not entry.is_file():
                raise ValueError(f"skill files must be regular files: {entry}")
            files.append(
                LocalSkillFile(
                    path=entry.relative_to(root).as_posix(),
                    content_base64=base64.b64encode(entry.read_bytes()).decode("ascii"),
                    executable=_is_executable(entry),
                )
            )
        return cls(files=files)


type HarnessSkill = LocalSkillBundle | RegistrySkill


class SerializedUnifiedObject(BaseModel):
    """Type-tagged JSON state for Unified Harness SDK extension points."""

    # The outermost model being validated decides whether an error prints its input. Restored state
    # can carry a secret origin whose `ref` is a secret pasted by mistake, so this one must hide it.
    model_config = ConfigDict(frozen=True, extra="forbid", hide_input_in_errors=True)

    type: str
    state: dict[str, JsonValue]
    # A Sandbox's network and header binding travel beside its type-owned state, so no sandbox type,
    # built-in or custom, has to serialize them itself.
    sandbox_policy: SandboxPolicy | None = None


# The policy of the Sandbox that deserialize_unified is rebuilding, which Sandbox.__init__ takes
# in place of its arguments: from_unified_state rebuilds only the type-owned state.
_restored_sandbox_policy: contextvars.ContextVar[tuple[str, SandboxPolicy] | None] = contextvars.ContextVar(
    "_restored_sandbox_policy", default=None
)


class UnifiedSerializable:
    """Small registry-backed serialization contract for Unified Harness authoring."""

    _unified_types: ClassVar[dict[str, type["UnifiedSerializable"]]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        UnifiedSerializable._unified_types[unified_type_key(cls)] = cls

    def to_unified_state(self) -> dict[str, JsonValue]:
        """Return the state needed to rebuild this value."""

        return {}

    @classmethod
    def from_unified_state(cls, state: dict[str, JsonValue]) -> Self:
        """Rebuild a value from state emitted by ``to_unified_state``."""

        if state:
            raise TypeError(f"{cls.__name__} must override from_unified_state for non-empty state")
        return cls()

    def serialize_unified(self) -> dict[str, JsonValue]:
        _reject_unserialized_extension_state(self)
        return SerializedUnifiedObject(
            type=unified_type_key(type(self)),
            state=_JSON_OBJECT.validate_python(self.to_unified_state()),
        ).model_dump(mode="json")


def deserialize_unified[T: UnifiedSerializable](
    state: Mapping[str, object],
    *,
    expected: type[T],
    default_sandbox_policy: SandboxPolicy | None = None,
) -> T:
    """Restore one registered Unified Harness authoring object.

    ``default_sandbox_policy`` stands in for a sandbox state that carries no policy, such as one an
    earlier worker serialized before a continue-as-new.
    """

    serialized = SerializedUnifiedObject.model_validate(state)
    value_type = UnifiedSerializable._unified_types.get(serialized.type)
    if value_type is None:
        raise TypeError(f"Unified Harness authoring type {serialized.type!r} is not registered")
    policy = serialized.sandbox_policy or default_sandbox_policy
    token = _restored_sandbox_policy.set(None if policy is None else (serialized.type, policy))
    try:
        restored = value_type.from_unified_state(serialized.state)
    finally:
        _restored_sandbox_policy.reset(token)
    if policy is not None and isinstance(restored, Sandbox) and getattr(restored, "_policy", None) != policy:
        raise TypeError(f"{type(restored).__name__}.from_unified_state must build the sandbox through its constructor")
    if not isinstance(restored, expected):
        raise TypeError(f"Unified state rebuilt {type(restored).__name__}; expected {expected.__name__}")
    return cast(T, restored)


def unified_type_key(value_type: type[object]) -> str:
    return f"{value_type.__module__}:{value_type.__qualname__}"


def _snapshot(value: object) -> object:
    """A deep copy of a constructor argument, or the argument itself when it cannot be copied.

    A JSON value always copies; one that does not is not JSON, and serialization refuses it.
    """

    try:
        return deepcopy(value)
    except Exception:  # noqa: BLE001 - an uncopyable argument must not break constructing the Hook
        return value


def replays_constructor_arguments(value_type: type[UnifiedSerializable]) -> bool:
    """Whether ``value_type`` is rebuilt from its recorded constructor arguments."""

    return issubclass(value_type, SandboxHook) and value_type.to_unified_state is SandboxHook.to_unified_state


# Values compared by value: JSON data, and the sets and tuples a constructor commonly derives from it.
_PLAIN_DATA: TypeAdapter[object] = TypeAdapter(
    JsonValue | frozenset[JsonValue] | set[JsonValue] | tuple[JsonValue, ...]
)


def _same_attributes(value: SandboxHook, rebuilt: SandboxHook) -> bool:
    authored, restored = _authored_attributes(value), _authored_attributes(rebuilt)
    return authored.keys() == restored.keys() and all(
        _same_attribute(authored[name], restored[name]) for name in authored
    )


def _authored_attributes(value: SandboxHook) -> dict[str, object]:
    return {name: field for name, field in vars(value).items() if name != "_constructor_arguments"}


_CONTAINERS = (list, tuple, dict, set, frozenset)


def _same_attribute(authored: object, rebuilt: object) -> bool:
    """Whether a rebuilt attribute holds what the authored one does.

    Plain data, such as a counter, and a value whose type defines equality, such as a generated
    ``UUID``, must be equal. An object that compares by identity, such as a client built from a URL,
    is never equal to a correct rebuild of it, so its type alone shows it was rebuilt; so does a
    container of such objects.
    """

    try:
        return _PLAIN_DATA.validate_python(authored, strict=True) == _PLAIN_DATA.validate_python(rebuilt, strict=True)
    except ValueError:
        pass
    if type(authored) is not type(rebuilt):
        return False
    if isinstance(authored, _CONTAINERS) or type(authored).__eq__ is object.__eq__:
        return True
    try:
        return bool(authored == rebuilt)
    except Exception:  # noqa: BLE001 - equality without a truth value, such as an array's, says nothing
        return True


class Hook(stateful.StatefulModel):
    """Unified Harness Hook. Override the points you need; returning ``None`` continues unchanged.

    A Hook is a Pydantic model. Its fields are its state: the Session keeps their values and every
    call starts from the values the last successful call left. Anything else the Hook holds, such
    as a client, is a ``PrivateAttr``, which is never saved.
    """

    _tools: tuple[HarnessTool, ...] = PrivateAttr(default=())

    def __init__(self, *, tools: Sequence[HarnessTool | tool_authoring.ClientTool[..., Any]] = (), **data: Any) -> None:
        # An old Hook may set attributes before it calls this; Pydantic would drop them.
        early = {} if hasattr(self, "__pydantic_fields_set__") else dict(self.__dict__)
        super().__init__(**data)
        self.__dict__.update(early)
        self._tools = tuple(tool_authoring.declared_tool(tool) for tool in tools)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        init = cls.__dict__.get("__init__")
        if init is not None:
            cls.__init__ = _finish_old_init(init)  # type: ignore[method-assign]
        defined = [name for name in ("to_unified_state", "from_unified_state") if name in cls.__dict__]
        if defined:
            stateful.warn_deprecated(
                f"Hook {cls.__qualname__} defines {' and '.join(defined)}, which Hook no longer has: "
                "declare its state as a field or a PrivateAttr; nothing calls these methods."
            )

    def _set_undeclared(self, name: str, value: Any) -> None:
        cls = type(self)
        if cls.model_fields:
            # Each call runs on a copy rebuilt from the fields, so the attribute would be lost.
            super()._set_undeclared(name, value)
        if (cls, name) not in _WARNED_UNDECLARED:
            _WARNED_UNDECLARED.add((cls, name))
            stateful.warn_deprecated(
                f"Hook {cls.__qualname__} sets the undeclared attribute {name!r}: declare it as a field "
                "or PrivateAttr. Undeclared attributes are never saved: all Sessions of a process share them, or a "
                "call loses them when it ends, and a Workflow agent rejects a Hook that has them when it starts."
            )
        object.__setattr__(self, name, value)

    # Compared and hashed by identity, not by field values, so a Hook can be a set member or dict key.
    def __eq__(self, other: object) -> bool:
        return self is other

    def __hash__(self) -> int:
        return object.__hash__(self)

    @property
    def tools(self) -> Sequence[HarnessTool]:
        return tuple(self._tools)

    async def pre_agent_turn(
        self,
        ctx: HookCallbackContext,
        request: PreAgentTurnHookInvocation,
    ) -> PreAgentTurnHookContinue | PreAgentTurnHookSkip | hooks.HookDecision | None:
        return PreAgentTurnHookContinue(user_content=request.user_content)

    async def post_agent_turn(
        self,
        ctx: HookCallbackContext,
        result: PostAgentTurnHookInvocation,
    ) -> PostAgentTurnHookAccept | None:
        return PostAgentTurnHookAccept()

    async def pre_llm_call(
        self,
        ctx: HookCallbackContext,
        invocation: PreLlmCallHookInvocation,
    ) -> PreLlmCallHookContinue | PreLlmCallHookSkip | hooks.HookDecision | None:
        return PreLlmCallHookContinue()

    async def post_llm_call(
        self,
        ctx: HookCallbackContext,
        invocation: PostLlmCallHookInvocation,
    ) -> PostLlmCallHookAccept | PostLlmCallHookRetry | PostLlmCallHookReject | hooks.HookDecision | None:
        return PostLlmCallHookAccept()

    async def pre_tool_call(
        self,
        ctx: HookCallbackContext,
        call: hooks.PreToolCall,
    ) -> PreToolCallHookContinue | PreToolCallHookSkip | hooks.HookDecision | None:
        return PreToolCallHookContinue(effective_arguments=call.tool_call.call.arguments)

    async def post_tool_call(
        self,
        ctx: HookCallbackContext,
        result: hooks.PostToolCall,
    ) -> PostToolCallHookContinue | None:
        return PostToolCallHookContinue(tool_result=result.tool_result)


_WARNED_UNDECLARED: set[tuple[type[Hook], str]] = set()


def _finish_old_init(init: Callable[..., None]) -> Callable[..., None]:
    """Wrap a Hook's own ``__init__``, so an old Hook that never calls ``super().__init__()`` still works."""

    @functools.wraps(init)
    def wrapper(self: Hook, *args: Any, **kwargs: Any) -> None:
        init(self, *args, **kwargs)
        if not hasattr(self, "__pydantic_fields_set__"):
            Hook.__init__(self)

    return wrapper


def legacy_hook_reason(hook: Hook) -> str | None:
    """Say why ``hook`` is an old-style Hook, or return ``None`` for a Hook whose state is its fields.

    An old-style Hook has no fields and sets attributes it does not declare. It runs only
    in-process, as one shared object, and nothing of it is saved.
    """

    cls = type(hook)
    undeclared = [
        name
        for name in vars(hook)
        if name not in cls.model_fields
        and not isinstance(inspect.getattr_static(cls, name, None), functools.cached_property)
    ]
    return f"it sets the undeclared attribute {undeclared[0]!r}" if undeclared else None


class SandboxCallbackContext:
    """Context a sandbox hook receives in ``on_create`` and ``on_destroy``."""

    def __init__(self, sandbox: HookSandbox) -> None:
        self._sandbox = sandbox

    @property
    def sandbox(self) -> HookSandbox:
        return self._sandbox


class SandboxHook(UnifiedSerializable):
    """Observe a Unified Harness sandbox's create and destroy lifecycle.

    ``on_create`` and ``on_destroy`` may declare Session inputs with
    ``Annotated[T, agents.Depends()]`` parameters, like tools and hooks.

    The arguments a subclass is constructed with are recorded, so a worker rebuilds the sandbox
    hook with the same arguments. They must be JSON values. A subclass that writes its own
    ``to_unified_state`` and ``from_unified_state`` replaces this contract.
    """

    #: Whether the hook changes state outside the workspace that the host would keep, such as the
    #: user's global git configuration. ``DangerousLocalSandbox`` runs on the host and refuses it.
    _changes_host_state: ClassVar[bool] = False
    _constructor_arguments: tuple[tuple[object, ...], dict[str, object]] = ((), {})

    def __new__(cls, *args: object, **kwargs: object) -> Self:
        value = super().__new__(cls)
        # A sandbox hook without a constructor of its own has no arguments to record.
        if cls.__init__ is not object.__init__:
            # A snapshot, so neither the constructor nor the caller can change what a worker replays.
            value._constructor_arguments = (
                tuple(_snapshot(argument) for argument in args),
                {name: _snapshot(argument) for name, argument in kwargs.items()},
            )
        return value

    def to_unified_state(self) -> dict[str, JsonValue]:
        args, kwargs = self._replayable_arguments()
        if not args and not kwargs:
            return {}
        return {"args": cast(list[JsonValue], list(args)), "kwargs": cast(dict[str, JsonValue], kwargs)}

    def _replayable_arguments(self) -> tuple[tuple[object, ...], dict[str, object]]:
        """The constructor arguments a worker replays, each checked to be a JSON value as it is.

        A value that would only become JSON by conversion, such as a tuple, is refused: the rebuilt
        value would get a different type.
        """

        args, kwargs = self._constructor_arguments
        if not args and not kwargs:
            return (), {}
        label = f"Sandbox hook {type(self).__name__}"
        try:
            bound = inspect.signature(type(self).__init__).bind(self, *args, **kwargs)
        except TypeError:
            # The constructor rejected these arguments, so the value was never built with them.
            raise TypeError(f"{label} was built with arguments its constructor rejects") from None
        replayed_args, replayed_kwargs = list(bound.args[1:]), dict(bound.kwargs)
        # Checked as replayed: one value per positional, so a ``*args`` tuple is checked item by item.
        named = [
            *(
                (self._positional_name(bound.signature, index), value)
                for index, value in enumerate(replayed_args, start=1)
            ),
            *replayed_kwargs.items(),
        ]
        for name, value in named:
            try:
                _JSON_VALUE.validate_python(value, strict=True)
            except ValueError:
                raise TypeError(
                    f"{label} cannot run on a worker: its constructor argument {name!r} "
                    f"is not a JSON value (got {type(value).__name__})"
                ) from None
        return tuple(replayed_args), replayed_kwargs

    @staticmethod
    def _positional_name(signature: inspect.Signature, index: int) -> str:
        """The parameter the ``index``-th positional (from 1, after ``self``) fills."""

        parameters = list(signature.parameters.values())[1:]
        for position, parameter in enumerate(parameters, start=1):
            if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
                return f"{parameter.name}[{index - position}]"
            if position == index:
                return parameter.name
        return f"#{index}"

    @classmethod
    def from_unified_state(cls, state: dict[str, JsonValue]) -> Self:
        # A subclass that writes its own state but keeps this rebuilder gets the base contract's error.
        if not replays_constructor_arguments(cls):
            return super().from_unified_state(state)
        if not state:
            return cls()
        args, kwargs = state.get("args"), state.get("kwargs")
        if not isinstance(args, list) or not isinstance(kwargs, dict):
            raise TypeError(f"{cls.__name__} state does not hold its constructor arguments")
        # A subclass constructor takes its own parameters, not the base class's alone.
        return cls(*args, **cast(dict[str, Any], kwargs))

    async def on_create(self, ctx: SandboxCallbackContext) -> None:
        del ctx

    async def on_destroy(self, ctx: SandboxCallbackContext) -> None:
        del ctx


type SandboxAccess = Literal["none", "files", "full"]
SANDBOX_ACCESS_LEVELS: tuple[SandboxAccess, ...] = ("none", "files", "full")


def access_covers(supported: SandboxAccess, requested: SandboxAccess) -> bool:
    """Whether a sandbox that serves ``supported`` can give ``requested``: each level includes the lower ones."""

    return SANDBOX_ACCESS_LEVELS.index(requested) <= SANDBOX_ACCESS_LEVELS.index(supported)


class Sandbox(UnifiedSerializable):
    """Base class for SDK-owned Unified Harness sandbox authoring.

    ``access`` sets the sandbox tools the model gets: ``"files"`` gives the file tools,
    ``"full"`` adds bash, and ``"none"`` gives neither while tools, hooks and skills
    still use the sandbox. ``None`` gives every level the sandbox supports. A sandbox type declares
    in ``supported_access`` the widest level it serves, and its constructor refuses a wider one.

    ``network`` sets the outbound connections the sandbox can open, and defaults to
    ``Network.none()``. ``header_bindings`` lists the secrets the sandbox gets on those connections. A
    sandbox type declares in ``supported_network`` and ``supported_header_bindings`` what it can
    enforce, and its constructor refuses the rest.
    """

    supported_network: ClassVar[tuple[NetworkMode, ...]] = ()
    supported_header_bindings: ClassVar[tuple[type[BaseModel], ...]] = ()
    supported_access: ClassVar[SandboxAccess] = "full"
    delete_on_cleanup = True
    supports_background_processes = False
    _supports_python = True
    _hooks: Sequence[SandboxHook] = ()
    # The access level reaches the Harness through AgentConfig.sandbox_access, so the unified
    # sandbox state, which only rebuilds the sandbox driver, does not carry it.
    _access: SandboxAccess | None = None

    def __init__(
        self,
        *,
        network: Network | None = None,
        header_bindings: Sequence[SandboxHeaderBinding] = (),
        hooks: Sequence[SandboxHook] = (),
        access: SandboxAccess | None = None,
    ) -> None:
        if access is not None and access not in SANDBOX_ACCESS_LEVELS:
            raise ValueError(f"Sandbox access must be one of {SANDBOX_ACCESS_LEVELS}, not {access!r}")
        self._check_access(access)
        restored = _restored_sandbox_policy.get()
        if restored is not None and restored[0] == unified_type_key(type(self)):
            # Consumed once, by the sandbox of the restored type: one that from_unified_state builds
            # on the side, before or after it, keeps its own policy.
            _restored_sandbox_policy.set(None)
            policy = restored[1]
        else:
            policy = SandboxPolicy(network=network or Network.none(), header_bindings=tuple(header_bindings))
        self._check_policy(policy)
        self._policy = policy
        self._hooks = tuple(hooks)
        # The Harness resolves None to the widest level its Host serves, so a narrower sandbox resolves it here.
        self._access = access if access is not None or self.supported_access == "full" else self.supported_access

    def _check_access(self, access: SandboxAccess | None) -> None:
        name = type(self).__name__
        supported = self.supported_access
        if supported not in SANDBOX_ACCESS_LEVELS:
            raise ValueError(f"{name}.supported_access must be one of {SANDBOX_ACCESS_LEVELS}, not {supported!r}")
        if access is not None and not access_covers(supported, access):
            raise ValueError(f"{name} supports access up to {supported!r}, not {access!r}")

    def _check_policy(self, policy: SandboxPolicy) -> None:
        name = type(self).__name__
        mode = policy.network.mode
        if mode not in self.supported_network:
            if not self.supported_network:
                raise ValueError(f"{name} declares no network policy it can enforce; set {name}.supported_network")
            supported = " or ".join(f"network=Network.{supported}()" for supported in self.supported_network)
            raise ValueError(f"{name} does not support Network.{mode}(); pass {supported}")
        seen: set[type[object]] = set()
        for injection in policy.header_bindings:
            injection_type = type(injection)
            if not issubclass(injection_type, self.supported_header_bindings):
                raise ValueError(f"{name} does not support agents.{injection_type.__name__}")
            if injection_type is not HeaderBinding and injection_type in seen:
                raise ValueError(f"{name} accepts at most one agents.{injection_type.__name__}")
            seen.add(injection_type)
        # A binding the network cannot reach would be accepted and then never applied.
        for injection in policy.header_bindings:
            if (blocked := network_blocks(policy.network, injection)) is None:
                continue
            hints = ["network=Network.all()"] if "all" in self.supported_network else []
            if "allow" in self.supported_network and not isinstance(injection, WorkspaceHeaderBindings):
                hints.append("the hosts in Network.allow(hosts=...)")
            fix = f"pass {' or '.join(hints)}" if hints else f"{name} supports no network that reaches it"
            raise ValueError(
                f"{name}: agents.{type(injection).__name__} {blocked}, which Network.{mode}() blocks; {fix}"
            )

    @property
    def network(self) -> Network:
        return self._policy.network

    @property
    def header_bindings(self) -> tuple[SandboxHeaderBinding, ...]:
        return self._policy.header_bindings

    @property
    def secret_names(self) -> tuple[str, ...]:
        """The names of the secrets that ``header_bindings`` picks, in order and without duplicates."""

        return tuple(
            dict.fromkeys(
                injection.secret_name for injection in self.header_bindings if isinstance(injection, HeaderBinding)
            )
        )

    @property
    def secret_origins(self) -> dict[str, SecretOrigin]:
        return dict(self._policy.secret_origins)

    def _check_secret_origins(self, origins: Mapping[str, SecretOrigin]) -> None:
        """Refuse an origin that this sandbox type cannot resolve for the header binding that names it."""

        del origins

    def bind_secret_origins(self, origins: Mapping[str, SecretOrigin]) -> Self:
        """Return a copy of this sandbox that carries the origin of each secret its ``header_bindings`` names."""

        known = {**self._policy.secret_origins, **origins}
        missing = [name for name in self.secret_names if name not in known]
        if missing:
            raise ValueError(
                f"{type(self).__name__} header_bindings names undeclared secrets {missing}; declare each in "
                "Agent(secrets={name: agents.MistralSecret(...)})"
            )
        needed = {name: known[name] for name in self.secret_names}
        if needed == self._policy.secret_origins:
            return self
        self._check_secret_origins(needed)
        bound = copy(self)
        bound._policy = SandboxPolicy(
            network=self._policy.network, header_bindings=self._policy.header_bindings, secret_origins=needed
        )
        return bound

    @property
    def policy(self) -> SandboxPolicy:
        return self._policy

    def serialize_unified(self) -> dict[str, JsonValue]:
        serialized = SerializedUnifiedObject.model_validate(super().serialize_unified())
        return serialized.model_copy(update={"sandbox_policy": self._policy}).model_dump(mode="json")

    @property
    def hooks(self) -> Sequence[SandboxHook]:
        return tuple(self._hooks)

    @property
    def access(self) -> SandboxAccess | None:
        return self._access

    @property
    def is_executable(self) -> bool:
        """Whether the sandbox gets a driver that runs commands and writes and reads files.

        A sandbox that is not executable, such as ``NoSandbox``, gets no driver: no tools, hooks or files.
        """

        return True

    def _supports_files(self) -> bool:
        """Whether the SDK can write files into the sandbox and read them back, such as skill folders.

        Every driver implements ``write_files()`` and ``read_file()``, so an executable sandbox holds files.
        """

        return self.is_executable


class NoSandbox(Sandbox):
    """Run without a sandbox."""

    supported_network = ("none",)
    delete_on_cleanup = False

    def __init__(self, *, hooks: Sequence[SandboxHook] = ()) -> None:
        super().__init__(hooks=hooks)

    @property
    def is_executable(self) -> bool:
        return False


class EgressPolicy(BaseModel):
    """IP-level outbound policy of a `MistralSandbox`.

    Authors pass only `EgressPolicy.custom(allow_cidrs=...)`, as `MistralSandbox(egress=...)`.
    The other modes are how the Koyeb driver receives `Network.none()` and `Network.all()`.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    mode: Literal["block_all", "allow_all", "custom"] = "block_all"
    allow_cidrs: tuple[str, ...] = ()

    @classmethod
    def block_all(cls) -> EgressPolicy:
        return cls(mode="block_all")

    @classmethod
    def allow_all(cls) -> EgressPolicy:
        return cls(mode="allow_all")

    @classmethod
    def custom(cls, *, allow_cidrs: Sequence[str]) -> EgressPolicy:
        return cls(mode="custom", allow_cidrs=tuple(allow_cidrs))

    @field_validator("allow_cidrs")
    @classmethod
    def _validate_allow_cidrs(cls, entries: tuple[str, ...]) -> tuple[str, ...]:
        stripped = tuple(entry.strip() for entry in entries)
        for entry in stripped:
            # ip_network accepts IPv6 zone IDs, which Koyeb cannot route.
            if "%" in entry:
                raise ValueError(f"Invalid allow_cidrs entry {entry!r}: zone-ID addresses are not allowed")
            try:
                ipaddress.ip_network(entry, strict=False)
            except ValueError:
                raise ValueError(f"Invalid allow_cidrs entry {entry!r}: expected an IP address or CIDR") from None
        return stripped

    @model_validator(mode="after")
    def _validate_mode(self) -> Self:
        if self.mode == "custom" and not self.allow_cidrs:
            raise ValueError("EgressPolicy.custom needs at least one CIDR; use Network.none() instead")
        if self.mode != "custom" and self.allow_cidrs:
            raise ValueError(f"allow_cidrs is only valid with mode 'custom', not {self.mode!r}")
        return self


class MistralSandbox(Sandbox):
    """Managed Koyeb sandbox configuration for the Unified Harness runtime.

    Koyeb filters outbound traffic by IP address, so ``network`` takes ``Network.none()`` or
    ``Network.all()``. ``egress=EgressPolicy.custom(allow_cidrs=...)`` opens the listed addresses
    on top of ``Network.none()``. Sandbox Proxy serves ``header_bindings``.
    """

    supported_network = ("none", "all")
    supported_header_bindings = (GitHubBinding, WorkspaceHeaderBindings)

    def __init__(
        self,
        *,
        image: str | None = None,
        supports_background_processes: bool | None = None,
        instance_type: str | None = None,
        region: str | None = None,
        name_prefix: str | None = None,
        ttl_seconds: int | None = None,
        idle_timeout_seconds: int | None = None,
        default_exec_timeout_seconds: int | None = None,
        privileged: bool | None = None,
        docker_daemon_enabled: bool | None = None,
        docker_daemon_network_mode: str | None = None,
        enable_light_sleep: bool | None = None,
        setup_script: str | None = None,
        setup_script_timeout_seconds: int | None = None,
        readiness_max_retries: int | None = None,
        readiness_interval_seconds: float | None = None,
        readiness_probe_timeout_seconds: int | None = None,
        wait_ready_timeout_seconds: int | None = None,
        enable_mesh: bool | None = None,
        network: Network | None = None,
        egress: EgressPolicy | None = None,
        header_bindings: Sequence[SandboxHeaderBinding] = (),
        pre_provisioned_sandbox_id: str | None = None,
        hooks: Sequence[SandboxHook] = (),
        access: SandboxAccess | None = None,
    ) -> None:
        super().__init__(network=network, header_bindings=header_bindings, hooks=hooks, access=access)
        if egress is not None:
            if egress.mode != "custom":
                raise ValueError(
                    "MistralSandbox(egress=...) takes only EgressPolicy.custom(allow_cidrs=...); "
                    "pass network=Network.none() or network=Network.all() instead"
                )
            if self.network.mode != "none":
                raise ValueError(
                    "MistralSandbox(egress=EgressPolicy.custom(...)) opens the listed addresses on top of "
                    f"Network.none(); it cannot be combined with Network.{self.network.mode}()"
                )
            # A default route opens everything while network still reads none().
            if any(ipaddress.ip_network(cidr, strict=False).prefixlen == 0 for cidr in egress.allow_cidrs):
                raise ValueError(
                    "MistralSandbox(egress=EgressPolicy.custom(...)) cannot open every address; "
                    "pass network=Network.all() instead"
                )
        # What the author passed, before this process's settings fill in the rest. A definition
        # that runs in another process, such as the shared worker, applies that process's settings.
        authored = {
            "image": image,
            "instance_type": instance_type,
            "region": region,
            "name_prefix": name_prefix,
            "ttl_seconds": ttl_seconds,
            "idle_timeout_seconds": idle_timeout_seconds,
            "default_exec_timeout_seconds": default_exec_timeout_seconds,
            "privileged": privileged,
            "docker_daemon_enabled": docker_daemon_enabled,
            "docker_daemon_network_mode": docker_daemon_network_mode,
            "enable_light_sleep": enable_light_sleep,
            "setup_script": setup_script,
            "setup_script_timeout_seconds": setup_script_timeout_seconds,
            "readiness_max_retries": readiness_max_retries,
            "readiness_interval_seconds": readiness_interval_seconds,
            "readiness_probe_timeout_seconds": readiness_probe_timeout_seconds,
            "wait_ready_timeout_seconds": wait_ready_timeout_seconds,
            "enable_mesh": enable_mesh,
            "pre_provisioned_sandbox_id": pre_provisioned_sandbox_id,
        }
        self.authored_settings: Mapping[str, Any] = {
            name: value for name, value in authored.items() if value is not None
        }
        settings = MistralSandboxSettings()
        self.image = image if image is not None else settings.image
        self.supports_background_processes = (
            image is None if supports_background_processes is None else supports_background_processes
        )
        self.instance_type = instance_type if instance_type is not None else settings.instance_type
        self.region = region if region is not None else settings.region
        self.name_prefix = name_prefix if name_prefix is not None else settings.name_prefix
        self.ttl_seconds = ttl_seconds if ttl_seconds is not None else settings.ttl_seconds
        self.idle_timeout_seconds = (
            idle_timeout_seconds if idle_timeout_seconds is not None else settings.idle_timeout_seconds
        )
        self.default_exec_timeout_seconds = (
            default_exec_timeout_seconds
            if default_exec_timeout_seconds is not None
            else settings.default_exec_timeout_seconds
        )
        self.privileged = privileged if privileged is not None else settings.privileged
        self.docker_daemon_enabled = (
            docker_daemon_enabled if docker_daemon_enabled is not None else settings.docker_daemon_enabled
        )
        self.docker_daemon_network_mode = (
            docker_daemon_network_mode
            if docker_daemon_network_mode is not None
            else settings.docker_daemon_network_mode
        )
        self.enable_light_sleep = enable_light_sleep if enable_light_sleep is not None else settings.enable_light_sleep
        self.setup_script = setup_script if setup_script is not None else settings.setup_script
        self.setup_script_timeout_seconds = (
            setup_script_timeout_seconds
            if setup_script_timeout_seconds is not None
            else settings.setup_script_timeout_seconds
        )
        self.readiness_max_retries = (
            readiness_max_retries if readiness_max_retries is not None else settings.readiness_max_retries
        )
        self.readiness_interval_seconds = (
            readiness_interval_seconds
            if readiness_interval_seconds is not None
            else settings.readiness_interval_seconds
        )
        self.readiness_probe_timeout_seconds = (
            readiness_probe_timeout_seconds
            if readiness_probe_timeout_seconds is not None
            else settings.readiness_probe_timeout_seconds
        )
        self.wait_ready_timeout_seconds = (
            wait_ready_timeout_seconds
            if wait_ready_timeout_seconds is not None
            else settings.wait_ready_timeout_seconds
        )
        self.enable_mesh = enable_mesh if enable_mesh is not None else settings.enable_mesh

        self.egress = egress
        self.pre_provisioned_sandbox_id = (
            pre_provisioned_sandbox_id
            if pre_provisioned_sandbox_id is not None
            else settings.pre_provisioned_sandbox_id
        )

    @property
    def egress_policy(self) -> EgressPolicy:
        """The IP-level policy that enforces ``network`` and ``egress`` on Koyeb."""

        if self.egress is not None:
            return self.egress
        return EgressPolicy.allow_all() if self.network.mode == "all" else EgressPolicy.block_all()

    def to_unified_state(self) -> dict[str, JsonValue]:
        return {
            "image": self.image,
            "supports_background_processes": self.supports_background_processes,
            "instance_type": self.instance_type,
            "region": self.region,
            "name_prefix": self.name_prefix,
            "ttl_seconds": self.ttl_seconds,
            "idle_timeout_seconds": self.idle_timeout_seconds,
            "default_exec_timeout_seconds": self.default_exec_timeout_seconds,
            "privileged": self.privileged,
            "docker_daemon_enabled": self.docker_daemon_enabled,
            "docker_daemon_network_mode": self.docker_daemon_network_mode,
            "enable_light_sleep": self.enable_light_sleep,
            "setup_script": self.setup_script,
            "setup_script_timeout_seconds": self.setup_script_timeout_seconds,
            "readiness_max_retries": self.readiness_max_retries,
            "readiness_interval_seconds": self.readiness_interval_seconds,
            "readiness_probe_timeout_seconds": self.readiness_probe_timeout_seconds,
            "wait_ready_timeout_seconds": self.wait_ready_timeout_seconds,
            "enable_mesh": self.enable_mesh,
            "egress": self.egress.model_dump(mode="json") if self.egress is not None else None,
            "pre_provisioned_sandbox_id": self.pre_provisioned_sandbox_id,
            "hooks": [hook.serialize_unified() for hook in self.hooks],
        }

    @classmethod
    def from_unified_state(cls, state: dict[str, JsonValue]) -> Self:
        values = dict(state)
        raw_hooks = values.pop("hooks", [])
        if not isinstance(raw_hooks, list):
            raise TypeError("MistralSandbox state hooks must be a list")
        parsed = _MistralSandboxState.model_validate(values)
        restored = cls(
            image=parsed.image,
            supports_background_processes=parsed.supports_background_processes,
            instance_type=parsed.instance_type,
            region=parsed.region,
            name_prefix=parsed.name_prefix,
            ttl_seconds=parsed.ttl_seconds,
            idle_timeout_seconds=parsed.idle_timeout_seconds,
            default_exec_timeout_seconds=parsed.default_exec_timeout_seconds,
            privileged=parsed.privileged,
            docker_daemon_enabled=parsed.docker_daemon_enabled,
            docker_daemon_network_mode=parsed.docker_daemon_network_mode,
            enable_light_sleep=parsed.enable_light_sleep,
            setup_script=parsed.setup_script,
            setup_script_timeout_seconds=parsed.setup_script_timeout_seconds,
            readiness_max_retries=parsed.readiness_max_retries,
            readiness_interval_seconds=parsed.readiness_interval_seconds,
            readiness_probe_timeout_seconds=parsed.readiness_probe_timeout_seconds,
            wait_ready_timeout_seconds=parsed.wait_ready_timeout_seconds,
            enable_mesh=parsed.enable_mesh,
            egress=parsed.egress,
            pre_provisioned_sandbox_id=parsed.pre_provisioned_sandbox_id,
            hooks=tuple(
                deserialize_unified(_JSON_OBJECT.validate_python(hook), expected=SandboxHook) for hook in raw_hooks
            ),
        )
        restored.setup_script = parsed.setup_script
        restored.pre_provisioned_sandbox_id = parsed.pre_provisioned_sandbox_id
        return restored


class LocalDockerSandbox(Sandbox):
    """Local Docker sandbox configuration for Unified Harness development.

    The container gets Docker's default network, so ``network`` must be ``Network.all()``.
    """

    supported_network = ("all",)

    def __init__(
        self,
        *,
        image: str | None = None,
        supports_background_processes: bool | None = None,
        shell: Literal["bash", "sh"] | None = None,
        default_exec_timeout_seconds: int | None = None,
        setup_script: str | None = None,
        setup_script_timeout_seconds: int | None = None,
        network: Network | None = None,
        header_bindings: Sequence[SandboxHeaderBinding] = (),
        hooks: Sequence[SandboxHook] = (),
        access: SandboxAccess | None = None,
    ) -> None:
        super().__init__(network=network, header_bindings=header_bindings, hooks=hooks, access=access)
        self.image = image
        self.supports_background_processes = (
            image is None if supports_background_processes is None else supports_background_processes
        )
        self.shell = shell
        self.default_exec_timeout_seconds = default_exec_timeout_seconds
        self.setup_script = setup_script
        self.setup_script_timeout_seconds = setup_script_timeout_seconds

    def to_unified_state(self) -> dict[str, JsonValue]:
        return {
            "image": self.image,
            "supports_background_processes": self.supports_background_processes,
            "shell": self.shell,
            "default_exec_timeout_seconds": self.default_exec_timeout_seconds,
            "setup_script": self.setup_script,
            "setup_script_timeout_seconds": self.setup_script_timeout_seconds,
            "hooks": [hook.serialize_unified() for hook in self.hooks],
        }

    @classmethod
    def from_unified_state(cls, state: dict[str, JsonValue]) -> Self:
        values = dict(state)
        raw_hooks = values.pop("hooks", [])
        if not isinstance(raw_hooks, list):
            raise TypeError("LocalDockerSandbox state hooks must be a list")
        parsed = _LocalDockerSandboxState.model_validate(values)
        return cls(
            image=parsed.image,
            supports_background_processes=parsed.supports_background_processes,
            shell=parsed.shell,
            default_exec_timeout_seconds=parsed.default_exec_timeout_seconds,
            setup_script=parsed.setup_script,
            setup_script_timeout_seconds=parsed.setup_script_timeout_seconds,
            hooks=tuple(
                deserialize_unified(_JSON_OBJECT.validate_python(hook), expected=SandboxHook) for hook in raw_hooks
            ),
        )


class DangerousLocalSandbox(Sandbox):
    """Host-local executor: runs commands directly in the worker process.

    DANGER: no container, no isolation — model-generated commands run on the host as
    the worker user. Dev/CI only; never enable in production.

    Commands reach every network the host reaches, so ``network`` must be ``Network.all()``.

    ``workspace`` is the host folder where commands run and the agent reads and writes files.
    Without it, the sandbox creates a new folder under
    ``~/.cache/mistral-vibe-harness-local-host/``. A relative ``workspace`` is resolved
    against the worker's working folder.

    ``delete_on_cleanup`` deletes the workspace when the session closes. It defaults to
    ``True`` without ``workspace`` and to ``False`` with one, so the sandbox never deletes
    your folder unless you ask. A workspace to delete must be absolute and must not contain
    your home folder or the worker's working folder; the session fails at start otherwise.
    """

    supported_network = ("all",)
    supports_background_processes = True

    def __init__(
        self,
        *,
        shell: Literal["bash", "sh"] | None = None,
        default_exec_timeout_seconds: int | None = None,
        workspace: str | None = None,
        delete_on_cleanup: bool | None = None,
        network: Network | None = None,
        header_bindings: Sequence[SandboxHeaderBinding] = (),
        hooks: Sequence[SandboxHook] = (),
        access: SandboxAccess | None = None,
    ) -> None:
        # A value that is not a SandboxHook is left to the Harness, which names it.
        if refused := [
            type(hook).__name__ for hook in hooks if isinstance(hook, SandboxHook) and hook._changes_host_state
        ]:
            raise ValueError(
                f"DangerousLocalSandbox runs on the host, so it refuses {', '.join(refused)}: "
                "it would change the host user's own configuration"
            )
        super().__init__(network=network, header_bindings=header_bindings, hooks=hooks, access=access)
        warnings.warn(
            "DangerousLocalSandbox runs model-generated commands directly on the host with "
            "no isolation. Use for local development and CI only.",
            stacklevel=2,
        )
        self.shell = shell
        self.default_exec_timeout_seconds = default_exec_timeout_seconds
        self.workspace = workspace
        self.delete_on_cleanup = workspace is None if delete_on_cleanup is None else delete_on_cleanup

    def to_unified_state(self) -> dict[str, JsonValue]:
        return {
            "shell": self.shell,
            "default_exec_timeout_seconds": self.default_exec_timeout_seconds,
            "workspace": self.workspace,
            "delete_on_cleanup": self.delete_on_cleanup,
            "hooks": [hook.serialize_unified() for hook in self.hooks],
        }

    @classmethod
    def from_unified_state(cls, state: dict[str, JsonValue]) -> Self:
        values = dict(state)
        raw_hooks = values.pop("hooks", [])
        if not isinstance(raw_hooks, list):
            raise TypeError("DangerousLocalSandbox state hooks must be a list")
        parsed = _DangerousLocalSandboxState.model_validate(values)
        return cls(
            shell=parsed.shell,
            default_exec_timeout_seconds=parsed.default_exec_timeout_seconds,
            workspace=parsed.workspace,
            delete_on_cleanup=parsed.delete_on_cleanup,
            hooks=tuple(
                deserialize_unified(_JSON_OBJECT.validate_python(hook), expected=SandboxHook) for hook in raw_hooks
            ),
        )


class BashkitSandbox(Sandbox):
    """Bashkit sandbox configuration for the Unified Harness runtime.

    Private and loopback addresses stay refused even when ``network`` allows them. Set
    ``block_private_ips=False`` to reach a service on your machine, for example in local tests.

    ``instance_id`` names the sandbox's host folders, together with each Session's id. Without
    it, the folders are named after the Session alone, so a new process that reopens the Session
    finds them again.
    """

    supported_network = ("none", "all", "allow")
    _supports_python = False

    def __init__(
        self,
        *,
        instance_id: str | None = None,
        network: Network | None = None,
        block_private_ips: bool = True,
        header_bindings: Sequence[SandboxHeaderBinding] = (),
        hooks: Sequence[SandboxHook] = (),
        access: SandboxAccess | None = None,
    ) -> None:
        super().__init__(network=network, header_bindings=header_bindings, hooks=hooks, access=access)
        self.instance_id = instance_id
        self.block_private_ips = block_private_ips

    def to_unified_state(self) -> dict[str, JsonValue]:
        return {
            "instance_id": self.instance_id,
            "block_private_ips": self.block_private_ips,
            "hooks": [hook.serialize_unified() for hook in self.hooks],
        }

    @classmethod
    def from_unified_state(cls, state: dict[str, JsonValue]) -> Self:
        values = dict(state)
        raw_hooks = values.pop("hooks", [])
        if not isinstance(raw_hooks, list):
            raise TypeError("BashkitSandbox state hooks must be a list")
        parsed = _BashkitSandboxState.model_validate(values)
        return cls(
            instance_id=parsed.instance_id,
            block_private_ips=parsed.block_private_ips,
            hooks=tuple(
                deserialize_unified(_JSON_OBJECT.validate_python(hook), expected=SandboxHook) for hook in raw_hooks
            ),
        )


_FILE_METHODS = ("write_files", "read_file")


class CustomSandbox(Sandbox):
    """Implement an SDK-owned sandbox with Vibe workflow request and result models.

    Declare in ``supported_network`` and ``supported_header_bindings`` what the sandbox enforces, and
    read ``self.network`` and ``self.header_bindings`` in ``create()``. The SDK refuses any other
    policy, ``Network.none()`` included, so a subclass that declares nothing cannot be built.

    Override ``write_files()`` and ``read_file()`` to let the sandbox receive files from the SDK, such as
    skill folders.
    """

    @property
    def workspace(self) -> str:
        return "/workspace"

    def _supports_files(self) -> bool:
        # Its driver forwards to the author's methods, so it also needs write_files() and read_file() overridden.
        overrides = all(getattr(type(self), name) is not getattr(CustomSandbox, name) for name in _FILE_METHODS)
        return self.is_executable and overrides

    async def create(self) -> str:
        raise NotImplementedError(f"{type(self).__name__}.create() is not implemented")

    async def delete(self) -> None:
        return None

    async def execute(
        self,
        request: WorkflowSandboxExecuteRequest,
    ) -> WorkflowSandboxExecuteResult:
        raise NotImplementedError(f"{type(self).__name__}.execute() is not implemented")

    async def read_file(
        self,
        request: WorkflowSandboxReadFileRequest,
    ) -> WorkflowSandboxReadFileResult:
        raise NotImplementedError(f"{type(self).__name__}.read_file() is not implemented")

    async def write_files(self, request: WorkflowSandboxWriteFilesRequest) -> WorkflowSandboxWriteFilesResult:
        """Write the files of ``request.source`` under ``request.root``, and return where they are.

        Optional: without it and ``read_file()``, the sandbox cannot hold skill folders. Like
        ``execute()``, this method runs in Workflow code, so pass ``request.source`` to your own
        activity and call ``resolve_file_source(source)`` there: the source holds references, and
        only the activity sees the bytes. With ``request.replace``, delete what the root holds first.
        """

        del request
        raise NotImplementedError(f"{type(self).__name__} cannot receive files from the SDK: implement write_files()")

    async def on_session_start(self) -> None:
        return None

    async def on_session_end(self) -> None:
        return None


def _reject_unserialized_extension_state(value: UnifiedSerializable) -> None:
    value_type = type(value)
    if isinstance(value, SandboxHook):
        default_rebuilder = inspect.getattr_static(SandboxHook, "from_unified_state")
        custom_rebuilder = inspect.getattr_static(value_type, "from_unified_state") is not default_rebuilder
        custom_serializer = not replays_constructor_arguments(value_type)
        # Either one alone would rebuild from state the other does not write.
        if custom_serializer and not custom_rebuilder:
            raise TypeError(f"{value_type.__name__} implements to_unified_state but not from_unified_state")
        if custom_rebuilder and not custom_serializer:
            raise TypeError(f"{value_type.__name__} implements from_unified_state but not to_unified_state")
        if custom_serializer:
            return
        # Raises when an argument is not JSON, naming the argument.
        state = value.to_unified_state()
        try:
            rebuilt = type(value).from_unified_state(state)
        except Exception as error:
            raise TypeError(
                f"{value_type.__name__} cannot be rebuilt: its constructor raised {type(error).__name__} "
                "when called again with its arguments"
            ) from error
        if not _same_attributes(value, rebuilt):
            raise TypeError(
                f"{value_type.__name__} holds state its constructor arguments do not rebuild; "
                "set it in the constructor or implement Unified Harness serialization"
            )
        return
    if not isinstance(value, CustomSandbox):
        return
    state = {name: field for name, field in vars(value).items() if name not in {"_hooks", "_access", "_policy"}}
    uses_default_serializer = value_type.to_unified_state is UnifiedSerializable.to_unified_state
    uses_default_deserializer = inspect.getattr_static(value_type, "from_unified_state") is inspect.getattr_static(
        UnifiedSerializable, "from_unified_state"
    )

    if state and (uses_default_serializer or uses_default_deserializer):
        raise TypeError(
            f"{value_type.__name__} has instance state but does not implement Unified Harness serialization"
        )


class Harness:
    """SDK-owned capability collection compiled by the Unified Harness runtime."""

    def __init__(
        self,
        *,
        sandbox: Sandbox | None = None,
        tools: HarnessTools | None = None,
        guardrails: Sequence[Hook] | None = None,
        hooks: Sequence[Hook] | None = None,
        connectors: Sequence[HarnessConnector] | None = None,
        skills: Sequence[HarnessSkill | SandboxWorkspaceSkills | AllRegistrySkills] | None = None,
        mcps: dict[str, McpHttpSourceConfiguration] | None = None,
        secrets: Mapping[str, SecretOrigin] | None = None,
    ) -> None:
        self._secrets = _checked_secret_origins(secrets or {})
        self._sandbox = (sandbox or NoSandbox()).bind_secret_origins(self._secrets)
        self._tools = tuple(tool_authoring.authored_tool(tool) for tool in tools or ())
        self._guardrails = tuple(guardrails or ())
        self._hooks = tuple(hooks or ())
        self._connectors, self._connector_discovery = split_connectors(connectors or ())
        self._skills, self._workspace_skills, self._skill_discovery = split_skills(skills or ())
        self._mcps = {name: source.model_copy(deep=True) for name, source in (mcps or {}).items()}
        if any(not isinstance(guardrail, Hook) for guardrail in self._guardrails):
            raise TypeError("Harness guardrails must subclass agents.Hook")
        if any(not isinstance(hook, Hook) for hook in self._hooks):
            raise TypeError("Harness hooks must subclass agents.Hook")
        if any(not isinstance(hook, SandboxHook) for hook in self._sandbox.hooks):
            raise TypeError("Sandbox hooks must subclass agents.SandboxHook")

    @property
    def sandbox(self) -> Sandbox:
        return self._sandbox

    @property
    def secrets(self) -> dict[str, SecretOrigin]:
        """The origin of each secret, by name."""

        return dict(self._secrets)

    @property
    def tools(self) -> Sequence[HarnessTool]:
        return tuple(self._tools)

    @property
    def guardrails(self) -> Sequence[Hook]:
        return tuple(self._guardrails)

    @property
    def hooks(self) -> Sequence[Hook]:
        return tuple(self._hooks)

    @property
    def connectors(self) -> Sequence[connector_decorator.ConnectorSlot]:
        return tuple(self._connectors)

    @property
    def connector_discovery(self) -> connector_selection.AllConnectors | None:
        return self._connector_discovery

    @property
    def skills(self) -> Sequence[HarnessSkill]:
        """The explicitly authored skills the SDK writes into the sandbox."""

        return tuple(self._skills)

    @property
    def skill_discovery(self) -> AllRegistrySkills | None:
        """Select Registry skills to discover when the root Session starts."""

        return self._skill_discovery

    @property
    def workspace_skills(self) -> Sequence[SandboxWorkspaceSkills]:
        """Where the SDK finds the skills already in the sandbox."""

        return tuple(self._workspace_skills)

    @property
    def mcps(self) -> dict[str, McpHttpSourceConfiguration]:
        return {name: source.model_copy(deep=True) for name, source in self._mcps.items()}

    def copy_for_isolation(self) -> Self:
        return deepcopy(self)


def _checked_secret_origins(secrets: Mapping[str, object]) -> dict[str, SecretOrigin]:
    # Errors name the secret, never its value: a raw value passed by mistake must not reach logs.
    checked: dict[str, SecretOrigin] = {}
    for name, origin in secrets.items():
        validate_secret_name(name)
        if not isinstance(origin, MistralSecret):
            raise TypeError(
                f"Secret {name!r} must be an agents.MistralSecret, "
                f"not a {type(origin).__name__}; pass where the value comes from, never the value"
            )
        if isinstance(origin, MistralSecret) and not origin.worker_env:
            raise ValueError(
                f"Secret {name!r} is a MistralSecret without worker_env=True, and no destination can "
                "read a MistralSecret yet; set worker_env=True to give it to the worker"
            )
        checked[name] = origin
    return checked


def requires_on_behalf_of(harness: Harness, subagents: Sequence[Subagent] | None = None) -> bool:
    """Whether this agent tree acts on behalf of the user who starts a session.

    Three authored capabilities borrow that user's identity at runtime, so the
    workflow must run ``on_behalf_of``:

    - connectors left at the default ``run_as="auto"`` resolve their credentials
      from the session user. A ``run_as="deployment"`` connector uses the
      deployment's own service identity instead, and the compiler rejects mixed
      ``run_as`` values within one agent, so the check is all-or-nothing across
      the connectors one agent declares. ``all_connectors()`` discovery always
      uses the session user's identity, including when ``auto_auth=False``.
    - ``all_registry_skills()`` reads the Registry catalog and skill contents with the
      session user's identity.
    - a sandbox with a GitHub binding or the Sandbox Proxy admin config gets short-lived
      credentials for the session user; without it the sandbox would run with the
      deployment's identity.

    Every child Session in the tree runs as the user who started its root, so a
    ``subagents`` entry, or one nested in it, whose own connectors borrow that
    user's identity makes the whole tree need it.
    """
    if harness.skill_discovery is not None or _connectors_act_for_user(harness.connectors, harness.connector_discovery):
        return True
    pending = list(subagents or ())
    while pending:
        layer = pending.pop()
        if _connectors_act_for_user(layer.connectors or (), layer.connector_discovery):
            return True
        pending.extend(layer.subagents or ())
    return any(
        isinstance(binding, GitHubBinding | WorkspaceHeaderBindings) for binding in harness.sandbox.header_bindings
    )


def subagents_can_share_sandbox(sandbox: Sandbox) -> bool:
    """Whether child Sessions can share this Sandbox with their root.

    Children inherit the root's Sandbox by borrowing it, and only the Mistral (Koyeb) Sandbox can
    be borrowed today. A Sandbox that cannot execute gives children nothing to borrow.
    """
    return isinstance(sandbox, MistralSandbox) or not sandbox.is_executable


def _connectors_act_for_user(
    slots: Sequence[connector_decorator.ConnectorSlot],
    discovery: connector_selection.AllConnectors | None,
) -> bool:
    if discovery is not None:
        return True
    return bool(slots) and all(slot.run_as.value == "auto" for slot in slots)


_HTTP_URL = TypeAdapter(AnyHttpUrl)


class RemoteMCP(McpHttpSourceConfiguration):
    """An MCP server the agent reaches over HTTP, declared under a name in ``Agent(mcps=...)``.

    The Harness model it extends ignores unknown fields so an older client keeps reading a newer
    server's Session. An author's declaration is checked strictly instead: a misspelled keyword is
    a ``TypeError``, and a bad value raises ``SdkError`` naming the argument.
    """

    def __init__(
        self,
        *,
        url: str,
        auth_header_env_vars: Mapping[str, str] | None = None,
        model_access: ToolModelAccess | None = None,
        disabled_tools: Sequence[str] | None = None,
        startup_timeout_seconds: float | None = None,
        tool_timeout_seconds: float | None = None,
        namespace: str | None = None,
        id: str | None = None,  # noqa: A002 - the Harness field's name
        name: str | None = None,
    ) -> None:
        """Declare a remote MCP server.

        Args:
            url: The server's ``http://`` or ``https://`` endpoint.
            auth_header_env_vars: Header name to the NAME of the environment variable holding that
                header's complete value, read where the agent runs.
            model_access: How the model reaches the server's tools. Unset, it is ``"direct"`` for an
                agent without programs and ``"programmatic"`` otherwise.
            disabled_tools: The server's own names of tools to leave out.
            startup_timeout_seconds: How long listing the server's tools may take. Defaults to 30.
            tool_timeout_seconds: How long one tool call may take. Defaults to 300.
            namespace: The namespace of the server's tools. Defaults to its key in ``mcps``.
            id: The source's ID in the Session.
            name: The source's display name in the Session.
        """

        # Only what the author passed, so an omitted argument stays out of ``model_fields_set``:
        # assembly reads that to tell an unset ``model_access`` from an explicit one.
        declared = {
            "url": url,
            "auth_header_env_vars": auth_header_env_vars,
            "model_access": model_access,
            "disabled_tools": disabled_tools,
            "startup_timeout_seconds": startup_timeout_seconds,
            "tool_timeout_seconds": tool_timeout_seconds,
            "namespace": namespace,
            "id": id,
            "name": name,
        }
        try:
            super().__init__(**{field: value for field, value in declared.items() if value is not None})
        except ValidationError as error:
            raise SdkError(f"Invalid RemoteMCP: {_validation_problems(error)}") from None

    @field_validator("url")
    @classmethod
    def _require_http_url(cls, value: str) -> str:
        # The Host checks the endpoint with the same rule when it connects; failing here instead
        # is an error at declaration, not a source silently dropped from the model's tools.
        url = value.strip()
        try:
            _HTTP_URL.validate_python(url)
        except ValidationError:
            raise ValueError(f"{value!r} is not an http:// or https:// URL with a host") from None
        return url


# Pydantic would show each field's camelCase wire alias; the keywords ``__init__`` takes are snake_case.
_init_signature = inspect.signature(RemoteMCP.__init__)
RemoteMCP.__signature__ = _init_signature.replace(parameters=list(_init_signature.parameters.values())[1:])


def _validation_problems(error: ValidationError) -> str:
    """Word ``error`` by argument name: the Harness model reports its camelCase wire aliases."""

    by_alias = {field.alias or name: name for name, field in RemoteMCP.model_fields.items()}
    problems = []
    for problem in error.errors(include_url=False):
        # Only the first part is an argument; the rest are the author's own dict keys and list indexes.
        location = [
            str(by_alias.get(str(part), part) if index == 0 else part) for index, part in enumerate(problem["loc"])
        ]
        message = problem["msg"].removeprefix("Value error, ")
        problems.append(f"{'.'.join(location)}: {message}" if location else message)
    return "; ".join(problems)


State = SerializedUnifiedObject


class _MistralSandboxState(BaseModel):
    image: str
    supports_background_processes: bool = True
    instance_type: str
    region: str
    name_prefix: str
    ttl_seconds: int
    idle_timeout_seconds: int
    default_exec_timeout_seconds: int
    privileged: bool
    docker_daemon_enabled: bool
    docker_daemon_network_mode: str
    enable_light_sleep: bool
    setup_script: str | None
    setup_script_timeout_seconds: int
    readiness_max_retries: int
    readiness_interval_seconds: float
    readiness_probe_timeout_seconds: int
    wait_ready_timeout_seconds: int
    enable_mesh: bool
    egress: EgressPolicy | None = None
    pre_provisioned_sandbox_id: str | None


class _LocalDockerSandboxState(BaseModel):
    image: str | None
    supports_background_processes: bool = True
    shell: Literal["bash", "sh"] | None
    default_exec_timeout_seconds: int | None
    setup_script: str | None
    setup_script_timeout_seconds: int | None


class _DangerousLocalSandboxState(BaseModel):
    shell: Literal["bash", "sh"] | None
    default_exec_timeout_seconds: int | None
    workspace: str | None = None
    delete_on_cleanup: bool | None = None


class _BashkitSandboxState(BaseModel):
    instance_id: str | None
    block_private_ips: bool = True


__all__ = [
    "BashkitSandbox",
    "CallbackContext",
    "CallbackSession",
    "HookCallbackContext",
    "CustomSandbox",
    "DangerousLocalSandbox",
    "Harness",
    "HarnessSkill",
    "EgressPolicy",
    "Hook",
    "SandboxExecutionResult",
    "LocalDockerSandbox",
    "LocalSkillBundle",
    "LocalSkillFile",
    "MistralSandbox",
    "NoSandbox",
    "PermissionMode",
    "RemoteMCP",
    "UnifiedSerializable",
    "Sandbox",
    "SandboxCallbackContext",
    "SandboxHook",
    "SerializedUnifiedObject",
    "State",
    "ToolCallbackContext",
    "deserialize_unified",
    "requires_on_behalf_of",
    "split_connectors",
    "split_skills",
    "subagents_can_share_sandbox",
]
