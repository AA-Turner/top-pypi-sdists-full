"""Stage-1 foundation tests — the discriminator-as-data law and the wrappers.

These pin the behaviors the whole kinds program stands on (plan of record:
``common-docs/systems/architecture/content-ir/FEATURE.md``): a kind says
what it is inside its own data, nesting is self-describing at every level, the
wire form roundtrips, and the runtime wrappers never blur into their payloads.
"""

from __future__ import annotations

import json
from typing import Annotated, Union

import jsonschema
import pytest
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

from matrx_graph.content_ir.model import KindModel, KindSubModel, is_kind_instance, kind_of
from matrx_graph.content_ir.wrappers import (
    AgentResultWrapper,
    NodeOutcomeWrapper,
    ToolResultWrapper,
)


class WebResult(KindModel, kind="web_result"):
    url: str
    title: str
    snippet: str = ""


class VideoResult(KindModel, kind="video_result"):
    url: str
    duration_s: int | None = None


class Markdown(KindModel, kind="markdown"):
    text: str


class NewsResult(KindModel, kind="news_result"):
    url: str
    title: str


class PlainNested(KindSubModel):
    value: str


class SearchResults(KindModel, kind="search_results"):
    """Sectioned, as the pilot registered it — never one flattened list."""

    query: str
    web: list[WebResult] = []
    news: list[NewsResult] = []


def test_discriminator_is_data_on_the_wire() -> None:
    dumped = WebResult(url="https://example.com", title="Example").model_dump()
    assert dumped["__kind"] == "web_result"
    assert dumped["url"] == "https://example.com"


def test_nesting_is_self_describing_at_every_level() -> None:
    dumped = SearchResults(query="pizza", web=[WebResult(url="https://a", title="A")]).model_dump()
    assert dumped["__kind"] == "search_results"
    assert dumped["web"][0]["__kind"] == "web_result"


def test_wire_form_roundtrips() -> None:
    original = SearchResults(query="q", web=[WebResult(url="https://a", title="A")])
    wire = original.model_dump()
    # A payload that already carries __kind is accepted as-is: nothing to strip.
    assert SearchResults(**wire).model_dump() == wire


def test_plain_nested_structure_accepts_the_marker_and_declares_it() -> None:
    """Closed sub-structures must not reject a marker from another producer."""
    value = PlainNested.model_validate({"__kind": "foreign_shape", "value": "kept"})
    assert value.value == "kept"
    assert "__kind" not in value.model_dump()
    schema = PlainNested.model_json_schema()
    assert schema["properties"]["__kind"]["type"] == "string"
    assert "__kind" not in schema.get("required", [])


def test_declared_fields_survive_strictness() -> None:
    # The bug this pins: redeclaring the discriminator too early in class
    # construction froze a half-built schema, and every real field came back
    # "extra_forbidden".
    assert WebResult(url="u", title="t").url == "u"
    with pytest.raises(ValidationError):
        WebResult(url="u", title="t", bogus=1)  # type: ignore[call-arg]


def test_schema_pins_the_kind() -> None:
    prop = WebResult.model_json_schema()["properties"]["__kind"]
    assert prop["const"] == "web_result"


def test_dump_agrees_with_the_registered_schema_without_ceremony() -> None:
    # THE FORCING FUNCTION: a kind's own dump must validate against the kind's
    # own schema, with no caller remembering ``by_alias=True``. Registered
    # kinds are additionalProperties:false with ``__kind`` declared, so a dump
    # spelled ``kind_`` is rejected by its own contract.
    dumped = WebResult(url="https://example.com", title="Example").model_dump()
    assert "__kind" in dumped and "kind_" not in dumped
    jsonschema.validate(dumped, WebResult.model_json_schema())


def test_a_kind_nested_in_a_plain_model_still_dumps_the_wire_key() -> None:
    # The defect this pins: ``model_dump`` overrides on the base only fire when
    # a caller dumps the KIND directly. A kind nested inside a plain pydantic
    # model (a node's ``output_schema``, the first real KindModel producer) is
    # serialized by pydantic-core, which emitted ``kind_`` and got the payload
    # rejected by the live registry. Fixed by ``serialize_by_alias`` on the
    # base config, which applies at every depth.
    class NodeOutput(BaseModel):
        results: list[WebResult] = Field(default_factory=list)
        count: int = 0

    out = NodeOutput(results=[WebResult(url="https://a", title="A")], count=1)
    assert out.model_dump()["results"][0]["__kind"] == "web_result"
    assert "kind_" not in json.loads(out.model_dump_json())["results"][0]


def test_python_field_names_remain_available_on_request() -> None:
    # The escape hatch stays explicit: opting out is a deliberate argument, not
    # the default a forgetful caller falls into.
    assert "kind_" in WebResult(url="u", title="t").model_dump(by_alias=False)


def test_tagged_union_dispatches_on_kind_for_free() -> None:
    adapter = TypeAdapter(Annotated[Union[WebResult, VideoResult], Field(discriminator="kind_")])
    got = adapter.validate_python({"__kind": "video_result", "url": "https://v"})
    assert isinstance(got, VideoResult)


def test_kind_of_reads_both_halves_of_the_boundary() -> None:
    site = WebResult(url="https://a", title="A")
    assert kind_of(site) == "web_result"
    assert kind_of(site.model_dump()) == "web_result"
    assert kind_of({"a": 1}) is None
    assert is_kind_instance({"a": 1}) is False


def test_node_outcome_carries_context_and_nests_the_payload() -> None:
    outcome = NodeOutcomeWrapper[SearchResults](
        run_id="run-1",
        node_id="search",
        workflow_id="wf-9",
        output_kind="search_results",
        output_kind_ok=True,
        output=SearchResults(query="q", web=[WebResult(url="https://a", title="A")]),
    )
    wire = outcome.model_dump()
    assert wire["__kind"] == "node_outcome"
    assert wire["run_id"] == "run-1"
    # The payload is NESTED and keeps its own identity — never spread onto the
    # wrapper, which is the corruption this whole program exists to undo.
    assert wire["output"]["__kind"] == "search_results"
    assert wire["output"]["web"][0]["__kind"] == "web_result"
    assert outcome.payload_kind() == "search_results"
    assert NodeOutcomeWrapper(**wire).model_dump() == wire


def test_agent_result_simple_case_is_one_element() -> None:
    result = AgentResultWrapper(content=[Markdown(text="Just prose.")])
    assert result.content_kinds() == ["markdown"]
    assert isinstance(result.primary(), Markdown)


def test_agent_result_complex_case_is_the_same_shape() -> None:
    result = AgentResultWrapper(
        content=[
            Markdown(text="Intro"),
            WebResult(url="https://x", title="X"),
            WebResult(url="https://y", title="Y"),
        ]
    )
    assert result.content_kinds() == ["markdown", "web_result", "web_result"]
    # Several instances: no implicit "the" result — routing is explicit.
    assert result.primary() is None
    assert [w.url for w in result.instances_of("web_result")] == ["https://x", "https://y"]


def test_tool_result_wraps_a_typed_payload() -> None:
    wire = ToolResultWrapper(
        tool_name="fetch",
        output_kind="web_result",
        output=WebResult(url="https://t", title="T"),
    ).model_dump()
    assert wire["__kind"] == "tool_result"
    assert wire["output"]["__kind"] == "web_result"


def test_model_copy_cannot_forge_identity() -> None:
    # Round-1 adversarial F9: the discriminator is CLASS identity, not
    # instance data — a copy with update={"kind_": ...} keeps the class slug,
    # so serialization and kind_of() can never disagree.
    site = WebResult(url="https://a", title="A")
    forged = site.model_copy(update={"kind_": "evil", "title": "B"})
    assert forged.title == "B"  # ordinary updates still work
    assert forged.model_dump()["__kind"] == "web_result"
    assert kind_of(forged) == "web_result"
