"""Every scan decoder must survive hostile-but-small input without raising."""

import json
import plistlib
import sys
from xml.parsers.expat import ExpatError

import json5
import pytest
import yaml

from runlayer_cli.safe_parse import (
    PARSE_ERRORS,
    parse_json,
    parse_json5,
    parse_plist,
    parse_toml,
    parse_yaml,
)

from tests.hostile_inputs import DEEP_NESTING, DEEP_NESTING_TOML

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def test_raw_decoders_raise_recursion_error_on_deep_nesting():
    """Documents the hazard the wrappers exist for: none of these is a ValueError."""
    for decode, text in (
        (json5.loads, DEEP_NESTING),
        (json.loads, DEEP_NESTING),
        (yaml.safe_load, DEEP_NESTING),
        (tomllib.loads, DEEP_NESTING_TOML),
    ):
        with pytest.raises(RecursionError):
            decode(text)
    assert RecursionError in PARSE_ERRORS


@pytest.mark.parametrize(
    ("parse", "text"),
    [
        (parse_json5, DEEP_NESTING),
        (parse_json, DEEP_NESTING),
        (parse_yaml, DEEP_NESTING),
        (parse_toml, DEEP_NESTING_TOML),
    ],
    ids=["json5", "json", "yaml", "toml"],
)
def test_wrappers_turn_deep_nesting_into_failure_outcome(parse, text):
    outcome = parse(text)
    assert outcome["value"] is None
    assert outcome["error"] is not None
    assert outcome["error"].startswith("RecursionError")


@pytest.mark.parametrize(
    ("parse", "text"),
    [
        (parse_json5, "{not json"),
        (parse_json, "{not json"),
        (parse_yaml, "a: [unclosed"),
        (parse_toml, "a = = 1"),
    ],
)
def test_wrappers_report_ordinary_syntax_errors(parse, text):
    outcome = parse(text)
    assert outcome["value"] is None
    assert outcome["error"] is not None


def test_wrappers_return_decoded_value():
    assert parse_json5('{"a": 1, // c\n}')["value"] == {"a": 1}
    assert parse_json('{"a": 1}')["value"] == {"a": 1}
    assert parse_yaml("a: 1")["value"] == {"a": 1}
    assert parse_toml("a = 1")["value"] == {"a": 1}


def test_decoder_specific_errors_are_covered_without_module_top_imports():
    """``PARSE_ERRORS`` names only builtins; each decoder's own error class
    must still be caught (as a ``ValueError`` subclass or, for YAML, locally).
    """
    assert issubclass(json.JSONDecodeError, PARSE_ERRORS)
    assert issubclass(tomllib.TOMLDecodeError, PARSE_ERRORS)
    assert issubclass(plistlib.InvalidFileException, PARSE_ERRORS)
    assert issubclass(UnicodeDecodeError, PARSE_ERRORS)
    assert not issubclass(yaml.YAMLError, PARSE_ERRORS)
    error = parse_yaml("a: [unclosed")["error"]
    assert error is not None and error.startswith("ParserError")


def test_parse_json_accepts_bytes_and_reports_bad_utf8():
    assert parse_json(b'{"a": 1}')["value"] == {"a": 1}
    outcome = parse_json(b"\xff\xfe")
    assert outcome["value"] is None
    assert outcome["error"] is not None


def test_yaml_empty_document_is_success_with_none_value():
    """Empty YAML is a legitimate null document, not a decode failure."""
    outcome = parse_yaml("")
    assert outcome == {"value": None, "error": None}


_PLIST_BAD_INTEGER = (
    b"<plist><dict><key>CFBundleShortVersionString</key>"
    b"<integer>invalid</integer></dict></plist>"
)
_PLIST_TRUNCATED_XML = b"<plist><dict><key>CFBundleShortVersionString</key>"
_PLIST_BAD_DATE = (
    b"<plist><dict><key>CFBundleShortVersionString</key>"
    b"<date>invalid</date></dict></plist>"
)
_PLIST_KEY_OUTSIDE_DICT = b"<plist><key>CFBundleShortVersionString</key></plist>"


@pytest.mark.parametrize(
    ("raw", "raised"),
    [
        (_PLIST_BAD_INTEGER, ValueError),
        (_PLIST_TRUNCATED_XML, ExpatError),
        (_PLIST_BAD_DATE, AttributeError),
        (_PLIST_KEY_OUTSIDE_DICT, IndexError),
    ],
    ids=["bad-integer", "truncated-xml", "bad-date", "key-outside-dict"],
)
def test_raw_plist_decoder_leaks_handler_internals(raw, raised):
    """Documents the hazard: the XML reader has no enumerable failure set.

    None of these is ``InvalidFileException``, and two are not even
    ``ValueError``; each is whatever the element handler tripped over.
    """
    with pytest.raises(raised) as excinfo:
        plistlib.loads(raw)
    assert not isinstance(excinfo.value, plistlib.InvalidFileException)


@pytest.mark.parametrize(
    ("raw", "error_prefix"),
    [
        (_PLIST_BAD_INTEGER, "ValueError"),
        (_PLIST_TRUNCATED_XML, "ExpatError"),
        (_PLIST_BAD_DATE, "AttributeError"),
        (_PLIST_KEY_OUTSIDE_DICT, "IndexError"),
        (b"not a plist at all", "InvalidFileException"),
    ],
    ids=["bad-integer", "truncated-xml", "bad-date", "key-outside-dict", "not-a-plist"],
)
def test_parse_plist_turns_decode_failures_into_outcome(raw, error_prefix):
    outcome = parse_plist(raw)
    assert outcome["value"] is None
    assert outcome["error"] is not None
    assert outcome["error"].startswith(error_prefix)


def test_parse_plist_lets_memory_error_surface(monkeypatch):
    """The broad catch stops at the same line as ``PARSE_ERRORS``."""

    def exhausted(_raw):
        raise MemoryError

    monkeypatch.setattr(plistlib, "loads", exhausted)
    with pytest.raises(MemoryError):
        parse_plist(b"<plist/>")


def test_parse_plist_returns_decoded_value_for_xml_and_binary():
    document = {"CFBundleShortVersionString": "2.4.1"}
    assert parse_plist(plistlib.dumps(document))["value"] == document
    binary = plistlib.dumps(document, fmt=plistlib.FMT_BINARY)
    assert parse_plist(binary)["value"] == document
