# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""First coverage of ``Table.get_failed_row_addresses`` (GEN-864).

Exercises the documented failed-row retry loop end to end: a backfill with
row-skipping error handling records the ``_rowaddr`` of every failed row in
the error store; the caller fetches them via ``get_failed_row_addresses``
and re-backfills with ``where="_rowaddr IN (...)"``.

Found bug (GEN-868; root cause lance-format/lance#8126, Linear OSS-1627):
on *stable-row-id* tables, Lance evaluates ``_rowaddr`` scan filters in
``_rowid`` coordinate space. Fragment-0 addresses equal rowids and appear
to work; addresses at or above ``2**32`` match nothing; and an address
that collides with a live rowid matches the WRONG row. Failed rows are
recorded by physical address, so the documented retry loop silently
no-ops for any failure beyond fragment 0 — the retry backfill reports
DONE and the failed rows stay null. The SRID roundtrip below xfails
dynamically on that exact confirmed no-op state only — setup errors,
precondition failures, and corruption still fail loudly — and fails with
a cleanup reminder once the bug is fixed.

Also pins the stale-address hazard: a compaction between the failing run
and the retry renumbers row addresses, so recorded addresses match nothing
(or, worst case, the wrong rows — hard-failed here as corruption).
"""

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pyarrow as pa
import pytest

from conftest import make_id_value_table
from geneva import udf
from geneva.debug.error_store import skip_on_error

if TYPE_CHECKING:
    from geneva.db import Connection
    from geneva.table import Table
    from geneva.transformer import UDF

pytestmark = pytest.mark.ray

_SRID_ON = {"new_table_enable_stable_row_ids": "true"}
_SRID_OFF = {"new_table_enable_stable_row_ids": "false"}

# 3 fragments x 4 rows -> ids 0..11. One injected failure in fragment 1
# (id 5) and one in fragment 2 (id 9).
_FAIL_IDS = (5, 9)
_EXPECTED_ADDRS = [(1 << 32) + 1, (2 << 32) + 1]


def _make_table(db: "Connection", name: str, *, srid: bool) -> "Table":
    """3-fragment id/value table with explicit SRID storage options.

    Built directly rather than via ``make_multifragment_table`` because these
    tests need the ``make_id_value_table`` schema. Storage options use the
    explicit string forms lancedb parses; geneva normalizes bools and
    mixed-case strings as of GEN-869.
    """
    tbl = db.create_table(
        name,
        make_id_value_table(4, start=0),
        storage_options=dict(_SRID_ON if srid else _SRID_OFF),
    )
    for i in range(1, 3):
        tbl.add(make_id_value_table(4, start=i * 4))
    return tbl


# Healed-mode recomputes of rows that never failed add this offset. Healthy
# rows already hold id * 10, so a retry that resolves stale addresses to the
# wrong rows would otherwise rewrite the identical value and be invisible to
# the before/after corruption guards.
_WRONG_ROW_SENTINEL = 1_000_000


def _flaky_udf(marker_path: str, version: str) -> "UDF":
    """A scalar UDF that fails for ``_FAIL_IDS`` until the marker exists.

    Once healed (marker present), an invocation for a row outside
    ``_FAIL_IDS`` returns ``id * 10 + _WRONG_ROW_SENTINEL``: a retry that
    recomputes a row it should never touch changes that row visibly.
    """

    @udf(data_type=pa.int64(), version=version, on_error=skip_on_error())
    def flaky_times_ten(id: int) -> int:  # noqa: A002
        healed = os.path.exists(marker_path)
        if id in (5, 9):
            if not healed:
                raise ValueError(f"injected failure for id {id}")
            return id * 10
        return id * 10 + 1_000_000 if healed else id * 10

    return flaky_times_ten


def _snapshot(tbl: "Table") -> list[tuple[int, int | None]]:
    res = tbl.to_arrow()
    return sorted(zip(res["id"].to_pylist(), res["out"].to_pylist(), strict=True))


def _run_failing_backfill(
    db: "Connection", tmp_path: Path, name: str, *, srid: bool
) -> tuple["Table", str, list[int]]:
    """Backfill with two injected failures; return table, marker, addrs."""
    tbl = _make_table(db, name, srid=srid)
    marker_path = str(tmp_path / f"{name}.marker")
    tbl.add_columns({"out": _flaky_udf(marker_path, f"{name}-v1")})

    result = tbl.backfill("out", _admission_check=False)
    assert result.status == "DONE"
    assert [v for _, v in _snapshot(tbl)] == [
        None if i in _FAIL_IDS else i * 10 for i in range(12)
    ]

    addrs = tbl.get_failed_row_addresses(result.job_id, "out")
    # Recording works on SRID and non-SRID tables alike: exactly the two
    # failed rows, at their physical addresses (frag_id << 32 | offset).
    assert sorted(addrs) == _EXPECTED_ADDRS
    return tbl, marker_path, addrs


def _retry_where(addrs: list[int]) -> str:
    return f"_rowaddr IN ({', '.join(map(str, sorted(addrs)))})"


def test_retry_failed_rows_by_rowaddr_roundtrip_non_srid(
    db, tmp_path: Path, local_ray_context
) -> None:
    """The documented failed-row retry loop works end to end (non-SRID).

    The failing run completes (failed rows null), records exactly the two
    failed ``_rowaddr``s under the job id, and the targeted retry fills only
    those rows — every other row is byte-identical to before the retry.
    """
    tbl, marker_path, addrs = _run_failing_backfill(
        db, tmp_path, "err_retry_nosrid", srid=False
    )
    before = _snapshot(tbl)

    Path(marker_path).write_text("healed")
    retry = tbl.backfill("out", where=_retry_where(addrs), _admission_check=False)
    assert retry.status == "DONE"

    after = _snapshot(tbl)
    assert [v for _, v in after] == [i * 10 for i in range(12)]
    # Rows outside the failed set are byte-identical to before the retry.
    assert [row for row in after if row[0] not in _FAIL_IDS] == [
        row for row in before if row[0] not in _FAIL_IDS
    ]


def test_retry_failed_rows_by_rowaddr_roundtrip(
    db, tmp_path: Path, local_ray_context
) -> None:
    """The documented failed-row retry loop on an SRID table.

    Identical flow to the non-SRID roundtrip above, which passes. On a
    stable-row-id table the retry backfill completes without touching the
    failed rows: recording is unaffected — ``get_failed_row_addresses``
    returns the right addresses (asserted in the helper) — but the
    ``_rowaddr`` WHERE is evaluated in rowid coordinate space
    (lance-format/lance#8126), and both recorded addresses lie beyond
    fragment 0 (``>= 2**32``), so they match nothing.

    A test-level xfail marker would also swallow fixture errors and every
    precondition assertion (pytest reports any marked-test exception as
    XFAIL), so the xfail is raised dynamically only once the exact known
    no-op state is confirmed: retry DONE, untouched rows byte-identical,
    failed rows still null. Anything else fails loudly — including the bug
    getting fixed, which trips the cleanup reminder at the end (the strict
    tripwire this replaces).
    """
    tbl, marker_path, addrs = _run_failing_backfill(
        db, tmp_path, "err_retry_srid", srid=True
    )
    before = _snapshot(tbl)

    Path(marker_path).write_text("healed")
    retry = tbl.backfill("out", where=_retry_where(addrs), _admission_check=False)
    assert retry.status == "DONE"

    after = _snapshot(tbl)
    # Hard guarantee: rows outside the failed set must never change.
    assert [row for row in after if row[0] not in _FAIL_IDS] == [
        row for row in before if row[0] not in _FAIL_IDS
    ]
    if [row for row in after if row[0] in _FAIL_IDS] == [(i, None) for i in _FAIL_IDS]:
        # The exact confirmed bug state: the retry was a silent no-op.
        pytest.xfail(
            "GEN-868 / lance-format/lance#8126 (OSS-1627): _rowaddr filters "
            "on SRID tables are evaluated in rowid coordinate space — high "
            "addresses match nothing, colliding values match the wrong row — "
            "so the documented retry is a silent no-op"
        )
    # The retry touched the failed rows: enforce the intended contract.
    assert [v for _, v in after] == [i * 10 for i in range(12)]
    pytest.fail(
        "GEN-868 / lance-format/lance#8126 appear fixed: the _rowaddr retry "
        "filled the failed rows on an SRID table — remove this test's xfail "
        "scaffolding and keep the hard assertions"
    )


@pytest.mark.parametrize("stable_row_ids", [True, False], ids=["srid_on", "srid_off"])
def test_retry_failed_rows_after_compaction_pins_staleness(
    db, tmp_path: Path, local_ray_context, stable_row_ids: bool
) -> None:
    """Pins the stale-address hazard in the failed-row retry loop (GEN-864).

    ``get_failed_row_addresses`` returns *physical* row addresses, which a
    compaction invalidates (fragments merge and renumber). Pinned
    observation, with and without stable row ids: retrying with the stale
    addresses is a silent no-op — the ``where`` matches no live row, the
    failed rows stay null, and no error is raised. (On SRID tables the
    retry would be a no-op even without the compaction — see the xfail
    above.) Callers must re-derive failed rows, and must not compact
    between the failing run and the retry.

    Hard guarantee enforced here: the stale addresses must never resolve to
    *different* live rows and recompute them — any change outside the failed
    set is silent corruption and fails loudly. This is a live hazard, not a
    hypothetical: on SRID tables ``_rowaddr`` filters are evaluated in rowid
    coordinate space (lance-format/lance#8126), where a stale address that
    collides with a live rowid matches the wrong row. Healthy rows already
    hold the same ``id * 10`` the UDF would recompute, so the guard only has
    teeth because healed-mode invocations for never-failed rows write
    ``id * 10 + _WRONG_ROW_SENTINEL`` (see ``_flaky_udf``), making a
    wrong-row write distinguishable from the value already stored.
    """
    name = f"err_stale_{'on' if stable_row_ids else 'off'}"
    tbl, marker_path, addrs = _run_failing_backfill(
        db, tmp_path, name, srid=stable_row_ids
    )

    tbl.compact_files()  # merges the 3 fragments; row addresses renumber
    before = _snapshot(tbl)
    assert [v for _, v in before] == [
        None if i in _FAIL_IDS else i * 10 for i in range(12)
    ]

    Path(marker_path).write_text("healed")
    retry = tbl.backfill("out", where=_retry_where(addrs), _admission_check=False)
    assert retry.status == "DONE"

    after = _snapshot(tbl)
    # Any healed-mode write to a never-failed row carries the sentinel.
    wrong_row_writes = [
        (i, v) for i, v in after if v is not None and v >= _WRONG_ROW_SENTINEL
    ]
    assert wrong_row_writes == [], (
        f"stale row addresses recomputed the wrong rows: {wrong_row_writes}"
    )
    # Hard guarantee: nothing outside the failed set may change.
    assert [row for row in after if row[0] not in _FAIL_IDS] == [
        row for row in before if row[0] not in _FAIL_IDS
    ], "stale row addresses recomputed the wrong rows: silent corruption"
    # Pinned observation: the retry is a silent no-op — the stale addresses
    # match nothing, so the failed rows are still null.
    assert [row for row in after if row[0] in _FAIL_IDS] == [
        (i, None) for i in _FAIL_IDS
    ]
