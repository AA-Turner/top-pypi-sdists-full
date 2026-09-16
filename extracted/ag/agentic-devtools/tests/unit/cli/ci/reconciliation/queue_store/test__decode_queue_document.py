"""Strict wire decoding protects persisted histories before dict construction."""

import pytest

from agentic_devtools.cli.ci.reconciliation.queue_store import _decode_queue_document


@pytest.mark.parametrize(
    "raw",
    [
        b'{"attempts":{},"attempts":{}}',
        b'{"attempts":{"a":{"sequence":1,"sequence":0}}}',
        b'{"revision":NaN}',
        b'{"revision":Infinity}',
        b"[]",
        b"\xff",
        b"{invalid",
    ],
)
def test_rejects_corrupt_wire_data(raw):
    with pytest.raises(ValueError):
        _decode_queue_document(raw)


def test_preserves_valid_document():
    assert _decode_queue_document(b'{"revision":1,"attempts":{}}') == {"revision": 1, "attempts": {}}
