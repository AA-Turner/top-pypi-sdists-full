# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Crosses op-sequences x fault-points x write-path flavors against an Arrow oracle.

Flavors exercise distinct durable-write paths: ``backfill`` (DataReplacement),
``mv-identity`` (projection MV refresh), ``sparse`` (sparse-row backfill, atomic
``Update``), ``chunker`` (UDTF 1:N view that ``Append``s rows), and ``repair`` (filtered
re-backfill of one already-committed row; ``task_size=1`` forces per-range checkpoints,
so a fault can strand checkpoint state over a pre-existing output file -- the
resume-trusts-stale-coverage precondition. Its oracle covers only the filtered row).
The commit fault matches a per-flavor op-name (``FLAVOR_COMMIT_OPS``); frag/ckpt/twrite
faults only reach ``backfill`` and ``repair``.

Every fault is a failure a durable write can ACTUALLY exhibit -- a real storage error
(``raise`` / ``raise_after``), a lost/no-op write (``drop``), or a faithful worker death
(``actordeath``: kill the applier actor -> ``RayActorError`` -> geneva's real death
path). There is deliberately no fabricated ``short`` / partial-write fault: object-store
writes are atomic and a lance file carries its own row count, so a silently-truncated
artifact cannot arise, and injecting one only produces disputable findings. The
application-level ways a durable artifact ends up short (a worker dying mid-fragment and
its partial checkpoint being trusted on resume; a skip-on-error dropping rows) need a
specific precondition to reproduce and are covered faithfully by the targeted scenarios
in ``worker_death_faults.py`` (e.g. ``repair_resume_noop``, ``skip_budget_bypass``).
``backfill-skip`` is backfill with a zero-skip-budget column, run ONLY with
``actordeath`` to expose the bypass where the death silently NULLs the dead rows. The
``sparse`` and ``chunker`` write paths are not yet routed through the injectable
indirections (their data writes go through ``lance.fragment.write_fragments`` /
``LanceFragment.create``, under ``SparseActor`` / ``ChunkerExpandActor`` rather than
``ApplierActor``), so for those two flavors only the commit fault fires; others NOFIRE.

Every flavor runs the same op alphabet (``OPS``); the matrix is uniform. The one
combination whose oracle is invalid -- ``chunker`` with an in-place source UPDATE, where
the 1:N view is known-stale regardless of any fault -- is classified ``KNOWN_STALE`` and
counted separately, so it is visible in the summary rather than silently omitted.

Each ``(flavor, op-sequence, fault)`` case builds the flavor, applies the op-sequence
(materializing cleanly after every op but the last), materializes the last op with one
fault injected, runs up to two clean resumes, and classifies against the invariant: a
faulted job must either complete correctly or fail loudly -- it must never report
success while the table is wrong. Verdicts: ``HEAL``; ``FALSE_SUCCESS`` (reported DONE
while rows were missing/stale -- a hard finding even though a manual rerun healed it,
since nothing reruns a DONE job in production); ``DIVERGE_GAP`` / ``DIVERGE_VALUE``
(resume silently left it wrong); ``STUCK`` (resume crashed AND left a gap); ``WEDGE``
(the case hung until the per-case alarm killed it -- a liveness wedge); ``CORRUPT``
/ ``CORRUPT_FALSE_SUCCESS`` (left it unreadable); ``NOFIRE``; ``KNOWN_STALE``. The
``probe`` case is not a fault: it reads the view after EVERY durable write of one clean
materialization (any committed state is a state a concurrent reader could see) and
verdicts ``EXPOSED`` (a boundary read saw placeholder NULL view rows -- a hard finding)
or ``CLEAN_READS``; it crosses only the view flavors, since a NULL mid-backfill is
inherent to adding a column in place. Only HEAL / NOFIRE / KNOWN_STALE / CLEAN_READS
pass.

Not a pytest test (it monkeypatches ``ray`` before importing geneva); run directly, or
via ``test_differential_fault_sweep``. ``GENEVA_FAULTSWEEP_MAXLEN`` sets op-sequence
depth (default 2); ``SWEEP_WORKERS`` the pool size; ``GENEVA_FAULTSWEEP_FLAVORS``
restricts the flavor set (csv); ``GENEVA_FAULTSWEEP_CASE_TIMEOUT_S`` the per-case
wedge alarm (default 120). Progress goes to the driver's stderr (live line on a tty,
one line per 10% otherwise); worker stderr is silenced unless
``GENEVA_FAULTSWEEP_WORKER_STDERR=1``.
"""

# ruff: noqa: T201 -- this is a CLI script; print() is the intended output

import itertools
import logging
import multiprocessing as mp
import os
import shutil
import signal
import sys
import tempfile
import time
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import NamedTuple

# Silence geneva noise below CRITICAL: the raise faults log the injected error, and the
# pipeline logs per-job INFO. logging.disable is a global floor geneva's own logging
# cannot raise back (a plain setLevel on "geneva" gets overridden at job time).
logging.disable(logging.ERROR)
# Suppress geneva's live tqdm progress lines (job/heartbeat/writer/...); over hundreds
# of in-process cases they interleave with the summary and add nothing.
os.environ.setdefault("TQDM_DISABLE", "1")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ray_shim  # noqa: E402

ray_shim.install()  # MUST precede the geneva import below

import lance  # noqa: E402
import pyarrow as pa  # noqa: E402
import ray  # noqa: E402 -- the real module; the shim patches scheduling, not exceptions
from geneva_faults import (  # noqa: E402
    CheckpointFaultPolicy,
    FlakyCommitter,
    FlakyFragmentFileWriter,
    FlakyTableWriter,
    by_op_name,
    flaky_checkpoint_wrap,
)

import geneva  # noqa: E402
from geneva import connect, udf  # noqa: E402
from geneva.checkpoint import using_checkpoint_store_wrap  # noqa: E402
from geneva.committer import using_committer  # noqa: E402
from geneva.db import Connection  # noqa: E402
from geneva.debug.error_store import skip_on_error  # noqa: E402
from geneva.fragment_writer import using_fragment_file_writer  # noqa: E402
from geneva.table import Table  # noqa: E402
from geneva.table_writer import using_table_writer  # noqa: E402

ray_shim.stub_geneva_cluster_polling()

APPEND, DELETE, UPDATE, COMPACT = "A", "D", "U", "C"
OPS = [APPEND, DELETE, UPDATE, COMPACT]  # every flavor runs the full op alphabet


@udf(data_type=pa.int64())
def _double(value: int) -> int:
    return value * 2


# Zero skip budget: ANY skipped row must fail the job. A worker death NULLs the rows.
@udf(data_type=pa.int64(), on_error=skip_on_error(max_skip_count=0))
def _double_skip(value: int) -> int:
    return value * 2


SPARSE_MODE = "sparse_rows"  # update_mode for the sparse (delete+append) path


class _Chunk(NamedTuple):
    k: int
    derived: int


@geneva.chunker
def _expand2(value: int) -> Iterator[_Chunk]:
    # 1:2 expansion -- the UDTF/chunker flavor, a distinct checkpoint/commit path
    for k in range(2):
        yield _Chunk(k=k, derived=value * 10 + k)


def _initial() -> pa.Table:
    return pa.table({"id": [1, 2, 3, 4], "value": [10, 20, 30, 40]})


def _append_block(n: int) -> pa.Table:
    base = 100 * (n + 1)
    ids = [base, base + 1, base + 2]
    return pa.table({"id": ids, "value": [i * 10 for i in ids]})


def _apply_op(source: Table, op: str, append_n: int) -> None:
    if op == APPEND:
        source.add(_append_block(append_n))
    elif op == DELETE:
        source.delete("id % 2 = 0")
    elif op == UPDATE:
        source.update(where="id % 2 = 1", values_sql={"value": "-1"})
    elif op == COMPACT:
        source.compact_files()


def _sorted(rows: list[tuple]) -> list[tuple]:
    return sorted(
        rows, key=lambda r: tuple((x is None, x if x is not None else 0) for x in r)
    )


def _live(source: Table) -> list[tuple]:
    t = source.to_arrow()
    return list(zip(t["id"].to_pylist(), t["value"].to_pylist(), strict=True))


def _mk_source(db: Connection, name: str) -> Table:
    return db.create_table(
        name, _initial(), storage_options={"new_table_enable_stable_row_ids": "true"}
    )


# flavor descriptors: (setup, materialize, oracle, read, ops); mv None for backfill
def _setup_backfill(db: Connection, name: str) -> tuple[Table, Table | None]:
    s = _mk_source(db, name)
    s.add_columns({"doubled": _double})
    s.backfill("doubled", where="1=1", _admission_check=False)
    return s, None


def _materialize_backfill(source: Table, _mv: Table | None) -> None:
    source.backfill("doubled", where="1=1", _admission_check=False)


def _oracle_backfill(source: Table, _mv: Table | None) -> list[tuple]:
    return _sorted([(i, v, (None if v is None else v * 2)) for (i, v) in _live(source)])


def _read_backfill(source: Table, _mv: Table | None) -> list[tuple]:
    t = source.to_arrow()
    return _sorted(
        list(
            zip(
                t["id"].to_pylist(),
                t["value"].to_pylist(),
                t["doubled"].to_pylist(),
                strict=True,
            )
        )
    )


def _setup_backfill_skip(db: Connection, name: str) -> tuple[Table, Table | None]:
    # Like backfill but the UDF has a zero skip budget; only a worker death skips.
    s = _mk_source(db, name)
    s.add_columns({"doubled": _double_skip})
    s.backfill("doubled", where="1=1", _admission_check=False)
    return s, None


def _setup_mv(db: Connection, name: str) -> tuple[Table, Table | None]:
    s = _mk_source(db, name)
    mv = (
        s.search(None).select(["id", "value"]).create_materialized_view(db, f"m_{name}")
    )  # pyright: ignore[reportAttributeAccessIssue]
    mv.refresh(_admission_check=False)
    return s, mv


def _materialize_mv(_source: Table, mv: Table | None) -> None:
    assert mv is not None
    mv.refresh(_admission_check=False)


def _oracle_mv(source: Table, _mv: Table | None) -> list[tuple]:
    return _sorted(_live(source))


def _read_mv(_source: Table, mv: Table | None) -> list[tuple]:
    assert mv is not None
    t = mv.to_arrow()
    return _sorted(list(zip(t["id"].to_pylist(), t["value"].to_pylist(), strict=True)))


# sparse-update flavor: re-backfill via the sparse (delete+append) commit path
def _setup_sparse(db: Connection, name: str) -> tuple[Table, Table | None]:
    s = _mk_source(db, name)
    s.add_columns({"doubled": _double})
    s.backfill("doubled", where="1=1", _admission_check=False, update_mode=SPARSE_MODE)
    return s, None


def _materialize_sparse(source: Table, _mv: Table | None) -> None:
    source.backfill(
        "doubled", where="1=1", _admission_check=False, update_mode=SPARSE_MODE
    )


# repair flavor: filtered re-backfill of ONE already-committed row. task_size=1 forces
# per-range checkpoints, so a fault can strand checkpoint state over a pre-existing
# output file -- the precondition for a resume trusting stale coverage and no-oping.
_REPAIR_TARGET = 1  # odd id: UPDATE staleness hits it, DELETE (even ids) never does


def _setup_repair(db: Connection, name: str) -> tuple[Table, Table | None]:
    s = _mk_source(db, name)
    s.add_columns({"doubled": _double})
    s.backfill("doubled", where="1=1", commit_granularity=1, _admission_check=False)
    return s, None


def _materialize_repair(source: Table, _mv: Table | None) -> None:
    source.backfill(
        "doubled",
        where=f"id = {_REPAIR_TARGET}",
        task_size=1,
        commit_granularity=1,
        _admission_check=False,
    )


def _oracle_repair(source: Table, _mv: Table | None) -> list[tuple]:
    # The repair's contract covers only the filtered row: it must end up recomputed
    # from the CURRENT source value (or the job must fail loud). Other rows are
    # legitimately stale until repaired, so they are outside this oracle.
    return _sorted(
        [
            (i, v, None if v is None else v * 2)
            for (i, v) in _live(source)
            if i == _REPAIR_TARGET
        ]
    )


def _read_repair(source: Table, _mv: Table | None) -> list[tuple]:
    t = source.to_arrow()
    return _sorted(
        [
            (i, v, d)
            for (i, v, d) in zip(
                t["id"].to_pylist(),
                t["value"].to_pylist(),
                t["doubled"].to_pylist(),
                strict=True,
            )
            if i == _REPAIR_TARGET
        ]
    )


# chunker/UDTF 1:2 expansion view; each output row keyed (id*10+k) for the gap calc
def _setup_chunker(db: Connection, name: str) -> tuple[Table, Table | None]:
    s = _mk_source(db, name)
    mv = db.create_udtf_view(
        f"m_{name}", s.search(None).select(["id", "value"]), _expand2
    )
    mv.refresh(_admission_check=False)
    return s, mv


def _materialize_chunker(_source: Table, mv: Table | None) -> None:
    assert mv is not None
    mv.refresh(_admission_check=False)


def _oracle_chunker(source: Table, _mv: Table | None) -> list[tuple]:
    out: list[tuple] = []
    for i, v in _live(source):
        out.append((i * 10, None if v is None else v * 10))
        out.append((i * 10 + 1, None if v is None else v * 10 + 1))
    return _sorted(out)


def _read_chunker(_source: Table, mv: Table | None) -> list[tuple]:
    assert mv is not None
    t = mv.to_arrow()
    return _sorted(
        [
            (i * 10 + k, d)
            for i, k, d in zip(
                t["id"].to_pylist(),
                t["k"].to_pylist(),
                t["derived"].to_pylist(),
                strict=True,
            )
        ]
    )


FLAVORS: dict[str, tuple] = {  # flavor -> (setup, materialize, oracle, read)
    "backfill": (
        _setup_backfill,
        _materialize_backfill,
        _oracle_backfill,
        _read_backfill,
    ),
    "mv-identity": (_setup_mv, _materialize_mv, _oracle_mv, _read_mv),
    "sparse": (_setup_sparse, _materialize_sparse, _oracle_backfill, _read_backfill),
    # backfill with a ZERO skip budget; only actordeath routes through the skip path.
    "backfill-skip": (
        _setup_backfill_skip,
        _materialize_backfill,
        _oracle_backfill,
        _read_backfill,
    ),
    "chunker": (_setup_chunker, _materialize_chunker, _oracle_chunker, _read_chunker),
    # filtered repair of one committed row (per-range checkpoints via task_size=1)
    "repair": (_setup_repair, _materialize_repair, _oracle_repair, _read_repair),
}

# The committer op-name for each flavor's durable DATA commit, so the commit fault hits
# the data write not a marker/system commit.
FLAVOR_COMMIT_OPS: dict[str, tuple[str, ...]] = {
    "backfill": ("DataReplacement",),
    "mv-identity": ("DataReplacement",),
    "sparse": ("Update",),
    "chunker": ("Append",),
    "backfill-skip": ("DataReplacement",),
    "repair": ("DataReplacement",),
}


# fault matrix. (target, mode, occ): occ a 1-based occurrence or "all", on the LAST op.
FAULTS: list[tuple[str, str, object]] = [
    # No ("commit", "drop", ...): LanceDataset.commit is atomic on the object-store
    # path -- it lands the manifest or raises, so a commit that returns success without
    # writing is not a reachable state. The reachable "fragment stranded, job reports
    # success" end-state is driven faithfully by the frag writer-death fault below and
    # asserted in scenario_graceful_degradation_false_success.
    ("commit", "raise", 1),
    ("commit", "raise_after", 1),
    # retryable-conflict shapes: geneva's commit loop classifies conflicts by error
    # text and retries against the refetched version. "conflict" = a concurrent writer
    # won the version (commit did NOT land; the retry should heal). "conflict_after" =
    # the commit LANDED but the ack was lost; a retry that cannot tell itself from the
    # original re-applies an already-landed commit (double-apply probe).
    ("commit", "conflict", 1),
    ("commit", "conflict_after", 1),
    ("twrite-add", "drop", 1),
    ("twrite-add", "raise", 1),
    ("twrite-add", "raise_after", 1),
    ("frag", "raise", 1),
    ("ckpt-set", "drop", 1),
    ("ckpt-set", "raise", 1),
    # checkpoint read-side faults, modeling the real invisible-directory path (the
    # identity sidecar write is best-effort and negatively cached, so LISTs can return
    # nothing and the mismatch probes can report "no reprocess needed" over changed
    # data). "list drop" hides checkpoint coverage; "mismatch drop" hides staleness.
    ("ckpt-list", "drop", 1),
    ("ckpt-list", "drop", "all"),
    ("ckpt-list", "raise", 1),
    ("ckpt-mismatch", "drop", "all"),
    # actordeath: a faithful worker death (real RayActorError -> geneva's real death
    # path). Resume must heal every row (backfill-skip: expose the skip-budget bypass).
    ("actordeath", "kill", 1),
    ("actordeath", "kill", "all"),
    # other actor classes and loss shapes (see _DEATH_SPECS): the fragment-writer actor
    # dying or going unavailable mid-write (its session restarts it and replays cached
    # tasks), the sparse/chunker actors dying, and an applier OOM -- which surfaces as
    # ray's OutOfMemoryError, a RayError that is NOT a RayActorError, probing whether
    # the pool's actor-loss taxonomy covers it.
    ("writerdeath", "kill", 1),
    # every write call dies -> the session's restart budget (MAX_WRITER_RESTARTS)
    # exhausts; the job must fail loud, never report success with the fragment missing.
    ("writerdeath", "kill", "all"),
    ("writerdeath", "unavail", 1),
    ("sparsedeath", "kill", 1),
    ("chunkerdeath", "kill", 1),
    ("actordeath", "oom", 1),
    # queue faults: applier->writer checkpoint enqueues are fire-and-forget
    # (put_nowait, no awaited ack) with an in-band seal sentinel, and the writer
    # NULL-fills any range unfilled at seal. A lost enqueue is silent NULLs over real
    # UDF output; a duplicated enqueue probes idempotent ingestion.
    ("queue", "drop", 1),
    ("queue", "drop", "all"),
    ("queue", "dup", 1),
    # probe: no injected failure -- a read of the view after EVERY durable write during
    # the materialization. Any committed state is a state a concurrent reader could see,
    # so a visible placeholder (NULL view column) at any boundary is a finding. Crossed
    # only with the view flavors (see _PROBE_FLAVORS): a NULL mid-backfill is inherent
    # to adding a column in place, not a bug.
    ("probe", "observe", "all"),
]

# Flavors where a mid-refresh NULL view column is a violation (placeholder exposure).
_PROBE_FLAVORS = frozenset({"mv-identity", "chunker"})

# (target, mode) -> (actor class, method, error factory). The error types are the ones
# real Ray surfaces: ActorDiedError/ActorUnavailableError are RayActorError subclasses
# (the writer session catches exactly those two); OutOfMemoryError is a plain RayError,
# OUTSIDE the pool's actor-loss set -- the taxonomy probe.
_DEATH_SPECS: dict[tuple[str, str], tuple[str, str, Callable[[], BaseException]]] = {
    ("actordeath", "kill"): ("ApplierActor", "run", ray.exceptions.RayActorError),
    ("actordeath", "oom"): (
        "ApplierActor",
        "run",
        lambda: ray.exceptions.OutOfMemoryError("injected worker OOM kill"),
    ),
    ("writerdeath", "kill"): (
        "FragmentWriter",
        "write",
        ray.exceptions.ActorDiedError,
    ),
    ("writerdeath", "unavail"): (
        "FragmentWriter",
        "write",
        lambda: ray.exceptions.ActorUnavailableError("injected unavailable", None),
    ),
    ("sparsedeath", "kill"): ("SparseActor", "run", ray.exceptions.RayActorError),
    ("chunkerdeath", "kill"): (
        "ChunkerExpandActor",
        "expand_batch",
        ray.exceptions.RayActorError,
    ),
}

# fault target -> flavors it can reach (unlisted targets run on every flavor); keeps
# the matrix free of structurally-impossible cases.
_ALL_FLAVORS = frozenset(FLAVORS)
_FAULT_FLAVORS: dict[str, frozenset[str]] = {
    "probe": _PROBE_FLAVORS,
    "writerdeath": frozenset({"backfill", "mv-identity", "repair"}),
    "sparsedeath": frozenset({"sparse"}),
    "chunkerdeath": frozenset({"chunker"}),
    # only FragmentWriterSession flavors route checkpoints through the queue
    "queue": frozenset({"backfill", "mv-identity", "repair"}),
}


class _ReadProbe:
    """Shared recorder for the probe wrappers: after each successful durable write it
    reads the view and records whether a placeholder (NULL view column) was visible."""

    def __init__(self, sees_placeholder: Callable[[], bool]) -> None:
        self._sees_placeholder = sees_placeholder
        self.writes = 0
        self.exposed_at: list[int] = []

    def after_write(self) -> None:
        self.writes += 1
        if self._sees_placeholder():
            self.exposed_at.append(self.writes)


class _ProbeCommitter(FlakyCommitter):
    """Pass-through committer (no faults) that runs the read-probe after each commit."""

    def __init__(self, probe: _ReadProbe) -> None:
        super().__init__()
        self._probe = probe

    def commit(self, *args: object, **kwargs: object) -> object:
        out = super().commit(*args, **kwargs)  # type: ignore[arg-type]
        self._probe.after_write()
        return out


class _ProbeTableWriter(FlakyTableWriter):
    """Pass-through table writer (no faults) probing after each add/update/delete."""

    def __init__(self, probe: _ReadProbe) -> None:
        super().__init__()
        self._probe = probe

    def _maybe(self, op: str, ltbl: object, *args: object, **kwargs: object) -> object:
        out = super()._maybe(op, ltbl, *args, **kwargs)
        self._probe.after_write()
        return out


def _probe_materialize(
    materialize: Callable, read: Callable, source: Table, mv: Table | None
) -> str:
    """One clean materialization with the read-probe installed at the committer and
    table-writer indirections. EXPOSED if any boundary read saw a placeholder.

    Each boundary read opens the view's lance dataset fresh (a concurrent reader sees
    the latest committed version; the harness Table handle stays pinned mid-job). A
    placeholder is a row with a NULL view column; rows-marked-usable via a True
    ``__is_set`` anywhere means readers have a filter, so it does not count as exposed.
    """
    assert mv is not None

    def _sees_placeholder() -> bool:
        try:
            t = lance.dataset(mv.uri).to_table()
        except Exception:  # noqa: BLE001 -- transiently unreadable view: not exposure
            return False
        cols = [c for c in t.column_names if not c.startswith("__")]
        if not any(v is None for c in cols for v in t[c].to_pylist()):
            return False
        # a True __is_set anywhere is a usable read-side gate -- not exposed
        gated = "__is_set" in t.column_names and any(t["__is_set"].to_pylist())
        return not gated

    probe = _ReadProbe(_sees_placeholder)
    with (
        using_committer(_ProbeCommitter(probe)),
        using_table_writer(_ProbeTableWriter(probe)),
    ):
        materialize(source, mv)
    if probe.writes == 0:
        return "NOFIRE"
    return "EXPOSED" if probe.exposed_at else "CLEAN_READS"


def _fault(
    spec: tuple[str, str, object], commit_ops: tuple[str, ...]
) -> tuple[object, Callable[[], bool]]:
    """Return ``(context_manager, fired_predicate)`` for a fault spec. The predicate
    reports whether the fault fired, so a spec targeting a write the flavor never issues
    is a recognizable NOFIRE. ``commit_ops`` is what the commit fault matches on."""
    target, mode, occ = spec
    occs = frozenset(range(1, 64)) if occ == "all" else frozenset({int(occ)})  # type: ignore[arg-type]
    drop = occs if mode == "drop" else ()
    rai = occs if mode == "raise" else ()
    raf = occs if mode == "raise_after" else ()
    cfl = occs if mode == "conflict" else ()
    cfa = occs if mode == "conflict_after" else ()
    if target == "commit":
        f = FlakyCommitter(
            match=by_op_name(*commit_ops),
            drop_at=drop,
            raise_at=rai,
            raise_after=raf,
            conflict_at=cfl,
            conflict_after=cfa,
        )
        fired = (f.dropped, f.raised, f.raised_after, f.conflicted, f.conflicted_after)
        return using_committer(f), lambda: any(fired)
    if target == "twrite-add":
        w = FlakyTableWriter(ops={"add"}, drop_at=drop, raise_at=rai, raise_after=raf)
        return using_table_writer(w), lambda: bool(
            w.dropped or w.raised or w.raised_after
        )
    if target == "frag":
        # fragment writer raises a real storage error (an atomic write either lands or
        # fails; there is no partial/short object in object storage).
        fw = FlakyFragmentFileWriter(raise_at=rai)
        return using_fragment_file_writer(fw), lambda: bool(fw.raised)
    if target in ("ckpt-set", "ckpt-list", "ckpt-mismatch"):
        op = {"ckpt-set": "set", "ckpt-list": "list", "ckpt-mismatch": "mismatch"}[
            target
        ]
        p = CheckpointFaultPolicy(ops={op}, drop_at=drop, raise_at=rai)
        return using_checkpoint_store_wrap(flaky_checkpoint_wrap(p)), lambda: bool(
            p.dropped or p.raised
        )
    if target == "queue":
        qp = ray_shim.make_queue_fault_policy(
            drop_at=drop, dup_at=occs if mode == "dup" else ()
        )
        return ray_shim.using_queue_faults(qp), lambda: bool(qp.dropped or qp.dupped)
    if (target, mode) in _DEATH_SPECS:
        # kill the target actor with the spec'd error; fires only where the actor runs
        cls, method, factory = _DEATH_SPECS[(target, mode)]
        pol = ray_shim.make_actor_death_policy(cls, method, tuple(occs), factory)
        return ray_shim.using_actor_death_policy(pol), lambda: bool(pol.fired)
    raise ValueError(f"unknown fault target {target!r}")


def _gap(got: list[tuple], exp: list[tuple]) -> tuple[int, int]:
    """``(n_missing_or_null, n_wrong_value)`` between a read and the oracle. The first
    counts oracle rows null/absent in the read (silent loss); the second counts wrong
    non-null values plus any row-count mismatch."""
    if got == exp:
        return (0, 0)
    g = {r[0]: r[-1] for r in got}
    e = {r[0]: r[-1] for r in exp}
    n_null = sum(1 for k, v in e.items() if g.get(k) is None and v is not None)
    n_val = abs(len(got) - len(exp))
    for k, v in e.items():
        gv = g.get(k)
        if gv is not None and v is not None and gv != v:
            n_val += 1
    return (n_null, n_val)


# Read-state sentinel: the table cannot be read at all (a corrupt artifact committed).
_UNREADABLE = "UNREADABLE"


def _state(read: Callable, oracle: Callable, source: Table, mv: Table | None) -> object:
    """Post-materialization state: a ``(n_null, n_val)`` gap vs the oracle, or
    ``_UNREADABLE`` if reading the table raises."""
    try:
        return _gap(read(source, mv), oracle(source, mv))
    except Exception:  # noqa: BLE001 -- an unreadable table is itself the signal
        return _UNREADABLE


def _classify(
    fired: bool,
    faulted_raised: Exception | None,
    state_f: object,
    resume_raised: Exception | None,
    state_r: object,
) -> str:
    """Map an outcome to a verdict. FALSE_SUCCESS and DIVERGE_* (the job lied about the
    data) are hard findings; CORRUPT (unreadable) and STUCK (resume crashed) are loud
    findings, surfaced but needing real-Ray / real-storage confirmation."""
    if not fired and faulted_raised is None:
        return "NOFIRE"
    if state_r is _UNREADABLE:
        # CORRUPT_FALSE_SUCCESS when the faulted op also reported success
        return "CORRUPT_FALSE_SUCCESS" if faulted_raised is None else "CORRUPT"
    nn_r, nv_r = state_r  # type: ignore[misc]
    if nn_r == 0 and nv_r == 0:
        fs = (0, 0) if state_f is _UNREADABLE else state_f
        if faulted_raised is None and any(fs):  # type: ignore[arg-type]
            # The job reported DONE while rows were missing/stale; only the manual
            # rerun below healed it. Nothing reruns a DONE job in production, so this
            # is the silent-false-success bug class, not a pass.
            return "FALSE_SUCCESS"
        return "HEAL"
    if resume_raised is not None:
        return "STUCK"  # loud but unrecovered (resume crashes, gap remains)
    return "DIVERGE_VALUE" if nv_r else "DIVERGE_GAP"  # SILENT divergence


def _run_case(db: Connection, name: str, flavor: str, seq: tuple, fault: tuple) -> str:
    # The chunker view is known-stale after an in-place source update, so its oracle is
    # invalid for any sequence containing UPDATE. Surface that as KNOWN_STALE (a
    # non-finding, distinct from a real divergence) rather than running it.
    if flavor == "chunker" and UPDATE in seq:
        return _KNOWN_STALE
    setup, materialize, oracle, read = FLAVORS[flavor]
    source, mv = setup(db, name)
    if read(source, mv) != oracle(source, mv):
        return "NEW@init"  # baseline divergence before any fault (should not happen)

    append_n = 0
    for op in seq[:-1]:
        _apply_op(source, op, append_n)
        if op == APPEND:
            append_n += 1
        materialize(source, mv)

    last = seq[-1]
    _apply_op(source, last, append_n)

    if fault[0] == "probe":
        return _probe_materialize(materialize, read, source, mv)

    cm, fired = _fault(fault, FLAVOR_COMMIT_OPS[flavor])
    faulted_raised: Exception | None = None
    with cm:
        try:
            materialize(source, mv)
        except Exception as e:  # noqa: BLE001 -- the injected fault (or its fallout)
            faulted_raised = e
    did_fire = fired()
    state_f = _state(read, oracle, source, mv)

    # up to two clean resume attempts -- a fair chance to heal before STUCK/CORRUPT
    resume_raised: Exception | None = None
    state_r = state_f
    for _ in range(2):
        try:
            materialize(source, mv)
            resume_raised = None
        except Exception as e:  # noqa: BLE001
            resume_raised = e
        state_r = _state(read, oracle, source, mv)
        if state_r == (0, 0):
            break

    return _classify(did_fire, faulted_raised, state_f, resume_raised, state_r)


# Hard findings -- the job lied about the data (reported success while it was wrong,
# silently left it diverged, or exposed placeholder rows to readers) -- fail the sweep.
_FINDINGS = ("FALSE_SUCCESS", "DIVERGE_GAP", "DIVERGE_VALUE", "EXPOSED", "NEW@init")
# Soft findings -- LOUD robustness gaps (resume crash / corrupt unreadable table /
# a case that hung until the per-case alarm killed it).
_SOFT = ("STUCK", "CORRUPT", "CORRUPT_FALSE_SUCCESS", "WEDGE")


# A case that neither completes nor fails is itself a finding (a liveness wedge --
# e.g. a writer waiting forever on a queue item that will never arrive), and it must
# not stall the whole batch. SIGALRM fires on the worker's main thread, so the wedge
# surfaces wherever the case is stuck. It subclasses BaseException, not Exception, so
# the alarm-raised wedge propagates through the broad ``except Exception`` blocks in
# _run_case (which wrap the faulted materialize -- the likeliest wedge site) instead of
# being swallowed there and misclassified as an ordinary injected fault.
class _CaseWedgeError(BaseException):
    pass


def _on_case_timeout(signum: int, frame: object) -> None:
    raise _CaseWedgeError


_CASE_TIMEOUT_S = int(os.environ.get("GENEVA_FAULTSWEEP_CASE_TIMEOUT_S", "120"))
# A case whose oracle is known-invalid (not a finding): chunker + in-place source
# UPDATE. Counted and printed so the skip is visible, never silently omitted.
_KNOWN_STALE = "KNOWN_STALE"

# Plain-English rendering of the terse case grammar, so the summary reads at a glance.
_FLAVOR_DESC = {
    "backfill": "backfill",
    "mv-identity": "MV refresh",
    "sparse": "sparse backfill",
    "backfill-skip": "backfill (zero skip-budget)",
    "chunker": "chunker view",
    "repair": "filtered repair",
}
_OP_DESC = {"A": "append", "D": "delete", "U": "update", "C": "compact"}
# WHERE a fault fires: the durable write (or worker) it targets.
_TARGET_DESC = {
    "commit": "the manifest commit",
    "twrite-add": "the table add()",
    "frag": "the fragment-file write",
    "ckpt-set": "the checkpoint write",
    "ckpt-list": "the checkpoint LIST",
    "ckpt-mismatch": "the checkpoint staleness probe",
    "actordeath": "the applier worker",
    "writerdeath": "the fragment-writer actor",
    "sparsedeath": "the sparse-update actor",
    "chunkerdeath": "the chunker expand actor",
    "queue": "a checkpoint enqueue to the writer",
    "probe": "a concurrent reader",
}
# WHAT KIND of fault: what that target does under injection. All are real failures a
# durable write can actually exhibit -- no fabricated partial/short artifacts.
_MODE_DESC = {
    "drop": "was silently dropped (no-op, returned success)",
    "raise": "raised an error partway",
    "raise_after": "completed, then raised an error",
    "conflict": "lost the version race to a concurrent writer (retryable conflict)",
    "conflict_after": "landed but reported a retryable conflict (lost ack)",
    "kill": "was killed mid-write",
    "oom": "was OOM-killed (OutOfMemoryError, outside the actor-loss set)",
    "unavail": "became unavailable mid-write (ActorUnavailableError)",
    "dup": "was delivered twice (duplicated enqueue)",
    "observe": "read the view after every durable write",
}
# verdict -> (is a PASS?, one-line meaning). Drives the count-table tags and grouping.
_VERDICT_MEANING = {
    "HEAL": (True, "resume healed the table"),
    "FALSE_SUCCESS": (False, "reported DONE while rows were missing/stale"),
    "NOFIRE": (True, "fault point not on this write path"),
    "KNOWN_STALE": (True, "oracle invalid (chunker + in-place update), skipped"),
    "CLEAN_READS": (True, "no placeholder visible at any write boundary"),
    "EXPOSED": (False, "a mid-refresh reader saw placeholder NULL rows"),
    "DIVERGE_GAP": (False, "reported success, left NULL rows -- SILENT DATA LOSS"),
    "DIVERGE_VALUE": (False, "reported success, left wrong values -- SILENT CORRUPT"),
    "STUCK": (False, "resume crashed and the gap never heals"),
    "WEDGE": (False, "the job hung until the case timeout killed it"),
    "CORRUPT": (False, "left the table unreadable"),
    "CORRUPT_FALSE_SUCCESS": (False, "reported success, left the table UNREADABLE"),
    "NEW@init": (False, "baseline diverged before any fault (harness bug)"),
}


def _verdict_meaning(verdict: str) -> tuple[bool, str]:
    if verdict.startswith("CASE_CRASH"):
        return False, "the harness itself crashed running the case"
    return _VERDICT_MEANING.get(verdict, (False, "unclassified verdict"))


def _describe_case(flavor: str, seq: tuple, fault: tuple) -> str:
    """One line telling the whole story: the op sequence, where in it the fault fired,
    and which durable write was hit and how. The verdict is the group header."""
    target, mode, occ = fault
    *clean, hit = seq
    hitop = _OP_DESC.get(hit, hit)
    if clean:
        prior = ", ".join(_OP_DESC.get(o, o) for o in clean)
        stage = f"after [{prior}], while materializing the {hitop}"
    else:
        stage = f"while materializing the {hitop}"
    when = "on every occurrence" if occ == "all" else f"on occurrence {occ}"
    return (
        f"{_FLAVOR_DESC.get(flavor, flavor)}: {stage}, "
        f"{_TARGET_DESC.get(target, target)} {_MODE_DESC.get(mode, mode)} ({when})"
    )


def _case_key(flavor: str, seq: tuple, fault: tuple) -> str:
    """The terse grep-able key (the old grammar), kept for reproducing one case."""
    return f"{flavor}-{''.join(seq)}-{fault[0]}:{fault[1]}@{fault[2]}"


def _shrink(recs: list[tuple]) -> list[tuple[tuple, int]]:
    """Collapse each distinct bug onto its minimal failing case.

    The fault fires while materializing a sequence's FINAL op; the prefix ops only
    build prior state. Findings that share (flavor, fault, final op) within one
    verdict are the same bug reached through different prefixes, so report the
    shortest-prefix instance (the sweep enumerates lengths bottom-up, so the minimal
    case is always in the same run) and fold the rest into a variant count. No
    re-execution: this is pure post-processing over the run's own results. Returns
    ``[(record, n_longer_variants)]`` sorted by case key.
    """
    by_bug: dict[tuple, list[tuple]] = {}
    for rec in recs:
        _v, flavor, seq, fault = rec
        by_bug.setdefault((flavor, fault, seq[-1]), []).append(rec)
    shrunk: list[tuple[tuple, int]] = []
    for variants in by_bug.values():
        variants.sort(key=lambda r: (len(r[2]), r[2]))
        shrunk.append((variants[0], len(variants) - 1))
    shrunk.sort(key=lambda t: _case_key(t[0][1], t[0][2], t[0][3]))
    return shrunk


def _init_worker() -> None:
    """Silence a pool worker's stderr so lance's Rust-side warnings (e.g. the
    per-commit DataReplacement stability notice, which no log-level setting gates) do
    not swamp the driver's progress line and summary. Python-side noise is already
    off (logging.disable); exceptions are classified in-process, not printed. Set
    ``GENEVA_FAULTSWEEP_WORKER_STDERR=1`` to keep worker stderr for debugging."""
    if os.environ.get("GENEVA_FAULTSWEEP_WORKER_STDERR") == "1":
        return
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 2)
    os.close(devnull)


def _process_batch(
    batch: list[tuple],
) -> tuple[dict[str, int], list[tuple], list[tuple]]:
    """Run (flavor, seq, fault) cases, each in its own tempdir; returns
    (verdict_counts, hard_findings, soft_findings). Each finding is a raw
    ``(verdict, flavor, seq, fault)`` record the summary renders in English."""
    counts: dict[str, int] = {}
    findings: list[tuple] = []
    soft: list[tuple] = []
    signal.signal(signal.SIGALRM, _on_case_timeout)
    with Connection.local_ray_context():  # no-op under the shim
        for i, (flavor, seq, fault) in enumerate(batch):
            name = f"{flavor[:6]}_{i}"
            tmp = tempfile.mkdtemp(prefix="faultsweep_")
            signal.alarm(_CASE_TIMEOUT_S)
            try:
                v = _run_case(connect(tmp), name, flavor, seq, fault)
            except _CaseWedgeError:
                v = "WEDGE"
            except Exception as ex:  # noqa: BLE001
                v = f"CASE_CRASH:{type(ex).__name__}"
            finally:
                signal.alarm(0)
                shutil.rmtree(tmp, ignore_errors=True)
            counts[v] = counts.get(v, 0) + 1
            rec = (v, flavor, seq, fault)
            if v in _FINDINGS or v.startswith("CASE_CRASH"):
                findings.append(rec)
            elif v in _SOFT:
                soft.append(rec)
    return counts, findings, soft


def main() -> int:
    max_len = int(os.environ.get("GENEVA_FAULTSWEEP_MAXLEN", "2"))
    workers = int(os.environ.get("SWEEP_WORKERS", str(min(8, os.cpu_count() or 2))))
    batch_size = int(os.environ.get("SWEEP_BATCH", "12"))
    only = os.environ.get("GENEVA_FAULTSWEEP_FLAVORS")
    flavors = only.split(",") if only else list(FLAVORS)

    seqs: list[tuple] = []
    for length in range(1, max_len + 1):
        seqs.extend(itertools.product(OPS, repeat=length))

    cases: list[tuple] = []
    for flavor in flavors:
        # backfill-skip runs actordeath only; boundary faults duplicate backfill.
        faults = (
            [f for f in FAULTS if f[0] == "actordeath"]
            if flavor == "backfill-skip"
            else FAULTS
        )
        # drop faults whose target cannot reach this flavor (see _FAULT_FLAVORS)
        faults = [f for f in faults if flavor in _FAULT_FLAVORS.get(f[0], _ALL_FLAVORS)]
        cases.extend((flavor, seq, fault) for seq in seqs for fault in faults)

    batches = [cases[i : i + batch_size] for i in range(0, len(cases), batch_size)]
    counts: dict[str, int] = {}
    findings: list[tuple] = []
    soft: list[tuple] = []
    t0 = time.monotonic()
    done = 0
    next_pct = 10
    live = sys.stderr.isatty()
    with mp.Pool(workers, _init_worker, maxtasksperchild=4) as pool:
        for c, f, s in pool.imap_unordered(_process_batch, batches):
            for k, v in c.items():
                counts[k] = counts.get(k, 0) + v
            findings.extend(f)
            soft.extend(s)
            # progress on the driver's stderr (workers' stderr is silenced): a live
            # rewritten line on a tty, one line per 10% otherwise (CI logs).
            done += sum(c.values())
            n_found = len(findings) + len(soft)
            msg = (
                f"swept {done}/{len(cases)} cases | "
                f"{n_found} finding(s) | {int(time.monotonic() - t0)}s"
            )
            if live:
                print(f"\r  {msg}", end="", file=sys.stderr, flush=True)
            elif done * 100 >= next_pct * len(cases):
                print(f"  {msg}", file=sys.stderr, flush=True)
                next_pct += 10
    if live:
        print(file=sys.stderr)

    # silent failures (readable-but-wrong) + case crashes; loud = crash/unreadable
    n_silent = sum(counts.get(k, 0) for k in _FINDINGS) + sum(
        v for k, v in counts.items() if k.startswith("CASE_CRASH")
    )
    n_loud = sum(counts.get(k, 0) for k in _SOFT)
    n_fail = n_silent + n_loud
    elapsed = time.monotonic() - t0
    print(
        f"=== fault sweep: {len(cases)} cases | {len(flavors)} flavors x "
        f"{len(FAULTS)} faults | L<={max_len} | {workers} workers ==="
    )
    print(
        f"completed in {elapsed:.0f}s ({len(cases) / max(elapsed, 1e-9):.1f} cases/s)"
    )

    # count table: pass verdicts first, then failing ones (adjacent to the detail),
    # each tagged ok/FAIL with a plain-English meaning.
    print("\nverdicts (ok = expected outcome, FAIL = a durability bug):")
    for verdict in sorted(counts, key=lambda k: (not _verdict_meaning(k)[0], k)):
        ok, meaning = _verdict_meaning(verdict)
        tag = "ok  " if ok else "FAIL"
        print(f"  {tag}  {verdict:<22}{counts[verdict]:>4}  {meaning}")

    # failing cases, grouped by verdict, rendered as "fault injected -> outcome".
    fails = soft + findings
    if fails:
        print("\nfailing cases (fault injected -> what went wrong; shrunk to the")
        print("shortest-prefix instance of each distinct (flavor, fault, final-op)):")
        grouped: dict[str, list[tuple]] = {}
        for rec in fails:
            grouped.setdefault(rec[0], []).append(rec)
        for verdict in sorted(grouped, key=lambda k: (not _verdict_meaning(k)[0], k)):
            recs = grouped[verdict]
            _, meaning = _verdict_meaning(verdict)
            shrunk = _shrink(recs)
            print(f"\n  {verdict} x{len(recs)} -- {meaning}")
            for rec, extra in shrunk[:50]:
                _v, flavor, seq, fault = rec
                desc = _describe_case(flavor, seq, fault)
                more = f"  (+{extra} longer-prefix variants)" if extra else ""
                print(f"    {desc:<58} [{_case_key(flavor, seq, fault)}]{more}")
            if len(shrunk) > 50:
                print(f"    ... (+{len(shrunk) - 50} more)")

    if n_fail:
        print(
            f"\nFAIL: {n_fail}/{len(cases)} cases neither healed nor failed cleanly "
            f"({n_loud} loud, {n_silent} silent/crash)."
        )
    else:
        print(
            f"\nPASS: all {len(cases)} cases healed on resume or failed loudly and "
            "cleanly (no CORRUPT / STUCK / DIVERGE)."
        )
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
