"""Verbose scan output must render the per-agent evidence detail section.

Regression: the scan command called ``format_summary(result.agents)`` inside its
``if verbose and not quiet`` guard but dropped ``verbose``, so the "Evidence
detail:" block (only emitted when ``verbose=True``) never printed.
"""

from __future__ import annotations

from unittest import mock

import pytest
import typer

from runlayer_cli.commands.scan import _run_scan
from runlayer_cli.scan.agents.detect import (
    DiscoveredAgent,
    Evidence,
    METHOD_STATIC,
)
from runlayer_cli.scan.service import ScanResult


def _agent_with_evidence() -> DiscoveredAgent:
    return DiscoveredAgent(
        location="/x/proj",
        name="proj",
        framework_id="langchain",
        display_name="Langchain",
        language="Python",
        confidence=0.9,
        margin=0.9,
        score=9.0,
        runner_up=None,
        runner_up_score=0.0,
        detection_method=METHOD_STATIC,
        evidence=[Evidence("package_dep", "langchain", "pyproject.toml")],
        manifests=["pyproject.toml"],
        languages=["Python"],
        agent_fingerprint="f" * 64,
    )


def _result_with_agent() -> ScanResult:
    return ScanResult(
        device_id="d",
        hostname=None,
        os=None,
        os_version=None,
        username=None,
        org_device_id=None,
        scan_duration_ms=0,
        collector_version="test",
        configurations=[],
        agents=[_agent_with_evidence()],
    )


@mock.patch("runlayer_cli.commands.scan.scan_all_clients")
def test_verbose_scan_prints_evidence_detail(mock_scan, capsys):
    """--verbose must forward through to format_summary so evidence detail prints."""
    mock_scan.return_value = _result_with_agent()

    with pytest.raises(typer.Exit):
        _run_scan(
            effective_host="h",
            effective_secret="s",
            device_id=None,
            org_device_id=None,
            dry_run=True,
            verbose=True,
            quiet=False,
            no_projects=True,
            project_depth=7,
            project_timeout=60,
            cpu_cores=2,
            max_cpu_percent=50,
            memory_limit_mb=1024,
            username=None,
            detect_agents=True,
            detect_agent_frameworks=True,
            detect_processes=False,
            detect_containers=False,
            detect_disguised_skills=False,
            detect_renamed_plugin_caches=False,
            log_file_path="x",
        )

    out = capsys.readouterr().out
    assert "Evidence detail:" in out
