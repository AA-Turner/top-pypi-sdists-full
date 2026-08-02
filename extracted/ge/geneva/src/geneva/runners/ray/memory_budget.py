# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Startup memory budget for backfill jobs.

Deferred carry-forward added a second memory-consuming site -- the
writer task's matched-output working set + old-column tranche stream -- on top of
the applier actor's input/UDF/pending buffers. This module turns those sites into
a single up-front estimate so operators can size pods *before* launching a job
instead of discovering the ceiling via OOMKill 30 minutes in.

Note: the writer streams the matched files lazily (one tranche + the files
overlapping the current window resident), so the estimate below — which reserves
for the full matched set — is a conservative upper bound; tightening it to unlock
more writer concurrency is a follow-up.

Everything here is a pure computation (no Ray / Lance imports) so it can be unit
tested and logged on the driver before the cluster context is entered. See
``internal_docs/deferred-carry-forward-memory-model.md`` for the model.
"""

from __future__ import annotations

import os

import attrs

# 1 GiB head-room per actor for allocator fragmentation, decode scratch (PIL /
# numpy), and Arrow pool slop that RSS accounting misses.
DEFAULT_SLACK_BYTES = 1 << 30

# An applier holds the input batch *and* the UDF output for a checkpoint chunk
# in flight at once, so the chunk's bytes count roughly twice.
_APPLIER_INFLIGHT_MULTIPLIER = 2

# Writer-task working set ~= the fragment's output bytes plus encode/copy
# scratch. Reserve a bit more than the raw data so Ray bin-packs honestly; a
# small over-reservation is the safe direction (fewer co-located heavy writers).
DEFAULT_WRITER_MEMORY_OVERHEAD = float(
    os.environ.get("GENEVA_WRITER_MEMORY_OVERHEAD", "1.5")
)
# Cost-proportional CPU: ~1 declared CPU per this many working bytes, so a big
# blob fragment reserves enough CPU that Ray co-locates fewer of them. The Lance
# encoder still bursts to all cores; this only governs *how many* land together.
DEFAULT_WRITER_BYTES_PER_CPU = int(
    os.environ.get("GENEVA_WRITER_BYTES_PER_CPU", str(4 << 30))
)

_UNITS = ("B", "KiB", "MiB", "GiB", "TiB")


def match_selectivity_hint() -> float:
    """WHERE match fraction (0..1) for sizing deferred-CF writers.

    Defaults to 1.0 (worst case: every row matches) because we don't have a
    per-fragment match count when the writer task is created. A sparse
    re-backfill can set ``GENEVA_MATCH_SELECTIVITY_HINT`` to right-size the
    writer's matched working set so Ray schedules more concurrent writers.
    """
    raw = os.environ.get("GENEVA_MATCH_SELECTIVITY_HINT")
    if raw is None:
        return 1.0
    try:
        return min(1.0, max(0.0, float(raw)))
    except ValueError:
        return 1.0


def estimate_writer_task_resources(
    *,
    num_rows: int,
    avg_row_bytes: int,
    base_memory_bytes: int,
    floor_num_cpus: float,
    overhead: float = DEFAULT_WRITER_MEMORY_OVERHEAD,
    bytes_per_cpu: int = DEFAULT_WRITER_BYTES_PER_CPU,
) -> tuple[int, float]:
    """Truthful ``(memory_bytes, num_cpus)`` for one fragment writer task.

    A fixed 0.1 CPU / 1 GiB reservation lets Ray pack many large-blob writers
    onto one pod, where their real (tens of GiB, all-core) footprints collide
    and wedge. Declaring the actual working set
    (``num_rows × avg_row_bytes``) makes Ray co-locate only as many as fit.

    ``base_memory_bytes`` / ``floor_num_cpus`` are the existing fixed defaults,
    used as floors so small writers stay cheap to schedule.
    """
    working = max(0, int(num_rows)) * max(0, int(avg_row_bytes))
    memory = int(base_memory_bytes + overhead * working)
    num_cpus = max(float(floor_num_cpus), working / float(max(1, bytes_per_cpu)))
    return memory, num_cpus


def humanize_bytes(n: int) -> str:
    """Render a byte count as a short binary-unit string (e.g. ``15.0 GiB``)."""
    size = float(max(0, int(n)))
    for unit in _UNITS:
        if size < 1024.0 or unit == _UNITS[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} {_UNITS[-1]}"


@attrs.frozen(kw_only=True)
class MemoryBudget:
    """Projected per-actor / per-writer / per-pod RAM for a backfill job.

    All sizes are bytes. The estimate is deliberately conservative -- it is a
    sizing floor, not a measurement.
    """

    avg_row_bytes: int
    checkpoint_size: int
    intra_applier_concurrency: int
    pending_target_bytes: int
    actors_per_pod: int
    deferred_carry_forward: bool = False
    # Worst-case matched rows in a single fragment (WHERE selectivity x fragment
    # rows). Only relevant to the deferred-CF writer's matched working set.
    matched_rows_per_frag_est: int = 0
    tranche_rows: int = 0
    slack_bytes: int = DEFAULT_SLACK_BYTES
    # Fixed base the FragmentWriter task reserves from Ray on top of its working
    # set (``PipelineResourceConfig.fragment_writer_memory``); included here so
    # ``per_writer_bytes`` matches the actual Ray reservation, not just the data.
    writer_base_memory_bytes: int = 1 << 30
    writer_memory_overhead: float = DEFAULT_WRITER_MEMORY_OVERHEAD

    @property
    def applier_inflight_bytes(self) -> int:
        """Input batch + UDF output held in flight for one checkpoint chunk."""
        return int(
            _APPLIER_INFLIGHT_MULTIPLIER
            * self.checkpoint_size
            * self.avg_row_bytes
            * max(1, self.intra_applier_concurrency)
        )

    @property
    def per_actor_bytes(self) -> int:
        """Ceiling for one applier actor: in-flight chunk + pending buffer + slack."""
        return int(
            self.applier_inflight_bytes + self.pending_target_bytes + self.slack_bytes
        )

    @property
    def per_writer_bytes(self) -> int:
        """Ray reservation for one deferred-CF writer: base + overhead x working.

        Mirrors ``estimate_writer_task_resources`` -- the actual ``memory=``
        attached to the FragmentWriter actor -- so ``pod_minimum`` is a true
        floor. The reserved working set is the matched set + one tranche
        (``(matched + tranche) x avg_row_bytes``); the base + 1.5x overhead is
        what Ray demands of the pod on top of it.

        Zero when carry-forward is not deferred (the legacy writer streams
        checkpoints and is not a separate large-memory site).
        """
        if not self.deferred_carry_forward:
            return 0
        working = (
            self.matched_rows_per_frag_est + self.tranche_rows
        ) * self.avg_row_bytes
        return int(
            self.writer_base_memory_bytes + self.writer_memory_overhead * working
        )

    @property
    def pod_minimum_bytes(self) -> int:
        """Minimum pod RAM: all co-located actors plus one writer task."""
        return int(
            max(1, self.actors_per_pod) * self.per_actor_bytes + self.per_writer_bytes
        )

    def format_block(self) -> str:
        """Render the multi-line INFO budget block for the backfill launch log."""
        lines = [
            "memory budget estimate:",
            f"  avg_row_bytes        ~= {humanize_bytes(self.avg_row_bytes)}",
            f"  checkpoint_size       = {self.checkpoint_size} rows",
            f"  intra_applier_conc    = {self.intra_applier_concurrency}",
            f"  pending_target        = {humanize_bytes(self.pending_target_bytes)}",
            f"  per_actor_bytes      ~= {humanize_bytes(self.per_actor_bytes)}"
            f"  (2 x ckpt x row x ic + pending + slack)",
        ]
        if self.deferred_carry_forward:
            lines += [
                f"  matched_rows/frag est = {self.matched_rows_per_frag_est}"
                f"  (worst case; WHERE selectivity x frag rows)",
                f"  tranche_rows          = {self.tranche_rows}",
                f"  per_writer_bytes     ~= {humanize_bytes(self.per_writer_bytes)}"
                f"  (base + overhead x (matched + tranche) x row)"
                f"  [deferred carry-forward]",
            ]
        else:
            lines.append("  per_writer_bytes     ~= n/a (carry-forward not deferred)")
        lines += [
            f"  actors_per_pod        = {self.actors_per_pod}",
            f"  pod_minimum          ~= {humanize_bytes(self.pod_minimum_bytes)}"
            f"  (actors_per_pod x per_actor + per_writer)",
            "  size pod_memory_request >= pod_minimum before launch; see "
            "internal_docs/deferred-carry-forward-memory-model.md",
        ]
        return "\n".join(lines)
