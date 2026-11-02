"""Tests for internal helpers in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _escape_yaml_string


class TestEscapeYamlString:
    """Tests for the _escape_yaml_string helper function (now always-quote per FR-005)."""

    def test_empty_string_returns_quoted_empty(self) -> None:
        """Empty string returns double-quoted empty string."""
        assert _escape_yaml_string("") == '""'

    def test_plain_string_quoted(self) -> None:
        """Plain alphanumeric string is always double-quoted per FR-005."""
        assert _escape_yaml_string("hello") == '"hello"'

    def test_string_with_colon_quoted(self) -> None:
        """String containing colon is quoted."""
        result = _escape_yaml_string("key: value")
        assert result.startswith('"')
        assert result.endswith('"')

    def test_string_with_hash_quoted(self) -> None:
        """String containing hash is quoted."""
        result = _escape_yaml_string("has #tag")
        assert result.startswith('"')

    def test_string_with_newline_escaped(self) -> None:
        """Newlines in string are escaped."""
        result = _escape_yaml_string("line1\nline2")
        assert "\\n" in result

    def test_yaml_boolean_true_quoted(self) -> None:
        """YAML boolean 'true' is quoted to prevent bool parsing."""
        assert _escape_yaml_string("true") == '"true"'

    def test_yaml_boolean_false_quoted(self) -> None:
        """YAML boolean 'false' is quoted to prevent bool parsing."""
        assert _escape_yaml_string("false") == '"false"'

    def test_yaml_boolean_yes_quoted(self) -> None:
        """YAML boolean 'yes' is quoted to prevent bool parsing."""
        assert _escape_yaml_string("yes") == '"yes"'

    def test_yaml_boolean_no_quoted(self) -> None:
        """YAML boolean 'no' is quoted to prevent bool parsing."""
        assert _escape_yaml_string("no") == '"no"'

    def test_yaml_boolean_on_quoted(self) -> None:
        """YAML boolean 'on' is quoted to prevent bool parsing."""
        assert _escape_yaml_string("on") == '"on"'

    def test_yaml_boolean_off_quoted(self) -> None:
        """YAML boolean 'off' is quoted to prevent bool parsing."""
        assert _escape_yaml_string("off") == '"off"'

    def test_yaml_null_quoted(self) -> None:
        """YAML null 'null' is quoted to prevent null parsing."""
        assert _escape_yaml_string("null") == '"null"'

    def test_yaml_tilde_quoted(self) -> None:
        """YAML null '~' is quoted to prevent null parsing."""
        assert _escape_yaml_string("~") == '"~"'

    def test_yaml_reserved_case_insensitive(self) -> None:
        """YAML reserved scalars are quoted regardless of case."""
        assert _escape_yaml_string("True") == '"True"'
        assert _escape_yaml_string("YES") == '"YES"'
        assert _escape_yaml_string("Null") == '"Null"'

    def test_numeric_integer_string_quoted(self) -> None:
        """Numeric-only string '42' is quoted to prevent integer parsing."""
        assert _escape_yaml_string("42") == '"42"'

    def test_numeric_zero_string_quoted(self) -> None:
        """Numeric-only string '0' is quoted to prevent integer parsing."""
        assert _escape_yaml_string("0") == '"0"'

    def test_numeric_float_string_quoted(self) -> None:
        """Numeric float string '3.14' is quoted to prevent float parsing."""
        assert _escape_yaml_string("3.14") == '"3.14"'

    def test_numeric_negative_string_quoted(self) -> None:
        """Negative numeric string '-1' is quoted to prevent integer parsing."""
        assert _escape_yaml_string("-1") == '"-1"'

    def test_numeric_scientific_notation_quoted(self) -> None:
        """Scientific notation string '1e5' is quoted to prevent float parsing."""
        assert _escape_yaml_string("1e5") == '"1e5"'

    def test_non_numeric_alphanumeric_quoted(self) -> None:
        """Alphanumeric string is always quoted per FR-005 always-quote rule."""
        assert _escape_yaml_string("abc123") == '"abc123"'

    def test_backslash_escaped(self) -> None:
        """Backslash in value is escaped."""
        assert _escape_yaml_string("a\\b") == '"a\\\\b"'

    def test_double_quote_escaped(self) -> None:
        """Double quote in value is escaped."""
        assert _escape_yaml_string('say "hi"') == '"say \\"hi\\""'

    def test_carriage_return_escaped(self) -> None:
        """Carriage return is escaped to \\r."""
        assert _escape_yaml_string("a\rb") == '"a\\rb"'

    def test_tab_escaped(self) -> None:
        """Tab is escaped to \\t."""
        assert _escape_yaml_string("a\tb") == '"a\\tb"'

    def test_control_char_escaped_as_unicode(self) -> None:
        """Control characters are escaped as \\uXXXX."""
        assert _escape_yaml_string("a\x01b") == '"a\\u0001b"'

    def test_timestamp_string_quoted(self) -> None:
        """ISO-8601 timestamp string is always quoted."""
        assert _escape_yaml_string("2026-07-28T15:00:00+00:00") == '"2026-07-28T15:00:00+00:00"'
