"""THE SEND BOUNDARY — the one system that shapes a prompt before a provider call.

Why this module exists
----------------------
Prompt caching is worth 5-10x on input cost across a tool loop, and the cache
lives or dies on ONE property: the prefix (tools + system + the leading
messages) must be byte-stable between rounds. Every mutation applied to a
``UnifiedConfig`` between "the resolver handed it back" and "the provider
client got it" is therefore a potential cache killer.

For a while those mutations were scattered: the resolver trimmed WITH a
``cache_state`` (so the Phase-2 cache gate could protect a live prefix), while
the executor's in-loop trim called the same function with NO ``cache_state`` —
so an in-loop trim could rewrite the cached prefix on EVERY iteration to
reclaim a few thousand tokens, re-paying full input price for the rest of the
run. That is the class of hole this module closes for good.

The law (also written into
``common-docs/systems/agents/execution-runtime/STREAM-CONTRACT.md``):

    **Nothing shapes a prompt outside the send boundary.** Every mutation of
    the wire-facing message list, system prompt, or wire config between the
    ConversationResolver and the provider call happens INSIDE
    ``prepare_for_send``. ``trim_messages_context`` may be called from nowhere
    else. New shaping steps are added HERE, where the cache gate, the audit
    record and the guard all already apply.

Mechanically enforced by ``packages/matrx-ai/tests/test_send_boundary_guard.py``
— a static scan with an explicit allowlist. Adding a new hole makes the suite
red.

What it owns
------------
``prepare_for_send`` runs at two stages of one run:

``stage="resolve"`` — once, in ``ConversationResolver.from_conversation_id``:
  1. pin the system-prompt date to the conversation's ``created_at`` so the
     cacheable system prefix never wobbles across midnight / reload,
  2. relax a fulfilled persisted structured-output contract for a natural
     follow-up (with an explicit INFO audit),
  3. the cache-gated context trim,
  4. record the audit as ``AppContext.metadata["last_trim_report"]`` (which
     persistence lands on iteration 1's ``cx_request.trim_summary``).

``stage="loop"`` — every iteration, at the executor's actual send boundary:
  1. host reference-fence staging,
  2. the cache-gated context trim — SAME gate as the resolver's,
  3. record the audit as
     ``AppContext.metadata["trim_reports_by_iteration"][iteration]``,
  4. derive the provider prompt-cache routing key,
  5. build the clone-at-send wire config (picklist / fence materialization).

Cache state: the freshest evidence, not the stalest
---------------------------------------------------
``cx_conversation.cache_state`` is only refreshed when a request COMPLETES, so
inside a long tool loop the persisted ``last_response_at`` ages while the cache
is in fact being refreshed by every round. This module therefore keeps its own
per-loop record of the last send and overlays it on the persisted state. A
loop's second and later iterations always evaluate against a live cache — which
is precisely the case the old ungated in-loop trim was destroying.

Nothing here may break a send. Every step is individually best-effort: a step
that fails is announced (yellow) and skipped, never fatal.
"""

from __future__ import annotations

import logging
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.context_trim import TrimPolicy, TrimReport, trim_messages_context

logger = logging.getLogger(__name__)

STAGE_RESOLVE = "resolve"
STAGE_LOOP = "loop"

# Bounded in-process memories. Both are pure optimisations/observations: losing
# an entry costs a DB read or a more conservative gate decision, never
# correctness.
_MAX_TRACKED = 512
_CACHE_STATE_MEMO: OrderedDict[str, dict[str, Any]] = OrderedDict()
_LAST_SEND_AT: OrderedDict[str, float] = OrderedDict()


@dataclass
class SendPrep:
    """What the send boundary did on this pass.

    ``wire_config`` is the clone-at-send config the caller must hand to the
    provider (and swap back off ``current_request`` afterwards); ``None`` means
    there was nothing to materialize and the canonical config goes on the wire.
    """

    stage: str
    trim_report: TrimReport | None = None
    wire_config: Any | None = None
    cache_state: dict[str, Any] | None = None
    steps: list[str] = field(default_factory=list)
    # What the context pre-flight measured (estimated tokens vs the model's
    # declared window). ``None`` = not measurable (no declared window) or
    # disabled; an over-window prompt never gets here — it raises.
    preflight: dict[str, Any] | None = None


async def prepare_for_send(
    config: Any,
    *,
    stage: str,
    conversation_id: str | None = None,
    request_id: str | None = None,
    iteration: int | None = None,
    conversation_row: Any | None = None,
    cache_state: dict[str, Any] | None = None,
    policy: TrimPolicy | None = None,
    user_input: Any = None,
    config_overrides: Any = None,
) -> SendPrep:
    """THE entry point. Shape ``config`` for the provider and audit what happened.

    Args:
        config: the canonical ``UnifiedConfig`` about to be sent.
        stage: ``STAGE_RESOLVE`` (pre-run, in the resolver) or ``STAGE_LOOP``
            (per-iteration, at the executor's send boundary).
        conversation_id / request_id: loop identity — used for the cache
            routing key and for the live cache-state overlay.
        iteration: 1-based iteration number; keys the per-iteration trim audit.
        conversation_row: the loaded ``cx_conversation`` row (resolve stage) —
            source of the system-date pin and of ``cache_state``.
        cache_state: explicit cache state override. When omitted the module
            resolves it (memo + live-send overlay).
        policy: trim policy override (tests); defaults to ``TrimPolicy()``.
        user_input / config_overrides: resolve-stage turn intent used to decide
            whether a completed structured contract may relax to text.

    Never raises for a SHAPING failure — a failing step is logged and skipped.
    The one deliberate exception is the context pre-flight: a prompt that
    provably cannot fit the model's window raises ``PromptTooLargeError`` here,
    before the provider is called and before anything is spent.
    """
    prep = SendPrep(stage=stage)

    if stage == STAGE_RESOLVE and conversation_row is not None:
        _run_step(prep, "pin_system_date", lambda: _pin_system_date(config, conversation_row))

    if stage == STAGE_RESOLVE:
        _run_step(
            prep,
            "response_format_followup",
            lambda: _apply_followup_response_format(
                config,
                user_input=user_input,
                config_overrides=config_overrides,
                prior_request_status=getattr(conversation_row, "last_request_status", None),
            ),
        )

    if stage == STAGE_LOOP:
        await _stage_reference_fences(prep, config)

    effective_cache_state = _resolve_cache_state(
        conversation_id=conversation_id,
        request_id=request_id,
        provided=cache_state,
        stage=stage,
    )
    prep.cache_state = effective_cache_state

    _run_step(
        prep,
        "context_trim",
        lambda: _gated_trim(
            prep,
            config,
            cache_state=effective_cache_state,
            policy=policy,
            stage=stage,
            iteration=iteration,
            conversation_id=conversation_id,
        ),
    )

    # PRE-FLIGHT — deliberately NOT inside ``_run_step``: every other step here
    # is best-effort and skippable, this one is a REFUSAL and must reach the
    # caller. It runs after the trim (so it measures what actually goes on the
    # wire) and before anything is sent.
    prep.preflight = _preflight(config, stage=stage, conversation_id=conversation_id)
    prep.steps.append("context_preflight")

    if stage == STAGE_LOOP:
        _run_step(
            prep,
            "prompt_cache_key",
            lambda: _set_prompt_cache_key(config, conversation_id, request_id),
        )
        _run_step(prep, "wire_config", lambda: _build_wire(prep, config))
        _mark_sent(conversation_id, request_id)

    return prep


# --------------------------------------------------------------------------- #
# Steps                                                                        #
# --------------------------------------------------------------------------- #


def _preflight(config: Any, *, stage: str, conversation_id: str | None) -> dict[str, Any] | None:
    """Measure the prompt against the resolved model's context window.

    Raises ``PromptTooLargeError`` when it provably does not fit (see
    ``matrx_ai.config.context_preflight``). Anything that goes wrong INSIDE the
    measurement (catalog unreachable, an unserializable part) yields a skip,
    announced by the module itself — never a blocked send.
    """
    from matrx_ai.config.context_preflight import PromptTooLargeError, check_prompt_fits

    step = _step_name(conversation_id)
    try:
        return check_prompt_fits(config, step=step)
    except PromptTooLargeError as exc:
        vcprint(f"[send_boundary/{stage}] {exc}", color="red")
        raise


def _step_name(conversation_id: str | None) -> str:
    """The name the refusal points at: the workflow STEP when the call is made
    inside one, else the conversation it belongs to."""
    try:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001
        ctx = None
    if ctx is not None:
        node_id = (ctx.metadata or {}).get("workflow_node_id")
        if node_id:
            run_id = getattr(ctx, "execution_id", None) or ""
            return f"{node_id} (workflow run {run_id})" if run_id else str(node_id)
    return f"conversation {conversation_id}" if conversation_id else "this call"


def _apply_followup_response_format(
    config: Any,
    *,
    user_input: Any,
    config_overrides: Any,
    prior_request_status: str | None,
) -> None:
    """Relax a completed one-answer JSON contract at the send boundary."""
    from matrx_ai.config.response_format import (
        response_format_transition_after_first_structured_answer,
    )

    transition = response_format_transition_after_first_structured_answer(
        config,
        user_input=user_input,
        config_overrides=config_overrides,
        prior_request_status=prior_request_status,
    )
    if transition is None:
        return

    config.response_format = {"type": "text"}
    try:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        if ctx is not None:
            transition["conversation_id"] = getattr(ctx, "conversation_id", None)
            transition["origin_class"] = getattr(ctx, "origin_class", None)
            ctx.metadata["response_format_transition"] = transition
    except Exception:  # observability can never change response behavior
        pass

    # vcprint, NOT logger.info (V-34, 2026-09-12): four live walks and this line was
    # in none of the server logs, because the host's logging config does not print
    # this module's logger while every other send-boundary fact goes out through
    # vcprint — which both prints and records. An announcement nobody can find is a
    # silent one. Still exactly ONE record, so the format transition is never
    # double-reported.
    vcprint(
        "[send_boundary/resolve] response_format_relaxed_after_first_structured_answer "
        f"conversation_id={transition.get('conversation_id')} from={transition['from']} "
        f"to=text reason={transition['reason']} origin_class={transition.get('origin_class')}",
        color="cyan",
    )


def _gated_trim(
    prep: SendPrep,
    config: Any,
    *,
    cache_state: dict[str, Any] | None,
    policy: TrimPolicy | None,
    stage: str,
    iteration: int | None,
    conversation_id: str | None,
) -> None:
    """The ONLY call site of ``trim_messages_context`` in the platform.

    Identical at both stages — same gate, same policy, same audit shape. That
    sameness IS the fix: an in-loop trim can no longer rebuild a live cached
    prefix for savings the resolver would have refused to take.
    """
    messages = getattr(config, "messages", None)
    if messages is None:
        return
    messages_list = messages if isinstance(messages, list) else list(messages)

    report = trim_messages_context(messages_list, policy=policy, cache_state=cache_state)
    prep.trim_report = report
    _record_trim_report(report, stage=stage, iteration=iteration)

    if report.blocks_rewritten:
        vcprint(
            f"[send_boundary/{stage}] context-trim rewrote {report.blocks_rewritten} "
            f"tool-result block(s) (freed {report.freed_chars} chars) "
            f"for {conversation_id}",
            color="yellow",
        )
    elif report.eligible_but_skipped_reason == "cache_protect":
        gate = (report.policy or {}).get("cache_gate") or {}
        vcprint(
            f"[send_boundary/{stage}] context-trim SKIPPED to protect a live prompt "
            f"cache (est {gate.get('est_savings_tokens')} tokens < "
            f"{gate.get('min_required_tokens')} required) for {conversation_id}",
            color="cyan",
        )


def _record_trim_report(report: TrimReport, *, stage: str, iteration: int | None) -> None:
    """Land the audit on AppContext in the shape persistence already reads.

    ``last_trim_report`` → iteration 1's ``cx_request.trim_summary``;
    ``trim_reports_by_iteration[n]`` → iteration n's row. See
    ``orchestrator/requests.py`` and ``db/persistence.py::_latest_trim_summary``.

    A no-op pass is not recorded (it would blank a meaningful row); a
    cache-protect SKIP is, because ``_refresh_cache_state`` accumulates
    ``cumulative_trimmable_chars`` from exactly those reports.
    """
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return
    if stage == STAGE_RESOLVE:
        ctx.metadata["last_trim_report"] = report.to_dict()
        return
    meaningful = bool(report.blocks_rewritten) or report.eligible_but_skipped_reason == (
        "cache_protect"
    )
    if iteration is None or not meaningful:
        return
    ctx.metadata.setdefault("trim_reports_by_iteration", {})[iteration] = report.to_dict()


async def _stage_reference_fences(prep: SendPrep, config: Any) -> None:
    """Resolve the host's in-content reference fences into the wire swaps.

    Per-send and in THIS task — the only placement that covers continue turns,
    current-turn user input, programmatic child agents, ``/resume`` and
    injection drains alike. Optional seam: unconfigured host → no stager.
    """
    try:
        from matrx_ai._ext import get_reference_fence_stager

        stager = get_reference_fence_stager()
    except Exception:  # noqa: BLE001 — optional seam, never fatal
        stager = None
    if stager is None:
        return
    try:
        await stager(config)
        prep.steps.append("reference_fences")
    except Exception as exc:  # noqa: BLE001
        vcprint(
            f"[send_boundary] reference fence stager failed (ignored): {type(exc).__name__}: {exc}",
            color="yellow",
        )


def _set_prompt_cache_key(config: Any, conversation_id: str | None, request_id: str | None) -> None:
    from matrx_ai.providers.cache_guard import provider_prompt_cache_key

    config.prompt_cache_key = provider_prompt_cache_key(conversation_id, request_id)


def _build_wire(prep: SendPrep, config: Any) -> None:
    """Clone-at-send: swap placeholder tokens / fences for their real values.

    The canonical config keeps the placeholders so the secret never reaches
    persistence, snapshots, or the conversation labeler.
    """
    from matrx_ai.config.picklist_runtime import build_wire_config

    prep.wire_config = build_wire_config(config)


def _pin_system_date(config: Any, conversation_row: Any) -> None:
    """Freeze the system-prompt date to the conversation's ``created_at``.

    The "Current date" decoration is pinned ONCE per conversation to an
    immutable, already-persisted anchor so the cacheable system prefix never
    changes — not between loop rounds, not across midnight, not across a DB
    reload. Best-effort: if anything is missing we leave ``date_anchor`` unset
    and SystemInstruction falls back to a single memoized ``now()``.
    """
    si = getattr(config, "system_instruction", None)
    if si is None or getattr(si, "date_anchor", None):
        return
    created = getattr(conversation_row, "created_at", None)
    if created is None:
        return
    if isinstance(created, str):
        # Persisted ISO timestamp — the date is the leading 10 chars.
        anchor = created[:10]
    else:
        try:
            anchor = created.strftime("%Y-%m-%d")
        except Exception:  # noqa: BLE001
            return
    if len(anchor) == 10:
        si.date_anchor = anchor


def _run_step(prep: SendPrep, name: str, fn: Any) -> None:
    """Run one shaping step; a failure is announced and skipped, never fatal."""
    try:
        fn()
        prep.steps.append(name)
    except Exception as exc:  # noqa: BLE001 — the send must stay available
        vcprint(
            f"[send_boundary/{prep.stage}] step {name!r} failed (ignored): "
            f"{type(exc).__name__}: {exc}",
            color="yellow",
        )


# --------------------------------------------------------------------------- #
# Cache state — freshest evidence wins                                         #
# --------------------------------------------------------------------------- #


def _loop_key(conversation_id: str | None, request_id: str | None) -> str:
    return f"{request_id or 'unknown-request'}:{conversation_id or 'unknown-conversation'}"


def remember_cache_state(conversation_id: str | None, cache_state: dict[str, Any] | None) -> None:
    """Memoize a conversation's persisted cache state for the rest of the run.

    The resolver reads the row once; the loop then evaluates the gate every
    iteration without a DB round-trip.
    """
    if not conversation_id or not cache_state:
        return
    _CACHE_STATE_MEMO[conversation_id] = dict(cache_state)
    _CACHE_STATE_MEMO.move_to_end(conversation_id)
    while len(_CACHE_STATE_MEMO) > _MAX_TRACKED:
        _CACHE_STATE_MEMO.popitem(last=False)


def _mark_sent(conversation_id: str | None, request_id: str | None) -> None:
    key = _loop_key(conversation_id, request_id)
    _LAST_SEND_AT[key] = time.time()
    _LAST_SEND_AT.move_to_end(key)
    while len(_LAST_SEND_AT) > _MAX_TRACKED:
        _LAST_SEND_AT.popitem(last=False)


def _resolve_cache_state(
    *,
    conversation_id: str | None,
    request_id: str | None,
    provided: dict[str, Any] | None,
    stage: str,
) -> dict[str, Any] | None:
    """The cache state the gate should reason about on THIS send.

    Persisted state (refreshed only when a request completes) overlaid with
    this process's own record of the last send in this loop. Inside a live tool
    loop the overlay is the only accurate evidence — every round refreshes the
    provider cache, while the DB row keeps saying the last response was minutes
    ago.
    """
    if provided:
        remember_cache_state(conversation_id, provided)
    base = dict(provided or {})
    if not base and conversation_id:
        memo = _CACHE_STATE_MEMO.get(conversation_id)
        if memo:
            base = dict(memo)

    if stage == STAGE_LOOP:
        last_send = _LAST_SEND_AT.get(_loop_key(conversation_id, request_id))
        if last_send is not None:
            live_iso = datetime.fromtimestamp(last_send, UTC).isoformat()
            if _is_newer(live_iso, base.get("last_response_at")):
                base["last_response_at"] = live_iso
                base.setdefault("cache_state_source", "live_loop_send")

    return base or None


def _is_newer(candidate_iso: str, existing: Any) -> bool:
    if not existing:
        return True
    try:
        cand = datetime.fromisoformat(candidate_iso)
        prev = datetime.fromisoformat(str(existing).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return True
    if prev.tzinfo is None:
        prev = prev.replace(tzinfo=UTC)
    return cand > prev


def reset_loop_state(conversation_id: str | None = None, request_id: str | None = None) -> None:
    """Drop this loop's live-send record (housekeeping / tests)."""
    _LAST_SEND_AT.pop(_loop_key(conversation_id, request_id), None)
    if conversation_id:
        _CACHE_STATE_MEMO.pop(conversation_id, None)
