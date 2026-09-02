"""Parity for the fourteen structured-input blocks.

Phase 1b.2, Retirement Ledger row 6. Seven of these are the classes the broken
`UnifiedContent` union was hiding — the ones whose absence made the published
contract closure 26 instead of 33.

READ THE COVERAGE HONESTLY. Only 30 blocks of this family exist in production
(input_notes 12, input_webpage 8, input_table 6, input_task 2, input_workbook 2);
the other NINE types have never been persisted at all. A green suite here is
structural conformance, not evidence about production behaviour — there is
almost none to be evidence about. The types are modelled because the
deserializer can return them and the contract must declare what it can return.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from matrx_ai.config.models.structured_input import (
    STRUCTURED_INPUT_MODEL_MAP,
    StructuredInputBaseModel,
)
from matrx_ai.config.structured_input_config import (
    STRUCTURED_INPUT_TYPE_MAP,
    _StructuredInputBase,
)

WIRE_TYPES = sorted(STRUCTURED_INPUT_TYPE_MAP)
# The five types that exist in chat.message today, with their block counts.
STORED = {"input_notes": 12, "input_webpage": 8, "input_table": 6, "input_task": 2, "input_workbook": 2}


def test_the_two_maps_are_in_lockstep():
    """A new registered input type with no twin fails HERE, rather than
    silently missing one — the same reconciliation that caught the union."""
    assert set(STRUCTURED_INPUT_MODEL_MAP) == set(STRUCTURED_INPUT_TYPE_MAP)
    assert len(STRUCTURED_INPUT_MODEL_MAP) == 14


@pytest.mark.parametrize("wire", WIRE_TYPES)
def test_same_public_fields(wire):
    old, new = STRUCTURED_INPUT_TYPE_MAP[wire], STRUCTURED_INPUT_MODEL_MAP[wire]
    # _editable_tools is init=False on the dataclass and a PrivateAttr on the
    # twin; it is not a public field on either, so it is compared separately.
    old_names = [f.name for f in dataclasses.fields(old) if not f.name.startswith("_")]
    assert sorted(old_names) == sorted(new.model_fields)


@pytest.mark.parametrize("wire", WIRE_TYPES)
def test_defaults_match(wire):
    old, new = STRUCTURED_INPUT_TYPE_MAP[wire], STRUCTURED_INPUT_MODEL_MAP[wire]
    built = new()
    for f in dataclasses.fields(old):
        if f.name.startswith("_"):
            continue
        if f.default is not dataclasses.MISSING:
            expected = f.default
        elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
            expected = f.default_factory()  # type: ignore[misc]
        else:
            continue
        assert getattr(built, f.name) == expected, f"{new.__name__}.{f.name}"


@pytest.mark.parametrize("wire", WIRE_TYPES)
def test_annotations_are_identical(wire):
    old, new = STRUCTURED_INPUT_TYPE_MAP[wire], STRUCTURED_INPUT_MODEL_MAP[wire]
    old_hints, new_hints = typing.get_type_hints(old), typing.get_type_hints(new)
    for name in new.model_fields:
        assert new_hints[name] == old_hints[name], f"{new.__name__}.{name}"


@pytest.mark.parametrize("wire", WIRE_TYPES)
def test_the_discriminator_default_matches_its_registry_key(wire):
    assert STRUCTURED_INPUT_TYPE_MAP[wire]().type == wire
    assert STRUCTURED_INPUT_MODEL_MAP[wire]().type == wire


# ── failure mode 9: the private attribute ─────────────────────────────────────


@pytest.mark.parametrize("wire", WIRE_TYPES)
def test_editable_tools_default_is_preserved_per_subclass(wire):
    old, new = STRUCTURED_INPUT_TYPE_MAP[wire], STRUCTURED_INPUT_MODEL_MAP[wire]
    assert new()._editable_tools == old()._editable_tools


@pytest.mark.parametrize("wire", WIRE_TYPES)
def test_editable_tools_gate_is_identical(wire):
    """Only an EXPLICIT editable=True injects tools; None and False inject
    nothing. The behaviour, not just the constant."""
    old, new = STRUCTURED_INPUT_TYPE_MAP[wire], STRUCTURED_INPUT_MODEL_MAP[wire]
    for editable in (None, False, True):
        assert old(editable=editable).editable_tools() == new(editable=editable).editable_tools()


def test_both_shapes_refuse_the_private_kwarg_LOUDLY():
    """CUTOVER failure mode 9, measured — and it resolves better than predicted.

    The catalogue warned that a private attribute is "silently dropped or
    raises". A bare pydantic model DOES silently drop it: passing
    `_editable_tools=` to a model without `extra="forbid"` returns the default
    and says nothing. But these twins carry `extra="forbid"`, which turns that
    silent drop into a ValidationError — so BOTH shapes refuse loudly, and the
    failure mode is neutralised by a config choice already made for other
    reasons.

    Different exception types (TypeError vs ValidationError) and the same
    contract: a caller cannot set this, and cannot believe they did.
    """
    old = STRUCTURED_INPUT_TYPE_MAP["input_notes"]
    new = STRUCTURED_INPUT_MODEL_MAP["input_notes"]

    with pytest.raises(TypeError):
        old(_editable_tools=frozenset({"hacked"}))
    with pytest.raises(Exception):
        new(_editable_tools=frozenset({"hacked"}))

    # And the per-subclass constant is untouched by the attempt.
    assert new()._editable_tools == frozenset({"note"})


def test_extra_forbid_is_what_makes_that_refusal_loud():
    """Falsification of the line above: drop extra="forbid" and the silent
    drop the catalogue warned about is exactly what you get. This is why the
    config choice is load-bearing rather than cosmetic."""
    from pydantic import BaseModel, ConfigDict, PrivateAttr

    class Permissive(BaseModel):
        model_config = ConfigDict()  # no extra="forbid"
        _editable_tools: frozenset[str] = PrivateAttr(default=frozenset({"note"}))

    built = Permissive(_editable_tools=frozenset({"hacked"}))
    assert built._editable_tools == frozenset({"note"}), (
        "pydantic no longer silently drops a private kwarg — re-check failure mode 9"
    )


def test_private_attr_is_absent_from_the_schema_and_the_dump():
    new = STRUCTURED_INPUT_MODEL_MAP["input_notes"]
    assert "_editable_tools" not in new.model_fields
    assert "_editable_tools" not in new().model_dump()
    assert "_editable_tools" not in new.model_json_schema()["properties"]


# ── coverage, stated rather than implied ──────────────────────────────────────


def test_nine_of_the_fourteen_have_never_been_persisted():
    """Recorded so a green suite is not mistaken for production evidence."""
    never_stored = set(STRUCTURED_INPUT_TYPE_MAP) - set(STORED)
    assert len(never_stored) == 9
    assert sum(STORED.values()) == 30


@pytest.mark.parametrize("wire", sorted(STORED))
def test_the_stored_types_round_trip_through_the_one_deserializer(wire):
    from matrx_ai.config.unified_content import reconstruct_content

    rebuilt = reconstruct_content({"type": wire})
    assert type(rebuilt) is STRUCTURED_INPUT_TYPE_MAP[wire]

    values = {
        f.name: getattr(rebuilt, f.name)
        for f in dataclasses.fields(rebuilt)
        if not f.name.startswith("_")
    }
    twin = STRUCTURED_INPUT_MODEL_MAP[wire](**values)
    for name, expected in values.items():
        assert getattr(twin, name) == expected, name
        assert type(getattr(twin, name)) is type(expected), name


def test_the_base_model_mirrors_the_base_dataclass():
    base_public = sorted(f.name for f in dataclasses.fields(_StructuredInputBase) if not f.name.startswith("_"))
    assert sorted(StructuredInputBaseModel.model_fields) == base_public
