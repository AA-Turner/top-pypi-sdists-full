# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Executable form of the stable-row-ID invariant spec (GEN-842).

Every invariant in ``src/tests/stable_row_id_invariants.yaml`` has exactly one
test function here, registered by id. ``test_spec_and_registry_agree`` enforces
both directions, so an invariant cannot be documented without being checked and
a check cannot drift away from its documented statement.

Invariants marked ``status: broken`` in the spec run under
``xfail(strict=True)``: they fail today, and they will fail *the suite* the
moment an upstream fix lands, which is the signal to update the spec.

WHY THIS EXISTS
---------------
Geneva mixes two identity domains that look identical on the wire (both are
u64):

  * a **row address** -- ``fragment_id << 32 | offset`` -- which is physical and
    moves whenever compaction rewrites a fragment. Geneva's backfill engine is
    built entirely on this, deliberately (see SRID-G12).
  * a **stable row ID** -- a logical identity that survives compaction, update
    and rewrite, and only exists when the table was created with
    ``new_table_enable_stable_row_ids``. Geneva's materialized-view engine is
    built entirely on this.

When a table lacks stable row IDs, ``_rowid`` silently *is* the row address.
Nothing about the column type or name says so. Every bug in this family comes
from code that read one domain and assumed the other.

KNOWN DEFECTS THIS MODULE PINS
------------------------------
Left failing (xfail strict), with the tracker reference in the spec:

  SRID-L11  scalar-index scan after compaction raises an internal error
            on a stable-row-id dataset .......................... OSS-1607
            Lance-side; not fixable here.
  SRID-G09  __source_row_id is int64 against a u64 domain ........ GEN-852
            Fails loud rather than corrupting, and widening the column is a
            breaking schema change for existing views -- needs a migration.
  SRID-G14  chunker work items are not fragment-aligned under
            stable row IDs ................................ ....... GEN-853
            Locality only, not correctness.

Fixed in this branch, and now asserted rather than xfailed: SRID-G06, SRID-G07,
SRID-G08 (GEN-839), SRID-G10, SRID-G11. SRID-G03 is only PARTIALLY fixed -- the
baseline now advances, but the cross-version guard still raises ahead of it on a
non-SRID source, so ENT-2036 defect B's symptom survives; see the spec note.
SRID-G16 remains broken and is pinned in test_stable_row_id_mv.py.

Deliberately NOT hypothesis-driven: the op-sequence cases use fixed seeds
(``_SEQUENCE_SEEDS``) so a failure names a replayable sequence rather than a
shrink-dependent counterexample, and so this module carries no dependency that
``main`` does not already have.
"""

from __future__ import annotations

import contextlib
import random
import re
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any

import lance
import pyarrow as pa
import pytest
import yaml

from geneva import connect
from geneva.db import dataset_uses_stable_row_ids, has_stable_row_ids

if TYPE_CHECKING:
    from collections.abc import Callable

SPEC_PATH = Path(__file__).parent / "stable_row_id_invariants.yaml"

# Fixed seeds for the op-sequence driver. Six is enough to cover the
# interesting interleavings while staying inside make test-fast's budget.
_SEQUENCE_SEEDS = range(6)


# ---------------------------------------------------------------------------
# Spec loading
# ---------------------------------------------------------------------------


def _load_spec() -> dict[str, Any]:
    with SPEC_PATH.open() as f:
        return yaml.safe_load(f)


SPEC = _load_spec()
INVARIANTS: dict[str, dict[str, Any]] = {i["id"]: i for i in SPEC["invariants"]}

_REGISTRY: dict[str, Callable[[Path], None]] = {}

# Invariants owned by the Ray-marked MV suite rather than this module.
_OWNED_BY_MV_SUITE = {
    "SRID-G03",
    "SRID-G04",
    "SRID-G05",
    "SRID-G15",
    "SRID-G16",
}


def checks(
    invariant_id: str,
) -> Callable[[Callable[[Path], None]], Callable[[Path], None]]:
    """Register a function as the check for one spec invariant."""

    def deco(fn: Callable[[Path], None]) -> Callable[[Path], None]:
        if invariant_id in _REGISTRY:
            raise RuntimeError(f"duplicate check for {invariant_id}")
        _REGISTRY[invariant_id] = fn
        return fn

    return deco


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def make_rows(start: int, count: int) -> pa.Table:
    """Rows with a durable business key, so identity drift is observable."""
    return pa.table(
        {
            "key": pa.array(list(range(start, start + count)), pa.int64()),
            "cat": pa.array(
                ["A" if i % 3 == 0 else "B" for i in range(start, start + count)],
                pa.string(),
            ),
            "val": pa.array(
                [float(i) for i in range(start, start + count)], pa.float64()
            ),
        }
    )


def write_srid(
    uri: str, data: pa.Table, *, mode: str = "create", **kw: Any
) -> lance.LanceDataset:
    return lance.write_dataset(data, uri, mode=mode, enable_stable_row_ids=True, **kw)


def key_to_row_id(ds: lance.LanceDataset) -> dict[int, int]:
    """business key -> _rowid, the mapping every MV invariant is really about."""
    t = ds.to_table(columns=["key"], with_row_id=True)
    return dict(zip(t["key"].to_pylist(), t["_rowid"].to_pylist(), strict=True))


def compact(uri: str, target: int) -> lance.LanceDataset:
    ds = lance.dataset(uri)
    ds.optimize.compact_files(target_rows_per_fragment=target)
    return lance.dataset(uri)


# ---------------------------------------------------------------------------
# Fixture guard -- prove the matrix cell is what it claims before trusting it
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("stable", [True, False], ids=["srid-on", "srid-off"])
def test_fixture_is_what_it_claims_to_be(tmp_path: Path, stable: bool) -> None:
    """A green invariant test is worthless if the fixture silently lost SRID."""
    uri = str(tmp_path / "d.lance")
    ds = lance.write_dataset(
        make_rows(0, 20), uri, enable_stable_row_ids=stable, max_rows_per_file=10
    )
    assert ds.has_stable_row_ids is stable
    assert has_stable_row_ids(ds.get_fragments()) is stable
    assert dataset_uses_stable_row_ids(ds) is stable
    assert len(list(ds.get_fragments())) == 2
    if stable:
        assert all(f.metadata.row_id_meta is not None for f in ds.get_fragments())
    else:
        # Without SRID, _rowid IS the row address: fragment 1 starts at 1 << 32.
        ids = ds.to_table(columns=[], with_row_id=True)["_rowid"].to_pylist()
        assert ids[0] == 0
        assert ids[10] == 1 << 32, (
            "expected _rowid to be a physical address without stable row IDs"
        )


# ===========================================================================
# Lance layer
# ===========================================================================


@checks("SRID-L01")
def _l01(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 40), max_rows_per_file=10)
    before = set(key_to_row_id(ds).values())
    after = set(key_to_row_id(compact(uri, 100)).values())
    assert before == after, (
        f"compaction changed the live id set: lost={sorted(before - after)[:5]} "
        f"gained={sorted(after - before)[:5]}"
    )


@checks("SRID-L02")
def _l02(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 40), max_rows_per_file=10)
    before = key_to_row_id(ds)
    after = key_to_row_id(compact(uri, 100))
    drifted = {
        k: (before[k], after.get(k)) for k in before if after.get(k) != before[k]
    }
    assert not drifted, (
        f"{len(drifted)} keys changed row id across compaction: "
        f"{list(drifted.items())[:3]}"
    )


@checks("SRID-L03")
def _l03(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 30), max_rows_per_file=10)
    before = key_to_row_id(ds)
    ds.update({"val": "-1.0"}, where="cat = 'A'")
    after = key_to_row_id(lance.dataset(uri))
    drifted = {
        k: (before[k], after.get(k)) for k in before if after.get(k) != before[k]
    }
    assert not drifted, (
        f"update remapped {len(drifted)} rows: {list(drifted.items())[:3]}"
    )


@checks("SRID-L04")
def _l04(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 30), max_rows_per_file=10)
    before = key_to_row_id(ds)
    upd = pa.table(
        {
            "key": pa.array([1, 2, 3], pa.int64()),
            "cat": pa.array(["Z"] * 3, pa.string()),
            "val": pa.array([9.0] * 3, pa.float64()),
        }
    )
    (
        ds.merge_insert("key")
        .when_matched_update_all()
        .when_not_matched_insert_all()
        .execute(upd)
    )
    after = key_to_row_id(lance.dataset(uri))
    drifted = {
        k: (before[k], after.get(k)) for k in (1, 2, 3) if after.get(k) != before[k]
    }
    assert not drifted, f"merge_insert remapped matched rows: {drifted}"


@checks("SRID-L05")
def _l05(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 20), max_rows_per_file=10)
    retired = set(key_to_row_id(ds).values())
    ds.delete("key < 10")
    ds = write_srid(uri, make_rows(100, 10), mode="append")
    fresh = {rid for k, rid in key_to_row_id(ds).items() if k >= 100}
    assert not (fresh & retired), f"reused retired ids: {sorted(fresh & retired)[:5]}"
    assert min(fresh) >= max(retired), (
        f"new ids not allocated above the high-water mark: "
        f"min(new)={min(fresh)} max(previous)={max(retired)}"
    )


@checks("SRID-L06")
def _l06(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    write_srid(uri, make_rows(0, 20), max_rows_per_file=10)
    for i in range(1, 5):
        write_srid(uri, make_rows(100 * i, 10), mode="append")
    lance.dataset(uri).delete("key % 2 = 0")
    ds = compact(uri, 13)
    per_frag: dict[int, set[int]] = {}
    for frag in ds.get_fragments():
        ids = frag.to_table(columns=[], with_row_id=True)["_rowid"].to_pylist()
        assert len(ids) == len(set(ids)), (
            f"duplicate id within fragment {frag.fragment_id}"
        )
        per_frag[frag.fragment_id] = set(ids)
    frag_ids = list(per_frag)
    for i, a in enumerate(frag_ids):
        for b in frag_ids[i + 1 :]:
            shared = per_frag[a] & per_frag[b]
            assert not shared, (
                f"row id live in fragments {a} and {b}: {sorted(shared)[:5]}"
            )


@checks("SRID-L07")
def _l07(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 40), max_rows_per_file=10)
    before = key_to_row_id(ds)
    ds = compact(uri, 100)
    wanted_keys = [0, 7, 13, 39]
    got = ds._take_rows([before[k] for k in wanted_keys], columns=["key"])
    assert got["key"].to_pylist() == wanted_keys, (
        f"take by stable id after compaction returned {got['key'].to_pylist()}"
    )


@checks("SRID-L08")
def _l08(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 40), max_rows_per_file=10)
    ds.create_scalar_index("key", index_type="BTREE")
    ds = compact(uri, 100)
    assert ds.has_stable_row_ids, "manifest lost the flag across compaction"
    ds.optimize.optimize_indices()
    ds = lance.dataset(uri)
    assert ds.has_stable_row_ids, "manifest lost the flag across optimize_indices"
    assert all(f.metadata.row_id_meta is not None for f in ds.get_fragments()), (
        "a fragment lost row_id_meta"
    )


@checks("SRID-L09")
def _l09(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 30), max_rows_per_file=10)
    before = key_to_row_id(ds)
    ds.add_columns({"doubled": "val * 2"})
    after = key_to_row_id(lance.dataset(uri))
    drifted = {
        k: (before[k], after.get(k)) for k in before if after.get(k) != before[k]
    }
    assert not drifted, (
        f"add_columns remapped {len(drifted)} rows: {list(drifted.items())[:3]}"
    )


@checks("SRID-L10")
def _l10(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 100), max_rows_per_file=100)
    # Warm whatever per-fragment row-id-sequence cache exists before the
    # overwrite reuses fragment id 0 (the OSS-1606 shape).
    assert ds.count_rows("key >= 0") == 100
    ds = write_srid(uri, make_rows(0, 60), mode="overwrite")
    assert ds.count_rows() == 60
    write_srid(uri, make_rows(0, 100), mode="append")
    ds = compact(uri, 200)
    assert ds.count_rows() == 160, (
        f"row count {ds.count_rows()} after overwrite+compact"
    )
    ids = ds.to_table(columns=[], with_row_id=True)["_rowid"].to_pylist()
    assert len(ids) == 160, f"scan produced {len(ids)} ids for 160 rows"
    assert len(set(ids)) == len(ids), "duplicate stable row ids after overwrite"


@checks("SRID-L11")
def _l11(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    write_srid(uri, make_rows(0, 100), max_rows_per_file=100)
    ds = write_srid(uri, make_rows(100, 100), mode="append")
    ds.create_scalar_index("key", index_type="ZONEMAP")
    ds = compact(uri, 500)
    n = ds.to_table(filter="key > 0").num_rows
    assert n == 199, f"filtered scan through the zone map returned {n}, expected 199"


@checks("SRID-L12")
def _l12(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 30), max_rows_per_file=10)
    at_v1 = key_to_row_id(ds)
    write_srid(uri, make_rows(100, 10), mode="append")
    lance.dataset(uri).delete("key = 5")
    at_v2 = key_to_row_id(compact(uri, 100))

    id_to_key_v1 = {rid: k for k, rid in at_v1.items()}
    id_to_key_v2 = {rid: k for k, rid in at_v2.items()}
    survivors = set(id_to_key_v1) & set(id_to_key_v2)
    assert survivors, "no ids survived to the later version"
    changed = {
        rid: (id_to_key_v1[rid], id_to_key_v2[rid])
        for rid in survivors
        if id_to_key_v1[rid] != id_to_key_v2[rid]
    }
    assert not changed, (
        f"row id now denotes a different logical row: {list(changed.items())[:3]}"
    )
    assert at_v1[5] not in id_to_key_v2, "the deleted row's id is still live at v2"


@checks("SRID-L13")
def _l13(tmp: Path) -> None:
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 1).schema.empty_table())
    assert ds.count_rows() == 0
    assert ds.has_stable_row_ids, "manifest flag absent on an empty SRID table"


@checks("SRID-L14")
def _l14(tmp: Path) -> None:
    """Pins the SHAPE of a short take -- the hazard behind SRID-G11."""
    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 20), max_rows_per_file=10)
    m = key_to_row_id(ds)
    ds.delete("key = 3")
    ds = lance.dataset(uri)
    requested = [m[1], m[3], m[2]]
    got = ds._take_rows(requested, columns=["key"])
    assert got.num_rows == 2, (
        f"expected a short take of 2 rows, got {got.num_rows}; if Lance now "
        "emits a null placeholder for missing ids, SRID-G11 may be fixed"
    )
    assert got["key"].to_pylist() == [1, 2], got["key"].to_pylist()
    # The point: the caller cannot tell from the result WHICH id dropped out,
    # so a positional join against `requested` shifts every row after the hole.
    assert len(requested) != got.num_rows


@checks("SRID-L15")
def _l15(tmp: Path) -> None:
    """Pins that scan order is NOT ascending by row id -- see SRID-G14."""
    uri = str(tmp / "d.lance")
    write_srid(uri, make_rows(0, 20), max_rows_per_file=10)
    for i in range(1, 4):
        write_srid(uri, make_rows(100 * i, 10), mode="append")
    lance.dataset(uri).delete("key % 3 = 0")
    ds = compact(uri, 7)
    order = ds.to_table(columns=[], with_row_id=True)["_rowid"].to_pylist()
    assert order != sorted(order), (
        "scan order is now ascending by row id; if Lance guarantees this, "
        "pipeline.py:6833's fragment-locality sort becomes valid and SRID-G14 "
        "can be closed"
    )


# ===========================================================================
# Geneva layer
# ===========================================================================


@checks("SRID-G01")
def _g01(tmp: Path) -> None:
    db = connect(tmp)
    for i, truthy in enumerate([True, "true", 1]):
        tbl = db.create_table(
            f"t{i}",
            make_rows(0, 5),
            storage_options={"new_table_enable_stable_row_ids": truthy},
        )
        ds = tbl.to_lance()
        assert ds.has_stable_row_ids, f"{truthy!r} did not enable stable row IDs"
    plain = db.create_table("plain", make_rows(0, 5))
    assert not plain.to_lance().has_stable_row_ids


@checks("SRID-G02")
def _g02(tmp: Path) -> None:
    from geneva.query import MATVIEW_META_VERSION

    db = connect(tmp)
    for name, stable, expected in [("src_on", True, "2"), ("src_off", False, "1")]:
        opts = {"new_table_enable_stable_row_ids": "true"} if stable else {}
        tbl = db.create_table(name, make_rows(0, 10), storage_options=opts)
        # Creating an MV over a source without stable row IDs must warn that
        # refresh is pinned to the creation version.
        warns = (
            pytest.warns(UserWarning, match="without stable row IDs")
            if not stable
            else contextlib.nullcontext()
        )
        with warns:
            view = (
                tbl.search(None)
                .select(["key"])
                .create_materialized_view(db, f"mv_{name}")
            )
        md = {
            (k.decode() if isinstance(k, bytes) else k): (
                v.decode() if isinstance(v, bytes) else v
            )
            for k, v in (view.to_lance().schema.metadata or {}).items()
        }
        assert md.get(MATVIEW_META_VERSION) == expected, (
            f"source stable={stable} produced MV version "
            f"{md.get(MATVIEW_META_VERSION)!r}, expected {expected!r}"
        )


@checks("SRID-G06")
def _g06(tmp: Path) -> None:
    """An empty stable-row-id table must be detected as having them.

    Asserts the behaviour of the path Geneva actually uses, not that the
    fragment-only helper is clairvoyant: with zero fragments it cannot be, which
    is exactly why the call sites read the manifest instead.

    Scope: the exist_ok validator is the only call site pinned here.
    create_materialized_view rejects empty sources before its stable-row-id
    check, so on a zero-fragment table -- the one case where the fragment and
    manifest helpers disagree -- its manifest read is unreachable and there is
    nothing to assert.
    """
    db = connect(tmp)
    opts = {"new_table_enable_stable_row_ids": "true"}
    tbl = db.create_table(
        "empty_srid", make_rows(0, 1).schema.empty_table(), storage_options=opts
    )
    ds = tbl.to_lance()
    assert ds.count_rows() == 0
    assert not list(ds.get_fragments()), "expected a table with no fragments"
    assert dataset_uses_stable_row_ids(ds), "manifest must report stable row IDs"

    # exist_ok validation must not silently skip just because there are no
    # fragments to look at.
    db.create_table(
        "empty_srid",
        make_rows(0, 1).schema.empty_table(),
        storage_options=opts,
        exist_ok=True,
    )

    # ...and must still reject a table that genuinely lacks them.
    db.create_table("empty_plain", make_rows(0, 1).schema.empty_table())
    with pytest.raises(ValueError, match="does not have stable row IDs enabled"):
        db.create_table(
            "empty_plain",
            make_rows(0, 1).schema.empty_table(),
            storage_options=opts,
            exist_ok=True,
        )


@checks("SRID-G07")
def _g07(tmp: Path) -> None:
    """Same as G06, reached by emptying a populated table rather than by
    creating an empty one -- no "empty source" guard applies on this route."""
    db = connect(tmp)
    opts = {"new_table_enable_stable_row_ids": "true"}
    tbl = db.create_table("drained", make_rows(0, 10), storage_options=opts)
    tbl.delete("key >= 0")
    tbl.checkout_latest()

    ds = tbl.to_lance()
    assert ds.count_rows() == 0
    assert not list(ds.get_fragments()), "expected every fragment to be dropped"
    assert dataset_uses_stable_row_ids(ds), (
        "a drained table still has stable row IDs on its manifest"
    )
    # The fragment-based helper is the one that gets this wrong -- that asymmetry
    # is the defect, so pin it rather than asserting the two agree.
    assert not has_stable_row_ids(ds.get_fragments()), (
        "expected the fragment-based helper to report False on zero fragments; if "
        "it no longer does, this invariant and GEN-856 both need revisiting"
    )
    db.create_table(
        "drained",
        make_rows(0, 1).schema.empty_table(),
        storage_options=opts,
        exist_ok=True,
    )

    # The negative half: a drained table that genuinely lacks stable row IDs must
    # still be rejected. Without this the check passes with its own fix reverted,
    # because the old code path also let the positive case through -- by skipping
    # validation entirely rather than by getting the answer right.
    plain = db.create_table("plain_drained", make_rows(0, 10))
    plain.delete("key >= 0")
    plain.checkout_latest()
    assert not list(plain.to_lance().get_fragments())
    with pytest.raises(ValueError, match="does not have stable row IDs enabled"):
        db.create_table(
            "plain_drained",
            make_rows(0, 1).schema.empty_table(),
            storage_options=opts,
            exist_ok=True,
        )


@checks("SRID-G08")
def _g08(tmp: Path) -> None:
    from geneva.db import Connection, NamespaceConfig

    def supports(impl: str | None, props: dict[str, str] | None) -> bool:
        conn = Connection.__new__(Connection)
        conn._ns_config = NamespaceConfig(
            namespace_client_impl=impl, namespace_client_properties=props
        )
        return conn._supports_stable_row_ids_on_create()

    # Sanity: the two backends the method already gets right.
    assert supports(None, None), "local connections must support it"
    assert supports("dir", {"root": str(tmp)}), "directory namespaces must support it"

    assert supports("rest", {"uri": "http://127.0.0.1:1"}), (
        "rest namespaces must be reported as able to enable stable row IDs on "
        "create -- they reach storage through a LanceNamespaceDBConnection that "
        "honours the per-request option. Reporting False here builds every "
        "enterprise MV table without stable row IDs, unrepairably (GEN-839)."
    )


@checks("SRID-G09")
def _g09(tmp: Path) -> None:
    """The MV __source_row_id column must span the full u64 row-id domain.

    Asserts the materialized column type on a real view. The previous version
    asserted only that pyarrow rejects a u64 -> int64 cast and named no Geneva
    symbol at all, so GEN-852 could widen every declaration in src/geneva without
    this check moving -- the exact defect SRID-G11's docstring calls out.
    """
    # The domain problem, documented: the cast fails loud rather than wrapping.
    with pytest.raises(pa.ArrowInvalid):
        pa.array([2**63 + 5], pa.uint64()).cast(pa.int64())

    db = connect(tmp)
    src = db.create_table(
        "g09_src",
        make_rows(0, 4),
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )
    view = src.search(None).select(["val"]).create_materialized_view(db, "g09_view")
    actual = view.to_lance().schema.field("__source_row_id").type
    assert actual == pa.uint64(), (
        f"MV __source_row_id is {actual}, not uint64. Row ids are u64, so the top "
        f"half of the domain is unrepresentable -- casting id 2**63+5 into "
        f"{actual} raises ArrowInvalid. Fails loud rather than corrupting, and "
        "widening it is a breaking schema change for existing views (GEN-852)."
    )


@checks("SRID-G10")
def _g10(tmp: Path) -> None:
    """geneva/query.py declares _rowaddr as int64; Lance emits uint64."""
    from geneva.query import GenevaQueryBuilder

    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 5))
    lance_type = (
        ds.to_table(columns=[], with_row_address=True).schema.field("_rowaddr").type
    )
    assert lance_type == pa.uint64(), lance_type

    declared = None
    for src_field in _declared_metacol_fields(GenevaQueryBuilder):
        if src_field.name == "_rowaddr":
            declared = src_field.type
    assert declared is not None, "could not locate the declared _rowaddr metacol field"
    assert declared == lance_type, (
        f"geneva/query.py declares _rowaddr as {declared}, Lance emits "
        f"{lance_type}; every other Geneva site uses uint64"
    )

    # "everywhere" is part of the statement, so scan the whole package rather
    # than trusting query.py to be the only offender -- an int64 declaration in
    # apply/ or runners/ would otherwise pass this check unnoticed.
    import geneva

    root = Path(geneva.__file__).parent
    offenders = [
        f"{py.relative_to(root)}: pa.{m.group(1)}()"
        for py in sorted(root.rglob("*.py"))
        for m in re.finditer(
            r'pa\.field\(\s*"_rowaddr"\s*,\s*pa\.(\w+)\(\)', py.read_text()
        )
        if m.group(1) != "uint64"
    ]
    assert not offenders, (
        "_rowaddr must be declared uint64 at every Geneva site, matching the "
        f"column Lance emits; found {offenders}"
    )


def _declared_metacol_fields(cls: type) -> list[pa.Field]:
    """Pull the literal pa.field(...) metacol declarations out of query.py."""
    import ast
    import inspect

    src = inspect.getsource(inspect.getmodule(cls))
    out: list[pa.Field] = []
    for node in ast.walk(ast.parse(src)):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "field"
            and len(node.args) == 2
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value in ("_rowaddr", "_rowid")
        ):
            continue
        type_src = ast.unparse(node.args[1])
        if type_src.endswith("()") and hasattr(pa, type_src[3:-2]):
            out.append(pa.field(node.args[0].value, getattr(pa, type_src[3:-2])()))
    return out


@checks("SRID-G11")
def _g11(tmp: Path) -> None:
    """A short take must not shift values onto the wrong destination rows.

    Exercises the real alignment helper that ``CopyTask.to_batches`` uses --
    an earlier version of this test replayed the logic inline, which meant
    fixing the production path could not turn it green.
    """
    from geneva.apply.task import align_dst_row_addrs, take_columns_with_rowid

    uri = str(tmp / "d.lance")
    ds = write_srid(uri, make_rows(0, 20), max_rows_per_file=10)
    m = key_to_row_id(ds)
    ds.delete("key = 3")
    ds = lance.dataset(uri)

    # What CopyTask reads out of the destination fragment: stored source row
    # ids paired positionally with the physical destination slots.
    requested = [m[1], m[3], m[2]]
    dst_row_addrs = pa.array([1001, 1003, 1002], pa.uint64())

    # The take carries its own survivor list back, so realigning costs no extra
    # read of the source. Projecting _rowid must not disturb request order.
    take_columns, added = take_columns_with_rowid(["key"])
    assert (take_columns, added) == (["_rowid", "key"], True)
    taken = ds._take_rows(requested, columns=take_columns)
    assert taken["_rowid"].to_pylist() == [m[1], m[2]], (
        "the take must report the surviving ids in request order; alignment "
        "reads them straight out of the result"
    )

    aligned = align_dst_row_addrs(
        requested,
        taken.num_rows,
        dst_row_addrs,
        taken_row_ids=taken["_rowid"],
    )

    landed = dict(zip(taken["key"].to_pylist(), aligned.to_pylist(), strict=True))
    assert landed == {1: 1001, 2: 1002}, (
        f"source keys landed in destination slots {landed}, expected "
        "{1: 1001, 2: 1002}. The take dropped the MIDDLE id, so trimming the "
        "tail would put key 2's value in key 3's physical slot."
    )

    # The full-length case must be untouched, and must not touch the source at
    # all -- passing no dataset and no ids proves it short-circuits first.
    full = pa.array([1001, 1002, 1003], pa.uint64())
    assert align_dst_row_addrs(requested, 3, full) is full

    # An address-domain source cannot project _rowid across deleted rows, so it
    # falls back to scanning. Same answer, and the only path that pays for one.
    ns_uri = str(tmp / "ns.lance")
    ns = lance.write_dataset(make_rows(0, 20), ns_uri, max_rows_per_file=10)
    assert not ns.has_stable_row_ids
    ns_m = key_to_row_id(ns)
    ns.delete("key = 3")
    ns = lance.dataset(ns_uri)
    ns_requested = [ns_m[1], ns_m[3], ns_m[2]]
    with pytest.raises(OSError, match="must not target deleted rows"):
        ns._take_rows(ns_requested, columns=take_columns_with_rowid(["key"])[0])
    ns_taken = ns._take_rows(ns_requested, columns=["key"])
    assert align_dst_row_addrs(
        ns_requested, ns_taken.num_rows, dst_row_addrs, dataset=ns
    ).to_pylist() == [1001, 1002]

    # If the counts still cannot be reconciled, refuse rather than guess.
    with pytest.raises(ValueError, match="Refusing to write values"):
        align_dst_row_addrs(requested, 1, dst_row_addrs, taken_row_ids=taken["_rowid"])

    # With no way to identify survivors, refuse rather than trim the tail.
    with pytest.raises(ValueError, match="Refusing to write values"):
        align_dst_row_addrs(requested, 2, dst_row_addrs)

    # Production passes a ChunkedArray, not an Array (the _rowaddr column of a
    # scanner result). The helper must not care.
    chunked = pa.chunked_array([pa.array([1001, 1003], pa.uint64())])
    assert align_dst_row_addrs(
        [m[1], m[3]], 1, chunked, taken_row_ids=pa.array([m[1]], pa.uint64())
    ).to_pylist() == [1001]

    # A chunker view repeats __source_row_id once per chunk. Duplicates survive
    # or drop as a group, so every slot of a live id must be kept.
    dup_requested = [m[1], m[3], m[1], m[2]]
    dup_addrs = pa.array([2001, 2003, 2002, 2004], pa.uint64())
    assert align_dst_row_addrs(
        dup_requested,
        3,
        dup_addrs,
        taken_row_ids=pa.array([m[1], m[1], m[2]], pa.uint64()),
    ).to_pylist() == [2001, 2002, 2004]

    # Expression projections are dicts, not lists; _rowid has to land there too.
    assert take_columns_with_rowid({"doubled": "val * 2"}) == (
        {"_rowid": "_rowid", "doubled": "val * 2"},
        True,
    )
    # Already-projected _rowid is left alone, and must NOT be dropped afterwards.
    assert take_columns_with_rowid(["_rowid", "key"]) == (["_rowid", "key"], False)

    # Both arms of the SRID gate in to_batches, through the production path.
    _g11_through_copytask(tmp, stable=True)
    _g11_through_copytask(tmp, stable=False)


def _g11_through_copytask(tmp: Path, *, stable: bool) -> None:
    """Same invariant, driven through CopyTask.to_batches rather than the helper.

    The helper-level assertions above cannot see the call site. Reverting
    apply/task.py to the old ``slice(0, table.num_rows)`` leaves every one of them
    green, so without this the branch's headline correctness fix is unguarded
    exactly where it matters (GEN-619 is the same wrong-slot/NULL-gap symptom).

    Run for BOTH domains, because to_batches branches on the source: a stable-row-id
    source reads its survivors out of the take's own _rowid column, an address-domain
    one falls back to scanning. Each arm is only reachable from one of these calls,
    and ``scans`` pins which one paid for a scan -- otherwise inverting the gate, or
    dropping the fallback's dataset argument, leaves the suite green while either
    re-introducing the rescan this change exists to remove or breaking the fallback.
    """
    import geneva.apply.task as task_mod
    from geneva.apply.task import CopyTask

    db = connect(tmp / f"copytask_db_{'srid' if stable else 'addr'}")
    src = db.create_table(
        "ct_src",
        make_rows(0, 6),
        storage_options={"new_table_enable_stable_row_ids": "true"} if stable else None,
    )
    assert src.to_lance().has_stable_row_ids is stable, (
        "fixture did not produce the intended row-id domain, so this call would "
        "silently exercise the same to_batches arm as the other one"
    )
    # Creation pre-populates one placeholder row per source row, carrying
    # __source_row_id -- which is what CopyTask reads back out.
    view = src.search(None).select(["val"]).create_materialized_view(db, "ct_view")

    # Drop a source row that is NOT last, so a tail trim misaligns everything
    # after the hole instead of harmlessly dropping the final entry.
    src.delete("key = 2")
    src.checkout_latest()

    task = CopyTask(
        src=src.get_reference(),
        dst=view.get_reference(),
        columns=["val"],
        frag_id=0,
        offset=0,
        limit=0,
    )

    scans = 0
    real_live_row_ids = task_mod._live_row_ids

    def counting_live_row_ids(dataset: Any, row_ids: list[int]) -> set[int]:
        nonlocal scans
        scans += 1
        return real_live_row_ids(dataset, row_ids)

    task_mod._live_row_ids = counting_live_row_ids
    try:
        batches = list(task.to_batches())
    finally:
        task_mod._live_row_ids = real_live_row_ids

    landed = {
        val: addr
        for batch in batches
        for val, addr in zip(
            batch["val"].to_pylist(), batch["_rowaddr"].to_pylist(), strict=True
        )
    }

    # val == key for make_rows, and the MV placeholders are created in source
    # order, so surviving key k belongs in destination slot k.
    expected = {float(k): k for k in (0, 1, 3, 4, 5)}
    assert landed == expected, (
        f"CopyTask placed source values in destination slots {landed}, expected "
        f"{expected}. Key 2 was deleted mid-list, so trimming the tail off "
        "dst_row_addrs shifts every later value onto its predecessor's row."
    )

    # A stable-row-id source must realign from the take it already paid for. This
    # is the whole point of projecting _rowid: no second pass over the source.
    if stable:
        assert scans == 0, (
            f"CopyTask scanned the source {scans}x to realign a short take on a "
            "stable-row-id source; the take's own _rowid column already says which "
            "ids survived, so this is the expensive path the projection replaced"
        )
    else:
        assert scans == 1, (
            f"expected exactly one fallback scan on an address-domain source, got "
            f"{scans}. Lance refuses to project _rowid across deleted rows there, "
            "so the scan is the only way to identify survivors"
        )

    # _rowid is projected only to identify survivors; it must not reach the
    # writer as an extra column the destination schema never declared.
    for batch in batches:
        assert "_rowid" not in batch.schema.names, (
            f"CopyTask leaked the alignment probe column into its output: "
            f"{batch.schema.names}"
        )


@checks("SRID-G12")
def _g12(tmp: Path) -> None:
    """Backfill checkpoint keys are address-domain, by design."""
    from geneva.checkpoint_utils import format_checkpoint_key

    key = format_checkpoint_key("udf-x_ver-1", frag_id=7, start=100, end=200)
    assert key == "udf-x_ver-1_frag-7_range-100-200", key
    assert "frag-7" in key, "fragment id is load-bearing in the checkpoint key"

    from geneva.checkpoint import parse_frag_id_from_checkpoint_key

    assert parse_frag_id_from_checkpoint_key(key) == 7


@checks("SRID-G13")
def _g13(tmp: Path) -> None:
    """No retrofit: an existing table cannot gain stable row IDs.

    Pinned as by-design. If Lance ever adds a migration and this starts
    passing, Geneva should expose it (ENT-2072) and the spec entry should move
    from by-design to holds.
    """
    db = connect(tmp)
    tbl = db.create_table("t", make_rows(0, 10))
    assert not tbl.to_lance().has_stable_row_ids

    # Asking for stable row IDs on an existing table without them is refused
    # rather than quietly upgrading it.
    with pytest.raises(ValueError, match="does not have stable row IDs enabled"):
        db.create_table(
            "t",
            make_rows(0, 10),
            storage_options={"new_table_enable_stable_row_ids": "true"},
            exist_ok=True,
        )

    assert not db.open_table("t").to_lance().has_stable_row_ids, (
        "the table gained stable row IDs in place -- a retrofit path now exists "
        "and Geneva should expose it (ENT-2072)"
    )


def _fragment_runs(order: list[int], frag_of: dict[int, int]) -> tuple[int, int]:
    """(fragment runs, distinct fragments) for a work-item ordering.

    One run per fragment is optimal; any excess is a fragment the actor pool
    opens, leaves, and comes back to.
    """
    seq = [frag_of[rid] for rid in order]
    runs = 1 + sum(1 for a, b in zip(seq, seq[1:], strict=False) if a != b)
    return runs, len({*seq})


@checks("SRID-G14")
def _g14(tmp: Path) -> None:
    """Chunker work items must be fragment-aligned.

    Note what this does NOT assert: that sorting by row id is fragment-aligned.
    It isn't, it cannot be made to be, and the earlier version of this check
    asserted exactly that -- pinning a false Lance premise rather than the
    Geneva code standing on it, so the only way to turn it green was upstream.

    A plain append/delete/compact sequence happens to stay aligned, because
    compaction hands each output fragment a contiguous id range. The premise
    breaks once an **update** has moved low-id rows into a late fragment and
    compaction then merges that fragment with a high-id one: the fragment now
    owns two disjoint id ranges, and sorting by id revisits it twice.

    So _append_expanded_fragments no longer sorts. It accumulates one fragment
    at a time, which is aligned by construction; this pins that ordering, and
    pins that the discarded sort really was worse on the same data.
    """
    uri = str(tmp / "d.lance")
    write_srid(uri, make_rows(0, 10), max_rows_per_file=10)
    for i in range(1, 4):
        write_srid(uri, make_rows(100 * i, 10), mode="append")
    # Rewrites the first fragment's low-id rows into a brand new late fragment,
    # keeping their original (low) stable row ids.
    lance.dataset(uri).update({"val": "-1.0"}, where="key < 5")
    ds = compact(uri, 12)

    frag_of: dict[int, int] = {}
    per_fragment: list[list[int]] = []
    for frag in ds.get_fragments():
        ids: list[int] = frag.to_table(columns=[], with_row_id=True)[
            "_rowid"
        ].to_pylist()
        per_fragment.append(ids)
        for rid in ids:
            frag_of[rid] = frag.fragment_id

    # How _append_expanded_fragments builds all_new_row_ids: one fragment's ids
    # appended at a time, in fragment iteration order, no global sort.
    accumulated = [rid for ids in per_fragment for rid in ids]
    runs, n_frags = _fragment_runs(accumulated, frag_of)
    assert runs == n_frags, (
        f"accumulating {len(frag_of)} work items fragment-by-fragment produced "
        f"{runs} fragment runs across {n_frags} fragments, so {runs - n_frags} "
        f"fragment(s) are visited more than once. Layout: "
        f"{[frag_of[r] for r in accumulated]}"
    )

    # And the sort that used to follow it was measurably worse on this data, so
    # restoring it cannot look like a no-op refactor.
    sorted_runs, sorted_frags = _fragment_runs(sorted(frag_of), frag_of)
    assert sorted_runs > sorted_frags, (
        "sorting work items by row id is fragment-aligned on this sequence, so "
        "this check no longer demonstrates why _append_expanded_fragments must "
        "not sort. Make the fixture adversarial again (update + compact, so one "
        "fragment owns two disjoint id ranges) or retire the invariant."
    )

    # The production path must not reintroduce it. Parsed, not grepped: the file
    # explains the deleted sort in a comment, and a substring check cannot tell
    # that prose from a live call. Read as source rather than importing
    # runners.ray.pipeline, which would pull Ray into a suite kept deliberately
    # Ray-free so it can live in make test-fast.
    assert _sorts_work_items("_append_expanded_fragments") is None, (
        f"_append_expanded_fragments sorts its work items by row id again "
        f"({_sorts_work_items('_append_expanded_fragments')}), which costs "
        f"{sorted_runs - sorted_frags} extra fragment visit(s) on this fixture; "
        "stable row ids do not encode fragment_id (SRID-G14, GEN-853)"
    )


def _sorts_work_items(func_name: str, var: str = "all_new_row_ids") -> str | None:
    """Describe how *func_name* sorts *var*, or None if it does not.

    Catches both `var.sort()` and `var = sorted(var)`.
    """
    import ast

    import geneva

    src = (Path(geneva.__file__).parent / "runners" / "ray" / "pipeline.py").read_text()
    func = next(
        (
            n
            for n in ast.walk(ast.parse(src))
            if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef)
            and n.name == func_name
        ),
        None,
    )
    assert func is not None, f"{func_name} no longer exists in pipeline.py"
    for node in ast.walk(func):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if (
            isinstance(f, ast.Attribute)
            and f.attr == "sort"
            and isinstance(f.value, ast.Name)
            and f.value.id == var
        ):
            return f"{var}.sort() at line {node.lineno}"
        if (
            isinstance(f, ast.Name)
            and f.id == "sorted"
            and node.args
            and isinstance(node.args[0], ast.Name)
            and node.args[0].id == var
        ):
            return f"sorted({var}) at line {node.lineno}"
    return None


# ---------------------------------------------------------------------------
# Seeded op-sequence driver -- the stateful half
# ---------------------------------------------------------------------------

_OPS = ("append", "delete", "update", "compact", "add_column")


@pytest.mark.parametrize("seed", _SEQUENCE_SEEDS)
def test_row_identity_survives_random_op_sequences(tmp_path: Path, seed: int) -> None:
    """The core Geneva contract, under seeded interleavings of every op.

    Shadow oracle: ``key -> row_id`` for every row ever written. Any op that
    changes an existing key's row id, or resurrects a deleted one, is a
    violation. Failure messages carry the full op log so the case replays.
    """
    rng = random.Random(seed)
    uri = str(tmp_path / "d.lance")
    log: list[str] = []

    write_srid(uri, make_rows(0, 12), max_rows_per_file=5)
    log.append("write(0,12)")
    oracle = dict(key_to_row_id(lance.dataset(uri)))
    retired: set[int] = set()
    next_key = 100
    added_columns = 0

    def context(note: str) -> str:
        return f"seed={seed} note={note}\n  ops: {' -> '.join(log)}"

    for _ in range(10):
        op = rng.choice(_OPS)
        ds = lance.dataset(uri)
        live_keys = sorted(key_to_row_id(ds))

        if op == "append":
            n = rng.randint(1, 6)
            write_srid(uri, make_rows(next_key, n), mode="append")
            log.append(f"append({next_key},{n})")
            next_key += 100
        elif op == "delete" and live_keys:
            victim = rng.choice(live_keys)
            retired.add(oracle[victim])
            ds.delete(f"key = {victim}")
            log.append(f"delete(key={victim})")
        elif op == "update" and live_keys:
            victim = rng.choice(live_keys)
            ds.update({"val": "-42.0"}, where=f"key = {victim}")
            log.append(f"update(key={victim})")
        elif op == "compact":
            target = rng.choice([3, 7, 50])
            ds.optimize.compact_files(target_rows_per_fragment=target)
            log.append(f"compact({target})")
        elif op == "add_column":
            added_columns += 1
            ds.add_columns({f"c{added_columns}": "val * 2"})
            log.append(f"add_column(c{added_columns})")
        else:
            continue

        current = key_to_row_id(lance.dataset(uri))

        drifted = {
            k: (oracle[k], current[k])
            for k in current
            if k in oracle and current[k] != oracle[k]
        }
        assert not drifted, (
            f"row id changed for surviving keys {list(drifted.items())[:3]}\n"
            + context(f"after {log[-1]}")
        )

        resurrected = set(current.values()) & retired
        assert not resurrected, (
            f"retired row ids came back live: {sorted(resurrected)[:5]}\n"
            + context(f"after {log[-1]}")
        )

        ids = list(current.values())
        assert len(ids) == len(set(ids)), "duplicate live row ids\n" + context(
            f"after {log[-1]}"
        )

        oracle.update(current)

    final = lance.dataset(uri)
    assert final.has_stable_row_ids, "manifest lost the stable-row-id flag\n" + context(
        "final"
    )


# ---------------------------------------------------------------------------
# Spec-driven dispatch
# ---------------------------------------------------------------------------


def _params() -> list[Any]:
    out = []
    for inv_id, inv in INVARIANTS.items():
        if inv_id in _OWNED_BY_MV_SUITE:
            continue
        marks = []
        if inv["status"] == "broken":
            bug = inv.get("bug") or "DRAFT (unfiled)"
            marks.append(
                pytest.mark.xfail(
                    strict=True,
                    reason=f"{inv_id} is a known defect: {bug}",
                )
            )
        out.append(pytest.param(inv_id, marks=marks, id=inv_id))
    return out


@pytest.mark.parametrize("invariant_id", _params())
def test_invariant(invariant_id: str, tmp_path: Path) -> None:
    """Run the registered check for one spec invariant."""
    inv = INVARIANTS[invariant_id]
    check = _REGISTRY.get(invariant_id)
    assert check is not None, f"no check registered for {invariant_id}"
    try:
        check(tmp_path)
    except AssertionError as exc:
        raise AssertionError(
            f"{invariant_id} [{inv['layer']}/{inv['severity']}] violated.\n"
            f"  statement: {inv['statement'].strip()}\n"
            f"  geneva depends on: {inv['geneva_depends_on'].strip()}\n"
            f"  detail: {exc}"
        ) from exc


def test_spec_and_registry_agree() -> None:
    """No invariant documented without a check; no check without an invariant.

    The MV-suite half is read from that module's ``COVERS`` map, which points at
    the actual test functions. ``_OWNED_BY_MV_SUITE`` alone could not tell that a
    test it claimed coverage from had been renamed or deleted, so the spec would
    have gone on asserting coverage for nothing.
    """
    from test_stable_row_id_mv import COVERS as MV_COVERS

    assert set(MV_COVERS) == _OWNED_BY_MV_SUITE, (
        "the MV suite's COVERS map and _OWNED_BY_MV_SUITE have drifted: "
        f"only in COVERS {sorted(set(MV_COVERS) - _OWNED_BY_MV_SUITE)}, "
        f"only in the set {sorted(_OWNED_BY_MV_SUITE - set(MV_COVERS))}"
    )
    for inv_id, fn in MV_COVERS.items():
        assert callable(fn), f"{inv_id} maps to {fn!r}, not a test function"

    documented = set(INVARIANTS)
    checked = set(_REGISTRY) | set(MV_COVERS)
    assert documented == checked, (
        f"documented but unchecked: {sorted(documented - checked)}\n"
        f"checked but undocumented: {sorted(checked - documented)}"
    )


def test_spec_records_which_builds_it_was_measured_on() -> None:
    """A status is only meaningful next to the build it was measured against."""
    measured = SPEC["measured_on"]
    assert isinstance(measured, list), "measured_on must be a list of builds"
    assert measured, "measured_on must name at least one build"
    for entry in measured:
        assert "pylance==" in entry, f"no pylance version in {entry!r}"
        assert "lancedb==" in entry, f"no lancedb version in {entry!r}"


def test_status_totals_are_what_the_write_ups_claim() -> None:
    """A tripwire so the spec, the PR body and the Notion page move together.

    These totals are quoted outside this repo. Changing a status is legitimate --
    silently leaving the prose saying something else is not.
    """
    counts = Counter(inv["status"] for inv in SPEC["invariants"])
    expected = {"holds": 24, "by-design": 4, "broken": 3}
    assert dict(counts) == expected, (
        f"invariant status totals are now {dict(counts)}, not {expected}. If that "
        "is intended, update this test, the PR body's 'Results' section and the "
        "Notion write-up in the same change."
    )


def test_spec_cites_symbols_not_line_numbers() -> None:
    """Citations must survive an unrelated edit to the file they point at.

    An executable spec is only worth as much as its pointers. Bare ``file.py:123``
    references rot on the next diff -- roughly a third of them were already stale
    by the time this spec first landed, several broken by its own changes. Name
    the function or method instead.
    """
    stale = [
        f"{inv['id']}.{field}: {hit}"
        for inv in SPEC["invariants"]
        for field in ("statement", "geneva_depends_on", "note")
        for hit in re.findall(r"[\w./]+\.py:\d+(?:-\d+)?", inv.get(field) or "")
    ]
    assert not stale, (
        "cite a function or method name, not a line number:\n  " + "\n  ".join(stale)
    )


def test_spec_citations_resolve_to_real_symbols() -> None:
    """Every ``symbol (file.py)`` citation must resolve against src/geneva.

    The line-number ban above is necessary but not sufficient: the first de-rot
    pass itself introduced citations to two functions that never existed
    (``_create_chunker_view``, and ``_validate_existing_table_stable_row_ids``
    without its "has"). A cited name that fails a word-boundary search of the
    file it cites is rot from birth.

    Only identifier-shaped names are checked -- an underscore, a dot or a
    leading capital, which every genuine symbol citation in the spec has --
    so prose like "the writer's fill path (runners/ray/writer.py)" is exempt.
    """
    import geneva

    src_root = Path(geneva.__file__).parent
    citation_forms = [
        re.compile(r"\b([A-Za-z_][A-Za-z0-9_.]*)\s+\(([\w./]+\.py)\)"),
        re.compile(r"\(([A-Za-z_][A-Za-z0-9_.]*) in ([\w./]+\.py)\)"),
    ]
    unresolved = []
    for inv in SPEC["invariants"]:
        for field in ("statement", "geneva_depends_on", "note"):
            text = inv.get(field) or ""
            for form in citation_forms:
                for symbol, rel_path in form.findall(text):
                    looks_like_symbol = (
                        "_" in symbol or "." in symbol or symbol[0].isupper()
                    )
                    if not looks_like_symbol:
                        continue
                    target = src_root / rel_path
                    name = symbol.rsplit(".", 1)[-1]
                    if not target.is_file():
                        unresolved.append(
                            f"{inv['id']}.{field}: no such file {rel_path!r}"
                        )
                    elif not re.search(rf"\b{re.escape(name)}\b", target.read_text()):
                        unresolved.append(
                            f"{inv['id']}.{field}: {symbol!r} not found in {rel_path}"
                        )
    assert not unresolved, (
        "citations that do not resolve to a real symbol:\n  " + "\n  ".join(unresolved)
    )


def test_spec_fields_are_well_formed() -> None:
    """The spec is a cross-repo contract; keep it parseable and complete."""
    required = {
        "id",
        "layer",
        "statement",
        "geneva_depends_on",
        "severity",
        "status",
        "bug",
    }
    for inv in SPEC["invariants"]:
        missing = required - set(inv)
        assert not missing, f"{inv.get('id')} is missing {sorted(missing)}"
        assert inv["layer"] in {"lance", "geneva"}, inv["id"]
        assert inv["severity"] in {"critical", "high", "medium", "low"}, inv["id"]
        assert inv["status"] in {"holds", "broken", "by-design"}, inv["id"]
        assert inv["id"].startswith("SRID-"), inv["id"]
    ids = [i["id"] for i in SPEC["invariants"]]
    assert len(ids) == len(set(ids)), "duplicate invariant ids"


def test_vibecheck_mapping_is_actionable() -> None:
    """Every vibecheck entry names either a real variant or a proposed one.

    ``proposed`` entries are the concrete ask to lancedb/lance-vibecheck: the
    invariants Geneva needs that its model does not currently check.
    """
    known = {
        "RowCount",
        "FullScanMatch",
        "FilteredScanMatch",
        "IndexConsistency",
        "IndexFileIntegrity",
        "ManifestIntegrity",
        "PreviousVersionIntegrity",
        "VectorSearchConsistency",
        "RowIdConsistency",
        "CountRowsConsistency",
        "BlobConsistency",
    }
    proposed: set[str] = set()
    for inv in SPEC["invariants"]:
        vc = inv.get("vibecheck")
        if not vc:
            continue
        assert ("invariant" in vc) ^ ("proposed" in vc), (
            f"{inv['id']}: exactly one of invariant/proposed is required"
        )
        if "invariant" in vc:
            assert vc["invariant"] in known, (
                f"{inv['id']} names {vc['invariant']!r}, which is not a variant "
                "of lance-vibecheck's Invariant enum"
            )
        else:
            proposed.add(vc["proposed"])
    assert proposed, "the vibecheck ask should not be empty"
