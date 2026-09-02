"""D-3 — the stable agent-facing handle.

S2 and S6 both initially landed on ``session_id = run_id``. S2 flagged the case
that breaks it: an ``automation_only`` run that must be closed and reopened
headed for a human takeover ENDS one run and BEGINS another — but the agent is
holding one identifier across that moment.

DECISIONS.md D-3 (RATIFIED): the agent-facing handle stays **stable across a
reopen**. It is therefore not the bare run id at every instant; it is a handle
that resolves to the current run for its profile, and ``run_id`` is returned
alongside it as additive detail. The reopen is made visible to the agent through
the existing ``reopened_for_handoff`` outcome — never through a silently changed
identifier.

The stable handle IS the opaque ``profile_id`` (S6 §3.1): access is re-checked
on every single call regardless, so the handle alone grants nothing
(``OPEN(profile-id-opacity)`` recommendation). ``session_id``/``run_id`` remain
the per-run detail (S6 §4.1). This module makes that resolution explicit and
testable: given the stable handle, resolve the CURRENT run.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict


class AgentBrowserHandle(BaseModel):
    """What the agent holds across a reopen. ``handle`` is stable for the
    profile's lifetime; ``run_id`` is the current run and changes on a reopen."""

    model_config = ConfigDict(extra="forbid")

    handle: str  # the stable, opaque agent-facing handle (== profile_id, S6 §3.1)
    run_id: str | None  # the CURRENT run for this handle; None when no live run


@runtime_checkable
class RunResolver(Protocol):
    """Browser Manager resolution: stable handle → current run id. The durable
    column that makes this resolution survive a reopen lives in S1."""

    async def current_run_id(self, handle: str) -> str | None: ...


def stable_handle_for(profile_id: str) -> str:
    """The agent-facing handle for a profile. Identity today; a distinct function
    so a future opaque-token decision (``OPEN(profile-id-opacity)``) changes ONE
    place, never every call site."""
    return profile_id


async def resolve_current_run(
    resolver: RunResolver, *, profile_id: str
) -> AgentBrowserHandle:
    """Resolve a stable handle to its current run. A reopened profile resolves to
    its NEW run id here, so the handle the agent held keeps working — the run
    change surfaces only through ``reopened_for_handoff``, never as a broken
    identifier."""
    handle = stable_handle_for(profile_id)
    run_id = await resolver.current_run_id(handle)
    return AgentBrowserHandle(handle=handle, run_id=run_id)
