"""Authoring-time model lifecycle: a deprecated id that declares a successor is
RESOLVED, never refused.

Live defect 2026-09-12 (Masterwork Conductor, conversation 2546a1d2): the agent
builder authored Gemini 3.7 Flash (`is_deprecated`, `successor_id` = Gemini 3.8
Flash) and the birth gate refused the whole build — "selected unavailable
model_id=…" — while the replacement sat declared in the catalog. Call time is
unchanged (deprecated still runs, never substituted); only a WRITE of a new
reference resolves.
"""

from __future__ import annotations

import pytest

from matrx_ai.catalog.lifecycle import (
    ModelNotAuthorableError,
    resolve_authoring_model_id,
)

DEPRECATED = "d9a88a0a-b1f5-4676-a1d5-3e38003edf6e"  # gemini-3.7-flash, live shape
SUCCESSOR = "b32f2079-4fa5-4613-a01d-726f1243ebe5"  # gemini-3.8-flash


def _states(*rows: dict) -> dict[str, dict]:
    return {r["id"]: r for r in rows}


def _model(model_id: str, **over) -> dict:
    row = {
        "id": model_id,
        "name": model_id,
        "common_name": model_id,
        "is_deprecated": False,
        "is_primary": True,
        "retired_at": None,
        "successor_id": None,
        "provider_id": "google",
        "capabilities": {"output": ["text"]},
    }
    row.update(over)
    return row


def test_live_model_resolves_to_itself_with_no_note() -> None:
    states = _states(_model(SUCCESSOR))
    r = resolve_authoring_model_id(SUCCESSOR, states)
    assert r.model_id == SUCCESSOR
    assert r.substituted is False
    assert r.note == ""


def test_deprecated_with_successor_resolves_to_the_successor() -> None:
    states = _states(
        _model(DEPRECATED, is_deprecated=True, is_primary=False, successor_id=SUCCESSOR),
        _model(SUCCESSOR),
    )
    r = resolve_authoring_model_id(DEPRECATED, states)
    assert r.model_id == SUCCESSOR
    assert r.substituted is True
    assert r.chain == (DEPRECATED, SUCCESSOR)
    assert SUCCESSOR in r.note and "deprecated" in r.note


def test_retired_model_follows_the_chain_through_a_deprecated_middle() -> None:
    states = _states(
        _model("a", retired_at="2026-01-01", is_primary=False, successor_id="b"),
        _model("b", is_deprecated=True, is_primary=False, successor_id="c"),
        _model("c"),
    )
    r = resolve_authoring_model_id("a", states)
    assert r.model_id == "c"
    assert r.chain == ("a", "b", "c")
    assert "retired" in r.note


def test_deprecated_without_successor_is_refused_loudly() -> None:
    states = _states(_model("a", is_deprecated=True, is_primary=False))
    with pytest.raises(ModelNotAuthorableError, match="names no successor_id"):
        resolve_authoring_model_id("a", states)


def test_successor_cycle_is_refused_rather_than_looping() -> None:
    states = _states(
        _model("a", is_deprecated=True, is_primary=False, successor_id="b"),
        _model("b", is_deprecated=True, is_primary=False, successor_id="a"),
    )
    with pytest.raises(ModelNotAuthorableError, match="cycles"):
        resolve_authoring_model_id("a", states)


def test_chain_longer_than_the_hop_limit_is_refused() -> None:
    rows = [
        _model(str(i), is_deprecated=True, is_primary=False, successor_id=str(i + 1))
        for i in range(8)
    ]
    rows.append(_model("8"))
    with pytest.raises(ModelNotAuthorableError, match="longer than"):
        resolve_authoring_model_id("0", _states(*rows))


def test_unknown_and_empty_ids_are_refused() -> None:
    with pytest.raises(ModelNotAuthorableError, match="not in the live model catalog"):
        resolve_authoring_model_id("nope", _states(_model("a")))
    with pytest.raises(ModelNotAuthorableError, match="no model_id"):
        resolve_authoring_model_id("", _states(_model("a")))


def test_successor_pointing_outside_the_catalog_is_refused() -> None:
    states = _states(_model("a", is_deprecated=True, is_primary=False, successor_id="ghost"))
    with pytest.raises(ModelNotAuthorableError, match="not in the live model catalog"):
        resolve_authoring_model_id("a", states)
