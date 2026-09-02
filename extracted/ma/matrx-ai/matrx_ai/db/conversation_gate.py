"""
Conversation Gate — Ensures cx_conversation and cx_user_request rows
exist before AI execution begins.

The boundary layer (API route handler, batch script, workflow trigger)
is responsible for creating both rows.  The AI execution engine
(``execute_until_complete``) only reads and updates them.

**Conversation** — ``ensure_conversation_exists()``

  Idempotent: creates the ``cx_conversation`` row if it does not already
  exist, and is a no-op if it does.  Called by boundary-layer code before
  any execution starts.

  API routes may additionally call ``verify_existing_conversation()`` as
  an early-exit check for the ``is_new_conversation=False`` path.

**User Request** — ``ensure_user_request_exists()``

  Idempotent: creates a ``cx_user_request`` row with ``status='pending'``
  if one does not already exist for the given ``request_id``, and is a
  no-op if it does.  The boundary layer calls this ONCE per user action
  (HTTP request, button click, batch job, workflow trigger), using the
  ``request_id`` from ``AppContext`` as the primary key.

  A ``cx_user_request`` is ONE backend API call (one user action), keyed
  solely by ``request_id`` and owned by ``user_id``. It has NO conversation.
  The request↔conversation relationship is genuinely many-to-many and lives
  entirely on ``cx_request`` (which carries BOTH ``user_request_id`` and
  ``conversation_id``): one request can fan out to many conversations
  (batch), and one conversation spans many requests (multi-turn).

  This guarantees:
    - Every user action is recorded, even those that crash mid-flight.
    - Downstream ``cx_tool_call`` rows can immediately reference the
      ``request_id`` FK without a post-hoc backfill.
    - A batch of N AI calls under one user action — across one OR many
      conversations — shares a single ``cx_user_request`` row that
      aggregates all costs and tokens, with one ``cx_request`` per call
      carrying its own ``conversation_id``.

  ``create_pending_user_request()`` is retained for callers that need
  a strict INSERT (e.g. internal tools that guarantee no duplicate).

Downstream persistence (``ai.db.persistence``) only **updates** — it
never creates conversations or user requests.
"""

from __future__ import annotations

import asyncio
import traceback
from collections import OrderedDict
from contextvars import ContextVar
from typing import Any
from uuid import UUID

from matrx_connect.reservations import try_get_tracker
from matrx_utils import detached_task, vcprint

from matrx_ai.agents.conversation_type import derive_conversation_type

from .ownership_fields import stamp_org_id, stamp_row_owner


def _cxm():
    # Lazy: resolving cxm constructs host-injected ORM managers, which requires
    # matrx_ai.configure() with real DB bases. Import at call time so
    # `import matrx_ai.db.conversation_gate` (and everything that transitively
    # reaches it: executor, providers, catalog) works in an unconfigured or
    # client-host environment — config errors at CALL time, never import time.
    from matrx_ai.db.cx_managers import cxm

    return cxm


# Lazy access to persistence.queue_helpers — breaks the matrx_ai.persistence
# ↔ matrx_ai.db circular import (queue_helpers transitively imports through
# orchestrator → db). Defined at module level as module functions that
# import-then-call on first invocation; subsequent calls are cheap.


def _get_coordinator():
    from matrx_ai.persistence.queue_helpers import get_coordinator as _gc

    return _gc()


def _get_active_lane_coordinator():
    """Return request ownership only while its lane can still finalize writes.

    A coroutine scheduled inside a request can begin after its copied
    ``RequestLane`` has drained.  Materializing a coordinator in that stale
    scope creates a terminal, one-shot owner and records
    ``persistence_after_lane_drain``.  Conversation creation is an awaited
    durability boundary, so a terminal inherited lane is not ownership at all:
    its caller must take the existing governed direct-write branch instead.
    """
    from matrx_connect.lane import get_current_lane

    lane = get_current_lane()
    if lane is not None and getattr(lane, "phase", None) != "active":
        return None
    return _get_coordinator()


def _queue_conversation_create(**kwargs):
    from matrx_ai.persistence.queue_helpers import (
        queue_conversation_create as _qcc,
    )

    return _qcc(**kwargs)


def _queue_conversation_update(conv_id, **kwargs):
    from matrx_ai.persistence.queue_helpers import (
        queue_conversation_update as _qcu,
    )

    return _qcu(conv_id, **kwargs)


def _queue_user_request_create(**kwargs):
    from matrx_ai.persistence.queue_helpers import (
        queue_user_request_create as _qurc,
    )

    return _qurc(**kwargs)


def _queue_user_request_update(req_id, **kwargs):
    from matrx_ai.persistence.queue_helpers import (
        queue_user_request_update as _quru,
    )

    return _quru(req_id, **kwargs)


class ConversationGateError(Exception):
    pass


class ConversationRunInFlightError(ConversationGateError):
    """A start is already in flight on this conversation id.

    A SUBCLASS on purpose: every existing ``except ConversationGateError``
    keeps working. Callers that can tell the difference map this to the
    retryable ``run_in_flight`` 409 instead of the terminal duplicate-key one —
    the id is not taken forever, it is busy for a moment.
    """


def _is_valid_uuid(value: str | None) -> bool:
    if not value:
        return False
    try:
        UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def _require_valid_user_id(user_id: str | None, context: str = "") -> str:
    if _is_valid_uuid(user_id):
        return user_id  # type: ignore[return-value]
    label = f" ({context})" if context else ""
    raise ConversationGateError(
        f"Invalid user_id{label}: {user_id!r} — "
        f"a valid UUID is required. Guest users are assigned a UUID via "
        f"guest_executions at the middleware layer before reaching this point."
    )


def _stamp_agent_refs(
    create_kwargs: dict[str, Any],
    ctx: Any,
    *,
    id_key: str,
    version_key: str,
) -> None:
    """Stamp the request's agent attribution onto an outgoing INSERT — but only
    when each id is a real UUID.

    Defense-in-depth (Layer 2) behind the route-boundary ``require_uuid`` guard
    (``aidream/api/utils/identifiers.py``). A malformed id that slips past the
    boundary — historically matrx-frontend's memory-only ``cmp-<uuid>``
    synthetic agent ids from the agent-comparison feature — is DROPPED with a
    loud warning rather than written into a Postgres UUID column. Rationale:
    ``agent_id`` is optional attribution; losing it is recoverable. Letting it
    poison the INSERT is not — it raised asyncpg ``22P02``, cascaded into FK
    violations on every child row, and tripped the ``PersistenceBarrierError``
    data-loss stop. Data first: keep the conversation/request, drop the bad tag.
    """
    if not ctx:
        return
    for attr, key in (("agent_id", id_key), ("agent_version_id", version_key)):
        value = getattr(ctx, attr, None)
        if not value:
            continue
        if _is_valid_uuid(value):
            create_kwargs[key] = value
        else:
            vcprint(
                "\n"
                "================================================================\n"
                "  matrx-ai — conversation_gate._stamp_agent_refs (validation gate)\n"
                "----------------------------------------------------------------\n"
                "  My job: keep malformed identifiers out of cx_* UUID columns.\n"
                f"  Caught: ctx.{attr}={value!r} is NOT a valid UUID.\n"
                f"  Action: DROPPED the '{key}' attribution from this write so the\n"
                "          row still persists (data first). The conversation/request\n"
                "          is saved WITHOUT agent attribution.\n"
                "  Likely cause: a memory-only / synthetic client id (e.g. `cmp-…`)\n"
                "          reached an AI-executing endpoint. The route boundary\n"
                "          (require_uuid) should have rejected it with a 422 — if it\n"
                "          got here, an internal caller bypassed the boundary.\n"
                "================================================================",
                color="red",
            )


def _resolve_conversation_type(ctx: Any, parent_conversation_id: str | None = None) -> str:
    """Resolve the conversation_type to stamp on a cx_conversation INSERT.

    Trusts an explicitly-set ``ctx.conversation_type`` (the fork / scheduler /
    pipeline sites set it), and otherwise re-derives from the
    ``is_internal_agent`` / ``source_feature`` / parent-lineage signals so an
    internal run is never silently written as ``standard``. Returns ``standard``
    when there is no context at all.
    """
    if not ctx:
        return derive_conversation_type(
            explicit=None,
            parent_conversation_id=parent_conversation_id,
        )
    return derive_conversation_type(
        explicit=getattr(ctx, "conversation_type", None),
        is_internal_agent=bool(getattr(ctx, "is_internal_agent", False)),
        source_feature=getattr(ctx, "source_feature", None),
        parent_conversation_id=parent_conversation_id
        or getattr(ctx, "parent_conversation_id", None),
    )


def _stamp_origin(
    create_kwargs: dict[str, Any],
    ctx: Any,
    *,
    with_witness: bool,
) -> None:
    """Stamp the reconciled origin_class (+ witness on cx_user_request rows).

    Runs the ONE trust reconciliation: matrx_connect.reconcile_origin rebuilds
    the class from platform-witnessed facts and overrules any claim the facts
    don't support (screaming + preserving the claim as evidence in the witness).
    Never raises — attribution must never cost a paid write.
    """
    try:
        from matrx_connect import reconcile_origin

        origin_class, witness = reconcile_origin(ctx)
    except Exception as exc:  # noqa: BLE001 — data first, provenance second
        vcprint(
            f"[ConversationGate] origin reconciliation failed ({exc}) — "
            "stamping origin_class='system' with an error witness",
            color="red",
        )
        origin_class = "system"
        witness = {"contradictions": [f"reconcile_origin raised: {exc}"]}
    create_kwargs["origin_class"] = origin_class
    if with_witness:
        create_kwargs["origin_witness"] = witness


_AUTO_TITLE_PREFIX = "Auto: "

# source_feature → sidebar label. Never use bare "Chat" — the labeler replaces
# these placeholders after the first turn, but many rows keep the initial title
# when labeling fails or is skipped.
_SOURCE_FEATURE_TITLE_LABELS: dict[str, str] = {
    "chat": "New conversation",
    "manual": "Manual chat",
    "agent": "Agent run",
    "conversation": "Conversation",
    "conversation_resume": "Conversation",
    "fork_and_run": "Fork",
    "prompt": "Prompt",
    "agent_blocks": "Agent blocks",
    "workflow_run": "Workflow run",
    "workflow_node_test": "Workflow node test",
    "workflow_worker": "Workflow worker",
    "server-run": "Scheduled run",
    "socket_compat": "Legacy socket",
    "auto_ingest_ner": "Auto ingest",
    "ner": "Auto ingest NER",
    "podcasts": "Podcast pipeline",
    "web_research": "Web research",
    "rag": "RAG pipeline",
    "pdf-cleaner": "PDF cleaner",
    "content_processing_upload_hook": "Content processing",
    "kg_clustering_namer": "KG clustering",
}


def _humanize_source_feature(source_feature: str) -> str:
    mapped = _SOURCE_FEATURE_TITLE_LABELS.get(source_feature)
    if mapped:
        return mapped
    return source_feature.replace("_", " ").replace("-", " ").strip().title()


def _strip_auto_title_prefix(title: str) -> str:
    stripped = title.strip()
    if stripped.upper().startswith("AUTO:"):
        return stripped.split(":", 1)[1].strip()
    if stripped.startswith("Auto:"):
        return stripped.split(":", 1)[1].strip()
    return stripped


def compact_step_label(label: str) -> str:
    """Drop redundant pipeline wording before persisting an auto title."""
    step = _strip_auto_title_prefix(label)
    if step.lower().startswith("generate "):
        step = step[9:].strip()
    _SHORT_LABELS: dict[str, str] = {
        "Produce Podcast Audio": "Podcast Audio",
        "Write Podcast Script": "Podcast Script",
        "Design Podcast Title & Visuals": "Podcast Metadata",
        "Research Podcast Content": "Podcast Research",
        "Extract Podcast Source Content": "Podcast Extraction",
        "Summarize Research Page": "Page Summary",
        "Suggest Research Setup": "Research Setup",
        "Synthesize Keyword Findings": "Keyword Synthesis",
        "Update Keyword Synthesis": "Keyword Update",
        "Generate Research Report": "Research Report",
        "Update Research Report": "Report Update",
        "Consolidate Tag Findings": "Tag Consolidation",
        "Suggest Page Tags": "Page Tags",
        "Assemble Research Document": "Research Document",
        "Clean RAG PDF Page": "RAG PDF Cleanup",
        "Contextualize RAG Chunk": "RAG Chunk Context",
        "Expand RAG Query": "RAG Query Expand",
        "Generate RAG HyDE Document": "RAG HyDE",
        "Clean PDF Extracted Text": "PDF Cleanup",
        "Orient Document for NER": "NER Orient",
        "Review NER Suggestions": "NER Review",
        "Propose New Scopes": "New Scopes",
        "Canonicalize NER Entities": "NER Canonicalize",
    }
    if step.startswith("Generate Podcast Image "):
        return step.replace("Generate Podcast Image ", "Podcast Image ", 1)
    if step.startswith("Generate Podcast Video "):
        return step.replace("Generate Podcast Video ", "Podcast Video ", 1)
    if step.startswith("Fill Scope Slots ("):
        return step.replace("Fill Scope Slots (", "Scope Slots (", 1)
    if step.startswith("Extract Deep Chunk Entities ("):
        return step.replace("Extract Deep Chunk Entities (", "Chunk Entities (", 1)
    if step.startswith("Extract Chunk Entities ("):
        return step
    if step.startswith("Propose Context Items ("):
        return step.replace("Propose Context Items (", "Context Items (", 1)
    if step.startswith("Detect Magic Moments ("):
        return step.replace("Detect Magic Moments (", "Magic Moments (", 1)
    if step.startswith("Canonicalize Entity Batch ("):
        return step.replace("Canonicalize Entity Batch (", "Entity Batch (", 1)
    if step.startswith("Mine Context Values ("):
        return step.replace("Mine Context Values (", "Mine Values (", 1)
    if step.startswith("Refine Scope Suggestions ("):
        return step.replace("Refine Scope Suggestions (", "Refine Scopes (", 1)
    if step.startswith("Discover Scope Suggestions ("):
        return step.replace("Discover Scope Suggestions (", "Discover Scopes (", 1)
    return _SHORT_LABELS.get(step, step)


def _format_auto_title(label: str) -> str:
    step = compact_step_label(label)
    if not step:
        return f"{_AUTO_TITLE_PREFIX}Conversation"
    return f"{_AUTO_TITLE_PREFIX}{step}"


def _format_initial_title(label: str, ctx: Any) -> str:
    """Reserve ``Auto:`` for work not initiated by a person."""
    step = compact_step_label(label) or "Conversation"
    if ctx is not None and getattr(ctx, "origin_class", "") == "human":
        return step
    return _format_auto_title(step)


def has_auto_title_prefix(title: str | None) -> bool:
    if not title:
        return False
    stripped = str(title).strip()
    return stripped.upper().startswith("AUTO:") or stripped.startswith("Auto:")


CONVERSATION_STEP_LABEL_KEY = "conversation_step_label"


def resolve_step_label_for_title(label: str, agent_display_name: str | None = None) -> str:
    """Map a ``run_agent`` / ``child_agent_context`` label to a sidebar title.

    Callers pass either a human-facing string (preferred for orchestrated
    pipelines) or a short technical slug. When the slug is opaque, the loaded
    agent's display name wins so text agents show up under their DB name.
    """
    stripped = (label or "").strip()
    agent = (agent_display_name or "").strip()

    if not stripped:
        return agent or "Sub-agent"

    if " " in stripped:
        return stripped

    if ":" in stripped:
        if agent:
            return agent
        tail = stripped.rsplit(":", 1)[-1]
        return tail.replace("_", " ").replace("-", " ").strip().title()

    if agent:
        return agent

    return stripped.replace("_", " ").replace("-", " ").strip().title()


def _resolve_initial_conversation_title(
    *,
    title: str | None,
    ctx: Any,
) -> str:
    if title:
        return title

    if not ctx:
        return _format_auto_title("Conversation")

    step_label = ctx.metadata.get(CONVERSATION_STEP_LABEL_KEY) if ctx.metadata else None
    if isinstance(step_label, str) and step_label.strip():
        return _format_initial_title(step_label.strip(), ctx)

    agent_name = ctx.metadata.get("agent_name") if ctx.metadata else None
    if isinstance(agent_name, str) and agent_name.strip():
        return _format_initial_title(agent_name.strip(), ctx)

    if ctx.source_feature:
        return _format_initial_title(_humanize_source_feature(ctx.source_feature), ctx)

    return _format_initial_title("Conversation", ctx)


async def resolve_parent_conversation_lineage(
    parent_conversation_id: str | None,
    child_conversation_id: str,
) -> str | None:
    """Return ``parent_conversation_id`` only when its row exists on disk.

    ``parent_conversation_id`` (and its sibling ``forked_from_id``) is a
    nullable, self-referential FK on ``cx_conversation`` that carries fork /
    sub-agent **lineage** — pure provenance metadata. It is NOT a row the
    child depends on for correctness.

    Stamping a parent that isn't present in ``cx_conversation`` FK-violates
    the child INSERT (``cx_conversation_parent_conversation_id_fkey``) and
    sends the ENTIRE child conversation to ``system_write_failure`` — a far
    worse outcome than dropping a lineage tag. This mirrors
    :func:`_stamp_agent_refs`: an optional attribution column must never be
    allowed to poison the write that carries it.

    The check runs against committed DB state, so a parent that is merely
    *queued-but-not-yet-flushed* in another coordinator scope (e.g. a
    sub-agent spawned on a brand-new conversation's first turn) reads as
    absent and degrades to NULL — identical to the outcome the row would have
    had anyway (the child landed before the parent flushed), but without the
    FK violation and the lost write. Data first.

    Returns the verified parent id, or ``None`` (drop the lineage) when it
    isn't present or can't be confirmed.
    """
    if not _is_valid_uuid(parent_conversation_id):
        return None
    try:
        rows = await _cxm().conversation.filter_conversations(
            id=parent_conversation_id,
        )
    except Exception as exc:
        # A read failure here must NOT block the child write. Fail toward
        # NULL (drop the lineage) — losing provenance is recoverable; losing
        # the conversation is not.
        vcprint(
            f"[ConversationGate] parent-lineage existence check raised "
            f"({type(exc).__name__}: {exc}); dropping parent_conversation_id "
            f"{parent_conversation_id!r} from {child_conversation_id} to keep "
            f"the write safe.",
            color="yellow",
        )
        return None
    if rows:
        return parent_conversation_id
    vcprint(
        "\n"
        "================================================================\n"
        "  matrx-ai — conversation_gate.resolve_parent_conversation_lineage\n"
        "  (parent-lineage validation gate)\n"
        "----------------------------------------------------------------\n"
        "  My job: keep a child cx_conversation INSERT from FK-violating on a\n"
        "          parent_conversation_id that has no row on disk.\n"
        f"  Caught: parent_conversation_id={parent_conversation_id!r} is a valid\n"
        "          UUID but is NOT present in cx_conversation.\n"
        f"  Action: DROPPED the parent lineage tag from conversation\n"
        f"          {child_conversation_id} so the row still persists (data first).\n"
        "          The FK violation would otherwise lose the whole conversation\n"
        "          to system_write_failure.\n"
        "  Likely cause: a sub-agent forked from a conversation that was never\n"
        "          persisted (out-of-band / test parent), or the parent's own\n"
        "          write hasn't landed yet in a separate coordinator scope.\n"
        "================================================================",
        color="red",
    )
    return None


# =========================================================================
# Core operations
# =========================================================================


# --------------------------------------------------------------------------- #
# Re-attempting a start: adopting an UNSTARTED conversation
#
# THE RULE
#   ``is_new=true`` on an id that already exists is a conflict ONLY IF that
#   conversation has actually STARTED. A row that the caller owns and that has
#   never carried a turn is not a collision — it is the same creation, tried
#   again — so it is ADOPTED and the request proceeds.
#
# WHY IT IS SHAPED THIS WAY
#   The conversation row is published BEFORE the stream opens (a deliberate
#   durability boundary — see ``create_new_conversation``). Anything that kills
#   the request after that point leaves a shell behind, and the client, which
#   minted the id and keys its entire local state by it, can never use that id
#   again. On 2026-08-30 that surfaced as a user being told "conversation
#   already exists" about a conversation he had never had; a census that day
#   found 1,297 such shells in 30 days (10% of all conversations created).
#
#   The failure list is unbounded — a pre-stream validation error, a client
#   disconnect, a provider error, an OOM, a deploy mid-request, a closed laptop.
#   Enumerating it and teaching each path to clean up is a game that can only be
#   lost, and every new endpoint re-opens it.
#
#   So this does not test HISTORY, it tests a PRECONDITION. "Has this
#   conversation started?" is a positive fact about the row that every one of
#   those failures leaves in the identical state, which makes the rule
#   failure-path-agnostic by construction. There is nothing to enumerate.
#
# WHY IT IS SAFE
#   * Another user's id is never adopted (``created_by`` must match) — an
#     unowned id keeps returning the same conflict it always did.
#   * A started conversation is never adopted, so no message, request, cost or
#     ordering is ever rewritten. Nothing is lost because nothing exists yet.
#   * Adoption is a single-row compare-and-swap on ``version``. N racing
#     double-submits produce exactly ONE adopter; the losers get the ordinary
#     409. The primary key used to be doing that job by accident; now a real
#     lock does it on purpose.
# --------------------------------------------------------------------------- #

#: Written on the conversation at creation and cleared when the start attempt
#: fails or the turn records its own status. While it stands and is FRESH, a
#: run owns this id and nobody may adopt it.
CONVERSATION_START_CLAIM_STATUS = "pending"

#: How long an unreleased claim keeps an id. Deliberate failures RELEASE the
#: claim (see ``release_conversation_start_claim``), so this bound only governs
#: the cases nobody can clean up after — a crash, a kill, a dropped connection.
#: Long enough that a slow prep is never mistaken for a corpse.
CONVERSATION_START_CLAIM_STALE_SECONDS = 900

#: Adoption REFUSES rather than clearing these. Each is state a fresh create
#: could never produce, so re-stamping would not yield "a brand-new
#: conversation" — it would yield a hybrid.
#:
#: * ``system_instruction`` — ``chat.reject_system_instruction_mutation()``
#:   makes it immutable once set, so it CANNOT be cleared. An adopted shell
#:   would run every turn under a dead attempt's frozen system prompt.
#: * ``parent_conversation_id`` / ``forked_from_id`` — lineage. Adopting one
#:   silently makes the new conversation a child of an unrelated parent.
#: * ``deleted_at`` — the row is in the trash. A brand-new conversation must
#:   not be born invisible; mint a fresh id instead.
_ADOPTION_BLOCKING_COLUMNS: tuple[str, ...] = (
    "system_instruction",
    "parent_conversation_id",
    "deleted_at",
)

#: Reset to a fresh row's value on adoption even though a create never sets them
#: — carrying a dead attempt's value here is how an adopted conversation stops
#: being equivalent to a new one. Adoption's rule is: match a fresh create, or
#: refuse. A column that is neither re-stamped from ``create_kwargs``, listed
#: here, nor blocking above is identity (``id``/``created_by``/``created_at``).
_ADOPTION_RESET_TO_DEFAULT: dict[str, Any] = {
    "last_model_id": None,
    "last_request_status": None,
    "last_request_id": None,
    "last_context_breakdown": None,
    "description": None,
    "keywords": None,
    "task_id": None,
    "cache_state": {},
    "sandbox_instance_id": None,
    "app_instance_id": None,
    "is_favorite": False,
    "exclude_from_kg": False,
    "forked_from_id": None,
    "forked_at_position": None,
}


#: The conversation THIS request created, if any. Set the moment the row is
#: published; read by the release helper so a caller can hand the id back
#: without threading the id through every frame between here and the failure.
_pending_start_claim: ContextVar[tuple[str, str] | None] = ContextVar(
    "matrx_ai_pending_conversation_start_claim", default=None
)


def _record_start_claim(conversation_id: str, user_id: str) -> None:
    _pending_start_claim.set((str(conversation_id), str(user_id)))


async def release_pending_start_claim() -> None:
    """Release the claim on whatever conversation THIS request created.

    A no-op when the request created nothing (a continue turn, an ephemeral
    run, or a start that never got that far), so callers can invoke it on any
    failure path without first working out whether it applies.
    """
    claim = _pending_start_claim.get()
    if claim is None:
        return
    _pending_start_claim.set(None)
    await release_conversation_start_claim(claim[0], claim[1])


async def release_conversation_start_claim(conversation_id: str, user_id: str) -> None:
    """Give the id back after a start attempt fails before the stream opens.

    The claim exists so a concurrent double-submit cannot adopt a conversation
    whose run is still alive. A DELIBERATE failure — a rejected attachment, a
    failed validation, an unresolvable scope — knows the run is dead, so it
    hands the id straight back and the person's very next retry adopts it with
    no wait. The staleness bound is only for the failures that cannot say so.

    Never raises: a failure to release costs a retry delay, never the request.
    """
    if not conversation_id or not user_id:
        return
    try:
        from matrx_orm import (
            COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
            Session,
            allow_direct_coordinator_write,
        )

        with allow_direct_coordinator_write(
            _cxm().conversation.model,
            reason="releasing a conversation start claim after a pre-stream failure",
            acknowledgement=COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
        ):
            async with Session():
                await _cxm().conversation.update_where(
                    {
                        "id": conversation_id,
                        "created_by": str(user_id),
                        "message_count": 0,
                        "last_request_status": CONVERSATION_START_CLAIM_STATUS,
                    },
                    last_request_status=None,
                )
    except Exception as exc:  # noqa: BLE001 — best effort by design
        vcprint(
            f"[ConversationGate] Could not release the start claim on "
            f"{conversation_id} ({exc}). The id frees itself after "
            f"{CONVERSATION_START_CLAIM_STALE_SECONDS}s.",
            color="yellow",
        )


def _start_claim_is_live(existing: Any) -> bool:
    """Is another request still holding this id?

    True when the claim stands AND is fresh. A stale claim is a corpse — the
    request that wrote it died without releasing — and must not keep the id
    forever, which is the whole failure this system exists to end.
    """
    status = str(getattr(existing, "last_request_status", "") or "")
    if status != CONVERSATION_START_CLAIM_STATUS:
        return False

    from datetime import UTC, datetime, timedelta

    stamped = getattr(existing, "updated_at", None) or getattr(existing, "created_at", None)
    if stamped is None:
        return True  # cannot age it => treat the claim as live (fail closed)
    try:
        age = datetime.now(UTC) - stamped
    except TypeError:  # naive datetime
        return True
    return age < timedelta(seconds=CONVERSATION_START_CLAIM_STALE_SECONDS)


#: What a re-attempted start may re-stamp on the shell it adopts. These are all
#: start-state: what the caller declared when opening the conversation, none of
#: it derived from a turn that never ran.
#:
#: ``organization_id`` is deliberately here. An UNSTARTED conversation's
#: organization is still the caller's to choose — that is precisely the case
#: that produced the incident (the first attempt stamped one org and died; the
#: retry must be free to name another). The moment a turn lands, the row's
#: organization freezes forever, which is also what the frontend enforces
#: (``requireExecutionOrganizationId``: mutable while ``cacheOnly``, frozen once
#: persisted). One rule, both halves of the stack.
_ADOPTABLE_START_FIELDS: tuple[str, ...] = (
    "title",
    "config",
    "metadata",
    "variables",
    "overrides",
    "source_app",
    "source_feature",
    "is_ephemeral",
    "conversation_type",
    "organization_id",
    "initial_agent_id",
    "initial_agent_version_id",
    "origin_class",
    "origin_witness",
    "forked_from_id",
    "forked_at_position",
)


async def _conversation_has_started(existing: Any, conversation_id: str) -> bool:
    """Has a turn ever landed on this conversation?

    Two independent signals, either one sufficient, because a false NEGATIVE
    here would let a real conversation be re-stamped:

    1. ``message_count`` on the row — the cheap denormalized counter.
    2. An actual ``chat.message`` read — the truth, consulted whenever the
       counter says zero, so counter drift can never make a live conversation
       look adoptable.

    A read failure counts as STARTED (fail closed): if we cannot prove the
    conversation is empty, we refuse to adopt it and the caller gets the same
    conflict it would have received before.
    """
    try:
        if int(getattr(existing, "message_count", 0) or 0) > 0:
            return True
    except (TypeError, ValueError):
        return True

    try:
        messages = await _cxm().message.filter_messages_by_conversation_id(conversation_id)
    except Exception as exc:  # noqa: BLE001 — cannot prove empty => not adoptable
        vcprint(
            f"[ConversationGate] Could not verify emptiness of {conversation_id} "
            f"({exc}) — treating it as STARTED and refusing adoption (fail closed).",
            color="yellow",
        )
        return True
    return bool(messages)


async def _adopt_unstarted_conversation(
    existing: Any,
    conversation_id: str,
    user_id: str,
    create_kwargs: dict[str, Any],
) -> None:
    """Re-stamp an unstarted shell as this request's brand-new conversation.

    Raises :class:`ConversationGateError` — carrying the words the router maps to
    a 409 — when the id is genuinely taken: owned by somebody else, already
    started, or lost the compare-and-swap to a concurrent adopter.
    """
    owner = str(getattr(existing, "created_by", "") or "")
    if owner and owner != str(user_id):
        raise ConversationGateError(
            f"Failed to create conversation {conversation_id}: duplicate key — "
            f"a conversation with this id already exists and belongs to another user"
        )

    if await _conversation_has_started(existing, conversation_id):
        raise ConversationGateError(
            f"Failed to create conversation {conversation_id}: duplicate key — "
            f"a conversation with this id already exists and has already started"
        )

    if _start_claim_is_live(existing):
        # A run already owns this id and is still alive. This is the
        # double-submit case; the caller maps it to the RETRYABLE run_in_flight
        # 409, which the client backs off on rather than showing as an error.
        raise ConversationRunInFlightError(
            f"conversation {conversation_id} is claimed by a start already in flight"
        )

    blocking = [
        column
        for column in _ADOPTION_BLOCKING_COLUMNS
        if getattr(existing, column, None) is not None
    ]
    if blocking:
        # Cannot be made equivalent to a fresh create — refuse rather than
        # produce a hybrid. See _ADOPTION_BLOCKING_COLUMNS.
        raise ConversationGateError(
            f"Failed to create conversation {conversation_id}: duplicate key — "
            f"a conversation with this id already exists and carries state a new "
            f"conversation cannot have ({', '.join(blocking)})"
        )

    # An adopted conversation must be INDISTINGUISHABLE from a freshly created
    # one. Start from the fresh-create defaults for everything a create does not
    # set, then lay this request's start-state over the top — so a column nobody
    # thought about gets RESET (safe) rather than carried (a dead attempt's data
    # leaking into a live conversation).
    updates: dict[str, Any] = dict(_ADOPTION_RESET_TO_DEFAULT)
    updates.update(
        {
            field: create_kwargs[field]
            for field in _ADOPTABLE_START_FIELDS
            if field in create_kwargs
        }
    )
    # ``status`` is reset so a shell abandoned in a terminal state starts clean.
    updates["status"] = create_kwargs.get("status", "active")
    updates["message_count"] = 0
    # This request now owns the id.
    updates["last_request_status"] = CONVERSATION_START_CLAIM_STATUS
    if create_kwargs.get("last_request_id"):
        updates["last_request_id"] = create_kwargs["last_request_id"]

    current_version = getattr(existing, "version", None)
    scope = {"id": conversation_id, "created_by": str(user_id), "message_count": 0}

    # Governed like the sibling create: adoption is an AWAITED durability
    # boundary that must land before the stream opens, not turn persistence, so
    # it declares the same intentional Coordinator bypass the out-of-lane create
    # path declares — and for the same reason (the row must be committed and
    # strictly error-checked before anything downstream assumes it).
    from matrx_orm import (
        COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
        Session,
        allow_direct_coordinator_write,
    )

    try:
        with allow_direct_coordinator_write(
            _cxm().conversation.model,
            reason=(
                "pre-stream adoption of an unstarted conversation — a "
                "compare-and-swap that must be awaited and strictly checked "
                "before the stream opens"
            ),
            acknowledgement=COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
        ):
            async with Session():
                if current_version is None:
                    # Version-less row (older data / a host without the column):
                    # fall back to a narrowed conditional update. Still owner-
                    # and emptiness-scoped; just without the concurrent-adopter
                    # tiebreak.
                    result = await _cxm().conversation.update_where(scope, **updates)
                    if getattr(result, "rows_affected", 0) == 0:
                        raise ConversationGateError(
                            f"Failed to create conversation {conversation_id}: "
                            f"duplicate key — a conversation with this id already "
                            f"exists and could not be adopted"
                        )
                else:
                    await _cxm().conversation.update_where(
                        scope, expected_version=int(current_version), **updates
                    )
    except ConversationGateError:
        raise
    except Exception as exc:
        # OptimisticLockError / DoesNotExist => somebody else got there first,
        # or the row started between our check and our write. Either way this id
        # is taken NOW, which is the ordinary 409 the client already understands.
        raise ConversationGateError(
            f"Failed to create conversation {conversation_id}: duplicate key — "
            f"a conversation with this id already exists (lost the adoption race: {exc})"
        ) from exc

    mark_conversation_known(conversation_id, scope=_ENSURED_DURABLE)
    _record_start_claim(conversation_id, str(user_id))
    vcprint(
        f"[ConversationGate] Adopted unstarted conversation {conversation_id} "
        f"for a re-attempted start (no turn had landed on it).",
        color="green",
    )


async def create_new_conversation(
    conversation_id: str,
    user_id: str,
    metadata: dict[str, Any] | None = None,
    forked_from_id: str | None = None,
    forked_at_position: int | None = None,
    title: str | None = None,
) -> None:
    """INSERT a cx_conversation row with the given client-generated ID.

    Reads ``initial_variables`` and ``initial_overrides`` from the current
    AppContext (set by agent/chat routes via ctx.extend()) so they are
    written on creation without callers needing to pass them explicitly.

    ``forked_from_id`` / ``forked_at_position`` populate the fork lineage
    fields on ``cx_conversation`` — used by the fork endpoint to record
    which conversation a new row branched from and at what message
    position. Both are optional; non-fork calls omit them entirely.

    ``title`` overrides the default agent-name / source-feature derived
    title when the caller already knows what to write (e.g. a fork
    wanting to copy the source conversation's title).

    An id that ALREADY EXISTS is not automatically a failure: when the row is
    the caller's own and no turn has ever landed on it, this is the same
    creation re-attempted (its first try died before the stream opened), so the
    shell is ADOPTED — re-stamped with this request's start-state, including its
    organization — and the call succeeds. See "Re-attempting a start" above for
    why the test is the row's STATE rather than the reason the first attempt
    failed. A started conversation, or one owned by another user, still raises.

    Raises ``ConversationGateError`` on any failure (duplicate PK, FK
    violation, network error, etc.).
    """
    if not _is_valid_uuid(conversation_id):
        raise ConversationGateError(f"conversation_id is not a valid UUID: {conversation_id!r}")

    safe_user_id = _require_valid_user_id(user_id, "create_new_conversation")

    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()

    # Client host: the store owns conversation creation — same dispatch the
    # sibling gate paths (ensure_conversation_exists, create_pending_user_request)
    # already do. The ORM path below must never run without Postgres.
    from matrx_ai.client_host import get_conversation_store

    store = get_conversation_store()
    if store is not None:
        if title or metadata or forked_from_id or forked_at_position is not None:
            vcprint(
                {
                    "conversation_id": conversation_id,
                    "title": title,
                    "metadata_keys": sorted(metadata) if metadata else [],
                    "forked_from_id": forked_from_id,
                    "forked_at_position": forked_at_position,
                },
                "[ConversationGate] store path: ConversationStore protocol has no "
                "title/metadata/fork-lineage fields yet — these values are NOT "
                "persisted on the client host (protocol v2 gap).",
                color="yellow",
            )
        try:
            await store.ensure_conversation_exists(
                conversation_id,
                safe_user_id,
                variables=dict(ctx.initial_variables) if ctx else {},
                overrides=dict(ctx.initial_overrides) if ctx else {},
            )
        except Exception as exc:
            raise ConversationGateError(
                f"conversation_store.ensure_conversation_exists failed for {conversation_id}: {exc}"
            ) from exc
        return

    resolved_title = _resolve_initial_conversation_title(title=title, ctx=ctx)

    # Seed the JSONB config blob with the agent's default model when the
    # caller has stashed it under ctx.metadata["initial_model"]. This makes
    # the row self-rescuing: even if the very first turn fails before
    # persistence.py runs (gaierror, OOM, client disconnect, etc.), a
    # subsequent continue-mode load will still find a usable model in
    # config["model"] thanks to the defensive read in
    # cx_managers.get_conversation_unified_config. Only the agent flow
    # populates this today (see prepare_agent_run); other callers omit it
    # and get the prior {} behavior.
    initial_model: str | None = ctx.metadata.get("initial_model") if ctx else None
    initial_config: dict[str, Any] = {"model": initial_model} if initial_model else {}

    create_kwargs: dict[str, Any] = {
        "id": conversation_id,
        "created_by": safe_user_id,
        "status": "active",
        "message_count": 0,
        "config": initial_config,
        "title": resolved_title,
        "metadata": metadata or {},
        "variables": ctx.initial_variables if ctx else {},
        "overrides": ctx.initial_overrides if ctx else {},
        "source_app": ctx.source_app if ctx else "",
        "source_feature": ctx.source_feature if ctx else "",
        "is_ephemeral": not ctx.store if ctx else False,
        "conversation_type": _resolve_conversation_type(ctx),
    }
    # THE START CLAIM. Committed with the row itself, so a second request
    # arriving milliseconds later can SEE that a run already owns this id.
    #
    # Without it, adoption had a hole big enough to drive a double-click
    # through: request A publishes the conversation before the stream opens and
    # then spends the whole turn in prep (its messages land in ONE transaction
    # at end-of-stream), so for seconds there is no committed evidence A exists.
    # B would find an "unstarted" conversation, adopt it, re-stamp its
    # organization, and run a second loop on the same row — interleaving message
    # positions and, because chat.message inherits org from its parent, landing
    # A's messages in B's organization.
    #
    # The turn-admission lock cannot cover this: it looks for a live run in
    # runtime.global_execution / chat.request, and neither exists yet during
    # prep. This claim does, because it is written in the same commit as the row.
    if ctx is not None and getattr(ctx, "request_id", ""):
        create_kwargs["last_request_id"] = str(ctx.request_id)
    create_kwargs["last_request_status"] = CONVERSATION_START_CLAIM_STATUS
    _stamp_origin(create_kwargs, ctx, with_witness=False)
    _stamp_agent_refs(
        create_kwargs,
        ctx,
        id_key="initial_agent_id",
        version_key="initial_agent_version_id",
    )
    stamp_org_id(create_kwargs, getattr(ctx, "organization_id", None))
    if forked_from_id is not None:
        create_kwargs["forked_from_id"] = forked_from_id
    if forked_at_position is not None:
        create_kwargs["forked_at_position"] = forked_at_position

    # KD-1 Phase 2 — in-lane path: the route opened the RequestLane at entry,
    # so a Coordinator is available BEFORE the conversation is created. Use a
    # pending-aware existence SELECT + a queued INSERT:
    #   * `filter_conversations(id=...)` runs through the QueryBuilder's
    #     pending-read merge (`pending_ops_across_stack`), so a duplicate
    #     client-supplied id — already committed OR queued earlier in this same
    #     request — still raises ConversationGateError synchronously here (the
    #     router maps "already exists" → 409). Server-minted UUIDs can't
    #     collide, so the queue is safe for them by construction. (A true
    #     cross-request race on the same client-supplied id is caught by the
    #     PK constraint at flush and lands in system_write_failure — loud,
    #     never silent.)
    #   * The INSERT is synchronously published before the stream opens. A
    #     first-turn inbox/cancel/attachment request is a DIFFERENT request and
    #     cannot see this request's pending-read overlay. Deferring the row to
    #     end-of-stream therefore made queue-while-streaming fail with 404 on
    #     /chat/new. This is a deliberate durability boundary, not a hot-loop
    #     commit; the Coordinator rolls a fresh Session for the turn writes.
    coordinator = _get_active_lane_coordinator()
    if coordinator is not None:
        try:
            existing = await _cxm().conversation.filter_conversations(id=conversation_id)
        except Exception as exc:
            raise ConversationGateError(
                f"Failed to create conversation {conversation_id}: existence check failed: {exc}"
            ) from exc
        if existing:
            # NOT automatically a conflict — see "Re-attempting a start" above.
            # An unstarted shell the caller owns is the SAME creation retried;
            # adopt it and proceed. Anything else raises the ordinary 409.
            await _adopt_unstarted_conversation(
                existing[0], conversation_id, safe_user_id, create_kwargs
            )
            return
        coordinator.set_correlation(
            user_id=safe_user_id,
            conversation_id=conversation_id,
        )
        _queue_conversation_create(**create_kwargs)
        try:
            await coordinator.finalize(reason="conversation_start")
        except Exception as exc:
            raise ConversationGateError(
                f"Failed to publish conversation {conversation_id} before streaming: {exc}"
            ) from exc
        mark_conversation_known(conversation_id, scope=_ENSURED_DURABLE)
        _record_start_claim(conversation_id, safe_user_id)
        vcprint(
            f"[ConversationGate] Published conversation before streaming: {conversation_id}",
            color="green",
        )
        return

    # Out-of-lane path (fork gate detached task, dry_run, workflows, scripts):
    # this caller expects strict error semantics (the fork gate fatal_errors
    # the request when the INSERT fails). Keep it awaited so the existing
    # _on_gate_done flow still works — low-traffic paths where the blocking
    # write cost is irrelevant.
    #
    # Adoption applies here too: the rule is about the STATE of the row, not
    # about which code path is asking, so both doors must agree. A retried
    # workflow/fork start on an id whose first attempt died gets the same
    # second chance a chat turn gets.
    try:
        existing_rows = await _cxm().conversation.filter_conversations(id=conversation_id)
    except Exception as exc:
        raise ConversationGateError(
            f"Failed to create conversation {conversation_id}: existence check failed: {exc}"
        ) from exc
    if existing_rows:
        await _adopt_unstarted_conversation(
            existing_rows[0], conversation_id, safe_user_id, create_kwargs
        )
        return

    try:
        # Governed write: no Coordinator Session is active — open a one-shot
        # Session ourselves so the INSERT is durable + strict-safe. Awaited +
        # immediate commit + RAISE-on-failure semantics preserved.
        from matrx_orm import (
            COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
            Session,
            allow_direct_coordinator_write,
        )

        with allow_direct_coordinator_write(
            _cxm().conversation.model,
            reason=("out-of-lane conversation create — no Coordinator exists in this scope"),
            acknowledgement=COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
        ):
            async with Session():
                await _cxm().conversation.create_conversation(**create_kwargs)
        vcprint(
            f"[ConversationGate] Created conversation: {conversation_id}...",
            color="green",
        )
    except Exception as exc:
        raise ConversationGateError(
            f"Failed to create conversation {conversation_id}: {exc}"
        ) from exc


async def ensure_conversation_exists(
    conversation_id: str,
    user_id: str,
    parent_conversation_id: str | None = None,
) -> None:
    """Ensure a cx_conversation row exists for the given ID.

    Idempotent: creates if missing, no-op if already present.
    Called at the start of ``execute_until_complete()`` so every
    execution path (API, test, agent-to-agent, internal) is covered.

    On creation, writes ``initial_variables`` and ``initial_overrides``
    from the current AppContext (set by agent/chat routes via ctx.extend()).
    These are write-once — subsequent calls for the same conversation_id
    are no-ops and never overwrite them.

    Fire-and-forget safe — logs errors but never raises.

    Client host: when a ConversationStore is configured (matrx-local), the
    write is delegated to the store and NOTHING below runs — no cxm, no
    coordinator (0.1.26 ConversationHandler semantics).
    """
    from matrx_ai.client_host import get_conversation_store

    store = get_conversation_store()
    if store is not None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        try:
            await store.ensure_conversation_exists(
                conversation_id=conversation_id,
                user_id=user_id,
                parent_conversation_id=parent_conversation_id,
                variables=ctx.initial_variables if ctx else {},
                overrides=ctx.initial_overrides if ctx else {},
            )
        except Exception as exc:
            vcprint(
                f"[ConversationGate] ConversationStore.ensure_conversation_exists failed: {exc}",
                color="yellow",
            )
        return

    if not _is_valid_uuid(conversation_id):
        vcprint(
            f"[ConversationGate] Cannot ensure conversation: not a valid UUID: {conversation_id!r}",
            color="yellow",
        )
        return

    safe_user_id = _require_valid_user_id(user_id, "ensure_conversation_exists")

    # Memo fast-path — prep already created (or a prior call confirmed) this row.
    # Skip the existence SELECT; still do the cheap tracker registration.
    memo_scope = _known_conversation_ids.get(conversation_id)
    if memo_scope is _ENSURED_DURABLE or memo_scope == _coord_scope_key():
        _known_conversation_ids.move_to_end(conversation_id)
        tracker = try_get_tracker()
        if tracker:
            tracker.register_existing("matrx", "conversation", conversation_id)
        return

    existing = await _cxm().conversation.filter_conversations(
        id=conversation_id,
    )
    if existing:
        mark_conversation_known(conversation_id, scope=_ENSURED_DURABLE)
        tracker = try_get_tracker()
        if tracker:
            tracker.register_existing("matrx", "conversation", conversation_id)
        return

    # Read write-once creation data from context (may be empty for non-agent calls)
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()

    title = _resolve_initial_conversation_title(title=None, ctx=ctx)

    create_kwargs: dict[str, Any] = {
        "id": conversation_id,
        "created_by": safe_user_id,
        "status": "active",
        "message_count": 0,
        "config": {},
        "title": title,
        "metadata": {},
        "variables": ctx.initial_variables if ctx else {},
        "overrides": ctx.initial_overrides if ctx else {},
        "source_app": ctx.source_app if ctx else "",
        "source_feature": ctx.source_feature if ctx else "",
        "is_ephemeral": not ctx.store if ctx else False,
        "conversation_type": _resolve_conversation_type(ctx, parent_conversation_id),
    }
    _stamp_origin(create_kwargs, ctx, with_witness=False)
    _stamp_agent_refs(
        create_kwargs,
        ctx,
        id_key="initial_agent_id",
        version_key="initial_agent_version_id",
    )
    stamp_org_id(create_kwargs, getattr(ctx, "organization_id", None))
    verified_parent = await resolve_parent_conversation_lineage(
        parent_conversation_id,
        conversation_id,
    )
    if verified_parent:
        create_kwargs["parent_conversation_id"] = verified_parent

    # Route through the WriteCoordinator when a request scope is active
    # (the common path — every streaming request reaches here). The INSERT
    # lands at end-of-stream flush, alongside cx_message / cx_request /
    # cx_user_request — one transaction for the whole turn. When called
    # outside a request (boot-time / scripts), fall back to the direct
    # ORM create so the row still lands.
    if _get_active_lane_coordinator() is not None:
        _queue_conversation_create(**create_kwargs)
        mark_conversation_known(conversation_id, scope=_coord_scope_key())
        vcprint(
            f"[ConversationGate] Queued conversation create: {conversation_id}",
            color="green",
        )
        tracker = try_get_tracker()
        if tracker:
            tracker.register_existing("matrx", "conversation", conversation_id)
        if ctx and ctx.auth_type == "fingerprint" and ctx.fingerprint_id:
            # Phase F: detached_task — guest-execution log writes its own
            # row and would race the parent flush if it inherited the
            # transaction connection.
            detached_task(
                _log_guest_execution(
                    fingerprint=ctx.fingerprint_id,
                    conversation_id=conversation_id,
                    ip_address=ctx.ip_address,
                    user_agent=ctx.user_agent,
                ),
                name="log_guest_execution",
            )
        return

    try:
        # Out-of-request branch (no Coordinator) — open a one-shot Session so the
        # conversation INSERT is governed (durable + strict-safe).
        from matrx_orm import (
            COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
            Session,
            allow_direct_coordinator_write,
        )

        with allow_direct_coordinator_write(
            _cxm().conversation.model,
            reason=("out-of-lane conversation ensure — no Coordinator exists in this scope"),
            acknowledgement=COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
        ):
            async with Session() as session:
                await _cxm().conversation.create_conversation(**create_kwargs)
        report = await session.flush(reason="conversation_gate")
        if report.error is not None:
            raise RuntimeError(report.error)
        mark_conversation_known(conversation_id, scope=_ENSURED_DURABLE)
        vcprint(
            f"[ConversationGate] Auto-created conversation: {conversation_id}",
            color="green",
        )
        tracker = try_get_tracker()
        if tracker:
            tracker.register_existing("matrx", "conversation", conversation_id)
        if ctx and ctx.auth_type == "fingerprint" and ctx.fingerprint_id:
            # Phase F: detached_task — guest-execution log writes its own
            # row and would race the parent flush if it inherited the
            # transaction connection.
            detached_task(
                _log_guest_execution(
                    fingerprint=ctx.fingerprint_id,
                    conversation_id=conversation_id,
                    ip_address=ctx.ip_address,
                    user_agent=ctx.user_agent,
                ),
                name="log_guest_execution",
            )
    except Exception as exc:
        recheck = await _cxm().conversation.filter_conversations(
            id=conversation_id,
        )
        if recheck:
            return
        vcprint(
            f"[ConversationGate] Failed to ensure conversation: {exc}",
            color="yellow",
        )


async def _log_guest_execution(
    fingerprint: str,
    conversation_id: str,
    ip_address: str | None,
    user_agent: str | None,
) -> None:
    from matrx_ai.db.guest_registry import log_guest_execution

    await log_guest_execution(
        fingerprint=fingerprint,
        resource_type="conversation",
        resource_id=conversation_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )


async def verify_existing_conversation(
    conversation_id: str,
) -> dict[str, Any]:
    """SELECT and return the conversation row.

    Raises ``ConversationGateError`` if the conversation does not exist or
    the ID is invalid.
    """
    if not _is_valid_uuid(conversation_id):
        raise ConversationGateError(f"conversation_id is not a valid UUID: {conversation_id!r}")

    # Client host: read through the store, never the cx_ ORM tables.
    from matrx_ai.client_host import get_conversation_store

    store = get_conversation_store()
    if store is not None:
        try:
            data = await store.get_conversation_data(conversation_id)
        except Exception as exc:
            raise ConversationGateError(
                f"conversation_store read failed for {conversation_id}: {type(exc).__name__}: {exc}"
            ) from exc
        row = (data or {}).get("conversation")
        if not row:
            raise ConversationGateError(f"Conversation not found: {conversation_id}")
        return row if isinstance(row, dict) else {"id": conversation_id}

    matches = await _cxm().conversation.filter_conversations(
        id=conversation_id,
    )

    if not matches:
        raise ConversationGateError(f"Conversation not found: {conversation_id}")

    row = matches[0]
    vcprint(
        f"[ConversationGate] Verified conversation: {conversation_id}...",
        color="green",
    )
    if isinstance(row, dict):
        return row

    # Model instance — expose the identity fields AppContext restore needs.
    # Previously this collapsed to ``{"id": ...}`` and silently dropped
    # organization_id / agent attribution, forcing every caller to re-fetch.
    def _s(name: str) -> str | None:
        val = getattr(row, name, None)
        return str(val) if val is not None else None

    return {
        "id": str(getattr(row, "id", conversation_id)),
        "organization_id": _s("organization_id"),
        "task_id": _s("task_id"),
        "initial_agent_id": _s("initial_agent_id"),
        "initial_agent_version_id": _s("initial_agent_version_id"),
        # Conversation variables are immutable: they were substituted into
        # the authored prompt on turn one.  Continuation callers may re-send
        # them as a resource-binding witness, so the shared execution gate
        # needs the persisted values before any message is appended or model
        # work begins.
        "variables": getattr(row, "variables", None),
    }


async def update_conversation_status(
    conversation_id: str,
    status: str,
) -> None:
    """Update the status field on an existing cx_conversation row.

    Fire-and-forget safe — logs errors but never raises.
    Client host: no-op (0.1.26 parity) — the store owns status transitions
    through persist_completed_request.
    """
    from matrx_ai.client_host import get_conversation_store

    if get_conversation_store() is not None:
        return
    if not _is_valid_uuid(conversation_id):
        return
    if _get_coordinator() is not None:
        _queue_conversation_update(conversation_id, status=status)
        return
    try:
        await _cxm().conversation.update_conversation(
            conversation_id,
            status=status,
        )
    except Exception as exc:
        vcprint(
            f"[ConversationGate] Failed to update status to {status!r}: {exc}",
            color="yellow",
        )


# =========================================================================
# User request lifecycle
# =========================================================================


async def _store_pending_user_request(request_id: str, user_id: str) -> bool:
    """Client-host dispatch shared by ``create_pending_user_request`` and
    ``ensure_user_request_exists``: when a ConversationStore is configured,
    delegate the pending user-request insert to it (the store owns
    idempotency) and return True so the caller early-returns. Fire-and-forget
    safe — logs errors but never raises."""
    from matrx_ai.client_host import get_conversation_store

    store = get_conversation_store()
    if store is None:
        return False
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    try:
        await store.create_pending_user_request(
            request_id=request_id,
            conversation_id=(getattr(ctx, "conversation_id", "") or "") if ctx else "",
            user_id=user_id,
        )
    except Exception as exc:
        vcprint(
            f"[ConversationGate] ConversationStore.create_pending_user_request failed: {exc}",
            color="yellow",
        )
    return True


async def create_pending_user_request(
    request_id: str,
    user_id: str,
) -> None:
    """INSERT a cx_user_request row with status='pending'.

    Called at the start of ``execute_until_complete()`` so the row exists
    before any tool calls run.  The ``request_id`` from ``AIMatrixRequest``
    becomes the PK so downstream systems can reference it immediately.

    The row carries NO conversation — see the module docstring; the
    request↔conversation link lives on ``cx_request``.

    Fire-and-forget safe — logs errors but never raises.

    Client host: delegated to the ConversationStore when configured
    (conversation_id comes from the current AppContext — a cx_user_request
    has no conversation server-side, but the 0.1.26 handler shape carries it).
    """
    if await _store_pending_user_request(request_id, user_id):
        return

    if not _is_valid_uuid(request_id):
        vcprint(
            f"[ConversationGate] Cannot create pending request "
            f"(legacy cx_user_request · runtime.global_request): "
            f"request_id is not a valid UUID: {request_id!r}",
            color="yellow",
        )
        return

    safe_user_id = _require_valid_user_id(user_id, "create_pending_user_request")

    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()

    create_kwargs: dict[str, Any] = {
        "id": request_id,
        "status": "pending",
        "iterations": 0,
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_cached_tokens": 0,
        "total_tokens": 0,
        "total_cost": 0,
        "total_tool_calls": 0,
        "metadata": {},
        "source_app": ctx.source_app if ctx else "",
        "source_feature": ctx.source_feature if ctx else "",
    }
    _stamp_origin(create_kwargs, ctx, with_witness=True)
    _stamp_agent_refs(
        create_kwargs,
        ctx,
        id_key="agent_id",
        version_key="agent_version_id",
    )
    stamp_row_owner(create_kwargs, safe_user_id)
    stamp_org_id(create_kwargs, getattr(ctx, "organization_id", None))

    try:
        await _cxm().user_request.create_user_request(**create_kwargs)
        from matrx_ai.db.request_tracking_log import format_request_tracking_label

        vcprint(
            f"[ConversationGate] Created pending request: "
            f"{format_request_tracking_label(request_id)}...",
            color="green",
        )
    except Exception as exc:
        vcprint(
            f"[ConversationGate] Failed to create pending request "
            f"(legacy cx_user_request · runtime.global_request): {exc}",
            color="yellow",
        )


# Per-request_id asyncio locks make the check-then-create dance atomic
# WITHIN a single process. Without this, N concurrent callers (sub-agents,
# parallel pipeline steps, fan-out tool calls) all race to insert the same
# row and the loser(s) get duplicate-key IntegrityError logged loudly by
# the ORM manager BEFORE the recheck-recovery below can swallow it.
#
# We don't garbage-collect the lock dict — request_ids are UUIDs and the
# expected lifetime of any one lock is one user action, so the dict's
# growth is bounded by RPS × seconds-per-request and doesn't accumulate
# meaningfully in practice.
_user_request_locks: dict[str, asyncio.Lock] = {}
_user_request_locks_guard = asyncio.Lock()

# Process-local memo of request_ids whose cx_user_request row is known to exist
# (created or confirmed this process). The boundary layer (API route prep) and
# the executor BOTH call ensure_user_request_exists for the same request_id —
# the executor as a self-heal for non-boundary callers (workflows, batch). Sub-
# agents also inherit the parent's request_id and re-ensure. Without this memo,
# every redundant call pays a SELECT (~100ms on a remote pooler) for a row we
# already created this turn. The cheap tracker.register_existing side effect
# still runs on a memo hit.
#
# 🔴 The memo entry is SCOPED, not a bare "exists" flag, because "the row is
# created" is not the same as "the row is DURABLE." An out-of-request write
# commits synchronously (durable the moment ensure returns); a write inside a
# WriteCoordinator is only QUEUED into THAT coordinator's Session and does not
# commit until the turn/child barrier. Two sub-agents forked concurrently from
# one parent request (podcast script + metadata, run as concurrent tasks) each
# get their OWN coordinator but SHARE the parent request_id. If the memo were a
# global "exists" flag, the first sub-agent to ensure() would set it after
# merely QUEUING the parent into its own Session, and the sibling would then
# SKIP queuing the parent into ITS Session — flushing a cx_request whose
# user_request_id has no parent row → asyncpg ForeignKeyViolationError
# cx_request_user_request_id_fkey (the 2026-07-13 blank-title podcast class).
# So a queued entry is scoped to the coordinator that queued it (only THAT
# coordinator may trust it); only a durably-committed entry is trusted by any
# scope. A sibling coordinator re-queues its own idempotent parent INSERT, and
# the Session's individual-write pkey swallow (session.py::_individual_write_pass)
# collapses the duplicate — FK always resolves in-Session.
_ENSURED_DURABLE = object()  # sentinel: row is committed — any scope may trust it
_ensured_request_ids: OrderedDict[str, object] = OrderedDict()
_ENSURED_MEMO_MAX = 50_000


def _coord_scope_key() -> object:
    """The trust scope for a memo entry written right now.

    ``_ENSURED_DURABLE`` when no coordinator is active (the row committed through
    a one-shot Session — durable, universally trustworthy); otherwise the
    identity of the active WriteCoordinator (the row is only queued into that
    coordinator's Session, so only the same coordinator may skip re-queuing it).
    """
    coord = _get_active_lane_coordinator()
    return _ENSURED_DURABLE if coord is None else id(coord)


def _remember_ensured(request_id: str, scope: object) -> None:
    _ensured_request_ids[request_id] = scope
    _ensured_request_ids.move_to_end(request_id)
    while len(_ensured_request_ids) > _ENSURED_MEMO_MAX:
        _ensured_request_ids.popitem(last=False)


# Same idea for cx_conversation. Prep's create_new_conversation (aidream) INSERTs
# the conversation row directly, then the executor calls
# ensure_conversation_exists() which re-SELECTs to confirm it — a redundant round-
# trip on every turn whose conversation prep already created. Mark the id known at
# creation (here AND from create_new_conversation via mark_conversation_known) so
# the executor's self-heal SELECT is skipped.
_known_conversation_ids: OrderedDict[str, object] = OrderedDict()


def mark_conversation_known(conversation_id: str, *, scope: object | None = None) -> None:
    """Memoize a durable row globally or a queued row for its coordinator only."""
    if not conversation_id:
        return
    _known_conversation_ids[conversation_id] = scope or _ENSURED_DURABLE
    _known_conversation_ids.move_to_end(conversation_id)
    while len(_known_conversation_ids) > _ENSURED_MEMO_MAX:
        _known_conversation_ids.popitem(last=False)


async def _get_user_request_lock(request_id: str) -> asyncio.Lock:
    async with _user_request_locks_guard:
        lock = _user_request_locks.get(request_id)
        if lock is None:
            lock = asyncio.Lock()
            _user_request_locks[request_id] = lock
        return lock


async def _create_user_request(
    *,
    request_id: str,
    user_id: str,
) -> None:
    """Create (or queue) a single cx_user_request row under ``request_id``.

    Idempotent against the row's own existence — a no-op if a row with
    ``request_id`` is already present (DB read or pending-queue). The caller
    owns the per-request_id lock; this helper owns only the build + write.

    The row carries NO conversation — request↔conversation lives on
    ``cx_request``.
    """
    from datetime import UTC, datetime

    from matrx_ai.context.app_context import try_get_app_context

    existing = await _cxm().user_request.filter_user_requests(id=request_id)
    if existing:
        tracker = try_get_tracker()
        if tracker:
            tracker.register_existing("matrx", "user_request", request_id)
        return

    ctx = try_get_app_context()

    create_kwargs: dict[str, Any] = {
        "id": request_id,
        "status": "pending",
        # Heartbeat seed — the lifecycle watchdog ages off last_activity_at,
        # so a request must start "fresh" or it would be abandoned before its
        # first turn ever commits. Refreshed each turn in persist_completed_request.
        "last_activity_at": datetime.now(UTC),
        "iterations": 0,
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_cached_tokens": 0,
        "total_tokens": 0,
        "total_cost": 0,
        "total_tool_calls": 0,
        "metadata": {},
        "source_app": ctx.source_app if ctx else "",
        "source_feature": ctx.source_feature if ctx else "",
    }
    _stamp_origin(create_kwargs, ctx, with_witness=True)
    _stamp_agent_refs(
        create_kwargs,
        ctx,
        id_key="agent_id",
        version_key="agent_version_id",
    )
    stamp_row_owner(create_kwargs, user_id)
    stamp_org_id(create_kwargs, getattr(ctx, "organization_id", None))

    # Route through the WriteCoordinator when in a request scope.
    # The row queues alongside the eventual UPDATE-to-completed from
    # persist_completed_request. Cancellation can no longer land the INSERT
    # but skip the UPDATE because BOTH live in the same end-of-stream
    # transaction.
    if _get_coordinator() is not None:
        qk = dict(create_kwargs)
        qk.pop("id", None)
        _queue_user_request_create(id=request_id, **qk)
        tracker = try_get_tracker()
        if tracker:
            tracker.register_existing("matrx", "user_request", request_id)
        return

    try:
        # Out-of-request branch (no Coordinator) — open a one-shot Session so the
        # user_request INSERT is governed (durable + strict-safe), mirroring
        # ensure_conversation_exists. Reached from the ~14 router-prep callers
        # that run before the streaming lane opens (podcast/agent-run prep
        # included). cx_user_request is Coordinator-OWNED, so this deliberate
        # pre-lane write must carry the explicit direct-write acknowledgement —
        # without it every podcast/agent-run prep fires a false
        # CoordinatorWriteViolation ownership alarm (Session write_scope=None).
        from matrx_orm import (
            COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
            Session,
            allow_direct_coordinator_write,
        )

        with allow_direct_coordinator_write(
            _cxm().user_request.model,
            reason=(
                "pre-lane router-prep ensure of cx_user_request — no Coordinator "
                "exists yet; the row must land before the streaming lane opens"
            ),
            acknowledgement=COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
        ):
            async with Session():
                await _cxm().user_request.create_user_request(**create_kwargs)
        from matrx_ai.db.request_tracking_log import format_request_tracking_label

        vcprint(
            f"[ConversationGate] Ensured request: {format_request_tracking_label(request_id)}...",
            color="green",
        )
        tracker = try_get_tracker()
        if tracker:
            tracker.register_existing("matrx", "user_request", request_id)
    except Exception as exc:
        recheck = await _cxm().user_request.filter_user_requests(id=request_id)
        if recheck:
            # Cross-process race resolved — another worker beat us to the
            # insert.  Silently consume and let the caller proceed.
            return
        vcprint(
            f"[ConversationGate] Failed to ensure request "
            f"(legacy cx_user_request · runtime.global_request): {exc}",
            color="yellow",
        )


async def ensure_user_request_exists(
    request_id: str,
    user_id: str,
) -> None:
    """Ensure a cx_user_request row exists for the given request_id.

    A ``cx_user_request`` is ONE backend API call (one user action), keyed
    solely by ``request_id`` and owned by ``user_id``. It has NO conversation
    — the request↔conversation bridge lives on ``cx_request`` (which carries
    both ``user_request_id`` and ``conversation_id``). One ``request_id``
    legitimately spans many conversations (batch) and one conversation spans
    many ``request_id``s (multi-turn); both are represented purely through
    ``cx_request`` rows now.

    Idempotent: creates with status='pending' if missing, no-op if already
    present.  Concurrency-safe: per-request_id asyncio.Lock serialises
    concurrent callers within a process so the check-then-create runs at most
    once per request_id.  Cross-process races are recovered via the recheck
    in ``_create_user_request``.

    Fire-and-forget safe — logs errors but never raises.

    Client host: delegated to the ConversationStore when configured — the
    store's create_pending_user_request owns idempotency.
    """
    if await _store_pending_user_request(request_id, user_id):
        return

    if not _is_valid_uuid(request_id):
        vcprint(
            f"[ConversationGate] Cannot ensure request "
            f"(legacy cx_user_request · runtime.global_request): "
            f"request_id is not a valid UUID: {request_id!r}",
            color="yellow",
        )
        return

    safe_user_id = _require_valid_user_id(user_id, "ensure_user_request_exists")

    lock = await _get_user_request_lock(request_id)
    async with lock:
        # Memo fast-path — we already ensured this row this process. Skip the
        # redundant existence SELECT (the duplicate-call cost) but still do the
        # cheap in-memory tracker registration the existing-row branch does.
        # A memo hit counts ONLY when the row is durably committed
        # (``_ENSURED_DURABLE``) or was queued by the SAME coordinator now
        # active — a sibling coordinator must fall through and queue the parent
        # into its own Session (see the memo doc above: the concurrent
        # podcast-fan-out FK-orphan class).
        memo_scope = _ensured_request_ids.get(request_id)
        if memo_scope is not None and (
            memo_scope is _ENSURED_DURABLE or memo_scope == _coord_scope_key()
        ):
            _ensured_request_ids.move_to_end(request_id)
            tracker = try_get_tracker()
            if tracker:
                tracker.register_existing("matrx", "user_request", request_id)
            return

        existing = await _cxm().user_request.filter_user_requests(id=request_id)
        if existing:
            # Already recorded — normal retry / resume / multi-turn /
            # batch-fan-out path. One row per user action, shared by every
            # cx_request it spawns regardless of conversation.
            _remember_ensured(request_id, _coord_scope_key())
            tracker = try_get_tracker()
            if tracker:
                tracker.register_existing("matrx", "user_request", request_id)
            return

        await _create_user_request(
            request_id=request_id,
            user_id=safe_user_id,
        )
        _remember_ensured(request_id, _coord_scope_key())


async def update_user_request_status(
    request_id: str,
    status: str,
    error: str | None = None,
) -> None:
    """Update the status (and optionally error) on an existing cx_user_request.

    Fire-and-forget safe — logs errors but never raises.
    Client host: no-op (0.1.26 parity) — the store owns status transitions
    through persist_completed_request.
    """
    from matrx_ai.client_host import get_conversation_store

    if get_conversation_store() is not None:
        return
    if not _is_valid_uuid(request_id):
        return

    update_kwargs: dict[str, Any] = {"status": status}
    if error is not None:
        update_kwargs["error"] = error

    if _get_coordinator() is not None:
        _queue_user_request_update(request_id, **update_kwargs)
        return

    try:
        # Out-of-request branch (no Coordinator) — one-shot Session so the
        # user_request UPDATE is governed (durable + strict-safe).
        # cx_user_request is Coordinator-OWNED; same deliberate pre/post-lane
        # acknowledgement as _create_user_request above, or this fires a false
        # CoordinatorWriteViolation ownership alarm.
        from matrx_orm import (
            COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
            Session,
            allow_direct_coordinator_write,
        )

        with allow_direct_coordinator_write(
            _cxm().user_request.model,
            reason=(
                "out-of-lane cx_user_request status update — no Coordinator exists in this scope"
            ),
            acknowledgement=COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
        ):
            async with Session():
                await _cxm().user_request.update_user_request(
                    request_id,
                    **update_kwargs,
                )
    except Exception as exc:
        vcprint(
            f"[ConversationGate] Failed to update user_request status to {status!r}: {exc}",
            color="yellow",
        )


# =========================================================================
# Concurrent launch helper
# =========================================================================


def launch_conversation_gate(
    conversation_id: str,
    is_new_conversation: bool,
    execution_task: asyncio.Task[Any],
) -> asyncio.Task[Any] | None:
    """Wire up the conversation gate for new conversations.

    Reads ``user_id`` and ``emitter`` from the current ``ExecutionContext``.

    For ``is_new_conversation=True``:
        Fires the INSERT as a concurrent ``asyncio.Task``.  When that task
        finishes, a done-callback inspects the result:
        - On success -> no-op, execution continues.
        - On failure -> cancels ``execution_task`` and pushes a fatal error
          through the emitter.

    For ``is_new_conversation=False``:
        Returns ``None``.  The caller is expected to have already awaited
        ``verify_existing_conversation()`` before starting execution.

    Returns the gate task (or None) so the caller can track it if needed.
    """
    if not is_new_conversation:
        return None

    from matrx_ai.context.app_context import get_app_context

    exec_ctx = get_app_context()
    user_id = exec_ctx.user_id
    emitter = exec_ctx.emitter

    async def _gate_task() -> None:
        await create_new_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

    gate_task = asyncio.create_task(_gate_task())

    def _on_gate_done(t: asyncio.Task[Any]) -> None:
        exc = t.exception()
        if exc is None:
            return

        vcprint(
            f"[ConversationGate] INSERT failed — cancelling execution: {exc}",
            color="red",
        )

        execution_task.cancel()

        async def _send_fatal() -> None:
            try:
                await emitter.fatal_error(
                    error_type="conversation_gate_error",
                    message=str(exc),
                    user_message="Failed to initialize conversation. Please try again.",
                    details=traceback.format_exception(type(exc), exc, exc.__traceback__),
                )
            except Exception:
                pass

        try:
            asyncio.get_running_loop()
            from matrx_utils import detached_task

            detached_task(_send_fatal(), name="conversation_gate_fatal_event")
        except RuntimeError:
            pass

    gate_task.add_done_callback(_on_gate_done)
    return gate_task
