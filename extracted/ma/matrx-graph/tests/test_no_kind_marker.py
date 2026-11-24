"""A model that is not a kind declares no ``__kind`` (rules 28 + 31), drops a blank on
read and keeps an old row's NAMED value as written (rule 32) — ``NoKindMarker``."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from matrx_graph.content_ir.model import NoKindMarker, no_kind_marker


class _Plain(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, serialize_by_alias=True)

    kind: NoKindMarker = no_kind_marker()
    title: str


def test_an_old_rows_named_kind_parses_and_is_kept_as_written() -> None:
    row = _Plain.model_validate({"__kind": "news_signal", "title": "t"})
    assert row.kind == "news_signal"
    assert row.model_dump(by_alias=True) == {"__kind": "news_signal", "title": "t"}


def test_a_blank_on_read_is_dropped() -> None:
    row = _Plain.model_validate({"__kind": "", "title": "t"})
    assert row.kind is None
    assert row.model_dump(by_alias=True) == {"title": "t"}


def test_nothing_it_writes_claims_a_kind() -> None:
    assert _Plain(title="t").model_dump(by_alias=True) == {"title": "t"}
    assert "__kind" not in _Plain(title="t").model_dump_json(by_alias=True)


def test_its_schema_declares_no_kind_not_even_blank() -> None:
    assert "__kind" not in _Plain.model_json_schema(by_alias=True)["properties"]
