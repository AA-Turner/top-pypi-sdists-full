"""End-of-run cost summary for agent commands (Tier 1 #2a, v0.1.19).

Reads `.efterlev/receipts.log` for entries this invocation produced
(filtered by `started_at`), aggregates token usage by model, looks up
pricing in `efterlev.llm.pricing`, and returns a single-line summary
suitable for printing as the last line of an agent command's success
output.

Reads receipts.log over per-agent collection because the data is
already captured at the data layer (v0.1.9 token telemetry on every
Claim record), so this presentation surface adds zero coupling to the
agent API. See DECISIONS 2026-05-06 "Tier 1 #2a design" for the full
rationale and alternatives considered.

Returns None when no LLM-bearing receipts are found in the window
(e.g. the agent ran with `StubLLMClient` in tests, or the agent
short-circuited before invoking the LLM). Returning None lets the
caller skip the print without an awkward "0 tokens spent" line.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from efterlev.llm.pricing import (
    estimate_cost_usd,
    is_bedrock_model,
)
from efterlev.llm.pricing import (
    lookup as lookup_pricing,
)
from efterlev.provenance.receipts import ReceiptLog


def _aggregate_by_model(
    entries: list[dict[str, Any]],
    started_at: datetime,
) -> dict[str, tuple[int, int]]:
    """Sum (input_tokens, output_tokens) per model for entries past `started_at`.

    Entries without a `model` field, without `input_tokens`/`output_tokens`,
    or with a timestamp before `started_at` are skipped. Returns an empty
    dict when nothing matches.
    """
    by_model: dict[str, tuple[int, int]] = {}
    for entry in entries:
        ts_str = entry.get("ts")
        model = entry.get("model")
        in_tok = entry.get("input_tokens")
        out_tok = entry.get("output_tokens")
        if not ts_str or not model or in_tok is None or out_tok is None:
            continue
        try:
            ts = datetime.fromisoformat(ts_str)
        except ValueError:
            continue
        if ts < started_at:
            continue
        prev_in, prev_out = by_model.get(model, (0, 0))
        by_model[model] = (prev_in + int(in_tok), prev_out + int(out_tok))
    return by_model


def summarize_run_cost(
    workspace_root: Path,
    started_at: datetime,
) -> str | None:
    """Return a one-line cost summary for receipts past `started_at`, or None.

    Single-model run produces:
        `LLM cost: 38,201 in / 8,455 out tokens on claude-sonnet-4-6 (~$0.24)`
    Multi-model run (e.g. Opus → Sonnet fallback fired mid-run) produces:
        `LLM cost: 41,200 in / 9,012 out tokens on opus + sonnet (~$1.34)`
    Bedrock backend appends ` (via bedrock; AWS region pricing may differ)`.
    Unregistered model appends ` (pricing for <model> not registered)`.
    Subscription backend (v0.1.151 / #356) replaces the $ figure with
    "subscription run (no per-call billing)" because per-token cost
    doesn't reflect the flat-rate subscription.
    """
    receipts_path = workspace_root / ".efterlev" / "receipts.log"
    if not receipts_path.is_file():
        return None
    log = ReceiptLog(receipts_path)
    by_model = _aggregate_by_model(log.read_all(), started_at)
    if not by_model:
        return None

    # v0.1.151 / #356: detect subscription backend from workspace config so
    # we don't multiply ClaudeCodeClient's zero-tokens by Anthropic API
    # rates and print a misleading $0.00 (which reads as "this run was
    # free" when the user might wonder if it ran at all). Tolerant: any
    # config-read failure falls through to the legacy $-based summary.
    is_subscription = False
    try:
        from efterlev.config import load_config

        cfg = load_config(workspace_root / ".efterlev" / "config.toml")
        is_subscription = cfg.llm.backend == "claude_code"
    except Exception:
        pass
    if is_subscription:
        # v0.1.176 / #383: count DISTINCT prompt_hash values since started_at
        # — that's the true LLM-call count. The prior code counted every
        # receipt record (evidence + claims + deterministic outputs), which
        # massively overstated calls: a 60-KSI run reported ~275 "calls" when
        # only ~62 LLM calls happened. Each LLM call has one prompt_hash; a
        # batched gap call writes 5 claims that SHARE that prompt_hash, so
        # counting claim records (or all receipts) over-counts. Distinct
        # non-null prompt_hash since started_at is exact. Records without a
        # prompt_hash (deterministic evidence/inventory/etc.) aren't LLM
        # calls and are correctly excluded.
        prompt_hashes: set[str] = set()
        for e in log.read_all():
            ts_str = e.get("ts")
            ph = e.get("prompt_hash")
            if not ts_str or not ph:
                continue
            try:
                if datetime.fromisoformat(ts_str) >= started_at:
                    prompt_hashes.add(ph)
            except ValueError:
                continue
        call_count = len(prompt_hashes)
        models_str = next(iter(by_model)) if len(by_model) == 1 else " + ".join(sorted(by_model))
        plural = "s" if call_count != 1 else ""
        return (
            f"LLM cost: subscription run (no per-call billing) — "
            f"{call_count} call{plural} to {models_str}"
        )

    total_in = sum(in_tok for in_tok, _ in by_model.values())
    total_out = sum(out_tok for _, out_tok in by_model.values())

    # Compute cost across all models. Sum what we can price; flag if any
    # model in the run is unregistered (the dollar estimate is then
    # partial; surface that honestly in the suffix).
    total_cost = 0.0
    unpriced_models: list[str] = []
    any_bedrock = False
    for model, (in_tok, out_tok) in by_model.items():
        cost = estimate_cost_usd(model, in_tok, out_tok)
        if cost is None:
            unpriced_models.append(model)
        else:
            total_cost += cost
        if is_bedrock_model(model):
            any_bedrock = True

    # Model display: single-model uses the full ID; multi-model uses a
    # short comma-joined form (sonnet/opus stems; doesn't matter much
    # because the receipts.log has the full IDs for any deeper lookup).
    if len(by_model) == 1:
        model_str = next(iter(by_model))
    else:
        model_str = " + ".join(_short_model_name(m) for m in sorted(by_model))

    cost_str: str
    if unpriced_models and not lookup_pricing(next(iter(by_model))):
        # Every model in the run was unregistered — no dollar estimate at all.
        cost_str = f" (pricing for {', '.join(sorted(set(unpriced_models)))} not registered)"
    elif unpriced_models:
        # Mixed: some priced, some not. Surface the partial-estimate caveat.
        cost_str = (
            f" (~${total_cost:.2f}; "
            f"pricing for {', '.join(sorted(set(unpriced_models)))} not registered)"
        )
    else:
        cost_str = f" (~${total_cost:.2f})"

    bedrock_str = " (via bedrock; AWS region pricing may differ)" if any_bedrock else ""

    return (
        f"LLM cost: {total_in:,} in / {total_out:,} out tokens "
        f"on {model_str}{cost_str}{bedrock_str}"
    )


def _short_model_name(model_id: str) -> str:
    """`claude-sonnet-4-6` → `sonnet-4-6`; `us.anthropic.claude-opus-4-7-v1:0`
    → `opus-4-7`. Strips noise from multi-model summary lines."""
    # Strip the bedrock prefix if present.
    if model_id.startswith("us.anthropic."):
        model_id = model_id.removeprefix("us.anthropic.")
    if model_id.startswith("anthropic."):
        model_id = model_id.removeprefix("anthropic.")
    # Strip the `claude-` prefix and the `-v1:0` Bedrock suffix.
    model_id = model_id.removeprefix("claude-")
    if ":" in model_id:
        model_id = model_id.split(":", 1)[0]
    if model_id.endswith("-v1"):
        model_id = model_id.removesuffix("-v1")
    return model_id
