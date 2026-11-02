"""Contract tests for the shared lexical refinement path normalizer."""

import pytest

from agentic_devtools.cli.issue_template import refinement_paths
from agentic_devtools.cli.issue_template.refinement_paths import normalize_refinement_path


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("src/nested/file.py", "src/nested/file.py"),
        (r"Src\Nested\File.PY", "Src/Nested/File.PY"),
        (r"Src\Nested/File.PY", "Src/Nested/File.PY"),
        (".env", ".env"),
        ("dir/file..py", "dir/file..py"),
        (".../file", ".../file"),
        ("src//nested///file.py", "src//nested///file.py"),
        ("src/file/", "src/file/"),
        (r"src\\nested\\file.py", "src//nested//file.py"),
        (r"src/\u002e\u002e/file", "src//u002e/u002e/file"),
        ("src/%2e%2e/file", "src/%2e%2e/file"),
        ("[file]`{name}:part", "[file]`{name}:part"),
        ("C:", "C:"),
        ("C:part", "C:part"),
        (r"c:part\file", "c:part/file"),
        ("Å:/part", "Å:/part"),
        ("AA:/part", "AA:/part"),
        ("1:/part", "1:/part"),
        ("src/zero\u200bwidth", "src/zero\u200bwidth"),
        ("src/é.py", "src/é.py"),
    ],
)
def test_preserves_valid_tokens_except_slash_conversion(value: str, expected: str) -> None:
    assert normalize_refinement_path(value) == (expected, None)


@pytest.mark.parametrize(
    ("value", "error"),
    [
        ("", "empty_token"),
        ("   ", "whitespace_character"),
        ("src/file name", "whitespace_character"),
        (" src/file", "whitespace_character"),
        ("src/file ", "whitespace_character"),
        ("src/\u00a0file", "whitespace_character"),
        ("src/\u2028file", "whitespace_character"),
        ("src/\x00file", "control_character"),
        ("src/\x7ffile", "control_character"),
        ("src/\x80file", "control_character"),
        ("src/\x9ffile", "control_character"),
        ("\t", "control_character"),
        ("src/\nfile", "control_character"),
        ("/root/file", "absolute_path"),
        (r"\root\file", "absolute_path"),
        ("//server/share/file", "absolute_path"),
        (r"\\server\share\file", "absolute_path"),
        ("C:/part", "absolute_path"),
        (r"C:\part", "absolute_path"),
        ("c:/part", "absolute_path"),
        (r"z:\part", "absolute_path"),
        ("A:/", "absolute_path"),
        ("Z:/part", "absolute_path"),
        ("/", "absolute_path"),
        ("\\", "absolute_path"),
        (".", "traversal_segment"),
        ("..", "traversal_segment"),
        ("./file", "traversal_segment"),
        (r".\file", "traversal_segment"),
        ("../file", "traversal_segment"),
        (r"..\file", "traversal_segment"),
        ("src/./file", "traversal_segment"),
        (r"src\.\file", "traversal_segment"),
        ("src/../file", "traversal_segment"),
        (r"src\..\file", "traversal_segment"),
        ("src/.", "traversal_segment"),
        (r"src\..", "traversal_segment"),
        ("src//..//file", "traversal_segment"),
    ],
)
def test_returns_exact_lexical_error(value: str, error: str) -> None:
    assert normalize_refinement_path(value) == (None, error)


@pytest.mark.parametrize(
    ("value", "error"),
    [
        (" /../file\x00", "control_character"),
        ("/../file\t", "control_character"),
        ("/../file name", "whitespace_character"),
        (r"C:\..\file name", "whitespace_character"),
        ("../file name", "whitespace_character"),
        ("/../file", "absolute_path"),
        (r"\\server\..\file", "absolute_path"),
        (r"C:\..\file", "absolute_path"),
    ],
)
def test_uses_ordered_error_precedence(value: str, error: str) -> None:
    assert normalize_refinement_path(value) == (None, error)


def test_exposes_only_the_approved_public_symbol() -> None:
    assert [name for name in vars(refinement_paths) if not name.startswith("_")] == ["normalize_refinement_path"]
