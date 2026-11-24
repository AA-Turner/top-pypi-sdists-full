"""A plain sub-structure carries NO ``__kind`` — never a blank (Content IR rule 31).

``KindSubModel`` used to declare the nested marker ``const ""``; that put a blank
kind on 859 nested definitions across 345 live kind schemas. Now:

1. the schema declares no ``__kind`` on a sub-structure (and a named child kind
   keeps its own ``const``);
2. reading accepts a blank ``"__kind": ""`` and drops it, and keeps a NAMED value
   exactly as written (rule 32: nothing destroys a kind name);
3. removing a live blank marker is backward compatible (the compatibility gate)
   and IS drift (the publisher must see it and write it).
"""

from __future__ import annotations

import copy

import pytest
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import _structurally_equal, compatibility_verdict


class _Part(KindSubModel):
    label: str


class _Named(KindModel, kind="nested_marker_absent_named_child"):
    label: str


class _Whole(KindModel, kind="nested_marker_absent_whole"):
    parts: list[_Part]
    named: _Named | None = None


#: Every blank form stored on live rows on 2026-11-02 (counts from the registry).
LIVE_BLANK_FORMS = (
    {"type": "string", "const": "", "title": "Kind", "default": "",
     "description": "Plain sub-structure: no kind of its own. Always empty."},  # 766
    {"type": "string", "const": "",
     "description": "No registered kind: this position is plain structure. Always empty."},  # 108
    {"type": "string", "const": "", "title": "Kind", "default": "",
     "description": "Not a kind: no kind of its own. Always empty."},  # 8
    {"type": "string", "const": "", "title": "Kind", "default": ""},  # 1
    {"type": "string", "const": ""},  # the bare trigger form
)


def _with_live_marker(schema: dict, form: dict) -> dict:
    old = copy.deepcopy(schema)
    old["$defs"]["_Part"].setdefault("properties", {})["__kind"] = form
    return old


def test_a_sub_structure_schema_declares_no_kind_at_all() -> None:
    schema = _Whole.model_json_schema()
    assert "__kind" not in schema["$defs"]["_Part"]["properties"]
    assert schema["$defs"]["_Named"]["properties"]["__kind"]["const"] == "nested_marker_absent_named_child"
    assert '"const": ""' not in str(schema).replace("'", '"')


def test_a_blank_on_read_is_dropped_and_never_written() -> None:
    part = _Part.model_validate({"__kind": "", "label": "a"})
    assert part.model_dump() == {"label": "a"}
    assert "__kind" not in _Part(label="b").model_dump_json()
    whole = _Whole.model_validate(
        {"__kind": "nested_marker_absent_whole", "parts": [{"__kind": "", "label": "a"}, {"label": "b"}]}
    )
    assert whole.model_dump()["parts"] == [{"label": "a"}, {"label": "b"}]


def test_a_named_marker_is_kept_exactly_as_written() -> None:
    part = _Part.model_validate({"__kind": "grew_from", "label": "a"})
    assert part.model_dump() == {"__kind": "grew_from", "label": "a"}


@pytest.mark.parametrize("form", LIVE_BLANK_FORMS)
def test_removing_a_live_blank_marker_is_backward_compatible(form: dict) -> None:
    new = _Whole.model_json_schema()
    verdict = compatibility_verdict(new, _with_live_marker(new, form))
    assert verdict.compatible, verdict.breaking


@pytest.mark.parametrize("form", LIVE_BLANK_FORMS)
def test_removing_a_live_blank_marker_is_drift_the_publisher_writes(form: dict) -> None:
    """Fails before 2026-11-02: the drift check forgave ``const ""`` as storage noise,
    so a row carrying the bare or description-only blank was 'match' and never
    republished — the blank stayed live forever."""
    new = _Whole.model_json_schema()
    assert not _structurally_equal(new, _with_live_marker(new, form))


@pytest.mark.parametrize(
    "identity_form",
    ({"type": "string", "const": "customer"}, {"type": "string", "enum": ["customer"]}),
)
def test_a_live_identity_marker_is_never_forgiven(identity_form: dict) -> None:
    new = _Whole.model_json_schema()
    verdict = compatibility_verdict(new, _with_live_marker(new, identity_form))
    assert not verdict.compatible
