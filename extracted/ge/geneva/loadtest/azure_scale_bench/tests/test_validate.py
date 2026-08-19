# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for validate.py pure helpers (bucketing + ok-gating)."""

from __future__ import annotations

from loadtest.azure_scale_bench import validate


def test_bucket_of() -> None:
    assert validate.bucket_of(0) == "out_of_range"
    assert validate.bucket_of(500) == "lt_1kib"
    assert validate.bucket_of(2000) == "1_4kib"
    assert validate.bucket_of(100 << 20) == "gt_64mib"
    assert validate.bucket_of(200 << 20) == "out_of_range"


def test_size_histogram_counts() -> None:
    hist = validate.size_histogram([500, 2000, 2000, 0])
    assert hist["lt_1kib"] == 1
    assert hist["1_4kib"] == 2
    assert hist["out_of_range"] == 1  # the size-0 (errored) row


def test_histogram_rows_sum_to_sample() -> None:
    hist = validate.size_histogram([500, 2000, 2000])
    rows = validate.histogram_rows(hist)
    assert sum(count for _, count, *_ in rows) == 3


def test_validation_ok_truth_table() -> None:
    base = {
        "schema_ok": True,
        "sampled_rows": 10,
        "decode_tried": 8,
        "decode_pillow_ok": 8,
    }
    assert validate.validation_ok(base)
    assert not validate.validation_ok({**base, "schema_ok": False})
    assert not validate.validation_ok({**base, "sampled_rows": 0})
    assert not validate.validation_ok({**base, "decode_tried": 0})
    assert not validate.validation_ok({**base, "decode_pillow_ok": 7})
