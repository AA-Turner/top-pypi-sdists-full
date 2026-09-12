"""Structured compile errors.

Errors are **records, not strings**. A human reads the rendered form; the
built-in Dreadnode agent needs the fields, so it can fix a graph in one pass
rather than parsing prose (PRD §3, W13).

This is the one W13 requirement that runs backwards into W1 — cheap to design in
now, a retrofit once a renderer exists.
"""

import typing as t

from pydantic import BaseModel, ConfigDict

__all__ = ["CompileError", "ErrorCode", "WorkflowCompileError"]

ErrorCode = t.Literal[
    "WF-VALID-001",  # no step consumes StartEvent
    "WF-VALID-002",  # more than one step consumes StartEvent
    "WF-VALID-003",  # no step emits StopEvent
    "WF-VALID-004",  # Collect with no matching fan-out
    "WF-VALID-005",  # unreachable step
    "WF-VALID-006",  # dead-end event: emitted but never consumed
    "WF-VALID-007",  # cycle
    "WF-VALID-008",  # unknown agent name
    "WF-VALID-009",  # malformed or duplicate node key
    "WF-VALID-010",  # topology document over the size cap
    "WF-VALID-011",  # ctx.result() targets a fan-out step
    "WF-VALID-012",  # min_success exceeds the statically-known fan-out width
    "WF-VALID-013",  # step signature is not (ctx, event)
    "WF-VALID-014",  # missing or unresolvable return annotation
    "WF-VALID-015",  # `from __future__ import annotations` breaks introspection
    "WF-VALID-016",  # emitted type is not a WorkflowEvent
    "WF-VALID-017",  # Collect declares a type nothing emits
    "WF-VALID-018",  # title template references an unknown input field
    "WF-VALID-019",  # distinct event classes share a topology name
]


class CompileError(BaseModel):
    """One problem with an authored workflow."""

    model_config = ConfigDict(extra="forbid")

    code: ErrorCode
    message: str
    step: str | None = None
    path: str | None = None
    line: int | None = None
    hint: str | None = None

    def render(self) -> str:
        """The human-facing form."""
        where = ""
        if self.path and self.line:
            where = f"{self.path}:{self.line}: "
        elif self.step:
            where = f"step {self.step!r}: "
        out = f"{where}{self.message} [{self.code}]"
        if self.hint:
            out += f"\n    hint: {self.hint}"
        return out


class WorkflowCompileError(Exception):
    """Raised with *every* problem found, not just the first.

    Fixing a graph should be one pass, not whack-a-mole — for a human and for an
    agent alike.
    """

    def __init__(self, workflow: str, errors: t.Sequence[CompileError]) -> None:
        self.workflow = workflow
        self.errors = list(errors)
        super().__init__(self._render())

    def _render(self) -> str:
        lines = [
            f"workflow {self.workflow!r} failed to compile "
            f"({len(self.errors)} problem{'s' if len(self.errors) != 1 else ''}):",
        ]
        lines.extend(f"  - {e.render()}" for e in self.errors)
        return "\n".join(lines)

    def to_json_list(self) -> list[dict[str, t.Any]]:
        """The agent-facing form, for ``validate_workflow``."""
        return [e.model_dump(mode="json") for e in self.errors]
