"""Make every call FIT before it is sent — detection, the compaction seam, and a forced-trim fallback.

THE DEFECT THIS CLOSES (2026-10-22, conversation 9b224bf5): a long sandbox conversation on Claude
Opus 5.5 (1,000,000-token window) reached ~270k input tokens. The cost-gated trim held (cache
payback), the context pre-flight passed (270k is far under the window), and then the host's
per-call input cap (200,000, ``automation.guardrails/max_input_tokens``, applied because the turn
was the agent waking itself — "automated") REFUSED the call. The conversation died. Two limits
existed; neither one shrank anything, and the trim never knew the lower one.

THE RULE: before a call is sent, it is measured against EVERY limit that applies to it — the
model's context window (× the pre-flight trip fraction) and the host's per-call input budget — and
when it is over, it is made to fit:

  1. COMPACTION (the summarization system — installed by the host via ``set_compactor``), at the
     RESOLVE stage only: at the loop stage the list is the executor's ledger (indexes) and only
     the forced trim runs.
  2. Fallback until compaction exists: a FORCED trim — the cache gate ignored, older tool results
     and tool-call arguments reduced to their previews — stepping to more aggressive tiers.
  3. Still over: nothing more is done here; the pre-flight / host guard refuse with their own
     sentence. Every pass is announced and recorded on ``SendPrep.fit``.

The host's budget comes through ONE injected resolver (``set_input_budget_resolver``): this package
never imports the host. The resolver returns ``(limit_tokens, estimated_tokens)`` measured with the
HOST's own estimator, so the fit decision and the host's refusal can never disagree.
"""

from __future__ import annotations

import dataclasses
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import vcprint

logger = logging.getLogger(__name__)

#: ``(ctx, config) -> (limit_tokens, estimated_tokens) | None``. ``None`` = no host budget applies.
InputBudgetResolver = Callable[[Any, Any], "tuple[int, int] | None"]
#: ``(config, *, limit_tokens, estimated_tokens, ctx, conversation_id) -> bool`` — True when it
#: compacted something. ``conversation_id`` is the SEND's conversation (the ambient ``ctx`` may name
#: another one); the compactor refuses a mismatch.
Compactor = Callable[..., Awaitable[bool]]

#: The send boundary's resolve stage (``send_boundary.STAGE_RESOLVE``; not imported — that module
#: imports this one): the only stage at which the compactor may change the message list.
_STAGE_RESOLVE = "resolve"

_budget_resolver: InputBudgetResolver | None = None
_compactor: Compactor | None = None

#: Forced-trim tiers tried in order (positions back, minimum chars). Position = half an iteration,
#: so ``2`` keeps the newest iteration's results intact — the model always sees what it just did.
FORCED_TIERS: tuple[tuple[int, int, int, int], ...] = (
    # (tier_1_back, tier_1_chars, tier_2_back, tier_2_chars)
    (4, 4000, 8, 1000),
    (2, 1000, 2, 400),
)


def set_input_budget_resolver(resolver: InputBudgetResolver | None) -> None:
    """Host hook: the per-call input budget (aidream: ``platform_guardrails.input_budget``)."""
    global _budget_resolver
    _budget_resolver = resolver


def set_compactor(compactor: Compactor | None) -> None:
    """Host hook: the conversation compaction (summarization) system. See ``ensure_fits``."""
    global _compactor
    _compactor = compactor


def _limits(config: Any) -> list[dict[str, Any]]:
    """Every limit that applies to this call, each with its own measurement."""
    from matrx_ai.config.context_preflight import (
        _POLICY,
        _declared_window,
        estimate_prompt_tokens,
    )

    found: list[dict[str, Any]] = []
    if _POLICY.enabled:
        model_ref = str(
            getattr(config, "matrx_model_name", None) or getattr(config, "model", "") or ""
        )
        window = _declared_window(model_ref) if model_ref else None
        if window:
            found.append(
                {
                    "limit": "context_window",
                    "limit_tokens": int(window * _POLICY.trip_fraction),
                    "estimated_tokens": estimate_prompt_tokens(config),
                }
            )
    if _budget_resolver is not None:
        from matrx_ai.context.app_context import try_get_app_context

        try:
            budget = _budget_resolver(try_get_app_context(), config)
        except Exception as exc:  # noqa: BLE001 — a broken read never blocks; the host guard still runs
            vcprint(
                f"[input_fit] host input budget unreadable ({type(exc).__name__}: {exc})",
                color="red",
            )
            logger.error("input_fit: host input budget resolver raised", exc_info=True)
            budget = None
        if budget:
            limit_tokens, estimated = budget
            found.append(
                {
                    "limit": "host_input_budget",
                    "limit_tokens": int(limit_tokens),
                    "estimated_tokens": int(estimated),
                }
            )
    return found


def _over(limits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [lim for lim in limits if lim["estimated_tokens"] > lim["limit_tokens"]]


async def ensure_fits(
    config: Any,
    *,
    policy: Any,
    stage: str,
    conversation_id: str | None,
    trim: Callable[[list[Any], Any], Any],
) -> dict[str, Any] | None:
    """Detect an over-limit call and make it fit. Returns the record (``None`` = nothing applied).

    ``trim`` is ``send_boundary._forced_trim`` — the trim seam lives only in the send boundary."""
    limits = _limits(config)
    over = _over(limits)
    if not over:
        return {"fits": True, "limits": limits} if limits else None

    record: dict[str, Any] = {"fits": False, "before": over, "passes": []}
    worst = max(over, key=lambda lim: lim["estimated_tokens"] - lim["limit_tokens"])
    vcprint(
        f"[input_fit/{stage}] {conversation_id or '-'}: ~{worst['estimated_tokens']:,} input tokens over "
        f"{worst['limit']} {worst['limit_tokens']:,} — making it fit",
        color="yellow",
    )

    # ===================================================================================== #
    # COMPACTION INSERTION POINT — the summarization system plugs in HERE, via              #
    # ``set_compactor(...)`` from the host. It receives the config (messages are mutable in #
    # place), the tightest limit and the current estimate, and returns True when it         #
    # compacted. It runs BEFORE the forced trim below; when it brings the call under every  #
    # limit, the forced trim never runs. Until a compactor is installed, the forced trim is #
    # the only thing that keeps an over-limit conversation alive.                           #
    # ===================================================================================== #
    # Compaction runs ONLY at the resolve stage — before the executor records its turn cursors.
    # At the loop stage ``config`` is the executor's live ledger: its trigger position, its
    # pre-execution count and ``committed_position`` are list INDEXES, and the history may only
    # GROW during a turn (``executor._scream_if_history_shifted``). Splicing a summary into it
    # mid-turn files ``persisted_history_shifted`` and the barrier reverts it — the paid condense
    # is wasted and rows of the turn can be lost. An over-limit loop iteration takes the forced
    # trim below (it rewrites blocks in place, never removes a message); the next turn's resolve
    # condenses.
    if _compactor is not None and stage != _STAGE_RESOLVE:
        record["passes"].append({"pass": "compaction", "changed": False, "skipped": "loop_stage"})
    elif _compactor is not None:
        from matrx_ai.context.app_context import try_get_app_context

        try:
            compacted = await _compactor(
                config,
                limit_tokens=worst["limit_tokens"],
                estimated_tokens=worst["estimated_tokens"],
                ctx=try_get_app_context(),
                conversation_id=conversation_id,
            )
        except Exception as exc:  # noqa: BLE001 — compaction failure falls through to the forced trim
            vcprint(
                f"[input_fit] compaction failed ({type(exc).__name__}: {exc}); forced trim next",
                color="red",
            )
            logger.error("input_fit: compactor raised", exc_info=True)
            compacted = False
        record["passes"].append({"pass": "compaction", "changed": bool(compacted)})
        over = _over(_limits(config))
        if not over:
            record["fits"] = True
            return record

    # FALLBACK — forced trim, cache gate ignored, stepping to more aggressive tiers.
    from matrx_ai.config.context_trim import TrimPolicy

    messages = getattr(config, "messages", None)
    if messages is not None:
        messages_list = messages if isinstance(messages, list) else list(messages)
        base = policy if isinstance(policy, TrimPolicy) else TrimPolicy()
        for t1_back, t1_chars, t2_back, t2_chars in FORCED_TIERS:
            forced = dataclasses.replace(
                base,
                tier_1_min_positions_back=t1_back,
                tier_1_min_output_chars=t1_chars,
                tier_2_min_positions_back=t2_back,
                tier_2_min_output_chars=t2_chars,
                source=f"{base.source}:forced_to_fit",
            )
            report = trim(messages_list, forced)
            record["passes"].append(
                {
                    "pass": f"forced_trim_{t1_back}_{t2_back}",
                    "blocks_rewritten": getattr(report, "blocks_rewritten", 0),
                    "freed_chars": getattr(report, "freed_chars", 0),
                }
            )
            over = _over(_limits(config))
            if not over:
                record["fits"] = True
                break

    record["after"] = _limits(config)
    if record["fits"]:
        vcprint(
            f"[input_fit/{stage}] {conversation_id or '-'}: fits now ({record['passes']})",
            color="yellow",
        )
    else:
        vcprint(
            f"[input_fit/{stage}] {conversation_id or '-'}: STILL over after every pass — the pre-flight / "
            "host guard will refuse. Compaction is the fix (see COMPACTION INSERTION POINT).",
            color="red",
        )
        logger.error("input_fit: call still over its limit after every pass: %s", record)
    return record


__all__ = [
    "FORCED_TIERS",
    "ensure_fits",
    "set_compactor",
    "set_input_budget_resolver",
]
