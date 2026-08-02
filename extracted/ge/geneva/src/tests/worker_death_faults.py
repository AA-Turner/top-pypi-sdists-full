# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Shim-backed worker-death fault scenarios for the backfill pipeline -- no Ray
cluster, sub-second. Run one per process: ``worker_death_faults.py <scenario>``;
``test_worker_death_fault_injection`` runs each as a subprocess. Each exits 0 iff
its invariant held.

Two fault mechanisms: boundary faults swap the global committer/table-writer/checkpoint
for a flaky one to fabricate the durable state a death might leave; faithful actor death
(``ray_shim.using_actor_death``) kills the applier actor so the task surfaces as a
``RayActorError``, driving geneva's real death path (ActorPool -> ``ActorPoolTaskError``
-> ``_handle_fatal_task_failure``) which the boundary faults cannot reach.

Like ``mv_differential_sweep.py`` this monkeypatches ``ray`` before importing geneva.
Each scenario asserts the CORRECT invariant (exit 0 == geneva fails loud or leaves no
silent loss; non-zero == bug present); not-yet-fixed bugs exit non-zero and their pytest
cases are marked ``xfail(strict=True)`` so a fix surfaces as XPASS.
"""

# ruff: noqa: T201 -- CLI script; print() is the intended output

import json
import shutil
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ray_shim  # noqa: E402

ray_shim.install()  # MUST precede the geneva import below

import lance  # noqa: E402
import pyarrow as pa  # noqa: E402
from geneva_faults import (  # noqa: E402
    CheckpointFaultPolicy,
    FlakyCommitter,
    FlakyFragmentFileWriter,
    FlakyTableWriter,
    InterleavingCommitter,
    by_op_name,
    flaky_checkpoint_wrap,
)

from geneva import connect, udf  # noqa: E402
from geneva.checkpoint import using_checkpoint_store_wrap  # noqa: E402
from geneva.committer import using_committer  # noqa: E402
from geneva.db import Connection  # noqa: E402
from geneva.debug.error_store import skip_on_error  # noqa: E402
from geneva.fragment_writer import using_fragment_file_writer  # noqa: E402
from geneva.table import Table  # noqa: E402
from geneva.table_writer import LanceTableWriter, using_table_writer  # noqa: E402

ray_shim.stub_geneva_cluster_polling()

# Per-fragment data commits are DataReplacement; the completion marker is a Transaction.
# Matching DataReplacement targets the data commits, not the marker.
_FRAGMENT_COMMIT = by_op_name("DataReplacement")

# Transaction property stamping job completion. The lance-agent reads it to advance the
# column's completed_iteration and stop re-dispatching, so if it lands while data was
# lost the loss is persistent.
_MARKER_KEY = "lancedb:agent:completed_job_json"


def _completion_marker(source: Table) -> dict | None:
    """Decoded ``completed_job_json`` payload from any committed version's transaction
    properties, else None. Reads durably, the way the lance-agent scans it."""
    ds = source.to_lance()
    for v in ds.versions():
        txn = ds.read_transaction(v["version"])
        props = getattr(txn, "transaction_properties", None) if txn else None
        if props and _MARKER_KEY in props:
            return json.loads(props[_MARKER_KEY])
    return None


@udf(data_type=pa.int64())
def _double(value: int) -> int:
    return value * 2


@udf(data_type=pa.int64(), version="v2")
def _triple(value: int) -> int:
    return value * 3


def _initial() -> pa.Table:
    return pa.table({"id": [1, 2, 3, 4], "value": [10, 20, 30, 40]})


def _block(n: int) -> pa.Table:
    base = 100 * (n + 1)
    ids = [base, base + 1, base + 2]
    return pa.table({"id": ids, "value": [i * 10 for i in ids]})


def _make_source(db: Connection) -> Table:
    # 3 fragments so a per-fragment fault touches one and leaves the rest as a control.
    source = db.create_table(
        "s", _initial(), storage_options={"new_table_enable_stable_row_ids": "true"}
    )
    source.add(_block(0))
    source.add(_block(1))
    source.add_columns({"doubled": _double})
    return source


def _rows(source: Table) -> list[tuple]:
    t = source.to_arrow()
    z = zip(
        t["id"].to_pylist(),
        t["value"].to_pylist(),
        t["doubled"].to_pylist(),
        strict=True,
    )
    return sorted(z, key=lambda r: r[0])


def _backfill(source: Table) -> None:
    # commit_granularity=1 -> one commit per fragment, so a faulted commit costs one
    # fragment, not the whole batch.
    source.backfill(
        "doubled", where="1=1", commit_granularity=1, _admission_check=False
    )


def _nulls(rows: list[tuple]) -> list[tuple]:
    return [r for r in rows if r[2] is None]


def scenario_marker_after_dropped_commit() -> int:
    """A real fragment-writer death strands the fragment's data file, geneva's
    graceful-degradation path swallows the RayError to a success, and the completion
    marker then lands durably: the agent advances completed_iteration and never
    re-dispatches -- the NULL gap is PERMANENT. Asserts the persistence precondition
    that the immediate false-success test does not: marker present AND rows NULL.

    Uses a writer death, not a committer drop, because LanceDataset.commit is atomic on
    the object-store path (it lands the manifest or raises); a commit that returns
    success without writing is not reachable. The reachable way to strand a fragment
    while the job proceeds to commit the marker is a swallowed write failure."""
    tmp = tempfile.mkdtemp(prefix="wd_marker_")
    try:
        db = connect(tmp)
        source = _make_source(db)

        # A real fragment-writer death: the file is never written, cleanup degrades it
        # to a WARNING + success, and the completion marker (a separate Transaction)
        # commits normally after the missing fragment.
        flaky = FlakyFragmentFileWriter(raise_at={1})
        raised: Exception | None = None
        with using_fragment_file_writer(flaky):
            try:
                _backfill(source)
            except Exception as e:  # noqa: BLE001 -- we WANT to know if it raised
                raised = e

        rows = _rows(source)
        gap = _nulls(rows)
        marker = _completion_marker(source)
        outcome = f"raised {type(raised).__name__}" if raised else "reported success"
        print(f"writes seen  : {flaky.calls}   raised: {flaky.raised}")
        print(f"null gap     : {len(gap)} of {len(rows)} -> {[r[0] for r in gap]}")
        print(f"backfill     : {outcome}")
        print(f"marker       : {marker}")

        if not flaky.raised:
            print("INCONCLUSIVE: no fragment write was faulted (no wrapped write hit).")
            return 1
        if raised is not None:
            print(
                f"PASS: the fragment-writer death failed LOUD "
                f"({type(raised).__name__}) -- not a silent success."
            )
            return 0
        if not gap:
            print("PASS: the dropped commit left no NULL gap (healed / no-op).")
            return 0
        if marker is None:
            print(
                "PASS: no completion marker was committed -- the agent re-dispatches, "
                "so the gap is recoverable (not persistent)."
            )
            return 0
        print(
            f"\nFAIL (bug present): the completion marker landed (completed_job_json "
            f"for column {marker.get('column_name')!r}) while {len(gap)} of "
            f"{len(rows)} rows are silently NULL. The lance-agent reads this marker, "
            f"advances completed_iteration, never re-dispatches -- gap is PERSISTENT."
        )
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_resume_heals() -> int:
    """Die on the first fragment commit (checkpoint already durable), then resume with
    a fresh backfill: the resume must complete every row (no orphaned NULLs)."""
    tmp = tempfile.mkdtemp(prefix="wd_resume_heals_")
    try:
        db = connect(tmp)
        source = _make_source(db)

        flaky = FlakyCommitter(raise_at={1}, match=_FRAGMENT_COMMIT)
        died: Exception | None = None
        with using_committer(flaky):
            try:
                _backfill(source)
            except Exception as e:  # noqa: BLE001 -- the death we injected
                died = e
        after_death = _rows(source)
        attempt1 = f"died {type(died).__name__}" if died else "RETURNED"
        print(f"commits seen : {flaky.calls}   raised: {flaky.raised}")
        print(f"attempt 1    : {attempt1}")
        print(f"after death  : {len(_nulls(after_death))} of {len(after_death)} null")

        if not flaky.raised:
            print("FAIL: no commit raised -- the committer was not exercised.")
            return 1
        if died is None or "injected worker death" not in str(died):
            print(
                "FAIL: attempt 1 did not die from the injected fault "
                f"(got {died!r}); the committer death did not kill the job."
            )
            return 1

        # Resume: a fresh backfill with the default committer should find the durable
        # checkpoint + orphaned fragment file and finish the job.
        _backfill(source)
        rows = _rows(source)
        gap = _nulls(rows)
        print(f"after resume : {len(gap)} of {len(rows)} null")
        print(f"rows         : {rows}")

        if gap:
            print(
                f"REGRESSION: resume left {len(gap)} of {len(rows)} rows NULL "
                f"-> {[r[0] for r in gap]} -- checkpoint resume did not heal the "
                "interrupted job."
            )
            return 1
        print(
            "\nHELD: worker died at the fragment commit; a fresh backfill resumed and "
            "completed every row."
        )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_mv_refresh_lost_append() -> int:
    """Drop the MV refresh's row-landing append (Table.add of placeholder rows): the
    refresh must NOT report success while leaving the view silently incomplete. Faults
    the Table.add -> _ltbl.add write layer, which the committer cannot reach."""
    tmp = tempfile.mkdtemp(prefix="wd_mv_refresh_")
    try:
        db = connect(tmp)
        src = db.create_table(
            "s", _initial(), storage_options={"new_table_enable_stable_row_ids": "true"}
        )
        mv = src.search(None).select(["id", "value"]).create_materialized_view(db, "m")
        mv.refresh(_admission_check=False)  # populate (4 rows)
        src.add(_block(0))
        src.add(_block(1))  # +6 rows the next refresh must land

        flaky = FlakyTableWriter(ops={"add"}, drop_at={1})
        raised: Exception | None = None
        with using_table_writer(flaky):
            try:
                mv.refresh(_admission_check=False)
            except Exception as e:  # noqa: BLE001 -- we WANT to know if it raised
                raised = e
        src_rows = src.count_rows()
        mv_rows = mv.to_arrow().num_rows
        outcome = f"raised {type(raised).__name__}" if raised else "reported success"
        print(f"adds seen    : {flaky.calls}   dropped: {flaky.dropped}")
        print(f"refresh      : {outcome}")
        print(f"MV rows      : {mv_rows} / source {src_rows}")

        if not flaky.dropped:
            print("INCONCLUSIVE: no add was dropped -- the table writer was not run.")
            return 1
        if raised is not None:
            print(
                f"PASS: the lost append failed LOUD ({type(raised).__name__}) -- the "
                "refresh did not silently report success."
            )
            return 0
        if mv_rows >= src_rows:
            print(f"PASS: the MV is complete ({mv_rows}/{src_rows}) -- no lost append.")
            return 0

        # False success is transient here -- a later clean refresh self-heals (the
        # source watermark was not advanced past the lost rows) -- but reporting
        # success while incomplete still violates the invariant.
        mv.refresh(_admission_check=False)
        healed = mv.to_arrow().num_rows
        print(f"after resume : MV {healed} / {src_rows}")
        print(
            f"\nFAIL (bug present): refresh reported success but the MV held {mv_rows} "
            f"of {src_rows} rows (missing {src_rows - mv_rows}); a later refresh "
            f"healed to {healed} (transient -- false success, self-correcting)."
        )
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_mv_refresh_exposes_placeholders() -> int:
    """A healthy MV refresh is not atomic to a reader: it commits placeholder rows
    (view columns NULL, ``__is_set=False``) at an intermediate version, then fills them
    with a later ``DataReplacement``. ``__is_set`` is written False but never flipped on
    fill and never filtered on read, so a reader at the intermediate version cannot tell
    placeholder NULLs from genuine ones. No fault injected: captures the post-append
    version and reads the MV there. Transient -- a serving-consistency gap, not loss."""
    tmp = tempfile.mkdtemp(prefix="wd_mv_placeholder_")
    try:
        db = connect(tmp)
        src = db.create_table(
            "s", _initial(), storage_options={"new_table_enable_stable_row_ids": "true"}
        )
        mv = src.search(None).select(["id", "value"]).create_materialized_view(db, "m")
        mv.refresh(_admission_check=False)  # populate 4
        src.add(_block(0))  # +3 rows the next refresh must land

        # Pass-through writer that records the post-add version of m.lance.
        captured: dict[str, object] = {}

        class _CaptureWriter(LanceTableWriter):
            def add(self, ltbl: object, *a: object, **k: object) -> object:
                r = super().add(ltbl, *a, **k)
                uri = str(getattr(ltbl, "uri", "") or "")
                if "m.lance" in uri:
                    captured["uri"] = uri
                    captured["version"] = lance.dataset(uri).version
                return r

        with using_table_writer(_CaptureWriter()):
            mv.refresh(_admission_check=False)

        uri = captured.get("uri")
        mid_version = captured.get("version")
        if not isinstance(uri, str) or not isinstance(mid_version, int):
            print("INCONCLUSIVE: never captured the placeholder-append version.")
            return 1

        final = lance.dataset(uri)
        mid = lance.dataset(uri, version=mid_version)
        mt = mid.to_table()
        ft = final.to_table()
        mid_ids = mt["id"].to_pylist()
        mid_isset = mt["__is_set"].to_pylist()
        final_ids = ft["id"].to_pylist()
        final_isset = ft["__is_set"].to_pylist()
        leaked = [i for i, v in enumerate(mid_ids) if v is None]

        print(f"versions     : placeholder@{mid_version} -> final@{final.version}")
        print(f"mid   id     : {mid_ids}")
        print(f"mid   __is_set: {mid_isset}")
        print(f"final id     : {final_ids}")
        print(f"final __is_set: {final_isset}")
        print(f"leaked NULL view rows @ mid: {len(leaked)} of {mt.num_rows}")

        if mid_version >= final.version:
            print("PASS: no separate intermediate version -- the refresh is atomic.")
            return 0
        if not leaked:
            print("PASS: the intermediate version exposes no NULL placeholders.")
            return 0
        if any(v is None for v in final_ids):
            print(
                "FAIL (worse bug): the FINAL version still has NULL view rows -- not "
                "even transient (persistent placeholder loss)."
            )
            return 1
        # __is_set never True at either version, so a reader cannot use it to exclude
        # placeholders.
        if any(mid_isset) or any(final_isset):
            print(
                "PASS: __is_set is True somewhere -- a reader can use it to exclude "
                "placeholders (a usable gate)."
            )
            return 0
        print(
            f"\nFAIL (bug present): a healthy refresh exposed {len(leaked)} "
            f"placeholder rows with NULL view columns at intermediate version "
            f"{mid_version}; __is_set is uniformly False (never flipped, never "
            f"filtered), so a reader has no signal to exclude them. Final version "
            f"{final.version} is complete."
        )
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_graceful_degradation_false_success() -> int:
    """Fail one fragment's data-file WRITE (inside the writer actor), not a commit: the
    backfill must NOT report success while that fragment's rows stay NULL. Exercises the
    graceful-degradation path -- a writer failure surfaces as a ``RayError`` and
    ``cleanup`` logs a warning and returns success, reporting the job clean with a
    fragment missing. PASSES when cleanup fails the job instead of degrading."""
    tmp = tempfile.mkdtemp(prefix="wd_graceful_degradation_")
    try:
        db = connect(tmp)
        source = _make_source(db)

        flaky = FlakyFragmentFileWriter(raise_at={1})
        raised: Exception | None = None
        with using_fragment_file_writer(flaky):
            try:
                _backfill(source)
            except Exception as e:  # noqa: BLE001 -- we WANT to know if it raised
                raised = e

        rows = _rows(source)
        gap = _nulls(rows)
        outcome = f"raised {type(raised).__name__}" if raised else "reported success"
        print(f"writes seen  : {flaky.calls}   raised: {flaky.raised}")
        print(f"null gap     : {len(gap)} of {len(rows)} -> {[r[0] for r in gap]}")
        print(f"backfill     : {outcome}")
        print(f"rows         : {rows}")

        if not flaky.raised:
            print("INCONCLUSIVE: no fragment write was faulted (no wrapped write hit).")
            return 1
        if raised is not None:
            print(
                f"PASS: the fragment-write failure surfaced LOUD "
                f"({type(raised).__name__}) -- cleanup fails the job, not degrades it."
            )
            return 0
        if not gap:
            print("PASS: the fragment-write failure left no NULL gap (healed / no-op).")
            return 0
        print(
            f"\nFAIL (bug present): a fragment write failed; the backfill reported "
            f"success but {len(gap)} of {len(rows)} rows are silently NULL (graceful "
            f"degradation)."
        )
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_checkpoint_loss_recovers() -> int:
    """Drop a per-batch checkpoint WRITE (the dedupe/recovery store): a lost checkpoint
    must NOT become a silent false success. Expected to be recovery-robust -- the job
    fails loud (missing checkpoint caught on read-back) rather than committing NULLs,
    and a resume heals the column. Contrast ``graceful-degradation``, where a stranded
    fragment is a silent NULL gap."""
    tmp = tempfile.mkdtemp(prefix="wd_ckpt_loss_")
    try:
        db = connect(tmp)
        source = _make_source(db)

        policy = CheckpointFaultPolicy(ops={"set"}, drop_at={2})
        raised: Exception | None = None
        with using_checkpoint_store_wrap(flaky_checkpoint_wrap(policy)):
            try:
                _backfill(source)
            except Exception as e:  # noqa: BLE001 -- loud failure is the expected path
                raised = e

        rows1 = _rows(source)
        gap1 = _nulls(rows1)
        outcome = f"raised {type(raised).__name__}" if raised else "reported success"
        print(f"ckpt set drops: {policy.dropped}")
        print(f"attempt 1     : {outcome}; nulls {len(gap1)} of {len(rows1)}")

        if not policy.dropped:
            print("FAIL: no checkpoint write was dropped -- write not exercised.")
            return 1
        # Guard: a clean success that silently left NULLs.
        if raised is None and gap1:
            print(
                f"BUG: backfill reported success but left {len(gap1)} of {len(rows1)} "
                f"rows NULL after a dropped checkpoint write -> {[r[0] for r in gap1]}"
            )
            return 1

        # Resume with the default store: the column must complete.
        _backfill(source)
        gap2 = _nulls(_rows(source))
        print(f"after resume  : {len(gap2)} null")
        if gap2:
            print(f"REGRESSION: resume left {len(gap2)} NULL -> {[r[0] for r in gap2]}")
            return 1
        print(
            "\nHELD: a lost checkpoint write was loud + recoverable (not a silent "
            "false success); the resume completed every row."
        )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_schema_change_recomputes() -> int:
    """Schema change: dropping a materialized column and re-adding it with a DIFFERENT
    UDF must recompute the whole column, never reuse the prior UDF's checkpointed
    values. The guard is the per-fragment output-field-id check (apply/utils.py); a
    regression would silently keep the OLD value*2. Asserts the held invariant -- the
    column recomputes to value*3 everywhere."""
    tmp = tempfile.mkdtemp(prefix="wd_schema_change_")
    try:
        db = connect(tmp)
        source = _make_source(db)
        _backfill(source)  # all rows -> value*2
        before = _rows(source)
        if any(d != v * 2 for (_i, v, d) in before):
            print(f"FAIL: baseline backfill is not value*2: {before}")
            return 1

        # Drop the column, re-add with a new udf (value*3).
        source.drop_columns(["doubled"])
        source.add_columns({"doubled": _triple})
        source.backfill("doubled", where="1=1", _admission_check=False)

        rows = _rows(source)
        stale = [(i, d) for (i, v, d) in rows if d != v * 3]
        print(f"rows after re-add+backfill: {rows}")
        print(f"stale (not value*3)      : {stale}")
        if stale:
            print(
                f"BUG: {len(stale)} row(s) kept a stale value after the column's UDF "
                f"changed (checkpoint reused across a definition change) -> {stale}"
            )
            return 1
        print(
            "\nHELD: dropping + re-adding the column with a new UDF recomputed every "
            "row to value*3 -- the prior UDF's checkpoints were correctly invalidated."
        )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_source_change_not_silently_stale() -> int:
    """Source change: after a row's SOURCE value is updated in place, re-running the
    backfill must recompute that row's derived column or fail loudly -- never report
    success while leaving the derived value stale. The hazard is stale-skipping the
    changed row (the ``srcfiles_hash`` mismatch check only hashes ``fragments[0]``).
    Recompute OR raise pass; only a silent stale is a failure."""
    tmp = tempfile.mkdtemp(prefix="wd_source_change_")
    try:
        db = connect(tmp)
        source = _make_source(db)
        _backfill(source)  # all rows -> value*2
        # id=201 lives in a later fragment (not fragments[0]).
        target, new_value = 201, 9999
        source.update(where=f"id = {target}", values_sql={"value": str(new_value)})

        raised: Exception | None = None
        try:
            _backfill(source)
        except Exception as e:  # noqa: BLE001 -- a loud failure satisfies the invariant
            raised = e

        rows = {i: (v, d) for (i, v, d) in _rows(source)}
        tv, td = rows[target]
        outcome = f"raised {type(raised).__name__}" if raised else "reported success"
        print(f"re-backfill  : {outcome}")
        print(f"id={target}      : value={tv} doubled={td} (fresh would be {tv * 2})")

        if tv != new_value:
            print(f"FAIL: source update did not apply (value={tv}).")
            return 1
        # Only violation: a silent success that left the derived value stale.
        if raised is None and td != tv * 2:
            print(
                f"BUG: re-backfill reported success but left id={target} doubled={td} "
                f"stale (source value is now {tv}; fresh would be {tv * 2})."
            )
            return 1
        if raised is not None:
            print(
                "\nHELD: a re-backfill after an in-place source change failed LOUD "
                "(commit conflict) rather than silently keeping a stale value. "
                "(Loud rough edge -- confirm the conflict behavior on real Ray.)"
            )
        else:
            print(
                f"\nHELD: the re-backfill recomputed id={target} to {td} after its "
                "source value changed."
            )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_repair_resume_noop() -> int:
    """Filtered repair (re-backfill of an ALREADY-COMMITTED column with where=<subset>)
    that dies after writing per-range checkpoints but before committing its
    DataReplacement must NOT silently no-op on resume.

    Run 1 recomputes the matched row and writes per-range checkpoints, but the worker
    dies at the fragment file write, before the fragment is recorded and committed, so
    nothing lands and the per-range checkpoints survive with no fragment dedupe marker.
    Run 2 (same udf version, clean) sees full per-range coverage for the fragment AND a
    pre-existing output data file (the baseline column), concludes the fragment is done,
    emits zero tasks, commits nothing, and reports success -- while the target row keeps
    its stale pre-repair value.

    The death is modelled at the fragment file write rather than the commit: the writer
    records the fragment dedupe marker and purges the per-range checkpoints before the
    commit, so merely dropping the commit leaves a correctly-invalidated dedupe marker
    and does not reach the skip. A whole-fragment source update keeps the matched rows
    co-located in one multi-row fragment, and task_size=1 forces per-range checkpoints
    (several tasks per fragment) instead of a single whole-fragment direct write that
    would write a dedupe marker.

    The invariant: after resume the repaired value is correct OR the resume failed loud.
    A silent no-op (success + stale) with zero commit work on resume is the bug."""
    tmp = tempfile.mkdtemp(prefix="wd_repair_resume_noop_")
    try:
        db = connect(tmp)
        n = 6
        ids = list(range(1, n + 1))
        source = db.create_table(
            "s",
            pa.table({"id": ids, "value": [i * 10 for i in ids]}),
            storage_options={"new_table_enable_stable_row_ids": "true"},
        )
        source.add_columns({"doubled": _double})
        source.backfill(
            "doubled", where="1=1", commit_granularity=1, _admission_check=False
        )
        before = {i: (v, d) for (i, v, d) in _rows(source)}
        if any(d != v * 2 for (v, d) in before.values()):
            print(f"INCONCLUSIVE: baseline backfill is not value*2: {before}")
            return 1

        # Change every row's source value so the committed doubled is now stale
        # (carried forward, not recomputed by update). Updating the whole fragment
        # keeps the rows co-located in one multi-row fragment.
        target, new_value = 1, 999
        source.update(where=f"id <= {n}", values_sql={"value": str(new_value)})
        stale = {i: d for (i, v, d) in _rows(source)}[target]
        correct = new_value * 2
        if stale == correct:
            print(f"INCONCLUSIVE: id={target} was not left stale after update: {stale}")
            return 1

        # Run 1: filtered repair whose fragment file write dies AFTER the per-range
        # checkpoints are written but BEFORE the fragment is recorded/committed.
        fw = FlakyFragmentFileWriter(raise_at={1})
        raised1: Exception | None = None
        with using_fragment_file_writer(fw):
            try:
                source.backfill(
                    "doubled",
                    where=f"id = {target}",
                    task_size=1,
                    commit_granularity=1,
                    _admission_check=False,
                )
            except Exception as e:  # noqa: BLE001 -- record whether run 1 raised
                raised1 = e
        after1 = {i: d for (i, v, d) in _rows(source)}[target]
        run1 = f"raised {type(raised1).__name__}" if raised1 else "reported success"
        print(f"run 1        : {run1}; fragment-file writes raised {fw.raised}")
        print(f"after run 1  : id={target} doubled={after1} (stale={stale})")

        if not fw.raised:
            print(
                "INCONCLUSIVE: run 1 faulted no fragment-file write -- the repair took "
                "the whole-fragment direct-write path or ran no task, so the "
                "checkpoint-then-stranded-write state was never created."
            )
            return 1
        if after1 != stale:
            print(
                f"INCONCLUSIVE: run 1 changed id={target} to {after1} despite the "
                "faulted write -- the stranded-write state was not established."
            )
            return 1

        # Run 2: resume the SAME filtered repair, clean. Count DataReplacement commits
        # to confirm whether the planner emitted any work.
        flaky2 = FlakyCommitter(match=_FRAGMENT_COMMIT)
        raised2: Exception | None = None
        with using_committer(flaky2):
            try:
                source.backfill(
                    "doubled",
                    where=f"id = {target}",
                    task_size=1,
                    commit_granularity=1,
                    _admission_check=False,
                )
            except Exception as e:  # noqa: BLE001 -- a loud failure satisfies invariant
                raised2 = e
        after2 = {i: d for (i, v, d) in _rows(source)}[target]
        run2 = f"raised {type(raised2).__name__}" if raised2 else "reported success"
        print(f"run 2        : {run2}; DataReplacement commits {flaky2.calls}")
        print(f"after resume : id={target} doubled={after2} (correct={correct})")

        if raised2 is not None:
            print(
                f"PASS: the resume failed LOUD ({type(raised2).__name__}) rather than "
                "silently no-op'ing the interrupted repair."
            )
            return 0
        if after2 == correct:
            print(
                f"PASS: the resume recomputed id={target} to {after2} -- the "
                "interrupted repair was completed."
            )
            return 0
        if flaky2.calls > 0:
            print(
                f"INCONCLUSIVE: the resume attempted {flaky2.calls} commit(s) but left "
                f"id={target} doubled={after2} (want {correct}) -- a divergence other "
                "than the planner no-op; not the targeted bug."
            )
            return 1
        print(
            f"\nFAIL (bug present): the clean resume reported success, committed "
            f"nothing ({flaky2.calls} DataReplacement), and left id={target} "
            f"doubled={after2} STALE (correct is {correct}). Full per-range checkpoint "
            f"coverage plus the pre-existing output data file made the planner skip "
            f"the fragment as done, so the interrupted repair silently no-op'd."
        )
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- faithful worker death (shim-level actor kill, not a fabricated commit/short) ---
# These kill the applier actor the way real Ray does: the in-flight task surfaces as a
# RayActorError, driving geneva's real death path (ActorPool `_get_next_by_fut` ->
# `ActorPoolTaskError` -> _handle_fatal_task_failure). The commit/fragment faults cannot
# reach it -- they raise errors not in the pool's `_ACTOR_LOSS_ERRORS`.


@udf(data_type=pa.int64(), on_error=skip_on_error(max_skip_count=0))
def _double_skip(value: int) -> int:
    return value * 2


def _make_source_skip(db: Connection) -> Table:
    """A 3-fragment source whose ``doubled`` column carries a ZERO skip budget -- any
    skipped row must fail the job (precondition for the skip-budget bypass scenario)."""
    source = db.create_table(
        "s", _initial(), storage_options={"new_table_enable_stable_row_ids": "true"}
    )
    source.add(_block(0))
    source.add(_block(1))
    source.add_columns({"doubled": _double_skip})
    return source


def scenario_applier_death_fails_loud() -> int:
    """A backfill whose applier actor dies on its first task must fail LOUD and heal on
    a clean resume -- never silently drop the dead task's rows. With no skip budget,
    `_handle_fatal_task_failure` re-raises the lost task as a `FatalWorkerExitError` and
    a clean resume must complete every row. The healthy actor-death path."""
    tmp = tempfile.mkdtemp(prefix="wd_applier_death_loud_")
    try:
        db = connect(tmp)
        source = _make_source(db)

        raised: Exception | None = None
        with ray_shim.using_actor_death("ApplierActor", "run", (1,)) as policy:
            try:
                _backfill(source)
            except Exception as e:  # noqa: BLE001 -- we WANT to know if it raised
                raised = e

        rows = _rows(source)
        gap = _nulls(rows)
        outcome = f"raised {type(raised).__name__}" if raised else "reported success"
        print(f"applier death : fired on call(s) {policy.fired}")
        print(f"faulted run   : {outcome}")
        print(f"null gap      : {len(gap)} of {len(rows)} -> {[r[0] for r in gap]}")

        if not policy.fired:
            print("FAIL: the applier death never fired -- ApplierActor.run not called.")
            return 1
        if raised is None:
            print(
                "BUG: the backfill reported SUCCESS despite a worker death -- the dead "
                f"task's rows ({[r[0] for r in gap]}) were silently dropped."
            )
            return 1

        _backfill(source)  # clean resume must heal
        gap2 = _nulls(_rows(source))
        print(f"after resume  : {len(gap2)} null -> {[r[0] for r in gap2]}")
        if gap2:
            print(f"FAIL: resume did not heal -- {len(gap2)} rows still NULL.")
            return 1
        print(
            "\nHELD: the applier death failed LOUD (FatalWorkerExitError via the real "
            "ActorPool death path) and a clean resume healed every row."
        )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_applier_death_skip_budget_bypass() -> int:
    """An applier death under ``skip_on_error(max_skip_count=0)`` must NOT report
    success -- a ZERO skip budget means any skipped row fails the job. The fatal-task
    null-checkpoint path charges ``skipped_stats['null_checkpoints']`` but never
    ``skip_tracker.record_batch``, so a worker-death NULL bypasses the budget and the
    job reports done with the dead task's rows NULL. The bug violates the invariant, so
    this exits non-zero (its pytest case is xfail)."""
    tmp = tempfile.mkdtemp(prefix="wd_applier_death_skip_")
    try:
        db = connect(tmp)
        source = _make_source_skip(db)

        raised: Exception | None = None
        with ray_shim.using_actor_death("ApplierActor", "run", (1,)) as policy:
            try:
                _backfill(source)
            except Exception as e:  # noqa: BLE001 -- we WANT to know if it raised
                raised = e

        rows = _rows(source)
        gap = _nulls(rows)
        outcome = f"raised {type(raised).__name__}" if raised else "reported success"
        print("skip budget   : max_skip_count=0 (any skip must FAIL the job)")
        print(f"applier death : fired on call(s) {policy.fired}")
        print(f"faulted run   : {outcome}")
        print(f"null gap      : {len(gap)} of {len(rows)} -> {[r[0] for r in gap]}")

        if not policy.fired:
            print("INCONCLUSIVE: the applier death never fired (no ApplierActor.run).")
            return 1
        if raised is not None:
            print(
                f"PASS: the job failed LOUD ({type(raised).__name__}) -- the zero skip "
                "budget held; the worker-death rows were not silently skipped."
            )
            return 0
        if not gap:
            print("PASS: no NULL gap -- the death healed within the run.")
            return 0
        print(
            f"\nFAIL (bug present): backfill reported SUCCESS with {len(gap)} of "
            f"{len(rows)} rows silently NULL despite a ZERO skip budget -- the "
            "worker-death null-checkpoint bypassed the skip-budget charge."
        )
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_concurrent_append_during_backfill() -> int:
    """A user append lands between the backfill's version read and its first fragment
    commit -- a deterministic concurrent-writer race (the append is injected just
    before the commit executes, so geneva's conflict handling resolves a REAL version
    bump, not synthetic error text). The invariant: every row that existed at job
    start must end up correct (by the job or by one clean resume), the table must
    stay readable, and neither run may report success with a start row wrong. Rows
    appended mid-job may legitimately stay NULL until a later run."""
    tmp = tempfile.mkdtemp(prefix="wd_concurrent_append_")
    try:
        db = connect(tmp)
        source = _make_source(db)
        start_ids = {r[0] for r in _rows(source)}

        ic = InterleavingCommitter(
            lambda: source.add(_block(2)), match=_FRAGMENT_COMMIT
        )
        raised: Exception | None = None
        with using_committer(ic):
            try:
                _backfill(source)
            except Exception as e:  # noqa: BLE001 -- record the faulted-run outcome
                raised = e

        if not ic.fired:
            print("INCONCLUSIVE: the interleaved append never fired.")
            return 1

        rows = _rows(source)  # raises if the table was left unreadable
        wrong = [r for r in rows if r[0] in start_ids and r[2] != r[1] * 2]
        new_rows = [r for r in rows if r[0] not in start_ids]
        outcome = f"raised {type(raised).__name__}" if raised else "reported success"
        print("interleave    : append committed before fragment commit #1")
        print(f"faulted run   : {outcome}")
        print(f"start rows    : {len(wrong)} of {len(start_ids)} wrong -> {wrong}")
        print(f"mid-job rows  : {[(r[0], r[2]) for r in new_rows]}")

        if raised is None and wrong:
            print(
                f"\nFAIL (bug present): the backfill reported SUCCESS with "
                f"{len(wrong)} pre-existing row(s) wrong after a concurrent append."
            )
            return 1
        if wrong:
            _backfill(source)  # failed loud: one clean resume must heal start rows
            rows = _rows(source)
            wrong = [r for r in rows if r[0] in start_ids and r[2] != r[1] * 2]
            print(f"after resume  : {len(wrong)} start row(s) wrong")
            if wrong:
                print("\nFAIL: a clean resume did not heal the pre-existing rows.")
                return 1
        print(
            "\nHELD: the concurrent append was resolved -- every pre-existing row is "
            "correct and the table stayed readable."
        )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


SCENARIOS: dict[str, Callable[[], int]] = {
    "marker-after-dropped-commit": scenario_marker_after_dropped_commit,
    "resume-heals": scenario_resume_heals,
    "mv-refresh-lost-append": scenario_mv_refresh_lost_append,
    "mv-refresh-exposes-placeholders": scenario_mv_refresh_exposes_placeholders,
    "graceful-degradation": scenario_graceful_degradation_false_success,
    "checkpoint-loss-recovers": scenario_checkpoint_loss_recovers,
    "schema-change-recomputes": scenario_schema_change_recomputes,
    "source-change-not-silently-stale": scenario_source_change_not_silently_stale,
    "repair-resume-noop": scenario_repair_resume_noop,
    "applier-death-fails-loud": scenario_applier_death_fails_loud,
    "applier-death-skip-budget-bypass": scenario_applier_death_skip_budget_bypass,
    "concurrent-append-during-backfill": scenario_concurrent_append_during_backfill,
}


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in SCENARIOS:
        print(f"usage: {argv[0]} {{{'|'.join(SCENARIOS)}}}", file=sys.stderr)
        return 2
    print(f"=== scenario: {argv[1]} ===")
    return SCENARIOS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
