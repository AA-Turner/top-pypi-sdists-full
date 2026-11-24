"""Content-IR rule 31: a blank ``__kind`` is reported (ERROR log), never silent."""

from __future__ import annotations

import logging

import pytest

from matrx_graph.content_ir.accessor import has_kind_marker
from matrx_graph.content_ir.blank_kind import report_blank_kind, reset_blank_kind_reports


@pytest.fixture(autouse=True)
def _fresh() -> None:
    reset_blank_kind_reports()


def test_blank_kind_is_reported_once(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR):
        assert report_blank_kind("t", {"__kind": ""}) is True
        report_blank_kind("t", {"__kind": ""})
    assert len(caplog.records) == 1
    assert "content-ir rule 31" in caplog.records[0].getMessage()


def test_detector_reports_and_keeps_its_answer(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR):
        assert has_kind_marker({"__kind": ""}) is True
    assert len(caplog.records) == 1


def test_named_kind_and_absent_key_are_silent(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR):
        assert report_blank_kind("t", {"__kind": "report"}) is False
        assert report_blank_kind("t", {"title": "x"}) is False
        assert has_kind_marker({"__kind": "report"}) is True
    assert caplog.records == []
