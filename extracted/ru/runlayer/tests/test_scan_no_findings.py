"""_no_findings treats agents as findings on every path (F5 regression)."""

from __future__ import annotations

from runlayer_cli.commands.scan import _no_findings
from runlayer_cli.scan.agent_definition_scanner import DiscoveredAgentDefinition
from runlayer_cli.scan.client_presence import DetectedClient
from runlayer_cli.scan.agents.detect import build_install_agent
from runlayer_cli.scan.device import DiscoveredWSLDistro
from runlayer_cli.scan.service import ScanResult


def _result(**overrides) -> ScanResult:
    base = dict(
        device_id="d",
        hostname=None,
        os=None,
        os_version=None,
        username=None,
        org_device_id=None,
        scan_duration_ms=0,
        collector_version="test",
        configurations=[],
    )
    base.update(overrides)
    return ScanResult(**base)


def test_empty_scan_is_no_findings():
    assert _no_findings(_result()) is True


def test_detected_client_only_is_a_finding():
    detected = DetectedClient(
        client="cursor",
        display_name="Cursor",
        detected_via=["app"],
    )
    assert _no_findings(_result(detected_clients=[detected])) is False


def test_agents_only_is_a_finding():
    # The submit path previously ignored agents here and printed "nothing found"
    # for an agent-only scan. Agents must count as a finding everywhere.
    agent = build_install_agent(
        framework_id="openclaw",
        display_name="OpenClaw",
        location="/Users/dev/.openclaw",
        evidence=[],
        markers=["cli"],
    )
    assert _no_findings(_result(agents=[agent])) is False


def test_agent_definitions_only_is_a_finding():
    definition = DiscoveredAgentDefinition(
        client="cursor",
        name="reviewer",
        description=None,
        scope="project",
        path="/repo/.cursor/agents/review.md",
        project_path="/repo",
        content_hash="hash",
    )

    assert _no_findings(_result(agent_definitions=[definition])) is False


def test_containers_only_is_a_finding():
    assert _no_findings(_result(containers=[object()])) is False


def test_successful_empty_container_inventory_is_a_finding():
    """The backend needs an explicit empty inventory to mark prior rows stopped."""
    assert _no_findings(_result(containers_scanned=True)) is False


def test_wsl_inventory_only_is_a_finding():
    distro = DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)

    assert _no_findings(_result(wsl_distros=[distro], wsl_scanned=True)) is False


def test_successful_empty_wsl_inventory_is_a_finding():
    assert _no_findings(_result(wsl_scanned=True)) is False
