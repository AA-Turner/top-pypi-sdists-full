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

Two halves, with different statuses:

- ``MemoryBudget`` is in use. ``_log_backfill_memory_budget`` builds one on
  every backfill and prints ``format_block()``. Its ``per_actor_bytes`` is
  computed independently of the estimator below, so the two can disagree.
- ``estimate_applier_memory`` and ``ApplierMemoryModel`` have no production
  caller. GEN-820 / #1102 wires them to admission and ``setup_actor``. An
  error in them is inert until then.

The estimate answers one question: what a task of N rows should reserve,
sized from ``bytes_per_row`` sampled over 128 rows. It is a floor, not a
ceiling -- ``string``, ``binary``, ``list`` and blob columns have no schema
maximum, so a later row can exceed it by any factor. Bounding it needs a
maximum that is both known and enforced; neither is here.

Ordinary variance does not need one. ``_iter_row_budget_slices`` narrows a
slice when rows are large and widens it when they are not, and a task priced
too large is re-split by OOM recovery.

Reserving for a maximum is not an alternative: every row in a batch may reach
it, so the floor becomes ``slot_rows * max_row_bytes`` -- 2.5 TiB at a
1024-row batch with a 512 MiB maximum.
"""

from __future__ import annotations

import logging
import math
import os
from typing import Any

import attrs
import pyarrow as pa

# 1 GiB head-room per actor for allocator fragmentation, decode scratch (PIL /
# numpy), and Arrow pool slop that RSS accounting misses.
DEFAULT_SLACK_BYTES = 1 << 30

# Writer-task working set ~= the fragment's output bytes plus encode/copy
# scratch. Reserve a bit more than the raw data so Ray bin-packs honestly; a
# small over-reservation is the safe direction (fewer co-located heavy writers).
DEFAULT_WRITER_MEMORY_OVERHEAD = float(
    os.environ.get("GENEVA_WRITER_MEMORY_OVERHEAD", "1.5")
)


_LOG = logging.getLogger(__name__)

_LOG = logging.getLogger(__name__)

_UNITS = ("B", "KiB", "MiB", "GiB", "TiB")


def resolve_default_actor_memory(config: Any = None) -> int:
    """Bytes one applier actor reserves when its UDF declares no ``memory``.

    One function for both the actor's Ray reservation and admission's
    provisioning check, so the two cannot name different figures: a scheduler
    that admits one number while Ray receives another is worse than either.

    Reads ``applier_default_memory_bytes`` structurally, falling back to the
    process ``JobConfig`` when no config is threaded in. ``0`` means no floor
    -- actors go unreserved, which is a supported configuration.
    """
    value = getattr(config, "applier_default_memory_bytes", None)
    if value is None:
        from geneva.jobs.config import JobConfig

        value = JobConfig.get().applier_default_memory_bytes
    return max(0, int(value))


def unplaceable_reservation_warning(
    request_bytes: int, node_memory_bytes: float | None
) -> str | None:
    """A message when a reservation exceeds any node, or ``None``.

    Ray advertises a node's ``memory`` resource *after* carving out the object
    store (~30% of RAM), so schedulable memory is well under physical RAM -- a
    4 GiB container offers about 2.55 GiB. An actor asking for more than any
    node has is never scheduled: the autoscaler retries until the job fails,
    naming nothing.

    Said rather than silently corrected. Shrinking the request to fit would
    reserve less than the job was sized for and make the figure admission
    approved differ from the one Ray receives -- trading a visible failure for
    an invisible one. ``None`` node memory means the answer is unknown, and
    nothing is claimed.
    """
    if node_memory_bytes is None or node_memory_bytes <= 0:
        return None
    if request_bytes <= node_memory_bytes:
        return None
    return (
        f"Reserving {humanize_bytes(request_bytes)} per applier actor, but the "
        f"largest node offers {humanize_bytes(int(node_memory_bytes))} of "
        "schedulable memory, so the actor cannot be placed. Ray reserves part "
        "of each node for its object store, so this is below the node's RAM. "
        "Lower JOB__APPLIER_DEFAULT_MEMORY_BYTES, set @udf(memory=), or use "
        "larger nodes."
    )


def largest_node_memory() -> float | None:
    """Schedulable ``memory`` on the biggest live Ray node, or None."""
    try:
        import ray

        if not ray.is_initialized():
            return None
        sizes = [
            float(node.get("Resources", {}).get("memory", 0.0))
            for node in ray.nodes()
            if node.get("Alive")
        ]
        return max(sizes) if sizes else None
    except Exception:
        _LOG.debug("could not read Ray node memory; leaving the default", exc_info=True)
        return None


def concurrent_slots(
    *,
    enable_gpu_pipelining: bool,
    pipelining_prefetch_depth: int,
    intra_applier_concurrency: int,
    **_ignored: Any,
) -> int:
    """How many scan batches an actor can hold at once.

    A prefetch slot when pipelining, a worker process when multiprocessing.
    Ignores the estimator's other arguments so a caller can splat a whole
    ``fixed`` mapping at it.
    """
    if enable_gpu_pipelining:
        return max(1, int(pipelining_prefetch_depth))
    return max(1, int(intra_applier_concurrency))


def estimate_applier_memory(
    *,
    scan_batch_bytes: int,
    max_inflight_batches: int | None = None,
    checkpoint_write_buffer_bytes: int,
    intra_applier_concurrency: int,
    enable_gpu_pipelining: bool,
    pipelining_prefetch_depth: int,
    num_gpus: float,
    lance_io_buffer_bytes: int,
    native_overhead_bytes: int,
    blob_buffer_bytes: int,
    worker_baseline_bytes: int,
    user_expansion_factor: float,
    user_expansion_constant_bytes: int,
    gpu_overhead_bytes: int,
    task_bytes: int | None = None,
) -> int:
    """White-box per-actor RAM floor for an applier whose UDF left ``memory``
    unset.

    The reservation is a fixed once-per-actor base, a per-in-flight-thread term,
    and a per-worker-process term::

        total       = fixed_buffers
                      + per_thread * inflight_threads
                      + per_process * worker_copies

        fixed_buffers = min(lance_io_buffer, task_bytes)
                        + checkpoint_write_buffer
                        + blob_buffer          # 0 unless blob columns are read
                        + native_overhead
                        + 2 * scan_batch_bytes  # parent-queued batch, mp only
        expanded      = (scan_batch_bytes + user_expansion_constant)
                        * user_expansion_factor
        per_thread    = scan_batch_bytes + expanded
        per_process   = worker_baseline + gpu_overhead

    ``fixed_buffers`` are held once per actor regardless of concurrency: the
    Lance IO readahead buffer, the checkpoint write buffer, the blob coalescing
    buffer, native (object_store / Tokio) overhead, and -- when multiprocessing
    -- the batch the parent has queued but no worker has taken yet, counted
    twice because the parent holds both the raw Arrow batch and the IPC buffer
    serialized from it.

    The Lance IO readahead buffer is capped by ``task_bytes`` (the whole read
    task, since an actor runs one at a time). It is a ceiling on buffering
    rather than an up-front allocation, so a task with fewer bytes than the
    ceiling can never fill it. ``task_bytes=None`` means the row width is
    unknown, and the uncapped buffer stands -- a failed sample must not produce
    an under-reserved actor. The checkpoint buffer is deliberately *not*
    capped: it holds output, which an expanding UDF makes larger than its
    input.

    The blob coalescing buffer is *not* capped by ``task_bytes`` either, and
    for a different reason: ``task_bytes`` is logical payload sampled from
    Arrow widths, while the reader coalesces gaps between values and fetches
    the whole span. Two 1 KiB blobs 100 MiB apart are 2 KiB logical and one
    ~100 MiB read. What does bound it is the reader's own budget:
    ``_iter_row_budget_slices`` cuts a slice once the *coalesced* size exceeds
    ``blob_read_buffer_size``, so the configured value is already a physical
    bound and is charged in full. Callers pass 0 when the job reads no blob
    columns -- the coalescing path never runs then, so there is nothing to
    reserve. That, not a logical-byte cap, is what keeps a narrow non-blob task
    from being charged for a buffer it never allocates.

    One row whose blob exceeds the budget is still never split --
    ``_iter_row_budget_slices`` cuts *between* rows -- so the charge is a floor
    for oversized records, not a bound: a single 1 GiB blob against a 128 MiB
    budget reads 8x what is reserved, and the gap has no ceiling. Nothing here
    refuses such a row; the charge prices the buffer, not the outlier.

    ``per_thread`` is what each *in-flight* thread holds: its own raw scan batch
    plus the expanded working copy the user code materializes from it (both
    resident at once). Every in-flight thread has its own scan --
    ``inflight_threads`` is ``prefetch_depth`` when pipelining (each prefetch
    slot) or ``intra_applier_concurrency`` when multiprocessing (each worker).

    ``per_process`` is per worker process: the Python/libs baseline (one
    interpreter) and any GPU host overhead (CUDA context + staged batch, GPU
    UDFs only). ``worker_copies`` is 1 when pipelining (one shared in-actor
    model) or ``intra_applier_concurrency`` when multiprocessing.

    ``scan_batch_bytes`` is what *one* in-flight slot holds -- a single map-task
    batch (``batch_size x avg_row_bytes``), not the whole read task. An actor
    runs one read task at a time and streams it through the slots in
    ``map_task.batch_size()`` chunks (``ReadTask.to_batches`` in the
    multiprocess applier, the reader thread in the pipelined one), so
    ``max_inflight_batches`` caps ``inflight_threads`` at the number of batches
    that task actually contains: a task smaller than the slot count can never
    fill every slot, and charging it per slot would reserve several times the
    bytes the task can hold. ``None`` leaves the slot count uncapped.

    ``user_expansion_factor`` is the
    main fudge: stored bytes can balloon when user code (a UDF or chunker)
    materializes them (e.g. JPEG -> raw pixels). ``user_expansion_constant_bytes``
    is a fixed per-batch working-set floor added to the scan batch *before* the
    factor; callers derive it as ``user_row_overhead_bytes x max_rows_per_batch``
    to reserve for per-row data the scan sample can't see (e.g. an image the UDF
    downloads), so it holds on a first backfill with no sample.

    The return value is the full actor reservation (already scaled by
    concurrency); callers use it directly, not multiplied again.
    """
    # Each in-flight thread has its own scan batch: a prefetch slot when
    # pipelining, or a worker process when multiprocessing. Worker processes
    # (the interpreter/model copies) are one when pipelining (shared in-actor
    # model) or one per concurrent worker otherwise.
    inflight_threads = concurrent_slots(
        enable_gpu_pipelining=enable_gpu_pipelining,
        pipelining_prefetch_depth=pipelining_prefetch_depth,
        intra_applier_concurrency=intra_applier_concurrency,
    )
    worker_copies = (
        1 if enable_gpu_pipelining else max(1, int(intra_applier_concurrency))
    )

    # A read task holds only so many batches; slots beyond that sit empty.
    if max_inflight_batches is not None:
        inflight_threads = min(inflight_threads, max(1, int(max_inflight_batches)))

    scan_batch_bytes = max(0, int(scan_batch_bytes))

    # The Lance IO readahead is a *ceiling* on buffering, not an allocation
    # Lance makes up front, and an actor reads one task at a time -- it cannot
    # hold more than the task has bytes, so charging it in full to a task that
    # cannot fill it reserves memory the actor will never touch. Measured: a
    # 20k-row, 8 B/row table reserved 4.63 GiB per actor and peaked at 0.34 GiB
    # (13.8x), which at concurrency 8 demanded 37 GiB and was rejected outright.
    #
    # ``task_bytes is None`` means the width could not be sampled -- not that
    # there is no data -- so the full buffer stands. Bounding to zero there
    # would turn a failed sample into an unreserved actor, which is the OOM
    # this floor exists to prevent.
    #
    # The blob buffer is deliberately not capped the same way: ``task_bytes``
    # is logical payload, and the coalescing reader fetches whole spans across
    # the gaps between values -- 2 KiB of logical blob can be a 100 MiB read.
    # Its real bound is the reader's own slicing budget, which is this
    # configured value, so it is charged in full whenever it applies at all.
    # Callers pass 0 for jobs that read no blob columns.
    read_buffer_cap = (
        max(0, int(task_bytes)) if task_bytes is not None and task_bytes > 0 else None
    )
    lance_io = max(0, int(lance_io_buffer_bytes))
    blob_buffer = max(0, int(blob_buffer_bytes))
    if read_buffer_cap is not None:
        lance_io = min(lance_io, read_buffer_cap)

    fixed_buffers = (
        lance_io
        # Not bounded by ``task_bytes``: this one holds *output*, and a UDF that
        # expands (8 B id -> a 4 KiB embedding) produces more than it reads.
        + max(0, int(checkpoint_write_buffer_bytes))
        + blob_buffer
        + max(0, int(native_overhead_bytes))
        # ``MultiProcessBatchApplier.run`` primes to ``num_processes + 1``
        # futures before draining the head, so the parent holds a batch beyond
        # the slots charged below, queued for a worker that has not taken it
        # yet. It holds that batch *twice*: ``batch``, the raw Arrow one it
        # read, and ``data``, the IPC buffer serialized from it -- both still
        # bound at the wait, and neither released before the drain loop ends.
        # Not raw-plus-expanded, though: the expansion happens in the worker,
        # which its own slot covers.
        #
        # Only when the task has more batches than the actor has slots. At or
        # below that the loop never reaches ``num_processes + 1`` futures, and
        # ``inflight_threads`` is already capped at the batch count -- so every
        # batch is charged a full slot and the queued copies are not extra. An
        # unknown batch count charges them, since it cannot be ruled out.
        + (
            2 * scan_batch_bytes
            if not enable_gpu_pipelining
            and (
                max_inflight_batches is None
                or max_inflight_batches > max(1, int(intra_applier_concurrency))
            )
            else 0
        )
    )

    # Per in-flight thread: its raw scan batch plus the expanded working copy
    # the user code materializes from it (both resident at once).
    expanded_batch_bytes = int(
        (scan_batch_bytes + max(0, int(user_expansion_constant_bytes)))
        * max(1.0, user_expansion_factor)
    )
    per_thread = scan_batch_bytes + expanded_batch_bytes

    # Per worker process: the Python/libs baseline and any GPU host overhead.
    gpu_overhead = (
        int(max(0, int(gpu_overhead_bytes))) if num_gpus and num_gpus > 0 else 0
    )
    per_process = max(0, int(worker_baseline_bytes)) + gpu_overhead

    return int(
        fixed_buffers + per_thread * inflight_threads + per_process * worker_copies
    )


@attrs.define
class ApplierMemoryModel:
    """Prices an applier's per-actor reservation at any read-task row count.

    Built once per job from its config and concurrency knobs. Both questions
    asked of the estimate come off the same object:

    - ``memory_for_rows`` -- what to reserve for a read task of N rows. The
      actor's own reservation and the provisioning admission checks it against
      both call this, so "admission provisions what the actor reserves" holds by
      construction rather than by two call sites building the same twelve
      arguments and agreeing.
    - ``max_rows_for_budget`` -- the inverse, for telling a caller which
      ``task_size`` would have fit.

    ``bytes_per_row`` of 0 means the byte sample was unavailable: the read term
    drops out and the data-independent fixed-buffer floor still reserves.
    """

    bytes_per_row: float = attrs.field(converter=lambda v: max(0.0, float(v or 0.0)))
    user_row_overhead_bytes: int = attrs.field(converter=int)
    # Rows in one map-task batch (``map_task.batch_size()``) -- what a single
    # in-flight slot holds, and the unit a read task is streamed through the
    # slots in. The adaptive sizer only ever shrinks below it, so it is an
    # upper bound.
    batch_rows: int = attrs.field(converter=lambda v: max(1, int(v)))
    # Row-independent estimator arguments, resolved once at build time.
    fixed: dict[str, Any] = attrs.field()
    # Whether the coalesced blob path runs. Only decides whether that buffer
    # is charged -- it is not a claim about whether the estimate is a ceiling,
    # which needs the schema and an enforcer, neither of which is here.
    reads_blob_columns: bool = attrs.field(default=True)

    @classmethod
    def build(
        cls,
        cfg: object,
        *,
        bytes_per_row: float | None,
        batch_rows: int,
        checkpoint_write_buffer_bytes: int,
        intra_applier_concurrency: int,
        enable_gpu_pipelining: bool,
        pipelining_prefetch_depth: int,
        num_gpus: float,
        blob_buffer_bytes: int | None = None,
        reads_blob_columns: bool = True,
    ) -> ApplierMemoryModel:
        """Resolve the model from a ``JobConfig`` (read structurally to keep
        this module a leaf).

        ``enable_gpu_pipelining``/``pipelining_prefetch_depth`` are explicit
        rather than read off ``cfg``: they also drive CPU accounting, and
        callers pass the resolved value for the job at hand. ``batch_rows`` is
        ``map_task.batch_size()`` -- the rows one in-flight slot holds.

        ``blob_buffer_bytes`` is the *effective* range-blob read buffer for this
        job. ``backfill(blob_read_buffer_size=...)`` outranks the config knob in
        the reader (``resolve_blob_read_buffer_size``), so callers resolve it
        once on the driver and pass the same value here; ``None`` means no
        override and the config knob stands, matching the reader.

        ``reads_blob_columns`` says whether the job range-reads any blob column
        at all. The coalescing path only runs when there are blob column plans,
        so a job without them allocates no buffer and is charged none. This is
        the switch that keeps a narrow non-blob task off the blob charge --
        deliberately a presence question, not a size one, because the buffer's
        size is bounded by the reader's slicing budget rather than by how many
        logical bytes the task holds. It defaults to ``True`` so a caller that
        has not answered over-reserves rather than under-reserves.
        """
        return cls(
            bytes_per_row=bytes_per_row,  # type: ignore[arg-type]
            user_row_overhead_bytes=cfg.applier_user_row_overhead_bytes,  # type: ignore[attr-defined]
            batch_rows=batch_rows,
            reads_blob_columns=reads_blob_columns,
            fixed={
                "checkpoint_write_buffer_bytes": checkpoint_write_buffer_bytes,
                "intra_applier_concurrency": intra_applier_concurrency,
                "enable_gpu_pipelining": enable_gpu_pipelining,
                "pipelining_prefetch_depth": pipelining_prefetch_depth,
                "num_gpus": num_gpus,
                "lance_io_buffer_bytes": cfg.applier_lance_io_buffer_bytes,  # type: ignore[attr-defined]
                "native_overhead_bytes": cfg.applier_native_overhead_bytes,  # type: ignore[attr-defined]
                "blob_buffer_bytes": (
                    (
                        cfg.applier_blob_buffer_bytes  # type: ignore[attr-defined]
                        if blob_buffer_bytes is None
                        else blob_buffer_bytes
                    )
                    if reads_blob_columns
                    else 0
                ),
                "worker_baseline_bytes": cfg.applier_worker_baseline_bytes,  # type: ignore[attr-defined]
                "user_expansion_factor": cfg.applier_user_expansion_factor,  # type: ignore[attr-defined]
                "gpu_overhead_bytes": cfg.applier_gpu_overhead_bytes,  # type: ignore[attr-defined]
            },
        )

    def memory_for_rows(self, rows: int) -> int:
        """Per-actor reservation for a read task covering ``rows`` rows.

        The task is charged as the batches it decomposes into, not as one
        resident block per slot: a slot holds ``batch_rows`` (or the whole task,
        when that is smaller), and only ``ceil(rows / batch_rows)`` slots can be
        fed from one task at a time.
        """
        task_rows = max(0, int(rows))
        slot_rows = min(self.batch_rows, task_rows)
        inflight_batches = -(-task_rows // slot_rows) if slot_rows else 1
        # Bytes the whole task can produce, bounding the read buffers. ``None``
        # when the width is unknown, so they stay uncapped rather than collapse.
        #
        # Rounded *up*: a sub-byte width truncates to 0, which reads as
        # "unknown" and restores the full uncapped buffers, pricing a known-
        # narrow task as an unmeasurable one. Arrow bit-packs booleans, so a
        # single ``bool`` column samples at 0.125 B/row and every task under 8
        # rows hit it. ``max_rows_for_budget`` probes ``memory_for_rows(1)``
        # first, so the truncation also made it answer ``None`` for budgets
        # that fit hundreds of rows.
        task_bytes = (
            math.ceil(self.bytes_per_row * task_rows) if self.bytes_per_row else None
        )
        scan_batch_bytes = int(self.bytes_per_row * slot_rows)

        return estimate_applier_memory(
            scan_batch_bytes=scan_batch_bytes,
            max_inflight_batches=inflight_batches,
            task_bytes=task_bytes,
            # Per-row working set the scan sample can't see (an image the UDF
            # downloads), so a first backfill with no sample still reserves.
            user_expansion_constant_bytes=self.user_row_overhead_bytes * slot_rows,
            **self.fixed,
        )

    def max_rows_for_budget(self, budget_bytes: int, *, max_rows: int) -> int | None:
        """Largest row count at or below ``max_rows`` whose reservation fits.

        ``memory_for_rows`` is monotonic in the row count, so a binary search is
        exact. ``None`` when even one row doesn't fit -- the data-independent
        buffers alone exceed the budget, so the row cap isn't the lever.
        """
        if budget_bytes <= 0 or max_rows <= 0:
            return None
        if self.memory_for_rows(1) > budget_bytes:
            return None
        if self.memory_for_rows(max_rows) <= budget_bytes:
            return max_rows
        low, high = 1, max_rows
        while low < high:
            mid = (low + high + 1) // 2
            if self.memory_for_rows(mid) <= budget_bytes:
                low = mid
            else:
                high = mid - 1
        return low


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
) -> tuple[int, float]:
    """``(memory_bytes, num_cpus)`` for one fragment writer task.

    A fixed 1 GiB reservation lets Ray pack many large-blob writers onto one
    pod, where their real (tens of GiB) footprints collide and wedge.
    Declaring the working set (``num_rows × avg_row_bytes``) makes Ray
    co-locate only as many as fit.

    **Memory only.** CPU used to scale with the working set too, as a second
    co-location lever, but the two failure modes are not comparable: too little
    memory is an OOM kill, while too little CPU is a slower job. A CPU number
    large enough to matter can also make the bundle unsatisfiable -- Ray
    schedules CPU and memory together, so a writer asking for more cores than
    any node has is never placed at all. That is a hard failure bought for a
    soft benefit, and the declared figure was never a claim about real usage
    anyway: the Lance encoder bursts to all cores regardless.

    ``floor_num_cpus`` is what every non-deferred-carry-forward writer already
    declares, so this keeps the two paths consistent rather than making one of
    them special.

    ``base_memory_bytes`` / ``floor_num_cpus`` are the existing fixed defaults,
    used as floors so small writers stay cheap to schedule.
    """
    working = max(0, int(num_rows)) * max(0, int(avg_row_bytes))
    memory = int(base_memory_bytes + overhead * working)
    return memory, float(floor_num_cpus)


def humanize_bytes(n: int) -> str:
    """Render a byte count as a short binary-unit string (e.g. ``15.0 GiB``)."""
    size = float(max(0, int(n)))
    for unit in _UNITS:
        if size < 1024.0 or unit == _UNITS[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} {_UNITS[-1]}"


def estimate_fixed_width_output_row_bytes(schema: pa.Schema) -> int | None:
    """Estimate fixed-width output bytes/row from a declared Arrow schema.

    Returns None when any non-``_rowaddr`` field has variable or unknown width.
    """
    total = 0
    for field in schema:
        if field.name == "_rowaddr":
            continue
        field_bytes = _fixed_width_type_bytes(field.type)
        if field_bytes is None:
            return None
        total += field_bytes
    return total


def choose_output_avg_row_bytes(
    *,
    fixed_width_output_avg_row_bytes: int | None,
    sampled_output_avg_row_bytes: int | None,
) -> int | None:
    """Choose the applier output bytes/row estimate for startup budgeting.

    The declared schema is exact when it is fixed-width. For variable-width
    re-backfills, a sample of the existing output columns is a better estimate
    than the input row size fallback.
    """
    if fixed_width_output_avg_row_bytes is not None:
        return fixed_width_output_avg_row_bytes
    return sampled_output_avg_row_bytes


def _fixed_width_type_bytes(dtype: pa.DataType) -> int | None:
    if _is_variable_or_unknown_container(dtype):
        return None

    if pa.types.is_struct(dtype):
        total = 0
        for field in dtype:
            field_bytes = _fixed_width_type_bytes(field.type)
            if field_bytes is None:
                return None
            total += field_bytes
        return total

    if pa.types.is_fixed_size_list(dtype):
        value_bytes = _fixed_width_type_bytes(dtype.value_type)
        if value_bytes is None:
            return None
        return int(dtype.list_size) * value_bytes

    if (
        pa.types.is_boolean(dtype)
        or pa.types.is_integer(dtype)
        or pa.types.is_floating(dtype)
        or pa.types.is_decimal(dtype)
        or pa.types.is_fixed_size_binary(dtype)
        or pa.types.is_temporal(dtype)
        or pa.types.is_interval(dtype)
    ):
        try:
            return max(1, int(dtype.byte_width))
        except ValueError:
            return max(1, int(dtype.bit_width + 7) // 8)

    return None


def _is_variable_or_unknown_container(dtype: pa.DataType) -> bool:
    variable_predicates = (
        pa.types.is_binary,
        pa.types.is_large_binary,
        pa.types.is_string,
        pa.types.is_large_string,
        pa.types.is_list,
        pa.types.is_large_list,
        pa.types.is_map,
        pa.types.is_union,
        pa.types.is_dictionary,
    )
    return any(predicate(dtype) for predicate in variable_predicates)


@attrs.frozen(kw_only=True)
class MemoryBudget:
    """Projected per-actor / per-writer / per-pod RAM for a backfill job.

    All sizes are bytes. The estimate is deliberately conservative -- it is a
    sizing floor, not a measurement.
    """

    input_avg_row_bytes: int
    output_avg_row_bytes: int | None
    writer_avg_row_bytes: int
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
    def effective_output_avg_row_bytes(self) -> int:
        """Output bytes/row used for applier sizing, falling back to input size."""
        if self.output_avg_row_bytes is None:
            return max(0, int(self.input_avg_row_bytes))
        return max(0, int(self.output_avg_row_bytes))

    @property
    def applier_inflight_bytes(self) -> int:
        """Input batch + UDF output held in flight for one checkpoint chunk."""
        return int(
            self.checkpoint_size
            * max(1, self.intra_applier_concurrency)
            * (
                max(0, int(self.input_avg_row_bytes))
                + self.effective_output_avg_row_bytes
            )
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
        (``(matched + tranche) x writer_avg_row_bytes``); the base + 1.5x
        overhead is what Ray demands of the pod on top of it.

        Zero when carry-forward is not deferred (the legacy writer streams
        checkpoints and is not a separate large-memory site).
        """
        if not self.deferred_carry_forward:
            return 0
        working = (
            self.matched_rows_per_frag_est + self.tranche_rows
        ) * self.writer_avg_row_bytes
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
        if self.output_avg_row_bytes is None:
            output_estimate = (
                "n/a (unknown; using input_avg_row_bytes fallback "
                f"{humanize_bytes(self.effective_output_avg_row_bytes)})"
            )
        else:
            output_estimate = humanize_bytes(self.output_avg_row_bytes)

        lines = [
            "memory budget estimate:",
            f"  input_avg_row_bytes  ~= {humanize_bytes(self.input_avg_row_bytes)}",
            f"  output_avg_row_bytes ~= {output_estimate}",
            f"  writer_avg_row_bytes ~= {humanize_bytes(self.writer_avg_row_bytes)}",
            f"  checkpoint_size       = {self.checkpoint_size} rows",
            f"  intra_applier_conc    = {self.intra_applier_concurrency}",
            f"  pending_target        = {humanize_bytes(self.pending_target_bytes)}",
            f"  per_actor_bytes      ~= {humanize_bytes(self.per_actor_bytes)}"
            f"  (ckpt x ic x (input + output) + pending + slack)",
        ]
        if self.deferred_carry_forward:
            lines += [
                f"  matched_rows/frag est = {self.matched_rows_per_frag_est}"
                f"  (worst case; WHERE selectivity x frag rows)",
                f"  tranche_rows          = {self.tranche_rows}",
                f"  per_writer_bytes     ~= {humanize_bytes(self.per_writer_bytes)}"
                f"  (base + overhead x (matched + tranche) x writer_row)"
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
