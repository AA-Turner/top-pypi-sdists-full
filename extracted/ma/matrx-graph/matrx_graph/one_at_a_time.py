"""One at a time per key — a step that never runs twice at once for the same key (``data.one_at_a_time``).

THE GENERAL PROBLEM. Two runs that read, change and write back the same thing (a living
document, a ledger, a brand's profile, a conversation summary) must not do it at the same time:
the second overwrites the first's edits. A trigger fires per change, so two quick changes start
two runs; ``max_concurrent_runs`` caps a whole workflow (any key) and refuses instead of
waiting; ``data.once`` reuses a saved result and is the wrong tool for work that must happen
again (it would skip a run whose inputs repeat and flag every changed input). This setting
gives exactly the guarantee: for one key, at most one invocation of the step is working; the
next one WAITS its turn, then runs.

Authored on a node (opt-in, per step)::

    "data": {"one_at_a_time": {
        "key": ["session_id"],         # dotted paths into the step's RESOLVED inputs;
                                       # [] / absent = the whole input is the key
        "scope": "workflow",           # run | workflow | organization
        "name": "interview-document"   # optional: steps sharing a name share the turn
    }}                                 # (default: this step's id)

Put it on the step that does the read-change-write — usually a ``subgraph.call`` running the
whole unit — so the turn covers all of it.

THE RULES (each one has a test in ``tests/test_one_at_a_time.py``):

* The key comes from the step's resolved inputs — never from a request body. The organization is
  always part of the turn's identity; the acting user and the step's settings are not (the turn
  guards a shared thing, whoever touches it).
* While another invocation holds the turn, this one waits and SAYS so: a progress line on the step
  and one ``engine.waiting_turn`` info row in the run log, naming the run it waits for.
* The turn is a lease renewed while the step works (the ``workflow.once`` lease knobs). A holder
  that dies stops renewing; the first waiter after the lease runs out takes over. A run resumed at
  the same position takes its own earlier turn back at once.
* The turn ends when the step ends — success, failure, interrupt or cancel. Nothing is stored.
* A missing key part or a broken store never blocks a run: the step runs without a turn and the
  step carries an ``engine.one_at_a_time_unavailable`` review flag saying why.

The turns live in the same injected store as ``data.once`` claims (``configure_step_result_store``),
under the step type ``one_at_a_time:<name>``; a released turn leaves no row.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

TurnScope = Literal["run", "workflow", "organization"]

#: The store namespace a turn lives under — never a real step type (those have no colon prefix).
TURN_STEP_TYPE_PREFIX = "one_at_a_time:"

_MISSING = object()


class OneAtATimePolicy(BaseModel):
    """A parsed ``data.one_at_a_time`` setting."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    key: list[str] = Field(default_factory=list)
    scope: TurnScope = "workflow"
    name: str | None = Field(default=None, min_length=1, max_length=200)


def parse_one_at_a_time(raw: Any) -> OneAtATimePolicy | None:
    """``data.one_at_a_time`` → :class:`OneAtATimePolicy`; None when absent. Raises ``ValueError``
    (with the reason) on a malformed setting — the compiler turns it into a CompilationError."""
    if raw is None or raw is False:
        return None
    if raw is True:
        return OneAtATimePolicy()
    if not isinstance(raw, dict):
        raise ValueError(f"expected an object or true, got {type(raw).__name__}")
    data = dict(raw)
    key = data.get("key", [])
    if isinstance(key, str):
        data["key"] = [key]
    elif key is None:
        data["key"] = []
    try:
        policy = OneAtATimePolicy.model_validate(data)
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc
    for path in policy.key:
        if not path.strip() or any(not part for part in path.split(".")):
            raise ValueError(f"key part {path!r} is not a dotted path into the step's inputs")
    if policy.name is not None and not policy.name.strip():
        raise ValueError("name must not be blank")
    return policy


def _at_path(value: Any, path: str) -> Any:
    for part in path.split("."):
        if isinstance(value, dict):
            if part not in value:
                return _MISSING
            value = value[part]
        elif isinstance(value, list) and part.isdigit():
            index = int(part)
            if index >= len(value):
                return _MISSING
            value = value[index]
        else:
            return _MISSING
    return value


def turn_step_type(policy: OneAtATimePolicy, node_id: str) -> str:
    """The store namespace of this step's turn: its ``name``, else the step's own id."""
    return TURN_STEP_TYPE_PREFIX + (policy.name.strip() if policy.name else node_id)


def turn_key(policy: OneAtATimePolicy, inputs: dict[str, Any]) -> tuple[str | None, list[str]]:
    """The turn's key for these inputs, or ``(None, missing_paths)`` when a declared key part is
    absent (the step then runs without a turn and the engine flags it)."""
    if not policy.key:
        parts: Any = inputs
    else:
        found: list[Any] = []
        missing: list[str] = []
        for path in policy.key:
            value = _at_path(inputs, path)
            if value is _MISSING:
                missing.append(path)
            found.append(None if value is _MISSING else value)
        if missing:
            return None, missing
        parts = {"paths": policy.key, "parts": found}
    text = json.dumps(parts, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest(), []
