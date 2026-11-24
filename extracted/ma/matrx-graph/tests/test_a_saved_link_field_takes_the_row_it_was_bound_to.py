"""``coerce_link_fields`` — the Python twin of TS ``coerceLinkFields`` (``@ai-matrx/records`` kind-fields): a value
bound to a LINK column becomes what the store's write door takes for a link, or is refused naming the field.
The fixture is the live Field documents of Harbor Lane's "Client replies" table (PF-BB walk)."""

from __future__ import annotations

import pytest

from matrx_graph.kind_fields import LinkFieldRefused, coerce_link_fields

FIELDS = [
    {"key": "title", "label": "Title", "type": "text", "config": {}},
    {"key": "client", "label": "Client", "type": "relation", "relation_max": 1, "config": {}},
    {"key": "request", "label": "Request", "type": "relation", "relation_max": 1, "config": {}},
]
ROW = "51781b52-1a2d-4906-86d3-ffed27f5956d"
CLIENT = "10e76da1-d586-46cc-8c5f-c6dd80758818"


def test_every_link_shape_becomes_ids_and_empties_stay() -> None:
    address = {"__kind": "relation", "token": "record", "_record_id": ROW, "table_id": "e5f3de01-b457-4608-894f-2a8e88d48cb9"}
    assert coerce_link_fields(FIELDS, {"request": address, "client": CLIENT}) == {"request": ROW, "client": CLIENT}
    assert coerce_link_fields(FIELDS, {"client": [CLIENT]}) == {"client": [CLIENT]}
    assert coerce_link_fields(FIELDS, {"client": [{"id": CLIENT}]}) == {"client": [CLIENT]}
    assert coerce_link_fields(FIELDS, {"client": {"__kind": "relation", "token": "record", "id": CLIENT}}) == {"client": CLIENT}
    assert coerce_link_fields(FIELDS, {"client": None}) == {"client": None}
    assert coerce_link_fields(FIELDS, {"client": []}) == {"client": []}


def test_a_value_naming_no_record_is_refused_and_text_is_untouched() -> None:
    with pytest.raises(LinkFieldRefused) as refused:
        coerce_link_fields(FIELDS, {"client": "Linked record"})
    assert str(refused.value) == 'Client links to a record, and it was given "Linked record", which is not a record. Nothing was saved.'
    with pytest.raises(LinkFieldRefused, match="^Request links to a record"):
        coerce_link_fields(FIELDS, {"request": {"label": "x"}})
    assert coerce_link_fields(FIELDS, {"title": {"_record_id": CLIENT}}) == {"title": {"_record_id": CLIENT}}


def test_an_entity_reference_relation_is_left_as_given() -> None:
    fields = [{"key": "owner", "label": "Owner", "type": "relation", "config": {"allowed_types": ["user"]}}]
    assert coerce_link_fields(fields, {"owner": {"token": "user", "id": CLIENT}}) == {"owner": {"token": "user", "id": CLIENT}}
