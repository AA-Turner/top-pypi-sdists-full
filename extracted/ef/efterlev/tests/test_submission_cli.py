"""Smoke tests for `efterlev.cli.submission_cli.run_submission_package`.

Exercises the CLI wrapper (exit codes, output rendering, output-path resolution).
Complements `test_submission_package.py` which covers the underlying
`build_submission` primitive.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from efterlev.cli.submission_cli import run_submission_package


def _seed_minimal_artifacts(root: Path) -> None:
    """Lay down the minimum reports + manifests that build_submission discovers.

    Mirrors `tests/test_submission_package.py::_seed_artifacts` (full set), so
    the CLI smoke tests have a complete bundle to package without coupling to
    the primitive's discovery glob details.
    """
    reports = root / ".efterlev" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "poam").mkdir(exist_ok=True)
    (reports / "oscal").mkdir(exist_ok=True)
    (root / ".efterlev" / "manifests").mkdir(exist_ok=True)

    (reports / "attestation-20260527.json").write_text('{"frmr": "yes"}', encoding="utf-8")
    (reports / "poam" / "poam-20260527.md").write_text("# POA&M\n", encoding="utf-8")
    (reports / "oscal" / "poam-20260527.json").write_text('{"oscal": "poam"}', encoding="utf-8")
    (reports / "oscal" / "component-definition-20260527.json").write_text(
        '{"oscal": "cd"}', encoding="utf-8"
    )
    (reports / "gap-20260527.html").write_text("<html>gap</html>", encoding="utf-8")
    (reports / "documentation-20260527.html").write_text("<html>doc</html>", encoding="utf-8")
    (root / ".efterlev" / "manifests" / "ksi-afr-per.yml").write_text(
        "ksi_id: KSI-AFR-PER\n", encoding="utf-8"
    )


def test_returns_1_when_efterlev_dir_missing(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """No `.efterlev/` → friendly stderr message, exit 1."""
    rc = run_submission_package(tmp_path, output=None, archive=True, package_version=None)
    assert rc == 1
    err = capsys.readouterr().err
    assert "no `.efterlev/` directory" in err
    assert "efterlev init" in err


def test_archive_mode_produces_zip(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Happy path with archive=True: zip written, success summary rendered."""
    _seed_minimal_artifacts(tmp_path)

    rc = run_submission_package(tmp_path, output=None, archive=True, package_version="0.0.1")
    out = capsys.readouterr().out

    assert rc == 0
    assert "Building submission package" in out
    assert "Hand this to your 3PAO" in out
    assert "Version:    0.0.1" in out

    # Default zip output lives under `<root>/efterlev-out/submissions/`
    # (visible-output split landed at v0.1.160 / #365).
    submission_dir = tmp_path / "efterlev-out" / "submissions"
    zips = list(submission_dir.glob("*.zip"))
    assert len(zips) == 1
    with zipfile.ZipFile(zips[0]) as z:
        names = z.namelist()
    assert any("attestation/" in n for n in names)
    assert any("poam/" in n for n in names)


def test_directory_mode_writes_files(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """archive=False: writes a directory tree of artifacts, not a zip."""
    _seed_minimal_artifacts(tmp_path)

    rc = run_submission_package(tmp_path, output=None, archive=False, package_version=None)
    out = capsys.readouterr().out

    assert rc == 0
    # In directory mode the CLI suppresses the "Size:" line that the archive
    # branch prints; assert on the rendered shape rather than a sentinel string.
    assert "Size:" not in out

    submission_dir = tmp_path / "efterlev-out" / "submissions"
    # Latest run directory: pick the only child (deterministic for one run).
    children = [p for p in submission_dir.iterdir() if p.is_dir()]
    assert len(children) == 1
    run_dir = children[0]
    assert (run_dir / "README.md").is_file()
    assert (run_dir / "index.json").is_file()


def test_custom_output_path_is_honored(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Explicit `--output <path>` overrides the default `efterlev-out/submissions/` location."""
    _seed_minimal_artifacts(tmp_path)
    custom_out = tmp_path / "deliverable.zip"

    rc = run_submission_package(tmp_path, output=custom_out, archive=True, package_version=None)
    out = capsys.readouterr().out

    assert rc == 0
    assert custom_out.exists()
    assert str(custom_out) in out
