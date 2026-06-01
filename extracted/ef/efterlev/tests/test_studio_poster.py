"""Tests for the Studio share-poster export."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from efterlev.cli.main import app
from efterlev.studio.poster import render_poster_svg, write_poster
from efterlev.studio.web_data import build_studio_data

runner = CliRunner()


def test_render_poster_svg_structure() -> None:
    svg = render_poster_svg(build_studio_data(None))
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert "efterlev" in svg
    assert "READINESS" in svg
    # one verdict tile per KSI (each crisp tile core is an rx="6" rect)
    assert svg.count('rx="6"') == 60
    # legend labels present
    assert "implemented" in svg and "gap" in svg


def test_write_poster_creates_file(tmp_path: Path) -> None:
    out = write_poster(None, tmp_path / "posture.svg")
    assert out.exists()
    assert out.read_text(encoding="utf-8").startswith("<svg")


def test_studio_poster_cli_writes_and_exits(tmp_path: Path) -> None:
    dest = tmp_path / "p.svg"
    result = runner.invoke(app, ["studio", "--poster", str(dest)])
    assert result.exit_code == 0
    assert dest.exists()
    assert "Wrote poster" in result.output
    assert dest.read_text(encoding="utf-8").count('rx="6"') == 60
