"""Tool registry contracts and execution wiring.

Tools are executable capabilities with explicit side-effect metadata. This
module keeps the runtime boundary small: registry, approval policy, execution
backend, and the capability adapter that kernel code can call.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Literal, Mapping, Protocol, runtime_checkable

from packages.capabilities.runtime import CapabilityDescriptor, ToolCapability
from packages.contracts.runtime import ExecutionResult
from packages.security import ApprovalClass, PolicyDecision, SecurityPolicy, SecurityRequest, evaluate_with_telemetry


@dataclass(frozen=True, slots=True)
class ToolSideEffectMetadata:
    """Static metadata describing how a tool can affect the world."""

    risk_class: str = "low"
    approval_class: str = "standard"
    writes_state: bool = False
    reads_state: bool = False
    touches_network: bool = False
    touches_secrets: bool = False
    categories: tuple[str, ...] = ()
    notes: str | None = None


ToolAudience = Literal["model", "operator", "both"]
ToolRequester = Literal["model", "operator"]


@dataclass(frozen=True, slots=True)
class ToolAvailability:
    """Runtime-resolved availability state for a tool."""

    is_available: bool = True
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    """Serializable definition of a tool."""

    tool_id: str
    display_name: str
    version: str
    schema: Mapping[str, Any] = field(default_factory=dict)
    side_effects: ToolSideEffectMetadata = field(default_factory=ToolSideEffectMetadata)
    description: str = ""
    enabled: bool = True
    family: str = ""
    audience: ToolAudience = "both"
    availability: ToolAvailability = field(default_factory=ToolAvailability)
    backend: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)
    provenance: str = ""
    execution: Mapping[str, Any] = field(default_factory=dict)

    @property
    def available(self) -> bool:
        return self.availability.is_available

    def visible_to(self, audience: ToolAudience) -> bool:
        if self.audience == "both":
            return True
        return self.audience == audience

    @property
    def required_fields(self) -> tuple[str, ...]:
        required = self.schema.get("required", ())
        if not isinstance(required, list | tuple):
            return ()
        return tuple(str(item) for item in required if str(item).strip())

    def model_function_schema(self) -> dict[str, object]:
        return {
            "type": "function",
            "function": {
                "name": self.tool_id,
                "description": self.description,
                "parameters": dict(self.schema),
            },
        }

    def prompt_summary(self) -> str:
        required = ", ".join(self.required_fields) if self.required_fields else "none"
        properties = self.schema.get("properties", {})
        parameter_summaries: list[str] = []
        if isinstance(properties, Mapping):
            for name, payload in properties.items():
                if not isinstance(payload, Mapping):
                    parameter_summaries.append(str(name))
                    continue
                description = str(payload.get("description") or "").strip()
                type_name = payload.get("type")
                enum = payload.get("enum")
                parts = [str(name)]
                if type_name:
                    parts.append(f"type={type_name}")
                if enum:
                    parts.append(f"enum={tuple(enum)}")
                if description:
                    parts.append(description)
                parameter_summaries.append(" | ".join(parts))
        parameters = "; ".join(parameter_summaries) if parameter_summaries else "no parameters"
        return f"{self.tool_id}: {self.description} Required: {required}. Parameters: {parameters}."


def build_tool_fallback_prompt(tools: tuple[ToolDefinition, ...]) -> str:
    """Render a text fallback for transports without native tool calling."""

    if not tools:
        return ""
    tool_lines = "; ".join(
        f"{tool.display_name} ({tool.tool_id}): {tool.description}"
        for tool in tools
    )
    summaries = " ".join(tool.prompt_summary() for tool in tools)
    return (
        "available-tools: governed built-ins are available through the runtime; "
        f"{tool_lines}\n"
        "tool-call-protocol: call governed built-in tools directly when the active provider supports native "
        "tool calling. Otherwise emit <tool_call><invoke name=\"tool.id\"><parameter name=\"arg\">value"
        "</parameter></invoke></tool_call>; multiple invoke blocks are allowed, structured values may be "
        "encoded as JSON inside a parameter body, and the final answer must not include raw tool markup.\n"
        "tool-usage-discipline: use tools only when they materially advance the current request. "
        "For ordinary social conversation or acknowledgements with no durable state change, do not call any tool. "
        "A self-introduction or answer to a naming prompt in any language is a durable state change; capture the "
        "name with tool.profile.manage before replying. "
        "When the user shares durable identity, biography, preference, boundary, relationship, recurring-work, "
        "or stable personal facts, prefer tool.profile.manage if it is available. When the user changes Aegis "
        "display name, persona, personality, initiative, charter, or relationship stance, route that as "
        "profile identity or relationship state through tool.profile.manage as well; after profile writes, use updated facts naturally "
        "instead of narrating storage mechanics unless asked. Use tool.activity.manage for user-followed actionable "
        "work threads with progress state; never use it for greetings, biography, identity facts, preferences, or "
        "relationship notes. Before creating or splitting durable activity plans, shape one parent outcome plus "
        "stable child workstreams, normalize titles instead of copying user wording as flat goals, and use "
        "tool.clarify only if ambiguity in the parent outcome, child boundaries, or durable tracking scope would "
        "create a different activity tree; otherwise make a reasonable assumption and proceed. "
        "Treat activities as dynamic durable work threads: create only for followable work, focus when resuming "
        "or switching threads, update when scope/status/deadline/checkpoint changes, complete when finished, "
        "drop when canceled or no longer worth carrying, and delete only accidental or duplicate activity state. "
        "Use tool.process.manage only after a background process was started through "
        "tool.terminal.exec background=true. For complex tasks, cross-file changes, or work that clearly spans "
        "three or more meaningful steps, prefer using tool.todo.manage early to create or update a concise todo "
        "board even when the user did not explicitly request one. Use tool.todo.manage as an in-session execution "
        "board while working; do not use it as the durable tracking surface for user-followed work.\n"
        f"tool-parameter-schemas: {summaries}"
    )


@dataclass(frozen=True, slots=True)
class ToolInvocation:
    """Invocation record passed to the execution backend."""

    invocation_id: str
    tool_id: str
    session_id: str
    arguments: Mapping[str, Any] = field(default_factory=dict)
    requested_at: datetime | None = None
    requester: ToolRequester | None = None


@dataclass(frozen=True, slots=True)
class ToolExecutionRecord:
    """Normalized execution result with invocation provenance."""

    execution_id: str
    invocation: ToolInvocation
    result: ExecutionResult
    approved: bool
    approval: "ToolApprovalResult | None" = None
    side_effects: tuple[str, ...] = ()
    detail: str | None = None


@dataclass(frozen=True, slots=True)
class ToolManifest:
    source_path: str
    tools: tuple[ToolDefinition, ...]


@dataclass(frozen=True, slots=True)
class ToolManifestLoadRecord:
    source_path: str
    tool_ids: tuple[str, ...]
    executable_tool_ids: tuple[str, ...]
    loaded_at: datetime
    status: str = "loaded"
    detail: str | None = None


ToolApprovalDecision = Literal["approved", "denied", "deferred"]
ToolLifecyclePhase = Literal[
    "requested",
    "classified",
    "approval.granted",
    "approval.denied",
    "approval.deferred",
    "execution.started",
    "execution.completed",
    "execution.failed",
]


@dataclass(frozen=True, slots=True)
class ToolApprovalResult:
    decision: ToolApprovalDecision
    risk_class: str
    required_controls: tuple[str, ...] = ()
    reason: str | None = None
    approval_token: str | None = None

    @property
    def approved(self) -> bool:
        return self.decision == "approved"


@dataclass(frozen=True, slots=True)
class ToolLifecycleEvent:
    event_id: str
    invocation: ToolInvocation
    phase: ToolLifecyclePhase
    detail: str
    approval: ToolApprovalResult | None = None
    execution: ExecutionResult | None = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@runtime_checkable
class ToolRegistry(Protocol):
    def register(self, definition: ToolDefinition) -> None:
        """Register a tool definition."""

    def get(self, tool_id: str) -> ToolDefinition | None:
        """Return a tool definition if it is registered."""

    def list(self) -> tuple[ToolDefinition, ...]:
        """Return all registered tool definitions."""


@runtime_checkable
class ToolExecutionBackend(Protocol):
    def execute(self, definition: ToolDefinition, invocation: ToolInvocation) -> ExecutionResult:
        """Execute a tool definition for the provided invocation."""


ToolHandler = Callable[[ToolInvocation], Mapping[str, Any] | ExecutionResult]
ToolObserver = Callable[[ToolLifecycleEvent], None]


@runtime_checkable
class ApprovalGateway(Protocol):
    def authorize(
        self,
        definition: ToolDefinition,
        invocation: ToolInvocation,
    ) -> ToolApprovalResult:
        """Authorize a tool invocation before execution."""


@dataclass(frozen=True, slots=True)
class SecurityApprovalGateway:
    policy: SecurityPolicy
    telemetry: object
    source: str = "tool.runtime"
    auto_approve_deferred: bool = False

    def authorize(
        self,
        definition: ToolDefinition,
        invocation: ToolInvocation,
    ) -> ToolApprovalResult:
        request = _security_request_for_tool(definition, invocation)
        if request is None:
            return ToolApprovalResult(
                decision="approved",
                risk_class=definition.side_effects.risk_class,
                reason="No approval class was configured for this tool invocation.",
            )
        result = evaluate_with_telemetry(
            self.policy,
            request,
            self.telemetry,
            source=self.source,
        )
        decision = _tool_decision_from_policy(result.decision)
        reason = result.rationale
        approval_token: str | None = None
        if decision == "deferred":
            approval_token = f"approval:{invocation.invocation_id}"
            if self.auto_approve_deferred:
                decision = "approved"
                approval_token = f"auto:{invocation.invocation_id}"
                reason = (
                    f"{result.rationale} Auto-approved on {self.source} "
                    "until an external approval surface is configured."
                )
        return ToolApprovalResult(
            decision=decision,
            risk_class=result.risk_level.value,
            required_controls=result.required_controls,
            reason=reason,
            approval_token=approval_token,
        )


@dataclass(frozen=True, slots=True)
class CallableApprovalGateway:
    policy: Callable[[ToolDefinition, ToolInvocation], bool]

    def authorize(
        self,
        definition: ToolDefinition,
        invocation: ToolInvocation,
    ) -> ToolApprovalResult:
        approved = self.policy(definition, invocation)
        return ToolApprovalResult(
            decision="approved" if approved else "denied",
            risk_class=definition.side_effects.risk_class,
            reason=(
                "approved by callable approval gateway"
                if approved
                else "blocked by callable approval gateway"
            ),
        )


@runtime_checkable
class ToolLoader(Protocol):
    def load(self, path: Path) -> ToolManifest:
        """Load a tool manifest from disk."""


class JsonToolLoader:
    """Load tool manifests from a JSON-shaped file."""

    def load(self, path: Path) -> ToolManifest:
        payload = json.loads(path.read_text(encoding="utf-8"))
        tools = tuple(_tool_from_dict(item, source_path=path) for item in payload.get("tools", ()))
        return ToolManifest(source_path=str(path), tools=tools)


class InMemoryToolRegistry:
    """Small in-memory registry used by tests and local wiring."""

    def __init__(self) -> None:
        self._definitions: dict[str, ToolDefinition] = {}

    def register(self, definition: ToolDefinition) -> None:
        self._definitions[definition.tool_id] = definition

    def get(self, tool_id: str) -> ToolDefinition | None:
        return self._definitions.get(tool_id)

    def list(self) -> tuple[ToolDefinition, ...]:
        return tuple(self._definitions.values())


class InMemoryToolExecutor:
    """Bind tool handlers and execute them through a normalized contract."""

    def __init__(self) -> None:
        self._handlers: dict[str, ToolHandler] = {}

    def bind(self, tool_id: str, handler: ToolHandler) -> None:
        self._handlers[tool_id] = handler

    def execute(self, definition: ToolDefinition, invocation: ToolInvocation) -> ExecutionResult:
        handler = self._handlers.get(definition.tool_id)
        if handler is None:
            raise KeyError(f"no execution handler bound for tool: {definition.tool_id}")

        payload = handler(invocation)
        if isinstance(payload, ExecutionResult):
            return payload

        summary = str(payload.get("summary", definition.description or definition.display_name))
        outcome = str(payload.get("outcome", "success"))
        produced_artifact_ids = tuple(payload.get("produced_artifact_ids", ()))
        telemetry_event_ids = tuple(payload.get("telemetry_event_ids", ()))
        side_effects = tuple(payload.get("side_effects", definition.side_effects.categories))
        return ExecutionResult(
            execution_id=str(payload.get("execution_id", invocation.invocation_id)),
            session_id=invocation.session_id,
            outcome=outcome,
            summary=summary,
            produced_artifact_ids=produced_artifact_ids,
            telemetry_event_ids=telemetry_event_ids,
            side_effects=side_effects,
        )


class ToolRuntime(ToolCapability):
    """Capability adapter that enforces registry, approval, and execution flow."""

    def __init__(
        self,
        registry: ToolRegistry | None = None,
        executor: ToolExecutionBackend | None = None,
        approval_gateway: ApprovalGateway | None = None,
    ) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="tool.runtime",
            kind="tool_runtime",
            version="1.0.0",
            metadata={
                "description": "In-process tool execution adapter.",
            },
        )
        self._registry = registry or InMemoryToolRegistry()
        self._executor = executor or InMemoryToolExecutor()
        self._approval_gateway = approval_gateway
        self._executions: list[ToolExecutionRecord] = []
        self._manifest_loads: list[ToolManifestLoadRecord] = []
        self._observers: list[ToolObserver] = []
        self._observer_lock = Lock()

    @property
    def registry(self) -> ToolRegistry:
        return self._registry

    @property
    def executor(self) -> ToolExecutionBackend:
        return self._executor

    def register_tool(self, definition: ToolDefinition, handler: ToolHandler | None = None) -> None:
        self._register_tool(definition, handler=handler)

    def _register_tool(self, definition: ToolDefinition, handler: ToolHandler | None = None) -> bool:
        self._registry.register(definition)
        resolved_handler = handler or _handler_from_execution_spec(definition)
        if resolved_handler is not None and hasattr(self._executor, "bind"):
            self._executor.bind(definition.tool_id, resolved_handler)  # type: ignore[attr-defined]
            return True
        return False

    def describe(self, tool_id: str) -> ToolDefinition | None:
        return self._registry.get(tool_id)

    def list_tools(
        self,
        *,
        audience: ToolAudience | None = None,
        enabled_only: bool = False,
        available_only: bool = False,
    ) -> tuple[ToolDefinition, ...]:
        tools = self._registry.list()
        if audience is not None:
            tools = tuple(tool for tool in tools if tool.visible_to(audience))
        if enabled_only:
            tools = tuple(tool for tool in tools if tool.enabled)
        if available_only:
            tools = tuple(tool for tool in tools if tool.available)
        return tools

    def load_manifest(self, path: Path, loader: ToolLoader | None = None) -> ToolManifest:
        manifest = (loader or JsonToolLoader()).load(path)
        executable_tool_ids: list[str] = []
        for tool in manifest.tools:
            existing = self._registry.get(tool.tool_id)
            candidate = tool
            if existing is not None:
                if _tool_identity(existing) != _tool_identity(tool):
                    raise ValueError(
                        f"tool is already registered with different metadata: {tool.tool_id}"
                    )
                candidate = replace(tool, enabled=existing.enabled)
            bound = self._register_tool(candidate)
            if bound:
                executable_tool_ids.append(candidate.tool_id)
        self._manifest_loads.append(
            ToolManifestLoadRecord(
                source_path=manifest.source_path,
                tool_ids=tuple(tool.tool_id for tool in manifest.tools),
                executable_tool_ids=tuple(executable_tool_ids),
                loaded_at=datetime.now(timezone.utc),
            )
        )
        return manifest

    def list_manifest_loads(self) -> tuple[ToolManifestLoadRecord, ...]:
        return tuple(self._manifest_loads)

    def list_executions(self) -> tuple[ToolExecutionRecord, ...]:
        return tuple(self._executions)

    def subscribe(self, observer: ToolObserver) -> Callable[[], None]:
        with self._observer_lock:
            self._observers.append(observer)

        def _unsubscribe() -> None:
            with self._observer_lock:
                if observer in self._observers:
                    self._observers.remove(observer)

        return _unsubscribe

    def set_enabled(self, tool_id: str, enabled: bool) -> ToolDefinition:
        definition = self._registry.get(tool_id)
        if definition is None:
            raise KeyError(f"tool is not registered: {tool_id}")
        updated = replace(definition, enabled=enabled)
        self._registry.register(updated)
        return updated

    def invoke(
        self,
        tool_name: str,
        arguments: Mapping[str, Any],
        *,
        session_id: str,
        requester: ToolRequester | None = None,
    ) -> ExecutionResult:
        definition = self._registry.get(tool_name)
        if definition is None:
            raise KeyError(f"tool is not registered: {tool_name}")
        if not definition.enabled:
            raise ValueError(f"tool is disabled: {tool_name}")
        if not definition.available:
            detail = f"tool is unavailable: {tool_name}"
            if definition.availability.reason:
                detail += f" ({definition.availability.reason})"
            raise ValueError(detail)
        if requester is not None and not definition.visible_to(requester):
            raise PermissionError(f"tool is not visible to {requester}: {tool_name}")

        invocation = ToolInvocation(
            invocation_id=f"{session_id}:{tool_name}",
            tool_id=tool_name,
            session_id=session_id,
            arguments=dict(arguments),
            requested_at=datetime.now(timezone.utc),
            requester=requester,
        )
        self._emit_event(
            ToolLifecycleEvent(
                event_id=f"{invocation.invocation_id}:requested",
                invocation=invocation,
                phase="requested",
                detail=f"requested {tool_name}",
            )
        )

        approval = self._authorize(definition, invocation)
        self._emit_event(
            ToolLifecycleEvent(
                event_id=f"{invocation.invocation_id}:classified",
                invocation=invocation,
                phase="classified",
                detail=_classification_detail(definition, approval),
                approval=approval,
            )
        )
        self._emit_event(
            ToolLifecycleEvent(
                event_id=f"{invocation.invocation_id}:{_approval_phase(approval)}",
                invocation=invocation,
                phase=_approval_phase(approval),
                detail=approval.reason or f"approval {approval.decision} for {tool_name}",
                approval=approval,
            )
        )
        if not approval.approved:
            outcome = "deferred" if approval.decision == "deferred" else "blocked"
            blocked = ExecutionResult(
                execution_id=invocation.invocation_id,
                session_id=session_id,
                outcome=outcome,
                summary=approval.reason or f"tool invocation {approval.decision}: {tool_name}",
                side_effects=definition.side_effects.categories,
            )
            self._executions.append(
                ToolExecutionRecord(
                    execution_id=blocked.execution_id,
                    invocation=invocation,
                    result=blocked,
                    approved=False,
                    approval=approval,
                    side_effects=blocked.side_effects,
                    detail=approval.reason or f"approval {approval.decision}",
                )
            )
            return blocked

        self._emit_event(
            ToolLifecycleEvent(
                event_id=f"{invocation.invocation_id}:execution.started",
                invocation=invocation,
                phase="execution.started",
                detail=f"executing {tool_name}",
                approval=approval,
            )
        )

        try:
            result = self._executor.execute(definition, invocation)
        except Exception as error:
            failure = ExecutionResult(
                execution_id=invocation.invocation_id,
                session_id=session_id,
                outcome="error",
                summary=str(error),
                side_effects=definition.side_effects.categories,
            )
            self._executions.append(
                ToolExecutionRecord(
                    execution_id=failure.execution_id,
                    invocation=invocation,
                    result=failure,
                    approved=approval.approved,
                    approval=approval,
                    side_effects=failure.side_effects,
                    detail=str(error),
                )
            )
            self._emit_event(
                ToolLifecycleEvent(
                    event_id=f"{invocation.invocation_id}:execution.failed",
                    invocation=invocation,
                    phase="execution.failed",
                    detail=str(error),
                    approval=approval,
                    execution=failure,
                )
            )
            raise
        if result.side_effects:
            final = result
        else:
            final = replace(result, side_effects=definition.side_effects.categories, session_id=session_id)
        self._executions.append(
            ToolExecutionRecord(
                execution_id=final.execution_id,
                invocation=invocation,
                result=final,
                approved=approval.approved,
                approval=approval,
                side_effects=final.side_effects,
                detail=final.summary,
            )
        )
        self._emit_event(
            ToolLifecycleEvent(
                event_id=f"{invocation.invocation_id}:execution.completed",
                invocation=invocation,
                phase="execution.completed",
                detail=final.summary,
                approval=approval,
                execution=final,
            )
        )
        return final

    def _authorize(
        self,
        definition: ToolDefinition,
        invocation: ToolInvocation,
    ) -> ToolApprovalResult:
        if definition.side_effects.approval_class == "none":
            return ToolApprovalResult(
                decision="approved",
                risk_class=definition.side_effects.risk_class,
                reason="approval bypassed because approval_class=none",
            )
        if self._approval_gateway is None:
            return ToolApprovalResult(
                decision="approved",
                risk_class=definition.side_effects.risk_class,
                reason="tool runtime has no approval gateway configured",
            )
        return self._approval_gateway.authorize(definition, invocation)

    def _emit_event(self, event: ToolLifecycleEvent) -> None:
        with self._observer_lock:
            observers = tuple(self._observers)
        for observer in observers:
            try:
                observer(event)
            except Exception:
                continue


def _tool_from_dict(payload: Mapping[str, Any], *, source_path: Path | None = None) -> ToolDefinition:
    side_effects_payload = payload.get("side_effects", {})
    availability_payload = payload.get("availability", {})
    if isinstance(availability_payload, Mapping):
        availability = ToolAvailability(
            is_available=bool(availability_payload.get("is_available", True)),
            reason=str(availability_payload.get("reason")) if availability_payload.get("reason") is not None else None,
        )
    else:
        availability = ToolAvailability(is_available=bool(availability_payload))
    return ToolDefinition(
        tool_id=payload["tool_id"],
        display_name=payload["display_name"],
        version=payload["version"],
        schema=payload.get("schema", {}),
        side_effects=ToolSideEffectMetadata(
            risk_class=side_effects_payload.get("risk_class", "low"),
            approval_class=side_effects_payload.get("approval_class", "standard"),
            writes_state=bool(side_effects_payload.get("writes_state", False)),
            reads_state=bool(side_effects_payload.get("reads_state", False)),
            touches_network=bool(side_effects_payload.get("touches_network", False)),
            touches_secrets=bool(side_effects_payload.get("touches_secrets", False)),
            categories=tuple(side_effects_payload.get("categories", ())),
            notes=side_effects_payload.get("notes"),
        ),
        description=payload.get("description", ""),
        enabled=payload.get("enabled", True),
        family=str(payload.get("family") or ""),
        audience=str(payload.get("audience") or "both"),
        availability=availability,
        backend=str(payload.get("backend") or ""),
        metadata=payload.get("metadata", {}),
        provenance=str(payload.get("provenance") or source_path or ""),
        execution=payload.get("execution", {}),
    )


def _tool_identity(definition: ToolDefinition) -> ToolDefinition:
    return replace(definition, enabled=True)


def _handler_from_execution_spec(definition: ToolDefinition) -> ToolHandler | None:
    if not definition.execution:
        return None
    kind = str(definition.execution.get("kind", "")).strip()
    if kind == "structured_result":
        outcome = str(definition.execution.get("outcome", "success"))
        summary_template = str(
            definition.execution.get("summary_template", definition.description or definition.display_name)
        )
        execution_template = str(definition.execution.get("execution_id_template", "{invocation_id}"))
        produced_artifact_ids = tuple(definition.execution.get("produced_artifact_ids", ()))
        telemetry_event_ids = tuple(definition.execution.get("telemetry_event_ids", ()))
        side_effects = tuple(definition.execution.get("side_effects", definition.side_effects.categories))

        def _handler(invocation: ToolInvocation) -> Mapping[str, Any]:
            values = {
                "invocation_id": invocation.invocation_id,
                "session_id": invocation.session_id,
                "tool_id": invocation.tool_id,
                **{str(key): value for key, value in invocation.arguments.items()},
            }
            return {
                "execution_id": execution_template.format_map(_SafeFormatMap(values)),
                "outcome": outcome,
                "summary": summary_template.format_map(_SafeFormatMap(values)),
                "produced_artifact_ids": produced_artifact_ids,
                "telemetry_event_ids": telemetry_event_ids,
                "side_effects": side_effects,
            }

        return _handler
    raise ValueError(f"unsupported tool execution kind: {kind or '<empty>'}")


class _SafeFormatMap(dict[str, Any]):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def _tool_decision_from_policy(decision: PolicyDecision) -> ToolApprovalDecision:
    if decision == PolicyDecision.ALLOW:
        return "approved"
    if decision == PolicyDecision.DENY:
        return "denied"
    return "deferred"


def _approval_phase(approval: ToolApprovalResult) -> ToolLifecyclePhase:
    if approval.decision == "approved":
        return "approval.granted"
    if approval.decision == "denied":
        return "approval.denied"
    return "approval.deferred"


def _classification_detail(definition: ToolDefinition, approval: ToolApprovalResult) -> str:
    controls = ", ".join(approval.required_controls) or "<none>"
    return (
        f"{definition.tool_id} classified as risk={approval.risk_class}; "
        f"decision={approval.decision}; controls={controls}"
    )


def _security_request_for_tool(
    definition: ToolDefinition,
    invocation: ToolInvocation,
) -> SecurityRequest | None:
    approval_class = _resolve_approval_class(definition.side_effects)
    if approval_class is None:
        return None
    return SecurityRequest(
        request_id=f"req:tool:{invocation.invocation_id}",
        approval_class=approval_class,
        operation=definition.tool_id,
        session_id=invocation.session_id,
        description=definition.description or definition.display_name,
        is_external=definition.side_effects.touches_network,
        is_destructive=definition.side_effects.writes_state,
        consent_given=False,
        target_trusted=False,
        metadata={
            "tool_id": definition.tool_id,
            "approval_class": approval_class.value,
            "risk_class": definition.side_effects.risk_class,
        },
    )


def _resolve_approval_class(side_effects: ToolSideEffectMetadata) -> ApprovalClass | None:
    raw = side_effects.approval_class.strip().lower()
    if raw in {"", "none"}:
        return None
    for approval_class in ApprovalClass:
        if raw == approval_class.value:
            return approval_class
    if raw == "strict":
        if side_effects.touches_network:
            return ApprovalClass.NETWORK
        if side_effects.writes_state and side_effects.reads_state:
            return ApprovalClass.EXEC
        if side_effects.writes_state:
            return ApprovalClass.WRITE
        return ApprovalClass.EXEC
    if raw == "standard":
        if side_effects.touches_network:
            return ApprovalClass.NETWORK
        if side_effects.writes_state:
            return ApprovalClass.WRITE
        return ApprovalClass.READ
    return ApprovalClass.WRITE if side_effects.writes_state else ApprovalClass.READ
