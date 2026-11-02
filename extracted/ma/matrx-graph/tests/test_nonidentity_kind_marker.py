"""A plain sub-structure's ``__kind`` is ``const ""`` — pinned, read leniently, evolvable.

KindSubModel used to declare the nested marker as a free string, and agents
bound to the schema wrote junk there. The pin must (1) appear in the schema,
(2) never refuse an old value on read, and (3) pass the compatibility gate
against every live declaration it replaces.
"""

from __future__ import annotations

import copy

import pytest
from matrx_graph.content_ir.markers import normalize_nonidentity_markers
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import compatibility_verdict


class _Part(KindSubModel):
    label: str


class _Named(KindModel, kind="nonidentity_marker_named_child"):
    label: str


class _Whole(KindModel, kind="nonidentity_marker_whole"):
    parts: list[_Part]
    named: _Named | None = None


LIVE_FORMS = (
    {"type": "string"},  # the registry write trigger's stamp
    {"type": "string", "title": "Kind", "default": ""},  # the old KindSubModel
    {"anyOf": [{"type": "string"}, {"type": "null"}], "default": None},  # agent_factory._Strict
)


def _with_live_marker(schema: dict, form: dict) -> dict:
    old = copy.deepcopy(schema)
    for definition in old["$defs"].values():
        marker = definition.get("properties", {}).get("__kind")
        if isinstance(marker, dict) and marker.get("const") == "":
            definition["properties"]["__kind"] = form
    return old


def test_schema_pins_the_empty_marker() -> None:
    marker = _Whole.model_json_schema()["$defs"]["_Part"]["properties"]["__kind"]
    assert marker["const"] == "" and marker["type"] == "string"


@pytest.mark.parametrize("form", LIVE_FORMS)
def test_pinning_is_backward_compatible_against_every_live_form(form: dict) -> None:
    new = _Whole.model_json_schema()
    verdict = compatibility_verdict(new, _with_live_marker(new, form))
    assert verdict.compatible, verdict.breaking


@pytest.mark.parametrize(
    "identity_form",
    (
        {"type": "string", "const": "customer"},
        {"type": "string", "enum": ["customer"]},
    ),
)
def test_pinning_never_forgives_a_live_identity_marker(identity_form: dict) -> None:
    new = _Whole.model_json_schema()
    verdict = compatibility_verdict(new, _with_live_marker(new, identity_form))
    assert not verdict.compatible
    assert verdict.breaking == ("changes the type/constraints of field 'parts'",)


def test_normalize_sets_junk_to_empty_and_leaves_identity_alone() -> None:
    schema = _Whole.model_json_schema()
    value = {
        "__kind": "nonidentity_marker_whole",
        "parts": [{"__kind": "grew_from", "label": "a"}, {"label": "b"}, {"__kind": None, "label": "c"}],
        "named": {"__kind": "nonidentity_marker_named_child", "label": "n"},
    }
    out = normalize_nonidentity_markers(value, schema)
    assert [p.get("__kind", "<absent>") for p in out["parts"]] == ["", "<absent>", ""]
    assert out["named"]["__kind"] == "nonidentity_marker_named_child"
    assert out["__kind"] == "nonidentity_marker_whole"
    assert value["parts"][0]["__kind"] == "grew_from"  # pure
    assert normalize_nonidentity_markers(out, schema) == out  # idempotent
