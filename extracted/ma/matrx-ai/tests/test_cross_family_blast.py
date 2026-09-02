"""Cross-family blast net — every family's golden configs fired at every OTHER
family's resolver.

A user (or an agent config, or a model fallback/reroute) can point any saved
settings blob at any model: a config written for an Anthropic budget-thinking
model WILL eventually hit a Groq offering. The per-family golden tests prove
each family handles ITS OWN configs; this test proves each family survives
EVERYONE ELSE'S:

  1. never raises,
  2. never leaks a provider key outside that family's legal wire vocabulary
     (the union of its rules' provider keys / processor outputs — observed
     across its own golden), and
  3. never sends a string value outside the family's observed/mapped value set,
     nor a number outside its clamp bounds.

Compiled maps come from the golden fixtures (no DB), so this runs offline on
every CI pass — the permanent blast net.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_ai.catalog.controls import flatten_dotted

from test_chat_param_golden import (
    FIXTURE_DIR,
    compiled_from_golden,
    load_golden,
    outbound_for_case,
)

_MAX_FAILURES_SHOWN = 8

# Numeric keys where any finite number a source family produced is legal for a
# target family too (token counts / budgets are clamped upstream by providers).
_NUMERIC_KEYS_UNBOUNDED = {
    "max_tokens",
    "max_completion_tokens",
    "max_output_tokens",
    "thinking.budget_tokens",
    "seed",
}


def _variant_keys() -> list[str]:
    return sorted(path.stem for path in FIXTURE_DIR.glob("*.json"))


def _legal_vocabulary(payload: dict[str, Any]) -> tuple[set[str], dict[str, set[Any]]]:
    """(legal provider keys, observed string values per key) for a family —
    from its OWN golden cases plus its rules' declared targets."""
    keys: set[str] = set()
    values: dict[str, set[Any]] = {}
    for case in payload["cases"]:
        for key, value in case["params"].items():
            keys.add(key)
            if isinstance(value, str | bool):
                values.setdefault(key, set()).add(value)
    for canonical_key, rule in payload["rules"].items():
        if rule.get("supported") is False:
            continue
        if rule.get("processor"):
            continue  # processor outputs are covered by the observed cases
        keys.add(rule.get("provider_key") or canonical_key)
        value_map = rule.get("value_map") or {}
        for mapped in value_map.values():
            if mapped is not None:
                values.setdefault(rule.get("provider_key") or canonical_key, set()).add(mapped)
    return keys, values


def _all_source_configs() -> list[dict[str, Any]]:
    seen: set[str] = set()
    configs: list[dict[str, Any]] = []
    for variant in _variant_keys():
        for case in load_golden(variant)["cases"]:
            marker = json.dumps(case["config"], sort_keys=True, default=str)
            if marker in seen:
                continue
            seen.add(marker)
            configs.append(case["config"])
    return configs


@pytest.mark.parametrize("target_variant", _variant_keys())
def test_every_foreign_config_is_safe(target_variant: str) -> None:
    payload = load_golden(target_variant)
    compiled = compiled_from_golden(payload)
    legal_keys, legal_values = _legal_vocabulary(payload)

    failures: list[str] = []
    for config in _all_source_configs():
        try:
            params = outbound_for_case(compiled, config)
        except Exception as exc:  # noqa: BLE001 — the assertion IS "never raises"
            failures.append(f"RAISED {type(exc).__name__}: {exc} for config={config}")
            continue
        flat = flatten_dotted(params) if any(isinstance(v, dict) for v in params.values()) else params
        for key, value in flat.items():
            if key not in legal_keys:
                failures.append(f"LEAK key {key!r}={value!r} for config={config}")
                continue
            if isinstance(value, bool | str):
                allowed = legal_values.get(key)
                if allowed and value not in allowed:
                    failures.append(
                        f"ILLEGAL VALUE {key!r}={value!r} (allowed: {sorted(map(str, allowed))}) "
                        f"for config={config}"
                    )
            elif isinstance(value, int | float) and key not in _NUMERIC_KEYS_UNBOUNDED:
                rule = None
                for canonical_key, candidate in payload["rules"].items():
                    if (candidate.get("provider_key") or canonical_key) == key:
                        rule = candidate
                        break
                clamp = (rule or {}).get("clamp") or {}
                low, high = clamp.get("min"), clamp.get("max")
                if (low is not None and value < low) or (high is not None and value > high):
                    failures.append(
                        f"OUT OF RANGE {key!r}={value!r} (clamp {low}..{high}) for config={config}"
                    )
    if failures:
        pytest.fail(
            f"{target_variant}: {len(failures)} unsafe foreign-config outcomes:\n"
            + "\n".join(failures[:_MAX_FAILURES_SHOWN])
        )
