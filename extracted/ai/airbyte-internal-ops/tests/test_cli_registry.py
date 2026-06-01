# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the CLI registry commands."""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from airbyte_ops_mcp.registry import (
    ConnectorMetadata,
    ConnectorPublishResult,
    is_valid_for_progressive_rollout,
    strip_rc_suffix,
)
from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_credentials_token
from airbyte_ops_mcp.registry.compile import (
    _apply_overrides_to_latest_entry,
    _apply_release_candidates_to_entries,
    _build_composite_registry_json,
    _cleanup_disabled_registry_entries,
)
from airbyte_ops_mcp.registry.generate import (
    _apply_overrides_from_registry,
    is_registry_enabled,
)
from airbyte_ops_mcp.registry.metrics import (
    apply_metrics_to_registry_entries,
    find_latest_connector_metrics_blob,
    parse_connector_metrics_jsonl,
    read_latest_connector_metrics,
)
from airbyte_ops_mcp.registry.store import RegistryStore


@pytest.mark.unit
@pytest.mark.parametrize(
    "version,expected",
    [
        pytest.param("1.2.3-rc.1", True, id="rc_version"),
        pytest.param("1.2.3-rc.10", True, id="rc_version_double_digit"),
        pytest.param("0.0.1-rc.1", True, id="rc_version_zero"),
        pytest.param("1.2.3", True, id="stable_ga_version"),
        pytest.param("1.2.3-preview.abc123", False, id="preview_version_rejected"),
        pytest.param("1.2.3-alpha.1", True, id="alpha_version"),
        pytest.param("1.2.3-beta.1", True, id="beta_version"),
    ],
)
def test_is_valid_for_progressive_rollout(version: str, expected: bool) -> None:
    """Test version validation for progressive rollout."""
    assert is_valid_for_progressive_rollout(version) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "version,expected",
    [
        pytest.param("1.2.3-rc.1", "1.2.3", id="rc_version"),
        pytest.param("1.2.3-rc.10", "1.2.3", id="rc_version_double_digit"),
        pytest.param("0.0.1-rc.1", "0.0.1", id="rc_version_zero"),
        pytest.param("1.2.3", "1.2.3", id="stable_version_unchanged"),
    ],
)
def test_strip_rc_suffix(version: str, expected: str) -> None:
    """Test stripping release candidate suffix from version."""
    assert strip_rc_suffix(version) == expected


@pytest.mark.unit
def test_connector_metadata_model() -> None:
    """Test ConnectorMetadata Pydantic model."""
    metadata = ConnectorMetadata(
        name="source-github",
        docker_repository="airbyte/source-github",
        docker_image_tag="1.2.3-rc.1",
        support_level="certified",
        definition_id="abc123",
    )
    assert metadata.name == "source-github"
    assert metadata.docker_repository == "airbyte/source-github"
    assert metadata.docker_image_tag == "1.2.3-rc.1"
    assert metadata.support_level == "certified"
    assert metadata.definition_id == "abc123"


@pytest.mark.unit
def test_connector_publish_result_model() -> None:
    """Test ConnectorPublishResult Pydantic model."""
    result = ConnectorPublishResult(
        connector="source-github",
        version="1.2.3",
        action="progressive-rollout-cleanup",
        status="success",
        docker_image="airbyte/source-github:1.2.3",
        registry_updated=True,
        message="Cleaned up release candidate",
    )
    assert result.connector == "source-github"
    assert result.version == "1.2.3"
    assert result.action == "progressive-rollout-cleanup"
    assert result.status == "success"
    assert result.docker_image == "airbyte/source-github:1.2.3"
    assert result.registry_updated is True
    assert result.message == "Cleaned up release candidate"


def run_cli(
    *args: str, cwd: str | Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Run the airbyte-ops CLI with the given arguments."""
    cmd = [sys.executable, "-m", "airbyte_ops_mcp.cli.app", *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent / "src")},
    )


@pytest.mark.unit
def test_cli_help() -> None:
    """Test CLI help output."""
    result = run_cli("--help")
    assert result.returncode == 0
    assert "airbyte-ops" in result.stdout.lower()
    assert "registry" in result.stdout


@pytest.mark.unit
def test_registry_connector_version_next_help() -> None:
    """Test connector-version next help output."""
    result = run_cli("registry", "connector-version", "next", "--help")
    assert result.returncode == 0
    assert "name" in result.stdout
    assert "sha" in result.stdout
    assert "base-version" in result.stdout


@pytest.mark.unit
def test_registry_connector_version_next_missing_name() -> None:
    """Test connector-version next fails without name."""
    result = run_cli(
        "registry",
        "connector-version",
        "next",
        "--sha",
        "abcdef1",
    )
    assert result.returncode != 0


@pytest.mark.unit
def test_registry_help() -> None:
    """Test registry subcommand help output."""
    result = run_cli("registry", "--help")
    assert result.returncode == 0
    # Check for command groups
    assert "progressive-rollout" in result.stdout
    assert "connector" in result.stdout
    assert "connector-version" in result.stdout
    assert "mirror" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_help() -> None:
    """Test registry progressive-rollout sub-app help output."""
    result = run_cli("registry", "progressive-rollout", "--help")
    assert result.returncode == 0
    assert "create" in result.stdout
    assert "cleanup" in result.stdout
    assert "status" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_cleanup_help() -> None:
    """Test registry progressive-rollout cleanup help output."""
    result = run_cli("registry", "progressive-rollout", "cleanup", "--help")
    assert result.returncode == 0
    assert "name" in result.stdout.lower()
    assert "dry-run" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_create_help() -> None:
    """Test registry progressive-rollout create help output."""
    result = run_cli("registry", "progressive-rollout", "create", "--help")
    assert result.returncode == 0
    assert "name" in result.stdout.lower()
    assert "dry-run" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_status_help() -> None:
    """Test registry progressive-rollout status help output."""
    result = run_cli("registry", "progressive-rollout", "status", "--help")
    assert result.returncode == 0
    assert "name" in result.stdout.lower()
    assert "repo-path" in result.stdout
    assert "active-only" in result.stdout
    assert "with-terminal" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_cleanup_missing_required_options() -> None:
    """Test that missing required options causes an error."""
    result = run_cli("registry", "progressive-rollout", "cleanup")
    assert result.returncode != 0


@pytest.mark.unit
def test_registry_progressive_rollout_create_missing_required_options() -> None:
    """Test that missing required options causes an error."""
    result = run_cli("registry", "progressive-rollout", "create")
    assert result.returncode != 0


@pytest.mark.unit
def test_registry_progressive_rollout_cleanup_dry_run(tmp_path: Path) -> None:
    """Test progressive-rollout cleanup with dry-run."""
    connector_dir = tmp_path / "airbyte-integrations" / "connectors" / "source-test"
    connector_dir.mkdir(parents=True)
    (connector_dir / "metadata.yaml").write_text(
        "data:\n  dockerRepository: airbyte/source-test\n  dockerImageTag: 1.0.0-rc.1\n"
    )
    result = run_cli(
        "registry",
        "progressive-rollout",
        "cleanup",
        "--store",
        "coral:dev",
        "--name",
        "source-test",
        "--repo-path",
        str(tmp_path),
        "--dry-run",
        cwd=tmp_path,
    )
    assert result.returncode == 0
    assert "dry-run" in result.stdout
    assert "source-test" in result.stdout
    assert "1.0.0" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_create_dry_run(tmp_path: Path) -> None:
    """Test progressive-rollout create with dry-run."""
    connector_dir = tmp_path / "airbyte-integrations" / "connectors" / "source-test"
    connector_dir.mkdir(parents=True)
    (connector_dir / "metadata.yaml").write_text(
        "data:\n  dockerRepository: airbyte/source-test\n  dockerImageTag: 1.0.0-rc.1\n"
    )
    result = run_cli(
        "registry",
        "progressive-rollout",
        "create",
        "--store",
        "coral:dev",
        "--name",
        "source-test",
        "--repo-path",
        str(tmp_path),
        "--dry-run",
        cwd=tmp_path,
    )
    assert result.returncode == 0
    assert "dry-run" in result.stdout
    assert "source-test" in result.stdout
    assert "1.0.0" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_cleanup_non_rc_version(
    tmp_path: Path,
) -> None:
    """Test progressive-rollout cleanup works even for non-RC on-disk version.

    In the promote workflow the on-disk metadata.yaml is bumped to GA
    before cleanup runs, so cleanup must NOT gate on the version format.
    """
    connector_dir = tmp_path / "airbyte-integrations" / "connectors" / "source-test"
    connector_dir.mkdir(parents=True)
    (connector_dir / "metadata.yaml").write_text(
        "data:\n  dockerRepository: airbyte/source-test\n  dockerImageTag: 1.0.0\n"
    )
    result = run_cli(
        "registry",
        "progressive-rollout",
        "cleanup",
        "--store",
        "coral:dev",
        "--name",
        "source-test",
        "--repo-path",
        str(tmp_path),
        "--dry-run",
        cwd=tmp_path,
    )
    # Should succeed even though on-disk version is GA — cleanup does not
    # gate on version format because the promote workflow bumps
    # the version before calling cleanup.
    assert result.returncode == 0
    assert "dry-run" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_create_ga_version(
    tmp_path: Path,
) -> None:
    """Test progressive-rollout create succeeds for GA version.

    GA versions are now valid for progressive rollout — no `-rc` suffix
    or `enableProgressiveRollout` metadata flag is required at this layer.
    """
    connector_dir = tmp_path / "airbyte-integrations" / "connectors" / "source-test"
    connector_dir.mkdir(parents=True)
    (connector_dir / "metadata.yaml").write_text(
        "data:\n  dockerRepository: airbyte/source-test\n  dockerImageTag: 1.0.0\n"
    )
    result = run_cli(
        "registry",
        "progressive-rollout",
        "create",
        "--store",
        "coral:dev",
        "--name",
        "source-test",
        "--repo-path",
        str(tmp_path),
        "--dry-run",
        cwd=tmp_path,
    )
    assert result.returncode == 0
    assert "dry-run" in result.stdout
    assert "source-test" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_create_preview_version_rejected(
    tmp_path: Path,
) -> None:
    """Test progressive-rollout create rejects preview versions."""
    connector_dir = tmp_path / "airbyte-integrations" / "connectors" / "source-test"
    connector_dir.mkdir(parents=True)
    (connector_dir / "metadata.yaml").write_text(
        "data:\n  dockerRepository: airbyte/source-test\n  dockerImageTag: 1.0.0-preview.abc123\n"
    )
    result = run_cli(
        "registry",
        "progressive-rollout",
        "create",
        "--store",
        "coral:dev",
        "--name",
        "source-test",
        "--repo-path",
        str(tmp_path),
        cwd=tmp_path,
    )
    assert result.returncode == 1
    assert "failure" in result.stdout
    assert "not valid for progressive rollout" in result.stdout


@pytest.mark.unit
def test_registry_progressive_rollout_cleanup_connector_not_found(
    tmp_path: Path,
) -> None:
    """Test error when connector directory doesn't exist."""
    connectors_dir = tmp_path / "airbyte-integrations" / "connectors"
    connectors_dir.mkdir(parents=True)
    result = run_cli(
        "registry",
        "progressive-rollout",
        "cleanup",
        "--store",
        "coral:dev",
        "--name",
        "source-nonexistent",
        "--repo-path",
        str(tmp_path),
        cwd=tmp_path,
    )
    assert result.returncode != 0
    assert "not found" in result.stdout.lower() or "not found" in result.stderr.lower()


@pytest.mark.unit
def test_dockerhub_help() -> None:
    """Test dockerhub subcommand help output."""
    result = run_cli("dockerhub", "--help")
    assert result.returncode == 0
    assert "inspect-image" in result.stdout


@pytest.mark.unit
def test_dockerhub_inspect_image_help() -> None:
    """Test dockerhub inspect-image help output."""
    result = run_cli("dockerhub", "inspect-image", "--help")
    assert result.returncode == 0
    assert "image" in result.stdout.lower()
    assert "tag" in result.stdout.lower()


@pytest.mark.unit
def test_registry_artifacts_generate_help() -> None:
    """Test registry connector-version artifacts generate help output."""
    result = run_cli("registry", "connector-version", "artifacts", "generate", "--help")
    assert result.returncode == 0
    assert "generate" in result.stdout.lower()


@pytest.mark.unit
def test_registry_artifacts_publish_help() -> None:
    """Test registry connector-version artifacts publish help output."""
    result = run_cli("registry", "connector-version", "artifacts", "publish", "--help")
    assert result.returncode == 0
    assert "publish" in result.stdout.lower()


@pytest.mark.unit
def test_registry_connector_version_yank_help() -> None:
    """Test registry connector-version yank help output."""
    result = run_cli("registry", "connector-version", "yank", "--help")
    assert result.returncode == 0
    assert "yank" in result.stdout.lower()


@pytest.mark.unit
def test_yank_connector_version_response_model() -> None:
    """Test YankConnectorVersionResponse Pydantic model."""
    from airbyte_ops_mcp.mcp.registry import YankConnectorVersionResponse

    response = YankConnectorVersionResponse(
        message="Yank workflow triggered for source-faker@1.2.3 on coral:dev.",
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/registry-yank.yml",
        github_run_id=12345,
        github_run_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/runs/12345",
    )
    assert response.message.startswith("Yank workflow triggered")
    assert response.github_run_id == 12345
    assert response.workflow_url is not None
    assert response.github_run_url is not None

    # Test with only required fields
    minimal = YankConnectorVersionResponse(message="Token not found.")
    assert minimal.workflow_url is None
    assert minimal.github_run_id is None
    assert minimal.github_run_url is None


@pytest.mark.unit
def test_registry_connector_version_unyank_help() -> None:
    """Test registry connector-version unyank help output."""
    result = run_cli("registry", "connector-version", "unyank", "--help")
    assert result.returncode == 0
    assert "unyank" in result.stdout.lower()


@pytest.mark.unit
def test_registry_store_mirror_help() -> None:
    """Test registry store mirror help output."""
    result = run_cli("registry", "store", "mirror", "--help")
    assert result.returncode == 0
    assert "mirror" in result.stdout.lower()


@pytest.mark.unit
def test_registry_store_compile_help() -> None:
    """Test registry store compile help output."""
    result = run_cli("registry", "store", "compile", "--help")
    assert result.returncode == 0
    assert "compile" in result.stdout.lower()


@pytest.mark.unit
def test_registry_store_delete_dev_latest_help() -> None:
    """Test registry store delete-dev-latest help output."""
    result = run_cli("registry", "store", "delete-dev-latest", "--help")
    assert result.returncode == 0
    assert "delete" in result.stdout.lower() or "latest" in result.stdout.lower()


@pytest.mark.unit
def test_registry_connector_list_help() -> None:
    """Test registry connector list help output."""
    result = run_cli("registry", "connector", "list", "--help")
    assert result.returncode == 0
    assert "list" in result.stdout.lower()


@pytest.mark.unit
def test_registry_connector_version_list_help() -> None:
    """Test registry connector-version list help output."""
    result = run_cli("registry", "connector-version", "list", "--help")
    assert result.returncode == 0
    assert "list" in result.stdout.lower()


@pytest.mark.unit
def test_registry_connector_version_metadata_get_help() -> None:
    """Test registry connector-version metadata get help output."""
    result = run_cli("registry", "connector-version", "metadata", "get", "--help")
    assert result.returncode == 0
    assert "metadata" in result.stdout.lower() or "get" in result.stdout.lower()


@pytest.mark.unit
def test_version_flag() -> None:
    """Test that 'airbyte-ops --version' prints a version string."""
    result = run_cli("--version")
    assert result.returncode == 0
    assert result.stdout.strip(), "--version flag should produce output"


@pytest.mark.unit
def test_version_flag_not_intercepted_by_publish() -> None:
    """Regression test: --version as a subcommand param must not be hijacked.

    Previously, cyclopts' default --version meta-command on every App instance
    intercepted --version tokens meant for subcommands like 'artifacts publish
    --version 1.2.3', printing the cyclopts version and exiting 0 without
    running the actual command.
    """
    result = run_cli(
        "registry",
        "connector-version",
        "artifacts",
        "publish",
        "--name",
        "source-test",
        "--version",
        "1.2.3",
        "--artifacts-dir",
        "/nonexistent",
        "--store",
        "coral:dev",
    )
    # The command should NOT silently succeed with just a version number.
    # It should either fail (missing artifacts dir) or produce publish output.
    # The key assertion: stdout must NOT be just a bare version number.
    output = result.stdout.strip()
    assert not output.replace(".", "").isdigit(), (
        f"--version was intercepted by cyclopts meta-command: got '{output}'"
    )


@pytest.mark.unit
def test_version_flag_not_intercepted_by_yank() -> None:
    """Regression test: --version on yank must not be hijacked by cyclopts."""
    result = run_cli(
        "registry",
        "connector-version",
        "yank",
        "--name",
        "source-test",
        "--version",
        "1.2.3",
    )
    output = result.stdout.strip()
    assert not output.replace(".", "").isdigit(), (
        f"--version was intercepted by cyclopts meta-command: got '{output}'"
    )


# =============================================================================
# Compile: RC injection into global registry entries
# =============================================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    "entries,rc_entries,expected_rc_key",
    [
        pytest.param(
            [
                {
                    "dockerRepository": "airbyte/source-github",
                    "dockerImageTag": "1.0.0",
                    "releases": {"breakingChanges": {}},
                },
            ],
            {
                "airbyte/source-github": {
                    "version": "1.1.0-rc.1",
                    "entry": {
                        "dockerRepository": "airbyte/source-github",
                        "dockerImageTag": "1.1.0-rc.1",
                    },
                },
            },
            "1.1.0-rc.1",
            id="single_rc_injected",
        ),
        pytest.param(
            [
                {
                    "dockerRepository": "airbyte/source-github",
                    "dockerImageTag": "1.0.0",
                },
            ],
            {},
            None,
            id="no_rcs_no_change",
        ),
        pytest.param(
            [
                {
                    "dockerRepository": "airbyte/source-github",
                    "dockerImageTag": "1.0.0",
                },
            ],
            {
                "airbyte/source-postgres": {
                    "version": "2.0.0-rc.1",
                    "entry": {
                        "dockerRepository": "airbyte/source-postgres",
                        "dockerImageTag": "2.0.0-rc.1",
                    },
                },
            },
            None,
            id="rc_for_different_connector",
        ),
    ],
)
def test_apply_release_candidates_to_entries(
    entries: list[dict],
    rc_entries: dict,
    expected_rc_key: str | None,
) -> None:
    """Test _apply_release_candidates_to_entries injects RC info correctly."""
    result = _apply_release_candidates_to_entries(entries, rc_entries)
    assert len(result) == len(entries)
    entry = result[0]
    if expected_rc_key:
        assert "releases" in entry
        assert "releaseCandidates" in entry["releases"]
        assert expected_rc_key in entry["releases"]["releaseCandidates"]
    else:
        rc_section = entry.get("releases", {}).get("releaseCandidates")
        assert rc_section is None or len(rc_section) == 0


@pytest.mark.unit
@pytest.mark.parametrize(
    "metadata_data,expected",
    [
        pytest.param({}, True, id="missing_overrides"),
        pytest.param({"registryOverrides": {}}, True, id="empty_overrides"),
        pytest.param({"registryOverrides": {"cloud": {}}}, True, id="missing_enabled"),
        pytest.param(
            {"registryOverrides": {"cloud": {"enabled": True}}},
            True,
            id="explicit_enabled",
        ),
        pytest.param(
            {"registryOverrides": {"cloud": {"enabled": False}}},
            False,
            id="explicit_disabled",
        ),
        pytest.param(
            {"registryOverrides": {"cloud": None}},
            True,
            id="non_dict_registry_block",
        ),
    ],
)
def test_is_registry_enabled_default(metadata_data: dict, expected: bool) -> None:
    """Registry enablement defaults to enabled unless explicitly disabled."""
    assert is_registry_enabled(metadata_data, "cloud") is expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "metadata_data",
    [
        pytest.param(
            {"dockerRepository": "airbyte/source-test"}, id="missing_overrides"
        ),
        pytest.param(
            {
                "dockerRepository": "airbyte/source-test",
                "registryOverrides": None,
            },
            id="non_dict_overrides",
        ),
        pytest.param(
            {
                "dockerRepository": "airbyte/source-test",
                "registryOverrides": {"cloud": None},
            },
            id="non_dict_registry_block",
        ),
    ],
)
def test_apply_overrides_from_registry_defaults_to_empty(
    metadata_data: dict,
) -> None:
    """Registry override application defaults malformed blocks to empty."""
    assert _apply_overrides_from_registry(metadata_data, "cloud") == metadata_data


class InMemoryRegistryFileSystem:
    """Minimal filesystem for registry compile unit tests."""

    def __init__(self, files: dict[str, str]) -> None:
        self.files = files
        self.deleted: list[str] = []

    def exists(self, path: str) -> bool:
        return path in self.files

    def open(self, path: str, mode: str = "r") -> io.StringIO:
        if "w" in mode:
            handle = io.StringIO()

            def close() -> None:
                self.files[path] = handle.getvalue()

            handle.close = close
            return handle
        if "r" not in mode:
            msg = f"Unsupported mode: {mode}"
            raise ValueError(msg)
        if path not in self.files:
            raise FileNotFoundError(path)
        return io.StringIO(self.files[path])

    def rm(self, path: str) -> None:
        self.deleted.append(path)
        self.files.pop(path, None)


class InMemoryGlobFileSystem:
    """Minimal glob-capable filesystem for registry metrics tests."""

    def __init__(self, files: dict[str, str]) -> None:
        self.files = files

    def glob(self, pattern: str) -> list[str]:
        prefix, suffix = pattern.split("*", maxsplit=1)
        return [
            path
            for path in self.files
            if path.startswith(prefix) and path.endswith(suffix)
        ]

    def open(self, path: str, mode: str = "r"):
        if "r" not in mode:
            msg = f"Unsupported mode: {mode}"
            raise ValueError(msg)
        if path not in self.files:
            raise FileNotFoundError(path)
        return io.StringIO(self.files[path])


@pytest.mark.unit
def test_parse_connector_metrics_jsonl() -> None:
    """Connector metrics JSONL is grouped by definition ID and platform."""
    jsonl_content = "\n".join(
        [
            json.dumps(
                {
                    "_airbyte_data": {
                        "connector_definition_id": "source-def",
                        "airbyte_platform": "cloud",
                        "sync_success_rate": "high",
                        "usage": "medium",
                    }
                }
            ),
            json.dumps(
                {
                    "_airbyte_data": {
                        "connector_definition_id": "source-def",
                        "airbyte_platform": "oss",
                        "sync_success_rate": "null",
                        "usage": "low",
                    }
                }
            ),
            json.dumps(
                {
                    "_airbyte_data": {
                        "connector_definition_id": "destination-def",
                        "airbyte_platform": "all",
                        "sync_success_rate": "medium",
                        "usage": "null",
                    }
                }
            ),
        ]
    )

    result = parse_connector_metrics_jsonl(jsonl_content, blob_path="metrics.jsonl")

    assert result.blob_path == "metrics.jsonl"
    assert result.connector_count == 2
    assert result.registry_metrics_for_definition_id("source-def") == {
        "cloud": {"sync_success_rate": "high", "usage": "medium"},
        "oss": {"sync_success_rate": None, "usage": "low"},
    }
    assert result.registry_metrics_for_definition_id("destination-def") == {
        "all": {"sync_success_rate": "medium", "usage": None},
    }
    assert result.registry_metrics_for_definition_id("missing-def") == {}


@pytest.mark.unit
def test_find_latest_connector_metrics_blob() -> None:
    """Latest connector metrics blob is selected by object name."""
    fs = InMemoryGlobFileSystem(
        {
            "ab-analytics-connector-metrics/data/connector_quality_metrics/2026_05_07_0.jsonl": "",
            "ab-analytics-connector-metrics/data/connector_quality_metrics/2026_05_08_0.jsonl": "",
            "ab-analytics-connector-metrics/data/connector_quality_metrics/readme.txt": "",
        }
    )

    assert find_latest_connector_metrics_blob(fs) == (
        "ab-analytics-connector-metrics/data/connector_quality_metrics/2026_05_08_0.jsonl"
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "files,expected_blob_path,expected_metrics",
    [
        pytest.param(
            {},
            None,
            {},
            id="no_matches",
        ),
        pytest.param(
            {
                "ab-analytics-connector-metrics/data/connector_quality_metrics/2026_05_07_0.jsonl": "",
                "ab-analytics-connector-metrics/data/connector_quality_metrics/2026_05_08_0.jsonl": json.dumps(
                    {
                        "_airbyte_data": {
                            "connector_definition_id": "source-def",
                            "airbyte_platform": "cloud",
                            "sync_success_rate": "high",
                            "usage": "medium",
                        }
                    }
                ),
            },
            "ab-analytics-connector-metrics/data/connector_quality_metrics/2026_05_08_0.jsonl",
            {"cloud": {"sync_success_rate": "high", "usage": "medium"}},
            id="reads_latest_match",
        ),
    ],
)
def test_read_latest_connector_metrics(
    files: dict[str, str],
    expected_blob_path: str | None,
    expected_metrics: dict[str, dict[str, str | None]],
) -> None:
    """Latest connector metrics are read when a matching export exists."""
    result = read_latest_connector_metrics(fs=InMemoryGlobFileSystem(files))

    assert result.blob_path == expected_blob_path
    assert result.registry_metrics_for_definition_id("source-def") == expected_metrics


@pytest.mark.unit
def test_get_gcs_credentials_token_prefers_gcs_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """GCS credentials use explicit registry credentials before Devin defaults."""
    monkeypatch.setenv(
        "GCS_CREDENTIALS", json.dumps({"client_email": "gcs@example.com"})
    )
    monkeypatch.setenv(
        "GCP_GSM_CREDENTIALS",
        json.dumps({"client_email": "gcp-gsm@example.com"}),
    )

    assert get_gcs_credentials_token() == {"client_email": "gcs@example.com"}


@pytest.mark.unit
def test_get_gcs_credentials_token_uses_gcp_gsm_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Devin registry testing credentials are accepted when `GCS_CREDENTIALS` is unset."""
    monkeypatch.delenv("GCS_CREDENTIALS", raising=False)
    monkeypatch.setenv(
        "GCP_GSM_CREDENTIALS",
        json.dumps({"client_email": "gcp-gsm@example.com"}),
    )

    assert get_gcs_credentials_token() == {"client_email": "gcp-gsm@example.com"}


@pytest.mark.unit
def test_apply_metrics_to_registry_entries() -> None:
    """Registry metrics injection updates generated.metrics only for matches."""
    metrics_bundle = parse_connector_metrics_jsonl(
        json.dumps(
            {
                "_airbyte_data": {
                    "connector_definition_id": "source-def",
                    "airbyte_platform": "cloud",
                    "sync_success_rate": "high",
                    "usage": "medium",
                }
            }
        )
    )
    entries = [
        {
            "sourceDefinitionId": "source-def",
            "dockerRepository": "airbyte/source-test",
            "generated": {"source_file_info": {"metadata_file_path": "metadata.yaml"}},
        },
        {
            "destinationDefinitionId": "destination-def",
            "dockerRepository": "airbyte/destination-test",
        },
    ]

    injected_count = apply_metrics_to_registry_entries(entries, metrics_bundle)

    assert injected_count == 1
    assert entries[0]["generated"] == {
        "source_file_info": {"metadata_file_path": "metadata.yaml"},
        "metrics": {"cloud": {"sync_success_rate": "high", "usage": "medium"}},
    }
    assert "generated" not in entries[1]


@pytest.mark.unit
def test_cleanup_disabled_registry_entries_preserves_missing_overrides() -> None:
    """Legacy cleanup keeps connectors without registry overrides enabled."""
    store = RegistryStore.parse("coral:dev")
    base = f"{store.bucket_root}/metadata/airbyte"
    files = {
        f"{base}/source-missing/latest/metadata.yaml": "data:\n  name: Source Missing\n",
        f"{base}/source-missing/1.0.0/cloud.json": "{}",
        f"{base}/source-missing/1.0.0/oss.json": "{}",
        f"{base}/source-missing/latest/cloud.json": "{}",
        f"{base}/source-missing/latest/oss.json": "{}",
        f"{base}/source-disabled/latest/metadata.yaml": (
            "data:\n"
            "  registryOverrides:\n"
            "    cloud:\n"
            "      enabled: false\n"
            "    oss:\n"
            "      enabled: false\n"
        ),
        f"{base}/source-disabled/1.0.0/cloud.json": "{}",
        f"{base}/source-disabled/1.0.0/oss.json": "{}",
        f"{base}/source-disabled/latest/cloud.json": "{}",
        f"{base}/source-disabled/latest/oss.json": "{}",
    }
    fs = InMemoryRegistryFileSystem(files)

    deleted = _cleanup_disabled_registry_entries(
        fs,
        store=store,
        connector_versions={
            "source-missing": ["1.0.0"],
            "source-disabled": ["1.0.0"],
        },
    )

    assert "source-missing" not in deleted
    assert set(deleted["source-disabled"]) == {
        f"{base}/source-disabled/1.0.0/cloud.json",
        f"{base}/source-disabled/1.0.0/oss.json",
        f"{base}/source-disabled/latest/cloud.json",
        f"{base}/source-disabled/latest/oss.json",
    }


@pytest.mark.unit
def test_apply_overrides_to_latest_entry_handles_malformed_override_blocks() -> None:
    """Latest sync treats malformed registry overrides as empty."""
    store = RegistryStore.parse("coral:dev")
    base = f"{store.bucket_root}/metadata/airbyte/source-nondict"
    files = {
        f"{base}/latest/metadata.yaml": (
            "data:\n"
            "  dockerRepository: airbyte/source-nondict\n"
            "  registryOverrides:\n"
            "    cloud:\n"
            "    oss:\n"
        ),
        f"{base}/latest/cloud.json": (
            '{"dockerRepository": "airbyte/source-nondict", '
            '"generated": {"source_file_info": {"metadata_file_path": '
            '"metadata/airbyte/source-nondict/1.0.0/metadata.yaml"}}}'
        ),
        f"{base}/latest/oss.json": (
            '{"dockerRepository": "airbyte/source-nondict", '
            '"generated": {"source_file_info": {"metadata_file_path": '
            '"metadata/airbyte/source-nondict/1.0.0/metadata.yaml"}}}'
        ),
    }
    fs = InMemoryRegistryFileSystem(files)

    _apply_overrides_to_latest_entry(
        fs,
        store=store,
        connector="source-nondict",
        version="1.0.0",
    )

    cloud_entry = json.loads(files[f"{base}/latest/cloud.json"])
    oss_entry = json.loads(files[f"{base}/latest/oss.json"])
    latest_metadata_path = "metadata/airbyte/source-nondict/latest/metadata.yaml"
    assert cloud_entry["generated"]["source_file_info"]["metadata_file_path"] == (
        latest_metadata_path
    )
    assert oss_entry["generated"]["source_file_info"]["metadata_file_path"] == (
        latest_metadata_path
    )


# =============================================================================
# Compile: composite_registry.json builder
# =============================================================================


@pytest.mark.unit
def test_build_composite_registry_json_union_and_availability() -> None:
    """Composite registry should union cloud + oss with availability tags."""
    cloud_entries = [
        {
            "name": "GitHub",
            "sourceDefinitionId": "src-github",
            "dockerRepository": "airbyte/source-github",
            "dockerImageTag": "1.0.0",
            "supportLevel": "certified",
        },
        {
            "name": "Snowflake",
            "destinationDefinitionId": "dst-snowflake",
            "dockerRepository": "airbyte/destination-snowflake",
            "dockerImageTag": "2.0.0",
            "supportLevel": "certified",
        },
    ]
    oss_entries = [
        {
            "name": "GitHub",
            "sourceDefinitionId": "src-github",
            "dockerRepository": "airbyte/source-github",
            "dockerImageTag": "0.9.0",  # older; should NOT win (cloud preferred)
            "supportLevel": "certified",
        },
        {
            "name": "Milvus",
            "destinationDefinitionId": "dst-milvus",
            "dockerRepository": "airbyte/destination-milvus",
            "dockerImageTag": "0.1.0",
            "supportLevel": "community",
        },
    ]

    result = _build_composite_registry_json(
        cloud_entries=cloud_entries,
        oss_entries=oss_entries,
    )

    assert set(result.keys()) == {"sources", "destinations"}
    assert len(result["sources"]) == 1
    assert len(result["destinations"]) == 2

    by_def_id: dict[str, dict] = {}
    for entry in result["sources"] + result["destinations"]:
        def_id = entry.get("sourceDefinitionId") or entry.get("destinationDefinitionId")
        by_def_id[def_id] = entry

    # GitHub: in both → availability=["cloud","oss"], cloud entry wins.
    github = by_def_id["src-github"]
    assert github["availability"] == ["cloud", "oss"]
    assert github["dockerImageTag"] == "1.0.0"

    # Snowflake: cloud-only → availability=["cloud"].
    snowflake = by_def_id["dst-snowflake"]
    assert snowflake["availability"] == ["cloud"]

    # Milvus: oss-only → availability=["oss"], oss entry preserved.
    milvus = by_def_id["dst-milvus"]
    assert milvus["availability"] == ["oss"]
    assert milvus["supportLevel"] == "community"


@pytest.mark.unit
def test_build_composite_registry_json_empty() -> None:
    """Composite registry with no input entries returns empty lists."""
    result = _build_composite_registry_json(cloud_entries=[], oss_entries=[])
    assert result == {"sources": [], "destinations": []}


@pytest.mark.unit
def test_build_composite_registry_json_deterministic_order() -> None:
    """Output order must be deterministic, sorted by dockerRepository."""
    cloud_entries = [
        {
            "sourceDefinitionId": "b",
            "dockerRepository": "airbyte/source-b",
            "dockerImageTag": "1.0.0",
        },
        {
            "sourceDefinitionId": "a",
            "dockerRepository": "airbyte/source-a",
            "dockerImageTag": "1.0.0",
        },
    ]
    oss_entries = [
        {
            "sourceDefinitionId": "c",
            "dockerRepository": "airbyte/source-c",
            "dockerImageTag": "1.0.0",
        },
    ]

    result = _build_composite_registry_json(
        cloud_entries=cloud_entries,
        oss_entries=oss_entries,
    )

    docker_repos = [e["dockerRepository"] for e in result["sources"]]
    assert docker_repos == [
        "airbyte/source-a",
        "airbyte/source-b",
        "airbyte/source-c",
    ]


@pytest.mark.unit
def test_build_composite_registry_json_does_not_mutate_inputs() -> None:
    """Composite builder must not mutate the cloud/oss entry dicts."""
    cloud_entry = {
        "sourceDefinitionId": "src-x",
        "dockerRepository": "airbyte/source-x",
        "dockerImageTag": "1.0.0",
    }
    oss_entry = {
        "sourceDefinitionId": "src-y",
        "dockerRepository": "airbyte/source-y",
        "dockerImageTag": "1.0.0",
    }

    _build_composite_registry_json(
        cloud_entries=[cloud_entry],
        oss_entries=[oss_entry],
    )

    assert "availability" not in cloud_entry
    assert "availability" not in oss_entry


@pytest.mark.unit
def test_build_composite_registry_json_carries_unkeyed_entries() -> None:
    """Entries missing definitionId must still appear in the composite output.

    `_compile_global_registry()` preserves entries that lack both
    `sourceDefinitionId` and `destinationDefinitionId`, so the composite
    builder must too — otherwise the "superset" guarantee is silently
    violated.  Dedup falls back to `dockerRepository` for these entries.
    """
    # Same dockerRepository in both registries but no definitionId —
    # should be deduped and get availability=["cloud","oss"], cloud wins.
    cloud_entries = [
        {
            "name": "Legacy-NoId",
            "dockerRepository": "airbyte/source-legacy-no-id",
            "dockerImageTag": "1.0.0",
        },
    ]
    oss_entries = [
        {
            "name": "Legacy-NoId",
            "dockerRepository": "airbyte/source-legacy-no-id",
            "dockerImageTag": "0.9.0",
        },
        # OSS-only entry missing both definitionId and dockerRepository.
        # Must still be carried through (last-resort dedup by object id).
        {
            "name": "Unkeyed",
            "dockerImageTag": "0.1.0",
        },
    ]

    result = _build_composite_registry_json(
        cloud_entries=cloud_entries,
        oss_entries=oss_entries,
    )

    all_entries = result["sources"] + result["destinations"]
    by_name = {e["name"]: e for e in all_entries}

    # Shared dockerRepository: deduped, cloud wins, availability=["cloud","oss"].
    assert "Legacy-NoId" in by_name
    legacy = by_name["Legacy-NoId"]
    assert legacy["availability"] == ["cloud", "oss"]
    assert legacy["dockerImageTag"] == "1.0.0"

    # Entry missing both definitionId and dockerRepository: still present.
    assert "Unkeyed" in by_name
    assert by_name["Unkeyed"]["availability"] == ["oss"]
