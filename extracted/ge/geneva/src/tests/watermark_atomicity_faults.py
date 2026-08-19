# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Shim-backed scenarios probing MV-refresh watermark atomicity -- no Ray cluster,
sub-second. Run one per process: ``watermark_atomicity_faults.py <scenario>``;
``test_watermark_atomicity`` runs each as a subprocess. Each exits 0 iff its invariant
held.

Background: a 1:1 MV refresh records its ``last_refreshed`` watermark by a SEPARATE
write (``_set_last_refreshed_version`` -> ``update_field_metadata``, table.py) that is
not atomic with the data commit. The watermark is written client-side AFTER the refresh
job returns, so a dropped/lost data commit can leave the watermark advanced past rows
the MV never durably landed.

These scenarios establish (a) that the inflated-watermark state is REACHABLE via a real
dropped append, and then test whether that inflated watermark causes silent data loss:
a forward refresh that skips the missing rows (persistent gap), or a backward refresh
that mis-deletes valid rows. The hypothesis under test is whether the non-atomic
watermark is an exploitable defect or whether geneva self-repairs because new-row
detection is destination-state-driven (not watermark-driven).

Like ``worker_death_faults.py`` this monkeypatches ``ray`` before importing geneva.
"""

# ruff: noqa: T201 -- CLI script; print() is the intended output

import shutil
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ray_shim  # noqa: E402

ray_shim.install()  # MUST precede the geneva import below

import pyarrow as pa  # noqa: E402
from geneva_faults import FlakyCommitter, by_op_name  # noqa: E402

from geneva import connect  # noqa: E402
from geneva.committer import using_committer  # noqa: E402
from geneva.db import Connection  # noqa: E402
from geneva.table import (  # noqa: E402
    Table,
    _get_last_refreshed_version,
    _set_last_refreshed_version,
)

ray_shim.stub_geneva_cluster_polling()


def _initial() -> pa.Table:
    return pa.table({"id": [1, 2, 3, 4], "value": [10, 20, 30, 40]})


def _block(n: int) -> pa.Table:
    base = 100 * (n + 1)
    ids = [base, base + 1, base + 2]
    return pa.table({"id": ids, "value": [i * 10 for i in ids]})


def _make_source(db: Connection) -> Table:
    return db.create_table(
        "s", _initial(), storage_options={"new_table_enable_stable_row_ids": "true"}
    )


def _make_mv(db: Connection, src: Table) -> Table:
    return src.search(None).select(["id", "value"]).create_materialized_view(db, "m")


def _watermark(mv: Table) -> int | None:
    mv.checkout_latest()
    return _get_last_refreshed_version(mv)


def _mv_ids(mv: Table) -> list[int]:
    mv.checkout_latest()
    t = mv.to_arrow()
    return sorted(i for i in t["id"].to_pylist() if i is not None)


def scenario_lost_append_advances_watermark() -> int:
    """Reachability check: drop the refresh's row-landing write -- the atomic Append
    commit of the populated fragments -- on a forward refresh, then report whether
    the watermark advanced past the rows that never landed. This is the
    precondition for any watermark-atomicity bug -- if the watermark does NOT
    advance on a lost append, the inflated-watermark state is unreachable."""
    tmp = tempfile.mkdtemp(prefix="wm_lost_append_")
    try:
        db = connect(tmp)
        src = _make_source(db)
        mv = _make_mv(db, src)
        mv.refresh(_admission_check=False)  # populate 4 rows; watermark -> v_a
        wm_a = _watermark(mv)
        src.add(_block(0))
        src.add(_block(1))  # +6 rows; source advances to v_b
        v_b = src.version

        # Only fault the view's own Append commits: job-history and other
        # tables also commit through the committer seam.
        class _DropMvAppend(FlakyCommitter):
            def commit(self, dataset_or_uri: Any, operation: Any, **kw: Any) -> Any:
                if "m.lance" not in str(dataset_or_uri):
                    return self.inner.commit(dataset_or_uri, operation, **kw)
                return super().commit(dataset_or_uri, operation, **kw)

        flaky = _DropMvAppend(match=by_op_name("Append"), drop_at={1})
        raised: Exception | None = None
        with using_committer(flaky):
            try:
                mv.refresh(_admission_check=False)
            except Exception as e:  # noqa: BLE001 -- we WANT to know if it raised
                raised = e

        ids = _mv_ids(mv)
        wm_after = _watermark(mv)
        outcome = f"raised {type(raised).__name__}" if raised else "reported success"
        print(f"appends seen  : {flaky.calls}  dropped: {flaky.dropped}")
        print(f"refresh       : {outcome}")
        print(f"source version: v_a-watermark={wm_a}  v_b={v_b}")
        print(f"MV ids        : {ids} ({len(ids)} rows)")
        print(f"watermark now : {wm_after}")

        if not flaky.dropped:
            print(
                "INCONCLUSIVE: no Append commit was dropped -- the committer "
                "was not run."
            )
            return 1
        if raised is not None:
            print(
                f"NOT REACHABLE HERE: the lost append failed LOUD "
                f"({type(raised).__name__}); the watermark write never ran, so the "
                "inflated-watermark state is not produced by this fault."
            )
            return 0
        complete = len(ids) >= src.count_rows()
        inflated = wm_after is not None and v_b is not None and wm_after >= v_b
        if complete:
            print("NOT REACHABLE HERE: the MV is complete -- no rows were lost.")
            return 0
        if inflated:
            print(
                f"\nREACHABLE: the placeholder append was dropped (MV holds {len(ids)} "
                f"of {src.count_rows()} rows) yet the refresh reported success and the "
                f"watermark advanced to {wm_after} (>= lost-rows version {v_b}). The "
                "watermark is non-atomic with the data commit. Subsequent scenarios "
                "test whether that inflated watermark causes loss."
            )
            return 0
        print(
            f"NOT REACHABLE HERE: MV incomplete but the watermark did NOT advance "
            f"(watermark={wm_after}, v_b={v_b}); the inflated state was not produced."
        )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_inflated_watermark_forward_heals() -> int:
    """Silent-data-loss test. Model the atomicity gap directly: a complete MV at v_a,
    then source grows to v_b but the v_b data commit is lost WHILE the watermark write
    lands (we advance the watermark to v_b by hand, leaving the rows missing). A
    subsequent forward refresh to v_b must REPAIR (re-add the missing rows), not
    silently skip them on the strength of the inflated watermark. A persistent gap is
    the bug."""
    tmp = tempfile.mkdtemp(prefix="wm_forward_heals_")
    try:
        db = connect(tmp)
        src = _make_source(db)
        mv = _make_mv(db, src)
        mv.refresh(_admission_check=False)  # 4 rows; watermark -> v_a
        before_ids = _mv_ids(mv)

        src.add(_block(0))
        src.add(_block(1))  # +6 rows; source -> v_b
        v_b = src.version
        full = src.count_rows()

        # Model "data commit lost, watermark write landed": advance the watermark to v_b
        # without landing the v_b rows. The MV still holds only the v_a rows.
        _set_last_refreshed_version(mv, v_b)
        mv.checkout_latest()
        wm = _watermark(mv)
        gap_ids = _mv_ids(mv)
        print(f"v_a ids       : {before_ids}")
        print(f"source -> v_b={v_b}, full row count={full}")
        print(f"inflated wm   : {wm}  (MV holds {len(gap_ids)} of {full} rows)")

        if wm != v_b:
            print(f"INCONCLUSIVE: failed to inflate watermark (got {wm}, want {v_b}).")
            return 1
        if len(gap_ids) >= full:
            print("INCONCLUSIVE: MV already complete -- no gap to heal.")
            return 1

        # Forward refresh to v_b. src_version (v_b) >= watermark (v_b): forward path.
        mv.refresh(src_version=v_b, _admission_check=False)
        healed_ids = _mv_ids(mv)
        print(f"after refresh : {healed_ids} ({len(healed_ids)} of {full} rows)")

        missing = full - len(healed_ids)
        if missing == 0:
            print(
                "\nHELD (benign): the forward refresh re-detected the missing source "
                "fragments and re-added every row despite the inflated watermark -- "
                "new-row detection is destination-state-driven, so the non-atomic "
                "watermark did NOT cause a silent gap."
            )
            return 0
        print(
            f"\nFAIL (bug present): the inflated watermark caused the forward refresh "
            f"to SKIP {missing} of {full} rows -- a persistent silent gap (false "
            "success). The watermark must be atomic with the data commit."
        )
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_inflated_watermark_no_misdelete() -> int:
    """Mis-deletion test. With the watermark inflated to v_b (data missing), issue a
    refresh to an INTERMEDIATE source version v_mid where v_a < v_mid < v_b. Relative to
    the inflated watermark this is a BACKWARD (point-in-time) refresh, which deletes MV
    rows not present at the target version. The v_a rows that legitimately exist at
    v_mid must survive -- a backward refresh keyed on a bogus watermark must not delete
    valid rows."""
    tmp = tempfile.mkdtemp(prefix="wm_no_misdelete_")
    try:
        db = connect(tmp)
        src = _make_source(db)
        mv = _make_mv(db, src)
        mv.refresh(_admission_check=False)  # 4 rows at v_a
        v_a_ids = _mv_ids(mv)

        src.add(_block(0))  # +3 rows -> v_mid
        v_mid = src.version
        src.add(_block(1))  # +3 rows -> v_b
        v_b = src.version

        # Inflate watermark to v_b while the MV still holds only the original v_a rows.
        _set_last_refreshed_version(mv, v_b)
        mv.checkout_latest()
        print(f"v_a ids       : {v_a_ids}")
        print(f"versions      : v_mid={v_mid}  v_b={v_b}  inflated wm={_watermark(mv)}")
        print(f"MV before     : {_mv_ids(mv)}")

        # Refresh to v_mid: v_mid < watermark(v_b) -> backward/point-in-time path.
        mv.refresh(src_version=v_mid, _admission_check=False)
        after_ids = _mv_ids(mv)
        print(f"MV after v_mid: {after_ids}")

        # Every original v_a row still exists in the source at v_mid, so none may be
        # deleted. (The refresh may also ADD the v_mid rows; we only assert no valid
        # row was wrongly removed.)
        wrongly_deleted = [i for i in v_a_ids if i not in after_ids]
        if wrongly_deleted:
            print(
                f"\nFAIL (bug present): the backward refresh against the inflated "
                f"watermark DELETED valid rows {wrongly_deleted} that exist at v_mid "
                "-- silent data loss via watermark-driven mis-routing."
            )
            return 1
        print(
            "\nHELD (benign): the backward refresh deleted no valid rows -- deletion "
            "is keyed on actual source-row presence at the target version, not on the "
            "watermark value, so an inflated watermark cannot mis-delete."
        )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


SCENARIOS: dict[str, Callable[[], int]] = {
    "lost-append-advances-watermark": scenario_lost_append_advances_watermark,
    "inflated-watermark-forward-heals": scenario_inflated_watermark_forward_heals,
    "inflated-watermark-no-misdelete": scenario_inflated_watermark_no_misdelete,
}


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in SCENARIOS:
        print(f"usage: {argv[0]} {{{'|'.join(SCENARIOS)}}}", file=sys.stderr)
        return 2
    print(f"=== scenario: {argv[1]} ===")
    return SCENARIOS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
