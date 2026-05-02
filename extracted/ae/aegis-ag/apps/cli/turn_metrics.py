"""Chat turn metric rendering helpers for CLI surfaces."""

from __future__ import annotations

from packages.kernel.runtime import KernelOutcome

from .shell_progress_support import outcome_intent_meta


def cache_hit_metric_line(execution: object) -> str:
    if not bool(getattr(execution, "cache_usage_reported", False)):
        return ""
    prompt_tokens = max(0, int(getattr(execution, "prompt_tokens", 0) or 0))
    cached_tokens = max(0, int(getattr(execution, "cached_prompt_tokens", 0) or 0))
    creation_tokens = max(0, int(getattr(execution, "cache_creation_prompt_tokens", 0) or 0))
    if prompt_tokens <= 0:
        return "cache_hit_rate: n/a"
    label = f"{(cached_tokens / prompt_tokens) * 100:.1f}%"
    creation_note = f"; cache_write_tokens={creation_tokens}" if creation_tokens else ""
    return f"cache_hit_rate: {label} ({cached_tokens}/{prompt_tokens} input tokens cached{creation_note})"


def cache_hit_meta_segment(execution: object) -> str:
    if not bool(getattr(execution, "cache_usage_reported", False)):
        return ""
    prompt_tokens = max(0, int(getattr(execution, "prompt_tokens", 0) or 0))
    if prompt_tokens <= 0:
        return "cache hit · n/a"
    cached_tokens = max(0, int(getattr(execution, "cached_prompt_tokens", 0) or 0))
    return f"cache hit · {(cached_tokens / prompt_tokens) * 100:.1f}%"


def _append_meta_segment(meta: str, segment: str) -> str:
    if not segment:
        return meta
    if not meta:
        return segment
    return f"{meta} · {segment}"


def _append_outcome(self, outcome: KernelOutcome) -> None:
    self._last_prompt_tokens = outcome.execution.prompt_tokens
    self._last_completion_tokens = outcome.execution.completion_tokens
    self._last_total_tokens = outcome.execution.total_tokens
    if self.debug and outcome.stages:
        stage_lines = [
            f"{stage.stage} | {stage.detail} | {stage.recorded_at.isoformat(timespec='seconds')}"
            for stage in outcome.stages
        ]
        self._append_entry("status", "Runtime stages", "\n".join(stage_lines))
    assistant_name = self.runtime.inspect_profile(self.runtime.inspect_session(self.session_id).profile_id).state.display_name
    assistant_lines = [outcome.execution.summary]
    if self.debug and outcome.plan is not None:
        assistant_lines.append(f"plan: {outcome.plan.rationale}")
    if self.debug:
        assistant_lines.extend(
            [
                f"execution: {outcome.execution.outcome}",
                f"goals_in_play: {len(outcome.goals)}",
                f"memory_hits: {len(outcome.memories)}",
            ]
        )
    meta = _append_meta_segment(outcome_intent_meta(outcome), cache_hit_meta_segment(outcome.execution))
    self._append_entry("assistant", assistant_name, "\n".join(assistant_lines), meta=meta)
