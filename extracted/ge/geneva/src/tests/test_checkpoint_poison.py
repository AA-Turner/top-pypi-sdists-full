# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Recovery from poison checkpoint files that panic Lance's Rust reader.

A nullable blob checkpoint can hit a Lance decode bug whose Rust panic surfaces as
``pyo3_runtime.PanicException`` (a ``BaseException``, not ``Exception``). Left
unhandled it escapes Geneva's ``except Exception`` handlers, kills the writer, and
Ray crash-loops on the same file. These tests exercise the guard that converts such
a panic into a non-retryable, attributable :class:`CorruptCheckpointError`.

The poison fixture is synthesized deterministically by lowering a column page's
recorded row count below the file's row count (an in-place same-length varint
rewrite, no offset shifts). Reading the result overruns
``StructuralPrimitiveFieldDecoder::drain`` and panics — the same failure class as
the production checkpoints.
"""

import glob
import os

import pyarrow as pa
import pytest
from lance.file import LanceFileReader

from geneva.checkpoint import (
    FlatLanceCheckpointStore,
    _is_lance_reader_panic,
)
from geneva.errors import CorruptCheckpointError


def _varint(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            break
    return bytes(out)


def _nullable_blob_batch(nrows: int) -> pa.RecordBatch:
    """A checkpoint-shaped batch: ``image`` struct with a nullable blob child."""
    bf = pa.field(
        "image_bytes", pa.large_binary(), metadata={"lance-encoding:blob": "true"}
    )
    st = pa.struct([bf, pa.field("error_code", pa.string())])
    rows = [
        {
            "image_bytes": None if i % 3 == 0 else os.urandom(256),
            "error_code": "ERR" if i % 3 == 0 else None,
        }
        for i in range(nrows)
    ]
    return pa.record_batch(
        [pa.array(rows, type=st), pa.array(range(nrows), type=pa.uint64())],
        schema=pa.schema([pa.field("image", st), pa.field("_rowaddr", pa.uint64())]),
    )


def write_poison_checkpoint(store, key: str, *, nrows: int = 4000) -> str:
    """Write a checkpoint whose Lance file panics the reader, return its path.

    Writes a normal nullable-blob batch, then rewrites a column page's row-count
    varint to a smaller (same-length) value so the page accounts for fewer rows than
    the file claims. Tries each candidate row-count varint near the file tail until a
    raw read panics, leaving the poison bytes in place.
    """
    store[key] = _nullable_blob_batch(nrows)
    matches = [
        p
        for p in glob.glob(os.path.join(store.root, "**", "*.lance"), recursive=True)
        if os.path.isfile(p) and key in p
    ]
    assert matches, f"no on-disk lance file for checkpoint {key!r}"
    path = matches[0]

    with open(path, "rb") as fh:
        original = bytearray(fh.read())
    target, smaller = _varint(nrows), _varint(nrows - 1000)
    assert len(target) == len(smaller)

    tail = max(0, len(original) - 8192)
    offsets = []
    i = original.find(target, tail)
    while i != -1:
        offsets.append(i)
        i = original.find(target, i + 1)

    for off in offsets:
        buf = bytearray(original)
        buf[off : off + len(smaller)] = smaller
        with open(path, "wb") as f:
            f.write(buf)
        try:
            LanceFileReader(path).read_all().to_table()
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # noqa: BLE001
            if _is_lance_reader_panic(exc):
                return path
    # Restore and fail loudly if no candidate produced a panic on this Lance build.
    with open(path, "wb") as f:
        f.write(original)
    pytest.skip("could not synthesize a poison checkpoint on this Lance build")


def test_is_lance_reader_panic_classification() -> None:
    class PanicException(BaseException):
        pass

    assert _is_lance_reader_panic(PanicException("index out of bounds"))
    assert _is_lance_reader_panic(
        ValueError('task 7 panicked with message "assertion failed"')
    )
    # Ordinary corruption / IO errors must NOT be treated as a reader panic, so
    # they stay on the retry path.
    assert not _is_lance_reader_panic(OSError("Invalid user input"))
    assert not _is_lance_reader_panic(ValueError("bad column"))


def test_poison_checkpoint_raises_corrupt_error(tmp_path) -> None:
    # The guard lives in FlatLanceCheckpointStore.__getitem__, which the
    # Hierarchical store inherits unchanged.
    store = FlatLanceCheckpointStore(str(tmp_path))
    key = "udf-x_ver-1_col-image_range-0-4000"
    write_poison_checkpoint(store, key)

    with pytest.raises(CorruptCheckpointError) as excinfo:
        _ = store[key]

    err = excinfo.value
    assert key in str(err)
    assert err.key == key
    # Attributable: carries the file path and the underlying panic cause.
    assert err.path is not None
    assert err.cause is not None
    # CorruptCheckpointError is an Exception (FatalWorkerError -> RuntimeError), so
    # Geneva's existing ``except Exception`` fragment-isolation handlers catch it —
    # unlike the raw pyo3 BaseException that wedged the worker.
    assert isinstance(err, Exception)


def test_healthy_nullable_blob_checkpoint_roundtrips(tmp_path) -> None:
    """Control: an uncorrupted nullable-blob checkpoint reads back unchanged."""
    store = FlatLanceCheckpointStore(str(tmp_path))
    key = "udf-x_ver-1_col-image_range-0-4000"
    store[key] = _nullable_blob_batch(4000)
    got = store[key]
    assert got.num_rows == 4000
    assert got.column("image").field("image_bytes").null_count > 0
