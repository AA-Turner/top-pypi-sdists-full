# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for normalize and phash UDF bodies (Pillow; no Ray/Azure)."""

from __future__ import annotations

import io
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pyarrow as pa
import pytest
from PIL import Image

from loadtest.azure_scale_bench import (
    constants,
    dedupe_inject,
    failure_inject,
    normalize,
    phash,
    runner,
)
from loadtest.azure_scale_bench.benchmark_env import BenchConfig


def _png(width: int = 50, height: int = 40, color: tuple = (10, 20, 30)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (width, height), color).save(buffer, format="PNG")
    return buffer.getvalue()


def _cfg(**overrides: Any) -> BenchConfig:
    return BenchConfig(**overrides)


def test_normalize_grayscales_and_resizes() -> None:
    out, err = normalize.normalize_image(_png(), size=32)
    assert err is None
    assert out is not None
    with Image.open(io.BytesIO(out)) as img:
        assert img.size == (32, 32)
        assert img.mode == "L"


def test_normalize_empty_and_bad_inputs() -> None:
    assert normalize.normalize_image(None, size=32) == (None, "empty input")
    assert normalize.normalize_image(b"", size=32) == (None, "empty input")
    out, err = normalize.normalize_image(b"not an image", size=32)
    assert out is None
    assert err is not None


def test_compute_phash_shape_and_determinism() -> None:
    data = _png()
    h = phash.compute_phash(data)
    assert h is not None
    assert len(h) == 8
    assert all(0 <= b <= 255 for b in h)
    assert h == phash.compute_phash(data)


def test_compute_phash_bad_input_returns_none() -> None:
    assert phash.compute_phash(None) is None
    assert phash.compute_phash(b"") is None
    assert phash.compute_phash(b"garbage") is None


def test_stages_accept_file_like_blob() -> None:
    # The range blob reader passes a file-like object, not raw bytes.
    out, err = normalize.normalize_image(io.BytesIO(_png()), size=16)
    assert err is None
    assert out is not None
    assert phash.compute_phash(io.BytesIO(_png())) is not None


def test_phash_row_computes_without_injection() -> None:
    data = _png()
    assert phash.phash_row(
        1, data, duplicate_pct=0.0, num_groups=0, bit_flips=2
    ) == phash.compute_phash(data)


def test_phash_row_uses_injection_when_member() -> None:
    # pct=1.0 ⇒ every row is a member ⇒ injected hash overrides the image.
    injected = phash.phash_row(3, _png(), duplicate_pct=1.0, num_groups=10, bit_flips=2)
    expected = dedupe_inject.injected_hash(
        3, duplicate_pct=1.0, num_groups=10, bit_flips=2
    )
    assert injected == expected


def test_normalize_row_injected_failure() -> None:
    out, err = normalize.normalize_row(
        0, _png(), size=32, inject_rate=1.0, inject_seed=0
    )
    assert out is None
    assert err == failure_inject.INJECTED_ERROR


def test_normalize_row_without_injection_normalizes() -> None:
    out, err = normalize.normalize_row(
        0, _png(), size=16, inject_rate=0.0, inject_seed=0
    )
    assert err is None
    assert out is not None


def test_phash_row_injected_failure_returns_none() -> None:
    # injection wins over duplicate injection: a failed pHash is null regardless
    assert (
        phash.phash_row(
            0,
            _png(),
            duplicate_pct=1.0,
            num_groups=10,
            bit_flips=2,
            inject_rate=1.0,
            inject_seed=0,
        )
        is None
    )


def test_injected_same_group_rows_cluster() -> None:
    num_groups, bit_flips = 6, 2
    groups: dict[int, list[int]] = {}
    for i in range(200):
        g = dedupe_inject.expected_group(i, duplicate_pct=1.0, num_groups=num_groups)
        assert g is not None
        groups.setdefault(g, []).append(i)
    pair = next(rows for rows in groups.values() if len(rows) >= 2)[:2]
    h1 = phash.phash_row(
        pair[0], None, duplicate_pct=1.0, num_groups=num_groups, bit_flips=bit_flips
    )
    h2 = phash.phash_row(
        pair[1], None, duplicate_pct=1.0, num_groups=num_groups, bit_flips=bit_flips
    )
    assert h1 is not None
    assert h2 is not None
    assert dedupe_inject.hamming(h1, h2) <= 2 * bit_flips


# --- batched normalize: builder shape, versions, ordering, memory ------------

_INPUT_COL = f"{constants.struct_col('smoke1')}.image_bytes"


def test_build_normalize_udf_batched_is_array_input() -> None:
    from geneva.transformer import UDFArgType

    scalar = normalize.build_normalize_udf(_cfg(), _INPUT_COL)
    assert scalar.arg_type == UDFArgType.SCALAR

    batched = normalize.build_normalize_udf_batched(
        _cfg(normalize_concurrency=4), _INPUT_COL
    )
    assert batched.arg_type == UDFArgType.ARRAY
    assert batched.is_multi_output is False  # batched UDFs cannot be Columns[...]
    assert batched.data_type == normalize._NORM_STRUCT
    assert batched.input_columns == [_cfg().row_index_col, _INPUT_COL]


def test_udf_resource_kwargs_omits_num_cpus_when_unset() -> None:
    # The real invariant: no explicit num_cpus is marshaled unless --per-actor-cpus is
    # set, so the geneva @udf default (1 CPU) stands and scheduling is unchanged.
    kwargs = runner.udf_resource_kwargs(_cfg())
    assert "num_cpus" not in kwargs
    assert "memory" in kwargs  # per-actor memory is always reserved


def test_udf_resource_kwargs_includes_num_cpus_when_set() -> None:
    assert runner.udf_resource_kwargs(_cfg(per_actor_cpus=4))["num_cpus"] == 4.0


def test_normalize_udf_reserves_per_actor_cpus() -> None:
    scalar = normalize.build_normalize_udf(_cfg(per_actor_cpus=4), _INPUT_COL)
    assert scalar.num_cpus == 4.0
    batched = normalize.build_normalize_udf_batched(
        _cfg(normalize_concurrency=8, per_actor_cpus=4), _INPUT_COL
    )
    assert batched.num_cpus == 4.0


def test_normalize_udf_default_cpu_reservation_unchanged() -> None:
    # Unset per_actor_cpus ⇒ geneva @udf default (1 CPU); memory still reserved.
    udf = normalize.build_normalize_udf(_cfg(), _INPUT_COL)
    assert udf.num_cpus == 1.0
    assert udf.memory == int(1.5 * 1024**3)


def test_batched_plan_warns_without_cpu_reservation(caplog) -> None:  # noqa: ANN001
    with caplog.at_level(logging.WARNING):
        normalize._log_batched_normalize_plan(_cfg(normalize_concurrency=8))
    assert any("--per-actor-cpus" in m for m in caplog.messages)


def test_batched_plan_no_warn_with_cpu_reservation(caplog) -> None:  # noqa: ANN001
    with caplog.at_level(logging.WARNING):
        normalize._log_batched_normalize_plan(
            _cfg(normalize_concurrency=8, per_actor_cpus=4)
        )
    assert not any("--per-actor-cpus" in m for m in caplog.messages)


def test_batched_plan_no_warn_single_thread(caplog) -> None:  # noqa: ANN001
    # 1 thread fits the default 1 CPU: the reservation footgun does not apply.
    with caplog.at_level(logging.WARNING):
        normalize._log_batched_normalize_plan(_cfg(normalize_concurrency=1))
    assert not any("--per-actor-cpus" in m for m in caplog.messages)


def test_normalize_scalar_udf_version_unchanged() -> None:
    # Golden value: the scalar version keys every in-flight normalize column's
    # checkpoints. If this assert fails, the change re-keys existing scalar columns
    # (a full reprocess at scale) — don't just update the literal, keep the knob
    # string backward-compatible instead.
    assert normalize._udf_version(_cfg()) == "0.1-7d0489f699"
    # normalize_concurrency must NOT perturb the scalar version.
    assert normalize._udf_version(
        _cfg(normalize_concurrency=4)
    ) == normalize._udf_version(_cfg())


def test_normalize_udf_versions_differ_by_mode_and_concurrency() -> None:
    scalar = normalize._udf_version(_cfg())
    b4 = normalize._udf_version(_cfg(normalize_concurrency=4), batched=True)
    b8 = normalize._udf_version(_cfg(normalize_concurrency=8), batched=True)
    assert scalar != b4  # scalar vs batched re-keys
    assert b4 != b8  # a concurrency change within batched mode re-keys
    # a failure-injection knob change re-keys the (scalar) version too
    assert normalize._udf_version(_cfg(inject_failure_rate=0.1)) != scalar


def test_normalize_rows_order_preserving() -> None:
    # Distinct COLOR per row so each normalized PNG is byte-distinct — a reorder or
    # duplication would change the output list. (Varying only size would be erased by
    # the resize-to-square, making the comparison tautological.)
    rows = [(i, _png(color=(10 + 20 * i, 30, 40))) for i in range(12)]
    serial = normalize.normalize_rows(
        rows, size=16, inject_rate=0.0, inject_seed=0, max_workers=1
    )
    threaded = normalize.normalize_rows(
        rows, size=16, inject_rate=0.0, inject_seed=0, max_workers=4
    )
    assert threaded == serial
    # every row normalized to a 16x16 grayscale PNG
    for out, err in threaded:
        assert err is None
        assert out is not None
        with Image.open(io.BytesIO(out)) as img:
            assert img.size == (16, 16)
            assert img.mode == "L"


def test_normalize_batch_arrays_chunk_boundary() -> None:
    n = 7
    row_index = pa.array(list(range(n)), pa.int64())
    # Distinct COLOR per row so each normalized PNG is byte-distinct — otherwise a
    # reorder/duplication across the chunk boundary would go undetected.
    image_bytes = pa.array(
        [_png(color=(10 + 20 * i, 30, 40)) for i in range(n)], pa.large_binary()
    )
    one_chunk = normalize.normalize_batch_arrays(
        row_index, image_bytes, size=16, inject_rate=0.0, inject_seed=0, chunk_rows=n
    )
    # chunk_rows=2 forces multiple chunks across a boundary; output must be identical
    chunked = normalize.normalize_batch_arrays(
        row_index,
        image_bytes,
        size=16,
        inject_rate=0.0,
        inject_seed=0,
        max_workers=3,
        chunk_rows=2,
    )
    assert chunked == one_chunk
    assert len(chunked) == n
    # matches the scalar per-row path row-for-row (parity with scalar semantics)
    expected = [
        normalize.normalize_row(
            i, image_bytes[i].as_py(), size=16, inject_rate=0.0, inject_seed=0
        )
        for i in range(n)
    ]
    assert chunked == expected


def test_normalize_rows_reuses_external_executor() -> None:
    """A passed-in executor is reused across calls (not shut down) — no per-batch pool
    churn, the property the batched UDF relies on."""
    rows = [(i, _png()) for i in range(3)]
    with ThreadPoolExecutor(max_workers=2) as pool:
        out1 = normalize.normalize_rows(
            rows, size=16, inject_rate=0.0, inject_seed=0, executor=pool
        )
        out2 = normalize.normalize_rows(
            rows, size=16, inject_rate=0.0, inject_seed=0, executor=pool
        )
    assert out1 == out2
    assert all(err is None for _, err in out1)  # pool still usable -> not shut down


def test_normalize_rows_injected_failure_batch() -> None:
    rows = [(i, _png()) for i in range(5)]
    injected = normalize.normalize_rows(
        rows, size=16, inject_rate=1.0, inject_seed=0, max_workers=2
    )
    assert all(
        out is None and err == failure_inject.INJECTED_ERROR for out, err in injected
    )
    clean = normalize.normalize_rows(
        rows, size=16, inject_rate=0.0, inject_seed=0, max_workers=2
    )
    assert all(out is not None and err is None for out, err in clean)


def test_normalize_udf_batched_no_forced_checkpoint_cap() -> None:
    # Warning-only design: the batched builder must NOT force a max_checkpoint_size.
    batched = normalize.build_normalize_udf_batched(
        _cfg(normalize_concurrency=4), _INPUT_COL
    )
    assert batched.max_checkpoint_size is None
    # an explicit --max-checkpoint-size is preserved
    explicit = normalize.build_normalize_udf_batched(
        _cfg(normalize_concurrency=4, max_checkpoint_size=8000), _INPUT_COL
    )
    assert explicit.max_checkpoint_size == 8000


def test_log_batched_normalize_plan_warns_without_checkpoint(
    caplog: Any,
) -> None:
    import logging

    with caplog.at_level(logging.WARNING, logger=normalize._LOG.name):
        normalize._log_batched_normalize_plan(_cfg(normalize_concurrency=4))
    assert any("adaptive sizing" in r.message for r in caplog.records)


# --- normalize_concurrency bounds + in-flight product guard ------------------


def test_normalize_concurrency_bounds() -> None:
    _cfg(normalize_concurrency=1).validate()  # lower bound ok
    _cfg(normalize_concurrency=8).validate()  # mid-range ok
    _cfg(normalize_concurrency=constants.MAX_NORMALIZE_CONCURRENCY).validate()  # upper
    with pytest.raises(ValueError, match="normalize_concurrency"):
        _cfg(normalize_concurrency=0).validate()
    with pytest.raises(ValueError, match="normalize_concurrency"):
        _cfg(normalize_concurrency=constants.MAX_NORMALIZE_CONCURRENCY + 1).validate()


def test_normalize_in_flight_product_guard() -> None:
    # within the default ceiling: 8 * 1 * 8 = 64
    _cfg(normalize_concurrency=8).validate()
    # exceeds the default 50_000: 2048 * 1 * 32 = 65_536 — message names CPU transforms
    with pytest.raises(ValueError, match="concurrent image transforms"):
        _cfg(concurrency=2048, normalize_concurrency=32).validate()
    # intra_concurrency participates: 100 * 10 * 100 = 100_000
    with pytest.raises(ValueError, match="intra_concurrency"):
        _cfg(
            concurrency=100, intra_concurrency=10, normalize_concurrency=100
        ).validate()
    # raising --max-in-flight is the intentional escape hatch
    _cfg(concurrency=2048, normalize_concurrency=32, max_in_flight=100_000).validate()
    # the guard only applies to the batched normalizer (normalize_concurrency set)
    _cfg(concurrency=100_000).validate()


# --- Ray E2E: batched vs scalar normalize over the range blob path -----------

# Same nested image struct download-images produces (blob-encoded image_bytes), so the
# range reader decomposes it and materializes the blob leaf just like production.
_E2E_STRUCT = pa.struct(
    [
        pa.field("image_bytes", pa.large_binary(), metadata=constants.MMLB_BLOB_META),
        pa.field("time", pa.int32(), nullable=True),
        pa.field("error", pa.string(), nullable=True),
    ]
)


def _build_norm_input_table(uri: str, suffix: str, images: list[bytes]) -> None:
    """Write a Lance table with row_index + a nested blob image struct."""
    import lance

    struct_col = constants.struct_col(suffix)
    struct_vals = [{"image_bytes": img, "time": None, "error": None} for img in images]
    table = pa.table(
        {
            "row_index": pa.array(list(range(len(images))), pa.int64()),
            struct_col: pa.array(struct_vals, _E2E_STRUCT),
        }
    )
    lance.write_dataset(table, uri, data_storage_version=constants.DATA_STORAGE_VERSION)
    # Confirm the nested blob marker survived the write, so the range reader engages.
    ds = lance.dataset(uri)
    img_field = ds.schema.field(struct_col).type.field("image_bytes")
    assert img_field.metadata.get(b"lance-encoding:blob") == b"true"


@pytest.mark.ray
def test_batched_normalize_matches_scalar_over_range_blob(tmp_path: Any) -> None:
    """run_normalize (blob_read_strategy='range') over a nested image blob struct.

    Scalar and batched must classify every row identically — normal, per-row decode
    error, and deterministic injected failure — proving the batched UDF correctly
    consumes a range-materialized blob column (the first batched consumer to do so).
    """
    import lance

    n = 8
    rate, seed = 0.5, 16
    injected = {
        i for i in range(n) if failure_inject.should_fail(i, rate=rate, seed=seed)
    }
    good = [i for i in range(n) if i not in injected]
    assert injected, injected  # the chosen seed injects a deterministic subset
    assert good, good  # ...and leaves clean rows to normalize
    garbage_idx = good[0]  # a real decode error, distinct from injected failures
    images = [
        b"not-a-png" if i == garbage_idx else _png(width=12 + i, height=10 + i)
        for i in range(n)
    ]

    suffix = "nrm1"
    norm = constants.norm_col(suffix)

    def _run(name: str, normalize_concurrency: int | None) -> dict[str, int]:
        uri = str(tmp_path / f"{name}.lance")
        _build_norm_input_table(uri, suffix, images)
        cfg = _cfg(
            bench_uri=uri,
            suffix=suffix,
            concurrency=1,
            intra_concurrency=1,
            normalize_concurrency=normalize_concurrency,
            inject_failure_rate=rate,
            inject_failure_seed=seed,
            norm_size=16,
        )
        metrics = normalize.run_normalize(cfg)
        assert metrics["normalize_concurrency"] == normalize_concurrency
        ds = lance.dataset(uri)
        assert norm in ds.schema.names
        return {
            "injected": ds.count_rows(filter=f"{norm}.error = 'injected failure'"),
            "errored": ds.count_rows(
                filter=f"{norm}.error IS NOT NULL "
                f"AND {norm}.error != 'injected failure'"
            ),
            # ok REQUIRES non-null normalized bytes: an error-null row with null bytes
            # (a struct-packing regression) must not count as a success.
            "ok": ds.count_rows(
                filter=f"{norm}.error IS NULL AND {norm}.image_bytes IS NOT NULL"
            ),
            # Must be 0: no row may have both null error and null bytes.
            "orphan_null": ds.count_rows(
                filter=f"{norm}.error IS NULL AND {norm}.image_bytes IS NULL"
            ),
            # Bytes exist iff the row normalized OK (error rows carry null bytes).
            "bytes_present": ds.count_rows(filter=f"{norm}.image_bytes IS NOT NULL"),
        }

    scalar_counts = _run("norm_scalar", None)
    batched_counts = _run("norm_batched", 4)

    assert scalar_counts == batched_counts  # scalar/batched parity over the range path
    assert scalar_counts["injected"] == len(injected)
    assert scalar_counts["errored"] == 1  # the single garbage row
    assert scalar_counts["ok"] == n - len(injected) - 1
    assert scalar_counts["orphan_null"] == 0  # no (null error, null bytes) rows
    assert scalar_counts["bytes_present"] == scalar_counts["ok"]  # bytes iff ok


# --- batched phash: builder shape, versions, ordering, injection -------------

_PHASH_INPUT_COL = f"{constants.norm_col('smoke1')}.image_bytes"


def test_build_phash_udf_batched_is_array_input() -> None:
    from geneva.transformer import UDFArgType

    scalar = phash.build_phash_udf(_cfg(), _PHASH_INPUT_COL, 0)
    assert scalar.arg_type == UDFArgType.SCALAR

    batched = phash.build_phash_udf_batched(
        _cfg(phash_concurrency=4), _PHASH_INPUT_COL, 0
    )
    assert batched.arg_type == UDFArgType.ARRAY
    assert batched.is_multi_output is False  # batched UDFs cannot be Columns[...]
    assert batched.data_type == phash._PHASH_TYPE
    assert batched.input_columns == [_cfg().row_index_col, _PHASH_INPUT_COL]


def test_phash_udf_reserves_per_actor_cpus() -> None:
    scalar = phash.build_phash_udf(_cfg(per_actor_cpus=4), _PHASH_INPUT_COL, 0)
    assert scalar.num_cpus == 4.0
    batched = phash.build_phash_udf_batched(
        _cfg(phash_concurrency=8, per_actor_cpus=4), _PHASH_INPUT_COL, 0
    )
    assert batched.num_cpus == 4.0


def test_phash_udf_default_cpu_reservation_unchanged() -> None:
    # Unset per_actor_cpus ⇒ geneva @udf default (1 CPU); memory still reserved.
    udf = phash.build_phash_udf(_cfg(), _PHASH_INPUT_COL, 0)
    assert udf.num_cpus == 1.0
    assert udf.memory == int(1.5 * 1024**3)


def test_batched_phash_plan_warns_without_cpu_reservation(caplog) -> None:  # noqa: ANN001
    with caplog.at_level(logging.WARNING):
        phash._log_batched_phash_plan(_cfg(phash_concurrency=8))
    assert any("--per-actor-cpus" in m for m in caplog.messages)


def test_batched_phash_plan_no_warn_with_cpu_reservation(caplog) -> None:  # noqa: ANN001
    with caplog.at_level(logging.WARNING):
        phash._log_batched_phash_plan(_cfg(phash_concurrency=8, per_actor_cpus=4))
    assert not any("--per-actor-cpus" in m for m in caplog.messages)


def test_batched_phash_plan_no_warn_single_thread(caplog) -> None:  # noqa: ANN001
    # 1 thread fits the default 1 CPU: the reservation footgun does not apply.
    with caplog.at_level(logging.WARNING):
        phash._log_batched_phash_plan(_cfg(phash_concurrency=1))
    assert not any("--per-actor-cpus" in m for m in caplog.messages)


def test_phash_scalar_udf_version_unchanged() -> None:
    # Golden value: the scalar version keys every in-flight phash column's
    # checkpoints. If this assert fails, the change re-keys existing scalar columns
    # (a full reprocess at scale) — don't just update the literal, keep the knob
    # string backward-compatible instead.
    assert phash._udf_version(_cfg(), 0) == "0.1-ff126b8125"
    # phash_concurrency must NOT perturb the scalar version.
    assert phash._udf_version(_cfg(phash_concurrency=4), 0) == phash._udf_version(
        _cfg(), 0
    )


def test_phash_udf_versions_differ_by_mode_and_concurrency() -> None:
    scalar = phash._udf_version(_cfg(), 0)
    b4 = phash._udf_version(_cfg(phash_concurrency=4), 0, batched=True)
    b8 = phash._udf_version(_cfg(phash_concurrency=8), 0, batched=True)
    assert scalar != b4  # scalar vs batched re-keys
    assert b4 != b8  # a concurrency change within batched mode re-keys
    # a dedupe/failure knob change re-keys the (scalar) version too
    assert phash._udf_version(_cfg(duplicate_pct=0.1), 0) != scalar


def test_phash_rows_order_preserving() -> None:
    # The injected-hash path keys each row's hash on row_index, so outputs are
    # distinct per row (asserted below) — a reorder or duplication would change the
    # output list. (Solid-color PNGs can share a perceptual hash, which would make a
    # content-based comparison tautological, so drive distinctness via injection.)
    n = 12
    row_indices = list(range(n))
    images = [_png() for _ in range(n)]  # content irrelevant: injection overrides
    kw: dict[str, Any] = {
        "duplicate_pct": 1.0,
        "num_groups": n,
        "bit_flips": 2,
        "inject_rate": 0.0,
        "inject_seed": 0,
    }
    serial = phash.phash_rows(row_indices, images, max_workers=1, **kw)
    threaded = phash.phash_rows(row_indices, images, max_workers=4, **kw)
    assert all(h is not None for h in serial)  # injection populates every row
    assert len({tuple(h) for h in serial if h is not None}) == n  # distinctness guard
    assert threaded == serial
    # parity with the scalar per-row path (both could be equally wrong otherwise)
    expected = [phash.phash_row(i, images[i], **kw) for i in range(n)]
    assert serial == expected


def test_phash_rows_edge_lengths() -> None:
    kw: dict[str, Any] = {"duplicate_pct": 0.0, "num_groups": 0, "bit_flips": 2}
    assert phash.phash_rows([], [], **kw) == []
    one = phash.phash_rows([0], [_png()], **kw)
    assert one == [phash.compute_phash(_png())]  # single row → scalar compute


def test_phash_rows_reuses_external_executor() -> None:
    """A passed-in executor is reused across calls (not shut down) — no per-batch pool
    churn, the property the batched UDF relies on."""
    row_indices = list(range(3))
    images = [_png() for _ in range(3)]
    kw: dict[str, Any] = {"duplicate_pct": 0.0, "num_groups": 0, "bit_flips": 2}
    with ThreadPoolExecutor(max_workers=2) as pool:
        out1 = phash.phash_rows(row_indices, images, executor=pool, **kw)
        out2 = phash.phash_rows(row_indices, images, executor=pool, **kw)
    assert out1 == out2
    assert all(h is not None for h in out1)  # pool still usable -> not shut down


def test_phash_rows_injected_failure_batch() -> None:
    row_indices = list(range(5))
    images = [_png() for _ in range(5)]
    # injection wins over duplicate injection: a failed pHash is null regardless
    injected = phash.phash_rows(
        row_indices,
        images,
        duplicate_pct=1.0,
        num_groups=10,
        bit_flips=2,
        inject_rate=1.0,
        inject_seed=0,
        max_workers=2,
    )
    assert all(h is None for h in injected)
    clean = phash.phash_rows(
        row_indices, images, duplicate_pct=0.0, num_groups=0, bit_flips=2, max_workers=2
    )
    assert all(h is not None for h in clean)


def test_phash_rows_duplicate_injection_batch() -> None:
    n = 6
    row_indices = list(range(n))
    images = [_png() for _ in range(n)]
    out = phash.phash_rows(
        row_indices,
        images,
        duplicate_pct=1.0,
        num_groups=10,
        bit_flips=2,
        max_workers=3,
    )
    for i, h in zip(row_indices, out, strict=True):
        assert h == dedupe_inject.injected_hash(
            i, duplicate_pct=1.0, num_groups=10, bit_flips=2
        )


def test_phash_rows_none_and_bad_bytes() -> None:
    # duplicate_pct=0.0 ⇒ no injection: None/garbage bytes → None in both paths.
    row_indices = [0, 1, 2]
    values: list[Any] = [None, b"garbage", _png()]
    kw: dict[str, Any] = {"duplicate_pct": 0.0, "num_groups": 0, "bit_flips": 2}
    serial = phash.phash_rows(row_indices, values, max_workers=1, **kw)
    threaded = phash.phash_rows(row_indices, values, max_workers=2, **kw)
    assert serial[0] is None
    assert serial[1] is None
    assert serial[2] is not None
    assert threaded == serial
    expected = [
        phash.phash_row(i, v, **kw) for i, v in zip(row_indices, values, strict=True)
    ]
    assert serial == expected


def test_phash_rows_length_mismatch() -> None:
    with pytest.raises(ValueError, match="length mismatch"):
        phash.phash_rows([0, 1], [_png()], duplicate_pct=0.0, num_groups=0, bit_flips=2)


def test_phash_batch_arrays_chunk_boundary() -> None:
    n = 7
    row_index = pa.array(list(range(n)), pa.int64())
    image_bytes = pa.array([_png() for _ in range(n)], pa.large_binary())
    # Injection keys each row's hash on row_index ⇒ distinct per row (asserted), so a
    # reorder/duplication across the chunk boundary would be detected. (Solid-color
    # PNGs can share a perceptual hash, which would make the comparison tautological.)
    kw: dict[str, Any] = {"duplicate_pct": 1.0, "num_groups": n, "bit_flips": 2}
    one_chunk = phash.phash_batch_arrays(row_index, image_bytes, chunk_rows=n, **kw)
    # chunk_rows=2 forces multiple chunks across a boundary; output must be identical
    chunked = phash.phash_batch_arrays(
        row_index, image_bytes, max_workers=3, chunk_rows=2, **kw
    )
    assert all(h is not None for h in one_chunk)
    assert (
        len({tuple(h) for h in one_chunk if h is not None}) == n
    )  # distinctness guard
    assert chunked == one_chunk
    assert len(chunked) == n
    # matches the scalar per-row path row-for-row (parity with scalar semantics)
    expected = [phash.phash_row(i, image_bytes[i].as_py(), **kw) for i in range(n)]
    assert chunked == expected


def test_log_batched_phash_plan_warns_without_checkpoint(caplog: Any) -> None:
    with caplog.at_level(logging.WARNING, logger=phash._LOG.name):
        phash._log_batched_phash_plan(_cfg(phash_concurrency=4))
    assert any("adaptive sizing" in r.message for r in caplog.records)


def test_log_batched_phash_plan_no_warn_with_checkpoint(caplog: Any) -> None:
    with caplog.at_level(logging.WARNING, logger=phash._LOG.name):
        phash._log_batched_phash_plan(_cfg(phash_concurrency=4, checkpoint_size=1024))
    assert not any("adaptive sizing" in r.message for r in caplog.records)


def test_phash_udf_batched_no_forced_checkpoint_cap() -> None:
    # Warning-only design: the batched builder must NOT force a max_checkpoint_size.
    batched = phash.build_phash_udf_batched(
        _cfg(phash_concurrency=4), _PHASH_INPUT_COL, 0
    )
    assert batched.max_checkpoint_size is None
    # an explicit --max-checkpoint-size is preserved
    explicit = phash.build_phash_udf_batched(
        _cfg(phash_concurrency=4, max_checkpoint_size=8000), _PHASH_INPUT_COL, 0
    )
    assert explicit.max_checkpoint_size == 8000


def test_build_phash_udf_batched_is_picklable() -> None:
    # The primary stated risk: the lazy pool_box must not capture a live executor at
    # ship time, so the builder's output must cloudpickle cleanly (as Ray ships it).
    import cloudpickle

    udf = phash.build_phash_udf_batched(_cfg(phash_concurrency=4), _PHASH_INPUT_COL, 0)
    blob = cloudpickle.dumps(udf)  # built but never called → pool_box[0] is None
    assert isinstance(blob, bytes)
    assert len(blob) > 0


# --- phash_concurrency bounds + in-flight product guard ----------------------


def test_phash_concurrency_bounds() -> None:
    _cfg(phash_concurrency=1).validate()  # lower bound ok
    _cfg(phash_concurrency=8).validate()  # mid-range ok
    _cfg(phash_concurrency=constants.MAX_PHASH_CONCURRENCY).validate()  # upper
    with pytest.raises(ValueError, match="phash_concurrency"):
        _cfg(phash_concurrency=0).validate()
    with pytest.raises(ValueError, match="phash_concurrency"):
        _cfg(phash_concurrency=constants.MAX_PHASH_CONCURRENCY + 1).validate()


def test_phash_in_flight_product_guard() -> None:
    # within the default ceiling: 8 * 1 * 8 = 64
    _cfg(phash_concurrency=8).validate()
    # exceeds the default 50_000: 2048 * 1 * 32 = 65_536 — message names computations
    with pytest.raises(ValueError, match="concurrent pHash computations"):
        _cfg(concurrency=2048, phash_concurrency=32).validate()
    # intra_concurrency participates: 100 * 10 * 100 = 100_000
    with pytest.raises(ValueError, match="intra_concurrency"):
        _cfg(concurrency=100, intra_concurrency=10, phash_concurrency=100).validate()
    # raising --max-in-flight is the intentional escape hatch
    _cfg(concurrency=2048, phash_concurrency=32, max_in_flight=100_000).validate()
    # the guard only applies to the batched pHash UDF (phash_concurrency set)
    _cfg(concurrency=100_000).validate()


# --- Ray E2E: batched vs scalar phash over the range blob path ---------------


def _build_phash_input_table(uri: str, suffix: str, images: list[bytes]) -> None:
    """Write a Lance table with row_index + a nested blob normalized-image struct."""
    import lance

    norm = constants.norm_col(suffix)
    struct_vals = [{"image_bytes": img, "error": None} for img in images]
    table = pa.table(
        {
            "row_index": pa.array(list(range(len(images))), pa.int64()),
            norm: pa.array(struct_vals, normalize._NORM_STRUCT),
        }
    )
    lance.write_dataset(table, uri, data_storage_version=constants.DATA_STORAGE_VERSION)
    # Confirm the nested blob marker survived the write, so the range reader engages.
    ds = lance.dataset(uri)
    img_field = ds.schema.field(norm).type.field("image_bytes")
    assert img_field.metadata.get(b"lance-encoding:blob") == b"true"


@pytest.mark.ray
def test_batched_phash_matches_scalar_over_range_blob(tmp_path: Any) -> None:
    """run_phash (blob_read_strategy='range') over a nested normalized-image struct.

    Scalar and batched must produce identical pHashes per row and null the same rows
    (both an injected failure and a garbage image null to None — phash has no error
    field). Proves the batched UDF correctly consumes a range-materialized blob column.
    """
    import lance

    n = 8
    rate, seed = 0.5, 16
    injected = {
        i for i in range(n) if failure_inject.should_fail(i, rate=rate, seed=seed)
    }
    good = [i for i in range(n) if i not in injected]
    assert injected, injected  # the chosen seed injects a deterministic subset
    assert good, good  # ...and leaves clean rows to hash
    garbage_idx = good[0]  # a real decode failure, distinct from injected failures
    images = [
        b"not-a-png" if i == garbage_idx else _png(width=12 + i, height=10 + i)
        for i in range(n)
    ]

    suffix = "phb1"
    phash_col = constants.phash_col(suffix)

    def _run(name: str, phash_concurrency: int | None) -> dict[Any, Any]:
        uri = str(tmp_path / f"{name}.lance")
        _build_phash_input_table(uri, suffix, images)
        cfg = _cfg(
            bench_uri=uri,
            suffix=suffix,
            concurrency=1,
            intra_concurrency=1,
            phash_concurrency=phash_concurrency,
            inject_failure_rate=rate,
            inject_failure_seed=seed,
            duplicate_pct=0.0,  # parity over real hashes + failures, no dup injection
        )
        metrics = phash.run_phash(cfg)
        assert metrics["phash_concurrency"] == phash_concurrency
        ds = lance.dataset(uri)
        assert phash_col in ds.schema.names
        tbl = ds.to_table(columns=["row_index", phash_col])
        idxs = tbl.column("row_index").to_pylist()
        hashes = tbl.column(phash_col).to_pylist()
        # Row-keyed so the comparison is robust to any row reordering.
        return {
            ri: (tuple(h) if h is not None else None)
            for ri, h in zip(idxs, hashes, strict=True)
        }

    scalar = _run("phash_scalar", None)
    batched = _run("phash_batched", 4)

    assert scalar == batched  # scalar/batched parity over the range path (all rows)
    null_rows = {ri for ri, h in scalar.items() if h is None}
    assert null_rows == injected | {garbage_idx}  # injected + garbage both null
    populated = {ri for ri, h in scalar.items() if h is not None}
    assert len(populated) == n - len(injected | {garbage_idx})
