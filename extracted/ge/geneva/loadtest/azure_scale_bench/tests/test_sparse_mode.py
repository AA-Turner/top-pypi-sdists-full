# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for the sparse (``--update-mode sparse_rows``) repair path."""

from __future__ import annotations

import logging
from typing import Any

import pyarrow as pa
import pytest

from loadtest.azure_scale_bench import (
    constants,
    download_images,
    runner,
    upload_images,
)
from loadtest.azure_scale_bench.benchmark_env import BenchConfig
from loadtest.azure_scale_bench.object_writer import LocalFileReader, LocalFileWriter
from loadtest.azure_scale_bench.run import build_parser
from loadtest.azure_scale_bench.tests.test_download_images import (
    _cfg,
    _params,
    _ref_locator,
)

# --- constants / config / CLI ------------------------------------------------


def test_update_mode_constant_matches_geneva() -> None:
    # constants.py must not import geneva at parse time, so the parity between the
    # bench's string and geneva's engine constant is pinned here instead.
    from geneva.runners.sparse_update import SPARSE_UPDATE_MODE

    assert constants.UPDATE_MODE_SPARSE == SPARSE_UPDATE_MODE


def test_cli_update_mode_maps_to_config(monkeypatch: Any) -> None:
    monkeypatch.delenv("BENCH_UPDATE_MODE", raising=False)
    base = ["download-images", "--clone-target", "az://d/t.lance", "--suffix", "s1"]

    args = build_parser().parse_args(base)
    assert BenchConfig.from_env_and_args(args).update_mode == "fragment"

    args = build_parser().parse_args(
        base + ["--update-mode", "sparse_rows", "--repair-errors"]
    )
    cfg = BenchConfig.from_env_and_args(args)
    cfg.validate()
    assert cfg.update_mode == "sparse_rows"

    monkeypatch.setenv("BENCH_UPDATE_MODE", "sparse_rows")
    args = build_parser().parse_args(base)
    assert BenchConfig.from_env_and_args(args).update_mode == "sparse_rows"


def test_validate_rejects_unknown_update_mode() -> None:
    with pytest.raises(ValueError, match="update_mode"):
        BenchConfig(update_mode="bogus").validate()


def test_validate_rejects_sparse_with_overwrite() -> None:
    with pytest.raises(ValueError, match="overwrite"):
        BenchConfig(
            update_mode="sparse_rows", overwrite=True, repair_errors=True
        ).validate()


def test_validate_rejects_sparse_without_repair_or_where() -> None:
    # The default resume predicate (url IS NULL) can never converge in sparse mode
    # (the url anchor is carried forward, not rewritten).
    with pytest.raises(ValueError, match="converge"):
        BenchConfig(update_mode="sparse_rows").validate()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"repair_errors": True},
        {"where": "row_index < 10"},
    ],
)
def test_validate_accepts_sparse_repair_scopes(kwargs: dict) -> None:
    BenchConfig(update_mode="sparse_rows", **kwargs).validate()  # must not raise


# --- runner.sparse_update_kwargs ----------------------------------------------


def test_sparse_update_kwargs_maps_supported_knobs() -> None:
    cfg = BenchConfig(
        concurrency=16,
        num_frags=1,
        commit_granularity_pct=5.0,
    )
    kwargs = runner.sparse_update_kwargs(cfg, num_fragments=1000)
    assert kwargs["concurrency"] == 16
    assert kwargs["where"] == "row_index >= 0 AND row_index < 1000000"
    assert kwargs["commit_granularity"] == 50


def test_sparse_update_kwargs_derives_granularity_to_fill_pool() -> None:
    # Without --commit-granularity-pct the engine's auto default (>= n/20 per
    # range) would cap the actor pool at 20; the bench sizes ranges off the
    # requested concurrency instead.
    kwargs = runner.sparse_update_kwargs(
        BenchConfig(concurrency=16), num_fragments=1000
    )
    assert kwargs["commit_granularity"] == 62  # 1000 // 16 -> ~16 range tasks
    kwargs = runner.sparse_update_kwargs(BenchConfig(concurrency=8), num_fragments=4)
    assert kwargs["commit_granularity"] == 1  # never below one fragment per range
    # unknown fragment count -> leave it to the engine's auto-scaling
    assert "commit_granularity" not in runner.sparse_update_kwargs(
        BenchConfig(concurrency=8)
    )


def test_sparse_update_kwargs_warns_on_non_default_actor_memory(caplog: Any) -> None:
    # Sparse actors schedule at Ray defaults; a tuned --per-actor-memory-gib is a
    # no-op there and must be called out.
    with caplog.at_level(logging.WARNING, logger="loadtest.azure_scale_bench.runner"):
        runner.sparse_update_kwargs(BenchConfig(per_actor_memory_gib=4.0))
    (record,) = [r for r in caplog.records if "ignoring" in r.getMessage()]
    assert "per_actor_memory_gib" in record.getMessage()


def test_sparse_update_kwargs_warns_on_per_actor_cpus(caplog: Any) -> None:
    # The sparse repair UDF reserves no resources, so --per-actor-cpus is a no-op
    # under sparse update_mode and must be called out like --per-actor-memory-gib.
    with caplog.at_level(logging.WARNING, logger="loadtest.azure_scale_bench.runner"):
        runner.sparse_update_kwargs(BenchConfig(per_actor_cpus=4))
    (record,) = [r for r in caplog.records if "ignoring" in r.getMessage()]
    assert "per_actor_cpus" in record.getMessage()


def test_sparse_update_kwargs_suppresses_checkpoint_knobs(caplog: Any) -> None:
    cfg = BenchConfig(
        concurrency=8,
        intra_concurrency=2,
        task_size=2048,
        checkpoint_size=1000,
        min_checkpoint_size=500,
        max_checkpoint_size=2000,
        flush_interval_seconds=60.0,
    )
    with caplog.at_level(logging.WARNING, logger="loadtest.azure_scale_bench.runner"):
        kwargs = runner.sparse_update_kwargs(cfg)
    assert set(kwargs) == {"concurrency"}  # nothing else leaks into the engine call
    (record,) = [r for r in caplog.records if "ignoring" in r.getMessage()]
    for name in (
        "task_size",
        "checkpoint_size",
        "min_checkpoint_size",
        "max_checkpoint_size",
        "flush_interval_seconds",
        "intra_concurrency",
    ):
        assert name in record.getMessage()


def test_sparse_update_kwargs_quiet_when_nothing_ignored(caplog: Any) -> None:
    with caplog.at_level(logging.WARNING, logger="loadtest.azure_scale_bench.runner"):
        runner.sparse_update_kwargs(BenchConfig(concurrency=4))
    assert not [r for r in caplog.records if "ignoring" in r.getMessage()]


# --- repair UDF builders --------------------------------------------------------


@pytest.mark.parametrize("download_concurrency", [None, 4])
def test_repair_udf_is_single_output_image_struct(
    download_concurrency: int | None,
) -> None:
    cfg = _cfg(suffix="s1", download_concurrency=download_concurrency)
    udf = download_images.build_ref_repair_udf(cfg)
    # The sparse engine slots the UDF output into the ONE image-struct column and
    # carries the siblings, so the repair UDF must be single-output with the exact
    # struct type the column was created with.
    assert udf.is_multi_output is False
    assert udf.data_type == download_images._DOWNLOAD_STRUCT
    assert udf.input_columns == download_images._ref_input_columns(cfg)
    assert "sparse-repair" in udf.version


def test_repair_udf_version_differs_from_download_udf() -> None:
    cfg = _cfg(suffix="s1")
    repair = download_images.build_ref_repair_udf(cfg)
    download = download_images.build_ref_download_udf(cfg)
    assert repair.version != download.version


# --- sparse guards ---------------------------------------------------------------


def test_sparse_requires_existing_columns(tmp_path: Any) -> None:
    """Sparse mode on a fresh table must refuse before creating any columns."""
    import lance

    ref = pa.table(
        {
            "row_index": pa.array([0, 1], pa.int64()),
            "image_id": pa.array([0, 1], pa.int64()),
            "url": pa.array(["u0", "u1"], pa.string()),
            "account": pa.array(["a", "a"], pa.string()),
            "container": pa.array(["c", "c"], pa.string()),
            "object_key": pa.array(["k0", "k1"], pa.string()),
        }
    )
    uri = str(tmp_path / "ref.lance")
    lance.write_dataset(ref, uri, data_storage_version=constants.DATA_STORAGE_VERSION)

    cfg = _cfg(
        bench_uri=uri,
        suffix="sparse1",
        update_mode="sparse_rows",
        repair_errors=True,
    )
    with pytest.raises(RuntimeError, match="fragment-mode download first"):
        download_images.run_download_images(cfg)
    # the guard fired before add_columns — no ingest columns were created
    assert constants.struct_col("sparse1") not in lance.dataset(uri).schema.names

    # sparse + overwrite refuses BEFORE resolve_existing_columns can drop columns,
    # even for programmatic callers that skip cfg.validate()
    overwrite_cfg = _cfg(
        bench_uri=uri,
        suffix="sparse1",
        update_mode="sparse_rows",
        repair_errors=True,
        overwrite=True,
    )
    with pytest.raises(ValueError, match="overwrite would drop"):
        download_images.run_download_images(overwrite_cfg)


# --- sparse repair end-to-end (real local Geneva/Ray) ----------------------------


@pytest.mark.ray
@pytest.mark.parametrize("download_concurrency", [None, 4])
def test_sparse_repair_end_to_end(
    tmp_path: Any, monkeypatch: Any, download_concurrency: int | None
) -> None:
    """Fragment-mode download with one failed row, then a sparse repair pass.

    Mirrors test_direct_ref_backfill_end_to_end's repair phase but drives it through
    ``--update-mode sparse_rows``: the engine deletes the matched (error) row by
    address and appends the recomputed replacement, carrying the url/seed_id sibling
    columns forward. Asserts the repair converged (errors == 0), the sparse metrics
    are reported, and the carried siblings survive on every row.
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
    real_repair = download_images.build_ref_repair_udf
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
    monkeypatch.setattr(
        download_images,
        "build_ref_repair_udf",
        lambda cfg: real_repair(cfg, reader_factory=_local_reader),
    )

    suffix = "sparse2"
    cfg = _cfg(bench_uri=uri, suffix=suffix, download_concurrency=download_concurrency)
    metrics = download_images.run_download_images(cfg)
    assert metrics["update_mode"] == "fragment"
    if metrics.get("errors") is not None:
        assert metrics["errors"] == 1

    # seed the missing blob, then repair via the sparse row-update engine
    up = upload_images.upload_one(
        image_ids[3], lambda _a: LocalFileWriter(tmp_path, container), params
    )
    assert up["ok"] is True

    repair_cfg = _cfg(
        bench_uri=uri,
        suffix=suffix,
        download_concurrency=download_concurrency,
        repair_errors=True,
        update_mode="sparse_rows",
    )
    repair_cfg.validate()
    repair_metrics = download_images.run_download_images(repair_cfg)

    assert repair_metrics["update_mode"] == "sparse_rows"
    # the metrics record the composed repair predicate (regression: the sparse
    # path must not consume the caller's kwargs["where"] before metrics are built)
    assert repair_metrics["where"] == f"{constants.struct_col(suffix)}.error != ''"
    assert repair_metrics["rows_matched"] == 1
    assert repair_metrics["rows_written"] == 1
    assert repair_metrics["fragments_failed"] == 0
    assert repair_metrics["fragments_touched"] >= 1
    assert "amplification_saved" in repair_metrics
    assert "selectivity" in repair_metrics
    assert repair_metrics["committed_version"] > repair_metrics["base_version"]
    assert repair_metrics["ok"] is True
    assert repair_metrics["total_rows"] == len(image_ids)
    assert repair_metrics["rows_filled"] == len(image_ids)
    if repair_metrics.get("errors") is not None:
        assert repair_metrics["errors"] == 0
        assert repair_metrics["downloaded_ok"] == len(image_ids)

    # carried siblings survive on every row (sparse relocates the repaired row, so
    # compare by row_index, not physical order)
    ds = lance.dataset(uri)
    got = ds.to_table(
        columns=[
            "row_index",
            constants.ingest_seed_id_col(suffix),
            constants.ingest_url_col(suffix),
        ]
    ).sort_by("row_index")
    assert got.column(constants.ingest_seed_id_col(suffix)).to_pylist() == image_ids
    assert got.column(constants.ingest_url_col(suffix)).to_pylist() == [
        loc["url"] for loc in locs
    ]
