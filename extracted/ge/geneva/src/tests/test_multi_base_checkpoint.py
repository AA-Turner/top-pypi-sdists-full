# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Multi-base placement: fragment checkpoints and staged backfill output
files must land in the storage base holding the fragment's data files."""

import pickle
from pathlib import Path

import lance
import pyarrow as pa
import pytest
from lance import DatasetBasePath

import geneva
from geneva import udf
from geneva.apply.task import BackfillUDFTask
from geneva.apply.utils import _check_fragment_data_file_exists
from geneva.checkpoint import (
    CheckpointStore,
    FlatLanceCheckpointStore,
    InMemoryCheckpointStore,
    MultiBaseCheckpointStore,
    parse_frag_id_from_checkpoint_key,
)
from geneva.runners.ray.writer import (
    build_fragment_checkpoint_batch,
    write_fragment_file,
)
from geneva.utils.multi_base import (
    FragmentBasePlacement,
    lance_supports_multi_base_data_replacement,
    maybe_wrap_checkpoint_store_for_bases,
    resolve_dataset_bases,
    resolve_fragment_bases,
)

BASE_NAME = "b1"


def _make_multi_base_dataset(
    tmp_path: Path, *, rows_per_fragment: int = 8, fragments_per_side: int = 1
) -> tuple[str, str]:
    """`foo` table: fragments 0..n-1 at the dataset root, n..2n-1 in a base.

    Returns (table_uri, base_dir).
    """
    root = str(tmp_path / "foo.lance")
    base_dir = str(tmp_path / "base1")
    side_rows = rows_per_fragment * fragments_per_side
    ds = lance.write_dataset(
        pa.table({"a": list(range(side_rows))}),
        root,
        max_rows_per_file=rows_per_fragment,
        data_storage_version="2.0",
    )
    ds.add_bases([DatasetBasePath(base_dir, name=BASE_NAME, is_dataset_root=True)])
    lance.write_dataset(
        pa.table({"a": list(range(side_rows, 2 * side_rows))}),
        root,
        mode="append",
        max_rows_per_file=rows_per_fragment,
        target_bases=[BASE_NAME],
        data_storage_version="2.0",
    )
    return root, base_dir


def _frag_key(frag_id: int, *, batch: bool = False) -> str:
    key = f"udf-x_ver-1_col-b_where-e3b0_uri-e3b0_srcfiles-abc123_frag-{frag_id}"
    return f"{key}_range-0-4" if batch else key


def _batch() -> pa.RecordBatch:
    return pa.RecordBatch.from_pydict({"v": [1]})


# ---------------------------------------------------------------------------
# Placement resolution
# ---------------------------------------------------------------------------


def test_resolve_bases_and_fragment_bases(tmp_path: Path) -> None:
    root, base_dir = _make_multi_base_dataset(tmp_path)
    ds = lance.dataset(root)

    bases = resolve_dataset_bases(ds)
    assert set(bases) == {1}
    assert bases[1].uri == base_dir
    assert bases[1].is_dataset_root
    assert bases[1].data_dir == f"{base_dir}/data"
    assert bases[1].checkpoint_root("_ckp") == f"{base_dir}/_ckp"

    frag_to_base = resolve_fragment_bases(ds.get_fragments())
    assert frag_to_base == {1: 1}

    placement = FragmentBasePlacement.from_dataset(ds)
    assert placement is not None
    assert placement.base_id_for_frag(0) is None
    assert placement.base_id_for_frag(1) == 1
    assert placement.data_dir_for_frag(0) is None
    assert placement.data_dir_for_frag(1) == f"{base_dir}/data"
    assert placement.base_data_dirs() == {1: f"{base_dir}/data"}
    assert placement.base_checkpoint_uris("_ckp") == {1: f"{base_dir}/_ckp"}


def test_placement_none_for_single_base_dataset(tmp_path: Path) -> None:
    root = str(tmp_path / "plain.lance")
    ds = lance.write_dataset(pa.table({"a": [1, 2, 3]}), root)
    assert resolve_dataset_bases(ds) == {}
    assert FragmentBasePlacement.from_dataset(ds) is None


def test_non_dataset_root_base_data_dir() -> None:
    from geneva.utils.multi_base import DatasetBaseInfo

    info = DatasetBaseInfo(base_id=2, uri="s3://bucket/dir", is_dataset_root=False)
    assert info.data_dir == "s3://bucket/dir"
    assert info.checkpoint_root("_ckp") == "s3://bucket/dir/_ckp"


def test_dataset_root_base_dirs_preserve_uri_query() -> None:
    from geneva.utils.multi_base import DatasetBaseInfo

    # An object-store URI may carry credentials in its query (e.g. an Azure
    # SAS token); appending a subdirectory must not drop it, or the per-base
    # file session built from it reads unauthenticated.
    info = DatasetBaseInfo(
        base_id=0,
        uri="az://container/table.lance?sv=abc&sig=xyz",
        is_dataset_root=True,
    )
    assert info.data_dir == "az://container/table.lance/data?sv=abc&sig=xyz"
    assert (
        info.checkpoint_root("_ckp") == "az://container/table.lance/_ckp?sv=abc&sig=xyz"
    )


# ---------------------------------------------------------------------------
# MultiBaseCheckpointStore routing
# ---------------------------------------------------------------------------


def _make_router(tmp_path: Path) -> MultiBaseCheckpointStore:
    default = FlatLanceCheckpointStore(str(tmp_path / "root_ckp"))
    return MultiBaseCheckpointStore(
        default,
        base_checkpoint_uris={1: str(tmp_path / "base1_ckp")},
        frag_to_base={1: 1, 3: 1},
    )


def test_router_routes_by_fragment(tmp_path: Path) -> None:
    router = _make_router(tmp_path)

    router[_frag_key(0)] = _batch()  # unmapped frag -> default store
    router[_frag_key(1)] = _batch()  # mapped frag -> base store
    router[_frag_key(1, batch=True)] = _batch()
    router["udtf_x_1_src-2__all___batch-0001"] = _batch()  # no frag -> default

    default, base = router.default_store, router.base_stores[1]
    assert _frag_key(0) in default
    assert _frag_key(0) not in base
    assert _frag_key(1) in base
    assert _frag_key(1) not in default
    assert _frag_key(1, batch=True) in base
    assert "udtf_x_1_src-2__all___batch-0001" in default

    # router-level reads see both stores
    assert _frag_key(0) in router
    assert _frag_key(1) in router
    assert router[_frag_key(1)].num_rows == 1

    keys = set(router.list_keys())
    assert keys == {
        _frag_key(0),
        _frag_key(1),
        _frag_key(1, batch=True),
        "udtf_x_1_src-2__all___batch-0001",
    }


def test_router_read_fallback_to_default(tmp_path: Path) -> None:
    """Pre-upgrade checkpoints live at the table root; reads must find them
    even for fragments now routed to a base."""
    router = _make_router(tmp_path)
    router.default_store[_frag_key(1)] = _batch()

    assert _frag_key(1) in router
    assert router[_frag_key(1)].num_rows == 1
    router.delete(_frag_key(1))
    assert _frag_key(1) not in router


def test_router_purge_fallback_across_stores(tmp_path: Path) -> None:
    """Orphaned fragments (dropped from the manifest) route to the default
    store but their checkpoints may live in a base store."""
    router = _make_router(tmp_path)
    orphan_key = _frag_key(9)  # frag 9 unmapped -> routes to default
    router.base_stores[1][orphan_key] = _batch()

    assert orphan_key in router
    router.purge(orphan_key)
    assert orphan_key not in router.base_stores[1]

    with pytest.raises(KeyError):
        router.purge(orphan_key)


def test_router_delete_and_purge_remove_all_copies(tmp_path: Path) -> None:
    """A transient routing failure (or a pre-upgrade run) can leave the same
    key in both the table root and its base; delete/purge must remove every
    copy or cleanup leaves a stale duplicate behind."""
    router = _make_router(tmp_path)
    router.default_store[_frag_key(1)] = _batch()
    router.base_stores[1][_frag_key(1)] = _batch()

    router.purge(_frag_key(1))
    assert _frag_key(1) not in router.default_store
    assert _frag_key(1) not in router.base_stores[1]
    with pytest.raises(KeyError):
        router.purge(_frag_key(1))

    router.default_store[_frag_key(3)] = _batch()
    router.base_stores[1][_frag_key(3)] = _batch()
    router.delete(_frag_key(3))
    assert _frag_key(3) not in router
    with pytest.raises(KeyError):
        router.delete(_frag_key(3))


def test_router_purge_many_groups_by_store(tmp_path: Path) -> None:
    router = _make_router(tmp_path)
    keys = [_frag_key(0), _frag_key(1), _frag_key(3, batch=True)]
    for key in keys:
        router[key] = _batch()
    router.purge_many(keys)
    assert list(router.list_keys()) == []


def test_router_pickle_roundtrip(tmp_path: Path) -> None:
    router = _make_router(tmp_path)
    router[_frag_key(1)] = _batch()

    restored = pickle.loads(pickle.dumps(router))
    assert isinstance(restored, MultiBaseCheckpointStore)
    assert restored.frag_to_base == {1: 1, 3: 1}
    assert _frag_key(1) in restored


def test_from_uri_builds_router(tmp_path: Path) -> None:
    store = CheckpointStore.from_uri(
        str(tmp_path / "root_ckp"),
        base_checkpoint_uris={1: str(tmp_path / "base1_ckp")},
        frag_to_base={1: 1},
    )
    assert isinstance(store, MultiBaseCheckpointStore)
    assert store.uri() == str(tmp_path / "root_ckp")

    plain = CheckpointStore.from_uri(str(tmp_path / "root_ckp2"))
    assert isinstance(plain, FlatLanceCheckpointStore)

    memory = CheckpointStore.from_uri(
        "memory", base_checkpoint_uris={1: "x"}, frag_to_base={1: 1}
    )
    assert isinstance(memory, InMemoryCheckpointStore)


def test_maybe_wrap_checkpoint_store(tmp_path: Path) -> None:
    root, base_dir = _make_multi_base_dataset(tmp_path)
    placement = FragmentBasePlacement.from_dataset(lance.dataset(root))
    store = FlatLanceCheckpointStore(f"{root}/_ckp")

    wrapped = maybe_wrap_checkpoint_store_for_bases(store, placement)
    assert isinstance(wrapped, MultiBaseCheckpointStore)
    assert wrapped.base_checkpoint_uris == {1: f"{base_dir}/_ckp"}
    assert wrapped.frag_to_base == {1: 1}
    # idempotent
    assert maybe_wrap_checkpoint_store_for_bases(wrapped, placement) is wrapped
    # no placement / in-memory store -> unchanged
    assert maybe_wrap_checkpoint_store_for_bases(store, None) is store
    mem = InMemoryCheckpointStore()
    assert maybe_wrap_checkpoint_store_for_bases(mem, placement) is mem


def test_parse_frag_id_from_checkpoint_key() -> None:
    assert parse_frag_id_from_checkpoint_key(_frag_key(7)) == 7
    assert parse_frag_id_from_checkpoint_key(_frag_key(7, batch=True)) == 7
    assert parse_frag_id_from_checkpoint_key("a" * 64) is None  # legacy sha256
    assert parse_frag_id_from_checkpoint_key("udtf_x_1_src-2_fragment") is None


def test_unwrap_default_checkpoint_store(tmp_path: Path) -> None:
    from geneva.checkpoint import unwrap_default_checkpoint_store

    router = _make_router(tmp_path)
    assert unwrap_default_checkpoint_store(router) is router.default_store
    plain = FlatLanceCheckpointStore(str(tmp_path / "plain_ckp"))
    assert unwrap_default_checkpoint_store(plain) is plain


def test_router_mismatch_detection_spans_base_stores(tmp_path: Path) -> None:
    """UDF-version / srcfiles mismatch checks must see base-routed fragment
    checkpoints (stale-data protection on re-backfill)."""
    router = _make_router(tmp_path)
    # Fragment 1 routes to the base store; its dedupe key encodes _ver-1.
    router[_frag_key(1)] = _batch()
    assert _frag_key(1) in router.base_stores[1]

    assert not router.has_udf_version_mismatch("b", "1")
    assert router.has_udf_version_mismatch("b", "2")
    assert not router.has_srcfiles_hash_mismatch("b", "abc123")
    assert router.has_srcfiles_hash_mismatch("b", "def456")


def test_router_srcfiles_mismatch_uses_union_across_stores(tmp_path: Path) -> None:
    """Per-fragment srcfiles hashes are spread across stores; the check is
    "current not in the UNION". Any-child delegation would spuriously report
    a mismatch (and force a full recompute) whenever one store lacks the
    probed hash."""
    router = _make_router(tmp_path)
    # Fragment 0 (root store) hash abc123; fragment 1 (base store) hash beef99.
    router[_frag_key(0)] = _batch()
    key_frag1 = "udf-x_ver-1_col-b_where-e3b0_uri-e3b0_srcfiles-beef99_frag-1"
    router[key_frag1] = _batch()
    assert key_frag1 in router.base_stores[1]

    assert not router.has_srcfiles_hash_mismatch("b", "abc123")
    assert not router.has_srcfiles_hash_mismatch("b", "beef99")
    assert router.has_srcfiles_hash_mismatch("b", "def456")


# ---------------------------------------------------------------------------
# Staged file write + probe
# ---------------------------------------------------------------------------


def test_write_fragment_file_into_base(tmp_path: Path) -> None:
    root, base_dir = _make_multi_base_dataset(tmp_path)
    data_dir = f"{base_dir}/data"

    data_file, rows, _ms = write_fragment_file(
        root,
        iter([pa.RecordBatch.from_pydict({"b": [1, 2, 3]})]),
        column_names=["b"],
        field_ids=[1],
        column_indices=[0],
        data_storage_version="2.0",
        data_dir=data_dir,
        base_id=1,
    )
    assert rows == 3
    assert data_file.base_id == 1
    assert (Path(data_dir) / data_file.path).exists()
    assert not (Path(root) / "data" / data_file.path).exists()


def test_fragment_checkpoint_batch_base_id_roundtrip() -> None:
    batch = build_fragment_checkpoint_batch(file_path="f.lance", base_id=3)
    assert batch["base_id"][0].as_py() == 3
    legacy = build_fragment_checkpoint_batch(file_path="f.lance")
    assert "base_id" not in legacy.schema.names


@udf(data_type=pa.int32())
def _times_ten(a: int) -> int:
    return a * 10


def test_probe_finds_staged_file_in_base(tmp_path: Path) -> None:
    """A staged-but-uncommitted output file in a base must be found via the
    payload base_id, and the probe must return that base_id so the resume
    commit points at the right base."""
    from geneva.runners.ray.pipeline import _get_fragment_dedupe_key

    root, base_dir = _make_multi_base_dataset(tmp_path)
    store = FlatLanceCheckpointStore(str(tmp_path / "ckp"))
    map_task = BackfillUDFTask(udfs={"b": _times_ten})

    from lance.file import LanceFileWriter

    staged = Path(base_dir) / "data" / "staged_b.lance"
    with LanceFileWriter(str(staged)) as writer:
        writer.write_batch(pa.table({"b": [10, 20, 30]}).to_batches()[0])

    dedupe_key = _get_fragment_dedupe_key(root, 1, map_task)
    store[dedupe_key] = build_fragment_checkpoint_batch(
        file_path="staged_b.lance", base_id=1
    )

    base_dirs = {1: f"{base_dir}/data"}
    checked = _check_fragment_data_file_exists(
        root, 1, map_task, store, expected_rows=3, base_dirs=base_dirs
    )
    assert checked == ("staged_b.lance", 1)

    # Unknown base id in the payload invalidates the checkpoint.
    checked = _check_fragment_data_file_exists(
        root, 1, map_task, store, expected_rows=3, base_dirs=None
    )
    assert checked is None


def test_probe_root_payload_unchanged(tmp_path: Path) -> None:
    """Payloads without base_id keep probing {uri}/data (pre-upgrade)."""
    from geneva.runners.ray.pipeline import _get_fragment_dedupe_key

    root, base_dir = _make_multi_base_dataset(tmp_path)
    store = FlatLanceCheckpointStore(str(tmp_path / "ckp"))
    map_task = BackfillUDFTask(udfs={"b": _times_ten})

    from lance.file import LanceFileWriter

    staged = Path(root) / "data" / "staged_root.lance"
    with LanceFileWriter(str(staged)) as writer:
        writer.write_batch(pa.table({"b": [1, 2, 3]}).to_batches()[0])

    dedupe_key = _get_fragment_dedupe_key(root, 0, map_task)
    store[dedupe_key] = build_fragment_checkpoint_batch(file_path="staged_root.lance")

    checked = _check_fragment_data_file_exists(
        root, 0, map_task, store, expected_rows=3, base_dirs={1: f"{base_dir}/data"}
    )
    assert checked == ("staged_root.lance", None)


# ---------------------------------------------------------------------------
# End-to-end backfill
# ---------------------------------------------------------------------------


def _assert_multi_base_backfill(
    tmp_path: Path, root: str, base_dir: str, **backfill_kwargs
) -> None:
    db = geneva.connect(str(tmp_path))
    tbl = db.open_table("foo")
    tbl.add_columns({"b": _times_ten})
    tbl.backfill("b", **backfill_kwargs)
    tbl.checkout_latest()

    size = tbl.count_rows()
    data = tbl.to_arrow().to_pydict()
    assert data["b"] == [a * 10 for a in data["a"]]

    from geneva.utils.multi_base import lance_supports_multi_base_data_replacement

    data_placement = lance_supports_multi_base_data_replacement()
    ds = lance.dataset(root)
    output_paths: dict[int, str] = {}
    for frag in ds.get_fragments():
        files = frag.data_files()
        frag_base = files[0].base_id
        out_files = list(files[1:])
        assert len(out_files) == 1, f"fragment {frag.fragment_id}: {files}"
        out = out_files[0]
        output_paths[frag.fragment_id] = out.path
        # Output data files follow the fragment's base only when the
        # installed pylance can commit DataReplacement into bases.
        expected_base = frag_base if data_placement else None
        assert out.base_id == expected_base, (
            f"fragment {frag.fragment_id} output file base {out.base_id} != "
            f"expected {expected_base}"
        )
        data_root = Path(base_dir if expected_base == 1 else root) / "data"
        assert (data_root / out.path).exists()

    # Fragment dedupe checkpoints live with their fragment's base.
    root_keys = {p.stem for p in (Path(root) / "_ckp").glob("*.lance")}
    base_ckp = Path(base_dir) / "_ckp"
    base_keys = (
        {p.stem for p in base_ckp.glob("*.lance")} if base_ckp.exists() else set()
    )
    frag_bases = {
        frag.fragment_id: frag.data_files()[0].base_id for frag in ds.get_fragments()
    }
    assert any(base_id == 1 for base_id in frag_bases.values())
    for frag_id, frag_base in frag_bases.items():
        expected, other = (
            (base_keys, root_keys) if frag_base == 1 else (root_keys, base_keys)
        )
        assert any(parse_frag_id_from_checkpoint_key(k) == frag_id for k in expected), (
            f"fragment {frag_id} dedupe checkpoint missing from its base store"
        )
        assert not any(
            parse_frag_id_from_checkpoint_key(k) == frag_id for k in other
        ), f"fragment {frag_id} checkpoint leaked into the wrong store"

    # Re-run: every fragment must be skipped via its dedupe checkpoint —
    # the committed output files stay byte-identical (same uuid paths).
    tbl.backfill("b", **backfill_kwargs)
    tbl.checkout_latest()
    ds = lance.dataset(root)
    for frag in ds.get_fragments():
        files = frag.data_files()
        assert [f.path for f in files[1:]] == [output_paths[frag.fragment_id]]
        if data_placement:
            assert files[1].base_id == files[0].base_id
    assert tbl.count_rows() == size
    data = tbl.to_arrow().to_pydict()
    assert data["b"] == [a * 10 for a in data["a"]]


# Multi-base backfill needs a pylance whose DataReplacement commit is
# base-aware: older versions fail in lance's commit path (file-size stat of
# base fragments resolves against the dataset root) before geneva placement
# even matters.
requires_multi_base_lance = pytest.mark.skipif(
    not lance_supports_multi_base_data_replacement(),
    reason="installed pylance cannot commit DataReplacement on multi-base datasets",
)


@pytest.mark.ray
@requires_multi_base_lance
def test_backfill_multi_base_writer_path(tmp_path: Path, local_ray_context) -> None:
    """checkpoint_size < fragment rows: batch checkpoints flow through the
    FragmentWriter actor, which reads them from the fragment's base store."""
    root, base_dir = _make_multi_base_dataset(
        tmp_path, rows_per_fragment=8, fragments_per_side=2
    )
    _assert_multi_base_backfill(
        tmp_path,
        root,
        base_dir,
        batch_size=4,
        min_checkpoint_size=4,
        max_checkpoint_size=4,
    )


@pytest.mark.ray
@requires_multi_base_lance
def test_backfill_multi_base_direct_path(tmp_path: Path, local_ray_context) -> None:
    """Default sizing: single-batch fragments take the direct fragment write
    fast path on the applier."""
    root, base_dir = _make_multi_base_dataset(
        tmp_path, rows_per_fragment=8, fragments_per_side=2
    )
    _assert_multi_base_backfill(tmp_path, root, base_dir)


# ---------------------------------------------------------------------------
# Compaction vs placement / routing
# ---------------------------------------------------------------------------


def test_resolve_fragment_bases_after_compaction(tmp_path: Path) -> None:
    """Lance compacts multi-base datasets by writing the merged fragment's
    single data file at the dataset root (base_id=None), pulling
    base-resident data back to the root (as of pylance 9.0.0-beta.21).
    Placement follows the new fragment's first data file: it maps to no
    base, so its checkpoint keys route to the default store, and with no
    base holding a fragment the store wrapper stays a plain store. A router
    built before the compaction keeps routing the removed fragment's keys to
    its base — the reason orphan cleanup relies on read/purge fallbacks that
    span every store."""
    root, base_dir = _make_multi_base_dataset(tmp_path)
    ds = lance.dataset(root)
    assert resolve_fragment_bases(ds.get_fragments()) == {1: 1}
    pre_frag_ids = {frag.fragment_id for frag in ds.get_fragments()}

    metrics = ds.optimize.compact_files()
    assert metrics.fragments_removed == 2
    assert metrics.fragments_added == 1

    ds = lance.dataset(root)
    frags = ds.get_fragments()
    assert len(frags) == 1
    new_frag = frags[0]
    assert new_frag.fragment_id not in pre_frag_ids
    assert [df.base_id for df in new_frag.data_files()] == [None]
    assert ds.to_table()["a"].to_pylist() == list(range(16))

    # frag_to_base follows the first data file's base: root -> unmapped.
    assert resolve_fragment_bases(frags) == {}
    placement = FragmentBasePlacement.from_dataset(ds)
    assert placement is not None  # base_paths persists in the manifest
    assert set(placement.bases) == {1}
    assert placement.frag_to_base == {}
    assert placement.base_id_for_frag(new_frag.fragment_id) is None

    # Rebuilding the store wrapper from post-compaction placement yields no
    # router at all: no base holds a fragment, so the store stays plain.
    store = FlatLanceCheckpointStore(f"{root}/_ckp")
    assert maybe_wrap_checkpoint_store_for_bases(store, placement) is store

    # A router built from the PRE-compaction placement (a job that outlives
    # the compaction) routes new-fragment keys to the default store and the
    # removed base fragment's keys to its base store.
    stale_router = MultiBaseCheckpointStore(
        store,
        base_checkpoint_uris={1: f"{base_dir}/_ckp"},
        frag_to_base={1: 1},
    )
    new_key = _frag_key(new_frag.fragment_id)
    assert stale_router._store_for_key(new_key) is stale_router.default_store
    assert stale_router._store_for_key(_frag_key(1)) is stale_router.base_stores[1]


@pytest.mark.ray
@pytest.mark.multibackfill
@requires_multi_base_lance
def test_multi_base_backfill_resume_after_compaction(
    tmp_path: Path, local_ray_context
) -> None:
    """A backfill resumed after compaction stays correct on a multi-base
    dataset.

    Compaction merges the root- and base-side fragments into one root
    fragment (renumbering fragments, so the first run's per-fragment
    checkpoints no longer apply) and folds the partially filled 'b' column
    into the merged data file. The resume must recompute and commit against
    the merged fragment without routing errors and leave b == a * 10
    everywhere."""
    root, base_dir = _make_multi_base_dataset(
        tmp_path, rows_per_fragment=8, fragments_per_side=2
    )
    db = geneva.connect(str(tmp_path))
    tbl = db.open_table("foo")
    tbl.add_columns({"b": _times_ten})

    # Partial leg: only the root-side fragments (rows 0..15).
    tbl.backfill("b", where="a < 16")
    tbl.checkout_latest()
    data = tbl.to_arrow().to_pydict()
    assert [b for a, b in zip(data["a"], data["b"], strict=True) if a < 16] == [
        a * 10 for a in range(16)
    ]
    # The base-side rows must still be unfilled: if the predicate were ignored
    # the "resume" below would be a no-op and the test would prove nothing.
    filled_early = sorted(
        a
        for a, b in zip(data["a"], data["b"], strict=True)
        if a >= 16 and b is not None
    )
    assert not filled_early, (
        f"first leg ignored where='a < 16': rows {filled_early[:5]} already filled"
    )

    tbl.compact_files()
    tbl.checkout_latest()
    ds = lance.dataset(root)
    assert len(ds.get_fragments()) == 1

    # Resume: fill the remaining rows against the merged fragment.
    tbl.backfill("b")
    tbl.checkout_latest()
    data = tbl.to_arrow().to_pydict()
    assert data["b"] == [a * 10 for a in data["a"]]
    assert sorted(data["a"]) == list(range(32))
