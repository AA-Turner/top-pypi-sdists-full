"""Tests for `efterlev.agents.cost_summary` (Tier 1 #2a, v0.1.19).

Covers:
- Single-model run produces the canonical one-line summary with dollars.
- Multi-model run (Opus + Sonnet, e.g. on a fallback) sums correctly and
  uses the short-name comma form.
- Bedrock model gets the "via bedrock; AWS region pricing may differ"
  suffix.
- Unregistered model (future Sonnet 4.7 lands before pricing.py updates)
  falls through to a tokens-only line with a "pricing for X not
  registered" suffix.
- Mixed registered + unregistered run shows partial dollar estimate
  with the partial-pricing caveat.
- Receipts.log entries with ts < started_at are excluded (so this run's
  summary doesn't accidentally include the prior run's spend).
- No receipts.log file (cold workspace) returns None.
- Receipts.log with no LLM-bearing entries (StubLLMClient case) returns
  None — keeps the agent success path clean in tests.

Pricing-table coverage is in test_pricing.py.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from efterlev.agents.cost_summary import summarize_run_cost


def _write_receipt(receipts_path: Path, **fields: object) -> None:
    """Append one JSON line to a receipts.log fixture."""
    receipts_path.parent.mkdir(parents=True, exist_ok=True)
    with receipts_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(fields) + "\n")


def test_returns_none_when_workspace_has_no_receipts_log(tmp_path: Path) -> None:
    """Cold workspace (no `.efterlev/receipts.log` at all) → no summary."""
    started = datetime.now(UTC)
    assert summarize_run_cost(tmp_path, started) is None


def test_returns_none_when_no_llm_entries_in_window(tmp_path: Path) -> None:
    """StubLLMClient case: receipts.log exists but no entries carry
    `model` + `input_tokens` + `output_tokens` (deterministic-only run).
    Returning None keeps the agent success path clean instead of
    printing a pointless `0 tokens` line."""
    receipts = tmp_path / ".efterlev" / "receipts.log"
    started = datetime.now(UTC)
    # An evidence-record write (no model, no token counts).
    _write_receipt(
        receipts,
        ts=(started + timedelta(seconds=1)).isoformat(),
        record_id="sha256:abc",
        record_type="evidence",
        derived_from=[],
        primitive="scan_terraform@0.1.0",
        agent=None,
        model=None,
        prompt_hash=None,
    )
    assert summarize_run_cost(tmp_path, started) is None


def test_single_model_run_produces_dollar_estimate(tmp_path: Path) -> None:
    """Canonical happy path: one agent invoked one model, summary shows
    summed tokens + dollar estimate from the pricing table."""
    receipts = tmp_path / ".efterlev" / "receipts.log"
    started = datetime.now(UTC)
    for in_tok, out_tok in [(10000, 2000), (15000, 3000), (5000, 1000)]:
        _write_receipt(
            receipts,
            ts=(started + timedelta(seconds=1)).isoformat(),
            record_id=f"sha256:{in_tok}",
            record_type="claim",
            derived_from=[],
            primitive=None,
            agent="gap_agent",
            model="claude-sonnet-4-6",
            prompt_hash="sha256:p",
            input_tokens=in_tok,
            output_tokens=out_tok,
        )
    line = summarize_run_cost(tmp_path, started)
    assert line is not None
    # 30,000 in + 6,000 out at $3/MTok in, $15/MTok out =
    #   30000 * 3 / 1e6 + 6000 * 15 / 1e6 = 0.09 + 0.09 = $0.18
    assert "30,000 in / 6,000 out tokens" in line
    assert "claude-sonnet-4-6" in line
    assert "~$0.18" in line


def test_multi_model_run_sums_and_uses_short_names(tmp_path: Path) -> None:
    """Opus + Sonnet (fallback fired mid-run): per-model totals roll up,
    display uses short-name form so the line stays readable."""
    receipts = tmp_path / ".efterlev" / "receipts.log"
    started = datetime.now(UTC)
    _write_receipt(
        receipts,
        ts=(started + timedelta(seconds=1)).isoformat(),
        record_id="sha256:o",
        record_type="claim",
        derived_from=[],
        primitive=None,
        agent="gap_agent",
        model="claude-opus-4-7",
        prompt_hash="sha256:p1",
        input_tokens=20000,
        output_tokens=4000,
    )
    _write_receipt(
        receipts,
        ts=(started + timedelta(seconds=2)).isoformat(),
        record_id="sha256:s",
        record_type="claim",
        derived_from=[],
        primitive=None,
        agent="gap_agent",
        model="claude-sonnet-4-6",
        prompt_hash="sha256:p2",
        input_tokens=10000,
        output_tokens=2000,
    )
    line = summarize_run_cost(tmp_path, started)
    assert line is not None
    # Tokens: 30,000 in / 6,000 out
    assert "30,000 in / 6,000 out" in line
    # Short-name display, alphabetical: opus + sonnet
    assert "opus-4-7 + sonnet-4-6" in line
    # Cost: opus 20000*15 + 4000*75 = 0.30 + 0.30 = 0.60
    #     + sonnet 10000*3 + 2000*15 = 0.03 + 0.03 = 0.06
    #     = 0.66
    assert "~$0.66" in line


def test_bedrock_model_appends_proxy_suffix(tmp_path: Path) -> None:
    """Bedrock-backed runs get a clarifying suffix because AWS pricing
    varies by region; the dollar estimate uses the Anthropic API rate
    as a proxy and we surface that honestly."""
    receipts = tmp_path / ".efterlev" / "receipts.log"
    started = datetime.now(UTC)
    _write_receipt(
        receipts,
        ts=(started + timedelta(seconds=1)).isoformat(),
        record_id="sha256:b",
        record_type="claim",
        derived_from=[],
        primitive=None,
        agent="gap_agent",
        model="us.anthropic.claude-sonnet-4-6-v1:0",
        prompt_hash="sha256:p",
        input_tokens=10000,
        output_tokens=2000,
    )
    line = summarize_run_cost(tmp_path, started)
    assert line is not None
    assert "via bedrock; AWS region pricing may differ" in line
    # Cost still computed (bedrock ID is aliased to Anthropic rate).
    assert "~$0.06" in line


def test_unregistered_model_skips_dollar_estimate(tmp_path: Path) -> None:
    """A future Anthropic model lands in a customer's wheel before
    pricing.py is updated. Surface the tokens, skip the dollar estimate,
    and tell the user which model is unpriced — never crash."""
    receipts = tmp_path / ".efterlev" / "receipts.log"
    started = datetime.now(UTC)
    _write_receipt(
        receipts,
        ts=(started + timedelta(seconds=1)).isoformat(),
        record_id="sha256:f",
        record_type="claim",
        derived_from=[],
        primitive=None,
        agent="gap_agent",
        model="claude-sonnet-4-7-future",
        prompt_hash="sha256:p",
        input_tokens=10000,
        output_tokens=2000,
    )
    line = summarize_run_cost(tmp_path, started)
    assert line is not None
    assert "10,000 in / 2,000 out" in line
    # No dollar estimate for an entirely-unpriced run.
    assert "~$" not in line
    assert "pricing for claude-sonnet-4-7-future not registered" in line


def test_mixed_priced_and_unpriced_models_shows_partial_estimate(tmp_path: Path) -> None:
    """Multi-model run where one model is unregistered: show the
    partial dollar estimate covering the priced models, qualify with
    a note naming the unpriced one."""
    receipts = tmp_path / ".efterlev" / "receipts.log"
    started = datetime.now(UTC)
    _write_receipt(
        receipts,
        ts=(started + timedelta(seconds=1)).isoformat(),
        record_id="sha256:s",
        record_type="claim",
        derived_from=[],
        primitive=None,
        agent="gap_agent",
        model="claude-sonnet-4-6",
        prompt_hash="sha256:p1",
        input_tokens=10000,
        output_tokens=2000,
    )
    _write_receipt(
        receipts,
        ts=(started + timedelta(seconds=2)).isoformat(),
        record_id="sha256:f",
        record_type="claim",
        derived_from=[],
        primitive=None,
        agent="gap_agent",
        model="claude-future-model",
        prompt_hash="sha256:p2",
        input_tokens=5000,
        output_tokens=1000,
    )
    line = summarize_run_cost(tmp_path, started)
    assert line is not None
    # Tokens combined.
    assert "15,000 in / 3,000 out" in line
    # Dollar estimate covers only the priced model (Sonnet: $0.03 + $0.03 = $0.06).
    assert "~$0.06" in line
    # Partial-pricing caveat names the unregistered model.
    assert "pricing for claude-future-model not registered" in line


def test_started_at_filter_excludes_prior_run_entries(tmp_path: Path) -> None:
    """receipts.log accumulates across runs. The summary must include
    only entries with `ts >= started_at` so this run's cost line doesn't
    sweep up the previous run's spend."""
    receipts = tmp_path / ".efterlev" / "receipts.log"
    # Prior run (1 hour ago).
    prior_run = datetime.now(UTC) - timedelta(hours=1)
    _write_receipt(
        receipts,
        ts=prior_run.isoformat(),
        record_id="sha256:old",
        record_type="claim",
        derived_from=[],
        primitive=None,
        agent="gap_agent",
        model="claude-opus-4-7",
        prompt_hash="sha256:p_old",
        input_tokens=99999,  # huge — would dominate if not filtered out
        output_tokens=99999,
    )
    # Current run starts now.
    started = datetime.now(UTC)
    _write_receipt(
        receipts,
        ts=(started + timedelta(seconds=1)).isoformat(),
        record_id="sha256:new",
        record_type="claim",
        derived_from=[],
        primitive=None,
        agent="gap_agent",
        model="claude-sonnet-4-6",
        prompt_hash="sha256:p_new",
        input_tokens=10000,
        output_tokens=2000,
    )
    line = summarize_run_cost(tmp_path, started)
    assert line is not None
    # Only the current-run Sonnet entry shows up.
    assert "10,000 in / 2,000 out" in line
    assert "claude-sonnet-4-6" in line
    assert "claude-opus-4-7" not in line
    # And the dollar estimate matches Sonnet alone, not the giant prior-run total.
    assert "~$0.06" in line


def test_subscription_counts_distinct_prompt_hash_not_receipts(tmp_path: Path) -> None:
    """v0.1.176 / #383: on the claude_code subscription path, the cost line
    reports the TRUE LLM-call count (distinct prompt_hash), not the total
    receipt count. A batched gap call writes 5 claims sharing one
    prompt_hash, and deterministic records (evidence, no prompt_hash)
    aren't calls — the prior code counted all of them, overstating ~5x.
    """
    from efterlev.config import Config, LLMConfig, save_config

    save_config(
        Config(llm=LLMConfig(backend="claude_code", model="claude-sonnet-4-6")),
        tmp_path / ".efterlev" / "config.toml",
    )
    receipts = tmp_path / ".efterlev" / "receipts.log"
    started = datetime.now(UTC)
    # 1 batched gap call -> 5 claims sharing one prompt_hash.
    for i in range(5):
        _write_receipt(
            receipts,
            ts=(started + timedelta(seconds=1)).isoformat(),
            record_id=f"sha256:claim{i}",
            record_type="claim",
            agent="gap_agent",
            model="claude-sonnet-4-6",
            prompt_hash="sha256:batch1",
            input_tokens=1000,
            output_tokens=200,
        )
    # A second distinct LLM call (different prompt_hash).
    _write_receipt(
        receipts,
        ts=(started + timedelta(seconds=2)).isoformat(),
        record_id="sha256:claim5",
        record_type="claim",
        agent="documentation_agent",
        model="claude-sonnet-4-6",
        prompt_hash="sha256:doc1",
        input_tokens=2000,
        output_tokens=400,
    )
    # 3 deterministic records (evidence, no prompt_hash) — NOT LLM calls.
    for i in range(3):
        _write_receipt(
            receipts,
            ts=(started + timedelta(seconds=1)).isoformat(),
            record_id=f"sha256:ev{i}",
            record_type="evidence",
            primitive="scan_terraform@0.1.0",
            model=None,
            prompt_hash=None,
        )
    line = summarize_run_cost(tmp_path, started)
    assert line is not None
    assert "subscription run (no per-call billing)" in line
    # 9 receipts total, but only 2 distinct prompt_hash = 2 true LLM calls.
    assert "2 calls to claude-sonnet-4-6" in line
    assert "9 call" not in line
