# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Cloud MCP installs release locks without breaking immutable git previews."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/deploy-mcp-command.yml"
CONTEXT = ROOT / "infra/internal-mcp-servers/docker/cloud-mcp"
SHA = "a" * 40
GIT_REQUIREMENT = f"airbyte @ git+https://github.com/airbytehq/PyAirbyte@{SHA}"


@pytest.mark.parametrize("image", ["cloud-mcp", "agent-mcp"])
def test_bootstrap_cloud_build_uses_matching_lock_and_requirement(image: str) -> None:
    config = yaml.safe_load((CONTEXT / "cloudbuild.yaml").read_text())
    version = "1.0.0-rc.44"
    image_uri = f"region-docker.pkg.dev/project/{image}/{image}:latest"

    def render(value: str) -> str:
        return value.replace("${_PYAIRBYTE_VERSION}", version).replace(
            "${_IMAGE}", image_uri
        )

    download, build = config["steps"]
    assert download["name"] == "gcr.io/cloud-builders/curl"
    assert "--fail" in download["args"]
    assert [render(arg) for arg in download["args"]][-3:] == [
        "--output",
        "pylock.toml",
        f"https://github.com/airbytehq/PyAirbyte/releases/download/v{version}/pylock.toml",
    ]
    assert build["name"] == "gcr.io/cloud-builders/docker"
    assert [render(arg) for arg in build["args"]] == [
        "build",
        "--build-arg",
        f"PYAIRBYTE_REQUIREMENT=airbyte=={version}",
        "--tag",
        image_uri,
        ".",
    ]
    assert [render(value) for value in config["images"]] == [image_uri]


def test_local_and_remote_bootstrap_commands_include_required_lock_inputs() -> None:
    text = (ROOT / "infra/internal-mcp-servers/BOOTSTRAP.md").read_text()
    assert '--output "$CLOUD_MCP_DIR/pylock.toml"' in text
    assert (
        text.count('--build-arg "PYAIRBYTE_REQUIREMENT=airbyte==$PYAIRBYTE_VERSION"')
        == 2
    )
    assert (
        text.count(
            "--config=infra/internal-mcp-servers/docker/cloud-mcp/cloudbuild.yaml"
        )
        == 2
    )
    assert text.count("_PYAIRBYTE_VERSION=${PYAIRBYTE_VERSION},_IMAGE=") == 2


def _step(name: str) -> dict[str, Any]:
    workflow = yaml.safe_load(WORKFLOW.read_text())
    return next(
        step
        for step in workflow["jobs"]["deploy-mcp"]["steps"]
        if step.get("name") == name
    )


def _run(
    name: str, tmp_path: Path, env: dict[str, str], curl: str = "exit 22"
) -> tuple[subprocess.CompletedProcess[str], dict[str, str]]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    curl_path = bin_dir / "curl"
    curl_path.write_text(f"#!/bin/sh\n{curl}\n")
    curl_path.chmod(0o755)
    output = tmp_path / "output"
    output.touch()
    result = subprocess.run(
        ["bash", "-euo", "pipefail", "-c", _step(name)["run"]],
        cwd=tmp_path,
        env={
            **os.environ,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "GITHUB_OUTPUT": str(output),
            "REQUESTED_SOURCE_SHA": "",
            **env,
        },
        capture_output=True,
        text=True,
        check=False,
    )
    return result, dict(line.split("=", 1) for line in output.read_text().splitlines())


@pytest.mark.parametrize(
    ("requirement", "release_tag"),
    [
        ("airbyte==1.0.0-rc.44", "v1.0.0-rc.44"),
        ("airbyte==1.0.0rc44", "v1.0.0-rc.44"),
        ("airbyte==0.56.0", "v0.56.0"),
    ],
)
def test_release_pin_selects_matching_asset(
    tmp_path: Path, requirement: str, release_tag: str
) -> None:
    result, outputs = _run(
        "Resolve PyAirbyte requirement",
        tmp_path,
        {"REQUESTED_REQUIREMENT": requirement, "IS_PREVIEW": "false"},
    )
    assert result.returncode == 0, result.stderr
    assert outputs == {"requirement": requirement, "release_tag": release_tag}


def test_empty_requirement_resolves_pypi_and_normalizes_release_tag(
    tmp_path: Path,
) -> None:
    result, outputs = _run(
        "Resolve PyAirbyte requirement",
        tmp_path,
        {"REQUESTED_REQUIREMENT": "", "IS_PREVIEW": "false"},
        curl='echo \'{"info": {"version": "1.0.0rc44"}}\'',
    )
    assert result.returncode == 0, result.stderr
    assert outputs == {
        "requirement": "airbyte==1.0.0rc44",
        "release_tag": "v1.0.0-rc.44",
    }


@pytest.mark.parametrize("curl", ["exit 22", "echo '{\"info\": {}}'"])
def test_pypi_lookup_failures_stop_before_build(tmp_path: Path, curl: str) -> None:
    result, outputs = _run(
        "Resolve PyAirbyte requirement",
        tmp_path,
        {"REQUESTED_REQUIREMENT": "", "IS_PREVIEW": "false"},
        curl=curl,
    )
    assert result.returncode != 0
    assert outputs == {}


def test_upstream_sha_preview_selects_commit_lock(tmp_path: Path) -> None:
    result, outputs = _run(
        "Resolve PyAirbyte requirement",
        tmp_path,
        {"REQUESTED_REQUIREMENT": GIT_REQUIREMENT, "IS_PREVIEW": "true"},
    )
    assert result.returncode == 0, result.stderr
    assert outputs == {"requirement": GIT_REQUIREMENT, "git_sha": SHA}


@pytest.mark.parametrize(
    "version",
    ["1.0.0rc44.dev1467123456", "1.0.0-rc.44.dev1467123456", "1.0.0.dev1+local"],
)
def test_published_dev_wheel_keeps_wheel_pin_and_exports_exact_source_lock(
    tmp_path: Path, version: str
) -> None:
    requirement = f"airbyte=={version}"
    result, outputs = _run(
        "Resolve PyAirbyte requirement",
        tmp_path,
        {
            "REQUESTED_REQUIREMENT": requirement,
            "REQUESTED_SOURCE_SHA": SHA,
            "IS_PREVIEW": "true",
        },
    )
    assert result.returncode == 0, result.stderr
    assert outputs == {"requirement": requirement, "git_sha": SHA}


@pytest.mark.parametrize(
    ("requirement", "preview", "source_sha"),
    [
        ("airbyte==1.0.0.dev1", "true", ""),
        ("airbyte==1.0.0.dev1", "false", SHA),
        ("airbyte==1.0.0.dev1", "false", ""),
        ("airbyte==1.0.0.dev1", "true", "a" * 7),
        ("airbyte==1.0.0.dev1", "true", "release-candidate/v1"),
        ("airbyte==1.0.0.dev1", "true", "A" * 40),
        ("airbyte==1.0.0.dev1", "true", SHA + "\nrequirement=other"),
        ("airbyte==1.0.0rc44", "true", SHA),
        (GIT_REQUIREMENT, "true", SHA),
    ],
)
def test_dev_wheel_source_contract_rejects_missing_mutable_or_release_overrides(
    tmp_path: Path, requirement: str, preview: str, source_sha: str
) -> None:
    result, outputs = _run(
        "Resolve PyAirbyte requirement",
        tmp_path,
        {
            "REQUESTED_REQUIREMENT": requirement,
            "REQUESTED_SOURCE_SHA": source_sha,
            "IS_PREVIEW": preview,
        },
    )
    assert result.returncode != 0
    assert "::error::" in result.stdout
    assert outputs == {}


def test_build_source_sha_is_wired_for_both_dispatch_styles() -> None:
    workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)
    inputs = workflow["on"]["workflow_dispatch"]["inputs"]
    assert inputs["cloud-mcp-pyairbyte-source-sha"]["default"] == ""
    assert workflow["env"]["MCP_CLOUD_MCP_PYAIRBYTE_SOURCE_SHA"] == (
        "${{ github.event.client_payload.cloud-mcp-pyairbyte-source-sha || "
        "github.event.inputs.cloud-mcp-pyairbyte-source-sha || '' }}"
    )
    assert _step("Resolve PyAirbyte requirement")["env"]["REQUESTED_SOURCE_SHA"] == (
        "${{ env.MCP_CLOUD_MCP_PYAIRBYTE_SOURCE_SHA }}"
    )


@pytest.mark.parametrize(
    ("requirement", "preview"),
    [
        (GIT_REQUIREMENT, "false"),
        (GIT_REQUIREMENT.replace(SHA, "release-candidate/v1"), "true"),
        (GIT_REQUIREMENT.replace("airbytehq", "another-owner"), "true"),
        ("airbyte>=1.0.0", "true"),
        ("airbyte==1.0.*", "false"),
        ("airbyte==1.0.0\nrequirement=other", "true"),
        ("airbyte @ https://example.com/airbyte.whl", "true"),
        ("other==1.0.0", "false"),
    ],
)
def test_unlocked_and_mutable_requirements_are_rejected(
    tmp_path: Path, requirement: str, preview: str
) -> None:
    result, outputs = _run(
        "Resolve PyAirbyte requirement",
        tmp_path,
        {"REQUESTED_REQUIREMENT": requirement, "IS_PREVIEW": preview},
    )
    assert result.returncode != 0
    assert "::error::Cloud MCP requires" in result.stdout
    assert outputs == {}


def test_missing_release_lock_fails_without_export_fallback(tmp_path: Path) -> None:
    result, _ = _run(
        "Download PyAirbyte release lock",
        tmp_path,
        {"RELEASE_TAG": "v1.0.0-rc.44", "BUILD_CONTEXT": str(tmp_path)},
    )
    assert result.returncode == 22
    assert not (tmp_path / "pylock.toml").exists()
    download = _step("Download PyAirbyte release lock")
    assert "outputs.release_tag != ''" in download["if"]
    assert "releases/download/${RELEASE_TAG}/pylock.toml" in download["run"]


def test_preview_exports_runtime_only_from_the_exact_commit() -> None:
    checkout = _step("Check out PyAirbyte preview lock source")
    export = _step("Export PyAirbyte preview lock")
    assert checkout["with"]["repository"] == "airbytehq/PyAirbyte"
    assert (
        checkout["with"]["ref"] == "${{ steps.pyairbyte-requirement.outputs.git_sha }}"
    )
    assert checkout["with"]["persist-credentials"] is False
    assert checkout["if"] == export["if"]
    assert "outputs.git_sha != ''" in export["if"]
    for argument in ("--locked", "--no-dev", "--no-emit-project", "--extra datadog"):
        assert argument in export["run"]
    assert (
        '--output-file "$GITHUB_WORKSPACE/$BUILD_CONTEXT/pylock.toml"' in export["run"]
    )


def test_dockerfile_preserves_the_lock_when_installing_extras() -> None:
    dockerfile = (CONTEXT / "Dockerfile").read_text()
    lock = dockerfile.index("uv pip install -r /app/pylock.toml")
    wheel = dockerfile.index(
        'uv pip install --no-cache --no-deps -- "$PYAIRBYTE_REQUIREMENT"'
    )
    extras = dockerfile.index("--constraint /tmp/locked-constraints.txt")
    assert lock < wheel < extras
    assert "--prerelease=allow" not in dockerfile
    assert 'test -n "$PYAIRBYTE_REQUIREMENT"' in dockerfile
    requirements = (CONTEXT / "requirements.txt").read_text().splitlines()
    assert "airbyte" not in requirements
    assert "ddtrace" not in requirements
