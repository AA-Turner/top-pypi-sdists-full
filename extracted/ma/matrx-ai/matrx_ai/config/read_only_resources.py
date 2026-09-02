"""Per-request read-only resource registry — the hard enforcement behind an
explicitly read-only (``editable=False``) structured-input attachment.

When a user marks an id-backed attachment read-only, the agent must not be able
to modify *that resource* no matter how it tries: not via the resource's own edit
tool, not via the generic ``data`` tool, and not because the agent already
happens to carry an edit tool. The soft READ-ONLY notice in the injected context
handles the well-behaved case cheaply; this registry is the hard backstop that
makes the lock real.

Mechanism: the resolver walks every user message each turn and records the live
ids of all explicitly read-only attachments into ``AppContext.metadata`` under
``READ_ONLY_RESOURCE_IDS_KEY``. Any write-capable tool calls
:func:`is_resource_read_only` with its target id before mutating and refuses when
it is locked. The metadata dict is shared across ``with_overrides`` copies (see
``AppContext``), so a single in-place write is visible to every downstream tool.

The collector applies attachment decisions in message order, so the latest
explicit decision for an id wins: false locks, true unlocks, and an omitted value
does not override. This is mode-agnostic by design: ids are UUIDs, so a single
flat set is enough and identities from different resource families do not
collide.
"""

from __future__ import annotations

from collections.abc import Iterable

# Key under AppContext.metadata holding the set[str] of read-only resource ids
# for the current request. Mirrors the PROJECTED_AGENT_TOOLS_KEY convention.
READ_ONLY_RESOURCE_IDS_KEY = "read_only_resource_ids"

# Uniform, model-readable refusal returned by every write tool that hits a locked
# resource. Short and actionable — the user, not the agent, holds the unlock.
READ_ONLY_TOOL_MESSAGE = (
    "This resource is attached as read-only. It cannot be modified. "
    "Ask the user to enable 'editable' on the attachment if a change is needed."
)


def set_read_only_resource_ids(metadata: dict, ids: Iterable[str]) -> None:
    """Replace the request's read-only id set on the given metadata dict.

    Mutates in place (metadata is the shared ``AppContext.metadata``). Rebuilt
    every turn from the full message history, so a plain replace is correct — an
    empty set clears the key entirely so a stale lock never lingers.
    """
    id_set = {i for i in ids if i}
    if id_set:
        metadata[READ_ONLY_RESOURCE_IDS_KEY] = id_set
    else:
        metadata.pop(READ_ONLY_RESOURCE_IDS_KEY, None)


def is_resource_read_only(resource_id: str | None) -> bool:
    """Whether ``resource_id`` is locked read-only for the current request.

    Reads the active ``AppContext``; returns ``False`` when there is no context
    or no lock set (the safe default — absence of a lock never blocks a write).
    """
    if not resource_id:
        return False
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return False
    ids = (ctx.metadata or {}).get(READ_ONLY_RESOURCE_IDS_KEY)
    return bool(ids) and resource_id in ids


def has_read_only_resources() -> bool:
    """Whether the current request carries any explicit read-only locks."""
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return False
    return bool((ctx.metadata or {}).get(READ_ONLY_RESOURCE_IDS_KEY))
