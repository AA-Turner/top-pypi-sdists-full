# tests/test_language.py
from __future__ import annotations

from chardet.pipeline import DetectionResult
from chardet.pipeline.language import _to_utf8, fill_languages


def test_fill_languages_populates_single_language_encoding():
    """fill_languages should fill in language for single-language encodings via Tier 1."""
    results = [DetectionResult("koi8-r", 0.90, None)]
    filled = fill_languages(b"test data", results)
    assert filled[0].language is not None


def test_fill_languages_passes_through_existing_language():
    """fill_languages should not overwrite a language that's already set."""
    results = [DetectionResult("utf-8", 0.95, "fr")]
    filled = fill_languages(b"bonjour", results)
    assert filled[0].language == "fr"
    assert filled[0] is results[0]  # passthrough preserves identity


def test_fill_languages_passes_through_binary_results():
    """fill_languages should leave binary results (encoding=None) untouched."""
    results = [DetectionResult(None, 0.95, None)]
    filled = fill_languages(b"\x00\x01\x02", results)
    assert filled[0].language is None
    assert filled[0] is results[0]


def test_to_utf8_unknown_encoding():
    """_to_utf8 with an unknown encoding should return None."""
    assert _to_utf8(b"Hello world", "not-a-real-encoding") is None


def test_to_utf8_passthrough():
    """_to_utf8 with utf-8 encoding should return data unchanged."""
    data = b"Hello \xc3\xa9"
    assert _to_utf8(data, "utf-8") is data
