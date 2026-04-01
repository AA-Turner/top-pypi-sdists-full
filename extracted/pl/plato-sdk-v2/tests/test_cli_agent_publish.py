"""Light tests for `plato agent publish` --skip-docker and --no-cache flags."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit as ClickExit

from plato.cli.agent import _push_single_agent


@pytest.fixture()
def agent_dir(tmp_path: Path) -> Path:
    """Create a minimal agent directory with pyproject.toml, Dockerfile, and dist/."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "test-agent"\nversion = "0.1.0"\ndescription = "test"\n')
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text("FROM python:3.12\n")
    # Create dist/ with a fake wheel so the publish step finds it
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "test_agent-0.1.0-py3-none-any.whl").touch()
    return tmp_path


_COMMON_PATCHES = [
    patch("plato.cli.agent.subprocess.run", return_value=MagicMock(returncode=0, stdout="", stderr="")),
    patch("plato.cli.agent.maybe_bump_package_version", return_value="0.1.0"),
]


def _apply_patches(extra_patches: list | None = None):
    """Return stacked context managers for common + extra patches."""
    patches = list(_COMMON_PATCHES)
    if extra_patches:
        patches.extend(extra_patches)
    return patches


@patch("plato.cli.agent.wait_for_pypi_version")
@patch("plato.cli.agent._publish_agent_image")
def test_no_cache_passed_to_publish_agent_image(
    mock_publish_image: MagicMock,
    mock_wait_pypi: MagicMock,
    agent_dir: Path,
) -> None:
    """--no-cache should forward no_cache=True to _publish_agent_image."""
    with (
        patch("plato.cli.agent.subprocess.run", return_value=MagicMock(returncode=0, stdout="", stderr="")),
        patch("plato.cli.agent.maybe_bump_package_version", return_value="0.1.0"),
    ):
        _push_single_agent(agent_dir, dry_run=True, no_cache=True)

    mock_publish_image.assert_called_once()
    assert mock_publish_image.call_args.kwargs.get("no_cache") is True


@patch("plato.cli.agent.wait_for_pypi_version")
@patch("plato.cli.agent._publish_agent_image")
def test_no_cache_default_is_false(
    mock_publish_image: MagicMock,
    mock_wait_pypi: MagicMock,
    agent_dir: Path,
) -> None:
    """By default no_cache should be False."""
    with (
        patch("plato.cli.agent.subprocess.run", return_value=MagicMock(returncode=0, stdout="", stderr="")),
        patch("plato.cli.agent.maybe_bump_package_version", return_value="0.1.0"),
    ):
        _push_single_agent(agent_dir, dry_run=True)

    mock_publish_image.assert_called_once()
    assert mock_publish_image.call_args.kwargs.get("no_cache") is False


@patch("plato.cli.agent.retag_image", return_value=True)
@patch("plato.cli.agent._publish_agent_image")
def test_skip_docker_retags_instead_of_building(
    mock_publish_image: MagicMock,
    mock_retag: MagicMock,
    agent_dir: Path,
) -> None:
    """--skip-docker should retag the existing image, not build a new one."""
    with (
        patch("plato.cli.agent.subprocess.run", return_value=MagicMock(returncode=0, stdout="", stderr="")),
        patch("plato.cli.agent.maybe_bump_package_version", return_value="0.1.0"),
    ):
        _push_single_agent(agent_dir, dry_run=True, skip_docker=True)

    mock_retag.assert_called_once()
    mock_publish_image.assert_not_called()


@patch("plato.cli.agent.retag_image", return_value=False)
@patch("plato.cli.agent._publish_agent_image")
def test_skip_docker_exits_on_retag_failure(
    mock_publish_image: MagicMock,
    mock_retag: MagicMock,
    agent_dir: Path,
) -> None:
    """--skip-docker should exit with error if retag fails."""
    with (
        patch("plato.cli.agent.subprocess.run", return_value=MagicMock(returncode=0, stdout="", stderr="")),
        patch("plato.cli.agent.maybe_bump_package_version", return_value="0.1.0"),
    ):
        with pytest.raises((SystemExit, ClickExit)):
            _push_single_agent(agent_dir, dry_run=True, skip_docker=True)

    mock_publish_image.assert_not_called()
