# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Refresh-time growth with total source fragment count (GEN-629).

Under stable row ids the refresh planner cannot map ``__source_row_id``
values back to source fragments (``_extract_fragment_ids_from_row_ids``
returns an empty set for v2), so a refresh processes every source fragment
even when only one new fragment was appended since the last refresh.
Incremental refresh latency therefore grows with the total fragment count F,
not with the size of the change.

Each scale point builds an SRID source with F fragments, populates an
identity MV, appends ONE small fragment, and times the incremental refresh.
Correctness (MV == source oracle) is asserted hard after every refresh;
timing is only logged, with a warning when t(800)/t(200) exceeds 6x.

Sources are built with ``LanceFragment.create`` + one batched
``LanceOperation.Append`` commit on the geneva table's underlying dataset
(fast at high F). A module-scoped probe verifies that batch-appended
fragments carry stable row ids -- the manifest flag is set and a probe row
keeps its ``_rowid`` across a compaction -- and falls back to one-``add``-per-
fragment builds (capped at F=200) when they do not.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, cast

import lance
import pyarrow as pa
import pytest

import geneva
from geneva.db import dataset_uses_stable_row_ids
from stress_tests.stress_results import log_result, make_result, scale_params

if TYPE_CHECKING:
    from pathlib import Path

    from geneva.db import Connection
    from geneva.table import Table

_LOG = logging.getLogger(__name__)

pytestmark = pytest.mark.limit

_SRID_OPTS = {"new_table_enable_stable_row_ids": "true"}
_ROWS_PER_FRAGMENT = 10

# Fragment-count sweep; the 3000 point is exploratory.
_FRAGMENT_SWEEP = [50, 200, 800, 3000]
_EXPLORE_THRESHOLD = 3000

# The per-add fallback builder is too slow for the high scale points.
_PER_ADD_MAX_FRAGMENTS = 200

# Soft bound on incremental refresh growth between the two largest
# regression points (4x fragment growth; warn beyond 6x time growth).
_RATIO_BASE_F = 200
_RATIO_HIGH_F = 800
_MAX_REFRESH_TIME_RATIO = 6.0

# Incremental refresh seconds per completed fragment count, for the
# cross-point ratio check. Points run sequentially in ascending order.
_REFRESH_TIMES: dict[int, float] = {}


def _frag_block(frag_idx: int, rows_per_fragment: int) -> pa.Table:
    start = frag_idx * rows_per_fragment
    ids = list(range(start, start + rows_per_fragment))
    return pa.table({"id": pa.array(ids, type=pa.int64())})


def _build_batched(db: Connection, name: str, num_fragments: int) -> Table:
    """SRID source with F fragments: one create_table + one batched Append."""
    tbl = db.create_table(
        name, _frag_block(0, _ROWS_PER_FRAGMENT), storage_options=_SRID_OPTS
    )
    uri = tbl.to_lance().uri
    fragments = [
        lance.LanceFragment.create(uri, _frag_block(i, _ROWS_PER_FRAGMENT))
        for i in range(1, num_fragments)
    ]
    if fragments:
        read_version = tbl.to_lance().version
        lance.LanceDataset.commit(
            uri, lance.LanceOperation.Append(fragments), read_version=read_version
        )
    tbl.checkout_latest()
    return tbl


def _build_per_add(db: Connection, name: str, num_fragments: int) -> Table:
    """Fallback SRID source builder: one ``add`` commit per fragment."""
    tbl = db.create_table(
        name, _frag_block(0, _ROWS_PER_FRAGMENT), storage_options=_SRID_OPTS
    )
    for i in range(1, num_fragments):
        tbl.add(_frag_block(i, _ROWS_PER_FRAGMENT))
    return tbl


def _rowid_map(tbl: Table) -> dict[int, int]:
    """Map id -> _rowid for every row of the table."""
    t = tbl.to_lance().scanner(columns=["id"], with_row_id=True).to_table()
    ids = cast("list[int]", t["id"].to_pylist())
    row_ids = cast("list[int]", t["_rowid"].to_pylist())
    return dict(zip(ids, row_ids, strict=True))


@pytest.fixture(scope="module")
def builder_mode(tmp_path_factory: pytest.TempPathFactory) -> str:
    """Verify batch-appended fragments carry stable row ids; pick the builder.

    Returns "batched" when a probe table built via ``LanceFragment.create`` +
    ``LanceOperation.Append`` has the stable-row-id manifest flag AND every
    probe row keeps its ``_rowid`` across ``compact_files()``. Returns
    "per_add" otherwise, which caps the sweep at F=200.
    """
    db = geneva.connect(str(tmp_path_factory.mktemp("srid_probe")))
    probe = _build_batched(db, "probe", 8)

    probe_ds = probe.to_lance()
    all_fragments_srid = all(
        f.metadata.row_id_meta is not None for f in probe_ds.get_fragments()
    )
    if not dataset_uses_stable_row_ids(probe_ds) or not all_fragments_srid:
        _LOG.warning(
            "batch-appended fragments lack stable row ids (manifest flag or "
            "per-fragment row_id_meta); falling back to per-add builds "
            "capped at F=%d",
            _PER_ADD_MAX_FRAGMENTS,
        )
        return "per_add"

    before = _rowid_map(probe)
    probe.compact_files()
    probe.checkout_latest()
    after = _rowid_map(probe)
    if before != after:
        _LOG.warning(
            "_rowid values changed across compaction on batch-appended "
            "fragments; falling back to per-add builds capped at F=%d",
            _PER_ADD_MAX_FRAGMENTS,
        )
        return "per_add"

    return "batched"


def _oracle_ids(src: Table) -> list[int]:
    src.checkout_latest()
    return sorted(cast("list[int]", src.to_arrow()["id"].to_pylist()))


def _mv_ids(mv: Table) -> list[int]:
    mv.checkout_latest()
    return sorted(cast("list[int]", mv.to_arrow()["id"].to_pylist()))


def _identity_mv(db: Connection, src: Table, name: str) -> Table:
    # geneva's query builders lose the GenevaQueryBuilder type through
    # search()/select(); create_materialized_view exists at runtime.
    query = src.search(None).select(["id"])
    return query.create_materialized_view(db, name)  # pyright: ignore[reportAttributeAccessIssue]


@pytest.mark.parametrize(
    "num_fragments",
    scale_params(
        _FRAGMENT_SWEEP, id_prefix="fragments", explore_threshold=_EXPLORE_THRESHOLD
    ),
)
def test_mv_refresh_time_grows_with_fragment_count(
    tmp_path: Path,
    local_ray,
    builder_mode: str,
    num_fragments: int,
) -> None:
    """Time one incremental refresh (single appended fragment) at F fragments.

    The MV must equal the source oracle after both the populating refresh and
    the timed incremental refresh; timings are logged per point and the
    t(800)/t(200) ratio warns when it exceeds 6x.
    """
    if builder_mode == "per_add" and num_fragments > _PER_ADD_MAX_FRAGMENTS:
        pytest.skip(
            f"per-add fallback builder caps the sweep at "
            f"F={_PER_ADD_MAX_FRAGMENTS} (batch-appended fragments did not "
            f"carry stable row ids)"
        )

    db = geneva.connect(str(tmp_path))
    build = _build_batched if builder_mode == "batched" else _build_per_add

    t0 = time.monotonic()
    src = build(db, "src_frags", num_fragments)
    build_s = time.monotonic() - t0
    assert len(src.to_lance().get_fragments()) == num_fragments
    assert dataset_uses_stable_row_ids(src.to_lance())

    mv = _identity_mv(db, src, "mv_frags")

    # Populating refresh (processes all F fragments; excluded from the
    # incremental measurement).
    t0 = time.monotonic()
    mv.refresh(_admission_check=False)
    initial_refresh_s = time.monotonic() - t0
    assert _mv_ids(mv) == _oracle_ids(src)

    # One appended fragment is the entire source delta ...
    src.add(_frag_block(num_fragments, _ROWS_PER_FRAGMENT))

    # ... yet the refresh processes all F+1 fragments (empty fragment map
    # for v2), which is what this timing captures.
    t0 = time.monotonic()
    mv.refresh(_admission_check=False)
    incremental_refresh_s = time.monotonic() - t0
    assert _mv_ids(mv) == _oracle_ids(src)

    _REFRESH_TIMES[num_fragments] = incremental_refresh_s

    result = make_result(
        scale=num_fragments,
        latencies=[incremental_refresh_s],
        error_count=0,
        elapsed_s=build_s + initial_refresh_s + incremental_refresh_s,
        metadata={
            "builder_mode": builder_mode,
            "build_s": build_s,
            "initial_refresh_s": initial_refresh_s,
            "incremental_refresh_s": incremental_refresh_s,
            "rows_per_fragment": _ROWS_PER_FRAGMENT,
        },
    )
    log_result(result)
    _LOG.info(
        "F=%d: build=%.1fs initial_refresh=%.1fs incremental_refresh=%.1fs "
        "(curve so far: %s)",
        num_fragments,
        build_s,
        initial_refresh_s,
        incremental_refresh_s,
        {f: round(t, 2) for f, t in sorted(_REFRESH_TIMES.items())},
    )

    if _RATIO_BASE_F in _REFRESH_TIMES and _RATIO_HIGH_F in _REFRESH_TIMES:
        base = _REFRESH_TIMES[_RATIO_BASE_F]
        high = _REFRESH_TIMES[_RATIO_HIGH_F]
        ratio = high / base if base > 0 else float("inf")
        if ratio > _MAX_REFRESH_TIME_RATIO:
            _LOG.warning(
                "REFRESH TIME GROWTH: t(%d)/t(%d) = %.1fx (> %.1fx) -- "
                "incremental refresh cost tracks total fragment count "
                "(GEN-629)",
                _RATIO_HIGH_F,
                _RATIO_BASE_F,
                ratio,
                _MAX_REFRESH_TIME_RATIO,
            )
        else:
            _LOG.info(
                "refresh time ratio t(%d)/t(%d) = %.1fx",
                _RATIO_HIGH_F,
                _RATIO_BASE_F,
                ratio,
            )
