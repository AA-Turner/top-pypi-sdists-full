"""Tests for decoding Git-quoted paths."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _decode_quoted_path


def test_decodes_octal_utf8_and_named_escapes() -> None:
    header = r'"caf\303\251\tfile.py"'

    assert _decode_quoted_path(header, 0, len(header) - 1) == "café\tfile.py"


def test_rejects_unknown_escape_and_invalid_utf8() -> None:
    unknown_escape = r'"\q"'
    invalid_utf8 = r'"\377"'

    assert _decode_quoted_path(unknown_escape, 0, len(unknown_escape) - 1) is None
    assert _decode_quoted_path(invalid_utf8, 0, len(invalid_utf8) - 1) is None
