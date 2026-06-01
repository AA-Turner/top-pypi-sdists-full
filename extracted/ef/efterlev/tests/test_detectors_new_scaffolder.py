"""Tests for `efterlev detectors new <id>` -- the contributor scaffolder.

Held in LIMITATIONS.md "Future ideas" since the v0.1.18+ planning surface;
shipped as the v0.1.53 single-PR feature. The scaffolder generates the
canonical 5-file detector folder skeleton plus fixture directories so a
new contributor doesn't have to remember the convention by reading
existing detectors.

The tests below use a tmp_path detectors-root override (via
monkeypatching `efterlev.detectors.__file__`) so the scaffolder writes
into the tmp tree and the real source tree stays untouched.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from efterlev.cli.main import app

runner = CliRunner()


def _redirect_detectors_root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Make `efterlev.detectors.__file__` point at a tmp_path so the
    scaffolder writes into tmp instead of the real source tree."""
    import efterlev.detectors as det_pkg

    fake_init = tmp_path / "detectors" / "__init__.py"
    fake_init.parent.mkdir(parents=True, exist_ok=True)
    fake_init.write_text("", encoding="utf-8")
    monkeypatch.setattr(det_pkg, "__file__", str(fake_init))
    return fake_init.parent


def test_scaffolds_5_file_folder_with_fixtures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`efterlev detectors new aws.foo_bar` creates the canonical
    folder shape: __init__.py + detector.py + mapping.yaml +
    evidence.yaml + README.md, plus fixtures/should_{match,not_match}/.gitkeep."""
    detectors_root = _redirect_detectors_root(monkeypatch, tmp_path)
    result = runner.invoke(
        app,
        ["detectors", "new", "aws.foo_bar", "--ksi", "KSI-CNA-RVP", "--control", "SI-3"],
    )
    assert result.exit_code == 0, result.output
    folder = detectors_root / "aws" / "foo_bar"
    for filename in (
        "__init__.py",
        "detector.py",
        "mapping.yaml",
        "evidence.yaml",
        "README.md",
        "fixtures/should_match/.gitkeep",
        "fixtures/should_not_match/.gitkeep",
    ):
        assert (folder / filename).is_file(), f"expected {filename} to exist"


def test_detector_py_stub_has_decorator_and_empty_detect(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The generated detector.py is a registration-ready stub: it has
    the @detector decorator with the requested id/ksis/controls/source,
    and a detect() function that returns []."""
    detectors_root = _redirect_detectors_root(monkeypatch, tmp_path)
    result = runner.invoke(
        app,
        [
            "detectors",
            "new",
            "aws.bar_baz",
            "--ksi",
            "KSI-CNA-MAT",
            "--ksi",
            "KSI-CNA-RVP",
            "--control",
            "SC-7",
            "--source",
            "terraform",
        ],
    )
    assert result.exit_code == 0
    detector_py = (detectors_root / "aws" / "bar_baz" / "detector.py").read_text(encoding="utf-8")
    assert "@detector(" in detector_py
    assert 'id="aws.bar_baz"' in detector_py
    assert '"KSI-CNA-MAT"' in detector_py
    assert '"KSI-CNA-RVP"' in detector_py
    assert '"SC-7"' in detector_py
    assert 'source="terraform"' in detector_py
    assert "def detect(resources: list[TerraformResource]) -> list[Evidence]:" in detector_py
    assert "return out" in detector_py  # the stub's empty return path


def test_mapping_yaml_includes_ksis_and_controls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """mapping.yaml lists the requested KSIs + controls with TODO
    placeholders for notes."""
    detectors_root = _redirect_detectors_root(monkeypatch, tmp_path)
    result = runner.invoke(
        app,
        ["detectors", "new", "aws.qux", "--ksi", "KSI-X", "--control", "AC-3"],
    )
    assert result.exit_code == 0
    mapping = (detectors_root / "aws" / "qux" / "mapping.yaml").read_text(encoding="utf-8")
    assert "detector_id: aws.qux" in mapping
    assert "id: KSI-X" in mapping
    assert "id: AC-3" in mapping


def test_supplementary_detector_when_no_ksi(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No --ksi provided: the detector is supplementary (800-53-only).
    mapping.yaml's ksis is the empty-list placeholder; the README's
    KSI table notes the supplementary status."""
    detectors_root = _redirect_detectors_root(monkeypatch, tmp_path)
    result = runner.invoke(app, ["detectors", "new", "aws.supp_only", "--control", "SC-99"])
    assert result.exit_code == 0
    mapping = (detectors_root / "aws" / "supp_only" / "mapping.yaml").read_text(encoding="utf-8")
    assert "[]  # supplementary detector (no KSI mapping)" in mapping
    readme = (detectors_root / "aws" / "supp_only" / "README.md").read_text(encoding="utf-8")
    assert "supplementary 800-53-only detector" in readme


def test_refuses_to_overwrite_existing_folder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Re-running with the same id (or running where the folder
    already exists) refuses with exit 1 and a clear error."""
    _redirect_detectors_root(monkeypatch, tmp_path)
    first = runner.invoke(app, ["detectors", "new", "aws.dup_test"])
    assert first.exit_code == 0
    second = runner.invoke(app, ["detectors", "new", "aws.dup_test"])
    assert second.exit_code == 1
    assert "already exists" in second.output


def test_rejects_invalid_detector_id_format(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Detector id must be `<cloud>.<snake_case_name>`."""
    _redirect_detectors_root(monkeypatch, tmp_path)
    result = runner.invoke(app, ["detectors", "new", "no_dot_in_id"])
    assert result.exit_code == 2
    assert "must be `<cloud>.<snake_case_name>`" in result.output


def test_rejects_unsupported_cloud(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Cloud must be one of aws / github / gcp / azure."""
    _redirect_detectors_root(monkeypatch, tmp_path)
    result = runner.invoke(app, ["detectors", "new", "oracle.foo"])
    assert result.exit_code == 2
    assert "unsupported cloud `oracle`" in result.output


def test_rejects_non_snake_case_name(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Detector name must be snake_case starting with a letter."""
    _redirect_detectors_root(monkeypatch, tmp_path)
    # Starts with a digit -- rejected.
    result = runner.invoke(app, ["detectors", "new", "aws.1foo"])
    assert result.exit_code == 2
    assert "must be snake_case starting with a letter" in result.output


def test_rejects_unsupported_source(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """--source must be one of terraform / terraform-plan / github."""
    _redirect_detectors_root(monkeypatch, tmp_path)
    result = runner.invoke(app, ["detectors", "new", "aws.foo", "--source", "kubernetes"])
    assert result.exit_code == 2
    assert "unsupported source `kubernetes`" in result.output
