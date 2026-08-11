import pytest

from snowflake.core._internal.utils import get_local_file_path, is_single_quoted, normalize_path, quote_name


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
    ("name", "keep_case", "expected"),
    [
        # Already quoted names - should return as-is
        ('"already_quoted"', False, '"already_quoted"'),
        ('"already_quoted"', True, '"already_quoted"'),
        ('"MyName"', False, '"MyName"'),
        ('"MyName"', True, '"MyName"'),
        # Unquoted case-insensitive identifiers (simple identifiers)
        # With keep_case=False, should uppercase and quote
        ("simple_id", False, '"SIMPLE_ID"'),
        ("simple_id123", False, '"SIMPLE_ID123"'),
        ("_privatevar", False, '"_PRIVATEVAR"'),
        ("var_with_$dollar", False, '"VAR_WITH_$DOLLAR"'),
        # Unquoted case-insensitive identifiers
        # With keep_case=True, should quote without uppercasing
        ("simple_id", True, '"simple_id"'),
        ("simple_id123", True, '"simple_id123"'),
        ("_privatevar", True, '"_privatevar"'),
        # Names with special characters that require quoting and escaping
        ("name-with-hyphens", False, '"name-with-hyphens"'),
        ("name.with.dots", False, '"name.with.dots"'),
        ("name with spaces", False, '"name with spaces"'),
        # Names with double quotes inside - need escaping
        ('name"with"quotes', False, '"name""with""quotes"'),
        ('name"with"quotes', True, '"name""with""quotes"'),
        ('"ANOTHER   ""NAME""WITH   ""QUOTES"""', False, '"ANOTHER   ""NAME""WITH   ""QUOTES"""'),
        # Mixed case simple identifiers - with keep_case
        ("MySimpleName", False, '"MYSIMPLENAME"'),
        ("MySimpleName", True, '"MySimpleName"'),
        # Single character names
        ("a", False, '"A"'),
        ("A", False, '"A"'),
        ("_", False, '"_"'),
    ],
)
def test_quote_name_parametrized(name: str, keep_case: bool, expected: str) -> None:
    """Exercise :func:`~snowflake.core._internal.utils.quote_name` across identifier forms."""
    result = quote_name(name, keep_case=keep_case)
    assert result == expected


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
