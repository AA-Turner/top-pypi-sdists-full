# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Standalone shim-backed differential sweep over geneva's incremental compute
paths -- fast, no Ray cluster. Installs ``ray_shim`` then drives a source table
through *exhaustive* op sequences, refreshing/backfilling after every op and
comparing to a model-free Arrow oracle (the source recomputed). Exhaustive is only
practical for small sequence lengths, which is the point -- short sequences over
many flavors find the bugs.

Flavors (the power is in covering them all through one engine, plus the
combination):
  mv-identity / mv-filtered -- projection MV ``SELECT id, value [WHERE value>50]``.
  backfill                  -- ``add_columns`` + ``backfill`` of a UDF column.
  chunker                   -- ``create_udtf_view`` (1:N expansion) + refresh.
  mvbf-identity / mvbf-flt  -- COMBINATION: a projection MV over a *backfilled*
                               computed column (exercises backfill AND MV refresh).

Each divergence is classified against the KNOWN bugs for that flavor; anything else
is NEW (confirm on real Ray). Exits non-zero iff a NEW signature is found.

  mv* / backfill: none expected. GEN-619 (incremental refresh nulling a surviving
          row on an in-fragment delete) is fixed, so any mv/mvbf divergence is now
          a regression and counts as NEW.
  chunker: GEN-611 (chunker output goes stale on an in-place source update).

``GENEVA_MVDIFF_SRID=off`` sweeps NON-stable-row-id sources. The ``_rowaddr``-based
flavors (backfill / sparse / cf-*) keep their oracles -- those write paths must stay
oracle-correct without stable row ids -- while the mv* / mvbf* / chunker flavors flip
to GUARD runners: a v1 (non-SRID) view must refresh correctly AT its base version
(``GUARD-CONTENT``: oracle equality) and refuse any cross-version refresh with the
documented error, leaving the view byte-identical to its last-good state
(``GUARD-MISS`` / ``GUARD-WRONGERR`` / ``GUARD-MUTATE`` / ``GUARD-CONTENT`` are all
NEW findings).

Not a pytest test (it monkeypatches ``ray`` before importing geneva); run directly,
or via ``test_mv_differential_shim`` which executes it as a subprocess.
``GENEVA_MVDIFF_MAXLEN`` sets depth (default 3); ``SWEEP_WORKERS`` the pool size;
``GENEVA_MVDIFF_FLAVORS`` restricts the flavor set (csv); ``GENEVA_MVDIFF_SRID``
selects stable-row-id mode (``on``, the default, or ``off``).
"""

# ruff: noqa: T201 -- this is a CLI script; print() is the intended output

import itertools
import multiprocessing as mp
import os
import shutil
import sys
import tempfile
import warnings
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ray_shim  # noqa: E402

ray_shim.install()  # MUST precede the geneva import below

import pyarrow as pa  # noqa: E402

import geneva  # noqa: E402
from geneva import connect, udf  # noqa: E402
from geneva.db import Connection, dataset_uses_stable_row_ids  # noqa: E402
from geneva.table import Table  # noqa: E402

ray_shim.stub_geneva_cluster_polling()  # ~1.5x faster refresh; observability only

# Stable-row-id mode for every source table the sweep builds (see the docstring).
# Strict on|off: a typo silently meaning "on" would let a mis-configured srid-off
# leg pass as a duplicate srid-on run. ("both" belongs to the pytest axis in
# test_matview_differential, not to this one-mode-per-process script.)
_SRID_ENV = os.environ.get("GENEVA_MVDIFF_SRID", "on")
if _SRID_ENV not in ("on", "off"):
    print(f"GENEVA_MVDIFF_SRID must be 'on' or 'off', got {_SRID_ENV!r}")
    raise SystemExit(2)
_SRID = _SRID_ENV == "on"
if not _SRID:
    # View creation over a non-SRID source warns by design; under srid-off that
    # warning fires for every guard case and is pure noise (module-level so the
    # spawned pool workers, which re-import this module, inherit the filter).
    warnings.filterwarnings("ignore", message=".*without stable row IDs.*")

# --- op alphabet -----------------------------------------------------------
APPEND, DELETE, UPDATE, COMPACT, ADDCOL, MOVE = "A", "D", "U", "C", "X", "M"
# B = partial-WHERE re-backfill: matched rows recompute, unmatched carry forward.
BACKFILL = "B"
CF_PARTIAL_EXPR = "value > 25"  # a proper subset of the initial rows
IDENTITY, FILTERED = "identity", "filtered"
FILTER_EXPR = "value > 50"
SPARSE_MODE = "sparse_rows"  # update_mode for the sparse row-update path


@udf(data_type=pa.int64())
def _double(value: int) -> int:
    return value * 2


# --- carry-forward DATATYPE registry --------------------------------------
# Every carry-forward UDF reads a NON-blob input (``value``) and PRODUCES a column
# encoding ``value*2``, so that column is a carry-forward / non-UDF-input column --
# exactly the shape a filtered (partial) re-backfill must carry forward for the
# unmatched rows. The payload encodes ``value*2`` uniformly so one int-valued
# ``model`` is the oracle for every datatype (``decode`` recovers the int).


@udf(data_type=pa.int32())
def _double_i32(value: int) -> int:
    return value * 2


@udf(data_type=pa.float64())
def _double_f64(value: int) -> float:
    return float(value * 2)


@udf(data_type=pa.string())
def _double_str(value: int) -> str:
    return f"v={value * 2}"


@udf(data_type=pa.large_string())
def _double_lstr(value: int) -> str:
    return f"v={value * 2}"


# plain (NON-blob) binary: large_binary WITHOUT the blob encoding marker. Isolates
# that it is the blob *encoding* (descriptor storage), not binary data, that breaks.
@udf(data_type=pa.large_binary())
def _double_bin(value: int) -> bytes:
    return f"v={value * 2}".encode()


@udf(data_type=pa.list_(pa.int64()))
def _double_list(value: int) -> list:
    return [value * 2]


# fixed_size_list<float32> -- the vector/embedding shape ubiquitous in lancedb.
@udf(data_type=pa.list_(pa.float32(), 4))
def _double_vec(value: int) -> list:
    return [float(value * 2), 0.0, 0.0, 0.0]


# non-blob struct (no descriptor leaves) -- contrast with the struct-nested-blob.
@udf(data_type=pa.struct([("a", pa.int64()), ("b", pa.int64())]))
def _double_struct(value: int) -> dict:
    return {"a": value * 2, "b": value}


_BLOB_META = {"lance-encoding:blob": "true"}


@udf(data_type=pa.large_binary(), field_metadata=_BLOB_META)
def _double_blob(value: int) -> bytes:
    return f"v={value * 2}".encode()


# struct<image_bytes: large_binary [blob], width: int64> -- the enterprise shape
# (``image.image_bytes``): a struct with a NESTED blob leaf carried forward.
_IMG_TYPE = pa.struct(
    [
        pa.field(
            "image_bytes", pa.large_binary(), metadata={b"lance-encoding:blob": b"true"}
        ),
        pa.field("width", pa.int64()),
    ]
)


@udf(data_type=_IMG_TYPE)
def _double_struct_blob(value: int) -> dict:
    return {"image_bytes": f"v={value * 2}".encode(), "width": value}


# decode: map a materialized cell back to the doubled int (or None == uncomputed),
# so every datatype shares the one int-valued oracle ``model``.
def _dec_int(cell: object) -> object:
    return cell  # int column: cell IS the doubled int


def _dec_round(cell: object) -> int:
    return int(round(cell))  # type: ignore[arg-type]  # float column


def _dec_payload(cell: object) -> int | None:
    # An empty payload means "uncomputed": appended rows start with a null column,
    # and compaction can materialize that null as a zero-length blob/string rather
    # than a null cell -- treat both as None so the oracle (model) still matches.
    s = cell.decode() if isinstance(cell, (bytes, bytearray)) else str(cell)
    s = s.removeprefix("v=")
    return int(s) if s else None


def _dec_first(cell: object) -> int | None:
    # list / fixed_size_list: the first element carries value*2.
    if not cell or cell[0] is None:  # type: ignore[index]
        return None
    return int(round(cell[0]))  # type: ignore[index]


def _dec_field(cell: object) -> int | None:
    a = cell.get("a") if cell else None  # type: ignore[attr-defined]  # struct 'a'
    return None if a is None else int(a)


class _CFKind(NamedTuple):
    """A carry-forward column datatype: producing UDF + how to read it back.

    ``leaf`` is the nested blob field for a struct-with-blob column (else None).
    ``blob`` marks columns stored as Lance blobs -- a plain scan returns them as
    ``struct<position,size>`` descriptors, so the oracle must materialize bytes via
    ``take_blobs`` (see ``_read_doubled``). ``decode`` maps a materialized cell back
    to the doubled int so every datatype shares the one int-valued oracle model.

    Types that cannot encode ``value*2`` under that shared model (bool, temporal)
    are intentionally omitted -- they also can't expose an ``if_else`` carry-forward
    gap that the numeric/binary/nested types don't already cover."""

    name: str
    col: str
    udf: object
    leaf: str | None
    blob: bool
    decode: object


# The carry-forward datatypes the sweep exercises. Add one here and both its
# legacy (-off) and deferred (-on) flavors generate automatically (see FLAVORS).
# Sweeping all of them finds any type that can't carry forward, not just blobs.
_CF_KINDS = [
    # --- non-blob ---
    _CFKind("int", "doubled", _double, None, False, _dec_int),
    _CFKind("int32", "i32", _double_i32, None, False, _dec_int),
    _CFKind("float", "f64", _double_f64, None, False, _dec_round),
    _CFKind("str", "tag", _double_str, None, False, _dec_payload),
    _CFKind("lstr", "ltag", _double_lstr, None, False, _dec_payload),
    _CFKind("binary", "bin", _double_bin, None, False, _dec_payload),
    _CFKind("list", "lst", _double_list, None, False, _dec_first),
    _CFKind("vector", "vec", _double_vec, None, False, _dec_first),
    _CFKind("struct", "pair", _double_struct, None, False, _dec_field),
    # --- blob (descriptor-backed) ---
    _CFKind("blob", "img", _double_blob, None, True, _dec_payload),
    _CFKind(
        "structblob", "image", _double_struct_blob, "image_bytes", True, _dec_payload
    ),
]
_CF_INT = _CF_KINDS[0]  # default kind for _run_cf's signature


class _Chunk(NamedTuple):
    k: int
    derived: int


@geneva.chunker
def _expand2(value: int) -> Iterator[_Chunk]:
    for k in range(2):
        yield _Chunk(k=k, derived=value * 10 + k)


def _sorted(rows: list[tuple]) -> list[tuple]:
    return sorted(
        rows, key=lambda r: tuple((x is None, x if x is not None else 0) for x in r)
    )


def _initial() -> pa.Table:
    return pa.table({"id": [1, 2, 3, 4], "value": [10, 20, 30, 40]})


def _append_block(n: int) -> pa.Table:
    base = 100 * (n + 1)
    ids = [base, base + 1, base + 2]
    return pa.table({"id": ids, "value": [i * 10 for i in ids]})


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


def _live(source: Table) -> list[tuple]:
    t = source.to_arrow()
    return list(zip(t["id"].to_pylist(), t["value"].to_pylist(), strict=True))


# --- per-flavor build / refresh / read / oracle / classify -----------------
def _mk_source(db: Connection, name: str) -> Table:
    # srid-off must OMIT the option entirely: bool False crashes create_table
    # (GEN-869) and the string "false" is silently inert.
    opts = {"new_table_enable_stable_row_ids": "true"} if _SRID else None
    tbl = db.create_table(name, _initial(), storage_options=opts)
    if not _SRID:
        # Second fragment so COMPACT has real work: a pure-compaction version
        # bump is the exact hazard the srid-off refresh guard exists for, and
        # compact_files on a 1-fragment no-deletes table commits nothing --
        # a (C,) guard case would silently never leave the base version.
        tbl.add(pa.table({"id": [50, 51], "value": [500, 510]}))
    assert dataset_uses_stable_row_ids(tbl.to_lance()) is _SRID
    return tbl


def _has_null(rows: list[tuple]) -> bool:
    return any(any(x is None for x in r) for r in rows)


def _null_clobber(got: list[tuple], exp: list[tuple]) -> bool:
    """A computed value null in ``got`` but non-null in the oracle: an unmatched
    row null-filled instead of carried forward."""
    g = {r[0]: r[-1] for r in got}
    e = {r[0]: r[-1] for r in exp}
    return any(g.get(k) is None and v is not None for k, v in e.items())


def _run_mv(db: Connection, name: str, shape: str, seq: tuple, backfilled: bool) -> str:
    """Projection MV. If backfilled, the source first gets a backfilled `doubled`
    column and the MV projects it too (the combination flavor)."""
    source = _mk_source(db, f"s_{name}")
    cols = ["id", "value"]
    if backfilled:
        source.add_columns({"doubled": _double})
        source.backfill("doubled", where="1=1", _admission_check=False)
        cols = ["id", "value", "doubled"]
    q = source.search(None)
    if shape == FILTERED:
        q = q.where(FILTER_EXPR)
    mv = q.select(cols).create_materialized_view(db, f"m_{name}")  # pyright: ignore[reportAttributeAccessIssue]
    mv.refresh(_admission_check=False)

    def oracle() -> list[tuple]:
        rows = _live(source)
        if shape == FILTERED:
            rows = [(i, v) for (i, v) in rows if v is not None and v > 50]
        if backfilled:
            return _sorted([(i, v, (None if v is None else v * 2)) for (i, v) in rows])
        return _sorted(rows)

    def read() -> list[tuple]:
        t = mv.to_arrow()
        if backfilled:
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
        return _sorted(
            list(zip(t["id"].to_pylist(), t["value"].to_pylist(), strict=True))
        )

    if read() != oracle():
        return "GEN-619" if _has_null(read()) else f"NEW@init: {read()[:6]}"
    append_n = 0
    for step, op in enumerate(seq):
        _apply_op(source, op, append_n, step)
        if backfilled and op in (APPEND, UPDATE, MOVE):
            source.backfill("doubled", where="1=1", _admission_check=False)
        if op == APPEND:
            append_n += 1
        mv.refresh(_admission_check=False)
        got = read()
        if got != oracle():
            return "GEN-619" if _has_null(got) else f"NEW@{op}: {got[:6]}"
    return "PASS"


def _run_backfill(db: Connection, name: str, shape: str, seq: tuple) -> str:
    """add_columns + full backfill of `doubled = value*2` after each op."""
    source = _mk_source(db, f"s_{name}")
    source.add_columns({"doubled": _double})
    source.backfill("doubled", where="1=1", _admission_check=False)

    def oracle() -> list[tuple]:
        return _sorted(
            [(i, v, (None if v is None else v * 2)) for (i, v) in _live(source)]
        )

    def read() -> list[tuple]:
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

    if read() != oracle():
        return f"NEW@init: {read()[:6]}"
    append_n = 0
    for step, op in enumerate(seq):
        _apply_op(source, op, append_n, step)
        if op == APPEND:
            append_n += 1
        source.backfill("doubled", where="1=1", _admission_check=False)
        got = read()
        if got != oracle():
            sig = "NEW-NULL" if _has_null(got) else "NEW"
            return f"{sig}@{op}: {got[:6]}"
    return "PASS"


def _read_doubled(source: Table, kind: _CFKind) -> dict:
    """``id -> recovered doubled int`` (None where the column is null).

    For a blob column a plain scan returns ``struct<position,size>`` descriptors,
    not bytes, so we materialize the payload via ``take_blobs`` (keyed by stable
    row id). ``kind.decode`` recovers the doubled int from each cell; ``kind.leaf``
    selects the nested blob field for a struct-with-blob column."""
    if not kind.blob:
        t = source.to_arrow()
        return {
            i: (None if c is None else kind.decode(c))
            for i, c in zip(t["id"].to_pylist(), t[kind.col].to_pylist(), strict=True)
        }

    ds = source.to_lance()
    t = ds.to_table(columns=["id", kind.col], with_row_id=True)
    ids = t["id"].to_pylist()
    rowids = t["_rowid"].to_pylist()
    descs = t[kind.col].to_pylist()  # descriptor dict(s), or None for unfilled rows
    out: dict = {}
    live_ids: list = []
    live_rowids: list = []
    for i, rid, d in zip(ids, rowids, descs, strict=True):
        present = d is not None and (kind.leaf is None or d.get(kind.leaf) is not None)
        if present:
            live_ids.append(i)
            live_rowids.append(rid)
        else:
            out[i] = None
    if live_rowids:
        blob_col = kind.col if kind.leaf is None else f"{kind.col}.{kind.leaf}"
        blobs = ds.take_blobs(blob_col, ids=live_rowids)
        for i, b in zip(live_ids, blobs, strict=True):
            out[i] = kind.decode(b.readall())
    return out


def _run_cf(
    db: Connection,
    name: str,
    shape: str,
    seq: tuple,
    *,
    defer: bool,
    kind: _CFKind = _CF_INT,
) -> str:
    """Partial-WHERE re-backfill with carry-forward.

    Backfill ``kind.col = value*2`` fully, then drive an op sequence whose ``B`` op
    does a PARTIAL re-backfill -- matched rows recompute, unmatched keep their prior
    value. The stateful ``model`` is the oracle for that. ``kind`` selects the
    carry-forward column's datatype (int / blob / struct-with-nested-blob); the
    blob variants are the ones that exercise the carry-forward crash.

    defer=False runs the legacy path; defer=True runs the deferred path. A ``B``
    crash is reported as ``CF-DEFER`` (deferred) or ``CF-LEGACY`` (legacy) -- both
    NEW unless listed in the flavor's known set.
    """
    import geneva.runners.ray.pipeline as p

    # Guard for builds without the flag: fall back to the legacy path rather than
    # raising AttributeError.
    has_flag = hasattr(p, "DEFAULT_DEFER_CARRY_FORWARD")
    prev = getattr(p, "DEFAULT_DEFER_CARRY_FORWARD", False)
    try:
        # Establish the column with the LEGACY path: deferred carry-forward is the
        # variable under test, and the initial full backfill is just setup (nothing
        # to carry forward yet). Forcing it off here means every datatype reaches the
        # op loop identically, so the only thing ``defer`` changes is the per-op
        # filtered RE-backfill (the ``B`` op). Also mirrors the real shape: the first
        # backfill has no WHERE; only the later filtered re-backfill defers.
        p.DEFAULT_DEFER_CARRY_FORWARD = False
        source = _mk_source(db, f"s_{name}")
        source.add_columns({kind.col: kind.udf})
        source.backfill(kind.col, where=None, _admission_check=False)
        p.DEFAULT_DEFER_CARRY_FORWARD = defer
        # model[id] -> expected doubled (None == not yet computed / carried null).
        model = {i: (None if v is None else v * 2) for i, v in _live(source)}

        def _matched(v: int | None) -> bool:
            return v is not None and v > 25  # mirrors CF_PARTIAL_EXPR

        def oracle() -> list[tuple]:
            return _sorted([(i, v, model.get(i)) for i, v in _live(source)])

        def read() -> list[tuple]:
            doubled = _read_doubled(source, kind)
            return _sorted([(i, v, doubled.get(i)) for i, v in _live(source)])

        if read() != oracle():
            return f"NEW@init: got={read()[:6]} exp={oracle()[:6]}"
        append_n = 0
        for step, op in enumerate(seq):
            if op == BACKFILL:
                try:
                    source.backfill(
                        kind.col, where=CF_PARTIAL_EXPR, _admission_check=False
                    )
                except Exception as ex:  # noqa: BLE001
                    # Classify rather than raise: report the crash signature
                    # (CF-DEFER = deferred path; CF-LEGACY = legacy applier).
                    sig = "CF-DEFER" if defer else "CF-LEGACY"
                    return f"{sig}@{op}: {type(ex).__name__}: {str(ex)[:50]}"
                for i, v in _live(source):
                    if _matched(v):
                        model[i] = None if v is None else v * 2  # else carry-forward
            else:
                _apply_op(source, op, append_n, step)
                if op == APPEND:
                    append_n += 1
                # reconcile ids: drop deleted, new rows start uncomputed (null).
                live_ids = {i for i, _ in _live(source)}
                for i in [k for k in model if k not in live_ids]:
                    del model[i]
                for i, _ in _live(source):
                    model.setdefault(i, None)
            got, exp = read(), oracle()
            if got != exp:
                if defer:
                    # deferred-path divergence
                    return f"CF-DEFER@{op}: got={got[:6]} exp={exp[:6]}"
                sig = "CF-NULLCLOBBER" if _null_clobber(got, exp) else "CF-DIVERGE"
                return f"{sig}@{op}: got={got[:6]} exp={exp[:6]}"
        return "PASS"
    finally:
        if has_flag:
            p.DEFAULT_DEFER_CARRY_FORWARD = prev
        else:
            delattr(p, "DEFAULT_DEFER_CARRY_FORWARD")  # remove our footprint


def _run_sparse(db: Connection, name: str, shape: str, seq: tuple) -> str:
    """Partial-WHERE re-backfill via the SPARSE path (``update_mode=sparse_rows``).

    Sparse (delete+append) must produce the same logical result as carry-forward
    (in-place column rewrite), so it shares the carry-forward oracle: backfill
    ``doubled = value*2`` fully, then drive an op sequence whose ``B`` op partially
    re-backfills (matched rows recompute, unmatched carry forward). The stateful
    ``model`` is the oracle; any divergence is a sparse-path bug (``SPARSE-*``).
    An equivalence test: sparse vs carry-forward across the swept op sequences."""
    source = _mk_source(db, f"s_{name}")
    source.add_columns({"doubled": _double})
    source.backfill(
        "doubled", where="1=1", _admission_check=False, update_mode=SPARSE_MODE
    )
    model = {i: (None if v is None else v * 2) for i, v in _live(source)}

    def _matched(v: int | None) -> bool:
        return v is not None and v > 25  # mirrors CF_PARTIAL_EXPR

    def oracle() -> list[tuple]:
        return _sorted([(i, v, model.get(i)) for i, v in _live(source)])

    def read() -> list[tuple]:
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

    if read() != oracle():
        return f"SPARSE-DIVERGE@init: got={read()[:6]} exp={oracle()[:6]}"
    append_n = 0
    for step, op in enumerate(seq):
        if op == BACKFILL:
            try:
                source.backfill(
                    "doubled",
                    where=CF_PARTIAL_EXPR,
                    _admission_check=False,
                    update_mode=SPARSE_MODE,
                )
            except Exception as ex:  # noqa: BLE001
                return f"SPARSE-CRASH@{op}: {type(ex).__name__}: {str(ex)[:50]}"
            for i, v in _live(source):
                if _matched(v):
                    model[i] = None if v is None else v * 2  # else carry-forward
        else:
            _apply_op(source, op, append_n, step)
            if op == APPEND:
                append_n += 1
            # reconcile ids: drop deleted, new rows start uncomputed (null).
            live_ids = {i for i, _ in _live(source)}
            for i in [k for k in model if k not in live_ids]:
                del model[i]
            for i, _ in _live(source):
                model.setdefault(i, None)
        got, exp = read(), oracle()
        if got != exp:
            sig = "SPARSE-NULLCLOBBER" if _null_clobber(got, exp) else "SPARSE-DIVERGE"
            return f"{sig}@{op}: got={got[:6]} exp={exp[:6]}"
    return "PASS"


def _run_chunker(db: Connection, name: str, shape: str, seq: tuple) -> str:
    """1:2 chunker view; oracle is the row->2-chunk expansion."""
    source = _mk_source(db, f"s_{name}")
    mv = db.create_udtf_view(
        f"m_{name}", source.search(None).select(["id", "value"]), _expand2
    )
    mv.refresh(_admission_check=False)

    def oracle() -> list[tuple]:
        out = []
        for i, v in _live(source):
            out += [
                (i, 0, (None if v is None else v * 10)),
                (i, 1, (None if v is None else v * 10 + 1)),
            ]
        return _sorted(out)

    def read() -> list[tuple]:
        t = mv.to_arrow()
        return _sorted(
            list(
                zip(
                    t["id"].to_pylist(),
                    t["k"].to_pylist(),
                    t["derived"].to_pylist(),
                    strict=True,
                )
            )
        )

    if read() != oracle():
        return f"NEW@init: {read()[:6]}"
    append_n = 0
    for step, op in enumerate(seq):
        _apply_op(source, op, append_n, step)
        if op == APPEND:
            append_n += 1
        mv.refresh(_admission_check=False)
        got, exp = read(), oracle()
        if got != exp:
            if _has_null(got):
                return f"GEN-619@{op}: {got[:6]}"
            if len(got) != len(exp):
                return f"NEW-COUNT@{op}: |got|={len(got)} |exp|={len(exp)}"
            # count ok, non-null, values wrong on an update == chunker stale == GEN-611
            if op in (UPDATE, MOVE):
                return "GEN-611"
            return f"NEW@{op}: {got[:6]}"
    return "PASS"


# --- srid-off GUARD runners -------------------------------------------------
# A view over a non-SRID source is format v1: refresh succeeds iff the source is
# still AT the view's base version, else the guard must raise (projection MV: a
# client-side RuntimeError mentioning "stable row IDs", table.py; chunker: a
# worker-side ValueError mentioning "chunker materialized view", pipeline.py)
# and must leave the view byte-identical to its last-good state. An at-base
# refresh must also MATCH the oracle (GUARD-CONTENT): the frozen snapshot every
# later GUARD-MUTATE check compares against must itself be right.


class _MvSnap(NamedTuple):
    """The view state a guard raise must leave untouched."""

    version: int
    schema: str
    rows: list[tuple]


def _mv_snapshot(mv: Table) -> _MvSnap:
    """Full-state snapshot of the view's LATEST version.

    Spans every part of the no-mutation contract, not just the rows: a refresh
    that commits a new version whose content happens to be identical, or that
    changes only the schema or its field metadata, has still mutated the view
    even though an order-insensitive row snapshot alone would compare equal."""
    mv.checkout_latest()
    t = mv.to_arrow()
    cols = t.column_names
    rows = _sorted([tuple(row[c] for c in cols) for row in t.to_pylist()])
    return _MvSnap(mv.version, _schema_repr(mv.schema), rows)


def _schema_repr(schema: pa.Schema) -> str:
    """Field names, types, nullability, and metadata, as a comparable string."""
    fields = ";".join(
        f"{f.name}:{f.type}:{'null' if f.nullable else 'notnull'}:"
        f"{sorted((f.metadata or {}).items())}"
        for f in schema
    )
    return f"{fields}|meta={sorted((schema.metadata or {}).items())}"


def _snap_diff(got: _MvSnap, exp: _MvSnap) -> str:
    """Name the part of the view state that moved, most structural first."""
    if got.version != exp.version:
        return f"version {exp.version}->{got.version}"
    if got.schema != exp.schema:
        return f"schema {exp.schema} != {got.schema}"
    return f"rows got={got.rows[:6]} exp={exp.rows[:6]}"


def _guard_step(
    mv: Table,
    source: Table,
    base_version: int,
    snapshot: _MvSnap,
    op: str,
    err_type: type[Exception],
    err_text: str,
    content_fail: Callable[[], str | None],
) -> tuple[str | None, _MvSnap]:
    """One guarded refresh: returns ``(failure_or_None, current_snapshot)``.

    Refresh must succeed iff the source is back at ``base_version`` (the
    version-based state model); a raise must be ``err_type`` carrying
    ``err_text`` and must not have mutated the view. A refresh that succeeds
    at base must also pass ``content_fail`` (oracle equality): freezing a
    wrong snapshot would make every later GUARD-MUTATE check vacuous."""
    at_base = source.version == base_version
    try:
        mv.refresh(_admission_check=False)
    except Exception as ex:  # noqa: BLE001 -- classify, don't crash the case
        if at_base:
            detail = f"{type(ex).__name__}: {str(ex)[:60]}"
            return f"GUARD-WRONGERR@{op}: raised at base version: {detail}", snapshot
        if not (isinstance(ex, err_type) and err_text in str(ex)):
            return f"GUARD-WRONGERR@{op}: {type(ex).__name__}: {str(ex)[:60]}", snapshot
        got = _mv_snapshot(mv)
        if got != snapshot:
            return f"GUARD-MUTATE@{op}: {_snap_diff(got, snapshot)}", snapshot
        return None, snapshot
    if not at_base:
        return f"GUARD-MISS@{op}: refresh succeeded across versions", snapshot
    fail = content_fail()
    if fail is not None:
        return f"{fail}@{op}", snapshot
    return None, _mv_snapshot(mv)  # refreshed at base: re-freeze last-good


def _run_mv_guard(
    db: Connection, name: str, shape: str, seq: tuple, backfilled: bool
) -> str:
    """srid-off projection MV (and mvbf combination): assert the cross-version
    refresh guard on top of at-base content. The initial refresh happens at the
    base version, so it must succeed, match the oracle (GUARD-CONTENT), and
    freeze the baseline snapshot."""
    source = _mk_source(db, f"s_{name}")
    cols = ["id", "value"]
    if backfilled:
        source.add_columns({"doubled": _double})
        source.backfill("doubled", where="1=1", _admission_check=False)
        cols = ["id", "value", "doubled"]
    q = source.search(None)
    if shape == FILTERED:
        q = q.where(FILTER_EXPR)
    mv = q.select(cols).create_materialized_view(db, f"m_{name}")  # pyright: ignore[reportAttributeAccessIssue]

    def oracle() -> list[tuple]:
        rows = _live(source)
        if shape == FILTERED:
            rows = [(i, v) for (i, v) in rows if v is not None and v > 50]
        if backfilled:
            return _sorted([(i, v, (None if v is None else v * 2)) for (i, v) in rows])
        return _sorted(rows)

    def content_fail() -> str | None:
        t = mv.to_arrow()
        got = _sorted(list(zip(*(t[c].to_pylist() for c in cols), strict=True)))
        exp = oracle()
        return None if got == exp else f"GUARD-CONTENT: got={got[:6]} exp={exp[:6]}"

    mv.refresh(_admission_check=False)  # at base version: the initial sync
    base_version = source.version
    snapshot = _mv_snapshot(mv)
    fail = content_fail()
    if fail is not None:
        return f"{fail}@init"
    append_n = 0
    for step, op in enumerate(seq):
        _apply_op(source, op, append_n, step)
        if backfilled and op in (APPEND, UPDATE, MOVE):
            # the source-side backfill is the _rowaddr parity path: it must keep
            # working under srid-off even though the MV refresh is guarded off
            source.backfill("doubled", where="1=1", _admission_check=False)
        if op == APPEND:
            append_n += 1
        fail, snapshot = _guard_step(
            mv,
            source,
            base_version,
            snapshot,
            op,
            RuntimeError,
            "stable row IDs",
            content_fail,
        )
        if fail is not None:
            return fail
    return "PASS"


def _run_chunker_guard(db: Connection, name: str, shape: str, seq: tuple) -> str:
    """srid-off chunker view: same guard contract, worker-side ValueError."""
    source = _mk_source(db, f"s_{name}")
    mv = db.create_udtf_view(
        f"m_{name}", source.search(None).select(["id", "value"]), _expand2
    )

    def content_fail() -> str | None:
        t = mv.to_arrow()
        got = _sorted(
            list(
                zip(
                    t["id"].to_pylist(),
                    t["k"].to_pylist(),
                    t["derived"].to_pylist(),
                    strict=True,
                )
            )
        )
        exp = []
        for i, v in _live(source):
            exp += [
                (i, 0, (None if v is None else v * 10)),
                (i, 1, (None if v is None else v * 10 + 1)),
            ]
        exp = _sorted(exp)
        return None if got == exp else f"GUARD-CONTENT: got={got[:6]} exp={exp[:6]}"

    mv.refresh(_admission_check=False)  # at base version: the initial sync
    base_version = source.version
    snapshot = _mv_snapshot(mv)
    fail = content_fail()
    if fail is not None:
        return f"{fail}@init"
    append_n = 0
    for step, op in enumerate(seq):
        _apply_op(source, op, append_n, step)
        if op == APPEND:
            append_n += 1
        fail, snapshot = _guard_step(
            mv,
            source,
            base_version,
            snapshot,
            op,
            ValueError,
            "chunker materialized view",
            content_fail,
        )
        if fail is not None:
            return fail
    return "PASS"


# flavor -> (runner, shapes, op alphabet, known-signature set)
# GEN-619 is fixed, so mv/mvbf flavors expect NO divergence -- a reappearing null
# (still labelled "GEN-619" by the runner) falls through to NEW and fails the sweep.
_KNOWN_MV: set[str] = set()
_KNOWN_CK = {"GEN-611"}
# Carry-forward known-bug sets (per datatype, see the FLAVORS loop). The blob
# carry-forward crashes are fixed, so both paths expect no divergence -- a
# recurrence falls through to NEW and fails the sweep. CF-DEFER = deferred path;
# CF-LEGACY = legacy applier path.
_KNOWN_CF_DEFER: set[str] = set()
_KNOWN_CF_LEGACY: set[str] = set()
FLAVORS = {
    "mv-identity": (
        lambda db, n, sh, sq: _run_mv(db, n, sh, sq, False),
        [IDENTITY],
        [APPEND, DELETE, UPDATE, COMPACT, ADDCOL],
        _KNOWN_MV,
    ),
    "mv-filtered": (
        lambda db, n, sh, sq: _run_mv(db, n, sh, sq, False),
        [FILTERED],
        [APPEND, DELETE, UPDATE, COMPACT, ADDCOL],
        _KNOWN_MV,
    ),
    "backfill": (
        lambda db, n, sh, sq: _run_backfill(db, n, sh, sq),
        [IDENTITY],
        [APPEND, DELETE, UPDATE, COMPACT],
        set(),
    ),
    # sparse must match carry-forward over every short op sequence; any divergence
    # is NEW (no known sparse bugs). BACKFILL exercises a partial re-backfill.
    "sparse": (
        lambda db, n, sh, sq: _run_sparse(db, n, sh, sq),
        [IDENTITY],
        [APPEND, DELETE, UPDATE, COMPACT, BACKFILL],
        set(),
    ),
    "chunker": (
        lambda db, n, sh, sq: _run_chunker(db, n, sh, sq),
        [IDENTITY],
        [APPEND, DELETE, UPDATE, COMPACT, MOVE],
        _KNOWN_CK,
    ),
    "mvbf-identity": (
        lambda db, n, sh, sq: _run_mv(db, n, sh, sq, True),
        [IDENTITY],
        [APPEND, DELETE, UPDATE, COMPACT],
        _KNOWN_MV,
    ),
    "mvbf-filtered": (
        lambda db, n, sh, sq: _run_mv(db, n, sh, sq, True),
        [FILTERED],
        [APPEND, DELETE, UPDATE, COMPACT],
        _KNOWN_MV,
    ),
}


def _cf_ops(kind: _CFKind) -> list[str]:
    """Op alphabet for a carry-forward flavor. UPDATE is dropped for blob datatypes:
    updating a row with a materialized blob column hits an unrelated lance internal
    error, so it would only add noise."""
    base = [APPEND, DELETE, COMPACT, BACKFILL]
    return base if kind.blob else [*base[:-1], UPDATE, BACKFILL]


# Carry-forward coverage: sweep every datatype in ``_CF_KINDS`` through the same
# partial-WHERE re-backfill, on both the legacy (-off) and deferred (-on) path.
# Adding a datatype extends the sweep automatically; the blob datatypes are the
# carry-forward stress cases (see the known-set comment above). Under srid-off
# only the representative kinds run (int + the two blob shapes) to bound the
# case count -- the cf oracle itself is srid-agnostic (_rowaddr-based).
_CF_SWEEP_KINDS = (
    _CF_KINDS
    if _SRID
    else [k for k in _CF_KINDS if k.name in ("int", "blob", "structblob")]
)
for _k in _CF_SWEEP_KINDS:
    FLAVORS[f"cf-{_k.name}-off"] = (
        lambda db, n, sh, sq, k=_k: _run_cf(db, n, sh, sq, defer=False, kind=k),
        [IDENTITY],
        _cf_ops(_k),
        _KNOWN_CF_LEGACY,
    )
    FLAVORS[f"cf-{_k.name}-on"] = (
        lambda db, n, sh, sq, k=_k: _run_cf(db, n, sh, sq, defer=True, kind=k),
        [IDENTITY],
        _cf_ops(_k),
        _KNOWN_CF_DEFER,
    )

# srid-off: the view flavors flip to the GUARD runners (same names, same shapes
# and op alphabets, so GENEVA_MVDIFF_FLAVORS keeps working unchanged). Their
# known sets are EMPTY: any GUARD-* signature is a NEW finding. backfill/sparse
# keep their srid-on runners and oracles -- parity is the invariant there.
if not _SRID:
    FLAVORS.update(
        {
            "mv-identity": (
                lambda db, n, sh, sq: _run_mv_guard(db, n, sh, sq, False),
                [IDENTITY],
                [APPEND, DELETE, UPDATE, COMPACT, ADDCOL],
                set(),
            ),
            "mv-filtered": (
                lambda db, n, sh, sq: _run_mv_guard(db, n, sh, sq, False),
                [FILTERED],
                [APPEND, DELETE, UPDATE, COMPACT, ADDCOL],
                set(),
            ),
            "chunker": (
                lambda db, n, sh, sq: _run_chunker_guard(db, n, sh, sq),
                [IDENTITY],
                [APPEND, DELETE, UPDATE, COMPACT, MOVE],
                set(),
            ),
            "mvbf-identity": (
                lambda db, n, sh, sq: _run_mv_guard(db, n, sh, sq, True),
                [IDENTITY],
                [APPEND, DELETE, UPDATE, COMPACT],
                set(),
            ),
            "mvbf-filtered": (
                lambda db, n, sh, sq: _run_mv_guard(db, n, sh, sq, True),
                [FILTERED],
                [APPEND, DELETE, UPDATE, COMPACT],
                set(),
            ),
        }
    )


def _seqs(ops: list[str], max_len: int) -> list[tuple]:
    out: list[tuple] = []
    for length in range(1, max_len + 1):
        out.extend(itertools.product(ops, repeat=length))
    return out


def _process_batch(batch: list[tuple]) -> tuple[int, list[str]]:
    """Run a small batch of (flavor, shape, seq) cases. Each case gets its OWN
    tempdir + db, removed immediately after, so on-disk fragments and live lance
    dataset handles never accumulate. Workers are additionally recycled via
    ``maxtasksperchild`` to release in-process geneva/shim state. Bounding memory
    this way is what makes the exhaustive sweep practical.
    Returns (known_count, new_signatures)."""
    known = 0
    new: list[str] = []
    with Connection.local_ray_context():  # no-op under the shim
        for i, (flavor, shape, seq) in enumerate(batch):
            runner, _shapes, _ops, known_sigs = FLAVORS[flavor]
            name = f"{flavor[:6]}_{shape[:3]}_{i}"
            tmp = tempfile.mkdtemp(prefix="mvdiff_")
            try:
                r = runner(connect(tmp), name, shape, seq)
            except Exception as ex:  # noqa: BLE001
                r = f"NEW-CRASH: {type(ex).__name__}: {str(ex)[:120]}"
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            if r == "PASS":
                continue
            sig = r.split("@", 1)[0].split(":", 1)[0]
            if sig in known_sigs:
                known += 1
            else:
                new.append(f"{flavor}-{shape[:3]}-{''.join(seq)}: {r}")
    return known, new


def main() -> int:
    max_len = int(os.environ.get("GENEVA_MVDIFF_MAXLEN", "3"))
    workers = int(os.environ.get("SWEEP_WORKERS", str(min(8, os.cpu_count() or 2))))
    batch_size = int(os.environ.get("SWEEP_BATCH", "16"))
    recycle = int(os.environ.get("SWEEP_RECYCLE", "4"))  # batches per worker process
    only = os.environ.get("GENEVA_MVDIFF_FLAVORS")
    flavors = only.split(",") if only else list(FLAVORS)
    srid = "on" if _SRID else "off"

    unknown = [f for f in flavors if f not in FLAVORS]
    if unknown:
        print(f"unknown flavor(s) {unknown}; available: {sorted(FLAVORS)}")
        return 2

    cases: list[tuple] = []
    for flavor in flavors:
        _runner, shapes, ops, _known = FLAVORS[flavor]
        for shape in shapes:
            cases.extend((flavor, shape, seq) for seq in _seqs(ops, max_len))
    if not cases:
        # a "0 cases, no failures" exit would read as coverage; make it loud.
        print("no cases selected; check GENEVA_MVDIFF_FLAVORS / GENEVA_MVDIFF_MAXLEN")
        return 2
    batches = [cases[i : i + batch_size] for i in range(0, len(cases), batch_size)]
    print(
        f"=== shim sweep start: srid={srid} | {len(cases)} cases over "
        f"{len(flavors)} flavors | L<={max_len} | {workers} workers ===",
        flush=True,
    )

    known, new = 0, []
    # maxtasksperchild recycles a worker after `recycle` batches so accumulated
    # in-process state (lance buffers, geneva caches, the shim's asyncio loop) is
    # freed; combined with the per-case tempdir cleanup this caps peak memory.
    with mp.Pool(workers, maxtasksperchild=recycle) as pool:
        for k, n in pool.imap_unordered(_process_batch, batches):
            known += k
            new.extend(n)

    print(
        f"=== shim sweep: {len(cases)} cases over {len(flavors)} flavors "
        f"(L<={max_len}, {workers} workers, srid={srid}); "
        f"{known} known-bug, {len(new)} NEW ==="
    )
    for line in new[:50]:
        print(f"  NEW {line}")
    if not new:
        note = (
            ": all divergences are the known bug (GEN-611 chunker stale-on-update)"
            if known
            else ""
        )
        print(f"  no new-signature failures{note}")
    return 1 if new else 0


if __name__ == "__main__":
    mp.set_start_method("spawn")
    raise SystemExit(main())
