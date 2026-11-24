"""A step's node_started record never re-serializes an argument delivered unchanged.

L-SPEED 6e part 2 (2026-11-10): every step of the research pick child spent ~20 ms (0.45 s per child live) in
``_parse_step_inputs`` — mostly ``model_dump(mode="json")`` of the 900 KB ``items`` list, a copy that
``_share_delivered`` then compared to the delivered list and threw away. An argument whose parsed value equals the
delivered object is now recorded AS the delivered object and left out of the dump.

Red before: ``model_dump`` was asked to serialize ``items`` (no ``exclude``), and the record was a copy until the
comparison swapped it.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, JsonValue

from matrx_graph.executor.scheduler import _parse_step_inputs


class _In(BaseModel):
    items: list[JsonValue]
    label: str = ""
    model_config = ConfigDict(extra="allow")


def _rows() -> list[dict[str, Any]]:
    return [{"id": i, "body": "x" * 40, "tags": ["a", "b"]} for i in range(100)]


def test_an_argument_delivered_unchanged_is_never_dumped(monkeypatch) -> None:
    excluded: list[Any] = []
    real = BaseModel.model_dump

    def spy(self, *args, **kwargs):
        excluded.append(kwargs.get("exclude"))
        return real(self, *args, **kwargs)

    monkeypatch.setattr(_In, "model_dump", spy)
    rows = _rows()
    extra = {"k": 1}
    delivered = {"items": rows, "more": extra}
    merged = {"items": [dict(r) for r in rows], "label": "x", "more": dict(extra)}  # the gate's copy
    model, error, record = _parse_step_inputs(_In, merged, "test", delivered)
    assert error is None and model is not None
    assert record["items"] is rows and record["more"] is extra, "the record is the delivered object itself"
    assert excluded and all(e and "items" in e for e in excluded), (
        f"model_dump serialized the delivered list again (exclude={excluded})"
    )
    assert list(record) == ["items", "label", "more"] and record["label"] == "x"


def test_a_changed_argument_is_dumped_as_before() -> None:
    rows = _rows()
    merged = {"items": [*rows[:-1]], "label": "x"}  # not what was delivered
    _model, _error, record = _parse_step_inputs(_In, merged, "test", {"items": rows})
    assert record["items"] == rows[:-1] and record["items"] is not rows
