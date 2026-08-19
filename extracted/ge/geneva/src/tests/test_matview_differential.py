# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Differential tests for geneva's incremental compute paths: drive a source table
through op sequences and compare each refresh/backfill against a model-free Arrow
oracle (the source recomputed), checked at every step. Covers several flavors
through one engine:

  mv-identity / mv-filtered -- projection MV ``SELECT id, value [WHERE value>50]``.
  backfill                  -- ``add_columns`` + ``backfill`` of a UDF column.
  mvbf-identity / mvbf-flt  -- a projection MV over a *backfilled* computed column.

(The ``create_udtf_view`` chunker flavor is covered by the no-cluster shim sweep in
``test_mv_differential_shim``; a module-level chunker does not deserialize in a
real-Ray worker from the test module, a packaging quirk unrelated to correctness.)

Every flavor also runs on an SRID axis: srid=True (stable row IDs, the default)
expects full oracle equality after every sync; srid=False expects a version-based
state model -- an MV refresh succeeds iff the source is still at the MV's base
version, otherwise the cross-version guard (table.py) raises client-side and must
leave the MV byte-identical to its last-good state. Backfills are rowaddr-based
and must behave identically on both sides of the axis.

Any divergence hard-fails (catches refresh bugs). GEN-619 (MV refresh nulling a
surviving row when an earlier row in the same fragment is removed) is fixed, so a
null is now a real regression, not an expected xfail. The reproducers for the
confirmed bugs are at the bottom: the GEN-619 and GEN-620 ones are passing
regression guards; GEN-621 remains strict-xfail until fixed.

The full sweep is opt-in via ``GENEVA_MVDIFF_EXHAUSTIVE=1`` (``GENEVA_MVDIFF_MAXLEN``
for depth, ``GENEVA_MVDIFF_SRID`` in {"on", "off", "both"} for the axis). The fast
no-cluster shim version runs in ``test_mv_differential_shim``.
"""

import itertools
import os
import warnings
from collections.abc import Callable
from datetime import timedelta
from typing import NamedTuple

import pyarrow as pa
import pytest

from geneva import udf
from geneva.db import Connection, dataset_uses_stable_row_ids
from geneva.table import Table

pytestmark = pytest.mark.ray


# --- op alphabet -----------------------------------------------------------
APPEND = "A"  # append a block of fresh ids (100-spaced)
DELETE = "D"  # DELETE WHERE id % 2 = 0 -> in-place deletion in surviving frags
UPDATE = "U"  # UPDATE odd ids SET value=-1 -> crosses the value>50 filter
COMPACT = "C"  # compact_files -> fragment rewrite
ADDCOL = "X"  # add an unreferenced all-null column -> must NOT corrupt the view
MOVE = "M"  # UPDATE value>50 SET value=value+1 -> in-place value change
MERGE = "I"  # merge_insert upsert: matched id crosses the filter + one fresh id
ENTER = "E"  # UPDATE value<=50 SET value=value+1000 -> moves rows INTO the filter
REINSERT = "R"  # delete id 3 + re-add it with a new value (same key, new row)
NOOP = "N"  # no source change -> the following sync pins refresh idempotence
OPTIMIZE = "O"  # optimize(cleanup_older_than=0): compaction + version cleanup

IDENTITY = "identity"  # SELECT id, value
FILTERED = "filtered"  # SELECT id, value WHERE value > 50
FILTER_EXPR = "value > 50"


@udf(data_type=pa.int64())
def _double(value: int) -> int:
    return value * 2


def _sorted(rows: list[tuple]) -> list[tuple]:
    return sorted(
        rows, key=lambda r: tuple((x is None, x if x is not None else 0) for x in r)
    )


def _initial() -> pa.Table:
    ids = [1, 2, 3, 4]
    return pa.table({"id": ids, "value": [i * 10 for i in ids]})


def _append_block(n: int) -> pa.Table:
    base = 100 * (n + 1)
    ids = [base, base + 1, base + 2]
    return pa.table({"id": ids, "value": [i * 10 for i in ids]})


def _make_source(db: Connection, name: str, srid: bool = True) -> Table:
    """Create the seed source table; ``srid`` toggles stable row IDs.

    srid=False omits ``new_table_enable_stable_row_ids`` entirely rather than
    setting it, so the table relies on the lance default. db.py normalizes
    falsy and mixed-case values as of GEN-869, so passing "false" would work
    too; omitting keeps this independent of that normalization."""
    opts = {"new_table_enable_stable_row_ids": "true"} if srid else None
    tbl = db.create_table(name, _initial(), storage_options=opts)
    if not srid:
        # Second fragment so COMPACT has real work: a pure-compaction version
        # bump is the exact hazard the srid-off refresh guard exists for, and
        # compact_files on a 1-fragment no-deletes table commits nothing.
        tbl.add(pa.table({"id": [50, 51], "value": [500, 510]}))
    assert dataset_uses_stable_row_ids(tbl.to_lance()) is srid
    return tbl


def _apply_op(source: Table, op: str, append_n: int, step: int) -> None:
    if op == APPEND:
        source.add(_append_block(append_n))
    elif op == DELETE:
        source.delete("id % 2 = 0")
    elif op == UPDATE:
        source.update(where="id % 2 = 1", values_sql={"value": "-1"})
    elif op == COMPACT:
        source.compact_files()
    elif op == ADDCOL:
        source._ltbl.add_columns({f"extra_{step}": "CAST(NULL AS BIGINT)"})
    elif op == MOVE:
        source.update(where="value > 50", values_sql={"value": "value + 1"})
    elif op == MERGE:
        # Upsert: id 1 (survives DELETE) gets a value crossing the value>50
        # boundary, plus one fresh id; values unique per step.
        block = pa.table({"id": [1, 9000 + step], "value": [500 + step, 9000 + step]})
        (
            source.merge_insert("id")
            .when_matched_update_all()
            .when_not_matched_insert_all()
            .execute(block)
        )
    elif op == ENTER:
        source.update(where="value <= 50", values_sql={"value": "value + 1000"})
    elif op == REINSERT:
        # Same user key, new row identity: the view must show the new value
        # with no ghost or duplicate.
        source.delete("id = 3")
        source.add(pa.table({"id": [3], "value": [3000 + step]}))
    elif op == NOOP:
        pass
    elif op == OPTIMIZE:
        source.optimize(cleanup_older_than=timedelta(0))
    else:  # pragma: no cover
        raise ValueError(f"unknown op {op}")


def _live(source: Table) -> list[tuple]:
    t = source.to_arrow()
    return list(zip(t["id"].to_pylist(), t["value"].to_pylist(), strict=True))


def _has_null(rows: list[tuple]) -> bool:
    return any(any(x is None for x in r) for r in rows)


def _refresh(obj: Table) -> None:
    # _admission_check=False: local Ray admission control can hang (see conftest).
    obj.refresh(_admission_check=False)


def _sync(flavor: str, source: Table, target: Table) -> None:
    """Bring the target up to date with the current source. The action differs by
    flavor: a backfilled column is re-backfilled in place (the plain ``backfill``
    flavor has no separate view, so it never calls refresh); a view is refreshed.
    The combination flavor (mvbf) does both -- backfill the source column, then
    refresh the MV that projects it."""
    if _is_backfilled(flavor):
        source.backfill("doubled", where="1=1", _admission_check=False)
    if flavor != "backfill":
        _refresh(target)


def _create_mv(query: object, db: Connection, name: str) -> Table:
    # geneva's query builders lose the GenevaQueryBuilder type through
    # search()/where()/select(); create_materialized_view exists at runtime.
    return query.create_materialized_view(db, name)  # pyright: ignore[reportAttributeAccessIssue]


# --- flavors: build / drive / read / oracle, with a known-bug classifier ----
class _Flavor(NamedTuple):
    shapes: tuple[str, ...]
    ops: tuple[str, ...]


FLAVORS: dict[str, _Flavor] = {
    "mv-identity": _Flavor(
        (IDENTITY,),
        (
            APPEND,
            DELETE,
            UPDATE,
            COMPACT,
            ADDCOL,
            MERGE,
            ENTER,
            REINSERT,
            NOOP,
            OPTIMIZE,
        ),
    ),
    "mv-filtered": _Flavor(
        (FILTERED,),
        (
            APPEND,
            DELETE,
            UPDATE,
            COMPACT,
            ADDCOL,
            MERGE,
            ENTER,
            REINSERT,
            NOOP,
            OPTIMIZE,
        ),
    ),
    # backfill/mvbf omit UPDATE and the newer mutation ops (MERGE/ENTER/REINSERT/
    # NOOP/OPTIMIZE): re-running full backfill (where='1=1') after an in-place
    # source update hits a real-Ray commit conflict (concurrent committers) that
    # the single-threaded shim cannot reproduce. The shim sweep covers UPDATE for
    # these flavors exhaustively and cleanly.
    "backfill": _Flavor((IDENTITY,), (APPEND, DELETE, COMPACT)),
    "mvbf-identity": _Flavor((IDENTITY,), (APPEND, DELETE, COMPACT)),
    "mvbf-filtered": _Flavor((FILTERED,), (APPEND, DELETE, COMPACT)),
}
# NOTE: the chunker (create_udtf_view) flavor is covered by the in-process shim
# sweep (test_mv_differential_shim), not here: a module-level @geneva.chunker does
# not deserialize in a real-Ray worker from the test module, which is a packaging
# quirk unrelated to refresh correctness. The shim exercises the chunker refresh
# logic (and pins GEN-611) in-process where no marshaling is involved.


def _is_backfilled(flavor: str) -> bool:
    return flavor.startswith("mvbf") or flavor == "backfill"


def _build(
    db: Connection, flavor: str, shape: str, name: str, srid: bool = True
) -> tuple[Table, Table, int]:
    """Return (source, target, base_version). target is what we refresh + read (the
    source itself for the plain backfill flavor); base_version is the source version
    immediately before MV creation -- the version the MV records as its refresh
    base (meaningful for the srid=False state model)."""
    source = _make_source(db, f"src_{name}", srid=srid)
    if _is_backfilled(flavor):
        source.add_columns({"doubled": _double})
        source.backfill("doubled", where="1=1", _admission_check=False)
    if flavor == "backfill":
        return source, source, source._ltbl.version
    cols = ["id", "value", "doubled"] if flavor.startswith("mvbf") else ["id", "value"]
    q = source.search(None)
    if shape == FILTERED:
        q = q.where(FILTER_EXPR)
    q = q.select(cols)
    base_version = source._ltbl.version
    if srid:
        return source, _create_mv(q, db, f"mv_{name}"), base_version
    with warnings.catch_warnings():
        # A non-SRID source warns at MV creation (query.py); that limitation is
        # exactly the condition under test here, so silence it.
        warnings.filterwarnings(
            "ignore", message=".*without stable row IDs.*", category=UserWarning
        )
        return source, _create_mv(q, db, f"mv_{name}"), base_version


def _oracle(source: Table, flavor: str, shape: str) -> list[tuple]:
    rows = _live(source)
    if shape == FILTERED:
        rows = [(i, v) for (i, v) in rows if v is not None and v > 50]
    if _is_backfilled(flavor):
        return _sorted([(i, v, None if v is None else v * 2) for (i, v) in rows])
    return _sorted(rows)


def _read(target: Table, flavor: str) -> list[tuple]:
    t = target.to_arrow()
    cols = ("id", "value", "doubled") if _is_backfilled(flavor) else ("id", "value")
    return _sorted(list(zip(*(t[c].to_pylist() for c in cols), strict=True)))


def _check(got: list[tuple], exp: list[tuple], ctx: str) -> None:
    # GEN-619 (refresh nulling a surviving row) is fixed, so any divergence -- a
    # null or otherwise -- is now a real regression and hard-fails.
    if got == exp:
        return
    pytest.fail(f"refresh divergence ({ctx}):\n  got={got}\n  exp={exp}")


def _drive(
    source: Table,
    seq: tuple[str, ...],
    name: str,
    sync_and_check: Callable[[str], None],
) -> None:
    """Apply ``seq`` step by step, invoking ``sync_and_check`` after the build and
    after every op (each invocation is one sync point)."""
    sync_and_check(f"{name} initial")
    append_n = 0
    for step, op in enumerate(seq):
        _apply_op(source, op, append_n, step)
        if op == APPEND:
            append_n += 1
        sync_and_check(f"{name} after step {step} ({op})")


def _run_sequence(
    db: Connection, flavor: str, shape: str, seq: tuple[str, ...]
) -> None:
    name = f"{flavor[:6]}_{shape[:3]}_" + ("".join(seq) if seq else "empty")
    source, target, _ = _build(db, flavor, shape, name)

    def sync_and_check(ctx: str) -> None:
        _sync(flavor, source, target)
        _check(_read(target, flavor), _oracle(source, flavor, shape), ctx)

    _drive(source, seq, name, sync_and_check)


def _run_sequence_srid_off(
    db: Connection, flavor: str, shape: str, seq: tuple[str, ...]
) -> None:
    """Differential run against a source WITHOUT stable row IDs.

    Backfills are rowaddr-based and must behave identically to srid-on (oracle
    equality at every sync point). MV refresh follows a version-based state
    model: it succeeds iff the source is still at the MV's base version; any
    later source version (data op, backfill commit, or a pure compaction) trips
    the cross-version guard, which raises client-side and must leave the MV
    byte-identical to its last-good state."""
    name = f"off_{flavor[:6]}_{shape[:3]}_" + ("".join(seq) if seq else "empty")
    source, target, base_version = _build(db, flavor, shape, name, srid=False)

    if flavor == "backfill":
        # No view involved: rowaddr parity, same oracle discipline as srid-on.
        def sync_and_check(ctx: str) -> None:
            _sync(flavor, source, target)
            _check(_read(target, flavor), _oracle(source, flavor, shape), ctx)

        _drive(source, seq, name, sync_and_check)
        return

    def _mv_state() -> tuple[int, pa.Schema, list[tuple]]:
        """Latest MV state as (version, schema, sorted rows over all columns).

        checkout_latest first: the handle pins the version it last saw, so a
        version committed out-of-band by a failed refresh would otherwise stay
        invisible. Lance versions are immutable, so an unchanged latest version
        number IS the byte-identical guarantee; schema (with metadata) and row
        contents are compared as belt-and-braces."""
        target.checkout_latest()
        t = target.to_arrow()
        rows = _sorted(
            list(zip(*(t[c].to_pylist() for c in t.column_names), strict=True))
        )
        return target._ltbl.version, t.schema, rows

    # Snapshot once right after build: for mvbf flavors the initial _sync
    # backfill can bump the source version, so even the FIRST refresh may hit
    # the guard; the frozen-snapshot assertion needs a baseline either way.
    snapshot = _mv_state()

    def sync_and_check(ctx: str) -> None:
        nonlocal snapshot
        if _is_backfilled(flavor):
            # The source backfill must succeed regardless of SRID.
            source.backfill("doubled", where="1=1", _admission_check=False)
        # Sync the handle so the version below matches what the refresh guard
        # resolves via a fresh open of the source table.
        source.checkout_latest()
        if source._ltbl.version == base_version:
            _refresh(target)
            snapshot = _mv_state()
            _check(_read(target, flavor), _oracle(source, flavor, shape), ctx)
        else:
            with pytest.raises(RuntimeError, match="stable row IDs"):
                _refresh(target)
            version, schema, rows = _mv_state()
            snap_version, snap_schema, snap_rows = snapshot
            assert version == snap_version, (
                f"cross-version guard committed a new MV version ({ctx}): "
                f"v{snap_version} -> v{version}"
            )
            assert schema.equals(snap_schema, check_metadata=True), (
                f"cross-version guard mutated the MV schema ({ctx}):\n"
                f"  got={schema}\n  frozen={snap_schema}"
            )
            assert rows == snap_rows, (
                f"cross-version guard mutated the MV ({ctx}):\n"
                f"  got={rows}\n  frozen={snap_rows}"
            )

    _drive(source, seq, name, sync_and_check)


# --- always-on named cases (small, one or two op steps per flavor) ----------
# Each entry is a (flavor, shape, seq, srid) tuple.
_NAMED: list[tuple[str, str, tuple, bool]] = [
    ("mv-identity", IDENTITY, (APPEND,), True),
    ("mv-identity", IDENTITY, (APPEND, DELETE), True),
    ("mv-identity", IDENTITY, (ADDCOL, APPEND), True),
    ("mv-filtered", FILTERED, (APPEND,), True),
    ("mv-filtered", FILTERED, (UPDATE,), True),
    ("mv-filtered", FILTERED, (APPEND, UPDATE), True),
    ("mv-filtered", FILTERED, (DELETE, APPEND), True),
    ("backfill", IDENTITY, (APPEND,), True),
    ("backfill", IDENTITY, (APPEND, DELETE), True),
    ("backfill", IDENTITY, (DELETE, APPEND), True),
    ("mvbf-identity", IDENTITY, (APPEND,), True),
    ("mvbf-identity", IDENTITY, (APPEND, DELETE), True),
    ("mvbf-filtered", FILTERED, (APPEND,), True),
    ("mvbf-filtered", FILTERED, (APPEND, DELETE), True),
    # newer source-mutation ops
    ("mv-identity", IDENTITY, (MERGE,), True),
    ("mv-filtered", FILTERED, (MERGE,), True),
    ("mv-identity", IDENTITY, (MERGE, COMPACT), True),
    ("mv-identity", IDENTITY, (REINSERT,), True),
    ("mv-filtered", FILTERED, (ENTER,), True),
    ("mv-filtered", FILTERED, (OPTIMIZE, APPEND), True),
    ("mv-identity", IDENTITY, (APPEND, NOOP), True),
    # srid-off axis: guard on a data-op bump, on a PURE compaction bump, at the
    # initial mvbf sync (backfill commit), and backfill rowaddr parity.
    ("mv-identity", IDENTITY, (APPEND,), False),
    ("mv-identity", IDENTITY, (COMPACT,), False),
    ("mvbf-identity", IDENTITY, (APPEND,), False),
    ("backfill", IDENTITY, (APPEND, DELETE), False),
]


def _case_id(flavor: str, seq: tuple, srid: bool, shape: str | None = None) -> str:
    mid = f"-{shape[:3]}" if shape else ""
    return f"{flavor}{mid}-{''.join(seq)}" + ("" if srid else "-nosrid")


def _dispatch(db: Connection, flavor: str, shape: str, seq: tuple, srid: bool) -> None:
    if srid:
        _run_sequence(db, flavor, shape, seq)
    else:
        _run_sequence_srid_off(db, flavor, shape, seq)


@pytest.mark.parametrize(
    ("flavor", "shape", "seq", "srid"),
    _NAMED,
    ids=[_case_id(fl, q, srid) for (fl, _sh, q, srid) in _NAMED],
)
def test_differential_named(
    db: Connection, local_ray_context, flavor: str, shape: str, seq: tuple, srid: bool
) -> None:
    _dispatch(db, flavor, shape, seq, srid)


# --- opt-in exhaustive sweep ----------------------------------------------
def _exhaustive() -> list[tuple]:
    max_len = int(os.environ.get("GENEVA_MVDIFF_MAXLEN", "2"))
    srid_env = os.environ.get("GENEVA_MVDIFF_SRID", "on")
    if srid_env not in ("on", "off", "both"):
        raise ValueError(f"GENEVA_MVDIFF_SRID must be on|off|both, got {srid_env!r}")
    srids = {"on": (True,), "off": (False,), "both": (True, False)}[srid_env]
    cases: list[tuple] = []
    for srid in srids:
        # srid-off runs are guard-dominated after the first version bump, so
        # depth beyond 2 adds little signal; cap it.
        cap = max_len if srid else min(max_len, 2)
        for flavor, fl in FLAVORS.items():
            for shape in fl.shapes:
                for length in range(1, cap + 1):
                    cases.extend(
                        (flavor, shape, seq, srid)
                        for seq in itertools.product(fl.ops, repeat=length)
                    )
    return cases


_EXHAUSTIVE = _exhaustive()


@pytest.mark.skipif(
    not os.environ.get("GENEVA_MVDIFF_EXHAUSTIVE"),
    reason="opt-in: set GENEVA_MVDIFF_EXHAUSTIVE=1 to run the sweep",
)
@pytest.mark.parametrize(
    ("flavor", "shape", "seq", "srid"),
    _EXHAUSTIVE,
    ids=[_case_id(fl, q, srid, shape=sh) for (fl, sh, q, srid) in _EXHAUSTIVE],
)
def test_differential_exhaustive(
    db: Connection, local_ray_context, flavor: str, shape: str, seq: tuple, srid: bool
) -> None:
    _dispatch(db, flavor, shape, seq, srid)


# --- explicit reproducers for the confirmed bugs (strict: flip when fixed) ---
def _rows(mv: Table) -> list[tuple]:
    t = mv.to_arrow()
    return _sorted(list(zip(t["id"].to_pylist(), t["value"].to_pylist(), strict=True)))


def test_gen619_incremental_delete_nulls_trailing_survivor(
    db: Connection, local_ray_context
) -> None:
    # Regression guard for GEN-619 (fixed): incremental refresh must NOT null a
    # surviving row when an earlier row in the same fragment is removed.
    src = _make_source(db, "g619_src")
    mv = _create_mv(
        src.search(None).where("value > 50").select(["id", "value"]), db, "g619_mv"
    )
    _refresh(mv)
    src.add(pa.table({"id": [100, 101], "value": [1000, 1010]}))  # one fragment
    _refresh(mv)
    assert _rows(mv) == [(100, 1000), (101, 1010)]
    src.delete("id = 100")  # delete the row preceding survivor 101 in the fragment
    _refresh(mv)
    # Pre-fix this read back (None, None); survivor 101 must keep its real values.
    assert _rows(mv) == [(101, 1010)]


def test_gen619_compounds_across_mv_chain(db: Connection, local_ray_context) -> None:
    # Regression guard for the GEN-619 MV-chain compounding variant (fixed): the
    # outer MV (identity over identity) must exactly equal the inner MV; pre-fix it
    # nulled an ADDITIONAL trailing survivor at each layer.
    src = _make_source(db, "g619c_src")
    mv1 = _create_mv(src.search(None).select(["id", "value"]), db, "g619c_mv1")
    _refresh(mv1)
    mv2 = _create_mv(mv1.search(None).select(["id", "value"]), db, "g619c_mv2")
    _refresh(mv2)
    src.add(pa.table({"id": [100, 101, 102], "value": [1000, 1010, 1020]}))
    _refresh(mv1)
    _refresh(mv2)
    src.delete("id % 2 = 0")  # removes 2, 4, 100, 102; survivors 1, 3, 101
    _refresh(mv1)
    _refresh(mv2)
    # identity-over-identity: the outer MV must EXACTLY equal the inner MV.
    assert _rows(mv2) == _rows(mv1)


def test_gen620_first_refresh_after_source_delete(
    db: Connection, local_ray_context
) -> None:
    # A source delete landing between MV creation and the first refresh
    # leaves stale placeholders; the refresh must prune them and yield the
    # survivors' real values.
    src = _make_source(db, "g620_src")
    mv = _create_mv(src.search(None).select(["id", "value"]), db, "g620_mv")
    src.delete("id % 2 = 0")  # delete BEFORE the view's first refresh -> leaves 1, 3
    _refresh(mv)
    assert _rows(mv) == [(1, 10), (3, 30)]


@pytest.mark.xfail(
    strict=True,
    reason="GEN-621: projection MV over a blob-encoded "
    "column produces all-null rows on refresh",
)
def test_gen621_blob_projection_mv_all_null(db: Connection, local_ray_context) -> None:
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field(
                "b", pa.large_binary(), metadata={b"lance-encoding:blob": b"true"}
            ),
        ]
    )
    data = pa.table(
        {"id": [0, 1, 2, 3], "b": [b"B" * (i + 1) for i in range(4)]}, schema=schema
    )
    src = db.create_table(
        "g621_src",
        data,
        storage_options={
            "new_table_enable_stable_row_ids": "true",
            "new_table_data_storage_version": "2.0",
        },
    )
    mv = _create_mv(src.search(None).select(["id", "b"]), db, "g621_mv")
    _refresh(mv)
    arr = mv.to_arrow()
    got = dict(zip(arr["id"].to_pylist(), arr["b"].to_pylist(), strict=True))
    assert got == {0: b"B", 1: b"BB", 2: b"BBB", 3: b"BBBB"}  # BUG: {None: None}
