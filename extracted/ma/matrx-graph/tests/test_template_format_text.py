"""``{"$format": "..."}`` — one text built from values, in every template that shapes items."""

from __future__ import annotations

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._template import TemplatePathMissing, substitute_template


def test_format_builds_a_link_from_the_element_the_inputs_and_the_position() -> None:
    out = substitute_template(
        {"href": {"$format": "/decks/{in.deck.id}/cards/{item.id}?n={index}"}},
        {"id": "c7"},
        index=2,
        extra={"deck": {"id": "d1"}},
    )
    assert out == {"href": "/decks/d1/cards/c7?n=2"}


def test_a_missing_value_fails_instead_of_building_a_broken_link() -> None:
    with pytest.raises(TemplatePathMissing, match="in.saved.deck"):
        substitute_template({"$format": "/decks/{in.saved.deck.0.id}"}, None, extra={"saved": {"deck": []}})
    with pytest.raises(TemplatePathMissing):
        substitute_template({"$format": "/x/{in.id}"}, None, extra={"id": None})


def test_optional_renders_a_missing_value_as_empty_text() -> None:
    assert substitute_template({"$format": "/x/{in.nope}", "optional": True}, None, extra={}) == "/x/"
    assert substitute_template({"$optional": {"$format": "/x/{in.nope}"}, "default": None}, None, extra={}) is None


def test_values_are_url_encoded_only_when_asked() -> None:
    extra = {"q": "a b&c"}
    assert substitute_template({"$format": "/s?q={in.q}"}, None, extra=extra) == "/s?q=a b&c"
    assert substitute_template({"$format": "/s?q={in.q}", "encode": "url"}, None, extra=extra) == "/s?q=a%20b%26c"
    with pytest.raises(ExecutionError):
        substitute_template({"$format": "/s", "encode": "html"}, None, extra=extra)


def test_format_needs_text() -> None:
    with pytest.raises(ExecutionError):
        substitute_template({"$format": 3}, None, extra={})
