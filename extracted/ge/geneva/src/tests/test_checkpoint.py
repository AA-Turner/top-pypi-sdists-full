# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import json
import pickle
import tempfile
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import lance
import pyarrow as pa
import pytest
from lance.file import LanceFileReader, ReaderResults

from geneva.checkpoint import (
    CheckpointConfig,
    CheckpointRootMixedLayoutError,
    CheckpointStore,
    FlatLanceCheckpointStore,
    HierarchicalLanceCheckpointStore,
    InMemoryCheckpointStore,
    MultiBaseCheckpointStore,
    _parse_flat_key,
    _select_store_class,
    discard_short_checkpoint,
    read_checkpoint_num_rows,
    stamp_checkpoint_num_rows,
    strip_checkpoint_num_rows,
)
from geneva.checkpoint_utils import hash_string
from geneva.errors import CorruptCheckpointError

pytestmark = pytest.mark.slow

# Identity prefix shared by the sample flat checkpoint keys used across the suite.
_FLAT_KEY_BASE_NO_URI = "udf-foo_ver-1_col-c_where-aa"
_FLAT_KEY_BASE_NO_SRC = f"{_FLAT_KEY_BASE_NO_URI}_uri-bb"
_FLAT_KEY_BASE = f"{_FLAT_KEY_BASE_NO_SRC}_srcfiles-cc"


def _bf_hash(base: str = _FLAT_KEY_BASE) -> str:
    return hash_string(base.split("_uri-", 1)[0])


def _fragment_shard(frag_id: int) -> str:
    return hash_string(str(frag_id))[:2]


def _fragment_identity(frag_id: int, base: str = _FLAT_KEY_BASE) -> str:
    if "_srcfiles-" not in base:
        return str(frag_id)
    srcfiles = base.rsplit("_srcfiles-", 1)[1]
    return f"{frag_id}_src-{srcfiles}"


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/new_dir"),
    ],
)
def test_checkpoint(store: CheckpointStore) -> None:
    store["key"] = pa.RecordBatch.from_pydict({"a": [1, 2, 3]})
    assert "key" in store
    assert "key" in list(store.list_keys())
    assert store["key"].to_pydict() == {"a": [1, 2, 3]}


@pytest.mark.parametrize("layout", ["flat", "hierarchical"])
def test_lance_checkpoint_read_range_preserves_values_and_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, layout: str
) -> None:
    if layout == "flat":
        store: CheckpointStore = FlatLanceCheckpointStore(str(tmp_path / "flat"))
        key = "key"
        empty_key = "empty"
        missing_key = "missing"
    else:
        store = HierarchicalLanceCheckpointStore(
            str(tmp_path / "hierarchical"), write_identity_sidecar=False
        )
        key = f"{_FLAT_KEY_BASE}_frag-7_range-0-5"
        empty_key = f"{_FLAT_KEY_BASE}_frag-8_range-0-0"
        missing_key = f"{_FLAT_KEY_BASE}_frag-9_range-0-1"

    payload_field = pa.field(
        "payload",
        pa.large_binary(),
        metadata={b"lance-encoding:blob": b"true"},
    )
    schema = pa.schema(
        [payload_field, pa.field("_rowaddr", pa.uint64())],
        metadata={b"schema-key": b"schema-value"},
    )
    batch = stamp_checkpoint_num_rows(
        pa.record_batch(
            [
                pa.array([b"a", b"b", None, b"d", b"e"], pa.large_binary()),
                pa.array(range(5), pa.uint64()),
            ],
            schema=schema,
        )
    )
    store[key] = batch

    read_calls: list[tuple[int, int, int, int]] = []
    original_read_range = LanceFileReader.read_range

    def tracked_read_range(
        reader: LanceFileReader,
        start: int,
        num_rows: int,
        *,
        batch_size: int = 1024,
        batch_readahead: int = 16,
    ) -> ReaderResults:
        read_calls.append((start, num_rows, batch_size, batch_readahead))
        return original_read_range(
            reader,
            start,
            num_rows,
            batch_size=batch_size,
            batch_readahead=batch_readahead,
        )

    def reject_full_read(
        _reader: LanceFileReader,
        *,
        batch_size: int = 1024,
        batch_readahead: int = 16,
    ) -> ReaderResults:
        del batch_size, batch_readahead
        raise AssertionError("read_range must not materialize the whole checkpoint")

    monkeypatch.setattr(LanceFileReader, "read_range", tracked_read_range)
    monkeypatch.setattr(LanceFileReader, "read_all", reject_full_read)

    middle = store.read_range(key, 1, 2)
    assert middle.column("payload").to_pylist() == [b"b", None]
    assert middle.column("_rowaddr").to_pylist() == [1, 2]
    assert middle.schema.equals(batch.schema, check_metadata=True)
    assert read_checkpoint_num_rows(middle) == 5

    tail = store.read_range(key, 4, 8)
    assert tail.column("payload").to_pylist() == [b"e"]
    assert tail.column("_rowaddr").to_pylist() == [4]
    assert tail.schema.equals(batch.schema, check_metadata=True)

    empty_range = store.read_range(key, 99, 8)
    assert empty_range.num_rows == 0
    assert empty_range.schema.equals(batch.schema, check_metadata=True)

    empty_batch = stamp_checkpoint_num_rows(
        pa.RecordBatch.from_arrays(
            [pa.array([], type=field.type) for field in schema], schema=schema
        )
    )
    store[empty_key] = empty_batch
    empty_checkpoint = store.read_range(empty_key, 0, 0)
    assert empty_checkpoint.num_rows == 0
    assert empty_checkpoint.schema.equals(empty_batch.schema, check_metadata=True)
    assert read_checkpoint_num_rows(empty_checkpoint) == 0

    with pytest.raises(KeyError):
        store.read_range(missing_key, 0, 1)
    with pytest.raises(KeyError):
        store.read_range(missing_key, 0, 0)

    assert read_calls == [
        (1, 2, 2, 1),
        (4, 1, 1, 1),
    ]


def test_multi_base_checkpoint_read_range_delegates_to_bounded_reads(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = MultiBaseCheckpointStore(
        FlatLanceCheckpointStore(str(tmp_path / "default")),
        base_checkpoint_uris={1: str(tmp_path / "base")},
        frag_to_base={7: 1},
    )
    routed_key = f"{_FLAT_KEY_BASE}_frag-7_range-0-5"
    fallback_key = f"{_FLAT_KEY_BASE}_frag-7_range-5-10"
    batch = pa.RecordBatch.from_pydict({"value": list(range(5))})
    store[routed_key] = batch
    # Simulate a checkpoint written at the default root before multi-base
    # routing existed. The router must preserve its fallback lookup while
    # delegating the bounded read to the store that actually contains the key.
    store.default_store[fallback_key] = batch

    read_calls: list[tuple[int, int, int, int]] = []
    original_read_range = LanceFileReader.read_range

    def tracked_read_range(
        reader: LanceFileReader,
        start: int,
        num_rows: int,
        *,
        batch_size: int = 1024,
        batch_readahead: int = 16,
    ) -> ReaderResults:
        read_calls.append((start, num_rows, batch_size, batch_readahead))
        return original_read_range(
            reader,
            start,
            num_rows,
            batch_size=batch_size,
            batch_readahead=batch_readahead,
        )

    def reject_full_read(
        _reader: LanceFileReader,
        *,
        batch_size: int = 1024,
        batch_readahead: int = 16,
    ) -> ReaderResults:
        del batch_size, batch_readahead
        raise AssertionError("multi-base range reads must not read full checkpoints")

    monkeypatch.setattr(LanceFileReader, "read_range", tracked_read_range)
    monkeypatch.setattr(LanceFileReader, "read_all", reject_full_read)

    assert store.read_range(routed_key, 1, 2).column("value").to_pylist() == [1, 2]
    assert store.read_range(fallback_key, 2, 2).column("value").to_pylist() == [2, 3]
    assert read_calls == [(1, 2, 2, 1), (2, 2, 2, 1)]


def test_lance_checkpoint_read_range_restores_blob_v2_metadata(
    tmp_path: Path,
) -> None:
    store = FlatLanceCheckpointStore(str(tmp_path))
    schema = pa.schema(
        [pa.field("_rowaddr", pa.uint64()), lance.blob_field("payload")],
        metadata={b"schema-key": b"schema-value"},
    )
    batch = stamp_checkpoint_num_rows(
        pa.record_batch(
            [
                pa.array(range(3), type=pa.uint64()),
                lance.blob_array([b"a", None, b"c"]),
            ],
            schema=schema,
        )
    )
    store["key"] = batch

    middle = store.read_range("key", 1, 1)
    assert middle.schema.equals(batch.schema, check_metadata=True)
    assert read_checkpoint_num_rows(middle) == 3

    empty = store.read_range("key", batch.num_rows, 0)
    assert empty.num_rows == 0
    assert empty.schema.equals(batch.schema, check_metadata=True)
    assert read_checkpoint_num_rows(empty) == 3


def test_in_memory_checkpoint_read_range_uses_slice_semantics() -> None:
    store = InMemoryCheckpointStore()
    schema = pa.schema([pa.field("value", pa.int64())], metadata={b"key": b"value"})
    batch = stamp_checkpoint_num_rows(
        pa.RecordBatch.from_arrays([pa.array(range(5), pa.int64())], schema=schema)
    )
    store["key"] = batch

    middle = store.read_range("key", 1, 2)
    assert middle.column("value").to_pylist() == [1, 2]
    assert middle.schema.equals(batch.schema, check_metadata=True)
    assert read_checkpoint_num_rows(middle) == 5

    assert store.read_range("key", 4, 8).column("value").to_pylist() == [4]
    empty = store.read_range("key", 99, 8)
    assert empty.num_rows == 0
    assert empty.schema.equals(batch.schema, check_metadata=True)

    with pytest.raises(ValueError, match="start must be non-negative"):
        store.read_range("key", -1, 1)
    with pytest.raises(ValueError, match="row count must be non-negative"):
        store.read_range("key", 0, -1)


@pytest.mark.parametrize("panic_stage", ["metadata", "read_range"])
def test_lance_checkpoint_read_range_converts_reader_panic(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, panic_stage: str
) -> None:
    store = FlatLanceCheckpointStore(str(tmp_path))
    store["key"] = pa.RecordBatch.from_pydict({"value": [1]})

    class PanicException(BaseException):
        pass

    def panic_metadata(_reader: LanceFileReader) -> None:
        raise PanicException("injected Lance metadata panic")

    def panic_read_range(
        _reader: LanceFileReader,
        start: int,
        num_rows: int,
        *,
        batch_size: int = 1024,
        batch_readahead: int = 16,
    ) -> ReaderResults:
        del start, num_rows, batch_size, batch_readahead
        raise PanicException("injected Lance reader panic")

    if panic_stage == "metadata":
        monkeypatch.setattr(LanceFileReader, "metadata", panic_metadata)
        num_rows = 0
    else:
        monkeypatch.setattr(LanceFileReader, "read_range", panic_read_range)
        num_rows = 1

    with pytest.raises(CorruptCheckpointError) as excinfo:
        store.read_range("key", 0, num_rows)

    error = excinfo.value
    assert error.key == "key"
    assert error.path is not None
    assert error.cause is not None
    assert "PanicException" in error.cause


def test_default_ckp_store() -> None:
    store = CheckpointConfig(mode="tempfile").make()
    assert isinstance(store, FlatLanceCheckpointStore)
    assert store.root.startswith(tempfile.gettempdir())


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/delete_test"),
    ],
)
def test_delete_checkpoint(store: CheckpointStore) -> None:
    """Test deleting a single checkpoint."""
    store["key1"] = pa.RecordBatch.from_pydict({"a": [1, 2, 3]})
    assert "key1" in store

    store.delete("key1")
    assert "key1" not in store
    assert "key1" not in list(store.list_keys())
    with pytest.raises(KeyError):
        store["key1"]


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/delete_missing_test"),
    ],
)
def test_delete_nonexistent_key_raises(store: CheckpointStore) -> None:
    """Test that deleting a non-existent key raises KeyError."""
    with pytest.raises(KeyError):
        store.delete("nonexistent")


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/delete_prefix_test"),
    ],
)
def test_delete_prefix(store: CheckpointStore) -> None:
    """Test deleting all checkpoints matching a prefix."""
    batch = pa.RecordBatch.from_pydict({"a": [1]})
    store["job1_frag0"] = batch
    store["job1_frag1"] = batch
    store["job1_frag2"] = batch
    store["job2_frag0"] = batch

    deleted = store.delete_prefix("job1_")
    assert deleted == 3
    assert "job1_frag0" not in store
    assert "job1_frag1" not in store
    assert "job1_frag2" not in store
    assert "job2_frag0" in store


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/delete_prefix_empty_test"),
    ],
)
def test_delete_prefix_no_match(store: CheckpointStore) -> None:
    """Test delete_prefix returns 0 when no keys match."""
    store["key1"] = pa.RecordBatch.from_pydict({"a": [1]})
    deleted = store.delete_prefix("nonexistent_")
    assert deleted == 0
    assert "key1" in store


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/frag_prefix_safety_test"),
    ],
)
def test_delete_prefix_frag_id_is_unambiguous(store: CheckpointStore) -> None:
    """``_range-`` terminator prevents frag-1 prefix from matching frag-10."""
    batch = pa.RecordBatch.from_pydict({"a": [1]})
    base = "udf-x_ver-1_col-c_where-w_uri-u"
    store[f"{base}_frag-1"] = batch
    store[f"{base}_frag-1_range-0-100"] = batch
    store[f"{base}_frag-1_range-100-200"] = batch
    store[f"{base}_frag-10"] = batch
    store[f"{base}_frag-10_range-0-100"] = batch
    store[f"{base}_frag-100_range-0-100"] = batch

    deleted = store.delete_prefix(f"{base}_frag-1_range-")
    assert deleted == 2
    assert f"{base}_frag-1" in store
    assert f"{base}_frag-1_range-0-100" not in store
    assert f"{base}_frag-1_range-100-200" not in store
    assert f"{base}_frag-10" in store
    assert f"{base}_frag-10_range-0-100" in store
    assert f"{base}_frag-100_range-0-100" in store


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/relist_test"),
    ],
)
def test_list_keys_excludes_deleted_includes_rewritten(store: CheckpointStore) -> None:
    """list_keys() drops a deleted key and re-includes it once re-written."""
    batch = pa.RecordBatch.from_pydict({"a": [1]})
    store["k"] = batch
    assert "k" in list(store.list_keys())

    store.delete("k")
    assert "k" not in store
    assert "k" not in list(store.list_keys())

    # Re-writing re-adds the key.
    store["k"] = batch
    assert "k" in store
    assert "k" in list(store.list_keys())


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/purge_test"),
    ],
)
def test_purge_removes_key(store: CheckpointStore) -> None:
    """purge() removes a key and raises KeyError when it does not exist."""
    store["k"] = pa.RecordBatch.from_pydict({"a": [1]})
    assert "k" in store
    store.purge("k")
    assert "k" not in store
    with pytest.raises(KeyError):
        store.purge("missing")


def test_purge_physically_removes_flat_data(tmp_path: Path) -> None:
    """purge() reclaims the data entry on disk."""
    store = FlatLanceCheckpointStore(str(tmp_path))
    store["k"] = pa.RecordBatch.from_pydict({"a": [1]})
    data = tmp_path / "k.lance"
    assert data.exists()

    store.purge("k")
    assert "k" not in store
    assert not data.exists()


def test_delete_physically_removes_flat_data(tmp_path: Path) -> None:
    """delete() physically removes the data entry on disk."""
    store = FlatLanceCheckpointStore(str(tmp_path))
    store["k"] = pa.RecordBatch.from_pydict({"a": [1]})
    assert (tmp_path / "k.lance").exists()

    store.delete("k")
    assert "k" not in store
    assert not (tmp_path / "k.lance").exists()


def test_store_survives_pickle(tmp_path: Path) -> None:
    """The store must round-trip through pickling to Ray workers."""
    store = FlatLanceCheckpointStore(str(tmp_path))
    store["k"] = pa.RecordBatch.from_pydict({"a": [1]})

    rehydrated = pickle.loads(pickle.dumps(store))
    assert rehydrated.root == store.root
    assert "k" in rehydrated
    assert rehydrated["k"].to_pydict() == {"a": [1]}


def test_purge_many_max_workers_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """``CHECKPOINT__PURGE_MANY_MAX_WORKERS`` pins the fan-out (or disables it)."""
    from geneva.checkpoint import _purge_many_max_workers

    monkeypatch.delenv("CHECKPOINT__PURGE_MANY_MAX_WORKERS", raising=False)
    assert _purge_many_max_workers(32) == 32

    monkeypatch.setenv("CHECKPOINT__PURGE_MANY_MAX_WORKERS", "1")
    assert _purge_many_max_workers(32) == 1

    monkeypatch.setenv("CHECKPOINT__PURGE_MANY_MAX_WORKERS", "8")
    assert _purge_many_max_workers(32) == 8

    # Non-numeric falls back to the default (defensive, not a typed config).
    monkeypatch.setenv("CHECKPOINT__PURGE_MANY_MAX_WORKERS", "nope")
    assert _purge_many_max_workers(32) == 32

    # Values below 1 are clamped to 1 (the serial-path threshold).
    monkeypatch.setenv("CHECKPOINT__PURGE_MANY_MAX_WORKERS", "0")
    assert _purge_many_max_workers(32) == 1


# ---------------------------------------------------------------------------
# purge_many (GEN-554) — bulk inline-cleanup hot path
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/purge_many_test"),
    ],
)
def test_purge_many_removes_all_keys(store: CheckpointStore) -> None:
    """``purge_many`` deletes every supplied key across all backends."""
    batch = pa.RecordBatch.from_pydict({"a": [1]})
    keys = [f"k{i}" for i in range(5)]
    for k in keys:
        store[k] = batch

    store.purge_many(keys)
    for k in keys:
        assert k not in store


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/purge_many_missing_test"),
    ],
)
def test_purge_many_tolerates_missing_keys(store: CheckpointStore) -> None:
    """Missing keys are silently skipped (best-effort semantics).

    Mirrors the on-commit cleanup contract: the fragment writer's
    ``cached_tasks`` list may include batch keys an earlier attempt already
    purged, so ``purge_many`` must never raise ``KeyError`` on them.
    """
    batch = pa.RecordBatch.from_pydict({"a": [1]})
    store["present"] = batch

    # Mix of present + missing — no raise, present key is removed.
    store.purge_many(["present", "missing-1", "missing-2"])
    assert "present" not in store


def test_purge_many_empty_keys_is_noop(tmp_path: Path) -> None:
    """``purge_many([])`` must not allocate filesystems or spin a pool."""
    store = FlatLanceCheckpointStore(str(tmp_path))
    # No exception, no side effects.
    store.purge_many([])


def test_purge_many_physically_removes_flat_data(tmp_path: Path) -> None:
    """``purge_many`` removes the data entries on disk.

    Pairs with ``test_purge_physically_removes_flat_data``; that test pins
    the single-key contract, this one pins the bulk path callers from
    ``FragmentWriterManager._record_fragment`` rely on.
    """
    store = FlatLanceCheckpointStore(str(tmp_path))
    batch = pa.RecordBatch.from_pydict({"a": [1]})
    keys = [f"k{i}" for i in range(4)]
    for k in keys:
        store[k] = batch
    for k in keys:
        assert (tmp_path / f"{k}.lance").exists()

    store.purge_many(keys)
    for k in keys:
        assert k not in store
        assert not (tmp_path / f"{k}.lance").exists()


class _CountingSession:
    def __init__(self, wrapped: object) -> None:
        self._wrapped = wrapped
        self.contains_calls: Counter[str] = Counter()

    def contains(self, path: str) -> bool:
        self.contains_calls[path] += 1
        return self._wrapped.contains(path)  # type: ignore[attr-defined]

    def __getattr__(self, name: str) -> object:
        return getattr(self._wrapped, name)


@pytest.mark.parametrize(
    "store_cls",
    [FlatLanceCheckpointStore, HierarchicalLanceCheckpointStore],
)
def test_getitem_after_contains_does_not_repeat_data_contains(
    tmp_path: Path,
    store_cls: type[FlatLanceCheckpointStore],
) -> None:
    """A successful read should not HEAD the checkpoint after ``key in store``."""
    store = store_cls(str(tmp_path))
    key = f"{_FLAT_KEY_BASE}_frag-0_range-0-100"
    store[key] = pa.RecordBatch.from_pydict({"x": [1]})
    path = store._make_path(key)
    session = _CountingSession(store.session)
    store._session = session  # type: ignore[assignment]

    assert key in store
    assert store[key].to_pydict() == {"x": [1]}

    assert session.contains_calls[path] == 1


@pytest.mark.parametrize(
    "store_cls",
    [FlatLanceCheckpointStore, HierarchicalLanceCheckpointStore],
)
def test_getitem_missing_key_raises_keyerror(
    tmp_path: Path,
    store_cls: type[FlatLanceCheckpointStore],
) -> None:
    store = store_cls(str(tmp_path))

    with pytest.raises(KeyError):
        store[f"{_FLAT_KEY_BASE}_frag-404_range-0-100"]


def test_purge_many_issues_one_batched_purge(tmp_path: Path) -> None:
    """Wire test: a bulk ``purge_many`` call issues O(1) batched-purge call.

    Regression guard for the GEN-554 hot path: the call site in
    ``FragmentWriterManager._record_fragment`` used to fan out one
    ``purge(key)`` per batch checkpoint, which on Azure cost ~22s/commit.
    This test asserts the store collapses the whole list into a single
    resolve-fs + bulk-delete call rather than ``len(keys)`` of them.
    """
    store = FlatLanceCheckpointStore(str(tmp_path))
    batch = pa.RecordBatch.from_pydict({"a": [1]})
    keys = [f"k{i}" for i in range(20)]
    for k in keys:
        store[k] = batch

    paths_passed: list[list[str]] = []
    original = store._purge_paths_parallel

    def spy(session_rel_paths: list[str]) -> None:
        paths_passed.append(list(session_rel_paths))
        original(session_rel_paths)

    store._purge_paths_parallel = spy  # type: ignore[method-assign]
    store.purge_many(keys)

    # Exactly one bulk dispatch — not one per key.
    assert len(paths_passed) == 1
    # One data path per key (no marker sidecars).
    assert len(paths_passed[0]) == len(keys)
    for k in keys:
        assert k not in store


def test_hierarchical_purge_many_removes_data(tmp_path: Path) -> None:
    """Hierarchical store inherits ``purge_many`` and removes hierarchical paths."""
    store = HierarchicalLanceCheckpointStore(str(tmp_path))
    batch = pa.RecordBatch.from_pydict({"x": [1]})
    keys = [
        f"{_FLAT_KEY_BASE}_frag-0_range-0-100",
        f"{_FLAT_KEY_BASE}_frag-0_range-100-200",
        f"{_FLAT_KEY_BASE}_frag-1_range-0-100",
    ]
    for k in keys:
        store[k] = batch
    for k in keys:
        assert k in store

    store.purge_many(keys)
    for k in keys:
        assert k not in store

    # Sidecar must survive a purge of just the batch keys (orphan-frag /
    # bf-dir cleanup is out of band).
    bf = _bf_hash()
    assert (tmp_path / f"bf={bf}" / "_identity.json").exists()


def test_checkpoint_store_rehydrates_namespace_session_from_properties(
    tmp_path: Path,
) -> None:
    """Pickled namespace stores should continue writing under the table _ckp dir."""
    from geneva import connect

    db = connect(tmp_path)
    db.create_table("checkpointed", pa.table({"value": [1]}))
    store = FlatLanceCheckpointStore(
        str(tmp_path / "checkpointed.lance" / "_ckp"),
        namespace_client_impl="dir",
        namespace_client_properties={"root": str(tmp_path)},
        table_id=["checkpointed"],
    )
    rehydrated = pickle.loads(pickle.dumps(store))
    batch = pa.record_batch([pa.array([42])], names=["value"])

    rehydrated["frag"] = batch

    assert "frag" in rehydrated
    assert (tmp_path / "checkpointed.lance" / "_ckp" / "frag.lance").exists()
    assert not (tmp_path / "checkpointed.lance" / "frag.lance").exists()


def _seed_checkpoint_store(store: CheckpointStore) -> None:
    """Populate a store with a representative mix of checkpoint keys."""
    batch = pa.RecordBatch.from_pydict({"a": [1]})
    base = "udf-foo_ver-1_col-c_where-w_uri-u"
    # frag 0: has dedupe + two batch keys -> batches should be cleaned
    store[f"{base}_frag-0"] = batch
    store[f"{base}_frag-0_range-0-100"] = batch
    store[f"{base}_frag-0_range-100-200"] = batch
    # frag 1: has batch keys but no dedupe yet -> retained
    store[f"{base}_frag-1_range-0-100"] = batch
    # frag 99: orphaned (no longer in dataset)
    store[f"{base}_frag-99"] = batch
    store[f"{base}_frag-99_range-0-100"] = batch
    # UDTF partition with both _fragment and _batch- keys
    udtf_prefix = "udtf_x_v1_src-1_g=a"
    store[f"{udtf_prefix}_batch-0000"] = batch
    store[f"{udtf_prefix}_batch-0001"] = batch
    store[f"{udtf_prefix}_fragment"] = batch


def test_table_cleanup_checkpoints(tmp_path: Path) -> None:
    """Manual sweep removes redundant batch + orphan-frag + UDTF batch keys."""
    from geneva import connect

    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"id": list(range(8))}))
    # Single fragment with id 0 exists; frag 99 is intentionally orphaned.
    current_frag_ids = {f.fragment_id for f in tbl.to_lance().get_fragments()}
    assert 99 not in current_frag_ids

    store = tbl.get_reference().open_checkpoint_store()
    _seed_checkpoint_store(store)

    counts = tbl.cleanup_checkpoints()

    # frag-0 has 2 batch keys + matching dedupe; frag-99 has 1 batch + matching
    # dedupe — all three batches collapse under their dedupe in pass 1.
    assert counts["batch_deleted"] == 3
    # frag-99 dedupe + frag-1 batch (no dedupe, frag id not in dataset) are
    # the remaining orphans.
    assert counts["orphan_frag_deleted"] == 2
    assert counts["udtf_batch_deleted"] == 2

    base = "udf-foo_ver-1_col-c_where-w_uri-u"
    udtf_prefix = "udtf_x_v1_src-1_g=a"

    assert f"{base}_frag-0" in store  # dedupe key retained
    assert f"{base}_frag-0_range-0-100" not in store
    assert f"{base}_frag-0_range-100-200" not in store
    assert f"{base}_frag-99" not in store
    assert f"{base}_frag-99_range-0-100" not in store
    assert f"{udtf_prefix}_fragment" in store
    assert f"{udtf_prefix}_batch-0000" not in store
    assert f"{udtf_prefix}_batch-0001" not in store


def test_table_cleanup_checkpoints_pass_flags(tmp_path: Path) -> None:
    """Each `_clean_*` flag scopes the sweep to a single pass."""
    from geneva import connect

    base = "udf-foo_ver-1_col-c_where-w_uri-u"
    udtf_prefix = "udtf_x_v1_src-1_g=a"

    # Pass 1 only: batch checkpoints under matching dedupe keys.
    db = connect(tmp_path / "batches")
    tbl = db.create_table("t", pa.table({"id": list(range(8))}))
    store = tbl.get_reference().open_checkpoint_store()
    _seed_checkpoint_store(store)
    counts = tbl.cleanup_checkpoints(
        _clean_batches=True,
        _clean_orphan_fragments=False,
        _clean_udtf_batches=False,
    )
    assert counts == {
        "batch_deleted": 3,
        "orphan_frag_deleted": 0,
        "udtf_batch_deleted": 0,
    }
    # Orphan frag-99 dedupe survives this scoped pass.
    assert f"{base}_frag-99" in store
    assert f"{udtf_prefix}_batch-0000" in store

    # Pass 2 only: orphaned fragment ids.
    db = connect(tmp_path / "orphans")
    tbl = db.create_table("t", pa.table({"id": list(range(8))}))
    store = tbl.get_reference().open_checkpoint_store()
    _seed_checkpoint_store(store)
    counts = tbl.cleanup_checkpoints(
        _clean_batches=False,
        _clean_orphan_fragments=True,
        _clean_udtf_batches=False,
    )
    # frag-99 dedupe + frag-99 batch + frag-1 batch — all reference a missing
    # frag id (only frag 0 exists in the dataset).
    assert counts == {
        "batch_deleted": 0,
        "orphan_frag_deleted": 3,
        "udtf_batch_deleted": 0,
    }
    # Pass 1 was skipped, so batches under matching dedupe survive.
    assert f"{base}_frag-0_range-0-100" in store
    assert f"{udtf_prefix}_batch-0000" in store

    # Pass 3 only: UDTF batch keys with completed partition.
    db = connect(tmp_path / "udtf")
    tbl = db.create_table("t", pa.table({"id": list(range(8))}))
    store = tbl.get_reference().open_checkpoint_store()
    _seed_checkpoint_store(store)
    counts = tbl.cleanup_checkpoints(
        _clean_batches=False,
        _clean_orphan_fragments=False,
        _clean_udtf_batches=True,
    )
    assert counts == {
        "batch_deleted": 0,
        "orphan_frag_deleted": 0,
        "udtf_batch_deleted": 2,
    }
    assert f"{base}_frag-0_range-0-100" in store
    assert f"{base}_frag-99" in store
    assert f"{udtf_prefix}_batch-0000" not in store


# ---------------------------------------------------------------------------
# HierarchicalLanceCheckpointStore (hierarchical layout)
# ---------------------------------------------------------------------------


def _hierarchical_store(tmp_path: Path) -> HierarchicalLanceCheckpointStore:
    return HierarchicalLanceCheckpointStore(str(tmp_path))


def test_v2_parse_key_fragment_and_range() -> None:
    prefix, uri, frag, start, end = _parse_flat_key(f"{_FLAT_KEY_BASE}_frag-7")
    assert prefix == _FLAT_KEY_BASE
    assert uri == "bb"
    assert frag == 7
    assert start is None
    assert end is None

    prefix, uri, frag, start, end = _parse_flat_key(
        f"{_FLAT_KEY_BASE}_frag-3_range-0-100"
    )
    assert prefix == _FLAT_KEY_BASE
    assert uri == "bb"
    assert frag == 3
    assert (start, end) == (0, 100)


def test_v2_parse_key_rejects_udtf_and_malformed() -> None:
    with pytest.raises(ValueError, match="unrecognized checkpoint key"):
        _parse_flat_key("udtf_x_v1_src-1_g=a_batch-0000")
    with pytest.raises(ValueError, match="unrecognized checkpoint key"):
        _parse_flat_key("not-a-checkpoint-key")
    # frag- must be followed by a digit.
    with pytest.raises(ValueError, match="unrecognized checkpoint key"):
        _parse_flat_key(f"{_FLAT_KEY_BASE}_frag-")


def test_v2_make_path_layout(tmp_path: Path) -> None:
    store = _hierarchical_store(tmp_path)
    bf = _bf_hash()
    assert (
        store._make_path(f"{_FLAT_KEY_BASE}_frag-7")
        == f"bf={bf}/fragments/fs={_fragment_shard(7)}/7_src-cc.lance"
    )
    assert (
        store._make_path(f"{_FLAT_KEY_BASE}_frag-3_range-0-100")
        == f"bf={bf}/ranges/fs={_fragment_shard(3)}/3_src-cc/0-100.lance"
    )


def test_v2_fragment_srcfiles_hashes_share_backfill_dir(tmp_path: Path) -> None:
    store = _hierarchical_store(tmp_path)
    batch = pa.RecordBatch.from_pydict({"x": [1]})
    other_base = f"{_FLAT_KEY_BASE_NO_SRC}_srcfiles-dd"
    keys = {
        f"{_FLAT_KEY_BASE}_frag-0",
        f"{other_base}_frag-1",
    }

    for key in keys:
        store[key] = batch

    bf = _bf_hash()
    assert sorted(p.name for p in tmp_path.iterdir() if p.name.startswith("bf=")) == [
        f"bf={bf}"
    ]
    assert len(list(tmp_path.rglob("_identity.json"))) == 1
    assert (
        tmp_path
        / f"bf={bf}"
        / "fragments"
        / f"fs={_fragment_shard(0)}"
        / "0_src-cc.lance"
    ).exists()
    assert (
        tmp_path
        / f"bf={bf}"
        / "fragments"
        / f"fs={_fragment_shard(1)}"
        / "1_src-dd.lance"
    ).exists()
    assert set(store.list_keys()) == keys


def test_v2_round_trip_write_read_list(tmp_path: Path) -> None:
    store = _hierarchical_store(tmp_path)
    batch = pa.RecordBatch.from_pydict({"x": [1, 2, 3]})

    keys = [
        f"{_FLAT_KEY_BASE}_frag-0",
        f"{_FLAT_KEY_BASE}_frag-0_range-0-100",
        f"{_FLAT_KEY_BASE}_frag-0_range-100-200",
        f"{_FLAT_KEY_BASE}_frag-1_range-0-100",
    ]
    for k in keys:
        store[k] = batch

    # Read each back.
    for k in keys:
        assert k in store
        assert store[k].to_pydict() == {"x": [1, 2, 3]}

    # List with and without prefix scoping.
    listed = set(store.list_keys())
    assert listed == set(keys)
    scoped = set(store.list_keys(prefix=_FLAT_KEY_BASE))
    assert scoped == set(keys)
    # A prefix that does not match anything yields nothing.
    assert list(store.list_keys(prefix=f"{_FLAT_KEY_BASE}_frag-99")) == []


def test_hierarchical_round_trips_chunker_fragment_key(tmp_path: Path) -> None:
    """Chunker work-item keys are not UDF frag/range keys but must still work."""
    store = _hierarchical_store(tmp_path)
    batch = pa.RecordBatch.from_pydict({"fragment_json": ["{}"]})
    key = "chunker_clips_abc123_src-42_rowids-100-102_fragment"

    store[key] = batch

    assert key in store
    assert store[key].to_pydict() == {"fragment_json": ["{}"]}
    assert list(store.list_keys(prefix="chunker_clips_abc123_src-42")) == [key]
    assert (tmp_path / "_keys" / f"{key}.lance").exists()

    store.purge(key)
    assert key not in store
    assert not (tmp_path / "_keys" / f"{key}.lance").exists()


def test_hierarchical_generic_prefix_scopes_to_keys_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import geneva.checkpoint as checkpoint_module

    store = _hierarchical_store(tmp_path)
    batch = pa.RecordBatch.from_pydict({"fragment_json": ["{}"]})
    key = "chunker_clips_abc123_src-42_rowids-100-102_fragment"
    store[key] = batch

    scopes: list[str | None] = []
    original_timed_list = checkpoint_module.timed_list

    def _spy_timed_list(
        session: object,
        scope: str | None,
        *,
        op: str,
        layout: str | None = None,
        root: str | None = None,
    ) -> list[str]:
        if op == "list_keys":
            scopes.append(scope)
        return original_timed_list(session, scope, op=op, layout=layout, root=root)

    monkeypatch.setattr(checkpoint_module, "timed_list", _spy_timed_list)

    assert list(store.list_keys(prefix="chunker_clips_abc123_src-42")) == [key]
    assert scopes == ["_keys"]


def test_hierarchical_generic_fallback_rejects_malformed_udf_key(
    tmp_path: Path,
) -> None:
    store = _hierarchical_store(tmp_path)

    with pytest.raises(ValueError, match="unrecognized checkpoint key"):
        store["not-a-checkpoint-key"] = pa.RecordBatch.from_pydict({"x": [1]})


def test_hierarchical_generic_fallback_rejects_malformed_chunker_key(
    tmp_path: Path,
) -> None:
    store = _hierarchical_store(tmp_path)

    with pytest.raises(ValueError, match="unrecognized checkpoint key"):
        store["chunker_clips_abc123_src-42"] = pa.RecordBatch.from_pydict({"x": [1]})


@pytest.mark.parametrize(
    "base",
    [
        _FLAT_KEY_BASE,
        "udf-foo_ver-1_col-c_where-aa_uri-bb",
        "udf-test_frag-x_ver-1_col-c_where-aa_uri-bb_srcfiles-cc",
    ],
)
def test_v2_range_prefix_list_scopes_to_fragment_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, base: str
) -> None:
    """ReadTask resume probes should list one fragment, not the whole bf-dir.

    The setup writes range checkpoints under frag-0 and frag-1. Listing the
    frag-0 range prefix should return only frag-0 ranges and issue one scoped
    LIST against that fragment's range directory.
    """
    import geneva.checkpoint as checkpoint_module

    store = _hierarchical_store(tmp_path)
    batch = pa.RecordBatch.from_pydict({"x": [1]})
    matching = [
        f"{base}_frag-0_range-0-100",
        f"{base}_frag-0_range-100-200",
    ]
    for key in [
        *matching,
        f"{base}_frag-1_range-0-100",
        f"{base}_frag-0",
    ]:
        store[key] = batch

    scopes: list[str | None] = []
    original_timed_list = checkpoint_module.timed_list

    def _spy_timed_list(
        session: object,
        scope: str | None,
        *,
        op: str,
        layout: str | None = None,
        root: str | None = None,
    ) -> list[str]:
        if op == "list_keys":
            scopes.append(scope)
        return original_timed_list(session, scope, op=op, layout=layout, root=root)

    monkeypatch.setattr(checkpoint_module, "timed_list", _spy_timed_list)

    prefix = f"{base}_frag-0_range-"
    assert sorted(store.list_keys(prefix=prefix)) == matching

    bf = _bf_hash(base)
    assert scopes == [
        f"bf={bf}/ranges/fs={_fragment_shard(0)}/{_fragment_identity(0, base)}"
    ]


def test_v2_identity_prefix_with_frag_range_text_lists_bf_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import geneva.checkpoint as checkpoint_module

    base = "udf-test_frag-1_range-x_ver-1_col-c_where-aa_uri-bb_srcfiles-cc"
    store = _hierarchical_store(tmp_path)
    batch = pa.RecordBatch.from_pydict({"x": [1]})
    keys = [
        f"{base}_frag-0",
        f"{base}_frag-0_range-0-100",
        f"{base}_frag-1_range-0-100",
    ]
    for key in keys:
        store[key] = batch

    scopes: list[str | None] = []
    original_timed_list = checkpoint_module.timed_list

    def _spy_timed_list(
        session: object,
        scope: str | None,
        *,
        op: str,
        layout: str | None = None,
        root: str | None = None,
    ) -> list[str]:
        if op == "list_keys":
            scopes.append(scope)
        return original_timed_list(session, scope, op=op, layout=layout, root=root)

    monkeypatch.setattr(checkpoint_module, "timed_list", _spy_timed_list)

    assert sorted(store.list_keys(prefix=base)) == keys
    assert store.delete_prefix(base) == len(keys)
    assert list(store.list_keys(prefix=base)) == []

    bf = _bf_hash(base)
    assert scopes == [
        f"bf={bf}",
        f"bf={bf}",
        f"bf={bf}",
    ]


def test_v2_identity_sidecar_written(tmp_path: Path) -> None:
    store = _hierarchical_store(tmp_path)
    store[f"{_FLAT_KEY_BASE}_frag-0"] = pa.RecordBatch.from_pydict({"x": [1]})
    bf = _bf_hash()
    sidecar = tmp_path / f"bf={bf}" / "_identity.json"
    assert sidecar.is_file(), "expected _identity.json to exist next to data"
    payload = json.loads(sidecar.read_text())
    assert payload["prefix"] == _FLAT_KEY_BASE_NO_SRC
    assert "_srcfiles-" not in payload["prefix"]


def test_v2_purge_many_physically_removes_hierarchical_data(tmp_path: Path) -> None:
    """purge_many must actually reclaim hierarchical checkpoint entries on disk,
    not silently no-op.

    ``_purge_one`` swallows delete failures (to tolerate missing entries), so
    guard that a real delete still happens on a reachable backend — redundant
    per-batch checkpoints must be cleaned up to scale. The delete now routes
    through the blob-only ``session.delete_file``, so it also reclaims storage
    on flat-namespace / unreachable-dfs accounts (GEN-658).
    """
    store = _hierarchical_store(tmp_path)
    keys = [f"{_FLAT_KEY_BASE}_frag-0", f"{_FLAT_KEY_BASE}_frag-1"]
    for key in keys:
        store[key] = pa.RecordBatch.from_pydict({"x": [1]})
    paths = [tmp_path / store._make_path(key) for key in keys]
    assert all(p.exists() for p in paths), "data entries should exist after write"
    assert all(key in store for key in keys)

    store.purge_many(keys)

    for key, path in zip(keys, paths, strict=True):
        assert key not in store, f"{key} should be gone from the store"
        assert not path.exists(), f"{path} should be physically removed"


@pytest.mark.parametrize("exc_type", [FileNotFoundError, OSError])
def test_v2_has_udf_version_mismatch_ignores_missing_fragment_leaf_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, exc_type: type[OSError]
) -> None:
    import geneva.checkpoint as checkpoint_module

    store = _hierarchical_store(tmp_path)
    store[f"{_FLAT_KEY_BASE}_frag-0_range-0-100"] = pa.RecordBatch.from_pydict(
        {"x": [1]}
    )
    original_timed_list = checkpoint_module.timed_list

    def _raise_on_fragment_leaves(
        session: object,
        scope: str | None,
        *,
        op: str,
        layout: str | None = None,
        root: str | None = None,
    ) -> list[str]:
        if op == "list_fragment_leaves":
            raise exc_type("missing fragments")
        return original_timed_list(session, scope, op=op, layout=layout, root=root)

    monkeypatch.setattr(checkpoint_module, "timed_list", _raise_on_fragment_leaves)

    assert store.has_udf_version_mismatch("c", "1") is False


def test_v2_has_udf_version_mismatch_propagates_unexpected_fragment_leaf_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import geneva.checkpoint as checkpoint_module

    store = _hierarchical_store(tmp_path)
    store[f"{_FLAT_KEY_BASE}_frag-0_range-0-100"] = pa.RecordBatch.from_pydict(
        {"x": [1]}
    )
    original_timed_list = checkpoint_module.timed_list

    def _raise_on_fragment_leaves(
        session: object,
        scope: str | None,
        *,
        op: str,
        layout: str | None = None,
        root: str | None = None,
    ) -> list[str]:
        if op == "list_fragment_leaves":
            raise RuntimeError("list failed")
        return original_timed_list(session, scope, op=op, layout=layout, root=root)

    monkeypatch.setattr(checkpoint_module, "timed_list", _raise_on_fragment_leaves)

    with pytest.raises(RuntimeError, match="list failed"):
        store.has_udf_version_mismatch("c", "1")


def test_v2_identity_sidecar_uses_object_store_not_pyarrow_fs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The identity sidecar write and read must not touch PyArrow's
    AzureFileSystem, which probes the dfs.core.windows.net HNS endpoint and
    aborts on flat-namespace / unreachable-dfs accounts (GEN-645).

    Sabotage ``filesystem_from_uri`` at its source so any PyArrow filesystem
    use raises, then assert the sidecar still round-trips through the Lance
    object_store session — the same path the checkpoint data uses.
    """
    import geneva.utils.storage as storage_module

    def _no_pyarrow_fs(*args: object, **kwargs: object) -> tuple[object, str]:
        raise AssertionError(
            "identity sidecar must use the object_store session, not PyArrow fs"
        )

    monkeypatch.setattr(storage_module, "filesystem_from_uri", _no_pyarrow_fs)

    # Write on the driver path (required=True) must succeed without PyArrow fs.
    store = _hierarchical_store(tmp_path)
    store.ensure_identity_sidecar(_FLAT_KEY_BASE)

    bf = _bf_hash()
    sidecar = tmp_path / f"bf={bf}" / "_identity.json"
    assert sidecar.is_file(), "sidecar must be written via the object_store session"
    assert json.loads(sidecar.read_text())["prefix"] == _FLAT_KEY_BASE_NO_SRC

    # Read on a cold store must resolve the identity without PyArrow fs.
    cold = HierarchicalLanceCheckpointStore(str(tmp_path))
    assert cold._read_identity(f"bf={bf}") == _FLAT_KEY_BASE_NO_SRC


def test_v2_iter_bf_identities_enumerates_blob_only_no_pyarrow_fs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """bf-dir enumeration must go through the blob-only object_store session
    (``list_with_delimiter``), never PyArrow's AzureFileSystem, which probes
    the Azure HNS endpoint and aborts on flat-namespace / unreachable-dfs
    accounts. If it silently yielded nothing there, has_udf_version_mismatch /
    has_srcfiles_hash_mismatch would report "no mismatch" and reuse stale
    checkpoints even when the UDF changed (GEN-645/GEN-661).
    """
    import geneva.utils.storage as storage_module

    # Seed a bf= dir with its identity sidecar via the unsabotaged store.
    store = _hierarchical_store(tmp_path)
    store[f"{_FLAT_KEY_BASE}_frag-0"] = pa.RecordBatch.from_pydict({"x": [1]})

    # Cold store; sabotage PyArrow fs so only the blob-only session can satisfy
    # enumeration — proving no HNS probe is on the path.
    cold = HierarchicalLanceCheckpointStore(str(tmp_path))

    def _no_pyarrow_fs(*args: object, **kwargs: object) -> tuple[object, str]:
        raise AssertionError("bf-dir enumeration must not use PyArrow fs")

    monkeypatch.setattr(storage_module, "filesystem_from_uri", _no_pyarrow_fs)

    assert list(cold.iter_bf_identities()) == [(_bf_hash(), _FLAT_KEY_BASE_NO_SRC)]


def test_v2_driver_identity_sidecar_allows_worker_writes_without_sidecar(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    driver = HierarchicalLanceCheckpointStore(str(tmp_path))
    driver.ensure_identity_sidecar(_FLAT_KEY_BASE)

    worker = HierarchicalLanceCheckpointStore(
        str(tmp_path), write_identity_sidecar=False
    )
    sidecar_attempts: list[tuple[str, str]] = []

    def fail_sidecar_write(bf_dir: str, prefix: str) -> None:
        sidecar_attempts.append((bf_dir, prefix))
        raise AssertionError("worker must not try to write identity sidecar")

    monkeypatch.setattr(worker, "_write_identity_if_missing", fail_sidecar_write)

    batch = pa.RecordBatch.from_pydict({"x": [1]})
    keys = [
        f"{_FLAT_KEY_BASE}_frag-0_range-0-100",
        f"{_FLAT_KEY_BASE}_frag-0_range-100-200",
        f"{_FLAT_KEY_BASE}_frag-1",
    ]
    for key in keys:
        worker[key] = batch

    assert sidecar_attempts == []
    assert len(list(tmp_path.rglob("_identity.json"))) == 1
    reader = HierarchicalLanceCheckpointStore(str(tmp_path))
    assert sorted(reader.list_keys(prefix=_FLAT_KEY_BASE)) == sorted(keys)


def test_checkpoint_store_from_uri_can_disable_hierarchical_sidecar_writes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        CheckpointConfig,
        "get",
        classmethod(lambda cls: cls(store_layout="hierarchical")),
    )
    store = CheckpointStore.from_uri(str(tmp_path), write_identity_sidecar=False)
    assert isinstance(store, HierarchicalLanceCheckpointStore)
    assert store.write_identity_sidecar is False


def test_checkpoint_store_from_uri_ignores_sidecar_flag_for_flat(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        CheckpointConfig,
        "get",
        classmethod(lambda cls: cls(store_layout="flat")),
    )
    store = CheckpointStore.from_uri(str(tmp_path), write_identity_sidecar=False)
    assert isinstance(store, FlatLanceCheckpointStore)


def test_v2_list_keys_skips_jobs_subdir(tmp_path: Path) -> None:
    # Manually create a _jobs/ entry to simulate a completion handler write.
    store = _hierarchical_store(tmp_path)
    store[f"{_FLAT_KEY_BASE}_frag-0"] = pa.RecordBatch.from_pydict({"x": [1]})
    bf = _bf_hash()
    jobs_dir = tmp_path / f"bf={bf}" / "_jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    (jobs_dir / "abc.lance").write_bytes(b"")

    keys = list(store.list_keys())
    assert keys == [f"{_FLAT_KEY_BASE}_frag-0"]


def test_v2_delete_single_and_prefix(tmp_path: Path) -> None:
    store = _hierarchical_store(tmp_path)
    batch = pa.RecordBatch.from_pydict({"x": [1]})
    store[f"{_FLAT_KEY_BASE}_frag-0"] = batch
    store[f"{_FLAT_KEY_BASE}_frag-0_range-0-100"] = batch
    store[f"{_FLAT_KEY_BASE}_frag-0_range-100-200"] = batch

    store.delete(f"{_FLAT_KEY_BASE}_frag-0_range-0-100")
    assert f"{_FLAT_KEY_BASE}_frag-0_range-0-100" not in store
    assert f"{_FLAT_KEY_BASE}_frag-0_range-100-200" in store

    # Prefix-scoped delete only matches the range subset.
    removed = store.delete_prefix(f"{_FLAT_KEY_BASE}_frag-0_range-")
    assert removed == 1
    assert f"{_FLAT_KEY_BASE}_frag-0" in store


def test_v2_delete_prefix_identity_removes_whole_bf(tmp_path: Path) -> None:
    """An identity-only prefix deletes every key in its ``bf={H}`` subtree.

    The keys read as absent and stop appearing in ``list_keys``, while a
    sibling backfill identity is unaffected.
    """
    store = _hierarchical_store(tmp_path)
    batch = pa.RecordBatch.from_pydict({"x": [1]})
    store[f"{_FLAT_KEY_BASE}_frag-0"] = batch
    store[f"{_FLAT_KEY_BASE}_frag-0_range-0-100"] = batch
    store[f"{_FLAT_KEY_BASE}_frag-1_range-0-100"] = batch
    # A second backfill identity that must survive.
    other_base = "udf-other_ver-1_col-c_where-aa_uri-bb_srcfiles-zz"
    store[f"{other_base}_frag-0"] = batch

    removed = store.delete_prefix(_FLAT_KEY_BASE)
    assert removed == 3

    # All three keys are logically gone and no longer listed.
    assert f"{_FLAT_KEY_BASE}_frag-0" not in store
    assert f"{_FLAT_KEY_BASE}_frag-0_range-0-100" not in store
    assert f"{_FLAT_KEY_BASE}_frag-1_range-0-100" not in store
    assert list(store.list_keys(_FLAT_KEY_BASE)) == []

    # Other identity is untouched.
    assert f"{other_base}_frag-0" in store


def test_v2_purge_physically_removes_data(tmp_path: Path) -> None:
    """purge() reclaims a hierarchical checkpoint's data entry on disk."""
    store = _hierarchical_store(tmp_path)
    key = f"{_FLAT_KEY_BASE}_frag-0"
    store[key] = pa.RecordBatch.from_pydict({"x": [1]})
    bf = _bf_hash()
    data = (
        tmp_path
        / f"bf={bf}"
        / "fragments"
        / f"fs={_fragment_shard(0)}"
        / "0_src-cc.lance"
    )
    assert data.exists()

    store.purge(key)
    assert key not in store
    assert not data.exists()


def test_v2_list_keys_excludes_deleted_includes_rewritten(tmp_path: Path) -> None:
    """Hierarchical list_keys() drops a deleted key and re-lists it once rewritten."""
    store = _hierarchical_store(tmp_path)
    key = f"{_FLAT_KEY_BASE}_frag-0"
    batch = pa.RecordBatch.from_pydict({"x": [1]})
    store[key] = batch
    assert key in list(store.list_keys())

    store.delete(key)
    assert key not in store
    assert key not in list(store.list_keys())

    store[key] = batch
    assert key in store
    assert key in list(store.list_keys())


def test_v2_delete_prefix_partial_only_matched_keys(tmp_path: Path) -> None:
    """A partial prefix (e.g. one fragment's ranges) only removes the
    matched keys — the rest of the bf-dir survives.
    """
    store = _hierarchical_store(tmp_path)
    batch = pa.RecordBatch.from_pydict({"x": [1]})
    store[f"{_FLAT_KEY_BASE}_frag-0"] = batch
    store[f"{_FLAT_KEY_BASE}_frag-0_range-0-100"] = batch
    store[f"{_FLAT_KEY_BASE}_frag-0_range-100-200"] = batch
    store[f"{_FLAT_KEY_BASE}_frag-1_range-0-100"] = batch

    removed = store.delete_prefix(f"{_FLAT_KEY_BASE}_frag-0_range-")
    assert removed == 2
    assert f"{_FLAT_KEY_BASE}_frag-0" in store
    assert f"{_FLAT_KEY_BASE}_frag-1_range-0-100" in store
    # Identity sidecar must survive a partial delete.
    bf = _bf_hash()
    assert (tmp_path / f"bf={bf}" / "_identity.json").exists()


def test_hierarchical_refuses_root_with_flat_entries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import geneva.checkpoint as checkpoint_module

    # Seed the root with a flat-layout checkpoint and then try to open
    # the hierarchical store against it.
    flat = FlatLanceCheckpointStore(str(tmp_path))
    flat[f"{_FLAT_KEY_BASE}_frag-7"] = pa.RecordBatch.from_pydict({"x": [1]})

    call_scopes: list[str | None] = []
    original_timed_list = checkpoint_module.timed_list

    def _spy_timed_list(
        session: object,
        scope: str | None,
        *,
        op: str,
        layout: str | None = None,
        root: str | None = None,
    ) -> list[str]:
        if op == "coexistence_check":
            call_scopes.append(scope)
        return original_timed_list(session, scope, op=op, layout=layout, root=root)

    monkeypatch.setattr(checkpoint_module, "timed_list", _spy_timed_list)

    hierarchical = HierarchicalLanceCheckpointStore(str(tmp_path))
    with pytest.raises(CheckpointRootMixedLayoutError):
        hierarchical[f"{_FLAT_KEY_BASE}_frag-9"] = pa.RecordBatch.from_pydict(
            {"x": [1]}
        )
    assert call_scopes == [None]


def test_hierarchical_concurrent_first_writes_share_coexistence_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import geneva.checkpoint as checkpoint_module

    store = HierarchicalLanceCheckpointStore(str(tmp_path))
    batch = pa.RecordBatch.from_pydict({"x": [1]})
    call_scopes: list[str | None] = []
    call_lock = threading.Lock()
    start = threading.Barrier(8)
    original_timed_list = checkpoint_module.timed_list

    def _spy_timed_list(
        session: object,
        scope: str | None,
        *,
        op: str,
        layout: str | None = None,
        root: str | None = None,
    ) -> list[str]:
        if op == "coexistence_check":
            with call_lock:
                call_scopes.append(scope)
            # Keep the first check in-flight long enough for peer writers to
            # pile up on the guard; without the lock each would issue LIST.
            time.sleep(0.05)
            return []
        return original_timed_list(session, scope, op=op, layout=layout, root=root)

    monkeypatch.setattr(checkpoint_module, "timed_list", _spy_timed_list)

    keys = [f"{_FLAT_KEY_BASE}_frag-{i}" for i in range(8)]

    def _write(key: str) -> None:
        start.wait()
        store[key] = batch

    with ThreadPoolExecutor(max_workers=len(keys)) as pool:
        list(pool.map(_write, keys))

    assert call_scopes == [None]
    assert set(store.list_keys(prefix=_FLAT_KEY_BASE)) == set(keys)


def test_hierarchical_shares_paths_across_invocations(tmp_path: Path) -> None:
    """Two store instances with the same root must resolve identical paths."""
    a = _hierarchical_store(tmp_path)
    a[f"{_FLAT_KEY_BASE}_frag-0"] = pa.RecordBatch.from_pydict({"x": [1]})

    # Simulate a "second backfill invocation" by constructing a fresh store
    # against the same root. It must see the previous attempt's checkpoint.
    b = HierarchicalLanceCheckpointStore(str(tmp_path))
    assert f"{_FLAT_KEY_BASE}_frag-0" in b


def test_hierarchical_full_uri_no_double_ckp(tmp_path: Path) -> None:
    """Full URIs and the sidecar path built from ``self.root`` must not double
    the ``_ckpv2`` segment.

    In namespace-session mode the session-relative paths carry a leading
    ``_ckpv2/`` while ``self.root`` already ends in ``_ckpv2``; joining them
    naively yields ``.../_ckpv2/_ckpv2/...``. Only surfaces on the namespace
    path, so local-FS round-trip tests can't catch it.
    """
    root = str(tmp_path / "_ckpv2")
    store = HierarchicalLanceCheckpointStore(root)
    bf = _bf_hash()

    # Non-namespace mode: bf-dir has no _ckpv2 prefix, nothing to strip.
    bf_dir = store._bf_dir("bb", bf)
    assert store._full_uri(bf_dir) == f"{root}/bf={bf}"
    # The sidecar is read/written at a session-relative path that is a sibling
    # of the data leaves (same bf-dir), never an absolute URI.
    assert f"{bf_dir}/{store._IDENTITY_FILE}" == f"bf={bf}/_identity.json"
    assert store._make_path(f"{_FLAT_KEY_BASE}_frag-7").startswith(f"{bf_dir}/")

    # Namespace-session mode: bf-dir carries the _ckpv2 prefix; _full_uri must
    # strip it so it isn't doubled against root, and the sidecar rel-path keeps
    # exactly one _ckpv2 segment.
    store._uses_namespace_session = lambda: True  # type: ignore[method-assign]
    bf_dir_ns = store._bf_dir("bb", bf)
    assert bf_dir_ns.startswith("_ckpv2/")
    assert store._full_uri(bf_dir_ns) == f"{root}/bf={bf}"
    assert f"{bf_dir_ns}/{store._IDENTITY_FILE}".count("_ckpv2") == 1
    assert store._make_path(f"{_FLAT_KEY_BASE}_frag-7").startswith(f"{bf_dir_ns}/")


def test_v2_list_bf_dir_leaves_scope_not_doubled_in_namespace_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The delimited LIST in _list_bf_dir_leaves must scope to the bare
    checkpoint root prefix, not a doubled ``_ckpv2/_ckpv2``.

    In namespace mode ``_ckp_root()`` is the bare prefix (no trailing slash); a
    doubled scope lists empty *without raising* on most backends, so
    iter_bf_identities would silently yield nothing -> has_udf_version_mismatch /
    has_srcfiles_hash_mismatch always return "no mismatch" and reuse stale
    checkpoints (GEN-645).
    """
    import types

    import geneva.checkpoint as checkpoint_module

    root = str(tmp_path / "_ckpv2")
    store = HierarchicalLanceCheckpointStore(root)
    store._uses_namespace_session = lambda: True  # type: ignore[method-assign]

    captured: dict[str, object] = {}

    def _capture(
        session: object, scope: object, **kwargs: object
    ) -> types.SimpleNamespace:
        captured["scope"] = scope
        return types.SimpleNamespace(common_prefixes=[], objects=[])

    monkeypatch.setattr(checkpoint_module, "timed_list_with_delimiter", _capture)
    store._list_bf_dir_leaves()

    assert captured["scope"] == "_ckpv2"
    assert str(captured["scope"]).count("_ckpv2") == 1


@pytest.mark.parametrize(
    "corrupt_payload",
    [
        '{"prefix": "udf-',  # truncated JSON (writer crashed mid-write)
        "not json at all",  # bad bytes
        "[1, 2, 3]",  # valid JSON but not an object (.get raises AttributeError)
        '{"prefix": 123}',  # object but prefix is non-string
        "{}",  # object but prefix is absent
    ],
)
def test_hierarchical_read_identity_corrupt_sidecar_cached_as_absent(
    tmp_path: Path, corrupt_payload: str
) -> None:
    """A partial/corrupt ``_identity.json`` is treated as absent, not re-raised.

    A writer that crashed mid-write can leave a truncated or non-object
    sidecar. ``_read_identity`` must return ``None`` and negatively cache it
    (like a 404) so ``list_keys`` doesn't re-read it for every path in the dir
    (GEN-615).
    """
    store = _hierarchical_store(tmp_path)
    store[f"{_FLAT_KEY_BASE}_frag-0"] = pa.RecordBatch.from_pydict({"x": [1]})

    bf_dirs = list(tmp_path.glob("bf=*"))
    assert len(bf_dirs) == 1
    (bf_dirs[0] / "_identity.json").write_text(corrupt_payload)

    # Fresh store starts cold, so the read actually hits the corrupt sidecar.
    cold = HierarchicalLanceCheckpointStore(str(tmp_path))
    bf_dir = bf_dirs[0].name  # "bf={hash}" — same key _read_identity uses

    assert cold._read_identity(bf_dir) is None
    # Absence is cached: the value is recorded as None, not just missing.
    assert bf_dir in cold._identity_cache
    assert cold._identity_cache[bf_dir] is None


def test_config_selects_store_class(tmp_path: Path) -> None:
    """``store_layout="hierarchical"`` selects ``HierarchicalLanceCheckpointStore``."""
    store = CheckpointConfig(
        mode="tempfile",
        store_layout="hierarchical",
    ).make()
    assert type(store) is HierarchicalLanceCheckpointStore
    # Default is flat — exact-type check so a future subclass swap is noticed.
    default_store = CheckpointConfig(mode="tempfile").make()
    assert type(default_store) is FlatLanceCheckpointStore
    # Unknown layout values raise immediately.
    with pytest.raises(ValueError, match="store_layout"):
        CheckpointConfig(mode="tempfile", store_layout="unknown")


# ---------------------------------------------------------------------------
# DEFAULT_TABLE_SUBDIR + TableReference.open_checkpoint_store wiring (GEN-536)
# ---------------------------------------------------------------------------


def test_default_table_subdir_per_class() -> None:
    """Flat keeps ``_ckp`` (backward-compatible); hierarchical lands at a sibling."""
    assert FlatLanceCheckpointStore.DEFAULT_TABLE_SUBDIR == "_ckp"
    assert HierarchicalLanceCheckpointStore.DEFAULT_TABLE_SUBDIR == "_ckpv2"


def test_select_store_class_for_each_layout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``_select_store_class()`` honors the configured layout (and unset = flat).

    Patches ``CheckpointConfig.get`` directly rather than driving the env-var
    loader; the loader walks every required nested field (e.g.
    ``object_store.path``) the moment any ``CHECKPOINT__*`` env var is set,
    which is orthogonal to the layout selection under test.
    """
    for layout, expected in (
        ("flat", FlatLanceCheckpointStore),
        ("hierarchical", HierarchicalLanceCheckpointStore),
    ):
        monkeypatch.setattr(
            CheckpointConfig,
            "get",
            classmethod(lambda cls, _layout=layout: cls(store_layout=_layout)),
        )
        assert _select_store_class() is expected

    # Config unavailable / failing falls back to flat (default).
    def _raise(cls: type) -> "CheckpointConfig":
        raise RuntimeError("config unavailable")

    monkeypatch.setattr(CheckpointConfig, "get", classmethod(_raise))
    assert _select_store_class() is FlatLanceCheckpointStore


def test_hierarchical_at_sibling_subdir_ignores_flat_root(tmp_path: Path) -> None:
    """Hierarchical at ``_ckpv2/`` must not trip on flat entries at ``_ckp/``.

    Regression for GEN-536: before the per-class subdir split, both layouts
    shared ``<table>/_ckp/`` and the hierarchical store's coexistence guard
    fired immediately on any table with pre-existing flat checkpoints.
    """
    flat_root = tmp_path / "_ckp"
    hier_root = tmp_path / "_ckpv2"

    flat = FlatLanceCheckpointStore(str(flat_root))
    flat[f"{_FLAT_KEY_BASE}_frag-7"] = pa.RecordBatch.from_pydict({"x": [1]})
    assert (flat_root / f"{_FLAT_KEY_BASE}_frag-7.lance").exists()

    hierarchical = HierarchicalLanceCheckpointStore(str(hier_root))
    # Writing must succeed — the coexistence guard sees only the sibling root.
    hierarchical[f"{_FLAT_KEY_BASE}_frag-9"] = pa.RecordBatch.from_pydict({"x": [2]})
    assert f"{_FLAT_KEY_BASE}_frag-9" in hierarchical
    # Flat sibling is untouched.
    assert f"{_FLAT_KEY_BASE}_frag-7" in flat


def _patch_layout(monkeypatch: pytest.MonkeyPatch, layout: str) -> None:
    """Force ``CheckpointConfig.get().store_layout`` to a given value for tests."""
    monkeypatch.setattr(
        CheckpointConfig,
        "get",
        classmethod(lambda cls, _layout=layout: cls(store_layout=_layout)),
    )


def test_open_checkpoint_store_uses_per_class_subdir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``TableReference.open_checkpoint_store`` resolves the subdir per layout."""
    from geneva import connect

    monkeypatch.delenv("GENEVA_CHECKPOINT_SUBDIR", raising=False)
    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    tbl_ref = db.open_table("t").get_reference()

    # Flat (default) -> _ckp.
    _patch_layout(monkeypatch, "flat")
    flat_store = tbl_ref.open_checkpoint_store()
    assert type(flat_store) is FlatLanceCheckpointStore
    assert flat_store.root.rstrip("/").endswith("/t.lance/_ckp")

    # Hierarchical -> _ckpv2.
    _patch_layout(monkeypatch, "hierarchical")
    hier_store = tbl_ref.open_checkpoint_store()
    assert type(hier_store) is HierarchicalLanceCheckpointStore
    assert hier_store.root.rstrip("/").endswith("/t.lance/_ckpv2")


def test_open_checkpoint_store_hierarchical_purge_many_uses_table_subdir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Hierarchical write/list/purge all target the per-table checkpoint root."""
    from geneva import connect

    monkeypatch.delenv("GENEVA_CHECKPOINT_SUBDIR", raising=False)
    _patch_layout(monkeypatch, "hierarchical")

    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    store = db.open_table("t").get_reference().open_checkpoint_store()
    assert type(store) is HierarchicalLanceCheckpointStore
    assert store._uses_namespace_session()

    batch = pa.RecordBatch.from_pydict({"x": [1]})
    fragment_key = f"{_FLAT_KEY_BASE}_frag-0"
    range_keys = [
        f"{_FLAT_KEY_BASE}_frag-0_range-0-100",
        f"{_FLAT_KEY_BASE}_frag-0_range-100-200",
    ]
    for key in [fragment_key, *range_keys]:
        store[key] = batch

    bf = _bf_hash()
    hier_root = tmp_path / "t.lance" / "_ckpv2"
    wrong_root = tmp_path / "t.lance" / "_ckp"
    range_dir = (
        hier_root / f"bf={bf}" / "ranges" / f"fs={_fragment_shard(0)}" / "0_src-cc"
    )
    fragment_path = (
        hier_root
        / f"bf={bf}"
        / "fragments"
        / f"fs={_fragment_shard(0)}"
        / "0_src-cc.lance"
    )

    assert set(store.list_keys(_FLAT_KEY_BASE)) == {fragment_key, *range_keys}
    assert list(range_dir.rglob("*.lance"))
    assert fragment_path.exists()
    assert not list(wrong_root.rglob("*.lance"))

    store.purge_many(range_keys)

    assert list(store.list_keys(_FLAT_KEY_BASE)) == [fragment_key]
    assert fragment_key in store
    for key in range_keys:
        assert key not in store
    assert not list(range_dir.rglob("*.lance"))
    assert fragment_path.exists()


def test_open_checkpoint_store_hierarchical_purge_many_uses_nested_table_subdir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Nested checkpoint subdirs must stay relative to the table root."""
    from geneva import connect

    monkeypatch.delenv("GENEVA_CHECKPOINT_SUBDIR", raising=False)
    _patch_config(
        monkeypatch,
        store_layout="hierarchical",
        hierarchical_subdir="_ckp/custom",
    )

    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    store = db.open_table("t").get_reference().open_checkpoint_store()
    assert type(store) is HierarchicalLanceCheckpointStore
    assert store._uses_namespace_session()

    batch = pa.RecordBatch.from_pydict({"x": [1]})
    fragment_key = f"{_FLAT_KEY_BASE}_frag-0"
    range_keys = [
        f"{_FLAT_KEY_BASE}_frag-0_range-0-100",
        f"{_FLAT_KEY_BASE}_frag-0_range-100-200",
    ]
    for key in [fragment_key, *range_keys]:
        store[key] = batch

    bf = _bf_hash()
    hier_root = tmp_path / "t.lance" / "_ckp" / "custom"
    wrong_root = tmp_path / "t.lance" / "custom"
    range_dir = (
        hier_root / f"bf={bf}" / "ranges" / f"fs={_fragment_shard(0)}" / "0_src-cc"
    )
    fragment_path = (
        hier_root
        / f"bf={bf}"
        / "fragments"
        / f"fs={_fragment_shard(0)}"
        / "0_src-cc.lance"
    )

    assert set(store.list_keys(_FLAT_KEY_BASE)) == {fragment_key, *range_keys}
    assert list(range_dir.rglob("*.lance"))
    assert fragment_path.exists()
    assert not list(wrong_root.rglob("*.lance"))

    store.purge_many(range_keys)

    assert list(store.list_keys(_FLAT_KEY_BASE)) == [fragment_key]
    for key in range_keys:
        assert key not in store
    assert not list(range_dir.rglob("*.lance"))
    assert fragment_path.exists()


def test_checkpoint_store_from_uri_preserves_nested_session_root_subdir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Worker-side store rebuilds must keep nested table checkpoint roots."""
    from geneva import connect

    monkeypatch.delenv("GENEVA_CHECKPOINT_SUBDIR", raising=False)
    _patch_config(
        monkeypatch,
        store_layout="hierarchical",
        hierarchical_subdir="_ckp/custom",
    )

    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    store = db.open_table("t").get_reference().open_checkpoint_store()
    assert isinstance(store, HierarchicalLanceCheckpointStore)
    assert store.session_root_subdir == "_ckp/custom"

    rebuilt = CheckpointStore.from_uri(
        store.uri(),
        namespace_client_impl=store.namespace_client_impl,
        namespace_client_properties=store.namespace_client_properties,
        table_id=store.table_id,
        storage_options=store.storage_options,
        session_root_subdir=store.session_root_subdir,
    )
    assert isinstance(rebuilt, HierarchicalLanceCheckpointStore)
    assert rebuilt.session_root_subdir == "_ckp/custom"

    batch = pa.RecordBatch.from_pydict({"x": [1]})
    fragment_key = f"{_FLAT_KEY_BASE}_frag-0"
    range_keys = [
        f"{_FLAT_KEY_BASE}_frag-0_range-0-100",
        f"{_FLAT_KEY_BASE}_frag-0_range-100-200",
    ]
    for key in [fragment_key, *range_keys]:
        rebuilt[key] = batch

    correct_root = tmp_path / "t.lance" / "_ckp" / "custom"
    wrong_root = tmp_path / "t.lance" / "custom"
    assert set(rebuilt.list_keys(_FLAT_KEY_BASE)) == {fragment_key, *range_keys}
    assert list(correct_root.rglob("*.lance"))
    assert not list(wrong_root.rglob("*.lance"))

    rebuilt.purge_many(range_keys)

    assert list(rebuilt.list_keys(_FLAT_KEY_BASE)) == [fragment_key]
    for key in range_keys:
        assert key not in rebuilt


def test_open_checkpoint_store_env_subdir_override(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``GENEVA_CHECKPOINT_SUBDIR`` overrides the per-class default for both layouts."""
    from geneva import connect

    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    tbl_ref = db.open_table("t").get_reference()

    monkeypatch.setenv("GENEVA_CHECKPOINT_SUBDIR", "_ckp_custom")

    # Flat layout honors the override.
    _patch_layout(monkeypatch, "flat")
    flat_store = tbl_ref.open_checkpoint_store()
    assert type(flat_store) is FlatLanceCheckpointStore
    assert flat_store.root.rstrip("/").endswith("/t.lance/_ckp_custom")

    # Hierarchical layout honors the same override.
    _patch_layout(monkeypatch, "hierarchical")
    hier_store = tbl_ref.open_checkpoint_store()
    assert type(hier_store) is HierarchicalLanceCheckpointStore
    assert hier_store.root.rstrip("/").endswith("/t.lance/_ckp_custom")


# ---------------------------------------------------------------------------
# Per-layout config fields exposed via CheckpointConfig (GEN-536 follow-up)
# ---------------------------------------------------------------------------


def test_checkpoint_config_per_layout_subdir_defaults() -> None:
    """``CheckpointConfig`` defaults track the canonical class constants."""
    cfg = CheckpointConfig()
    assert cfg.flat_subdir == FlatLanceCheckpointStore.DEFAULT_TABLE_SUBDIR
    assert (
        cfg.hierarchical_subdir == HierarchicalLanceCheckpointStore.DEFAULT_TABLE_SUBDIR
    )


def _patch_config(
    monkeypatch: pytest.MonkeyPatch,
    *,
    store_layout: str = "flat",
    flat_subdir: str | None = None,
    hierarchical_subdir: str | None = None,
) -> None:
    """Force ``CheckpointConfig.get()`` to a config with the given fields.

    Patches the cached classmethod directly rather than driving the env-var
    loader; the loader eagerly walks every required nested field (e.g.
    ``object_store.path``) the moment any ``CHECKPOINT__*`` env var is set,
    which is orthogonal to the per-layout subdir selection under test.
    """
    kwargs: dict[str, str] = {"store_layout": store_layout}
    if flat_subdir is not None:
        kwargs["flat_subdir"] = flat_subdir
    if hierarchical_subdir is not None:
        kwargs["hierarchical_subdir"] = hierarchical_subdir
    monkeypatch.setattr(
        CheckpointConfig,
        "get",
        classmethod(lambda cls, _kw=kwargs: cls(**_kw)),
    )


def test_open_checkpoint_store_honors_config_flat_subdir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``CheckpointConfig.flat_subdir`` flows through to the resolved URI."""
    from geneva import connect

    monkeypatch.delenv("GENEVA_CHECKPOINT_SUBDIR", raising=False)
    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    tbl_ref = db.open_table("t").get_reference()

    _patch_config(monkeypatch, store_layout="flat", flat_subdir="_ckp_flat_cfg")
    store = tbl_ref.open_checkpoint_store()
    assert type(store) is FlatLanceCheckpointStore
    assert store.root.rstrip("/").endswith("/t.lance/_ckp_flat_cfg")


def test_open_checkpoint_store_honors_config_hierarchical_subdir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``CheckpointConfig.hierarchical_subdir`` flows through to the resolved URI."""
    from geneva import connect

    monkeypatch.delenv("GENEVA_CHECKPOINT_SUBDIR", raising=False)
    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    tbl_ref = db.open_table("t").get_reference()

    _patch_config(
        monkeypatch,
        store_layout="hierarchical",
        hierarchical_subdir="_ckp_hier_cfg",
    )
    store = tbl_ref.open_checkpoint_store()
    assert type(store) is HierarchicalLanceCheckpointStore
    assert store.root.rstrip("/").endswith("/t.lance/_ckp_hier_cfg")


def test_open_checkpoint_store_config_subdir_picks_field_for_layout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Only the field matching the active ``store_layout`` is consulted."""
    from geneva import connect

    monkeypatch.delenv("GENEVA_CHECKPOINT_SUBDIR", raising=False)
    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    tbl_ref = db.open_table("t").get_reference()

    # Set both fields, but expect the flat one to be used.
    _patch_config(
        monkeypatch,
        store_layout="flat",
        flat_subdir="_ckp_flat_cfg",
        hierarchical_subdir="_ckp_hier_cfg",
    )
    flat_store = tbl_ref.open_checkpoint_store()
    assert flat_store.root.rstrip("/").endswith("/t.lance/_ckp_flat_cfg")

    # Flip the layout, same config -> hierarchical_subdir is used instead.
    _patch_config(
        monkeypatch,
        store_layout="hierarchical",
        flat_subdir="_ckp_flat_cfg",
        hierarchical_subdir="_ckp_hier_cfg",
    )
    hier_store = tbl_ref.open_checkpoint_store()
    assert hier_store.root.rstrip("/").endswith("/t.lance/_ckp_hier_cfg")


def test_open_checkpoint_store_blanket_env_beats_config_field(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``GENEVA_CHECKPOINT_SUBDIR`` wins over the per-layout config field."""
    from geneva import connect

    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    tbl_ref = db.open_table("t").get_reference()

    _patch_config(
        monkeypatch,
        store_layout="flat",
        flat_subdir="_ckp_flat_cfg",
        hierarchical_subdir="_ckp_hier_cfg",
    )
    monkeypatch.setenv("GENEVA_CHECKPOINT_SUBDIR", "_ckp_blanket")

    flat_store = tbl_ref.open_checkpoint_store()
    assert flat_store.root.rstrip("/").endswith("/t.lance/_ckp_blanket")

    _patch_config(
        monkeypatch,
        store_layout="hierarchical",
        flat_subdir="_ckp_flat_cfg",
        hierarchical_subdir="_ckp_hier_cfg",
    )
    hier_store = tbl_ref.open_checkpoint_store()
    assert hier_store.root.rstrip("/").endswith("/t.lance/_ckp_blanket")


def test_checkpoint_config_per_layout_subdir_env_vars(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Env-var loader flows ``CHECKPOINT__*_SUBDIR`` into ``CheckpointConfig``.

    Matches the env-var convention already established by the PR's
    ``CHECKPOINT__STORE_LAYOUT`` (``CheckpointConfig.name() == "checkpoint"``).
    Constructs the config directly through ``from_loader`` to bypass the
    ``CheckpointConfig.get`` ``lru_cache`` -- the path under test is that
    the env vars flow into the attrs fields. Also sets
    ``CHECKPOINT__OBJECT_STORE__PATH`` because the env-var loader eagerly
    walks every required nested field the moment any ``CHECKPOINT__*`` env
    var is present, and ``ObjectStoreCheckpointConfig.path`` is required.
    """
    from geneva.config.loader import EnvVarResolver
    from geneva.config.loader import loader as make_loader

    monkeypatch.setenv("CHECKPOINT__FLAT_SUBDIR", "_ckp_flat_env")
    monkeypatch.setenv("CHECKPOINT__HIERARCHICAL_SUBDIR", "_ckp_hier_env")
    monkeypatch.setenv("CHECKPOINT__OBJECT_STORE__PATH", str(tmp_path))

    cfg = CheckpointConfig.from_loader(make_loader(EnvVarResolver()))
    assert cfg.flat_subdir == "_ckp_flat_env"
    assert cfg.hierarchical_subdir == "_ckp_hier_env"


def test_checkpoint_num_rows_stamp_roundtrip() -> None:
    batch = pa.RecordBatch.from_pydict({"a": [1, 2, 3, 4]})
    assert read_checkpoint_num_rows(batch) is None

    stamped = stamp_checkpoint_num_rows(batch)
    assert read_checkpoint_num_rows(stamped) == 4
    # slice preserves the stamp: a truncated batch still records the full count
    assert read_checkpoint_num_rows(stamped.slice(0, 2)) == 4

    stripped = strip_checkpoint_num_rows(stamped)
    assert read_checkpoint_num_rows(stripped) is None
    # stripping an unstamped batch is a no-op
    assert strip_checkpoint_num_rows(batch) is batch


@pytest.mark.parametrize(
    "store",
    [
        InMemoryCheckpointStore(),
        FlatLanceCheckpointStore(f"{tempfile.mkdtemp()}/short_ckpt_test"),
    ],
)
def test_discard_short_checkpoint(store: CheckpointStore) -> None:
    batch = pa.RecordBatch.from_pydict({"a": [1, 2, 3, 4]})

    # a full stamped checkpoint survives the round-trip and is kept
    store["full"] = stamp_checkpoint_num_rows(batch)
    assert not discard_short_checkpoint(store, "full", store["full"])
    assert "full" in store

    # a legacy unstamped checkpoint cannot be validated and is kept
    store["legacy"] = batch
    assert not discard_short_checkpoint(store, "legacy", store["legacy"])
    assert "legacy" in store

    # a short write (stamp says 4 rows, file holds 2) is deleted and reported
    store["short"] = stamp_checkpoint_num_rows(batch).slice(0, 2)
    assert discard_short_checkpoint(store, "short", store["short"])
    assert "short" not in store
