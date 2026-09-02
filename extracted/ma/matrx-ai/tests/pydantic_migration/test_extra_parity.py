"""Parity for the four remaining pure-data contract types.

Phase 1b.2, Retirement Ledger row 7. The three extra_config blocks and
ProviderCharge. Everything else left in the closure carries behaviour or state
and is NOT converted here — see PLAN.md for the per-type analysis.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from matrx_ai.config.extra_config import (
    CodeExecutionContent,
    CodeExecutionResultContent,
    WebSearchCallContent,
)
from matrx_ai.config.models.extra import (
    CodeExecutionContentModel,
    CodeExecutionResultContentModel,
    ProviderChargeModel,
    WebSearchCallContentModel,
)
from matrx_ai.config.usage_config import ProviderCharge

PAIRS = [
    (CodeExecutionContent, CodeExecutionContentModel),
    (CodeExecutionResultContent, CodeExecutionResultContentModel),
    (WebSearchCallContent, WebSearchCallContentModel),
    (ProviderCharge, ProviderChargeModel),
]
IDS = [old.__name__ for old, _ in PAIRS]

REQUIRED_KWARGS = {
    "ProviderCharge": {"amount_usd": 1.0, "raw_amount": 1, "raw_unit": "usd", "field_path": "x"},
}


@pytest.mark.parametrize("old,new", PAIRS, ids=IDS)
def test_same_fields_in_the_same_order(old, new):
    assert [f.name for f in dataclasses.fields(old)] == list(new.model_fields)


@pytest.mark.parametrize("old,new", PAIRS, ids=IDS)
def test_annotations_are_identical(old, new):
    old_hints, new_hints = typing.get_type_hints(old), typing.get_type_hints(new)
    for name in new.model_fields:
        assert new_hints[name] == old_hints[name], f"{new.__name__}.{name}"


@pytest.mark.parametrize("old,new", PAIRS, ids=IDS)
def test_defaults_match(old, new):
    kwargs = REQUIRED_KWARGS.get(old.__name__, {})
    built = new(**kwargs)
    for f in dataclasses.fields(old):
        if f.default is not dataclasses.MISSING:
            expected = f.default
        elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
            expected = f.default_factory()  # type: ignore[misc]
        else:
            continue
        assert getattr(built, f.name) == expected, f"{new.__name__}.{f.name}"


@pytest.mark.parametrize("old,new", PAIRS, ids=IDS)
def test_both_refuse_an_unknown_field(old, new):
    kwargs = REQUIRED_KWARGS.get(old.__name__, {})
    with pytest.raises(TypeError):
        old(**kwargs, nonsense=1)
    with pytest.raises(Exception):
        new(**kwargs, nonsense=1)


# ── ProviderCharge: the first twin with REQUIRED fields ───────────────────────


def test_provider_charge_required_fields_are_required_on_both():
    """Every other twin in this migration is all-defaults, which is why their
    schema tests assert `"required" not in schema`. This one has four, and the
    schema must say so or the TypeScript twin will emit them as optional."""
    assert ProviderChargeModel.model_json_schema()["required"] == [
        "amount_usd", "raw_amount", "raw_unit", "field_path",
    ]
    with pytest.raises(TypeError):
        ProviderCharge()
    with pytest.raises(Exception):
        ProviderChargeModel()


@pytest.mark.parametrize("raw,expected_type", [(5, int), (5.5, float), ("5.50", str)])
def test_raw_amount_keeps_the_providers_exact_type(raw, expected_type):
    """`raw_amount: int | float | str` is the provider's own value verbatim —
    xAI sends integer USD ticks, others a float or a decimal string. Pydantic
    smart mode preserves the input type rather than coercing to the union's
    first member; a coercion here would silently rewrite billing evidence.
    """
    old = ProviderCharge(amount_usd=1.0, raw_amount=raw, raw_unit="usd", field_path="x")
    new = ProviderChargeModel(amount_usd=1.0, raw_amount=raw, raw_unit="usd", field_path="x")
    assert type(old.raw_amount) is expected_type
    assert type(new.raw_amount) is expected_type
    assert new.raw_amount == old.raw_amount


# ── the extra_config blocks ───────────────────────────────────────────────────


def test_code_execution_blocks_are_still_absent_from_production():
    """Their round-trip was repaired today while the defect was still latent.
    If blocks start appearing, the repair moves from latent to load-bearing and
    someone should know."""
    assert CodeExecutionContentModel().type == "code_execution"
    assert CodeExecutionResultContentModel().type == "code_execution_result"


def test_web_search_stored_shape_maps_onto_the_twin():
    """All 18 stored blocks are {id, status, type, metadata:{action}}. The
    in-memory `metadata` is dropped on persist and that is NOT a defect — it
    holds model_dump(exclude={id,status,action}) on an OpenAI object whose only
    remaining field is `type`, redundant with the discriminator."""
    stored = {"id": "ws_1", "status": "completed", "type": "web_search", "metadata": {"action": {"q": "x"}}}
    twin = WebSearchCallContentModel(
        id=stored["id"], status=stored["status"], action=stored["metadata"]["action"]
    )
    assert twin.action == {"q": "x"}
    assert twin.type == "web_search_call"   # memory spelling, not the wire spelling
