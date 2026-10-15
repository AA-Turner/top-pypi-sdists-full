# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Which source `regression-test --connector-name` builds."""

from __future__ import annotations

from pathlib import Path

import pytest

from airbyte_ops_mcp.cli import cloud

pytestmark = pytest.mark.unit


@pytest.fixture
def built(monkeypatch) -> list[Path]:
    directories: list[Path] = []
    monkeypatch.setattr(cloud, "verify_docker_installation", lambda: True)
    monkeypatch.setattr(
        cloud.MetadataFile, "from_file", classmethod(lambda cls, path: object())
    )

    def fake_build(*, connector_directory, tag, **_kwargs):
        directories.append(connector_directory)
        return f"airbyte/source-example:{tag}"

    monkeypatch.setattr(cloud, "build_connector_image", fake_build)
    return directories


def _connector(root: Path) -> Path:
    directory = root / "airbyte-integrations" / "connectors" / "source-example"
    directory.mkdir(parents=True)
    (directory / "metadata.yaml").write_text("data: {}\n")
    return directory


def test_a_preferred_repo_root_wins_over_auto_discovery(tmp_path, monkeypatch, built):
    """Auto-discovery can find another checkout on the machine; the caller's root wins."""
    other = _connector(tmp_path / "other-checkout")
    wanted = _connector(tmp_path / "wanted")
    monkeypatch.setattr(cloud, "find_connector_root_from_name", lambda _name: other)

    image = cloud._build_connector_image_from_source(
        "source-example", repo_root=tmp_path / "wanted", prefer_repo_root=True
    )

    assert image == "airbyte/source-example:dev"
    assert built == [wanted]


def test_by_default_auto_discovery_still_wins(tmp_path, monkeypatch, built):
    """Outside reproduction cases the precedence is unchanged."""
    other = _connector(tmp_path / "other-checkout")
    _connector(tmp_path / "wanted")
    monkeypatch.setattr(cloud, "find_connector_root_from_name", lambda _name: other)

    cloud._build_connector_image_from_source(
        "source-example", repo_root=tmp_path / "wanted"
    )

    assert built == [other]


def test_a_repo_root_is_the_fallback_when_nothing_is_discovered(
    tmp_path, monkeypatch, built
):
    wanted = _connector(tmp_path / "wanted")

    def not_found(_name: str) -> Path:
        raise FileNotFoundError(_name)

    monkeypatch.setattr(cloud, "find_connector_root_from_name", not_found)

    cloud._build_connector_image_from_source(
        "source-example", repo_root=tmp_path / "wanted"
    )

    assert built == [wanted]


def test_a_preferred_repo_root_without_the_connector_fails(
    tmp_path, monkeypatch, built
):
    monkeypatch.setattr(
        cloud, "find_connector_root_from_name", lambda _name: tmp_path / "unused"
    )

    assert (
        cloud._build_connector_image_from_source(
            "source-example", repo_root=tmp_path, prefer_repo_root=True
        )
        is None
    )
    assert built == []
