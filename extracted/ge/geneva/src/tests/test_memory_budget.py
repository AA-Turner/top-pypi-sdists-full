# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for the backfill memory budget estimator."""

from geneva.runners.ray.memory_budget import (
    DEFAULT_SLACK_BYTES,
    MemoryBudget,
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
        "avg_row_bytes": 25 * KIB,
        "checkpoint_size": 16384,
        "intra_applier_concurrency": 1,
        "pending_target_bytes": GIB,
        "actors_per_pod": 3,
    }
    base.update(over)
    return MemoryBudget(**base)  # type: ignore[arg-type]


def test_per_actor_formula() -> None:
    b = _budget()
    # 2 x 16384 x 25KiB x 1 = 800 MiB in-flight, + 1 GiB pending + 1 GiB slack.
    assert b.applier_inflight_bytes == 2 * 16384 * 25 * KIB
    assert b.per_actor_bytes == b.applier_inflight_bytes + GIB + DEFAULT_SLACK_BYTES


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
        matched_rows_per_frag_est=1000,
        tranche_rows=64,
        writer_base_memory_bytes=GIB,
        writer_memory_overhead=1.5,
    )
    working = (1000 + 64) * 25 * KIB
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
    assert "per_actor_bytes" in text
    assert "per_writer_bytes" in text
    assert "pod_minimum" in text
    assert "deferred-carry-forward-memory-model.md" in text


def test_format_block_marks_writer_na_when_not_deferred() -> None:
    text = _budget(deferred_carry_forward=False).format_block()
    assert "n/a" in text


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
