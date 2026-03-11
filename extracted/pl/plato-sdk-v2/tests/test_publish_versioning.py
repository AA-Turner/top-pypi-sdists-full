"""Tests for agent/world publish version bump behavior."""

from __future__ import annotations

from datetime import datetime

from typer.testing import CliRunner

from plato.cli import agent as agent_cli
from plato.cli import world as world_cli
from plato.cli.agent import agent_app
from plato.cli.utils import compute_bumped_version
from plato.cli.world import world_app

runner = CliRunner()


class _Result:
    def __init__(self, returncode: int = 0):
        self.returncode = returncode
        self.stdout = ""
        self.stderr = ""


def test_compute_bumped_version_supports_patch_minor_and_dev():
    """Version helper should handle release and dated dev bumps."""
    now = datetime(2026, 3, 11, 14, 5, 6)

    assert compute_bumped_version("1.2.3") == "1.2.4"
    assert compute_bumped_version("1.2.3", minor=True) == "1.3.0"
    assert compute_bumped_version("1.2.3", dev=True, now=now) == "1.2.4.dev20260311140506"
    assert compute_bumped_version("1.2.4.dev20260310120000", dev=True, now=now) == "1.2.4.dev20260311140506"


def test_agent_publish_prompts_and_bumps_patch_version(monkeypatch, tmp_path):
    """Standard agent publish should ask before bumping and then write the new version."""
    pkg_path = tmp_path / "agent"
    pkg_path.mkdir()
    pyproject = pkg_path / "pyproject.toml"
    pyproject.write_text(
        """[project]
name = "example-agent"
version = "1.2.3"
description = "Example agent"
"""
    )

    dist_dir = pkg_path / "dist"
    dist_dir.mkdir()
    (dist_dir / "example_agent-1.2.4-py3-none-any.whl").write_text("wheel")

    monkeypatch.setattr(agent_cli, "require_api_key", lambda: "test-key")
    monkeypatch.setattr(agent_cli.subprocess, "run", lambda *args, **kwargs: _Result())

    result = runner.invoke(agent_app, ["publish", str(pkg_path)], input="y\n")

    assert result.exit_code == 0
    assert "Bump version (patch) from 1.2.3 to 1.2.4?" in result.output
    assert 'version = "1.2.4"' in pyproject.read_text()


def test_world_publish_dev_bumps_without_prompt_and_prints_note(monkeypatch, tmp_path):
    """Dev publish should skip confirmation, write a dated dev version, and print the SDK note."""
    pkg_path = tmp_path / "world"
    pkg_path.mkdir()
    pyproject = pkg_path / "pyproject.toml"
    pyproject.write_text(
        """[project]
name = "plato-world-example"
version = "0.2.3"
description = "Example world"
"""
    )

    class _FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 3, 11, 14, 5, 6, tzinfo=tz)

    monkeypatch.setattr("plato.cli.utils.datetime", _FrozenDatetime)

    expected_version = "0.2.4.dev20260311140506"
    dist_dir = pkg_path / "dist"
    dist_dir.mkdir()
    (dist_dir / f"plato_world_example-{expected_version}-py3-none-any.whl").write_text("wheel")

    monkeypatch.setattr(world_cli, "require_api_key", lambda: "test-key")
    monkeypatch.setattr(world_cli.subprocess, "run", lambda *args, **kwargs: _Result())
    monkeypatch.setattr(
        world_cli,
        "_extract_schema_from_wheel",
        lambda wheel_path, module_name: {"properties": {}, "agents": [], "secrets": []},
    )

    result = runner.invoke(world_app, [str(pkg_path), "--dev"])

    assert result.exit_code == 0
    assert "Bump version" not in result.output
    assert f"Updated version: {expected_version}" in result.output
    assert "sdk changes will have to be published if there were any changes" in result.output
    assert f'version = "{expected_version}"' in pyproject.read_text()


def test_world_publish_dev_refreshes_existing_dev_timestamp(monkeypatch, tmp_path):
    """Dev publish should keep the same numeric base version and refresh the dev timestamp."""
    pkg_path = tmp_path / "world"
    pkg_path.mkdir()
    pyproject = pkg_path / "pyproject.toml"
    pyproject.write_text(
        """[project]
name = "plato-world-example"
version = "0.2.4.dev20260310112233"
description = "Example world"
"""
    )

    class _FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 3, 11, 14, 5, 6, tzinfo=tz)

    monkeypatch.setattr("plato.cli.utils.datetime", _FrozenDatetime)

    dist_dir = pkg_path / "dist"
    dist_dir.mkdir()
    (dist_dir / "plato_world_example-0.2.4.dev20260311140506-py3-none-any.whl").write_text("wheel")

    monkeypatch.setattr(world_cli, "require_api_key", lambda: "test-key")
    monkeypatch.setattr(world_cli.subprocess, "run", lambda *args, **kwargs: _Result())
    monkeypatch.setattr(
        world_cli,
        "_extract_schema_from_wheel",
        lambda wheel_path, module_name: {"properties": {}, "agents": [], "secrets": []},
    )

    result = runner.invoke(world_app, [str(pkg_path), "--dev"])

    assert result.exit_code == 0
    assert "Bump version" not in result.output
    assert "Updated version: 0.2.4.dev20260311140506" in result.output
    assert "sdk changes will have to be published if there were any changes" in result.output
    assert 'version = "0.2.4.dev20260311140506"' in pyproject.read_text()
