"""Tests for parsing the complete fixture-tree inventory."""

import pytest

from agentic_devtools.cli.ci.windows_fixture_bytes import _parse_fixture_inventory

_PATH = b"tests/fixtures/reviewing-agent-benchmark/fixture"
_BLOB = b"b" * 40


def test_parse_fixture_inventory_returns_each_path_and_blob() -> None:
    record = b"100644 blob " + _BLOB + b"\t" + _PATH + b"\0"

    assert _parse_fixture_inventory(record, "a" * 40) == {_PATH: _BLOB}


@pytest.mark.parametrize(
    ("tree_output", "message"),
    [
        (b"", "empty"),
        (b"not terminated", "truncated"),
        (b"100644 blob " + _BLOB + b"\t" + _PATH, "truncated"),
        (b"bad\0", "Malformed"),
        (
            b"100644 blob " + _BLOB + b"\t" + _PATH + b"\0" * 2,
            "Malformed",
        ),
        (
            b"100644 blob " + _BLOB + b"\t" + _PATH + b"\0" + b"100644 blob " + _BLOB + b"\t" + _PATH + b"\0",
            "Duplicate",
        ),
    ],
)
def test_parse_fixture_inventory_rejects_incomplete_or_ambiguous_data(tree_output: bytes, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        _parse_fixture_inventory(tree_output, "a" * 40)


def test_parse_fixture_inventory_rejects_non_bytes_output() -> None:
    with pytest.raises(ValueError, match="malformed"):
        _parse_fixture_inventory("not bytes", "a" * 40)  # type: ignore[arg-type]
