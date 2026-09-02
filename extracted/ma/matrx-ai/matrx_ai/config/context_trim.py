"""In-memory context trimmer for tool-result content blocks.

Purpose
-------
As a conversation grows, old tool results bloat what the model has to
read on every turn. This module exposes a single function,
``trim_messages_context``, that walks a ``list[UnifiedMessage]`` and
replaces the ``content`` of any tool_result block that is BOTH:

  * far enough back (positional distance from the current head), AND
  * large enough (output_chars exceeds the tier's threshold), AND
  * not image/video/audio-bearing (those carry references the model
    will lose if we mutate the content),

with a compact augmented preview that tells the model the original
output is recoverable.

Two tiers (matching the user's spec):

  Tier 1 — at ``tier_1_min_positions_back`` (default 5) back: replace
           anything over ``tier_1_min_output_chars`` (default 500).
  Tier 2 — at ``tier_2_min_positions_back`` (default 15) back: replace
           anything over ``tier_2_min_output_chars`` (default 200) —
           same substitution, more aggressive threshold.

What this function is NOT
-------------------------
* It does NOT write to the database. Originals remain authoritative.
* It does NOT change the position, id, role, status, metadata, or any
  other field on a UnifiedMessage. Only the ``content`` of qualifying
  tool_result blocks is rewritten.
* It does NOT touch the call_id / tool_use_id / name / is_error fields
  on the block — provider tool_use ↔ tool_result pairing stays intact.
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

    Defaults match the user's stated rule:
      * 5+ positions back AND > 500 chars  → replace
      * 15+ positions back AND > 200 chars → replace
    """

    tier_1_min_positions_back: int = 5
    tier_1_min_output_chars: int = 500
    tier_2_min_positions_back: int = 15
    tier_2_min_output_chars: int = 200

    # Image/video/audio results carry a typed reference (file_id, ImageContent
    # block, etc.) that the model needs intact for re-display. We refuse to
    # mutate any block whose content is a typed-block list, AND skip results
    # whose output_preview heuristically looks like a media wrapper.
    skip_media_results: bool = True

    # Marker text inserted at the top of the augmented preview.
    substitute_message: str = _DEFAULT_SUBSTITUTE

    def to_snapshot(self) -> dict[str, Any]:
        """Plain-dict snapshot for persistence (cx_request.trim_summary)."""
        return {
            "tier_1_min_positions_back": self.tier_1_min_positions_back,
            "tier_1_min_output_chars": self.tier_1_min_output_chars,
            "tier_2_min_positions_back": self.tier_2_min_positions_back,
            "tier_2_min_output_chars": self.tier_2_min_output_chars,
            "skip_media_results": self.skip_media_results,
        }


@dataclass
class TrimReport:
    """Audit of one ``trim_messages_context`` pass.

    Persisted verbatim onto ``cx_request.trim_summary`` so the Model Context UI
    can show what just happened (which blocks got rewritten, why, what the
    policy was) without diffing snapshots.

    Fields:
      * blocks_rewritten — count of tool_result blocks whose content was
        replaced with the augmented preview.
      * freed_chars — chars removed from the in-memory payload (before - after).
      * before_total_chars / after_total_chars — JSON-string size of the trimmed
        slice (only tool_result blocks counted) before and after the pass.
      * rewritten_blocks — per-block detail: list of {message_position,
        call_id, tool_name, before_chars, after_chars}.
      * eligible_but_skipped_reason — one of None | "cache_protect" |
        "no_eligible_messages". Distinguishes "ran but nothing matched" from
        "didn't run because of the cache gate."
      * policy — the TrimPolicy.to_snapshot() in effect when this pass ran.
    """

    blocks_rewritten: int = 0
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
    """Trim tool_result content in-place. Returns a TrimReport.

    Safe to call on any message list — non-qualifying blocks are
    skipped silently. Idempotent: re-running on the same list does
    nothing new (the augmented preview's own size is well below either
    tier's threshold, so it won't re-qualify).

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

        for block in msg.content:
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
                    "tier": "tier_2"
                    if positions_back >= policy.tier_2_min_positions_back
                    else "tier_1",
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

    Walks the same eligibility predicate as the main loop but sums
    ``output_chars`` instead of mutating. Conservative — uses
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
