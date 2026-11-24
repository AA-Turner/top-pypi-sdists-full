"""Content-IR rule 31: the block detector REPORTS a blank ``__kind`` and keeps its answer."""

from __future__ import annotations

import logging

import pytest
from matrx_graph.content_ir.blank_kind import reset_blank_kind_reports

from matrx_ai.processing.blocks.block_detector import (
    _embedded_kind_json_regions,
    root_kind_declaration,
)


@pytest.fixture(autouse=True)
def _fresh() -> None:
    reset_blank_kind_reports()


def test_blank_root_kind_is_reported_and_still_none(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR):
        assert root_kind_declaration('{"__kind": "", "a": 1}') is None
    assert any("content-ir rule 31" in r.getMessage() for r in caplog.records)


def test_blank_embedded_kind_is_reported_and_not_a_region(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR):
        assert _embedded_kind_json_regions('text {"__kind": "", "a": 1} text') == []
    assert any("content-ir rule 31" in r.getMessage() for r in caplog.records)


def test_named_kind_and_absent_key_are_silent(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR):
        assert root_kind_declaration('{"__kind": "report", "a": 1}') == "report"
        assert root_kind_declaration('{"a": 1}') is None
        assert len(_embedded_kind_json_regions('x {"__kind": "report"} y')) == 1
        assert _embedded_kind_json_regions('x {"a": 1} y') == []
    assert caplog.records == []
