"""Tests for chat.py extracted helper functions."""

from __future__ import annotations

from unittest.mock import MagicMock

from anteroom.routers.chat import (
    _extract_streaming_content,
    _extract_streaming_language,
    _get_client_id,
    _get_db_name,
    _is_safe_name,
)

# ---------------------------------------------------------------------------
# _is_safe_name
# ---------------------------------------------------------------------------


class TestIsSafeName:
    def test_valid_simple(self) -> None:
        assert _is_safe_name("my-db") is True

    def test_valid_underscore(self) -> None:
        assert _is_safe_name("DB_Name") is True

    def test_valid_single_char(self) -> None:
        assert _is_safe_name("a") is True

    def test_valid_max_length(self) -> None:
        assert _is_safe_name("a" * 64) is True

    def test_valid_uuid_shaped(self) -> None:
        assert _is_safe_name("550e8400-e29b-41d4-a716-446655440000") is True

    def test_valid_digits_only(self) -> None:
        assert _is_safe_name("12345") is True

    def test_invalid_empty(self) -> None:
        assert _is_safe_name("") is False

    def test_invalid_too_long(self) -> None:
        assert _is_safe_name("a" * 65) is False

    def test_invalid_space(self) -> None:
        assert _is_safe_name("my db") is False

    def test_invalid_dot(self) -> None:
        assert _is_safe_name("my.db") is False

    def test_invalid_slash(self) -> None:
        assert _is_safe_name("my/db") is False

    def test_invalid_semicolon(self) -> None:
        assert _is_safe_name("db;drop") is False

    def test_invalid_newline(self) -> None:
        assert _is_safe_name("db\ntable") is False

    def test_invalid_sql_injection(self) -> None:
        assert _is_safe_name("'; DROP TABLE --") is False


# ---------------------------------------------------------------------------
# _get_db_name
# ---------------------------------------------------------------------------


class TestGetDbName:
    def _make_request(self, db_param: str | None = None) -> MagicMock:
        request = MagicMock()
        params: dict[str, str] = {}
        if db_param is not None:
            params["db"] = db_param
        request.query_params = params
        return request

    def test_missing_db_param_returns_personal(self) -> None:
        assert _get_db_name(self._make_request()) == "personal"

    def test_invalid_name_returns_personal(self) -> None:
        assert _get_db_name(self._make_request("my.db")) == "personal"

    def test_valid_name_returned(self) -> None:
        assert _get_db_name(self._make_request("team-db")) == "team-db"

    def test_empty_string_returns_personal(self) -> None:
        assert _get_db_name(self._make_request("")) == "personal"

    def test_slash_returns_personal(self) -> None:
        assert _get_db_name(self._make_request("path/inject")) == "personal"


# ---------------------------------------------------------------------------
# _get_client_id
# ---------------------------------------------------------------------------


class TestGetClientId:
    def _make_request(self, client_id: str | None = None) -> MagicMock:
        request = MagicMock()
        headers: dict[str, str] = {}
        if client_id is not None:
            headers["x-client-id"] = client_id
        request.headers = headers
        return request

    def test_valid_uuid_returned(self) -> None:
        uuid_val = "550e8400-e29b-41d4-a716-446655440000"
        assert _get_client_id(self._make_request(uuid_val)) == uuid_val

    def test_invalid_uuid_returns_empty(self) -> None:
        assert _get_client_id(self._make_request("not-a-uuid")) == ""

    def test_missing_header_returns_empty(self) -> None:
        assert _get_client_id(self._make_request()) == ""

    def test_empty_header_returns_empty(self) -> None:
        assert _get_client_id(self._make_request("")) == ""

    def test_partial_uuid_returns_empty(self) -> None:
        assert _get_client_id(self._make_request("550e8400-e29b")) == ""


# ---------------------------------------------------------------------------
# _extract_streaming_content
# ---------------------------------------------------------------------------


class TestExtractStreamingContent:
    def test_no_content_key(self) -> None:
        assert _extract_streaming_content('{"title": "hello"') is None

    def test_content_key_no_value_yet(self) -> None:
        assert _extract_streaming_content('{"content"') is None

    def test_content_key_colon_no_quote(self) -> None:
        assert _extract_streaming_content('{"content":') is None

    def test_simple_text(self) -> None:
        assert _extract_streaming_content('{"content": "hello world"') == "hello world"

    def test_newline_escape(self) -> None:
        assert _extract_streaming_content('{"content": "line1\\nline2"') == "line1\nline2"

    def test_tab_escape(self) -> None:
        assert _extract_streaming_content('{"content": "col1\\tcol2"') == "col1\tcol2"

    def test_carriage_return_escape(self) -> None:
        assert _extract_streaming_content('{"content": "a\\rb"') == "a\rb"

    def test_quote_escape(self) -> None:
        assert _extract_streaming_content('{"content": "say \\"hi\\""') == 'say "hi"'

    def test_backslash_escape(self) -> None:
        assert _extract_streaming_content('{"content": "path\\\\dir"') == "path\\dir"

    def test_forward_slash_escape(self) -> None:
        assert _extract_streaming_content('{"content": "a\\/b"') == "a/b"

    def test_backspace_escape(self) -> None:
        assert _extract_streaming_content('{"content": "a\\bb"') == "a\bb"

    def test_formfeed_escape(self) -> None:
        assert _extract_streaming_content('{"content": "a\\fb"') == "a\fb"

    def test_unicode_escape(self) -> None:
        assert _extract_streaming_content('{"content": "caf\\u00e9"') == "caf\u00e9"

    def test_incomplete_unicode_escape(self) -> None:
        result = _extract_streaming_content('{"content": "caf\\u00')
        assert result == "caf"

    def test_incomplete_backslash_at_end(self) -> None:
        result = _extract_streaming_content('{"content": "hello\\')
        assert result == "hello"

    def test_closed_string(self) -> None:
        assert _extract_streaming_content('{"content": "done", "other": 1}') == "done"

    def test_empty_content(self) -> None:
        assert _extract_streaming_content('{"content": ""') == ""

    def test_whitespace_around_colon(self) -> None:
        assert _extract_streaming_content('{"content" : "ok"') == "ok"


# ---------------------------------------------------------------------------
# _extract_streaming_language
# ---------------------------------------------------------------------------


class TestExtractStreamingLanguage:
    def test_no_language_key(self) -> None:
        assert _extract_streaming_language('{"content": "hello"') is None

    def test_valid_language(self) -> None:
        assert _extract_streaming_language('{"language": "python"') == "python"

    def test_language_with_plus(self) -> None:
        assert _extract_streaming_language('{"language": "c++"') == "c++"

    def test_language_with_hash(self) -> None:
        assert _extract_streaming_language('{"language": "c#"') == "c#"

    def test_language_too_long(self) -> None:
        assert _extract_streaming_language('{"language": "' + "a" * 51 + '"') is None

    def test_language_with_special_chars(self) -> None:
        assert _extract_streaming_language('{"language": "lang;drop"') is None

    def test_language_with_space(self) -> None:
        assert _extract_streaming_language('{"language": "my lang"') is None

    def test_language_empty(self) -> None:
        assert _extract_streaming_language('{"language": ""') is None
