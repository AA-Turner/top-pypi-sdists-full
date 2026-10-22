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
(measured as ``len(json.dumps(arguments))``) is trimmed IN ITS OWN SHAPE:
every key and short value stays, each long string or list is cut and ends in
a note saying the rest was trimmed. The tool's stored state is authoritative;
the model re-reads it (e.g. ``get_workflow``) when needed. A new call carrying
that note is refused by the tool executor (``arguments_carry_trim_marker``).

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
  after persisted messages for the reported ``message_position``. Their
  position field is never mutated.

Distance is counted in MODEL ITERATIONS, not raw messages (2026-10-17)
---------------------------------------------------------------------
"Positions back" used to be the raw message distance from the head. A parallel
batch of tool calls appends one message per result, so a result only one or two
model iterations old could already be 12+ messages back and get cleared before
the model had read it (conversation e9c0d599: a provider-settings read and a DB
structure read were cleared before the agent used them). Now:

  * ``iterations_back`` = how many assistant messages come after the message.
  * ``positions_back``  = ``2 × iterations_back`` (+1 for an assistant message):
    one iteration is ONE assistant message plus its results, however many
    results it produced. In a serial one-call-per-iteration loop this is exactly
    the old raw distance, so the ruled 12/24 knob values keep their measured
    meaning; a parallel batch no longer inflates it.
  * A block with ``iterations_back == 0`` is NEVER trimmed, whatever the tiers
    say: a result the model has not yet had one turn to act on stays whole.
"""

from __future__ import annotations

import json
import math
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from matrx_ai.config.message_config import UnifiedMessage

_DEFAULT_SUBSTITUTE = (
    "[tool result cleared] Replaced with keys and chars -- Fetch again when necessary"
)

# A stale call keeps its REAL shape: every key and every short value stays,
# and only a long string (or a long list) is cut, with this note in place of
# the rest. It used to become ``{"result": "[tool arguments cleared] …",
# "keys": […], "chars": N}`` — a fake argument object the model then copied as
# its own arguments on new calls (conversation 9b224bf5, 2026-10-21: two
# ``agent`` calls and one ``shell_python`` call sent that object and were
# refused). ``{n}`` is the count removed; the note names its own kind.
_DEFAULT_ARGUMENTS_SUBSTITUTE = (
    "…[{n} more {unit} trimmed from context; the call ran with the full value — "
    "never copy this text into a new call]"
)

# The words every note carries. The tool executor refuses a NEW call whose
# arguments contain them (``arguments_carry_trim_marker``): the model copied
# trimmed history, and running it would send a truncated value.
TRIMMED_ARGUMENT_MARKER = "trimmed from context; the call ran with the full value"
# The retired stub's words — still refused if a model reproduces them.
_RETIRED_ARGUMENT_STUB_MARKER = "[tool arguments cleared]"

# How much of a long string value a trimmed call keeps, and how many items
# of a long list.
ARGUMENT_STRING_KEEP_CHARS = 240
ARGUMENT_LIST_KEEP_ITEMS = 8

# Phase 2: cache-aware gate constants.
#
# When prompt-cache is alive AND the trimmable savings on this turn are below
# this floor, skip the trim entirely — breaking the cache prefix to save a few
# hundred tokens is a losing trade. Real "let's reclaim space" turns easily
# clear 5K (one large page-fetch, one screenshot, one big search result).
CACHE_GATE_MIN_SAVED_TOKENS = 5000

# THE CACHE GATE MODE (``agents.context_trim / cache_gate_mode``, ai_114).
#
#   legacy  — the 2026-05-16 rule: a warm-cache trim runs whenever it frees at
#             least ``cache_gate_min_saved_tokens``. It never weighs the
#             rebuild, and a trim rewrites everything after its first rewritten
#             block at the cache-WRITE price (Cora's 2026-10-15 Opus 5.5 job:
#             21 mid-loop trims freed 4-25K tokens each and forced 53-128K-token
#             rewrites — ~775 ¢ of avoidable writes on one $18 job).
#   payback — a warm-cache trim runs only when it pays back:
#             freed_tokens × read_price × expected_remaining_calls
#               ≥ rewrite_tokens × (write_price − read_price),
#             at the model's real catalog prices. Otherwise it is HELD: the
#             eligible blocks stay as they are (recorded, accumulated into
#             ``cache_state.cumulative_trimmable_chars``) and are taken together
#             at the next cold cache, when the rewrite is paid anyway — or at
#             once when the prompt nears the model's window / the pre-flight
#             ceiling, so a held trim can never cause a refusal.
# A cold cache (expired or unknown) trims exactly as legacy always did.
CACHE_GATE_MODE_LEGACY = "legacy"
CACHE_GATE_MODE_PAYBACK = "payback"
CACHE_GATE_MODES: tuple[str, ...] = (CACHE_GATE_MODE_LEGACY, CACHE_GATE_MODE_PAYBACK)

# Starting values (agent-set, 2026-10-16; the knob rows carry basis + review date).
#: How many more warm-cache sends a freed token is expected to be saved on.
#: Conservative: a tool loop iteration sequence measured 7-17 sends (Cora's job);
#: a held trim is never lost — it is taken at the next cold cache.
PAYBACK_EXPECTED_REMAINING_CALLS = 20
#: A held trim is forced once the estimated prompt reaches this percent of the
#: pre-flight ceiling (context window × trip fraction).
PAYBACK_FORCE_WINDOW_PERCENT = 85

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

# THE BUDGET ESTIMATE — "will this fit / how big is it", shown to a person or
# checked against a model's window. The opposite direction from the savings
# divisor above: here an UNDER-count is the dangerous error (it promises a fit
# the provider then refuses), so the ratios are the MEASURED ones, set just
# below the 2.98 chars/token a real 316,200-char research context was billed at
# (105,969 input tokens, Context Builder Brand Profile run, 2026-07-25). The
# measurement is recorded once, in matrx-frontend ``lib/tokens/estimate.ts``
# (``CHARS_PER_TOKEN``); these values are its server twin and
# ``aidream/services/conversation_context/tests/test_one_token_estimator.py``
# fails when the two drift. Re-measure there; never restore a textbook 4.
CHARS_PER_TOKEN_MEASURED: dict[str, float] = {
    "prose": 2.9,  # ordinary prose with markup: articles, notes, documents
    "structured": 2.4,  # JSON / structured payloads / URL and link lists
}


def estimate_budget_tokens(chars: int, shape: str = "prose") -> int:
    """Estimated tokens for ``chars`` characters of ``shape`` content — the one
    budget estimator, rounding up exactly like the client's ``estimateTokens``."""
    if chars <= 0:
        return 0
    return math.ceil(chars / CHARS_PER_TOKEN_MEASURED[shape])


@dataclass
class TrimPolicy:
    """Tunable policy for ``trim_messages_context``.

    Defaults are Arman's 2026-09-09 ruling (see module docstring):
      * 12+ positions back AND > 8000 chars → replace
      * 24+ positions back AND > 2000 chars → replace
    A "position" is half a model iteration (2026-10-17): one assistant message
    plus all its results count as 2, so a parallel batch cannot age a fresh
    result, and nothing is trimmed before the model has acted on it once.
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
    # gate; set False to restore the result-only behavior.
    trim_tool_call_arguments: bool = True

    # The note that replaces the cut part of a long argument value; ``{n}``
    # and ``{unit}`` are filled per value. Must contain TRIMMED_ARGUMENT_MARKER.
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
            "cache_gate_mode": self.cache_gate_mode,
            "cache_gate_min_saved_tokens": self.cache_gate_min_saved_tokens,
            "payback_expected_remaining_calls": self.payback_expected_remaining_calls,
            "payback_force_window_percent": self.payback_force_window_percent,
            "source": self.source,
        }

    # The cache gate (see CACHE_GATE_MODE_* above). Knobs, ai_114.
    cache_gate_mode: str = CACHE_GATE_MODE_LEGACY
    cache_gate_min_saved_tokens: int = CACHE_GATE_MIN_SAVED_TOKENS
    payback_expected_remaining_calls: int = PAYBACK_EXPECTED_REMAINING_CALLS
    payback_force_window_percent: int = PAYBACK_FORCE_WINDOW_PERCENT

    # Where the tier numbers came from — lands in every audit row so a trim is
    # always attributable: "package_default" (standalone, no host resolver),
    # "org_knobs" (the host's per-organization knob resolution), or
    # "package_default:resolver_failed" (the host resolver raised; announced).
    source: str = "package_default"


# --------------------------------------------------------------------------- #
# Org knobs — the host resolves the tiers per organization                     #
# --------------------------------------------------------------------------- #
#
# The tiers are an OPINION (cost vs recall), so they are organization knobs
# (law 6): ``platform.feature_knob`` feature ``agents.context_trim``, seeded by
# aidream ``db/migrations/ai_096`` with exactly the ruled defaults above,
# overridable at the ORGANIZATION rung. This package must not import the host,
# so the host installs ONE async resolver at boot
# (``set_trim_policy_resolver``) and ``prepare_for_send`` — the one send
# boundary — resolves the policy through it. With no host the dataclass
# defaults are the ruling. A resolver that RAISES (e.g. the host's
# ``KnobNotRegisteredError`` for a missing row) is announced in red and the
# audit row carries ``source="package_default:resolver_failed"`` — never a
# silent default.

TRIM_POLICY_KNOB_FEATURE = "agents.context_trim"
#: Integer knobs (read with the host's int reader).
TRIM_POLICY_KNOB_KEYS: tuple[str, ...] = (
    "tier_1_min_positions_back",
    "tier_1_min_output_chars",
    "tier_2_min_positions_back",
    "tier_2_min_output_chars",
    "cache_gate_min_saved_tokens",
    "payback_expected_remaining_calls",
    "payback_force_window_percent",
)
#: Text knobs (read with the host's str reader). ``cache_gate_mode``: legacy | payback.
TRIM_POLICY_KNOB_STR_KEYS: tuple[str, ...] = ("cache_gate_mode",)

#: ``async (organization_id) -> TrimPolicy``.
TrimPolicyResolver = Callable[[str | None], Awaitable[TrimPolicy]]

_TRIM_POLICY_RESOLVER: TrimPolicyResolver | None = None


def set_trim_policy_resolver(resolver: TrimPolicyResolver | None) -> None:
    """Install the host's per-organization knob reader (``None`` = standalone)."""
    global _TRIM_POLICY_RESOLVER
    _TRIM_POLICY_RESOLVER = resolver


def get_trim_policy_resolver() -> TrimPolicyResolver | None:
    return _TRIM_POLICY_RESOLVER


def trim_policy_from_knobs(values: dict[str, Any]) -> TrimPolicy:
    """Build a policy from resolved knob values (every key REQUIRED — a missing
    one raises ``KeyError`` naming it rather than quietly using a default)."""
    mode = str(values["cache_gate_mode"]).strip().lower()
    if mode not in CACHE_GATE_MODES:
        raise ValueError(
            f"agents.context_trim/cache_gate_mode is {mode!r}; allowed: {CACHE_GATE_MODES}"
        )
    return TrimPolicy(
        **{key: int(values[key]) for key in TRIM_POLICY_KNOB_KEYS},
        cache_gate_mode=mode,
        source="org_knobs",
    )


async def resolve_trim_policy(organization_id: str | None) -> TrimPolicy:
    """The trim policy this organization's sends obey."""
    resolver = _TRIM_POLICY_RESOLVER
    if resolver is None:
        return TrimPolicy()
    try:
        policy = await resolver(organization_id)
    except Exception as exc:  # noqa: BLE001 — one failure shape, said out loud
        from matrx_utils import vcprint

        vcprint(
            f"[context_trim] the {TRIM_POLICY_KNOB_FEATURE} knobs could not be resolved for "
            f"organization {organization_id!r} ({type(exc).__name__}: {exc}); this send uses "
            "the package's ruled defaults (12/8000 + 24/2000). Fix the knob rows or the "
            "host resolver.",
            color="red",
        )
        return TrimPolicy(source="package_default:resolver_failed")
    if not isinstance(policy, TrimPolicy):
        raise TypeError(
            f"trim policy resolver returned {type(policy).__name__}, not TrimPolicy"
        )
    return policy


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


@dataclass
class CacheGateInputs:
    """What the payback rule needs that the message list alone cannot say.

    Built by the send boundary from the config it is about to send (catalog
    prices, the model's window, the pre-flight's estimate). Every field may be
    ``None``: a payback gate with no prices announces it and falls back to the
    legacy floor rather than guessing.

    Prices are USD per million tokens. ``write_price`` is the price of the
    cache tier that covers the REWRITTEN region (the history after the first
    trimmed block), ``rewrite_ttl_secs`` its lifetime.
    """

    model: str | None = None
    read_price: float | None = None
    write_price: float | None = None
    rewrite_ttl_secs: int | None = None
    long_cache: bool = False
    estimated_prompt_tokens: int | None = None
    preflight_ceiling_tokens: int | None = None

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "read_price": self.read_price,
            "write_price": self.write_price,
            "rewrite_ttl_secs": self.rewrite_ttl_secs,
            "long_cache": self.long_cache,
            "estimated_prompt_tokens": self.estimated_prompt_tokens,
            "preflight_ceiling_tokens": self.preflight_ceiling_tokens,
        }


def trim_messages_context(
    messages: list[UnifiedMessage],
    policy: TrimPolicy | None = None,
    cache_state: dict[str, Any] | None = None,
    gate_inputs: CacheGateInputs | None = None,
) -> TrimReport:
    """Trim tool_result content and tool_call arguments in-place. Returns a TrimReport.

    Safe to call on any message list — non-qualifying blocks are
    skipped silently. Idempotent: re-running on the same list does
    nothing new (the augmented preview's own size is well below either
    tier's threshold, so it won't re-qualify; the argument stub is
    additionally recognized by its marker and never re-rewritten).

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

    # THE CACHE GATE — one decision, one audit shape (``policy["cache_gate"]``).
    if cache_state:
        gate = _decide_cache_gate(
            messages,
            policy,
            current_position,
            effective_positions,
            cache_state,
            gate_inputs,
        )
        if gate is not None:
            report.policy["cache_gate"] = gate
            if gate["skipped"]:
                report.eligible_but_skipped_reason = "cache_protect"
                return report

    distances = _iteration_distances(messages)
    for msg, (positions_back, iterations_back) in zip(messages, distances, strict=True):
        effective_position = effective_positions[id(msg)]
        tier_rule = _tier_for(policy, positions_back, iterations_back)
        if tier_rule is None:
            continue
        tier, min_chars = tier_rule

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
                        "iterations_back": iterations_back,
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
                    "iterations_back": iterations_back,
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
    return age < (float(_cache_ttl_secs(cache_state)) * CACHE_GATE_TTL_RATIO)


def _cache_ttl_secs(cache_state: dict[str, Any]) -> int:
    """The lifetime of the cache that covers the history a trim would rewrite:
    ``est_cache_ttl_secs`` when the state carries it (the send boundary sets it
    from the wire's real marks — see ``cache_marks.history_cache_ttl_secs``),
    else the provider default."""
    ttl = cache_state.get("est_cache_ttl_secs")
    if not ttl:
        provider = (cache_state.get("last_provider") or "").lower()
        ttl = DEFAULT_CACHE_TTLS_SECS.get(provider, 300)
    return int(ttl)


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
    0`` while assistant content held 1.5M chars). Counted with the ONE
    estimator (``estimate_budget_tokens``, measured ratios) so the savings the
    gate weighs and the size the preflight refuses are the same tokens; the
    caution lives in ``CACHE_GATE_MIN_SAVED_TOKENS``, never in a second divisor.
    """
    total_chars, _first, _blocks = _eligible_scan(messages, policy, current_position)
    return estimate_budget_tokens(total_chars, "prose")


# Rough size of the stub a rewritten block leaves behind (marker + keys + size).
_STUB_CHARS_ESTIMATE = 300


def _is_assistant(msg: UnifiedMessage) -> bool:
    return str(getattr(msg, "role", "") or "").lower() == "assistant"


def _iteration_distances(messages: list[UnifiedMessage]) -> list[tuple[int, int]]:
    """Per message: ``(positions_back, iterations_back)`` measured in model
    iterations (see the module docstring). One pass, right to left.

    ONE model iteration counts ONCE. A translator may store one provider
    response as several consecutive assistant messages (text, then tool calls;
    a terminal-handoff answer after the reply). Counting each of them moved
    older results ~2x faster through the tiers than intended (adversarial
    review M2, 2026-10-18). A new iteration always needs a non-assistant
    message (tool result, person turn) before it, so a run of consecutive
    assistant messages is one iteration."""
    out: list[tuple[int, int]] = [(0, 0)] * len(messages)
    iterations_after = 0
    right_is_assistant = False
    for index in range(len(messages) - 1, -1, -1):
        msg = messages[index]
        assistant = _is_assistant(msg)
        same_iteration = assistant and right_is_assistant
        after = iterations_after - 1 if same_iteration else iterations_after
        out[index] = (2 * after + (1 if assistant else 0), after)
        if assistant and not same_iteration:
            iterations_after += 1
        right_is_assistant = assistant
    return out


def _tier_for(policy: TrimPolicy, positions_back: int, iterations_back: int) -> tuple[str, int] | None:
    """``(tier, min_chars)`` for a message at this distance, or ``None`` when it
    is too recent — including the hard rule: never before the model has had at
    least one turn after it (``iterations_back >= 1``)."""
    if iterations_back < 1 or positions_back < policy.tier_1_min_positions_back:
        return None
    if positions_back >= policy.tier_2_min_positions_back:
        return "tier_2", policy.tier_2_min_output_chars
    return "tier_1", policy.tier_1_min_output_chars


def _eligible_scan(
    messages: list[UnifiedMessage],
    policy: TrimPolicy,
    current_position: int,
) -> tuple[int, int | None, int]:
    """(eligible chars, list index of the first message holding one, block count).

    The same eligibility predicate as the trim loop, without mutating.
    """
    del current_position  # distance is counted in model iterations, not positions
    total_chars = 0
    first_index: int | None = None
    blocks = 0
    distances = _iteration_distances(messages)
    for index, msg in enumerate(messages):
        tier_rule = _tier_for(policy, *distances[index])
        if tier_rule is None:
            continue
        _tier, min_chars = tier_rule
        for block in msg.content:
            if policy.trim_tool_call_arguments and _is_tool_call_block(block):
                arg_chars = _tool_call_argument_chars(block)
                if arg_chars < min_chars:
                    continue
                if _already_trimmed_arguments(block):
                    continue
                total_chars += arg_chars
                blocks += 1
                if first_index is None:
                    first_index = index
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
            blocks += 1
            if first_index is None:
                first_index = index
    return total_chars, first_index, blocks


def _rewrite_region_tokens(
    messages: list[UnifiedMessage], first_index: int, eligible_chars: int, blocks: int
) -> int:
    """Tokens a trim makes the provider WRITE again: every message from the first
    rewritten one to the end, as it will look AFTER the trim. Measured with the
    pre-flight's serializer and the one budget estimator, so it is the same kind
    of number as the prompt estimate."""
    from matrx_ai.config.context_preflight import _chars

    region_chars = sum(_chars(msg) for msg in messages[first_index:])
    after = max(0, region_chars - eligible_chars) + blocks * _STUB_CHARS_ESTIMATE
    return estimate_budget_tokens(after, "prose")


def _decide_cache_gate(
    messages: list[UnifiedMessage],
    policy: TrimPolicy,
    current_position: int,
    effective_positions: dict[int, int],
    cache_state: dict[str, Any],
    gate_inputs: CacheGateInputs | None,
) -> dict[str, Any] | None:
    """THE cache gate decision. Returns the audit dict (``skipped`` True = hold).

    Cold cache (expired / unknown age) → take, in every mode: the rewrite is paid
    anyway, so this is also where held trims are collected.
    """
    del effective_positions  # positions are re-derived by the scan
    mode = (policy.cache_gate_mode or CACHE_GATE_MODE_LEGACY).lower()
    age = _cache_age_secs(cache_state)
    ttl = _cache_ttl_secs(cache_state)
    base: dict[str, Any] = {
        "mode": mode,
        "cache_state_age_secs": age,
        "cache_ttl_secs": ttl,
    }
    if gate_inputs is not None:
        base["inputs"] = gate_inputs.to_snapshot()
    if mode == CACHE_GATE_MODE_PAYBACK:
        # Payback margin points the other way: treating a live cache as cold costs
        # a full rewrite (Cora 2026-10-18: 263 s of a 300 s TTL, 70 ¢), treating an
        # expired one as warm only delays a trim. Between RATIO x TTL and TTL the
        # cache counts as warm; only age >= TTL (or unknown) is cold.
        cold = age is None or age >= float(ttl)
    else:
        cold = not _is_cache_likely_alive(cache_state)
    if cold:
        return {**base, "skipped": False, "rule": "cold_cache", "decision": "take"}

    eligible_chars, first_index, blocks = _eligible_scan(messages, policy, current_position)
    est_savings_tokens = estimate_budget_tokens(eligible_chars, "prose")
    base["est_savings_tokens"] = est_savings_tokens
    base["est_savings_chars"] = eligible_chars

    def legacy(rule: str) -> dict[str, Any]:
        floor = int(policy.cache_gate_min_saved_tokens)
        hold = est_savings_tokens < floor
        return {
            **base,
            "skipped": hold,
            "rule": rule,
            "decision": "hold" if hold else "take",
            "min_required_tokens": floor,
        }

    if mode != CACHE_GATE_MODE_PAYBACK:
        return legacy("legacy_floor")
    if first_index is None or est_savings_tokens <= 0:
        return {**base, "skipped": False, "rule": "nothing_eligible", "decision": "take"}

    inputs = gate_inputs or CacheGateInputs()
    base["inputs"] = inputs.to_snapshot()
    rewrite_tokens = _rewrite_region_tokens(messages, first_index, eligible_chars, blocks)
    calls = max(1, int(policy.payback_expected_remaining_calls))
    base["rewrite_tokens"] = rewrite_tokens
    base["expected_remaining_calls"] = calls

    # Near the window / the pre-flight ceiling: a held trim is taken NOW, so
    # holding can never be what makes a send get refused.
    ceiling = inputs.preflight_ceiling_tokens
    if ceiling and inputs.estimated_prompt_tokens is not None:
        force_at = int(ceiling * max(1, int(policy.payback_force_window_percent)) / 100)
        base["force_at_tokens"] = force_at
        if inputs.estimated_prompt_tokens >= force_at:
            return {**base, "skipped": False, "rule": "forced_near_limit", "decision": "take"}

    read_price, write_price = inputs.read_price, inputs.write_price
    if read_price is None or write_price is None:
        from matrx_utils import vcprint

        vcprint(
            f"[context_trim] payback cache gate has no catalog prices for "
            f"{inputs.model!r}; this send uses the legacy floor rule instead.",
            color="yellow",
        )
        return legacy("payback_unpriced:legacy_floor")

    benefit_usd = est_savings_tokens * read_price * calls / 1_000_000
    cost_usd = rewrite_tokens * max(0.0, write_price - read_price) / 1_000_000
    take = benefit_usd >= cost_usd
    return {
        **base,
        "skipped": not take,
        "rule": "payback",
        "decision": "take" if take else "hold",
        "benefit_usd": round(benefit_usd, 6),
        "rewrite_cost_usd": round(cost_usd, 6),
    }


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
    """True if this call's arguments were already trimmed by an earlier pass."""
    return arguments_carry_trim_marker(_get_arguments(block)) is not None


def arguments_carry_trim_marker(arguments: Any) -> str | None:
    """The trim note found anywhere in ``arguments``, or None.

    Used twice: here, so a trimmed call is never trimmed again; and by the tool
    executor, which refuses a NEW call carrying it (the model copied history).
    """
    try:
        text = json.dumps(arguments, default=str, ensure_ascii=False)
    except (TypeError, ValueError):
        text = str(arguments)
    for marker in (TRIMMED_ARGUMENT_MARKER, _RETIRED_ARGUMENT_STUB_MARKER):
        if marker in text:
            return marker
    return None


def _trim_argument_value(value: Any, note: str) -> Any:
    """``value`` with every long string and long list cut, shape kept."""
    if isinstance(value, str):
        if len(value) <= ARGUMENT_STRING_KEEP_CHARS:
            return value
        cut = len(value) - ARGUMENT_STRING_KEEP_CHARS
        return value[:ARGUMENT_STRING_KEEP_CHARS] + note.format(n=cut, unit="characters")
    if isinstance(value, dict):
        return {k: _trim_argument_value(v, note) for k, v in value.items()}
    if isinstance(value, list):
        kept = [_trim_argument_value(v, note) for v in value[:ARGUMENT_LIST_KEEP_ITEMS]]
        if len(value) > ARGUMENT_LIST_KEEP_ITEMS:
            kept.append(note.format(n=len(value) - ARGUMENT_LIST_KEEP_ITEMS, unit="items"))
        return kept
    return value


def _rewrite_tool_call_arguments(block: Any, note: str) -> None:
    """Trim a stale tool call's ``arguments`` in place of themselves.

    Every key stays and every short value stays; a long string keeps its first
    ``ARGUMENT_STRING_KEEP_CHARS`` characters and a long list its first
    ``ARGUMENT_LIST_KEEP_ITEMS`` items, each followed by ``note``. The result
    is still a plain dict (an object for every provider), and the block's
    id / call_id / name / type / metadata are untouched, so the provider's
    tool_use ↔ tool_result pairing survives intact.
    """
    arguments = _get_arguments(block)
    if not isinstance(arguments, dict):
        return
    _set_arguments(block, _trim_argument_value(arguments, note))


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
