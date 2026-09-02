"""Observability pricing layer with layered configuration.

Provides ``lookup_call_cost()`` — the observability-specific cost lookup
that loads pricing from a state-dir override file or env var, merges with
built-in defaults, and delegates computation to the existing
``CostEstimator`` from ``llm/cost_estimator.py``.
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path
from typing import Any

from agentic_devtools.orchestration.llm.cost_estimator import (
    DEFAULT_PRICING,
    CostEstimator,
    PricingTable,
)
from agentic_devtools.orchestration.llm.types import TokenUsage


def _load_pricing_file(file_path: Path) -> dict[str, dict[str, float]]:
    """Load and validate a pricing override file.

    Returns a dict of model -> {input, output} prices, skipping
    invalid entries with a stderr warning.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        raw = json.loads(content)
    except (OSError, json.JSONDecodeError) as exc:
        print(
            f"[observability] WARNING: Failed to load pricing file {file_path}: {exc}",
            file=sys.stderr,
        )
        return {}

    if not isinstance(raw, dict):
        print(
            f"[observability] WARNING: Pricing file {file_path} is not a JSON object",
            file=sys.stderr,
        )
        return {}

    valid: dict[str, dict[str, float]] = {}
    for model, entry in raw.items():
        if not isinstance(entry, dict):
            print(
                f"[observability] WARNING: Skipping invalid pricing entry for model {model!r}",
                file=sys.stderr,
            )
            continue
        if "input" not in entry or "output" not in entry:
            print(
                f"[observability] WARNING: Skipping incomplete pricing entry for model {model!r}",
                file=sys.stderr,
            )
            continue
        if isinstance(entry["input"], bool) or isinstance(entry["output"], bool):
            print(
                f"[observability] WARNING: Skipping boolean pricing entry for model {model!r}"
                f" (rates must be numeric, not bool)",
                file=sys.stderr,
            )
            continue
        try:
            input_rate = float(entry["input"])
            output_rate = float(entry["output"])
        except (TypeError, ValueError):
            print(
                f"[observability] WARNING: Skipping non-numeric pricing entry for model {model!r}",
                file=sys.stderr,
            )
            continue
        if input_rate < 0 or output_rate < 0:
            print(
                f"[observability] WARNING: Skipping negative pricing entry for model {model!r}"
                f" (input={input_rate}, output={output_rate}); rates must be non-negative USD/1M tokens",
                file=sys.stderr,
            )
            continue
        valid[model] = {"input": input_rate, "output": output_rate}

    return valid


def build_pricing_table(state_dir: str | Path | None = None) -> PricingTable:
    """Build a PricingTable merging defaults with file overrides.

    Resolution order:
    1. ``AGDT_LLM_PRICING_FILE`` env var (highest priority).
    2. ``<state_dir>/observability/pricing.json`` (if state_dir provided).
    3. Built-in ``DEFAULT_PRICING`` as base.

    Invalid files or entries are skipped with stderr warnings; the
    resulting table always includes at least the built-in defaults.
    """
    merged: dict[str, dict[str, float]] = {k: dict(v) for k, v in DEFAULT_PRICING.items()}

    # Try state-dir file
    if state_dir is not None:
        state_pricing = Path(state_dir) / "observability" / "pricing.json"
        if state_pricing.is_file():
            overrides = _load_pricing_file(state_pricing)
            merged.update(overrides)

    # Try env var file (highest priority)
    env_path = os.environ.get("AGDT_LLM_PRICING_FILE")
    if env_path:
        env_file = Path(env_path)
        if env_file.is_file():
            overrides = _load_pricing_file(env_file)
            merged.update(overrides)
        else:
            print(
                f"[observability] WARNING: AGDT_LLM_PRICING_FILE={env_path} does not exist",
                file=sys.stderr,
            )

    return PricingTable(prices=merged)


def coerce_token_count(value: Any) -> int | None:
    """Safely coerce a token count to int.

    Accepts ``int``, ``float``, and numeric strings.  Returns ``None``
    for ``bool`` inputs (bool is a subclass of int but is not a valid
    count), ``None`` inputs, negative values, and any value that cannot
    be converted (including infinity and other overflow-producing floats).
    """
    if value is None:
        return None
    # bool is a subclass of int — treat True/False as invalid counts.
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    # Accept float and string representations (e.g. from parsed JSON).
    # Convert to float first so we can reject negatives and non-finite
    # values (inf / -inf / NaN) before calling int(), which raises
    # OverflowError for infinite floats.
    try:
        as_float = float(value)
    except (TypeError, ValueError):
        return None
    if as_float < 0 or not math.isfinite(as_float):
        # Reject negatives, NaN, positive infinity, and negative infinity.
        # math.isfinite() also guarantees that int() below won't raise
        # OverflowError (only non-finite floats can trigger that).
        return None
    return int(as_float)


def lookup_call_cost(
    model: str,
    input_tokens: int | float | str | None,
    output_tokens: int | float | str | None,
    pricing_table: PricingTable | None = None,
) -> float | None:
    """Look up the estimated cost for an LLM call.

    Returns ``None`` when the model is unpriced or tokens are ``None``
    (never returns ``$0.00`` for missing data).

    Non-int token values (strings, floats) are coerced to int before
    computation so that callers using parsed JSON or provider libraries
    that return floats never cause a crash in the observability pipeline.

    Args:
        model: Provider model identifier.
        input_tokens: Input token count (None if unavailable). Strings
            and floats are coerced; bools and unconvertible values are
            treated as None.
        output_tokens: Output token count (None if unavailable). Same
            coercion rules as ``input_tokens``.
        pricing_table: Optional pre-built pricing table.

    Returns:
        Estimated cost in USD, or None.
    """
    coerced_input = coerce_token_count(input_tokens)
    coerced_output = coerce_token_count(output_tokens)

    if coerced_input is None or coerced_output is None:
        return None

    table = pricing_table or build_pricing_table()
    estimator = CostEstimator(pricing=table)
    usage = TokenUsage(
        input_tokens=coerced_input,
        output_tokens=coerced_output,
        total_tokens=coerced_input + coerced_output,
    )
    return estimator.estimate_cost(model, usage)


def _resolve_pricing_overrides(state_dir: str | Path | None = None) -> dict[str, Any]:
    """Internal: resolve override entries for testing/debugging."""
    overrides: dict[str, Any] = {}
    if state_dir is not None:
        state_pricing = Path(state_dir) / "observability" / "pricing.json"
        if state_pricing.is_file():
            overrides.update(_load_pricing_file(state_pricing))
    env_path = os.environ.get("AGDT_LLM_PRICING_FILE")
    if env_path:
        env_file = Path(env_path)
        if env_file.is_file():
            overrides.update(_load_pricing_file(env_file))
    return overrides
