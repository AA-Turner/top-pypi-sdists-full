"""The agent request builders put the key and only the given fields on the wire.

The api_key travels as a field on the request message — the gRPC carrier the
Agent API reads (there is no metadata auth on this surface). `output_schema`
is a JSON string on the contract, so the builder accepts the natural dict and
encodes it; proto3 cannot distinguish an absent optional from an unset one at
the builder level, so presence is asserted through HasField.
"""

import pytest

from seltz._types import OMIT
from seltz.services.agent_service import (
    _cancel_request,
    _create_request,
    _get_request,
    _list_request,
)


def test_create_carries_query_and_key() -> None:
    request = _create_request("key", "what is pgmq?", OMIT)
    assert request.query == "what is pgmq?"
    assert request.api_key == "key"
    assert not request.HasField("output_schema")


@pytest.mark.parametrize("absent", [OMIT, None])
def test_create_omits_an_absent_output_schema(absent) -> None:
    assert not _create_request("key", "q", absent).HasField("output_schema")


def test_create_encodes_a_dict_output_schema_as_json() -> None:
    request = _create_request("key", "q", {"type": "json_object"})
    assert request.output_schema == '{"type": "json_object"}'


def test_create_encodes_non_ascii_without_escapes() -> None:
    """The schema is customer prose too (descriptions, enum values); it must
    survive as UTF-8, not as \\u escapes."""
    request = _create_request("key", "q", {"type": "json_object", "note": "naïve"})
    assert "naïve" in request.output_schema
    assert "\\u" not in request.output_schema


def test_create_passes_a_string_output_schema_through() -> None:
    request = _create_request("key", "q", '{"type": "text"}')
    assert request.output_schema == '{"type": "text"}'


def test_get_and_cancel_carry_id_and_key() -> None:
    for build in (_get_request, _cancel_request):
        request = build("key", "run_0189")
        assert request.run_id == "run_0189"
        assert request.api_key == "key"


def test_list_sets_paging_fields_only_when_given() -> None:
    bare = _list_request("key", OMIT, OMIT)
    assert bare.api_key == "key"
    assert not bare.HasField("limit")
    assert not bare.HasField("after")

    paged = _list_request("key", 2, "run_0189")
    assert paged.limit == 2
    assert paged.after == "run_0189"
