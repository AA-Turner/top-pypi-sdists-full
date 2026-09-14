"""In-memory context trimmer for tool-call and tool-result content blocks.

Purpose
-------
As a conversation grows, old tool traffic bloats what the model has to
read on every turn — and it bloats it from BOTH sides: the result the tool
returned, and the ARGUMENTS the assistant sent to call it. This module
exposes a single function, ``trim_messages_context``, that walks a
``list[UnifiedMessage]`` and compacts both, under the same two tiers and
the same cache gate.

Why both sides (measured 2026-09-13 in ``chat.request`` / ``chat.message``)
--------------------------------------------------------------------------
Until 2026-09-13 this trimmer rewrote tool_result blocks ONLY. The Masterwork
Conductor saves workflow definitions through the ``workflow_author`` tool with
25-73K-char argument payloads, and those payloads live in assistant messages
forever: one conversation reached 1.5M chars of assistant content against 19K
of tool results, average request context 362K tokens, peak 559K, $95 on Opus 5.
408 of 419 Conductor requests reported the trimmer had run and freed NOTHING
(``est_savings_tokens: 0``) because nothing eligible existed on the result
side. Arguments are now trimmed too (``TrimPolicy.trim_tool_call_arguments``).

It replaces the ``content`` of any tool_result block that is BOTH:

  * far enough back (positional distance from the current head), AND
  * large enough (output_chars exceeds the tier's threshold), AND
  * not image/video/audio-bearing (those carry references the model
    will lose if we mutate the content),

with a compact augmented preview that tells the model the original
output is recoverable — and, when
``TrimPolicy.trim_tool_call_arguments`` is on (the default), the
``arguments`` of any tool_call block far enough back and large enough
(measured as ``len(json.dumps(arguments))``) with a compact stub naming
the top-level keys and the original size. The tool's stored state is
authoritative; the model re-reads it (e.g. ``get_workflow``) when needed.

Two tiers (Arman's ruling 2026-09-09, from the re-fetch measurements in
``chat.vw_tool_refetch``; the 2026-06 defaults of 5/500 and 15/200 cleared a
result about two tool calls after it arrived, and agents re-fetched it):

  Tier 1 — at ``tier_1_min_positions_back`` (default 12) back: replace
           anything over ``tier_1_min_output_chars`` (default 8000).
  Tier 2 — at ``tier_2_min_positions_back`` (default 24) back: replace
           anything over ``tier_2_min_output_chars`` (default 2000) —
           same substitution, more aggressive threshold.

These are opinions and therefore knobs: pass a ``TrimPolicy`` into
``send_boundary.prepare_for_send`` to override per organization once an
org-settings source exists; never hardcode taste elsewhere.

What this function is NOT
-------------------------
* It does NOT write to the database. Originals remain authoritative.
* It does NOT change the position, id, role, status, metadata, or any
  other field on a UnifiedMessage. Only the ``content`` of qualifying
  tool_result blocks and the ``arguments`` of qualifying tool_call
  blocks are rewritten.
* It does NOT touch the id / call_id / tool_use_id / name / type /
  is_error fields on either block — provider tool_use ↔ tool_result
  pairing stays intact, and the rewritten ``arguments`` stays a plain
  dict so every provider serializer keeps working (Anthropic ``input``
  is an object, OpenAI ``arguments`` is ``json.dumps`` of it, Google
  ``args`` is the object).
* Freshly appended in-memory turns whose ``position`` is ``None`` are ordered
  after persisted messages for distance calculations. Their position field is
  never mutated.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from matrx_ai.config.message_config import UnifiedMessage

_DEFAULT_SUBSTITUTE = (
    "[tool result cleared] Replaced with keys and chars -- Fetch again when necessary"
)

_DEFAULT_ARGUMENTS_SUBSTITUTE = (
    "[tool arguments cleared] Large arguments removed from context after this call scrolled "
    "back -- the tool's stored state is authoritative; re-read it (e.g. get_workflow) when needed"
)

# Phase 2: cache-aware gate constants.
#
# When prompt-cache is alive AND the trimmable savings on this turn are below
# this floor, skip the trim entirely — breaking the cache prefix to save a few
# hundred tokens is a losing trade. Real "let's reclaim space" turns easily
# clear 5K (one large page-fetch, one screenshot, one big search result).
CACHE_GATE_MIN_SAVED_TOKENS = 5000

# Per-provider TTL estimate. We treat the cache as "likely alive" if it's
# been less than CACHE_GATE_TTL_RATIO of this since the last response. Static
# constants in v1 — Phase 6 may replace with calibrated values learned from
# cache_read_input_tokens transitions.
DEFAULT_CACHE_TTLS_SECS: dict[str, int] = {
    "anthropic": 300,
    "openai": 300,
    "google": 300,
    "groq": 300,
    "xai": 300,
    "cerebras": 300,
    "together": 300,
    "fireworks": 300,
    "cohere": 300,
}
CACHE_GATE_TTL_RATIO = 0.8

# Chars-per-token estimate for the savings calc. Conservative on purpose — we
# want to UNDER-estimate savings (which leans toward "not enough, skip") so
# the gate is more cautious about breaking cache. Real ratios are ~3.5-4.
CHARS_PER_TOKEN_ESTIMATE = 4.0


@dataclass
class TrimPolicy:
    """Tunable policy for ``trim_messages_context``.

    Defaults are Arman's 2026-09-09 ruling (see module docstring):
      * 12+ positions back AND > 8000 chars → replace
      * 24+ positions back AND > 2000 chars → replace
    """

    tier_1_min_positions_back: int = 12
    tier_1_min_output_chars: int = 8000
    tier_2_min_positions_back: int = 24
    tier_2_min_output_chars: int = 2000

    # Image/video/audio results carry a typed reference (file_id, ImageContent
    # block, etc.) that the model needs intact for re-display. We refuse to
    # mutate any block whose content is a typed-block list, AND skip results
    # whose output_preview heuristically looks like a media wrapper.
    skip_media_results: bool = True

    # Marker text inserted at the top of the augmented preview.
    substitute_message: str = _DEFAULT_SUBSTITUTE

    # Trim the ASSISTANT side too: stale, large tool_call ``arguments``
    # payloads (2026-09-13 — see module docstring). Same tiers, same cache
    # gate; set False to restore the result-only behaviour.
    trim_tool_call_arguments: bool = True

    # Marker text inserted as the stub's ``result`` key.
    substitute_arguments_message: str = _DEFAULT_ARGUMENTS_SUBSTITUTE

    def to_snapshot(self) -> dict[str, Any]:
        """Plain-dict snapshot for persistence (cx_request.trim_summary)."""
        return {
            "tier_1_min_positions_back": self.tier_1_min_positions_back,
            "tier_1_min_output_chars": self.tier_1_min_output_chars,
            "tier_2_min_positions_back": self.tier_2_min_positions_back,
            "tier_2_min_output_chars": self.tier_2_min_output_chars,
            "skip_media_results": self.skip_media_results,
            "trim_tool_call_arguments": self.trim_tool_call_arguments,
        }


@dataclass
class TrimReport:
    """Audit of one ``trim_messages_context`` pass.

    Persisted verbatim onto ``cx_request.trim_summary`` so the Model Context UI
    can show what just happened (which blocks got rewritten, why, what the
    policy was) without diffing snapshots.

    Fields:
      * blocks_rewritten — count of blocks rewritten by this pass: tool_result
        contents replaced with the augmented preview PLUS tool_call arguments
        replaced with the compact stub. Persistence and the cache-state
        accounting read this field, so argument rewrites count here too.
      * arguments_rewritten — how many of ``blocks_rewritten`` were tool_call
        argument payloads (0 before 2026-09-13).
      * freed_chars — chars removed from the in-memory payload (before - after).
      * before_total_chars / after_total_chars — JSON-string size of the trimmed
        slice (only tool_result blocks counted) before and after the pass.
      * rewritten_blocks — per-block detail: list of {message_position,
        call_id, tool_name, before_chars, after_chars}. An argument rewrite
        additionally carries ``"block": "tool_call"``; result entries are
        unchanged (no ``block`` key).
      * eligible_but_skipped_reason — one of None | "cache_protect" |
        "no_eligible_messages". Distinguishes "ran but nothing matched" from
        "didn't run because of the cache gate."
      * policy — the TrimPolicy.to_snapshot() in effect when this pass ran.
    """

    blocks_rewritten: int = 0
    arguments_rewritten: int = 0
    freed_chars: int = 0
    before_total_chars: int = 0
    after_total_chars: int = 0
    rewritten_blocks: list[dict[str, Any]] = None  # type: ignore[assignment]
    eligible_but_skipped_reason: str | None = None
    policy: dict[str, Any] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.rewritten_blocks is None:
            self.rewritten_blocks = []
        if self.policy is None:
            self.policy = {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "blocks_rewritten": self.blocks_rewritten,
            "arguments_rewritten": self.arguments_rewritten,
            "freed_chars": self.freed_chars,
            "before_total_chars": self.before_total_chars,
            "after_total_chars": self.after_total_chars,
            "rewritten_blocks": self.rewritten_blocks,
            "eligible_but_skipped_reason": self.eligible_but_skipped_reason,
            "policy": self.policy,
        }


def trim_messages_context(
    messages: list[UnifiedMessage],
    policy: TrimPolicy | None = None,
    cache_state: dict[str, Any] | None = None,
) -> TrimReport:
    """Trim tool_result content and tool_call arguments in-place. Returns a TrimReport.

    Safe to call on any message list — non-qualifying blocks are
    skipped silently. Idempotent: re-running on the same list does
    nothing new (the augmented preview's own size is well below either
    tier's threshold, so it won't re-qualify; the argument stub is
    additionally recognised by its marker and never re-rewritten).

    Cache-aware gate (Phase 2): when ``cache_state`` is provided and indicates
    that the prompt cache is likely still alive AND the eligible savings on
    this turn are below CACHE_GATE_MIN_SAVED_TOKENS, the trim is skipped
    entirely. This protects the cache prefix when the savings don't justify
    the break. Pass ``cache_state=None`` (the legacy call) to disable the gate.
    """
    if policy is None:
        policy = TrimPolicy()

    report = TrimReport(policy=policy.to_snapshot())

    persisted_positions = [m.position for m in messages if m.position is not None]
    max_persisted_position = max(persisted_positions, default=-1)
    next_unposted_position = max_persisted_position + 1
    effective_positions: dict[int, int] = {}
    for msg in messages:
        if msg.position is not None:
            effective_positions[id(msg)] = msg.position
        else:
            effective_positions[id(msg)] = next_unposted_position
            next_unposted_position += 1
    if not effective_positions:
        report.eligible_but_skipped_reason = "no_eligible_messages"
        return report
    current_position = max(effective_positions.values())

    # Cache-aware gate: estimate what we'd save THIS pass and compare to the
    # cost of breaking the cache prefix. If cache is fresh and savings are
    # small, skip outright.
    if cache_state and _is_cache_likely_alive(cache_state):
        est_savings_tokens = _estimate_savings_tokens(messages, policy, current_position)
        if est_savings_tokens < CACHE_GATE_MIN_SAVED_TOKENS:
            report.eligible_but_skipped_reason = "cache_protect"
            report.policy["cache_gate"] = {
                "skipped": True,
                "est_savings_tokens": est_savings_tokens,
                "min_required_tokens": CACHE_GATE_MIN_SAVED_TOKENS,
                "cache_state_age_secs": _cache_age_secs(cache_state),
            }
            return report

    for msg in messages:
        effective_position = effective_positions[id(msg)]
        positions_back = current_position - effective_position
        if positions_back < policy.tier_1_min_positions_back:
            continue

        if positions_back >= policy.tier_2_min_positions_back:
            min_chars = policy.tier_2_min_output_chars
        else:
            min_chars = policy.tier_1_min_output_chars

        tier = "tier_2" if positions_back >= policy.tier_2_min_positions_back else "tier_1"

        for block in msg.content:
            if policy.trim_tool_call_arguments and _is_tool_call_block(block):
                before_len = _tool_call_argument_chars(block)
                if before_len < min_chars:
                    continue
                if _already_trimmed_arguments(block):
                    continue

                _rewrite_tool_call_arguments(block, policy.substitute_arguments_message)
                after_len = _tool_call_argument_chars(block)

                report.blocks_rewritten += 1
                report.arguments_rewritten += 1
                report.before_total_chars += before_len
                report.after_total_chars += after_len
                report.freed_chars += max(0, before_len - after_len)
                report.rewritten_blocks.append(
                    {
                        "block": "tool_call",
                        "message_position": (
                            int(msg.position) if msg.position is not None else effective_position
                        ),
                        "call_id": _get_call_identifier(block),
                        "tool_name": _get_block_attr(block, "name"),
                        "before_chars": before_len,
                        "after_chars": after_len,
                        "positions_back": positions_back,
                        "tier": tier,
                    }
                )
                continue

            if not _is_tool_result_block(block):
                continue
            block_chars_before = _get_output_chars(block)
            if block_chars_before < min_chars:
                continue
            if policy.skip_media_results and _is_media_bearing(block):
                continue
            if _already_trimmed(block):
                continue

            content_before = _get_content(block)
            try:
                before_len = len(json.dumps(content_before, default=str))
            except (TypeError, ValueError):
                before_len = block_chars_before

            _rewrite_block_content(block, policy.substitute_message)

            content_after = _get_content(block)
            try:
                after_len = len(json.dumps(content_after, default=str))
            except (TypeError, ValueError):
                after_len = 0

            report.blocks_rewritten += 1
            report.before_total_chars += before_len
            report.after_total_chars += after_len
            report.freed_chars += max(0, before_len - after_len)
            report.rewritten_blocks.append(
                {
                    "message_position": (
                        int(msg.position) if msg.position is not None else effective_position
                    ),
                    "call_id": _get_block_attr(block, "call_id"),
                    "tool_name": _get_block_attr(block, "name"),
                    "before_chars": before_len,
                    "after_chars": after_len,
                    "positions_back": positions_back,
                    "tier": tier,
                }
            )

    return report


def _get_block_attr(block: Any, attr: str) -> str:
    """Read ``attr`` off a block whether it's a dataclass or a raw dict."""
    value = getattr(block, attr, None)
    if value is None and isinstance(block, dict):
        value = block.get(attr)
    return str(value) if value is not None else ""


# --------------------------------------------------------------------------- #
# Cache-aware gate helpers (Phase 2)                                          #
# --------------------------------------------------------------------------- #


def _cache_age_secs(cache_state: dict[str, Any]) -> float | None:
    """Seconds since ``cache_state.last_response_at`` (None if not present)."""
    last = cache_state.get("last_response_at")
    if not last:
        return None
    try:
        dt = datetime.fromisoformat(str(last).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    now = datetime.now(UTC)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return max(0.0, (now - dt).total_seconds())


def _is_cache_likely_alive(cache_state: dict[str, Any]) -> bool:
    """True when the prompt-cache prefix is probably still cached.

    Uses the per-provider TTL (``cache_state.est_cache_ttl_secs`` if set,
    else the DEFAULT_CACHE_TTLS_SECS lookup) and the age since the last
    response. We treat it as "alive" only inside CACHE_GATE_TTL_RATIO of
    the TTL — leaving a margin so we don't get clipped right at expiry.

    Returns False (cache assumed dead) when we can't determine age — the
    safe choice is to allow trims rather than block them on bad data.
    """
    age = _cache_age_secs(cache_state)
    if age is None:
        return False
    ttl = cache_state.get("est_cache_ttl_secs")
    if not ttl:
        provider = (cache_state.get("last_provider") or "").lower()
        ttl = DEFAULT_CACHE_TTLS_SECS.get(provider, 300)
    return age < (float(ttl) * CACHE_GATE_TTL_RATIO)


def _estimate_savings_tokens(
    messages: list[UnifiedMessage],
    policy: TrimPolicy,
    current_position: int,
) -> int:
    """Estimate how many tokens this pass would free.

    Walks the same eligibility predicate as the main loop but sums sizes
    instead of mutating — tool_result ``output_chars`` AND, since
    2026-09-13, stale tool_call argument payloads, so the cache gate makes
    the right call on a conversation whose weight is all on the call side
    (the Conductor case: 408 of 419 requests measured ``est_savings_tokens:
    0`` while assistant content held 1.5M chars). Conservative — uses
    CHARS_PER_TOKEN_ESTIMATE divisor (under-estimates real tokens, which
    is the safe direction: makes the gate more cautious about firing).
    """
    total_chars = 0
    max_persisted_position = max(
        (msg.position for msg in messages if msg.position is not None),
        default=-1,
    )
    next_unposted_position = max_persisted_position + 1
    for msg in messages:
        effective_position = msg.position
        if effective_position is None:
            effective_position = next_unposted_position
            next_unposted_position += 1
        positions_back = current_position - effective_position
        if positions_back < policy.tier_1_min_positions_back:
            continue
        if positions_back >= policy.tier_2_min_positions_back:
            min_chars = policy.tier_2_min_output_chars
        else:
            min_chars = policy.tier_1_min_output_chars
        for block in msg.content:
            if policy.trim_tool_call_arguments and _is_tool_call_block(block):
                arg_chars = _tool_call_argument_chars(block)
                if arg_chars < min_chars:
                    continue
                if _already_trimmed_arguments(block):
                    continue
                total_chars += arg_chars
                continue
            if not _is_tool_result_block(block):
                continue
            chars = _get_output_chars(block)
            if chars < min_chars:
                continue
            if policy.skip_media_results and _is_media_bearing(block):
                continue
            if _already_trimmed(block):
                continue
            total_chars += chars
    return int(total_chars / CHARS_PER_TOKEN_ESTIMATE)


# --------------------------------------------------------------------------- #
# Helpers — kept small and defensive                                          #
# --------------------------------------------------------------------------- #


def _is_tool_result_block(block: Any) -> bool:
    """True only for tool_result content blocks.

    Robust to both dataclass instances and raw dicts since both shapes
    coexist in the codebase (rebuilt-from-DB messages, freshly-parsed
    inbound payloads).
    """
    block_type = getattr(block, "type", None)
    if block_type is None and isinstance(block, dict):
        block_type = block.get("type")
    return block_type == "tool_result"


def _is_tool_call_block(block: Any) -> bool:
    """True only for assistant tool_call / function_call content blocks.

    Same dataclass-or-dict tolerance as ``_is_tool_result_block``.
    """
    block_type = getattr(block, "type", None)
    if block_type is None and isinstance(block, dict):
        block_type = block.get("type")
    return block_type in ("tool_call", "function_call")


def _get_arguments(block: Any) -> Any:
    value = getattr(block, "arguments", None)
    if value is None and isinstance(block, dict):
        value = block.get("arguments")
    return value


def _set_arguments(block: Any, new_arguments: dict[str, Any]) -> None:
    if isinstance(block, dict):
        block["arguments"] = new_arguments
    else:
        block.arguments = new_arguments


def _tool_call_argument_chars(block: Any) -> int:
    """Serialized size of the block's ``arguments`` — 0 when unmeasurable.

    Measured the way the payload actually reaches a provider
    (``json.dumps``), so the threshold means what it says on the wire.
    """
    arguments = _get_arguments(block)
    if not isinstance(arguments, dict) or not arguments:
        return 0
    try:
        return len(json.dumps(arguments, default=str))
    except (TypeError, ValueError):
        return 0


def _already_trimmed_arguments(block: Any) -> bool:
    """True if this call's arguments were already replaced by an earlier pass."""
    arguments = _get_arguments(block)
    if not isinstance(arguments, dict):
        return False
    marker = arguments.get("result")
    return isinstance(marker, str) and marker.startswith("[tool arguments cleared]")


def _rewrite_tool_call_arguments(block: Any, marker: str) -> None:
    """Replace a stale tool call's ``arguments`` with a compact stub.

    Shape (a plain dict — NOT a JSON string — so ``to_anthropic`` keeps an
    object ``input``, ``to_openai`` keeps ``json.dumps(...)`` of an object,
    and ``to_google`` keeps an object ``args``)::

        {"result": "<marker>", "keys": [...top-level keys...], "chars": <before>}

    The block's id / call_id / name / type / metadata are untouched, so the
    provider's tool_use ↔ tool_result pairing survives intact.
    """
    arguments = _get_arguments(block)
    before_chars = _tool_call_argument_chars(block)
    keys = [str(k) for k in arguments.keys()] if isinstance(arguments, dict) else []
    _set_arguments(
        block,
        {
            "result": marker,
            "keys": keys,
            "chars": before_chars,
        },
    )


def _get_call_identifier(block: Any) -> str:
    """Join key of a tool_call block — ``id`` on ToolCallContent, ``call_id``
    on the raw-dict form emitted by ``to_dict()``."""
    for attr in ("id", "call_id"):
        value = _get_block_attr(block, attr)
        if value:
            return value
    return ""


def _get_output_chars(block: Any) -> int:
    value = getattr(block, "output_chars", None)
    if value is None and isinstance(block, dict):
        value = block.get("output_chars")
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _get_output_preview(block: Any) -> dict[str, Any] | None:
    value = getattr(block, "output_preview", None)
    if value is None and isinstance(block, dict):
        value = block.get("output_preview")
    if isinstance(value, dict):
        return value
    return None


def _get_content(block: Any) -> Any:
    value = getattr(block, "content", None)
    if value is None and isinstance(block, dict):
        value = block.get("content")
    return value


def _set_content(block: Any, new_content: Any) -> None:
    if isinstance(block, dict):
        block["content"] = new_content
    else:
        setattr(block, "content", new_content)


def _is_media_bearing(block: Any) -> bool:
    """Heuristic — refuse to mutate results that carry media references.

    Two signals (either is sufficient):
      1. ``content`` is a list of typed blocks (in-memory image/audio/video
         path emitted by ``ToolResult.to_tool_result_content``).
      2. ``output_preview`` looks like a media wrapper — ``kind`` is one
         of the known media kinds OR ``media_type`` starts with image/
         audio/video.
    """
    content = _get_content(block)
    if isinstance(content, list) and content:
        for item in content:
            if (
                hasattr(item, "to_anthropic")
                or hasattr(item, "to_openai")
                or hasattr(item, "to_google")
            ):
                return True

    preview = _get_output_preview(block)
    if preview:
        kind = preview.get("kind")
        if isinstance(kind, str) and kind in {
            "image_ref",
            "image",
            "audio",
            "video",
            "media_ref",
        }:
            return True
        media_type = preview.get("media_type")
        if isinstance(media_type, str) and (
            media_type.startswith("image/")
            or media_type.startswith("audio/")
            or media_type.startswith("video/")
        ):
            return True
    return False


def _already_trimmed(block: Any) -> bool:
    """True if this block has already been rewritten by an earlier pass.

    The trimmer is idempotent by construction, but a quick short-circuit
    keeps the work O(n) on subsequent passes.
    """
    content = _get_content(block)
    if not isinstance(content, str) or not content:
        return False
    # The marker key is unique enough that prefix-checking the JSON-stringified
    # content avoids false positives.
    return content.startswith('{"result": "[tool result cleared]')


def _rewrite_block_content(block: Any, marker: str) -> None:
    """Replace the block's content with an augmented preview JSON.

    The shape mirrors the user's spec:
      {
        "result": "<marker>",
        ...all original output_preview keys preserved...
      }

    If no output_preview exists we still produce a minimal substitution
    so the model sees the marker. The block's call_id / tool_use_id /
    name / is_error / output_chars are intentionally untouched.
    """
    preview = _get_output_preview(block) or {}
    augmented: dict[str, Any] = {"result": marker}
    # Preserve preview keys verbatim AFTER ``result`` so renderers that
    # display the first-key always see the marker.
    for key, value in preview.items():
        if key == "result":
            continue
        augmented[key] = value
    _set_content(block, json.dumps(augmented))
