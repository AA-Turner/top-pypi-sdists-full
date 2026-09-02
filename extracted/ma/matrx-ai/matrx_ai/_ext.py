"""
External Dependency Registry for matrx-ai package.

Provides a configuration-based approach for injecting external dependencies
that come from the host application (settings, file handlers, supabase client,
user_data functions, api_management functions, etc.).

This allows matrx-ai to function as a proper installable package without
directly importing from the host codebase.

Usage (host application startup):

    from matrx_ai._ext import configure_ext

    configure_ext(
        settings=settings,
        get_supabase_client=get_async_supabase_client,
        ...
    )

Usage (within matrx-ai package):

    from matrx_ai._ext import get_ext
    settings = get_ext("settings")
"""

from __future__ import annotations

from typing import Any

_registry: dict[str, Any] = {}
_configured = False


class ExtNotConfiguredError(RuntimeError):
    pass


def configure_ext(**kwargs: Any) -> None:
    global _configured
    _registry.update(kwargs)
    _configured = True


def is_configured() -> bool:
    return _configured


def get_ext(name: str) -> Any:
    if name not in _registry:
        raise ExtNotConfiguredError(
            f"matrx-ai external dependency '{name}' not registered. "
            f"Call matrx_ai.configure() before using this functionality."
        )
    return _registry[name]


def has_ext(name: str) -> bool:
    return name in _registry


# ---------------------------------------------------------------------------
# Post-finalize hook (Phase B — universal auto-ingest seam)
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a callable that the orchestrator invokes once a
# conversation turn is set up / finalized, so the host can fire its own
# fire-and-forget side effects (KG auto-ingest of the new messages) WITHOUT
# matrx-ai importing aidream. matrx-ai never knows what the hook does — it
# only knows "call it, swallow nothing, never block on it".
#
# Contract:
#   * The hook is OPTIONAL. When unconfigured, ``get_post_finalize_hook()``
#     returns None and the orchestrator skips it — matrx-ai stays standalone.
#   * The hook MUST be non-blocking from the orchestrator's perspective: the
#     host implementation schedules its work via detached_task and returns
#     immediately. matrx-ai calls it best-effort and never awaits real work.
#   * Signature (keyword-only, forward-compatible):
#         hook(*, conversation_id: str, user_id: str,
#              organization_id: str | None, messages: list,
#              is_continuation: bool) -> None
#     The host ignores kwargs it doesn't need.

_POST_FINALIZE_HOOK_KEY = "post_finalize_hook"


def get_post_finalize_hook() -> Any:
    """Return the host-injected post-finalize hook, or None when unset."""
    return _registry.get(_POST_FINALIZE_HOOK_KEY)


# ---------------------------------------------------------------------------
# Output-apply dispatcher (structured-output → durable side-effect seam)
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a dispatcher that the orchestrator invokes once a
# run's FINAL structured output has been parsed and the turn persisted, but
# BEFORE the stream closes (send_end). This is what lets an agent whose schema
# output carries a reserved apply-envelope key trigger a deterministic,
# server-side side effect that "has the last word" on the still-open stream —
# without matrx-ai knowing anything about what the side effect is.
#
# Contract:
#   * OPTIONAL. Unconfigured → ``get_matrx_directives_dispatcher()`` returns None
#     and the orchestrator skips it (matrx-ai stays standalone).
#   * AWAITED (unlike the fire-and-forget post-finalize hook): it runs to
#     completion before the orchestrator returns ``completed``, so the apply
#     lands before send_end. The host MUST keep it reasonably fast and MUST
#     NOT raise — it owns its own try/except and reports failures to the client
#     as warnings (warn-not-fatal). The orchestrator wraps the call in a
#     backstop try/except regardless, so a misbehaving dispatcher can never
#     turn a delivered AI response into a failed request.
#   * matrx-ai is agnostic about the envelope: it calls the dispatcher for any
#     non-empty dict structured output and lets the HOST do the reserved-key
#     early-return. The magic key lives in aidream, not here.
#   * Signature (keyword-only, forward-compatible):
#         async dispatcher(*, parsed: dict, ctx) -> None
#     ``parsed`` is the already-extracted structured-output object; ``ctx`` is
#     the active AppContext (emitter, user_id, organization_id,
#     conversation_id, request_id). The host ignores kwargs it doesn't need.

_MATRX_DIRECTIVES_DISPATCHER_KEY = "matrx_directives_dispatcher"


def get_matrx_directives_dispatcher() -> Any:
    """Return the host-injected Matrx Directives dispatcher, or None when unset."""
    return _registry.get(_MATRX_DIRECTIVES_DISPATCHER_KEY)


# ---------------------------------------------------------------------------
# Reference-fence stager (per-send wire-swap staging seam)
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a callable that resolves its in-content reference
# fences (the ```matrx envelope encoding) found in the config's text into the
# per-request wire swaps, so ``build_wire_config`` substitutes their live
# values into the throwaway provider clone. matrx-ai knows nothing about the
# encoding or the resolution — it only guarantees WHEN staging runs.
#
# Contract:
#   * OPTIONAL. Unconfigured → ``get_reference_fence_stager()`` returns None
#     and the orchestrator skips it (matrx-ai stays standalone).
#   * AWAITED once per loop iteration, immediately before the wire clone is
#     built — so fences arriving from ANY path (rebuilt history on a continue
#     turn, the current turn's user input, a programmatically-run child agent,
#     /resume, a turn-boundary injection drain) are staged in the task that
#     actually sends. Tool calls run in their own asyncio tasks (execute_batch
#     → gather), so swaps staged inside a tool task are invisible here — this
#     per-loop call is what makes every loop self-sufficient.
#   * The host MUST keep the no-fence path cheap (sentinel scan first) and
#     MUST NOT raise; the orchestrator wraps it in a backstop regardless.
#   * Signature: ``async stager(config) -> None`` — the host reads identity
#     (user_id) from its own request context.

_REFERENCE_FENCE_STAGER_KEY = "reference_fence_stager"


def get_reference_fence_stager() -> Any:
    """Return the host-injected reference-fence stager, or None when unset."""
    return _registry.get(_REFERENCE_FENCE_STAGER_KEY)


# ---------------------------------------------------------------------------
# Iteration tool refresh (per-iteration host-owned toolset reconciliation)
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a callable invoked once per loop iteration at the
# turn-boundary drain point (``drain_pending``), immediately before the
# provider call is built. It lets the host reconcile the ACTIVE toolset
# against durable state that can change while a run is in flight — the first
# consumer is mid-run Orchestra roster injection (ruling D-37): a member added
# to a RUNNING supervisor Orchestra becomes callable on the very next
# iteration, and a removed member's tool is filtered at this same safe
# pre-API-call point. matrx-ai never knows what the host reconciles — it only
# guarantees WHEN the hook runs and rebinds the context it returns.
#
# Contract:
#   * OPTIONAL. Unconfigured → ``get_iteration_tool_refresh()`` returns None
#     and the drain skips it (matrx-ai stays standalone).
#   * AWAITED once per iteration inside ``drain_pending`` — the same placement
#     as the in-memory mutation drain and the DB inbox, so the refreshed
#     toolset is what the imminent provider call sees. Removal here is safe by
#     construction: no tool_use can be pending an answer at this point.
#   * The host MUST gate itself cheaply: a run that carries no host-relevant
#     state (a plain agent) must pay ZERO extra reads. Best-effort at the
#     caller: a refresh failure logs LOUDLY and never kills the run.
#   * Signature: ``async refresh(config, ctx) -> AppContext | None`` — returns
#     the rebound context when it replaced it (the drain ``set_app_context``s
#     it), or None/same-ctx when nothing changed.

_ITERATION_TOOL_REFRESH_KEY = "iteration_tool_refresh"


def get_iteration_tool_refresh() -> Any:
    """Return the host-injected per-iteration tool refresh, or None when unset."""
    return _registry.get(_ITERATION_TOOL_REFRESH_KEY)


# ---------------------------------------------------------------------------
# Programmatic-agent context preparation (host resource boundary)
# ---------------------------------------------------------------------------
#
# HTTP/workflow agent starts pass through the host's canonical request
# preparation. Programmatic children (agent-as-tool, agent_call, NamedAgent)
# execute ``Agent`` directly, so the package offers one optional hook at that
# boundary. The host can expand file ids into lazy resource-family context,
# seed permanent agent resources, and inject the capabilities those resources
# advertise without matrx-ai importing host/database code.
#
# Contract:
#   * OPTIONAL. Standalone matrx-ai hosts continue unchanged.
#   * AWAITED after variables and user input are applied, immediately before
#     provider execution.
#   * Signature: ``async hook(*, agent, app_ctx) -> AppContext | None``.
#     The hook may mutate ``agent.config`` and returns the active derived
#     context when it replaced it.

_PROGRAMMATIC_AGENT_PREPARE_HOOK_KEY = "programmatic_agent_prepare_hook"


def get_programmatic_agent_prepare_hook() -> Any:
    """Return the host resource-boundary hook, or None when unset."""
    return _registry.get(_PROGRAMMATIC_AGENT_PREPARE_HOOK_KEY)


# ---------------------------------------------------------------------------
# Conversation-value writer (reference-mode agent results)
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a callable that stores a child agent's result in
# its durable per-conversation value store and returns a BOUNDED descriptor
# dict (key, description, kind, chars, preview, json_keys, fence). matrx-ai
# never knows the storage or the fence encoding — it only forwards the value
# and puts the returned descriptor into the caller's tool_result.
#
# Contract:
#   * OPTIONAL. Unconfigured → reference-mode agent calls degrade LOUDLY to
#     inline results (a standalone matrx-ai install has no store).
#   * AWAITED inside the tool task; the host owns identity (reads its request
#     context), event emission, and failure handling. A raise fails the tool
#     call (a dangling descriptor must never be returned).
#   * Signature (keyword-only):
#         async writer(*, key, description, value, json_schema=None,
#                      source_agent_id=None, source_call_id=None) -> dict

_CONVERSATION_VALUE_WRITER_KEY = "conversation_value_writer"


def get_conversation_value_writer() -> Any:
    """Return the host-injected conversation-value writer, or None when unset."""
    return _registry.get(_CONVERSATION_VALUE_WRITER_KEY)


# ---------------------------------------------------------------------------
# Conversation forker (fork-mode conversation-aware agent_call)
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a callable that durably copies a conversation's
# rows up to a position (its canonical fork helper) and returns the new
# conversation's identity. matrx-ai never knows which tables a fork copies —
# the host owns the copy; matrx-ai only runs the child agent inside the
# returned conversation.
#
# Contract:
#   * OPTIONAL. Unconfigured → ``agent_call(history_mode="fork")`` fails with a
#     clean ``feature_unavailable`` tool error (a standalone matrx-ai install
#     has no durable conversation store to fork).
#   * AWAITED inside the tool task, AFTER the tool's own ownership gate passed.
#     The host may re-check but must not silently widen access.
#   * Raises on failure (the tool converts it into a failed tool result).
#   * Signature (keyword-only):
#         async forker(*, source_conversation_id, user_id, up_to_position=None,
#                      parent_conversation_id=None, conversation_type=None,
#                      title=None) -> dict   # {"conversation_id", "message_count"}

_CONVERSATION_FORKER_KEY = "conversation_forker"


def get_conversation_forker() -> Any:
    """Return the host-injected conversation forker, or None when unset."""
    return _registry.get(_CONVERSATION_FORKER_KEY)


# ---------------------------------------------------------------------------
# Sandbox token minter (in-loop binding durability)
# ---------------------------------------------------------------------------
#
# A sandbox binding on ``ctx.metadata["active_sandbox"]`` carries a SHORT-LIVED
# scoped bearer token (the orchestrator mints them at ≤15 min, default 5 min).
# A long coding loop — or a client that disconnected and can no longer refresh —
# easily outlives that token, at which point every fs/shell/git tool call to the
# sandbox 401/403s and the agent gets a hard mid-task "auth failed" (which is NOT
# recoverable from inside the loop without this seam). The host (aidream) injects
# a minter that re-issues a fresh token for a live box via the orchestrator's
# master-key ``/agent-binding`` — server-side, independent of the client's token
# AND its connectivity. ``_sandbox_proxy`` calls it once on a 401/403 and retries.
#
# Contract:
#   * OPTIONAL. Unconfigured → the proxy cannot refresh and surfaces the auth
#     error as before (matrx-ai stays standalone; a bare install has no minter).
#   * AWAITED inline on a 401/403, at most once per proxied request. The host
#     owns the orchestrator call + its own error handling; it returns a fresh
#     token string or None (never raises — a raise is treated as "no token").
#   * Signature (keyword-only, forward-compatible):
#         async minter(*, sandbox_id: str, base_url: str) -> str | None
#     ``base_url`` is the binding's ``<orchestrator>/sandboxes/<id>`` so the host
#     can reach the correct orchestrator/tier. The host ignores kwargs it doesn't
#     need.

_SANDBOX_TOKEN_MINTER_KEY = "sandbox_token_minter"


def get_sandbox_token_minter() -> Any:
    """Return the host-injected sandbox token minter, or None when unset."""
    return _registry.get(_SANDBOX_TOKEN_MINTER_KEY)


# ---------------------------------------------------------------------------
# Turn-directive handler (inline non-blocking marker channel)
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a handler the orchestrator awaits after each
# iteration's response is appended (and once for the final response), passing
# ONLY that turn's model-authored text plus the live config. The host scans the
# text for its directive fences (e.g. context_groom) and applies them — an
# inline marker the model emits mid-prose without spending a tool call or
# ending its turn. matrx-ai never knows the encoding or the side effect.
#
# Contract:
#   * OPTIONAL. Unconfigured → skipped entirely (matrx-ai stays standalone).
#   * POSITION INVARIANT (security boundary): the orchestrator hands the
#     handler ONLY current-turn model-authored text — never history, user, or
#     tool content. The host must still do its own kind/type guarding.
#   * AWAITED before the per-turn barrier, so writes the handler queues on the
#     coordinator ride the same turn commit. Invoked on EVERY iteration when
#     configured (it also drains host-side pending state, e.g. a groom tool
#     call queued earlier in the turn) — the no-work path must stay cheap.
#     MUST NOT raise (the orchestrator wraps it in a backstop regardless).
#   * Signature: ``async handler(*, turn_text: str, config,
#     auto_stub_keys: list[str]) -> None`` — ``config`` is the LIVE
#     UnifiedConfig (the host may rewrite in-flight message content, e.g.
#     stubbing consumed tool results); ``auto_stub_keys`` are serve-once
#     value keys whose results the response JUST consumed (stub now — the
#     consumption-time contract).

_TURN_DIRECTIVE_HANDLER_KEY = "turn_directive_handler"


def get_turn_directive_handler() -> Any:
    """Return the host-injected turn-directive handler, or None when unset."""
    return _registry.get(_TURN_DIRECTIVE_HANDLER_KEY)


# ---------------------------------------------------------------------------
# Child-execution spawner (matrx-runtime spine lineage, best-effort)
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a callable that records a child agent run as a
# CHILD execution on its request-management spine ("conversation →
# conversation"). matrx-ai knows nothing about the spine — it reports "a child
# ran" and hands back usage; the host does all tracking OFF the hot path
# (detached tasks) per the spine's zero-latency + best-effort contract.
#
# Contract:
#   * OPTIONAL. Unconfigured (or no live root execution) → returns None and
#     nothing is tracked; the run is unaffected either way.
#   * ``spawner(*, label, link_id) -> (execution_id, settle) | None`` —
#     execution_id is pre-minted (synchronously known, e.g. for a
#     HandoffOutcome); ``settle`` is ``async settle(*, success: bool,
#     usage_history) -> None`` and MUST be awaited exactly once after the
#     child run finishes (it detaches internally; a failure to settle is
#     swept by the host's reaper).

_CHILD_EXECUTION_SPAWNER_KEY = "child_execution_spawner"


def get_child_execution_spawner() -> Any:
    """Return the host-injected child-execution spawner, or None when unset."""
    return _registry.get(_CHILD_EXECUTION_SPAWNER_KEY)


# ---------------------------------------------------------------------------
# Agent-run (multi-stage ledger) spine tracker
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a callable that records one `agent_run` pass
# (the RunCheckpointer's durable multi-stage run — podcast, research, ...) as a
# `global_execution` on its request-management spine. matrx-ai knows nothing
# about the spine — the checkpointer reports "a run pass began" at start/resume
# and settles the outcome at finish/fail; the host does all tracking OFF the
# hot path (detached tasks) per the spine's zero-latency + best-effort contract.
#
# Contract:
#   * OPTIONAL. Unconfigured → None; nothing is tracked, the run is unaffected.
#   * ``tracker(*, run_id, kind, user_id) -> settle | None`` — the host resolves
#     the ambient request context itself (nesting root-vs-child) and re-stamps
#     its nesting key so per-stage AI calls land as children of the run.
#   * ``settle`` is ``async settle(status: str, error: str | None = None)`` and
#     MUST be called exactly once with the run's terminal outcome ("completed" /
#     "failed"); an unsettled pass is swept by the host's reaper.

_AGENT_RUN_TRACKER_KEY = "agent_run_tracker"


def get_agent_run_tracker() -> Any:
    """Return the host-injected agent-run spine tracker, or None when unset."""
    return _registry.get(_AGENT_RUN_TRACKER_KEY)


# ---------------------------------------------------------------------------
# Runtime-spine loop control (Request Management Layer seams)
# ---------------------------------------------------------------------------
#
# Two OPTIONAL host hooks that put the LIVE conversation loop under the
# runtime engine's control primitives without matrx-ai importing the host:
#
#   * ``spine_control_check`` — ``async () -> str | None``. Polled by the
#     orchestrator at every iteration boundary (same place as the in-process
#     cancel registry). Returns None to proceed, or a short human reason when
#     the request's execution TREE must stop (durable cancel signal, tree
#     dollar budget, deadline, per-quantity limit). The host implementation
#     reads its own ambient context to find the tree; matrx-ai never knows how.
#     MUST be best-effort inside: an infrastructure blip returns None (allow),
#     never raises. A non-None reason ends the loop exactly like a registry
#     cancel — a valid final turn with status "cancelled".
#
#   * ``spine_call_meter`` — SYNC ``(usage) -> None``. Called once per billed
#     provider call at the usage chokepoint with that call's TokenUsage. The
#     host schedules a DETACHED meter write (zero hot-path cost) so tree
#     rollups/budgets see spend DURING the turn, not only at settle. MUST be
#     non-blocking and never raise.
#
# Unconfigured → both no-op; matrx-ai stays standalone.

_SPINE_CONTROL_CHECK_KEY = "spine_control_check"
_SPINE_CALL_METER_KEY = "spine_call_meter"


def get_spine_control_check() -> Any:
    """Return the host-injected spine control poll, or None when unset."""
    return _registry.get(_SPINE_CONTROL_CHECK_KEY)


def get_spine_call_meter() -> Any:
    """Return the host-injected per-call spine meter hook, or None when unset."""
    return _registry.get(_SPINE_CALL_METER_KEY)


# ---------------------------------------------------------------------------
# Internal-agent-run tracker (Request Management Layer — run_agent funnel seam)
# ---------------------------------------------------------------------------
#
# OPTIONAL host hook that puts every INTERNAL agent execution (`run_agent` —
# the one funnel behind NamedAgent.run, the agent-service `run_one_agent`,
# research fan-out, podcast metadata, batch derivations, …) on the host's
# runtime spine without matrx-ai importing the host. Closes the dual-write
# gap where internal runs minted legacy cx_user_request rows with no spine
# twin (2026-07-24 parity audit: 200 orphan rows/day across 8 features, all
# routed through this single funnel).
#
# Contract:
#   * ``async tracker(*, label: str, source_feature: str) -> settle | None``.
#     Called INSIDE the forked child context (so the host's ambient context
#     carries the run's request_id / agent identity / source tags). Returns
#     None when the run should not be tracked here (e.g. it is already inside
#     a host-tracked execution tree whose own machinery owns it) — then
#     run_agent does nothing further.
#   * ``settle`` is ``async settle(status: str, *, error: str | None = None,
#     meters: dict | None = None) -> None`` — called EXACTLY ONCE after the
#     run finishes: status "completed"/"failed", meters carrying the run's
#     final quantities ({"usd", "input_tokens", "output_tokens"}). The host
#     implementation detaches its writes; nothing blocks the run.
#   * Best-effort at every step: a tracker/settle failure never affects the
#     agent run. Unconfigured → no-op; matrx-ai stays standalone.

_INTERNAL_RUN_TRACKER_KEY = "internal_run_tracker"


def get_internal_run_tracker() -> Any:
    """Return the host-injected internal-agent-run tracker, or None when unset."""
    return _registry.get(_INTERNAL_RUN_TRACKER_KEY)


# ---------------------------------------------------------------------------
# Pronunciation-locator resolver (ElevenLabs native-dictionary seam)
# ---------------------------------------------------------------------------
#
# The host (aidream) injects a resolver that maps a user to their published
# ElevenLabs pronunciation-dictionary locator(s). The ElevenLabs TTS provider
# calls it when a request did not already carry explicit locators, so stored
# audio gets the user's effective dictionary applied natively — without
# matrx-ai importing aidream's DB rollup / publication ledger.
#
# Contract:
#   * OPTIONAL. Unconfigured → ``get_pronunciation_locator_resolver()`` returns
#     None and the provider sends no locators (matrx-ai stays standalone).
#   * BEST-EFFORT: the provider wraps the call and swallows failures — a
#     dictionary problem must never break or delay a paid TTS render.
#   * Signature (keyword-only, forward-compatible):
#         async resolver(*, user_id: str | None) -> list[dict[str, str]]
#     Returns at most 3 {pronunciation_dictionary_id, version_id} dicts.

_PRONUNCIATION_LOCATOR_RESOLVER_KEY = "pronunciation_locator_resolver"


def get_pronunciation_locator_resolver() -> Any:
    """Return the host-injected pronunciation-locator resolver, or None."""
    return _registry.get(_PRONUNCIATION_LOCATOR_RESOLVER_KEY)


# ---------------------------------------------------------------------------
# RLS-scoped structured-query runner
# ---------------------------------------------------------------------------
#
# The host injects a callable that executes a structured single-table select
# inside ``acting_as_user``. The package passes table/field/filter/order data,
# never a statement or fragment.
#
# Contract:
#   * OPTIONAL. Unconfigured → non-super-admin structured reads fail closed.
#   * Signature (keyword-only, forward-compatible):
#         async runner(*, table, match, fields, order_by, limit, offset)
#             -> list[dict]
#   * Raises on DB error; the tool translates the exception into a human message.

_SCOPED_QUERY_RUNNER_KEY = "run_scoped_query"


def get_scoped_query_runner() -> Any:
    """Return the host-injected RLS structured-query runner, or None."""
    return _registry.get(_SCOPED_QUERY_RUNNER_KEY)


# ---------------------------------------------------------------------------
# Bookmark resolver (structured-input `input_list` bookmark materialization)
# ---------------------------------------------------------------------------
#
# A structured-input ``input_list`` may carry Matrx bookmarks (pointers to a
# user's saved list items). Resolving them to text needs the host's ownership-
# gated ReferenceOrchestrator bridge (`resolve_bookmarks`), which reads user
# data via matrx-orm — a layer this package must not import. The host injects
# the resolver here; matrx-ai calls it at materialization time.
#
# Contract:
#   * OPTIONAL. Unconfigured → ``get_bookmark_resolver()`` returns None and the
#     input_list resolves to NOTHING (standalone matrx-ai has no bookmark store);
#     never an error, never a raw aidream import.
#   * Signature (keyword-only, forward-compatible):
#         async resolver(bookmarks: list, *, user_id: str | None) -> list[str]
#     Ownership-gated: a bookmark the caller can't read yields nothing (fail
#     closed), never another user's items.

_BOOKMARK_RESOLVER_KEY = "bookmark_resolver"


def get_bookmark_resolver() -> Any:
    """Return the host-injected bookmark resolver, or None when unset."""
    return _registry.get(_BOOKMARK_RESOLVER_KEY)


# ---------------------------------------------------------------------------
# Referenceable-record loader (structured-input note/task snapshot resolution)
# ---------------------------------------------------------------------------
#
# A structured-input `input_note`/`input_task` may reference a user's saved
# note/task by id. Fetching it needs the host's ownership-gated loader
# (`load_referenceable_record`, runs inside acting_as_user / RLS), which reads
# user data via matrx-orm — a layer this package must not import.
#
# Contract:
#   * OPTIONAL. Unconfigured → ``get_referenceable_record_loader()`` returns None
#     and a referenced record resolves to a failure notice (standalone matrx-ai
#     has no note/task store); never an error, never a raw aidream import.
#   * Signature (positional, forward-compatible):
#         async loader(kind: str, record_id: str) -> Any | None
#     Ownership-gated: a record the caller can't read yields None (fail closed).

_REFERENCEABLE_RECORD_LOADER_KEY = "referenceable_record_loader"


def get_referenceable_record_loader() -> Any:
    """Return the host-injected referenceable-record loader, or None when unset."""
    return _registry.get(_REFERENCEABLE_RECORD_LOADER_KEY)
