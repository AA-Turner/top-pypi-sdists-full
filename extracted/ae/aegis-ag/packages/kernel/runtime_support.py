"""Canonical event-to-outcome lifecycle orchestration.

The kernel is intentionally thin: it coordinates the turn lifecycle across the
shared contracts and capability ports without embedding provider, SQL, or
delivery specifics.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from html import unescape as html_unescape
import json
import os
from pathlib import Path
import re
from typing import Any, Protocol, runtime_checkable
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from packages.agent_runs import AgentRunService
from packages.capabilities.runtime import (
    ContextCapability,
    DeliveryAdapterCapability,
    MemoryCapability,
    ModelProviderCapability,
    PlanningCapability,
    TelemetrySinkCapability,
    ToolCapability,
)
from packages.embeddings import EmbeddingService
from packages.security import SecurityPolicy
from packages.contracts.runtime import (
    ActivityGraph,
    AgentRunState,
    AgentRunStep,
    CloneIdentityRecord,
    ContextBundle,
    EvidenceRetrievalRequest,
    EventEnvelope,
    ExecutionResult,
    GoalNode,
    IntentDecision,
    IntentResolutionRequest,
    MemoryRecord,
    PlanDraft,
    ProfileState,
    RelationshipMemoryRecord,
    SessionContinuityState,
    SessionState,
    UserCardRecord,
)
from packages.planning.runtime import PlanningDecision, build_plan_draft_from_decision, goal_graph_to_activity_graph
from packages.session import SessionLineageService
from packages.tools.tool_result_storage import (
    ToolResultBudgetConfig,
    enforce_tool_observation_budget,
    maybe_persist_tool_result,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@runtime_checkable
class KernelStoragePort(Protocol):
    """Typed storage port used by the kernel lifecycle."""

    def load_profile(self, profile_id: str) -> ProfileState | None:
        """Load a durable profile record."""

    def load_session(self, session_id: str) -> SessionState | None:
        """Load a durable session record."""

    def load_activity_graph(self, session_id: str) -> ActivityGraph | None:
        """Load the durable activity graph for a session."""

    def upsert_profile(
        self,
        profile: ProfileState,
        *,
        updated_at: datetime | None = None,
    ) -> None:
        """Persist a profile record."""

    def upsert_session(
        self,
        session: SessionState,
        *,
        resume_count_delta: int = 0,
    ) -> None:
        """Persist a session record."""

    def upsert_activity_graph(self, graph: ActivityGraph) -> None:
        """Persist a durable activity graph."""


@dataclass(frozen=True, slots=True)
class KernelDependencies:
    storage: KernelStoragePort
    context: ContextCapability
    planning: PlanningCapability
    memory: MemoryCapability
    model_provider: ModelProviderCapability
    telemetry: TelemetrySinkCapability
    tools: ToolCapability | None = None
    delivery: DeliveryAdapterCapability | None = None
    embedding_service: EmbeddingService | None = None
    security_policy: SecurityPolicy | None = None
    skill_runtime: object | None = None


@dataclass(frozen=True, slots=True)
class KernelTurnRequest:
    event: EventEnvelope
    prompt: str
    goal_query: str | None = None
    tool_name: str | None = None
    tool_arguments: Mapping[str, Any] = field(default_factory=dict)
    delivery_payload: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class KernelStageRecord:
    stage: str
    detail: str
    recorded_at: datetime


@dataclass(frozen=True, slots=True)
class KernelOutcome:
    event: EventEnvelope
    profile: ProfileState
    session: SessionState
    continuity: SessionContinuityState
    intent: IntentDecision
    goals: tuple[GoalNode, ...]
    goal_graph: ActivityGraph
    memories: tuple[MemoryRecord, ...]
    context: ContextBundle
    decision: PlanningDecision | None
    plan: PlanDraft | None
    run: AgentRunState | None
    execution: ExecutionResult
    delivery: ExecutionResult | None
    stages: tuple[KernelStageRecord, ...]


@dataclass(frozen=True, slots=True)
class _TextToolCall:
    tool_name: str
    arguments: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class _ParsedToolCalls:
    cleaned_text: str
    calls: tuple[_TextToolCall, ...]


_MAX_PARALLEL_TOOL_WORKERS = 8
_NEVER_PARALLEL_TOOLS = frozenset({"tool.clarify"})
_PARALLEL_SAFE_TOOLS = frozenset(
    {
        "tool.file.read",
        "tool.file.search",
        "tool.memory.recall",
        "tool.procedure.inspect",
        "tool.skill.list",
        "tool.skill.view",
        "tool.web.extract",
        "tool.web.read",
        "tool.web.search",
    }
)


@dataclass(frozen=True, slots=True)
class _ArtifactIntent:
    path: str


@dataclass(frozen=True, slots=True)
class _RecoveredStateBundle:
    identity: CloneIdentityRecord | None
    user: UserCardRecord | None
    relationship: RelationshipMemoryRecord | None

    @property
    def initiative_hint(self) -> str | None:
        if self.identity is None:
            return None
        return self.identity.initiative

    @property
    def continuity_notes(self) -> tuple[str, ...]:
        if self.relationship is None:
            return ()
        return self.relationship.continuity_notes


@dataclass(frozen=True, slots=True)
class _ClockContext:
    timezone_name: str
    session_start_local_datetime: datetime
    current_local_datetime: datetime
    session_start_local_date: str
    current_local_date: str
    session_start_weekday: str
    current_weekday: str
    date_changed: bool


@dataclass(frozen=True, slots=True)
class _MemoryRecoverySelection:
    memories: tuple[MemoryRecord, ...]
    query: str
    goal_ids: tuple[str, ...]
    scope_session_ids: tuple[str, ...]
    scope_reason: str


_TOOL_CALL_WRAPPER_PATTERN = re.compile(r"</?(?:[\w.-]+:)?tool_call[^>]*>", re.IGNORECASE)
_INVOKE_PATTERN = re.compile(
    r"<(?:[\w.-]+:)?invoke\s+name=(?P<quote>[\"'])(?P<name>.+?)(?P=quote)\s*>(?P<body>.*?)</(?:[\w.-]+:)?invoke>",
    re.IGNORECASE | re.DOTALL,
)
_PARAMETER_PATTERN = re.compile(
    r"<(?:[\w.-]+:)?parameter\s+name=(?P<quote>[\"'])(?P<name>.+?)(?P=quote)\s*>(?P<value>.*?)</(?:[\w.-]+:)?parameter>",
    re.IGNORECASE | re.DOTALL,
)


def _parse_text_tool_calls(raw: str) -> _ParsedToolCalls:
    calls: list[_TextToolCall] = []
    for match in _INVOKE_PATTERN.finditer(raw):
        tool_name = match.group("name").strip()
        if not tool_name:
            continue
        arguments: dict[str, Any] = {}
        for parameter in _PARAMETER_PATTERN.finditer(match.group("body")):
            name = parameter.group("name").strip()
            if not name:
                continue
            arguments[name] = _decode_text_tool_argument(parameter.group("value"))
        calls.append(_TextToolCall(tool_name=tool_name, arguments=arguments))
    cleaned = _strip_tool_markup(raw)
    return _ParsedToolCalls(cleaned_text=cleaned, calls=tuple(calls))


def _parse_execution_tool_calls(result: ExecutionResult) -> _ParsedToolCalls:
    cleaned = _strip_tool_markup(result.summary)
    if result.tool_calls:
        calls = tuple(
            _TextToolCall(
                tool_name=str(call.tool_name).strip(),
                arguments={str(key): value for key, value in call.arguments.items()},
            )
            for call in result.tool_calls
            if str(call.tool_name).strip()
        )
        return _ParsedToolCalls(cleaned_text=cleaned, calls=calls)
    return _parse_text_tool_calls(result.summary)


_JSON_LITERAL_PATTERN = re.compile(
    r"^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$"
)
_ARTIFACT_PATH_PATTERNS = (
    re.compile(
        r"""(?ix)
        \b(?:save|saved|write|written)\b
        (?:(?:\s+[a-z][\w-]*){0,6})?
        \s+(?:to|as|into)\s+
        (?P<path>["'`]?[^"'`\s,;:]+["'`]?)
        """
    ),
    re.compile(
        r"""(?ix)
        \b(?:file|markdown\s+file|report\s+file|notes\s+file)\b
        (?:(?:\s+[a-z][\w-]*){0,4})?
        \s+(?:named\s+)?
        (?P<path>["'`]?[^"'`\s,;:]+["'`]?)
        """
    ),
)


def _decode_text_tool_argument(raw_value: str) -> object:
    candidate = html_unescape(raw_value).strip()
    if not candidate:
        return ""
    if (
        candidate[0] in "[{\""
        or candidate in {"true", "false", "null"}
        or _JSON_LITERAL_PATTERN.match(candidate)
    ):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return candidate
    return candidate


def _strip_tool_markup(raw: str) -> str:
    cleaned = _INVOKE_PATTERN.sub("", raw)
    cleaned = _TOOL_CALL_WRAPPER_PATTERN.sub("", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _clean_execution_summary(result: ExecutionResult) -> ExecutionResult:
    cleaned = _dedupe_adjacent_repetition(_strip_tool_markup(result.summary))
    if not cleaned or cleaned == result.summary:
        return result
    return replace(result, summary=cleaned)


def _dedupe_adjacent_repetition(raw: str) -> str:
    text = raw.strip()
    if len(text) < 24:
        return text
    for separator in ("\n\n", "\n", " "):
        parts = [part.strip() for part in text.split(separator)]
        if len(parts) >= 2 and len(parts) % 2 == 0:
            midpoint = len(parts) // 2
            if parts[:midpoint] == parts[midpoint:] and any(part for part in parts[:midpoint]):
                return separator.join(parts[:midpoint]).strip()
    if len(text) % 2 == 0:
        midpoint = len(text) // 2
        left = text[:midpoint].strip()
        right = text[midpoint:].strip()
        if left and left == right:
            return left
    return text


def _with_execution_usage(
    result: ExecutionResult,
    *,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
    cached_prompt_tokens: int = 0,
    cache_creation_prompt_tokens: int = 0,
    cache_usage_reported: bool = False,
) -> ExecutionResult:
    return replace(
        result,
        prompt_tokens=max(0, prompt_tokens),
        completion_tokens=max(0, completion_tokens),
        total_tokens=max(0, total_tokens),
        cached_prompt_tokens=max(0, cached_prompt_tokens),
        cache_creation_prompt_tokens=max(0, cache_creation_prompt_tokens),
        cache_usage_reported=cache_usage_reported,
    )


def _augment_context_with_tool_results(
    context: ContextBundle,
    observations: list[str],
) -> ContextBundle:
    tool_section = "\n".join(("## runtime tool results", *observations))
    rendered_sections = [context.rendered_prompt or "", tool_section]
    artifact_ids = tuple((*context.artifact_ids, *(f"tool-result-{index + 1}" for index in range(len(observations)))))
    return replace(
        context,
        artifact_ids=artifact_ids,
        prompt_envelope=context.prompt_envelope.append_turn_injection(tool_section),
        rendered_prompt="\n\n".join(section for section in rendered_sections if section.strip()),
    )


def _execute_direct_tool_run(
    *,
    request: KernelTurnRequest,
    session: SessionState,
    tool_capability: ToolCapability,
    persist_agent_run: Any,
) -> tuple[ExecutionResult, AgentRunState]:
    run_service = AgentRunService()
    run = run_service.start_run(
        session_id=session.session_id,
        source_event_id=request.event.event_id,
        prompt=request.prompt,
    )
    persist_agent_run(run)
    result = tool_capability.invoke(
        request.tool_name or "",
        dict(request.tool_arguments),
        session_id=session.session_id,
    )
    run, tool_step = run_service.record_tool_step(
        run,
        tool_name=request.tool_name or "",
        arguments=request.tool_arguments,
        result=result,
    )
    persist_agent_run(run, step=tool_step)
    run = run_service.complete(run, summary=result.summary)
    persist_agent_run(run)
    return result, run


def _tool_followup_prompt(original_prompt: str, *, observations: tuple[str, ...]) -> str:
    result_block = "\n\n".join(observations)
    guided_prompt = _apply_request_execution_guidance(original_prompt)
    return (
        "Continue the same Aegis turn.\n"
        f"Original user request:\n{guided_prompt}\n\n"
        "The requested tool work has already been executed. Use the tool results below to answer directly as Aegis.\n"
        "If more tool work is still necessary, call another governed tool directly when native tool calling is available.\n"
        "When native tool calling is unavailable, you may emit another <tool_call> block with <invoke> and <parameter> tags.\n"
        "Do not repeat the exact same tool call with the same arguments after a validation error, noop result, or no-progress result; either correct the parameters or continue without it.\n"
        "Do not repeat raw tool-call markup in the final user-facing answer.\n\n"
        f"{result_block}"
    )


def _format_tool_arguments(arguments: Mapping[str, Any]) -> str:
    if not arguments:
        return "<none>"
    return ", ".join(f"{key}={_render_tool_argument_value(value)}" for key, value in sorted(arguments.items()))


def _tool_call_signature(call: _TextToolCall) -> str:
    payload = json.dumps(dict(sorted(call.arguments.items())), separators=(",", ":"), sort_keys=True)
    return f"{call.tool_name}:{payload}"


def _deduplicate_tool_calls(calls: Iterable[_TextToolCall]) -> tuple[_TextToolCall, ...]:
    unique: list[_TextToolCall] = []
    seen: set[str] = set()
    for call in calls:
        signature = _tool_call_signature(call)
        if signature in seen:
            continue
        seen.add(signature)
        unique.append(call)
    return tuple(unique)


def _should_parallelize_tool_batch(calls: tuple[_TextToolCall, ...]) -> bool:
    if len(calls) <= 1:
        return False
    for call in calls:
        if call.tool_name in _NEVER_PARALLEL_TOOLS:
            return False
        if call.tool_name == "tool.sub_agents":
            if not _sub_agents_call_is_parallel_safe(call):
                return False
            continue
        if call.tool_name not in _PARALLEL_SAFE_TOOLS:
            return False
        if (
            call.tool_name == "tool.file.read"
            and _normalized_tool_path(call.arguments.get("path")) is None
        ):
            return False
    return True


def _sub_agents_call_is_parallel_safe(call: _TextToolCall) -> bool:
    action = str(call.arguments.get("action") or "run").strip().lower()
    return action in {"start", "status", "check", "list"}


def _normalized_tool_path(raw_path: object) -> Path | None:
    if not isinstance(raw_path, (str, os.PathLike)):
        return None
    candidate = os.fspath(raw_path).strip()
    if not candidate:
        return None
    try:
        path = Path(candidate).expanduser()
        if not path.is_absolute():
            path = Path.cwd() / path
        return path.resolve(strict=False)
    except (OSError, RuntimeError, TypeError, ValueError):
        return None


def _render_tool_argument_value(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _model_turn_summary(result: ExecutionResult, *, parsed: _ParsedToolCalls) -> str:
    if parsed.cleaned_text.strip():
        return parsed.cleaned_text.strip()
    if parsed.calls:
        tool_list = ", ".join(call.tool_name for call in parsed.calls)
        return f"requested tool work: {tool_list}"
    return result.summary.strip()


def _resolve_clock_timezone(timezone_name: str | None) -> tuple[timezone | ZoneInfo, str]:
    candidate = str(timezone_name or "").strip()
    if candidate:
        try:
            return ZoneInfo(candidate), candidate
        except ZoneInfoNotFoundError:
            pass
    return timezone.utc, "UTC"


def _build_clock_context(
    session: SessionState,
    *,
    user: UserCardRecord | None,
    now: datetime | None = None,
) -> _ClockContext:
    resolved_now = now or _utc_now()
    if resolved_now.tzinfo is None:
        resolved_now = resolved_now.replace(tzinfo=timezone.utc)
    session_started_at = session.started_at
    if session_started_at.tzinfo is None:
        session_started_at = session_started_at.replace(tzinfo=timezone.utc)
    tzinfo, timezone_name = _resolve_clock_timezone(user.timezone if user is not None else None)
    session_local = session_started_at.astimezone(tzinfo)
    current_local = resolved_now.astimezone(tzinfo)
    return _ClockContext(
        timezone_name=timezone_name,
        session_start_local_datetime=session_local,
        current_local_datetime=current_local,
        session_start_local_date=session_local.date().isoformat(),
        current_local_date=current_local.date().isoformat(),
        session_start_weekday=session_local.strftime("%A"),
        current_weekday=current_local.strftime("%A"),
        date_changed=session_local.date() != current_local.date(),
    )


def _clock_prompt_sections(clock: _ClockContext) -> tuple[str, ...]:
    sections = [
        "\n".join(
            (
                "## runtime clock",
                f"- timezone: {clock.timezone_name}",
                f"- current local datetime: {clock.current_local_datetime.isoformat(timespec='seconds')}",
                f"- current local date: {clock.current_local_date} ({clock.current_weekday})",
                f"- session-start local date: {clock.session_start_local_date} ({clock.session_start_weekday})",
            )
        )
    ]
    if clock.date_changed:
        sections.append(
            "\n".join(
                (
                    "## runtime date change",
                    "- The local date has changed since this session started.",
                    f"- Today's local date is now {clock.current_local_date} ({clock.current_weekday}).",
                    f"- This session started on {clock.session_start_local_date} ({clock.session_start_weekday}).",
                    "- Use today's local date for any request about today/latest/current/recent information.",
                )
            )
        )
    return tuple(sections)


def _augment_context_with_clock(context: ContextBundle, *, clock: _ClockContext) -> ContextBundle:
    clock_sections = _clock_prompt_sections(clock)
    sections = [context.rendered_prompt or "", *clock_sections]
    artifact_ids = list(context.artifact_ids)
    artifact_ids.append("runtime-clock")
    if clock.date_changed:
        artifact_ids.append("runtime-date-change")
    return replace(
        context,
        artifact_ids=tuple(dict.fromkeys(artifact_ids)),
        prompt_envelope=context.prompt_envelope.append_turn_injection("\n\n".join(clock_sections)),
        rendered_prompt="\n\n".join(section for section in sections if section.strip()),
    )


def _has_temporal_request_markers(normalized_prompt: str) -> bool:
    temporal_markers = (
        "latest",
        "recent",
        "current",
        "today",
        "newest",
        "up-to-date",
        "this week",
        "this month",
        "this year",
        "今天",
        "今日",
        "当前",
        "现在",
        "最新",
        "近期",
        "最近",
        "本周",
        "本月",
        "今年",
        "刚刚",
        "刚发布",
    )
    return any(marker in normalized_prompt for marker in temporal_markers)


def _has_compare_request_markers(normalized_prompt: str) -> bool:
    return any(marker in normalized_prompt for marker in ("compare", "comparison", "versus", " vs ", "对比", "比较"))


def _apply_request_execution_guidance(prompt: str, *, clock: _ClockContext | None = None) -> str:
    if "Execution guidance for this turn:" in prompt:
        return prompt
    normalized = " ".join(prompt.casefold().split())
    if not normalized:
        return prompt
    multi_source = _looks_like_multi_source_research_request(normalized)
    artifact_intent = _artifact_intent_from_prompt(prompt)
    temporal_request = _has_temporal_request_markers(normalized)
    compare_request = _has_compare_request_markers(normalized)
    if not (multi_source or artifact_intent is not None or temporal_request or compare_request):
        return prompt
    lines = ["Execution guidance for this turn:"]
    if multi_source:
        lines.append("- Use more than one tool step and at least two distinct sources before concluding.")
        lines.append("- Preferred flow: tool.web.search first, then tool.web.extract or multiple tool.web.read calls, then synthesize.")
    if temporal_request:
        lines.append("- Prioritize current sources and pay attention to dates before summarizing.")
        if clock is not None:
            lines.append(
                f"- Current local datetime: {clock.current_local_datetime.isoformat(timespec='seconds')} ({clock.timezone_name})."
            )
            lines.append(
                f"- Current local date: {clock.current_local_date} ({clock.current_weekday}). Use this date in any search query about today/latest/current information and do not guess a stale year."
            )
            if clock.date_changed:
                lines.append(
                    f"- This session started on {clock.session_start_local_date}, but the local date has changed; prefer today's local date instead of the session-start date."
                )
    if compare_request:
        lines.append("- Compare approaches explicitly instead of returning a single-source note.")
    if artifact_intent is not None:
        lines.append(
            f"- The user explicitly requested a saved artifact at {artifact_intent.path}; complete the work and persist it there with tool.file.write or tool.code.execute."
        )
    return f"{prompt.rstrip()}\n\n" + "\n".join(lines)


def _looks_like_multi_source_research_request(normalized_prompt: str) -> bool:
    research_markers = (
        "research",
        "latest",
        "recent",
        "current",
        "approach",
        "approaches",
        "compare",
        "comparison",
        "ablation",
        "survey",
        "investigate",
    )
    synthesis_markers = ("summary", "summarize", "write a summary", "report", "overview")
    return any(marker in normalized_prompt for marker in research_markers) and (
        any(marker in normalized_prompt for marker in synthesis_markers)
        or any(marker in normalized_prompt for marker in ("compare", "comparison", "latest"))
    )


def _artifact_intent_from_prompt(prompt: str) -> _ArtifactIntent | None:
    for pattern in _ARTIFACT_PATH_PATTERNS:
        match = pattern.search(prompt)
        if match is None:
            continue
        candidate = _normalize_artifact_path_candidate(match.group("path"))
        if candidate is None:
            continue
        return _ArtifactIntent(path=candidate)
    return None


def _normalize_artifact_path_candidate(raw_value: str) -> str | None:
    candidate = raw_value.strip().strip("\"'`").rstrip(".,;:)]}")
    if not candidate or "://" in candidate:
        return None
    if "/" not in candidate and "." not in candidate:
        return None
    if "." not in Path(candidate).name:
        return None
    if candidate.startswith("-"):
        return None
    return candidate


def _tool_result_preview(summary: str, *, preview_chars: int) -> str:
    normalized = summary.strip()
    if preview_chars <= 0:
        return normalized
    if len(normalized) <= preview_chars:
        return normalized
    return f"{normalized[: max(0, preview_chars - 15)].rstrip()} ... [truncated]"


def _tool_result_budget_config(
    *,
    preview_chars: int,
    turn_budget_chars: int,
    persist_threshold_chars: int,
) -> ToolResultBudgetConfig:
    return ToolResultBudgetConfig(
        result_size_chars=persist_threshold_chars,
        turn_budget_chars=turn_budget_chars,
        preview_size_chars=preview_chars,
    )


def _budget_tool_result_summary(
    summary: str,
    *,
    tool_name: str,
    tool_use_id: str,
    config: ToolResultBudgetConfig,
) -> str:
    return maybe_persist_tool_result(
        summary,
        tool_name=tool_name,
        tool_use_id=tool_use_id,
        config=config,
    )


def _enforce_observation_budget(
    observations: list[str],
    *,
    turn_budget_chars: int | None = None,
    config: ToolResultBudgetConfig | None = None,
) -> list[str]:
    if config is None:
        config = ToolResultBudgetConfig(turn_budget_chars=turn_budget_chars or 0)
    return enforce_tool_observation_budget(observations, config=config)


__all__ = [name for name in globals() if not name.startswith("__")]
