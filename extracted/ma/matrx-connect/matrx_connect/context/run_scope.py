from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunScope:
    """Agent-run settings owned by PF-5 (the agent-run package): its one run function sets these at the run boundary; carried, never rebuilt."""

    # --- Block streaming ---
    block_mode: bool = False

    # --- Unit-version pinning for replay (chat.request_snapshot) ---
    # The workflow definition VERSION this call is being made inside, when the
    # run pinned one. `agent_version_id` on AppContext is the agent half and
    # already travels on every agent run; this is the workflow half, and there
    # was no carrier for it — a snapshot could not say which workflow version
    # produced the call, so a replay could not tell a candidate change apart
    # from an edit made to the workflow since.
    #
    # Set ONCE per run (the scheduler stamps it onto the run's context) and
    # inherited by every fork, so a nested agent call inside a workflow step
    # still records the run's pin.
    #
    # NULL is HONEST: a run started from a FLOATING definition genuinely has no
    # pinned version (workflow.run.definition_version_id is null there too), and
    # a call made outside any workflow has none either.
    workflow_definition_version_id: str | None = None

    # --- Observational memory ---
    # When True, the observational memory system (Observer + Reflector) runs
    # around each LLM turn — injects prior observations as a system message
    # pre-call, extracts new observations post-call. Admin-gated; persists on
    # cx_conversation.metadata.observational_memory once enabled. See
    # packages/matrx-ai/matrx_ai/memory/ and the OM integration guide.
    memory_enabled: bool = False
    memory_model: str | None = None
    #: The chosen CLASS of ``memory_model`` (an ai.offering id) — rides only with it.
    memory_offering_id: str | None = None
    memory_scope: str = "thread"


#: The field names that live on ``AppContext.run`` and nowhere else on a context.
RUN_SCOPE_FIELDS: frozenset[str] = frozenset(RunScope.__dataclass_fields__)
