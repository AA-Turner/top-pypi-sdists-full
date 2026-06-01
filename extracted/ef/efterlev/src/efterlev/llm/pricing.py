"""Per-model pricing snapshot for the end-of-run cost summary (Tier 1 #2a, v0.1.19).

Hardcoded table over a YAML config because (a) the table is small enough
that a Python dict is the right tool, (b) we want compile-time visibility
into "what models are priced," and (c) `as_of` dates encode honest
snapshot freshness without a separate file's load step. See DECISIONS
2026-05-06 "Tier 1 #2a design: end-of-run cost summary on agent commands"
for the alternatives considered.

Pricing source: Anthropic's published rates as of `as_of` per entry.
Anthropic occasionally adjusts prices and adds discounts; the
end-of-run summary uses the `~` prefix on the dollar estimate to signal
approximation. Bedrock backend uses the same rates as a proxy because
AWS Bedrock pricing varies by region and discount tier — the summary
adds a clarifying suffix in that case.

When you add a new model to the codebase (e.g. Sonnet 4.7 ships, the
factory switches), add an entry here in the same PR. `lookup()` returns
None for unregistered models, which the cost summary handles gracefully
(tokens-only, no dollar estimate).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# OpenAI Chat Completions reports the *served* model as a dated snapshot
# (e.g. "gpt-5.4-mini-2026-03-17") even when the request used the base
# alias ("gpt-5.4-mini"). The pricing table keys on the base alias, so
# `lookup` strips a trailing ISO date and retries — keeps cost estimates
# working for any snapshot of a registered model without a per-snapshot
# table edit. Anthropic/Bedrock dated IDs use `-YYYYMMDD` (no inner
# dashes) and so don't match this pattern.
_OPENAI_SNAPSHOT_DATE_SUFFIX = re.compile(r"-\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class ModelPrice:
    """Anthropic-published per-MTok pricing for one model.

    `input_per_mtok_usd` and `output_per_mtok_usd` are USD per million
    tokens of input / output. `as_of` is the ISO date the snapshot was
    taken — a maintainer reading this six months from now should suspect
    the price may have changed and re-check anthropic.com/pricing.
    """

    model_id: str
    input_per_mtok_usd: float
    output_per_mtok_usd: float
    as_of: str  # ISO date


# Model-ID → ModelPrice. Aliases (Bedrock IDs) point at the same
# Anthropic rate as their Anthropic-API counterpart; the cost summary
# qualifies bedrock-backed costs with a "via bedrock" suffix at the
# call site.
_PRICING: dict[str, ModelPrice] = {
    # Anthropic API IDs.
    "claude-opus-4-7": ModelPrice(
        model_id="claude-opus-4-7",
        input_per_mtok_usd=15.00,
        output_per_mtok_usd=75.00,
        as_of="2026-05-06",
    ),
    "claude-sonnet-4-6": ModelPrice(
        model_id="claude-sonnet-4-6",
        input_per_mtok_usd=3.00,
        output_per_mtok_usd=15.00,
        as_of="2026-05-06",
    ),
    "claude-haiku-4-5": ModelPrice(
        model_id="claude-haiku-4-5",
        input_per_mtok_usd=1.00,
        output_per_mtok_usd=5.00,
        as_of="2026-05-15",
    ),
    # Bedrock model IDs alias to the same Anthropic rate as proxies.
    # AWS Bedrock pricing varies by region and discount tier; the cost
    # summary surfaces the proxy nature in a suffix.
    "us.anthropic.claude-opus-4-7-v1:0": ModelPrice(
        model_id="us.anthropic.claude-opus-4-7-v1:0",
        input_per_mtok_usd=15.00,
        output_per_mtok_usd=75.00,
        as_of="2026-05-06",
    ),
    "us.anthropic.claude-sonnet-4-6-v1:0": ModelPrice(
        model_id="us.anthropic.claude-sonnet-4-6-v1:0",
        input_per_mtok_usd=3.00,
        output_per_mtok_usd=15.00,
        as_of="2026-05-06",
    ),
    "us.anthropic.claude-haiku-4-5-20251001-v1:0": ModelPrice(
        model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        input_per_mtok_usd=1.00,
        output_per_mtok_usd=5.00,
        as_of="2026-05-15",
    ),
    # NVIDIA Nemotron family on Bedrock (released 2026-03-18). On-Demand
    # pricing for us-east-1, us-east-2, us-west-2 per AWS published rates.
    # GovCloud-deployable; hybrid MoE architecture (12B active params)
    # gives Sonnet-class throughput at Haiku-class price.
    "nvidia.nemotron-super-3-120b": ModelPrice(
        model_id="nvidia.nemotron-super-3-120b",
        input_per_mtok_usd=0.15,
        output_per_mtok_usd=0.65,
        as_of="2026-05-15",
    ),
    "nvidia.nemotron-3-nano-30b-a3b": ModelPrice(
        model_id="nvidia.nemotron-3-nano-30b-a3b",
        input_per_mtok_usd=0.06,
        output_per_mtok_usd=0.24,
        as_of="2026-05-15",
    ),
    "nvidia.nemotron-nano-2": ModelPrice(
        model_id="nvidia.nemotron-nano-2",
        input_per_mtok_usd=0.06,
        output_per_mtok_usd=0.23,
        as_of="2026-05-15",
    ),
    # OpenAI gpt-oss family on Bedrock (released 2026-Q1). Reasoning
    # model — emits internal reasoning chains. May produce more output
    # tokens than non-reasoning models for the same task; same per-token
    # rate but real wall-clock + cost can be higher per Gap-Agent KSI
    # depending on prompt shape.
    "openai.gpt-oss-120b-1:0": ModelPrice(
        model_id="openai.gpt-oss-120b-1:0",
        input_per_mtok_usd=0.15,
        output_per_mtok_usd=0.65,
        as_of="2026-05-15",
    ),
    # OpenAI native API (Chat Completions) — added v0.1.211 alongside the
    # `openai` backend (experimental). Prices are the publicly-announced
    # GPT-5 family rates as of 2026-05-27; revisit on the first dispatch
    # if usage/receipts.log totals look off (estimate is informational, not
    # billing-authoritative).
    "gpt-5.4": ModelPrice(
        model_id="gpt-5.4",
        input_per_mtok_usd=1.25,
        output_per_mtok_usd=10.00,
        as_of="2026-05-27",
    ),
    # gpt-5.4-mini is the recommended OpenAI production model from v0.1.213:
    # eval-harness scored 95.8% precision + 100% recall on csp-starter-cfn
    # (vs. gpt-5 at 100%/95.8% and gpt-5.4 reliably failing the model-layer
    # citation validator). Pricing applies the gpt-5-mini ratio family-
    # convention; revisit if OpenAI publishes different rates.
    "gpt-5.4-mini": ModelPrice(
        model_id="gpt-5.4-mini",
        input_per_mtok_usd=0.25,
        output_per_mtok_usd=2.00,
        as_of="2026-05-28",
    ),
    "gpt-5.4-nano": ModelPrice(
        model_id="gpt-5.4-nano",
        input_per_mtok_usd=0.05,
        output_per_mtok_usd=0.40,
        as_of="2026-05-28",
    ),
    "gpt-5": ModelPrice(
        model_id="gpt-5",
        input_per_mtok_usd=1.25,
        output_per_mtok_usd=10.00,
        as_of="2026-05-27",
    ),
    "gpt-5-mini": ModelPrice(
        model_id="gpt-5-mini",
        input_per_mtok_usd=0.25,
        output_per_mtok_usd=2.00,
        as_of="2026-05-27",
    ),
    "gpt-5-nano": ModelPrice(
        model_id="gpt-5-nano",
        input_per_mtok_usd=0.05,
        output_per_mtok_usd=0.40,
        as_of="2026-05-27",
    ),
}


def lookup(model_id: str) -> ModelPrice | None:
    """Return the pricing entry for `model_id`, or None if unregistered.

    The cost summary's caller treats None as "skip the dollar estimate,
    show tokens-only." Don't raise on unregistered models — a future
    Anthropic release might land in a customer's wheel before this table
    is updated, and crashing the agent's success-path output over a
    missing pricing entry would be the wrong trade.
    """
    price = _PRICING.get(model_id)
    if price is not None:
        return price
    # Fall back to the base alias for OpenAI dated snapshots
    # (e.g. "gpt-5.4-mini-2026-03-17" → "gpt-5.4-mini").
    base = _OPENAI_SNAPSHOT_DATE_SUFFIX.sub("", model_id)
    if base != model_id:
        return _PRICING.get(base)
    return None


def estimate_cost_usd(
    model_id: str,
    input_tokens: int,
    output_tokens: int,
) -> float | None:
    """Return USD cost estimate, or None if `model_id` isn't registered."""
    price = lookup(model_id)
    if price is None:
        return None
    return (
        input_tokens * price.input_per_mtok_usd / 1_000_000
        + output_tokens * price.output_per_mtok_usd / 1_000_000
    )


def is_bedrock_model(model_id: str) -> bool:
    """True for Bedrock model IDs (which carry the `via bedrock` suffix
    in the cost summary). Bedrock IDs are dotted with provider/region
    prefixes (e.g. `us.anthropic.claude-...`, `nvidia.nemotron-...`,
    `openai.gpt-oss-...`)."""
    return model_id.startswith(
        (
            "us.anthropic.",
            "anthropic.",
            "nvidia.",
            "us.nvidia.",
            "meta.",
            "us.meta.",
            "openai.",
            "us.openai.",
        )
    )
