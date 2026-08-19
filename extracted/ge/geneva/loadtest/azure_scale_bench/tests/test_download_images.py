# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for the reuse-read download stage (Local readers/writers — no Azure)."""

from __future__ import annotations

import io
from typing import Any

import pyarrow as pa
import pytest

from loadtest.azure_scale_bench import (
    constants,
    download_images,
    expand_images,
    failure_inject,
    upload_images,
)
from loadtest.azure_scale_bench.benchmark_env import BenchConfig
from loadtest.azure_scale_bench.object_writer import LocalFileReader, LocalFileWriter


def _cfg(**overrides: Any) -> BenchConfig:
    base: dict[str, Any] = {
        "seed_run_id": "run1",
        "accounts": ("acctA", "acctB"),
        "loose_container": "cont",
        "base_prefix": "pre",
        "prefix_count": 16,
        "image_format": "png",
        "object_count": 64,
    }
    base.update(overrides)
    return BenchConfig(**base)


def _params(cfg: BenchConfig | None = None) -> upload_images._UploadParams:
    cfg = cfg or _cfg()
    assert cfg.seed_run_id is not None
    return upload_images._params(cfg, upload_images._seed_run_salt(cfg.seed_run_id))


# --- resume / repair predicate ----------------------------------------------


def test_resume_predicate_modes() -> None:
    assert (
        download_images.resume_predicate(
            "S", "U", repair_errors=False, has_explicit_where=False
        )
        == "U IS NULL"
    )
    assert (
        download_images.resume_predicate(
            "S", "U", repair_errors=True, has_explicit_where=False
        )
        == "S.error != ''"
    )
    # repair wins even with an explicit --where present
    assert (
        download_images.resume_predicate(
            "S", "U", repair_errors=True, has_explicit_where=True
        )
        == "S.error != ''"
    )
    # an explicit --where (no repair) means no extra predicate
    assert (
        download_images.resume_predicate(
            "S", "U", repair_errors=False, has_explicit_where=True
        )
        is None
    )


# --- schema compatibility with the existing normalize stage -----------------


def test_download_struct_matches_expand_struct() -> None:
    # normalize reads <struct_col>.image_bytes; the download struct must be the same
    # MMLB-shaped struct expand produces so the existing normalize stage consumes it.
    assert download_images._DOWNLOAD_STRUCT == expand_images._IMAGE_STRUCT


def test_combo_struct_top_field_is_normalize_input_column() -> None:
    combo = download_images.combo_struct("smoke1")
    assert combo.field(0).name == constants.struct_col("smoke1")
    image_struct = combo.field(0).type
    image_bytes = image_struct.field("image_bytes")
    assert image_bytes.type == pa.large_binary()
    # carries the Lance blob-encoding marker so normalize's range reader applies
    # (Arrow stores field metadata as bytes — decode before comparing)
    decoded = {k.decode(): v.decode() for k, v in (image_bytes.metadata or {}).items()}
    assert decoded == constants.MMLB_BLOB_META


# --- direct ref-table download (local mini-e2e) -----------------------------


def _ref_locator(image_id: int) -> dict[str, Any]:
    """Derive the ref-table locator columns for ``image_id`` (as build-ref-table)."""
    params = _params()
    prefix_id = upload_images.prefix_id_for(image_id, params)
    object_key = upload_images.object_key_for(image_id, prefix_id, params)
    return {
        "url": upload_images.url_for(object_key, params),
        "account": upload_images.account_for(image_id, params),
        "container": params.container,
        "object_key": object_key,
    }


def test_download_ref_one_reads_uploaded_object(tmp_path: Any) -> None:
    """A direct-ref row downloads the object its locator columns point at."""
    params = _params()
    image_id = 5
    loc = _ref_locator(image_id)

    writer = LocalFileWriter(tmp_path, loc["container"])
    up = upload_images.upload_one(image_id, lambda _a: writer, params)
    assert up["ok"] is True

    row = download_images.download_ref_one(
        0,
        image_id,
        loc["url"],
        loc["account"],
        loc["container"],
        loc["object_key"],
        lambda _account, container: LocalFileReader(tmp_path, container),
    )
    assert row["ok"] is True
    assert row["error"] == ""  # success leaves a non-null empty error (resume skip)
    assert row["seed_image_id"] == image_id
    assert row["source_url"] == loc["url"] == up["url"]
    assert row["time"] >= 0
    assert row["image_bytes"] is not None
    assert len(row["image_bytes"]) == up["actual_bytes"]
    with io.BytesIO(row["image_bytes"]) as buf:
        from PIL import Image

        with Image.open(buf) as img:
            img.load()


def test_download_ref_one_missing_object_records_error(tmp_path: Any) -> None:
    loc = _ref_locator(9)  # nothing uploaded — the object is absent
    row = download_images.download_ref_one(
        0,
        9,
        loc["url"],
        loc["account"],
        loc["container"],
        loc["object_key"],
        lambda _account, container: LocalFileReader(tmp_path, container),
    )
    assert row["ok"] is False
    assert row["image_bytes"] is None
    assert "not found" in (row["error"] or "")
    # the anchor is still written so the row is resumable / repairable
    assert row["source_url"] == loc["url"]


def test_download_ref_one_missing_locator_records_error() -> None:
    def _no_reader(_account: str, _container: str) -> Any:
        raise AssertionError("reader must not be called when a locator is missing")

    row = download_images.download_ref_one(
        0, 9, None, "acctA", "cont", "key", _no_reader
    )
    assert row["ok"] is False
    assert row["image_bytes"] is None
    assert "missing ref locator" in (row["error"] or "")
    assert row["seed_image_id"] == 9
    assert row["source_url"] == ""  # null url -> empty-string anchor, never None


def test_download_ref_one_injected_failure_skips_get() -> None:
    def _no_reader(_account: str, _container: str) -> Any:
        raise AssertionError("reader must not be called on an injected-failure row")

    loc = _ref_locator(7)
    row = download_images.download_ref_one(
        7,
        7,
        loc["url"],
        loc["account"],
        loc["container"],
        loc["object_key"],
        _no_reader,
        inject_rate=1.0,
        inject_seed=0,
    )
    assert row["ok"] is False
    assert row["error"] == failure_inject.INJECTED_ERROR
    assert row["source_url"] == loc["url"]


def test_download_ref_rows_threadpool_matches_serial(tmp_path: Any) -> None:
    """The threadpool batch helper is order-preserving and matches the serial path."""
    params = _params()
    image_ids = list(range(4))
    writer = LocalFileWriter(tmp_path, params.container)
    for image_id in image_ids[:2]:  # seed only some, so the batch mixes ok + missing
        upload_images.upload_one(image_id, lambda _a: writer, params)

    rows = []
    for row_index, image_id in enumerate(image_ids):
        loc = _ref_locator(image_id)
        rows.append(
            (
                row_index,
                image_id,
                loc["url"],
                loc["account"],
                loc["container"],
                loc["object_key"],
            )
        )

    def _factory(_account: str, container: str) -> Any:
        return LocalFileReader(tmp_path, container)

    serial = download_images.download_ref_rows(rows, _factory, max_workers=1)
    concurrent = download_images.download_ref_rows(rows, _factory, max_workers=4)
    assert [r["seed_image_id"] for r in concurrent] == image_ids  # order preserved
    assert [r["ok"] for r in concurrent] == [r["ok"] for r in serial]
    assert [r["ok"] for r in concurrent] == [True, True, False, False]


def test_download_ref_rows_packs_combo_struct(tmp_path: Any) -> None:
    params = _params()
    writer = LocalFileWriter(tmp_path, params.container)
    upload_images.upload_one(0, lambda _a: writer, params)
    rows = []
    for image_id in range(3):
        loc = _ref_locator(image_id)
        rows.append(
            (
                image_id,
                image_id,
                loc["url"],
                loc["account"],
                loc["container"],
                loc["object_key"],
            )
        )
    out = download_images.download_ref_rows(
        rows, lambda _a, c: LocalFileReader(tmp_path, c), max_workers=2
    )
    arr = pa.array(
        [download_images._row_to_tuple(r) for r in out],
        type=download_images.combo_struct("smoke1"),
    )
    assert len(arr) == 3
    assert arr.type == download_images.combo_struct("smoke1")


# --- direct ref-table column validation + UDF builders ----------------------


def test_require_ref_columns_reports_missing() -> None:
    full = [
        "row_index",
        "image_id",
        "url",
        "account",
        "container",
        "object_key",
    ]
    # a complete schema passes
    download_images._require_ref_columns(
        _cfg(), pa.schema([(c, pa.string()) for c in full])
    )
    # dropping a required column raises, naming it
    partial = pa.schema([(c, pa.string()) for c in full if c != "url"])
    with pytest.raises(ValueError, match="url"):
        download_images._require_ref_columns(_cfg(), partial)


def test_run_download_images_rejects_manifest_uri() -> None:
    # legacy seed-derived mode is gone; --url-manifest-uri must fail fast (before any
    # connection), pointing at build-ref-table instead
    with pytest.raises(ValueError, match="no longer supports --url-manifest-uri"):
        download_images.run_download_images(_cfg(manifest_uri="az://c/m.lance"))


def test_effective_batch_rows_prefers_checkpoint_size() -> None:
    # mirrors geneva resolve_batch_size: checkpoint_size wins over deprecated batch_size
    assert download_images._effective_batch_rows(_cfg(checkpoint_size=1000)) == 1000
    assert download_images._effective_batch_rows(_cfg(batch_size=5000)) == 5000
    assert (
        download_images._effective_batch_rows(
            _cfg(batch_size=10000, checkpoint_size=1000)
        )
        == 1000
    )
    assert download_images._effective_batch_rows(_cfg()) is None


def test_build_ref_download_udf_is_scalar_multi_output() -> None:
    from geneva.transformer import UDFArgType

    udf = download_images.build_ref_download_udf(_cfg())
    assert udf.arg_type == UDFArgType.SCALAR
    assert udf.is_multi_output is True
    assert pa.types.is_struct(udf.data_type)
    assert udf.input_columns == [
        "row_index",
        "image_id",
        "url",
        "account",
        "container",
        "object_key",
    ]


def test_build_ref_download_udf_batched_is_array_input() -> None:
    from geneva.transformer import UDFArgType

    udf = download_images.build_ref_download_udf_batched(_cfg(download_concurrency=4))
    assert udf.arg_type == UDFArgType.ARRAY
    assert udf.is_multi_output is False  # batched UDFs cannot be Columns[...]
    assert udf.data_type == download_images.combo_struct("smoke1")
    assert udf.input_columns == [
        "row_index",
        "image_id",
        "url",
        "account",
        "container",
        "object_key",
    ]


def test_ref_udf_versions_differ_by_mode_and_knobs() -> None:
    scalar = download_images._ref_udf_version(_cfg(), batched=False)
    batched = download_images._ref_udf_version(
        _cfg(download_concurrency=8), batched=True
    )
    assert scalar != batched
    # a failure-injection knob change re-keys the version (forces reprocess)
    injected = download_images._ref_udf_version(
        _cfg(inject_failure_rate=0.1), batched=False
    )
    assert injected != scalar


# --- download_concurrency bounds + reader/executor reuse --------------------


def test_download_concurrency_bounds() -> None:
    # validate() runs the knob checks (run.py calls it before dispatch)
    _cfg(download_concurrency=1).validate()  # lower bound ok
    _cfg(download_concurrency=8).validate()  # mid-range ok
    _cfg(download_concurrency=constants.MAX_DOWNLOAD_CONCURRENCY).validate()  # upper ok
    with pytest.raises(ValueError, match="download_concurrency"):
        _cfg(download_concurrency=0).validate()
    with pytest.raises(ValueError, match="download_concurrency"):
        _cfg(download_concurrency=constants.MAX_DOWNLOAD_CONCURRENCY + 1).validate()


def test_in_flight_product_guard() -> None:
    # within the default ceiling: 8 * 1 * 8 = 64
    _cfg(download_concurrency=8).validate()
    # exceeds the default 50_000: 2048 * 1 * 32 = 65_536
    with pytest.raises(ValueError, match="in-flight"):
        _cfg(concurrency=2048, download_concurrency=32).validate()
    # intra_concurrency is part of the product: 100 * 10 * 100 = 100_000
    with pytest.raises(ValueError, match="intra_concurrency"):
        _cfg(concurrency=100, intra_concurrency=10, download_concurrency=100).validate()
    # raising --max-in-flight is the intentional escape hatch
    _cfg(concurrency=2048, download_concurrency=32, max_in_flight=100_000).validate()
    # the guard only applies to the batched downloader (download_concurrency set)
    _cfg(concurrency=100_000).validate()


def test_expected_mean_bytes_matches_distribution() -> None:
    from loadtest.azure_scale_bench import image_distribution

    # the spec size distribution averages ~180 KiB; pin a loose sanity range
    assert 120_000 < image_distribution.expected_mean_bytes() < 260_000


def test_ref_reader_cache_injects_and_caches_by_account_container() -> None:
    calls: list[tuple[str, str]] = []

    def factory(account: str, container: str) -> Any:
        calls.append((account, container))
        return object()

    get = download_images._ref_reader_cache(factory)
    r1 = get("acctA", "cont")
    r2 = get("acctA", "cont")
    assert r1 is r2  # cached per (account, container) — built once
    get("acctA", "other")  # different container -> distinct reader
    get("acctB", "cont")  # different account -> distinct reader
    assert calls == [("acctA", "cont"), ("acctA", "other"), ("acctB", "cont")]


def test_download_ref_rows_reuses_external_executor(tmp_path: Any) -> None:
    """A passed-in executor is reused across calls (not shut down) — no per-batch
    pool churn, the property the batched UDF relies on."""
    from concurrent.futures import ThreadPoolExecutor

    params = _params()
    upload_images.upload_one(
        0, lambda _a: LocalFileWriter(tmp_path, params.container), params
    )
    loc = _ref_locator(0)
    rows = [(0, 0, loc["url"], loc["account"], loc["container"], loc["object_key"])]

    def _factory(_account: str, container: str) -> Any:
        return LocalFileReader(tmp_path, container)

    with ThreadPoolExecutor(max_workers=2) as pool:
        out1 = download_images.download_ref_rows(rows, _factory, executor=pool)
        out2 = download_images.download_ref_rows(rows, _factory, executor=pool)
    assert out1[0]["ok"] is True
    assert out2[0]["ok"] is True  # pool still usable -> it was not shut down


# --- direct-ref end-to-end backfill (real local Geneva/Ray) -----------------


@pytest.mark.ray
@pytest.mark.parametrize("download_concurrency", [None, 4])
def test_direct_ref_backfill_end_to_end(
    tmp_path: Any, monkeypatch: Any, download_concurrency: int | None
) -> None:
    """Build a tiny ref table and run direct-mode download via a real local backfill.

    Exercises the whole path — add_columns(UnpackedUDF(...)) on the ref table, the
    Geneva backfill (an Array UDF for the batched variant), unpack into the three
    sibling columns, and per-row error capture for a missing blob. A local reader is
    injected into the UDF closure so it ships to the Ray worker (same filesystem).
    Then a second --repair-errors run on the EXISTING columns exercises the reuse path
    (scalar UDF override vs batched udf=None) and selective re-fetch of only the failed
    row once its blob exists.
    """
    import lance

    params = _params()
    container = params.container
    image_ids = [0, 1, 2, 3]
    for image_id in image_ids[:3]:  # leave image_id=3 unseeded -> one error row
        up = upload_images.upload_one(
            image_id, lambda _a: LocalFileWriter(tmp_path, container), params
        )
        assert up["ok"] is True

    locs = [_ref_locator(i) for i in image_ids]
    ref = pa.table(
        {
            "row_index": pa.array(list(range(len(image_ids))), pa.int64()),
            "image_id": pa.array(image_ids, pa.int64()),
            "url": pa.array([loc["url"] for loc in locs], pa.string()),
            "account": pa.array([loc["account"] for loc in locs], pa.string()),
            "container": pa.array([loc["container"] for loc in locs], pa.string()),
            "object_key": pa.array([loc["object_key"] for loc in locs], pa.string()),
        }
    )
    uri = str(tmp_path / "ref.lance")
    lance.write_dataset(ref, uri, data_storage_version=constants.DATA_STORAGE_VERSION)

    def _local_reader(_account: str, container: str) -> Any:
        return LocalFileReader(tmp_path, container)

    real_scalar = download_images.build_ref_download_udf
    real_batched = download_images.build_ref_download_udf_batched
    monkeypatch.setattr(
        download_images,
        "build_ref_download_udf",
        lambda cfg: real_scalar(cfg, reader_factory=_local_reader),
    )
    monkeypatch.setattr(
        download_images,
        "build_ref_download_udf_batched",
        lambda cfg: real_batched(cfg, reader_factory=_local_reader),
    )

    cfg = _cfg(bench_uri=uri, suffix="e2e1", download_concurrency=download_concurrency)
    metrics = download_images.run_download_images(cfg)

    assert metrics["input_mode"] == "direct-ref-table"
    assert metrics["download_concurrency"] == download_concurrency
    assert metrics["total_rows"] == len(image_ids)
    assert metrics["rows_filled"] == len(image_ids)  # url anchor on every row
    assert metrics["ok"] is True  # error_rate 0.25 <= max_error_rate 0.5
    if metrics.get("errors") is not None:  # struct-subfield filter is best-effort
        assert metrics["errors"] == 1
        assert metrics["downloaded_ok"] == 3

    # the three unpacked sibling columns now exist on the ref table
    names = lance.dataset(uri).schema.names
    assert constants.struct_col("e2e1") in names
    assert constants.ingest_seed_id_col("e2e1") in names
    assert constants.ingest_url_col("e2e1") in names

    # --- repair phase: seed the missing blob, re-run with --repair-errors ----------
    # This backfills the EXISTING columns (reuse path): the scalar UDF is passed as the
    # backfill(udf=...) override; the batched UDF re-runs the stored UDF (udf=None).
    # The repair predicate selects only the previously-failed row (error != '').
    up = upload_images.upload_one(
        image_ids[3], lambda _a: LocalFileWriter(tmp_path, container), params
    )
    assert up["ok"] is True

    repair_cfg = _cfg(
        bench_uri=uri,
        suffix="e2e1",
        download_concurrency=download_concurrency,
        repair_errors=True,
    )
    repair_metrics = download_images.run_download_images(repair_cfg)
    assert repair_metrics["total_rows"] == len(image_ids)
    assert repair_metrics["rows_filled"] == len(image_ids)  # ok rows untouched
    assert repair_metrics["ok"] is True
    if repair_metrics.get("errors") is not None:
        # the once-failed row was selectively re-fetched and now succeeds
        assert repair_metrics["errors"] == 0
        assert repair_metrics["downloaded_ok"] == len(image_ids)


class _EmptySchemaTable:
    """A run table whose ingest columns for the suffix don't exist yet."""

    schema = pa.schema([])


class _MultiOutputUDF:
    is_multi_output = True


def test_repair_errors_refuses_when_ingest_columns_absent() -> None:
    """Repair on a fresh/typo'd suffix must fail, not report a clean no-op.

    The columns would be added all-NULL and the repair predicate
    (``{struct}.error != ''``) is NULL — never true — on every row, so the
    backfill would match zero rows and still exit 0.
    """
    cfg = _cfg(suffix="never1", repair_errors=True)

    with pytest.raises(RuntimeError, match=r"--repair-errors repairs existing"):
        download_images._apply_and_backfill(
            cfg,
            None,
            _EmptySchemaTable(),
            _MultiOutputUDF(),  # type: ignore[arg-type]
        )
