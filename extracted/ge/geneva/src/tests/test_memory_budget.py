# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for the backfill memory budget estimator."""

import pyarrow as pa
import pytest

from geneva.runners.ray.memory_budget import (
    DEFAULT_SLACK_BYTES,
    ApplierMemoryModel,
    MemoryBudget,
    choose_output_avg_row_bytes,
    estimate_applier_memory,
    estimate_fixed_width_output_row_bytes,
    estimate_writer_task_resources,
    humanize_bytes,
    match_selectivity_hint,
)

GIB = 1 << 30
KIB = 1 << 10


def test_humanize_bytes() -> None:
    assert humanize_bytes(0) == "0.0 B"
    assert humanize_bytes(512) == "512.0 B"
    assert humanize_bytes(KIB) == "1.0 KiB"
    assert humanize_bytes(15 * GIB) == "15.0 GiB"
    assert humanize_bytes(-5) == "0.0 B"  # clamped


def _budget(**over: object) -> MemoryBudget:
    base: dict[str, object] = {
        "input_avg_row_bytes": 25 * KIB,
        "output_avg_row_bytes": 25 * KIB,
        "writer_avg_row_bytes": 25 * KIB,
        "checkpoint_size": 16384,
        "intra_applier_concurrency": 1,
        "pending_target_bytes": GIB,
        "actors_per_pod": 3,
    }
    base.update(over)
    return MemoryBudget(**base)  # type: ignore[arg-type]


def test_per_actor_formula() -> None:
    b = _budget()
    # 16384 x (25KiB input + 25KiB output) x 1 = 800 MiB in-flight,
    # + 1 GiB pending + 1 GiB slack.
    assert b.applier_inflight_bytes == 16384 * (25 + 25) * KIB
    assert b.per_actor_bytes == b.applier_inflight_bytes + GIB + DEFAULT_SLACK_BYTES


def test_applier_inflight_uses_split_input_and_output_sizes() -> None:
    b = _budget(input_avg_row_bytes=8 * KIB, output_avg_row_bytes=32 * KIB)
    assert b.applier_inflight_bytes == 16384 * (8 + 32) * KIB


def test_unknown_output_size_falls_back_to_input_size() -> None:
    b = _budget(input_avg_row_bytes=8 * KIB, output_avg_row_bytes=None)
    assert b.effective_output_avg_row_bytes == 8 * KIB
    assert b.applier_inflight_bytes == 16384 * (8 + 8) * KIB


def test_intra_applier_concurrency_scales_inflight() -> None:
    assert _budget(intra_applier_concurrency=3).applier_inflight_bytes == (
        3 * _budget(intra_applier_concurrency=1).applier_inflight_bytes
    )


def test_per_writer_zero_when_not_deferred() -> None:
    assert _budget(deferred_carry_forward=False).per_writer_bytes == 0


def test_per_writer_when_deferred() -> None:
    # per_writer mirrors the Ray reservation: base + overhead x working set, so
    # pod_minimum is a true floor for the FragmentWriter task.
    b = _budget(
        deferred_carry_forward=True,
        writer_avg_row_bytes=40 * KIB,
        matched_rows_per_frag_est=1000,
        tranche_rows=64,
        writer_base_memory_bytes=GIB,
        writer_memory_overhead=1.5,
    )
    working = (1000 + 64) * 40 * KIB
    assert b.per_writer_bytes == GIB + int(1.5 * working)


def test_per_writer_matches_writer_task_reservation() -> None:
    # The advertised per_writer floor must equal the memory= Ray attaches to the
    # FragmentWriter via estimate_writer_task_resources for the same working set.
    matched, tranche = 1000, 64
    b = _budget(
        deferred_carry_forward=True,
        matched_rows_per_frag_est=matched,
        tranche_rows=tranche,
        writer_base_memory_bytes=GIB,
        writer_memory_overhead=1.5,
    )
    mem, _ = estimate_writer_task_resources(
        num_rows=matched + tranche,
        avg_row_bytes=25 * KIB,
        base_memory_bytes=GIB,
        floor_num_cpus=0.1,
        overhead=1.5,
    )
    assert b.per_writer_bytes == mem


def test_pod_minimum_includes_actors_and_writer() -> None:
    b = _budget(
        actors_per_pod=3,
        deferred_carry_forward=True,
        matched_rows_per_frag_est=1000,
        tranche_rows=64,
    )
    assert b.pod_minimum_bytes == 3 * b.per_actor_bytes + b.per_writer_bytes


def test_pod_minimum_no_writer_when_not_deferred() -> None:
    b = _budget(actors_per_pod=5)
    assert b.pod_minimum_bytes == 5 * b.per_actor_bytes


def test_format_block_mentions_sites_and_doc() -> None:
    text = _budget(
        deferred_carry_forward=True, matched_rows_per_frag_est=1000, tranche_rows=64
    ).format_block()
    assert "input_avg_row_bytes" in text
    assert "output_avg_row_bytes" in text
    assert "writer_avg_row_bytes" in text
    assert "per_actor_bytes" in text
    assert "per_writer_bytes" in text
    assert "pod_minimum" in text
    assert "deferred-carry-forward-memory-model.md" in text


def test_format_block_mentions_output_fallback_when_unknown() -> None:
    text = _budget(output_avg_row_bytes=None).format_block()
    assert "unknown; using input_avg_row_bytes fallback" in text


def test_format_block_marks_writer_na_when_not_deferred() -> None:
    text = _budget(deferred_carry_forward=False).format_block()
    assert "n/a" in text


# --- fixed-width output row estimator ---


def test_fixed_width_output_row_bytes_sums_fixed_fields_and_excludes_rowaddr() -> None:
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            pa.field("score", pa.float64()),
            pa.field("price", pa.decimal128(18, 2)),
            pa.field("hash", pa.binary(8)),
            pa.field("embedding", pa.list_(pa.float32(), 4)),
            pa.field(
                "metrics",
                pa.struct(
                    [
                        pa.field("count", pa.int16()),
                        pa.field("ok", pa.bool_()),
                    ]
                ),
            ),
            pa.field("_rowaddr", pa.uint64()),
        ]
    )

    assert estimate_fixed_width_output_row_bytes(schema) == 4 + 8 + 16 + 8 + 16 + 3


@pytest.mark.parametrize(
    "dtype",
    [
        pa.string(),
        pa.large_string(),
        pa.binary(),
        pa.large_binary(),
        pa.list_(pa.int32()),
        pa.map_(pa.string(), pa.int32()),
        pa.dictionary(pa.int32(), pa.string()),
        pa.sparse_union([pa.field("a", pa.int32())]),
        pa.struct([pa.field("fixed", pa.int32()), pa.field("variable", pa.string())]),
        pa.list_(pa.string(), 3),
    ],
)
def test_fixed_width_output_row_bytes_returns_none_for_variable_types(
    dtype: pa.DataType,
) -> None:
    assert (
        estimate_fixed_width_output_row_bytes(pa.schema([pa.field("value", dtype)]))
        is None
    )


def test_choose_output_avg_row_bytes_prefers_fixed_schema_estimate() -> None:
    assert (
        choose_output_avg_row_bytes(
            fixed_width_output_avg_row_bytes=16,
            sampled_output_avg_row_bytes=25 * KIB,
        )
        == 16
    )


def test_choose_output_avg_row_bytes_uses_existing_output_sample_for_variable() -> None:
    assert (
        choose_output_avg_row_bytes(
            fixed_width_output_avg_row_bytes=None,
            sampled_output_avg_row_bytes=25 * KIB,
        )
        == 25 * KIB
    )


def test_choose_output_avg_row_bytes_returns_none_without_schema_or_sample() -> None:
    assert (
        choose_output_avg_row_bytes(
            fixed_width_output_avg_row_bytes=None,
            sampled_output_avg_row_bytes=None,
        )
        is None
    )


# --- writer task resource sizing ---


def test_writer_resources_scale_memory_with_working_set() -> None:
    mem, _ = estimate_writer_task_resources(
        num_rows=1_000_000,
        avg_row_bytes=25 * KIB,
        base_memory_bytes=GIB,
        floor_num_cpus=0.1,
        overhead=1.5,
    )
    # base + 1.5 x (1M x 25KiB)
    assert mem == GIB + int(1.5 * 1_000_000 * 25 * KIB)


def test_writer_resources_cpu_proportional_to_working_set() -> None:
    _, cpus = estimate_writer_task_resources(
        num_rows=1_000_000,
        avg_row_bytes=25 * KIB,
        base_memory_bytes=GIB,
        floor_num_cpus=0.1,
        bytes_per_cpu=4 * GIB,
    )
    # 1M x 25KiB ~= 23.8 GiB / 4 GiB-per-cpu ~= 6 cpus
    assert cpus == (1_000_000 * 25 * KIB) / (4 * GIB)
    assert cpus > 0.1


def test_writer_resources_floor_for_tiny_fragments() -> None:
    mem, cpus = estimate_writer_task_resources(
        num_rows=10,
        avg_row_bytes=16,
        base_memory_bytes=GIB,
        floor_num_cpus=0.1,
    )
    assert cpus == 0.1  # floored — tiny writers stay cheap to schedule
    assert mem >= GIB  # never below the base


# --- deferred-CF match selectivity hint ---


def test_match_selectivity_default_is_conservative(monkeypatch) -> None:
    monkeypatch.delenv("GENEVA_MATCH_SELECTIVITY_HINT", raising=False)
    assert match_selectivity_hint() == 1.0  # worst case: every row matches


def test_match_selectivity_parsed_and_clamped(monkeypatch) -> None:
    monkeypatch.setenv("GENEVA_MATCH_SELECTIVITY_HINT", "0.01")
    assert match_selectivity_hint() == 0.01
    monkeypatch.setenv("GENEVA_MATCH_SELECTIVITY_HINT", "5")  # clamp to 1.0
    assert match_selectivity_hint() == 1.0
    monkeypatch.setenv("GENEVA_MATCH_SELECTIVITY_HINT", "-1")  # clamp to 0.0
    assert match_selectivity_hint() == 0.0
    monkeypatch.setenv("GENEVA_MATCH_SELECTIVITY_HINT", "nope")  # invalid -> 1.0
    assert match_selectivity_hint() == 1.0


def test_deferred_cf_writer_smaller_than_legacy() -> None:
    # A 1% match deferred-CF writer holds far less than a full-fragment writer.
    rows = 1_000_000
    legacy_mem, _ = estimate_writer_task_resources(
        num_rows=rows, avg_row_bytes=25 * KIB, base_memory_bytes=GIB, floor_num_cpus=0.1
    )
    matched = int(rows * 0.01) + 64  # MatchIndex + one tranche
    deferred_mem, _ = estimate_writer_task_resources(
        num_rows=matched,
        avg_row_bytes=25 * KIB,
        base_memory_bytes=GIB,
        floor_num_cpus=0.1,
    )
    assert deferred_mem < legacy_mem


# --- estimate_applier_memory -------------------------------------


def _applier(**over: object) -> int:
    base: dict[str, object] = {
        "scan_batch_bytes": 128 * (1 << 20),
        "checkpoint_write_buffer_bytes": GIB,
        "intra_applier_concurrency": 1,
        "enable_gpu_pipelining": False,
        "pipelining_prefetch_depth": 16,
        "num_gpus": 0.0,
        "lance_io_buffer_bytes": 2 * GIB,
        "native_overhead_bytes": 512 * (1 << 20),
        "blob_buffer_bytes": 128 * (1 << 20),
        "worker_baseline_bytes": GIB,
        "user_expansion_factor": 4.0,
        "user_expansion_constant_bytes": 0,
        "gpu_overhead_bytes": 2 * GIB,
    }
    base.update(over)
    return estimate_applier_memory(**base)  # type: ignore[arg-type]


def test_applier_memory_matches_explicit_formula() -> None:
    read = 128 * (1 << 20)
    # fixed once-per-actor buffers: io + checkpoint_write + blob + native
    fixed = 2 * GIB + GIB + 128 * (1 << 20) + 512 * (1 << 20)
    # each inflight thread holds the raw scan plus its expanded copy (read x 4)
    per_thread = read + int(read * 4.0)
    per_process = GIB  # baseline, no gpu; 1 worker copy
    assert _applier() == fixed + per_thread + per_process


def test_applier_memory_grows_with_read_batch() -> None:
    small = _applier(scan_batch_bytes=1 << 20)
    big = _applier(scan_batch_bytes=256 * (1 << 20))
    assert big > small


def test_applier_memory_floor_dominated_by_fixed_buffers() -> None:
    # A tiny read batch still reserves the once-per-actor buffers (~3.6 GiB).
    tiny = _applier(scan_batch_bytes=1024)
    assert tiny >= 2 * GIB + GIB + 512 * (1 << 20)


def test_applier_memory_scales_per_worker_with_concurrency() -> None:
    one = _applier(intra_applier_concurrency=1)
    four = _applier(intra_applier_concurrency=4)
    # More workers => more decoded per-worker copies AND more inflight reads.
    assert four > one


def test_applier_memory_gpu_adds_host_overhead() -> None:
    cpu = _applier(num_gpus=0.0)
    gpu = _applier(num_gpus=1.0)
    assert gpu == cpu + 2 * GIB


def test_applier_memory_caps_slots_at_the_batches_in_flight() -> None:
    # A read task holding a single batch can only feed one slot, however many
    # the actor runs -- but every worker process is still alive and baselined.
    read = 8 * (1 << 20)
    capped = _applier(
        scan_batch_bytes=read, intra_applier_concurrency=4, max_inflight_batches=1
    )
    fixed = 2 * GIB + GIB + 128 * (1 << 20) + 512 * (1 << 20)
    per_thread = read + int(read * 4.0)
    assert capped == fixed + per_thread + 4 * GIB
    assert capped < _applier(scan_batch_bytes=read, intra_applier_concurrency=4)


def test_applier_memory_cap_above_the_slot_count_changes_nothing() -> None:
    read = 8 * (1 << 20)
    assert _applier(
        scan_batch_bytes=read, intra_applier_concurrency=4, max_inflight_batches=99
    ) == _applier(scan_batch_bytes=read, intra_applier_concurrency=4)


def test_applier_memory_gpu_pipelining_uses_prefetch_depth() -> None:
    # Pipelining shares one worker process but keeps prefetch_depth batches in
    # flight, so the per-thread term (scan + expanded) scales with
    # prefetch_depth, while the process baseline is charged once.
    read = 8 * (1 << 20)
    piped = _applier(
        scan_batch_bytes=read,
        enable_gpu_pipelining=True,
        pipelining_prefetch_depth=8,
        intra_applier_concurrency=4,
    )
    fixed = 2 * GIB + GIB + 128 * (1 << 20) + 512 * (1 << 20)
    per_thread = read + int(read * 4.0)
    # 8 prefetch slots each hold scan + expanded; one shared worker process.
    assert piped == fixed + per_thread * 8 + GIB


def test_applier_memory_user_expansion_factor_floored_at_one() -> None:
    # A sub-1.0 user_expansion_factor cannot shrink the resident batch below itself.
    read = 64 * (1 << 20)
    est = _applier(scan_batch_bytes=read, user_expansion_factor=0.5)
    fixed = 2 * GIB + GIB + 128 * (1 << 20) + 512 * (1 << 20)
    per_thread = read + read  # raw scan + expanded (factor clamped up to 1.0)
    assert est == fixed + per_thread + GIB


def test_applier_memory_expansion_constant_added_before_factor() -> None:
    # The constant joins the scan batch inside the factor: (scan + const) * factor.
    read = 32 * (1 << 20)
    const = 16 * (1 << 20)
    est = _applier(
        scan_batch_bytes=read,
        user_expansion_constant_bytes=const,
        user_expansion_factor=4.0,
    )
    fixed = 2 * GIB + GIB + 128 * (1 << 20) + 512 * (1 << 20)
    per_thread = read + (read + const) * 4  # raw scan + expanded copy
    assert est == fixed + per_thread + GIB


def test_applier_memory_expansion_constant_floors_tiny_sample() -> None:
    # With a pathologically small scan batch, the constant still reserves a
    # per-worker working-copy floor of const * factor.
    const = 64 * (1 << 20)
    est_tiny = _applier(
        scan_batch_bytes=1,
        user_expansion_constant_bytes=const,
        user_expansion_factor=4.0,
    )
    est_none = _applier(
        scan_batch_bytes=1, user_expansion_constant_bytes=0, user_expansion_factor=4.0
    )
    assert est_tiny - est_none == const * 4


class TestApplierMemoryModel:
    """One object prices the reservation and inverts it, so the actor,
    admission, and the rejection advice can't drift apart."""

    IMAGE_BYTES = 150 * KIB

    def _model(
        self, *, bytes_per_row: float = 0.0, **over: object
    ) -> ApplierMemoryModel:
        import attrs

        from geneva.jobs.config import JobConfig

        args = {
            "checkpoint_write_buffer_bytes": GIB,
            "intra_applier_concurrency": 1,
            "enable_gpu_pipelining": False,
            "pipelining_prefetch_depth": 16,
            "num_gpus": 0.0,
            # Wider than the row counts these tests price, unless overridden:
            # one batch covers the task, so the task is the slot.
            "batch_rows": 1 << 20,
        }
        cfg_over = {k: over.pop(k) for k in list(over) if k.startswith("applier_")}
        args.update(over)
        cfg = attrs.evolve(JobConfig(), **cfg_over)  # type: ignore[arg-type]
        return ApplierMemoryModel.build(cfg, bytes_per_row=bytes_per_row, **args)  # type: ignore[arg-type]

    def test_memory_for_rows_matches_the_formula(self) -> None:
        model = self._model(
            bytes_per_row=self.IMAGE_BYTES, applier_user_row_overhead_bytes=1024
        )
        rows = 2048

        assert model.memory_for_rows(rows) == estimate_applier_memory(
            scan_batch_bytes=self.IMAGE_BYTES * rows,
            user_expansion_constant_bytes=1024 * rows,
            max_inflight_batches=1,  # one batch covers the whole task
            **model.fixed,
        )

    def test_a_slot_holds_one_batch_not_the_whole_task(self) -> None:
        # The actor streams the task through its slots in batch_rows chunks, so
        # a slot is charged one batch and only ceil(rows / batch_rows) slots can
        # be busy at once.
        model = self._model(
            bytes_per_row=self.IMAGE_BYTES, batch_rows=256, intra_applier_concurrency=4
        )

        assert model.memory_for_rows(1024) == estimate_applier_memory(
            scan_batch_bytes=self.IMAGE_BYTES * 256,
            user_expansion_constant_bytes=0,
            max_inflight_batches=4,
            **model.fixed,
        )

    def test_a_task_too_small_to_fill_the_slots_is_charged_once(self) -> None:
        # A one-row task can feed one worker; charging it four scan copies
        # would reserve memory the task cannot hold.
        model = self._model(
            bytes_per_row=self.IMAGE_BYTES, batch_rows=256, intra_applier_concurrency=4
        )
        one_worker = self._model(
            bytes_per_row=self.IMAGE_BYTES, batch_rows=256, intra_applier_concurrency=1
        )

        assert model.memory_for_rows(1) == estimate_applier_memory(
            scan_batch_bytes=self.IMAGE_BYTES,
            user_expansion_constant_bytes=0,
            max_inflight_batches=1,
            **model.fixed,
        )
        # The four worker processes are still alive and baselined; what the
        # extra three don't get is a scan/expansion copy each.
        assert model.memory_for_rows(1) - one_worker.memory_for_rows(1) == 3 * GIB

    def test_read_term_never_exceeds_the_task_it_reads(self) -> None:
        # The regression this guards: charging every prefetch slot the whole
        # read task inflated the GPU read term ~16x, rejecting jobs that fit.
        rows, batch_rows = 4096, 256
        model = self._model(
            bytes_per_row=self.IMAGE_BYTES,
            batch_rows=batch_rows,
            enable_gpu_pipelining=True,
            pipelining_prefetch_depth=16,
        )
        floor = self._model(
            bytes_per_row=0,
            batch_rows=batch_rows,
            enable_gpu_pipelining=True,
            pipelining_prefetch_depth=16,
        ).memory_for_rows(rows)
        task_bytes = rows * self.IMAGE_BYTES

        # Read term <= the task's bytes + their expanded copy (factor 4).
        assert model.memory_for_rows(rows) - floor <= task_bytes * 5

    def test_no_sample_still_reserves_the_fixed_floor(self) -> None:
        floor = self._model(bytes_per_row=0).memory_for_rows(4096)

        assert floor > 0
        assert floor < self._model(bytes_per_row=self.IMAGE_BYTES).memory_for_rows(4096)

    def test_row_overhead_reserves_without_a_sample(self) -> None:
        # Per-row working set the scan can't see (an image the UDF downloads).
        with_overhead = self._model(
            bytes_per_row=0, applier_user_row_overhead_bytes=150 * KIB
        ).memory_for_rows(4096)
        without = self._model(
            bytes_per_row=0, applier_user_row_overhead_bytes=0
        ).memory_for_rows(4096)

        assert with_overhead > without

    def test_memory_grows_with_rows(self) -> None:
        model = self._model(bytes_per_row=self.IMAGE_BYTES)

        assert model.memory_for_rows(1024) < model.memory_for_rows(8192)

    def test_pipelining_scales_by_prefetch_depth(self) -> None:
        # 2048 rows in 128-row batches = 16 batches, enough to fill either depth.
        deep = self._model(
            bytes_per_row=self.IMAGE_BYTES,
            batch_rows=128,
            enable_gpu_pipelining=True,
            pipelining_prefetch_depth=16,
        ).memory_for_rows(2048)
        shallow = self._model(
            bytes_per_row=self.IMAGE_BYTES,
            batch_rows=128,
            enable_gpu_pipelining=True,
            pipelining_prefetch_depth=2,
        ).memory_for_rows(2048)

        assert deep > shallow

    def test_blob_buffer_override_outranks_the_config_knob(self) -> None:
        # backfill(blob_read_buffer_size=) wins in the reader, so the
        # reservation has to follow it or the actor under-reserves.
        from geneva.jobs.config import JobConfig

        default = self._model(bytes_per_row=self.IMAGE_BYTES).memory_for_rows(1024)
        overridden = self._model(
            bytes_per_row=self.IMAGE_BYTES, blob_buffer_bytes=GIB
        ).memory_for_rows(1024)

        assert overridden - default == GIB - JobConfig().applier_blob_buffer_bytes

    def test_max_rows_for_budget_is_the_exact_boundary(self) -> None:
        model = self._model(bytes_per_row=self.IMAGE_BYTES)
        budget = 8 * GIB

        rows = model.max_rows_for_budget(budget, max_rows=1_000_000)

        assert rows is not None
        assert model.memory_for_rows(rows) <= budget < model.memory_for_rows(rows + 1)

    def test_max_rows_for_budget_caps_at_max_rows(self) -> None:
        model = self._model(bytes_per_row=8)

        assert model.max_rows_for_budget(64 * GIB, max_rows=500) == 500

    def test_max_rows_for_budget_none_below_the_fixed_floor(self) -> None:
        model = self._model(bytes_per_row=1)

        assert model.max_rows_for_budget(GIB, max_rows=1000) is None


class TestByteSizeEnvDefaults:
    """The estimator's buffer knobs default off env vars other components own.
    A value one of those components tolerates must not abort JobConfig."""

    def _cfg(self, monkeypatch, env: str, value: str | None):  # noqa: ANN001, ANN202
        from geneva.jobs.config import JobConfig

        if value is None:
            monkeypatch.delenv(env, raising=False)
        else:
            monkeypatch.setenv(env, value)
        return JobConfig()

    def test_lance_io_buffer_reads_lances_own_knob(self, monkeypatch) -> None:  # noqa: ANN001
        cfg = self._cfg(monkeypatch, "LANCE_DEFAULT_IO_BUFFER_SIZE", str(4 * GIB))

        assert cfg.applier_lance_io_buffer_bytes == 4 * GIB

    @pytest.mark.parametrize(
        "raw", ["2GB", "", "  ", "-1", str(1 << 65), "1_000", " 42 "]
    )
    def test_unusable_lance_io_buffer_falls_back(self, monkeypatch, raw) -> None:  # noqa: ANN001
        # Lance's parse_env_var (u64::from_str) rejects all of these and uses
        # 2 GiB, so we do too: failing JobConfig construction would break jobs
        # that run fine against Lance, and accepting what Rust rejects (the
        # underscore/whitespace cases, which int() would take) would estimate a
        # buffer Lance never allocates. A negative is rejected rather than
        # clamped to 0 later, which would silently drop the real 2 GiB.
        cfg = self._cfg(monkeypatch, "LANCE_DEFAULT_IO_BUFFER_SIZE", raw)

        assert cfg.applier_lance_io_buffer_bytes == 2 * GIB

    def test_blob_buffer_reads_the_deprecated_env(self, monkeypatch) -> None:  # noqa: ANN001
        cfg = self._cfg(
            monkeypatch, "GENEVA_RANGE_BLOB_READ_BUFFER_SIZE", str(256 * KIB)
        )

        assert cfg.applier_blob_buffer_bytes == 256 * KIB

    @pytest.mark.parametrize("raw", ["128MB", "0", "-1"])
    def test_unusable_blob_buffer_falls_back(self, monkeypatch, raw) -> None:  # noqa: ANN001
        # The reader rejects a non-positive buffer outright; fall back instead
        # of failing every JobConfig in the process.
        cfg = self._cfg(monkeypatch, "GENEVA_RANGE_BLOB_READ_BUFFER_SIZE", raw)

        assert cfg.applier_blob_buffer_bytes == 128 * 1024 * 1024
