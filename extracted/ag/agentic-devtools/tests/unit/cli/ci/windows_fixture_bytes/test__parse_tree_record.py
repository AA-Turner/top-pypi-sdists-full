"""Tests for parsing one exact Git fixture-tree record."""

import pytest

from agentic_devtools.cli.ci.windows_fixture_bytes import _parse_tree_record

_PATH = b"tests/fixtures/reviewing-agent-benchmark/a file\n.dat"
_BLOB = b"b" * 40


def test_parse_tree_record_preserves_the_raw_path_and_blob_id() -> None:
    record = b"100644 blob " + _BLOB + b"\t" + _PATH

    assert _parse_tree_record(record, 40) == (_PATH, _BLOB)


@pytest.mark.parametrize(
    "record",
    [
        b"",
        b"invalid",
        b"100644 blob\tx",
        b"100644 blob " + _BLOB + b" " + _BLOB + b"\tx",
        b"120000 blob " + _BLOB + b"\t" + _PATH,
        b"100644 commit " + _BLOB + b"\t" + _PATH,
        b"100644 blob " + b"g" * 40 + b"\t" + _PATH,
        b"100644 blob " + _BLOB + b"\toutside/file",
        b"100644 blob " + _BLOB + b"\ttests/fixtures/reviewing-agent-benchmark/../outside",
    ],
)
def test_parse_tree_record_rejects_unsupported_or_malformed_records(record: bytes) -> None:
    with pytest.raises(ValueError):
        _parse_tree_record(record, 40)


def test_parse_tree_record_accepts_sha256_blob_ids() -> None:
    blob = b"c" * 64
    record = b"100755 blob " + blob + b"\t" + _PATH

    assert _parse_tree_record(record, 64) == (_PATH, blob)
