"""Structured result contracts for background tasks and detached subagents (#1316).

TaskResult is a frozen dataclass that background tasks and detached subagents
populate on completion.  It is stored serialized in ``metadata_json`` so that
status tools can return a consistent, LLM-safe view without exposing internal
pointers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_SUMMARY_MAX_CHARS = 200
_LLM_TOOL_CALLS_MAX = 20


@dataclass(frozen=True)
class TaskResult:
    """Immutable result contract for completed async work units.

    Fields
    ------
    status:
        Terminal state — ``completed``, ``failed``, or ``cancelled``.
    summary:
        First 200 characters of primary output (stdout for shell tasks,
        ``output`` for subagents).
    exit_code:
        Shell exit code.  ``None`` for non-shell tasks.
    error:
        Human-readable error message or stderr preview.  ``None`` on success.
    tool_calls:
        Ordered list of tool names invoked (subagents only).
    output_pointer:
        Opaque reference to retrieve full output (``task_id`` for shell tasks,
        ``run_id`` for subagents).  **Never** exposed to the LLM.
    truncated:
        ``True`` when the summary was cut from a longer output.
    duration_seconds:
        Wall-clock elapsed time in seconds.
    """

    status: str
    summary: str
    exit_code: int | None
    error: str | None
    tool_calls: list[str]
    output_pointer: str | None
    truncated: bool
    duration_seconds: float

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Full serialization — suitable for storage in ``metadata_json``."""
        return {
            "status": self.status,
            "summary": self.summary,
            "exit_code": self.exit_code,
            "error": self.error,
            "tool_calls": list(self.tool_calls),
            "output_pointer": self.output_pointer,
            "truncated": self.truncated,
            "duration_seconds": self.duration_seconds,
        }

    def to_llm_dict(self) -> dict[str, Any]:
        """LLM-safe view — strips ``output_pointer`` and caps ``tool_calls``.

        This is the trust boundary: ``output_pointer`` is an internal reference
        that must never be forwarded to the model.  ``tool_calls`` is capped at
        ``_LLM_TOOL_CALLS_MAX`` entries to bound context size.
        """
        tool_calls = self.tool_calls[:_LLM_TOOL_CALLS_MAX]
        return {
            "status": self.status,
            "summary": self.summary,
            "exit_code": self.exit_code,
            "error": self.error,
            "tool_calls": tool_calls,
            "truncated": self.truncated,
            "duration_seconds": self.duration_seconds,
        }

    # ------------------------------------------------------------------
    # Deserialization
    # ------------------------------------------------------------------

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "TaskResult":
        """Reconstruct a ``TaskResult`` from a stored dict.

        Missing keys use safe defaults so older records (before this feature)
        can be loaded without errors.
        """
        return cls(
            status=d.get("status", "unknown"),
            summary=d.get("summary", ""),
            exit_code=d.get("exit_code"),
            error=d.get("error"),
            tool_calls=list(d.get("tool_calls") or []),
            output_pointer=d.get("output_pointer"),
            truncated=bool(d.get("truncated", False)),
            duration_seconds=float(d.get("duration_seconds", 0.0)),
        )

    # ------------------------------------------------------------------
    # Factory methods
    # ------------------------------------------------------------------

    @classmethod
    def from_shell_task(
        cls,
        exit_code: int,
        stdout: str,
        stderr: str,
        duration: float,
        task_id: str,
    ) -> "TaskResult":
        """Build a ``TaskResult`` from a completed shell subprocess.

        ``status`` is ``completed`` when ``exit_code == 0``, ``failed``
        otherwise.  ``summary`` is taken from the first ``_SUMMARY_MAX_CHARS``
        characters of stdout (or stderr when stdout is empty).
        """
        status = "completed" if exit_code == 0 else "failed"
        primary = stdout if stdout.strip() else stderr
        summary = primary[:_SUMMARY_MAX_CHARS]
        truncated = len(primary) > _SUMMARY_MAX_CHARS
        error: str | None = None
        if exit_code != 0:
            error = stderr[:_SUMMARY_MAX_CHARS] if stderr.strip() else f"Process exited with code {exit_code}"
        return cls(
            status=status,
            summary=summary,
            exit_code=exit_code,
            error=error,
            tool_calls=[],
            output_pointer=task_id,
            truncated=truncated,
            duration_seconds=round(duration, 3),
        )

    @classmethod
    def from_subagent_result(
        cls,
        result: dict[str, Any],
        run_id: str,
    ) -> "TaskResult":
        """Build a ``TaskResult`` from a completed subagent ``_run_subagent`` result dict.

        ``status`` is ``failed`` when ``result["error"]`` is set, ``completed``
        otherwise.  ``summary`` is taken from the first ``_SUMMARY_MAX_CHARS``
        characters of ``output``.  ``tool_calls`` is taken from
        ``tool_calls_made``.
        """
        error: str | None = result.get("error")
        status = "failed" if error else "completed"
        output: str = result.get("output") or ""
        summary = output[:_SUMMARY_MAX_CHARS]
        truncated = len(output) > _SUMMARY_MAX_CHARS
        raw_tool_calls = result.get("tool_calls_made") or []
        tool_calls = [str(t) for t in raw_tool_calls]
        duration = float(result.get("elapsed_seconds", 0.0))
        return cls(
            status=status,
            summary=summary,
            exit_code=None,
            error=error,
            tool_calls=tool_calls,
            output_pointer=run_id,
            truncated=truncated,
            duration_seconds=round(duration, 3),
        )
