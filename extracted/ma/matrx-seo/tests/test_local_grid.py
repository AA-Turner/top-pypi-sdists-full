"""Local rank grid geometry, matching and run semantics (OPENSEO-TOOLS-SPEC §5.4, T4).

The vectors are OpenSEO's own (every-app/open-seo@0ffff93,
``src/server/mcp/tools/local-seo-tools.test.ts`` "get_local_rank_grid" and
``local-seo-shared.ts``): the same center, spacing and expected coordinate
strings, so a drift from their formulas fails here.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_seo.local_grid import (
    GridAborted,
    GridAllFailed,
    GridPoint,
    PointResult,
    build_grid,
    business_data_coordinate,
    classify_point_failure,
    format_coordinate,
    grid_zoom,
    listing_search_coordinate,
    maps_coordinate,
    match_business,
    null_rank_reading,
    point_from_items,
    render_grid,
    run_grid,
    summarize,
)


def test_their_3x3_vector_at_latitude_40_with_2km_spacing() -> None:
    zoom = grid_zoom(2, 40)
    assert zoom == 13
    coords = [maps_coordinate(p.lat, p.lng, zoom) for p in build_grid(40, -74, 3, 2)]
    # Row-major, row 0 the NORTHERN edge — their exact strings.
    assert coords == [
        "40.0180874,-74.0234532,13z",
        "40.0180874,-74,13z",
        "40.0180874,-73.9765468,13z",
        "40,-74.0234532,13z",
        "40,-74,13z",
        "40,-73.9765468,13z",
        "39.9819126,-74.0234532,13z",
        "39.9819126,-74,13z",
        "39.9819126,-73.9765468,13z",
    ]


def test_5x5_is_row_major_north_first_and_centered() -> None:
    pts = build_grid(33.68, -117.83, 5, 1)
    assert len(pts) == 25
    assert (pts[0].row, pts[0].col) == (0, 0) and pts[0].lat > pts[24].lat
    assert pts[12].lat == 33.68 and pts[12].lng == -117.83
    assert pts[0].lng < pts[4].lng


def test_zoom_formula_and_clamp() -> None:
    # floor(log2(24045·cos(lat)/spacing)), clamped to 4..18.
    assert grid_zoom(0.25, 0) == 16
    assert grid_zoom(10, 60) == 10
    assert grid_zoom(0.25, 89.9999) >= 4
    assert grid_zoom(10, 89.9999) == 4  # cosine floor keeps it finite, clamp keeps it legal
    assert grid_zoom(0.001, 0) == 18


def test_near_polar_longitude_step_uses_the_cosine_floor() -> None:
    pts = build_grid(89.9999, 0, 3, 1)
    lon_step = pts[2].lng - pts[1].lng
    assert lon_step == pytest.approx(1 / (111.32 * 0.01), rel=1e-6)


def test_grid_refuses_sizes_and_spacing_outside_the_contract() -> None:
    with pytest.raises(ValueError):
        build_grid(40, -74, 4, 2)
    with pytest.raises(ValueError):
        build_grid(40, -74, 3, 0.1)
    with pytest.raises(ValueError):
        build_grid(40, -74, 3, 11)


def test_coordinate_formatters_match_their_shared_helpers() -> None:
    assert format_coordinate(33.123456789) == "33.1234568"
    assert format_coordinate(-84.987654321) == "-84.9876543"
    assert format_coordinate(40.0) == "40"
    # business_data: meters, clamped 200..199999 (their business.test.ts vector).
    assert business_data_coordinate(33.123456789, -84.987654321, 5) == "33.1234568,-84.9876543,5000"
    assert business_data_coordinate(1, 2, 0.01).endswith(",200")
    assert business_data_coordinate(1, 2, 500).endswith(",199999")
    # listings search: whole kilometers, at least 1.
    assert listing_search_coordinate(33.1, -84.9, 5) == "33.1,-84.9,5"
    assert listing_search_coordinate(33.1, -84.9, 0.3) == "33.1,-84.9,1"


def test_match_precedence_is_cid_then_place_id_then_name_across_all_rows() -> None:
    rows = [
        {"rank_absolute": 1, "title": "Acme Cafe Downtown", "cid": "999", "place_id": "pX"},
        {"rank_absolute": 2, "title": "Other", "cid": "555", "place_id": "p1"},
        {"rank_absolute": 3, "title": "Third", "cid": "123"},
    ]
    item, by = match_business(rows, cid="123", place_id="p1", name="acme cafe")
    assert (item["rank_absolute"], by) == (3, "cid")
    item, by = match_business(rows, cid="nope", place_id="p1", name="acme cafe")
    assert (item["rank_absolute"], by) == (2, "place_id")
    item, by = match_business(rows, name="ACME cafe")
    assert (item["rank_absolute"], by) == (1, "name")
    assert match_business(rows, cid="x") == (None, None)


def test_point_records_results_count_and_top_business_when_target_absent() -> None:
    point = GridPoint(0, 0, 40.0, -74.0)
    result, match, _ = point_from_items(
        point,
        [{"rank_absolute": 1, "title": "Other Cafe", "cid": "999"}],
        cid="123",
        place_id=None,
        name=None,
    )
    assert match is None
    assert result.rank is None and result.results_count == 1
    assert result.top_result == {"name": "Other Cafe", "cid": "999"}


def test_null_rank_is_read_against_results_count() -> None:
    assert null_rank_reading(None, 20) is None
    assert null_rank_reading(0, 20) == "no_results"
    assert null_rank_reading(3, 20) == "sparse"
    assert null_rank_reading(20, 20) == "outranked"


def test_summary_and_text_grid() -> None:
    pts = [PointResult(0, c, 0, 0, rank=2, results_count=20) for c in range(3)]
    pts += [PointResult(1, 0, 0, 0, rank=None, results_count=20)]
    pts += [PointResult(1, 1, 0, 0, error="failed; may still be charged")]
    pts += [PointResult(1, 2, 0, 0, rank=11, results_count=20)]
    pts += [PointResult(2, c, 0, 0, rank=4, results_count=20) for c in range(3)]
    s = summarize(pts)
    assert s == {
        "points_found": 7,
        "points_searched": 9,
        "points_failed": 1,
        "points_pending": 0,
        "avg_rank": round((2 * 3 + 11 + 4 * 3) / 7, 2),
        "top3": 3,
        "top10": 6,
    }
    assert render_grid(pts, 3).splitlines() == [" 2  2  2", " –  x 11", " 4  4  4"]


def test_failure_classes() -> None:
    assert (
        classify_point_failure("ProviderResponseError", "DataForSEO 40200: Payment Required.")
        == "abort"
    )
    assert (
        classify_point_failure("ProviderResponseError", "status_code 40101 Authentication failed")
        == "abort"
    )
    assert classify_point_failure("BudgetExceededError", "monthly ceiling") == "abort"
    assert classify_point_failure("ProviderResponseError", "40501 No Search Results.") == "empty"
    assert classify_point_failure("TimeoutError", "upstream blew up") == "point"


def _grid() -> list[GridPoint]:
    return build_grid(40, -74, 3, 2)


def test_credit_error_aborts_the_remaining_points() -> None:
    calls: list[GridPoint] = []

    async def search(p: GridPoint) -> PointResult:
        calls.append(p)
        raise RuntimeError("DataForSEO 40200: Payment Required. Insufficient balance")

    with pytest.raises(GridAborted) as caught:
        asyncio.run(run_grid(_grid(), search, concurrency=3))
    # Only the first batch may dispatch; later batches must not bill.
    assert len(calls) == 3
    assert len(caught.value.searched) == 3


def test_a_single_point_failure_keeps_the_grid() -> None:
    seen = 0

    async def search(p: GridPoint) -> PointResult:
        nonlocal seen
        seen += 1
        if (p.row, p.col) == (0, 0):
            raise RuntimeError("upstream blew up")
        return PointResult(p.row, p.col, p.lat, p.lng, rank=3, results_count=20)

    out = asyncio.run(run_grid(_grid(), search, concurrency=3))
    assert seen == 9
    assert out[0].error.startswith("failed: upstream blew up; may still be charged")
    assert out[0].rank is None
    assert summarize(out)["points_found"] == 8
    assert "x" in render_grid(out, 3)


def test_all_points_failing_raises_the_last_error_never_does_not_rank() -> None:
    async def search(p: GridPoint) -> PointResult:
        raise RuntimeError("upstream blew up")

    with pytest.raises(GridAllFailed, match="upstream blew up"):
        asyncio.run(run_grid(_grid(), search, concurrency=3))


def test_no_search_results_is_an_empty_point_not_a_failure() -> None:
    async def search(p: GridPoint) -> PointResult:
        raise RuntimeError("DataForSEO task failed: 40501 No Search Results.")

    out = asyncio.run(run_grid(_grid(), search, concurrency=3))
    assert all(p.error is None and p.results_count == 0 and p.rank is None for p in out)


# ── the dispatch budget (reopened D/E, 2026-09-28) ─────────────────────────


class _Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_grid_stops_dispatching_before_the_budget_and_marks_the_rest_pending() -> None:
    clock = _Clock()

    async def search(p: GridPoint) -> PointResult:
        clock.now += 20  # each batch takes 20 s on this clock
        return PointResult(p.row, p.col, p.lat, p.lng, rank=1, results_count=20)

    out = asyncio.run(run_grid(_grid(), search, concurrency=3, deadline=50, clock=clock))
    searched = [p for p in out if not p.pending]
    pending = [p for p in out if p.pending]
    # Batch 1 ends at t=60 > 50: batch 2 is never dispatched (never billed).
    assert len(out) == 9 and pending and searched
    assert all(p.rank is None and p.error is None for p in pending)
    assert summarize(out)["points_pending"] == len(pending)


def test_a_batch_still_running_at_the_deadline_is_stopped_with_a_named_cause() -> None:
    async def search(p: GridPoint) -> PointResult:
        if p.row == 0 and p.col == 1:
            await asyncio.sleep(5)
        return PointResult(p.row, p.col, p.lat, p.lng, rank=2, results_count=20)

    import time

    out = asyncio.run(run_grid(_grid(), search, concurrency=3, deadline=time.monotonic() + 0.3))
    slow = out[1]
    assert slow.error and "dispatch budget" in slow.error and "call rank_grid again" in slow.error
    assert all(p.pending for p in out[3:])


def test_a_failed_point_names_its_cause_and_the_next_step() -> None:
    async def search(p: GridPoint) -> PointResult:
        if (p.row, p.col) == (1, 1):
            raise RuntimeError("SEO collection run abc is already processing")
        return PointResult(p.row, p.col, p.lat, p.lng, rank=3, results_count=20)

    out = asyncio.run(run_grid(_grid(), search, concurrency=3))
    err = out[4].error
    assert "already processing" in err and "may still be charged" in err
    assert "call rank_grid again" in err
