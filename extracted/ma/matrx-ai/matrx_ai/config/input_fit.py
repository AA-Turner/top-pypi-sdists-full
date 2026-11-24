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
  3. LAST RESORT (2026-11-06, Company Setup conversation b59d533b: 317 messages, ~230k tokens,
     refused although the forced trim ran): old thinking blocks and old tool-call arguments the
     tier previews cannot shrink. ``_stub_history_to_fit`` drops thinking from earlier turns, then
     replaces old tool-call arguments and tool results with a short visible stub, oldest first,
     until the call fits; then (2026-11-12) the TEXT of earlier messages, oldest first — a chat is
     never refused for its own history. The latest turn (from the last user message on) is never touched.
  4. Still over: nothing more is done here; the pre-flight / host guard refuse with their own
     sentence. Every pass is announced and recorded on ``SendPrep.fit``.

The host's budget comes through ONE injected resolver (``set_input_budget_resolver``): this package
never imports the host. It is called ``resolver(ctx, config, prompt_tokens)`` — ``prompt_tokens``
is THIS package's estimate of the call, measured once per measurement and shared, so a host that
needs no estimate of its own never re-walks the prompt — and may be sync or async. It returns
``(limit_tokens, estimated_tokens)`` measured with the HOST's own estimator when the host refuses
over it (so the fit decision and the host's refusal can never disagree), or
``(limit_tokens, estimated_tokens, False)`` for a CONDENSE-ONLY limit (2026-10-24: a person's own
chat is condensed at the conversation's cap, never trimmed or refused for it): over such a limit
only step 1 runs; step 2 runs only while an ENFORCED limit (the model's window, an enforced host
budget) is over.
"""

from __future__ import annotations

import dataclasses
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import vcprint

logger = logging.getLogger(__name__)

#: ``(ctx, config, prompt_tokens) -> (limit_tokens, estimated_tokens[, enforced]) | None`` (sync or
#: async). ``None`` = no host budget applies; a third item ``False`` = a condense-only limit
#: (compaction, never the forced trim).
InputBudgetResolver = Callable[[Any, Any, int], Any]
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


async def _limits(config: Any) -> list[dict[str, Any]]:
    """Every limit that applies to this call, each with its own measurement. The prompt is
    estimated ONCE here and shared with the host's resolver."""
    import inspect

    from matrx_ai.config.context_preflight import (
        _POLICY,
        _declared_window,
        estimate_prompt_tokens,
    )

    found: list[dict[str, Any]] = []
    prompt_tokens: int | None = None
    if _POLICY.enabled:
        model_ref = str(
            getattr(config, "matrx_model_name", None) or getattr(config, "model", "") or ""
        )
        window = _declared_window(model_ref) if model_ref else None
        if window:
            prompt_tokens = estimate_prompt_tokens(config)
            found.append(
                {
                    "limit": "context_window",
                    "limit_tokens": int(window * _POLICY.trip_fraction),
                    "estimated_tokens": prompt_tokens,
                    "enforced": True,
                }
            )
    if _budget_resolver is not None:
        from matrx_ai.context.app_context import try_get_app_context

        if prompt_tokens is None:
            prompt_tokens = estimate_prompt_tokens(config)
        try:
            budget = _budget_resolver(try_get_app_context(), config, prompt_tokens)
            if inspect.isawaitable(budget):
                budget = await budget
        except Exception as exc:  # noqa: BLE001 — a broken read never blocks; the host guard still runs
            vcprint(
                f"[input_fit] host input budget unreadable ({type(exc).__name__}: {exc})",
                color="red",
            )
            logger.error("input_fit: host input budget resolver raised", exc_info=True)
            budget = None
        if budget:
            limit_tokens, estimated = budget[0], budget[1]
            enforced = bool(budget[2]) if len(budget) > 2 else True
            found.append(
                {
                    "limit": "host_input_budget",
                    "limit_tokens": int(limit_tokens),
                    "estimated_tokens": int(estimated),
                    "enforced": enforced,
                }
            )
    return found


async def cut_to_fit_enforced(config: Any) -> bool:
    """True when this call's host input budget is ENFORCED (an automated call): the only calls the
    cut-to-fit pass shortens, and so the only calls an earlier cut is reapplied to. A person's own
    work carries a condense-only budget and is never cut."""
    return any(lim["limit"] == "host_input_budget" and lim.get("enforced", True) for lim in await _limits(config))


def _over(limits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [lim for lim in limits if lim["estimated_tokens"] > lim["limit_tokens"]]


def _enforced(limits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The over-limits the forced trim answers to (a condense-only limit is never one)."""
    return [lim for lim in limits if lim.get("enforced", True)]


async def ensure_fits(
    config: Any,
    *,
    policy: Any,
    stage: str,
    conversation_id: str | None,
    trim: Callable[[list[Any], Any], Any],
    stubbed_text_keys: set[str] | None = None,
) -> dict[str, Any] | None:
    """Detect an over-limit call and make it fit. Returns the record (``None`` = nothing applied).

    ``trim`` is ``send_boundary._forced_trim`` — the trim seam lives only in the send boundary.
    ``stubbed_text_keys``: when given, the ``text_stub_key`` of every message text the last-resort
    pass stubs is added to it (the send boundary keeps them stubbed on every later round,
    ``restub_known_texts``)."""
    limits = await _limits(config)
    over = _over(limits)
    if not over:
        return {"fits": True, "limits": limits} if limits else None

    record: dict[str, Any] = {"fits": False, "before": over, "passes": []}
    worst = max(over, key=lambda lim: lim["estimated_tokens"] - lim["limit_tokens"])
    if not _enforced(over) and (_compactor is None or stage != _STAGE_RESOLVE):
        # Over only a condense-only limit, where nothing may condense: the send goes as it is
        # (a person's own chat is never trimmed or refused for its cap; the turn end condenses).
        record["fits"] = True
        record["condense_only"] = True
        return record
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
    from matrx_ai.config.request_firewall import active_request_firewall

    firewall = active_request_firewall()
    if _compactor is not None and stage != _STAGE_RESOLVE:
        record["passes"].append({"pass": "compaction", "changed": False, "skipped": "loop_stage"})
    elif _compactor is not None and firewall is not None and firewall.firewall.must_not_contain:
        # A REQUEST FIREWALL lists terms: condensing would send the whole conversation through a
        # second model call this step never asked for — refused there, it would fail the step
        # AFTER its own answer. Skipped, said; the forced trim below makes the call fit, or the
        # pre-flight refuses it BEFORE anything is sent.
        record["passes"].append({"pass": "compaction", "changed": False, "skipped": "request_firewall"})
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
        over = _over(await _limits(config))
        if not over:
            record["fits"] = True
            return record
    if not _enforced(over):
        # Still over only a condense-only limit: never trimmed or refused for it.
        record["fits"] = True
        record["condense_only"] = True
        record["after"] = await _limits(config)
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
                    # Which blocks, by call id: the cache guard places them on the wire and
                    # accepts their rewrite as lawful (never by count).
                    "rewritten_blocks": [
                        _block_ref(entry) for entry in (getattr(report, "rewritten_blocks", None) or ())
                        if isinstance(entry, dict)
                    ],
                }
            )
            over = _over(await _limits(config))
            if not _enforced(over):
                record["fits"] = True
                break

    if not record["fits"] and messages is not None:
        messages_list = messages if isinstance(messages, list) else list(messages)
        before_tokens = max(lim["estimated_tokens"] for lim in _enforced(over)) if _enforced(over) else 0
        stub_pass = await _stub_history_to_fit(config, messages_list, stubbed_text_keys=stubbed_text_keys)
        after_limits = await _limits(config)
        over = _over(after_limits)
        stub_pass["tokens_trimmed"] = max(
            0, before_tokens - max((lim["estimated_tokens"] for lim in after_limits), default=0)
        )
        record["passes"].append(stub_pass)
        if stub_pass["thinking_blocks_dropped"] or stub_pass["stubbed_blocks"]:
            vcprint(
                f"[input_fit/{stage}] {conversation_id or '-'}: last-resort trim — dropped "
                f"{stub_pass['thinking_blocks_dropped']} earlier thinking block(s), stubbed "
                f"{stub_pass['stubbed_blocks']} earlier tool input/result block(s), "
                f"~{stub_pass['tokens_trimmed']:,} tokens trimmed",
                color="yellow",
            )
        if not _enforced(over):
            record["fits"] = True

    record["after"] = await _limits(config)
    _announce_history_trimmed(record, config, stage=stage, conversation_id=conversation_id)
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


#: The warning code of the one line the person reads when history was shortened to fit
#: (promoted to a visible line by @ai-matrx/chat ``PROMOTED_WARNING_CODES``).
HISTORY_TRIMMED_CODE = "history_trimmed_to_fit"
HISTORY_TRIMMED_LINE = "Earlier messages were shortened to fit this model."
#: Request-holder scope (``matrx_ai.context.request_once``): one line per request, not one per
#: loop iteration.
_ANNOUNCED_SCOPE = "history_trim_announced"


def summarize_passes(record: dict[str, Any]) -> str:
    """A short human line for the passes that ran (counts only). The per-block call-id lists stay
    in ``record`` for the cache guard; they never ride a warning's text (thousands of chars a row)."""
    parts: list[str] = []
    for step in record.get("passes") or []:
        counts = [
            f"{key}={step[key]}"
            for key in ("blocks_rewritten", "freed_chars", "thinking_blocks_dropped", "stubbed_blocks", "tokens_trimmed")
            if step.get(key)
        ]
        if counts:
            parts.append(f"{step.get('pass')}({', '.join(counts)})")
    return "; ".join(parts) or "no pass changed anything"


def _trim_changed_something(record: dict[str, Any]) -> bool:
    for step in record.get("passes") or []:
        if step.get("blocks_rewritten") or step.get("thinking_blocks_dropped") or step.get("stubbed_blocks"):
            return True
    return False


def _deepest_trim(record: dict[str, Any]) -> str:
    """The most aggressive pass that changed something (``forced_trim_2_4``, ``stub_history``)."""
    deepest = ""
    for step in record.get("passes") or []:
        if step.get("blocks_rewritten") or step.get("thinking_blocks_dropped") or step.get("stubbed_blocks"):
            deepest = str(step.get("pass") or deepest)
    return deepest


def trim_line_key(model: str, record: dict[str, Any]) -> str:
    """What the saved line stands for: this model, this depth of trim. A new model or a deeper trim
    is a new thing to say; the same trim on the next turn is not."""
    return f"{model}|{_deepest_trim(record)}"


def _said_in_this_conversation(config: Any, key: str) -> bool:
    """The conversation's newest saved trim line (``metadata.warnings`` on an answer, the path that
    shows it again on reload) already says this: same model, same trim."""
    for message in reversed(list(getattr(config, "messages", None) or [])):
        role = getattr(message, "role", None)
        if getattr(role, "value", role) != "assistant":
            continue
        metadata = getattr(message, "metadata", None)
        warnings = metadata.get("warnings") if isinstance(metadata, dict) else None
        for warning in warnings if isinstance(warnings, list) else []:
            if isinstance(warning, dict) and warning.get("code") == HISTORY_TRIMMED_CODE:
                meta = warning.get("metadata")
                return isinstance(meta, dict) and meta.get("once_key") == key
    return False


def _announce_history_trimmed(
    record: dict[str, Any], config: Any, *, stage: str, conversation_id: str | None
) -> None:
    """Law 4: a history shortened to fit is SAID in the chat, never only in the server log.

    One-chat C2 (a switch to a smaller model, e.g. one on this computer): the forced trim and the
    last-resort stubs rewrite what the model sees; the person reads one line, once per request
    (the request holder, with or without an app context), and once per conversation until the
    model or the depth of the trim changes (read from the saved line on the conversation's
    answers). A compaction pass has its own line and is not repeated here."""
    if not _trim_changed_something(record):
        return
    model = str(getattr(config, "matrx_model_name", None) or getattr(config, "model", "") or "")
    key = trim_line_key(model, record)
    if _said_in_this_conversation(config, key):
        vcprint(
            f"[input_fit/{stage}] {conversation_id or '-'}: history shortened to fit {model or 'the model'} "
            "again; the chat already says so (same model, same trim)",
            color="yellow",
            verbose=True,
        )
        return
    from matrx_ai.context.request_once import first_time_this_request

    if not first_time_this_request(_ANNOUNCED_SCOPE):
        return
    from matrx_connect.context.events import WarningPayload

    from matrx_ai.providers.outbound_params import send_client_warning

    send_client_warning(
        WarningPayload(
            code=HISTORY_TRIMMED_CODE,
            system_message=(
                f"[input_fit/{stage}] {conversation_id or '-'}: history shortened to fit {model or 'the model'} "
                f"({'fits' if record.get('fits') else 'still over'}; passes {summarize_passes(record)})"
            ),
            user_message=HISTORY_TRIMMED_LINE,
            level="medium",
            recoverable=True,
            metadata={"model": model, "fits": bool(record.get("fits")), "once_key": key},
        ),
        name="input_fit_history_trimmed",
    )


#: What an old tool call's arguments / a tool result become in the last-resort pass.
STUB_TOOL_INPUT = "[earlier tool input trimmed]"
STUB_TOOL_RESULT = "[earlier tool result trimmed]"
STUB_THINKING = "[earlier thinking trimmed]"
STUB_TEXT = "[earlier message trimmed to fit]"


def _block_type(block: Any) -> Any:
    t = getattr(block, "type", None)
    if t is None and isinstance(block, dict):
        t = block.get("type")
    return t


def _droppable_thinking(block: Any) -> bool:
    """A thinking block the last-resort pass may drop: never a Gemini thought (its contract
    requires every thought block resent as received)."""
    if _block_type(block) not in ("thinking", "redacted_thinking"):
        return False
    provider = getattr(block, "provider", None)
    if provider is None and isinstance(block, dict):
        provider = block.get("provider")
    return str(provider or "").lower() != "google"


def _message_fingerprint(blocks: list[Any]) -> str:
    """The cache guard's position-free name for an assistant message: its remaining text."""
    from matrx_ai.providers.cache_guard import message_text_fingerprint

    texts = [getattr(b, "text", "") or "" for b in blocks if _block_type(b) == "text"]
    return message_text_fingerprint(texts)


def _block_ref(entry: dict[str, Any]) -> dict[str, str]:
    """The ids of one trim-report entry, nothing else (the record is persisted per request)."""
    ref = {k: str(entry[k]) for k in ("call_id", "tool_use_id", "block") if entry.get(k)}
    return ref


def _latest_turn_start(messages: list[Any]) -> int:
    """Index of the last user message: tool inputs and results from here on are never stubbed;
    with no user message at all, nothing is stubbed."""
    for i in range(len(messages) - 1, -1, -1):
        role = getattr(messages[i], "role", None)
        if role is None and isinstance(messages[i], dict):
            role = messages[i].get("role")
        if role == "user":
            return i
    return 0


def _live_turn_start(messages: list[Any]) -> int:
    """Index of the first message of the turn in progress: its thinking is never dropped.

    The turn starts at the newest PERSON message (a user message that is neither a tool result nor
    server-written), or at a server-written turn that opens a new turn (a woken turn's note: the
    message before it is not a tool result and not a tool-calling assistant turn). A host notice
    INSIDE a tool loop (loop guard, ceiling, answer check after a tool result) never starts a turn:
    Anthropic, "Preserving thinking blocks": "within a tool-use turn, pass thinking blocks back",
    and a tool-use loop is one assistant turn that ends only when the model completes its response
    (probe P1, 2026-11-09). With no user message at all, nothing is touched.
    """
    from matrx_ai.config.context_trim import _is_tool_call_block, _is_tool_result_block
    from matrx_ai.config.typed_text_last import is_host_authored

    def role_of(message: Any) -> str:
        role = getattr(message, "role", None)
        if role is None and isinstance(message, dict):
            role = message.get("role")
        return str(getattr(role, "value", role) or "").lower()

    def blocks(message: Any) -> list[Any]:
        content = getattr(message, "content", None)
        if content is None and isinstance(message, dict):
            content = message.get("content")
        return content if isinstance(content, list) else []

    def in_loop(message: Any) -> bool:
        role = role_of(message)
        if role == "tool":
            return True
        if role == "user":
            return any(_is_tool_result_block(b) for b in blocks(message))
        if role == "assistant":
            return any(_is_tool_call_block(b) for b in blocks(message)) or bool(
                isinstance(message, dict) and message.get("tool_calls")
            )
        return False

    for i in range(len(messages) - 1, -1, -1):
        message = messages[i]
        if role_of(message) != "user" or in_loop(message):
            continue
        if not is_host_authored(message):
            return i
        if i == 0 or not in_loop(messages[i - 1]):
            return i
    return 0


def _history_end(messages: list[Any]) -> int:
    """Where the newest turn starts — nothing from here on is ever stubbed: the last user message,
    and this send's own platform block riding a host turn just before her words (``order_for_wire``;
    found 2026-11-12: pass (c) stubbed it)."""
    from matrx_ai.config.typed_text_last import HOST_TURN_KEY

    protected_from = _latest_turn_start(messages)
    while protected_from > 0 and isinstance(getattr(messages[protected_from - 1], "metadata", None), dict) and (
        messages[protected_from - 1].metadata.get(HOST_TURN_KEY)
    ):
        protected_from -= 1
    return protected_from


def text_stub_key(text: str) -> str:
    """A position-free name for one message text the last-resort fit stubbed (its digest)."""
    import hashlib

    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:32]


def _stub_text_block(block: Any, stats: dict[str, Any]) -> None:
    """Replace one history text block with ``STUB_TEXT`` and count it on ``stats``."""
    from matrx_ai.config.attached_files import HOMED_BLOCK_MARK, homed_block_kind

    block.text = STUB_TEXT
    homed = getattr(block, "metadata", None)
    if isinstance(homed, dict) and homed.get(HOMED_BLOCK_MARK):
        # A homed block (a file, a held copy) is stubbed like any history text; the send
        # boundary unclaims it for this send and the host re-homes it (attached_files).
        stats.setdefault("homed_blocks_stubbed", []).append(
            {"kind": homed_block_kind(block), "key": str(homed[HOMED_BLOCK_MARK])}
        )
    stats["text_blocks_stubbed"] = int(stats.get("text_blocks_stubbed") or 0) + 1
    stats["stubbed_blocks"] = int(stats.get("stubbed_blocks") or 0) + 1


def holds_late_tool_definitions(message: Any) -> bool:
    """True for a replayed host turn that holds LATE TOOL DEFINITIONS (a carrier, or an earlier turn's kept whole
    block with late slots in it). The fit never stubs or cuts one, not even part-way: a definition is what the model
    calls, and the newest turn names it as available without sending it again (``late_tools.delta_slots``). A kept
    whole block that does not fit leaves the wire whole and leaves its definitions behind as a carrier
    (``send_boundary._drop_replayed_turn_context``). The second layer re-sends, in the newest turn, any offered
    definition that is not on the wire whole after the fit (``send_boundary._settle_late_tools_on_wire``)."""
    from matrx_ai.config.typed_text_last import LATE_TOOLS_CARRIER_KEY, REPLAYED_LATE_SLOTS_KEY

    metadata = getattr(message, "metadata", None)
    return isinstance(metadata, dict) and bool(
        metadata.get(LATE_TOOLS_CARRIER_KEY) or metadata.get(REPLAYED_LATE_SLOTS_KEY)
    )


def _stubbable_texts(messages: list[Any]) -> list[Any]:
    """Every history text block pass (c) may stub, oldest first, grouped per message."""
    out: list[Any] = []
    for msg in messages[: _history_end(messages)]:
        content = getattr(msg, "content", None)
        metadata = getattr(msg, "metadata", None)
        if (
            not isinstance(content, list)
            or (isinstance(metadata, dict) and metadata.get("compaction_summary"))
            or holds_late_tool_definitions(msg)
        ):
            out.append([])
            continue
        out.append([
            block for block in content
            if _block_type(block) == "text"
            and isinstance(getattr(block, "text", None), str)
            and len(block.text) > len(STUB_TEXT) + 20
        ])
    return out


def restub_known_texts(messages: list[Any], keys: set[str]) -> dict[str, Any] | None:
    """ONCE STUBBED, ALWAYS STUBBED: stub again every history text an EARLIER send of this
    conversation stubbed (``keys``: their ``text_stub_key``), before anything is measured.

    🚨 prompt_cache_prefix_drift (2026-11-17, chat 0fbc8c1f): the wire is rebuilt from the
    canonical list every round — the replayed page blocks and the person's turns are fresh copies —
    so a text the last-resort fit stubbed on round 2's wire came back whole on round 3, when the
    wire happened to fit ("messages[0] (user) changed (143 -> 4,760 bytes)"): every earlier turn's
    bytes moved and the whole cached prefix was written again. The newest turn is never touched.
    Returns the pass record (``sticky``; nothing to declare — the bytes equal the earlier round's),
    or ``None`` when nothing was stubbed."""
    if not keys:
        return None
    stats: dict[str, Any] = {
        "pass": "sticky_text_stubs",
        "sticky": True,
        "text_blocks_stubbed": 0,
        "stubbed_blocks": 0,
        "rewritten_blocks": [],
    }
    for blocks in _stubbable_texts(messages):
        for block in blocks:
            if text_stub_key(block.text) in keys:
                _stub_text_block(block, stats)
    return stats if stats["stubbed_blocks"] else None


async def _stub_history_to_fit(
    config: Any, messages: list[Any], *, stubbed_text_keys: set[str] | None = None
) -> dict[str, Any]:
    """LAST-RESORT fit: drop earlier thinking, then stub old tool inputs/results, oldest first.

    Runs only when the tiered forced trim left an enforced limit over. Rewrites blocks in place
    (never removes a message, so the executor's index ledger stays valid) and re-measures in
    batches, stopping the moment the call fits. The latest turn is never touched."""
    from matrx_ai.config.context_trim import (
        _get_arguments,
        _get_block_attr,
        _get_call_identifier,
        _is_media_bearing,
        _is_tool_call_block,
        _is_tool_result_block,
        _set_arguments,
        _set_content,
        arguments_carry_trim_marker,
    )
    from matrx_ai.config.unified_content import TextContent

    protected_from = _history_end(messages)
    thinking_from = min(_live_turn_start(messages), protected_from)
    stats: dict[str, Any] = {
        "pass": "stub_history",
        "thinking_blocks_dropped": 0,
        "stubbed_blocks": 0,
        # Which blocks, by call id (the cache guard places them on the wire); a rewrite with
        # nothing to place it by is counted in ``unplaced_blocks`` and stays reported as drift.
        "rewritten_blocks": [],
        "unplaced_blocks": 0,
    }

    def _call_ref(block: Any) -> dict[str, str] | None:
        call_id = _get_call_identifier(block)
        return {"call_id": call_id, "block": "tool_call"} if call_id else None

    def _result_ref(block: Any) -> dict[str, str] | None:
        ref = {"call_id": _get_block_attr(block, "call_id"), "tool_use_id": _get_block_attr(block, "tool_use_id")}
        return ref if ref["call_id"] or ref["tool_use_id"] else None

    def _note(ref: dict[str, str] | None, count: int = 1) -> None:
        if ref is None:
            stats["unplaced_blocks"] += count
        else:
            stats["rewritten_blocks"].append(ref)

    async def _fits() -> bool:
        return not _enforced(_over(await _limits(config)))

    # (a) thinking from earlier turns, all at once — it is dead weight outside the live loop.
    # Lawful only where the provider contract allows it (read 2026-11-09):
    # - Anthropic "Preserving thinking blocks": "Allowed: outside tool use, omit prior turns'
    #   thinking" — never the turn in progress (``thinking_from``: a notice inside a tool loop
    #   is not a turn start, ``_live_turn_start``).
    # - OpenAI Responses: reasoning is passed back for the turn in progress; earlier turns carry
    #   no requirement.
    # - Gemini ("Thinking"): "You MUST always resend all thought blocks exactly as they were
    #   received" — a Gemini thought (provider google) is never dropped.
    # Each assistant message's text fingerprint and how many earlier assistant messages share it:
    # the guard matches a declared drop to exactly ONE wire item (the n-th with that text).
    occurrence: dict[int, int] = {}
    seen: dict[str, int] = {}
    for at, msg in enumerate(messages[:thinking_from]):
        role = getattr(msg, "role", None)
        if str(getattr(role, "value", role) or "").lower() != "assistant":
            continue
        if getattr(msg, "is_visible_to_model", True) is False:
            continue  # never on the wire: counting it shifts the n-th item (review of 1804266da0b9)
        content = getattr(msg, "content", None)
        fingerprint = _message_fingerprint(content if isinstance(content, list) else [])
        occurrence[at] = seen.get(fingerprint, 0)
        seen[fingerprint] = occurrence[at] + 1
    for at, msg in enumerate(messages[:thinking_from]):
        content = getattr(msg, "content", None)
        if not isinstance(content, list):
            continue
        kept = [b for b in content if not _droppable_thinking(b)]
        dropped = len(content) - len(kept)
        if dropped and not kept:  # a message is never emptied — providers reject an empty one
            kept = [TextContent(text=STUB_THINKING)]
        if dropped and getattr(msg, "is_visible_to_model", True) is False:
            continue  # the wire never carries it: dropping saves nothing and has no item to place
        if dropped:
            stats["thinking_blocks_dropped"] += dropped
            # Thinking has no id of its own: the message is placed by a tool call or result
            # it carries, else by its remaining text (an assistant wire item with the same text).
            anchors = [r for r in (_call_ref(b) if _is_tool_call_block(b) else _result_ref(b)
                                   if _is_tool_result_block(b) else None for b in kept) if r]
            if not anchors and kept and at in occurrence:
                anchors = [{"message": _message_fingerprint(kept), "occurrence": occurrence[at]}]
            if anchors:
                stats["rewritten_blocks"].extend(anchors)
            else:
                stats["unplaced_blocks"] += dropped
            content[:] = kept
    if stats["thinking_blocks_dropped"] and await _fits():
        return stats

    # (b) tool-call arguments and tool results, oldest first, re-measured every few messages.
    for n, msg in enumerate(messages[:protected_from], 1):
        content = getattr(msg, "content", None)
        if not isinstance(content, list):
            continue
        for block in content:
            if _is_tool_call_block(block):
                args = _get_arguments(block)
                if isinstance(args, dict) and args and arguments_carry_trim_marker(args) is None:
                    if args != {"_trimmed": STUB_TOOL_INPUT}:
                        _set_arguments(block, {"_trimmed": STUB_TOOL_INPUT})
                        stats["stubbed_blocks"] += 1
                        _note(_call_ref(block))
            elif _is_tool_result_block(block) and not _is_media_bearing(block):
                body = getattr(block, "content", None)
                if isinstance(body, str) and body and len(body) > len(STUB_TOOL_RESULT) + 20:
                    _set_content(block, STUB_TOOL_RESULT)
                    stats["stubbed_blocks"] += 1
                    _note(_result_ref(block))
        if n % 8 == 0 and await _fits():
            return stats
    if await _fits():
        return stats

    # (c) the WORDS of earlier turns, oldest first (2026-11-12, Halcyon's Company Setup chat 0fbc8c1f:
    # every message refused "about 233,441 input tokens (limit 200,000)" — a history made of the
    # person's and the agent's own words, which (a) and (b) cannot shrink). A chat is never refused
    # for its own history: each earlier message's text becomes a short visible stub, in place (the
    # message stays, so the executor's index ledger and the role order hold), until the call fits.
    # A condensed summary row is the history's own short form and is kept; the latest turn is never
    # touched. Only what is left — the instructions, the tools and the newest turn — can still be
    # over a limit, and then the refusal says so.
    stats["text_blocks_stubbed"] = 0
    for n, blocks in enumerate(_stubbable_texts(messages), 1):
        for block in blocks:
            if stubbed_text_keys is not None:
                stubbed_text_keys.add(text_stub_key(block.text))
            _stub_text_block(block, stats)
            # No id to place a rewritten text by: the guard places it by the stub's own words, only
            # in a wire item that changed this round, never more items than declared (chat 0fbc8c1f
            # filed 22 of these as unproven drift, 2026-11-12).
            stats["rewritten_blocks"].append({"block": "text_stub"})
        if n % 8 == 0 and await _fits():
            return stats
    return stats


#: The line left at the end of a text block the cut-to-fit pass shortened (problem 14).
TEXT_CUT_MARKER = "\n\n[Cut to fit this call: {kept:,} of {total:,} characters kept]"
#: A block is never cut below this many characters; a call that cannot fit above it is refused.
TEXT_CUT_FLOOR_CHARS = 2_000
#: Measurement rounds before the pass gives up (each re-measures with the host's own estimator).
_TEXT_CUT_ROUNDS = 6


def cut_level(lengths: list[int], free: int, floor: int = TEXT_CUT_FLOOR_CHARS) -> int | None:
    """The length every block longer than it is cut to so ``free`` characters leave, largest block
    first: the largest comes down to the next largest, then both together, and so on (a water level).
    ``None`` = nothing to free; the level never goes below ``floor``."""
    if free <= 0:
        return None
    ordered = sorted((n for n in lengths if n > floor), reverse=True)
    if not ordered:
        return None
    removed = 0
    for i, top in enumerate(ordered):
        nxt = ordered[i + 1] if i + 1 < len(ordered) else floor
        step = (top - nxt) * (i + 1)
        if removed + step >= free:
            return max(floor, top - -(-(free - removed) // (i + 1)))
        removed += step
    return floor


_TEXT_CUT_TAIL_RE = __import__("re").compile(
    r"\n\n\[Cut to fit this call: ([\d,]+) of ([\d,]+) characters kept\]$"
)


def _cut_parts(text: str) -> tuple[str, int]:
    """``(head, total)`` of a text: an already-cut text gives back the head it kept and the length
    it was cut from (a deeper cut of ``head`` equals the same cut of the original), any other text
    gives itself and its own length."""
    found = _TEXT_CUT_TAIL_RE.search(text[-120:])
    if found is not None:
        kept = int(found.group(1).replace(",", ""))
        total = int(found.group(2).replace(",", ""))
        head = text[: len(text) - len(found.group(0))]
        if len(head) == kept:
            return head, total
    return text, len(text)


def text_cut_key(text: str) -> str:
    """A position-free name for a text the cut-to-fit pass may shorten, the SAME for the original
    and for any cut of it: the digest of its first ``TEXT_CUT_FLOOR_CHARS`` (never cut away) and
    the length it was cut from."""
    head, total = _cut_parts(text)
    return f"{text_stub_key(head[:TEXT_CUT_FLOOR_CHARS])}:{total}"


def _cut_text(head: str, total: int, kept: int) -> str:
    return head[:kept] + TEXT_CUT_MARKER.format(kept=kept, total=total)


def recut_known_texts(messages: list[Any], known: dict[str, int], *, replace: Callable[[int, Any], None]) -> dict[str, Any] | None:
    """ONCE CUT, CUT THE SAME WAY: every history text an EARLIER send of this conversation cut to
    fit (``known``: ``text_cut_key`` -> the length kept) is cut to that length again before
    anything is measured. Copy-on-write through ``replace(index, new_message)`` like the pass.

    The wire is rebuilt every round, and the cut pass picks its level from that round's excess, so
    without this a text cut on round N came back whole (or cut to a different length) on round N+1
    and every earlier turn's bytes moved — the whole cached prefix written again (the sibling of
    ``restub_known_texts``). The newest turn is never touched. Returns the pass record (``sticky``;
    nothing to declare — the bytes equal the earlier round's), or ``None`` when nothing was cut."""
    from copy import copy

    if not known:
        return None
    end = _history_end(messages)
    record: dict[str, Any] = {"pass": "sticky_text_cuts", "sticky": True, "blocks": [], "freed_chars": 0,
                              "stubbed_blocks": 0, "rewritten_blocks": []}
    cut_messages: dict[int, Any] = {}
    for mi, bi, sub, text in _text_blocks(messages[:end]):
        kept = known.get(text_cut_key(text))
        head, total = _cut_parts(text)
        if kept is None or len(head) <= kept:
            continue
        msg = cut_messages.get(mi)
        if msg is None:
            msg = copy(messages[mi])
            msg.content = list(messages[mi].content)
            cut_messages[mi] = msg
        new_text = _cut_text(head, total, kept)
        msg.content[bi] = _with_text(msg.content[bi], sub, new_text)
        record["blocks"].append({"message": mi, "block": bi, "kept_chars": kept, "total_chars": total})
        record["freed_chars"] += len(text) - len(new_text)
    for mi, msg in cut_messages.items():
        replace(mi, msg)
    record["stubbed_blocks"] = len(record["blocks"])
    return record if record["blocks"] else None


def _text_blocks(messages: list[Any]) -> list[tuple[int, int, Any, str]]:
    """(message index, block index, slot, text) of every text a cut may shorten: a plain text block
    (slot ``None``) and the text of a tool result — its whole string content (slot ``("tool", None)``)
    or each text item of its content list (slot ``("tool", i)``) — so the newest turn's tool result is
    offered too (review 2026-11-19 finding 6: such a call was still refused whole). A homed block (a
    file or held copy, ``attached_files``) is the host's to re-home and is never cut here, and a turn
    holding late tool definitions is never cut part-way (``holds_late_tool_definitions``)."""
    from matrx_ai.config.attached_files import HOMED_BLOCK_MARK

    found: list[tuple[int, int, Any, str]] = []
    for mi, msg in enumerate(messages):
        content = getattr(msg, "content", None)
        if not isinstance(content, list) or holds_late_tool_definitions(msg):
            continue
        for bi, block in enumerate(content):
            homed = getattr(block, "metadata", None)
            if isinstance(homed, dict) and homed.get(HOMED_BLOCK_MARK):
                continue
            kind = _block_type(block)
            if kind == "text":
                text = getattr(block, "text", None)
                if isinstance(text, str) and len(text) > TEXT_CUT_FLOOR_CHARS:
                    found.append((mi, bi, None, text))
            elif kind == "tool_result":
                inner = getattr(block, "content", None)
                if isinstance(inner, str):
                    if len(inner) > TEXT_CUT_FLOOR_CHARS:
                        found.append((mi, bi, ("tool", None), inner))
                elif isinstance(inner, list):
                    for i, item in enumerate(inner):
                        text = item.get("text") if isinstance(item, dict) else getattr(item, "text", None)
                        item_type = item.get("type") if isinstance(item, dict) else _block_type(item)
                        if item_type in (None, "text") and isinstance(text, str) and len(text) > TEXT_CUT_FLOOR_CHARS:
                            found.append((mi, bi, ("tool", i), text))
    return found


def _with_text(block: Any, slot: Any, text: str) -> Any:
    """A copy of ``block`` with the text at ``slot`` (see :func:`_text_blocks`) replaced; the original
    block, its content list and its items are never touched."""
    from copy import copy

    new = copy(block)
    if slot is None:
        new.text = text
        return new
    _, i = slot
    if i is None:
        new.content = text
        return new
    items = list(block.content)
    item = items[i]
    if isinstance(item, dict):
        items[i] = {**item, "text": text}
    else:
        item = copy(item)
        item.text = text
        items[i] = item
    new.content = items
    return new


#: The system instruction is cut LAST, and never below its first part nor this many characters.
SYSTEM_CUT_FLOOR_CHARS = 8_000


def _system_floor(text: str) -> int:
    """The least of the system text a cut keeps: its first part (up to the first blank line) and never
    less than ``SYSTEM_CUT_FLOOR_CHARS``."""
    first = text.find("\n\n")
    return max(SYSTEM_CUT_FLOOR_CHARS, first if first > 0 else 0)


async def _cut_system_to_fit(config: Any, limits: list[dict[str, Any]], record: dict[str, Any]) -> list[dict[str, Any]]:
    """The system instruction, cut last: still over after every message text reached its floor, the
    resolved system text is cut from its end (the same marker) down toward :func:`_system_floor`, on
    THIS config only (the wire copy: the attribute is replaced, the instruction object never touched).
    Returns the limits after."""
    resolved = getattr(config, "resolved_system_instruction", None)
    if resolved is None:
        si = getattr(config, "system_instruction", None)
        resolved = si if isinstance(si, str) else (str(si) if si is not None else None)
    if not isinstance(resolved, str):
        return limits
    head, total = _cut_parts(resolved)
    floor = _system_floor(head)
    if len(head) <= floor:
        return limits
    over = _enforced(_over(limits))
    chars_per_token = 4.0
    keep = len(head)
    for _round in range(_TEXT_CUT_ROUNDS):
        excess = max(lim["estimated_tokens"] - lim["limit_tokens"] for lim in over)
        keep = max(floor, keep - int(excess * chars_per_token * 1.02) - 120)
        before = max(lim["estimated_tokens"] for lim in over)
        config.system_instruction = _cut_text(head, total, keep)
        limits = await _limits(config)
        over = _enforced(_over(limits))
        if not over or keep <= floor:
            break
        dropped = before - max(lim["estimated_tokens"] for lim in over)
        if dropped > 0:
            chars_per_token = max(1.0, (len(head) - keep) / dropped)
    record["system_instruction"] = {"kept_chars": keep, "total_chars": total}
    record["freed_chars"] += len(head) - keep
    record["fits"] = not over
    return limits


async def cut_largest_text_to_fit(
    config: Any, *, replace: Callable[[int, Any], None], known_cuts: dict[str, int] | None = None
) -> dict[str, Any] | None:
    """LAST make-it-fit pass for an AUTOMATED call (problem 14, conversation dbb7b5a6 2026-11-08: one
    487,296-character message, every other pass freed 0, the call was refused whole). Runs only when
    an ENFORCED host input budget is over — a person's own work carries a condense-only budget and is
    never cut. The largest text blocks are cut first, each down toward the next largest, keeping the
    head of each and ending it with ``TEXT_CUT_MARKER``. Copy-on-write: a cut block's message is
    replaced through ``replace(index, new_message)`` and the original objects are never touched.
    Re-measured with the same limits (the host's own estimator) after every round. An already-cut
    text is measured by the head it kept and cut deeper from it (the same bytes as cutting the
    original). ``known_cuts``: when given, every cut is recorded in it (``text_cut_key`` -> length
    kept) so the send boundary cuts it the same way on every later round (``recut_known_texts``).
    Returns the pass record, or ``None`` when it does not apply."""
    from copy import copy

    limits = await _limits(config)
    if not any(lim["limit"] == "host_input_budget" and lim.get("enforced", True) for lim in _over(limits)):
        return None
    messages = list(getattr(config, "messages", None) or [])
    candidates = [(mi, bi, sub, *_cut_parts(text)) for mi, bi, sub, text in _text_blocks(messages)]
    record: dict[str, Any] = {"pass": "cut_largest_text", "blocks": [], "freed_chars": 0, "fits": False,
                              "rewritten_blocks": [], "stubbed_blocks": 0}
    over = _enforced(_over(limits))
    if not candidates:
        await _cut_system_to_fit(config, limits, record)
        record["tokens_trimmed"] = max(0, max(lim["estimated_tokens"] for lim in over)
                                       - max((lim["estimated_tokens"] for lim in await _limits(config)), default=0))
        return record
    excess = max(lim["estimated_tokens"] - lim["limit_tokens"] for lim in over)
    estimate_before = max(lim["estimated_tokens"] for lim in over)
    chars_per_token = 4.0  # the first guess; every round learns the real ratio from the re-measure
    free = 0
    level: int | None = None
    for _round in range(_TEXT_CUT_ROUNDS):
        free += int(excess * chars_per_token * 1.02) + 120 * len(candidates)
        level = cut_level([len(head) for _, _, _, head, _ in candidates], free)
        if level is None:
            break
        cut_messages = {}
        blocks: list[dict[str, Any]] = []
        for mi, bi, sub, head, total in candidates:
            if len(head) <= level:
                continue
            msg = cut_messages.get(mi)
            if msg is None:
                msg = copy(messages[mi])
                msg.content = list(messages[mi].content)
                cut_messages[mi] = msg
            msg.content[bi] = _with_text(msg.content[bi], sub, _cut_text(head, total, level))
            blocks.append({"message": mi, "block": bi, "kept_chars": level, "total_chars": total,
                           "freed": len(head) - level, "key": f"{text_stub_key(head[:TEXT_CUT_FLOOR_CHARS])}:{total}"})
        for mi, msg in cut_messages.items():
            replace(mi, msg)
        after = await _limits(config)
        record["blocks"] = blocks
        record["freed_chars"] = sum(b.pop("freed") for b in blocks)
        cut_keys = {(b["message"], b["block"]): b.pop("key") for b in blocks}
        record["level_chars"] = level
        still = _enforced(_over(after))
        if not still:
            record["fits"] = True
            break
        if level <= TEXT_CUT_FLOOR_CHARS:
            break
        estimate_now = max(lim["estimated_tokens"] for lim in still)
        dropped = estimate_before - estimate_now
        if dropped > 0:
            chars_per_token = max(1.0, record["freed_chars"] / dropped)
        excess = max(lim["estimated_tokens"] - lim["limit_tokens"] for lim in still)
        free = record["freed_chars"]
    if not record["fits"]:
        # every message text is at its floor (or none could give): the system instruction, last
        await _cut_system_to_fit(config, await _limits(config), record)
    if known_cuts is not None and record["blocks"]:
        for b in record["blocks"]:
            key = cut_keys[(b["message"], b["block"])]
            known_cuts[key] = min(known_cuts.get(key, b["kept_chars"]), b["kept_chars"])
    record["stubbed_blocks"] = len(record["blocks"])
    # Placed by the cache guard by the marker in their own words (``cache_guard._stub_text_parts``).
    record["rewritten_blocks"] = [{"block": "text_cut"} for _ in record["blocks"]]
    record["tokens_trimmed"] = max(0, estimate_before - max((lim["estimated_tokens"] for lim in await _limits(config)), default=0))
    return record


__all__ = [
    "FORCED_TIERS",
    "TEXT_CUT_MARKER",
    "cut_largest_text_to_fit",
    "cut_level",
    "cut_to_fit_enforced",
    "recut_known_texts",
    "restub_known_texts",
    "text_cut_key",
    "STUB_TOOL_INPUT",
    "STUB_TOOL_RESULT",
    "ensure_fits",
    "set_compactor",
    "set_input_budget_resolver",
]
