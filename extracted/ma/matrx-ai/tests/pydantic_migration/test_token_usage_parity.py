"""Parity for `TokenUsage` — the last persisted, billing-relevant contract type.

Phase 1b.2, Retirement Ledger row 8. Converted as its own step because it is the
only remaining sibling that is both persisted and money-adjacent.

TWO COVERAGE LIMITS, STATED UP FRONT because a green suite here is easy to
over-read:

  1. The corpus is 3,460 rows, not 5,473. The other 2,049 (37.4%) were written
     as Python `repr` STRINGS by `_json_safe` before today's fix, and are
     structurally unusable for this field.
  2. `provider_charge` is EXPLICITLY NULL in all 1,474 rows where it appears and
     populated in NONE — so the derivation below has never been observed in
     captured data and a corpus comparison CANNOT catch an error in it. It is
     pinned by direct assertion instead.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from matrx_ai.config.models.usage import TokenUsageModel
from matrx_ai.config.usage_config import TokenUsage

REQUIRED = {"input_tokens": 10, "output_tokens": 5}


def _both(**kwargs):
    return TokenUsage(**REQUIRED, **kwargs), TokenUsageModel(**REQUIRED, **kwargs)


def test_same_fields_in_the_same_order():
    assert [f.name for f in dataclasses.fields(TokenUsage)] == list(TokenUsageModel.model_fields)


def test_annotations_are_identical_except_the_staged_one():
    old, new = typing.get_type_hints(TokenUsage), typing.get_type_hints(TokenUsageModel)
    for name in TokenUsageModel.model_fields:
        if name == "provider_charge":
            continue  # staged Any until ProviderCharge's own row clears
        assert new[name] == old[name], name


def test_defaults_match():
    old, new = _both()
    for f in dataclasses.fields(TokenUsage):
        if f.default is not dataclasses.MISSING:
            expected = f.default
        elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
            expected = f.default_factory()  # type: ignore[misc]
        else:
            continue
        assert getattr(new, f.name) == expected == getattr(old, f.name), f.name


def test_the_two_required_fields_are_required_on_both():
    assert TokenUsageModel.model_json_schema()["required"] == ["input_tokens", "output_tokens"]
    with pytest.raises(TypeError):
        TokenUsage()
    with pytest.raises(Exception):
        TokenUsageModel()


def test_total_tokens_is_identical():
    old, new = _both(cached_input_tokens=2)
    assert old.total_tokens == new.total_tokens == 17


# ── the derivation the corpus cannot vouch for ────────────────────────────────


def test_derivation_fires_identically_for_a_provider_that_reports_a_charge():
    """xAI's integer tick field is the ONLY shape that produces a charge. Every
    mainstream provider returns None, which is why 1,474 stored rows have this
    null and none have a value."""
    old, new = _both(raw_usage={"total_cost": 1234})
    assert old.provider_charge is not None
    assert new.provider_charge is not None
    assert dataclasses.asdict(old.provider_charge) == dataclasses.asdict(new.provider_charge)


@pytest.mark.parametrize(
    "raw_usage",
    [None, {}, {"prompt_tokens": 10, "completion_tokens": 5}, {"input_tokens": 1, "cache_read_input_tokens": 2}],
    ids=["absent", "empty-dict", "openai-shape", "anthropic-shape"],
)
def test_derivation_stays_none_for_everything_else(raw_usage):
    """The empty-dict case is the subtle one: the guard is `and self.raw_usage`,
    TRUTHINESS not `is not None`, so `{}` must NOT trigger a lookup."""
    old, new = _both(raw_usage=raw_usage)
    assert old.provider_charge is None
    assert new.provider_charge is None


def test_an_already_set_charge_is_never_overwritten():
    sentinel = object()
    old, new = _both(raw_usage={"total_cost": 9}, provider_charge=sentinel)
    assert old.provider_charge is sentinel
    assert new.provider_charge is sentinel


def test_raw_usage_accepts_an_explicit_null_because_888_rows_hold_one():
    old, new = _both(raw_usage=None)
    assert old.raw_usage is None and new.raw_usage is None


# ── the corpus shape, and what it cannot cover ────────────────────────────────


def test_the_always_present_eight_round_trip():
    """The eight fields present in all 3,460 usable rows."""
    values = {
        "input_tokens": 100, "output_tokens": 50, "cached_input_tokens": 25,
        "matrx_model_name": "claude-sonnet-5", "provider_model_name": "claude-sonnet-5",
        "api": "anthropic", "response_id": "resp_1", "metadata": {"k": "v"},
    }
    old, new = TokenUsage(**values), TokenUsageModel(**values)
    for name in values:
        assert getattr(new, name) == getattr(old, name)
        assert type(getattr(new, name)) is type(getattr(old, name))


def test_the_cost_methods_are_NOT_ported_yet_and_that_blocks_the_flip():
    """Forcing function against a premature flip. The twin models the shape; the
    catalog-reading behaviour has not moved. Row 8 cannot reach S3 until it
    does, and this test is what makes that concrete rather than a note."""
    not_ported = [
        "calculate_cost", "calculate_catalog_cost", "calculate_cost_breakdown",
        "from_gemini", "from_openai", "from_anthropic", "aggregate_by_model",
    ]
    for name in not_ported:
        assert hasattr(TokenUsage, name), f"{name} vanished from the dataclass"
        assert not hasattr(TokenUsageModel, name), (
            f"{name} was ported — update this list and the row-8 flip criteria"
        )
