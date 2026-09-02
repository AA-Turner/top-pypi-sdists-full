"""Unit tests for ``media.stock_image.search`` — schema validation and the
no-API-key error path. Real Unsplash calls live in level2 / on-demand.
"""

from __future__ import annotations

import pytest
from matrx_graph.types.result import Failure, Success
from matrx_scraper.graph_nodes.stock_image_actions import (
    StockImage,
    StockImageSearchInput,
    StockImageSearchOutput,
    _parse_unsplash_item,
    stock_image_search,
)
from pydantic import ValidationError


def test_input_orientation_default_is_any():
    inp = StockImageSearchInput(query="cat")
    assert inp.orientation == "any"


def test_input_per_page_bounds():
    StockImageSearchInput(query="x", per_page=1)
    StockImageSearchInput(query="x", per_page=30)
    with pytest.raises(ValidationError):
        StockImageSearchInput(query="x", per_page=0)
    with pytest.raises(ValidationError):
        StockImageSearchInput(query="x", per_page=31)


def test_input_orientation_must_be_in_literal_set():
    with pytest.raises(ValidationError):
        StockImageSearchInput(query="x", orientation="diagonal")  # type: ignore[arg-type]


def test_stock_image_attribution_defaults():
    img = StockImage(
        url_full="https://full",
        url_regular="https://reg",
        url_thumb="https://thumb",
        source_id="abc",
    )
    assert img.attribution_required is True
    assert img.license == "Unsplash License"
    assert img.source == "unsplash"


def test_parse_unsplash_item_full_shape():
    item = {
        "id": "abc",
        "width": 4000,
        "height": 3000,
        "description": "A cat on a mat",
        "alt_description": None,
        "urls": {
            "raw": "https://r",
            "full": "https://f",
            "regular": "https://reg",
            "thumb": "https://t",
        },
        "user": {"name": "Jane", "links": {"html": "https://unsplash/jane"}},
    }
    img = _parse_unsplash_item(item)
    assert img.url_full == "https://f"
    assert img.url_regular == "https://reg"
    assert img.url_thumb == "https://t"
    assert img.width == 4000
    assert img.photographer_name == "Jane"
    assert img.photographer_url == "https://unsplash/jane"
    assert img.source_id == "abc"


def test_parse_unsplash_item_handles_missing_user_links():
    item = {
        "id": "x",
        "urls": {"full": "f", "regular": "r", "thumb": "t"},
        "user": {"name": "anon"},  # no links
    }
    img = _parse_unsplash_item(item)
    assert img.photographer_name == "anon"
    assert img.photographer_url is None


async def test_search_fails_without_api_key(monkeypatch):
    monkeypatch.delenv("UNSPLASH_ACCESS_KEY", raising=False)
    inputs = StockImageSearchInput(query="cat", api_key=None)
    out = await stock_image_search(None, inputs)  # type: ignore[arg-type]

    assert isinstance(out, Failure)
    assert out.error.code == "search_failed"
    assert "UNSPLASH_ACCESS_KEY" in out.error.message
    assert (out.error.details or {}).get("reason") == "missing_api_key"


async def test_blank_query_degrades_to_empty_success():
    inputs = StockImageSearchInput(query="   ")
    out = await stock_image_search(None, inputs)  # type: ignore[arg-type]

    assert isinstance(out, Success)
    assert isinstance(out.result, StockImageSearchOutput)
    assert out.result.images == []
    assert out.result.query == ""
