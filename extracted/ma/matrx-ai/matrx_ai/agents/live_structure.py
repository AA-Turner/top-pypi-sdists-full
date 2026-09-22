"""A conversation whose STRUCTURE is not its own — it belongs to a live Holder.

THE DEFECT THIS EXISTS FOR (2026-09-21). A Personal Staff thread is answered by
whoever holds a MANDATE, and an organization rebinds that Holder from the
console with no deploy. But continue-mode treats the persisted conversation as
the source of truth for the structural half of a turn — system prompt, model,
tools, settings — and ``persist_completed_request`` rewrites
``chat.conversation.config`` wholesale at the end of EVERY turn. So the belt the
Holder carried at 08:00 is frozen onto the row and re-frozen every turn after.

``personal_staff/thread_row.py`` already knew freezing was wrong there and drops
the structural keys — but it runs in ``open_staff_thread``, the IN-APP DOOR. The
SMS worker, the voice ingress, crash recovery and the deferred-result inbox
driver never open that door, so the repair was correct for one surface and
useless for the other four. Measured: ``ask_person`` was added to the Chief of
Staff's belt and five minutes later a headless turn on the live thread assembled
the OLD 18-tool belt and answered with the OLD refusal.

🚨 THE RULE THIS MODULE ENFORCES. A mandate-held conversation resolves the LIVE
Holder's prompt, model and belt on EVERY continuation, on EVERY surface, through
the ONE resolver seam (``ConversationResolver.from_conversation_id``) — never a
per-surface repair. Two halves, and both are needed:

  1. **The row says so, durably.** ``config[LIVE_STRUCTURE_KEY]`` marks the row
     as one whose structural half is not its own, and
     ``config[RESPONDER_MANDATE_KEY]`` names the role that answers in it. The
     marker rides in the ``config`` blob rather than a new column precisely
     because persistence rewrites that blob every turn — so the preserving code
     and the clobbering code are the same code, and a future turn cannot lose
     the marker without deleting the line that keeps it.
  2. **Persistence never re-freezes it.** ``HOLDER_OWNED_CONFIG_KEYS`` are
     dropped from the row on the way in, and the system prompt is not stamped.
     A row that carries no frozen structure cannot serve a stale one.

WHY THE MANDATE KEY AND NOT JUST ``initial_agent_id``. The row's named agent is
the Holder as of the last time somebody wrote it — which is the same staleness
one level up. When the row names a mandate, the live Holder is resolved through
the registered seam below, so rebinding the mandate moves the thread on the very
next turn whatever surface that turn arrives on.

BOUNDARY. matrx-ai must not import aidream: mandate resolution lives in the
host, so the host registers its resolver at boot
(``aidream/package_integration.py``). With no resolver registered — a package
consumer, a test — this module degrades to the row's named agent, which is still
live-per-turn and never worse than the frozen config it replaces.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from matrx_utils import vcprint

#: Marks a conversation whose structural half belongs to a live Holder.
LIVE_STRUCTURE_KEY = "structure_is_live"

#: Names the mandate whose Holder answers in this conversation.
RESPONDER_MANDATE_KEY = "responder_mandate_key"

#: Config keys that describe a HOLDER, not a conversation. Freezing these onto
#: a live-structure row is what made a rebound belt invisible to four of the
#: five continuation surfaces. ``model`` is deliberately NOT here: the staff
#: door writes the Holder's live model onto the row so a continuation that
#: cannot reach the Holder at all still has something to dispatch with.
HOLDER_OWNED_CONFIG_KEYS = (
    "system_prompt_frozen",
    "tool_authority_filtered",
    "tool_authority_exclusions",
    "tools",
    "authored_tools",
    "dynamic_tools",
    "custom_tools",
)


@dataclass(frozen=True)
class StructureSource:
    """Where a conversation's structural half comes from, read from its row."""

    conversation_id: str
    is_live: bool
    mandate_key: str | None
    named_agent_id: str | None
    named_is_version: bool
    user_id: str | None
    organization_id: str | None


#: ``(mandate_key, user_id, organization_id) -> agent_definition_id | None``
LiveHolderResolver = Callable[[str, str | None, str | None], Awaitable[str | None]]

_HOLDER_RESOLVER: LiveHolderResolver | None = None


def register_live_holder_resolver(resolver: LiveHolderResolver) -> None:
    """Host seam: teach this package how to turn a mandate key into its Holder."""
    global _HOLDER_RESOLVER
    _HOLDER_RESOLVER = resolver


def live_holder_resolver() -> LiveHolderResolver | None:
    return _HOLDER_RESOLVER


def marks_live_structure(config: Any) -> bool:
    """True when a config dict (or UnifiedConfig-ish object) carries the marker."""
    if isinstance(config, dict):
        return bool(config.get(LIVE_STRUCTURE_KEY))
    inner = getattr(config, "config", None)
    if isinstance(inner, dict):
        return bool(inner.get(LIVE_STRUCTURE_KEY))
    return False


def mandate_key_of(config: Any) -> str | None:
    if isinstance(config, dict):
        value = config.get(RESPONDER_MANDATE_KEY)
        return str(value) if value else None
    inner = getattr(config, "config", None)
    if isinstance(inner, dict):
        value = inner.get(RESPONDER_MANDATE_KEY)
        return str(value) if value else None
    return None


def stamp_live_structure(config: dict | None, *, mandate_key: str | None) -> dict:
    """The row's config as a live-structure row must carry it.

    Drops every Holder-owned key and writes the two markers. Used by the door
    that mints the thread and by persistence, which must reproduce exactly this
    shape at the end of every turn or the freeze comes back.
    """
    wanted = dict(config or {})
    for key in HOLDER_OWNED_CONFIG_KEYS:
        wanted.pop(key, None)
    wanted[LIVE_STRUCTURE_KEY] = True
    if mandate_key:
        wanted[RESPONDER_MANDATE_KEY] = str(mandate_key)
    return wanted


async def read_structure_source(conversation_id: str) -> StructureSource | None:
    """One primary-key read: what this row says about where its structure lives.

    Returns ``None`` for a client-host store (which owns its own configuration)
    and for any read failure — a rescue that cannot read must degrade to the
    behaviour it was rescuing, never take the turn down with it.
    """
    from matrx_ai.client_host import get_conversation_store

    if get_conversation_store() is not None:
        return None
    try:
        from matrx_ai.db import cxm

        row = await cxm.conversation.load_by_id(str(conversation_id))
    except Exception as exc:  # noqa: BLE001
        vcprint(
            f"[live-structure] could not read conversation {conversation_id} "
            f"({type(exc).__name__}: {exc}); the turn runs with the "
            f"conversation's own configuration.",
            color="yellow",
        )
        return None
    if row is None:
        return None

    config = row.config if isinstance(getattr(row, "config", None), dict) else {}
    version_id = getattr(row, "initial_agent_version_id", None)
    definition_id = getattr(row, "initial_agent_id", None)
    if version_id:
        named, named_is_version = str(version_id), True
    elif definition_id:
        named, named_is_version = str(definition_id), False
    else:
        named, named_is_version = None, False

    created_by = getattr(row, "created_by", None)
    org_id = getattr(row, "organization_id", None)
    return StructureSource(
        conversation_id=str(conversation_id),
        is_live=bool(config.get(LIVE_STRUCTURE_KEY)),
        mandate_key=(
            str(config[RESPONDER_MANDATE_KEY]) if config.get(RESPONDER_MANDATE_KEY) else None
        ),
        named_agent_id=named,
        named_is_version=named_is_version,
        user_id=str(created_by) if created_by else None,
        organization_id=str(org_id) if org_id else None,
    )


async def resolve_live_structure_agent(source: StructureSource) -> tuple[str | None, bool]:
    """The agent that supplies this turn's structural half, resolved LIVE.

    The mandate's current Holder when the row names a mandate and the host
    registered a resolver; otherwise the agent the row names. Never raises: a
    failure here degrades to the named agent and says so, because a staff thread
    answering from last week's belt is bad and a staff thread not answering at
    all is worse.
    """
    resolver = _HOLDER_RESOLVER
    if source.mandate_key and resolver is not None:
        try:
            holder = await resolver(
                source.mandate_key, source.user_id, source.organization_id
            )
        except Exception as exc:  # noqa: BLE001
            vcprint(
                f"[live-structure] mandate {source.mandate_key!r} could not be "
                f"resolved for conversation {source.conversation_id} "
                f"({type(exc).__name__}: {exc}). Falling back to the agent the "
                f"row names ({source.named_agent_id}). If the Holder was rebound, "
                f"this turn runs the previous one.",
                color="red",
            )
        else:
            if holder:
                return (str(holder), False)
            vcprint(
                f"[live-structure] mandate {source.mandate_key!r} has no Holder for "
                f"conversation {source.conversation_id}; falling back to the agent "
                f"the row names ({source.named_agent_id}).",
                color="yellow",
            )
    return (source.named_agent_id, source.named_is_version)


__all__ = [
    "HOLDER_OWNED_CONFIG_KEYS",
    "LIVE_STRUCTURE_KEY",
    "RESPONDER_MANDATE_KEY",
    "StructureSource",
    "live_holder_resolver",
    "mandate_key_of",
    "marks_live_structure",
    "read_structure_source",
    "register_live_holder_resolver",
    "resolve_live_structure_agent",
    "stamp_live_structure",
]
