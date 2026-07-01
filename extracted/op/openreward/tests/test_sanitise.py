import json

import pytest

from openreward.api.rollouts.serializers.models import _sanitise_content

# ── helpers ───────────────────────────────────────────────────────────────────

def is_json_serialisable(s: str) -> bool:
    try:
        json.dumps(s)
        return True
    except (ValueError, UnicodeEncodeError):
        return False


# ── surrogate handling ────────────────────────────────────────────────────────

class TestSurrogates:
    def test_lone_surrogate_becomes_backslash_escape(self):
        # \udcff is a surrogateescape stand-in for the byte 0xFF
        s = "hello\udcffworld"
        result = _sanitise_content(s)
        assert "\udcff" not in result
        assert is_json_serialisable(result)

    def test_surrogate_pair_encoded_safely(self):
        s = "\ud83d\ude00"  # not a proper pair in a str — both stay as surrogates
        result = _sanitise_content(s)
        assert is_json_serialisable(result)

    def test_no_surrogates_unchanged(self):
        s = "clean string"
        assert _sanitise_content(s) == s


# ── null byte stripping ──────────────────────────────────────────────────────

class TestNullBytes:
    def test_null_byte_stripped(self):
        result = _sanitise_content("before\x00after")
        assert "\x00" not in result
        assert result == "beforeafter"

    def test_multiple_nulls_stripped(self):
        result = _sanitise_content("\x00a\x00b\x00")
        assert result == "ab"


# ── characters that should be preserved ──────────────────────────────────────

class TestPreserved:
    def test_tab_preserved(self):
        s = "col1\tcol2"
        assert _sanitise_content(s) == s

    def test_newline_preserved(self):
        s = "line1\nline2"
        assert _sanitise_content(s) == s

    def test_carriage_return_preserved(self):
        s = "line1\r\nline2"
        assert _sanitise_content(s) == s

    def test_ansi_preserved(self):
        s = "\x1b[31mred text\x1b[0m"
        assert _sanitise_content(s) == s

    def test_bel_preserved(self):
        s = "alert\x07done"
        assert _sanitise_content(s) == s


# ── JSON serialisability (the core guarantee) ─────────────────────────────────

class TestJsonSerialisable:
    @pytest.mark.parametrize("raw", [
        "\x1b[31mred\x1b[0m",
        "hello\udcffworld",
        "\x00\x01\x02",
        "\x1b[38;5;200m\udcfe some output \x07",
        "perfectly normal string",
        "unicode: café, 日本語, emoji: 😀",
        "\t\n\r preserved",
    ])
    def test_output_is_always_json_serialisable(self, raw):
        assert is_json_serialisable(_sanitise_content(raw))


# ── combined / realistic inputs ───────────────────────────────────────────────

class TestRealistic:
    def test_mixed_ansi_and_null(self):
        s = "\x1b[32mOK\x1b[0m\x07 done\x00"
        result = _sanitise_content(s)
        assert result == "\x1b[32mOK\x1b[0m\x07 done"
        assert is_json_serialisable(result)

    def test_binary_garbage_from_surrogateescape(self):
        # Simulate reading a binary file with surrogateescape
        raw_bytes = bytes(range(0x80, 0xA0))
        s = raw_bytes.decode("utf-8", "surrogateescape")
        result = _sanitise_content(s)
        assert is_json_serialisable(result)

    def test_empty_string(self):
        assert _sanitise_content("") == ""
