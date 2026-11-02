"""A model that is not a kind keeps reading rows that still carry an invented ``__kind``
and never writes one (Content IR rule 28) — ``NoKindMarker`` / ``no_kind_marker()``."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from matrx_graph.content_ir.model import NON_IDENTITY_KIND, NoKindMarker, no_kind_marker


class _Plain(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)

    kind: NoKindMarker = no_kind_marker()
    title: str


def test_an_old_rows_invented_kind_parses_and_reads_as_no_kind() -> None:
    row = _Plain.model_validate({"__kind": "news_signal", "title": "t"})
    assert row.kind == NON_IDENTITY_KIND


def test_nothing_it_writes_claims_a_kind() -> None:
    assert _Plain(title="t").model_dump(by_alias=True) == {"title": "t"}
    assert "__kind" not in _Plain(title="t").model_dump_json(by_alias=True)


def test_its_schema_never_offers_a_kind_to_fill() -> None:
    marker = _Plain.model_json_schema(by_alias=True)["properties"]["__kind"]
    assert marker["const"] == NON_IDENTITY_KIND
