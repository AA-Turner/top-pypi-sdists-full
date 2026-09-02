"""A context item supplied by SEVERAL active scopes must survive whole.

`variables` is keyed by the bare item key and `cell_values` by context_item_id, but
neither of those names a concrete cell: a concrete cell is (context_item_id, scope_id).
A conversation attached to two Client scopes has two `primary_contact` cells, and two
scope types can both define `status`. These tests hold the line that nothing is dropped
and that the model is shown WHOSE value each one is.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.context_engine import (
    LEGACY_CONTEXT_CELL_SHAPE_ERROR_KIND,
    AgentContext,
    _apply_ambient,
    _normalize_cell_values,
)

ITEM_A = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"


def _cell(**kw: Any) -> dict[str, Any]:
    base = {"key": "primary_contact", "value": "x", "type": "string", "source": "scope:Acme"}
    base.update(kw)
    return base


def _ctx(direct: dict[str, Any]) -> AgentContext:
    return AgentContext(
        scope={"organization_id": "org-1"},
        scope_labels={},
        direct_variables=direct,
        tool_variables={},
        searchable_variables={},
    )


def test_two_scopes_both_appear_in_the_prompt_block_with_their_scope_names():
    block = _ctx(
        {
            "primary_contact": {
                "value": "David Okafor",
                "source": "scope:Golden State Indemnity Co.",
                "cells": [
                    _cell(value="David Okafor", scope_name="Golden State Indemnity Co."),
                    _cell(value="Janet Cole", scope_name="CSV Pharmacy, Inc."),
                ],
            }
        }
    ).build_system_prompt_block()

    # Neither client may be dropped, and each must be attributable.
    assert "David Okafor" in block
    assert "Janet Cole" in block
    assert "primary_contact [Golden State Indemnity Co.]" in block
    assert "primary_contact [CSV Pharmacy, Inc.]" in block


def test_single_scope_keeps_the_compact_one_line_form():
    block = _ctx(
        {
            "primary_contact": {
                "value": "David Okafor",
                "source": "scope:Acme",
                "cells": [_cell(value="David Okafor", scope_name="Acme")],
            }
        }
    ).build_system_prompt_block()
    assert "primary_contact: David Okafor  [scope:Acme]" in block
    assert "primary_contact [" not in block


def test_two_scopes_of_a_type_render_as_a_scope_label_list():
    block = AgentContext(
        scope={"organization_id": "org-1"},
        scope_labels={"client": ["CSV Pharmacy, Inc.", "Golden State Indemnity Co."]},
        direct_variables={},
        tool_variables={},
        searchable_variables={},
    ).build_system_prompt_block()
    assert "client: CSV Pharmacy, Inc., Golden State Indemnity Co." in block


def test_ambient_refresh_reaches_every_cell_not_just_the_scalar():
    variables = {
        "current_year": {
            "value": "STALE",
            "source": "system",
            "cells": [_cell(key="current_year", value="STALE", source="system")],
        }
    }
    cell_values = {ITEM_A: [_cell(key="current_year", value="STALE", source="system")]}
    _apply_ambient("user-1", variables, cell_values)
    assert variables["current_year"]["value"] != "STALE"
    assert variables["current_year"]["cells"][0]["value"] != "STALE"
    assert cell_values[ITEM_A][0]["value"] != "STALE"


def test_ambient_never_clobbers_a_scope_item_that_shares_a_reserved_key():
    variables = {
        "current_year": {
            "value": "the client's own value",
            "source": "scope:Acme",
            "cells": [_cell(key="current_year", value="the client's own value")],
        }
    }
    _apply_ambient("user-1", variables, {})
    assert variables["current_year"]["value"] == "the client's own value"


async def test_a_single_dict_cell_from_the_old_rpc_creates_structured_error(monkeypatch, caplog):
    """The pre-migration shape logs loudly and enters the structured repair queue."""
    captures: list[tuple[BaseException, dict[str, Any]]] = []

    async def fake_capture_error(exc: BaseException, **fields: Any) -> None:
        captures.append((exc, fields))

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error",
        fake_capture_error,
    )
    with caplog.at_level("ERROR"):
        cells_by_item = await _normalize_cell_values({ITEM_A: _cell()})
    cells = cells_by_item[ITEM_A]
    assert len(cells) == 1
    assert any("legacy single-cell values" in r.message for r in caplog.records)
    assert len(captures) == 1
    assert captures[0][1]["kind"] == LEGACY_CONTEXT_CELL_SHAPE_ERROR_KIND
    assert captures[0][1]["error_type"] == "LegacyContextCellShape"
    assert captures[0][1]["context"] == {
        "affected_item_count": 1,
        "required_migration": "ctx_resolve_full_context_lossless_cells_per_scope",
    }
