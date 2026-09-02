"""The B4 flip regression net — DB-resolver engine vs the frozen chat param golden.

``tests/fixtures/chat_param_golden/*.json`` freezes, per chat family variant,
what the retired legacy path (api_class + ThinkingConfig param blocks in each
translator) sent for ~900 canonical-config combos, TOGETHER WITH the merged
control rules (ai.api.rules <- ai.offering.override) and ai.setting value
orders in force when the golden was dumped (legacy == catalog held on every
case at dump time — ``scripts/dump_chat_param_golden.py``).

This test rebuilds the ``CompiledControlsMap`` from the fixture's rules — no
database — and asserts ``canonical_settings_from_config -> outbound`` still
reproduces the golden params byte-identically. It guards the ENGINE
(canonicalize / controls / processors). The live DB rules are guarded against
the same fixture by ``scripts/validate_catalog_parity.py`` Section B.

Regenerate the fixture ONLY for a deliberate, reviewed behaviour change:

    uv run python scripts/dump_chat_param_golden.py
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog.canonicalize import canonical_settings_from_config
from matrx_ai.catalog.controls import CompiledControlsMap, flatten_dotted
from matrx_ai.catalog.models import ControlRule

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "chat_param_golden"

_MAX_FAILURES_SHOWN = 10


def load_golden(variant_key: str) -> dict[str, Any]:
    path = FIXTURE_DIR / f"{variant_key}.json"
    return json.loads(path.read_text())


def compiled_from_golden(payload: dict[str, Any]) -> CompiledControlsMap:
    rules = {key: ControlRule.model_validate(rule) for key, rule in payload["rules"].items()}
    return CompiledControlsMap(rules=rules, value_orders=payload["value_orders"])


def _variant_keys() -> list[str]:
    keys = sorted(p.stem for p in FIXTURE_DIR.glob("*.json"))
    assert keys, f"no golden fixtures found under {FIXTURE_DIR}"
    return keys


def outbound_for_case(compiled: CompiledControlsMap, config: dict[str, Any]) -> dict[str, Any]:
    canonical = canonical_settings_from_config(SimpleNamespace(**config))
    canonical.pop("response_format", None)  # structural — owned by the translators
    params, _adjustments = compiled.outbound(canonical)
    return flatten_dotted(params)


@pytest.mark.parametrize("variant_key", _variant_keys())
def test_resolver_reproduces_golden(variant_key: str) -> None:
    payload = load_golden(variant_key)
    compiled = compiled_from_golden(payload)

    failures: list[str] = []
    for case in payload["cases"]:
        got = outbound_for_case(compiled, case["config"])
        expected = case["params"]
        if got != expected:
            failures.append(
                f"config={json.dumps(case['config'], sort_keys=True)}\n"
                f"  golden : {json.dumps(expected, sort_keys=True)}\n"
                f"  engine : {json.dumps(got, sort_keys=True, default=str)}"
            )
    if failures:
        shown = "\n".join(failures[:_MAX_FAILURES_SHOWN])
        pytest.fail(
            f"{variant_key}: {len(failures)}/{len(payload['cases'])} cases diverge "
            f"from the golden (engine vs frozen legacy output):\n{shown}"
        )


def test_golden_covers_expected_families() -> None:
    """The fixture set must never silently shrink — a deleted family fixture
    would take its whole regression net with it."""
    families = {load_golden(k)["family"] for k in _variant_keys()}
    expected = {
        "openai_standard",
        "openai_reasoning_minimal",
        "openai_reasoning",
        "openai_reasoning_xhigh",
        "google_thinking",
        "google_thinking_3",
        "anthropic_standard",
        "anthropic_adaptive",
        "groq_standard",
        "groq_reasoning",
        "groq_reasoning_toggle",
        "cerebras_standard",
        "cerebras_reasoning",
        "cerebras_reasoning_toggle",
        "xai_standard",
        "xai_reasoning",
        "together_text_standard",
        "huggingface_standard",
    }
    missing = expected - families
    assert not missing, f"golden fixtures missing for families: {sorted(missing)}"
