"""Durable run helpers for resumable long-horizon execution."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Iterable
from uuid import uuid4

from packages.contracts.runtime import AgentRunState, AgentRunStep, ExecutionResult


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _compact(value: str, *, limit: int = 320) -> str:
    normalized = " ".join(value.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def _format_arguments(arguments: Mapping[str, object]) -> str:
    if not arguments:
        return "<none>"
    return ", ".join(f"{key}={value}" for key, value in sorted(arguments.items()))


def _checkpoint_content_preview(step: AgentRunStep) -> str:
    if step.kind == "tool":
        return "tool-result-pruned: " + _compact(step.content, limit=160)
    if step.kind == "context_prompt":
        return "provider-system-prompt-pruned: " + _compact(step.content, limit=180)
    return _compact(step.content, limit=220)


@dataclass(frozen=True, slots=True)
class AgentLoopBudget:
    max_model_turns: int = 100
    max_wall_time_seconds: int = 8 * 60 * 60
    tool_result_preview_chars: int = 1_500
    tool_result_turn_budget_chars: int = 200_000
    tool_result_persist_threshold_chars: int = 100_000


@dataclass(frozen=True, slots=True)
class AgentRunService:
    budget: AgentLoopBudget = AgentLoopBudget()

    def start_run(
        self,
        *,
        session_id: str,
        source_event_id: str,
        prompt: str,
        now: datetime | None = None,
    ) -> AgentRunState:
        current = now or _utc_now()
        return AgentRunState(
            run_id=f"run:{session_id}:{uuid4().hex[:10]}",
            session_id=session_id,
            source_event_id=source_event_id,
            prompt=prompt.strip(),
            status="active",
            phase="model",
            step_count=0,
            model_turn_count=0,
            tool_call_count=0,
            max_model_turns=self.budget.max_model_turns,
            max_wall_time_seconds=self.budget.max_wall_time_seconds,
            created_at=current,
            updated_at=current,
        )

    def resume_run(
        self,
        run: AgentRunState,
        *,
        now: datetime | None = None,
    ) -> AgentRunState:
        return replace(
            run,
            status="active",
            phase="resume",
            updated_at=now or _utc_now(),
            waiting_reason=None,
        )

    def complete(
        self,
        run: AgentRunState,
        *,
        summary: str,
        now: datetime | None = None,
    ) -> AgentRunState:
        return replace(
            run,
            status="completed",
            phase="done",
            updated_at=now or _utc_now(),
            waiting_reason=None,
            continuation_prompt=None,
            last_summary=_compact(summary, limit=800),
        )

    def fail(
        self,
        run: AgentRunState,
        *,
        summary: str,
        reason: str = "failed",
        now: datetime | None = None,
    ) -> AgentRunState:
        return replace(
            run,
            status="failed",
            phase="done",
            updated_at=now or _utc_now(),
            waiting_reason=reason,
            continuation_prompt=None,
            last_summary=_compact(summary, limit=800),
        )

    def park(
        self,
        run: AgentRunState,
        *,
        continuation_prompt: str,
        waiting_reason: str,
        last_summary: str,
        now: datetime | None = None,
    ) -> AgentRunState:
        return replace(
            run,
            status="pending",
            phase="waiting",
            updated_at=now or _utc_now(),
            waiting_reason=waiting_reason,
            continuation_prompt=continuation_prompt,
            last_summary=_compact(last_summary, limit=800),
        )

    def record_model_turn(
        self,
        run: AgentRunState,
        *,
        summary: str,
        response_text: str | None = None,
        now: datetime | None = None,
    ) -> tuple[AgentRunState, AgentRunStep]:
        current = now or _utc_now()
        updated = replace(
            run,
            phase="model",
            step_count=run.step_count + 1,
            model_turn_count=run.model_turn_count + 1,
            updated_at=current,
            last_summary=_compact(summary, limit=800),
        )
        step = AgentRunStep(
            step_id=f"run-step:{uuid4().hex[:10]}",
            run_id=run.run_id,
            session_id=run.session_id,
            step_index=updated.step_count,
            kind="model",
            title=f"model turn {updated.model_turn_count}",
            content=_compact(response_text or summary, limit=6_000),
            created_at=current,
            outcome="ok",
        )
        return updated, step

    def record_context_prompt(
        self,
        run: AgentRunState,
        *,
        system_prompt: str | None = None,
        rendered_prompt: str | None = None,
        now: datetime | None = None,
    ) -> tuple[AgentRunState, AgentRunStep]:
        current = now or _utc_now()
        prompt_text = system_prompt if system_prompt is not None else (rendered_prompt or "")
        updated = replace(
            run,
            phase="context",
            step_count=run.step_count + 1,
            updated_at=current,
        )
        step = AgentRunStep(
            step_id=f"run-step:{uuid4().hex[:10]}",
            run_id=run.run_id,
            session_id=run.session_id,
            step_index=updated.step_count,
            kind="context_prompt",
            title="provider system prompt",
            content=prompt_text,
            created_at=current,
            outcome="ok",
        )
        return updated, step

    def record_tool_step(
        self,
        run: AgentRunState,
        *,
        tool_name: str,
        arguments: Mapping[str, object],
        result: ExecutionResult,
        now: datetime | None = None,
    ) -> tuple[AgentRunState, AgentRunStep]:
        current = now or _utc_now()
        updated = replace(
            run,
            phase="tool",
            step_count=run.step_count + 1,
            tool_call_count=run.tool_call_count + 1,
            updated_at=current,
            last_summary=_compact(result.summary, limit=800),
        )
        content = "\n".join(
            (
                f"arguments: {_format_arguments(arguments)}",
                f"outcome: {result.outcome}",
                f"summary: {_compact(result.summary, limit=900)}",
            )
        )
        step = AgentRunStep(
            step_id=f"run-step:{uuid4().hex[:10]}",
            run_id=run.run_id,
            session_id=run.session_id,
            step_index=updated.step_count,
            kind="tool",
            title=tool_name,
            content=content,
            created_at=current,
            outcome=result.outcome,
            tool_name=tool_name,
        )
        return updated, step

    def should_resume(self, prompt: str) -> bool:
        normalized = " ".join(prompt.casefold().split())
        if not normalized:
            return False
        explicit_phrases = (
            "continue",
            "resume",
            "keep going",
            "go on",
            "carry on",
            "pick up where you left off",
            "keep working",
            "continue that",
            "resume that",
            "finish this",
            "finish it",
            "keep digging",
        )
        return any(
            normalized == phrase
            or normalized.startswith(f"{phrase} ")
            or normalized.endswith(f" {phrase}")
            for phrase in explicit_phrases
        )

    def resume_prompt_for_request(self, run: AgentRunState, prompt: str) -> str:
        base = run.continuation_prompt or self.build_continuation_prompt(run, recent_steps=())
        normalized = " ".join(prompt.casefold().split())
        if normalized in {"continue", "resume", "keep going", "go on", "carry on", "finish this", "finish it"}:
            return base
        return f"{base}\n\nLatest user nudge:\n{prompt.strip()}"

    def build_continuation_prompt(
        self,
        run: AgentRunState,
        *,
        recent_steps: Iterable[AgentRunStep],
        observations: Iterable[str] = (),
    ) -> str:
        sections = [
            "Continue the same Aegis agent run from its durable checkpoint.",
            f"Original user request:\n{run.prompt}",
        ]
        step_lines = []
        for step in recent_steps:
            step_lines.append(f"- {step.kind} | {step.title} | {_checkpoint_content_preview(step)}")
        if step_lines:
            sections.append("Recent durable checkpoints:\n" + "\n".join(step_lines))
        observation_lines = [item.strip() for item in observations if item.strip()]
        if observation_lines:
            sections.append("Latest tool observations:\n" + "\n\n".join(observation_lines))
        sections.append(
            "Continue from the latest checkpoint instead of restarting from scratch. "
            "If more tool work is required, call more tools directly when native tool calling is available; "
            "otherwise emit more <tool_call> markup. "
            "When the work is done, answer directly as Aegis without raw tool markup."
        )
        return "\n\n".join(sections)

    def interruption_state(self, run: AgentRunState) -> str | None:
        if run.status != "pending":
            return None
        reason = run.waiting_reason or "checkpointed"
        return f"agent-run:{run.run_id}:{reason}"
