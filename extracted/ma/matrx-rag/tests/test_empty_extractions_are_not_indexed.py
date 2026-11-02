"""An extraction that found nothing is not searchable content (audit 2026-09-26: 17 empty chunks
of '{"__kind":"rulebook_chunk","rules":[]}' on one scanned PDF)."""

from __future__ import annotations

from matrx_rag.extraction_indexing import payload_is_empty


def test_empty_extractions_are_recognised_in_every_shape() -> None:
    for empty in (
        None, "", {}, [], {"rules": []}, {"__kind": "rulebook_chunk", "rules": []},
        {"__text__": '{"__kind":"rulebook_chunk","rules":[]}'}, {"__text__": '{"__kind": "","rules": []}'},
        {"__text__": "[]"}, [{"rules": []}, {}], {"a": "", "b": None, "c": {"d": []}},
    ):
        assert payload_is_empty(empty), empty


def test_real_content_is_never_called_empty() -> None:
    for real in (
        {"rules": [{"rule": "Always log the call."}]},
        {"__text__": "The patient was seen on Monday."},
        {"__text__": '{"rules":[{"rule":"x"}]}'},
        {"total": 0},
        "{not json but text",
    ):
        assert not payload_is_empty(real), real
