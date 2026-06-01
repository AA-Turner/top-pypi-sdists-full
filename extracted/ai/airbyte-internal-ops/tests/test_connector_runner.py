# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Docker-based connector runner."""

from __future__ import annotations

from pathlib import Path

import pytest

from airbyte_ops_mcp.regression_tests.connector_runner import ConnectorRunner
from airbyte_ops_mcp.regression_tests.models import (
    Command,
    ConnectorUnderTest,
    ExecutionInputs,
    TargetOrControl,
)


@pytest.fixture
def connector_under_test() -> ConnectorUnderTest:
    return ConnectorUnderTest(
        image_name="airbyte/source-shopify:3.2.4",
        target_or_control=TargetOrControl.TARGET,
    )


@pytest.fixture
def execution_inputs(
    connector_under_test: ConnectorUnderTest, tmp_path: Path
) -> ExecutionInputs:
    return ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )


@pytest.fixture
def runner(execution_inputs: ExecutionInputs) -> ConnectorRunner:
    return ConnectorRunner(execution_inputs=execution_inputs)


def test_build_docker_command_overrides_workdir(
    runner: ConnectorRunner, tmp_path: Path
) -> None:
    """The docker command must override the container's WORKDIR to /tmp.

    This ensures the non-root `airbyte` user (UID 1000) can write temporary files
    (e.g. bulk GraphQL result files in source-shopify) via relative paths without
    shadowing the connector code installed at /airbyte/integration_code.
    """
    cmd = runner._build_docker_command(tmp_path)

    assert "-w" in cmd, "Docker command must include -w flag"
    w_idx = cmd.index("-w")
    assert cmd[w_idx + 1] == "/tmp", (
        f"WORKDIR override must be /tmp, got: {cmd[w_idx + 1]}"
    )


@pytest.mark.parametrize(
    "proxy_url,expect_proxy_env",
    [
        pytest.param(None, False, id="no-proxy"),
        pytest.param("http://host.docker.internal:8080", True, id="with-proxy"),
    ],
)
def test_build_docker_command_proxy_settings(
    connector_under_test: ConnectorUnderTest,
    tmp_path: Path,
    proxy_url: str | None,
    expect_proxy_env: bool,
) -> None:
    """Proxy settings should be added when proxy_url is set, regardless of the /tmp WORKDIR override."""
    inputs = ExecutionInputs(
        connector_under_test=connector_under_test,
        command=Command.SPEC,
        output_dir=tmp_path / "output",
    )
    runner = ConnectorRunner(execution_inputs=inputs, proxy_url=proxy_url)
    cmd = runner._build_docker_command(tmp_path)

    if expect_proxy_env:
        assert "-e" in cmd
        env_values = [cmd[i + 1] for i, v in enumerate(cmd) if v == "-e"]
        proxy_envs = [e for e in env_values if "PROXY" in e.upper()]
        assert len(proxy_envs) >= 2, "Should set at least HTTP_PROXY and HTTPS_PROXY"
    else:
        env_values = [cmd[i + 1] for i, v in enumerate(cmd) if v == "-e"]
        proxy_envs = [e for e in env_values if "PROXY" in e.upper()]
        assert len(proxy_envs) == 0, "No proxy env vars expected"

    # WORKDIR override should always be present
    assert "-w" in cmd
