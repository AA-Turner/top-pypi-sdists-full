"""VISION-REACH W2 verifier (2026-10-02): a dataset page the size budget CUTS says it is partial.

Seen live (conversation 49b77b18-…): `dataset get` with limit 215 on a 215-row referral-inquiries table
answered `"count": 215` and NO PARTIAL note while carrying 163 rows — the 40k budget cut the rest after
the page had been judged whole. A model trusting `count` reports 215 rows it never saw.

SUT: `_dataset_get` (and `usertable_get_data`) — the page's count, partial flag and note after the cut.
Stubbed: the record-store arm (a dependency, answering a whole 215-row page the way the live arm did) and
the relation-wording pass (identity). Break caught: the count/partial computed before the cut."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.tools.implementations import datasets_tools as dt

SOURCES = ["Physician fax", "Website form", "Google Business Profile", "Phone call", "Insurance portal", "Walk-in"]


def _rows(n: int, width: int) -> list[dict]:
    return [
        {"row_id": f"5dfad433-37da-44ba-a2f0-{i:012d}",
         "data": {"caller": f"Caller {i}", "source": SOURCES[i % 6], "status": "New", "received": "2026-09-04",
                  "reason": "post-op ACL rehab referral " + "notes " * width},
         "created_at": "2026-10-03 00:37:17+00:00"}
        for i in range(n)
    ]


class _Arm:
    def __init__(self, rows: list[dict], total: int) -> None:
        self.rows, self.total = rows, total

    async def get(self, table_id, *, include, limit, offset, sort_by=None, sort_order="asc"):
        page = self.rows[offset: offset + limit]
        return {"dataset_id": table_id, "rows": page, "count": len(page), "offset": offset, "limit": limit,
                "total_rows": self.total}


@pytest.fixture
def world(monkeypatch):
    def install(rows, total):
        monkeypatch.setattr(dt, "_store_arm", lambda: _Arm(rows, total))

        async def same(_table, rows, _ctx):
            return rows

        monkeypatch.setattr(dt, "_rows_in_words", same)
    return install


CTX = SimpleNamespace(call_id="partial-page")


@pytest.mark.parametrize(("n", "width"), [(215, 30), (180, 60)])
async def test_a_page_cut_by_the_budget_reports_the_rows_it_carries_and_says_partial(world, n, width) -> None:
    world(_rows(n, width), n)
    res = await dt._dataset_get({"dataset_id": "ccdeb64c-4bf5-4e84-98b1-ee8defdb2bd3", "limit": n, "include": "data"}, CTX, 0.0)
    out = res.output
    carried = len(out["rows"])
    assert out["cap"]["rows_truncated"] is True and carried < n
    assert out["count"] == carried
    assert out["partial"] is True
    assert f"PARTIAL: rows 1-{carried} of {n}" in out["totals_note"]
    assert f"offset {carried}" in out["totals_note"]


async def test_a_whole_page_that_fits_is_not_called_partial(world) -> None:
    world(_rows(20, 1), 20)
    res = await dt._dataset_get({"dataset_id": "ccdeb64c-4bf5-4e84-98b1-ee8defdb2bd3", "limit": 50, "include": "data"}, CTX, 0.0)
    assert res.output["count"] == 20 and "partial" not in res.output


async def test_the_table_reader_says_the_cut_too(world) -> None:
    world(_rows(215, 30), 215)
    res = await dt.usertable_get_data({"table_id": "ccdeb64c-4bf5-4e84-98b1-ee8defdb2bd3", "limit": 215, "offset": 0}, CTX)
    out = res.output
    assert out["count"] == len(out["rows"]) < 215 and out["partial"] is True
    assert "of 215" in out["totals_note"]
