"""A RUN and its way back — what one outermost ``run_action`` did, and how it is undone.

One press, one tool call or one workflow step is one RUN (``ActionCall.run_id``), however many
Actions it runs inside itself. This module is the package half of "every run is one change":

* **The inverse is DECLARED, never derived from rows** (FULL-CONTROL-UNDO amendment 5). An Action
  says how its own effect is taken back: ``declare_action(..., inverse=fn)`` where
  ``fn(input, output) -> list[InverseStep] | None`` names the Actions (and their inputs) that undo
  it, or ``inverse=INVERSE_OF_PARTS`` to be undone by undoing, newest first, every Action it ran
  inside itself. An Action with no inverse is NOT undoable, and says so.
* **The router reports each outermost run to the host** (``configure_run_recorder``): ``begin`` as
  it starts and ``finish`` with a :class:`RunRecord` as it ends, whether it succeeded or failed.
  The host (aidream: ``services/action_runs``) writes the one envelope. With no recorder (a
  standalone graph) nothing is recorded and nothing changes.

The package knows nothing about the host's database: the recorder is injected.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)


class InverseStep(BaseModel):
    """One Action call that takes back (part of) a run: the Action's name and its input."""

    model_config = ConfigDict(extra="forbid")

    action: str = Field(min_length=1, max_length=200)
    input: dict[str, Any] = Field(default_factory=dict)


#: ``(input, output) -> steps``: ``None`` = this call cannot be undone; ``[]`` = nothing to undo.
InverseFn = Callable[[BaseModel, BaseModel], "list[InverseStep] | None"]
#: Undo this Action by undoing every Action it ran inside itself, newest first.
INVERSE_OF_PARTS = "inverse_of_parts"

_INVERSES: dict[str, InverseFn | str] = {}


def declare_inverse(action: str, inverse: InverseFn | str | None) -> None:
    """Say how ``action`` is undone (``None`` removes a declaration)."""
    if inverse is None:
        _INVERSES.pop(action, None)
        return
    if isinstance(inverse, str) and inverse != INVERSE_OF_PARTS:
        raise ValueError(f"Action {action!r}: an inverse is a function or INVERSE_OF_PARTS, not {inverse!r}.")
    if not isinstance(inverse, str) and not callable(inverse):
        raise TypeError(f"Action {action!r}: an inverse is a function or INVERSE_OF_PARTS.")
    _INVERSES[action] = inverse


def inverse_of(action: str) -> InverseFn | str | None:
    """The declared inverse of ``action``, or ``None`` when it declares none."""
    return _INVERSES.get(action)


@dataclass
class Part:
    """What one finished call contributes to its run's way back."""

    action: str
    steps: list[InverseStep] | None
    reason: str | None = None


@dataclass
class RunRecord:
    """One outermost run, as the router hands it to the host's recorder."""

    run_id: str
    action: str
    door: str
    authority: str | None
    app: Any
    input: BaseModel | None
    output: BaseModel | None
    #: The run's way back, newest first; ``None`` = it cannot be undone (``not_undoable`` says why).
    inverse: list[InverseStep] | None
    not_undoable: list[str] = field(default_factory=list)
    #: What ``begin`` returned (the host's mark), handed back unchanged.
    mark: Any = None
    error: BaseException | None = None


class RunRecorder(Protocol):
    async def begin(self, spec: Any, app: Any, run_id: str) -> Any: ...

    async def finish(self, record: RunRecord) -> None: ...


_RECORDER: list[RunRecorder] = []


def configure_run_recorder(recorder: RunRecorder | None) -> None:
    """The host plugs in the ONE recorder of runs (aidream: ``action_runs.recorder``)."""
    _RECORDER.clear()
    if recorder is not None:
        _RECORDER.append(recorder)


def run_recorder() -> RunRecorder | None:
    return _RECORDER[0] if _RECORDER else None


#: The parts list of the call that is running now: each finished child call appends one Part.
_PARTS: ContextVar[list[Part] | None] = ContextVar("action_run_parts", default=None)


def inverse_for(action: str, data: BaseModel | None, out: Any, parts: list[Part]) -> tuple[list[InverseStep] | None, str | None]:
    """The way back for one finished call: its declared inverse, or the reverse of its parts.

    ``out`` is the call's typed output, or a started / queued / client handle (read by status).
    """
    status = getattr(out, "status", None)
    if status in ("queued", "client"):
        return [], None  # nothing ran here
    if status == "started" and hasattr(out, "request_id"):
        return None, (
            f"{action} started work that finishes later; that work is not part of this change and "
            "cannot be undone with it."
        )
    declared = inverse_of(action)
    if declared is None:
        if not parts:
            return None, f"{action} declares no way to undo it."
        return None, f"{action} declares no way to undo it, so the changes it made inside itself stay."
    if declared == INVERSE_OF_PARTS:
        steps: list[InverseStep] = []
        for part in reversed(parts):
            if part.steps is None:
                return None, part.reason or f"{part.action} declares no way to undo it."
            steps.extend(part.steps)
        return steps, None
    try:
        made = declared(data, out)  # type: ignore[operator, arg-type]
        if made is None:
            return None, f"{action} cannot be undone in this case."
        # A badly shaped step is "not undoable", said; never an exception after the write succeeded.
        return [s if isinstance(s, InverseStep) else InverseStep.model_validate(s) for s in made], None
    except Exception as exc:  # noqa: BLE001 - an inverse that cannot be worked out is "not undoable", said
        logger.warning("action run: the inverse of %s could not be worked out (%s: %s)", action, type(exc).__name__, exc)
        return None, f"The way to undo {action} could not be worked out ({type(exc).__name__})."


def open_parts() -> tuple[list[Part], Any]:
    """A fresh parts list for the call starting now; returns it and the token to reset."""
    parts: list[Part] = []
    return parts, _PARTS.set(parts)


def close_parts(token: Any) -> None:
    _PARTS.reset(token)


def report_part(part: Part) -> None:
    """Hand a finished call's Part to the call that ran it (no-op for an outermost call)."""
    parent = _PARTS.get()
    if parent is not None:
        parent.append(part)



__all__ = [
    "INVERSE_OF_PARTS",
    "InverseFn",
    "InverseStep",
    "Part",
    "RunRecord",
    "RunRecorder",
    "close_parts",
    "configure_run_recorder",
    "declare_inverse",
    "inverse_for",
    "inverse_of",
    "open_parts",
    "report_part",
    "run_recorder",
]
