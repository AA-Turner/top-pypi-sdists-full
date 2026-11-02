"""Compile-time kind resolution — a bad binding fails at SAVE (plan §10d-B4).

These drive the REAL resolver against a fake ``kind_definition_manager``
registered through the package's own DI seam, so what is proven is the whole
path — declaration walk → catalog resolution → verdict — not a stubbed answer.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph.content_ir.authoring_gate import (
    authored_kind_bindings,
    resolve_authored_kinds,
)
from matrx_graph.db import _registry
from matrx_graph.kinds import KindDegradedReason, invalidate_kind_catalog_cache
from matrx_graph.types.definition import Definition


class _Row:
    """The subset of a ``content_ir.kind_definition`` row resolution reads."""

    def __init__(self, slug: str, *, is_active: bool = True, schema: dict | None = None) -> None:
        self.id = f"id-{slug}"
        self.kind = slug
        self.version = 1
        self.label = slug
        self.is_active = is_active
        self.emitted_json_schema = (
            schema if schema is not None else {"type": "object", "properties": {}}
        )
        self.deleted_at = None
        self.published_to_web = True


class _FakeCatalog:
    def __init__(self, rows: dict[str, _Row]) -> None:
        self._rows = rows

    async def load_items(self, **filters: Any) -> list[_Row]:
        slug = filters.get("kind")
        row = self._rows.get(slug) if slug else None
        return [row] if row is not None else []


@pytest.fixture(autouse=True)
def _catalog():
    invalidate_kind_catalog_cache()
    rows = {
        "web_result": _Row("web_result"),
        "retired_shape": _Row("retired_shape", is_active=False),
        "broken_shape": _Row("broken_shape", schema={"type": 12}),
    }
    # Snapshot the DI seam so a test that deliberately breaks it (the outage and
    # programmer-error pins below) cannot leak that state into any LATER test
    # file. Without this restore, the next suite to resolve a kind sees an
    # unregistered manager and degrades — which is how this file silently broke
    # `judge/test_self_validating_news_e2e.py`.
    _previous = dict(_registry._instances)
    _registry.configure_db(
        instances={
            "kind_definition_manager": _FakeCatalog(rows),
            "kind_edge_manager": _FakeCatalog({}),
        }
    )
    yield
    _registry._instances.clear()
    _registry._instances.update(_previous)
    invalidate_kind_catalog_cache()


def _definition(node_data: dict[str, Any], edges: list[dict[str, Any]] | None = None) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n1",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"label": "Shape It", **node_data},
                }
            ],
            "edges": edges or [],
        }
    )


# --- what counts as an authored binding ------------------------------------


def test_only_human_authored_bindings_are_collected() -> None:
    definition = _definition({"input_kind": "web_result", "output_kind": " web_result "})
    bindings = authored_kind_bindings(definition)
    assert {(b.field, b.kind) for b in bindings} == {
        ("input_kind", "web_result"),
        ("output_kind", "web_result"),
    }
    assert all(b.node_id == "n1" and b.label == "Shape It" for b in bindings)


def test_a_definition_with_no_kind_bindings_costs_nothing() -> None:
    assert authored_kind_bindings(_definition({})) == []


# --- the verdicts -----------------------------------------------------------


@pytest.mark.asyncio
async def test_a_registered_active_kind_is_clean() -> None:
    assert await resolve_authored_kinds(_definition({"output_kind": "web_result"})) == []


@pytest.mark.asyncio
async def test_a_typod_slug_blocks_and_names_the_node() -> None:
    problems = await resolve_authored_kinds(_definition({"output_kind": "web_reslut"}))
    assert [p.reason for p in problems] == [KindDegradedReason.KIND_NOT_REGISTERED]
    assert problems[0].blocking is True
    assert "Shape It" in problems[0].message
    assert "web_reslut" in problems[0].message


@pytest.mark.asyncio
async def test_an_inactive_kind_blocks() -> None:
    problems = await resolve_authored_kinds(_definition({"input_kind": "retired_shape"}))
    assert [p.reason for p in problems] == [KindDegradedReason.KIND_INACTIVE]
    assert problems[0].blocking is True


@pytest.mark.asyncio
async def test_a_broken_registration_is_advisory_not_the_authors_fault() -> None:
    problems = await resolve_authored_kinds(_definition({"output_kind": "broken_shape"}))
    assert [p.reason for p in problems] == [KindDegradedReason.SCHEMA_INVALID]
    assert problems[0].blocking is False
    assert "platform defect" in problems[0].message


@pytest.mark.asyncio
async def test_an_unreachable_catalog_never_blocks_an_author() -> None:
    """A REAL outage — the manager is wired, its query cannot reach the database.

    Emptying the DI seam is NOT an outage: it raises ``AttributeError``, which is
    a programmer error, and THE STRICTNESS LAW clause 6 deliberately refuses to
    let bad code hide behind ``catalog_unreachable``. So the fake here is
    faithful to the only shape a real outage takes: a registered manager whose
    load raises a connection error."""

    class _UnreachableManager:
        async def load_items(self, **_kwargs: object) -> list[object]:
            raise ConnectionError("could not connect to the kind catalog")

    invalidate_kind_catalog_cache()
    _registry._instances["kind_definition_manager"] = _UnreachableManager()
    problems = await resolve_authored_kinds(_definition({"output_kind": "web_result"}))
    assert [p.reason for p in problems] == [KindDegradedReason.CATALOG_UNREACHABLE]
    assert problems[0].blocking is False


@pytest.mark.asyncio
async def test_a_programmer_error_never_masquerades_as_an_outage() -> None:
    """The other half of clause 6, pinned: bad code must NOT reach the advisory
    path. An empty DI seam raises ``AttributeError`` and must surface as a
    RuntimeError naming the defect, never as ``catalog_unreachable``."""
    invalidate_kind_catalog_cache()
    _registry._instances["kind_definition_manager"] = None
    with pytest.raises(RuntimeError, match="DEFECT IN THIS CODE"):
        await resolve_authored_kinds(_definition({"output_kind": "web_result"}))


@pytest.mark.asyncio
async def test_an_edge_kind_filter_is_a_boundary_too() -> None:
    definition = Definition.model_validate(
        {
            "nodes": [
                {"id": "a", "type": "io.user_input", "position": {"x": 0, "y": 0}, "data": {}},
                {"id": "b", "type": "data.transform", "position": {"x": 1, "y": 0}, "data": {}},
            ],
            "edges": [
                {
                    "id": "e1",
                    "source": "a",
                    "target": "b",
                    "data": {"kind": "data", "kind_filter": "ghost_kind"},
                }
            ],
        }
    )
    problems = await resolve_authored_kinds(definition)
    assert [(p.binding.field, p.binding.edge_id) for p in problems] == [("kind_filter", "e1")]
    assert problems[0].blocking is True
