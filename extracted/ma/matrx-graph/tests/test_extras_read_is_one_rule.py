"""``extras_read``: the ONE rule for which extra inputs a step's input model takes.

The scheduler uses it to decide which declared workflow settings an ENTRY step is handed;
an open model that names its ``in_read_fields`` (Find Records' ``match``) uses it to refuse
any other extra as a misspelled setting. Live defect 2026-10-28: the two disagreed, so Find
Records as a first step was handed every declared setting and refused them all.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from matrx_graph.nodes._template import extras_read, in_names_read


class _Closed(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[int] = []


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _ReadsByName(BaseModel):
    model_config = ConfigDict(extra="allow")
    in_read_fields: ClassVar[tuple[str, ...]] = ("match",)
    match: dict = {}


def test_a_closed_model_takes_no_extra() -> None:
    assert extras_read(_Closed, {"items": [1]}) == set()


def test_an_open_model_that_does_not_say_takes_any_extra() -> None:
    assert extras_read(_Open, {}) is None


def test_a_model_naming_its_read_fields_takes_only_what_they_read() -> None:
    assert extras_read(_ReadsByName, {"match": {"id": "$in.brand_id"}}) == {"brand_id"}
    assert extras_read(_ReadsByName, {"match": {"id": {"$format": "x-{in.kit.id}"}}}) == {"kit"}
    assert extras_read(_ReadsByName, {"match": {"id": {"$input": "brand_id"}}}) == set()
    assert extras_read(_ReadsByName, {}) == set()


def test_reading_the_whole_namespace_takes_any_extra() -> None:
    assert in_names_read({"a": "$in"}) is None
    assert extras_read(_ReadsByName, {"match": {"row": "$in"}}) is None
