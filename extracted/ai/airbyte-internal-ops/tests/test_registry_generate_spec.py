# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for docker spec extraction in registry/generate.py."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.registry.generate import _run_docker_spec


def _completed(stdout: str) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=0, stdout=stdout, stderr="")


@pytest.mark.unit
@pytest.mark.parametrize(
    "mode,expected_edition",
    [
        pytest.param("cloud", "CLOUD", id="cloud"),
        pytest.param("oss", "COMMUNITY", id="oss"),
    ],
)
def test_run_docker_spec_sets_both_deployment_env_vars(
    mode: str, expected_edition: str
) -> None:
    spec_msg = json.dumps({"type": "SPEC", "spec": {"connectionSpecification": {}}})
    with patch(
        "airbyte_ops_mcp.registry.generate.subprocess.run",
        return_value=_completed(spec_msg),
    ) as mock_run:
        result = _run_docker_spec("airbyte/destination-dev-null:0.9.4", mode)

    assert result == {"connectionSpecification": {}}
    cmd = mock_run.call_args.args[0]
    assert f"DEPLOYMENT_MODE={mode}" in cmd
    assert f"AIRBYTE_EDITION={expected_edition}" in cmd
    assert cmd[-2:] == ["airbyte/destination-dev-null:0.9.4", "spec"]
