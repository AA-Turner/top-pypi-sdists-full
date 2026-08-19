# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for the loose-object upload job (LocalFileWriter — no Azure)."""

from __future__ import annotations

from typing import Any

import pyarrow as pa
import pytest

from loadtest.azure_scale_bench import (
    benchmark_env,
    constants,
    synthetic_image,
    upload_images,
)
from loadtest.azure_scale_bench.benchmark_env import BenchConfig
from loadtest.azure_scale_bench.object_writer import LocalFileWriter, ObjectStat


def _cfg(**overrides: Any) -> BenchConfig:
    base: dict[str, Any] = {
        "seed_run_id": "run1",
        "accounts": ("acctA", "acctB"),
        "loose_container": "cont",
        "base_prefix": "pre",
        "prefix_count": 16,
        "image_format": "png",
        "object_count": 8,
    }
    base.update(overrides)
    return BenchConfig(**base)


def _mk_params(cfg: BenchConfig | None = None) -> upload_images._UploadParams:
    cfg = cfg or _cfg()
    assert cfg.seed_run_id is not None
    return upload_images._params(cfg, upload_images._seed_run_salt(cfg.seed_run_id))


class _CountingWriter:
    """Wrap an ObjectWriter and count SUCCESSFUL puts (to assert idempotent skips).

    A conditional-create that raises ``ObjectExistsError`` is not counted, so a
    re-upload of an existing object registers no new write.
    """

    def __init__(self, inner: LocalFileWriter) -> None:
        self.inner = inner
        self.puts = 0

    def head(self, key: str) -> ObjectStat | None:
        return self.inner.head(key)

    def put(
        self,
        key: str,
        data: bytes,
        *,
        content_type: str,
        content_md5: str | None = None,
        overwrite: bool = True,
    ) -> str:
        etag = self.inner.put(
            key,
            data,
            content_type=content_type,
            content_md5=content_md5,
            overwrite=overwrite,
        )
        self.puts += 1
        return etag


def test_derivation_is_deterministic_and_scoped() -> None:
    p = _mk_params()
    assert upload_images.account_for(42, p) == upload_images.account_for(42, p)
    pid = upload_images.prefix_id_for(42, p)
    key = upload_images.object_key_for(42, pid, p)
    assert key == f"pre/run1/p{pid:05d}/42.png"
    assert upload_images.url_for(key, p) == f"az://cont/{key}"
    assert 0 <= pid < p.prefix_count
    assert upload_images.account_for(42, p) in p.accounts


def test_seed_run_changes_scatter() -> None:
    # Different seed-run ids scatter the same image to (generally) different keys.
    a = _mk_params(_cfg(seed_run_id="runA"))
    b = _mk_params(_cfg(seed_run_id="runB"))
    keys_a = {
        upload_images.object_key_for(i, upload_images.prefix_id_for(i, a), a)
        for i in range(50)
    }
    keys_b = {
        upload_images.object_key_for(i, upload_images.prefix_id_for(i, b), b)
        for i in range(50)
    }
    assert keys_a != keys_b


def test_upload_one_writes_object_and_row(tmp_path: Any) -> None:
    p = _mk_params()
    writer = LocalFileWriter(tmp_path, "cont")
    row = upload_images.upload_one(3, lambda _a: writer, p)
    assert row["ok"] is True
    assert row["error"] == ""  # success leaves a non-null empty error (resume skip)
    assert row["actual_bytes"] > 0
    assert row["width"] > 0
    assert row["height"] > 0
    assert row["url"].startswith("az://cont/pre/run1/")
    bucket_names = {n for n, *_ in constants.SIZE_BUCKETS}
    assert row["target_bucket"] in bucket_names
    assert row["actual_bucket"] in bucket_names
    # the recorded actual bucket must agree with the actual encoded size
    assert row["actual_bucket"] == synthetic_image.bucket_of(row["actual_bytes"])
    stat = writer.head(row["object_key"])
    assert stat is not None
    assert stat.size_bytes == row["actual_bytes"]


def test_upload_is_idempotent_no_reput(tmp_path: Any) -> None:
    p = _mk_params()
    counter = _CountingWriter(LocalFileWriter(tmp_path, "cont"))
    r1 = upload_images.upload_one(4, lambda _a: counter, p)
    r2 = upload_images.upload_one(4, lambda _a: counter, p)
    assert r1["ok"]
    assert r2["ok"]
    # both success paths (fresh create + existing-object match) leave error == ""
    assert r1["error"] == ""
    assert r2["error"] == ""
    # second call: conditional-create conflicts, HEAD confirms a match -> no re-put
    assert counter.puts == 1


def test_size_mismatch_fails_unless_overwrite(tmp_path: Any) -> None:
    p = _mk_params()
    writer = LocalFileWriter(tmp_path, "cont")
    pid = upload_images.prefix_id_for(6, p)
    key = upload_images.object_key_for(6, pid, p)
    writer.put(key, b"x", content_type="image/png")  # wrong-sized pre-existing object

    row = upload_images.upload_one(6, lambda _a: writer, p)
    assert row["ok"] is False
    assert "size" in (row["error"] or "")

    p_overwrite = _mk_params(_cfg(overwrite_objects=True))
    row2 = upload_images.upload_one(6, lambda _a: writer, p_overwrite)
    assert row2["ok"] is True


class _NoMd5Writer:
    """Wrap a LocalFileWriter but drop content_md5 from head() results.

    Simulates a same-key object written by another tool with no Content-MD5, which
    the conflict-match must NOT trust on size alone.
    """

    def __init__(self, inner: LocalFileWriter) -> None:
        self.inner = inner

    def head(self, key: str) -> ObjectStat | None:
        stat = self.inner.head(key)
        return None if stat is None else ObjectStat(stat.size_bytes, stat.etag, None)

    def put(
        self,
        key: str,
        data: bytes,
        *,
        content_type: str,
        content_md5: str | None = None,
        overwrite: bool = True,
    ) -> str:
        return self.inner.put(
            key,
            data,
            content_type=content_type,
            content_md5=content_md5,
            overwrite=overwrite,
        )


def test_existing_object_without_md5_is_not_trusted(tmp_path: Any) -> None:
    p = _mk_params()
    base = LocalFileWriter(tmp_path, "cont")
    assert upload_images.upload_one(8, lambda _a: base, p)["ok"] is True  # seed it

    # Same size, but no Content-MD5 to verify against -> refuse (not trusted).
    nomd5 = _NoMd5Writer(base)
    row = upload_images.upload_one(8, lambda _a: nomd5, p)
    assert row["ok"] is False
    assert "verified" in (row["error"] or "")

    # --overwrite-objects bypasses verification and replaces unconditionally.
    p_overwrite = _mk_params(_cfg(overwrite_objects=True))
    assert upload_images.upload_one(8, lambda _a: nomd5, p_overwrite)["ok"] is True


def test_ensure_id_table_resume_opens_existing(tmp_path: Any) -> None:
    # Resume must OPEN the existing (geneva-registered) id table via the physical
    # check, not gate on the paginated conn.table_names() and re-create it.
    uri = str(tmp_path / "img_manifest_run.lance")
    db_uri, table = benchmark_env.split_source_uri(uri)
    conn = benchmark_env.connect_geneva(db_uri, {})

    t1 = upload_images._ensure_id_table(conn, table, uri, {}, 50, 20)
    assert t1.count_rows() == 50
    t2 = upload_images._ensure_id_table(conn, table, uri, {}, 50, 20)  # resume
    assert t2.count_rows() == 50
    # a mismatched expected count is a partial/bad prior build -> refuse
    with pytest.raises(RuntimeError, match="partial or mismatched"):
        upload_images._ensure_id_table(conn, table, uri, {}, 99, 20)


def test_manifest_struct_builds(tmp_path: Any) -> None:
    p = _mk_params()
    writer = LocalFileWriter(tmp_path, "cont")
    rows = upload_images.upload_ids([0, 1, 2, 3], lambda _a: writer, p, max_workers=2)
    arr = pa.array(
        [upload_images._row_to_tuple(r) for r in rows],
        type=upload_images.MANIFEST_STRUCT,
    )
    assert len(arr) == 4
    assert arr.type == upload_images.MANIFEST_STRUCT
    assert all(r["ok"] for r in rows)


def test_seed_run_config_round_trip(tmp_path: Any) -> None:
    record = upload_images.SeedRunConfig(
        schema_version=upload_images.SEED_RUN_SCHEMA_VERSION,
        generator_version="1",
        distribution_version="1",
        seed_run_id="run1",
        seed_run_salt=12345,
        object_count=8,
        accounts=["acctA", "acctB"],
        container="cont",
        base_prefix="pre",
        prefix_count=16,
        image_format="png",
        include_large_tail=False,
        max_image_bytes=None,
        created_at="2026-06-19T00:00:00+00:00",
        delete_after="2026-12-16T00:00:00+00:00",
        manifest_uri="az://cont/m.lance",
    )
    uri = (tmp_path / "m.seedrun.json").as_uri()
    upload_images.write_seed_run(uri, record, {})
    assert upload_images.read_seed_run(uri, {}) == record


def test_seed_run_artifact_uri() -> None:
    assert (
        upload_images.seed_run_artifact_uri("az://c/m.lance") == "az://c/m.seedrun.json"
    )


def test_seed_run_compat_passes_and_drift_raises() -> None:
    cfg = _cfg()
    assert cfg.seed_run_id is not None
    salt = upload_images._seed_run_salt(cfg.seed_run_id)
    record = upload_images._build_seed_run_config(
        cfg, cfg.seed_run_id, salt, "az://cont/m.lance"
    )
    # matching knobs on resume -> no raise
    upload_images._assert_seed_run_compatible(record, cfg, salt)
    # a changed derivation knob (accounts) -> divergence -> raise
    drifted = _cfg(accounts=("acctA", "acctC"))
    with pytest.raises(RuntimeError, match="knobs differ"):
        upload_images._assert_seed_run_compatible(record, drifted, salt)


def test_build_upload_manifest_has_deps_module_indexes_env() -> None:
    m = upload_images.build_upload_manifest("up-smoke", account_name="oailancepub")
    # one manifest covers the whole pipeline: upload PUT, download GET, and the
    # normalize/phash imports (pillow/numpy/imagehash)
    assert {
        "azure-storage-blob",
        "azure-identity",
        "pillow",
        "numpy",
        "imagehash",
    } <= set(m.pip)
    # assert against the pins themselves so a version bump can't drift the test
    assert set(constants.UPLOAD_MANIFEST_LANCE_DEPS) <= set(m.pip)
    assert "./loadtest" in m.py_modules
    assert "https://pypi.fury.io/lancedb/" in m.pip_extra_index_urls
    assert "https://pypi.fury.io/lance-format/" in m.pip_extra_index_urls
    assert m.env_vars.get("AZURE_STORAGE_ACCOUNT_NAME") == "oailancepub"


def test_build_upload_manifest_can_exclude_lance_deps() -> None:
    m = upload_images.build_upload_manifest(
        "u", account_name="a", include_lance_deps=False
    )
    assert "azure-storage-blob" in m.pip
    assert not set(constants.UPLOAD_MANIFEST_LANCE_DEPS) & set(m.pip)


# --- batched upload (Array UDF) ----------------------------------------------


def _rows_sans_etag(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rows minus the writer-assigned etag (everything else is deterministic)."""
    return [{k: v for k, v in r.items() if k != "etag"} for r in rows]


def test_upload_ids_threadpool_matches_serial(tmp_path: Any) -> None:
    p = _mk_params()
    ids = list(range(10))
    serial = upload_images.upload_ids(
        ids, lambda _a: LocalFileWriter(tmp_path / "serial", "cont"), p
    )
    pooled = upload_images.upload_ids(
        ids,
        lambda _a: LocalFileWriter(tmp_path / "pool", "cont"),
        p,
        max_workers=4,
    )
    # identical rows in input order: derivation, render, and status all match
    assert _rows_sans_etag(pooled) == _rows_sans_etag(serial)
    assert all(r["ok"] for r in pooled)


def test_upload_ids_reuses_external_executor(tmp_path: Any) -> None:
    """A passed-in executor is reused across calls (not shut down) — no per-batch
    pool churn, the property the batched UDF relies on."""
    from concurrent.futures import ThreadPoolExecutor

    p = _mk_params()
    writer = LocalFileWriter(tmp_path, "cont")
    ids = [0, 1, 2]
    with ThreadPoolExecutor(max_workers=2) as pool:
        out1 = upload_images.upload_ids(ids, lambda _a: writer, p, executor=pool)
        out2 = upload_images.upload_ids(ids, lambda _a: writer, p, executor=pool)
    assert all(r["ok"] for r in out1)
    assert all(r["ok"] for r in out2)  # pool still usable -> it was not shut down
    assert _rows_sans_etag(out1) == _rows_sans_etag(out2)


def test_writer_cache_injects_and_caches_by_account() -> None:
    calls: list[str] = []

    def factory(account: str) -> Any:
        calls.append(account)
        return object()

    get = upload_images._writer_cache("cont", factory)
    w1 = get("acctA")
    w2 = get("acctA")
    assert w1 is w2  # cached per account — built once
    get("acctB")  # different account -> distinct writer
    assert calls == ["acctA", "acctB"]


def test_build_upload_udf_batched_is_array_input() -> None:
    from geneva.transformer import UDFArgType

    salt = upload_images._seed_run_salt("run1")
    udf = upload_images.build_upload_udf_batched(_cfg(upload_concurrency=4), salt)
    assert udf.arg_type == UDFArgType.ARRAY
    assert udf.is_multi_output is False  # batched UDFs cannot be Columns[...]
    assert udf.data_type == upload_images.MANIFEST_STRUCT
    assert udf.input_columns == ["image_id"]

    scalar = upload_images.build_upload_udf(_cfg(), salt)
    assert scalar.arg_type == UDFArgType.SCALAR
    assert scalar.input_columns == ["image_id"]


def test_upload_udf_versions_differ_by_mode_and_knobs() -> None:
    salt = upload_images._seed_run_salt("run1")
    scalar = upload_images._udf_version(_cfg(), salt)
    # Golden value: the scalar version keys every in-flight seed run's checkpoints.
    # If this assert fails, the change re-keys existing scalar checkpoints (a full
    # reprocess at scale) — don't just update the literal, make the knob string
    # backward-compatible instead.
    assert scalar == "0.1-2c4401155b"
    # upload_concurrency must NOT perturb the scalar version: existing scalar seed
    # runs keep their checkpoint keys.
    assert upload_images._udf_version(_cfg(upload_concurrency=4), salt) == scalar
    b4 = upload_images._udf_version(_cfg(upload_concurrency=4), salt, batched=True)
    b8 = upload_images._udf_version(_cfg(upload_concurrency=8), salt, batched=True)
    assert scalar != b4  # scalar vs batched re-keys
    assert b4 != b8  # a concurrency change within batched mode re-keys


def test_upload_concurrency_bounds() -> None:
    # validate() runs the knob checks (run.py calls it before dispatch)
    _cfg(upload_concurrency=1).validate()  # lower bound ok
    _cfg(upload_concurrency=8).validate()  # mid-range ok
    _cfg(upload_concurrency=constants.MAX_UPLOAD_CONCURRENCY).validate()  # upper ok
    with pytest.raises(ValueError, match="upload_concurrency"):
        _cfg(upload_concurrency=0).validate()
    with pytest.raises(ValueError, match="upload_concurrency"):
        _cfg(upload_concurrency=constants.MAX_UPLOAD_CONCURRENCY + 1).validate()


def test_upload_in_flight_product_guard() -> None:
    # within the default ceiling: 8 * 1 * 8 = 64
    _cfg(upload_concurrency=8).validate()
    # exceeds the default 50_000: 2048 * 1 * 32 = 65_536
    with pytest.raises(ValueError, match="in-flight PUTs"):
        _cfg(concurrency=2048, upload_concurrency=32).validate()
    # intra_concurrency is part of the product: 100 * 10 * 100 = 100_000
    with pytest.raises(ValueError, match="intra_concurrency"):
        _cfg(concurrency=100, intra_concurrency=10, upload_concurrency=100).validate()
    # raising --max-in-flight is the intentional escape hatch
    _cfg(concurrency=2048, upload_concurrency=32, max_in_flight=100_000).validate()
    # the guard only applies to the batched uploader (upload_concurrency set)
    _cfg(concurrency=100_000).validate()


# --- upload end-to-end backfill (real local Geneva/Ray) ----------------------


@pytest.mark.ray
@pytest.mark.parametrize("upload_concurrency", [None, 4])
def test_upload_backfill_end_to_end(
    tmp_path: Any, monkeypatch: Any, upload_concurrency: int | None
) -> None:
    """Run upload-images via a real local backfill in both modes.

    Exercises the whole path — id-table creation, add_columns(UnpackedUDF(...)),
    the Geneva backfill (an Array UDF for the batched variant), and unpack into
    the 15 manifest columns. A local writer is injected into the UDF closure so
    it ships to the Ray worker (same filesystem). Both modes must produce the
    identical deterministic derivation (urls/keys/accounts).
    """
    import lance

    container = "cont"

    def _local_writer(_account: str) -> Any:
        return LocalFileWriter(tmp_path, container)

    real_scalar = upload_images.build_upload_udf
    real_batched = upload_images.build_upload_udf_batched
    monkeypatch.setattr(
        upload_images,
        "build_upload_udf",
        lambda cfg, salt: real_scalar(cfg, salt, writer_factory=_local_writer),
    )
    monkeypatch.setattr(
        upload_images,
        "build_upload_udf_batched",
        lambda cfg, salt: real_batched(cfg, salt, writer_factory=_local_writer),
    )

    manifest_uri = str(tmp_path / "img_manifest_run1.lance")
    cfg = _cfg(
        object_count=6,
        seed_rows_per_fragment=4,  # two fragments
        manifest_uri=manifest_uri,
        upload_concurrency=upload_concurrency,
    )
    metrics = upload_images.run_upload_images(cfg)

    assert metrics["total_rows"] == 6
    assert metrics["rows_filled"] == 6
    assert metrics["uploaded_ok"] == 6
    assert metrics["errors"] == 0
    assert metrics["upload_concurrency"] == upload_concurrency
    assert metrics["ok"] is True

    ds = lance.dataset(manifest_uri)
    names = set(ds.schema.names)
    assert {name for name, _ in upload_images._MANIFEST_FIELDS} <= names

    # the filled columns match the scalar-computed deterministic derivation
    p = _mk_params(cfg)
    by_id = {row["image_id"]: row for row in ds.to_table().to_pylist()}
    for image_id in range(6):
        row = by_id[image_id]
        pid = upload_images.prefix_id_for(image_id, p)
        key = upload_images.object_key_for(image_id, pid, p)
        assert row["prefix_id"] == pid
        assert row["object_key"] == key
        assert row["url"] == upload_images.url_for(key, p)
        assert row["account"] == upload_images.account_for(image_id, p)
        assert row["ok"] is True
        assert row["error"] == ""
        assert row["actual_bytes"] > 0
        # the blob really landed on the (local) store
        stat = LocalFileWriter(tmp_path, container).head(key)
        assert stat is not None
        assert stat.size_bytes == row["actual_bytes"]
