"""FEAT-555 — shared contracts for NextTask continuations.

This module is a leaf: it must never import ``flowtask.tasks.task``,
``flowtask.tasks.pile`` or ``flowtask.conf``, all of which import it.
"""
from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..exceptions import TaskError  # verified: flowtask/exceptions.py:41
from ..models import TaskState  # verified: flowtask/models.py:19


class ChainError(TaskError):
    """Base error for NextTask continuations."""


class ChainEncodingError(ChainError):
    """A payload result could not be encoded for a process boundary."""


class ChainRefused(ChainError):
    """A hop was refused by the lineage/depth guard."""


class ChainTrigger(str, Enum):
    """Values accepted by the ``on:`` key of a NextTask step (spec §2 table)."""

    SUCCESS = "success"
    NODATA = "nodata"
    WARNING = "warning"
    FAILURE = "failure"
    ALWAYS = "always"

    def matches(self, state: TaskState) -> bool:
        """Return whether this trigger fires for a terminal task state.

        Args:
            state: The origin task's ``_state`` at ``close()`` time.

        Returns:
            True when the hop should run. ``ALWAYS`` matches every state.
        """
        # ALWAYS short-circuits to True for any state
        if self == ChainTrigger.ALWAYS:
            return True
        # Look up the trigger in TRIGGER_STATES and test membership
        states = TRIGGER_STATES.get(self)
        if states is None:
            # An unmapped trigger returns False, never raises
            return False
        return state in states


#: The normative ``on:`` → terminal ``TaskState`` mapping (spec §2, AC-9).
#: ALWAYS is intentionally absent: it is handled by `matches()` short-circuit.
TRIGGER_STATES: dict[ChainTrigger, frozenset[TaskState]] = {
    ChainTrigger.SUCCESS: frozenset({TaskState.DONE}),
    ChainTrigger.NODATA: frozenset({TaskState.DONE_WITH_NODATA}),
    ChainTrigger.WARNING: frozenset({TaskState.DONE_WITH_WARNINGS}),
    ChainTrigger.FAILURE: frozenset(
        {TaskState.ERROR, TaskState.EXCEPTION, TaskState.FAILED}
    ),
}

# Framework-only keys that TaskPile/YAML add to every step but are NOT
# Continuation fields. These must be stripped before model_validate.
_FRAMEWORK_KEYS = frozenset({"Group", "to_group"})


class Continuation(BaseModel):
    """One reserved ``NextTask`` step, validated at ``TaskPile.build()`` time."""

    model_config = ConfigDict(extra="forbid")

    step_name: str  # e.g. "NextTask_4"
    task: str
    program: str | None = None  # None → origin program
    executor: str | dict[str, Any] = "inline"
    priority: str | None = None  # qworker shortcut
    on: ChainTrigger = ChainTrigger.SUCCESS
    variables: dict[str, Any] = Field(default_factory=dict)
    result: bool = True  # False → hand off variables only
    storage: str | None = None  # None → inherit origin
    filestore: str | None = None  # None → inherit origin

    @classmethod
    def from_step(cls, step_name: str, params: dict[str, Any]) -> Continuation:
        """Build a Continuation from a raw ``NextTask`` YAML params dict.

        Args:
            step_name: The reserved step id, e.g. ``"NextTask_2"``.
            params: The YAML mapping under the ``NextTask:`` key.

        Returns:
            A validated Continuation.

        Raises:
            pydantic.ValidationError: Unknown key, missing ``task``, or a bad
                ``on:`` value. TaskPile wraps this into ``TaskDefinition``.
        """
        # Strip the framework-only keys that TaskPile/YAML add to every step
        # and that are NOT Continuation fields
        filtered_params = {
            k: v for k, v in params.items() if k not in _FRAMEWORK_KEYS
        }
        # Add step_name to the filtered params
        filtered_params["step_name"] = step_name
        # Validate the rest with pydantic
        return cls.model_validate(filtered_params)


class ChainLineageEntry(BaseModel):
    """One task in a chain's ancestry."""

    task_id: str
    program: str
    task: str


class ChainMetadata(BaseModel):
    """Provenance travelling with a chain payload."""

    origin_task_id: str
    origin_program: str
    origin_task: str
    origin_state: str  # TaskState.name, e.g. "DONE"
    finished_at: str  # ISO-8601 UTC
    stats_summary: dict[str, Any] | None = None
    lineage: list[ChainLineageEntry] = Field(default_factory=list)

    @property
    def depth(self) -> int:
        """Number of tasks already in this chain, including the origin."""
        return len(self.lineage)


class ChainPayload(BaseModel):
    """What an origin task hands to each of its continuations."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    result: Any = None
    variables: dict[str, Any] = Field(default_factory=dict)
    metadata: ChainMetadata

    def as_variables(self) -> dict[str, Any]:
        """Return the flat ``chain_*`` variables exposed to the hop.

        Returns:
            Exactly six keys: ``chain_origin_task_id``, ``chain_origin_program``,
            ``chain_origin_task``, ``chain_origin_state``, ``chain_depth`` and
            ``chain_lineage`` (a list of ``"<program>.<task>"`` strings).
        """
        # Build the six-key dict from self.metadata
        lineage_list = [
            f"{entry.program}.{entry.task}" for entry in self.metadata.lineage
        ]
        return {
            "chain_origin_task_id": self.metadata.origin_task_id,
            "chain_origin_program": self.metadata.origin_program,
            "chain_origin_task": self.metadata.origin_task,
            "chain_origin_state": self.metadata.origin_state,
            "chain_depth": self.metadata.depth,
            "chain_lineage": lineage_list,
        }


class ChainHopResult(BaseModel):
    """Outcome of one continuation hop; never raised, always returned."""

    step_name: str
    program: str
    task: str
    mode: str  # "inline" | "remote:<executor>" | "skipped" | "refused"
    status: str  # "success" | "failed" | "skipped" | "refused" | "cancelled"
    hop_task_id: str | None = None
    execution_id: str | None = None
    reason: str | None = None