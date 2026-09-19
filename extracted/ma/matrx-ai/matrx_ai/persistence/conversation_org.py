"""The organization a conversation's child rows belong to.

THE LAW (``common-docs/policies/context-is-carried-never-rebuilt.md``): a child
row lives in its PARENT record's organization. ``chat.message``,
``chat.tool_call``, ``chat.observational_memory`` and every other row hanging off
a conversation therefore take their ``organization_id`` from the conversation
row — never from whatever organization the ambient request happens to be
carrying.

Why this module exists: the child writes are queued from a synchronous door
(``matrx_ai.persistence.queue_helpers``), often from a detached task whose
contextvars are a COPY of some earlier scope, so the queue point can neither
await a DB read nor trust the ambient ``AppContext``. This registry is the
in-process answer to "which organization does conversation X live in?", written
once by the code that authoritatively reads or creates the conversation row:

* ``matrx_ai.db.conversation_gate`` — the existence SELECT and every create;
* ``queue_conversation_create`` — the write funnel for a new conversation;
* aidream's ``restore_conversation_context`` — the continue/resume path's
  authoritative read.

Measured 2026-09-17 on production: 211 ``chat.tool_call`` rows in 30 days (742
all-time) and 3,217 ``chat.message`` rows landed in an organization that was NOT
their conversation's, because the queue door stamped the ambient request's
organization — the user's ACTIVE organization, or a previous request's context
leaking across a detached-task boundary.

Bounded and process-local by design: a miss degrades to the previous behaviour
(ambient stamp + the DB's NULL-only inheritance trigger), never to a wrong
answer of its own invention.
"""

from __future__ import annotations

from collections import OrderedDict

__all__ = [
    "conversation_organization",
    "forget_conversation_organization",
    "remember_conversation_organization",
    "reset_conversation_organizations",
]

# Bounded so a long-lived worker cannot grow this without limit. Deliberately the
# SAME ceiling as conversation_gate's ``_known_conversation_ids`` memo: the two
# are written at the same moments, so matching ceilings keep them evicting in
# lockstep — a conversation the gate still remembers is one this registry can
# still answer for.
_MAX_ENTRIES = 50_000

_CONVERSATION_ORG: OrderedDict[str, str] = OrderedDict()


def remember_conversation_organization(
    conversation_id: str | None, organization_id: str | None
) -> None:
    """Record the organization the conversation row actually carries.

    Never raises. A falsy id on either side is ignored — an unknown organization
    is recorded as "unknown", never as a guess.
    """
    if not conversation_id or not organization_id:
        return
    key = str(conversation_id)
    value = str(organization_id)
    _CONVERSATION_ORG[key] = value
    _CONVERSATION_ORG.move_to_end(key)
    while len(_CONVERSATION_ORG) > _MAX_ENTRIES:
        _CONVERSATION_ORG.popitem(last=False)


def conversation_organization(conversation_id: str | None) -> str | None:
    """The conversation's organization, or ``None`` when this process has not
    read the row yet."""
    if not conversation_id:
        return None
    key = str(conversation_id)
    value = _CONVERSATION_ORG.get(key)
    if value is not None:
        _CONVERSATION_ORG.move_to_end(key)
    return value


def forget_conversation_organization(conversation_id: str | None) -> None:
    if not conversation_id:
        return
    _CONVERSATION_ORG.pop(str(conversation_id), None)


def reset_conversation_organizations() -> None:
    """Test seam — drop everything this process has recorded."""
    _CONVERSATION_ORG.clear()
