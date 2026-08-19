# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for the expansion UDF output struct, row mapping, and backfill args."""

from __future__ import annotations

import pyarrow as pa

from loadtest.azure_scale_bench import constants, expand_images, runner
from loadtest.azure_scale_bench.benchmark_env import BenchConfig

SUMMARY = "the quick brown fox jumps over the lazy dog"


def test_combo_struct_has_blob_image_and_scalars() -> None:
    suffix = "smoke1"
    struct = expand_images.combo_struct(suffix)
    assert pa.types.is_struct(struct)

    image_field = struct.field(constants.struct_col(suffix))
    assert pa.types.is_struct(image_field.type)
    child = image_field.type.field("image_bytes")
    assert pa.types.is_large_binary(child.type)
    assert child.metadata is not None
    assert child.metadata.get(b"lance-encoding:blob") == b"true"
    assert image_field.type.field("time").type == pa.int32()
    assert image_field.type.field("error").type == pa.string()

    names = [struct.field(i).name for i in range(struct.num_fields)]
    assert names[0] == constants.struct_col(suffix)
    assert names[1:] == constants.meta_cols(suffix)


def test_expand_row_shape_and_actual_bytes() -> None:
    row = expand_images.expand_row(
        42,
        SUMMARY,
        width=224,
        height=224,
        image_format="png",
        include_large_tail=False,
        max_bytes=64 << 10,
        font_dir="/nonexistent",
    )
    # Output is the image struct followed by the seven metadata scalars.
    assert len(row) == 1 + len(constants.META_FIELDS)
    image_value, *scalars = row
    assert len(image_value) == 3
    image_bytes, time_val, error = image_value
    assert isinstance(image_bytes, bytes)
    assert time_val is None
    assert error is None
    actual_bytes = scalars[5]
    assert actual_bytes == len(image_bytes)
    assert scalars[6] == "png"


def test_expand_row_error_path_captures_exception(monkeypatch) -> None:  # noqa: ANN001
    def boom(*args, **kwargs):  # noqa: ANN002, ANN003, ANN202
        raise RuntimeError("render failed")

    monkeypatch.setattr(expand_images.image_render, "build_payload", boom)
    row = expand_images.expand_row(
        1,
        SUMMARY,
        width=224,
        height=224,
        image_format="png",
        include_large_tail=False,
        max_bytes=None,
        font_dir=None,
    )
    image_value = row[0]
    assert image_value[0] is None  # image_bytes
    assert "render failed" in image_value[2]  # error
    assert row[2] in constants.FONTS  # font still derived


def test_fragment_window_where() -> None:
    cfg = BenchConfig(num_frags=1)
    assert runner.fragment_window_where(cfg) == "row_index >= 0 AND row_index < 1000000"

    cfg = BenchConfig(num_frags=3, skip_frags=2)
    assert (
        runner.fragment_window_where(cfg)
        == "row_index >= 2000000 AND row_index < 5000000"
    )

    cfg = BenchConfig(num_frags=1, where="error IS NOT NULL")
    assert runner.fragment_window_where(cfg) == (
        "row_index >= 0 AND row_index < 1000000 AND (error IS NOT NULL)"
    )

    assert runner.fragment_window_where(BenchConfig()) is None


def test_scoped_row_count() -> None:
    # --num-frags only: arithmetic from the fragment layout (count_rows unused).
    assert (
        runner.scoped_row_count(BenchConfig(num_frags=3), lambda f=None: 0) == 3_000_000
    )
    # No scope: full table count.
    assert runner.scoped_row_count(BenchConfig(), lambda f=None: 999) == 999
    # --where: counts rows matching the (combined) filter, not the full table.
    seen: dict[str, str | None] = {}

    def _count(f: str | None = None) -> int:
        seen["filter"] = f
        return 42

    assert runner.scoped_row_count(BenchConfig(where="x IS NOT NULL"), _count) == 42
    assert seen["filter"] is not None
    assert "x IS NOT NULL" in seen["filter"]


def test_rows_per_fragment_windowing() -> None:
    # Non-default rows_per_fragment flows into the window math.
    cfg = BenchConfig(rows_per_fragment=10, num_frags=2, skip_frags=3)
    assert runner.fragment_window_where(cfg) == "row_index >= 30 AND row_index < 50"
    assert runner.scoped_row_count(cfg, lambda f=None: 0) == 20  # arithmetic, no query

    # --skip-frags alone has no upper bound → must count the filter, not the table.
    seen: dict[str, str | None] = {}

    def _count(f: str | None = None) -> int:
        seen["filter"] = f
        return 5

    skip_only = BenchConfig(rows_per_fragment=10, skip_frags=3)
    assert runner.scoped_row_count(skip_only, _count) == 5
    assert seen["filter"] == "row_index >= 30"


def test_udf_version_tracks_knobs() -> None:
    a = expand_images.udf_version(BenchConfig(max_image_bytes=1024))
    b = expand_images.udf_version(BenchConfig(max_image_bytes=2048))
    same = expand_images.udf_version(BenchConfig(max_image_bytes=1024))
    assert a == same
    assert a != b  # changed knob ⇒ distinct checkpoint identity
    assert a.startswith("0.1-")


def test_backfill_kwargs_maps_knobs() -> None:
    cfg = BenchConfig(
        concurrency=16,
        intra_concurrency=2,
        num_frags=1,
        task_size=2048,
        commit_granularity_pct=5.0,
    )
    kwargs = runner.backfill_kwargs(cfg, num_fragments=1000)
    assert kwargs["concurrency"] == 16
    assert kwargs["intra_applier_concurrency"] == 2
    assert kwargs["task_size"] == 2048
    assert kwargs["where"] == "row_index >= 0 AND row_index < 1000000"
    assert kwargs["commit_granularity"] == 50  # 5% of 1000
    # blob_read_strategy only when requested (normalize/phash).
    assert "blob_read_strategy" not in kwargs
    assert (
        runner.backfill_kwargs(cfg, blob_read_strategy="range")["blob_read_strategy"]
        == "range"
    )


def test_udf_size_kwargs_maps_checkpoint_bounds() -> None:
    cfg = BenchConfig(
        batch_size=128,
        checkpoint_size=256,
        min_checkpoint_size=64,
        max_checkpoint_size=512,
    )
    assert runner.udf_size_kwargs(cfg) == {
        "batch_size": 128,
        "checkpoint_size": 256,
        "min_checkpoint_size": 64,
        "max_checkpoint_size": 512,
    }
