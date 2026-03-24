"""Workflow diagnosis: structured explanation of blocked and failed runs.

Pure functions — no I/O. The caller gathers run, steps, and events,
then passes them in.  The diagnosis engine pattern-matches ``stop_reason``
and extracts evidence from step records and events.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DiagnosisEvidence:
    """A single piece of evidence supporting the diagnosis."""

    source: str  # "step_summary", "step_findings", "event_payload", "stop_reason"
    content: str
    location: str | None = None  # step_id, event_id, etc.


@dataclass(frozen=True)
class Diagnosis:
    """Structured diagnosis of a non-success workflow run."""

    category: str  # "runner_failure", "gate_block", "budget", "cancel", etc.
    what: str  # One-line summary
    why: str  # One-line explanation
    evidence: list[DiagnosisEvidence] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    confidence: str = "high"  # "high", "medium", "low"


@dataclass(frozen=True)
class _OutputAnalysis:
    """Internal normalized view of a step's failure output."""

    why: str
    evidence: list[DiagnosisEvidence] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    confidence: str = "high"


def diagnose(
    run: dict[str, Any],
    steps: list[dict[str, Any]],
    events: list[dict[str, Any]],
) -> Diagnosis:
    """Produce a structured diagnosis for a non-success run.

    Returns a Diagnosis with category, explanation, evidence, and next actions.
    """
    status = run.get("status", "unknown")
    stop_reason = run.get("stop_reason") or ""
    run_id = run.get("id", "?")
    run_id_short = run_id[:8]

    # --- Step failure ---
    step_failed_match = re.match(r"step_failed:(.+)", stop_reason)
    if step_failed_match:
        failing_step_id = step_failed_match.group(1)
        step = _find_step(steps, failing_step_id)
        evidence = [DiagnosisEvidence(source="stop_reason", content=stop_reason)]
        analysis = (
            _analyze_step_output(step, step_id=failing_step_id)
            if step
            else _OutputAnalysis(
                why="Step not found in records",
                confidence="medium",
            )
        )
        evidence.extend(analysis.evidence)

        return Diagnosis(
            category="runner_failure",
            what=f"Step {failing_step_id} failed",
            why=_truncate(analysis.why, 180),
            evidence=evidence,
            next_actions=analysis.next_actions
            or [
                f"Inspect step output: aroom workflow history {run_id_short}",
                f"Fix the issue and resume: aroom workflow resume {run_id_short}",
            ],
            confidence=analysis.confidence,
        )

    # --- Gate block ---
    blocked_match = re.match(r"blocked_at:(.+)", stop_reason)
    if blocked_match or (status == "blocked" and not step_failed_match):
        blocking_step_id = blocked_match.group(1) if blocked_match else run.get("current_step_id", "?")
        step = _find_step(steps, blocking_step_id) if blocking_step_id != "?" else None
        summary = (step.get("result_summary") or stop_reason) if step else stop_reason
        why = _humanize_gate_reason(summary or stop_reason or f"blocked_at:{blocking_step_id}")

        evidence = [DiagnosisEvidence(source="stop_reason", content=stop_reason or f"blocked at {blocking_step_id}")]
        if step:
            evidence.append(
                DiagnosisEvidence(
                    source="step_summary",
                    content=_truncate(summary, 400),
                    location=blocking_step_id,
                )
            )

        return Diagnosis(
            category="gate_block",
            what=f"Run blocked at {blocking_step_id}",
            why=_truncate(why, 180),
            evidence=evidence,
            next_actions=[
                "Satisfy the gate condition (e.g., add required label, fix upstream issue)",
                f"Then resume: aroom workflow resume {run_id_short}",
            ],
        )

    # --- Budget exceeded ---
    budget_match = re.match(r"budget_exceeded:(.+)", stop_reason)
    if budget_match:
        dimension = budget_match.group(1)
        budget = run.get("budget") or {}
        usage = run.get("budget_usage") or {}

        evidence = [
            DiagnosisEvidence(source="stop_reason", content=stop_reason),
            DiagnosisEvidence(source="budget", content=f"Budget: {budget}, Usage: {usage}"),
        ]

        return Diagnosis(
            category="budget",
            what=f"Budget exceeded: {dimension}",
            why=f"The {dimension} limit was reached before the run completed",
            evidence=evidence,
            next_actions=[
                f"Increase budget: aroom workflow repair {run_id_short} --field budget.max_{dimension} --value <N>",
                f"Then resume: aroom workflow resume {run_id_short}",
            ],
        )

    # --- Cancel ---
    if stop_reason == "cancel_requested" or status == "cancelled":
        return Diagnosis(
            category="cancel",
            what="Run was cancelled by operator",
            why="An operator requested cancellation",
            evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason or "cancelled")],
            next_actions=[
                "To restart: aroom workflow run <workflow> with the same inputs",
            ],
        )

    # --- Approval denied / expired ---
    if "approval_denied" in stop_reason:
        return Diagnosis(
            category="approval",
            what="Approval was denied",
            why=stop_reason,
            evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason)],
            next_actions=[
                "Review the denial reason and adjust the workflow or step",
                f"Resume after changes: aroom workflow resume {run_id_short}",
            ],
        )
    if "approval_expired" in stop_reason:
        return Diagnosis(
            category="approval",
            what="Approval request expired",
            why="The approval was not resolved before the timeout",
            evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason)],
            next_actions=[
                f"Resume to re-trigger the approval: aroom workflow resume {run_id_short}",
            ],
        )

    # --- Unhandled exception ---
    if stop_reason == "unhandled_exception":
        failing_step_id = run.get("current_step_id", "?")
        step = _find_step(steps, failing_step_id) if failing_step_id != "?" else None
        analysis = (
            _analyze_step_output(step, step_id=failing_step_id)
            if step
            else _OutputAnalysis(why="No step context", confidence="medium")
        )

        return Diagnosis(
            category="engine_error",
            what="Unhandled exception in the workflow engine",
            why=_truncate(analysis.why, 180),
            evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason), *analysis.evidence],
            next_actions=analysis.next_actions
            or [
                f"Inspect: aroom workflow history {run_id_short}",
                "This may be a bug — check logs for the full traceback",
            ],
            confidence=analysis.confidence,
        )

    # --- Target locked ---
    if stop_reason == "target_locked":
        return Diagnosis(
            category="concurrency",
            what="Target is locked by another run",
            why="Another workflow run holds the concurrency lock on this target",
            evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason)],
            next_actions=[
                "Wait for the other run to complete, or cancel it",
                "Then retry: aroom workflow run <workflow>",
            ],
        )

    # --- Human gate timeout ---
    if "human_timeout" in stop_reason or "human_decision_expired" in stop_reason:
        return Diagnosis(
            category="human_gate",
            what="Human gate decision expired",
            why="The operator did not respond before the timeout",
            evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason)],
            next_actions=[
                f"Resume to re-trigger the gate: aroom workflow resume {run_id_short}",
            ],
        )

    # --- Operator stopped ---
    if "operator_stopped" in stop_reason:
        return Diagnosis(
            category="human_gate",
            what="Operator chose to stop the workflow",
            why=stop_reason,
            evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason)],
            next_actions=[
                "To restart: aroom workflow run <workflow> with the same inputs",
            ],
        )

    # --- Compensation failure ---
    comp_match = re.match(r"compensation_failed:(.+)", stop_reason)
    if comp_match:
        failed_steps = comp_match.group(1)
        return Diagnosis(
            category="compensation",
            what=f"Compensation failed for: {failed_steps}",
            why="One or more rollback steps failed after the primary failure",
            evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason)],
            next_actions=[
                f"Inspect: aroom workflow history {run_id_short}",
                "Manual intervention may be required for the failed compensation steps",
            ],
        )

    # --- Process interrupted ---
    if "process_interrupted" in stop_reason:
        return Diagnosis(
            category="engine_error",
            what="Process was interrupted",
            why="The engine process crashed or was killed during execution",
            evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason)],
            next_actions=[
                f"Resume from last checkpoint: aroom workflow resume {run_id_short}",
            ],
        )

    # --- Unknown / no stop reason ---
    return Diagnosis(
        category="unknown",
        what=f"Run ended with status: {status}",
        why=_humanize_identifier(stop_reason) if stop_reason else "No stop reason recorded",
        evidence=[DiagnosisEvidence(source="stop_reason", content=stop_reason or "(empty)")],
        next_actions=[
            f"Inspect: aroom workflow history {run_id_short}",
        ],
        confidence="low",
    )


def _find_step(steps: list[dict[str, Any]], step_id: str) -> dict[str, Any] | None:
    """Find a step by step_id."""
    for s in steps:
        if s.get("step_id") == step_id:
            return s
    return None


def _get_findings(step: dict[str, Any]) -> list[str]:
    """Extract finding content strings from a step."""
    findings = step.get("result_findings") or []
    return [f.get("content", "") for f in findings if f.get("content")]


def _analyze_step_output(step: dict[str, Any], *, step_id: str) -> _OutputAnalysis:
    """Extract the most actionable explanation from a failed step record."""
    summary = str(step.get("result_summary") or "").strip()
    findings = _get_findings(step)
    raw_excerpt = str(step.get("_diagnosis_output_excerpt") or "").strip()

    evidence: list[DiagnosisEvidence] = []
    if summary:
        evidence.append(DiagnosisEvidence(source="step_summary", content=_truncate(summary, 500), location=step_id))

    # Prefer non-generic content from summary, then findings, then raw output tail.
    candidates: list[tuple[str, str]] = []
    if summary:
        candidates.append(("step_summary", summary))
    for finding in findings:
        candidates.append(("step_findings", finding))
    if raw_excerpt:
        candidates.append(("raw_output", raw_excerpt))

    best_analysis: _OutputAnalysis | None = None
    for source, text in candidates:
        analysis = _analyze_text_block(text, source=source, step_id=step_id)
        if analysis is not None:
            merged = _OutputAnalysis(
                why=analysis.why,
                evidence=[*evidence, *[ev for ev in analysis.evidence if ev not in evidence]],
                next_actions=analysis.next_actions,
                confidence=analysis.confidence,
            )
            if analysis.confidence == "high":
                return merged
            if best_analysis is None:
                best_analysis = merged

    if best_analysis is not None:
        return best_analysis

    if findings:
        for finding in findings:
            evidence.append(
                DiagnosisEvidence(
                    source="step_findings",
                    content=_truncate(finding, 500),
                    location=step_id,
                )
            )
        return _OutputAnalysis(why=_truncate(findings[0], 180), evidence=evidence)

    if raw_excerpt:
        evidence.append(DiagnosisEvidence(source="raw_output", content=_truncate(raw_excerpt, 500), location=step_id))
        return _OutputAnalysis(why=_truncate(_first_meaningful_line(raw_excerpt), 180), evidence=evidence)

    return _OutputAnalysis(why=summary or "No details available", evidence=evidence, confidence="medium")


def _analyze_text_block(text: str, *, source: str, step_id: str) -> _OutputAnalysis | None:
    """Interpret a text block from summary, findings, or raw output."""
    text = text.strip()
    if not text:
        return None

    if "Traceback (most recent call last):" in text:
        return _analyze_traceback(text, source=source, step_id=step_id)

    command_failure = _parse_command_failure(text, step_id=step_id)
    if command_failure is not None:
        return command_failure

    json_failure = _parse_json_failure(text, source=source, step_id=step_id)
    if json_failure is not None:
        return json_failure

    first_line = _first_meaningful_line(text)
    if not first_line:
        return None

    why = (
        _humanize_identifier(first_line)
        if source == "step_summary" and _looks_like_identifier(first_line)
        else first_line
    )
    return _OutputAnalysis(
        why=why,
        evidence=[DiagnosisEvidence(source=source, content=_truncate(text, 500), location=step_id)],
        confidence="medium" if _is_generic_failure_text(first_line) else "high",
    )


def _analyze_traceback(text: str, *, source: str, step_id: str) -> _OutputAnalysis:
    """Extract the useful signal from a Python traceback."""
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    exception_line = next((line.strip() for line in reversed(lines) if line.strip()), "Traceback")

    frames: list[str] = []
    for line in lines:
        if re.match(r'^\s*File ".*", line \d+, in .+$', line):
            frames.append(line.strip())

    why = _specialize_exception_message(exception_line, text)
    evidence = [DiagnosisEvidence(source="exception", content=exception_line, location=step_id)]
    if frames:
        evidence.append(DiagnosisEvidence(source="traceback_frame", content=frames[-1], location=step_id))

    return _OutputAnalysis(
        why=why,
        evidence=evidence,
        next_actions=_next_actions_for_exception(exception_line, text),
    )


def _parse_command_failure(text: str, *, step_id: str) -> _OutputAnalysis | None:
    """Parse script-style `Command failed:` output."""
    match = re.match(r"^Command failed:\s*(?P<command>[^\n]+)(?:\n(?P<detail>.*))?$", text, re.DOTALL)
    if not match:
        return None

    command = (match.group("command") or "").strip()
    detail = (match.group("detail") or "").strip()
    evidence = [DiagnosisEvidence(source="command", content=command, location=step_id)]

    if detail:
        nested = _analyze_text_block(detail, source="command_output", step_id=step_id)
        if nested is not None:
            return _OutputAnalysis(
                why=nested.why,
                evidence=[*evidence, *nested.evidence],
                next_actions=nested.next_actions,
                confidence=nested.confidence,
            )

    why = f"Command failed: {command}" if command else "Command failed"
    return _OutputAnalysis(why=why, evidence=evidence)


def _parse_json_failure(text: str, *, source: str, step_id: str) -> _OutputAnalysis | None:
    """Parse structured JSON error output when present."""
    stripped = text.strip()
    if not stripped.startswith(("{", "[")):
        return None

    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        return None

    message = _extract_json_message(payload)
    if not message:
        return None

    evidence = [
        DiagnosisEvidence(
            source=source,
            content=_truncate(stripped, 500),
            location=step_id,
        )
    ]
    return _OutputAnalysis(why=message, evidence=evidence)


def _extract_json_message(payload: Any) -> str | None:
    """Extract a human-meaningful message from JSON-like data."""
    if isinstance(payload, str):
        return payload.strip() or None
    if isinstance(payload, dict):
        for key in ("error", "message", "detail", "reason", "stderr", "stdout"):
            value = payload.get(key)
            message = _extract_json_message(value)
            if message:
                if key == "error" and isinstance(value, dict):
                    code = value.get("code")
                    return f"{message} (code: {code})" if code else message
                return message
        return None
    if isinstance(payload, list):
        for item in payload:
            message = _extract_json_message(item)
            if message:
                return message
    return None


def _specialize_exception_message(exception_line: str, traceback_text: str) -> str:
    """Turn raw exception text into a clearer operator-facing explanation."""
    if exception_line.startswith("NotADirectoryError:") and "/.git/" in traceback_text:
        return (
            "The step tried to write under `.git/...`, but this run is in a linked git worktree "
            "where `.git` is a file, not a directory."
        )
    if exception_line.startswith("FileNotFoundError:"):
        return exception_line
    if exception_line.startswith("PermissionError:"):
        return exception_line
    if "Required tool not found in PATH:" in exception_line:
        return exception_line
    return exception_line


def _next_actions_for_exception(exception_line: str, traceback_text: str) -> list[str]:
    """Return targeted remediation hints for recognizable exceptions."""
    actions: list[str] = []
    if exception_line.startswith("NotADirectoryError:") and "/.git/" in traceback_text:
        actions.append("This step assumes `.git` is a directory; linked git worktrees store `.git` as a pointer file.")
        actions.append(
            "Run the workflow from the main checkout, or patch the script to resolve `git rev-parse --git-dir`."
        )
        return actions
    if "Required tool not found in PATH:" in exception_line:
        actions.append("Install the missing tool or make sure the workflow subprocess PATH includes it.")
        return actions
    return actions


def _humanize_gate_reason(reason: str) -> str:
    """Convert internal gate/block reasons into a readable sentence."""
    reason = reason.strip()
    if not reason:
        return "A gate condition blocked the run"
    if reason.startswith("blocked_"):
        reason = reason[len("blocked_") :]
    if reason.startswith("blocked_at:"):
        reason = reason[len("blocked_at:") :]
    return _humanize_identifier(reason)


def _humanize_identifier(value: str) -> str:
    """Turn `snake_case` stop reasons into readable text."""
    value = value.strip()
    if not value:
        return value
    if any(ch in value for ch in " \n\t") or ":" in value:
        return value
    humanized = value.replace("_", " ").strip()
    if not humanized:
        return value
    return humanized[0].upper() + humanized[1:]


def _looks_like_identifier(text: str) -> bool:
    """Heuristic: plain machine identifier rather than a sentence."""
    return bool(re.fullmatch(r"[a-z0-9_./:-]+", text)) and "_" in text


def _is_generic_failure_text(text: str) -> bool:
    """Detect placeholders that need better context than the first line alone."""
    normalized = text.strip().lower()
    if not normalized:
        return True
    generic_prefixes = (
        "traceback (most recent call last):",
        "exit code ",
        "command failed:",
        "runner error:",
        "no details",
    )
    return normalized.startswith(generic_prefixes)


def _first_meaningful_line(text: str) -> str:
    """Return the first non-empty line, skipping traceback headers."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and stripped != "Traceback (most recent call last):":
            return stripped
    return text.strip()


def _truncate(text: str, max_len: int) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."
