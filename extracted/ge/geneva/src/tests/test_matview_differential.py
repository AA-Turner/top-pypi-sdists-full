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

Any divergence hard-fails (catches refresh bugs). GEN-619 (MV refresh nulling a
surviving row when an earlier row in the same fragment is removed) is fixed, so a
null is now a real regression, not an expected xfail. The reproducers for the
confirmed bugs are at the bottom: the GEN-619 ones are now passing regression
guards; GEN-620/621 remain strict-xfail until fixed.

The full sweep is opt-in via ``GENEVA_MVDIFF_EXHAUSTIVE=1`` (``GENEVA_MVDIFF_MAXLEN``
for depth). The fast no-cluster shim version runs in ``test_mv_differential_shim``.
"""

import itertools
import os
from typing import NamedTuple

import pyarrow as pa
import pytest

from geneva import udf
from geneva.db import Connection
from geneva.table import Table

pytestmark = pytest.mark.ray


# --- op alphabet -----------------------------------------------------------
APPEND = "A"  # append a block of fresh ids (100-spaced)
DELETE = "D"  # DELETE WHERE id % 2 = 0 -> in-place deletion in surviving frags
UPDATE = "U"  # UPDATE odd ids SET value=-1 -> crosses the value>50 filter
COMPACT = "C"  # compact_files -> fragment rewrite
ADDCOL = "X"  # add an unreferenced all-null column -> must NOT corrupt the view
MOVE = "M"  # UPDATE value>50 SET value=value+1 -> in-place value change

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


def _make_source(db: Connection, name: str) -> Table:
    return db.create_table(
        name, _initial(), storage_options={"new_table_enable_stable_row_ids": "true"}
    )


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
    "mv-identity": _Flavor((IDENTITY,), (APPEND, DELETE, UPDATE, COMPACT, ADDCOL)),
    "mv-filtered": _Flavor((FILTERED,), (APPEND, DELETE, UPDATE, COMPACT, ADDCOL)),
    # backfill/mvbf omit UPDATE: re-running full backfill (where='1=1') after an
    # in-place source update hits a real-Ray commit conflict (concurrent committers)
    # that the single-threaded shim cannot reproduce. The shim sweep covers UPDATE
    # for these flavors exhaustively and cleanly.
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


def _build(db: Connection, flavor: str, shape: str, name: str) -> tuple[Table, Table]:
    """Return (source, target). target is what we refresh + read (the source itself
    for the plain backfill flavor)."""
    source = _make_source(db, f"src_{name}")
    if _is_backfilled(flavor):
        source.add_columns({"doubled": _double})
        source.backfill("doubled", where="1=1", _admission_check=False)
    if flavor == "backfill":
        return source, source
    cols = ["id", "value", "doubled"] if flavor.startswith("mvbf") else ["id", "value"]
    q = source.search(None)
    if shape == FILTERED:
        q = q.where(FILTER_EXPR)
    return source, _create_mv(q.select(cols), db, f"mv_{name}")


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


def _run_sequence(
    db: Connection, flavor: str, shape: str, seq: tuple[str, ...]
) -> None:
    name = f"{flavor[:6]}_{shape[:3]}_" + ("".join(seq) if seq else "empty")
    source, target = _build(db, flavor, shape, name)
    _sync(flavor, source, target)
    _check(_read(target, flavor), _oracle(source, flavor, shape), f"{name} initial")
    append_n = 0
    for step, op in enumerate(seq):
        _apply_op(source, op, append_n, step)
        if op == APPEND:
            append_n += 1
        _sync(flavor, source, target)
        _check(
            _read(target, flavor),
            _oracle(source, flavor, shape),
            f"{name} after step {step} ({op})",
        )


# --- always-on named cases (small, one or two op steps per flavor) ----------
_NAMED: list[tuple[str, str, tuple]] = [
    ("mv-identity", IDENTITY, (APPEND,)),
    ("mv-identity", IDENTITY, (APPEND, DELETE)),
    ("mv-identity", IDENTITY, (ADDCOL, APPEND)),
    ("mv-filtered", FILTERED, (APPEND,)),
    ("mv-filtered", FILTERED, (UPDATE,)),
    ("mv-filtered", FILTERED, (APPEND, UPDATE)),
    ("mv-filtered", FILTERED, (DELETE, APPEND)),
    ("backfill", IDENTITY, (APPEND,)),
    ("backfill", IDENTITY, (APPEND, DELETE)),
    ("backfill", IDENTITY, (DELETE, APPEND)),
    ("mvbf-identity", IDENTITY, (APPEND,)),
    ("mvbf-identity", IDENTITY, (APPEND, DELETE)),
    ("mvbf-filtered", FILTERED, (APPEND,)),
    ("mvbf-filtered", FILTERED, (APPEND, DELETE)),
]


@pytest.mark.parametrize(
    ("flavor", "shape", "seq"),
    _NAMED,
    ids=[f"{fl}-{''.join(q)}" for (fl, _sh, q) in _NAMED],
)
def test_differential_named(
    db: Connection, local_ray_context, flavor: str, shape: str, seq: tuple
) -> None:
    _run_sequence(db, flavor, shape, seq)


# --- opt-in exhaustive sweep ----------------------------------------------
def _exhaustive() -> list[tuple]:
    max_len = int(os.environ.get("GENEVA_MVDIFF_MAXLEN", "2"))
    cases: list[tuple] = []
    for flavor, fl in FLAVORS.items():
        for shape in fl.shapes:
            for length in range(1, max_len + 1):
                cases.extend(
                    (flavor, shape, seq)
                    for seq in itertools.product(fl.ops, repeat=length)
                )
    return cases


_EXHAUSTIVE = _exhaustive()


@pytest.mark.skipif(
    not os.environ.get("GENEVA_MVDIFF_EXHAUSTIVE"),
    reason="opt-in: set GENEVA_MVDIFF_EXHAUSTIVE=1 to run the sweep",
)
@pytest.mark.parametrize(
    ("flavor", "shape", "seq"),
    _EXHAUSTIVE,
    ids=[f"{fl}-{sh[:3]}-{''.join(q)}" for (fl, sh, q) in _EXHAUSTIVE],
)
def test_differential_exhaustive(
    db: Connection, local_ray_context, flavor: str, shape: str, seq: tuple
) -> None:
    _run_sequence(db, flavor, shape, seq)


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


@pytest.mark.xfail(
    strict=True,
    reason="GEN-620: first refresh after a pre-refresh "
    "source delete produces all-null rows",
)
def test_gen620_first_refresh_after_source_delete(
    db: Connection, local_ray_context
) -> None:
    src = _make_source(db, "g620_src")
    mv = _create_mv(src.search(None).select(["id", "value"]), db, "g620_mv")
    src.delete("id % 2 = 0")  # delete BEFORE the view's first refresh -> leaves 1, 3
    _refresh(mv)
    assert _rows(mv) == [(1, 10), (3, 30)]  # BUG: all rows read back (None, None)


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
