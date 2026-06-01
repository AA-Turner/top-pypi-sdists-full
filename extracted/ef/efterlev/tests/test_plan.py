"""Tests for `efterlev plan` — the Stage 0 pre-scan orientation command.

`plan` runs with no workspace, no IaC, no API key — it reads only bundled
package data (FRMR catalog + detector registry + manifest templates +
inheritance profiles). These tests pin the classification math against
the vendored catalog (60 KSIs / 11 themes, 34 automated-only + 23
procedural-only + 3 hybrid), the architecture overlay, and the rendered
output, plus a no-workspace CliRunner smoke.
"""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from efterlev.cli import plan as plan_mod
from efterlev.cli.main import app

runner = CliRunner()


# --- build_plan (deterministic, no workspace) --------------------------


def test_build_plan_baseline_shape() -> None:
    r = plan_mod.build_plan()
    assert r.baseline == "fedramp-20x-moderate"
    assert r.total == 60
    assert r.theme_count == 11
    # The buckets are disjoint and cover the whole baseline.
    assert r.automated_only + r.procedural_only + r.hybrid + r.uncovered == 60
    assert r.automated_only == 34
    assert r.procedural_only == 23
    assert r.hybrid == 3
    assert r.uncovered == 0


def test_build_plan_theme_rows_sum() -> None:
    r = plan_mod.build_plan()
    assert len(r.themes) == 11
    for row in r.themes:
        assert row.automated_only + row.procedural_only + row.hybrid == row.total
        assert row.needs_manifest == row.procedural_only + row.hybrid
    # AFR is the most manifest-heavy theme; it must sort first.
    assert r.themes[0].theme_id == "AFR"
    assert r.themes[0].needs_manifest == 10
    # Fully automated themes carry no manifest work.
    assert set(r.fully_automated_themes) == {"CNA", "IAM", "SCR"}


def test_build_plan_no_architecture_overlay() -> None:
    r = plan_mod.build_plan()
    assert r.architecture is None
    assert r.inherited_ksis == []
    assert r.inherited_profile_known is False


def test_build_plan_serverless_overlay() -> None:
    r = plan_mod.build_plan(architecture="serverless")
    assert r.inherited_profile == "aws-serverless"
    assert r.inherited_profile_known is True
    assert set(r.inherited_ksis) == {
        "KSI-CNA-IBP",
        "KSI-CNA-OFA",
        "KSI-CNA-MAT",
        "KSI-CNA-RVP",
    }


def test_build_plan_unknown_architecture_graceful() -> None:
    r = plan_mod.build_plan(architecture="ec2")
    assert r.architecture == "ec2"
    assert r.inherited_profile_known is False
    assert r.inherited_ksis == []


def test_build_plan_rejects_unknown_baseline() -> None:
    with pytest.raises(ValueError, match="unknown baseline"):
        plan_mod.build_plan(baseline="fedramp-20x-high")


# --- render_plan -------------------------------------------------------


def test_render_contains_key_sections() -> None:
    text = plan_mod.render_plan(plan_mod.build_plan())
    assert "FedRAMP 20x Moderate" in text
    assert "60 Key Security Indicators across 11 themes" in text
    assert "Automated from your IaC / runtime" in text
    assert "You author an Evidence Manifest" in text
    assert "Realistic next steps" in text
    # No-architecture render nudges toward the overlay.
    assert "--architecture serverless" in text


def test_render_serverless_lists_inherited() -> None:
    text = plan_mod.render_plan(plan_mod.build_plan(architecture="serverless"))
    assert "Architecture: serverless" in text
    assert "CSP-inherited" in text
    assert "KSI-CNA-IBP" in text
    assert "efterlev scope --inherited aws-serverless" in text


def test_render_promises_no_side_effects() -> None:
    text = plan_mod.render_plan(plan_mod.build_plan())
    assert "no files written" in text
    assert "no API calls" in text


# --- CLI smoke (no workspace) ------------------------------------------


def test_cli_plan_runs_without_workspace(tmp_path) -> None:
    # CliRunner gives a non-TTY stdin, so the interactive arch prompt is
    # skipped and the agnostic view renders.
    result = runner.invoke(app, ["plan"])
    assert result.exit_code == 0
    assert "your KSI landscape" in result.stdout


def test_cli_plan_architecture_flag() -> None:
    result = runner.invoke(app, ["plan", "--architecture", "serverless"])
    assert result.exit_code == 0
    assert "KSI-CNA-IBP" in result.stdout


def test_cli_plan_unknown_baseline_exits_2() -> None:
    result = runner.invoke(app, ["plan", "--baseline", "nope"])
    assert result.exit_code == 2
