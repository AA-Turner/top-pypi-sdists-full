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
``common-docs/systems/architecture/execution-runtime/STREAM-CONTRACT.md``):

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
  2a. on host-enabled permanent threads, mark earlier turns' live-machine
     readings (fs_list, shell_execute, browser reads) stale with their own
     timestamp (``config/perishable_state.py``),
  3. the cache-gated context trim,
  4. record the audit as ``AppContext.metadata["last_trim_report"]`` (which
     persistence lands on iteration 1's ``cx_request.trim_summary``).

``stage="loop"`` — every iteration, at the executor's actual send boundary:
  1. host reference-fence staging,
  1a. the DOCUMENT OUTPUT-CEILING floor — a declared structured output whose
     schema cannot bound its own size reaches the provider at the model's real
     maximum, whatever a stored agent row says,
  2. the cache-gated context trim — SAME gate as the resolver's,
  3. record the audit as
     ``AppContext.metadata["trim_reports_by_iteration"][iteration]``,
  3a. stage the LIVE PLAN — the agent's open task list, restated in the
     MessageList tail channel so it rides after the newest tool result and
     after every cache breakpoint (``config/live_plan.py``),
  3b. check that the newest person turn, as every chat translator will compose it,
     ENDS with the person's typed text (``config/typed_text_last.py``, announced),
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
from copy import copy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.context_trim import (
    CacheGateInputs,
    TrimPolicy,
    TrimReport,
    trim_messages_context,
)

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
    # What the perishable-state step marked stale on this pass (resolve stage,
    # host-enabled conversations only). ``None`` = the step did not run.
    perishable_report: dict[str, Any] | None = None
    # What the live-plan step staged at the end of this send (loop stage only).
    # ``None`` = no open tasks / no host source / the step failed (announced).
    live_plan: dict[str, Any] | None = None
    # What rides after the person's typed text in this send's composed person turn (loop stage),
    # or ``None`` — the law holds (``config/typed_text_last.py``).
    typed_text_problem: str | None = None
    # THE message list this send renders (loop stage): the newest person turn ordered so it
    # ENDS with their typed text, this turn's platform block on its own turn before it
    # (``order_for_wire``). Computed ONCE, here; it is ``wire_config.messages`` and every chat
    # translator renders exactly it. ``None`` = nothing to order (no person turn).
    wire_messages: list[Any] | None = None


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
    organization_id: str | None = None,
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
        policy: explicit trim policy (tests). When omitted the policy is the
            ORGANIZATION's: resolved through the host's knob resolver
            (``context_trim.set_trim_policy_resolver``; ``agents.context_trim``)
            for ``organization_id`` — or, when that is not passed, the carried
            AppContext's organization. No host resolver → the ruled defaults.
        organization_id: the organization whose trim knobs apply.
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

    if stage == STAGE_RESOLVE and conversation_row is not None:
        # AFTER the pin (the stored text carries the pinned date line), BEFORE
        # anything else reads the prompt: a frozen conversation sends exactly
        # the prompt its row stores — the cache line law.
        _run_step(
            prep,
            "enforce_frozen_prompt",
            lambda: _enforce_frozen_prompt(
                config, conversation_row, conversation_id=conversation_id
            ),
        )

    if stage == STAGE_RESOLVE:
        # AFTER the pin: it reads the anchor the pin just set.
        _run_step(prep, "announce_live_date", lambda: _announce_live_date(config))

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

    if stage == STAGE_RESOLVE:
        # BEFORE the trim: a result the trim later clears carries no content to
        # recite, and marking first keeps the trim's own idempotence key intact.
        await _mark_perishable_state(prep, config, conversation_id=conversation_id)

    if stage == STAGE_LOOP:
        # FIRST, before anything reads the prompt: a mandate-held turn sends the
        # held system text its row froze, unless the Holder or the org catalog
        # really changed (then a deliberate, loud cache break). Here and not at
        # the resolve stage because the org catalog is injected AFTER the
        # resolver, by the host's context assembly.
        _run_step(
            prep,
            "settle_held_prompt",
            lambda: _settle_held_prompt(config, conversation_id=conversation_id),
        )
        await _stage_reference_fences(prep, config)
        await _enforce_document_output_ceiling(prep, config)

    effective_cache_state = _resolve_cache_state(
        conversation_id=conversation_id,
        request_id=request_id,
        provided=cache_state,
        stage=stage,
    )
    prep.cache_state = effective_cache_state

    if policy is None:
        policy = await _resolve_org_trim_policy(prep, organization_id)

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
        # REFUSAL, like the pre-flight: a call with no conversational message at all
        # is rejected by every provider ("messages: at least one message is required")
        # after a paid round-trip. Say so here, before anything is sent.
        _refuse_empty_conversation(config, conversation_id=conversation_id)
        prep.steps.append("empty_conversation_check")
        # AFTER the trim and the pre-flight (the block is small and rides the
        # tail, after every cache breakpoint), BEFORE the wire clone (which
        # deep-copies the staged tail along with the messages).
        await _stage_live_plan(
            prep, config, conversation_id=conversation_id, organization_id=organization_id
        )
        _run_step(
            prep,
            "prompt_cache_key",
            lambda: _set_prompt_cache_key(config, conversation_id, request_id),
        )
        _run_step(prep, "wire_config", lambda: _build_wire(prep, config))
        # THE REQUEST ENDS WITH WHAT THE PERSON TYPED (Arman, 2026-10-19): AFTER the wire clone
        # (it orders the materialized messages), the newest person turn is ordered ONCE, here,
        # for the provider this send goes to; translators only render it. The result is checked
        # and announced loudly, never fatal (``config/typed_text_last.py``).
        profile = await _send_profile(config, conversation_id=conversation_id)
        _run_step(
            prep,
            "typed_text_last",
            lambda: order_for_wire(config, profile, prep=prep, conversation_id=conversation_id),
        )
        # What this send is made of (after the trim, i.e. what really goes out),
        # kept for the request's completion to store on the conversation.
        _run_step(
            prep,
            "context_breakdown",
            lambda: _remember_breakdown(conversation_id, config),
        )
        _mark_sent(conversation_id, request_id)

    return prep


# --------------------------------------------------------------------------- #
# Steps                                                                        #
# --------------------------------------------------------------------------- #


def config_with_messages(config: Any, messages: list[Any]) -> Any:
    """A shallow copy of ``config`` carrying ``messages`` — for RECORDS, never the wire.

    Run history persists a turn the model never saw as a request (a local-model
    turn, a mirrored coding session). The config it files must carry the full
    transcript; building that copy is a message-list replacement, so it lives here,
    in the one module the guard allows to do it.
    """
    from copy import copy

    from matrx_ai.config.message_config import MessageList

    clone = copy(config)
    clone.messages = MessageList(_messages=list(messages))
    return clone


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


EMPTY_CONVERSATION_USER_MESSAGE = "There is nothing to send yet. Type a message and try again."


class EmptyConversationError(ValueError):
    """The call carries no user/assistant/tool message — only a system prompt (or
    nothing). Raised BEFORE the provider; nothing was sent or spent."""

    def __init__(self, *, step: str) -> None:
        message = (
            f"Send boundary REFUSED this call before the provider: {step} has no "
            "message to send (only a system prompt, or nothing). Nothing was sent "
            "and nothing was spent. The caller must supply a user message, or the "
            "agent must carry one of its own."
        )
        super().__init__(message)
        self.step = step
        # A full RetryableError (not a lookalike): the executor's failure path reads
        # is_retryable / details / retry_schedule off it, and a lookalike without them
        # turned this plain refusal into an AttributeError naming the lookalike.
        from matrx_ai.providers.errors import RetryableError

        self.error_info = RetryableError(
            error_type="empty_conversation",
            message=message,
            status_code=422,
            is_retryable=False,
            user_message=EMPTY_CONVERSATION_USER_MESSAGE,
        )


def _has_sendable_message(message: Any) -> bool:
    if isinstance(message, dict):
        role = str(message.get("role") or "")
        content = message.get("content")
        visible = message.get("is_visible_to_model", True)
    else:
        role = str(getattr(message, "role", "") or "")
        content = getattr(message, "content", None)
        visible = getattr(message, "is_visible_to_model", True)
    if role in ("system", "developer") or visible is False:
        return False
    if isinstance(content, str):
        return bool(content.strip())
    for block in content or ():
        text = block.get("text") if isinstance(block, dict) else getattr(block, "text", None)
        block_type = block.get("type") if isinstance(block, dict) else getattr(block, "type", None)
        if str(block_type or "") in ("text", "ContentType.TEXT") or text is not None:
            if isinstance(text, str) and text.strip():
                return True
            continue
        return True  # a non-text block (image, file, tool call/result) is content
    return False


def _refuse_empty_conversation(config: Any, *, conversation_id: str | None) -> None:
    """Raise ``EmptyConversationError`` when no message would reach the provider."""
    messages = getattr(config, "messages", None)
    if messages is None:
        return  # not a conversational config (nothing to judge)
    if any(_has_sendable_message(m) for m in messages):
        return
    exc = EmptyConversationError(step=_step_name(conversation_id))
    vcprint(f"[send_boundary/loop] {exc}", color="red")
    raise exc


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

    gate_inputs = None
    if cache_state:
        gate_inputs = _cache_gate_inputs(config, policy)
        if gate_inputs is not None and gate_inputs.rewrite_ttl_secs:
            # The history's REAL lifetime from the wire's marks wins over the
            # persisted provider default (cache_marks.history_cache_ttl).
            cache_state = {**cache_state, "est_cache_ttl_secs": gate_inputs.rewrite_ttl_secs}
            prep.cache_state = cache_state

    report = trim_messages_context(
        messages_list, policy=policy, cache_state=cache_state, gate_inputs=gate_inputs
    )
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
        if gate.get("rule") == "payback":
            why = (
                f"frees ~{gate.get('est_savings_tokens')} tokens worth "
                f"${gate.get('benefit_usd')} over {gate.get('expected_remaining_calls')} sends "
                f"< ${gate.get('rewrite_cost_usd')} to rewrite {gate.get('rewrite_tokens')} tokens"
            )
        else:
            why = (
                f"est {gate.get('est_savings_tokens')} tokens < "
                f"{gate.get('min_required_tokens')} required"
            )
        vcprint(
            f"[send_boundary/{stage}] context-trim HELD to protect a live prompt "
            f"cache ({gate.get('rule')}: {why}) for {conversation_id}",
            color="cyan",
        )


def _cache_gate_inputs(config: Any, policy: TrimPolicy | None) -> CacheGateInputs | None:
    """Catalog prices, the history's cache lifetime and the pre-flight numbers for
    the payback gate. Only built in payback mode (legacy needs none of it); any
    failure yields ``None`` and the gate announces its fallback."""
    if policy is None or policy.cache_gate_mode != "payback":
        return None
    from matrx_ai.config.cache_marks import history_cache_ttl
    from matrx_ai.config.context_preflight import (
        _declared_window,
        current_policy,
        estimate_prompt_tokens,
    )
    from matrx_ai.config.usage_config import _get_db_pricing_lookup, lookup_model_pricing

    model_ref = str(getattr(config, "matrx_model_name", None) or getattr(config, "model", "") or "")
    long_cache = bool(getattr(config, "extended_prompt_cache", False))
    inputs = CacheGateInputs(model=model_ref or None, long_cache=long_cache)
    try:
        inputs.estimated_prompt_tokens = estimate_prompt_tokens(config)
        window = _declared_window(model_ref) if model_ref else None
        if window:
            inputs.preflight_ceiling_tokens = int(window * current_policy().trip_fraction)
    except Exception as exc:  # noqa: BLE001 — measurement must never block a send
        vcprint(f"[send_boundary] payback gate could not measure the prompt: {exc!r}", color="yellow")
    try:
        offering = str(getattr(config, "routing_offering_id", None) or "")
        lookup = _get_db_pricing_lookup()
        pricing = lookup_model_pricing(lookup, offering_id=offering, model_name=model_ref)
        if pricing is None and offering:
            pricing = lookup_model_pricing(lookup, model_name=model_ref)
        if pricing is not None:
            tier = pricing.get_tier(inputs.estimated_prompt_tokens or 0)
            ttl_secs, write_tier, _prefix = history_cache_ttl(pricing.api or model_ref, long=long_cache)
            inputs.rewrite_ttl_secs = ttl_secs
            if tier is not None:
                read = tier.cache_hit_price if tier.cache_hit_price is not None else tier.cached_input_price
                if write_tier == "1h" and tier.cache_write_1h_price is not None:
                    write = tier.cache_write_1h_price
                elif tier.cache_write_5m_price is not None:
                    write = tier.cache_write_5m_price
                else:
                    # No write premium on this wire (OpenAI, Gemini implicit): a
                    # rewrite is billed as fresh input.
                    write = tier.input_price
                inputs.read_price = float(read)
                inputs.write_price = float(write)
    except Exception as exc:  # noqa: BLE001 — pricing must never block a send
        vcprint(f"[send_boundary] payback gate could not read prices: {exc!r}", color="yellow")
    return inputs


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


async def _enforce_document_output_ceiling(prep: SendPrep, config: Any) -> None:
    """THE DOCUMENT-CEILING FLOOR AT THE WIRE — the last place it can still hold.

    Arman's ruling (2026-09-12, ``matrx_ai.config.output_ceiling``) says a
    DOCUMENT output gets the model's real maximum, and until now it was enforced
    only where a ceiling is AUTHORED: agent birth
    (``agent_factory.directive``), the agent update surface
    (``agent_service.crud``) and an authored workflow step
    (``graph_nodes.mandates.hold_step``). Every call whose ceiling comes from a
    STORED agent row instead — ``ai.agent.start``, ``ai.mandate.start``,
    ``ai.agent.produce``, an assignment step, a batch job, any HTTP agent run —
    reached the provider at whatever number the row happened to carry, because
    nothing re-judged it at send time.

    That is how workflow run ``d44f53b6-2e8e-49fc-a660-d43b835bbc49`` died
    (2026-09-12 19:29Z, definition "Newsroom Desk", node ``n_cross``): its agent
    row, minted 56 minutes earlier by the meta-builder, carried
    ``max_output_tokens: 32000`` under a model whose real maximum is 128,000,
    with an output schema of five arrays of free-text objects. The reply stopped
    at exactly 32,000 tokens (``finish_reason: max_tokens``), the JSON never
    closed, and $1.10 of run spend was lost. A birth-time-only guard cannot
    save a row that was born before the ruling reached the server — and there
    are years of such rows.

    SCOPE, deliberately narrow: only a call that DECLARES a structured output
    whose schema cannot bound its own size (an array, or a free-form string).
    That case is total loss by construction — truncated JSON does not parse, so
    nobody gets a partial answer — and it is the same judgment in a chat as in
    a workflow. Free PROSE is left alone here: in a conversation a small prose
    ceiling is a legitimate cost knob the organization chose (law 6), and the
    author-time layers already treat prose-with-nowhere-to-continue as a
    document. An ABSENT ceiling is untouched for the same reason as everywhere
    else: the offering default applies and inventing a number here would be the
    silent default the platform forbids.

    Reconciles and screams, never raises — raising a ceiling is free (you are
    billed for tokens generated, not permitted), and one repair quiets itself
    for the rest of the loop because the canonical config now carries the
    maximum.
    """
    try:
        from matrx_ai.config.output_ceiling import (
            as_int,
            declared_output_schema,
            enforce_document_ceiling,
            model_output_maximum,
        )

        requested = as_int(getattr(config, "max_output_tokens", None))
        if requested is None:
            return
        schema = declared_output_schema(config)
        if schema is None:
            return
        model = getattr(config, "matrx_model_name", None) or getattr(config, "model", None)
        repairs = enforce_document_ceiling(
            config,
            model_max=await model_output_maximum(model),
            output_schema=schema,
            # Irrelevant with a declared schema (the schema decides), passed
            # explicitly so the call reads the same as the other three.
            continuable=False,
            key="max_output_tokens",
            label=f"the declared structured output of {model or 'this call'}",
        )
        if not repairs:
            return
        prep.steps.append("document_output_ceiling")
        for repair in repairs:
            vcprint(
                f"[send_boundary/{prep.stage}] {repair}",
                title="⚠️ SEND BOUNDARY: output ceiling raised to the model maximum",
                color="yellow",
                log_level="WARNING",
            )
        _announce_ceiling_raise(
            model=model, requested=requested, sent=getattr(config, "max_output_tokens", None),
            repairs=repairs,
        )
    except Exception as exc:  # noqa: BLE001 — a guard's lookup never breaks a send
        vcprint(
            "[send_boundary] document output-ceiling floor failed (ignored): "
            f"{type(exc).__name__}: {exc}",
            color="yellow",
        )


def _announce_ceiling_raise(*, model: Any, requested: int, sent: Any, repairs: list[str]) -> None:
    """Law 4: the raise reaches the CALLER, not only the server log.

    The ceiling may have come from an explicit request ``config_overrides`` —
    live 2026-10-01, ``max_output_tokens: 300`` went out at 65,536 with every
    sibling override applied and nothing in the stream, which reads as "the
    override was silently ignored". One warning per request: the repair quiets
    itself on later iterations because the canonical config now holds the max.
    """
    from matrx_connect.context.events import WarningPayload

    from matrx_ai.providers.outbound_params import send_client_warning

    send_client_warning(
        WarningPayload(
            code="setting_adjusted",
            system_message=" ".join(repairs),
            user_message=(
                f"Output limit raised from {requested:,} to {sent:,} so the structured "
                "answer is not cut off."
            ),
            level="low",
            recoverable=True,
            metadata={
                "model": str(model),
                "adjusted": [
                    {"key": "max_output_tokens", "requested": requested, "sent": sent}
                ],
            },
        ),
        name="send_boundary_ceiling_warning",
    )


def order_for_wire(
    config: Any,
    profile: Any,
    *,
    prep: SendPrep | None = None,
    conversation_id: str | None = None,
) -> SendPrep:
    """THE REQUEST ENDS WITH WHAT THE PERSON TYPED: the one home of the typed-text-last reorder.

    Orders the newest person turn of the send (``prep.wire_config`` when the wire clone exists,
    else ``config``) so it ends with their typed text, this turn's platform block riding its own
    turn before it (``config/typed_text_last.py`` owns the order). Both inputs are resolved
    here, never in a translator: whether the provider carries the block after the cache line
    (``provider_profiles.TURN_CONTEXT_AFTER_CACHE_LINE``) and whether the model rejects two user
    turns in a row (the profile's ``strict_role_alternation``; that model keeps the block in the
    documented system-message fallback). Mid tool loop the block is never re-sent.

    The ordered list is stored on ``prep.wire_messages`` and becomes ``prep.wire_config``'s
    message list (a shallow wire copy when there was none — the canonical config and its ledger
    are never touched). Every chat translator renders exactly that list
    (``BaseTranslator.messages_for_wire``). Guard: ``tests/test_send_boundary_guard.py`` (seam
    "typed-text-last reorder": nothing else calls this or ``place_before_typed_text``).
    """
    from matrx_ai.config.provider_profiles import (
        chat_provider_of,
        requires_strict_role_alternation,
        turn_context_after_cache_line,
    )
    from matrx_ai.config.typed_text_last import (
        announce_problem,
        place_before_typed_text,
        typed_text_problem,
    )

    prep = prep if prep is not None else SendPrep(stage=STAGE_LOOP)
    source = prep.wire_config if prep.wire_config is not None else config
    messages = getattr(source, "messages", None)
    provider = chat_provider_of(profile)
    if provider is None:
        # Not a chat turn (speech, image, decision…): its prompt fold keeps the raw list.
        return prep
    listed = list(messages or [])
    block = None
    if turn_context_after_cache_line(provider) and not requires_strict_role_alternation(profile):
        last = listed[-1] if listed else None
        role = getattr(last, "role", None)
        if str(getattr(role, "value", role) or "").lower() != "tool":
            render = getattr(messages, "render_turn_context", None)
            block = render() if callable(render) else None
    ordered, _placed = place_before_typed_text(listed, block)
    problem = typed_text_problem(ordered)
    prep.typed_text_problem = problem
    if problem:
        announce_problem(problem, conversation_id=conversation_id, stage=prep.stage)
    if ordered is listed:
        return prep
    prep.wire_messages = ordered
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    wire.messages = _wire_list(messages, ordered)
    prep.wire_config = wire
    return prep


def _wire_list(messages: Any, ordered: list[Any]) -> Any:
    """A wire ``MessageList`` carrying ``ordered`` and the ledger's per-turn side channels."""
    from matrx_ai.config.message_config import MessageList

    if not isinstance(messages, MessageList):
        return MessageList(_messages=list(ordered))
    wire = copy(messages)
    wire._messages = list(ordered)
    wire._deferred_empty_messages = list(messages._deferred_empty_messages)
    wire._turn_context_blocks = dict(messages._turn_context_blocks)
    return wire


async def _send_profile(config: Any, *, conversation_id: str | None) -> Any:
    """The model profile this send is routed to (catalog), or ``None`` — announced, never fatal.

    Read only when there is a person turn to order; the provider call resolves the same profile.
    """
    from matrx_ai.config.typed_text_last import person_turn_index

    if person_turn_index(list(getattr(config, "messages", None) or [])) is None:
        return None
    try:
        from matrx_ai.catalog.resolve import resolve_call_profile

        return await resolve_call_profile(
            str(getattr(config, "model", "") or ""),
            offering_id=getattr(config, "routing_offering_id", None),
        )
    except Exception as exc:  # noqa: BLE001 — the provider call raises its own routing error
        vcprint(
            f"[send_boundary] could not resolve the model profile for {conversation_id}: {exc!r} "
            "— the person turn is NOT ordered at the boundary",
            color="red",
        )
        return None


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
    anchor = _utc_date(created)
    if anchor is None:
        return
    if len(anchor) == 10:
        si.date_anchor = anchor


def _utc_date(created: Any) -> str | None:
    """``YYYY-MM-DD`` of ``created`` in UTC — the one clock the system date uses
    (``SystemInstruction.effective_date`` renders turn one in UTC too)."""
    if isinstance(created, str):
        try:
            created = datetime.fromisoformat(created.replace("Z", "+00:00"))
        except ValueError:
            return created[:10] if len(created) >= 10 else None
    try:
        if getattr(created, "tzinfo", None) is not None:
            created = created.astimezone(UTC)
        return created.strftime("%Y-%m-%d")
    except Exception:  # noqa: BLE001
        return None


def _enforce_frozen_prompt(
    config: Any, conversation_row: Any, *, conversation_id: str | None
) -> None:
    """THE CACHE LINE LAW at the send boundary (Arman, 2026-10-16).

    "NOTHING, other than the removal of LARGE tool outputs should ever modify
    text behind the cache line." For a conversation whose prompt is frozen, the
    row's ``system_instruction`` IS the cached system prefix — it is what turn
    one sent and what every later turn must send byte for byte. If the config
    about to be sent renders anything else (an in-process cached config that
    lost its organization catalog, a decoration added after freezing), this
    screams (RED banner + ``system_error`` capture, kind
    ``prompt_cache_line_violation``) and sends the stored prompt instead.

    A mandate-held conversation stores no prompt (its live Holder is re-rendered
    every turn by design), so there is nothing to compare and this is a no-op.
    """
    if not getattr(config, "system_prompt_frozen", False):
        return
    stored = getattr(conversation_row, "system_instruction", None)
    if not isinstance(stored, str) or not stored:
        return
    current = getattr(config, "resolved_system_instruction", None) or ""
    if current == stored:
        return
    from matrx_ai.providers.cache_guard import scream_cache_line_violation

    restored = _restored_prompt(config, stored)
    scream_cache_line_violation(
        kind="frozen_prompt_differs_from_row",
        conversation_id=conversation_id,
        request_id=None,
        prev_text=stored,
        new_text=current,
        where="matrx_ai.config.send_boundary.prepare_for_send",
    )
    config.system_instruction = restored


def _restored_prompt(config: Any, stored: str) -> Any:
    """The stored system text, as the config's ``system_instruction`` must carry it."""
    import re

    from matrx_ai.instructions.core import SystemInstruction

    restored: Any = SystemInstruction.from_value(stored)
    # The stored text names the date turn one rendered; pin to THAT, not to a
    # re-derived one (conversation a1740422 sent "2026-10-15" on a prompt
    # stored with "2026-10-14").
    stored_date = re.search(r"Current date: (\d{4}-\d{2}-\d{2})", stored[:200])
    if isinstance(restored, SystemInstruction):
        restored.date_anchor = (
            stored_date.group(1)
            if stored_date
            else getattr(getattr(config, "system_instruction", None), "date_anchor", None)
        )
    if str(restored) != stored:
        # The stored text does not round-trip through SystemInstruction (a date
        # line it would re-render): send the stored bytes verbatim.
        restored = stored
    return restored


def _settle_held_prompt(config: Any, *, conversation_id: str | None) -> None:
    """THE CACHE LINE LAW on a mandate-held conversation (Arman, 2026-10-16).

    A held thread re-resolves its LIVE Holder every turn (belt, model, rebound
    mandate — ``agents/live_structure.py``), and until now that re-rendered the
    system text every turn too: the per-turn framing values and a rebuilt org
    catalog sat in front of the whole cached history (thread 3af9e95c: a
    144,074-byte system block with a new sha256 on every turn). Settled once per
    turn, on the first send, after the host injected the catalog:

    * the row holds a frozen record whose Holder and catalog fingerprints match
      this turn -> send the record's text, byte for byte;
    * no record yet -> freeze this turn's text (persistence writes it back);
    * a fingerprint changed (the Holder was edited or rebound, or the org catalog
      changed) -> send the new text, freeze it, and say so LOUDLY as a
      deliberate cache break. Nothing else may change it.
    """
    state = getattr(config, "held_prompt", None)
    if not isinstance(state, dict) or state.get("settled"):
        return
    from datetime import UTC, datetime

    from matrx_ai.agents.live_structure import catalog_fingerprint

    live = getattr(config, "resolved_system_instruction", None) or ""
    fingerprint = {"holder": state.get("holder") or "", "catalog": catalog_fingerprint(config)}
    stored = state.get("stored")
    if not (isinstance(stored, dict) and isinstance(stored.get("text"), str) and stored["text"]):
        stored = None
    if (
        stored is not None
        and stored.get("holder") == fingerprint["holder"]
        and stored.get("catalog") == fingerprint["catalog"]
    ):
        if live != stored["text"]:
            config.system_instruction = _restored_prompt(config, stored["text"])
        state["record"] = dict(stored)
        state["outcome"] = "kept"
    else:
        state["record"] = {
            "text": live,
            **fingerprint,
            "frozen_at": datetime.now(UTC).isoformat(),
        }
        state["outcome"] = "frozen" if stored is None else "rerendered"
        if stored is not None:
            from matrx_ai.providers.cache_guard import deliberate_cache_break

            changed = [k for k in ("holder", "catalog") if stored.get(k) != fingerprint[k]]
            deliberate_cache_break(
                kind="held_prompt_rerendered",
                reason=" and ".join(
                    {"holder": "the Holder changed", "catalog": "the org catalog changed"}[k]
                    for k in changed
                ),
                conversation_id=conversation_id,
                prev_text=stored["text"],
                new_text=live,
                where="matrx_ai.config.send_boundary.prepare_for_send",
            )
    state["settled"] = True


#: The turn-context slot the live date travels in (its own slot, so no other
#: contributor's block can delete it — see ``MessageList.attach_turn_context``).
LIVE_DATE_SLOT = "live_date"


def _announce_live_date(config: Any, *, now: datetime | None = None) -> None:
    """Tell the model the live instant on every turn (and name a stale pinned date).

    The system prefix's ``Current date`` is pinned to the conversation's
    ``created_at`` so the cached prefix stays byte-stable (``_pin_system_date``).
    That is right for one day and a lie on every day after it: a permanent
    thread — the Personal Staff thread lives for months — kept telling its model
    "Current date: 2026-09-22" on 09-28. On 2026-09-28 22:59Z test@test.com's
    Chief of Staff, whose own profile said "Monday, September 28", answered
    "Saturday, September 26" (Lane AZ2): the prefix said the 22nd, the thread
    said the 26th, and the model trusted the history.

    The fix keeps the cache: the prefix is untouched, and TODAY travels in the
    per-turn context channel (an uncached second system block), naming the
    pinned line for what it is. The date and time an agent states must always
    be the live ones.
    """

    si = getattr(config, "system_instruction", None)
    if si is None or not getattr(si, "include_date", False):
        return
    messages = getattr(config, "messages", None)
    attach = getattr(messages, "attach_turn_context", None)
    if attach is None:
        return
    moment = (now or datetime.now(UTC)).astimezone(UTC)
    today = moment.strftime("%Y-%m-%d")
    pinned = si.effective_date() if hasattr(si, "effective_date") else None
    # ALWAYS, not only when the pinned day is stale (Lane BC, 2026-10-03): a pin
    # that equals today IN UTC is still the wrong day for half the world for part
    # of every day — at 02:00Z it is yesterday evening in Los Angeles — so the
    # live instant travels on every turn and the person's own clock wins.
    began = (
        f'The "Current date: {pinned}" line in your instructions is the day this '
        f"conversation BEGAN, not today; never state it as the current date. "
        if pinned and pinned != today
        else ""
    )
    # 🚨 NO "Today is <UTC date>" HEADLINE (Lane BC, 2026-10-03 04:54Z): at 9:54 PM
    # Friday in Los Angeles the block opened "Today is Saturday, October 3" and the
    # Chief said Saturday, although its profile said Friday. The UTC date is named
    # only as the UTC reading of the instant, and the person's own date wins.
    attach(
        f"The current moment is {moment:%Y-%m-%dT%H:%MZ} (UTC). In UTC that falls on "
        f"{moment:%A}, {moment:%B} {moment.day}, {moment.year}, but the date and day "
        f"depend on the time zone. When your instructions give the person's own local "
        f"time, state THAT date, day and time to them, never the UTC ones. {began}"
        f"Never state a date or time remembered from earlier in this conversation as "
        f"the current one.",
        slot=LIVE_DATE_SLOT,
    )


async def _resolve_org_trim_policy(prep: SendPrep, organization_id: str | None) -> TrimPolicy:
    """The organization's trim policy (``agents.context_trim`` knobs via the host).

    The organization is the one the caller passes, else the one the carried
    AppContext holds — read, never rebuilt. A resolver failure is announced in
    red by ``resolve_trim_policy`` and the audit carries the fallback source.
    """
    from matrx_ai.config.context_trim import resolve_trim_policy

    org = organization_id
    if org is None:
        try:
            from matrx_ai.context.app_context import try_get_app_context

            ctx = try_get_app_context()
            org = getattr(ctx, "organization_id", None) if ctx is not None else None
        except Exception:  # noqa: BLE001 — no carried context is a legal standalone call
            org = None
    try:
        policy = await resolve_trim_policy(str(org) if org else None)
    except Exception as exc:  # noqa: BLE001 — a malformed resolver result, announced
        vcprint(
            f"[send_boundary/{prep.stage}] trim policy resolution failed for organization "
            f"{org!r} ({type(exc).__name__}: {exc}); using the ruled defaults",
            color="red",
        )
        return TrimPolicy(source="package_default:resolver_failed")
    prep.steps.append("trim_policy")
    return policy


async def _mark_perishable_state(
    prep: SendPrep, config: Any, *, conversation_id: str | None
) -> None:
    """Mark earlier turns' live-machine readings stale — host-enabled threads only.

    See ``config/perishable_state.py``. The host decides which conversations are
    permanent (``_ext.get_perishable_state_marker``); unconfigured or False →
    nothing happens. A failure is announced and skipped, never fatal.
    """
    from matrx_ai._ext import get_perishable_state_marker
    from matrx_ai.config.perishable_state import mark_perishable_state

    decider = get_perishable_state_marker()
    if decider is None or not conversation_id or not getattr(config, "messages", None):
        return
    try:
        if not await decider(conversation_id=str(conversation_id)):
            return
        report = mark_perishable_state(config.messages)
    except Exception as exc:  # noqa: BLE001 — shaping never costs a send
        vcprint(
            f"[send_boundary/{prep.stage}] step 'perishable_state' failed (ignored): "
            f"{type(exc).__name__}: {exc} — earlier workspace readings replay unmarked "
            "this turn.",
            color="yellow",
        )
        return
    prep.perishable_report = report.to_dict()
    prep.steps.append("perishable_state")
    if report.blocks_marked:
        vcprint(
            f"[send_boundary/{prep.stage}] {conversation_id}: marked "
            f"{report.blocks_marked} earlier-turn workspace reading(s) stale "
            f"({', '.join(sorted(set(report.tools)))}).",
            color="cyan",
        )


async def _stage_live_plan(
    prep: SendPrep, config: Any, *, conversation_id: str | None, organization_id: str | None
) -> None:
    """Restate the agent's open task list at the END of this send (``config/live_plan.py``).

    Rides the MessageList tail channel: after the newest tool result and after the
    rolling cache breakpoint, never in the system prompt, never persisted. A failure
    is announced and skipped — the send goes out without the block.
    """
    from matrx_ai.config.live_plan import LIVE_PLAN_SLOT, stage_live_plan

    org = organization_id
    if org is None:
        try:
            from matrx_ai.context.app_context import try_get_app_context

            ctx = try_get_app_context()
            org = getattr(ctx, "organization_id", None) if ctx is not None else None
        except Exception:  # noqa: BLE001 — no carried context is a legal standalone call
            org = None
    try:
        prep.live_plan = await stage_live_plan(
            config,
            conversation_id=conversation_id,
            organization_id=str(org) if org else None,
        )
    except Exception as exc:  # noqa: BLE001 — shaping never costs a send
        attach = getattr(getattr(config, "messages", None), "attach_tail_context", None)
        if attach is not None:
            attach("", slot=LIVE_PLAN_SLOT)
        vcprint(
            f"[send_boundary/{prep.stage}] step 'live_plan' failed (ignored): "
            f"{type(exc).__name__}: {exc} — this send goes out without the agent's "
            "task list at the end of its context.",
            color="yellow",
        )
        return
    prep.steps.append("live_plan")


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
        # LOUD, not only on the console: an ERROR line with the traceback reaches app_log, so a
        # step that fails on every send (``context_breakdown`` failed 344 times unseen) is seen.
        logger.error(
            "send_boundary step %r failed (ignored) at stage %s: %s: %s",
            name,
            prep.stage,
            type(exc).__name__,
            exc,
            exc_info=True,
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


#: The latest send's context breakdown per conversation, until the request's
#: completion stores it (``take_context_breakdown``). Bounded like _LAST_SEND_AT.
_LAST_BREAKDOWN: OrderedDict[str, dict[str, Any]] = OrderedDict()


def _remember_breakdown(conversation_id: str | None, config: Any) -> None:
    if not conversation_id:
        return
    from matrx_ai.config.context_breakdown import measure

    _LAST_BREAKDOWN[str(conversation_id)] = measure(config)
    _LAST_BREAKDOWN.move_to_end(str(conversation_id))
    while len(_LAST_BREAKDOWN) > _MAX_TRACKED:
        _LAST_BREAKDOWN.popitem(last=False)


def take_context_breakdown(conversation_id: str | None) -> dict[str, Any] | None:
    """The last send's breakdown for this conversation, removed once taken."""
    if not conversation_id:
        return None
    return _LAST_BREAKDOWN.pop(str(conversation_id), None)


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
