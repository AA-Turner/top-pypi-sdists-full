# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for breaking-change precedence over progressive rollout."""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest
import yaml

from airbyte_ops_mcp.registry.breaking_changes import (
    version_declares_breaking_change,
)
from airbyte_ops_mcp.registry.compile import _read_rc_registry_entry
from airbyte_ops_mcp.registry.publish_artifacts import publish_version_artifacts
from airbyte_ops_mcp.registry.store import RegistryStore


class InMemoryRegistryFileSystem:
    """Minimal filesystem for reading registry entries."""

    def __init__(self, files: dict[str, str]) -> None:
        self.files = files

    def exists(self, path: str) -> bool:
        return path in self.files

    def open(self, path: str, mode: str = "r") -> io.StringIO:
        if mode != "r":
            raise ValueError(f"Unsupported mode: {mode}")
        return io.StringIO(self.files[path])


@pytest.mark.unit
@pytest.mark.parametrize(
    "version,breaking_changes,expected",
    [
        pytest.param("2.0.0", {"2.0.0": {}}, True, id="exact_match"),
        pytest.param("2.0.0-rc.1", {"2.0.0": {}}, True, id="rc_matches_base"),
        pytest.param("2.0.0+build.1", {"2.0.0": {}}, True, id="build_matches_base"),
        pytest.param("2.1.0", {"2.0.0": {}}, False, id="later_version_does_not_match"),
        pytest.param("2.0.0", {"v2.0.0": {}}, True, id="version_key_is_parsed"),
    ],
)
def test_version_declares_breaking_change(
    version: str,
    breaking_changes: dict[str, dict],
    expected: bool,
) -> None:
    """Breaking-change matching compares normalized base versions."""
    assert version_declares_breaking_change(version, breaking_changes) is expected


def _write_artifacts(
    tmp_path: Path,
    *,
    version: str,
    breaking_changes: dict[str, dict],
) -> Path:
    artifacts_dir = tmp_path / version
    artifacts_dir.mkdir()
    (artifacts_dir / "metadata.yaml").write_text(
        yaml.safe_dump(
            {
                "data": {
                    "dockerImageTag": version,
                    "releases": {
                        "rolloutConfiguration": {
                            "enableProgressiveRollout": True,
                        },
                        "breakingChanges": breaking_changes,
                    },
                }
            }
        )
    )
    (artifacts_dir / "cloud.json").write_text("{}")
    return artifacts_dir


@pytest.mark.unit
@pytest.mark.parametrize(
    "version,breaking_changes,expected_override,expected_marker_published",
    [
        pytest.param(
            "2.0.0",
            {"2.0.0": {"message": "breaking"}},
            True,
            False,
            id="matching_breaking_version",
        ),
        pytest.param(
            "2.1.0",
            {"2.0.0": {"message": "historical breaking"}},
            False,
            True,
            id="historical_breaking_version",
        ),
    ],
)
def test_breaking_change_rollout_precedence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    version: str,
    breaking_changes: dict[str, dict],
    expected_override: bool,
    expected_marker_published: bool,
) -> None:
    """Breaking-change matching controls whether rollout markers are published."""
    artifacts_dir = _write_artifacts(
        tmp_path,
        version=version,
        breaking_changes=breaking_changes,
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.publish_artifacts.get_registry_entry",
        lambda **_: {"data": {"dockerImageTag": "9.9.9"}},
    )

    result = publish_version_artifacts(
        connector_name="source-test",
        version=version,
        artifacts_dir=artifacts_dir,
        store=RegistryStore.parse("coral:dev"),
        dry_run=True,
        with_validate=False,
    )

    assert result.progressive_rollout_overridden_by_breaking_change is expected_override
    assert result.progressive_rollout_overridden_by_published_ga is False
    assert ("progressive-rollout.yml" in result.files_uploaded) is (
        expected_marker_published
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "published_version,expected_override,expected_marker",
    [
        pytest.param("2.0.0", True, False, id="already-published-default-ga"),
        pytest.param("1.9.0", False, True, id="newer-version"),
        pytest.param(None, False, True, id="unreadable-published-latest"),
    ],
)
def test_published_default_ga_suppresses_rollout_marker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    published_version: str | None,
    expected_override: bool,
    expected_marker: bool,
) -> None:
    """Only a readable matching published version suppresses the rollout marker."""
    artifacts_dir = _write_artifacts(
        tmp_path,
        version="2.0.0",
        breaking_changes={},
    )

    def fake_get_registry_entry(**_: object) -> dict:
        if published_version is None:
            raise FileNotFoundError("latest metadata unavailable")
        return {"data": {"dockerImageTag": published_version}}

    monkeypatch.setattr(
        "airbyte_ops_mcp.registry.publish_artifacts.get_registry_entry",
        fake_get_registry_entry,
    )

    result = publish_version_artifacts(
        connector_name="source-test",
        version="2.0.0",
        artifacts_dir=artifacts_dir,
        store=RegistryStore.parse("coral:dev"),
        dry_run=True,
        with_validate=False,
    )

    assert result.progressive_rollout_overridden_by_published_ga is (expected_override)
    assert ("progressive-rollout.yml" in result.files_uploaded) is expected_marker


@pytest.mark.unit
@pytest.mark.parametrize(
    "version,entry,expected",
    [
        pytest.param(
            "2.0.0-rc.1",
            {
                "dockerImageTag": "2.0.0-rc.1",
                "releases": {"breakingChanges": {"2.0.0": {}}},
            },
            None,
            id="drops_breaking_candidate",
        ),
        pytest.param(
            "2.1.0-rc.1",
            {
                "dockerImageTag": "2.1.0-rc.1",
                "releases": {"breakingChanges": {"2.0.0": {}}},
            },
            {
                "dockerImageTag": "2.1.0-rc.1",
                "releases": {"breakingChanges": {"2.0.0": {}}},
            },
            id="keeps_non_breaking_candidate",
        ),
    ],
)
def test_compile_filters_breaking_change_candidates(
    version: str,
    entry: dict,
    expected: dict | None,
) -> None:
    """Compile suppresses only candidates matching their breaking declaration."""
    store = RegistryStore.parse("coral:dev")
    path = f"{store.bucket_root}/metadata/airbyte/source-test/{version}/cloud.json"
    fs = InMemoryRegistryFileSystem({path: json.dumps(entry)})

    result = _read_rc_registry_entry(
        fs,
        store=store,
        connector="source-test",
        rc_version=version,
        registry_type="cloud",
    )

    assert result == expected
