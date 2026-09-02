"""response_format_for_kind — kind slug -> strict provider-portable binding.

The kind catalog is DB-backed; tests seed matrx_graph.kinds' process cache
directly so no DB is touched.
"""

from __future__ import annotations

import time

import pytest
from matrx_graph import kinds as kinds_mod
from matrx_graph.kinds import KindEntry, invalidate_kind_catalog_cache

from matrx_ai.kinds import response_format_for_kind


def _seed(slug: str, json_schema) -> None:
    kinds_mod._cache[slug] = (
        time.monotonic(),
        KindEntry(slug=slug, version=1, label=slug, json_schema=json_schema),
    )


@pytest.fixture(autouse=True)
def _clean_cache():
    invalidate_kind_catalog_cache()
    yield
    invalidate_kind_catalog_cache()


async def test_binds_object_kind_with_portable_strict_schema():
    _seed(
        "test_shape",
        {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "count": {"type": "integer", "minimum": 0},
            },
            "required": ["title"],
        },
    )
    rf = await response_format_for_kind("test_shape")
    assert rf is not None and rf.type == "json_schema"
    assert rf.json_schema is not None and rf.json_schema.name == "test_shape"
    assert rf.json_schema.strict is True
    schema = rf.json_schema.schema_.model_dump(by_alias=True, exclude_none=True)
    # Portable pipeline: additionalProperties:false + all-required.
    assert schema["additionalProperties"] is False
    assert schema["required"] == ["__kind", "title", "count"]
    assert next(iter(schema["properties"])) == "__kind"
    assert schema["properties"]["__kind"]["const"] == "test_shape"


async def test_non_object_root_declines_loudly(caplog):
    _seed("test_any", {})
    with caplog.at_level("ERROR"):
        rf = await response_format_for_kind("test_any")
    assert rf is None
    assert any("cannot be made provider-portable" in r.message for r in caplog.records)


async def test_unregistered_kind_returns_none(monkeypatch, caplog):
    async def _none(**_kw):
        return []

    class _Mgr:
        load_items = staticmethod(_none)

    monkeypatch.setattr(kinds_mod, "_manager", lambda: _Mgr())
    with caplog.at_level("ERROR"):
        rf = await response_format_for_kind("ghost_kind")
    assert rf is None
