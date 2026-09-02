"""Conversation type — the single classification of how a cx_conversation began.

This replaces three scattered, partial encodings of the same idea:

* ``INTERNAL_SOURCE_FEATURES`` — a frozenset of ``source_feature`` strings used
  only by the title backfill (``conversation_title_backfill.py``).
* the ``"Auto: "`` title prefix written by ``conversation_gate._format_auto_title``.
* the runtime-only ``AppContext.is_internal_agent`` flag (persisted nowhere).

None of those is a durable, queryable column the UI can route on. The
``cx_conversation.conversation_type`` column (TEXT, NOT NULL, default
``'standard'``) is now that source of truth, and this module owns the vocabulary.

``source_app`` / ``source_feature`` are unchanged — they live on the user
request and describe the *caller*, not the conversation's origin class.

The column is plain TEXT (not a Postgres enum type) on purpose: adding a value
is a one-line change here, no migration. The :func:`coerce_conversation_type`
gate keeps unregistered values out of the column loudly.
"""

from __future__ import annotations

from enum import StrEnum

from matrx_utils import vcprint


class ConversationType(StrEnum):
    """How a conversation was initiated. Default ``STANDARD``."""

    # User-initiated: chat, manual, agent, prompt, agent_blocks, conversation,
    # fork_and_run, legacy socket. The default for any human-driven run.
    STANDARD = "standard"
    # Spawned by another agent mid-run (the fork_for_child_agent path; carries a
    # parent_conversation_id). Applies regardless of which domain spawned it.
    SUBAGENT = "subagent"
    # Scheduler-initiated (agent_runner_adapter; today source_feature 'server-run').
    SCHEDULED = "scheduled"
    # Workflow run / step (source_feature 'workflow_run' / 'workflow_worker').
    WORKFLOW = "workflow"
    # Research pipeline runs (today faked via feature / autonomy_level='auto').
    RESEARCH = "research"
    # Podcast generation runs.
    PODCAST = "podcast"
    # Catch-all internal/automated pipelines not covered above: NER ingest, RAG,
    # KG clustering, content-processing upload hook, agent-factory, pdf-cleaner.
    AUTO = "auto"
    # Internal test / system runs (e.g. tool_testing).
    SYSTEM = "system"


# Every type that is NOT a normal user-facing conversation. The UI uses this to
# decide whether a conversation belongs in the main thread list or in an
# internal/automation surface. is_internal_agent maps onto membership here.
INTERNAL_CONVERSATION_TYPES: frozenset[str] = frozenset(
    t.value for t in ConversationType if t is not ConversationType.STANDARD
)

_VALID_VALUES: frozenset[str] = frozenset(t.value for t in ConversationType)


# source_feature → conversation_type. Used only as a *derivation fallback* when
# an explicit type was not set (legacy / unmigrated callers). Explicitly-set
# types always win. Unmapped features fall through to STANDARD (and then to the
# is_internal_agent / parent-lineage signals in derive_conversation_type).
SOURCE_FEATURE_TO_TYPE: dict[str, str] = {
    # standard (user-facing)
    "chat": ConversationType.STANDARD,
    "manual": ConversationType.STANDARD,
    "agent": ConversationType.STANDARD,
    "agent_blocks": ConversationType.STANDARD,
    "prompt": ConversationType.STANDARD,
    "conversation": ConversationType.STANDARD,
    "conversation_resume": ConversationType.STANDARD,
    "fork_and_run": ConversationType.STANDARD,
    "socket_compat": ConversationType.STANDARD,
    # scheduled
    "server-run": ConversationType.SCHEDULED,
    # workflow
    "workflow_run": ConversationType.WORKFLOW,
    "workflow_worker": ConversationType.WORKFLOW,
    "workflow_decision_fallback": ConversationType.WORKFLOW,
    # research — the product feature plus the two automated research pipelines
    # that carry their own registered slugs (source_attribution, 2026-08-21).
    "research": ConversationType.RESEARCH,
    "web_research": ConversationType.RESEARCH,
    "deep_research_v1": ConversationType.RESEARCH,
    # podcasts
    "podcasts": ConversationType.PODCAST,
    # auto (internal automated pipelines)
    "auto_ingest_ner": ConversationType.AUTO,
    "ner": ConversationType.AUTO,
    "rag": ConversationType.AUTO,
    "agent_call": ConversationType.SUBAGENT,
    "agent_tool": ConversationType.SUBAGENT,
    "pdf-cleaner": ConversationType.AUTO,
    "content_processing_upload_hook": ConversationType.AUTO,
    "kg_clustering_namer": ConversationType.AUTO,
    "agent-factory": ConversationType.AUTO,
    # system
    "tool_testing": ConversationType.SYSTEM,
}


def is_valid_conversation_type(value: str | None) -> bool:
    return bool(value) and value in _VALID_VALUES


def is_internal_conversation(ctx: object | None) -> bool:
    """True when a context drives a non-user-facing conversation.

    ``conversation_type`` is the durable source of truth (any value other than
    ``standard`` is internal), but the runtime ``is_internal_agent`` flag is
    still honored so nothing regresses if a path sets the flag without the type
    (or vice-versa). Duck-typed so this module stays free of an AppContext
    import (and the matrx-connect dependency direction).
    """
    if ctx is None:
        return False
    if getattr(ctx, "is_internal_agent", False):
        return True
    return (
        getattr(ctx, "conversation_type", ConversationType.STANDARD.value)
        in INTERNAL_CONVERSATION_TYPES
    )


def coerce_conversation_type(value: str | None) -> str:
    """Validation gate — keep unregistered values out of the column, loudly.

    Returns a canonical ``ConversationType`` value. A registered value passes
    through; an empty / unknown value is coerced to ``STANDARD`` after a loud
    self-identifying banner so the typo (or missing registration) is impossible
    to miss in dev, while the write still succeeds (the column is NOT NULL).

    This catches our own antipattern (a mistyped or unregistered type string).
    It is NOT the place to derive a type from signals — that is
    :func:`derive_conversation_type`, which always runs after this in the gate,
    so an internal run whose explicit type was garbage is still rescued from a
    silent ``standard`` mislabel by the is_internal / source_feature signals.
    """
    if value in _VALID_VALUES:
        return value  # type: ignore[return-value]
    vcprint(
        "\n"
        "================================================================\n"
        "  matrx-ai — conversation_type.coerce_conversation_type\n"
        "  (conversation-type validation gate)\n"
        "----------------------------------------------------------------\n"
        "  My job: keep unregistered conversation_type values out of\n"
        "          cx_conversation.conversation_type.\n"
        f"  Caught: conversation_type={value!r} is not a registered\n"
        "          ConversationType value.\n"
        f"  Action: coerced to {ConversationType.STANDARD.value!r} so the write still\n"
        "          persists (the column is NOT NULL). If this run is internal,\n"
        "          the is_internal_agent / source_feature derivation fallback\n"
        "          will re-map it before persistence.\n"
        "  Fix:    set a real ConversationType at the context-construction site,\n"
        "          or register the new value in matrx_ai.agents.conversation_type.\n"
        f"  Known:  {sorted(_VALID_VALUES)}\n"
        "================================================================",
        color="red",
    )
    return ConversationType.STANDARD.value


def derive_conversation_type(
    *,
    explicit: str | None,
    is_internal_agent: bool = False,
    source_feature: str | None = None,
    parent_conversation_id: str | None = None,
) -> str:
    """Resolve the conversation type at a write site, with a safe fallback.

    Precedence:
      1. An explicitly-set, non-``standard`` registered type wins outright —
         the caller declared intent (e.g. ``fork_for_child_agent`` →
         ``subagent``).
      2. Otherwise (explicit is ``standard``, empty, or unregistered) re-derive
         from signals so an internal run is never silently labeled
         ``standard``:
           - ``is_internal_agent`` + a ``parent_conversation_id`` → ``subagent``
             (a forked child).
           - ``source_feature`` mapped via :data:`SOURCE_FEATURE_TO_TYPE` when
             that yields a non-``standard`` type.
           - ``is_internal_agent`` with no better signal → ``auto`` (an internal
             programmatic run that didn't set a finer type).
           - else ``standard``.
    """
    coerced = coerce_conversation_type(explicit) if explicit else ConversationType.STANDARD.value
    if coerced != ConversationType.STANDARD.value:
        return coerced

    if is_internal_agent and parent_conversation_id:
        return ConversationType.SUBAGENT.value

    if source_feature:
        mapped = SOURCE_FEATURE_TO_TYPE.get(source_feature)
        if mapped and mapped != ConversationType.STANDARD.value:
            return mapped

    if is_internal_agent:
        return ConversationType.AUTO.value

    return ConversationType.STANDARD.value
