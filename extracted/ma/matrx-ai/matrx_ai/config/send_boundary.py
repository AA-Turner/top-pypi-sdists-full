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

Mechanically enforced by ``tests/package_host_contracts/test_send_boundary_guard.py``
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
  1b. the ANSWER RESERVE — a call that will think keeps a reserved share of its
     output limit for the visible answer: the thinking budget is capped where the
     provider takes one, else the limit is raised (``config/answer_room.py``),
  2. the cache-gated context trim — SAME gate as the resolver's,
  3. record the audit as
     ``AppContext.metadata["trim_reports_by_iteration"][iteration]``,
  3a. stage the LIVE PLAN — the agent's open task list, restated in the
     MessageList tail channel so it rides after the newest tool result and
     after every cache breakpoint (``config/live_plan.py``),
  3a''. stage the TOOL BRIEFINGS — what a held tool family works on (the records tools: the
     index of the organization's tables), in the per-turn context channel, once per turn
     (``config/tool_briefings.py``),
  3a'. stage WHO MADE THIS AGENT — AI Matrx and the catalog lab of the model
     answering, in the per-turn context channel (``config/agent_identity.py``),
  3b. check that the newest person turn, as every chat translator will compose it,
     ENDS with the person's typed text (``config/typed_text_last.py``, announced),
  4. derive the provider prompt-cache routing key,
     and decide which cache marks the send writes (``config/cache_plan.py``),
  5. build the clone-at-send wire config (picklist / fence materialization),
  5a. voice the PERSON's attachment-only turns (a file or skill sent with no words) with one
     host-marked line on the wire copy only — never stored as hers (``_voice_attachment_only_turns``),
  5b. FIT THE WIRE — the built wire is measured against every limit again and made to fit
     (``_fit_wire``; #136: replayed kept page blocks pushed a "fitting" call over the host cap);
     what a wire fit once dropped or stubbed stays dropped/stubbed on every later send of the
     conversation (``_REPLAYED_CONTEXT_DROPPED``, ``_WIRE_TEXT_STUBS``), so the prefix never flips,
  6. LAST, the caller's REQUEST FIREWALL on the exact wire config — a refusal, never
     skipped (``config/request_firewall.py::check_at_send``).

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

import asyncio
import hashlib
import json
import logging
import re
import time
import weakref
from collections import OrderedDict
from contextvars import ContextVar
from copy import copy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from matrx_connect.chat_timing import chat_timing_mark
from matrx_utils import vcprint

from matrx_ai.config.context_trim import (
    CacheGateInputs,
    TrimPolicy,
    TrimReport,
    trim_messages_context,
)
from matrx_ai.config.served_via import served_via_kwargs

logger = logging.getLogger(__name__)

STAGE_RESOLVE = "resolve"
STAGE_LOOP = "loop"

# Bounded in-process memories. Both are pure optimisations/observations: losing
# an entry costs a DB read or a more conservative gate decision, never
# correctness.
_MAX_TRACKED = 512
_CACHE_STATE_MEMO: OrderedDict[str, dict[str, Any]] = OrderedDict()
_LAST_SEND_AT: OrderedDict[str, float] = OrderedDict()


#: ``SendPrep.history_ttl_secs`` before it is read (``_prep_history_ttl``).
_TTL_UNSET = object()


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
    # What the make-it-fit step measured and did (``config/input_fit.py``); ``None`` = no limit known.
    fit: dict[str, Any] | None = None
    # The settings applied for THIS call only (``one_call``, loop stage) — the cache guard reads them as a
    # declared change of the wire head (the empty-reply retry turns reasoning off). ``None`` = none.
    one_call_settings: dict[str, Any] | None = None
    # What the perishable-state step marked stale on this pass (resolve stage,
    # host-enabled conversations only). ``None`` = the step did not run.
    perishable_report: dict[str, Any] | None = None
    # The history window's cache decision on this pass (``warm``, the ``previous`` recorded cut, ``waits`` — the
    # cold-cache knob), shared with the stale markers so both move on ONE decision. ``None`` = no window ran.
    history_cut_context: dict[str, Any] | None = None
    # The earlier sends' trim rewrites made again on this pass (``context_trim.replay_trim_rewrites``):
    # ``{"results", "arguments", "present"}``. ``None`` = nothing recorded for this conversation.
    trim_replay: dict[str, Any] | None = None
    # Each prefix-shaping step's own decision this pass (``history_window``, ``stale_markers``), read by
    # ``_record_prefix`` to say whether the message prefix the provider cached was HELD or MOVED, and why.
    prefix_parts: dict[str, dict[str, Any]] = field(default_factory=dict)
    # That verdict (``history_cut.prefix`` on the request row and in the latency row's ``cache_outcome``).
    prefix: dict[str, Any] | None = None
    # The lifetime of the cache that covers the history, from the wire's real marks (``_history_ttl_secs``) — the
    # same number the payback trim gate uses — so the window, the markers and the verdict test warm/cold on the
    # TTL the gate does. ``_TTL_UNSET`` = not read yet this pass; ``None`` = no fact (the saved default stands).
    history_ttl_secs: Any = _TTL_UNSET
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
    # Which cache marks this send writes and why (loop stage; ``config/cache_plan.py``).
    cache_plan: Any | None = None
    # What the assistant-turn media carry moved on this send (loop stage): one record per part
    # (``kind``, ``file_id``, the assistant turn ``at``, ``merged`` into the next person turn for a
    # strict-alternation model). ``None`` = nothing moved (``config/assistant_turn_media.py``).
    carried_media: list[dict[str, Any]] | None = None
    # The homed blocks this send could not carry whole (``attached_files`` module header): a held
    # copy whose home the window cut (``why: "cut"``) or a homed block the fit step stubbed
    # (``why: "stubbed"``), each ``{"kind", "key", "why", "note_rewritten"?}``. ``None`` = none.
    homed_off_wire: list[dict[str, Any]] | None = None
    # This send's per-message digests (``_prefix_digests``, loop stage) and what comparing them with the previous
    # send found (``_check_prefix_bytes``): ``{"compared", "first_difference", "against"}``. ``None`` = not compared.
    message_digests: list[str] | None = None
    prefix_bytes: dict[str, Any] | None = None
    # The late tool definitions this send offers in turn context (loop stage; ``late_tools:<wire name>`` -> block),
    # set when the boundary carries them (``order_for_wire``). After the fit each must be on the wire WHOLE
    # (``_settle_late_tools_on_wire``); the ones that were not and went out in the newest turn: ``late_tools_resent``.
    late_tools_expected: dict[str, str] | None = None
    late_tools_resent: list[str] | None = None


def _loop_mark(stage: str, key: str, label: str) -> None:
    """A stage mark on the request's latency ledger (matrx-connect ``chat_timing``, block ``send_prep``) — loop
    stage only: the resolve stage runs inside the history load and must not close its segments."""
    if stage == STAGE_LOOP:
        chat_timing_mark(key, label)


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
    history_len: int | None = None,
    one_call: dict[str, Any] | None = None,
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
        history_len: how many of ``config.messages`` are the PERSISTED history (resolve stage; the
            rest is this turn's input) — the part the history window may cut.
        one_call: settings for THIS call only (loop stage), e.g. the empty-reply retry's reasoning
            off. Every later step sees them; they reach the provider on ``prep.wire_config`` and
            never the stored chat (CGU-10 IMG6 #1).

    Never raises for a SHAPING failure — a failing step is logged and skipped.
    The one deliberate exception is the context pre-flight: a prompt that
    provably cannot fit the model's window raises ``PromptTooLargeError`` here,
    before the provider is called and before anything is spent.

    A RAISED OUTPUT LIMIT RIDES THE WIRE, NEVER THE CHAT (CGU-10 IMG5 #8, 2026-11-11): the
    document-ceiling floor and the answer reserve raise ``max_output_tokens`` / clamp
    ``thinking_budget`` for THIS call. The raised values reach the provider on
    ``prep.wire_config`` and the canonical config gets the author's values back before this
    returns (or raises), so nothing stores the raise and the next turn starts from the
    author's limit (it grew 1,500 → 2,250 → 3,375 stored before). Guard:
    ``tests/test_a_raised_output_limit_is_never_stored.py``.

    THE SAME FOR EVERY ONE-CALL SETTING (CGU-10 IMG6 #1): the empty-reply retry's reasoning off
    arrives as ``one_call`` and rides the wire the same way; the canonical config (what the chat
    stores) leaves this function exactly as it came. Guard:
    ``tests/test_the_send_boundary_never_writes_the_stored_config.py``.
    """
    # ONE BOUNDARY AT A TIME PER CONFIG OBJECT (CGU-10 IMG6 #8): the raise-then-restore below is only
    # correct when no second send on the SAME canonical config reads it mid-raise. Two sends at once on
    # one shared config stored 2,250 and sent 3,375 / an unreserved 1,500. The resolver deep-copies the
    # config per request, so a chat never waits here; a caller that shares one object is serialized.
    lock = _boundary_lock(config) if stage == STAGE_LOOP else None
    held_token = None
    if lock is not None:
        # A NESTED send on the same config (a stage hook that runs a model on its parent's config, or a
        # task it starts) would wait for a lock its own caller holds — forever: ``asyncio.Lock`` is not
        # re-entrant, and re-entering would read the outer send's raised limits as authored. Refused
        # loudly instead (CGU-10 IMG7 #6). The context variable is copied into child tasks, so a task the
        # hook starts is refused the same way.
        held = _HELD_CONFIGS.get()
        if id(config) in held and lock.locked():
            raise NestedSendError(
                "prepare_for_send: a send on this config is already inside its own send boundary "
                f"(conversation {conversation_id!r}, request {request_id!r}). A nested model call must use "
                "its own config (``for_child_call``), never its parent's — waiting here would hang the turn."
            )
        await lock.acquire()
        held_token = _HELD_CONFIGS.set(held | {id(config)})
    authored = _authored_output_limits(config) if stage == STAGE_LOOP else None
    prep = SendPrep(stage=stage)
    try:
        if stage == STAGE_LOOP:
            # FIRST, before anything reads or clones the messages: a person's inline-only media is
            # stored so its wire label names the real file id (CGU-10 AND-IMG12 #2).
            await _store_person_inline_media(prep, config)
            _loop_mark(stage, "sb_media_stored", "send boundary: person inline media stored")
        if stage == STAGE_LOOP and one_call:
            for name, value in one_call.items():
                if name not in _OUTPUT_LIMIT_FIELDS:
                    raise ValueError(f"one_call setting {name!r} is not a per-call field ({_OUTPUT_LIMIT_FIELDS})")
                setattr(config, name, value)
            prep.one_call_settings = dict(one_call)
            prep.steps.append("one_call_settings")

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
            # HOW FAR BACK THIS CONVERSATION READS — a declared stage, here and nowhere else (B2,
            # 2026-10-30). FIRST of the history shaping: the markers and the trim see what is sent.
            # The cut moves only when the provider cache is already cold; a moved cut is recorded.
            await _apply_history_window(
                prep, config, conversation_id=conversation_id, cache_state=cache_state, history_len=history_len
            )

        if stage == STAGE_RESOLVE:
            # AFTER the window (it decides which messages are sent), BEFORE the markers and the trim: every
            # rewrite an earlier send's trim made is made again, whether or not THIS send's trim runs — the
            # history reloads pristine from the database, and a held trim used to send back in full what the last
            # send had cleared (2026-11-19, staff thread 3af9e95c: every warm ask re-wrote ~55k of history).
            if policy is None:
                policy = await _resolve_org_trim_policy(prep, organization_id)
            _run_step(
                prep,
                "trim_replay",
                lambda: _replay_trims(prep, config, conversation_id=conversation_id, cache_state=cache_state, policy=policy),
            )

        if stage == STAGE_RESOLVE:
            # BEFORE the trim: a result the trim later clears carries no content to
            # recite, and marking first keeps the trim's own idempotence key intact.
            # They move on the window's cold-cache decision: while warm, exactly the recorded markers are replayed.
            await _mark_perishable_state(prep, config, conversation_id=conversation_id, cache_state=cache_state)

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
            await _enforce_document_output_ceiling(
                prep, config, conversation_id=conversation_id, request_id=request_id
            )
            # AFTER the document floor (it may already have raised the limit to the model's maximum):
            # THINKING NEVER TAKES THE ANSWER'S ROOM — a call that will think keeps a reserved share of
            # its output limit for the visible answer, on every provider (``config/answer_room.py``).
            await _reserve_answer_room(prep, config, conversation_id=conversation_id, request_id=request_id)
            _loop_mark(stage, "sb_shaped", "send boundary: held prompt, fences, output ceiling, answer room")

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
        # HELD OR MOVED, AND WHY — every send says whether the message prefix the provider cached was rebuilt byte
        # for byte or deliberately changed (``history_cut.prefix`` → the request row and ``cache_outcome``).
        _run_step(prep, "prefix_outcome", lambda: _record_prefix(prep, config, stage=stage, iteration=iteration, conversation_id=conversation_id))

        _loop_mark(stage, "sb_trimmed", "send boundary: cache state + trim policy + context trim")
        # MAKE IT FIT — the call is measured against EVERY limit that applies (the model's window
        # and the host's per-call input budget); when over, compaction runs first (the host's
        # summarization system, ``input_fit.set_compactor``) and a forced trim is the fallback.
        # Before this step only the window was measured and nothing shrank a call to fit a lower
        # host limit (conversation 9b224bf5, 2026-10-22). ``matrx_ai/config/input_fit.py``.
        try:
            from matrx_ai.config.input_fit import ensure_fits

            prep.fit = await ensure_fits(
                config, policy=policy, stage=stage, conversation_id=conversation_id, trim=_forced_trim_for(conversation_id, config)
            )
            prep.steps.append("input_fit")
            if prep.fit is not None:
                _record_fit(prep.fit, stage=stage, iteration=iteration)
        except Exception as exc:  # noqa: BLE001 — the pre-flight / host guard still decide
            vcprint(f"[send_boundary/{stage}] input_fit failed (ignored): {type(exc).__name__}: {exc}", color="red")
            logger.error("send_boundary input_fit failed at stage %s", stage, exc_info=True)

        _loop_mark(stage, "sb_fit", "send boundary: input fit measured")
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
            # WHO MADE THIS AGENT (Arman, 2026-10-26): the per-turn context channel, rebuilt
            # from the model about to answer on every send — never the frozen prefix
            # (``config/agent_identity.py`` header). BEFORE the wire clone.
            await _stage_agent_identity(prep, config, organization_id=organization_id)
            # WHAT THE PERSON ASKED US TO REMEMBER (CGU-10): their saved memories and custom
            # instructions, in the per-turn context channel — never in a temporary chat they did not
            # opt in, never in a confidential one (``config/person_context.py``). BEFORE the wire clone.
            await _stage_person_context(prep, config)
            # WHERE THIS RUN IS RUNNING (2026-11-17): the system-generated ENVIRONMENT block, from the
            # run's real client/runtime signals and live tool set, AFTER the person's memories so a
            # memory written for another environment never outranks it (``config/run_environment.py``).
            await _stage_run_environment(prep, config)
            # AFTER the trim and the pre-flight (the block is small and rides the
            # tail, after every cache breakpoint), BEFORE the wire clone (which
            # deep-copies the staged tail along with the messages).
            await _stage_live_plan(
                prep, config, conversation_id=conversation_id, organization_id=organization_id
            )
            # THE AGENT ALWAYS KNOWS ITS HELPERS (Arman, 2026-10-28): every helper it started, with
            # its live state, rebuilt on every send in the per-turn context channel
            # (``config/helper_roster.py``). BEFORE the wire clone.
            await _stage_helper_roster(
                prep, config, conversation_id=conversation_id, organization_id=organization_id
            )
            # WHAT THE RUN'S TOOLS WORK ON (2026-11-14): a run holding a tool family the host registered
            # a briefing for (the records tools: the index of the organization's tables) is handed it
            # in the per-turn context channel, rendered once per turn (``config/tool_briefings.py``).
            # BEFORE the wire clone.
            await _stage_tool_briefings(prep, config)
            _loop_mark(stage, "sb_turn_context_staged", "send boundary: identity, memories, environment, plan, helpers, briefings")
            _run_step(
                prep,
                "prompt_cache_key",
                lambda: _set_prompt_cache_key(config, conversation_id, request_id),
            )
            # BEFORE the wire clone (which copies the field): which cache marks this send
            # writes — a mark nothing will read is a pure write surcharge (config/cache_plan.py).
            _run_step(prep, "prompt_cache_marks", lambda: _set_prompt_cache_marks(prep, config))
            _run_step(prep, "wire_config", lambda: _build_wire(prep, config))
            # AFTER the wire clone, BEFORE the person-turn ordering: a person turn that carries only
            # what she attached (no words) gets the host's marked line on the WIRE copy only, so no
            # provider sees an empty turn and nothing is ever stored as her words.
            _run_step(prep, "attachment_only_turns", lambda: _voice_attachment_only_turns(prep, config))
            # A STOPPED REPLY CUT INSIDE AN OPEN FENCE / MATH / SVG / HTML ROOT is closed on the WIRE copy only, with a
            # one-line note, so "continue" starts cleanly instead of inside the code (``config/stopped_turn.py``).
            _run_step(prep, "stopped_turn_regions", lambda: _close_stopped_turns(prep, config))
            # A RUN-END NOTICE ("ALL TOOLS ARE NOW DISABLED", "only this one reply fits") the person has spoken after is
            # spent: on the WIRE copy only it says that run is over, so "continue" really resumes
            # (``config/spent_run_notices.py``, P8-RUNS 2026-11-15).
            _run_step(prep, "spent_run_notices", lambda: _retire_spent_run_notices(prep, config))
            # THE FILE RULE (Arman, 2026-11-09): AFTER the wire clone, BEFORE the person-turn ordering:
            # each attached file the host decided goes whole rides in its OWN block at the start of the
            # turn it was attached to, on the WIRE copy only (``config/attached_files.py``).
            _run_step(prep, "attached_files", lambda: _place_attached_files(prep, config))
            # AFTER the wire clone, BEFORE the person-turn ordering: in a chat more than one person writes in, each
            # person turn is led by its writer's name on the WIRE copy only (``config/speakers.py``). One person: no change.
            await _name_speakers(prep, config)
            # AFTER the wire clone, BEFORE the person-turn ordering: the conversation's own
            # instructions follow the agent's on the wire only (the frozen prompt never changes).
            _run_step(prep, "conversation_instructions", lambda: _apply_conversation_instructions(prep, config))
            # THE AGENT'S MODES (Understanding v2 C5): the list, the current mode and its instructions follow
            # on the wire only, on EVERY call, so a ``set_mode`` inside a tool loop shows on the next call.
            _run_step(
                prep,
                "agent_modes",
                lambda: _apply_agent_modes(prep, config, request_id=request_id, conversation_id=conversation_id),
            )
            # THE REQUEST ENDS WITH WHAT THE PERSON TYPED (Arman, 2026-10-19): AFTER the wire clone
            # (it orders the materialized messages), the newest person turn is ordered ONCE, here,
            # for the provider this send goes to; translators only render it. The result is checked
            # and announced loudly, never fatal (``config/typed_text_last.py``).
            profile = await _send_profile(config, conversation_id=conversation_id, iteration=iteration)
            # A TEMPLATE THINKING PART RIDES ONLY TO ITS OWN MODEL: from another model it leaves the WIRE copy,
            # never sent as text; fails closed (``config/template_thinking.py``).
            await _apply_template_thinking(prep, config, profile)
            _run_step(
                prep,
                "typed_text_last",
                lambda: order_for_wire(
                    config, profile, prep=prep, conversation_id=conversation_id, iteration=iteration
                ),
            )
            # MEDIA ON AN ASSISTANT TURN (2026-11-10): AFTER the person-turn ordering, a made picture
            # (or file) on an earlier assistant turn rides a host-written user turn right after it,
            # on the WIRE copy only, for every provider whose API refuses media on an assistant turn
            # — so a Claude reply after a made picture is not a 400 and the model still sees it
            # (``config/assistant_turn_media.py``).
            _run_step(
            prep,
            "assistant_turn_media",
            lambda: _carry_assistant_media(prep, config, profile, iteration=iteration),
            records_itself=True,
        )
            # FIT WHAT IS SENT (#136, 2026-11-09): the make-it-fit step above measured the canonical
            # config, but the wire built since carries more — every earlier person turn's kept page
            # block replayed (``_replay_kept_turn_context``), this turn's block, the conversation's
            # instructions. The host refusal measures THIS wire, so a long chat "fit" at 182,861
            # tokens and was refused at 224,540 on every message, forever. The wire is measured
            # against every limit again and made to fit the same way, before anything else reads it.
            await _fit_wire(prep, config, policy=policy, stage=stage, conversation_id=conversation_id, iteration=iteration)
            # A TOOL NAMED AVAILABLE IS DEFINED ON THIS SEND (2026-11-19 review of c8a79d95939): AFTER every fit pass, each
            # late tool definition this send offers is on the wire whole; one a fit pass stubbed, cut or dropped goes out
            # in the newest turn and the prefix is recorded moved (the second layer: the fit never touches a carrier).
            _run_step(prep, "late_tools_on_wire", lambda: _settle_late_tools_on_wire(prep))
            # A HOMED BLOCK NOT ON THE WIRE IS NEVER CLAIMED (2026-11-12): a held copy the window cut,
            # or a homed block the fit just stubbed — the per-turn sentence about it becomes its
            # on-request sentence for this send, and the newest person turn records it so the host
            # homes a fresh copy next turn (``attached_files`` module header).
            _run_step(prep, "homed_off_wire", lambda: _settle_homed_off_wire(prep, config), records_itself=True)
            # A LONE SURROGATE NEVER REACHES A PROVIDER (L12b, 2026-11-03): it is not valid Unicode, so it cannot be
            # encoded and every provider refused the whole request ("An unexpected Groq error", adversarial P2-2). LAST
            # of the text-shaping steps, on exactly what goes on the wire, for every provider; a proper pair is kept.
            # OFF THE LOOP (2026-11-11): it reads every field of every wire part; on a long chat that froze the whole
            # server for 1.3-4.6s (event_loop_stall aidream-api:004bd02ae7555485).
            await _run_step_off_loop(
                prep,
                "lone_surrogates",
                lambda: _announce_lone_surrogates(
                    sanitize_wire_text(prep.wire_config if prep.wire_config is not None else config), conversation_id
                ),
            )
            # THE VERDICT IS CHECKED AGAINST THE BYTES (2026-11-19, staff thread 3af9e95c): a send recorded "held" while a
            # result the last send had cleared went out whole and the cache read only system + tools. LAST of the
            # shaping steps, on exactly the messages this send renders: each is digested (off the loop — it reads every
            # part) and compared with the previous send's, up to that send's cache line; a difference is a MOVED prefix
            # naming the first message that differs. Persisted beside the trim record, so any server task can compare.
            await _run_step_off_loop(prep, "prefix_digests", lambda: _prefix_digests(prep, config), records_itself=True)
            _run_step(
                prep,
                "prefix_bytes",
                lambda: _check_prefix_bytes(prep, conversation_id=conversation_id, request_id=request_id, iteration=iteration),
                records_itself=True,
            )
            # What this send is made of (after the trim, i.e. what really goes out),
            # kept for the request's completion to store on the conversation.
            _run_step(
                prep,
                "context_breakdown",
                lambda: _remember_breakdown(conversation_id, config),
            )
            # THE REQUEST FIREWALL (a REFUSAL, like the pre-flight — never inside ``_run_step``):
            # LAST, on the exact config the provider receives (the wire clone when one was built),
            # after every step above added to it. A caller's open firewall scope is checked on every
            # loop turn and every retry, so nothing reaches the provider unscanned — whatever a
            # door upstream already cleared (``config/request_firewall.py``). No scope: one
            # ContextVar read.
            from matrx_ai.config.request_firewall import check_at_send

            check_at_send(prep.wire_config if prep.wire_config is not None else config)
            prep.steps.append("request_firewall")
            _mark_sent(conversation_id, request_id)

        return prep
    finally:
        try:
            if authored is not None:
                _raised_limits_ride_the_wire(prep, config, authored)
        finally:
            if held_token is not None:
                _HELD_CONFIGS.reset(held_token)
            if lock is not None:
                lock.release()


class NestedSendError(RuntimeError):
    """A loop-stage send was started on a config whose own send boundary is still running."""


#: ids of the canonical configs whose loop-stage boundary THIS context is inside (CGU-10 IMG7 #6).
_HELD_CONFIGS: ContextVar[frozenset[int]] = ContextVar("send_boundary_held_configs", default=frozenset())

#: id(canonical config) -> the lock its loop-stage boundary runs under (dropped with the config).
_BOUNDARY_LOCKS: dict[int, asyncio.Lock] = {}


def _boundary_lock(config: Any) -> asyncio.Lock | None:
    key = id(config)
    lock = _BOUNDARY_LOCKS.get(key)
    if lock is not None:
        return lock
    try:
        weakref.finalize(config, _BOUNDARY_LOCKS.pop, key, None)
    except TypeError:
        return None  # an object without weak references (a test's SimpleNamespace): never shared
    lock = _BOUNDARY_LOCKS[key] = asyncio.Lock()
    return lock


# Every field a send-boundary step (or a one-call setting) may change for ONE call. Each is stored with
# the chat (``UnifiedConfig.to_storage_dict``), so each change moves to the wire copy and the canonical
# config gets the author's value back.
_OUTPUT_LIMIT_FIELDS: tuple[str, ...] = ("max_output_tokens", "thinking_budget", "reasoning_effort", "thinking_level")


def _authored_output_limits(config: Any) -> dict[str, Any]:
    return {name: getattr(config, name, None) for name in _OUTPUT_LIMIT_FIELDS}


def _raised_limits_ride_the_wire(prep: SendPrep, config: Any, authored: dict[str, Any]) -> None:
    """Move every per-call change (output limits, reasoning) off the canonical config onto the wire copy."""
    changed = {name: getattr(config, name, None) for name, value in authored.items() if getattr(config, name, None) != value}
    if not changed:
        return
    if prep is not None:
        if prep.wire_config is None or prep.wire_config is config:
            from copy import copy

            prep.wire_config = copy(config)  # shallow: only scalar limits differ from the canonical
        for name, value in changed.items():
            setattr(prep.wire_config, name, value)
    for name in changed:
        setattr(config, name, authored[name])


# --------------------------------------------------------------------------- #
# Steps                                                                        #
# --------------------------------------------------------------------------- #


def sanitize_wire_text(config: Any) -> int:
    """Replace every lone UTF-16 surrogate half in ``config``'s system text and message content parts with U+FFFD,
    in place, and return how many were replaced. Every string, dict or list field of every content part is covered
    (text, tool results, code, decisions…); a proper surrogate pair is never touched."""
    import dataclasses

    from matrx_ai.persistence.postgres_text import replace_lone_surrogates

    total = 0
    system = getattr(config, "system_instruction", None)
    if isinstance(system, str):
        clean, n = replace_lone_surrogates(system)
        if n:
            config.system_instruction = clean
            total += n
    for message in getattr(config, "messages", None) or []:
        for part in getattr(message, "content", None) or []:
            if not dataclasses.is_dataclass(part):
                continue
            for f in dataclasses.fields(part):
                current = getattr(part, f.name, None)
                if not isinstance(current, (str, dict, list, tuple)):
                    continue
                clean, n = replace_lone_surrogates(current)
                if n:
                    setattr(part, f.name, clean)
                    total += n
    return total


def _announce_lone_surrogates(replaced: int, conversation_id: str | None) -> None:
    if replaced:
        vcprint(
            f"[send_boundary] replaced {replaced} lone surrogate half/halves with U+FFFD before the provider call "
            f"(conversation {conversation_id or '-'}): not valid Unicode, every provider refuses it",
            color="yellow",
        )


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
    nothing). Raised BEFORE the provider; nothing was sent or spent.

    A CALLER REFUSAL (``providers/caller_refusal.py``): the caller sent nothing to answer, so a
    retry changes nothing and no provider was involved. Until 2026-11-13 it was not marked, so
    every refusal was filed as the provider's own issue (``anthropic.empty_conversation``) and
    counted toward that provider's outage alarm."""

    is_caller_refusal = True
    code = "empty_conversation"

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
            error_type=self.code,
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
    from matrx_ai.config.message_config import is_attachment_only_turn

    if role.lower().rsplit(".", 1)[-1] == "user" and is_attachment_only_turn(message):
        return True  # her attachment-only turn: voiced on the wire by ``_voice_attachment_only_turns``
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


def _host_holds_response_format(key: str) -> bool:
    """Whether the host declared this conversation's output contract as held on every turn."""
    try:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 — no context declares nothing
        return False
    metadata = getattr(ctx, "metadata", None) if ctx is not None else None
    return isinstance(metadata, dict) and metadata.get(key) is True


def _apply_followup_response_format(
    config: Any,
    *,
    user_input: Any,
    config_overrides: Any,
    prior_request_status: str | None,
) -> None:
    """Relax a completed one-answer JSON contract at the send boundary."""
    from matrx_ai.config.response_format import (
        RESPONSE_FORMAT_HOLDS_KEY,
        response_format_transition_after_first_structured_answer,
    )

    transition = response_format_transition_after_first_structured_answer(
        config,
        user_input=user_input,
        config_overrides=config_overrides,
        prior_request_status=prior_request_status,
        contract_holds=_host_holds_response_format(RESPONSE_FORMAT_HOLDS_KEY),
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


def _forced_trim(messages_list: list[Any], policy: TrimPolicy) -> Any:
    """The make-it-fit trim (``input_fit.ensure_fits``): cache gate off — the call is over a limit
    and would be refused, so keeping the cached prefix is worth nothing."""
    return trim_messages_context(messages_list, policy=policy, cache_state=None)


def _forced_trim_for(conversation_id: str | None, config: Any = None) -> Any:
    """``_forced_trim`` whose rewrites are remembered — APART from the gated trim's, with the input limit they were
    made under (``_input_limit_tokens``): a result cleared to make one send fit is cleared on every later send while
    that limit still binds or the cache is warm, and dropped once the model's window grew on a cold send
    (``_replay_trims``) — one turn on a small-window model never stubs a thread's results for life."""

    def trim(messages_list: list[Any], policy: TrimPolicy) -> Any:
        report = _forced_trim(messages_list, policy)
        if getattr(report, "blocks_rewritten", 0):
            _remember_trim_rewrites(
                conversation_id, report, messages_list, forced=True, limit_tokens=_input_limit_tokens(config)
            )
        return report

    return trim


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
    """The cache-gated call site of ``trim_messages_context`` (``_forced_trim`` is the other, for a call over a limit).

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
    # Every rewrite is remembered (and persisted into ``cache_state``) so every later send makes it again.
    if report.blocks_rewritten:
        _remember_trim_rewrites(conversation_id, report, messages_list)

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


def _catalog_model_name(model_ref: str) -> str | None:
    """``ai.model_definition.name`` for a model id, name or alias; ``None`` when unresolvable."""
    from matrx_ai.catalog.manager import ai_catalog_manager

    state = ai_catalog_manager.model_state(ai_catalog_manager.resolve_model_ref(model_ref))
    name = state.get("name")
    return str(name) if name else None


def model_cache_prices(
    model_ref: str,
    *,
    offering_id: str | None = None,
    estimated_tokens: int = 0,
    long_cache: bool = False,
) -> tuple[Any, int | None] | None:
    """``(CachePrices | None, rewrite_ttl_secs)`` for a model from the catalog, or ``None`` when the
    catalog has no pricing for it. THE price reader for the cache economics (the trim gate's payback
    rule and the condense decision): a cache read, the write tier that covers rewritten history, and
    fresh input. Raises on a lookup failure — the caller announces it."""
    from matrx_ai.config.cache_marks import history_cache_ttl
    from matrx_ai.config.context_trim import CachePrices
    from matrx_ai.config.usage_config import _get_db_pricing_lookup, lookup_model_pricing

    if not model_ref:
        return None
    lookup = _get_db_pricing_lookup()
    pricing = lookup_model_pricing(lookup, offering_id=offering_id or "", model_name=model_ref)
    if pricing is None and offering_id:
        pricing = lookup_model_pricing(lookup, model_name=model_ref)
    if pricing is None:
        # The request config carries the catalog model ID (or an alias), but the pricing lookup is
        # keyed by offering id and model NAME. Resolve the ref through the catalog's one routing
        # map, then read by the name — exact keys only, never a prefix or a guess.
        catalog_name = _catalog_model_name(model_ref)
        if catalog_name and catalog_name != model_ref:
            pricing = lookup_model_pricing(lookup, model_name=catalog_name)
    if pricing is None:
        return None
    tier = pricing.get_tier(estimated_tokens or 0)
    ttl_secs, write_tier, _prefix = history_cache_ttl(pricing.api or model_ref, long=long_cache)
    if tier is None:
        return None, ttl_secs
    read = tier.cache_hit_price if tier.cache_hit_price is not None else tier.cached_input_price
    if write_tier == "1h" and tier.cache_write_1h_price is not None:
        write = tier.cache_write_1h_price
    elif tier.cache_write_5m_price is not None:
        write = tier.cache_write_5m_price
    else:
        # No write premium on this wire (OpenAI, Gemini implicit): a rewrite is billed as fresh input.
        write = tier.input_price
    if read is None or write is None:
        return None, ttl_secs
    fresh = float(tier.input_price) if tier.input_price is not None else None
    return CachePrices(read_price=float(read), write_price=float(write), input_price=fresh), ttl_secs


def _cache_gate_inputs(config: Any, policy: TrimPolicy | None) -> CacheGateInputs | None:
    """Catalog prices, the history's cache lifetime and the pre-flight numbers for
    the payback gate. Only built in payback mode (legacy needs none of it); any
    failure yields ``None`` and the gate announces its fallback."""
    if policy is None or policy.cache_gate_mode != "payback":
        return None
    from matrx_ai.config.context_preflight import (
        _declared_window,
        current_policy,
        estimate_prompt_tokens,
    )

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
        prices = model_cache_prices(
            model_ref,
            offering_id=str(getattr(config, "routing_offering_id", None) or "") or None,
            estimated_tokens=inputs.estimated_prompt_tokens or 0,
            long_cache=long_cache,
        )
        if prices is not None:
            cache_prices, inputs.rewrite_ttl_secs = prices
            if cache_prices is not None:
                inputs.read_price = cache_prices.read_price
                inputs.write_price = cache_prices.write_price
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


def _record_fit(fit: dict[str, Any], *, stage: str, iteration: int | None) -> None:
    """Land the make-it-fit record on AppContext, the way ``_record_trim_report`` lands the trim.

    ``last_fit`` -> iteration 1's ``cx_request.metadata["input_fit"]`` (the resolve stage ran
    before iteration 1); ``fit_by_iteration[n]`` -> iteration n's row. Read by
    ``orchestrator/requests.py`` when it builds the request rows. Only a pass that applied
    something is recorded (``SendPrep.fit`` is ``None`` otherwise).
    """
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return
    if stage == STAGE_RESOLVE:
        ctx.metadata["last_fit"] = dict(fit)
        return
    if iteration is None:
        return
    ctx.metadata.setdefault("fit_by_iteration", {})[iteration] = dict(fit)


async def _fit_wire(
    prep: SendPrep, config: Any = None, *, policy: Any, stage: str, conversation_id: str | None, iteration: int | None
) -> None:
    """Make the WIRE fit every limit — the exact config the provider (and the host refusal) gets.

    Runs on the wire config when one was built, else on the canonical config itself — the per-turn
    blocks staged after the canonical fit (identity, person context, plan, helpers) grow it too, so
    "the canonical fit already measured what is sent" was never true (2026-11-12). Same passes as the canonical fit (``input_fit.ensure_fits``: forced trim tiers, then
    the last-resort stubs; the newest turn is never touched). Still over after them, the replayed
    page blocks of EARLIER turns (a prompt-cache convenience, never the person's or the model's
    words) leave the wire, oldest first, until it fits. Merged into ``prep.fit`` so the cache guard
    places every rewrite and the request row records it. Never raises: the host refusal still
    decides a call that cannot be fitted."""
    built = prep.wire_config is not None
    wire = prep.wire_config if built else config
    if wire is None:
        return
    try:
        from matrx_ai.config.input_fit import (
            _enforced,
            _limits,
            _over,
            ensure_fits,
            restub_known_texts,
        )

        # ONCE DROPPED, ALWAYS DROPPED (2026-11-15, prompt_cache_prefix_drift "the send boundary
        # rewrote N block(s) it could not place on the wire"): a conversation whose wire once needed
        # its replayed page blocks removed keeps them off EVERY later send — the next round of the
        # loop and every later request — before anything is measured. Otherwise round 1 fits with
        # them, round 2 (grown by tool results) drops them, and every earlier person turn's bytes
        # change mid-loop: the whole cached prefix re-billed, on every request of a long chat.
        sticky: list[dict[str, Any]] = []
        if built and _replayed_context_dropped(conversation_id):
            already = _drop_replayed_turn_context(wire)
            if already:
                sticky.append({"pass": "drop_replayed_turn_context", "on": "wire", "messages_dropped": already,
                               "sticky": True, "unplaced_blocks": already, "rewritten_blocks": []})
        # ONCE STUBBED, ALWAYS STUBBED (2026-11-17, prompt_cache_prefix_drift chat 0fbc8c1f
        # "messages[0] (user) changed (143 -> 4,760 bytes)"): the wire is rebuilt every round, so a
        # history text the last-resort fit stubbed on round N came back whole on round N+1 when the
        # wire fit without it, and the whole cached prefix was written again. Every text an earlier
        # send of this conversation stubbed is stubbed again before anything is measured.
        stub_keys = _wire_text_stubs(conversation_id)
        restubbed = restub_known_texts(list(getattr(wire, "messages", None) or []), stub_keys)
        if restubbed:
            sticky.append({**restubbed, "on": "wire"})
        wire, recut = await _recut_known_texts(prep, config, wire, conversation_id)
        if recut:
            sticky.append(recut)
        fit = await ensure_fits(
            wire, policy=policy, stage=stage, conversation_id=conversation_id, trim=_forced_trim_for(conversation_id, wire),
            stubbed_text_keys=stub_keys,
        )
        _remember_wire_text_stubs(conversation_id, stub_keys)
        prep.steps.append("input_fit_wire")
        if sticky:
            fit = dict(fit or {"fits": True})
            fit["passes"] = [*sticky, *(fit.get("passes") or [])]
        if fit is None:
            return
        if not fit.get("passes"):
            # The wire fits as built: still record ITS measure — the host refusal reads the wire, so
            # this (not the canonical config's) is the number it must agree with (one estimate).
            if prep.fit is not None and fit.get("limits"):
                prep.fit = {**prep.fit, "wire": {"after": fit["limits"]}}
                _record_fit(prep.fit, stage=stage, iteration=iteration)
            return
        passes = [dict(p, on="wire") for p in fit.get("passes") or []]
        if not fit.get("fits") and built:  # the replayed blocks exist only on a built wire (never the ledger)
            dropped = _drop_replayed_turn_context(wire)
            if dropped:
                _remember_replayed_context_dropped(conversation_id)
                passes.append({"pass": "drop_replayed_turn_context", "on": "wire", "messages_dropped": dropped,
                               "unplaced_blocks": dropped, "rewritten_blocks": []})
                fit["fits"] = not _enforced(_over(await _limits(wire)))
                fit["after"] = await _limits(wire)
        if not fit.get("fits"):
            cut = await _cut_text_to_fit(prep, config, wire, conversation_id)
            if cut is not None:
                wire = prep.wire_config
                passes.append(dict(cut, on="wire"))
                fit["fits"] = bool(cut.get("fits"))
                fit["after"] = await _limits(wire)
        merged = dict(prep.fit or {})
        merged["passes"] = [*(merged.get("passes") or []), *passes]
        merged["fits"] = bool(fit.get("fits"))
        merged["wire"] = {"before": fit.get("before"), "after": fit.get("after")}
        prep.fit = merged
        _record_fit(merged, stage=stage, iteration=iteration)
        if not fit.get("fits"):
            logger.error("send_boundary: the wire is still over its limit after every fit pass: %s", merged["wire"])
    except Exception as exc:  # noqa: BLE001 — the host guard still decides
        vcprint(f"[send_boundary/{stage}] wire input_fit failed (ignored): {type(exc).__name__}: {exc}", color="red")
        logger.error("send_boundary wire input_fit failed at stage %s", stage, exc_info=True)


#: ``AppContext.metadata`` key: what the cut-to-fit pass did on this call, for the host's warning alarm
#: (aidream ``platform_guardrails.every_call_refusal`` pops it). A child fork never inherits it.
TEXT_CUT_NOTICE_KEY = "input_fit_text_cut"


def _own_wire_list(config: Any, wire: Any) -> tuple[Any, list[Any]]:
    """``(wire, its message list)`` where the list is the WIRE's own — a shallow wire copy shares the
    canonical list, so a copy-on-write cut replaces entries here, never in the ledger. With no wire
    built yet (``wire is config``), one is made."""
    from matrx_ai.config.message_config import MessageList

    if wire is config:
        wire = copy(config)
    wire.messages = _wire_list(wire.messages, list(wire.messages or []))
    messages = wire.messages
    target = messages._messages if isinstance(messages, MessageList) else messages
    return wire, target


async def _recut_known_texts(prep: SendPrep, config: Any, wire: Any, conversation_id: str | None) -> Any:
    """ONCE CUT, CUT THE SAME WAY (sibling of the sticky stubs): every history text an earlier send of
    this conversation cut to fit is cut to the same length again, before anything is measured
    (``input_fit.recut_known_texts``), and only on a call whose cut-to-fit is enforced. Returns the wire
    to measure (a new one when it had to be made)."""
    from matrx_ai.config.input_fit import cut_to_fit_enforced, recut_known_texts

    known = _wire_text_cuts(conversation_id)
    if not known:
        return wire, None
    if not await cut_to_fit_enforced(wire):
        # A person's own turn in a conversation an automated call once cut: never cut here (review
        # 2026-11-19 finding 7: the earlier cut was reapplied and the person's history came back cut).
        return wire, None
    candidate, target = _own_wire_list(config, wire)

    def _replace(index: int, message: Any) -> None:
        target[index] = message

    record = recut_known_texts(list(target), known, replace=_replace)
    if record is None:
        return wire, None
    prep.wire_config = candidate
    if prep.wire_messages is not None:
        prep.wire_messages = list(target)
    prep.steps.append("input_fit_text_recut")
    return candidate, {**record, "on": "wire"}


#: Per conversation: ``input_fit.text_cut_key`` -> the length kept, for every text a wire cut-to-fit
#: shortened (``_cut_text_to_fit``); cut the same way on every later send (``_recut_known_texts``).
_WIRE_TEXT_CUTS: OrderedDict[str, dict[str, int]] = OrderedDict()


def _wire_text_cuts(conversation_id: str | None) -> dict[str, int]:
    return dict(_WIRE_TEXT_CUTS.get(str(conversation_id), {})) if conversation_id else {}


def _remember_wire_text_cuts(conversation_id: str | None, known: dict[str, int]) -> None:
    if not conversation_id or not known:
        return
    key = str(conversation_id)
    _WIRE_TEXT_CUTS[key] = dict(known)
    _WIRE_TEXT_CUTS.move_to_end(key)
    while len(_WIRE_TEXT_CUTS) > _MAX_TRACKED:
        _WIRE_TEXT_CUTS.popitem(last=False)


async def _cut_text_to_fit(
    prep: SendPrep, config: Any, wire: Any, conversation_id: str | None = None
) -> dict[str, Any] | None:
    """The LAST fit pass (problem 14): an automated call still over its enforced host budget has its
    largest text blocks cut to fit (``input_fit.cut_largest_text_to_fit``) — on the WIRE only. With no
    wire built yet, one is made here (a copy with its own message list), so the canonical config, its
    ledger and what is stored are never cut. The pass is said on the console and left for the host's
    warning alarm (``TEXT_CUT_NOTICE_KEY``)."""
    from matrx_ai.config.input_fit import cut_largest_text_to_fit

    wire, target = _own_wire_list(config, wire)

    def _replace(index: int, message: Any) -> None:
        target[index] = message

    known = _wire_text_cuts(conversation_id)
    cut = await cut_largest_text_to_fit(wire, replace=_replace, known_cuts=known)
    if cut is None or not (cut.get("blocks") or cut.get("system_instruction")):
        return cut
    _remember_wire_text_cuts(conversation_id, known)
    prep.wire_config = wire
    if prep.wire_messages is not None:
        prep.wire_messages = list(target)
    prep.steps.append("input_fit_text_cut")
    summary = {
        "fits": bool(cut.get("fits")),
        "freed_chars": cut.get("freed_chars"),
        "blocks": [{k: b[k] for k in ("kept_chars", "total_chars")} for b in cut.get("blocks") or []]
        + ([dict(cut["system_instruction"], system_instruction=True)] if cut.get("system_instruction") else []),
    }
    vcprint(
        f"[send_boundary/{prep.stage}] cut to fit: {len(summary['blocks'])} text block(s) shortened, "
        f"{summary['freed_chars']:,} characters cut ({'fits' if summary['fits'] else 'STILL over'})",
        color="yellow" if summary["fits"] else "red",
    )
    logger.warning("send_boundary: an automated call's text was cut to fit its input budget: %s", summary)
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is not None:
        ctx.metadata[TEXT_CUT_NOTICE_KEY] = summary
    return cut


#: Conversations whose wire once had to lose its replayed page blocks (``_fit_wire``): they stay
#: off every later send of that conversation in this process, so the prefix never flips back and forth.
_REPLAYED_CONTEXT_DROPPED: OrderedDict[str, float] = OrderedDict()


#: Per conversation: the ``input_fit.text_stub_key`` of every history text a wire fit stubbed
#: (``_fit_wire``). Kept stubbed on every later send of that conversation in this process, so a
#: stubbed text never comes back whole on a later round (the prefix never flips back and forth).
_WIRE_TEXT_STUBS: OrderedDict[str, set[str]] = OrderedDict()


def _wire_text_stubs(conversation_id: str | None) -> set[str]:
    """A copy of the conversation's stubbed-text keys (empty with no conversation)."""
    return set(_WIRE_TEXT_STUBS.get(str(conversation_id), ())) if conversation_id else set()


def _remember_wire_text_stubs(conversation_id: str | None, keys: set[str]) -> None:
    if not conversation_id or not keys:
        return
    key = str(conversation_id)
    _WIRE_TEXT_STUBS[key] = set(keys)
    _WIRE_TEXT_STUBS.move_to_end(key)
    while len(_WIRE_TEXT_STUBS) > _MAX_TRACKED:
        _WIRE_TEXT_STUBS.popitem(last=False)


def _replayed_context_dropped(conversation_id: str | None) -> bool:
    return bool(conversation_id) and str(conversation_id) in _REPLAYED_CONTEXT_DROPPED


def _remember_replayed_context_dropped(conversation_id: str | None) -> None:
    if not conversation_id:
        return
    key = str(conversation_id)
    _REPLAYED_CONTEXT_DROPPED[key] = time.time()
    _REPLAYED_CONTEXT_DROPPED.move_to_end(key)
    while len(_REPLAYED_CONTEXT_DROPPED) > _MAX_TRACKED:
        _REPLAYED_CONTEXT_DROPPED.popitem(last=False)


def _settle_late_tools_on_wire(prep: SendPrep) -> None:
    """🚨 A TOOL NAMED AVAILABLE ON THIS SEND HAS ITS FULL DEFINITION ON THIS SEND (review of c8a79d95939, 2026-11-19).

    The newest turn names the late tools earlier turns carry and does not send them again. A fit pass that stubbed,
    cut or dropped what carried one would leave the model told a tool is available with no definition — and the
    stub is sticky. The fit never touches a carrier (``input_fit.holds_late_tool_definitions``); this is the second,
    independent layer: after every fit pass, each definition this send offers (``prep.late_tools_expected``) must be
    on the wire whole (``late_tools.wire_definitions``: name + canonical digest). One that is not goes out in the
    newest turn's own block (a text part after it), and the prefix is recorded moved, loudly. Deterministic for one
    wire, so the sticky fit passes rebuild the same bytes on every later send."""
    from matrx_ai.config.typed_text_last import HOST_TURN_KEY, is_host_authored
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.providers.late_tools import definition_digest, wire_definitions

    expected = prep.late_tools_expected
    wire = prep.wire_config
    if not expected or wire is None:
        return
    messages = getattr(wire, "messages", None)
    listed = list(messages or [])
    texts = [
        getattr(block, "text", None)
        for message in listed
        for block in (getattr(message, "content", None) or [])
        if isinstance(getattr(message, "content", None), list)
    ]
    texts.extend((getattr(messages, "_tail_context_blocks", None) or {}).values())
    on_wire = set(wire_definitions(texts))
    from matrx_ai.providers.late_tools import _wire_name_of

    missing = {
        slot: block for slot, block in expected.items()
        if (_wire_name_of(slot), definition_digest(block)) not in on_wire
    }
    if not missing:
        return
    host_at = None
    for at in range(len(listed) - 1, -1, -1):
        metadata = getattr(listed[at], "metadata", None)
        if not (isinstance(metadata, dict) and metadata.get(HOST_TURN_KEY)):
            continue
        later = listed[at + 1 :]
        if any(str(getattr(getattr(m, "role", None), "value", getattr(m, "role", None)) or "").lower() == "user"
               and not is_host_authored(m) for m in later):
            host_at = at
            break
    names = sorted(missing)
    if host_at is None:
        vcprint(f"[send_boundary/late_tools] {len(names)} late tool definition(s) are not on the wire and no turn block "
                f"can carry them: {names}", color="red")
        logger.error("send_boundary: late tool definitions missing from the wire with no turn block: %s", names)
        return
    host = copy(listed[host_at])
    from matrx_ai.config.message_config import turn_context_slot_order

    text = "\n\n".join(missing[slot] for slot in turn_context_slot_order(missing))
    host.content = [*list(getattr(listed[host_at], "content", None) or []), TextContent(text=text)]
    listed[host_at] = host
    wire.messages = _wire_list(messages, listed)
    if prep.wire_messages is not None:
        prep.wire_messages = list(listed)
    prep.late_tools_resent = names
    reason = (f"late tool definitions re-sent in the newest turn: the fit left {len(names)} of them off the wire "
              f"({', '.join(names)})")
    vcprint(f"[send_boundary/late_tools] {reason}", color="yellow")
    logger.warning("send_boundary: %s", reason)
    try:
        from matrx_ai.providers.request_capture import note_capture

        note_capture(f"Late tools: {reason}")
    except Exception:  # noqa: BLE001 — an observer never breaks a send
        pass
    _record_prefix_moved(prep, reason)


def _record_prefix_moved(prep: SendPrep, reason: str) -> None:
    """Add ``reason`` to this send's prefix verdict and mark it moved (``history_cut.prefix``)."""
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return
    entry = dict(ctx.metadata.get("history_cut") or {})
    prefix = dict(entry.get("prefix") or {"action": "held", "reasons": []})
    prefix["reasons"] = [*(prefix.get("reasons") or []), reason]
    prefix.update(action="moved", cache_break=True)
    entry["prefix"] = prefix
    ctx.metadata["history_cut"] = entry
    prep.prefix = prefix


def _drop_replayed_turn_context(wire: Any) -> int:
    """Remove EARLIER turns' replayed page blocks from the wire's own list (never the ledger).

    Late tool definitions are not a page block: the model calls them, and the newest turn sends only what earlier
    turns do not carry. A carrier stays; a dropped whole block that held late definitions leaves them behind as a
    carrier in its place (deterministic, so a sticky drop rebuilds the same bytes on every later send)."""
    from matrx_ai.config.typed_text_last import (
        LATE_TOOLS_CARRIER_KEY,
        REPLAYED_LATE_SLOTS_KEY,
        REPLAYED_TURN_KEY,
        host_turn,
    )
    from matrx_ai.providers.late_tools import render_late_tools_carrier

    messages = getattr(wire, "messages", None)
    listed = list(messages or [])
    kept: list[Any] = []
    dropped = 0
    for m in listed:
        metadata = getattr(m, "metadata", None)
        if not (isinstance(metadata, dict) and metadata.get(REPLAYED_TURN_KEY)) or metadata.get(LATE_TOOLS_CARRIER_KEY):
            kept.append(m)
            continue
        dropped += 1
        carrier = render_late_tools_carrier(metadata.get(REPLAYED_LATE_SLOTS_KEY))
        if carrier:
            left = host_turn(m, carrier)
            left.metadata = {REPLAYED_TURN_KEY: True, LATE_TOOLS_CARRIER_KEY: True}
            kept.append(left)
    if dropped:
        wire.messages = _wire_list(messages, kept)
    return dropped


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


async def _enforce_document_output_ceiling(
    prep: SendPrep,
    config: Any,
    *,
    conversation_id: str | None = None,
    request_id: str | None = None,
) -> None:
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

    EXCEPT UNDER A PER-CALL SPEND CAP (2026-10-27). "Free" holds only when
    nothing prices the PERMITTED tokens — and the per-call cap
    (``guardrail_gate.admit_call_spend_cap``, asked after this boundary) does
    exactly that: it prices the call at its ceiling. Raised blindly, a list-shaped
    step carrying ``max_output_tokens: 20000`` under a $0.15 cap went out at
    128,000 (live run a880bc2e, V3 ``who_buys``) — on Gemini Flash about $0.48 at
    the ceiling, so every such step would be refused. Both rules hold at once:
    with a cap open the raise goes only as far as the cap affords
    (``_bound_ceiling_by_spend_cap``), never below the author's own limit, and an
    author's limit that is itself unaffordable is left for the cap to refuse
    before anything is sent.
    """
    try:
        from matrx_ai.config.output_ceiling import (
            as_int,
            declared_output_schema,
            enforce_document_ceiling,
            model_output_maximum,
        )
        from matrx_ai.providers.guardrail_gate import current_call_spend_cap

        requested = as_int(getattr(config, "max_output_tokens", None))
        if requested is None:
            return
        schema = declared_output_schema(config)
        if schema is None:
            return
        model = getattr(config, "matrx_model_name", None) or getattr(config, "model", None)
        cap = current_call_spend_cap()
        loop_key = _loop_key(conversation_id, request_id) if request_id else None
        repeat = False
        if cap is not None and loop_key is not None:
            # A capped loop's later rounds re-judge from the AUTHOR's limit, never from the
            # bounded number the last round wrote (a growing prompt affords less each round).
            authored = _AUTHORED_CEILING.get(loop_key)
            if authored is not None:
                repeat = True
                requested = authored
                config.max_output_tokens = authored
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
        bound = None
        if cap is not None:
            if loop_key is not None:
                _AUTHORED_CEILING[loop_key] = requested
                _AUTHORED_CEILING.move_to_end(loop_key)
                while len(_AUTHORED_CEILING) > _MAX_TRACKED:
                    _AUTHORED_CEILING.popitem(last=False)
            bound = await _bound_ceiling_by_spend_cap(config, cap=cap, authored=requested)
            repairs = [*repairs, bound]
        prep.steps.append("document_output_ceiling")
        for repair in repairs:
            vcprint(
                f"[send_boundary/{prep.stage}] {repair}",
                title="⚠️ SEND BOUNDARY: output ceiling raised for a document answer",
                color="yellow",
                log_level="WARNING",
            )
        if repeat or getattr(config, "max_output_tokens", None) == requested:
            return  # announced once per request; an unaffordable limit is the cap's to refuse
        if loop_key is not None:
            # The canonical config gets the author's limit back after every send (the raise rides
            # the wire only), so every round repairs again: announce and record it once per loop.
            if loop_key in _CEILING_ANNOUNCED:
                return
            _CEILING_ANNOUNCED[loop_key] = True
            while len(_CEILING_ANNOUNCED) > _MAX_TRACKED:
                _CEILING_ANNOUNCED.popitem(last=False)
        _record_ceiling_raise(
            model=model, requested=requested, sent=getattr(config, "max_output_tokens", None),
            repairs=repairs,
        )
        _announce_ceiling_raise(
            model=model, requested=requested, sent=getattr(config, "max_output_tokens", None),
            repairs=repairs, cap_usd=cap.max_usd if cap is not None else None,
        )
    except Exception as exc:  # noqa: BLE001 — a guard's lookup never breaks a send
        vcprint(
            "[send_boundary] document output-ceiling floor failed (ignored): "
            f"{type(exc).__name__}: {exc}",
            color="yellow",
        )


#: The share of a per-call cap the bounded ceiling may spend. The cap prices the call AFTER
#: this step, and the blocks staged after it (agent identity, live plan, conversation
#: instructions) add a few hundred input tokens; the headroom keeps a bounded call from being
#: refused by a hair. An estimation margin, not a limit.
_CAP_HEADROOM = 0.98

#: The author's own ceiling of a capped loop, keyed by ``_loop_key`` — so later rounds bound
#: from it rather than from the number the previous round wrote.
_AUTHORED_CEILING: OrderedDict[str, int] = OrderedDict()

#: Loops whose document-ceiling raise was already announced and recorded (``_loop_key``).
_CEILING_ANNOUNCED: OrderedDict[str, bool] = OrderedDict()


async def _bound_ceiling_by_spend_cap(config: Any, *, cap: Any, authored: int) -> str:
    """Lower a just-raised document ceiling to what the open per-call cap affords, in place.

    ``config.max_output_tokens`` holds the raised value (the model maximum) on entry. Priced
    by THE one estimator the cap itself uses (``guardrail_gate.estimate_call_usd``) — never a
    copy of the pricing: output is linear in tokens for a fixed prompt, so two estimates (at the
    author's limit and at the maximum) give the per-token price, and the result is re-checked.
    Never goes below ``authored``; when even that is unaffordable (or the call cannot be
    priced) the author's limit is sent and the cap refuses it before anything is spent.
    Returns the one-line account of what it did.
    """
    from types import SimpleNamespace

    from matrx_ai.providers.guardrail_gate import estimate_call_usd

    raised = int(config.max_output_tokens)
    budget = float(cap.max_usd) * _CAP_HEADROOM
    # Priced on the SAME profile the provider call resolves (and the cap prices): at this
    # point ``config.model`` is often a catalog id, which no price is keyed by (live
    # 2026-10-28, run c91d63b3: every capped step fell back to the author's limit).
    try:
        from matrx_ai.catalog.resolve import resolve_call_profile

        profile = await resolve_call_profile(
            str(getattr(config, "model", "") or ""),
            offering_id=getattr(config, "routing_offering_id", None),
            **served_via_kwargs(config),
        )
    except Exception as exc:  # noqa: BLE001 — priced from the config instead, loudly
        vcprint(f"[send_boundary] spend-cap bound could not resolve the profile: {exc!r}", color="yellow")
        profile = SimpleNamespace(
            model_name=getattr(config, "matrx_model_name", None) or getattr(config, "model", None),
            offering_id=getattr(config, "runtime_offering_id", None)
            or getattr(config, "offering_id", None),
        )

    def cost_at(tokens: int) -> float | None:
        config.max_output_tokens = tokens
        return estimate_call_usd(profile, config)[0]

    at_max = cost_at(raised)
    if at_max is not None and at_max <= budget:
        return f"Within the ${cap.max_usd:.2f} per-call cap (about ${at_max:.3f} at {raised:,})."
    at_authored = cost_at(authored)
    if at_max is None or at_authored is None or at_authored > budget or raised <= authored:
        config.max_output_tokens = authored
        return (
            f"Kept at the author's {authored:,}: even that is not affordable (or not priceable) "
            f"under the ${cap.max_usd:.2f} per-call cap, which decides next."
        )
    per_token = (at_max - at_authored) / (raised - authored)
    sent = authored + int((budget - at_authored) / per_token) if per_token > 0 else raised
    sent = max(authored, min(raised, sent))
    step = max(1, (sent - authored) // 100)
    while sent > authored and (cost_at(sent) or 0.0) > budget:
        sent = max(authored, sent - step)
    config.max_output_tokens = sent
    return (
        f"max_output_tokens raised {authored:,} -> {sent:,} (not {raised:,}), bounded by the "
        f"${cap.max_usd:.2f} per-call cap."
    )


def _record_ceiling_raise(*, model: Any, requested: int, sent: Any, repairs: list[str]) -> None:
    """The raise is STORED with the request, not only streamed.

    The stream warning reaches a live caller; a workflow step, a mandate run or a
    batch job has nobody reading its stream, so the only record was the server log.
    Live 2026-10-28 (agent d8901b25, chat.request a5c8e43a): the agent row said
    ``max_output_tokens: 3072`` and the call produced 19,208 output tokens, 15,993 of
    them thinking — Anthropic counts thinking inside ``max_tokens``, so the wire's
    128,000 was the whole answer, yet ``chat.request_snapshot.metadata.settings_adjustments``
    recorded only the effort translation. This writes the raise there too, beside the
    payload it shaped (``publish_settings_adjustments``, stored only: the warning
    below already tells the caller)."""
    from matrx_ai.catalog.models import Adjustment
    from matrx_ai.providers.outbound_params import publish_settings_adjustments

    publish_settings_adjustments(
        [
            Adjustment(
                key="max_output_tokens",
                action="raised",
                canonical_value=requested,
                sent_value=sent,
                reason=" ".join(repairs),
                expected=True,
                provenance="computed",
                law="document_output_ceiling",
            )
        ],
        model=model,
        seam="send_boundary",
        announce=False,
    )


def _announce_ceiling_raise(
    *, model: Any, requested: int, sent: Any, repairs: list[str], cap_usd: float | None = None
) -> None:
    """Law 4: the raise reaches the CALLER, not only the server log.

    The ceiling may have come from an explicit request ``config_overrides`` —
    live 2026-10-01, ``max_output_tokens: 300`` went out at 65,536 with every
    sibling override applied and nothing in the stream, which reads as "the
    override was silently ignored". One warning per request: the repair quiets
    itself on later iterations because the canonical config now holds the max.
    """
    from matrx_connect.context.events import WarningPayload

    from matrx_ai.cost_text import person_cost_text
    from matrx_ai.providers.outbound_params import send_client_warning

    send_client_warning(
        WarningPayload(
            code="setting_adjusted",
            system_message=" ".join(repairs),
            user_message=(
                f"Output limit raised from {requested:,} to {sent:,} so the structured "
                "answer is not cut off"
                + (f", bounded by the {person_cost_text(cap_usd)} cap." if cap_usd is not None else ".")
            ),
            level="low",
            recoverable=True,
            metadata={
                "model": str(model),
                "adjusted": [
                    {"key": "max_output_tokens", "requested": requested, "sent": sent}
                ],
                **({"call_spend_cap_usd": cap_usd} if cap_usd is not None else {}),
            },
        ),
        name="send_boundary_ceiling_warning",
    )


#: What the answer reserve changed on a loop, keyed by ``_loop_key``: (authored max, authored
#: budget, sent max, sent budget). A later round of the same loop starts again from the AUTHOR's
#: values — never from the raised ones (which would raise again) — and a reasoning-off retry
#: gets the author's limit back.
_ANSWER_ROOM: OrderedDict[str, tuple[int, Any, int, Any]] = OrderedDict()


async def _reserve_answer_room(
    prep: SendPrep,
    config: Any,
    *,
    conversation_id: str | None = None,
    request_id: str | None = None,
) -> None:
    """THINKING NEVER TAKES THE ANSWER'S ROOM (2026-11-04; ``config/answer_room.py``).

    Reads what thinking the call WILL carry from the catalog's own outbound pass, then caps the
    thinking budget (where the provider takes a number) or raises the output limit (where it does
    not), so ``agents.output_room.answer_reserve_share`` of the authored limit stays for the visible
    answer. Announced like every other boundary change: a client warning, the settings adjustment
    stored with the request, a yellow server line. Never raises; a lookup failure sends the call
    as authored (the empty-reply retry stays the last resort)."""
    try:
        from matrx_ai.config.answer_room import (
            answer_reserve_share,
            plan_answer_room,
            thinking_shape,
        )
        from matrx_ai.config.output_ceiling import as_int, model_output_maximum
        from matrx_ai.providers.guardrail_gate import current_call_spend_cap
        from matrx_ai.providers.outbound_params import preview_outbound_params

        if getattr(config, "served_via", None) is not None:
            return  # a person's own computer: no provider limit to protect, nothing billed
        loop_key = _loop_key(conversation_id, request_id)
        remembered = _ANSWER_ROOM.get(loop_key)
        if remembered is not None:
            authored_max, authored_budget, sent_max, sent_budget = remembered
            if as_int(getattr(config, "max_output_tokens", None)) == sent_max:
                config.max_output_tokens = authored_max
            if sent_budget is not None and getattr(config, "thinking_budget", None) == sent_budget:
                config.thinking_budget = authored_budget
        authored = as_int(getattr(config, "max_output_tokens", None))
        if authored is None:
            return  # no authored limit: the offering default (the model's maximum) applies
        from matrx_ai.catalog.resolve import resolve_call_profile

        profile = await resolve_call_profile(
            str(getattr(config, "model", "") or ""),
            offering_id=getattr(config, "routing_offering_id", None),
            **served_via_kwargs(config),
        )
        controls = profile.controls
        model_max = getattr(controls, "output_maximum", None) or await model_output_maximum(
            getattr(config, "matrx_model_name", None) or getattr(config, "model", None)
        )
        if model_max:
            authored = min(authored, int(model_max))
        shape = thinking_shape(preview_outbound_params(config, controls), controls)
        room = plan_answer_room(
            authored_max=authored, shape=shape, share=answer_reserve_share(), model_max=model_max
        )
        if room is None:
            return
        requested_budget = getattr(config, "thinking_budget", None)
        config.max_output_tokens = room.sent_max
        if room.sent_budget is not None:
            config.thinking_budget = room.sent_budget
        repairs = [room.reason]
        cap = current_call_spend_cap()
        if cap is not None and room.sent_max > authored:
            repairs.append(await _bound_ceiling_by_spend_cap(config, cap=cap, authored=authored))
        sent = as_int(getattr(config, "max_output_tokens", None)) or authored
        _ANSWER_ROOM[loop_key] = (authored, requested_budget, sent, room.sent_budget)
        _ANSWER_ROOM.move_to_end(loop_key)
        while len(_ANSWER_ROOM) > _MAX_TRACKED:
            _ANSWER_ROOM.popitem(last=False)
        prep.steps.append("answer_reserve")
        model = getattr(config, "matrx_model_name", None) or getattr(config, "model", None)
        vcprint(
            f"[send_boundary/{prep.stage}] {' '.join(repairs)}",
            title="⚠️ SEND BOUNDARY: output room reserved for the answer",
            color="yellow",
            log_level="WARNING",
        )
        if remembered is not None:
            return  # announced once per request
        _record_answer_reserve(
            model=model, authored=authored, sent=sent, requested_budget=requested_budget,
            sent_budget=room.sent_budget, reserve=room.reserve, repairs=repairs,
        )
        _announce_answer_reserve(
            model=model, authored=authored, sent=sent, requested_budget=requested_budget,
            sent_budget=room.sent_budget, reserve=room.reserve, repairs=repairs,
        )
    except Exception as exc:  # noqa: BLE001 — a guard's lookup never breaks a send
        vcprint(
            f"[send_boundary] answer reserve failed (ignored): {type(exc).__name__}: {exc}",
            color="yellow",
        )
        logger.error("send_boundary answer reserve failed", exc_info=True)


def _record_answer_reserve(
    *, model: Any, authored: int, sent: int, requested_budget: Any, sent_budget: Any, reserve: int,
    repairs: list[str],
) -> None:
    """STORED with the request (``chat.request_snapshot.metadata.settings_adjustments``)."""
    from matrx_ai.catalog.models import Adjustment
    from matrx_ai.providers.outbound_params import publish_settings_adjustments

    adjustments = []
    if sent != authored:
        adjustments.append(
            Adjustment(
                key="max_output_tokens", action="raised", canonical_value=authored, sent_value=sent,
                reason=" ".join(repairs), expected=True, provenance="computed", law="answer_reserve",
            )
        )
    if sent_budget is not None:
        adjustments.append(
            Adjustment(
                key="thinking_budget", action="clamped", canonical_value=requested_budget,
                sent_value=sent_budget, reason=" ".join(repairs), expected=True, provenance="computed",
                law="answer_reserve",
            )
        )
    publish_settings_adjustments(adjustments, model=model, seam="send_boundary", announce=False)


def _announce_answer_reserve(
    *, model: Any, authored: int, sent: int, requested_budget: Any, sent_budget: Any, reserve: int,
    repairs: list[str],
) -> None:
    """Law 4: the change reaches the CALLER, not only the server log."""
    from matrx_connect.context.events import WarningPayload

    from matrx_ai.providers.outbound_params import send_client_warning

    adjusted: list[dict[str, Any]] = []
    if sent != authored:
        adjusted.append({"key": "max_output_tokens", "requested": authored, "sent": sent})
    if sent_budget is not None:
        adjusted.append({"key": "thinking_budget", "requested": requested_budget, "sent": sent_budget})
    send_client_warning(
        WarningPayload(
            code="setting_adjusted",
            system_message=" ".join(repairs),
            user_message=(
                f"Output limit raised from {authored:,} to {sent:,} so thinking leaves room for the answer."
                if sent != authored
                else f"Thinking limited to {sent_budget:,} tokens so the answer keeps room."
            ),
            level="low",
            recoverable=True,
            metadata={"model": str(model), "answer_reserve_tokens": reserve, "adjusted": adjusted},
        ),
        name="send_boundary_answer_reserve_warning",
    )


def order_for_wire(
    config: Any,
    profile: Any,
    *,
    prep: SendPrep | None = None,
    conversation_id: str | None = None,
    iteration: int | None = None,
) -> SendPrep:
    """THE REQUEST ENDS WITH WHAT THE PERSON TYPED: the one home of the typed-text-last reorder.

    Orders the newest person turn of the send (``prep.wire_config`` when the wire clone exists,
    else ``config``) so it ends with their typed text, this turn's platform block riding its own
    turn before it (``config/typed_text_last.py`` owns the order). Both inputs are resolved
    here, never in a translator: whether the provider carries the block after the cache line
    (``provider_profiles.TURN_CONTEXT_AFTER_CACHE_LINE``) and whether the model rejects two user
    turns in a row (the profile's ``strict_role_alternation``; that model keeps the block in the
    documented system-message fallback). A send whose newest message is a tool result (a live
    tool loop at any iteration, or the first send of a resumed run) carries the block in the same
    place: its own host turn right before the person's typed text, never after the tool result
    (PB-05), and never before a server-written notice (``typed_text_last.turn_person_index``).
    Dropping it mid-loop erased the page values from the model's view after the first tool call
    (guards ``tests/test_a_tool_loop_keeps_its_page_values.py``,
    ``tests/test_a_resumed_turn_carries_its_page_values.py``,
    ``tests/test_page_context_never_follows_a_server_notice.py``).

    A tool-loop send caches a prefix that HOLDS the block (the rolling mark sits on the newest tool
    result). So that turn's block is kept on her turn when the turn ends
    (``keep_turn_context_for_next_turn``) and every later send replays it in the same place
    (``_replay_kept_turn_context``): the next turn's history is byte-identical to what the last
    send cached, and the whole previous tool loop is a cache read, not a re-write (guard
    ``tests/test_the_next_turn_reads_the_tool_loop_from_cache.py``).

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
        is_host_authored,
        notes_before_her_words,
        person_turn_index,
        place_before_typed_text,
        resumed_person_turn_index,
        turn_person_index,
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
    index: int | None = None
    in_messages = turn_context_after_cache_line(provider) and not requires_strict_role_alternation(
        profile
    )
    if in_messages:
        last = listed[-1] if listed else None
        role = getattr(last, "role", None)
        newest_is_tool = str(getattr(role, "value", role) or "").lower() == "tool"
        newest = person_turn_index(listed)
        newest_is_notice = newest is not None and is_host_authored(listed[newest])
        if newest_is_tool:
            # EVERY send of the turn carries its page values (2026-11-02, Office W1c: conversation
            # d8bf9416's second send had no block and the agent disowned the slides it had built
            # from the document). It rides exactly where the first send placed it — before her
            # typed text, never after a tool result (PB-05) — so the cached prefix is unchanged.
            index = resumed_person_turn_index(listed)
        elif newest_is_notice:
            # A server notice (loop guard, ceiling, answer check, injection) is not her turn: the
            # block stays before HER words, never before the notice that follows a tool result.
            index = turn_person_index(listed)
        places_block = (not newest_is_tool and not newest_is_notice) or index is not None
        current = index if index is not None else person_turn_index(listed)
        live: dict[str, str] = {}
        declared: frozenset[str] = frozenset()
        if places_block:
            # A queued turn that replaced an earlier one in this loop keeps that turn's block FIRST, so what
            # the earlier turn carries is known before this turn's late tools are staged (idempotent: the
            # freeze below calls it again).
            _keep_the_replaced_turns_block(getattr(config, "messages", None), listed, _turn_key(listed, index))
            live, declared = _late_tools_this_send(config, provider, carried=True)
            if iteration in (None, 1):  # the person's ask, never a later round of the same request (always warm)
                _note_turn_cadence(prep, config)
        # ONE plan of what earlier turns carry, for the replay below and for the delta: A WARM SEND ONLY APPENDS —
        # the late tool definitions earlier turns on this wire already carry are not sent again
        # (``late_tools.delta_slots``).
        replays = _plan_replays(listed, current, live, declared)
        # LATE TOOLS ride in this turn's block, BEFORE her typed text — never after it as their own
        # trailing turn (live guard ``scripts/check_request_ends_with_typed_text.py``, 2026-11-18:
        # 10 anthropic sends ended ``<late_tools>``). Staged every send; cleared when no block is
        # placed, so the translator's trailing channel (after a tool result) carries them instead.
        _stage_late_tools(messages, live, _carried_late_tools(replays))
        if live:
            prep.late_tools_expected = dict(live)
        if places_block:
            block = _turn_block(config, messages, listed, index)
        # What changed since the turn's first send rides AFTER the cache line, as the current
        # copy, on every send kind (tool result, notice, woken, resumed). Restaged every send.
        _stage_turn_context_changes(config, messages)
    else:
        replays = {}
        _stage_late_tools(messages, {}, {})
        # The translator renders the staged slots into the system message (strict alternation):
        # a Model view capture lists every block from those same slots (no-op unless capturing).
        from matrx_ai.providers.request_capture import record_turn_context_slots

        record_turn_context_slots(getattr(messages, "_turn_context_blocks", None))
    current = index if index is not None else person_turn_index(listed)
    ordered, _placed = place_before_typed_text(listed, block, index=index)
    if in_messages:
        # Placement above changed nothing before ``current``, so earlier indexes still hold.
        ordered = _replay_kept_turn_context(ordered, plan=replays)
    # A host note drained right after her turn (the inbox at her turn's first boundary) rides
    # before her own words, on every send alike (system_error 599b42da, 2026-11-18).
    ordered = notes_before_her_words(ordered)
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


def _stage_late_tools(messages: Any, live: dict[str, str], already: dict[str, str]) -> None:
    """Stage (or clear) this send's late tools in turn-context slots (``late_tools:<wire name>``).

    ``live``: the late tool definitions this send offers in its turn block (``_late_tools_this_send``; ``{}`` when
    the block is not placed or nothing is split — the slots are cleared and the translator's trailing channel
    delivers any late tools as before). ``already``: the definitions EARLIER turns on this wire carry
    (``_carried_late_tools``). Only the new or changed ones are staged, plus the one slot naming every late tool
    this send offers (``late_tools.delta_slots``): A WARM SEND ONLY APPENDS.
    """
    attach = getattr(messages, "attach_turn_context", None)
    if not callable(attach):
        return
    from matrx_ai.providers.late_tools import delta_slots, is_late_tools_slot

    slots = delta_slots(live, already)
    staged = getattr(messages, "_turn_context_blocks", None)
    for slot in [s for s in (staged or {}) if is_late_tools_slot(s) and s not in slots]:
        attach("", slot=slot)
    for slot, block in slots.items():
        attach(block, slot=slot)


#: Ledger attribute (``config.messages``): whether this turn's send found the conversation's prompt cache warm —
#: the cadence ``_keep_late_tools_for_next_turn`` stamps a carrier on.
_TURN_CADENCE_ATTR = "_late_tools_turn_warm"


def _note_turn_cadence(prep: SendPrep, config: Any) -> None:
    """Say on the ledger whether this send found the cache warm (the same input the cache gate and the prefix
    verdict read: ``cache_is_warm`` over ``cache_state`` with the history's lifetime)."""
    from matrx_ai.config.context_trim import cache_is_warm

    ledger = getattr(config, "messages", None)
    if ledger is None:
        return
    state = dict(prep.cache_state or {})
    warm = bool(state) and cache_is_warm(_with_history_ttl(state, _prep_history_ttl(prep, config)))
    try:
        setattr(ledger, _TURN_CADENCE_ATTR, warm)
    except (AttributeError, TypeError):  # a ledger that takes no attribute: no carrier is stamped (the 1x wire)
        pass


#: The tail slot carrying the turn-context policys that changed after the turn's first send.
TURN_CONTEXT_NOW_SLOT = "turn_context_now"


def _turn_key(listed: list[Any], index: int | None) -> Any:
    """Names the turn a send belongs to: her turn's position and her words."""
    import hashlib

    from matrx_ai.config.typed_text_last import person_turn_index, typed_words_of

    at = index if index is not None else person_turn_index(listed)
    if at is None:
        return None
    message = listed[at]
    words = typed_words_of(getattr(message, "content", None))
    return (at, getattr(message, "id", None), hashlib.sha1(words.encode("utf-8")).hexdigest())


def _turn_block(config: Any, messages: Any, listed: list[Any], index: int | None) -> str | None:
    """The block this send places before her words: frozen at the turn's FIRST send.

    🚨 ONE BLOCK PER TURN, BYTE-STABLE (PB-08 k=30, 2026-11-09: 30/30 lead conversations filed
    prompt_cache_prefix_drift — the helper roster slot is restaged every send, so re-rendering here
    rewrote her turn behind the cache line whenever a helper moved). The first send of EVERY turn
    kind (her own message, a woken turn, a resumed run, a first send with no block) freezes what
    it placed (``MessageList.freeze_turn_context``); later sends of the turn place that text.
    What changes mid-turn rides the tail as the current copy (``_stage_turn_context_changes``).
    The freeze lives on the canonical ledger (``config.messages``), reset when a turn starts
    (``executor.execute_until_complete``) and when it ends (``clear_turn_context``).
    """
    from matrx_ai.providers.request_capture import record_turn_context_slots

    ledger = getattr(config, "messages", None)
    freeze = getattr(ledger, "freeze_turn_context", None)
    if callable(freeze):
        staged = getattr(messages, "_turn_context_blocks", None)
        key = _turn_key(listed, index)
        _keep_the_replaced_turns_block(ledger, listed, key)
        block = freeze(
            key,
            staged if isinstance(staged, dict) else None,
            at_length=len(listed),
            kept=_kept_on_her_turn(listed, index),
        )
        # A Model view capture lists every block of this placed text from the slots it was
        # rendered from (no-op unless capturing).
        frozen = getattr(ledger, "frozen_turn_slots", None)
        record_turn_context_slots(frozen() if callable(frozen) else None)
        return block
    render = getattr(messages, "render_turn_context", None)
    record_turn_context_slots(getattr(messages, "_turn_context_blocks", None))
    return render() if callable(render) else None


def _keep_the_replaced_turns_block(ledger: Any, listed: list[Any], key: Any) -> None:
    """A NEWER person turn joined this loop: keep the block the loop sent on her earlier turn.

    🚨 C116 (2026-11-10): a queued message drained into a running loop (``drain_pending_injections``)
    is a new person turn, so the freeze re-froze for it and her earlier turn lost the block every
    earlier send had placed there — inside the prefix the provider cached. ``prompt_cache_prefix_drift``
    on groq, openai, anthropic (conversations 545440be, ad0e8d97, 85c1d3b6): ``system, CTX, user1``
    became ``system, user1, …, CTX, user2``. The frozen text is stamped on her earlier turn exactly as
    ``keep_turn_context_for_next_turn`` stamps it at the end of a request, and
    ``_replay_kept_turn_context`` places it again where the loop sent it. Guard:
    ``tests/test_a_queued_turn_joining_the_loop_keeps_the_cached_prefix.py``.
    """
    from matrx_ai.config.typed_text_last import (
        STORED_TURN_CONTEXT_KEY,
        STORED_TURN_CONTEXT_SLOTS_KEY,
        STORED_TYPED_LAYOUT_KEY,
        typed_layout,
    )

    frozen_key = getattr(ledger, "frozen_turn_key", None)
    old = frozen_key() if callable(frozen_key) else None
    if not old or key is None or old == key:
        return
    at = old[0]
    if not isinstance(at, int) or not isinstance(key[0], int) or at >= key[0] or at >= len(listed):
        return
    if _turn_key(listed, at) != old:  # not the same message any more (a rewritten history)
        return
    placed = getattr(ledger, "placed_turn_context", None)
    block = placed() if callable(placed) else None
    if not block:
        return
    slots_of = getattr(ledger, "frozen_turn_slots", None)
    slots = slots_of() if callable(slots_of) else None
    def _stamp(message: Any) -> bool:
        metadata = getattr(message, "metadata", None)
        metadata = dict(metadata) if isinstance(metadata, dict) else {}
        if metadata.get(STORED_TURN_CONTEXT_KEY) == block:
            return False
        metadata[STORED_TURN_CONTEXT_KEY] = block
        if slots is not None:
            metadata[STORED_TURN_CONTEXT_SLOTS_KEY] = slots
        layout = typed_layout(list(getattr(message, "content", None) or []))
        if layout is not None:
            metadata[STORED_TYPED_LAYOUT_KEY] = layout
        message.metadata = metadata
        return True

    # The wire item (this send's replay reads it) AND the stored message (every later send of the loop
    # builds its wire from it). ``listed`` holds COPIES when wire swaps deep-copy the list, an attached
    # file is homed on that turn, an attachment-only turn is voiced or the chat has several people
    # (REVIEW-C116 I1): stamping only the copy lost the block again from the next send on.
    _stamp(listed[at])
    stored = _stored_message(ledger, listed[at], at, old)
    if stored is not None and stored is not listed[at]:
        _stamp(stored)
    note = getattr(ledger, "note_kept_replaced_turn", None)
    if callable(note):
        note(at, stored if stored is not None else listed[at])


def _stored_message(ledger: Any, wire_message: Any, at: int, key: Any) -> Any:
    """The ledger's own message for ``wire_message`` (her turn at ``at``): the same object, else the
    one with its row id, else the ledger's message at ``at`` when it names the same turn; or None."""
    try:
        stored = list(ledger or [])
    except TypeError:
        return None
    if any(m is wire_message for m in stored):
        return wire_message
    row_id = getattr(wire_message, "id", None)
    if row_id:
        for message in stored:
            if getattr(message, "id", None) == row_id:
                return message
    if at < len(stored) and _turn_key(stored, at) == key and _only_turn_with_these_words(stored, at):
        return stored[at]
    return None


def _only_turn_with_these_words(stored: list[Any], at: int) -> bool:
    """True when no OTHER stored turn of the same role carries the same words as ``stored[at]``.

    The index fallback matches an id-less wire turn to the ledger by position + words; when the wire
    list is shifted against the ledger (trimmed, windowed) and two turns say the same thing ("ok"),
    position + words names the WRONG stored turn and the kept block + typed layout would be stamped
    and persisted on it (C116 round-2 review). Ambiguous → no stored match; the wire copy is still
    stamped, so nothing is lost."""
    from matrx_ai.config.typed_text_last import typed_words_of

    def _role(message: Any) -> str:
        role = getattr(message, "role", None)
        return str(getattr(role, "value", role) or "").lower()

    target = stored[at]
    words = typed_words_of(getattr(target, "content", None))
    return not any(
        index != at
        and _role(message) == _role(target)
        and typed_words_of(getattr(message, "content", None)) == words
        for index, message in enumerate(stored)
    )


def _kept_on_her_turn(listed: list[Any], index: int | None) -> tuple[str, dict[str, str] | None] | None:
    """The block an earlier send cached on her turn (``keep_turn_context_for_next_turn``), or None.

    A woken turn or a resumed run places its block on a person turn whose previous turn already
    cached one there: that exact text is placed again, so her old turn and the whole tool loop
    after it stay a cache read. What is live now rides the tail as the current copy.
    """
    from matrx_ai.config.typed_text_last import (
        STORED_TURN_CONTEXT_KEY,
        STORED_TURN_CONTEXT_SLOTS_KEY,
        person_turn_index,
    )

    at = index if index is not None else person_turn_index(listed)
    if at is None:
        return None
    metadata = getattr(listed[at], "metadata", None)
    if not isinstance(metadata, dict):
        return None
    block = metadata.get(STORED_TURN_CONTEXT_KEY)
    if not isinstance(block, str) or not block:
        return None
    slots = metadata.get(STORED_TURN_CONTEXT_SLOTS_KEY)
    return block, (
        {str(k): str(v) for k, v in slots.items() if isinstance(v, str)} if isinstance(slots, dict) else None
    )


def _stage_turn_context_changes(config: Any, messages: Any) -> None:
    """Stage (or clear) the tail copy of every turn slot that changed since the first send."""
    attach = getattr(messages, "attach_tail_context", None)
    if attach is None:
        return
    render = getattr(getattr(config, "messages", None), "render_turn_context_changes", None)
    text = None
    if callable(render):
        riding = {
            slot: block
            for slot, block in (getattr(messages, "_tail_context_blocks", None) or {}).items()
            if slot != TURN_CONTEXT_NOW_SLOT
        }
        text = render(getattr(messages, "_turn_context_blocks", None), riding)
    attach(text or "", slot=TURN_CONTEXT_NOW_SLOT)


def _replayed_on(message: Any) -> tuple[str, dict[str, str], bool] | None:
    """What an EARLIER turn ``message`` carries: ``(text, late tool definitions in it, carrier)``, or ``None``.

    Its kept whole block (``STORED_TURN_CONTEXT_KEY``; the late definitions are the kept slots'), else its late
    tools carrier (``STORED_LATE_TOOLS_KEY``). Read only through ``_plan_replays``, ONE reading for the replay and
    for what earlier turns carry, so the two never disagree."""
    from matrx_ai.config.typed_text_last import (
        STORED_LATE_TOOLS_KEY,
        STORED_TURN_CONTEXT_KEY,
        STORED_TURN_CONTEXT_SLOTS_KEY,
        is_host_authored,
        is_turn_opening,
    )
    from matrx_ai.providers.late_tools import definition_slots

    metadata = getattr(message, "metadata", None)
    if not isinstance(metadata, dict):
        return None
    # A host turn that OPENED its turn (a headless run's opening) carries a kept block like hers does.
    if is_host_authored(message) and not is_turn_opening(message):
        return None
    kept = metadata.get(STORED_TURN_CONTEXT_KEY)
    if isinstance(kept, str) and kept:
        return kept, definition_slots(metadata.get(STORED_TURN_CONTEXT_SLOTS_KEY)), False
    defined = definition_slots(metadata.get(STORED_LATE_TOOLS_KEY))
    return ("", defined, True) if defined else None


def _late_tools_this_send(config: Any, provider: str, *, carried: bool) -> tuple[dict[str, str], frozenset[str]]:
    """``(the late tool definitions this send offers in turn context, the wire names its tools list declares)``.

    ``({}, ∅)`` unless THIS send splits late tools out of its tools list into turn context: the knob
    (``agents.prompt_cache.late_tools_enabled``) and scope on, the gateway offered, a translator that delivers
    them, names not already held in the tools list (``late_tools.late_tool_names``) — and the block placed
    (``carried``). Only then are carriers replayed and the names slot staged: the knob off is a clean rollback."""
    from matrx_ai.providers.late_tools import (
        LATE_TOOLS_PROVIDERS,
        declared_wire_names,
        late_tools_slots,
    )

    if not carried or provider not in LATE_TOOLS_PROVIDERS:
        return {}, frozenset()
    live = late_tools_slots(config, provider=provider, supported=True)
    if not live:
        return {}, frozenset()
    return live, declared_wire_names(config, live)


def _plan_replays(
    listed: list[Any], current: int | None, live: dict[str, str], declared: frozenset[str]
) -> dict[int, tuple[str, dict[str, str], bool]]:
    """What this send places on each EARLIER turn: ``{index: (text, late definitions it carries, carrier)}``.

    Every kept whole block is replayed. With no late tools split on this send (``live`` empty) that is all: no
    carrier and no change to a kept block (the old wire). Otherwise each late definition is on the wire ONCE: it
    stays only on the newest earlier turn defining it, and only while this send still offers it as that same
    definition (canonical digest) or does not offer it at all; a definition superseded by a later turn or by this
    send's live one, or declared in this send's tools list, leaves the earlier turn (a carrier drops it, a kept block
    loses its exact bytes). A carrier left with nothing is not placed, so a thread never accumulates one per turn.
    A replayed definition never claims availability (``late_tools.retire_offer_header``); the newest turn's names
    slot does. Deterministic for one ``(listed, live, declared)``."""
    from matrx_ai.providers.late_tools import (
        _wire_name_of,
        definition_digest,
        render_late_tools_carrier,
        retire_offer_header,
    )

    found: dict[int, tuple[str, dict[str, str], bool]] = {}
    for at, message in enumerate(listed):
        if current is not None and at >= current:
            break
        replay = _replayed_on(message)
        if replay is not None:
            found[at] = replay
    if not live:
        return {at: replay for at, replay in found.items() if not replay[2]}
    owner: dict[str, int] = {}
    for at in sorted(found):
        for slot in found[at][1]:
            owner[slot] = at
    plan: dict[int, tuple[str, dict[str, str], bool]] = {}
    for at in sorted(found):
        text, defined, carrier = found[at]
        keep: dict[str, str] = {}
        gone: list[str] = []
        for slot, block in defined.items():
            superseded = (
                owner[slot] != at
                or _wire_name_of(slot) in declared
                or (slot in live and definition_digest(live[slot]) != definition_digest(block))
            )
            if superseded:
                gone.append(block)
            else:
                keep[slot] = block
        if carrier:
            rendered = render_late_tools_carrier(keep)
            if rendered:
                plan[at] = (rendered, keep, True)
            continue
        for block in gone:
            text = text.replace(block, "")
        plan[at] = (retire_offer_header(text), keep, False)
    return plan


def _carried_late_tools(plan: dict[int, tuple[str, dict[str, str], bool]]) -> dict[str, str]:
    """The late tool definitions the EARLIER turns of this send carry (each on exactly one turn, ``_plan_replays``)."""
    carried: dict[str, str] = {}
    for at in sorted(plan):
        carried.update(plan[at][1])
    return carried


def _replay_kept_turn_context(ordered: list[Any], *, plan: dict[int, tuple[str, dict[str, str], bool]]) -> list[Any]:
    """``ordered`` with every EARLIER turn's planned replay (``_plan_replays``) back where its sends carried it.

    A person turn carries ``STORED_TURN_CONTEXT_KEY`` when one of its sends held the block inside
    its cached prefix (``keep_turn_context_for_next_turn``). It is placed with the very function
    that placed it then (``place_before_typed_text``), marked as a replay, so the prefix this send
    shares with that turn's last send is byte-identical. The turn being answered now and everything after it use
    the live block, never a kept one (the plan holds only earlier indexes).

    A one-send turn whose send placed late tool definitions (``STORED_LATE_TOOLS_KEY``) gets them back in the same
    place as a CARRIER (``late_tools.render_late_tools_carrier``) when this send splits late tools: they stay inside
    the cached prefix and the newest turn sends only what is new.
    """
    from matrx_ai.config.typed_text_last import (
        LATE_TOOLS_CARRIER_KEY,
        REPLAYED_LATE_SLOTS_KEY,
        place_before_typed_text,
    )

    out = ordered
    for at in sorted(plan, reverse=True):
        text, defined, carrier = plan[at]
        extra: dict[str, Any] = {}
        if carrier:
            extra[LATE_TOOLS_CARRIER_KEY] = True
        elif defined:
            extra[REPLAYED_LATE_SLOTS_KEY] = dict(defined)
        out, _placed = place_before_typed_text(out, text, index=at, replayed=True, host_metadata=extra)
    return out


def keep_turn_context_for_next_turn(config: Any) -> tuple[int, Any] | None:
    """At the END of a turn: keep this turn's block on her turn when a send cached it.

    A send after her turn (a tool result or a server notice is newer than her words) placed the
    block before her words and cached a prefix holding it. The next turn replays her turn from
    storage, so without the block there its prefix diverged at her turn and the whole tool loop
    was written to the cache again (1.25x) instead of read (0.1x) — every agent that made a tool
    call. Stamps ``STORED_TURN_CONTEXT_KEY`` on her message (a new metadata dict; the person view
    ``user_content`` is untouched) and returns ``(index, message)`` for the caller to persist, or
    ``None`` when no send held the block. A one-send turn never needs it: its cache mark sat
    before the block.
    """
    from matrx_ai.config.typed_text_last import (
        STORED_TURN_CONTEXT_KEY,
        STORED_TURN_CONTEXT_SLOTS_KEY,
        STORED_TYPED_LAYOUT_KEY,
        turn_person_index,
        typed_layout,
    )

    messages = getattr(config, "messages", None)
    frozen_slots = getattr(messages, "frozen_turn_slots", None)
    slots = frozen_slots() if callable(frozen_slots) else None
    # What the turn's sends actually placed (and cached), not a re-render of slots restaged since.
    placed = getattr(messages, "placed_turn_context", None)
    block = placed() if callable(placed) else None
    if not block:
        render = getattr(messages, "render_turn_context", None)
        block = render() if callable(render) else None
    if not block:
        return None
    listed = list(messages or [])
    at = turn_person_index(listed)
    if at is None:
        return None
    later = listed[at + 1 :]
    if not any(
        str(getattr(getattr(m, "role", None), "value", getattr(m, "role", None)) or "").lower()
        in ("tool", "user")
        for m in later
    ):
        return _keep_late_tools_for_next_turn(at, listed[at], slots, messages)
    message = listed[at]
    metadata = getattr(message, "metadata", None)
    metadata = dict(metadata) if isinstance(metadata, dict) else {}
    # Which blocks were her typed text when the sends split her turn (the marks do not survive
    # storage); the replay splits her turn the same way (``typed_text_last.with_typed_layout``).
    layout = typed_layout(list(getattr(message, "content", None) or []))
    if (
        metadata.get(STORED_TURN_CONTEXT_KEY) == block
        and (slots is None or metadata.get(STORED_TURN_CONTEXT_SLOTS_KEY) == slots)
        and (layout is None or metadata.get(STORED_TYPED_LAYOUT_KEY) == layout)
    ):
        return None
    metadata[STORED_TURN_CONTEXT_KEY] = block
    if slots is not None:
        metadata[STORED_TURN_CONTEXT_SLOTS_KEY] = slots
    if layout is not None:
        metadata[STORED_TYPED_LAYOUT_KEY] = layout
    message.metadata = metadata
    return at, message


def _keep_late_tools_for_next_turn(
    at: int, message: Any, slots: dict[str, str] | None, ledger: Any = None
) -> tuple[int, Any] | None:
    """A one-send turn keeps no whole block (its cache mark sat before it), but the late tool DEFINITIONS its
    send placed stay on her turn (``STORED_LATE_TOOLS_KEY``): every later send replays them there, inside the
    cached prefix, and sends only what is new (``_replay_kept_turn_context`` / ``_carried_late_tools``).
    Returns ``(index, message)`` for the caller to persist when the stored value changed."""
    from matrx_ai.config.typed_text_last import STORED_LATE_TOOLS_KEY
    from matrx_ai.providers.late_tools import definition_slots

    if slots is None:
        return None
    if getattr(ledger, _TURN_CADENCE_ATTR, False) is not True:
        # COLD CADENCE STAMPS NOTHING (review of c8a79d95939, F6): a carrier sits before the rolling mark, so every
        # cold send writes it at 1.25x where the newest turn sent it at 1x — net-negative below ~22% warm asks. A
        # turn whose ask found the cache cold keeps nothing; one whose ask found it warm (the person replies within
        # the cache's life) stamps. A stamp is permanent and a carrier only ever lands after the previous send's
        # mark, so the rule never flips the cached prefix.
        return None
    defined = definition_slots(slots)
    metadata = getattr(message, "metadata", None)
    metadata = dict(metadata) if isinstance(metadata, dict) else {}
    if metadata.get(STORED_LATE_TOOLS_KEY, {}) == defined:
        return None
    if defined:
        metadata[STORED_LATE_TOOLS_KEY] = defined
    else:
        metadata.pop(STORED_LATE_TOOLS_KEY, None)
    message.metadata = metadata
    return at, message


def _carry_assistant_media(prep: SendPrep, config: Any, profile: Any, *, iteration: int | None = None) -> None:
    """Every media part an assistant turn may not carry on this send's wire, carried to a
    host-written user turn after it (``config/assistant_turn_media.py``). Wire copy only.

    For a model that refuses two user turns in a row (``requires_strict_role_alternation``) the
    parts lead the next person turn instead. When something moved it is RECORDED: on
    ``prep.carried_media``, as the ``assistant_turn_media`` step, and on the request row's
    ``metadata.assistant_media_carried`` (``_record_carried_media``) — never on a send where
    nothing moved."""
    from matrx_ai.config.assistant_turn_media import carry_assistant_media
    from matrx_ai.config.provider_profiles import chat_provider_of, requires_strict_role_alternation

    if chat_provider_of(profile) is None:
        return
    source = prep.wire_config if prep.wire_config is not None else config
    messages = getattr(source, "messages", None)
    moved: list[dict[str, Any]] = []
    carried = carry_assistant_media(
        list(messages or []),
        str(getattr(profile, "wire_format", "") or ""),
        strict_alternation=requires_strict_role_alternation(profile),
        moved_out=moved,
    )
    if carried is None:
        return
    prep.wire_messages = carried
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    wire.messages = _wire_list(messages, carried)
    prep.wire_config = wire
    prep.carried_media = moved
    prep.steps.append("assistant_turn_media")
    _record_carried_media(moved, iteration=iteration)


def _record_carried_media(moved: list[dict[str, Any]], *, iteration: int | None) -> None:
    """Land the carry on AppContext beside the fit record: ``carried_media_by_iteration[n]`` ->
    iteration n's ``chat.request.metadata["assistant_media_carried"]`` (``orchestrator/requests.py``)."""
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None or iteration is None:
        return
    ctx.metadata.setdefault("carried_media_by_iteration", {})[iteration] = [dict(m) for m in moved]


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


async def _send_profile(
    config: Any, *, conversation_id: str | None, iteration: int | None = None
) -> Any:
    """The model profile this send is routed to (catalog), or ``None`` — announced, never fatal.

    Read only when there is a person turn to order (the newest message, or — on a send whose
    newest message is a tool result — the person turn before it); the provider call resolves the
    same profile.
    """
    from matrx_ai.config.typed_text_last import person_turn_index, resumed_person_turn_index

    listed = list(getattr(config, "messages", None) or [])
    if person_turn_index(listed) is None and resumed_person_turn_index(listed) is None:
        return None
    try:
        from matrx_ai.catalog.resolve import resolve_call_profile

        return await resolve_call_profile(
            str(getattr(config, "model", "") or ""),
            offering_id=getattr(config, "routing_offering_id", None),
            **served_via_kwargs(config),
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


def _set_prompt_cache_marks(prep: SendPrep, config: Any) -> None:
    from matrx_ai.config.cache_plan import decide_cache_plan

    plan = decide_cache_plan(config)
    config.prompt_cache_marks = plan.marks
    prep.cache_plan = plan


def _build_wire(prep: SendPrep, config: Any) -> None:
    """Clone-at-send: swap placeholder tokens / fences for their real values.

    The canonical config keeps the placeholders so the secret never reaches
    persistence, snapshots, or the conversation labeler.
    """
    from matrx_ai.config.picklist_runtime import build_wire_config

    prep.wire_config = build_wire_config(config)


def _place_attached_files(prep: SendPrep, config: Any) -> None:
    """Every staged homed block (``attached_files.CONTEXT_FILE_BLOCKS_KEY``: attached files and held
    copies) in its own block at the start of its home person turn, on the wire copy only. Same bytes
    every send: cached once. ``_fit_wire`` never removes one (``_drop_replayed_turn_context`` takes
    only replayed platform turns); its last-resort pass may stub an EARLIER turn's text in place, as
    for any history text, and the host refusal decides a call still over."""
    from matrx_ai.config.attached_files import CONTEXT_FILE_BLOCKS_KEY, place_attached_files

    entries = (getattr(config, "metadata", None) or {}).get(CONTEXT_FILE_BLOCKS_KEY)
    if not entries:
        return
    source = prep.wire_config if prep.wire_config is not None else config
    messages = getattr(source, "messages", None)
    off_wire: list[dict[str, Any]] = []
    placed = place_attached_files(list(messages or []), entries, off_wire=off_wire)
    if off_wire:
        prep.homed_off_wire = [*(prep.homed_off_wire or []), *off_wire]
    if placed is None:
        return
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    wire.messages = _wire_list(messages, placed)
    prep.wire_config = wire


def _settle_homed_off_wire(prep: SendPrep, config: Any) -> None:
    """After the fit: every homed block this send does not carry whole (the window cut a held
    copy's home, or the fit stubbed a homed block) is (1) reported on ``prep.homed_off_wire``,
    (2) unclaimed — the per-turn block's sentence about a held copy becomes the host's
    ``off_wire`` sentence for this send (``attached_files.rewrite_off_wire_notes``), and
    (3) stamped on the newest person turn's metadata (``HOMED_OFF_WIRE_KEY``, held copies only:
    persisted with the turn) so the host homes a fresh copy next turn. Files keep their bytes."""
    from matrx_ai.config.attached_files import (
        CONTEXT_FILE_BLOCKS_KEY,
        HELD_COPY_KIND,
        HOMED_OFF_WIRE_KEY,
        newest_file_home,
        rewrite_off_wire_notes,
    )

    records = list(prep.homed_off_wire or [])
    for fit_pass in (prep.fit or {}).get("passes") or []:
        if fit_pass.get("on") == "wire":
            for hit in fit_pass.get("homed_blocks_stubbed") or []:
                if not any(r.get("key") == hit.get("key") for r in records):
                    records.append({"kind": hit.get("kind"), "key": hit.get("key"), "why": "stubbed"})
    if not records:
        return
    entries = (getattr(config, "metadata", None) or {}).get(CONTEXT_FILE_BLOCKS_KEY)
    held = [r for r in records if r.get("kind") == HELD_COPY_KIND]
    wire = prep.wire_config
    if held and wire is not None:
        messages = getattr(wire, "messages", None)
        rewritten = rewrite_off_wire_notes(list(messages or []), entries, held)
        if rewritten is not None:
            wire.messages = _wire_list(messages, rewritten)
            if prep.wire_messages is not None:
                prep.wire_messages = list(rewritten)
    prep.homed_off_wire = records
    prep.steps.append("homed_off_wire")
    unclaimed = [r for r in held if not r.get("note_rewritten")]
    vcprint(
        f"[send_boundary/{prep.stage}] homed block(s) not on this send's wire: {records}",
        color="red" if unclaimed else "yellow",
    )
    if unclaimed:
        # The per-turn text still claims a copy this request does not carry: never silent.
        logger.error("send_boundary: held copy note not rewritten for an off-wire copy: %s", unclaimed)
    home = newest_file_home(list(getattr(config, "messages", None) or []))
    if held and home is not None:
        metadata = dict(getattr(home, "metadata", None) or {})
        known = list(metadata.get(HOMED_OFF_WIRE_KEY) or [])
        for r in held:
            stamp = {"kind": r["kind"], "key": r["key"], "why": r["why"]}
            if stamp not in known:
                known.append(stamp)
        metadata[HOMED_OFF_WIRE_KEY] = known
        home.metadata = metadata


def _voice_attachment_only_turns(prep: SendPrep, config: Any) -> None:
    """THE PERSON'S ATTACHMENT-ONLY TURN IS NEVER GIVEN WORDS (2026-11-08).

    A person turn built by ``person_attachment_only_turn`` stores no text at all (``content`` and
    ``user_content`` are ``[]``); her file or skill rides the turn's context. Every provider refuses
    an empty user turn, so on the wire copy only, each such turn gets one text block the model
    reads: ``ATTACHMENT_ONLY_NOTICE``, marked ``authored_by: host`` on the block. The canonical
    config and its ledger are never touched. Same words on every send, so the cached prefix holds.
    Guard: ``aidream/services/ai_execution/tests/test_an_attachment_only_turn_puts_no_words_in_her_mouth.py``.
    """
    from matrx_ai.config.message_config import (
        ATTACHMENT_ONLY_NOTICE,
        HOST_AUTHORED_BY,
        is_attachment_only_turn,
    )
    from matrx_ai.config.unified_content import TextContent

    source = prep.wire_config if prep.wire_config is not None else config
    messages = getattr(source, "messages", None)
    listed = list(messages or [])
    voiced: list[Any] = []
    changed = False
    for message in listed:
        if is_attachment_only_turn(message) and not any(
            isinstance(block, TextContent) and str(block.text or "").strip()
            for block in (getattr(message, "content", None) or [])
        ):
            twin = copy(message)
            twin.content = [
                TextContent(
                    text=ATTACHMENT_ONLY_NOTICE,
                    metadata={"authored_by": HOST_AUTHORED_BY, "authored_reason": "attachment_only_turn"},
                ),
                *list(getattr(message, "content", None) or []),
            ]
            voiced.append(twin)
            changed = True
        else:
            voiced.append(message)
    if not changed:
        return
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    wire.messages = _wire_list(messages, voiced)
    prep.wire_config = wire


def _close_stopped_turns(prep: SendPrep, config: Any) -> None:
    """A stopped assistant turn that ends inside an open region is closed on the WIRE copy (never the saved row).

    Keyed on ``metadata.stopped`` or the executor's stop marker ending the turn's last text part; the
    canonical config and its ledger are never touched. Same words every send, so the cached prefix holds.
    Guard: ``tests/test_a_stopped_turn_is_closed_on_the_wire.py``.
    """
    from matrx_ai.config.stopped_turn import STOP_MARKER_RE, close_stopped_text, is_stopped_turn
    from matrx_ai.config.unified_content import TextContent

    source = prep.wire_config if prep.wire_config is not None else config
    messages = getattr(source, "messages", None)
    listed = list(messages or [])
    out: list[Any] = []
    changed = False
    for message in listed:
        content = list(getattr(message, "content", None) or [])
        last = next((i for i in range(len(content) - 1, -1, -1) if isinstance(content[i], TextContent)), None)
        if getattr(message, "role", None) != "assistant" or last is None:
            out.append(message)
            continue
        text = str(content[last].text or "")
        if not (is_stopped_turn(message) or STOP_MARKER_RE.search(text)):
            out.append(message)
            continue
        closed = close_stopped_text(text)
        if closed is None:
            out.append(message)
            continue
        twin = copy(message)
        part = copy(content[last])
        part.text = closed
        content[last] = part
        twin.content = content
        out.append(twin)
        changed = True
    if not changed:
        return
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    wire.messages = _wire_list(messages, out)
    prep.wire_config = wire


def _retire_spent_run_notices(prep: SendPrep, config: Any) -> None:
    """Every run-end notice the person has spoken after is replaced on the WIRE copy (never the saved row)."""
    from matrx_ai.config.spent_run_notices import retire_spent_run_notices

    source = prep.wire_config if prep.wire_config is not None else config
    messages = getattr(source, "messages", None)
    retired = retire_spent_run_notices(list(messages or []))
    if retired is None:
        return
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    wire.messages = _wire_list(messages, retired)
    prep.wire_config = wire


def _apply_conversation_instructions(prep: SendPrep, config: Any) -> None:
    """THIS CONVERSATION'S OWN INSTRUCTIONS (L3 one-chat G1): sent after the agent's own.

    The person's per-conversation instructions (``conversation_instructions``) follow the END of
    the agent's rendered system instruction on the wire clone, never replacing any of it. The canonical config keeps the agent's prompt as the row froze it, so persistence and
    the cache-line law (``_enforce_frozen_prompt``) see the same prefix every turn; the provider
    caches up to the agent's text and re-reads only what follows it. Unset or blank: no change.
    """
    from matrx_ai.config.prompt_block_producers import produce_conversation_instructions

    text = produce_conversation_instructions(config)  # block ``conversation_instructions``
    if text is None:
        return
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    agent_text = getattr(wire, "resolved_system_instruction", None)
    if agent_text is None and isinstance(getattr(wire, "system_instruction", None), str):
        agent_text = wire.system_instruction
    # The agent's prompt renders exactly as it would alone (its date pin, opening turn and all);
    # the conversation's text follows it, once.
    wire.system_instruction = f"{agent_text}\n\n{text}" if agent_text and agent_text.strip() else text
    prep.wire_config = wire


def _apply_agent_modes(prep: SendPrep, config: Any, *, request_id: Any = None, conversation_id: Any = None) -> None:
    """THE AGENT'S MODES (block ``agent_modes``): appended after the agent's system text (and the
    conversation's own instructions) on the wire clone only — the frozen prompt the row stores never
    changes, so a mode switch re-reads only what follows the agent's text. No modes: no change."""
    from matrx_ai.config.agent_modes import settle_turn_mode
    from matrx_ai.config.prompt_block_producers import produce_agent_modes

    # Once per turn: did the person flip the mode since the agent last knew it (D17)?
    settle_turn_mode(config, request_id=request_id, conversation_id=conversation_id)
    text = produce_agent_modes(config)
    if text is None:
        return
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    current = getattr(wire, "resolved_system_instruction", None)
    if current is None and isinstance(getattr(wire, "system_instruction", None), str):
        current = wire.system_instruction
    wire.system_instruction = f"{current}\n\n{text}" if current and current.strip() else text
    prep.wire_config = wire


_STORED_DATE = re.compile(r"Current date: (\d{4}-\d{2}-\d{2})")


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
    # The date the row's stored prompt already names wins: it is what turn one SENT.
    # Conversations stored before the one-UTC-clock rule (2026-10-18) carry a host-local
    # date one day off their UTC created_at; re-deriving from created_at re-rendered a
    # different digit every turn and fired a false frozen_prompt_differs_from_row (108 rows
    # to 2026-11-02, every one diverging at the date digit).
    stored = getattr(conversation_row, "system_instruction", None)
    if isinstance(stored, str):
        match = _STORED_DATE.search(stored[:200])
        if match:
            si.date_anchor = match.group(1)
            return
        from matrx_ai.instructions.core import DATE_BLOCK_OPEN

        # A frozen row whose stored prompt carries NO date at all: turn one sent none
        # (the agent opted out, or the text was frozen before the decoration existed).
        # A reload rebuilds the text with include_date=True, so every later turn put a
        # 77-char date block in front of the cached prefix and screamed (2026-10-31..11-03).
        if (
            stored
            and getattr(config, "system_prompt_frozen", False)
            and DATE_BLOCK_OPEN not in stored
            and "Current date: " not in stored
            and hasattr(si, "include_date")
        ):
            si.include_date = False
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


#: The turn-context policy the live date travels in (its own slot, so no other
#: contributor's block can delete it — see ``MessageList.attach_turn_context``).
LIVE_DATE_SLOT = "live_date"

#: ``AppContext.metadata`` key the host stamps with the person's own IANA zone when it knows it (the Chief's
#: front-line framing does). When present, the live-date block is written in THAT zone and names no UTC time at all
#: (2026-11-06: a UTC "current moment" beside the person's Pacific clock made the Chief answer in UTC on some turns).
PERSON_TIMEZONE_METADATA_KEY = "person_timezone"


def _carried_person_zone() -> Any:
    """The person's zone from the carried AppContext, or ``None`` (unknown / unusable)."""
    try:
        from zoneinfo import ZoneInfo

        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        name = (getattr(ctx, "metadata", None) or {}).get(PERSON_TIMEZONE_METADATA_KEY) if ctx else None
        return ZoneInfo(str(name)) if name else None
    except Exception:  # noqa: BLE001 - an unusable zone falls back to the UTC wording below
        return None


def _announce_live_date(config: Any, *, now: datetime | None = None, zone: Any = None) -> None:
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
    from matrx_ai.config.prompt_block_producers import produce_live_date

    moment = (now or datetime.now(UTC)).astimezone(UTC)
    zone = zone if zone is not None else _carried_person_zone()
    pinned = si.effective_date() if hasattr(si, "effective_date") else None
    attach(produce_live_date(moment, zone=zone, pinned=pinned), slot=LIVE_DATE_SLOT)  # block ``live_date``


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


#: Where a conversation's history cut lives: ``cx_conversation.cache_state[HISTORY_CUT_KEY]`` (persisted with the
#: cache facts it depends on by ``db/persistence._refresh_cache_state``).
HISTORY_CUT_KEY = "history_cut"
#: The cut THIS process decided for a conversation, until persistence writes it into ``cache_state``.
_HISTORY_CUT_MEMO: OrderedDict[str, dict[str, Any]] = OrderedDict()


def remembered_history_cut(conversation_id: str | None) -> dict[str, Any] | None:
    """The cut this process last decided for ``conversation_id`` (read by ``persistence._refresh_cache_state``)."""
    if not conversation_id:
        return None
    cut = _HISTORY_CUT_MEMO.get(str(conversation_id))
    return dict(cut) if cut is not None else None


def _remember_history_cut(conversation_id: str, cut: dict[str, Any]) -> None:
    _HISTORY_CUT_MEMO[conversation_id] = cut
    _HISTORY_CUT_MEMO.move_to_end(conversation_id)
    while len(_HISTORY_CUT_MEMO) > _MAX_TRACKED:
        _HISTORY_CUT_MEMO.popitem(last=False)


def _remember_the_held_cut(conversation_id: str, cut: dict[str, Any]) -> None:
    """A warm send replayed ``cut``: it becomes this process's cut, so persistence writes back the cut this send
    used (layer 1; ``history_cut_to_persist`` — the newer decision wins — is layer 2)."""
    _remember_history_cut(conversation_id, dict(cut))


def _cut_decided_at(cut: Any) -> datetime | None:
    if not isinstance(cut, dict) or not cut.get("at"):
        return None
    try:
        at = datetime.fromisoformat(str(cut["at"]))
    except ValueError:
        return None
    return at if at.tzinfo else at.replace(tzinfo=UTC)


def history_cut_to_persist(conversation_id: str | None, existing: dict[str, Any] | None) -> dict[str, Any] | None:
    """The cut ``persistence._refresh_cache_state`` writes into ``cache_state[HISTORY_CUT_KEY]``, or ``None`` to
    leave the row's cut as it is.

    This process's cut (``remembered_history_cut``: the cut its latest send used) — unless the row already holds a
    cut DECIDED LATER (its ``at``), which another server task moved while this request ran: the newer decision
    wins, announced, so a slow or stale writer never puts an older cut back (2026-11-19, staff thread 3af9e95c)."""
    remembered = remembered_history_cut(conversation_id)
    if remembered is None:
        return None
    on_row = (existing or {}).get(HISTORY_CUT_KEY)
    row_at, mine_at = _cut_decided_at(on_row), _cut_decided_at(remembered)
    if row_at is not None and (mine_at is None or row_at > mine_at):
        vcprint(
            f"[send_boundary] {conversation_id}: history cut decided {remembered.get('at')} not written over the "
            f"newer one another server task decided at {on_row.get('at')} — the next send starts from the newer cut.",
            color="yellow",
        )
        return None
    return remembered


def _first_kept_index(history: list[Any], cut: dict[str, Any]) -> int | None:
    """Where a recorded cut starts in this history: the message whose ``id`` (else ``position``) it names."""
    first_id, first_position = cut.get("first_id"), cut.get("first_position")
    for index, message in enumerate(history):
        if first_id and getattr(message, "id", None) == first_id:
            return index
        if first_position is not None and getattr(message, "position", None) == first_position:
            return index
    return None


def _record_history_cut(prep: SendPrep, decision: dict[str, Any]) -> None:
    """A history-window decision lands on AppContext (``history_cut`` → iteration 1's ``cx_request.metadata``)
    and in ``prep.steps``. A MOVED cut is a deliberate cache break and is also announced."""
    from matrx_ai.context.app_context import try_get_app_context

    prep.steps.append(f"history_window:{decision['action']}")
    prep.prefix_parts["history_window"] = dict(decision)
    ctx = try_get_app_context()
    if ctx is not None:
        ctx.metadata["history_cut"] = dict(decision)
    if decision.get("cache_break"):
        vcprint(
            f"[send_boundary/{prep.stage}] {decision.get('conversation_id')}: history cut MOVED "
            f"({decision.get('reason')}): {decision.get('kept')} of {decision.get('history')} persisted messages, "
            f"{decision.get('cleared_now', 0)} tool result(s) cleared — a deliberate cache break.",
            color="yellow",
        )


def _cut_context(
    conversation_id: str, cache_state: dict[str, Any] | None, *, ttl_secs: int | None = None
) -> tuple[bool, dict[str, Any] | None]:
    """(is the provider cache warm, the recorded history cut) — the ONE warm/cold decision the history window and
    the stale markers share: ``context_trim.cache_is_warm`` (the payback trim gate's own test — warm until the FULL
    TTL), on the TTL the gate uses (``ttl_secs``, from the wire's real marks; ``_history_ttl_secs``)."""
    from matrx_ai.config.context_trim import cache_is_warm

    state = dict(cache_state or {})
    if not state:
        memo = _CACHE_STATE_MEMO.get(str(conversation_id))
        state = dict(memo) if memo else {}
    previous = state.get(HISTORY_CUT_KEY) if isinstance(state.get(HISTORY_CUT_KEY), dict) else None
    if previous is None:
        previous = remembered_history_cut(conversation_id)
    return cache_is_warm(_with_history_ttl(state, ttl_secs)), previous


def _history_ttl_secs(config: Any) -> int | None:
    """The cache lifetime of the history from the wire's real marks — exactly the number the payback gate reads
    (``model_cache_prices(...)[1]``, via ``_cache_gate_inputs``). ``None`` = no fact; the saved default stands."""
    model_ref = str(getattr(config, "matrx_model_name", None) or getattr(config, "model", "") or "")
    if not model_ref:
        return None
    try:
        prices = model_cache_prices(
            model_ref,
            offering_id=str(getattr(config, "routing_offering_id", None) or "") or None,
            long_cache=bool(getattr(config, "extended_prompt_cache", False)),
        )
    except Exception as exc:  # noqa: BLE001 — the saved default then decides, announced
        vcprint(f"[send_boundary] history cache TTL unreadable for {model_ref!r}: {exc!r}", color="yellow")
        return None
    ttl = prices[1] if prices is not None else None
    return int(ttl) if ttl else None


def _prep_history_ttl(prep: SendPrep, config: Any) -> int | None:
    """``_history_ttl_secs`` read once per pass."""
    if prep.history_ttl_secs is _TTL_UNSET:
        prep.history_ttl_secs = _history_ttl_secs(config)
    return prep.history_ttl_secs


def _with_history_ttl(state: dict[str, Any], ttl_secs: int | None) -> dict[str, Any]:
    return {**state, "est_cache_ttl_secs": ttl_secs} if state and ttl_secs else state


async def _apply_history_window(
    prep: SendPrep,
    config: Any,
    *,
    conversation_id: str | None,
    cache_state: dict[str, Any] | None,
    history_len: int | None,
) -> None:
    """THE history window: every conversation the host gives a policy (rule 23), shaped HERE (B2).

    THE CACHE LAW (Arman): nothing but the removal of large tool outputs may change text behind the cache line.
    THE RULING (Arman, D3): every conversation gets the window. Both hold because the cut MOVES only when the
    provider cache is already cold (``context_trim.cache_is_warm`` on the conversation's cache state, with the
    marks-derived TTL — the same warm/cold test, on the same TTL, the trim's payback gate uses): a cold cache has no prefix left to protect. While it
    is warm the recorded cut is REPLAYED (same first message, same cleared tool results), so the prefix the
    provider cached is rebuilt byte for byte. Every moved cut is recorded (``_record_history_cut``) and the new
    cut is remembered in the cache state that persistence writes back.

    The host's door (``_ext.get_conversation_history_window``) returns a :class:`HistoryWindowPolicy` from its
    knobs, or ``None`` for no window. It MAY raise (a knob it cannot read): the turn fails loudly, never runs on a
    window nobody chose.
    """
    from matrx_ai._ext import get_conversation_history_window
    from matrx_ai.config.history_budget import (
        HistoryWindowUnavailable,
        clear_tool_results,
        current_turn_start,
        cut_oldest_turns_to_budget,
        last_turns,
        trim_history_to_token_budget,
    )

    door = get_conversation_history_window()
    messages = getattr(config, "messages", None)
    if door is None or not conversation_id or not messages:
        return
    count = len(messages) if history_len is None else max(0, min(int(history_len), len(messages)))
    history, tail = list(messages[:count]), list(messages[count:])
    if not history:
        return
    try:
        policy = await door(
            conversation_id=str(conversation_id),
            structure_is_live=bool(getattr(config, "responder_mandate_key", None)),
        )
        if policy is not None and int(policy.turns) <= 0:
            last_turns(history, int(policy.turns))  # raises the refusal sentence
    except Exception as exc:
        raise HistoryWindowUnavailable(
            f"the history window of conversation {conversation_id} could not be decided: {exc}"
        ) from exc
    if policy is None:
        return
    warm, previous = _cut_context(conversation_id, cache_state, ttl_secs=_prep_history_ttl(prep, config))
    prep.history_cut_context = {"warm": warm, "previous": previous, "waits": bool(policy.waits_for_cold_cache)}
    decision: dict[str, Any] = {"conversation_id": str(conversation_id), "history": len(history)}

    if warm and policy.waits_for_cold_cache:
        bounded = history
        if previous is not None:
            start = _first_kept_index(history, previous)
            if start is not None:
                bounded = history[start:]
            clear_tool_results(bounded, set(previous.get("cleared") or []))
            # THE CUT THIS SEND USED is what persistence writes back — never an older cut this process decided
            # earlier (2026-11-19, staff thread 3af9e95c: task B held on the cut task C had just moved, then wrote
            # back its own 14-minute-old cut; the next warm send, on a third task, started from it and the cache
            # broke at message 0).
            _remember_the_held_cut(str(conversation_id), previous)
        decision.update(action="held_warm", reason="the provider cache is warm", kept=len(bounded), cache_break=False)
    else:
        bounded = last_turns(history, int(policy.turns))
        # The turn in flight and the newest readings are never cleared (``trim_history_to_token_budget``).
        report = trim_history_to_token_budget(
            bounded,
            policy.token_budget,
            keep_recent_tool_results=int(getattr(policy, "keep_recent_tool_results", 0) or 0),
            protect_from=current_turn_start(bounded, tail),
        )
        # THE TURN BUDGET BINDS: still over it after the results are stubbed → the oldest whole turns are left
        # out (cold or gate-off only, like every move of the cut; a warm send replays the recorded first message).
        turn_budget = getattr(policy, "turn_token_budget", None)
        bounded, turn_cut = cut_oldest_turns_to_budget(
            bounded, turn_budget, protect_from=current_turn_start(bounded, tail)
        )
        kept_ids = {
            str(getattr(b, "tool_use_id", "") or "")
            for m in bounded
            for b in (getattr(m, "content", None) or [])
        }
        carried = [i for i in (previous or {}).get("cleared") or [] if i in kept_ids]
        cleared = sorted({*carried, *(i for i in report.cleared_ids if i in kept_ids)})
        first = bounded[0] if bounded else None
        cut = {
            "first_id": getattr(first, "id", None),
            "first_position": getattr(first, "position", None),
            "cleared": cleared,
            "turns": int(policy.turns),
            "token_budget": policy.token_budget,
            "turn_token_budget": turn_budget,
            "at": datetime.now(UTC).isoformat(),
        }
        if turn_cut.turns_dropped:
            decision["turn_budget"] = {
                "budget_tokens": turn_cut.budget_tokens,
                "tokens_before": turn_cut.tokens_before,
                "tokens_after": turn_cut.tokens_after,
                "turns_dropped": turn_cut.turns_dropped,
            }
            vcprint(
                f"[send_boundary/{prep.stage}] {conversation_id}: history ~{turn_cut.tokens_before:,} tokens over the "
                f"turn budget {turn_cut.budget_tokens:,} — the oldest {turn_cut.turns_dropped} turn(s) left out "
                f"(~{turn_cut.tokens_after:,} kept).",
                color="yellow",
            )
        moved = (
            previous is None and (len(bounded) != len(history) or bool(report.cleared_ids))
        ) or (
            previous is not None
            and (
                (previous.get("first_id"), previous.get("first_position")) != (cut["first_id"], cut["first_position"])
                or set(previous.get("cleared") or []) != set(cleared)
            )
        )
        decision.update(
            action="moved" if moved else "unchanged",
            reason="the provider cache is cold" if not warm else "the cold-cache gate is off (knob)",
            kept=len(bounded),
            cleared_now=len(report.cleared_ids),
            cache_break=bool(moved),
            turns=int(policy.turns),
        )
        _remember_history_cut(str(conversation_id), cut)
    _record_history_cut(prep, decision)
    if len(bounded) != len(history):
        config.messages.clear()
        config.messages.extend([*bounded, *tail])


#: Where a conversation's trim rewrites live: ``cx_conversation.cache_state[TRIM_REPLAY_KEY]`` (keys only, never
#: text — ``context_trim.trim_rewrite_record``), written by ``db/persistence._refresh_cache_state``.
TRIM_REPLAY_KEY = "trim_replay"
#: The record THIS process holds for a conversation, until persistence MERGES it into ``cache_state``.
_TRIM_REPLAY_MEMO: OrderedDict[str, dict[str, Any]] = OrderedDict()
#: Keys THIS process pruned from a conversation's record (their block left the history, or a forced clear was
#: dropped): persistence's merge subtracts them, so a write never brings back what this process let go.
_TRIM_REPLAY_DROPPED: OrderedDict[str, set[str]] = OrderedDict()
#: The forced (make-it-fit) clears: ``record["forced"] = {results, results_after_arguments, arguments,
#: limit_tokens}`` — kept apart from the gated trim's with the input limit they were made under.
FORCED_KEY = "forced"


def _fields(record: Any) -> dict[str, list[str]]:
    from matrx_ai.config.context_trim import TRIM_RECORD_FIELDS

    record = record if isinstance(record, dict) else {}
    return {f: list(dict.fromkeys(str(v) for v in record.get(f) or [] if v)) for f in TRIM_RECORD_FIELDS}


def _copy_record(record: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = _fields(record)
    forced = record.get(FORCED_KEY)
    if isinstance(forced, dict):
        out[FORCED_KEY] = {**_fields(forced), "limit_tokens": forced.get("limit_tokens")}
    return out


def remembered_trim_replay(conversation_id: str | None) -> dict[str, Any] | None:
    """The trim rewrites this process last recorded for ``conversation_id``."""
    if not conversation_id:
        return None
    record = _TRIM_REPLAY_MEMO.get(str(conversation_id))
    return _copy_record(record) if record is not None else None


def persisted_prefix_state(conversation_id: str | None, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    """What ``persistence._refresh_cache_state`` carries into ``cache_state`` so the next send — on any server
    task — rebuilds the prefix this one sent: today the trim rewrites (the history cut has its own key).

    MERGED with ``existing`` (the row's ``cache_state`` as read at write time), never a replacement (2026-11-19
    review): two requests on one conversation on two server tasks each hold only their own keys, and a
    replacement made the second write erase the first's — the cleared result came back in full on the next send.
    What this process pruned (``_TRIM_REPLAY_DROPPED``) is subtracted. ``{}`` when this process holds nothing."""
    if not conversation_id:
        return {}
    key = str(conversation_id)
    out: dict[str, Any] = {}
    # The last send's message digests (``_check_prefix_bytes``): the next send — on any server task — compares its
    # bytes against them. This request's own last send, so the newest record there is.
    digests = _PREFIX_BYTES_MEMO.get(key)
    if digests is not None:
        out[PREFIX_BYTES_KEY] = dict(digests)
    memo = _TRIM_REPLAY_MEMO.get(key)
    if memo is None:
        return out
    prior = (existing or {}).get(TRIM_REPLAY_KEY)
    out[TRIM_REPLAY_KEY] = _without(_merged_trim_record(prior, memo), _TRIM_REPLAY_DROPPED.get(key) or set())
    return out


def _bounded_put(memo: OrderedDict[str, Any], key: str, value: Any) -> None:
    memo[key] = value
    memo.move_to_end(key)
    while len(memo) > _MAX_TRACKED:
        memo.popitem(last=False)


def _store_trim_record(conversation_id: str, record: dict[str, Any], *, dropped: set[str] = frozenset(), revived: set[str] = frozenset()) -> None:
    _bounded_put(_TRIM_REPLAY_MEMO, conversation_id, record)
    gone = (_TRIM_REPLAY_DROPPED.get(conversation_id) or set()) | set(dropped)
    _bounded_put(_TRIM_REPLAY_DROPPED, conversation_id, gone - set(revived))


def _input_limit_tokens(config: Any) -> int | None:
    """The input limit a forced trim answers to: the model's declared context window (``None`` = unknown)."""
    if config is None:
        return None
    from matrx_ai.config.context_preflight import _declared_window

    model_ref = str(getattr(config, "matrx_model_name", None) or getattr(config, "model", "") or "")
    window = _declared_window(model_ref) if model_ref else None
    return int(window) if window else None


def _max_limit(*limits: Any) -> int | None:
    """The larger limit; an unknown one (``None``) wins — a clear whose limit is unknown is never dropped."""
    known = [int(x) for x in limits if isinstance(x, int) and x > 0]
    return None if len(known) != len(limits) or not known else max(known)


def _remember_trim_rewrites(
    conversation_id: str | None,
    report: TrimReport,
    messages: list[Any] | None = None,
    *,
    forced: bool = False,
    limit_tokens: int | None = None,
) -> None:
    """Add ``report``'s rewrites to this process's record: the gated trim's to the record proper, a forced trim's
    to ``record["forced"]`` with ``limit_tokens``. Both are first pruned to the blocks present in ``messages`` (the
    list the trim ran on) — a path that records but never replays (loop stage, the wire fit) stays bounded."""
    if not conversation_id:
        return
    from matrx_ai.config.context_trim import (
        TRIM_RECORD_FIELDS,
        record_keys_present,
        trim_rewrite_record,
    )

    key = str(conversation_id)
    prior = _TRIM_REPLAY_MEMO.get(key) or {}
    normal = _fields(prior)
    forced_prior = prior.get(FORCED_KEY) if isinstance(prior.get(FORCED_KEY), dict) else {}
    forced_fields = _fields(forced_prior)
    both = _merged_trim_record(normal, forced_fields)
    present = record_keys_present(list(messages)) if messages is not None else None
    full = trim_rewrite_record(report, both, present=present)
    keep = {f: set(full[f]) for f in TRIM_RECORD_FIELDS}
    added = {f: [k for k in full[f] if k not in set(both[f])] for f in TRIM_RECORD_FIELDS}
    normal = {f: [k for k in normal[f] if k in keep[f]] for f in TRIM_RECORD_FIELDS}
    forced_fields = {f: [k for k in forced_fields[f] if k in keep[f]] for f in TRIM_RECORD_FIELDS}
    target = forced_fields if forced else normal
    for f in TRIM_RECORD_FIELDS:
        target[f] = list(dict.fromkeys([*target[f], *added[f]]))
    record: dict[str, Any] = dict(normal)
    if any(forced_fields.values()):
        made_under = (
            _max_limit(forced_prior.get("limit_tokens"), limit_tokens)
            if forced and any(forced_prior.get(f) for f in TRIM_RECORD_FIELDS)
            else (limit_tokens if forced else forced_prior.get("limit_tokens"))
        )
        record[FORCED_KEY] = {**forced_fields, "limit_tokens": made_under}
    gone = {k for f in TRIM_RECORD_FIELDS for k in both[f] if k not in keep[f]}
    _store_trim_record(key, record, dropped=gone, revived={k for f in added.values() for k in f})


def _merged_trim_record(*records: Any) -> dict[str, Any]:
    """The union of the records, each list ordered and unique (a clearing made once is made forever; another server
    task may hold a newer one). Forced clears stay apart; a key the gated record holds leaves the forced one."""
    from matrx_ai.config.context_trim import TRIM_RECORD_FIELDS

    merged: dict[str, dict[str, None]] = {f: {} for f in TRIM_RECORD_FIELDS}
    forced: dict[str, dict[str, None]] = {f: {} for f in TRIM_RECORD_FIELDS}
    limits: list[Any] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        for f, keys in _fields(record).items():
            merged[f].update(dict.fromkeys(keys))
        part = record.get(FORCED_KEY)
        if isinstance(part, dict) and any(part.get(f) for f in TRIM_RECORD_FIELDS):
            for f, keys in _fields(part).items():
                forced[f].update(dict.fromkeys(keys))
            limits.append(part.get("limit_tokens"))
    out: dict[str, Any] = {f: list(keys) for f, keys in merged.items()}
    rest = {f: [k for k in keys if k not in merged[f]] for f, keys in forced.items()}
    if any(rest.values()):
        out[FORCED_KEY] = {**rest, "limit_tokens": _max_limit(*limits)}
    return out


def _without(record: dict[str, Any], gone: set[str]) -> dict[str, Any]:
    if not gone:
        return record
    out: dict[str, Any] = {f: [k for k in keys if k not in gone] for f, keys in _fields(record).items()}
    forced = record.get(FORCED_KEY)
    if isinstance(forced, dict):
        rest = {f: [k for k in keys if k not in gone] for f, keys in _fields(forced).items()}
        if any(rest.values()):
            out[FORCED_KEY] = {**rest, "limit_tokens": forced.get("limit_tokens")}
    return out


def _replay_trims(
    prep: SendPrep,
    config: Any,
    *,
    conversation_id: str | None,
    cache_state: dict[str, Any] | None,
    policy: TrimPolicy | None,
) -> None:
    """Make again every rewrite an earlier send's trim made (``context_trim.replay_trim_rewrites``), on cold and
    warm sends alike: the decision is a function of persisted state, never of whether this send's trim runs.

    The record is the union of the conversation's persisted ``cache_state.trim_replay`` and this process's memo,
    pruned to the blocks still sent (the window may have cut some) — the ONE place a record is pruned against the
    history. A replay only ever shrinks the prompt.

    FORCED CLEARS (made to fit a limit, ``input_fit``'s tiers reach 2 positions / 400 chars) replay while the
    cache is warm OR the current input limit is not larger than the one they were made under. When the model's
    window GREW and the cache is cold, they are dropped and leave the record: that send is cold anyway (restoring
    them costs nothing extra) and a thread is never stubbed for life by one turn on a small-window model."""
    messages = getattr(config, "messages", None)
    if not conversation_id or not messages:
        return
    from matrx_ai.config.context_trim import TRIM_RECORD_FIELDS, cache_is_warm, replay_trim_rewrites

    key = str(conversation_id)
    state = cache_state if cache_state else _CACHE_STATE_MEMO.get(key) or {}
    record = _without(
        _merged_trim_record(state.get(TRIM_REPLAY_KEY), _TRIM_REPLAY_MEMO.get(key)),
        _TRIM_REPLAY_DROPPED.get(key) or set(),
    )
    forced = record.get(FORCED_KEY) or {}
    if not any(record.get(f) for f in TRIM_RECORD_FIELDS) and not forced:
        return
    keep_forced, forced_note = True, None
    if forced:
        made_under = forced.get("limit_tokens")
        limit_now = _input_limit_tokens(config)
        warm = cache_is_warm(_with_history_ttl(dict(state), _prep_history_ttl(prep, config)))
        grown = bool(made_under and limit_now and limit_now > int(made_under))
        keep_forced = warm or not grown
        if not keep_forced:
            forced_note = {"made_under": made_under, "limit_now": limit_now}
    effective = _merged_trim_record(_fields(record), _fields(forced) if keep_forced else None)
    listed = messages if isinstance(messages, list) else list(messages)
    replay = replay_trim_rewrites(listed, effective, policy)
    present = {f: set(replay["present"].get(f) or []) for f in TRIM_RECORD_FIELDS}
    kept: dict[str, Any] = {f: [k for k in record.get(f) or [] if k in present[f]] for f in TRIM_RECORD_FIELDS}
    if keep_forced and forced:
        rest = {f: [k for k in forced.get(f) or [] if k in present[f]] for f in TRIM_RECORD_FIELDS}
        if any(rest.values()):
            kept[FORCED_KEY] = {**rest, "limit_tokens": forced.get("limit_tokens")}
    every = {k for f in TRIM_RECORD_FIELDS for k in [*(record.get(f) or []), *(forced.get(f) or [])]}
    still = {k for f in TRIM_RECORD_FIELDS for k in [*kept[f], *((kept.get(FORCED_KEY) or {}).get(f) or [])]}
    _store_trim_record(key, kept, dropped=every - still)
    dropped_forced = sum(len(forced.get(f) or []) for f in ("results", "arguments")) if forced_note else 0
    prep.trim_replay = {**replay, "forced_dropped": dropped_forced, **({"forced_note": forced_note} if forced_note else {})}
    if replay["results"] or replay["arguments"]:
        prep.steps.append(f"trim_replayed:{replay['results']}+{replay['arguments']}")
    if dropped_forced:
        prep.steps.append(f"trim_forced_dropped:{dropped_forced}")
        vcprint(
            f"[send_boundary/{prep.stage}] {key}: {dropped_forced} forced make-it-fit clear(s) dropped — the input "
            f"limit grew ({forced_note['made_under']} -> {forced_note['limit_now']}) and the cache is cold; those "
            "results go out whole again (a deliberate cache break on an already-cold send).",
            color="yellow",
        )


def _record_prefix(
    prep: SendPrep, config: Any = None, *, stage: str, iteration: int | None, conversation_id: str | None
) -> None:
    """Say whether this send HELD the message prefix the last send cached (byte for byte) or MOVED it, and why.

    Resolve stage: the verdict of the history window, the stale markers and the context trim (what the replay
    rebuilt does not count — it rebuilds what was already sent). Loop stage: a trim that rewrites mid-loop moves
    the prefix too and is added to the same record. Lands on ``AppContext.metadata["history_cut"]["prefix"]``
    (iteration 1's ``cx_request.metadata.history_cut``; the latency row's ``cache_outcome.prefix``)."""
    from matrx_ai.config.context_trim import cache_is_warm
    from matrx_ai.context.app_context import try_get_app_context

    report = prep.trim_report
    gate = ((report.policy or {}).get("cache_gate") or {}) if report is not None else {}
    rewritten = int(getattr(report, "blocks_rewritten", 0) or 0)
    trim_reason = (
        f"context trim rewrote {rewritten} block(s) ({gate.get('rule') or 'no cache state'})"
        + (f" at iteration {iteration}" if stage == STAGE_LOOP else "")
    )
    ctx = try_get_app_context()
    entry = dict(ctx.metadata.get("history_cut") or {}) if ctx is not None else {}

    if stage == STAGE_LOOP:
        if not rewritten or ctx is None:
            return
        prefix = dict(entry.get("prefix") or {"action": "held", "reasons": []})
        prefix["reasons"] = [*(prefix.get("reasons") or []), trim_reason]
        prefix.update(action="moved", cache_break=True)
        entry["prefix"] = prefix
        ctx.metadata["history_cut"] = entry
        prep.prefix = prefix
        return

    reasons: list[str] = []
    for part in ("history_window", "stale_markers"):
        decision = prep.prefix_parts.get(part) or {}
        if decision.get("cache_break"):
            reasons.append(f"{part.replace('_', ' ')} moved ({decision.get('reason')})")
    replay = prep.trim_replay or {}
    if replay.get("forced_dropped"):
        note = replay.get("forced_note") or {}
        reasons.append(
            f"forced make-it-fit clears dropped ({replay['forced_dropped']}): input limit grew "
            f"{note.get('made_under')} -> {note.get('limit_now')} on a cold cache"
        )
    if rewritten:
        reasons.append(trim_reason)
    state = dict(prep.cache_state or {})
    if state and config is not None:
        state = _with_history_ttl(state, _prep_history_ttl(prep, config))
    prefix = {
        "action": "moved" if reasons else "held",
        "cache_break": bool(reasons),
        "reasons": reasons,
        "cache": ("warm" if cache_is_warm(state) else "cold") if state else "unknown",
        "trim": {
            "replayed": int(replay.get("results", 0) or 0) + int(replay.get("arguments", 0) or 0),
            "rewritten_now": rewritten,
            "decision": gate.get("decision"),
            "rule": gate.get("rule"),
        },
    }
    prep.prefix = prefix
    if ctx is not None:
        entry.setdefault("conversation_id", str(conversation_id) if conversation_id else None)
        entry["prefix"] = prefix
        ctx.metadata["history_cut"] = entry


#: Where a conversation's last send's message digests live: ``cx_conversation.cache_state[PREFIX_BYTES_KEY]`` =
#: ``{"digests": "<8 hex chars per message, concatenated>", "stable": <messages its cache line covers>, "at",
#: "request_id", "iteration"}`` — hashes only, never text (the column reaches the client).
PREFIX_BYTES_KEY = "prefix_bytes"
#: The last send THIS process made per conversation, until persistence writes it into ``cache_state``.
_PREFIX_BYTES_MEMO: OrderedDict[str, dict[str, Any]] = OrderedDict()
_MESSAGE_DIGEST_CHARS = 8
#: A record keeps at most this many messages (a longer wire is compared over its first ones only).
_MAX_DIGESTED_MESSAGES = 4096


def _role_of(message: Any) -> str:
    role = getattr(message, "role", None)
    if role is None and isinstance(message, dict):
        role = message.get("role")
    return str(getattr(role, "value", role) or "")


def _part_of(block: Any) -> Any:
    part = block.to_storage_dict() if hasattr(block, "to_storage_dict") else block
    if isinstance(part, dict) and "cache_control" in part:  # a cache mark is not cached text
        part = {k: v for k, v in part.items() if k != "cache_control"}
    return part


def message_digest(message: Any) -> str:
    """A short digest of what ``message`` puts on the wire: its role and every content part (cache marks excluded)."""
    content = getattr(message, "content", None)
    if content is None and isinstance(message, dict):
        content = message.get("content")
    parts = [_part_of(b) for b in content] if isinstance(content, list) else content
    raw = json.dumps({"role": _role_of(message), "content": parts}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8", "replace")).hexdigest()[:_MESSAGE_DIGEST_CHARS]


def _stable_count(messages: list[Any]) -> int:
    """How many leading messages this send's cache line covers: all but the trailing person turn (its per-turn
    platform block and typed text are written after the rolling mark and change by design). A send that ends on a
    tool result (a loop round) covers every message."""
    end = len(messages)
    while end > 0 and _role_of(messages[end - 1]) == "user":
        end -= 1
    return end


def _prefix_digests(prep: SendPrep, config: Any) -> None:
    """Digest every message this send renders (off the loop: it reads every part of a long wire)."""
    messages = prep.wire_messages
    if messages is None:
        wire = prep.wire_config if prep.wire_config is not None else config
        messages = getattr(wire, "messages", None)
    if not messages:
        return
    listed = list(messages)[:_MAX_DIGESTED_MESSAGES]
    prep.message_digests = [message_digest(m) for m in listed]
    prep.prefix_bytes = {"stable": min(_stable_count(list(messages)), len(listed))}


def _previous_send_digests(prep: SendPrep, key: str) -> dict[str, Any] | None:
    """The conversation's last send: this process's own, or the row's (another server task's) when that is newer."""
    mine = _PREFIX_BYTES_MEMO.get(key)
    state = prep.cache_state if prep.cache_state else (_CACHE_STATE_MEMO.get(key) or {})
    row = state.get(PREFIX_BYTES_KEY) if isinstance(state, dict) else None
    row = row if isinstance(row, dict) and isinstance(row.get("digests"), str) else None
    if mine is None or row is None:
        return mine or row
    return row if _is_newer(str(row.get("at") or ""), mine.get("at")) else mine


def _check_prefix_bytes(prep: SendPrep, *, conversation_id: str | None, request_id: str | None, iteration: int | None) -> None:
    """Compare this send's message digests with the previous send's, up to the messages that send's cache line
    covered, and make the held/moved verdict say what the bytes say.

    The second, independent layer under the replay (the first makes the bytes equal; this one proves they are): a
    "held" verdict over a differing message becomes MOVED, with the reason "prefix bytes differ" and the index and
    role of the first message that differs. Every verdict carries ``bytes`` (what was compared). Side runs (a system
    process inside the conversation, an unsaved run) neither compare nor record."""
    digests = prep.message_digests
    if not conversation_id or digests is None:
        return
    from matrx_ai.context.app_context import try_get_app_context
    from matrx_ai.providers.final_outbound_snapshot import is_side_run

    ctx = try_get_app_context()
    if is_side_run(ctx):
        return
    key = str(conversation_id)
    previous = _previous_send_digests(prep, key)
    _bounded_put(
        _PREFIX_BYTES_MEMO,
        key,
        {
            "digests": "".join(digests),
            "stable": int((prep.prefix_bytes or {}).get("stable", len(digests))),
            "at": datetime.now(UTC).isoformat(),
            "request_id": request_id,
            "iteration": iteration,
        },
    )
    if previous is None:
        return
    raw = str(previous.get("digests") or "")
    before = [raw[i : i + _MESSAGE_DIGEST_CHARS] for i in range(0, len(raw), _MESSAGE_DIGEST_CHARS)]
    compared = max(0, min(int(previous.get("stable", len(before)) or 0), len(before)))
    first = next((i for i in range(compared) if i >= len(digests) or digests[i] != before[i]), None)
    same_request = bool(request_id) and previous.get("request_id") == request_id
    found = {
        "compared": compared,
        "first_difference": first,
        "against": "previous round" if same_request else "previous request",
    }
    prep.prefix_bytes = {**(prep.prefix_bytes or {}), **found}
    if ctx is None:
        return
    entry = dict(ctx.metadata.get("history_cut") or {})
    prefix = dict(entry.get("prefix") or {"action": "held", "cache_break": False, "reasons": []})
    # The first comparison of the request is the one against the previous request; a later round adds its own.
    prefix.setdefault("bytes", found)
    if first is not None:
        listed = list(prep.wire_messages or [])
        role = "absent" if first >= len(digests) else (_role_of(listed[first]) if first < len(listed) else "message")
        if prefix.get("action") == "held":
            where = f" at iteration {iteration}" if same_request and iteration else ""
            prefix["reasons"] = [
                *(prefix.get("reasons") or []),
                f"prefix bytes differ from the {found['against']} at message {first} of {compared} ({role}){where}",
            ]
            prefix.update(action="moved", cache_break=True)
        vcprint(
            f"[send_boundary/{prep.stage}] {key}: message {first} ({role}) differs from the {found['against']}'s, inside "
            f"the {compared} messages its cache line covered — the cached prefix is written again from there.",
            color="yellow",
        )
    entry["prefix"] = prefix
    ctx.metadata["history_cut"] = entry
    prep.prefix = prefix


async def _mark_perishable_state(
    prep: SendPrep, config: Any, *, conversation_id: str | None, cache_state: dict[str, Any] | None = None
) -> None:
    """Mark earlier turns' live-machine readings stale — host-enabled threads only.

    See ``config/perishable_state.py``. The host decides which conversations are
    permanent (``_ext.get_perishable_state_marker``); unconfigured or False →
    nothing happens. A failure is announced and skipped, never fatal.

    THE CACHE LAW (Arman: nothing but the removal of large tool outputs may change text behind the cache line):
    a marker rewrites an EARLIER turn, which the provider has cached. So the markers move only on the history
    window's cold-cache decision (``prep.history_cut_context``; no window → the same warm/cold test, gate on).
    While warm, exactly the keys the last cold turn marked (``history_cut.stale``) are re-marked; a cold pass
    marks every earlier reading and records the new set on the cut and on the request
    (``history_cut.stale_markers``), a moved set announced as a deliberate cache break.
    """
    from matrx_ai._ext import get_perishable_state_marker
    from matrx_ai.config.perishable_state import mark_perishable_state

    decider = get_perishable_state_marker()
    if decider is None or not conversation_id or not getattr(config, "messages", None):
        return
    try:
        if not await decider(
            conversation_id=str(conversation_id),
            structure_is_live=bool(getattr(config, "responder_mandate_key", None)),
        ):
            return
        cut_context = prep.history_cut_context
        if cut_context is None:
            warm, previous = _cut_context(str(conversation_id), cache_state, ttl_secs=_prep_history_ttl(prep, config))
            cut_context = {"warm": warm, "previous": previous, "waits": True}
        previous = cut_context.get("previous") or {}
        recorded = {str(k) for k in previous.get("stale") or []}
        hold = bool(cut_context.get("warm")) and bool(cut_context.get("waits"))
        report = mark_perishable_state(config.messages, only=recorded if hold else None)
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
    _record_stale_markers(
        prep,
        conversation_id=str(conversation_id),
        hold=hold,
        warm=bool(cut_context.get("warm")),
        previous=previous,
        marked=sorted(set(report.marked_keys)),
    )
    if report.blocks_marked:
        vcprint(
            f"[send_boundary/{prep.stage}] {conversation_id}: marked "
            f"{report.blocks_marked} earlier-turn workspace reading(s) stale "
            f"({', '.join(sorted(set(report.tools)))}).",
            color="cyan",
        )


def _record_stale_markers(
    prep: SendPrep,
    *,
    conversation_id: str,
    hold: bool,
    warm: bool,
    previous: dict[str, Any],
    marked: list[str],
) -> None:
    """Record the stale markers' cache decision the way the window records its cut: on the request
    (``history_cut.stale_markers`` → ``cx_request.metadata``) and, when they moved, on the cut persistence
    writes into ``cx_conversation.cache_state`` (``history_cut.stale``)."""
    from matrx_ai.context.app_context import try_get_app_context

    recorded = sorted({str(k) for k in previous.get("stale") or []})
    if hold:
        decision = {"action": "held_warm", "reason": "the provider cache is warm", "marked": len(marked), "cache_break": False}
    else:
        moved = marked != recorded
        decision = {
            "action": "moved" if moved else "unchanged",
            "reason": "the provider cache is cold" if not warm else "the cold-cache gate is off (knob)",
            "marked": len(marked),
            "cache_break": bool(moved),
        }
        cut = dict(_HISTORY_CUT_MEMO.get(conversation_id) or previous or {})
        cut["stale"] = marked
        _remember_history_cut(conversation_id, cut)
    prep.steps.append(f"stale_markers:{decision['action']}")
    prep.prefix_parts["stale_markers"] = dict(decision)
    ctx = try_get_app_context()
    if ctx is not None:
        entry = dict(ctx.metadata.get("history_cut") or {"conversation_id": conversation_id})
        entry["stale_markers"] = decision
        ctx.metadata["history_cut"] = entry
    if decision["cache_break"]:
        vcprint(
            f"[send_boundary/{prep.stage}] {conversation_id}: stale markers MOVED ({decision['reason']}): "
            f"{len(marked)} earlier block(s) marked — a deliberate cache break.",
            color="yellow",
        )


def _carried_org(organization_id: str | None) -> str | None:
    """The organization the caller passes, else the carried AppContext's — read, never rebuilt."""
    if organization_id is not None:
        return str(organization_id)
    try:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        org = getattr(ctx, "organization_id", None) if ctx is not None else None
    except Exception:  # noqa: BLE001 — no carried context is a legal standalone call
        org = None
    return str(org) if org else None


async def _stage_agent_identity(prep: SendPrep, config: Any, *, organization_id: str | None) -> None:
    """Tell the model who made it: AI Matrx and the catalog lab of ``config.model``.

    Staged in the turn-context policy ``agent_identity`` on every loop send (idempotent: the
    slot is replaced), so a model switch names the new lab and no frozen or held system
    prefix ever changes. Skipped when the system instruction has identity off (non-chat
    models). A failure is announced and the send goes out without the part.
    """
    from matrx_ai.config.agent_identity import IDENTITY_SLOT, render_identity

    messages = getattr(config, "messages", None)
    attach = getattr(messages, "attach_turn_context", None)
    if attach is None:
        return
    si = getattr(config, "system_instruction", None)
    if si is not None and not getattr(si, "include_identity", True):
        attach("", slot=IDENTITY_SLOT)
        return
    from matrx_ai.config.request_firewall import self_description_withheld

    if self_description_withheld():
        # A request firewall lists terms that must not reach the model: the platform's note
        # about itself is left out (owner ruling, 2026-10-27; ``request_firewall`` header).
        attach("", slot=IDENTITY_SLOT)
        prep.steps.append("agent_identity_withheld")
        return
    try:
        block = await render_identity(getattr(config, "model", None), _carried_org(organization_id))
    except Exception as exc:  # noqa: BLE001 — shaping never costs a send
        attach("", slot=IDENTITY_SLOT)
        vcprint(
            f"[send_boundary/{prep.stage}] step 'agent_identity' failed (ignored): "
            f"{type(exc).__name__}: {exc} — this send goes out without telling the agent "
            "who made it.",
            color="red",
        )
        logger.error("send_boundary agent_identity failed: %s: %s", type(exc).__name__, exc, exc_info=True)
        return
    attach(block or "", slot=IDENTITY_SLOT)
    if block:
        prep.steps.append("agent_identity")


async def _stage_run_environment(prep: SendPrep, config: Any) -> None:
    """Stage the ENVIRONMENT block (``config/run_environment.py``) in slot ``run_environment``.

    Present on every send of a run that holds at least one tool (a run with no tools gets none) unless the
    author switched the platform note ``run_environment`` off (``run_environment.environment_switch``); it
    is NOT identity and does not hang on the author's ``include_identity`` switch. Re-rendered whenever the
    held or loadable tool set changes, byte-identical otherwise. A
    prompt that names a tool the run does not hold is announced (yellow) and recorded as a step;
    the block itself says they are not available here. A failure is announced and the send
    goes out without the block.
    """
    from matrx_ai.config import run_environment as env_mod
    from matrx_ai.config.run_environment import ENVIRONMENT_SLOT, render_for_run

    messages = getattr(config, "messages", None)
    attach = getattr(messages, "attach_turn_context", None)
    if attach is None:
        return
    try:
        # The author's switch (platform note ``run_environment``): off = no block, the rung recorded.
        on, decided_by = await env_mod.environment_switch(env_mod._carried_context())
        if not on:
            attach("", slot=ENVIRONMENT_SLOT)
            prep.steps.append(f"run_environment_off:{decided_by}")
            return
        block, env, absent = await render_for_run(config)
    except Exception as exc:  # noqa: BLE001 — shaping never costs a send
        attach("", slot=ENVIRONMENT_SLOT)
        vcprint(
            f"[send_boundary/{prep.stage}] step 'run_environment' failed (ignored): "
            f"{type(exc).__name__}: {exc} — this send goes out without the ENVIRONMENT block.",
            color="red",
        )
        logger.error("send_boundary run_environment failed: %s: %s", type(exc).__name__, exc, exc_info=True)
        return
    attach(block, slot=ENVIRONMENT_SLOT)
    if not block:
        return
    prep.steps.append(f"run_environment:{env.name.lower()}")
    if absent:
        prep.steps.append("run_environment_prompt_drift:" + ",".join(absent))
        vcprint(
            f"[send_boundary/{prep.stage}] the agent's instructions name tools this run does not hold: "
            f"{', '.join(absent)} — fix the agent's prompt through the agent builder.",
            color="yellow",
        )


async def _stage_person_context(prep: SendPrep, config: Any) -> None:
    """Stage the person's saved memories and custom instructions (``config/person_context.py``).

    Slot ``person_context`` of the turn-context channel, replaced on every loop send (rendered once
    per turn). The gate reads the carried AppContext: a sealed chat, a temporary chat without the
    turn's opt-in, a machine or child run get an empty slot. Skipped for non-chat models. A failure
    is announced and the send goes out without the block.
    """
    from matrx_ai.config.person_context import PERSON_CONTEXT_SLOT, render_person_context

    messages = getattr(config, "messages", None)
    attach = getattr(messages, "attach_turn_context", None)
    if attach is None:
        return
    si = getattr(config, "system_instruction", None)
    if si is not None and not getattr(si, "include_identity", True):
        attach("", slot=PERSON_CONTEXT_SLOT)
        return
    try:
        # The run's whole tool set (preloaded, discovered mid-conversation, inline): a memory naming a tool outside it is flagged.
        from matrx_ai.config.run_environment import reachable_tool_names
        from matrx_ai.context.app_context import try_get_app_context

        # Held PLUS loadable (load_chrome_tools' own gates): a memory naming a loadable tool is not flagged.
        block, why = await render_person_context(try_get_app_context(), await reachable_tool_names(config) or None)
    except Exception as exc:  # noqa: BLE001 — shaping never costs a send
        attach("", slot=PERSON_CONTEXT_SLOT)
        vcprint(
            f"[send_boundary/{prep.stage}] step 'person_context' failed (ignored): "
            f"{type(exc).__name__}: {exc} — this send goes out without the person's saved "
            "memories and instructions.",
            color="red",
        )
        logger.error("send_boundary person_context failed: %s: %s", type(exc).__name__, exc, exc_info=True)
        return
    attach(block, slot=PERSON_CONTEXT_SLOT)
    prep.steps.append("person_context" if block else f"person_context_withheld:{why}")


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


async def _name_speakers(prep: SendPrep, config: Any) -> None:
    """Name each person turn's writer when two or more people wrote in this chat (``config/speakers.py``).

    A failure is announced loudly and skipped: the send goes out unnamed, exactly as before.
    """
    from matrx_ai.config.speakers import name_speakers

    source = prep.wire_config if prep.wire_config is not None else config
    messages = getattr(source, "messages", None)
    try:
        named = await name_speakers(list(messages or []))
    except Exception as exc:  # noqa: BLE001 — shaping never costs a send
        vcprint(
            f"[send_boundary/{prep.stage}] step 'speaker_names' failed (ignored): "
            f"{type(exc).__name__}: {exc} — this send goes out without the speakers' names.",
            color="red",
        )
        logger.error("send_boundary speaker_names failed: %s: %s", type(exc).__name__, exc, exc_info=True)
        return
    if named is None:
        return
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    wire.messages = _wire_list(messages, named)
    prep.wire_config = wire
    prep.steps.append("speaker_names")


async def _apply_template_thinking(prep: SendPrep, config: Any, profile: Any) -> None:
    """``config/template_thinking.py`` — records its own step name and notes, and fails closed itself."""
    from matrx_ai.config.template_thinking import apply_template_thinking

    await apply_template_thinking(prep, config, profile)


async def _stage_helper_roster(
    prep: SendPrep, config: Any, *, conversation_id: str | None, organization_id: str | None
) -> None:
    """Restate the agent's helpers on this send (``config/helper_roster.py``).

    A failure is announced loudly and skipped: the send goes out with the slot cleared, never
    with a stale roster.
    """
    from matrx_ai.config.helper_roster import stage_helper_roster

    try:
        if await stage_helper_roster(
            config, conversation_id=conversation_id, organization_id=_carried_org(organization_id)
        ):
            prep.steps.append("helper_roster")
    except Exception as exc:  # noqa: BLE001 — shaping never costs a send
        vcprint(
            f"[send_boundary/{prep.stage}] step 'helper_roster' failed (ignored): "
            f"{type(exc).__name__}: {exc} — this send goes out without the agent's helpers list.",
            color="red",
        )
        logger.error("send_boundary helper_roster failed: %s: %s", type(exc).__name__, exc, exc_info=True)


async def _stage_tool_briefings(prep: SendPrep, config: Any) -> None:
    """Stage every registered tool briefing this run's tools call for (``config/tool_briefings.py``).

    Each rides its own slot of the turn-context channel, so the turn's first send freezes it and
    no later send rewrites a cached prefix. A failing source is announced loudly and its slot goes
    out empty: the send is never lost and a stale briefing is never sent.
    """
    from matrx_ai.config.tool_briefings import stage_tool_briefings

    try:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 — no carried context is a legal standalone call
        ctx = None
    staged, failed = await stage_tool_briefings(config, ctx)
    for slot, exc in failed:
        vcprint(
            f"[send_boundary/{prep.stage}] step 'tool_briefing:{slot}' failed (ignored): "
            f"{type(exc).__name__}: {exc} — this send goes out without that briefing.",
            color="red",
        )
        logger.error(
            "send_boundary tool_briefing %s failed: %s: %s", slot, type(exc).__name__, exc, exc_info=exc
        )
    prep.steps.extend(f"tool_briefing:{slot}" for slot in staged)


async def _store_person_inline_media(prep: SendPrep, config: Any) -> None:
    """The BACKSTOP for a person's inline-only attachments (``keep_inline_person_media_or_capture``).

    The executor stores them once, before it reserves the person's row (CGU-10 AND-IMG13 #1), and
    writes each id back onto the part object this config holds — so here every part already names
    its file and nothing uploads. A caller that reaches the send without the executor (a single
    send, a helper) gets the same one upload here. A failure is captured, never blocks the send."""
    from matrx_ai.persistence.sealed import keep_inline_person_media_or_capture

    if await keep_inline_person_media_or_capture(getattr(config, "messages", None), where="send_boundary"):
        prep.steps.append("store_person_inline_media")


async def _run_step_off_loop(prep: SendPrep, name: str, fn: Any, *, records_itself: bool = False) -> None:
    """``_run_step`` in a worker thread: for a step whose cost grows with the whole wire (every field of every part),
    which must never hold the event loop. The boundary's per-config lock is held while it runs."""
    await asyncio.to_thread(_run_step, prep, name, fn, records_itself=records_itself)


def _run_step(prep: SendPrep, name: str, fn: Any, *, records_itself: bool = False) -> None:
    """Run one shaping step; a failure is announced and skipped, never fatal.

    ``records_itself``: the step appends its own name only when it changed something."""
    try:
        fn()
        if not records_itself:
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
    _AUTHORED_CEILING.pop(_loop_key(conversation_id, request_id), None)
    _CEILING_ANNOUNCED.pop(_loop_key(conversation_id, request_id), None)
    _ANSWER_ROOM.pop(_loop_key(conversation_id, request_id), None)
    if conversation_id:
        _CACHE_STATE_MEMO.pop(conversation_id, None)
        _TRIM_REPLAY_MEMO.pop(str(conversation_id), None)
        _TRIM_REPLAY_DROPPED.pop(str(conversation_id), None)
        _PREFIX_BYTES_MEMO.pop(str(conversation_id), None)
