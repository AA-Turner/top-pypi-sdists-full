# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for deterministic row-wise failure injection."""

from __future__ import annotations

from loadtest.azure_scale_bench import (
    download_images,
    failure_inject,
    normalize,
    phash,
)
from loadtest.azure_scale_bench.benchmark_env import BenchConfig


def test_rate_bounds() -> None:
    # rate 0 never fails; rate >= 1 always fails — for any row/seed.
    assert not any(failure_inject.should_fail(i, rate=0.0, seed=7) for i in range(100))
    assert all(failure_inject.should_fail(i, rate=1.0, seed=7) for i in range(100))


def test_deterministic() -> None:
    a = failure_inject.should_fail(12345, rate=0.3, seed=1)
    b = failure_inject.should_fail(12345, rate=0.3, seed=1)
    assert a == b


def test_fraction_is_approximately_rate() -> None:
    n, rate = 5000, 0.3
    failed = sum(failure_inject.should_fail(i, rate=rate, seed=0) for i in range(n))
    assert 0.25 < failed / n < 0.35  # within tolerance of the target fraction


def test_seed_changes_selection() -> None:
    sel0 = {i for i in range(2000) if failure_inject.should_fail(i, rate=0.3, seed=0)}
    sel1 = {i for i in range(2000) if failure_inject.should_fail(i, rate=0.3, seed=1)}
    assert sel0 != sel1
    # both still ~30% of the population
    assert 0.25 < len(sel0) / 2000 < 0.35
    assert 0.25 < len(sel1) / 2000 < 0.35


# --- udf version re-keys with injection (so repair recomputes, not reuses) ---
# Each stage builds its UDF from the CURRENT config and passes it to
# backfill(udf=...) on reuse; a changed inject rate must change the UDF version so
# the repair run gets a distinct checkpoint identity and actually recomputes.


def test_download_udf_version_changes_with_injection() -> None:
    v0 = download_images._ref_udf_version(
        BenchConfig(inject_failure_rate=0.0), batched=False
    )
    v1 = download_images._ref_udf_version(
        BenchConfig(inject_failure_rate=0.05), batched=False
    )
    assert v0 != v1
    # The documented stale-checkpoint escape hatch: bumping the seed (rate still 0)
    # re-keys the UDF, forcing a clean recompute of a bad repair checkpoint.
    seed_bumped = download_images._ref_udf_version(
        BenchConfig(inject_failure_rate=0.0, inject_failure_seed=999), batched=False
    )
    assert seed_bumped != v0


def test_normalize_udf_version_changes_with_injection() -> None:
    v0 = normalize._udf_version(BenchConfig(inject_failure_rate=0.0))
    v1 = normalize._udf_version(BenchConfig(inject_failure_rate=0.05))
    assert v0 != v1
    seed_bumped = normalize._udf_version(
        BenchConfig(inject_failure_rate=0.0, inject_failure_seed=999)
    )
    assert seed_bumped != v0  # seed re-keys even with injection off


def test_phash_udf_version_changes_with_injection() -> None:
    v0 = phash._udf_version(BenchConfig(inject_failure_rate=0.0), 100)
    v1 = phash._udf_version(BenchConfig(inject_failure_rate=0.05), 100)
    assert v0 != v1
    seed_bumped = phash._udf_version(
        BenchConfig(inject_failure_rate=0.0, inject_failure_seed=999), 100
    )
    assert seed_bumped != v0  # seed re-keys even with injection off


def test_download_backfill_override_is_multi_output_plain_udf() -> None:
    # The scalar download backfill(udf=...) override on reuse/repair must be the inner
    # plain UDF (the UnpackedUDF wrapper has no validate_against_schema) AND must be
    # is_multi_output=True, or geneva rejects a udf override for the unpacked group.
    from geneva.transformer import UDF, UnpackedUDF

    udf = download_images.build_ref_download_udf(BenchConfig())
    assert isinstance(udf, UDF)
    assert udf.is_multi_output is True
    assert hasattr(udf, "validate_against_schema")
    wrapper = UnpackedUDF(udf, prefix="")
    assert wrapper.udf is udf  # the column stores/runs this inner UDF
    assert not hasattr(wrapper, "validate_against_schema")
    # the explicit data_type still drives the real (suffix-qualified, blob) schema
    assert udf.data_type == download_images.combo_struct("smoke1")
