"""Integration test for wheel payload of bundled skill files."""

from __future__ import annotations

import tomllib
import zipfile
from pathlib import Path

import pytest


def test_setup_templates_use_normal_package_selection() -> None:
    """The setup templates are selected by the package root, not force-included."""
    repo_root = Path(__file__).resolve().parents[2]
    with (repo_root / "pyproject.toml").open("rb") as pyproject:
        wheel_config = tomllib.load(pyproject)["tool"]["hatch"]["build"]["targets"]["wheel"]

    assert wheel_config["packages"] == ["agentic_devtools"]
    assert "agentic_devtools/resources/setup-templates/**" not in wheel_config.get("exclude", [])
    assert "agentic_devtools/resources/setup-templates" not in wheel_config.get("force-include", {})


def test_wheel_contains_skill_entry_and_resource(tmp_path: Path) -> None:
    """Built wheel contains the bundled skills tree with representative files."""
    build = pytest.importorskip("build")
    repo_root = Path(__file__).resolve().parents[2]
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()

    builder = build.ProjectBuilder(str(repo_root))
    try:
        wheel_name = builder.build("wheel", str(dist_dir))
    except Exception as exc:
        cause = getattr(exc, "__cause__", None) or getattr(exc, "__context__", None)
        if (
            exc.__class__.__name__ == "BuildBackendException"
            and cause is not None
            and cause.__class__.__name__ == "BackendUnavailable"
        ):
            pytest.skip(f"wheel backend unavailable in this test environment: {exc}")
        raise
    wheel_path = dist_dir / wheel_name

    with zipfile.ZipFile(wheel_path) as wheel:
        names = wheel.namelist()

    expected_template = "agentic_devtools/resources/setup-templates/llm-providers.copilot.yml"
    assert names.count(expected_template) == 1
    assert len(names) == len(set(names))
    expected_entries = (
        "agentic_devtools/_bundled_skills/skills/run-targeted-checks/SKILL.md",
        "agentic_devtools/_bundled_skills/skills/write-github-commit-message/SKILL.md",
        "agentic_devtools/_bundled_skills/skills/write-github-commit-message/commit-types.md",
        "agentic_devtools/_bundled_skills/skills/ensure-repository-validation/SKILL.md",
        "agentic_devtools/_bundled_skills/skills/agdt-setup-pr/SKILL.md",
        "agentic_devtools/_bundled_skills/skills/fingerprint.py",
    )
    missing = [entry for entry in expected_entries if entry not in names]
    assert not missing, f"Missing bundled skill entries in wheel: {missing}"
