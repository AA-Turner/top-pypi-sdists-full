# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Stable-row-ID behaviour for materialized-view consumers (GEN-842).

The Ray-marked half of the invariant spec in
``src/tests/stable_row_id_invariants.yaml``. Where
``test_stable_row_id_invariants.py`` asserts the storage-engine contract, this
module drives the two Geneva features that actually depend on it end to end:

  * **plain UDTF materialized views** -- 1:1, refreshed via
    ``LanceOperation.Overwrite``, which re-stamps ``base_table_version``
  * **chunker materialized views** -- 1:N, refreshed via
    ``LanceOperation.Append``, which does *not*

That asymmetry is ENT-2036 defect B, and it is why a chunker MV dies by itself
on a normally-operating deployment: the maintenance agent compacts the source
once it passes 30 fragments, the source version moves, and the frozen baseline
makes every subsequent refresh fatal. Nothing the user does to the view is
involved.

KNOWN DEFECTS THIS MODULE PINS
------------------------------
  SRID-G16  chunker refresh is append-only: a source row UPDATED in place keeps
            its stable row id, is therefore never seen as new work, and its
            children go stale silently. Stable row IDs remove the ENT-2036
            crash but do not deliver the recompute ................. GEN-851

Note on ENT-2036 defect B: this branch makes the chunker path advance the
baseline, but that does NOT clear the defect's symptom. The cross-version guard
raises earlier in ``run_ray_copy_table`` than the stamp is reached, so on a source
without stable row IDs the baseline still cannot move --
``test_cross_version_guard_is_not_suppressible_by_error_mode`` pins that, and
``test_chunker_mv_advances_base_table_version`` deliberately uses an SRID source
so the guard is out of the way. See the SRID-G03 note in the spec.

Everything else here is expected to pass; it exists so that a future
unification of the UDTF and chunker refresh paths cannot silently regress the
side that currently works, and so that the "stable row IDs rescue this" claim
in ENT-2036 stays verified rather than assumed.

Chunker tests use ``ray_with_test_path`` rather than ``local_ray_context``:
Ray workers must be able to import this module to deserialize the chunker.
"""

from __future__ import annotations

# `Iterator` must stay a runtime import: geneva.chunker resolves the decorated
# function's return annotation to infer the output schema, and this module uses
# `from __future__ import annotations`, so the name has to be in module globals.
from collections.abc import Iterator  # noqa: TC003
from typing import TYPE_CHECKING, NamedTuple

import pyarrow as pa
import pytest

import geneva
from geneva import connect
from geneva.query import MATVIEW_META_BASE_VERSION

if TYPE_CHECKING:
    from pathlib import Path

    from geneva.db import Connection
    from geneva.table import Table

pytestmark = pytest.mark.ray


def _spec_status(invariant_id: str) -> str:
    """Read an invariant's status out of the YAML spec.

    Drives the xfail markers below off the spec rather than hardcoding them, so
    flipping a status to ``holds`` actually removes the marker and the test has to
    pass on its own.
    """
    from test_stable_row_id_invariants import INVARIANTS

    return INVARIANTS[invariant_id]["status"]


class Clip(NamedTuple):
    """Chunker output row. Module level so Ray workers can import it."""

    clip_start: int
    clip_end: int


@geneva.chunker(inherit_input_columns=True)
def split_into_clips(duration: float) -> Iterator[Clip]:
    """1:N expansion -- one clip per 10 seconds of source duration."""
    for start in range(0, int(duration), 10):
        yield Clip(clip_start=start, clip_end=min(start + 10, int(duration)))


_SCALED_SCHEMA = pa.schema(
    [pa.field("video_path", pa.string()), pa.field("scaled", pa.float64())]
)


@geneva.udtf(output_schema=_SCALED_SCHEMA, input_columns=["video_path", "duration"])
def scale_duration(source) -> Iterator[pa.RecordBatch]:
    """1:1 UDTF -- the control against the chunker path."""
    tbl = source.to_arrow()
    yield pa.RecordBatch.from_pydict(
        {
            "video_path": tbl.column("video_path").to_pylist(),
            "scaled": [d * 2.0 for d in tbl.column("duration").to_pylist()],
        }
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def videos(rows: list[tuple[str, float]]) -> pa.Table:
    return pa.table(
        {
            "video_path": pa.array([p for p, _ in rows], pa.string()),
            "duration": pa.array([d for _, d in rows], pa.float64()),
        }
    )


def make_source(
    tmp_path: Path, name: str = "videos", *, stable: bool = True
) -> tuple[Connection, Table]:
    db = connect(tmp_path)
    opts = {"new_table_enable_stable_row_ids": "true"} if stable else {}
    tbl = db.create_table(
        name,
        videos([("/v/a.mp4", 30.0), ("/v/b.mp4", 20.0), ("/v/c.mp4", 10.0)]),
        storage_options=opts,
    )
    assert tbl.to_lance().has_stable_row_ids is stable
    return db, tbl


def base_version(view: Table) -> int | None:
    """Read geneva::view::base_table_version off the view's schema metadata."""
    md = view.to_lance().schema.metadata or {}
    raw = md.get(MATVIEW_META_BASE_VERSION.encode())
    return int(raw.decode()) if raw is not None else None


def clips_by_video(view: Table) -> dict[str, list[tuple[int, int]]]:
    df = view.to_pandas()
    out: dict[str, list[tuple[int, int]]] = {}
    for path, start, end in zip(
        df["video_path"], df["clip_start"], df["clip_end"], strict=True
    ):
        out.setdefault(path, []).append((int(start), int(end)))
    for v in out.values():
        v.sort()
    return out


# ===========================================================================
# SRID-G03 / SRID-G04 -- does the refresh advance the baseline?
# ===========================================================================


def test_chunker_mv_advances_base_table_version(tmp_path, ray_with_test_path) -> None:
    """The baseline must track the source, or the view eventually dies.

    Run against a source WITH stable row IDs so the cross-version guard does not
    fire -- this isolates the frozen-baseline defect from the guard that hides
    it. On a source without stable row IDs the same frozen baseline is what
    makes every later refresh fatal.
    """
    db, source = make_source(tmp_path)
    query = source.search(None).select(["video_path", "duration"])
    view = db.create_udtf_view("clips_baseline", query, split_into_clips)

    view.refresh(_admission_check=False)
    view.checkout_latest()
    created_at = base_version(view)
    assert created_at is not None

    source.add(videos([("/v/d.mp4", 10.0)]))
    source.checkout_latest()
    moved_to = source.version
    assert moved_to > created_at

    view.refresh(_admission_check=False)
    view.checkout_latest()

    assert base_version(view) == moved_to, (
        f"chunker MV baseline is still {base_version(view)} after refreshing "
        f"against source version {moved_to}. A source WITHOUT stable row IDs "
        "becomes permanently unrefreshable at this point (ENT-2036 defect B)."
    )


def test_udtf_mv_advances_base_table_version(tmp_path, local_ray_context) -> None:
    """The control: the 1:1 UDTF path re-stamps the baseline correctly.

    Pinned so a future unification of the two refresh paths cannot regress the
    side that works.
    """
    db, source = make_source(tmp_path, "videos_udtf")
    query = source.search(None).select(["video_path", "duration"])
    view = db.create_udtf_view("scaled_baseline", query, scale_duration)

    view.refresh(_admission_check=False)
    view.checkout_latest()
    created_at = base_version(view)
    assert created_at is not None

    source.add(videos([("/v/d.mp4", 10.0)]))
    source.checkout_latest()
    moved_to = source.version
    assert moved_to > created_at

    view.refresh(_admission_check=False)
    view.checkout_latest()

    assert base_version(view) == moved_to, (
        f"UDTF MV baseline {base_version(view)} did not advance to {moved_to}; "
        "table.py:3087 is supposed to re-stamp it on every refresh"
    )


# ===========================================================================
# SRID-G05 -- the guard, and what it does and does not protect
# ===========================================================================


def test_cross_version_guard_is_not_suppressible_by_error_mode(
    tmp_path, monkeypatch
) -> None:
    """The guard runs in planning, so on_error cannot downgrade it to skipped rows.

    GEN-813 read this loud failure as a passing test. Pinning that it raises
    *before* any per-row work keeps "the guard fired" and "the rows were
    computed and skipped" distinguishable.
    """
    db, source = make_source(tmp_path, "videos_guard", stable=False)
    query = source.search(None).select(["video_path", "duration"])
    with pytest.warns(UserWarning, match="same source version"):
        view = db.create_udtf_view("clips_guard_mode", query, split_into_clips)

    created_at = source.version
    source.add(videos([("/v/d.mp4", 10.0)]))
    source.checkout_latest()
    assert source.version > created_at

    from geneva.runners.ray import pipeline as ray_pipeline

    def must_not_run(name: str):  # noqa: ANN202
        def sentinel(*_a: object, **_k: object) -> None:
            raise AssertionError(
                f"{name} ran; the guard is no longer ahead of per-row work and "
                "skip_on_error could now partially apply it"
            )

        return sentinel

    # _append_expanded_fragments is the per-row work a guard bypass would reach on
    # this scenario. _delete_stale_mv_rows is also patched, but on a never-refreshed
    # view with no rows neither of its two call sites is reachable, so on its own
    # it can never fire -- which is why this test used to assert nothing.
    monkeypatch.setattr(
        ray_pipeline,
        "_append_expanded_fragments",
        must_not_run("_append_expanded_fragments"),
    )
    monkeypatch.setattr(
        ray_pipeline, "_delete_stale_mv_rows", must_not_run("_delete_stale_mv_rows")
    )

    with pytest.raises(ValueError, match="stable row IDs"):
        ray_pipeline.run_ray_copy_table(
            view.get_reference(),
            db._packager,
            view.get_reference().open_checkpoint_store(),
            src_version=source.version,
        )

    assert view.count_rows() == 0, "a guarded refresh must commit nothing"


def test_stable_row_ids_lift_the_cross_version_guard(
    tmp_path, ray_with_test_path
) -> None:
    """The escape hatch ENT-2036 relies on: same sequence, but SRID on.

    Without stable row IDs this exact sequence is permanently fatal. Verifying
    it here keeps the claim honest rather than assumed.
    """
    db, source = make_source(tmp_path, "videos_escape")
    query = source.search(None).select(["video_path", "duration"])
    view = db.create_udtf_view("clips_escape", query, split_into_clips)

    view.refresh(_admission_check=False)
    view.checkout_latest()
    assert view.count_rows() == 6  # 30s->3, 20s->2, 10s->1

    source.add(videos([("/v/d.mp4", 40.0)]))
    source.checkout_latest()

    view.refresh(_admission_check=False)
    view.checkout_latest()

    assert view.count_rows() == 10, (
        f"cross-version chunker refresh produced {view.count_rows()} clips, "
        "expected 10 (6 existing + 4 for the new 40s video)"
    )
    assert clips_by_video(view)["/v/d.mp4"] == [(0, 10), (10, 20), (20, 30), (30, 40)]


# ===========================================================================
# SRID-G15 -- the production trigger: the maintenance agent compacts the source
# ===========================================================================


def test_chunker_mv_refreshes_after_source_compaction(
    tmp_path, ray_with_test_path
) -> None:
    """ENT-2036's real-world trigger, with stable row IDs in place.

    On the field deployment nothing touched the view: ordinary ingest pushed the
    source past 30 fragments and the maintenance agent compacted it on its own.
    This reproduces that shape deterministically via compact_files.
    """
    db, source = make_source(tmp_path, "videos_compact")
    for i in range(4):
        source.add(videos([(f"/v/extra{i}.mp4", 10.0)]))
    source.checkout_latest()
    assert len(list(source.to_lance().get_fragments())) > 1

    query = source.search(None).select(["video_path", "duration"])
    view = db.create_udtf_view("clips_compact", query, split_into_clips)
    view.refresh(_admission_check=False)
    view.checkout_latest()
    before = clips_by_video(view)
    assert len(before) == 7

    # Table.compact_files, not Table.optimize -- optimize compacts inside
    # lancedb's statically vendored lance, which is a different build.
    source.compact_files()
    source.checkout_latest()
    assert len(list(source.to_lance().get_fragments())) == 1

    view.refresh(_admission_check=False)
    view.checkout_latest()
    after = clips_by_video(view)

    assert after == before, (
        "source compaction changed the materialized clips.\n"
        f"  before: {before}\n"
        f"  after:  {after}"
    )


def test_mv_refreshes_after_source_compaction(tmp_path, local_ray_context) -> None:
    """The 1:1 MV equivalent of the above, via create_materialized_view."""
    db, source = make_source(tmp_path, "videos_mv_compact")
    for i in range(4):
        source.add(videos([(f"/v/extra{i}.mp4", float(i))]))
    source.checkout_latest()

    view = (
        source.search(None)
        .select(["video_path", "duration"])
        .create_materialized_view(db, "mv_compact")
    )
    view.refresh(_admission_check=False)
    view.checkout_latest()
    before = sorted(view.to_pandas()["video_path"].tolist())
    assert len(before) == 7

    source.compact_files()
    source.checkout_latest()

    view.refresh(_admission_check=False)
    view.checkout_latest()
    after = sorted(view.to_pandas()["video_path"].tolist())

    assert after == before, f"compaction changed MV contents: {before} -> {after}"


# ===========================================================================
# Source mutation: the lineage cases chunker MVs exist to get right
# ===========================================================================


def test_deleting_a_source_row_removes_its_children(
    tmp_path, ray_with_test_path
) -> None:
    """A deleted parent must not leave orphaned children behind."""
    db, source = make_source(tmp_path, "videos_delete")
    query = source.search(None).select(["video_path", "duration"])
    view = db.create_udtf_view("clips_delete", query, split_into_clips)
    view.refresh(_admission_check=False)
    view.checkout_latest()
    assert view.count_rows() == 6

    source.delete("video_path = '/v/a.mp4'")  # the 30s video -> 3 clips
    source.checkout_latest()

    view.refresh(_admission_check=False)
    view.checkout_latest()

    remaining = clips_by_video(view)
    assert "/v/a.mp4" not in remaining, (
        f"deleted source row still has children: {remaining.get('/v/a.mp4')}"
    )
    assert view.count_rows() == 3, (
        f"expected 3 surviving clips, got {view.count_rows()}: {remaining}"
    )


@pytest.mark.xfail(
    condition=_spec_status("SRID-G16") == "broken",
    strict=True,
    reason=(
        "SRID-G16: chunker refresh is append-only. "
        "_extract_new_row_ids_from_source_fragment (runners/ray/pipeline.py) "
        "treats a source row as work only when its _rowid is NOT already "
        "present in the view, so an UPDATED row -- which keeps its stable row "
        "id by design -- is never re-expanded and its children go stale "
        "silently. Deletes are handled (_delete_stale_mv_rows); updates are not."
    ),
)
def test_repoint_source_row_recomputes_its_children(
    tmp_path, ray_with_test_path
) -> None:
    """Repair -> refresh -> success, the case GEN-813 could not demonstrate.

    t9 in the fault harness re-points a video and then accepts a crash as a
    pass, so it never showed a recompute. This test removes the crash (stable
    row IDs are on, so the cross-version guard cannot fire) and asks the
    question t9 could not: does the re-point actually take effect?

    It does not. Verified separately that the update lands on the source
    (duration 30.0 -> 10.0) and that the row keeps its stable row id -- so the
    stale children are the MV's doing, not the source's. Enabling stable row
    IDs removes ENT-2036's crash but does NOT deliver the recompute; those are
    two different defects and only the first has a ticket.
    """
    db, source = make_source(tmp_path, "videos_repoint")
    query = source.search(None).select(["video_path", "duration"])
    view = db.create_udtf_view("clips_repoint", query, split_into_clips)
    view.refresh(_admission_check=False)
    view.checkout_latest()

    before = clips_by_video(view)
    assert before["/v/a.mp4"] == [(0, 10), (10, 20), (20, 30)]
    untouched = {k: v for k, v in before.items() if k != "/v/a.mp4"}

    # Re-point: same row, new content -> a different number of children.
    source.update(where="video_path = '/v/a.mp4'", values={"duration": 10.0})
    source.checkout_latest()

    view.refresh(_admission_check=False)
    view.checkout_latest()
    after = clips_by_video(view)

    assert after.get("/v/a.mp4") == [(0, 10)], (
        f"re-pointed row did not recompute: expected exactly 1 clip from the "
        f"new 10s duration, got {after.get('/v/a.mp4')}. 3 unchanged clips "
        "means the old children were kept rather than recomputed."
    )
    for path, clips in untouched.items():
        assert after.get(path) == clips, (
            f"untouched video {path} changed: {clips} -> {after.get(path)}"
        )


def test_source_row_ids_survive_the_whole_refresh_cycle(
    tmp_path, ray_with_test_path
) -> None:
    """__source_row_id must keep pointing at the parent it was stamped from.

    The end-to-end statement behind SRID-L02/L07/L12: after append, compaction
    and refresh, every child's stored parent id still resolves to the video that
    produced it.
    """
    db, source = make_source(tmp_path, "videos_lineage")
    query = source.search(None).select(["video_path", "duration"])
    view = db.create_udtf_view("clips_lineage", query, split_into_clips)
    view.refresh(_admission_check=False)
    view.checkout_latest()

    source.add(videos([("/v/d.mp4", 20.0)]))
    source.checkout_latest()
    source.compact_files()
    source.checkout_latest()

    view.refresh(_admission_check=False)
    view.checkout_latest()

    src = source.to_lance().to_table(columns=["video_path"], with_row_id=True)
    parent_of = dict(
        zip(src["_rowid"].to_pylist(), src["video_path"].to_pylist(), strict=True)
    )

    df = view.to_pandas()
    mismatched = [
        (int(rid), path, parent_of.get(int(rid)))
        for rid, path in zip(df["__source_row_id"], df["video_path"], strict=True)
        if parent_of.get(int(rid)) != path
    ]
    assert not mismatched, (
        "child rows point at the wrong parent after compaction; "
        f"(stored_id, child_video_path, actual_parent): {mismatched[:5]}"
    )


# ---------------------------------------------------------------------------
# Coverage map consumed by the fast suite's spec/registry guard
# ---------------------------------------------------------------------------

# The invariants this Ray-marked module owns, mapped to the test that checks
# each. test_stable_row_id_invariants.test_spec_and_registry_agree reads this
# instead of trusting a hardcoded id set: a set cannot notice that the test it
# claims coverage from was renamed or deleted, so the spec could keep asserting
# coverage for nothing.
COVERS = {
    "SRID-G03": test_chunker_mv_advances_base_table_version,
    "SRID-G04": test_udtf_mv_advances_base_table_version,
    "SRID-G05": test_cross_version_guard_is_not_suppressible_by_error_mode,
    "SRID-G15": test_chunker_mv_refreshes_after_source_compaction,
    "SRID-G16": test_repoint_source_row_recomputes_its_children,
}
