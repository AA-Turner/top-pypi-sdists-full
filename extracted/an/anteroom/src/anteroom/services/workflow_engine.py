"""Workflow engine — load, validate, and execute workflow definitions.

The engine core is domain-neutral. It orchestrates steps (runner, gate, loop)
defined in YAML without knowledge of what domain the workflow serves. Domain-
specific behavior (GitHub issue checks, PR creation, code review) lives in
workflow definitions, gate conditions, and runner adapters — not here.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import shlex
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

if TYPE_CHECKING:
    from ..config import WorkflowConfig
    from ..db import ThreadSafeConnection
    from .workflow_runners import RunnerRegistry, RunnerResult

logger = logging.getLogger(__name__)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Definition dataclasses (domain-neutral)
# ---------------------------------------------------------------------------


@dataclass
class WorkflowStepDef:
    """A single step in a workflow definition. Domain-neutral."""

    id: str
    type: str  # "runner", "gate", "loop"
    # Runner fields (opaque + agent)
    runner: str | None = None
    command: str | None = None  # shell: command string; python_script: script path
    argv: list[str] | None = None  # python_script: positional args
    prompt: str | None = None  # agent runners: user prompt
    system_prompt: str | None = None  # agent runners: system prompt override
    context_from: list[dict[str, str]] | None = None  # artifact refs from prior steps
    tools: list[str] | None = None  # agent runners: tool filter
    env: dict[str, str] | None = None  # additional env vars
    working_dir: str | None = None  # cwd override
    credentials: list[dict[str, str]] | None = None  # [{"name": "MY_KEY", "from": "cred_name"}]
    # Artifact integration (#957)
    skill_name: str | None = None  # skill to resolve and expand as prompt
    skill_args: str | None = None  # args for skill prompt expansion
    inject_rules: bool | None = None  # inject RULE/INSTRUCTION artifacts into system_prompt
    inject_conventions: bool | None = None  # inject global ANTEROOM.md into system_prompt
    # Gate fields
    condition: str | None = None
    if_false: str | None = None
    # Loop fields
    max_rounds: int | None = None
    steps: list[WorkflowStepDef] | None = None
    # Human gate fields
    options: list[dict[str, Any]] | None = None
    on_timeout: dict[str, Any] | None = None
    # Publish step fields (#966)
    destination: dict[str, Any] | None = None
    # Conditional execution (#959)
    when: dict[str, Any] | None = None
    # Retry configuration (#962)
    retry: dict[str, Any] | None = None
    # Common
    approval_mode: str | None = None
    timeout: int | None = None


@dataclass
class WorkflowDefinition:
    """A parsed workflow definition. Domain-neutral."""

    id: str
    version: str
    inputs: dict[str, dict[str, Any]] = field(default_factory=dict)
    policies: dict[str, Any] = field(default_factory=dict)
    steps: list[WorkflowStepDef] = field(default_factory=list)
    notifications: dict[str, Any] | None = None
    raw_yaml: bytes = field(default=b"", repr=False)
    content_hash: str = ""


# ---------------------------------------------------------------------------
# Gate condition registry (domain-neutral interface)
# ---------------------------------------------------------------------------

GateConditionFn = Any  # Callable[[dict, WorkflowStepDef], Awaitable[bool]]

_gate_registry: dict[str, GateConditionFn] = {}


def register_gate_condition(name: str, fn: GateConditionFn) -> None:
    _gate_registry[name] = fn


def get_gate_condition(name: str) -> GateConditionFn | None:
    return _gate_registry.get(name)


# ---------------------------------------------------------------------------
# Template resolution (domain-neutral)
# ---------------------------------------------------------------------------


def resolve_template(template: str, variables: dict[str, Any], *, shell_quote: bool = False) -> str:
    """Resolve {variable} placeholders from workflow inputs.

    If shell_quote=True, values are passed through shlex.quote() before
    interpolation (used for shell runner commands). Template variables
    must reference declared inputs only — undeclared variables raise KeyError.
    """
    resolved = {}
    for key, val in variables.items():
        str_val = str(val)
        resolved[key] = shlex.quote(str_val) if shell_quote else str_val
    return template.format(**resolved)


def resolve_context_from(
    context_refs: list[dict[str, str]],
    step_results: dict[str, dict[str, Any]],
    db: Any | None = None,
) -> str:
    """Resolve context_from references into a context string.

    Supports three ref types:
    - {"step": "<step_id>", "field": "<dotted.path>"} — prior step output
    - {"source_id": "<uuid>"} — Anteroom source by ID (#957)
    - {"source_group_id": "<uuid>"} — all sources in a group (#957)

    step_results maps step_id → step record dict (from storage).
    db is required for source/source_group refs.
    Returns a newline-joined string of resolved context values.
    """
    parts: list[str] = []
    for ref in context_refs:
        if "step" in ref:
            step_id = ref["step"]
            field_path = ref.get("field", "")
            step_data = step_results.get(step_id)
            if step_data is None:
                logger.warning("context_from: step %r not found in results", step_id)
                continue
            value = _resolve_dotted_path(step_data, field_path)
            if value is not None:
                parts.append(f"[{step_id}.{field_path}]\n{value}")
        elif "source_id" in ref:
            content = _resolve_source_ref(ref["source_id"], db)
            if content:
                parts.append(content)
        elif "source_group_id" in ref:
            content = _resolve_source_group_ref(ref["source_group_id"], db)
            if content:
                parts.append(content)
        else:
            logger.warning("context_from: unrecognized ref type: %s", ref)
    return "\n\n".join(parts)


def _resolve_source_ref(source_id: str, db: Any | None) -> str | None:
    """Resolve a source by UUID and return its content wrapped as untrusted."""
    if db is None:
        logger.warning("context_from source_id requires db connection")
        return None
    try:
        from .storage import get_source

        source = get_source(db, source_id)
        if source is None:
            logger.warning("context_from: source %r not found", source_id)
            return None
        content = source.get("content") or ""
        if not content:
            return None
        from .context_trust import wrap_untrusted

        return wrap_untrusted(content, origin=f"source:{source_id}", content_type="source")
    except Exception:
        logger.warning("Failed to resolve source %r", source_id, exc_info=True)
        return None


def _resolve_source_group_ref(group_id: str, db: Any | None) -> str | None:
    """Resolve all sources in a group and return concatenated content."""
    if db is None:
        logger.warning("context_from source_group_id requires db connection")
        return None
    try:
        from .storage import list_sources

        sources = list_sources(db, group_id=group_id)
        if not sources:
            logger.warning("context_from: source group %r empty or not found", group_id)
            return None
        parts = []
        from .context_trust import wrap_untrusted

        for src in sources:
            content = src.get("content") or ""
            if content:
                parts.append(wrap_untrusted(content, origin=f"source_group:{group_id}", content_type="source"))
        return "\n\n".join(parts) if parts else None
    except Exception:
        logger.warning("Failed to resolve source group %r", group_id, exc_info=True)
        return None


def _resolve_dotted_path(data: dict[str, Any], path: str) -> Any:
    """Resolve a dotted field path like 'result_artifacts.pr_number'."""
    current: Any = data
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


# ---------------------------------------------------------------------------
# Definition loader
# ---------------------------------------------------------------------------


def load_definition(source: str | Path) -> WorkflowDefinition:
    """Load and validate a workflow definition from YAML.

    source can be a file path or a YAML string (for testing).
    Retains raw bytes and computes SHA-256 content hash for drift detection (#964).
    """
    raw_bytes: bytes
    if isinstance(source, Path) or (isinstance(source, str) and "\n" not in source and source.endswith(".yaml")):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Workflow definition not found: {path}")
        raw_bytes = path.read_bytes()
        raw = yaml.safe_load(raw_bytes)
    else:
        raw_bytes = source.encode("utf-8") if isinstance(source, str) else source
        raw = yaml.safe_load(raw_bytes)

    if not isinstance(raw, dict):
        raise ValueError("Workflow definition must be a YAML mapping")
    if raw.get("kind") != "workflow":
        raise ValueError(f"Expected kind: workflow, got: {raw.get('kind')!r}")
    if not raw.get("id"):
        raise ValueError("Workflow definition must have an 'id' field")
    if not raw.get("version"):
        raise ValueError("Workflow definition must have a 'version' field")

    steps = [_parse_step(s) for s in raw.get("steps", [])]
    if not steps:
        raise ValueError("Workflow definition must have at least one step")

    content_hash = hashlib.sha256(raw_bytes).hexdigest()

    defn = WorkflowDefinition(
        id=raw["id"],
        version=raw["version"],
        inputs=raw.get("inputs", {}),
        policies=raw.get("policies", {}),
        steps=steps,
        notifications=raw.get("notifications"),
        raw_yaml=raw_bytes,
        content_hash=content_hash,
    )
    _validate_definition(defn)
    return defn


def _parse_step(raw: dict[str, Any]) -> WorkflowStepDef:
    if not raw.get("id"):
        raise ValueError("Each step must have an 'id' field")
    if not raw.get("type"):
        raise ValueError(f"Step {raw['id']!r} must have a 'type' field")
    step_type = raw["type"]
    if step_type not in ("runner", "gate", "loop", "human_gate", "publish"):
        raise ValueError(f"Step {raw['id']!r}: invalid type {step_type!r}")

    nested_steps = None
    if step_type == "loop":
        nested_raw = raw.get("steps", [])
        nested_steps = [_parse_step(s) for s in nested_raw]

    return WorkflowStepDef(
        id=raw["id"],
        type=step_type,
        runner=raw.get("runner"),
        command=raw.get("command"),
        argv=raw.get("argv"),
        prompt=raw.get("prompt"),
        system_prompt=raw.get("system_prompt"),
        context_from=raw.get("context_from"),
        tools=raw.get("tools"),
        env=raw.get("env"),
        working_dir=raw.get("working_dir"),
        condition=raw.get("condition"),
        if_false=raw.get("if_false"),
        max_rounds=raw.get("max_rounds"),
        steps=nested_steps,
        options=raw.get("options"),
        on_timeout=raw.get("on_timeout"),
        credentials=raw.get("credentials"),
        destination=raw.get("destination"),
        skill_name=raw.get("skill_name"),
        skill_args=raw.get("skill_args"),
        inject_rules=raw.get("inject_rules"),
        inject_conventions=raw.get("inject_conventions"),
        retry=raw.get("retry"),
        approval_mode=raw.get("approval_mode"),
        timeout=raw.get("timeout"),
        when=raw.get("when"),
    )


def _validate_definition(defn: WorkflowDefinition) -> None:
    """Validate step payloads and context_from references at load time.

    Ensures:
    - Shell runner steps have a command
    - Agent runner steps have a prompt
    - Gate steps have a condition
    - context_from references point to steps that appear earlier in execution order
    """
    from .workflow_runners import AGENT_RUNNER_TYPES

    all_steps = _all_steps(defn.steps)
    seen_step_ids: set[str] = set()

    for step in all_steps:
        if step.type == "runner":
            if not step.runner:
                raise ValueError(f"Runner step {step.id!r} has no runner type")
            if step.runner in ("shell",) and not step.command:
                raise ValueError(f"Shell runner step {step.id!r} requires a 'command' field")
            if step.runner == "python_script" and not step.command:
                raise ValueError(f"Python script runner step {step.id!r} requires a 'command' field")
            if step.runner in AGENT_RUNNER_TYPES and not step.prompt and not step.skill_name:
                raise ValueError(f"Agent runner step {step.id!r} requires a 'prompt' or 'skill_name' field")
            if step.skill_name and step.runner not in AGENT_RUNNER_TYPES:
                raise ValueError(f"Step {step.id!r}: skill_name requires an agent runner, got {step.runner!r}")
        elif step.type == "gate":
            if not step.condition:
                raise ValueError(f"Gate step {step.id!r} requires a 'condition' field")
        elif step.type == "human_gate":
            if not step.prompt:
                raise ValueError(f"Human gate step {step.id!r} requires a 'prompt' field")
            if not step.options:
                raise ValueError(f"Human gate step {step.id!r} requires an 'options' field")
            for opt in step.options:
                if not opt.get("id") or not opt.get("label") or not opt.get("outcome"):
                    raise ValueError(f"Human gate step {step.id!r}: each option needs 'id', 'label', 'outcome'")
                if opt["outcome"] == "branch" and not opt.get("next_step"):
                    raise ValueError(f"Human gate step {step.id!r}: branch option {opt['id']!r} requires 'next_step'")
                if opt["outcome"] == "stop" and not opt.get("stop_reason"):
                    raise ValueError(f"Human gate step {step.id!r}: stop option {opt['id']!r} requires 'stop_reason'")
                # Validate branch targets: top-level forward only
                if opt["outcome"] == "branch":
                    top_level_ids = [s.id for s in defn.steps]
                    target = opt["next_step"]
                    if target not in top_level_ids:
                        raise ValueError(
                            f"Human gate step {step.id!r}: branch target {target!r} not found in top-level steps"
                        )
                    current_idx = top_level_ids.index(step.id) if step.id in top_level_ids else -1
                    target_idx = top_level_ids.index(target)
                    if target_idx <= current_idx:
                        raise ValueError(
                            f"Human gate step {step.id!r}: branch target {target!r} must appear"
                            f" after the current step (forward-only in V1)"
                        )

        if step.credentials:
            if not isinstance(step.credentials, list):
                raise ValueError(f"Step {step.id!r}: 'credentials' must be a list")
            for cred in step.credentials:
                if not isinstance(cred, dict):
                    raise ValueError(f"Step {step.id!r}: each credential entry must be a mapping")

        if step.context_from:
            for ref in step.context_from:
                ref_step = ref.get("step")
                if not ref_step:
                    raise ValueError(f"Step {step.id!r}: context_from entry missing 'step' field")
                if not ref.get("field"):
                    raise ValueError(f"Step {step.id!r}: context_from entry missing 'field' field")
                if ref_step not in seen_step_ids:
                    raise ValueError(
                        f"Step {step.id!r}: context_from references step {ref_step!r}"
                        f" which has not appeared before this step in execution order"
                    )

        if step.when:
            when_operators = {"equals", "not_equals", "is_not_empty", "is_empty", "contains"}
            when_fields = {"result_status", "result_summary", "result_artifacts", "result_findings"}
            when = step.when
            if not isinstance(when, dict):
                raise ValueError(f"Step {step.id!r}: 'when' must be a mapping")
            if "step" not in when:
                raise ValueError(f"Step {step.id!r}: 'when' requires a 'step' field")
            if "field" not in when:
                raise ValueError(f"Step {step.id!r}: 'when' requires a 'field' field")
            ref_step = when["step"]
            if ref_step not in seen_step_ids:
                raise ValueError(
                    f"Step {step.id!r}: when references step {ref_step!r}"
                    f" which has not appeared before this step in execution order"
                )
            top_field = when["field"].split(".")[0]
            if top_field not in when_fields:
                raise ValueError(f"Step {step.id!r}: when field {when['field']!r} must start with one of {when_fields}")
            ops_found = when_operators & set(when.keys())
            if len(ops_found) != 1:
                raise ValueError(
                    f"Step {step.id!r}: 'when' must have exactly one operator from {when_operators},"
                    f" found {ops_found or 'none'}"
                )

        if step.retry:
            if not isinstance(step.retry, dict):
                raise ValueError(f"Step {step.id!r}: 'retry' must be a mapping")
            if step.type in ("gate", "human_gate"):
                raise ValueError(f"Step {step.id!r}: 'retry' is not allowed on {step.type} steps")
            max_attempts = step.retry.get("max_attempts")
            if max_attempts is None or not isinstance(max_attempts, int) or max_attempts < 1:
                raise ValueError(f"Step {step.id!r}: retry.max_attempts must be an integer >= 1")
            backoff = step.retry.get("backoff", "exponential")
            if backoff not in ("exponential", "fixed"):
                raise ValueError(f"Step {step.id!r}: retry.backoff must be 'exponential' or 'fixed', got {backoff!r}")
            initial_delay = step.retry.get("initial_delay", 5)
            if not isinstance(initial_delay, (int, float)) or initial_delay <= 0:
                raise ValueError(f"Step {step.id!r}: retry.initial_delay must be a positive number")
            max_delay = step.retry.get("max_delay", 60)
            if not isinstance(max_delay, (int, float)) or max_delay < initial_delay:
                raise ValueError(f"Step {step.id!r}: retry.max_delay must be >= initial_delay ({initial_delay})")

        if step.type == "publish":
            if not step.destination:
                raise ValueError(f"Publish step {step.id!r} requires a 'destination' field")
            if not isinstance(step.destination, dict):
                raise ValueError(f"Publish step {step.id!r}: 'destination' must be a mapping")
            adapter = step.destination.get("adapter")
            if adapter not in ("file", "webhook"):
                raise ValueError(f"Publish step {step.id!r}: unknown adapter {adapter!r}, must be 'file' or 'webhook'")
            if adapter == "file" and not step.destination.get("path"):
                raise ValueError(f"Publish step {step.id!r}: file adapter requires a 'path' field")
            if adapter == "webhook" and not step.destination.get("url"):
                raise ValueError(f"Publish step {step.id!r}: webhook adapter requires a 'url' field")

        seen_step_ids.add(step.id)


def validate_approval_mode(
    definition: WorkflowDefinition,
    effective_approval_mode: str,
) -> None:
    """Validate that workflow approval_mode is not more permissive than effective config.

    Strictness order: ask > ask_for_writes > ask_for_dangerous > auto
    A workflow can be equally strict or stricter, never more permissive.
    """
    strictness = {"auto": 0, "ask_for_dangerous": 1, "ask_for_writes": 2, "ask": 3}
    effective_level = strictness.get(effective_approval_mode, 2)

    for step in _all_steps(definition.steps):
        if step.approval_mode:
            step_level = strictness.get(step.approval_mode, -1)
            if step_level < 0:
                raise ValueError(f"Step {step.id!r}: invalid approval_mode {step.approval_mode!r}")
            if step_level < effective_level:
                raise ValueError(
                    f"Step {step.id!r}: approval_mode {step.approval_mode!r} is more permissive than"
                    f" effective config {effective_approval_mode!r}"
                )

    policy_mode = definition.policies.get("approval_mode")
    if policy_mode:
        policy_level = strictness.get(policy_mode, -1)
        if policy_level < 0:
            raise ValueError(f"Workflow policy approval_mode {policy_mode!r} is invalid")
        if policy_level < effective_level:
            raise ValueError(
                f"Workflow policy approval_mode {policy_mode!r} is more permissive than"
                f" effective config {effective_approval_mode!r}"
            )


def _all_steps(steps: list[WorkflowStepDef]) -> list[WorkflowStepDef]:
    """Flatten all steps including nested loop steps."""
    result: list[WorkflowStepDef] = []
    for step in steps:
        result.append(step)
        if step.steps:
            result.extend(_all_steps(step.steps))
    return result


# ---------------------------------------------------------------------------
# Drift report (#964)
# ---------------------------------------------------------------------------


def _build_drift_report(run: dict[str, Any], definition: WorkflowDefinition) -> str:
    """Build a human-readable drift report comparing stored vs current definitions."""
    stored_content = run.get("definition_content")
    if not stored_content:
        return "No stored definition content available for comparison."

    try:
        old_raw = yaml.safe_load(stored_content)
        old_steps = [s.get("id", "?") for s in old_raw.get("steps", [])]
    except Exception:
        old_steps = ["(unable to parse stored definition)"]

    new_steps = [s.id for s in definition.steps]

    lines = ["Step changes:"]
    added = set(new_steps) - set(old_steps)
    removed = set(old_steps) - set(new_steps)
    if added:
        lines.append(f"  Added: {', '.join(sorted(added))}")
    if removed:
        lines.append(f"  Removed: {', '.join(sorted(removed))}")
    if old_steps != new_steps and not added and not removed:
        lines.append(f"  Reordered: {old_steps} -> {new_steps}")
    if not added and not removed and old_steps == new_steps:
        lines.append("  Step IDs unchanged — other definition content changed.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Engine (domain-neutral orchestrator)
# ---------------------------------------------------------------------------


class WorkflowEngine:
    """Executes workflow definitions. Domain-neutral.

    The engine knows about steps, runners, gates, and loops. It does not
    know about GitHub, issues, PRs, or any domain-specific concepts.
    """

    def __init__(
        self,
        db: ThreadSafeConnection,
        config: WorkflowConfig,
        runner_registry: RunnerRegistry,
        *,
        effective_approval_mode: str = "ask_for_writes",
        ai_service: Any | None = None,
        tool_executor: Any | None = None,
        tools_openai: list[dict[str, Any]] | None = None,
        event_bus: Any | None = None,
        egress_allowed_domains: list[str] | None = None,
        egress_block_localhost: bool = False,
        credential_resolver: Any | None = None,
        artifact_registry: Any | None = None,
        skill_registry: Any | None = None,
        model_costs: dict[str, dict[str, float]] | None = None,
        publisher_registry: Any | None = None,
    ) -> None:
        self._db = db
        self._config = config
        self._runner_registry = runner_registry
        self._config_approval_mode = effective_approval_mode
        self._ai_service = ai_service
        self._tool_executor = tool_executor
        self._tools_openai = tools_openai
        self._event_bus = event_bus
        self._egress_allowed_domains = egress_allowed_domains or []
        self._egress_block_localhost = egress_block_localhost
        self._credential_resolver = credential_resolver
        self._artifact_registry = artifact_registry
        self._skill_registry = skill_registry
        self._model_costs = model_costs
        self._publisher_registry = publisher_registry
        self._pending_hook_tasks: list[Any] = []
        self._preapproved_step_id: str | None = None
        self._progress_callback: Any | None = None  # Callable[[str, str, dict], None]

    def set_progress_callback(self, callback: Any) -> None:
        """Set a callback for real-time progress reporting.

        callback(event_type: str, step_id: str | None, payload: dict)
        Called synchronously after each event is emitted. Used by CLI
        to display live step progress during execution.
        """
        self._progress_callback = callback

    async def _emit_event(
        self,
        run_id: str,
        event_type: str,
        step_id: str | None = None,
        payload: dict[str, Any] | None = None,
        *,
        definition: WorkflowDefinition | None = None,
    ) -> None:
        """Persist a durable event AND publish it to the event bus + hooks.

        This replaces direct calls to ws.create_workflow_event() so that
        every durable event is also published for live monitoring.
        """
        from . import workflow_storage as ws

        ws.create_workflow_event(
            self._db,
            run_id=run_id,
            event_type=event_type,
            step_id=step_id,
            payload=payload,
        )
        await self._publish_event(run_id, event_type, payload, definition=definition)

        if self._progress_callback is not None:
            try:
                self._progress_callback(event_type, step_id, payload or {})
            except Exception:
                logger.warning("Progress callback error", exc_info=True)

    async def _publish_event(
        self,
        run_id: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        *,
        definition: WorkflowDefinition | None = None,
    ) -> None:
        """Publish event to event bus and fire notification hooks."""
        event_data = {
            "type": f"workflow_{event_type}",
            "data": {"run_id": run_id, "event_type": event_type, **(payload or {})},
        }

        if self._event_bus is not None:
            try:
                await self._event_bus.publish(f"workflow:{run_id}", event_data)
            except Exception:
                logger.warning("Failed to publish event to bus", exc_info=True)

        if definition and definition.notifications:
            hooks = definition.notifications.get("hooks", [])
            if hooks:
                from .workflow_hooks import deliver_hooks

                try:
                    tasks = await deliver_hooks(hooks, event_data["data"])
                    self._pending_hook_tasks.extend(tasks)
                except Exception:
                    logger.warning("Failed to deliver hooks", exc_info=True)

    async def _drain_hooks(self) -> None:
        """Drain pending hook tasks before process exit."""
        if self._pending_hook_tasks:
            from .workflow_hooks import drain_pending_hooks

            await drain_pending_hooks(self._pending_hook_tasks)
            self._pending_hook_tasks.clear()

    def _compute_effective_budget(
        self,
        definition: WorkflowDefinition,
    ) -> dict[str, int] | None:
        """Compute effective budget from definition policies and config ceilings.

        For each dimension, the effective limit is the minimum of non-zero values
        from the definition's policies.budget and the config's workflow.budget.
        Returns None if all dimensions are zero (unlimited).
        """
        policy_budget = definition.policies.get("budget", {})
        config_budget = self._config.budget if hasattr(self._config, "budget") else None

        dims = ("max_duration_seconds", "max_steps", "max_tokens")
        effective: dict[str, int] = {}

        for dim in dims:
            try:
                policy_val = int(policy_budget.get(dim, 0)) if policy_budget else 0
            except (ValueError, TypeError):
                policy_val = 0
            config_val = int(getattr(config_budget, dim, 0)) if config_budget else 0
            # Effective = minimum of non-zero values
            candidates = [v for v in (policy_val, config_val) if v > 0]
            effective[dim] = min(candidates) if candidates else 0

        if all(v == 0 for v in effective.values()):
            return None
        return effective

    @staticmethod
    def _check_budget(
        budget: dict[str, int],
        usage: dict[str, Any],
        budget_start_time: float | None,
        prior_elapsed: float,
    ) -> str | None:
        """Check if any budget dimension is exceeded. Returns violated dimension or None."""
        max_dur = budget.get("max_duration_seconds", 0)
        if max_dur > 0 and budget_start_time is not None:
            elapsed = prior_elapsed + (time.monotonic() - budget_start_time)
            if elapsed >= max_dur:
                return "duration"

        max_steps = budget.get("max_steps", 0)
        if max_steps > 0 and usage.get("steps_completed", 0) >= max_steps:
            return "steps"

        max_tokens = budget.get("max_tokens", 0)
        if max_tokens > 0 and usage.get("total_tokens", 0) >= max_tokens:
            return "tokens"

        return None

    def _estimate_step_cost(self, artifacts: dict[str, Any]) -> float:
        """Estimate cost for a step based on token counts and model rates."""
        if not self._model_costs:
            return 0.0
        model = artifacts.get("model", "")
        rates = self._model_costs.get(model, {})
        if not rates:
            return 0.0
        input_rate = rates.get("input", 0.0)
        output_rate = rates.get("output", 0.0)
        prompt_t = artifacts.get("prompt_tokens", 0)
        completion_t = artifacts.get("completion_tokens", 0)
        return (prompt_t / 1_000_000) * input_rate + (completion_t / 1_000_000) * output_rate

    @staticmethod
    def _evaluate_when(when: dict[str, Any], step_results: dict[str, dict[str, Any]]) -> bool:
        """Evaluate a when clause against prior step results.

        Returns True if the step should execute, False if it should be skipped.
        """
        ref_step = when["step"]
        step_data = step_results.get(ref_step)
        if step_data is None:
            return False

        value = _resolve_dotted_path(step_data, when["field"])

        if "equals" in when:
            return bool(value == when["equals"])
        if "not_equals" in when:
            return bool(value != when["not_equals"])
        if "is_not_empty" in when:
            return bool(value)
        if "is_empty" in when:
            return not bool(value)
        if "contains" in when:
            if value is None:
                return False
            return when["contains"] in value
        return False

    @staticmethod
    def _calculate_backoff(attempt: int, backoff: str, initial_delay: float, max_delay: float) -> float:
        """Calculate backoff delay for a retry attempt.

        attempt is 1-based (first failed attempt = 1).
        """
        if backoff == "fixed":
            return initial_delay
        # exponential: initial_delay * 2^(attempt-1), capped at max_delay
        delay = initial_delay * (2 ** (attempt - 1))
        return delay if delay < max_delay else max_delay

    def _validate_step_credentials(self, definition: WorkflowDefinition) -> None:
        """Validate that all credential references in steps are declared in config.

        Called in start_run() BEFORE run record creation or lock acquisition.
        """
        for step in _all_steps(definition.steps):
            if not step.credentials:
                continue
            for cred in step.credentials:
                from_name = cred.get("from", "")
                if not from_name:
                    raise ValueError(f"Step {step.id!r}: credential entry missing 'from' field")
                if not cred.get("name"):
                    raise ValueError(f"Step {step.id!r}: credential entry missing 'name' field")
                if self._credential_resolver is None:
                    raise ValueError(
                        f"Step {step.id!r}: references credential {from_name!r} but no credential "
                        f"resolver is configured. Add credentials to workflow config."
                    )
                if not self._credential_resolver.has(from_name):
                    raise ValueError(
                        f"Step {step.id!r}: references undeclared credential {from_name!r}. "
                        f"Declare it in workflow.credentials config."
                    )

    def _resolve_step_credentials(self, step_def: WorkflowStepDef) -> dict[str, str]:
        """Resolve credential bindings for a step at execution time.

        Returns a dict mapping env var names to resolved values.
        Checks allowed_runners policy. Raises on failure.
        """
        if not step_def.credentials or self._credential_resolver is None:
            return {}

        from .workflow_credentials import CredentialResolutionError

        resolved: dict[str, str] = {}
        for cred in step_def.credentials:
            env_name = cred.get("name", "")
            from_name = cred.get("from", "")
            if not env_name or not from_name:
                raise CredentialResolutionError(
                    f"Step {step_def.id!r}: credential entry missing 'name' or 'from' field"
                )

            config = self._credential_resolver.get_config(from_name)
            if config and config.allowed_runners is not None:
                if step_def.runner and step_def.runner not in config.allowed_runners:
                    raise CredentialResolutionError(
                        f"Credential {from_name!r} is not allowed for runner type {step_def.runner!r}"
                    )

            resolved[env_name] = self._credential_resolver.resolve(from_name)

        return resolved

    def _build_agent_system_context(self, step_def: WorkflowStepDef, definition: WorkflowDefinition) -> str:
        """Build extra system prompt context from artifacts and conventions (#957).

        Returns a string to prepend to the agent's system_prompt.
        """
        parts: list[str] = []
        # Determine effective inject_rules/inject_conventions
        policies = definition.policies or {}
        inject_rules = step_def.inject_rules
        if inject_rules is None:
            inject_rules = policies.get("inject_rules", False)
        inject_conventions = step_def.inject_conventions
        if inject_conventions is None:
            inject_conventions = policies.get("inject_conventions", False)

        # Inject rules/instructions from artifact registry
        if inject_rules and self._artifact_registry is not None:
            try:
                from ..services.context_trust import wrap_untrusted

                for art in self._artifact_registry.list_all():
                    art_type = getattr(art, "artifact_type", None)
                    if art_type and art_type.value in ("rule", "instruction"):
                        content = getattr(art, "content", "") or ""
                        if not content:
                            continue
                        source = getattr(art, "source", None)
                        if source and getattr(source, "value", str(source)) == "built_in":
                            parts.append(f'<artifact type="{art_type.value}">\n{content}\n</artifact>')
                        else:
                            origin = f"artifact:{getattr(source, 'value', 'unknown')}"
                            parts.append(wrap_untrusted(content, origin=origin, content_type="artifact"))
            except Exception:
                logger.warning("Failed to inject artifact rules", exc_info=True)

        # Inject global conventions (ANTEROOM.md from ~/.anteroom/ only — trusted)
        if inject_conventions:
            try:
                from pathlib import Path

                global_instructions_path = Path.home() / ".anteroom" / "ANTEROOM.md"
                if global_instructions_path.exists():
                    content = global_instructions_path.read_text(encoding="utf-8")[:50_000]
                    if content.strip():
                        parts.append(f'<conventions source="global">\n{content}\n</conventions>')
            except Exception:
                logger.warning("Failed to load global conventions", exc_info=True)

        return "\n\n".join(parts)

    async def start_run(
        self,
        definition: WorkflowDefinition,
        *,
        target_kind: str,
        target_ref: str,
        inputs: dict[str, Any] | None = None,
        space_id: str | None = None,
    ) -> dict[str, Any]:
        """Start a new workflow run. Returns the run dict."""
        from . import workflow_storage as ws

        # Validate approval mode bounded by effective config
        effective_mode = self._config_approval_mode or "ask_for_writes"
        validate_approval_mode(definition, effective_mode)

        # Validate notification hook URLs against egress allowlist at load time
        if definition.notifications:
            hooks = definition.notifications.get("hooks", [])
            if hooks:
                from .workflow_hooks import validate_hook_config

                validate_hook_config(
                    hooks,
                    self._egress_allowed_domains,
                    block_localhost=self._egress_block_localhost,
                )

        # Validate publish step webhook URLs against egress allowlist (#966)
        for step in _all_steps(definition.steps):
            if step.type == "publish" and step.destination and step.destination.get("adapter") == "webhook":
                url = step.destination.get("url", "")
                if url and "{" not in url:  # Skip template URLs — validated at execution time
                    from .egress_allowlist import check_egress_allowed

                    if not check_egress_allowed(
                        url, self._egress_allowed_domains, block_localhost=self._egress_block_localhost
                    ):
                        raise ValueError(f"Publish step {step.id!r}: webhook URL {url!r} blocked by egress allowlist")

        # Validate required inputs
        for name, schema in definition.inputs.items():
            if schema.get("required") and (not inputs or name not in inputs):
                raise ValueError(f"Missing required input: {name!r}")

        # Validate credential bindings BEFORE run creation/lock (#970)
        self._validate_step_credentials(definition)

        # Compute effective budget: minimum of non-zero values per dimension (#967)
        budget = self._compute_effective_budget(definition)

        # Create run record with definition snapshot (#964) and budget (#967)
        run = ws.create_workflow_run(
            self._db,
            workflow_id=definition.id,
            workflow_version=definition.version,
            target_kind=target_kind,
            target_ref=target_ref,
            inputs=inputs,
            space_id=space_id,
            definition_hash=definition.content_hash or None,
            definition_content=definition.raw_yaml.decode("utf-8", errors="replace") if definition.raw_yaml else None,
            budget=budget or None,
        )

        # Acquire concurrency lock
        if not ws.acquire_lock(
            self._db,
            target_kind=target_kind,
            target_ref=target_ref,
            run_id=run["id"],
        ):
            ws.update_workflow_run(self._db, run["id"], status="failed", stop_reason="target_locked")
            raise RuntimeError(f"Target {target_kind}:{target_ref} is already locked by another run")

        # Mark running
        run = ws.update_workflow_run(
            self._db,
            run["id"],
            status="running",
            started_at=datetime.now(timezone.utc).isoformat(),
        )

        await self._emit_event(
            run_id=run["id"],
            event_type="run_started",
            payload={"workflow_id": definition.id, "target": f"{target_kind}:{target_ref}"},
            definition=definition,
        )

        # Write initial heartbeat BEFORE background loop (closes null-heartbeat window)
        ws.update_workflow_run(self._db, run["id"], heartbeat_at=_now())
        heartbeat_task = asyncio.create_task(self._heartbeat_loop(run["id"]))

        try:
            run = await self._execute_steps(
                run,
                definition.steps,
                inputs or {},
                definition,
                budget_start_time=time.monotonic(),
            )
        except Exception:
            logger.exception("Workflow run %s failed with exception", run["id"])
            run = ws.update_workflow_run(self._db, run["id"], status="failed", stop_reason="unhandled_exception")
            await self._emit_event(
                run_id=run["id"],
                event_type="run_failed",
                payload={"reason": "exception"},
            )
        finally:
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass
            ws.release_lock(self._db, run_id=run["id"])
            await self._drain_hooks()

        return run

    @staticmethod
    async def _retry_delay(seconds: float) -> None:
        """Sleep between retry attempts. Extracted for testability."""
        await asyncio.sleep(seconds)

    async def _heartbeat_loop(self, run_id: str) -> None:
        """Periodically update heartbeat_at while a run is active."""
        from . import workflow_storage as ws

        try:
            while True:
                await asyncio.sleep(self._config.heartbeat_interval)
                ws.update_workflow_run(self._db, run_id, heartbeat_at=_now())
        except asyncio.CancelledError:
            pass

    async def recover_interrupted_runs(self) -> list[dict[str, Any]]:
        """Find stale running runs, mark as paused, repair step state, release locks.

        Called on-demand by list/resume CLI commands, not on generic startup.
        """
        from . import workflow_storage as ws

        stale = ws.find_stale_runs(self._db, self._config.stale_threshold)
        recovered: list[dict[str, Any]] = []
        for run in stale:
            running_steps = ws.find_running_steps(self._db, run["id"])
            for step in running_steps:
                ws.update_workflow_step(
                    self._db,
                    step["id"],
                    status="interrupted",
                    completed_at=datetime.now(timezone.utc).isoformat(),
                )

            ws.update_workflow_run(
                self._db,
                run["id"],
                status="paused",
                stop_reason="process_interrupted",
            )
            ws.release_lock(self._db, run_id=run["id"])
            await self._emit_event(
                run_id=run["id"],
                event_type="run_paused",
                payload={
                    "reason": "process_interrupted",
                    "interrupted_steps": [s["step_id"] for s in running_steps],
                },
            )
            recovered.append(run)
        return recovered

    async def resume_run(
        self,
        run_id: str,
        definition: WorkflowDefinition,
        *,
        from_step: str | None = None,
        force: bool = False,
    ) -> dict[str, Any]:
        """Resume a paused or waiting_for_approval run from the last completed step.

        The definition must be provided by the caller (built-in or custom path).
        Each step gets a fresh session (session isolation preserved on resume).

        If the definition has changed since the run started (content hash mismatch),
        resume is blocked unless force=True (#964).
        """
        from . import workflow_storage as ws

        run = ws.get_workflow_run(self._db, run_id)
        if not run:
            raise ValueError(f"Run not found: {run_id}")
        if run["status"] not in ("paused", "waiting_for_approval", "waiting_for_input"):
            raise ValueError(
                f"Run {run_id} is not resumable (status: {run['status']}). "
                f"Only paused, waiting_for_approval, or waiting_for_input runs can be resumed."
            )

        # Definition drift detection (#964)
        stored_hash = run.get("definition_hash")
        if stored_hash and definition.content_hash and stored_hash != definition.content_hash:
            if not force:
                # Build drift report
                drift_details = _build_drift_report(run, definition)
                raise ValueError(
                    f"Definition has changed since run started (hash mismatch).\n"
                    f"Stored: {stored_hash[:12]}...\n"
                    f"Current: {definition.content_hash[:12]}...\n"
                    f"{drift_details}\n"
                    f"Use --force to override and resume with the new definition."
                )
            logger.warning(
                "Definition drift detected for run %s but force=True, proceeding",
                run_id,
            )
            await self._emit_event(
                run_id=run_id,
                event_type="definition_drift_overridden",
                payload={
                    "stored_hash": stored_hash,
                    "current_hash": definition.content_hash,
                },
            )
        elif not stored_hash and definition.content_hash:
            logger.warning(
                "Run %s has no stored definition hash (pre-existing run), proceeding with warning",
                run_id,
            )

        # Validate credential bindings BEFORE lock acquisition (#970)
        self._validate_step_credentials(definition)

        # Re-acquire lock
        if not ws.acquire_lock(
            self._db,
            target_kind=run["target_kind"],
            target_ref=run["target_ref"],
            run_id=run_id,
        ):
            raise RuntimeError(f"Target {run['target_kind']}:{run['target_ref']} is still locked")

        # Rebuild completed step set (include skipped steps so they aren't re-evaluated)
        completed = ws.list_completed_step_ids(self._db, run_id)
        for s in ws.list_workflow_steps(self._db, run_id):
            if s["status"] == "skipped":
                completed.add(s["step_id"])
        if from_step:
            # Override: skip everything before from_step
            all_step_ids = [s.id for s in _all_steps(definition.steps)]
            if from_step not in all_step_ids:
                ws.release_lock(self._db, run_id=run_id)
                raise ValueError(f"Step {from_step!r} not found in workflow definition")
            idx = all_step_ids.index(from_step)
            completed = set(all_step_ids[:idx])

        # Rebuild step_results from persisted data
        step_results = self._rebuild_step_results(run_id)

        # Handle approval resolution for waiting_for_approval runs (#950)
        if run["status"] == "waiting_for_approval":
            current_step_id = run.get("current_step_id")
            if current_step_id:
                all_steps = ws.list_workflow_steps(self._db, run_id)
                approval_step = next((s for s in all_steps if s["step_id"] == current_step_id), None)
                if approval_step and approval_step.get("approval_request_id"):
                    req = ws.get_approval_request(self._db, approval_step["approval_request_id"])
                    if req and req["status"] == "pending":
                        raise ValueError(
                            f"Approval request for run {run_id} is still pending. "
                            f"Use 'aroom workflow approve {run_id}' first."
                        )
                    if req and req["status"] == "denied":
                        ws.release_lock(self._db, run_id=run_id)
                        return ws.update_workflow_run(
                            self._db,
                            run_id,
                            status="cancelled",
                            stop_reason="approval_denied",
                            completed_at=datetime.now(timezone.utc).isoformat(),
                        )
                    if req and req["status"] == "expired":
                        ws.release_lock(self._db, run_id=run_id)
                        return ws.update_workflow_run(
                            self._db,
                            run_id,
                            status="cancelled",
                            stop_reason="approval_expired",
                            completed_at=datetime.now(timezone.utc).isoformat(),
                        )
                    # approved: mark the step for one-shot auto-approval on re-run.
                    # V1 strategy: the pre-loaded callback approves the FIRST
                    # approval-needed call in the fresh session, then reverts
                    # to normal deny-and-pause for any subsequent calls.
                    self._preapproved_step_id = current_step_id

        # Handle human decision resolution for waiting_for_input runs
        if run["status"] == "waiting_for_input":
            pending = ws.get_pending_decision(self._db, run_id)
            if pending:
                raise ValueError(
                    f"Human decision for run {run_id} is still pending. "
                    f"Use 'aroom workflow respond {run_id}' to make a decision first."
                )
            # Decision was resolved — find the human_gate step and process outcome
            current_step_id = run.get("current_step_id")
            if current_step_id:
                # Find the step's decision_id
                all_steps = ws.list_workflow_steps(self._db, run_id)
                gate_step = next((s for s in all_steps if s["step_id"] == current_step_id), None)
                if gate_step and gate_step.get("decision_id"):
                    decision = ws.get_human_decision(self._db, gate_step["decision_id"])
                    if decision and decision["status"] == "expired":
                        # Apply on_timeout outcome
                        step_def = next(
                            (s for s in _all_steps(definition.steps) if s.id == current_step_id),
                            None,
                        )
                        on_timeout = step_def.on_timeout if step_def else None
                        if on_timeout and on_timeout.get("outcome") == "stop":
                            ws.release_lock(self._db, run_id=run_id)
                            return ws.update_workflow_run(
                                self._db,
                                run_id,
                                status="cancelled",
                                stop_reason=on_timeout.get("stop_reason", "human_timeout"),
                                completed_at=datetime.now(timezone.utc).isoformat(),
                            )
                        # Default: treat expired as stop
                        ws.release_lock(self._db, run_id=run_id)
                        return ws.update_workflow_run(
                            self._db,
                            run_id,
                            status="cancelled",
                            stop_reason="human_decision_expired",
                            completed_at=datetime.now(timezone.utc).isoformat(),
                        )
                    if decision and decision["status"] == "resolved":
                        selected = decision.get("selected_option")
                        # Find the option definition
                        step_def = next(
                            (s for s in _all_steps(definition.steps) if s.id == current_step_id),
                            None,
                        )
                        if step_def and step_def.options:
                            opt = next((o for o in step_def.options if o["id"] == selected), None)
                            if opt:
                                if opt["outcome"] == "stop":
                                    ws.release_lock(self._db, run_id=run_id)
                                    return ws.update_workflow_run(
                                        self._db,
                                        run_id,
                                        status="cancelled",
                                        stop_reason=opt.get("stop_reason", "operator_stopped"),
                                        completed_at=datetime.now(timezone.utc).isoformat(),
                                    )
                                elif opt["outcome"] == "branch":
                                    # Skip to the branch target
                                    target = opt["next_step"]
                                    all_ids = [s.id for s in definition.steps]
                                    target_idx = all_ids.index(target)
                                    completed = set(all_ids[:target_idx])
                                # "continue" = just add the gate step to completed and proceed
                                completed.add(current_step_id)

        # Mark running, write initial heartbeat
        run = ws.update_workflow_run(self._db, run_id, status="running", stop_reason=None)
        ws.update_workflow_run(self._db, run_id, heartbeat_at=_now())
        heartbeat_task = asyncio.create_task(self._heartbeat_loop(run_id))

        await self._emit_event(
            run_id=run_id,
            event_type="run_resumed",
            payload={"skip_completed": list(completed)},
        )

        try:
            inputs = run.get("inputs") or {}
            # Reload budget usage from run record for resume (#967)
            budget_usage = run.get("budget_usage")
            run = await self._execute_steps(
                run,
                definition.steps,
                inputs,
                definition,
                skip_completed=completed,
                step_results=step_results,
                budget_start_time=time.monotonic(),
                initial_budget_usage=budget_usage,
            )
        except Exception:
            logger.exception("Resumed workflow run %s failed with exception", run_id)
            run = ws.update_workflow_run(
                self._db,
                run_id,
                status="failed",
                stop_reason="unhandled_exception",
            )
        finally:
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass
            ws.release_lock(self._db, run_id=run_id)
            await self._drain_hooks()

        return run

    def _rebuild_step_results(self, run_id: str) -> dict[str, dict[str, Any]]:
        """Rebuild step_results dict from persisted step records."""
        from . import workflow_storage as ws

        steps = ws.list_workflow_steps(self._db, run_id)
        results: dict[str, dict[str, Any]] = {}
        for step in steps:
            if step["status"] == "completed" and step.get("result_status"):
                results[step["step_id"]] = {
                    "result_status": step["result_status"],
                    "result_summary": step.get("result_summary"),
                    "result_artifacts": step.get("result_artifacts"),
                    "result_findings": step.get("result_findings"),
                }
        return results

    async def _execute_human_gate_step(
        self,
        step_def: WorkflowStepDef,
        run: dict[str, Any],
        inputs: dict[str, Any],
        step_results: dict[str, dict[str, Any]],
        step_record: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a human_gate step — persist decision request, pause the run.

        This has its own execution path — it does NOT return a RunnerResult
        through the generic handler. It directly transitions the run to
        waiting_for_input and returns.
        """
        from . import workflow_storage as ws

        # Resolve context from prior steps
        context = ""
        if step_def.context_from:
            context = resolve_context_from(step_def.context_from, step_results)

        # Render prompt with template variables
        prompt = step_def.prompt or ""
        if "{" in prompt:
            prompt = resolve_template(prompt, inputs)

        # Create human decision record
        decision = ws.create_human_decision(
            self._db,
            run_id=run["id"],
            step_id=step_def.id,
            prompt=prompt,
            context=context if context else None,
            options=step_def.options or [],
            timeout_at=None,  # V1: on-demand timeout only
        )

        # Store decision_id on the step record
        ws.update_workflow_step(
            self._db,
            step_record["id"],
            status="completed",
            result_status="blocked",
            result_summary=f"Waiting for human decision: {prompt[:80]}",
            decision_id=decision["id"],
            completed_at=datetime.now(timezone.utc).isoformat(),
        )

        # Transition run to waiting_for_input
        run = ws.update_workflow_run(
            self._db,
            run["id"],
            status="waiting_for_input",
            current_step_id=step_def.id,
        )
        await self._emit_event(
            run_id=run["id"],
            event_type="waiting_for_input",
            step_id=step_def.id,
            payload={
                "decision_id": decision["id"],
                "prompt": prompt[:200],
                "options": [{"id": o["id"], "label": o["label"]} for o in (step_def.options or [])],
            },
        )
        return run

    async def _execute_steps(
        self,
        run: dict[str, Any],
        steps: list[WorkflowStepDef],
        inputs: dict[str, Any],
        definition: WorkflowDefinition,
        *,
        skip_completed: set[str] | None = None,
        step_results: dict[str, dict[str, Any]] | None = None,
        budget_start_time: float | None = None,
        initial_budget_usage: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        from . import workflow_storage as ws

        if step_results is None:
            step_results = {}

        # Budget tracking state (#967)
        budget = run.get("budget")
        budget_usage: dict[str, Any] = initial_budget_usage or {
            "elapsed_seconds": 0,
            "steps_completed": 0,
            "total_tokens": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
        }
        # For elapsed_seconds on resume, we need the prior elapsed time
        prior_elapsed = budget_usage.get("elapsed_seconds", 0)

        for step_def in steps:
            if skip_completed and step_def.id in skip_completed:
                logger.info("Skipping completed step %r on resume", step_def.id)
                continue

            # Conditional execution: evaluate when clause (#959)
            if step_def.when is not None:
                if not self._evaluate_when(step_def.when, step_results):
                    step_record = ws.create_workflow_step(
                        self._db,
                        run_id=run["id"],
                        step_id=step_def.id,
                        step_type=step_def.type,
                        runner_type=step_def.runner,
                    )
                    ws.update_workflow_step(
                        self._db,
                        step_record["id"],
                        status="skipped",
                        result_summary="Condition not met",
                        completed_at=datetime.now(timezone.utc).isoformat(),
                    )
                    await self._emit_event(
                        run_id=run["id"],
                        event_type="step_skipped",
                        step_id=step_def.id,
                        payload={
                            "reason": "condition_not_met",
                            "when": step_def.when,
                        },
                    )
                    logger.info("Skipping step %r: when condition not met", step_def.id)
                    continue

            # Retry configuration (#962)
            max_attempts = 1
            retry_cfg = step_def.retry
            if retry_cfg and step_def.type in ("runner", "loop"):
                max_attempts = retry_cfg.get("max_attempts", 1)

            for attempt in range(1, max_attempts + 1):
                # Budget check before each attempt (#967, #962)
                if budget:
                    violation = self._check_budget(budget, budget_usage, budget_start_time, prior_elapsed)
                    if violation:
                        if budget_start_time is not None:
                            budget_usage["elapsed_seconds"] = int(
                                prior_elapsed + (time.monotonic() - budget_start_time)
                            )
                        run = ws.update_workflow_run(
                            self._db,
                            run["id"],
                            status="failed",
                            stop_reason=f"budget_exceeded:{violation}",
                            completed_at=datetime.now(timezone.utc).isoformat(),
                            budget_usage_json=budget_usage,
                        )
                        await self._emit_event(
                            run_id=run["id"],
                            event_type="run_failed",
                            payload={
                                "reason": f"budget_exceeded:{violation}",
                                "budget": budget,
                                "budget_usage": budget_usage,
                            },
                        )
                        return run

                step_record = ws.create_workflow_step(
                    self._db,
                    run_id=run["id"],
                    step_id=step_def.id,
                    step_type=step_def.type,
                    runner_type=step_def.runner,
                    attempt=attempt,
                )

                if attempt == 1:
                    ws.update_workflow_run(self._db, run["id"], current_step_id=step_def.id)
                step_started_payload: dict[str, Any] = {"step_type": step_def.type}
                if attempt > 1:
                    step_started_payload["attempt"] = attempt
                await self._emit_event(
                    run_id=run["id"],
                    event_type="step_started",
                    step_id=step_def.id,
                    payload=step_started_payload,
                )

                start_time = time.monotonic()
                ws.update_workflow_step(
                    self._db,
                    step_record["id"],
                    status="running",
                    started_at=datetime.now(timezone.utc).isoformat(),
                )

                try:
                    if step_def.type == "runner":
                        result = await self._execute_runner_step(
                            step_def, run, inputs, step_results, definition, step_record=step_record
                        )
                    elif step_def.type == "gate":
                        result = await self._execute_gate_step(step_def, run, inputs)
                    elif step_def.type == "loop":
                        result = await self._execute_loop_step(step_def, run, inputs, definition, step_results)
                    elif step_def.type == "publish":
                        result = await self._execute_publish_step(step_def, run, inputs, step_results)
                    elif step_def.type == "human_gate":
                        return await self._execute_human_gate_step(
                            step_def,
                            run,
                            inputs,
                            step_results,
                            step_record,
                        )
                    else:
                        raise ValueError(f"Unknown step type: {step_def.type!r}")
                except Exception as exc:
                    duration_ms = int((time.monotonic() - start_time) * 1000)
                    ws.update_workflow_step(
                        self._db,
                        step_record["id"],
                        status="failed",
                        result_status="failed",
                        result_summary=str(exc),
                        duration_ms=duration_ms,
                        completed_at=datetime.now(timezone.utc).isoformat(),
                    )
                    if attempt < max_attempts:
                        delay = self._calculate_backoff(
                            attempt,
                            retry_cfg.get("backoff", "exponential"),  # type: ignore[union-attr]
                            retry_cfg.get("initial_delay", 5),  # type: ignore[union-attr]
                            retry_cfg.get("max_delay", 60),  # type: ignore[union-attr]
                        )
                        await self._emit_event(
                            run_id=run["id"],
                            event_type="step_retry",
                            step_id=step_def.id,
                            payload={
                                "attempt": attempt,
                                "max_attempts": max_attempts,
                                "backoff_seconds": delay,
                                "error": str(exc),
                            },
                        )
                        await self._retry_delay(delay)
                        continue
                    # Final attempt failed — propagate
                    await self._emit_event(
                        run_id=run["id"],
                        event_type="step_failed",
                        step_id=step_def.id,
                        payload={"error": str(exc)},
                    )
                    run = ws.update_workflow_run(
                        self._db,
                        run["id"],
                        status="failed",
                        stop_reason=f"step_failed:{step_def.id}",
                        completed_at=datetime.now(timezone.utc).isoformat(),
                    )
                    await self._emit_event(
                        run_id=run["id"],
                        event_type="run_failed",
                        payload={"reason": f"step_failed:{step_def.id}"},
                    )
                    return run

                duration_ms = int((time.monotonic() - start_time) * 1000)

                if result.status == "blocked":
                    # Distinguish approval pause from generic gate block
                    is_approval_pause = result.summary == "Paused for approval"
                    run_status = "waiting_for_approval" if is_approval_pause else "blocked"

                    ws.update_workflow_step(
                        self._db,
                        step_record["id"],
                        status="completed",
                        result_status="blocked",
                        result_summary=result.summary,
                        result_artifacts=result.artifacts,
                        duration_ms=duration_ms,
                        completed_at=datetime.now(timezone.utc).isoformat(),
                    )
                    await self._emit_event(
                        run_id=run["id"],
                        event_type="waiting_for_approval" if is_approval_pause else "step_finished",
                        step_id=step_def.id,
                        payload={"result_status": "blocked"},
                    )
                    run = ws.update_workflow_run(
                        self._db,
                        run["id"],
                        status=run_status,
                        stop_reason=result.summary or f"blocked_at:{step_def.id}",
                        current_step_id=step_def.id,
                    )
                    if not is_approval_pause:
                        run = ws.update_workflow_run(
                            self._db,
                            run["id"],
                            completed_at=datetime.now(timezone.utc).isoformat(),
                        )
                    return run

                if result.status == "failed":
                    ws.update_workflow_step(
                        self._db,
                        step_record["id"],
                        status="failed",
                        result_status="failed",
                        result_summary=result.summary,
                        result_artifacts=result.artifacts,
                        result_findings=result.findings,
                        duration_ms=duration_ms,
                        completed_at=datetime.now(timezone.utc).isoformat(),
                    )
                    if attempt < max_attempts:
                        delay = self._calculate_backoff(
                            attempt,
                            retry_cfg.get("backoff", "exponential"),  # type: ignore[union-attr]
                            retry_cfg.get("initial_delay", 5),  # type: ignore[union-attr]
                            retry_cfg.get("max_delay", 60),  # type: ignore[union-attr]
                        )
                        await self._emit_event(
                            run_id=run["id"],
                            event_type="step_retry",
                            step_id=step_def.id,
                            payload={
                                "attempt": attempt,
                                "max_attempts": max_attempts,
                                "backoff_seconds": delay,
                                "error": result.summary,
                            },
                        )
                        await self._retry_delay(delay)
                        continue
                    # Final attempt — fall through to failure handling
                    await self._emit_event(
                        run_id=run["id"],
                        event_type="step_failed",
                        step_id=step_def.id,
                        payload={"result_status": "failed", "summary": result.summary},
                    )
                    run = ws.update_workflow_run(
                        self._db,
                        run["id"],
                        status="failed",
                        stop_reason=f"step_failed:{step_def.id}",
                        completed_at=datetime.now(timezone.utc).isoformat(),
                    )
                    await self._emit_event(
                        run_id=run["id"],
                        event_type="run_failed",
                        payload={"reason": f"step_failed:{step_def.id}"},
                    )
                    return run

                # Success — break out of retry loop
                break

            ws.update_workflow_step(
                self._db,
                step_record["id"],
                status="completed",
                result_status=result.status,
                result_summary=result.summary,
                result_artifacts=result.artifacts,
                result_findings=result.findings,
                raw_output_path=result.raw_output_path,
                duration_ms=duration_ms,
                completed_at=datetime.now(timezone.utc).isoformat(),
            )
            await self._emit_event(
                run_id=run["id"],
                event_type="step_finished",
                step_id=step_def.id,
                payload={"result_status": result.status, "duration_ms": duration_ms},
            )

            step_results[step_def.id] = {
                "result_status": result.status,
                "result_summary": result.summary,
                "result_artifacts": result.artifacts,
                "result_findings": result.findings,
            }

            # Update usage after step completion — always-on (#963, #967)
            budget_usage["steps_completed"] = budget_usage.get("steps_completed", 0) + 1
            step_tokens = result.artifacts.get("total_tokens", 0)
            budget_usage["total_tokens"] = budget_usage.get("total_tokens", 0) + step_tokens
            budget_usage["prompt_tokens"] = budget_usage.get("prompt_tokens", 0) + result.artifacts.get(
                "prompt_tokens", 0
            )
            budget_usage["completion_tokens"] = budget_usage.get("completion_tokens", 0) + result.artifacts.get(
                "completion_tokens", 0
            )
            step_cost = self._estimate_step_cost(result.artifacts)
            budget_usage["estimated_cost_usd"] = budget_usage.get("estimated_cost_usd", 0.0) + step_cost
            if budget_start_time is not None:
                budget_usage["elapsed_seconds"] = int(prior_elapsed + (time.monotonic() - budget_start_time))
            ws.update_workflow_run(
                self._db,
                run["id"],
                budget_usage_json=budget_usage,
            )

            run = ws.update_workflow_run(
                self._db,
                run["id"],
                attempt_count=run.get("attempt_count", 0) + 1,
            )

        # All steps completed
        run = ws.update_workflow_run(
            self._db,
            run["id"],
            status="completed",
            completed_at=datetime.now(timezone.utc).isoformat(),
        )
        await self._emit_event(
            run_id=run["id"],
            event_type="run_completed",
            payload={"total_steps": len(steps)},
        )
        return run

    def _expand_skill_prompt(self, step_def: WorkflowStepDef) -> str:
        """Resolve a skill by name and expand its prompt template (#957)."""
        if self._skill_registry is None:
            raise ValueError(
                f"Step {step_def.id!r}: skill_name requires a SkillRegistry. "
                "Configure the WorkflowEngine with a skill_registry."
            )
        skill_name = step_def.skill_name or ""
        skill = self._skill_registry.get(skill_name)
        if skill is None:
            raise ValueError(f"Step {step_def.id!r}: skill {skill_name!r} not found in registry")
        prompt = getattr(skill, "prompt", "") or ""
        if not prompt:
            raise ValueError(f"Step {step_def.id!r}: skill {skill_name!r} has no prompt")
        # Expand {args} placeholder with skill_args
        if step_def.skill_args and "{args}" in prompt:
            prompt = prompt.replace("{args}", step_def.skill_args)
        elif "{args}" in prompt:
            prompt = prompt.replace("{args}", "")
        return prompt

    async def _execute_runner_step(
        self,
        step_def: WorkflowStepDef,
        run: dict[str, Any],
        inputs: dict[str, Any],
        step_results: dict[str, dict[str, Any]],
        definition: WorkflowDefinition,
        step_record: dict[str, Any] | None = None,
    ) -> RunnerResult:
        from .workflow_runners import execute_agent_runner, execute_opaque_runner

        if not step_def.runner:
            raise ValueError(f"Runner step {step_def.id!r} has no runner type")
        if not self._runner_registry.is_registered(step_def.runner):
            raise ValueError(f"Unknown runner type: {step_def.runner!r}")

        timeout = step_def.timeout or self._config.step_timeout

        # Resolve credentials at execution time (#970)
        resolved_creds = self._resolve_step_credentials(step_def)

        # Resolve context from prior steps + source refs (#957)
        context = ""
        if step_def.context_from:
            context = resolve_context_from(step_def.context_from, step_results, db=self._db)

        if self._runner_registry.is_agent_runner(step_def.runner):
            # Skill prompt expansion (#957)
            if step_def.skill_name:
                prompt = self._expand_skill_prompt(step_def)
            else:
                prompt = step_def.prompt or ""
            if "{" in prompt:
                prompt = resolve_template(prompt, inputs)
            if context:
                prompt = f"{prompt}\n\n--- Prior step context ---\n{context}"

            # Build augmented system prompt from artifacts/conventions (#957)
            system_prompt = step_def.system_prompt or ""
            extra_context = self._build_agent_system_context(step_def, definition)
            if extra_context:
                system_prompt = f"{extra_context}\n\n{system_prompt}" if system_prompt else extra_context

            # Build per-step tool executor with credential env injection (#970)
            step_tool_executor = self._tool_executor
            if resolved_creds and self._tool_executor is not None:
                base_executor = self._tool_executor
                creds_snapshot = dict(resolved_creds)  # capture by value, not reference

                async def _cred_executor(name: str, args: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
                    kwargs.pop("_extra_env", None)  # prevent duplicate kwarg conflict
                    return await base_executor(name, args, _extra_env=creds_snapshot, **kwargs)

                step_tool_executor = _cred_executor

            # Create pause signal for approval gates (#950)
            pause_signal = asyncio.Event()

            from . import workflow_storage as ws

            _approval_fired = False
            _preapproved = getattr(self, "_preapproved_step_id", None) == step_def.id

            async def _workflow_confirm(verdict: Any) -> bool:
                nonlocal _approval_fired, _preapproved
                if not verdict.needs_approval:
                    return True
                if _preapproved:
                    _preapproved = False
                    self._preapproved_step_id = None
                    return True
                if _approval_fired:
                    pause_signal.set()
                    return False
                _approval_fired = True
                req = ws.create_approval_request(
                    self._db,
                    run_id=run["id"],
                    step_id=step_def.id,
                    tool_name=verdict.tool_name,
                    tool_args=getattr(verdict, "details", {}) or {},
                    risk_tier=str(getattr(verdict, "tier", "EXECUTE")),
                )
                if step_record:
                    ws.update_workflow_step(
                        self._db,
                        step_record["id"],
                        approval_request_id=req["id"],
                    )
                pause_signal.set()
                return False

            return await execute_agent_runner(
                prompt=prompt,
                system_prompt=system_prompt or None,
                tools_filter=step_def.tools,
                timeout=timeout,
                ai_service=self._ai_service,
                tool_executor=step_tool_executor,
                tools_openai=self._tools_openai,
                pause_signal=pause_signal,
                confirm_callback=_workflow_confirm,
                model=getattr(self._ai_service, "model", None),
            )
        else:
            # Merge credential env into step env for opaque runners (#970)
            step_env = dict(step_def.env or {})
            if resolved_creds:
                step_env.update(resolved_creds)

            if step_def.runner == "shell":
                if not step_def.command:
                    raise ValueError(f"Shell runner step {step_def.id!r} has no command")
                command = resolve_template(step_def.command, inputs, shell_quote=True)
                return await execute_opaque_runner(
                    mode="shell",
                    command=command,
                    env=step_env or None,
                    working_dir=step_def.working_dir,
                    timeout=timeout,
                )
            elif step_def.runner == "python_script":
                if not step_def.command:
                    raise ValueError(f"Python script runner step {step_def.id!r} has no command")
                argv = [resolve_template(a, inputs) for a in (step_def.argv or [])]
                return await execute_opaque_runner(
                    mode="exec",
                    command=step_def.command,
                    argv=argv,
                    env=step_env or None,
                    working_dir=step_def.working_dir,
                    timeout=timeout,
                )
            else:
                raise ValueError(f"Unknown opaque runner: {step_def.runner!r}")

    async def _execute_publish_step(
        self,
        step_def: WorkflowStepDef,
        run: dict[str, Any],
        inputs: dict[str, Any],
        step_results: dict[str, dict[str, Any]],
    ) -> RunnerResult:
        """Execute a publish step — deliver content to a destination adapter."""
        from .workflow_publishers import create_default_publisher_registry
        from .workflow_runners import RunnerResult

        registry = self._publisher_registry or create_default_publisher_registry()

        if not step_def.destination:
            return RunnerResult(status="failed", summary="No destination configured", duration_ms=0)

        adapter_name = step_def.destination.get("adapter", "")
        adapter = registry.get(adapter_name)
        if adapter is None:
            return RunnerResult(status="failed", summary=f"Unknown adapter: {adapter_name!r}", duration_ms=0)

        content = ""
        if step_def.context_from:
            content = resolve_context_from(step_def.context_from, step_results, db=self._db)

        resolved_dest = dict(step_def.destination)
        for key, val in resolved_dest.items():
            if isinstance(val, str) and "{" in val:
                resolved_dest[key] = resolve_template(val, inputs)

        # Post-template egress validation for webhook URLs (#966 security)
        if adapter_name == "webhook":
            resolved_url = resolved_dest.get("url", "")
            if resolved_url:
                from .egress_allowlist import check_egress_allowed

                if not check_egress_allowed(
                    resolved_url,
                    self._egress_allowed_domains,
                    block_localhost=self._egress_block_localhost,
                ):
                    return RunnerResult(
                        status="failed",
                        summary=f"Webhook URL {resolved_url!r} blocked by egress allowlist",
                        duration_ms=0,
                    )

        resolved_creds = self._resolve_step_credentials(step_def)

        return await adapter.publish(
            content=content,
            destination=resolved_dest,
            credentials=resolved_creds,
        )

    async def _execute_gate_step(
        self,
        step_def: WorkflowStepDef,
        run: dict[str, Any],
        inputs: dict[str, Any],
    ) -> RunnerResult:
        from .workflow_runners import RunnerResult

        if not step_def.condition:
            raise ValueError(f"Gate step {step_def.id!r} has no condition")

        condition_fn = get_gate_condition(step_def.condition)
        if condition_fn is None:
            raise ValueError(f"Unknown gate condition: {step_def.condition!r}")

        passed = await condition_fn(run, step_def, inputs)

        if passed:
            return RunnerResult(status="success", summary=f"Gate {step_def.condition!r} passed")
        else:
            return RunnerResult(
                status="blocked",
                summary=step_def.if_false or f"Gate {step_def.condition!r} failed",
            )

    async def _execute_loop_step(
        self,
        step_def: WorkflowStepDef,
        run: dict[str, Any],
        inputs: dict[str, Any],
        definition: WorkflowDefinition,
        step_results: dict[str, dict[str, Any]],
    ) -> RunnerResult:
        from . import workflow_storage as ws
        from .workflow_runners import RunnerResult

        if not step_def.steps:
            return RunnerResult(status="success", summary="Empty loop")

        max_rounds = step_def.max_rounds or self._config.max_review_rounds
        rounds_completed = 0

        for round_num in range(1, max_rounds + 1):
            all_succeeded = True
            for nested_step in step_def.steps:
                # Persist nested step record (same durability as top-level steps)
                nested_step_id = f"{nested_step.id}_r{round_num}"
                nested_record = ws.create_workflow_step(
                    self._db,
                    run_id=run["id"],
                    step_id=nested_step_id,
                    step_type=nested_step.type,
                    runner_type=nested_step.runner,
                )
                await self._emit_event(
                    run_id=run["id"],
                    event_type="step_started",
                    step_id=nested_step_id,
                    payload={"step_type": nested_step.type, "loop": step_def.id, "round": round_num},
                )
                ws.update_workflow_step(
                    self._db,
                    nested_record["id"],
                    status="running",
                    started_at=datetime.now(timezone.utc).isoformat(),
                )
                nested_start = time.monotonic()

                try:
                    if nested_step.type == "runner":
                        result = await self._execute_runner_step(
                            nested_step, run, inputs, step_results, definition, step_record=nested_record
                        )
                    elif nested_step.type == "gate":
                        result = await self._execute_gate_step(nested_step, run, inputs)
                    else:
                        raise ValueError(
                            f"Unsupported step type in loop: {nested_step.type!r}"
                            " (only 'runner' and 'gate' are allowed inside loops)"
                        )
                except Exception as exc:
                    nested_dur = int((time.monotonic() - nested_start) * 1000)
                    ws.update_workflow_step(
                        self._db,
                        nested_record["id"],
                        status="failed",
                        result_status="failed",
                        result_summary=str(exc),
                        duration_ms=nested_dur,
                        completed_at=datetime.now(timezone.utc).isoformat(),
                    )
                    await self._emit_event(
                        run_id=run["id"],
                        event_type="step_failed",
                        step_id=nested_step_id,
                        payload={"error": str(exc)},
                    )
                    return RunnerResult(status="failed", summary=f"Loop step {nested_step.id} failed: {exc}")

                # Persist nested step result
                nested_dur = int((time.monotonic() - nested_start) * 1000)
                ws.update_workflow_step(
                    self._db,
                    nested_record["id"],
                    status="completed",
                    result_status=result.status,
                    result_summary=result.summary,
                    result_artifacts=result.artifacts,
                    result_findings=result.findings,
                    duration_ms=nested_dur,
                    completed_at=datetime.now(timezone.utc).isoformat(),
                )
                await self._emit_event(
                    run_id=run["id"],
                    event_type="step_finished",
                    step_id=nested_step_id,
                    payload={"result_status": result.status, "duration_ms": nested_dur},
                )

                step_results[nested_step.id] = {
                    "result_status": result.status,
                    "result_summary": result.summary,
                    "result_artifacts": result.artifacts,
                    "result_findings": result.findings,
                }

                if result.status != "success":
                    all_succeeded = False

            rounds_completed = round_num
            if all_succeeded:
                break

        return RunnerResult(
            status="success",
            summary=f"Loop completed after {rounds_completed}/{max_rounds} rounds",
        )
