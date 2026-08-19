# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""MV refresh racing concurrent source compaction (ENT-2036 production shape).

A stable-row-id (SRID) source table receives a continuous stream of appends,
stripe deletes, and ``compact_files()`` calls from a background thread while
the foreground repeatedly refreshes an identity MV and a filtered MV.
Individual refreshes may fail loudly with retryable commit/conflict errors --
those are tolerated and counted -- but after the churn stops, a final refresh
must converge both MVs to exactly the rows of the live source (Arrow oracle,
hard assertion).

Without stable row ids the version-based guard applies instead: once the
source version moves past the MV's base version, every refresh must raise
``RuntimeError`` mentioning "stable row IDs" and leave the MV byte-identical
(frozen snapshot), including across a compaction commit that rewrites the
source's fragments.
"""

from __future__ import annotations

import contextlib
import logging
import threading
import time
from typing import TYPE_CHECKING

import pyarrow as pa
import pyarrow.compute as pc
import pytest

import geneva
from stress_tests.stress_results import log_result, make_result

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

    from geneva.db import Connection
    from geneva.table import Table

_LOG = logging.getLogger(__name__)

pytestmark = pytest.mark.limit

_SRID_OPTS = {"new_table_enable_stable_row_ids": "true"}
_FILTER_EXPR = "id % 2 = 0"

# Oracle-side equivalent of _FILTER_EXPR. Arrow has no modulo kernel, and every
# id is non-negative, so a zero low bit is an exact stand-in for evenness.
_EVEN_ID = pc.bit_wise_and(pc.field("id"), 1) == 0

# Oracle comparisons run on this canonical projection: field nullability can
# differ between a source table and an MV, and pa.Table.equals is
# nullability-sensitive, so both sides are cast before comparing.
_ROW_SCHEMA = pa.schema([("id", pa.int64()), ("value", pa.int64())])
_ROW_SORT = [("id", "ascending"), ("value", "ascending")]

# Background churn cadence and triggers.
_CHURN_PERIOD_S = 0.2
_CHURN_APPEND_ROWS = 60
_COMPACT_FRAGMENT_THRESHOLD = 30
_DELETE_EVERY_N_ITERATIONS = 3

_FOREGROUND_REFRESHES = 6
_FINAL_REFRESH_ATTEMPTS = 3

_explore_marks = [
    pytest.mark.stress_explore,
    pytest.mark.xfail(strict=False, reason="explore: probing for scale limits"),
]

# (num_fragments, rows_per_fragment) scale points.
_SCALE_PARAMS = [
    pytest.param(40, 500, id="frags-40x500"),
    pytest.param(200, 5000, id="frags-200x5000", marks=_explore_marks),
]


def _block(start_id: int, num_rows: int) -> pa.Table:
    """Build a data block with globally unique ids."""
    ids = list(range(start_id, start_id + num_rows))
    return pa.table({"id": ids, "value": [i * 10 for i in ids]})


def _build_srid_source(
    db: Connection, name: str, num_fragments: int, rows_per_fragment: int
) -> tuple[Table, int]:
    """Create an SRID source with one fragment per append; return (table, next_id)."""
    tbl = db.create_table(
        name, _block(0, rows_per_fragment), storage_options=_SRID_OPTS
    )
    next_id = rows_per_fragment
    for _ in range(num_fragments - 1):
        tbl.add(_block(next_id, rows_per_fragment))
        next_id += rows_per_fragment
    return tbl, next_id


def _create_mv(query: object, db: Connection, name: str) -> Table:
    # geneva's query builders lose the GenevaQueryBuilder type through
    # search()/where()/select(); create_materialized_view exists at runtime.
    return query.create_materialized_view(db, name)  # pyright: ignore[reportAttributeAccessIssue]


def _canonical(t: pa.Table) -> pa.Table:
    """Project to (id, value) in the canonical oracle schema and row order."""
    return t.select(["id", "value"]).cast(_ROW_SCHEMA).sort_by(_ROW_SORT)


def _mv_rows(mv: Table) -> pa.Table:
    mv.checkout_latest()
    return _canonical(mv.to_arrow())


def _oracle_rows(src: Table, filtered: bool) -> pa.Table:
    src.checkout_latest()
    rows = src.to_arrow()
    if filtered:
        rows = rows.filter(_EVEN_ID)
    return _canonical(rows)


def _divergence(view_name: str, got: pa.Table, expected: pa.Table) -> str:
    """Describe an MV/oracle mismatch; only built when the comparison fails."""

    def as_set(t: pa.Table) -> set[tuple]:
        return set(zip(t["id"].to_pylist(), t["value"].to_pylist(), strict=True))

    got_rows, expected_rows = as_set(got), as_set(expected)
    return (
        f"{view_name} MV diverged from source after final refresh: "
        f"{got.num_rows} rows vs oracle {expected.num_rows} rows; "
        f"extra={sorted(got_rows - expected_rows)[:5]} "
        f"missing={sorted(expected_rows - got_rows)[:5]}"
    )


class _ChurnStats:
    """Counters for the background source-churn thread."""

    def __init__(self) -> None:
        self.appends = 0
        self.deletes = 0
        self.compactions = 0
        self.errors: list[str] = []


@contextlib.contextmanager
def _background_churn(
    src: Table, next_id_start: int
) -> Generator[_ChurnStats, None, None]:
    """Run appends/stripe-deletes/compactions against the source in a thread.

    Each iteration appends one small fragment; every third iteration deletes a
    rotating modulo stripe; ``compact_files()`` runs whenever the fragment
    count reaches the threshold. Individual operation failures (e.g. commit
    conflicts with a concurrent refresh) are recorded, not raised: the source
    stays live and the oracle is recomputed from its final state.
    """
    stop = threading.Event()
    stats = _ChurnStats()

    def _loop() -> None:
        next_id = next_id_start
        iteration = 0
        while not stop.is_set():
            try:
                src.add(_block(next_id, _CHURN_APPEND_ROWS))
                next_id += _CHURN_APPEND_ROWS
                stats.appends += 1
                if iteration % _DELETE_EVERY_N_ITERATIONS == 2:
                    # Stripe index keyed on fired deletes, not iteration: with
                    # a %3 trigger, iteration % 6 only ever lands on 2 and 5.
                    src.delete(f"id % 6 = {stats.deletes % 6}")
                    stats.deletes += 1
                if len(src.to_lance().get_fragments()) >= _COMPACT_FRAGMENT_THRESHOLD:
                    src.compact_files()
                    stats.compactions += 1
            except Exception as exc:  # noqa: BLE001 - churn must keep going
                stats.errors.append(repr(exc))
            iteration += 1
            stop.wait(_CHURN_PERIOD_S)

    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
    try:
        yield stats
    finally:
        stop.set()
        thread.join(timeout=30.0)


def _final_refresh(mv: Table) -> int:
    """Refresh with retries for conflict errors; return the number of attempts."""
    for attempt in range(1, _FINAL_REFRESH_ATTEMPTS + 1):
        try:
            mv.refresh(_admission_check=False)
            return attempt
        except Exception:  # noqa: PERF203
            if attempt == _FINAL_REFRESH_ATTEMPTS:
                raise
            _LOG.warning(
                "final refresh attempt %d/%d failed; retrying",
                attempt,
                _FINAL_REFRESH_ATTEMPTS,
                exc_info=True,
            )
            time.sleep(1.0)
    raise AssertionError("unreachable")


@pytest.mark.parametrize(("num_fragments", "rows_per_fragment"), _SCALE_PARAMS)
def test_mv_refresh_racing_compaction_srid(
    tmp_path: Path,
    local_ray,
    num_fragments: int,
    rows_per_fragment: int,
) -> None:
    """Refreshes racing source compaction converge to the Arrow oracle.

    Per-refresh conflict errors are tolerated (counted, logged); after the
    churn quiesces, one final refresh must make both MVs exactly equal to the
    live source. Any divergence is silent corruption and hard-fails.
    """
    db = geneva.connect(str(tmp_path))
    src, next_id = _build_srid_source(db, "src_race", num_fragments, rows_per_fragment)

    mv_identity = _create_mv(src.search(None).select(["id", "value"]), db, "mv_id")
    mv_filtered = _create_mv(
        src.search(None).where(_FILTER_EXPR).select(["id", "value"]), db, "mv_flt"
    )
    views: list[tuple[str, Table, bool]] = [
        ("identity", mv_identity, False),
        ("filtered", mv_filtered, True),
    ]

    latencies: list[float] = []
    refresh_errors: list[str] = []
    t_start = time.monotonic()

    with _background_churn(src, next_id) as churn:
        for pass_num in range(_FOREGROUND_REFRESHES):
            for view_name, mv, _ in views:
                t0 = time.monotonic()
                try:
                    mv.refresh(_admission_check=False)
                    latencies.append(time.monotonic() - t0)
                except Exception as exc:  # noqa: BLE001 - loud conflicts tolerated
                    refresh_errors.append(f"{view_name}#{pass_num}: {exc!r}")
                    _LOG.warning(
                        "refresh %s pass %d failed under churn: %r",
                        view_name,
                        pass_num,
                        exc,
                    )

    # Churn has quiesced: a final refresh must converge each MV to the oracle.
    final_attempts: dict[str, int] = {}
    for view_name, mv, filtered in views:
        final_attempts[view_name] = _final_refresh(mv)
        got = _mv_rows(mv)
        expected = _oracle_rows(src, filtered)
        assert got.equals(expected), _divergence(view_name, got, expected)

    elapsed = time.monotonic() - t_start
    result = make_result(
        scale=num_fragments,
        latencies=latencies,
        error_count=len(refresh_errors),
        elapsed_s=elapsed,
        metadata={
            "rows_per_fragment": rows_per_fragment,
            "refresh_errors": refresh_errors[:5],
            "final_refresh_attempts": final_attempts,
            "churn_appends": churn.appends,
            "churn_deletes": churn.deletes,
            "churn_compactions": churn.compactions,
            "churn_errors": churn.errors[:5],
            "churn_error_count": len(churn.errors),
            "final_source_rows": src.count_rows(),
        },
    )
    log_result(result)
    _LOG.info(
        "racing refresh: %d/%d refreshes failed (tolerated), "
        "churn appends=%d deletes=%d compactions=%d errors=%d",
        len(refresh_errors),
        _FOREGROUND_REFRESHES * len(views),
        churn.appends,
        churn.deletes,
        churn.compactions,
        len(churn.errors),
    )


def test_mv_refresh_racing_compaction_guard_without_srid(
    tmp_path: Path,
    local_ray,
) -> None:
    """Without stable row ids the refresh guard holds under racing compaction.

    An MV over a non-SRID source can only refresh at the source version it was
    created from (table.py version guard). Once the source version moves, every
    refresh must raise ``RuntimeError`` mentioning "stable row IDs" and the MV
    must remain byte-identical -- a frozen snapshot -- across background
    append/delete churn AND a real compaction commit. The churn window is too
    short to reach the background compaction threshold reliably, so the
    compaction bump is applied in the foreground, where it is deterministic.
    """
    db = geneva.connect(str(tmp_path))
    # Omit the SRID storage option entirely: passing a bool crashes
    # create_table (GEN-869), and any presence of the key changes the shape.
    src = db.create_table("src_nosrid", _block(0, 50))
    next_id = 50
    for _ in range(9):
        src.add(_block(next_id, 50))
        next_id += 50

    with pytest.warns(UserWarning, match="stable row IDs"):
        mv = _create_mv(src.search(None).select(["id", "value"]), db, "mv_nosrid")

    # Populate at the base version (same-version refresh is allowed).
    mv.refresh(_admission_check=False)
    assert _mv_rows(mv).equals(_oracle_rows(src, filtered=False))

    base_version = src.version
    guard_raises = 0
    with _background_churn(src, next_id) as churn:
        # Wait for the source to move past the MV's base version.
        deadline = time.monotonic() + 30.0
        while src.version == base_version:
            if time.monotonic() > deadline:
                pytest.fail("background churn never advanced the source version")
            time.sleep(0.1)

        snapshot_version = mv.to_lance().version
        snapshot = mv.to_arrow()

        for _ in range(4):
            with pytest.raises(RuntimeError, match="stable row IDs"):
                mv.refresh(_admission_check=False)
            guard_raises += 1
            time.sleep(0.3)

    # One more attempt after quiescing: the source has definitely moved.
    with pytest.raises(RuntimeError, match="stable row IDs"):
        mv.refresh(_admission_check=False)
    guard_raises += 1

    # Deterministic compaction leg: a pure-compaction version bump is its own
    # hazard, and the background threshold is rarely crossed inside the short
    # churn window -- so compact in the foreground and re-check the guard.
    src.checkout_latest()
    pre_compact_version = src.version
    src.compact_files()
    src.checkout_latest()
    assert src.version != pre_compact_version, (
        "foreground compaction must commit a source version"
    )
    with pytest.raises(RuntimeError, match="stable row IDs"):
        mv.refresh(_admission_check=False)
    guard_raises += 1

    # The guard must leave the MV untouched: same version, same bytes.
    mv.checkout_latest()
    assert mv.to_lance().version == snapshot_version, (
        "guard raise must not commit to the MV"
    )
    assert mv.to_arrow().equals(snapshot), (
        "guard raise must leave the MV byte-identical"
    )

    result = make_result(
        scale=10,
        latencies=[],
        error_count=0,
        elapsed_s=0.0,
        metadata={
            "guard_raises": guard_raises,
            "churn_appends": churn.appends,
            "churn_compactions": churn.compactions,
            "foreground_compactions": 1,
            "churn_error_count": len(churn.errors),
        },
    )
    log_result(result)
