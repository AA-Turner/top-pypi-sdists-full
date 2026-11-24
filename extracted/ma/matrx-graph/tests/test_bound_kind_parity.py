"""PF-4: an ordinary table bound to a registered kind — the Python half of the twin.

``table_kind_binding_of`` / ``bound_kind_value`` must answer every case in
``fixtures/bound_kind_vectors.json`` exactly; the TS twin (``@ai-matrx/records``
``tableKindBindingOf`` / ``boundKindValue``) runs the same file from its own copy, which
``apps/shared/records/scripts/check-matrx-graph-snapshots.mjs`` holds byte-identical to this one.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_graph.kind_fields import bound_kind_value, table_kind_binding_of

VECTORS = json.loads((Path(__file__).parent / "fixtures" / "bound_kind_vectors.json").read_text())


@pytest.mark.parametrize("case", VECTORS["cases"], ids=[c["name"] for c in VECTORS["cases"]])
def test_bound_kind_vectors(case: dict) -> None:
    binding = table_kind_binding_of(case["facts"])
    assert binding == case["binding"]
    if binding is None:
        assert case["expected"] is None
        return
    got = bound_kind_value(
        binding,
        case["document"],
        case["withheld"],
        case["words"],
        linked=case.get("linked"),
        record_id=case.get("record_id"),
    )
    assert got == case["expected"]


def test_link_cases_ask_each_link_field_once_for_a_whole_list() -> None:
    from matrx_graph.kind_fields import bound_link_ids

    case = next(c for c in VECTORS["cases"] if c["name"] == "link_many_joined")
    binding = table_kind_binding_of(case["facts"])
    a, b, c = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb", "cccccccc-cccc-4ccc-8ccc-cccccccccccc"
    docs = [{"client": a}, {"client": [a, b]}, {"client": c}, {"client": None}]
    wanted = bound_link_ids(binding, docs)
    assert wanted == {next(iter(binding["links"].values())): [a, b, c]}  # one key (one ask), de-duplicated
    assert bound_link_ids(binding, docs, ["client"]) == {}  # a withheld column is never asked about


def test_a_field_on_the_linked_record_is_asked_once_per_link_column() -> None:
    """A kind field bound to ``<link> › <field on the linked record>``: every linked id across the rows, once,
    with the linked Table the link points at — read through the store's read door, never a second path."""
    from matrx_graph.kind_fields import bound_through_reads

    case = next(c for c in VECTORS["cases"] if c["name"] == "through_linked_field")
    binding = table_kind_binding_of(case["facts"])
    a, b = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
    docs = [{"door": a}, {"door": [a, b]}, {"door": None}]
    assert bound_through_reads(binding, docs) == {"door": {"table_id": binding["through"]["limit"]["table_id"], "ids": [a, b]}}
    assert bound_through_reads(binding, docs, ["door"]) == {}  # a withheld link is never followed


def test_vectors_cover_bound_unbound_missing_and_withheld() -> None:
    names = {c["name"] for c in VECTORS["cases"]}
    assert {"well_formed", "missing_required_and_empty", "withheld_column", "unbound"} <= names
