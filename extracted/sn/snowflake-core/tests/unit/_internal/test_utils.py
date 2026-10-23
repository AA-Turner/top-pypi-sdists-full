import pytest

from snowflake.core._internal.utils import (
    get_local_file_path,
    is_single_quoted,
    normalize_path,
)


@pytest.mark.parametrize(
    ("path", "is_local"),
    [
        # One backslash before quote: x\'
        ("x\\'", False),
        ("x\\'", True),
        # Two backslashes before quote: x\\'
        ("x\\\\'", False),
        ("x\\\\'", True),
        # Three backslashes before quote: x\\\'
        ("x\\\\\\'", False),
        ("x\\\\\\'", True),
    ],
)
def test_normalize_path_backslash_exploit(path: str, is_local: bool) -> None:
    """normalize_path must produce a properly closed single-quoted string for backslash-before-quote inputs."""
    result = normalize_path(path, is_local)
    assert is_single_quoted(result)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        # Valid single-quoted strings
        ("''", True),
        ("'hello'", True),
        ("'file:///tmp/load data'", True),
        ("'@stage/path'", True),
        (r"'it\'s a path'", True),  # Escaped inner quote (backslash-escape convention)
        ("'foo\\\\'", True),  # Escaped backslash followed by closing quote
        ("'legit' OR '1'='1'", False),  # Inner has unescaped quote
        ("'@stage' OVERWRITE=TRUE --'", False),
        ("hello", False),  # Not quoted at all
        ("@stage/path", False),
        ("'", False),  # Single quote only — length < 2
        ("'foo\\'", False),  # Trailing backslash consumes the closing quote → string not properly closed
    ],
)
def test_is_single_quoted(name: str, expected: bool) -> None:
    """Exercise :func:`~snowflake.core._internal.utils.is_single_quoted`."""
    assert is_single_quoted(name) is expected


@pytest.mark.parametrize(
    ("path", "is_local", "expected"),
    [
        # Already properly single-quoted — returned as-is
        ("'file:///tmp/data'", True, "'file:///tmp/data'"),
        ("'@my_stage/path'", False, "'@my_stage/path'"),
        # Plain local path — should get file:// prefix and quotes
        ("/tmp/data", True, "'file:///tmp/data'"),
        ("/tmp/load data", True, "'file:///tmp/load data'"),
        # Path containing a single quote — must be escaped
        ("/tmp/it's here", True, "'file:///tmp/it\\'s here'"),
        # bypasses naive is_single_quoted: 'x' AND 'y'
        ("'x' AND 'y'", False, "'@\\'x\\' AND \\'y\\''"),
        # Plain remote stage path
        ("@my_stage", False, "'@my_stage'"),
    ],
)
def test_normalize_path(path: str, is_local: bool, expected: str) -> None:
    """Exercise :func:`~snowflake.core._internal.utils.normalize_path`."""
    assert normalize_path(path, is_local) == expected


@pytest.mark.parametrize(
    ("file", "expected"),
    [
        # Properly single-quoted with file:// prefix
        ("'file:///tmp/data'", "/tmp/data"),
        # Properly single-quoted without prefix
        ("'/tmp/data'", "/tmp/data"),
        # Not quoted
        ("/tmp/data", "/tmp/data"),
        ("file:///tmp/data", "/tmp/data"),
        # looks quoted but has unescaped inner quote and as such is treated as
        # plain (unquoted) string; outer quotes are not stripped.
        ("'@stage' OVERWRITE=TRUE --'", "'@stage' OVERWRITE=TRUE --'"),
    ],
)
def test_get_local_file_path(file: str, expected: str) -> None:
    """Exercise :func:`~snowflake.core._internal.utils.get_local_file_path`."""
    assert get_local_file_path(file) == expected
