"""Tests for the worklist — `efterlev next`.

The substance (ranking, command selection, manifest precision, the boundary
item) lives in the pure `classified_work_items` / `rank_work_items` functions and
is tested directly. `build_worklist`'s uninitialized stage + the CLI are smoke-
tested without a seeded store.
"""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from efterlev.cli.main import app
from efterlev.worklist import (
    WorkItem,
    build_worklist,
    classified_work_items,
    rank_work_items,
)

runner = CliRunner()

_BASELINE = ["KSI-SVC-SNT", "KSI-CNA-RNT", "KSI-AFR-FSI", "KSI-AFR-ADS", "KSI-IAM-MFA"]
_PROCEDURAL = {"KSI-AFR-FSI", "KSI-AFR-ADS"}


def test_ranking_high_quick_before_high_involved_before_medium() -> None:
    items = [
        WorkItem("med", "", "c", "medium", "quick"),
        WorkItem("hi-involved", "", "c", "high", "involved"),
        WorkItem("hi-quick", "", "c", "high", "quick"),
    ]
    ranked = [w.title for w in rank_work_items(items)]
    assert ranked == ["hi-quick", "hi-involved", "med"]


def test_classified_selects_the_right_command_per_status() -> None:
    statuses = {
        "KSI-SVC-SNT": "not_implemented",  # non-procedural gap → remediate
        "KSI-CNA-RNT": "partial",  # partial → strengthen (remediate)
        "KSI-AFR-FSI": "evidence_layer_inapplicable",  # procedural, no manifest → draft
        "KSI-AFR-ADS": "evidence_layer_inapplicable",  # procedural, HAS manifest → skip
        "KSI-IAM-MFA": "implemented",  # done → no item
    }
    items = classified_work_items(
        _BASELINE,
        _PROCEDURAL,
        statuses,
        manifest_covered={"KSI-AFR-ADS"},
        boundary_declared=True,
    )
    by_ksi = {i.ksi_id: i for i in items if i.ksi_id}
    assert by_ksi["KSI-SVC-SNT"].command == "efterlev agent remediate --ksi KSI-SVC-SNT"
    assert by_ksi["KSI-SVC-SNT"].impact == "high"
    assert by_ksi["KSI-CNA-RNT"].command == "efterlev agent remediate --ksi KSI-CNA-RNT"
    assert by_ksi["KSI-AFR-FSI"].command == "efterlev manifests draft KSI-AFR-FSI"
    assert "KSI-AFR-ADS" not in by_ksi  # already has a manifest → not surfaced
    assert "KSI-IAM-MFA" not in by_ksi  # implemented → not surfaced


def test_undeclared_boundary_is_the_top_item() -> None:
    items = classified_work_items(
        _BASELINE,
        _PROCEDURAL,
        {"KSI-SVC-SNT": "not_implemented"},
        manifest_covered=set(),
        boundary_declared=False,
    )
    assert items[0].command == "efterlev boundary discover"
    assert items[0].impact == "high" and items[0].effort == "quick"


def test_declared_boundary_omits_the_boundary_item() -> None:
    items = classified_work_items(
        _BASELINE,
        _PROCEDURAL,
        {"KSI-SVC-SNT": "not_implemented"},
        manifest_covered=set(),
        boundary_declared=True,
    )
    assert all("boundary discover" not in i.command for i in items)


def test_uninitialized_workspace(tmp_path: Path) -> None:
    wl = build_worklist(tmp_path)
    assert wl.stage == "uninitialized"
    assert "efterlev init" in wl.headline
    cmds = [i.command for i in wl.items]
    assert "efterlev boundary discover" in cmds  # orient first
    assert any("efterlev init" in c for c in cmds)


def test_cli_uninitialized(tmp_path: Path) -> None:
    result = runner.invoke(app, ["next", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert "efterlev init" in result.output


def test_cli_json_shape(tmp_path: Path) -> None:
    result = runner.invoke(app, ["next", "--target", str(tmp_path), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["stage"] == "uninitialized"
    assert isinstance(data["items"], list) and data["items"]
    assert {"title", "why", "command", "impact", "effort", "ksi_id"} <= set(data["items"][0])
