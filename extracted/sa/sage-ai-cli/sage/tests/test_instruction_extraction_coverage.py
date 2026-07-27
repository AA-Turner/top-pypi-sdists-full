"""Full-branch tests for sage.core.instruction_extraction.InstructionExtractor."""

from __future__ import annotations

import pytest

from sage.core.instruction_extraction import InstructionExtractor, ExtractedInstruction


@pytest.fixture
def extractor():
    return InstructionExtractor()


class TestMarkerDetection:

    def test_make_sure_marker(self, extractor):
        results = extractor.extract("Please make sure to include tests")
        assert len(results) == 1
        assert results[0].type == "include"

    def test_dont_marker_classifies_exclude(self, extractor):
        results = extractor.extract("Don't add any TODO comments")
        assert len(results) == 1
        assert results[0].type == "exclude"

    def test_do_not_marker(self, extractor):
        results = extractor.extract("Do not use deprecated APIs")
        assert len(results) == 1
        assert results[0].type == "exclude"

    def test_never_marker_classifies_exclude(self, extractor):
        results = extractor.extract("Never log passwords")
        assert len(results) == 1
        assert results[0].type == "exclude"

    def test_format_keyword_classifies_format(self, extractor):
        results = extractor.extract("Please format the output as a table")
        assert any(i.type == "format" for i in results)

    def test_include_keyword(self, extractor):
        results = extractor.extract("Please include unit tests")
        assert results[0].type == "include"

    def test_no_marker_returns_empty(self, extractor):
        assert extractor.extract("How are you today") == []

    def test_multiple_sentences(self, extractor):
        text = "Please add tests. Don't use deprecated APIs. Always use type hints."
        results = extractor.extract(text)
        assert len(results) == 3

    def test_empty_string(self, extractor):
        assert extractor.extract("") == []


def test_dataclass_priority_default():
    ext = ExtractedInstruction(content="x", type="constraint")
    assert ext.priority == 1
