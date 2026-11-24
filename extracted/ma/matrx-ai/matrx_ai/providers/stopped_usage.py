"""A stopped call is billed for what it generated — never left at ~0 because its usage block never came.

A provider reports usage at the END of a stream (OpenAI-style chat completions: the last chunk;
Anthropic: ``message_delta``). When the person presses Stop the stream is cut first, so that block
never arrives: Anthropic's adapter keeps only ``message_start``'s count (8 output tokens beside a
4,983-character reply, $0.000118), and OpenAI-compatible adapters keep nothing at all (no provider,
no tokens, $0). T4-C, 2026-11-14: 172 of 189 stopped provider rows in 7 days carried no cost; 29 had
visible replies over 400 characters. The provider billed every token it generated.

:func:`complete_stopped_call_usage` runs at the ONE dispatch seam every provider call passes
(``UnifiedAIClient._dispatch_admitted``) when the call is cancelled. It measures what the call
actually generated — the turn text the stream carried (``get_turn_text``; the emitter clears it
before each model call, so it is this call's text) — through the ONE budget estimator
(``context_trim.estimate_budget_tokens``), and the prompt through the one prompt estimator
(``context_preflight.estimate_prompt_tokens``). Then:

* no usage attached → attach an estimated ``TokenUsage`` for this call's model/offering;
* usage attached but its output is below the estimate → raise the output to the estimate;
* the output counts the REASONING the call streamed as well as its visible text (the emitter's
  ``get_turn_reasoning_chars``): a call stopped while the model was still thinking was billed 8 tokens
  (run a90b318b, 2026-11-15) — reasoning tokens are output tokens the provider bills;
* HIDDEN thinking counts too. A model that hides its reasoning streams a "reasoning started" frame and
  then nothing, so no reasoning characters arrive: run 5b068a57 (claude-haiku-5-5, 2026-11-15) thought
  ~4.6 s in hiding and was billed 8 tokens, while at ~213 tokens/s the provider generated ~980. The
  thinking estimate is therefore the LARGER of the reasoning that streamed and the elapsed thinking time
  (the emitter's ``get_turn_thinking_ms``: this call's reasoning-start frame to the stop, never time before
  the provider began) x the model's output rate. The rate is catalog data,
  ``ai.offering.metadata.output_tokens_per_second`` (a knob, seeded from measured completed calls); an
  offering without one uses :data:`DEFAULT_OUTPUT_TOKENS_PER_SECOND` and the note says so;
* an emitter that keeps no turn text (a capture, tee or block emitter) bills the same input — the
  seam runs only for a DISPATCHED call, so a stopped call's row with no usage at all means no call was
  sent (``db/persistence.py`` marks such a row ``provider_call_sent: false``);
* a call stopped BEFORE its first token (no streamed text) still carries the estimated INPUT tokens
  with output 0 — the provider charges for the prompt it read. This seam runs only for a call that was
  DISPATCHED; a Stop that lands before the run's root opened never reaches a provider (the loop's
  iteration-0 stop check runs before the first call), so there is nothing to bill then;
* the counted input is priced the way the provider bills it (``_cache_split``; the lead's ruling of
  2026-11-16, made in Arman's absence, which he may overrule): the cache-marked prefix (system + tools) is
  priced from THIS send's own evidence: a cache read when an accepted send of the same provider cache
  scope (vendor + API-key fingerprint + prefix) was recorded before it; a prefix this send was first to
  write is priced as uncached input at 1x (ruling of 2026-11-17: a stopped call never costs above the
  full uncached price), and so is an unknown prefix; the rest is uncached input;
* usage at or above the estimate → untouched (the provider's own count wins).

Every estimate says so: ``usage.metadata["usage_estimated"]`` (copied onto the ``chat.request``
row's metadata by ``orchestrator/requests.py``), with the characters it was measured from.
Never raises: cost capture must never mask the stop.
"""

from __future__ import annotations

import asyncio
from typing import Any

from matrx_utils import vcprint

__all__ = [
    "DEFAULT_OUTPUT_TOKENS_PER_SECOND",
    "complete_stopped_call_usage",
    "hidden_thinking_rate",
    "stopped_output_estimate",
]

#: The stated fallback when an offering carries no ``output_tokens_per_second``: the slowest chat model we
#: measured (gpt-6.1-sol, p50 31 tokens/s over 7 days, 2026-11-15). Low on purpose — with no figure, the
#: estimate under-bills rather than over-bills the person. Announced in every estimate that uses it.
DEFAULT_OUTPUT_TOKENS_PER_SECOND = 30.0

#: The catalog key (``ai.offering.metadata``) holding a model's measured output rate.
OUTPUT_RATE_KEY = "output_tokens_per_second"


def _turn_texts() -> tuple[str, str | None, int, int] | None:
    """(this call's generated text, the part that left on the wire, reasoning characters streamed,
    milliseconds this call spent thinking) — None without a text stream."""
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        emitter = getattr(ctx, "emitter", None) if ctx is not None else None
        getter = getattr(emitter, "get_turn_text", None)
        if not callable(getter):
            return None
        generated = getter() or ""
        sent_getter = getattr(emitter, "sent_text_snapshot", None)
        sent = sent_getter() if callable(sent_getter) else None
        reasoning_getter = getattr(emitter, "get_turn_reasoning_chars", None)
        reasoning = int(reasoning_getter() or 0) if callable(reasoning_getter) else 0
        thinking_getter = getattr(emitter, "get_turn_thinking_ms", None)
        thinking_ms = int(thinking_getter() or 0) if callable(thinking_getter) else 0
        return generated, sent, reasoning, max(0, thinking_ms)
    except Exception:  # noqa: BLE001
        return None


def stopped_output_estimate(text: str, *, reasoning_chars: int = 0) -> int:
    """Output tokens for ``text`` plus ``reasoning_chars`` of streamed thinking, through the one budget
    estimator (0 for neither). Reasoning tokens are output tokens: every provider bills them so."""
    from matrx_ai.config.context_trim import estimate_budget_tokens

    chars = len(text or "") + max(0, int(reasoning_chars or 0))
    return estimate_budget_tokens(chars, "prose") if chars else 0


def hidden_thinking_rate(profile: Any) -> tuple[float, bool]:
    """(the model's output tokens/s from the catalog, True) — or (the stated default, False) without one."""
    meta = getattr(profile, "offering_metadata", None)
    raw = meta.get(OUTPUT_RATE_KEY) if isinstance(meta, dict) else None
    try:
        rate = float(raw) if raw is not None else 0.0
    except (TypeError, ValueError):
        rate = 0.0
    if rate > 0:
        return rate, True
    return DEFAULT_OUTPUT_TOKENS_PER_SECOND, False


def _prompt_estimate(config: Any) -> int:
    if config is None:
        return 0
    try:
        from matrx_ai.config.context_preflight import estimate_prompt_tokens

        return int(estimate_prompt_tokens(config) or 0)
    except Exception:  # noqa: BLE001
        return 0


def _cache_split(config: Any, prompt: int, evidence: Any = None) -> tuple[int, int, str]:
    """(cache-read tokens, 5-minute cache-write tokens, the note's branch) for ``prompt`` counted tokens.

    The lead's ruling (2026-11-16, made in Arman's absence; he may overrule it): an estimate is priced the
    way the provider bills it. The cache-marked prefix (system + tool declarations, the prefix
    ``config/cache_plan.py`` tracks) is priced from THIS send's own evidence (``cache_plan.PrefixEvidence``,
    never the prefix's latest state): a CACHE READ when an accepted send of the same provider cache scope
    was recorded within the cache life before this send began; otherwise (first sent by this send, or unknown)
    UNCACHED INPUT at 1x, never the 1.25x write rate — a stopped call never costs
    more than the full uncached price (rulings of 2026-11-16 and 11-17, same terms). The rest is uncached
    input. A send with no cache marks is all uncached input.
    Live walk 2026-11-16: 48,138 tokens all at full input = $0.096276 where the provider billed 2,945
    uncached + 37,458 cache-read = $0.009716."""
    if config is None or prompt <= 0:
        return 0, 0, ""
    try:
        from matrx_ai.config.cache_plan import (
            MARKS_NONE,
            PREFIX_READ,
            PREFIX_UNKNOWN,
            PREFIX_WRITE,
            marks_for,
        )
        from matrx_ai.config.context_preflight import estimate_cache_prefix_tokens

        if marks_for(config) == MARKS_NONE:
            return 0, 0, "; no cache marks on this send, all uncached input"
        prefix = min(prompt, max(0, int(estimate_cache_prefix_tokens(config) or 0)))
        if prefix <= 0:
            return 0, 0, ""
        # THIS send's own evidence, never the prefix's latest state (another send never changes it).
        state = getattr(evidence, "state", PREFIX_UNKNOWN)
        if state == PREFIX_READ:
            return prefix, 0, f"; the {prefix}-token cached prefix was warm, priced as a cache read"
        if state == PREFIX_WRITE:
            # Lead ruling 2026-11-17 (A, made in Arman's absence; he may overrule): never the 1.25x write rate. A
            # record missing from OUR store proves a write only if every sender of this key records there; another
            # stage or tool on the same key may have warmed it. 1x keeps "never above full uncached" by construction.
            return 0, 0, (
                f"; the {prefix}-token cached prefix was first sent by this send, priced as uncached input "
                "(a stopped call is never priced at the cache-write rate)"
            )
        return 0, 0, f"; the {prefix}-token cached prefix was unknown (not seen warm or written), priced as uncached input"
    except Exception as err:  # noqa: BLE001 — announced; the whole prompt stays uncached input
        vcprint(
            f"🚨 [stopped_usage] could not split a stopped call's prompt into its cache prefix "
            f"({type(err).__name__}: {err}); priced as uncached input.",
            color="red",
        )
        return 0, 0, "; cache split unavailable, all uncached input"


def complete_stopped_call_usage(
    exc: BaseException, *, profile: Any, config: Any = None, prefix_evidence: Any = None
) -> None:
    """Make a cancelled call's billed usage cover what it generated (see module doc). Never raises."""
    if not isinstance(exc, asyncio.CancelledError):
        return
    try:
        # An emitter with no turn text (a capture / tee / block emitter) still dispatched this call: the
        # provider read the prompt, so it is billed its input (run 1aacd937, 2026-11-15: a stopped helper
        # call left a provider row with no tokens and no cost).
        generated, sent, reasoning, thinking_ms = _turn_texts() or ("", None, 0, 0)
        output = stopped_output_estimate(generated, reasoning_chars=reasoning)
        thinking_note = ""
        if thinking_ms > 0:
            rate, from_catalog = hidden_thinking_rate(profile)
            timed = round(thinking_ms / 1000 * rate)
            streamed = stopped_output_estimate("", reasoning_chars=reasoning)
            if timed > streamed:
                # Streamed reasoning is PART of the thinking, never added on top of it.
                output += timed - streamed
                source = (
                    f"the catalog rate {rate:g} tokens/s"
                    if from_catalog
                    else f"the stated default {rate:g} tokens/s (no {OUTPUT_RATE_KEY} on this offering)"
                )
                thinking_note = (
                    f"; hidden thinking estimated as {thinking_ms / 1000:.1f} s x {source} = {timed} tokens"
                )
        prompt = _prompt_estimate(config)
        from matrx_ai.providers.errors import get_billed_usage as _billed

        if prefix_evidence is not None and (
            generated or reasoning > 0 or thinking_ms > 0 or _billed(exc) is not None
        ):
            # The stream started (text, reasoning, a thinking frame or the adapter's start usage): the
            # provider accepted this call, so its prefix is recorded for later sends.
            prefix_evidence.accepted()
        if output <= 0 and prompt <= 0:
            return  # nothing generated and nothing measurable read: nothing to bill
        from matrx_ai.config import TokenUsage
        from matrx_ai.providers.errors import attach_billed_usage, get_billed_usage

        note = (
            f"stopped call: the provider's usage block never arrived; output estimated from "
            f"{len(generated)} generated characters ({len(sent) if sent is not None else '?'} sent) "
            f"and {reasoning} reasoning characters{thinking_note}"
        )
        cache_read, cache_write, cache_note = _cache_split(config, prompt, prefix_evidence)
        billed = get_billed_usage(exc)
        if billed is None:
            usage = TokenUsage(
                # Inclusive of a cache write (the Anthropic convention); a cache read is not input.
                input_tokens=prompt - cache_read,
                output_tokens=output,
                cached_input_tokens=cache_read,
                cache_write_5m_tokens=cache_write,
                matrx_model_name=str(getattr(profile, "model_name", "") or ""),
                provider_model_name=str(getattr(profile, "provider_model_id", "") or ""),
                api=str(getattr(profile, "vendor", "") or ""),
                offering_id=str(getattr(profile, "offering_id", "") or ""),
            )
            usage.metadata["usage_estimated"] = note + "; input from the counted prompt" + cache_note
            attach_billed_usage(exc, usage)
            return
        if not isinstance(billed, TokenUsage):
            return
        reported = billed.output_tokens
        raised = reported < output
        fills_input = billed.input_tokens + billed.cached_input_tokens <= 0 < prompt
        if not (raised or fills_input):
            return  # the provider's own counts win — never lowered
        if raised:
            billed.output_tokens = output
        if fills_input:
            billed.input_tokens = prompt - cache_read
            billed.cached_input_tokens = cache_read
            billed.cache_write_5m_tokens = cache_write
        billed.metadata["usage_estimated"] = f"{note}; the provider had reported {reported}" + (
            cache_note if fills_input else ""
        )
    except Exception as err:  # noqa: BLE001 — the stop proceeds; the gap is announced
        vcprint(
            f"🚨 [stopped_usage] could not estimate a stopped call's usage "
            f"({type(err).__name__}: {err}); its cost may be under-recorded.",
            color="red",
        )
