# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for URI splitting and suffix-based output-column naming."""

from __future__ import annotations

import pytest

from loadtest.azure_scale_bench import benchmark_env, constants


def test_split_source_uri_source_and_bench() -> None:
    assert benchmark_env.split_source_uri(constants.SOURCE_URI) == (
        "az://datasets",
        constants.SOURCE_TABLE,
    )
    assert benchmark_env.split_source_uri(constants.BENCH_URI) == (
        "az://datasets",
        constants.BENCH_TABLE,
    )


def test_split_source_uri_trailing_slash_and_no_suffix() -> None:
    assert benchmark_env.split_source_uri("az://c/foo.lance/") == ("az://c", "foo")
    assert benchmark_env.split_source_uri("az://c/foo") == ("az://c", "foo")


@pytest.mark.parametrize("bad", ["", "foo", "foo.lance", "/foo.lance"])
def test_split_source_uri_rejects_unsplittable(bad: str) -> None:
    with pytest.raises(ValueError, match="cannot split"):
        benchmark_env.split_source_uri(bad)


@pytest.mark.parametrize("good", ["smoke1", "v01_baseline", "abc", "a1b2"])
def test_validate_suffix_accepts(good: str) -> None:
    assert constants.validate_suffix(good) == good
    # The metadata prefix must be a valid identifier for UnpackedUDF.
    assert (constants.meta_prefix(good) + "x").isidentifier()


@pytest.mark.parametrize("bad", ["", "bad-suffix", "has space", "dotted.suffix", "é"])
def test_validate_suffix_rejects(bad: str) -> None:
    with pytest.raises(ValueError, match="suffix"):
        constants.validate_suffix(bad)


def test_naming_helpers_consistent() -> None:
    s = "smoke1"
    assert constants.struct_col(s) == "summary_image_nested_smoke1"
    assert constants.meta_prefix(s) == "img_meta_smoke1_"
    assert constants.norm_col(s) == "image_norm_smoke1"
    assert constants.phash_col(s) == "phash_smoke1"
    assert constants.manifest_name(s) == "azure_scale_bench_smoke1"
    assert constants.actual_bytes_col(s) == "img_meta_smoke1_image_actual_bytes"
    assert constants.target_bytes_col(s) == "img_meta_smoke1_image_target_bytes"
    assert constants.ingest_seed_id_col(s) == "ingest_seed_image_id_smoke1"
    assert constants.ingest_url_col(s) == "ingest_source_url_smoke1"


def test_meta_cols_match_fields() -> None:
    s = "v01"
    cols = constants.meta_cols(s)
    assert len(cols) == len(constants.META_FIELDS)
    assert cols == [f"img_meta_{s}_{field}" for field in constants.META_FIELDS]


def test_all_suffix_columns_toggles() -> None:
    s = "v01"
    full = constants.all_suffix_columns(s)
    # struct + 7 metadata + norm + phash
    assert len(full) == 2 + len(constants.META_FIELDS) + 1
    assert constants.struct_col(s) in full
    assert constants.norm_col(s) in full
    assert constants.phash_col(s) in full

    no_downstream = constants.all_suffix_columns(
        s, include_norm=False, include_phash=False
    )
    assert constants.norm_col(s) not in no_downstream
    assert constants.phash_col(s) not in no_downstream


def test_size_bucket_weights_sum_to_one() -> None:
    total = sum(weight for _, _, _, weight in constants.SIZE_BUCKETS)
    # The spec weights sum to ~1.0 (rare >64 MiB tail nudges it slightly over).
    assert total == pytest.approx(1.0, abs=1e-4)


def test_size_buckets_are_ordered_and_contiguous() -> None:
    for (_, _, hi, _), (_, lo_next, _, _) in zip(
        constants.SIZE_BUCKETS, constants.SIZE_BUCKETS[1:], strict=False
    ):
        assert hi == lo_next, "buckets must tile the size range without gaps"
