"""Every variant the input-surface compiler emits EXISTS in the kind registry.

THE LAW (INPUT-SURFACE.md § Presentation variants + THE-MODEL): the kind
registry is the one home for anything that renders. So the COMPILER conforms to
the registry, never the reverse.

Why this needs a test rather than care: an unregistered variant name does not
fail. It degrades — silently — to the kind's default component, and the form
renders something plausible and wrong. The bakeoff browser proof caught a
3-option ``choice`` field rendering as a free-text textarea, because the
compiler emitted ``choice``/``long_text``/``file`` while the registry seeds
``textarea``/``dropdown``/``radio_list``/``pill_toggle`` on kind ``text``.
Nothing logged; the run form just quietly asked the wrong question.

The seed list is a FIXTURE (``fixtures/kind_registry_variants.json``), not a
live query — matrx-graph is a standalone package and its tests must run against
a bare checkout. Refresh the fixture from the registry when the seeds change;
never edit it to make a test pass.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_graph.types.input_surface import FIELD_TYPE_KINDS, FIELD_TYPE_VARIANTS

_FIXTURE = Path(__file__).parent / "fixtures" / "kind_registry_variants.json"


def _seeded_variants() -> dict[str, list[str]]:
    return json.loads(_FIXTURE.read_text())["variants_by_kind"]


@pytest.mark.parametrize("field_type", sorted(FIELD_TYPE_VARIANTS))
def test_emitted_variant_is_seeded_on_the_kind_it_accompanies(field_type: str) -> None:
    """The pin: a name the compiler can emit must exist ON that field's kind.

    A variant is only meaningful paired with its kind — ``textarea`` is seeded
    on both ``text`` and ``markdown``, and checking the name against a flat
    global set would let a real mispairing through.
    """
    variant = FIELD_TYPE_VARIANTS[field_type]
    if variant is None:
        return  # No variant selected — the kind's default component renders.

    kind = FIELD_TYPE_KINDS[field_type]
    seeded = _seeded_variants().get(kind, [])
    assert variant in seeded, (
        f"field type {field_type!r} compiles to kind {kind!r} and emits variant "
        f"{variant!r}, which the registry does not seed on that kind "
        f"(seeded: {seeded or 'none'}). The input would degrade silently to the "
        f"kind's default component. Fix the COMPILER to a seeded name, or seed "
        f"the variant in the registry first — the registry is the one home for "
        f"anything that renders."
    )


def test_every_field_type_has_both_a_kind_and_a_variant_entry() -> None:
    """The two tables are read together; a type missing from either is a hole."""
    assert set(FIELD_TYPE_VARIANTS) == set(FIELD_TYPE_KINDS)


def test_the_bakeoff_regressions_stay_fixed() -> None:
    """Named pins for the three names the browser proof caught.

    ``file`` emits no variant on purpose: a file field compiles to kind
    ``text``, on which the registry seeds no file variant. Asserting a variant
    that does not exist buys nothing over the honest default.
    """
    assert FIELD_TYPE_VARIANTS["long_text"] == "textarea"
    assert FIELD_TYPE_VARIANTS["choice"] == "dropdown"
    assert FIELD_TYPE_VARIANTS["file"] is None
    # The names that used to ship must not come back under any field type.
    assert not {"long_text", "choice", "file"} & set(FIELD_TYPE_VARIANTS.values())


def test_the_fixture_can_actually_fail() -> None:
    """Falsifiability: prove the check rejects an unregistered name.

    A guard that cannot fail is worse than no guard. This plants a known-bad
    pairing and asserts the same rule the pin uses would reject it.
    """
    seeded = _seeded_variants()
    assert "choice" not in seeded["text"], "the known-bad name is seeded — rewrite this test"
    assert "markdown_editor" not in seeded["text"], "a real mispairing would pass"
    assert "markdown_editor" in seeded["markdown"]


def test_the_several_values_list_pair_is_seeded() -> None:
    """A several-values text input compiles to (string_list, lines): both must be seeded."""
    from matrx_graph.types.input_surface import LIST_KIND, LIST_VARIANT

    assert LIST_VARIANT in _seeded_variants().get(LIST_KIND, [])
