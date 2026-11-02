"""Level 1: matrx_utils canonical primitives — hashing / ids / timeutils.

Pure-stdlib, no sibling package needed. Covers the determinism + fail-loud
contract of each primitive, plus the byte-faithfulness guarantee that lets the
existing scattered copies migrate without changing any already-emitted key.
"""
import datetime as dt
import json
import uuid

import pytest

from matrx_utils import (
    UTC,
    hash_bytes,
    hash_chunks,
    hash_text,
    new_hex,
    new_id,
    new_uuid,
    parse_iso,
    stable_hash,
    stable_json,
    to_iso,
    utcnow,
)


# --------------------------------------------------------------------------- #
# hashing
# --------------------------------------------------------------------------- #

def test_stable_hash_is_key_order_independent():
    a = stable_hash({"x": 1, "y": [1, 2], "z": {"b": 2, "a": 1}})
    b = stable_hash({"z": {"a": 1, "b": 2}, "y": [1, 2], "x": 1})
    assert a == b
    assert len(a) == 64  # full sha256 hex


def test_stable_hash_truncation_and_algo():
    full = stable_hash({"k": "v"})
    assert stable_hash({"k": "v"}, length=16) == full[:16]
    assert len(stable_hash({"k": "v"}, algo="sha1")) == 40
    with pytest.raises(ValueError):
        stable_hash({"k": "v"}, length=0)


def test_stable_json_matches_idempotency_form_byte_for_byte():
    """The canonical serialization MUST equal the existing cloud_sync/idempotency.py
    form so migrating that call site does not change emitted idempotency keys."""
    obj = {"b": 2, "a": 1, "when": dt.datetime(2026, 6, 24, tzinfo=UTC)}
    expected = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)
    assert stable_json(obj) == expected


def test_stable_hash_handles_non_json_scalars():
    # datetime / UUID / set-free objects encode via default=str instead of raising
    h = stable_hash({"id": uuid.UUID(int=0), "t": dt.datetime(2026, 1, 1, tzinfo=UTC)})
    assert len(h) == 64


def test_hash_text_bytes_and_chunks_agree():
    blob = b"hello world"
    assert hash_bytes(blob) == hash_text("hello world")
    assert hash_chunks([b"hello ", b"world"]) == hash_bytes(blob)
    assert hash_chunks([]) == hash_bytes(b"")  # empty stream == empty bytes


# --------------------------------------------------------------------------- #
# ids
# --------------------------------------------------------------------------- #

def test_new_id_is_a_uuid_string_and_unique():
    a, b = new_id(), new_id()
    assert a != b
    uuid.UUID(a)  # parses as a real uuid -> drop-in for str(uuid.uuid4())


def test_new_id_prefix():
    rid = new_id("req")
    assert rid.startswith("req_")
    uuid.UUID(rid.split("_", 1)[1])
    assert new_id("run", sep="-").startswith("run-")
    with pytest.raises(ValueError):
        new_id("")  # empty prefix is a bug, not a bare id


def test_new_hex_and_new_uuid():
    assert len(new_hex()) == 32
    assert len(new_hex(8)) == 8
    assert "-" not in new_hex()
    assert isinstance(new_uuid(), uuid.UUID)
    with pytest.raises(ValueError):
        new_hex(0)


# --------------------------------------------------------------------------- #
# timeutils
# --------------------------------------------------------------------------- #

def test_utcnow_is_aware_utc():
    now = utcnow()
    assert now.tzinfo is not None
    assert now.utcoffset() == dt.timedelta(0)


def test_parse_iso_tolerates_z_and_is_always_aware():
    z = parse_iso("2026-06-24T12:00:00Z")
    assert z.tzinfo is not None and z.utcoffset() == dt.timedelta(0)
    assert z.hour == 12
    # naive input is assumed UTC and stamped aware -> comparable to utcnow()
    naive = parse_iso("2026-06-24T12:00:00")
    assert naive.tzinfo is not None
    assert (utcnow() - naive)  # no TypeError == the whole point


def test_parse_iso_converts_offset_to_utc():
    east = parse_iso("2026-06-24T12:00:00+05:00")
    assert east.utcoffset() == dt.timedelta(0)
    assert east.hour == 7  # 12:00 +05:00 == 07:00 UTC


def test_to_iso_round_trips_and_normalizes_naive():
    when = dt.datetime(2026, 6, 24, 12, 0, 0, tzinfo=UTC)
    assert parse_iso(to_iso(when)) == when
    # naive in -> assumed UTC
    assert to_iso(dt.datetime(2026, 6, 24, 12, 0, 0)).endswith("+00:00")
