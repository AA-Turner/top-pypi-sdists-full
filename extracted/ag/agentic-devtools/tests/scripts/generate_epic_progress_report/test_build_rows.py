"""Tests for build_rows in generate_epic_progress_report."""

from __future__ import annotations

import datetime as dt

from tests.scripts.generate_epic_progress_report import _node, report


def test_blocked_bucket_only_contains_open_blocked_items_across_hierarchy():
    """Open blocked epic/feature/task items are included, while closed ones are excluded."""
    open_task = _node(301, labels=["speckit:blocked"])
    closed_task = _node(302, state="CLOSED", labels=["speckit:blocked"])
    open_feature = _node(201, labels=["speckit:blocked"], children=[open_task, closed_task])
    closed_feature = _node(202, state="CLOSED", labels=["speckit:blocked"])
    epic = _node(101, labels=["speckit:blocked"], children=[open_feature, closed_feature])

    rows = report.build_rows([epic], dt.datetime.now(dt.timezone.utc), {})

    assert [node.number for node in rows[0].blocked] == [101, 201, 301]
