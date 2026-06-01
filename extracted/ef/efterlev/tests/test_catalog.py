"""Tests for `efterlev catalog` — the Stage 0 KSI reference listing.

Like `plan`, `catalog` runs with no workspace and reads only bundled data.
These pin the per-KSI grouping/classification against the vendored catalog
(60 KSIs across 11 themes), the `--theme` filter, the JSON shape, and a
no-workspace CliRunner smoke. The evidence classification is shared with
`plan` (via `classify_ksi`), so the per-category totals must match plan's
34 scanner / 23 procedural / 3 hybrid split.
"""

from __future__ import annotations

import json

import pytest
from typer.testing import CliRunner

from efterlev.cli import catalog as cat
from efterlev.cli.main import app

runner = CliRunner()


# --- build_catalog -----------------------------------------------------


def test_build_catalog_covers_whole_baseline() -> None:
    r = cat.build_catalog()
    assert r.total == 60
    assert len(r.themes) == 11
    # Themes are id-sorted; every entry belongs to its theme.
    assert [t.theme_id for t in r.themes] == sorted(t.theme_id for t in r.themes)
    for t in r.themes:
        for e in t.entries:
            assert e.theme_id == t.theme_id


def test_build_catalog_category_totals_match_plan() -> None:
    r = cat.build_catalog()
    cats = [e.category for t in r.themes for e in t.entries]
    assert cats.count("scanner") == 34
    assert cats.count("procedural") == 23
    assert cats.count("hybrid") == 3
    assert cats.count("uncovered") == 0


def test_build_catalog_entries_have_controls_and_statement() -> None:
    r = cat.build_catalog()
    afr = next(t for t in r.themes if t.theme_id == "AFR")
    ads = next(e for e in afr.entries if e.ksi_id == "KSI-AFR-ADS")
    assert ads.category == "procedural"
    assert ads.controls  # AFR-ADS maps to several 800-53 controls
    # KSI statements are present for most KSIs.
    assert any(e.statement for t in r.themes for e in t.entries)


def test_build_catalog_theme_filter() -> None:
    r = cat.build_catalog(theme="afr")  # case-insensitive
    assert len(r.themes) == 1
    assert r.themes[0].theme_id == "AFR"
    assert r.total == 10


def test_build_catalog_unknown_theme_raises() -> None:
    with pytest.raises(ValueError, match="unknown theme"):
        cat.build_catalog(theme="ZZZ")


def test_build_catalog_unknown_baseline_raises() -> None:
    with pytest.raises(ValueError, match="unknown baseline"):
        cat.build_catalog(baseline="fedramp-20x-high")


# --- render + json -----------------------------------------------------


def test_render_lists_ksis_and_categories() -> None:
    text = cat.render_catalog(cat.build_catalog(theme="AFR"))
    assert "AFR — Authorization by FedRAMP" in text
    assert "KSI-AFR-ADS" in text
    assert "[manifest" in text
    assert "controls:" in text


def test_catalog_to_dict_shape() -> None:
    d = cat.catalog_to_dict(cat.build_catalog(theme="SCR"))
    assert d["baseline"] == "fedramp-20x-moderate"
    assert d["total"] == 2
    themes = d["themes"]
    assert isinstance(themes, list) and len(themes) == 1
    ksi = themes[0]["ksis"][0]
    assert set(ksi) == {"id", "name", "evidence", "controls", "statement"}
    assert ksi["evidence"] in {"scanner", "procedural", "hybrid", "uncovered"}


# --- CLI smoke (no workspace) ------------------------------------------


def test_cli_catalog_runs_without_workspace() -> None:
    result = runner.invoke(app, ["catalog"])
    assert result.exit_code == 0
    assert "Key Security Indicators" in result.stdout
    assert "KSI-" in result.stdout


def test_cli_catalog_json_parses() -> None:
    result = runner.invoke(app, ["catalog", "--theme", "SCR", "--json"])
    assert result.exit_code == 0
    parsed = json.loads(result.stdout)
    assert parsed["total"] == 2
    assert parsed["themes"][0]["id"] == "SCR"


def test_cli_catalog_unknown_theme_exits_2() -> None:
    result = runner.invoke(app, ["catalog", "--theme", "nope"])
    assert result.exit_code == 2
