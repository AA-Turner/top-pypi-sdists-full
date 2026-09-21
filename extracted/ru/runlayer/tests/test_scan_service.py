"""Tests for scan service orchestration."""

from contextlib import contextmanager
import datetime
import getpass
import json
import os
from pathlib import Path
import threading
from types import SimpleNamespace
from unittest import mock
import uuid

import httpx
import pytest
import structlog

from runlayer_cli.scan import orchestrator as scan_orchestrator
from runlayer_cli.scan import service as scan_service
from runlayer_cli.scan.agent_scan import AgentScanResult
from runlayer_cli.scan.client_presence import DetectedClient
from runlayer_cli.scan.clients import get_all_clients, get_client_by_name
from runlayer_cli.scan.completeness import ScanCompleteness, ScanCompletionStatus
from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig
from runlayer_cli.scan.processes.models import (
    DiscoveredProcess,
    ExtensionRootRef,
    OverrideConfigRef,
    ProcessDiscoveryResult,
)
from runlayer_cli.scan.skill_presence import (
    SkillPresenceParams,
    build_state,
    load_state,
    path_hash,
    save_state,
)
from runlayer_cli.scan.skill_scanner import SkillPhaseScan
from runlayer_cli.scan.timing import PhaseTimer
from runlayer_cli.scan.service import (
    CATEGORY_SURFACES,
    EXIT_SUBMIT_FAILED,
    EXIT_UNSUPPORTED,
    MAX_AGENT_DEFINITIONS,
    MAX_AGENTS,
    ScanResult,
    ScanSubmissionResult,
    ServerSubmission,
    _attribute_wsl_artifacts,
    _dedupe_path_configurations,
    _parse_process_override_configurations,
    _scan_manifest_payload,
    dedupe_host_container_configurations,
    reconcile_skill_presence,
    scan_all_clients,
    submit_discovered_agent_definitions,
    submit_discovered_agents,
    submit_discovered_servers,
    submit_scan_results,
)


def _effective_process_owner() -> str:
    get_euid = getattr(os, "geteuid", None)
    if callable(get_euid):
        return str(get_euid())
    return getpass.getuser()


def _wsl_inventory(names: tuple[str, ...], *, success: bool):
    from runlayer_cli.scan.device import DiscoveredWSLDistro, WSLDistroInventory

    return WSLDistroInventory(
        distros=tuple(
            DiscoveredWSLDistro(name=name, wsl_version=2, is_running=True)
            for name in names
        ),
        success=success,
    )


def test_project_phase_preserves_client_entry_format(tmp_path, monkeypatch):
    project = tmp_path / "project"
    config_path = project / "kilo.jsonc"
    project.mkdir()
    config_path.write_text(
        '{"mcp":{"filesystem":{"type":"local","command":["npx","-y","server"]}}}',
        encoding="utf-8",
    )
    client = scan_orchestrator.get_client_by_name("kilo_code")
    assert client is not None

    monkeypatch.setattr(
        scan_orchestrator, "get_clients_with_project_configs", lambda: [client]
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "get_client_by_name",
        lambda name: client if name == "kilo_code" else None,
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_and_node_modules_under_home",
        lambda *args, **kwargs: SimpleNamespace(
            found_paths=[config_path],
            node_modules_paths=[],
            logical_paths={},
            complete=True,
        ),
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_under_project_roots",
        lambda *args, **kwargs: [],
    )

    result = scan_orchestrator._scan_project_phase(
        governor=SimpleNamespace(checkpoint=lambda: None),
        project_scan_timeout=60,
        project_scan_depth=7,
        run_static_agents=False,
    )

    assert len(result.configurations) == 1
    server = result.configurations[0].servers[0]
    assert server.command == "npx"
    assert server.args == ["-y", "server"]
    assert result.skill_crawl_complete is True


def test_project_phase_nested_crawl_failure_marks_skill_crawl_incomplete(
    tmp_path, monkeypatch
):
    project = tmp_path / "project"
    config_path = project / "kilo.jsonc"
    project.mkdir()
    config_path.write_text(
        '{"mcp":{"filesystem":{"type":"local","command":["npx","-y","server"]}}}',
        encoding="utf-8",
    )
    client = scan_orchestrator.get_client_by_name("kilo_code")
    assert client is not None

    monkeypatch.setattr(
        scan_orchestrator, "get_clients_with_project_configs", lambda: [client]
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "get_client_by_name",
        lambda name: client if name == "kilo_code" else None,
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_and_node_modules_under_home",
        lambda *args, **kwargs: SimpleNamespace(
            found_paths=[config_path],
            node_modules_paths=[],
            logical_paths={},
            complete=True,
        ),
    )

    def incomplete_nested_crawl(*args, **kwargs):
        kwargs["completion"].mark_incomplete("nested_project_crawl_timed_out")
        return []

    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_under_project_roots",
        incomplete_nested_crawl,
    )

    result = scan_orchestrator._scan_project_phase(
        governor=SimpleNamespace(checkpoint=lambda: None),
        project_scan_timeout=60,
        project_scan_depth=7,
        run_static_agents=False,
    )

    assert result.skill_crawl_complete is False


def test_project_phase_main_crawl_failure_marks_skill_crawl_incomplete(monkeypatch):
    monkeypatch.setattr(
        scan_orchestrator, "get_clients_with_project_configs", lambda: []
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_and_node_modules_under_home",
        lambda *args, **kwargs: SimpleNamespace(
            found_paths=[],
            node_modules_paths=[],
            logical_paths={},
            complete=False,
        ),
    )

    result = scan_orchestrator._scan_project_phase(
        governor=SimpleNamespace(checkpoint=lambda: None),
        project_scan_timeout=60,
        project_scan_depth=7,
        run_static_agents=False,
    )

    assert result.skill_crawl_complete is False


def test_project_phase_propagates_skill_candidate_paths(tmp_path, monkeypatch):
    skill_dir = tmp_path / "project" / ".agents" / "skills" / "deploy"
    skill_dir.mkdir(parents=True)
    marker = skill_dir / "SKILL.md"
    marker.write_text("---\nname: deploy\ndescription: Deploy helper\n---\n")
    monkeypatch.setattr(
        scan_orchestrator, "get_clients_with_project_configs", lambda: []
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_and_node_modules_under_home",
        lambda *args, **kwargs: SimpleNamespace(
            found_paths=[marker],
            node_modules_paths=[],
            logical_paths={},
            complete=True,
        ),
    )

    result = scan_orchestrator._scan_project_phase(
        governor=SimpleNamespace(checkpoint=lambda: None),
        project_scan_timeout=60,
        project_scan_depth=7,
        run_static_agents=False,
    )

    assert result.project_skill_candidate_paths == [str(skill_dir.resolve())]


def test_project_skill_processing_failure_does_not_poison_mcp(tmp_path, monkeypatch):
    monkeypatch.setattr(
        scan_orchestrator,
        "get_clients_with_project_configs",
        lambda: [],
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "find_files_and_node_modules_under_home",
        lambda *args, **kwargs: SimpleNamespace(
            found_paths=[],
            node_modules_paths=[],
            logical_paths={},
            complete=True,
        ),
    )

    def capped_skills(*_args, scan_status, **_kwargs):
        scan_status.mark_incomplete("project_skill_scan_capped")
        return SkillPhaseScan([], [])

    monkeypatch.setattr(
        scan_orchestrator,
        "process_skill_paths_with_candidates",
        capped_skills,
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "process_agent_definition_paths",
        lambda *_args, **_kwargs: [],
    )
    monkeypatch.setattr(
        scan_orchestrator,
        "process_project_gemini_extensions",
        lambda _paths: ([], []),
    )

    result = scan_orchestrator._scan_project_phase(
        governor=SimpleNamespace(checkpoint=lambda: None),
        project_scan_timeout=60,
        project_scan_depth=7,
        run_static_agents=False,
    )

    assert result.completion.complete is True
    assert result.mcp_completion.complete is True
    assert result.skill_completion.reasons == ["project_skill_scan_capped"]


def test_container_config_dedupe_keeps_unverified_cross_surface_matches():
    duplicate_hash = "a" * 64
    host = MCPClientConfig(
        client="cursor",
        config_path=(
            "/Users/dev/OrbStack/docker/containers/cursor/workspace/orders/"
            ".cursor/mcp.json"
        ),
        project_path=("/Users/dev/OrbStack/docker/containers/cursor/workspace/orders"),
        config_scope="project",
        servers=[
            MCPServerConfig(name="github", type="stdio", config_hash=duplicate_hash)
        ],
    )
    different = MCPClientConfig(
        client="cursor",
        config_path="/Users/dev/project/.cursor/mcp.json",
        project_path="/Users/dev/project",
        config_scope="project",
        servers=[MCPServerConfig(name="linear", type="stdio", config_hash="b" * 64)],
    )
    container = MCPClientConfig(
        client="cursor",
        config_path="/workspace/orders/.cursor/mcp.json",
        project_path="/workspace/orders",
        config_scope="container",
        container_id="container-1",
        servers=[
            MCPServerConfig(name="github", type="stdio", config_hash=duplicate_hash)
        ],
    )

    deduped = dedupe_host_container_configurations([host, different, container])

    assert deduped == [host, different, container]


def test_container_config_dedupe_keeps_private_container_path_matching_host_file(
    tmp_path,
):
    duplicate_hash = "a" * 64
    project = tmp_path / "project"
    config_path = project / ".cursor" / "mcp.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("{}")
    host = MCPClientConfig(
        client="cursor",
        config_path=str(config_path),
        project_path=str(project),
        config_scope="project",
        servers=[
            MCPServerConfig(name="github", type="stdio", config_hash=duplicate_hash)
        ],
    )
    container = MCPClientConfig(
        client="cursor",
        config_path=str(config_path),
        project_path=str(project),
        config_scope="container",
        container_id="container-1",
        container_mounts_host_home=False,
        servers=[
            MCPServerConfig(name="github", type="stdio", config_hash=duplicate_hash)
        ],
    )

    assert dedupe_host_container_configurations([host, container]) == [host, container]


def test_container_config_dedupe_prefers_verified_same_backing_file(tmp_path):
    duplicate_hash = "a" * 64
    host_project = tmp_path / "host" / "orders"
    container_project = tmp_path / "container" / "orders"
    host_config = host_project / ".cursor" / "mcp.json"
    container_config = container_project / ".cursor" / "mcp.json"
    host_config.parent.mkdir(parents=True)
    container_config.parent.mkdir(parents=True)
    host_config.write_text("{}")
    os.link(host_config, container_config)
    host = MCPClientConfig(
        client="cursor",
        config_path=str(host_config),
        project_path=str(host_project),
        config_scope="project",
        servers=[
            MCPServerConfig(name="github", type="stdio", config_hash=duplicate_hash)
        ],
    )
    container = MCPClientConfig(
        client="cursor",
        config_path=str(container_config),
        project_path=str(container_project),
        config_scope="container",
        container_id="container-1",
        container_mounts_host_home=True,
        servers=[
            MCPServerConfig(name="github", type="stdio", config_hash=duplicate_hash)
        ],
    )

    assert dedupe_host_container_configurations([host, container]) == [container]


def test_path_dedupe_keeps_one_path_reported_under_several_identities():
    """One config path repeats across projects and containers legitimately."""
    plugin_in_orders = MCPClientConfig(
        client="cursor",
        config_path="/Users/dev/.cursor/plugins/linear/mcp.json",
        project_path="/Users/dev/orders",
        config_scope="project",
        plugin_identifier="linear",
        servers=[MCPServerConfig(name="linear", type="stdio")],
    )
    plugin_in_billing = MCPClientConfig(
        client="cursor",
        config_path="/Users/dev/.cursor/plugins/linear/mcp.json",
        project_path="/Users/dev/billing",
        config_scope="project",
        plugin_identifier="linear",
        servers=[MCPServerConfig(name="linear", type="stdio")],
    )
    container_one = MCPClientConfig(
        client="cursor",
        config_path="/workspace/.cursor/mcp.json",
        project_path="/workspace",
        config_scope="container",
        container_id="container-1",
        servers=[MCPServerConfig(name="github", type="stdio")],
    )
    container_two = MCPClientConfig(
        client="cursor",
        config_path="/workspace/.cursor/mcp.json",
        project_path="/workspace",
        config_scope="container",
        container_id="container-2",
        servers=[MCPServerConfig(name="github", type="stdio")],
    )
    rediscovered_container_one = MCPClientConfig(
        client="cursor",
        config_path="/workspace/.cursor/mcp.json",
        project_path="/workspace",
        config_scope="container",
        container_id="container-1",
        servers=[MCPServerConfig(name="github", type="stdio")],
    )

    deduped = _dedupe_path_configurations(
        [
            plugin_in_orders,
            plugin_in_billing,
            container_one,
            container_two,
            rediscovered_container_one,
        ]
    )

    assert [id(config) for config in deduped] == [
        id(plugin_in_orders),
        id(plugin_in_billing),
        id(container_one),
        id(container_two),
    ]


def test_path_dedupe_separates_one_linux_path_across_distros():
    ubuntu = MCPClientConfig(
        client="cursor",
        config_path="/home/dev/.cursor/mcp.json",
        config_scope="wsl",
        wsl_distro="Ubuntu",
        wsl_user="dev",
        servers=[MCPServerConfig(name="github", type="stdio")],
    )
    debian = MCPClientConfig(
        client="cursor",
        config_path="/home/dev/.cursor/mcp.json",
        config_scope="wsl",
        wsl_distro="Debian",
        wsl_user="dev",
        servers=[MCPServerConfig(name="github", type="stdio")],
    )
    ubuntu_case_variant = MCPClientConfig(
        client="cursor",
        config_path="/home/dev/.cursor/mcp.json",
        config_scope="wsl",
        wsl_distro="ubuntu",
        wsl_user="dev",
        servers=[MCPServerConfig(name="github", type="stdio")],
    )

    deduped = _dedupe_path_configurations([ubuntu, debian, ubuntu_case_variant])

    assert [id(config) for config in deduped] == [id(ubuntu), id(debian)]


def test_process_override_parses_vscode_user_data_config(tmp_path):
    vscode = get_client_by_name("vscode")
    assert vscode is not None
    user_data_dir = tmp_path / "custom-code"
    config_path = user_data_dir / "User" / "mcp.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        json.dumps({"servers": {"custom": {"command": "npx", "args": ["server"]}}}),
        encoding="utf-8",
    )

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="vscode",
                flag="--user-data-dir",
                value=str(user_data_dir),
                mcp_config="user_data_dir",
                user=_effective_process_owner(),
                pid=100,
            )
        ],
        configurations=[],
        clients=[vscode],
    )

    assert len(parsed) == 1
    assert parsed[0].config_path == str(config_path)
    assert parsed[0].config_scope == "process_override"
    assert parsed[0].servers[0].name == "custom"


def test_process_override_trusts_matching_sid_under_system(tmp_path):
    vscode = get_client_by_name("vscode")
    assert vscode is not None
    target_sid = "S-1-5-21-1-2-3-1001"
    user_data_dir = tmp_path / "custom-code"
    config_path = user_data_dir / "User" / "mcp.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        json.dumps({"servers": {"custom": {"command": "npx"}}}),
        encoding="utf-8",
    )

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="vscode",
                flag="--user-data-dir",
                value=str(user_data_dir),
                mcp_config="user_data_dir",
                user="SYSTEM",
                pid=100,
                owner_sid=target_sid,
            )
        ],
        configurations=[],
        clients=[vscode],
        windows_user_sid=target_sid,
    )

    assert [config.config_path for config in parsed] == [str(config_path)]


@pytest.mark.parametrize(
    ("owner_sid", "expected_reasons"),
    [
        (None, ["runtime_owner_resolution_failed"]),
        ("S-1-5-21-9-8-7-1002", []),
    ],
)
def test_process_override_rejects_missing_or_mismatched_target_sid(
    tmp_path,
    owner_sid,
    expected_reasons,
):
    claude = get_client_by_name("claude_code")
    assert claude is not None
    status = ScanCompletionStatus()

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value=str(tmp_path / "mcp.json"),
                mcp_config="file",
                user="SYSTEM",
                pid=100,
                owner_sid=owner_sid,
            )
        ],
        configurations=[],
        clients=[claude],
        scan_status=status,
        windows_user_sid="S-1-5-21-1-2-3-1001",
    )

    assert parsed == []
    assert status.reasons == expected_reasons


def test_process_override_unresolved_path_marks_runtime_incomplete() -> None:
    claude = get_client_by_name("claude_code")
    assert claude is not None
    status = ScanCompletionStatus()

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value="relative-mcp.json",
                mcp_config="file",
                user=_effective_process_owner(),
                pid=100,
            )
        ],
        configurations=[],
        clients=[claude],
        scan_status=status,
    )

    assert parsed == []
    assert status.reasons == ["runtime_override_config_path_resolution_failed"]


def test_excluded_process_override_client_does_not_mark_path_failure() -> None:
    status = ScanCompletionStatus()

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value="relative-mcp.json",
                mcp_config="file",
                user=_effective_process_owner(),
                pid=100,
            )
        ],
        configurations=[],
        clients=[],
        scan_status=status,
    )

    assert parsed == []
    assert status.complete
    assert status.reasons == []


def test_process_override_path_conversion_failure_marks_runtime_incomplete(
    monkeypatch,
) -> None:
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    status = ScanCompletionStatus()
    monkeypatch.setattr(
        scan_service,
        "Path",
        mock.Mock(side_effect=OSError("path conversion failed")),
    )

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value="redacted-sensitive-path",
                mcp_config="file",
                user=_effective_process_owner(),
                pid=100,
            )
        ],
        configurations=[],
        clients=[claude],
        scan_status=status,
    )

    assert parsed == []
    assert status.reasons == ["runtime_override_config_path_resolution_failed"]


def test_process_extension_non_directory_marks_runtime_incomplete(tmp_path):
    from runlayer_cli.scan import service as scan_service

    extension_root = tmp_path / "extensions"
    extension_root.write_text("not a directory")
    status = ScanCompletionStatus()

    roots = scan_service._resolve_process_extension_roots(
        [
            ExtensionRootRef(
                client="vscode",
                flag="--extensions-dir",
                value=str(extension_root),
                pid=42,
                user=_effective_process_owner(),
            )
        ],
        scan_status=status,
    )

    assert roots == []
    assert status.reasons == ["runtime_extension_root_not_directory"]


def test_wsl_process_extension_root_keeps_distro_identity(
    tmp_path,
    monkeypatch,
) -> None:
    from runlayer_cli.scan import service as scan_service

    distro_root = tmp_path / "Ubuntu"
    extension_root = distro_root / "home" / "alice" / ".vscode" / "extensions"
    extension_root.mkdir(parents=True)
    monkeypatch.setattr(
        scan_service,
        "get_wsl_distro_root",
        lambda distro: distro_root if distro == "Ubuntu" else None,
    )

    roots = scan_service._resolve_process_extension_roots(
        [
            ExtensionRootRef(
                client="vscode",
                flag="--extensions-dir",
                value="/home/alice/.vscode/extensions",
                pid=42,
                user="alice",
                wsl_distro="Ubuntu",
            )
        ]
    )

    assert len(roots) == 1
    assert roots[0].path == extension_root
    assert roots[0].client == "vscode"
    assert roots[0].wsl_distro == "Ubuntu"


def test_wsl_process_extension_plugin_keeps_host_runtime_manifest_surface() -> None:
    from runlayer_cli.scan import service as scan_service

    plugin = SimpleNamespace(
        container_id=None,
        device_scope=False,
        scope="process_override",
        wsl_distro="Ubuntu",
    )

    assert scan_service._artifact_manifest_surface(plugin, kind="plugin") == (
        "host_runtime"
    )


def test_wsl_plugin_maps_to_host_static_surface_the_manifest_emits() -> None:
    from runlayer_cli.scan import service as scan_service

    artifact = SimpleNamespace(
        container_id=None,
        device_scope=False,
        scope="user",
        wsl_distro="Ubuntu",
    )

    assert scan_service._artifact_manifest_surface(artifact, kind="skill") == "wsl"
    plugin_surface = scan_service._artifact_manifest_surface(artifact, kind="plugin")
    assert plugin_surface == "host_static"
    assert plugin_surface in scan_service.CATEGORY_SURFACES["plugin"]


def test_wsl_plugin_without_identifier_gates_plugin_host_static() -> None:
    from runlayer_cli.scan.service import submit_scan_results

    client = mock.MagicMock()
    client.submit_scan_manifest.return_value = {"reconciled": 0}
    scan_result = _submission_scan_result(os_name="windows", wsl_scanned=True)
    scan_result.plugins = [
        SimpleNamespace(
            name="wsl-plugin",
            identifier=None,
            container_id=None,
            device_scope=False,
            scope="user",
            wsl_distro="Ubuntu",
        )
    ]

    submission = submit_scan_results(client, scan_result)

    assert submission.incomplete_surfaces[("plugin", "host_static")] == (
        "plugin_identifier_missing"
    )
    assert all(
        surface in submission.surface_outcomes
        for surface in submission.incomplete_surfaces
    )
    entries = {
        (entry["category"], entry["surface"]): entry
        for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
    }
    assert entries[("plugin", "host_static")]["complete"] is False
    assert entries[("plugin", "host_static")]["reason"] == "plugin_identifier_missing"


def test_process_extension_unresolved_path_marks_runtime_incomplete() -> None:
    from runlayer_cli.scan import service as scan_service

    status = ScanCompletionStatus()

    roots = scan_service._resolve_process_extension_roots(
        [
            ExtensionRootRef(
                client="vscode",
                flag="--extensions-dir",
                value="relative-extensions",
                pid=42,
                user=_effective_process_owner(),
            )
        ],
        scan_status=status,
    )

    assert roots == []
    assert status.reasons == ["runtime_extension_root_path_resolution_failed"]


def test_process_override_maps_wsl_home_path_with_distro_identity(
    tmp_path,
    monkeypatch,
):
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    distro_root = tmp_path / "Ubuntu"
    config_path = distro_root / "home" / "alice" / "mcp.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        json.dumps({"mcpServers": {"custom": {"command": "npx"}}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        scan_service,
        "get_wsl_distro_root",
        lambda distro: distro_root if distro == "Ubuntu" else None,
        raising=False,
    )

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value="/home/alice/mcp.json",
                mcp_config="file",
                user="alice",
                pid=100,
                wsl_distro="Ubuntu",
            )
        ],
        configurations=[],
        clients=[claude],
    )

    assert len(parsed) == 1
    assert parsed[0].config_path == "/home/alice/mcp.json"
    assert parsed[0].config_scope == "process_override"
    assert parsed[0].wsl_distro == "Ubuntu"
    assert parsed[0].wsl_user == "alice"


def test_process_override_dedupes_pre_attributed_wsl_config(
    tmp_path,
    monkeypatch,
):
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    distro_root = tmp_path / "Ubuntu"
    config_path = distro_root / "home" / "alice" / "mcp.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        json.dumps({"mcpServers": {"custom": {"command": "npx"}}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        scan_service,
        "get_wsl_distro_root",
        lambda distro: distro_root if distro == "Ubuntu" else None,
        raising=False,
    )
    existing = MCPClientConfig(
        client="claude_code",
        config_path="/home/alice/mcp.json",
        config_scope="wsl",
        wsl_distro="Ubuntu",
        wsl_user="alice",
        servers=[MCPServerConfig(name="custom", type="stdio")],
    )

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value="/home/alice/mcp.json",
                mcp_config="file",
                user="alice",
                pid=100,
                wsl_distro="Ubuntu",
            )
        ],
        configurations=[existing],
        clients=[claude],
    )

    assert parsed == []


def test_process_override_rejects_wsl_path_outside_process_owner_home(
    tmp_path,
    monkeypatch,
):
    from runlayer_cli.scan import service as scan_service

    monkeypatch.setattr(
        scan_service,
        "get_wsl_distro_root",
        lambda _distro: tmp_path,
    )
    ref = OverrideConfigRef(
        client="claude_code",
        flag="--mcp-config",
        value="/home/bob/mcp.json",
        mcp_config="file",
        user="alice",
        pid=100,
        wsl_distro="Ubuntu",
    )

    assert scan_service._resolve_override_config_path(ref) is None


def test_process_override_missing_wsl_root_marks_runtime_incomplete(
    monkeypatch,
) -> None:
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    monkeypatch.setattr(scan_service, "get_wsl_distro_root", lambda _distro: None)
    status = ScanCompletionStatus()

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value="/home/alice/mcp.json",
                mcp_config="file",
                user="alice",
                pid=100,
                wsl_distro="Ubuntu",
            )
        ],
        configurations=[],
        clients=[claude],
        scan_status=status,
    )

    assert parsed == []
    assert status.reasons == ["runtime_override_config_path_resolution_failed"]


def test_process_extension_outside_wsl_home_marks_runtime_incomplete(
    tmp_path,
    monkeypatch,
) -> None:
    from runlayer_cli.scan import service as scan_service

    monkeypatch.setattr(
        scan_service,
        "get_wsl_distro_root",
        lambda _distro: tmp_path,
    )
    status = ScanCompletionStatus()

    roots = scan_service._resolve_process_extension_roots(
        [
            ExtensionRootRef(
                client="vscode",
                flag="--extensions-dir",
                value="/home/bob/.vscode/extensions",
                user="alice",
                pid=100,
                wsl_distro="Ubuntu",
            )
        ],
        scan_status=status,
    )

    assert roots == []
    assert status.reasons == ["runtime_extension_root_path_resolution_failed"]


def test_process_override_skips_path_already_scanned(tmp_path):
    claude = get_client_by_name("claude_code")
    assert claude is not None
    config_path = tmp_path / "mcp.json"
    config_path.write_text(
        json.dumps({"mcpServers": {"custom": {"command": "npx"}}}),
        encoding="utf-8",
    )
    existing = MCPClientConfig(
        client="claude_code",
        config_path=str(config_path),
        config_scope="global",
        servers=[MCPServerConfig(name="custom", type="stdio")],
    )

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value=str(config_path),
                mcp_config="file",
                user=_effective_process_owner(),
                pid=101,
            )
        ],
        configurations=[existing],
        clients=[claude],
    )

    assert parsed == []


@pytest.mark.parametrize("process_user", [None, "definitely-not-the-scan-user"])
def test_process_override_skips_untrusted_process_owner(
    tmp_path, process_user, monkeypatch
):
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    config_path = tmp_path / "mcp.json"
    config_path.write_text(
        json.dumps({"mcpServers": {"custom": {"command": "npx"}}}),
        encoding="utf-8",
    )
    ref = SimpleNamespace(
        client="claude_code",
        flag="--mcp-config",
        value=str(config_path),
        mcp_config="file",
        pid=102,
        cwd=None,
        user=process_user,
    )
    logger = mock.Mock()
    monkeypatch.setattr(scan_service, "logger", logger)

    parsed = _parse_process_override_configurations(
        [ref],
        configurations=[],
        clients=[claude],
    )

    assert parsed == []
    logger.debug.assert_called_once_with(
        "process_override_config_skipped_untrusted_owner",
        client="claude_code",
        flag="--mcp-config",
        owner_status="unknown" if process_user is None else "mismatch",
    )
    assert str(config_path) not in repr(logger.mock_calls)


def test_process_override_resolves_windows_owner_before_parsing(tmp_path, monkeypatch):
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    config_path = tmp_path / "mcp.json"
    config_path.write_text(
        json.dumps({"mcpServers": {"custom": {"command": "npx"}}}),
        encoding="utf-8",
    )
    run = mock.Mock(
        return_value=SimpleNamespace(
            returncode=0,
            stdout=json.dumps({"ProcessId": 4242, "User": getpass.getuser()}),
            stderr="",
        )
    )
    monkeypatch.setattr(scan_service.sys, "platform", "win32")
    monkeypatch.setattr(scan_service.subprocess, "run", run)

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value=str(config_path),
                mcp_config="file",
                user=None,
                pid=4242,
            )
        ],
        configurations=[],
        clients=[claude],
    )

    assert len(parsed) == 1
    assert parsed[0].config_path == str(config_path)
    run.assert_called_once()
    assert "4242" in " ".join(run.call_args.args[0])


def test_process_override_windows_owner_lookup_failure_fails_closed(
    tmp_path, monkeypatch
):
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    config_path = tmp_path / "mcp.json"
    config_path.write_text(
        json.dumps({"mcpServers": {"custom": {"command": "npx"}}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(scan_service.sys, "platform", "win32")
    monkeypatch.setattr(
        scan_service.subprocess,
        "run",
        mock.Mock(side_effect=OSError("lookup failed")),
    )

    status = ScanCompletionStatus()
    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value=str(config_path),
                mcp_config="file",
                user=None,
                pid=4343,
            )
        ],
        configurations=[],
        clients=[claude],
        scan_status=status,
    )

    assert parsed == []
    assert status.reasons == ["runtime_owner_resolution_failed"]


def test_windows_process_owner_lookup_caps_unique_pids(monkeypatch):
    from runlayer_cli.scan import service as scan_service

    run = mock.Mock(return_value=SimpleNamespace(returncode=0, stdout="[]", stderr=""))
    monkeypatch.setattr(scan_service.subprocess, "run", run)
    refs = [
        SimpleNamespace(pid=pid, user=None)
        for pid in range(1, scan_service.MAX_OVERRIDE_OWNER_LOOKUPS + 2)
    ]

    status = ScanCompletionStatus()
    assert scan_service._resolve_windows_process_owners(refs, status) == {}

    script = run.call_args.args[0][-1]
    assert f"ProcessId = {scan_service.MAX_OVERRIDE_OWNER_LOOKUPS}" in script
    assert f"ProcessId = {scan_service.MAX_OVERRIDE_OWNER_LOOKUPS + 1}" not in script
    assert status.reasons == ["runtime_owner_resolution_capped"]


@pytest.mark.parametrize("ref_kind", ["override", "extension"])
@pytest.mark.parametrize(
    (
        "scenario",
        "user",
        "owner_sid",
        "wsl_distro",
        "windows_user_sid",
        "expected_owner",
        "expected_reasons",
    ),
    [
        (
            "effective_user",
            _effective_process_owner(),
            None,
            None,
            None,
            _effective_process_owner(),
            [],
        ),
        (
            "matching_sid",
            "SYSTEM",
            "S-1-5-21-1-2-3-1001",
            None,
            "S-1-5-21-1-2-3-1001",
            "SYSTEM",
            [],
        ),
        (
            "sid_mismatch",
            "SYSTEM",
            "S-1-5-21-1-2-3-1002",
            None,
            "S-1-5-21-1-2-3-1001",
            None,
            [],
        ),
        (
            "lookup_trusted",
            None,
            None,
            None,
            None,
            _effective_process_owner(),
            [],
        ),
        (
            "lookup_failure",
            None,
            None,
            None,
            None,
            None,
            ["runtime_owner_resolution_failed"],
        ),
        (
            "wsl",
            "alice",
            "S-1-5-21-mismatch",
            "Ubuntu",
            "S-1-5-21-1-2-3-1001",
            "alice",
            [],
        ),
    ],
)
def test_process_path_ref_owner_trust_parity(
    monkeypatch,
    ref_kind,
    scenario,
    user,
    owner_sid,
    wsl_distro,
    windows_user_sid,
    expected_owner,
    expected_reasons,
):
    from runlayer_cli.scan import service as scan_service

    ref_kwargs = {
        "client": "claude_code" if ref_kind == "override" else "vscode",
        "flag": "--mcp-config" if ref_kind == "override" else "--extensions-dir",
        "value": "/home/alice/path",
        "pid": 4242,
        "user": user,
        "wsl_distro": wsl_distro,
        "owner_sid": owner_sid,
    }
    if ref_kind == "override":
        ref = OverrideConfigRef(mcp_config="file", **ref_kwargs)
        log_event = "process_override_config_skipped_untrusted_owner"
    else:
        ref = ExtensionRootRef(**ref_kwargs)
        log_event = "process_extension_root_skipped_untrusted_owner"

    platform = (
        "win32"
        if scenario
        in {
            "matching_sid",
            "sid_mismatch",
            "lookup_trusted",
            "lookup_failure",
            "wsl",
        }
        else "darwin"
    )
    monkeypatch.setattr(scan_service.sys, "platform", platform)
    run = mock.Mock()
    if scenario == "lookup_trusted":
        run.return_value = SimpleNamespace(
            returncode=0,
            stdout=json.dumps({"ProcessId": 4242, "User": _effective_process_owner()}),
            stderr="",
        )
    elif scenario == "lookup_failure":
        run.side_effect = OSError("lookup failed")
    monkeypatch.setattr(scan_service.subprocess, "run", run)
    logger = mock.Mock()
    monkeypatch.setattr(scan_service, "logger", logger)
    status = ScanCompletionStatus()

    resolver = scan_service._TrustedOwnerResolver.for_refs(
        [ref],
        windows_user_sid=windows_user_sid,
        scan_status=status,
        untrusted_log_event=log_event,
    )

    assert resolver.resolve(ref) == expected_owner
    assert status.reasons == expected_reasons
    if expected_owner is None:
        logger.debug.assert_called_once_with(
            log_event,
            client=ref.client,
            flag=ref.flag,
            owner_status="unknown" if user is None else "mismatch",
        )
    else:
        logger.debug.assert_not_called()


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="FIFO unsupported")
def test_process_override_skips_fifo_without_opening_it(tmp_path, monkeypatch):
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    config_path = tmp_path / "mcp.json"
    os.mkfifo(config_path)
    parse = mock.Mock()
    monkeypatch.setattr(scan_service, "parse_config_file", parse)
    logger = mock.Mock()
    monkeypatch.setattr(scan_service, "logger", logger)

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value=str(config_path),
                mcp_config="file",
                user=_effective_process_owner(),
                pid=4444,
            )
        ],
        configurations=[],
        clients=[claude],
    )

    assert parsed == []
    parse.assert_not_called()
    logger.debug.assert_called_once_with(
        "process_override_config_skipped_unsafe_file",
        client="claude_code",
        flag="--mcp-config",
        file_status="not_regular",
    )
    assert str(config_path) not in repr(logger.mock_calls)


def test_process_override_parse_failure_keeps_raw_path_out_of_logs(tmp_path):
    claude = get_client_by_name("claude_code")
    assert claude is not None
    config_path = tmp_path / "mcp.json"
    config_path.write_text("{not valid json", encoding="utf-8")

    with structlog.testing.capture_logs() as logs:
        parsed = _parse_process_override_configurations(
            [
                OverrideConfigRef(
                    client="claude_code",
                    flag="--mcp-config",
                    value=str(config_path),
                    mcp_config="file",
                    user=_effective_process_owner(),
                    pid=4646,
                )
            ],
            configurations=[],
            clients=[claude],
        )

    assert parsed == []
    assert any("Failed to parse config file" in log["event"] for log in logs)
    assert all(str(config_path) not in repr(log) for log in logs)


def test_process_override_skips_oversized_file_without_reading_it(
    tmp_path, monkeypatch
):
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    config_path = tmp_path / "mcp.json"
    with config_path.open("wb") as config_file:
        config_file.truncate(scan_service.MAX_OVERRIDE_CONFIG_BYTES + 1)
    parse = mock.Mock()
    monkeypatch.setattr(scan_service, "parse_config_file", parse)
    logger = mock.Mock()
    monkeypatch.setattr(scan_service, "logger", logger)

    parsed = _parse_process_override_configurations(
        [
            OverrideConfigRef(
                client="claude_code",
                flag="--mcp-config",
                value=str(config_path),
                mcp_config="file",
                user=_effective_process_owner(),
                pid=4545,
            )
        ],
        configurations=[],
        clients=[claude],
    )

    assert parsed == []
    parse.assert_not_called()
    logger.debug.assert_called_once_with(
        "process_override_config_skipped_unsafe_file",
        client="claude_code",
        flag="--mcp-config",
        file_status="too_large",
    )
    assert str(config_path) not in repr(logger.mock_calls)


class TestScanAllClients:
    def test_propagates_project_skill_crawl_completeness(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service

        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                skill_crawl_complete=True
            ),
        )
        monkeypatch.setattr(
            scan_service,
            "detect_client_presence",
            lambda _clients, **_kwargs: [],
        )

        result = scan_all_clients(
            device_id="device",
            scan_projects=True,
            governor=mock.MagicMock(),
        )

        assert result.skill_crawl_complete is True

    def test_propagates_skill_candidate_paths(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service

        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                project_skill_candidate_paths=["/repo/.agents/skills/project"],
                global_skill_candidate_paths=["/home/u/.claude/skills/global"],
            ),
        )
        monkeypatch.setattr(
            scan_service,
            "detect_client_presence",
            lambda _clients, **_kwargs: [],
        )

        result = scan_all_clients(
            device_id="device",
            scan_projects=True,
            governor=mock.MagicMock(),
        )

        assert result.project_skill_candidate_paths == ["/repo/.agents/skills/project"]
        assert result.global_skill_candidate_paths == ["/home/u/.claude/skills/global"]

    def test_populates_effective_presence_params(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service

        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                discovered_project_paths=[Path("/host/home/alice/repo")]
            ),
        )
        monkeypatch.setattr(
            scan_service,
            "detect_client_presence",
            lambda _clients, **_kwargs: [],
        )
        monkeypatch.setattr(
            scan_service.Path,
            "home",
            classmethod(lambda _cls: Path("/host/home/alice")),
        )
        monkeypatch.setenv("RUNLAYER_STRIP_PATH_PREFIX", "/host")

        result = scan_all_clients(
            device_id="device",
            project_scan_depth=999,
            governor=mock.MagicMock(),
        )

        assert result.project_scan_depth == 20
        assert result.project_scan_home == "/home/alice"

    def test_forwards_crawled_node_modules_to_presence(self, monkeypatch, tmp_path):
        from runlayer_cli.scan import service as scan_service

        node_modules = tmp_path / "renamed-prefix" / "node_modules"
        seen: dict[str, object] = {}
        phase_kwargs: dict[str, object] = {}
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])

        def run_phases(**kwargs):
            phase_kwargs.update(kwargs)
            return scan_orchestrator.ConcurrentScanResult(
                node_modules_paths=[node_modules]
            )

        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            run_phases,
        )

        def detect(clients, **kwargs):
            seen["clients"] = clients
            seen.update(kwargs)
            return []

        monkeypatch.setattr(scan_service, "detect_client_presence", detect)

        scan_all_clients(
            device_id="device",
            scan_projects=False,
            governor=mock.MagicMock(),
        )

        assert seen["node_modules_paths"] == [node_modules]
        assert "home" not in seen
        assert "environment" not in seen
        assert "windows_user_sid" not in seen
        assert "include_current_user_registry" not in seen
        assert phase_kwargs["machine_scope"] is True

    def test_forwards_disabled_machine_scope_to_extension_phase(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service

        phase_kwargs: dict[str, object] = {}
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])

        def run_phases(**kwargs):
            phase_kwargs.update(kwargs)
            return scan_orchestrator.ConcurrentScanResult()

        monkeypatch.setattr(scan_service, "run_concurrent_scan_phases", run_phases)
        monkeypatch.setattr(
            scan_service, "detect_client_presence", lambda *_a, **_k: []
        )

        scan_all_clients(
            device_id="device",
            scan_projects=False,
            machine_scope=False,
            governor=mock.MagicMock(),
        )

        assert phase_kwargs["machine_scope"] is False

    def test_launcher_truncation_marks_client_discovery_incomplete(
        self,
        monkeypatch,
    ):
        from runlayer_cli.scan import service as scan_service

        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(),
        )

        def detect(_clients, **kwargs):
            kwargs["scan_status"].complete = False
            return []

        monkeypatch.setattr(scan_service, "detect_client_presence", detect)

        result = scan_all_clients(
            device_id="device",
            scan_projects=False,
            governor=mock.MagicMock(),
        )

        assert result.client_discovery_complete is False

    @pytest.mark.parametrize(
        ("system_profile", "include_current_user_registry"),
        [(False, True), (True, False)],
    )
    def test_windows_sid_forwards_explicit_profile_context_to_presence(
        self,
        monkeypatch,
        tmp_path,
        system_profile: bool,
        include_current_user_registry: bool,
    ):
        from runlayer_cli.scan import service as scan_service

        profile_home = tmp_path / "Users" / "alice"
        sid = "S-1-5-21-1-2-3-1001"
        monkeypatch.setenv("USERPROFILE", str(profile_home))
        monkeypatch.setenv(
            "APPDATA",
            str(profile_home / "AppData" / "Roaming"),
        )
        monkeypatch.setenv(
            "LOCALAPPDATA",
            str(profile_home / "AppData" / "Local"),
        )
        monkeypatch.setattr(
            scan_service.Path,
            "home",
            classmethod(lambda cls: profile_home),
        )
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(),
        )
        seen: dict[str, object] = {}

        def detect(_clients, **kwargs):
            seen.update(kwargs)
            return []

        monkeypatch.setattr(scan_service, "detect_client_presence", detect)

        scan_all_clients(
            device_id="device",
            scan_projects=False,
            windows_user_sid=sid,
            windows_system_profile=system_profile,
            governor=mock.MagicMock(),
        )

        assert seen["home"] == profile_home
        assert seen["environment"] is scan_service.os.environ
        assert seen["windows_user_sid"] == sid
        assert seen["windows_system_profile"] is system_profile
        assert seen["include_current_user_registry"] is include_current_user_registry

    def test_shared_mcp_json_not_attributed_to_copilot_without_presence(
        self, monkeypatch
    ):
        from runlayer_cli.scan import service as scan_service
        from runlayer_cli.scan.clients import get_client_by_name

        claude = get_client_by_name("claude_code")
        copilot = get_client_by_name("github_copilot_cli")
        assert claude is not None
        assert copilot is not None

        config_path = "/workspace/project/.mcp.json"
        configurations = [
            MCPClientConfig(
                client=client.name,
                config_path=config_path,
                project_path="/workspace/project",
                config_scope="project",
                servers=[MCPServerConfig(name="shared", type="stdio")],
            )
            for client in (claude, copilot)
        ]
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [claude, copilot])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                configurations=configurations
            ),
        )
        monkeypatch.setattr(
            scan_service, "detect_client_presence", lambda _clients, **_kwargs: []
        )

        result = scan_all_clients(
            device_id="device",
            scan_projects=False,
            governor=mock.MagicMock(),
        )

        assert [config.client for config in result.configurations] == ["claude_code"]
        assert [client.client for client in result.detected_clients] == ["claude_code"]

    def test_shared_mcp_json_in_container_not_attributed_to_copilot_without_presence(
        self, monkeypatch
    ):
        from runlayer_cli.scan import service as scan_service
        from runlayer_cli.scan.clients import get_client_by_name

        claude = get_client_by_name("claude_code")
        copilot = get_client_by_name("github_copilot_cli")
        assert claude is not None
        assert copilot is not None

        config_path = "/workspace/project/.mcp.json"
        configurations = [
            MCPClientConfig(
                client=client.name,
                config_path=config_path,
                project_path="/workspace/project",
                config_scope="container",
                container_id="container-1",
                servers=[MCPServerConfig(name="shared", type="stdio")],
            )
            for client in (claude, copilot)
        ]
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [claude, copilot])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                configurations=configurations
            ),
        )
        monkeypatch.setattr(
            scan_service, "detect_client_presence", lambda _clients, **_kwargs: []
        )

        result = scan_all_clients(
            device_id="device",
            scan_projects=False,
            governor=mock.MagicMock(),
        )

        assert [config.client for config in result.configurations] == ["claude_code"]
        assert [client.client for client in result.detected_clients] == ["claude_code"]

    def test_container_presence_gates_colocated_container_config(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service
        from runlayer_cli.scan.clients import get_client_by_name
        from runlayer_cli.scan.containers import ContainerScanResult

        copilot = get_client_by_name("github_copilot_cli")
        assert copilot is not None
        configuration = MCPClientConfig(
            client=copilot.name,
            config_path="/workspace/project/.mcp.json",
            project_path="/workspace/project",
            config_scope="container",
            container_id="container-1",
            servers=[MCPServerConfig(name="shared", type="stdio")],
        )
        installed = DetectedClient(
            client=copilot.name,
            display_name=copilot.display_name,
            detected_via=["container"],
            config_paths=[
                "container:devbox:/usr/local/lib/node_modules/"
                "@github/copilot/package.json"
            ],
            container_ids=["container-1"],
        )
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [copilot])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(),
        )
        monkeypatch.setattr(
            scan_service,
            "detect_client_presence",
            lambda _clients, **_kwargs: [],
        )
        monkeypatch.setattr(
            scan_service,
            "scan_running_containers",
            lambda **_kwargs: ContainerScanResult(
                configurations=[configuration],
                detected_clients=[installed],
                scan_succeeded=True,
            ),
        )

        result = scan_all_clients(
            device_id="device",
            detect_containers=True,
            scan_projects=False,
            governor=mock.MagicMock(),
        )

        assert result.configurations == [configuration]
        assert result.detected_clients[0].detected_via == ["container", "server"]
        assert result.container_scan_requested is True
        assert result.container_scan_error is None

    def test_shared_mcp_json_attributed_to_copilot_when_present(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service
        from runlayer_cli.scan.clients import get_client_by_name

        copilot = get_client_by_name("github_copilot_cli")
        assert copilot is not None

        configuration = MCPClientConfig(
            client=copilot.name,
            config_path="/workspace/project/.mcp.json",
            project_path="/workspace/project",
            config_scope="project",
            servers=[MCPServerConfig(name="shared", type="stdio")],
        )
        installed = DetectedClient(
            client=copilot.name,
            display_name=copilot.display_name,
            detected_via=["cli"],
        )
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [copilot])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                configurations=[configuration]
            ),
        )
        monkeypatch.setattr(
            scan_service,
            "detect_client_presence",
            lambda _clients, **_kwargs: [installed],
        )

        result = scan_all_clients(
            device_id="device",
            scan_projects=False,
            governor=mock.MagicMock(),
        )

        assert result.configurations == [configuration]
        assert result.detected_clients[0].detected_via == ["cli", "config", "server"]

    def test_copilot_specific_project_config_is_presence_evidence(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service
        from runlayer_cli.scan.clients import get_client_by_name

        copilot = get_client_by_name("github_copilot_cli")
        assert copilot is not None

        configuration = MCPClientConfig(
            client=copilot.name,
            config_path="/workspace/project/.github/mcp.json",
            project_path="/workspace/project",
            config_scope="project",
            servers=[MCPServerConfig(name="shared", type="stdio")],
        )
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [copilot])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                configurations=[configuration]
            ),
        )
        monkeypatch.setattr(
            scan_service, "detect_client_presence", lambda _clients, **_kwargs: []
        )

        result = scan_all_clients(
            device_id="device",
            scan_projects=False,
            governor=mock.MagicMock(),
        )

        assert result.configurations == [configuration]
        assert result.detected_clients[0].detected_via == ["config", "server"]

    def test_returns_scan_result(self):
        """Returns ScanResult dataclass."""
        result = scan_all_clients(scan_projects=False)  # Skip project scan for speed
        assert isinstance(result, ScanResult)
        assert result.device_id is not None
        assert result.configurations is not None
        assert result.project_skill_candidate_paths == []
        assert isinstance(result.global_skill_candidate_paths, list)
        assert result.skill_crawl_complete is False

    def test_sequential_scans_clear_in_process_callbacks_and_wsl_cache(
        self,
        monkeypatch,
    ):
        from runlayer_cli.scan import plugin_scanner
        from runlayer_cli.scan import service as scan_service

        sentinel = object()
        seen_callbacks = []

        def fake_impl(_governor, **_kwargs):
            seen_callbacks.append(plugin_scanner._scan_checkpoint)
            plugin_scanner._scan_checkpoint = lambda: None
            return sentinel

        cache_clear = mock.Mock()
        monkeypatch.setattr(plugin_scanner, "_scan_checkpoint", None)
        monkeypatch.setattr(scan_service, "_scan_all_clients_impl", fake_impl)
        monkeypatch.setattr(
            scan_service.get_wsl_distro_inventory,
            "cache_clear",
            cache_clear,
        )
        governor = mock.MagicMock()

        assert scan_all_clients(governor=governor) is sentinel
        assert scan_all_clients(governor=governor) is sentinel

        assert seen_callbacks == [None, None]
        assert cache_clear.call_count == 2

    def test_includes_device_metadata(self):
        """Result includes device metadata."""
        result = scan_all_clients(scan_projects=False)
        assert result.hostname is not None
        assert result.os is not None

    def test_custom_device_id_used(self):
        """Custom device ID overrides auto-generated."""
        result = scan_all_clients(device_id="custom-id", scan_projects=False)
        assert result.device_id == "custom-id"

    def test_scan_duration_recorded(self):
        """Scan duration is recorded in milliseconds."""
        result = scan_all_clients(scan_projects=False)
        assert result.scan_duration_ms >= 0
        assert {
            "phase_01_global_configurations",
            "phase_02_project_crawl",
            "phase_03_claude_code_plugins",
            "phase_04_cursor_plugins",
            "phase_05_codex_plugins",
            "phase_06_opencode_plugins",
            "phase_07_gemini_extensions",
            "phase_08_copilot_plugins",
            "phase_09_global_skills",
            "phase_09b_disguised_skills",
            "phase_10_plugin_artifacts",
            "phase_11_install_agents",
            "phase_11_static_agents",
            "phase_12_runtime_processes",
            "phase_13_running_containers",
            "phase_13b_wsl_projects",
        }.issubset(result.phase_durations_ms)
        assert "phase_11_agent_detection" not in result.phase_durations_ms

    def test_scan_duration_uses_monotonic_clock(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service

        monotonic_values = iter([10.0, 10.25])
        monkeypatch.setattr(
            scan_service,
            "time",
            SimpleNamespace(
                monotonic=lambda: next(monotonic_values),
                time=lambda: (_ for _ in ()).throw(AssertionError("wall clock used")),
            ),
        )

        result = scan_all_clients(scan_projects=False)

        assert result.scan_duration_ms == 250

    def test_collector_version_recorded(self):
        """Collector version is recorded."""
        result = scan_all_clients(collector_version="1.2.3", scan_projects=False)
        assert result.collector_version == "1.2.3"

    def test_tools_included_in_api_payload(self):
        """Runlayer tool versions are included in scan submissions."""
        result = scan_all_clients(collector_version="1.2.3", scan_projects=False)
        payload = result.to_api_payload()
        assert {"name": "scan-collector", "version": "1.2.3"} in payload["tools"]

    def test_org_device_id_passed_through(self):
        """Organization device ID is passed through."""
        result = scan_all_clients(org_device_id="mdm-asset-123", scan_projects=False)
        assert result.org_device_id == "mdm-asset-123"

    def test_windows_user_sid_passed_through_every_payload(self):
        sid = "S-1-5-21-1-2-3-1001"
        result = scan_all_clients(
            windows_user_sid=sid,
            scan_projects=False,
        )

        assert result.windows_user_sid == sid
        assert result.to_api_payload()["windows_user_sid"] == sid
        assert result.to_agent_report_payload()["windows_user_sid"] == sid
        assert result.to_agent_definition_report_payload()["windows_user_sid"] == sid
        assert (
            _scan_manifest_payload(
                result,
                ScanSubmissionResult(),
            )["windows_user_sid"]
            == sid
        )

    def test_username_override(self):
        """Explicit username_override replaces auto-detected username."""
        result = scan_all_clients(username_override="awfrazer", scan_projects=False)
        assert result.username == "awfrazer"

    def test_username_override_none_uses_autodetect(self):
        """Without username_override, auto-detected username is used."""
        result = scan_all_clients(scan_projects=False)
        assert result.username is not None

    @mock.patch("runlayer_cli.scan.service.get_all_clients")
    @mock.patch("runlayer_cli.scan.orchestrator.get_clients_with_project_configs")
    @mock.patch("runlayer_cli.scan.orchestrator.get_client_by_name", return_value=None)
    def test_scans_all_enabled_clients(
        self,
        mock_get_by_name,
        mock_get_project_clients,
        mock_get_clients,
        tmp_path,
    ):
        """Scans all enabled clients."""
        from runlayer_cli.scan.clients import ConfigPath, MCPClientDefinition

        # Create a test config file
        config_file = tmp_path / "test_config.json"
        config_file.write_text(
            json.dumps({"mcpServers": {"test-server": {"command": "npx"}}})
        )

        mock_get_clients.return_value = [
            MCPClientDefinition(
                name="test_client",
                display_name="Test Client",
                paths=[ConfigPath(str(config_file), platform="all")],
                servers_key="mcpServers",
            )
        ]
        mock_get_project_clients.return_value = []  # No project configs

        result = scan_all_clients(scan_projects=False)
        configs = [c for c in result.configurations if c.client == "test_client"]
        assert len(configs) == 1

    @mock.patch("runlayer_cli.scan.service.discover_processes")
    def test_detect_processes_off_by_default(self, mock_discover):
        """PHASE 12 is opt-in: a default scan never polls the process table."""
        result = scan_all_clients(scan_projects=False)
        mock_discover.assert_not_called()
        assert result.processes == []

    @mock.patch("runlayer_cli.scan.service.discover_processes")
    def test_detect_processes_populates_result(self, mock_discover, tmp_path):
        """With the flag on, discovered processes are threaded into the result."""
        override_path = tmp_path / "mcp.json"
        override_path.write_text(
            json.dumps({"mcpServers": {"override": {"command": "npx"}}}),
            encoding="utf-8",
        )
        proc = DiscoveredProcess(
            pid=999,
            ppid=1,
            kind="mcp_server",
            discovery_source="listening_port",
            matched_client=None,
            exe="/usr/local/bin/node",
            argv_redacted=["node"],
            command_hash="h",
            config_hash=None,
            agent_framework_id=None,
            agent_fingerprint=None,
            agent_root_path=None,
            listening_ports=[3000],
            bind_scope="loopback",
            transport="http",
            ai_signals=["config_port_match:3000"],
            confidence=0.8,
            user=None,
            started_at=None,
            cwd_project=None,
        )
        mock_discover.return_value = ProcessDiscoveryResult(
            processes=[proc],
            override_config_refs=[
                OverrideConfigRef(
                    client="claude_code",
                    flag="--mcp-config",
                    value=str(override_path),
                    mcp_config="file",
                    pid=999,
                    user=_effective_process_owner(),
                    owner_sid="S-1-5-21-1-2-3-1001",
                )
            ],
        )
        result = scan_all_clients(
            detect_processes=True,
            scan_projects=False,
            windows_user_sid="S-1-5-21-1-2-3-1001",
        )
        mock_discover.assert_called_once()
        assert callable(mock_discover.call_args.kwargs["checkpoint"])
        assert (
            mock_discover.call_args.kwargs["windows_user_sid"] == "S-1-5-21-1-2-3-1001"
        )
        assert result.processes == [proc]
        assert result.total_processes == 1
        [override_config] = [
            config
            for config in result.configurations
            if config.config_scope == "process_override"
        ]
        assert override_config.config_path == str(override_path)
        assert override_config.servers[0].name == "override"

    @mock.patch("runlayer_cli.scan.service.discover_processes")
    def test_detect_processes_scans_extension_dir_override(
        self,
        mock_discover,
        tmp_path,
    ):
        extension_dir = tmp_path / "custom-extensions" / "vendor.ai-1.0.0"
        extension_dir.mkdir(parents=True)
        (extension_dir / "package.json").write_text(
            json.dumps(
                {
                    "publisher": "Vendor",
                    "name": "ai",
                    "version": "1.0.0",
                }
            ),
            encoding="utf-8",
        )
        mock_discover.return_value = ProcessDiscoveryResult(
            extension_root_refs=[
                ExtensionRootRef(
                    client="vscode",
                    flag="--extensions-dir",
                    value=str(extension_dir.parent),
                    pid=999,
                    user=_effective_process_owner(),
                )
            ]
        )

        result = scan_all_clients(detect_processes=True, scan_projects=False)

        override_plugins = [
            plugin
            for plugin in result.plugins
            if plugin.install_path == str(extension_dir)
        ]
        assert len(override_plugins) == 1
        assert override_plugins[0].client == "vscode"

    @mock.patch(
        "runlayer_cli.scan.service.discover_processes",
        return_value=ProcessDiscoveryResult(),
    )
    def test_no_detect_agents_disables_runtime_agent_channel(self, mock_discover):
        scan_all_clients(
            detect_agents=False,
            detect_processes=True,
            scan_projects=False,
        )

        assert mock_discover.call_args.kwargs["detect_agents"] is False

    @mock.patch("runlayer_cli.scan.service.scan_running_containers")
    def test_detect_containers_off_by_default(self, mock_scan_containers):
        """PHASE 13 does not touch Docker unless explicitly enabled."""
        result = scan_all_clients(scan_projects=False)
        mock_scan_containers.assert_not_called()
        assert result.containers == []
        assert result.container_scan_requested is False
        assert result.container_scan_error is None

    @mock.patch("runlayer_cli.scan.service.scan_running_containers")
    def test_failed_container_scan_reason_reaches_scan_result(
        self, mock_scan_containers
    ):
        from runlayer_cli.scan.containers import (
            CONTAINER_SCAN_UNAVAILABLE_REASON,
            ContainerScanResult,
        )

        mock_scan_containers.return_value = ContainerScanResult(
            failure_reason=CONTAINER_SCAN_UNAVAILABLE_REASON,
        )

        result = scan_all_clients(
            detect_containers=True,
            scan_projects=False,
        )

        assert result.container_scan_requested is True
        assert result.containers_scanned is False
        assert result.container_scan_error == CONTAINER_SCAN_UNAVAILABLE_REASON

    def test_disguised_skill_switch_reaches_concurrent_orchestrator(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service

        run_concurrent = mock.Mock(
            return_value=scan_orchestrator.ConcurrentScanResult()
        )
        monkeypatch.setattr(
            scan_service,
            "get_device_metadata",
            lambda: {
                "hostname": "mac",
                "os": "macos",
                "os_version": "15",
                "username": "alice",
                "serial_number": None,
            },
        )
        monkeypatch.setattr(scan_service, "get_installed_tools", lambda: [])
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(scan_service, "run_concurrent_scan_phases", run_concurrent)
        monkeypatch.setattr(
            scan_service, "detect_client_presence", lambda _clients, **_kwargs: []
        )

        scan_all_clients(
            device_id="device",
            scan_projects=False,
            detect_disguised_skills=True,
            governor=mock.MagicMock(),
        )

        assert run_concurrent.call_args.kwargs["detect_disguised_skills"] is True

    def test_renamed_plugin_cache_switch_reaches_concurrent_orchestrator(
        self, monkeypatch
    ):
        from runlayer_cli.scan import service as scan_service

        run_concurrent = mock.Mock(
            return_value=scan_orchestrator.ConcurrentScanResult()
        )
        monkeypatch.setattr(
            scan_service,
            "get_device_metadata",
            lambda: {
                "hostname": "mac",
                "os": "macos",
                "os_version": "15",
                "username": "alice",
                "serial_number": None,
            },
        )
        monkeypatch.setattr(scan_service, "get_installed_tools", lambda: [])
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(scan_service, "run_concurrent_scan_phases", run_concurrent)
        monkeypatch.setattr(
            scan_service, "detect_client_presence", lambda _clients, **_kwargs: []
        )

        scan_all_clients(
            device_id="device",
            scan_projects=False,
            detect_renamed_plugin_caches=True,
            governor=mock.MagicMock(),
        )

        assert run_concurrent.call_args.kwargs["detect_renamed_plugin_caches"] is True

    def test_rejected_agent_candidates_do_not_consume_wire_cap(
        self,
        monkeypatch,
    ):
        from runlayer_cli.scan import service as scan_service

        rejected_agents = [
            SimpleNamespace(is_agent=False) for _ in range(MAX_AGENTS + 1)
        ]
        monkeypatch.setattr(
            scan_service,
            "get_device_metadata",
            lambda: {
                "hostname": "mac",
                "os": "macos",
                "os_version": "15",
                "username": "alice",
                "serial_number": None,
            },
        )
        monkeypatch.setattr(scan_service, "get_installed_tools", lambda: [])
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                agents=rejected_agents
            ),
        )
        monkeypatch.setattr(
            scan_service,
            "detect_client_presence",
            lambda _clients, **_kwargs: [],
        )

        result = scan_all_clients(
            device_id="device",
            governor=mock.MagicMock(),
        )

        assert result.agent_discovery_complete is True
        assert result.completeness.agent_host_static.complete is True

    def test_windows_inventory_runs_without_container_detection(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service
        from runlayer_cli.scan.device import (
            DiscoveredWSLDistro,
            WSLDistroInventory,
        )

        inventory = WSLDistroInventory(
            distros=(
                DiscoveredWSLDistro(
                    name="Ubuntu",
                    wsl_version=2,
                    is_running=True,
                ),
            ),
            success=True,
        )
        inventory_mock = mock.Mock(return_value=inventory)
        monkeypatch.setattr(scan_service, "get_wsl_distro_inventory", inventory_mock)
        monkeypatch.setattr(
            scan_service,
            "scan_wsl_runtime_file_signals",
            lambda distros, **_kwargs: list(distros),
        )
        monkeypatch.setattr(
            scan_service,
            "get_device_metadata",
            lambda: {
                "hostname": "windows-host",
                "os": "windows",
                "os_version": "11",
                "username": "alice",
                "serial_number": None,
            },
        )
        monkeypatch.setattr(scan_service, "get_installed_tools", lambda: [])
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(),
        )
        monkeypatch.setattr(
            scan_service, "detect_client_presence", lambda _clients, **_kwargs: []
        )
        governor = mock.MagicMock()

        result = scan_all_clients(
            device_id="device",
            scan_projects=False,
            detect_containers=False,
            governor=governor,
        )

        inventory_mock.assert_called_once_with()
        assert result.wsl_scanned is True
        assert result.wsl_distros == list(inventory.distros)
        assert result.to_api_payload()["wsl_distros"] == [
            {
                "distro_name": "Ubuntu",
                "wsl_version": 2,
                "is_running": True,
                "scanned": False,
                "container_runtimes": [],
            }
        ]

    def test_failed_wsl_inventory_suppresses_wsl_attribution(self, monkeypatch):
        """A withheld inventory must also withhold WSL-scoped attribution.

        Rows parsed before a malformed one stay local-only, so nothing on the
        wire corroborates them. Shipping ``config_scope="wsl"`` against that
        inventory would force the backend to synthesize distro rows with a
        guessed running state.
        """
        from runlayer_cli.scan.agent_definition_scanner import (
            DiscoveredAgentDefinition,
        )
        from runlayer_cli.scan.containers import ContainerScanResult
        from runlayer_cli.scan.skill_scanner import (
            ARTIFACT_SKILL_MD,
            DiscoveredSkillArtifact,
        )
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        config = MCPClientConfig(
            client="cursor",
            config_path=r"\\wsl.localhost\Ubuntu\home\dev\repo\.cursor\mcp.json",
            project_path=r"\\wsl.localhost\Ubuntu\home\dev\repo",
            config_scope="project",
            servers=[MCPServerConfig(name="github", type="stdio")],
        )
        skill = DiscoveredSkillArtifact(
            name="deploy",
            path=r"\\wsl.localhost\Ubuntu\home\dev\.claude\skills\deploy",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="global",
            tool="claude_code",
        )
        definition = DiscoveredAgentDefinition(
            client="cursor",
            name="reviewer",
            description=None,
            scope="project",
            path=r"\\wsl.localhost\Ubuntu\home\dev\repo\.cursor\agents\review.md",
            project_path=r"\\wsl.localhost\Ubuntu\home\dev\repo",
            content_hash="a" * 64,
        )

        result = self._scan_windows_host(
            monkeypatch,
            inventory=_wsl_inventory(("Ubuntu",), success=False),
            wsl_project_result=WSLProjectScanResult(
                configurations=[config],
                skills=[skill],
                agent_definitions=[definition],
            ),
            container_result=ContainerScanResult(),
        )

        payload = result.to_api_payload()
        assert result.wsl_scanned is False
        assert "wsl_distros" not in payload
        assert config.config_scope == "project"
        assert config.wsl_distro is None
        assert "wsl" not in payload["configurations"][0]
        assert "wsl" not in skill.to_api_payload()
        assert "wsl" not in result.agent_definitions[0].to_api_payload()

    def test_successful_wsl_inventory_attributes_artifacts(self, monkeypatch):
        from runlayer_cli.scan.containers import ContainerScanResult
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        config = MCPClientConfig(
            client="cursor",
            config_path=r"\\wsl.localhost\Ubuntu\home\dev\repo\.cursor\mcp.json",
            project_path=r"\\wsl.localhost\Ubuntu\home\dev\repo",
            config_scope="project",
            servers=[MCPServerConfig(name="github", type="stdio")],
        )

        result = self._scan_windows_host(
            monkeypatch,
            inventory=_wsl_inventory(("Ubuntu",), success=True),
            wsl_project_result=WSLProjectScanResult(configurations=[config]),
            container_result=ContainerScanResult(),
        )

        payload = result.to_api_payload()
        assert payload["wsl_distros"] == [
            {
                "distro_name": "Ubuntu",
                "wsl_version": 2,
                "is_running": True,
                "scanned": False,
                "container_runtimes": [],
            }
        ]
        assert config.config_scope == "wsl"
        assert config.config_path == "/home/dev/repo/.cursor/mcp.json"
        assert payload["configurations"][0]["wsl"] == {
            "distro": "Ubuntu",
            "user": "dev",
        }

    def test_wsl_process_scan_failure_keeps_file_signal_results(self, monkeypatch):
        """A failed in-VM ps must not drop Phase 0 UNC file-signal results.

        The backend persists ``last_scanned_at`` / ``container_runtimes`` only
        when ``scanned`` is true, and process coverage has no wire channel of
        its own — clearing ``scanned`` here silently discards the successful
        file probes (which persist fine with DetectProcesses off).
        """
        from runlayer_cli.scan.containers import ContainerScanResult
        from runlayer_cli.scan.device import DiscoveredWSLDistro, WSLDistroInventory
        from runlayer_cli.scan.processes import ProcessDiscoveryResult
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        inventory = WSLDistroInventory(
            distros=(
                DiscoveredWSLDistro(
                    name="Ubuntu",
                    wsl_version=2,
                    is_running=True,
                    scanned=True,
                    container_runtimes=("docker",),
                ),
            ),
            success=True,
        )

        result = self._scan_windows_host(
            monkeypatch,
            inventory=inventory,
            wsl_project_result=WSLProjectScanResult(),
            container_result=ContainerScanResult(),
            # In-VM ps failed for every distro: no completed process scans.
            discover_processes=lambda **_kwargs: ProcessDiscoveryResult(),
        )

        assert result.to_api_payload()["wsl_distros"] == [
            {
                "distro_name": "Ubuntu",
                "wsl_version": 2,
                "is_running": True,
                "scanned": True,
                "container_runtimes": ["docker"],
            }
        ]

    def test_wsl_config_is_attributed_before_process_classification(self, monkeypatch):
        from runlayer_cli.scan.containers import ContainerScanResult
        from runlayer_cli.scan.processes import ProcessDiscoveryResult
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        config = MCPClientConfig(
            client="cursor",
            config_path=r"\\wsl.localhost\Ubuntu\home\dev\.cursor\mcp.json",
            config_scope="global",
            servers=[MCPServerConfig(name="github", type="stdio")],
        )
        observed_contexts = []

        def capture_process_context(*, configurations, **_kwargs):
            observed_contexts.extend(
                (
                    candidate.config_scope,
                    candidate.wsl_distro,
                    candidate.config_path,
                )
                for candidate in configurations
            )
            return ProcessDiscoveryResult()

        self._scan_windows_host(
            monkeypatch,
            inventory=_wsl_inventory(("Ubuntu",), success=True),
            wsl_project_result=WSLProjectScanResult(),
            container_result=ContainerScanResult(),
            concurrent_result=scan_orchestrator.ConcurrentScanResult(
                configurations=[config]
            ),
            discover_processes=capture_process_context,
        )

        assert observed_contexts == [("wsl", "Ubuntu", "/home/dev/.cursor/mcp.json")]

    def _scan_windows_host(
        self,
        monkeypatch,
        *,
        inventory,
        wsl_project_result,
        container_result,
        wsl_container_result=None,
        concurrent_result=None,
        discover_processes=None,
    ):
        """Run a scan as a Windows host with a stubbed WSL project walk."""
        from runlayer_cli.scan import service as scan_service

        monkeypatch.setattr(scan_service, "get_wsl_distro_inventory", lambda: inventory)
        monkeypatch.setattr(
            scan_service,
            "get_device_metadata",
            lambda: {
                "hostname": "windows-host",
                "os": "windows",
                "os_version": "11",
                "username": "alice",
                "serial_number": None,
            },
        )
        monkeypatch.setattr(scan_service, "get_installed_tools", lambda: [])
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: (
                concurrent_result
                if concurrent_result is not None
                else scan_orchestrator.ConcurrentScanResult()
            ),
        )
        if discover_processes is not None:
            monkeypatch.setattr(
                scan_service,
                "discover_processes",
                discover_processes,
            )
        monkeypatch.setattr(
            scan_service,
            "scan_wsl_runtime_file_signals",
            lambda distros, **_kwargs: list(distros),
        )
        monkeypatch.setattr(
            scan_service,
            "detect_client_presence",
            lambda _clients, **_kwargs: [],
        )
        monkeypatch.setattr(
            scan_service, "scan_running_containers", lambda **_kwargs: container_result
        )
        wsl_container_scan = mock.Mock(
            return_value=(
                wsl_container_result
                if wsl_container_result is not None
                else SimpleNamespace(
                    containers=[],
                    scanned_distros=[],
                )
            )
        )
        monkeypatch.setattr(scan_service, "scan_wsl_containers", wsl_container_scan)
        monkeypatch.setattr(
            scan_service, "scan_wsl_projects", lambda **_kwargs: wsl_project_result
        )
        governor = mock.MagicMock()
        result = scan_all_clients(
            device_id="device",
            scan_projects=False,
            detect_containers=True,
            detect_processes=discover_processes is not None,
            governor=governor,
        )
        if inventory.success and inventory.distros:
            assert (
                wsl_container_scan.call_args.kwargs["checkpoint"] is governor.checkpoint
            )
        return result

    def test_host_container_inventory_suppresses_duplicate_wsl_rows(self, monkeypatch):
        from runlayer_cli.scan.containers import (
            ContainerScanResult,
            DiscoveredContainer,
        )
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        host_running = DiscoveredContainer(
            container_id="running-cid",
            name="host-running",
            image_ref="example/running:latest",
            image_digest=None,
        )
        host_stopped = DiscoveredContainer(
            container_id="stopped-cid",
            name="host-stopped",
            image_ref="example/stopped:latest",
            image_digest=None,
            is_running=False,
        )
        unique_wsl = DiscoveredContainer(
            container_id="wsl-only-cid",
            name="wsl-only",
            image_ref="example/wsl:latest",
            image_digest=None,
            wsl_distro="Ubuntu",
        )
        result = self._scan_windows_host(
            monkeypatch,
            inventory=_wsl_inventory(("Ubuntu",), success=True),
            wsl_project_result=WSLProjectScanResult(),
            container_result=ContainerScanResult(
                containers=[host_running],
                stopped_containers=[host_stopped],
                scan_succeeded=True,
                stopped_containers_succeeded=True,
            ),
            wsl_container_result=SimpleNamespace(
                containers=[
                    DiscoveredContainer(
                        container_id=host_running.container_id,
                        name="wsl-running-duplicate",
                        image_ref=host_running.image_ref,
                        image_digest=None,
                        wsl_distro="Ubuntu",
                    ),
                    DiscoveredContainer(
                        container_id=host_stopped.container_id,
                        name="wsl-stopped-duplicate",
                        image_ref=host_stopped.image_ref,
                        image_digest=None,
                        wsl_distro="Ubuntu",
                    ),
                    unique_wsl,
                ],
                scanned_distros=["Ubuntu"],
            ),
        )

        assert result.containers == [host_running, unique_wsl]
        assert result.stopped_containers == [host_stopped]
        assert result.wsl_container_scanned_distros == ["Ubuntu"]

    def test_incomplete_wsl_container_inventory_blocks_container_authority(
        self,
        monkeypatch,
    ):
        from runlayer_cli.scan.containers import ContainerScanResult
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        reason = "wsl_container_scan_capped"
        result = self._scan_windows_host(
            monkeypatch,
            inventory=_wsl_inventory(("Ubuntu", "Debian"), success=True),
            wsl_project_result=WSLProjectScanResult(),
            container_result=ContainerScanResult(
                scan_succeeded=True,
                artifact_scan_succeeded=True,
            ),
            wsl_container_result=SimpleNamespace(
                containers=[],
                scanned_distros=["Ubuntu"],
                complete=False,
                incomplete_reasons=[reason],
            ),
        )

        payload = _scan_manifest_payload(result, ScanSubmissionResult())
        container_entries = [
            entry for entry in payload["entries"] if entry["surface"] == "container"
        ]
        assert {entry["category"] for entry in container_entries} == {
            "mcp",
            "client",
            "skill",
            "plugin",
            "agent_definition",
        }
        assert all(entry["complete"] is False for entry in container_entries)
        assert {entry["reason"] for entry in container_entries} == {reason}
        assert result.completeness.client_presence.complete is True

    def test_incomplete_wsl_results_without_reasons_block_authority(
        self,
        monkeypatch,
    ):
        from runlayer_cli.scan.containers import ContainerScanResult
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        result = self._scan_windows_host(
            monkeypatch,
            inventory=_wsl_inventory(("Ubuntu",), success=True),
            wsl_project_result=WSLProjectScanResult(complete=False),
            container_result=ContainerScanResult(
                scan_succeeded=True,
                artifact_scan_succeeded=True,
            ),
            wsl_container_result=SimpleNamespace(
                containers=[],
                scanned_distros=[],
                complete=False,
                incomplete_reasons=[],
            ),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(result, ScanSubmissionResult())[
                "entries"
            ]
        }
        assert entries[("mcp", "container")]["reason"] == (
            "wsl_container_inventory_incomplete"
        )
        assert entries[("mcp", "wsl")]["reason"] == "wsl_project_scan_failed"

    def test_failed_wsl_inventory_blocks_container_authority(
        self,
        monkeypatch,
    ):
        from runlayer_cli.scan.containers import ContainerScanResult
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        result = self._scan_windows_host(
            monkeypatch,
            inventory=_wsl_inventory(("Ubuntu",), success=False),
            wsl_project_result=WSLProjectScanResult(),
            container_result=ContainerScanResult(
                scan_succeeded=True,
                artifact_scan_succeeded=True,
            ),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(result, ScanSubmissionResult())[
                "entries"
            ]
        }

        assert entries[("mcp", "container")] == {
            "category": "mcp",
            "surface": "container",
            "complete": False,
            "reason": "wsl_inventory_incomplete",
        }

    @mock.patch("runlayer_cli.scan.service.scan_running_containers")
    def test_detect_containers_populates_configs_and_inventory(
        self, mock_scan_containers
    ):
        """PHASE 13 merges container configs and preserves inventory."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig
        from runlayer_cli.scan.agent_definition_scanner import (
            DiscoveredAgentDefinition,
        )
        from runlayer_cli.scan.containers import (
            ContainerScanResult,
            DiscoveredContainer,
            DiscoveredContainerImage,
        )
        from runlayer_cli.scan.client_presence import DetectedClient
        from runlayer_cli.scan.plugin_scanner import DiscoveredPluginArtifact
        from runlayer_cli.scan.skill_scanner import (
            ARTIFACT_SKILL_MD,
            DiscoveredSkillArtifact,
            SkillFile,
        )

        container = DiscoveredContainer(
            container_id="cid",
            name="devbox",
            image_ref="devbox:latest",
            image_digest=None,
        )
        stopped_container = DiscoveredContainer(
            container_id="stopped-cid",
            name="old-devbox",
            image_ref="devbox:old",
            image_digest="sha256:old",
            is_running=False,
        )
        container_image = DiscoveredContainerImage(
            repository="ghcr.io/example/mcp",
            tag="latest",
            digest="sha256:image",
        )
        config = MCPClientConfig(
            client="cursor",
            config_scope="container",
            container_id="cid",
            servers=[MCPServerConfig(name="github", type="stdio")],
        )
        skill = DiscoveredSkillArtifact(
            name="deploy",
            path="/workspace/.agents/skills/deploy",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="skill-id",
            files=[SkillFile(title="SKILL.md", content="# Deploy")],
            container_id="cid",
        )
        plugin = DiscoveredPluginArtifact(
            name="Python",
            plugin_type="vscode_extension",
            client="vscode",
            install_path="/home/vscode/.vscode/extensions/ms-python.python",
            identifier="plugin-id",
            source_identifier="ms-python.python",
            container_id="cid",
            container_name="devbox",
        )
        agent_definition = DiscoveredAgentDefinition(
            client="cursor",
            name="reviewer",
            description="Reviews code",
            scope="project",
            path="/workspace/.cursor/agents/review.md",
            project_path="/workspace",
            content_hash="agent-hash",
            container_id="cid",
        )
        mock_scan_containers.return_value = ContainerScanResult(
            containers=[container],
            stopped_containers=[stopped_container],
            container_images=[container_image],
            configurations=[config],
            detected_clients=[
                DetectedClient(
                    client="cursor",
                    display_name="Cursor",
                    client_version="4.5.6",
                    detected_via=["container"],
                    config_paths=[
                        "container:devbox:/hidden/node_modules/cursor/package.json"
                    ],
                    container_ids=["cid"],
                )
            ],
            skills=[skill],
            plugins=[plugin],
            agent_definitions=[agent_definition],
            scan_succeeded=True,
            stopped_containers_succeeded=True,
            container_images_succeeded=True,
        )

        result = scan_all_clients(detect_containers=True, scan_projects=False)

        mock_scan_containers.assert_called_once()
        assert result.containers == [container]
        assert result.container_configs == [config]
        assert skill in result.skills
        assert plugin in result.plugins
        assert agent_definition in result.agent_definitions
        assert result.total_agent_definitions >= 1
        assert result.total_containers == 1
        assert result.containers_scanned is True
        assert result.stopped_containers == [stopped_container]
        assert result.container_images == [container_image]
        detected_cursor = next(
            detected
            for detected in result.detected_clients
            if detected.client == "cursor"
        )
        assert "container" in detected_cursor.detected_via
        assert (
            "container:devbox:/hidden/node_modules/cursor/package.json"
            in detected_cursor.config_paths
        )
        payload = result.to_full_payload()
        assert [item["container_id"] for item in payload["containers"]] == ["cid"]
        assert [item["container_id"] for item in payload["stopped_containers"]] == [
            "stopped-cid"
        ]
        assert payload["container_images"] == [
            {
                "repository": "ghcr.io/example/mcp",
                "tag": "latest",
                "digest": "sha256:image",
            }
        ]
        assert payload["container_images_truncated"] is False
        plugin_payload = next(
            item for item in payload["plugins"] if item["identifier"] == "plugin-id"
        )
        assert plugin_payload["container"]["container_id"] == "cid"

    @mock.patch("runlayer_cli.scan.service.scan_wsl_projects")
    def test_detect_containers_leaves_wsl_projects_off_by_default(
        self, mock_scan_wsl_projects
    ):
        """PHASE 13b does not walk WSL homes unless container detection is enabled."""
        result = scan_all_clients(scan_projects=False)

        mock_scan_wsl_projects.assert_not_called()
        assert result.phase_durations_ms["phase_13b_wsl_projects"] == 0

    def test_detect_containers_merges_and_dedupes_wsl_artifacts(self, monkeypatch):
        from runlayer_cli.scan.agent_definition_scanner import (
            DiscoveredAgentDefinition,
        )
        from runlayer_cli.scan.skill_scanner import (
            ARTIFACT_SKILL_MD,
            DiscoveredSkillArtifact,
            SkillFile,
        )
        from runlayer_cli.scan.containers import ContainerScanResult
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        config_path = r"\\wsl.localhost\Ubuntu\home\dev\repo\.cursor\mcp.json"
        project_path = r"\\wsl.localhost\Ubuntu\home\dev\repo"
        config = MCPClientConfig(
            client="cursor",
            config_path=config_path,
            project_path=project_path,
            config_scope="project",
            servers=[
                MCPServerConfig(
                    name="github",
                    type="stdio",
                    config_hash="a" * 64,
                )
            ],
        )
        duplicate_config = MCPClientConfig(
            client="cursor",
            config_path=config_path,
            project_path=project_path,
            config_scope="project",
            servers=list(config.servers),
        )
        skill = DiscoveredSkillArtifact(
            name="deploy",
            path=project_path + r"\.agents\skills\deploy",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="wsl-skill",
            files=[SkillFile(title="SKILL.md", content="# Deploy")],
        )
        agent_definition = DiscoveredAgentDefinition(
            client="cursor",
            name="reviewer",
            description="Reviews code",
            scope="project",
            path=project_path + r"\.cursor\agents\reviewer.md",
            project_path=project_path,
            content_hash="agent-hash",
        )
        result = self._scan_windows_host(
            monkeypatch,
            inventory=_wsl_inventory(("Ubuntu",), success=True),
            wsl_project_result=WSLProjectScanResult(
                configurations=[config, duplicate_config],
                skills=[skill],
                agent_definitions=[agent_definition],
            ),
            container_result=ContainerScanResult(),
        )

        assert [
            item
            for item in result.configurations
            if item.client == "cursor"
            and item.config_path == "/home/dev/repo/.cursor/mcp.json"
        ] == [config]
        assert config.config_scope == "wsl"
        assert config.wsl_distro == "Ubuntu"
        assert config.wsl_user == "dev"
        assert skill in result.skills
        attributed_definition = next(
            item
            for item in result.agent_definitions
            if item.path == "/home/dev/repo/.cursor/agents/reviewer.md"
        )
        assert attributed_definition.wsl_distro == "Ubuntu"

    def test_wsl_config_survives_unrelated_container_dedupe_key(self, monkeypatch):
        """Container hash-key dedupe must not drop unrelated WSL configs.

        The host-bridge dedupe key is (client, project-relative config path,
        server hashes) — no absolute paths. A WSL project and an unrelated
        container project sharing `.cursor/mcp.json` + identical server
        definitions must both survive.
        """
        from runlayer_cli.scan.containers import (
            ContainerScanResult,
            DiscoveredContainer,
        )
        from runlayer_cli.scan.wsl_projects import WSLProjectScanResult

        duplicate_hash = "a" * 64
        container_config = MCPClientConfig(
            client="cursor",
            config_path="/workspace/orders/.cursor/mcp.json",
            project_path="/workspace/orders",
            config_scope="container",
            container_id="cid",
            servers=[
                MCPServerConfig(
                    name="github",
                    type="stdio",
                    config_hash=duplicate_hash,
                )
            ],
        )
        wsl_config = MCPClientConfig(
            client="cursor",
            config_path=r"\\wsl.localhost\Ubuntu\home\dev\billing\.cursor\mcp.json",
            project_path=r"\\wsl.localhost\Ubuntu\home\dev\billing",
            config_scope="project",
            servers=[
                MCPServerConfig(
                    name="github",
                    type="stdio",
                    config_hash=duplicate_hash,
                )
            ],
        )
        result = self._scan_windows_host(
            monkeypatch,
            inventory=_wsl_inventory(("Ubuntu",), success=True),
            wsl_project_result=WSLProjectScanResult(configurations=[wsl_config]),
            container_result=ContainerScanResult(
                containers=[
                    DiscoveredContainer(
                        container_id="cid",
                        name="devbox",
                        image_ref="devbox:latest",
                        image_digest=None,
                    )
                ],
                configurations=[container_config],
                scan_succeeded=True,
            ),
        )

        assert container_config in result.configurations
        assert wsl_config in result.configurations


def test_central_wsl_attribution_normalizes_every_artifact_route():
    from runlayer_cli.scan.agent_definition_scanner import DiscoveredAgentDefinition
    from runlayer_cli.scan.skill_scanner import (
        ARTIFACT_SKILL_MD,
        DiscoveredSkillArtifact,
    )

    global_config = MCPClientConfig(
        client="cursor",
        config_path=r"\\wsl.localhost\Ubuntu\home\alice\.cursor\mcp.json",
        config_scope="global",
        servers=[MCPServerConfig(name="global", type="stdio")],
    )
    project_config = MCPClientConfig(
        client="cursor",
        config_path=(r"\\wsl.localhost\Ubuntu\home\alice\repo\.cursor\mcp.json"),
        project_path=r"\\wsl$\Ubuntu\home\alice\repo",
        config_scope="project",
        servers=[
            MCPServerConfig(
                name="project",
                type="stdio",
                project_name=r"\\wsl$\Ubuntu\home\alice\repo",
            )
        ],
    )
    container_config = MCPClientConfig(
        client="cursor",
        config_path=r"\\wsl.localhost\Ubuntu\workspace\.cursor\mcp.json",
        config_scope="container",
        container_id="cid",
        servers=[MCPServerConfig(name="container", type="stdio")],
    )
    skill = DiscoveredSkillArtifact(
        name="review",
        path=r"\\wsl.localhost\Ubuntu\home\alice\.claude\skills\review",
        artifact_type=ARTIFACT_SKILL_MD,
        scope="global",
        tool="claude_code",
    )
    definition = DiscoveredAgentDefinition(
        client="cursor",
        name="reviewer",
        description=None,
        scope="project",
        path=(
            r"\\wsl.localhost\Ubuntu\home\alice\repo"
            r"\.cursor\agents\review.md"
        ),
        project_path=r"\\wsl$\Ubuntu\home\alice\repo",
        content_hash="a" * 64,
    )

    definitions = _attribute_wsl_artifacts(
        [global_config, project_config, container_config],
        [skill],
        [definition],
        inventory_distros=["Ubuntu"],
    )

    assert global_config.config_scope == "wsl"
    assert global_config.config_path == "/home/alice/.cursor/mcp.json"
    assert global_config.project_path is None
    assert project_config.config_path == "/home/alice/repo/.cursor/mcp.json"
    assert project_config.project_path == "/home/alice/repo"
    assert project_config.servers[0].project_name == "/home/alice/repo"
    assert project_config.wsl_distro == "Ubuntu"
    assert project_config.wsl_user == "alice"
    assert container_config.config_scope == "container"
    assert container_config.wsl_distro is None
    assert container_config.config_path.startswith("\\\\wsl.localhost")

    result = ScanResult(
        device_id="device",
        hostname="host",
        os="windows",
        os_version="11",
        username="alice",
        org_device_id=None,
        scan_duration_ms=1,
        collector_version="test",
        configurations=[global_config, project_config, container_config],
        skills=[skill],
        agent_definitions=definitions,
    )
    config_payload = result.to_api_payload()["configurations"][1]
    assert config_payload["config_scope"] == "wsl"
    assert config_payload["config_path"] == "/home/alice/repo/.cursor/mcp.json"
    assert config_payload["project_path"] == "/home/alice/repo"
    assert config_payload["wsl"] == {"distro": "Ubuntu", "user": "alice"}
    assert config_payload["servers"][0]["project_names"] == "/home/alice/repo"
    assert skill.to_api_payload()["wsl"] == {
        "distro": "Ubuntu",
        "user": "alice",
    }
    assert skill.to_api_payload()["path"] == "/home/alice/.claude/skills/review"
    assert definitions[0].to_api_payload()["wsl"] == {
        "distro": "Ubuntu",
        "user": "alice",
    }
    assert definitions[0].to_api_payload()["path"] == (
        "/home/alice/repo/.cursor/agents/review.md"
    )


def test_wsl_attribution_skips_distros_missing_from_the_inventory():
    """``docker-desktop-data`` is filtered out of the inventory on purpose."""
    config = MCPClientConfig(
        client="cursor",
        config_path=r"\\wsl.localhost\docker-desktop-data\home\alice\.cursor\mcp.json",
        config_scope="global",
        servers=[MCPServerConfig(name="global", type="stdio")],
    )

    _attribute_wsl_artifacts([config], [], [], inventory_distros=["Ubuntu"])

    assert config.config_scope == "global"
    assert config.wsl_distro is None
    assert config.config_path.startswith("\\\\wsl.localhost")


def test_wsl_attribution_preserves_process_override_scope():
    """A launch-flag config on a WSL UNC path keeps its process_override scope."""
    config = MCPClientConfig(
        client="claude-code",
        config_path=r"\\wsl.localhost\Ubuntu\home\alice\custom-mcp.json",
        config_scope="process_override",
        servers=[MCPServerConfig(name="custom", type="stdio")],
    )

    _attribute_wsl_artifacts([config], [], [], inventory_distros=["Ubuntu"])

    assert config.config_scope == "process_override"
    assert config.wsl_distro is None
    assert config.config_path.startswith("\\\\wsl.localhost")


def test_wsl_attribution_uses_the_inventory_spelling_of_the_distro():
    """The ``wsl`` block is the backend's key into the uploaded inventory."""
    config = MCPClientConfig(
        client="cursor",
        config_path=r"\\wsl.localhost\ubuntu-24.04\home\alice\.cursor\mcp.json",
        config_scope="global",
        servers=[MCPServerConfig(name="global", type="stdio")],
    )

    _attribute_wsl_artifacts([config], [], [], inventory_distros=["Ubuntu-24.04"])

    assert config.config_scope == "wsl"
    assert config.wsl_distro == "Ubuntu-24.04"


class TestConcurrentScanPhases:
    @staticmethod
    def _stub_empty_phases(monkeypatch):
        phase_results = {
            "_scan_global_configurations": scan_orchestrator.GlobalPhaseResult(),
            "_scan_cursor_plugin_phase": [],
            "scan_claude_code_plugins": [],
            "scan_codex_plugins": [],
            "scan_opencode_plugins": [],
            "scan_gemini_extensions": ([], []),
            "scan_copilot_plugins": ([], []),
            "scan_global_skills_with_candidates": SkillPhaseScan([], []),
            "scan_user_agent_definitions": [],
            "_scan_plugin_artifact_phase": [],
        }
        for phase_name, phase_result in phase_results.items():
            monkeypatch.setattr(
                scan_orchestrator,
                phase_name,
                lambda *args, _result=phase_result, **kwargs: _result,
            )
        monkeypatch.setattr(scan_orchestrator, "clear_git_remote_cache", lambda: None)
        monkeypatch.setattr(scan_orchestrator, "_wsl_homes", lambda **_: [])

    def test_project_partial_marks_client_presence_incomplete(self, monkeypatch):
        self._stub_empty_phases(monkeypatch)
        project_status = ScanCompletionStatus()
        project_status.mark_incomplete("project_crawl_timed_out")
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(
                node_modules_paths=[Path("/project/node_modules")],
                completion=project_status,
            ),
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        assert "project_crawl_timed_out" in result.completeness.client_presence.reasons

    @pytest.mark.parametrize(
        ("source", "reason"),
        [
            ("global_config", "global_config_incomplete"),
            ("plugin_config", "claude_plugin_scan_failed"),
            ("plugin_artifact", "plugin_artifact_incomplete"),
            ("global_skill", "global_skill_incomplete"),
            ("user_definition", "user_definition_incomplete"),
        ],
    )
    def test_presence_artifact_source_failure_marks_client_presence_incomplete(
        self,
        monkeypatch,
        source,
        reason,
    ):
        self._stub_empty_phases(monkeypatch)
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(),
        )

        if source == "global_config":
            status = ScanCompletionStatus()
            status.mark_incomplete(reason)
            monkeypatch.setattr(
                scan_orchestrator,
                "_scan_global_configurations",
                lambda *_args, **_kwargs: scan_orchestrator.GlobalPhaseResult(
                    completion=status,
                ),
            )
        elif source == "plugin_config":

            def fail_plugin_config():
                raise OSError("unreadable plugin config")

            monkeypatch.setattr(
                scan_orchestrator,
                "scan_claude_code_plugins",
                fail_plugin_config,
            )
        elif source == "plugin_artifact":

            def incomplete_plugin_artifacts(*, scan_status, **_kwargs):
                scan_status.mark_incomplete(reason)
                return []

            monkeypatch.setattr(
                scan_orchestrator,
                "_scan_plugin_artifact_phase",
                incomplete_plugin_artifacts,
            )
        elif source == "global_skill":

            def incomplete_global_skills(*, scan_status, **_kwargs):
                scan_status.mark_incomplete(reason)
                return SkillPhaseScan([], [])

            monkeypatch.setattr(
                scan_orchestrator,
                "scan_global_skills_with_candidates",
                incomplete_global_skills,
            )
        else:

            def incomplete_user_definitions(*, scan_status, **_kwargs):
                scan_status.mark_incomplete(reason)
                return []

            monkeypatch.setattr(
                scan_orchestrator,
                "scan_user_agent_definitions",
                incomplete_user_definitions,
            )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        assert reason in result.completeness.client_presence.reasons

    def test_handled_plugin_failure_marks_mcp_host_static_incomplete(
        self,
        monkeypatch,
    ):
        self._stub_empty_phases(monkeypatch)
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(),
        )

        def incomplete_plugin_artifacts(*, scan_status, **_kwargs):
            scan_status.mark_incomplete("plugin_manifest_read_failed")
            return []

        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_plugin_artifact_phase",
            incomplete_plugin_artifacts,
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        assert (
            "plugin_manifest_read_failed" in result.completeness.mcp_host_static.reasons
        )

    def test_global_config_failure_marks_wsl_static_incomplete(self, monkeypatch):
        self._stub_empty_phases(monkeypatch)
        global_status = ScanCompletionStatus()
        global_status.mark_incomplete("config_path_enumeration_failed")
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_global_configurations",
            lambda *_args, **_kwargs: scan_orchestrator.GlobalPhaseResult(
                completion=global_status,
            ),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(),
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        assert (
            "config_path_enumeration_failed" in result.completeness.wsl_static.reasons
        )

    def test_skill_failure_marks_static_agent_surface_incomplete(self, monkeypatch):
        self._stub_empty_phases(monkeypatch)
        skill_status = ScanCompletionStatus()
        skill_status.mark_incomplete("skill_marker_read_failed")
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(
                skill_completion=skill_status,
            ),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "discover_agents",
            lambda **_kwargs: SimpleNamespace(
                agents=[],
                complete=True,
                incomplete_reasons=[],
            ),
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=True,
        )

        assert (
            "skill_marker_read_failed" in result.completeness.agent_host_static.reasons
        )

    @pytest.mark.parametrize(
        "cap_field",
        [
            "node_modules_paths_truncated",
            "python_env_roots_truncated",
            "launcher_directories_truncated",
        ],
    )
    def test_hidden_space_output_caps_mark_dependent_surfaces_incomplete(
        self,
        monkeypatch,
        cap_field,
    ):
        self._stub_empty_phases(monkeypatch)
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(),
        )
        hidden_result = scan_orchestrator.HiddenSpaceScanResult()
        setattr(hidden_result, cap_field, True)
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_hidden_spaces",
            lambda **_kwargs: hidden_result,
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        assert (
            "hidden_space_scan_truncated" in result.completeness.client_presence.reasons
        )
        assert "hidden_space_scan_truncated" in result.completeness.wsl_static.reasons

    def test_project_skill_crawl_completeness_propagates(self, monkeypatch):
        self._stub_empty_phases(monkeypatch)
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(
                skill_crawl_complete=True
            ),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_hidden_spaces",
            lambda **_kwargs: scan_orchestrator.HiddenSpaceScanResult(),
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        assert result.skill_crawl_complete is True

    def test_global_skill_failure_marks_combined_crawl_incomplete(self, monkeypatch):
        self._stub_empty_phases(monkeypatch)
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(
                skill_crawl_complete=True
            ),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_global_skills_with_candidates",
            lambda **_kwargs: SkillPhaseScan([], [], complete=False),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_hidden_spaces",
            lambda **_kwargs: scan_orchestrator.HiddenSpaceScanResult(),
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        assert result.skill_crawl_complete is False

    def test_skill_candidate_paths_propagate_by_phase(self, monkeypatch):
        from runlayer_cli.scan.skill_scanner import (
            DiscoveredSkillArtifact,
        )

        self._stub_empty_phases(monkeypatch)
        project_skill = DiscoveredSkillArtifact(
            name="project",
            path="/repo/.agents/skills/project",
            artifact_type="skill_md",
            scope="project",
            tool="multi",
        )
        global_skill = DiscoveredSkillArtifact(
            name="global",
            path="/home/u/.claude/skills/global",
            artifact_type="skill_md",
            scope="global",
            tool="claude_code",
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(
                skills=[project_skill],
                discovered_project_paths=[Path("/repo")],
                project_skill_candidate_paths=[project_skill.path],
            ),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_global_skills_with_candidates",
            lambda **_kwargs: SkillPhaseScan(
                artifacts=[global_skill],
                candidate_paths=[global_skill.path],
            ),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_hidden_spaces",
            lambda **_kwargs: scan_orchestrator.HiddenSpaceScanResult(),
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        assert result.skills == [project_skill, global_skill]
        assert result.discovered_project_paths == [Path("/repo")]
        assert result.project_skill_candidate_paths == [project_skill.path]
        assert result.global_skill_candidate_paths == [global_skill.path]

    def test_disabled_project_phase_is_not_authoritative(self, monkeypatch):
        self._stub_empty_phases(monkeypatch)
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_hidden_spaces",
            lambda **_kwargs: scan_orchestrator.HiddenSpaceScanResult(),
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=False,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        assert result.skill_crawl_complete is False
        assert result.project_skill_candidate_paths == []
        assert result.global_skill_candidate_paths == []

    def test_disguised_skills_disabled_skips_probe_and_records_zero(self, monkeypatch):
        self._stub_empty_phases(monkeypatch)
        probe = mock.Mock(return_value=[])
        monkeypatch.setattr(scan_orchestrator, "scan_disguised_skills", probe)
        timer = PhaseTimer()

        with structlog.testing.capture_logs() as logs:
            scan_orchestrator.run_concurrent_scan_phases(
                clients=[],
                governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
                timer=timer,
                scan_projects=False,
                project_scan_timeout=60,
                project_scan_depth=7,
                detect_agents=False,
                run_static_agents=False,
                detect_disguised_skills=False,
            )

        probe.assert_not_called()
        assert timer.durations_ms()["phase_09b_disguised_skills"] == 0
        assert not [
            event for event in logs if event["event"] == "Scanning disguised skills"
        ]

    def test_disguised_skills_enabled_runs_probe_and_logs_phase(self, monkeypatch):
        self._stub_empty_phases(monkeypatch)
        hidden_sweep = mock.Mock(return_value=scan_orchestrator.HiddenSpaceScanResult())
        probe = mock.Mock(return_value=[])
        monkeypatch.setattr(scan_orchestrator, "scan_hidden_spaces", hidden_sweep)
        monkeypatch.setattr(scan_orchestrator, "scan_disguised_skills", probe)
        timer = PhaseTimer()

        with structlog.testing.capture_logs() as logs:
            scan_orchestrator.run_concurrent_scan_phases(
                clients=[],
                governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
                timer=timer,
                scan_projects=False,
                project_scan_timeout=37,
                project_scan_depth=7,
                detect_agents=False,
                run_static_agents=False,
                detect_disguised_skills=True,
            )

        probe.assert_called_once()
        assert hidden_sweep.call_args.kwargs["time_budget_s"] == 37
        assert probe.call_args.kwargs["time_budget_s"] == 37
        assert "phase_09b_disguised_skills" in timer.durations_ms()
        assert [
            event for event in logs if event["event"] == "Scanning disguised skills"
        ]

    def test_renamed_plugin_caches_disabled_skips_probe_and_records_zero(
        self, monkeypatch
    ):
        self._stub_empty_phases(monkeypatch)
        probe = mock.Mock(return_value=[])
        monkeypatch.setattr(scan_orchestrator, "scan_renamed_plugin_caches", probe)
        timer = PhaseTimer()

        with structlog.testing.capture_logs() as logs:
            scan_orchestrator.run_concurrent_scan_phases(
                clients=[],
                governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
                timer=timer,
                scan_projects=False,
                project_scan_timeout=60,
                project_scan_depth=7,
                detect_agents=False,
                run_static_agents=False,
            )

        probe.assert_not_called()
        assert timer.durations_ms()["phase_10b_renamed_plugin_caches"] == 0
        assert not [
            event
            for event in logs
            if event["event"] == "Scanning renamed plugin caches"
        ]

    def test_renamed_plugin_caches_enabled_merges_novel_artifacts(self, monkeypatch):
        from runlayer_cli.scan.plugin_scanner import DiscoveredPluginArtifact

        self._stub_empty_phases(monkeypatch)
        known = DiscoveredPluginArtifact(
            name="known",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/home/u/.cursor/plugins/cache/cursor-public/known",
            identifier="skill-known",
        )
        renamed_copy = DiscoveredPluginArtifact(
            name="known",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/home/u/.cursor/plugins/renamed-copy",
            identifier="skill-known",
        )
        novel = DiscoveredPluginArtifact(
            name="novel",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/home/u/.cursor/plugins/novel",
            identifier="skill-novel",
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_plugin_artifact_phase",
            lambda **_kwargs: [known],
        )
        probe = mock.Mock(return_value=[renamed_copy, novel])
        monkeypatch.setattr(scan_orchestrator, "scan_renamed_plugin_caches", probe)
        timer = PhaseTimer()

        with structlog.testing.capture_logs() as logs:
            result = scan_orchestrator.run_concurrent_scan_phases(
                clients=[],
                governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
                timer=timer,
                scan_projects=False,
                project_scan_timeout=60,
                project_scan_depth=7,
                detect_agents=False,
                run_static_agents=False,
                detect_renamed_plugin_caches=True,
            )

        probe.assert_called_once()
        assert "phase_10b_renamed_plugin_caches" in timer.durations_ms()
        assert [
            event
            for event in logs
            if event["event"] == "Scanning renamed plugin caches"
        ]
        assert [plugin.name for plugin in result.plugins] == ["known", "novel"]

    def test_independent_phases_overlap_and_assemble_in_phase_order(self, monkeypatch):
        from runlayer_cli.scan.agent_definition_scanner import (
            DiscoveredAgentDefinition,
        )

        crawl_started = threading.Event()
        independent_started = threading.Event()
        project_definition = DiscoveredAgentDefinition(
            client="cursor",
            name="project",
            description=None,
            scope="project",
            path="/repo/.cursor/agents/project.md",
            project_path="/repo",
            content_hash="same-content",
        )
        user_definition = DiscoveredAgentDefinition(
            client="cursor",
            name="user",
            description=None,
            scope="user",
            path="/home/u/.cursor/agents/user.md",
            project_path=None,
            content_hash="same-content",
        )

        def config(name: str) -> MCPClientConfig:
            return MCPClientConfig(client=name, servers=[])

        def project_phase(**kwargs):
            crawl_started.set()
            assert independent_started.wait(timeout=5)
            return scan_orchestrator.ProjectPhaseResult(
                configurations=[config("phase-2")],
                agent_definitions=[project_definition],
            )

        def claude_phase():
            assert crawl_started.wait(timeout=5)
            independent_started.set()
            return [config("phase-3")]

        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_global_configurations",
            lambda clients, governor: scan_orchestrator.GlobalPhaseResult(
                configurations=[config("phase-1")]
            ),
        )
        monkeypatch.setattr(scan_orchestrator, "_scan_project_phase", project_phase)
        monkeypatch.setattr(scan_orchestrator, "scan_claude_code_plugins", claude_phase)
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_cursor_plugin_phase",
            lambda paths: [config("phase-4")],
        )
        monkeypatch.setattr(
            scan_orchestrator, "scan_codex_plugins", lambda: [config("phase-5")]
        )
        monkeypatch.setattr(
            scan_orchestrator, "scan_opencode_plugins", lambda: [config("phase-6")]
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_gemini_extensions",
            lambda: ([config("phase-7")], []),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_copilot_plugins",
            lambda: ([config("phase-8")], []),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_global_skills_with_candidates",
            lambda **kwargs: SkillPhaseScan([], []),
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_user_agent_definitions",
            lambda **kwargs: [user_definition],
        )
        monkeypatch.setattr(
            scan_orchestrator, "_scan_plugin_artifact_phase", lambda **kwargs: []
        )
        monkeypatch.setattr(scan_orchestrator, "clear_git_remote_cache", lambda: None)
        monkeypatch.setattr(scan_orchestrator, "_wsl_homes", lambda **_: [])

        governor = SimpleNamespace(cpu_cores=2, checkpoint=lambda: None)
        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=governor,
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )
        second_result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=governor,
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        expected_order = [
            "phase-1",
            "phase-2",
            "phase-3",
            "phase-4",
            "phase-5",
            "phase-6",
            "phase-7",
            "phase-8",
        ]
        assert [item.client for item in result.configurations] == expected_order
        assert [item.client for item in second_result.configurations] == expected_order
        assert result.agent_definitions == [project_definition, user_definition]
        assert second_result.agent_definitions == [project_definition, user_definition]

    def test_wsl_homes_fan_out_to_home_artifact_phases(self, monkeypatch):
        wsl_homes = [
            Path(r"\\wsl.localhost\Ubuntu\home\alex"),
            Path(r"\\wsl.localhost\Debian\home\sam"),
        ]
        wsl_homes_mock = mock.Mock(return_value=wsl_homes)
        plugin_calls: dict[str, list[Path | None]] = {
            "claude": [],
            "codex": [],
            "opencode": [],
            "copilot": [],
        }
        extra_roots: dict[str, list[Path]] = {}

        def scan_claude(*, home=None):
            plugin_calls["claude"].append(home)
            return []

        def scan_codex(*, home=None):
            plugin_calls["codex"].append(home)
            return []

        def scan_opencode(*, home=None):
            plugin_calls["opencode"].append(home)
            return []

        def scan_copilot(*, home=None):
            plugin_calls["copilot"].append(home)
            return [], []

        def project_phase(**kwargs):
            extra_roots["project"] = list(kwargs["extra_home_roots"])
            return scan_orchestrator.ProjectPhaseResult()

        def global_skills(*, extra_home_roots=(), checkpoint=None, scan_status=None):
            extra_roots["skills"] = list(extra_home_roots)
            return SkillPhaseScan([], [])

        def user_agent_definitions(*, extra_home_roots=(), scan_status=None):
            extra_roots["agent_definitions"] = list(extra_home_roots)
            return []

        monkeypatch.setattr(scan_orchestrator, "_wsl_homes", wsl_homes_mock)
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_global_configurations",
            lambda clients, governor: scan_orchestrator.GlobalPhaseResult(),
        )
        monkeypatch.setattr(scan_orchestrator, "_scan_project_phase", project_phase)
        monkeypatch.setattr(
            scan_orchestrator, "_scan_cursor_plugin_phase", lambda paths: []
        )
        monkeypatch.setattr(scan_orchestrator, "scan_claude_code_plugins", scan_claude)
        monkeypatch.setattr(scan_orchestrator, "scan_codex_plugins", scan_codex)
        monkeypatch.setattr(scan_orchestrator, "scan_opencode_plugins", scan_opencode)
        monkeypatch.setattr(scan_orchestrator, "scan_copilot_plugins", scan_copilot)
        monkeypatch.setattr(
            scan_orchestrator, "scan_gemini_extensions", lambda: ([], [])
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_global_skills_with_candidates",
            global_skills,
        )
        monkeypatch.setattr(
            scan_orchestrator,
            "scan_user_agent_definitions",
            user_agent_definitions,
        )
        monkeypatch.setattr(
            scan_orchestrator, "_scan_plugin_artifact_phase", lambda **kwargs: []
        )
        monkeypatch.setattr(scan_orchestrator, "clear_git_remote_cache", lambda: None)

        scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
        )

        wsl_homes_mock.assert_called_once_with(scan_status=mock.ANY)
        assert plugin_calls == {
            "claude": [None, *wsl_homes],
            "codex": [None, *wsl_homes],
            "opencode": [None, *wsl_homes],
            "copilot": [None, *wsl_homes],
        }
        assert extra_roots == {
            "project": wsl_homes,
            "skills": wsl_homes,
            "agent_definitions": wsl_homes,
        }

    def test_agent_duration_reports_only_independent_phases(self, monkeypatch):
        phase_results = {
            "_scan_global_configurations": scan_orchestrator.GlobalPhaseResult(),
            "_scan_project_phase": scan_orchestrator.ProjectPhaseResult(),
            "scan_claude_code_plugins": [],
            "_scan_cursor_plugin_phase": [],
            "scan_codex_plugins": [],
            "scan_opencode_plugins": [],
            "scan_gemini_extensions": ([], []),
            "scan_copilot_plugins": ([], []),
            "scan_global_skills_with_candidates": SkillPhaseScan([], []),
            "scan_user_agent_definitions": [],
            "_scan_plugin_artifact_phase": [],
        }
        for phase_name, phase_result in phase_results.items():
            monkeypatch.setattr(
                scan_orchestrator,
                phase_name,
                lambda *args, _result=phase_result, **kwargs: _result,
            )
        monkeypatch.setattr(
            scan_orchestrator,
            "discover_agents",
            lambda **kwargs: SimpleNamespace(agents=[]),
        )
        monkeypatch.setattr(scan_orchestrator, "clear_git_remote_cache", lambda: None)
        monkeypatch.setattr(scan_orchestrator, "_wsl_homes", lambda **_: [])

        class AgentPhaseTimer(PhaseTimer):
            @contextmanager
            def phase(self, name):
                try:
                    yield
                finally:
                    duration_ms = {
                        "phase_11_install_agents": 40,
                        "phase_11_static_agents": 70,
                    }.get(name, 0)
                    self.record(name, duration_ms)

        timer = AgentPhaseTimer()
        governor = SimpleNamespace(cpu_cores=2, checkpoint=lambda: None)

        scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=governor,
            timer=timer,
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=True,
            run_static_agents=True,
        )

        durations = timer.durations_ms()
        assert durations["phase_11_install_agents"] == 40
        assert durations["phase_11_static_agents"] == 70
        assert "phase_11_agent_detection" not in durations

    def test_global_skill_descendant_filtered_at_assembly(self, tmp_path):
        from runlayer_cli.scan.agent_scan import discover_agents
        from runlayer_cli.scan.agents.detect import Evidence, build_install_agent
        from runlayer_cli.scan.skill_scanner import DiscoveredSkillArtifact

        skill = tmp_path / ".agents" / "skills" / "runlayer-qa"
        scripts = skill / "scripts"
        scripts.mkdir(parents=True)
        manifest = scripts / "package.json"
        manifest.write_text(
            '{"dependencies":{"@modelcontextprotocol/sdk":"^1.0.0"}}',
            encoding="utf-8",
        )
        (scripts / "server.ts").write_text(
            'import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";',
            encoding="utf-8",
        )
        static_agents = discover_agents(
            found_paths=[manifest],
            detect_install=False,
        ).agents
        assert len(static_agents) == 1

        install_agent = build_install_agent(
            framework_id="openclaw",
            display_name="OpenClaw",
            location=str(scripts),
            evidence=[Evidence("install_artifact", str(scripts), "test")],
        )
        global_skill = DiscoveredSkillArtifact(
            name="runlayer-qa",
            path=str(skill),
            artifact_type="skill_md",
            scope="global",
            tool="multi",
        )

        agents = scan_orchestrator._assemble_agents(
            [global_skill],
            [install_agent],
            static_agents,
        )

        assert agents == [install_agent]


class TestScanResultFullPayload:
    """F6: one method builds the dry-run view; the MCP wire payload excludes
    skills/plugins/agents (those submit through their own endpoints)."""

    def _result_with_findings(self):
        from runlayer_cli.scan.agents.detect import Evidence, build_install_agent
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig
        from runlayer_cli.scan.processes.models import DiscoveredProcess

        agent = build_install_agent(
            framework_id="openclaw",
            display_name="OpenClaw",
            location="/Users/dev/.openclaw",
            evidence=[Evidence("install_artifact", "/usr/local/bin/openclaw", "cli")],
            markers=["cli"],
        )
        process = DiscoveredProcess(
            pid=4321,
            ppid=1,
            kind="mcp_server",
            discovery_source="listening_port",
            matched_client=None,
            exe="/usr/local/bin/node",
            argv_redacted=["node", "server.js"],
            command_hash="deadbeef",
            config_hash="cfg-1",
            agent_framework_id=None,
            agent_fingerprint=None,
            agent_root_path=None,
            listening_ports=[3000],
            bind_scope="loopback",
            transport="http",
            ai_signals=["config_port_match:3000"],
            confidence=0.8,
            user="u",
            started_at=None,
            cwd_project="proj",
            settings_overrides=[{"flag": "--mcp-config", "value": "/tmp/custom.json"}],
        )
        return ScanResult(
            device_id="d",
            hostname="h",
            os="darwin",
            os_version="14",
            username="u",
            org_device_id=None,
            scan_duration_ms=1,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="cursor",
                    servers=[MCPServerConfig(name="s1", type="stdio")],
                    config_scope="global",
                )
            ],
            skills=[SimpleNamespace(to_api_payload=lambda: {"name": "skill-1"})],
            plugins=[SimpleNamespace(to_api_payload=lambda: {"name": "plugin-1"})],
            agents=[agent],
            processes=[process],
        )

    def test_wire_payload_excludes_skills_plugins_agents(self):
        payload = self._result_with_findings().to_api_payload()
        assert "skills" not in payload
        assert "plugins" not in payload
        assert "agents" not in payload
        assert [process["pid"] for process in payload["processes"]] == [4321]
        assert payload["processes"][0]["config_hash"] == "cfg-1"
        assert payload["processes"][0]["settings_overrides"] == [
            {"flag": "--mcp-config", "value": "/tmp/custom.json"}
        ]

    def test_every_scan_payload_reuses_one_aware_utc_start_timestamp(self):
        started_at = datetime.datetime(
            2026,
            9,
            3,
            12,
            34,
            56,
            789000,
            tzinfo=datetime.timezone.utc,
        )
        result = self._result_with_findings()
        result.scan_started_at = started_at

        payloads = (
            result.to_api_payload(),
            result.to_full_payload(include_agents=True),
            result.to_agent_report_payload(),
            result.to_agent_definition_report_payload(),
        )

        assert {payload["scan_started_at"] for payload in payloads} == {
            "2026-09-03T12:34:56.789000+00:00"
        }

    def test_wire_payload_includes_detected_clients(self, monkeypatch):
        from runlayer_cli.scan.wsl_presence import WSLClientContext

        monkeypatch.setenv("RUNLAYER_STRIP_PATH_PREFIX", "/container")
        result = self._result_with_findings()
        result.detected_clients = [
            DetectedClient(
                client="cursor",
                display_name="Cursor",
                client_version="1.2.3",
                detected_via=["app", "config"],
                config_paths=["/container/Users/dev/.cursor", "/other/.cursor"],
                wsl_contexts=[
                    WSLClientContext(distro="Ubuntu", user="dev"),
                ],
            )
        ]

        assert result.to_api_payload()["detected_clients"] == [
            {
                "client": "cursor",
                "display_name": "Cursor",
                "client_version": "1.2.3",
                "detected_via": ["app", "config"],
                "evidence_origin": "static",
                "config_paths": ["/Users/dev/.cursor", "/other/.cursor"],
                "wsl_contexts": [{"distro": "Ubuntu", "user": "dev"}],
            }
        ]

    def test_wire_payload_omits_processes_when_not_detected(self):
        result = self._result_with_findings()
        result.processes = []

        assert "processes" not in result.to_api_payload()

    def test_full_payload_includes_processes(self):
        payload = self._result_with_findings().to_full_payload()
        assert [p["pid"] for p in payload["processes"]] == [4321]
        assert payload["processes"][0]["config_hash"] == "cfg-1"

    def test_wire_payload_carries_serial_number(self):
        result = self._result_with_findings()
        result.serial_number = "C02XYZ123ABC"
        payload = result.to_api_payload()
        assert payload["serial_number"] == "C02XYZ123ABC"

    def test_wire_payload_carries_container_inventory_and_config_context(self):
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig
        from runlayer_cli.scan.containers import DiscoveredContainer

        result = self._result_with_findings()
        result.container_scan_requested = True
        result.containers_scanned = True
        result.containers = [
            DiscoveredContainer(
                container_id="cid",
                name="devbox",
                image_ref="devbox:latest",
                image_digest="sha256:abc",
                is_devcontainer=True,
                mounts_host_home=False,
                has_mcp_configs=True,
            )
        ]
        result.configurations = [
            MCPClientConfig(
                client="cursor",
                config_scope="container",
                container_id="cid",
                container_name="devbox",
                container_image_ref="devbox:latest",
                container_image_digest="sha256:abc",
                container_is_devcontainer=True,
                container_mounts_host_home=False,
                servers=[MCPServerConfig(name="github", type="stdio")],
            )
        ]

        payload = result.to_api_payload()

        assert payload["host_containers_scanned"] is True
        assert payload["wsl_container_scanned_distros"] == []
        assert payload["containers"] == [
            {
                "container_id": "cid",
                "name": "devbox",
                "image_ref": "devbox:latest",
                "image_digest": "sha256:abc",
                "runtime": "docker",
                "is_devcontainer": True,
                "is_running": True,
                "labels": {},
                "mounts_host_home": False,
                "has_mcp_configs": True,
                "has_ai_agents": False,
            }
        ]
        assert payload["configurations"][0]["container"] == {
            "container_id": "cid",
            "name": "devbox",
            "image_ref": "devbox:latest",
            "image_digest": "sha256:abc",
            "is_devcontainer": True,
            "mounts_host_home": False,
        }

    def test_requested_failed_container_scan_reports_negative_authority(self):
        result = self._result_with_findings()
        result.container_scan_requested = True
        result.container_scan_error = "Container runtime unavailable"

        payload = result.to_api_payload()

        assert payload["containers"] == []
        assert payload["host_containers_scanned"] is False
        assert payload["wsl_container_scanned_distros"] == []
        assert payload["container_scan_error"] == "Container runtime unavailable"

    def test_requested_failed_container_scan_defaults_to_incomplete_reason(self):
        result = self._result_with_findings()
        result.container_scan_requested = True

        assert (
            result.to_api_payload()["container_scan_error"]
            == "Container inventory incomplete"
        )

    def test_requested_container_scan_error_is_bounded_and_sanitized(self):
        result = self._result_with_findings()
        result.container_scan_requested = True
        result.container_scan_error = "  runtime\tunavailable\n" + ("x" * 300)

        reason = result.to_api_payload()["container_scan_error"]

        assert len(reason) == 200
        assert reason.startswith("runtime unavailable ")
        assert "\n" not in reason
        assert "\t" not in reason

    def test_disabled_container_scan_omits_container_authority(self):
        payload = self._result_with_findings().to_api_payload()

        assert "containers" not in payload
        assert "host_containers_scanned" not in payload
        assert "wsl_container_scanned_distros" not in payload
        assert "container_scan_error" not in payload

    def test_wire_payload_carries_wsl_container_scan_authority(self):
        from runlayer_cli.scan.containers import DiscoveredContainer

        result = self._result_with_findings()
        result.container_scan_requested = True
        result.containers = [
            DiscoveredContainer(
                container_id="wsl-cid",
                name="inside-wsl",
                image_ref="example/mcp:latest",
                image_digest=None,
                wsl_distro="Ubuntu",
            )
        ]
        result.wsl_container_scanned_distros = ["Ubuntu"]

        payload = result.to_api_payload()

        assert payload["host_containers_scanned"] is False
        assert payload["wsl_container_scanned_distros"] == ["Ubuntu"]
        assert payload["containers"][0]["wsl_distro"] == "Ubuntu"

    def test_partial_wsl_container_findings_are_uploaded_without_scan_authority(self):
        from runlayer_cli.scan.containers import DiscoveredContainer

        result = self._result_with_findings()
        result.container_scan_requested = True
        result.containers = [
            DiscoveredContainer(
                container_id="wsl-cid",
                name="inside-wsl",
                image_ref="devbox:latest",
                image_digest=None,
                wsl_distro="Ubuntu",
            )
        ]
        result.containers_scanned = False

        payload = result.to_api_payload()

        assert payload["host_containers_scanned"] is False
        assert payload["wsl_container_scanned_distros"] == []
        assert payload["containers"][0]["container_id"] == "wsl-cid"
        assert payload["containers"][0]["wsl_distro"] == "Ubuntu"

    def test_incomplete_wsl_inventory_is_local_only(self):
        from runlayer_cli.scan.device import DiscoveredWSLDistro

        result = self._result_with_findings()
        result.wsl_distros = [
            DiscoveredWSLDistro(
                name="Ubuntu",
                wsl_version=2,
                is_running=True,
            )
        ]
        result.wsl_scanned = False

        assert "wsl_distros" not in result.to_api_payload()
        assert result.to_full_payload()["wsl_distros"] == [
            {
                "distro_name": "Ubuntu",
                "wsl_version": 2,
                "is_running": True,
                "scanned": False,
                "container_runtimes": [],
            }
        ]

    def test_successful_empty_wsl_inventory_is_on_wire(self):
        result = self._result_with_findings()
        result.wsl_scanned = True

        assert result.to_api_payload()["wsl_distros"] == []

    def test_full_payload_folds_in_skills_and_plugins(self):
        payload = self._result_with_findings().to_full_payload()
        assert payload["skills"] == [{"name": "skill-1"}]
        assert payload["plugins"] == [{"name": "plugin-1"}]
        # Agents are opt-in in the dry-run view: default omits them.
        assert "agents" not in payload

    def test_full_payload_includes_agents_when_requested(self):
        payload = self._result_with_findings().to_full_payload(include_agents=True)
        assert [a["framework_id"] for a in payload["agents"]] == ["openclaw"]

    def test_agent_definition_payload_uses_dedicated_report(self):
        from runlayer_cli.scan.agent_definition_scanner import (
            DiscoveredAgentDefinition,
        )

        result = self._result_with_findings()
        result.agent_definitions = [
            DiscoveredAgentDefinition(
                client="cursor",
                name="reviewer",
                description="Reviews code",
                scope="project",
                path="/workspace/.cursor/agents/review.md",
                project_path="/workspace",
                content_hash="d" * 64,
            )
        ]

        assert "agent_definitions" not in result.to_api_payload()
        assert result.to_full_payload()["agent_definitions"] == [
            {
                "client": "cursor",
                "name": "reviewer",
                "description": "Reviews code",
                "scope": "project",
                "path": "/workspace/.cursor/agents/review.md",
                "project_path": "/workspace",
                "content_hash": "d" * 64,
            }
        ]
        assert result.to_agent_definition_report_payload() == {
            "device_id": "d",
            "hostname": "h",
            "os": "darwin",
            "os_version": "14",
            "username": "u",
            "org_device_id": None,
            "serial_number": None,
            "scan_session_id": str(result.scan_session_id),
            "scan_started_at": result.scan_started_at.isoformat(),
            "agent_definitions": [
                {
                    "client": "cursor",
                    "name": "reviewer",
                    "description": "Reviews code",
                    "scope": "project",
                    "path": "/workspace/.cursor/agents/review.md",
                    "project_path": "/workspace",
                    "content_hash": "d" * 64,
                }
            ],
        }
        assert result.total_agent_definitions == 1

    def test_phase_durations_are_dry_run_only(self):
        result = self._result_with_findings()
        result.phase_durations_ms = {"phase_02": 20, "phase_01": 10}

        assert "phase_durations_ms" not in result.to_api_payload()
        assert result.to_full_payload()["phase_durations_ms"] == {
            "phase_01": 10,
            "phase_02": 20,
        }


class TestAgentManifestCrawlGating:
    """F1 regression: agent manifest basenames widen the find crawl only when the
    STATIC agent-framework scan runs. It is ON by default now (agents submit), so
    the default run pays the crawl -- but --no-detect-agents or
    --no-detect-agent-frameworks must not, since those basenames are ubiquitous
    and balloon found_paths."""

    @mock.patch(
        "runlayer_cli.scan.orchestrator.find_files_and_node_modules_under_home",
        return_value=SimpleNamespace(
            found_paths=[],
            node_modules_paths=[],
            logical_paths={},
        ),
    )
    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.orchestrator.get_clients_with_project_configs",
        return_value=[],
    )
    def test_no_detect_agents_excludes_agent_manifest_filenames(
        self, mock_proj, mock_clients, mock_find
    ):
        from runlayer_cli.scan.agents.manifests import agent_manifest_search_filenames

        scan_all_clients(detect_agents=False)

        mock_find.assert_called_once()
        crawl_filenames = set(mock_find.call_args[0][0])
        agent_filenames = set(agent_manifest_search_filenames())
        assert not (crawl_filenames & agent_filenames), (
            "agent manifest basenames leaked into the --no-detect-agents crawl: "
            f"{crawl_filenames & agent_filenames}"
        )

    @mock.patch(
        "runlayer_cli.scan.orchestrator.find_files_and_node_modules_under_home",
        return_value=SimpleNamespace(
            found_paths=[],
            node_modules_paths=[],
            logical_paths={},
        ),
    )
    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.orchestrator.get_clients_with_project_configs",
        return_value=[],
    )
    def test_static_off_excludes_agent_manifest_filenames(
        self, mock_proj, mock_clients, mock_find
    ):
        """--no-detect-agent-frameworks (static off, install channel on): manifests
        must not widen the crawl even though the master switch is on."""
        from runlayer_cli.scan.agents.manifests import agent_manifest_search_filenames

        scan_all_clients(detect_agents=True, detect_agent_frameworks=False)

        mock_find.assert_called_once()
        crawl_filenames = set(mock_find.call_args[0][0])
        agent_filenames = set(agent_manifest_search_filenames())
        assert not (crawl_filenames & agent_filenames), (
            "agent manifest basenames leaked into a static-off crawl: "
            f"{crawl_filenames & agent_filenames}"
        )

    @mock.patch(
        "runlayer_cli.scan.orchestrator.find_files_and_node_modules_under_home",
        return_value=SimpleNamespace(
            found_paths=[],
            node_modules_paths=[],
            logical_paths={},
        ),
    )
    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.orchestrator.get_clients_with_project_configs",
        return_value=[],
    )
    def test_default_run_includes_agent_manifest_filenames(
        self, mock_proj, mock_clients, mock_find
    ):
        """Default scan = static ON: manifests widen the crawl so manifest-only
        agent projects are discoverable and submitted."""
        from runlayer_cli.scan.agents.manifests import agent_manifest_search_filenames

        scan_all_clients(detect_agents=True)

        mock_find.assert_called_once()
        crawl_filenames = set(mock_find.call_args[0][0])
        agent_filenames = set(agent_manifest_search_filenames())
        assert agent_filenames.issubset(crawl_filenames)

    @mock.patch(
        "runlayer_cli.scan.orchestrator.find_files_and_node_modules_under_home",
        return_value=SimpleNamespace(
            found_paths=[],
            node_modules_paths=[],
            logical_paths={},
        ),
    )
    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.orchestrator.get_clients_with_project_configs",
        return_value=[],
    )
    def test_detect_agent_frameworks_includes_agent_manifest_filenames(
        self, mock_proj, mock_clients, mock_find
    ):
        from runlayer_cli.scan.agents.manifests import agent_manifest_search_filenames

        scan_all_clients(detect_agents=True, detect_agent_frameworks=True)

        mock_find.assert_called_once()
        crawl_filenames = set(mock_find.call_args[0][0])
        agent_filenames = set(agent_manifest_search_filenames())
        assert agent_filenames.issubset(crawl_filenames)


class TestScanResultProperties:
    def test_total_servers_property(self):
        """total_servers sums servers from all configurations."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test",
            hostname="test",
            os="darwin",
            os_version="14.0",
            username="user",
            org_device_id=None,
            scan_duration_ms=100,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="client1",
                    servers=[
                        MCPServerConfig(name="s1", type="stdio"),
                        MCPServerConfig(name="s2", type="stdio"),
                    ],
                ),
                MCPClientConfig(
                    client="client2",
                    servers=[
                        MCPServerConfig(name="s3", type="sse"),
                    ],
                ),
            ],
        )

        assert result.total_servers == 3

    def test_clients_with_servers_property(self):
        """clients_with_servers returns list of client names."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test",
            hostname="test",
            os="darwin",
            os_version="14.0",
            username="user",
            org_device_id=None,
            scan_duration_ms=100,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="cursor",
                    servers=[MCPServerConfig(name="s1", type="stdio")],
                ),
                MCPClientConfig(
                    client="vscode",
                    servers=[MCPServerConfig(name="s2", type="stdio")],
                ),
            ],
        )

        assert result.clients_with_servers == ["cursor", "vscode"]

    def test_global_and_project_configs_properties(self):
        """global_configs and project_configs filter correctly."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test",
            hostname="test",
            os="darwin",
            os_version="14.0",
            username="user",
            org_device_id=None,
            scan_duration_ms=100,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="cursor",
                    servers=[MCPServerConfig(name="s1", type="stdio")],
                    config_scope="global",
                ),
                MCPClientConfig(
                    client="vscode",
                    servers=[MCPServerConfig(name="s2", type="stdio")],
                    config_scope="project",
                    project_path="/path/to/project",
                ),
            ],
        )

        assert len(result.global_configs) == 1
        assert result.global_configs[0].client == "cursor"
        assert len(result.project_configs) == 1
        assert result.project_configs[0].client == "vscode"


class TestProjectConfigServerNamePropagation:
    """Tests for project_name field propagation to servers."""

    def test_project_path_propagated_to_server_project_name(self):
        """Servers from project configs should have project_name set."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        # Simulate what happens in scan_all_clients for project configs
        config = MCPClientConfig(
            client="vscode",
            servers=[
                MCPServerConfig(name="server1", type="stdio", command="node"),
                MCPServerConfig(name="server2", type="sse", url="http://localhost"),
            ],
            config_scope="project",
            project_path="/home/user/my-project",
        )

        # Propagate project_path to servers (this is what the service does)
        for server in config.servers:
            server.project_name = config.project_path

        # Verify servers have project_name set
        assert config.servers[0].project_name == "/home/user/my-project"
        assert config.servers[1].project_name == "/home/user/my-project"

    def test_api_payload_includes_server_project_names(self):
        """API payload should include project_names on servers."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test",
            hostname="test",
            os="darwin",
            os_version="14.0",
            username="user",
            org_device_id=None,
            scan_duration_ms=100,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="vscode",
                    servers=[
                        MCPServerConfig(
                            name="s1",
                            type="stdio",
                            project_name="/home/user/my-project",
                        ),
                    ],
                    config_scope="project",
                    project_path="/home/user/my-project",
                ),
            ],
        )

        payload = result.to_api_payload()
        server = payload["configurations"][0]["servers"][0]
        assert server["project_names"] == "/home/user/my-project"

    def test_global_config_servers_have_no_project_name(self):
        """Servers from global configs should have project_name as None."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test",
            hostname="test",
            os="darwin",
            os_version="14.0",
            username="user",
            org_device_id=None,
            scan_duration_ms=100,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="cursor",
                    servers=[
                        MCPServerConfig(name="s1", type="stdio"),
                    ],
                    config_scope="global",
                ),
            ],
        )

        payload = result.to_api_payload()
        server = payload["configurations"][0]["servers"][0]
        assert server["project_names"] is None

    @pytest.mark.parametrize(
        "legacy_transport",
        ["http", "streamablehttp", "streamable-http", "streamable_http"],
    )
    def test_api_payload_normalizes_http_type(self, legacy_transport):
        """Payload maps HTTP aliases to streaming-http."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test",
            hostname="test",
            os="darwin",
            os_version="14.0",
            username="user",
            org_device_id=None,
            scan_duration_ms=100,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="goose",
                    servers=[
                        MCPServerConfig(
                            name="s1",
                            type=legacy_transport,
                            url="https://example.com/mcp",
                        ),
                    ],
                    config_scope="global",
                ),
            ],
        )

        payload = result.to_api_payload()
        server = payload["configurations"][0]["servers"][0]
        assert server["type"] == "streaming-http"

    def test_api_payload_includes_invalid_command_flag(self):
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test",
            hostname="test",
            os="darwin",
            os_version="14.0",
            username="user",
            org_device_id=None,
            scan_duration_ms=100,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="cursor",
                    servers=[
                        MCPServerConfig(
                            name="invalid",
                            type="stdio",
                            command="npx\nrm -rf /",
                            command_invalid=True,
                        )
                    ],
                )
            ],
        )

        server = result.to_api_payload()["configurations"][0]["servers"][0]
        assert server["command_invalid"] is True


class TestScanResultToApiPayload:
    def test_converts_to_dict(self):
        """ScanResult can be converted to API payload."""
        result = scan_all_clients(scan_projects=False)
        payload = result.to_api_payload()
        assert isinstance(payload, dict)
        assert "device_id" in payload
        assert "configurations" in payload

    def test_payload_includes_all_fields(self):
        """API payload includes all expected fields."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test-device",
            hostname="test-host",
            os="darwin",
            os_version="14.0",
            username="testuser",
            org_device_id="mdm-123",
            scan_duration_ms=500,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="cursor",
                    client_version="0.1.0",
                    config_path="/path/to/config.json",
                    config_modified_at="2024-01-01T00:00:00Z",
                    config_scope="global",
                    servers=[
                        MCPServerConfig(
                            name="test-server",
                            type="stdio",
                            command="npx",
                            args=["-y", "test"],
                            env={
                                "API_KEY": "literal-secret",
                                "TOKEN": "${env:TOKEN}",
                                "PORT": 8080,
                            },
                            headers={
                                "Authorization": "Bearer ${TOKEN}",
                                "X-Api-Key": "literal-header-secret",
                            },
                            config_hash="abc123",
                        )
                    ],
                )
            ],
        )

        payload = result.to_api_payload()

        assert payload["device_id"] == "test-device"
        assert payload["hostname"] == "test-host"
        assert payload["os"] == "darwin"
        assert payload["os_version"] == "14.0"
        assert payload["username"] == "testuser"
        assert payload["org_device_id"] == "mdm-123"
        assert payload["scan_duration_ms"] == 500
        assert payload["collector_version"] == "1.0.0"
        assert len(payload["configurations"]) == 1

        config = payload["configurations"][0]
        assert config["client"] == "cursor"
        assert config["config_scope"] == "global"
        assert len(config["servers"]) == 1

        server = config["servers"][0]
        assert server["name"] == "test-server"
        assert server["type"] == "stdio"
        assert server["command"] == "npx"
        assert server["args"] == ["-y", "test"]
        assert server["env"] == {
            "API_KEY": "<redacted:len=14>",
            "TOKEN": "${env:TOKEN}",
            "PORT": "8080",
        }
        assert server["headers"] == {
            "Authorization": "Bearer ${TOKEN}",
            "X-Api-Key": "<redacted:len=21>",
        }
        assert server["config_hash"] == "abc123"

    def test_payload_coerces_messy_wire_values(self):
        """ENG-4074: numeric/None env values, numeric args, and off-enum
        transport types are coerced/clamped on the wire so one server can't
        422 the whole batch (defense in depth with the backend before-validator).
        """
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test-device",
            hostname="test-host",
            os="darwin",
            os_version="14.0",
            username="testuser",
            org_device_id=None,
            scan_duration_ms=100,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="cursor",
                    servers=[
                        MCPServerConfig(
                            name="messy",
                            type="websocket",
                            command="npx",
                            args=["--port", 8080, None],
                            env={"PORT": 8080, "TOKEN": None},
                            config_hash="abc",
                        )
                    ],
                )
            ],
        )

        server = result.to_api_payload()["configurations"][0]["servers"][0]

        # Off-enum type with no url clamps to stdio.
        assert server["type"] == "stdio"
        assert server["args"] == ["--port", "8080"]
        assert server["env"] == {"PORT": "8080"}

    def test_payload_clamps_off_enum_type_to_streaming_http_with_url(self):
        """A url-bearing off-enum transport clamps to streaming-http."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig

        result = ScanResult(
            device_id="test",
            hostname="test",
            os="darwin",
            os_version="14.0",
            username="user",
            org_device_id=None,
            scan_duration_ms=100,
            collector_version="1.0.0",
            configurations=[
                MCPClientConfig(
                    client="cursor",
                    servers=[
                        MCPServerConfig(
                            name="s1",
                            type="websocket",
                            url="https://example.com/mcp",
                        ),
                    ],
                ),
            ],
        )

        server = result.to_api_payload()["configurations"][0]["servers"][0]
        assert server["type"] == "streaming-http"


class TestToAgentReportPayload:
    """The per-agent submission payload: device context + redacted agents."""

    def _agent(self, *, framework_id="langchain", location="/Users/alice/proj"):
        from runlayer_cli.scan.agents.detect import DiscoveredAgent

        return DiscoveredAgent(
            location=location,
            name="proj",
            framework_id=framework_id,
            display_name="X",
            language="Python" if framework_id else None,
            confidence=0.9,
            margin=0.5,
            score=1.0,
            runner_up=None,
            runner_up_score=0.0,
            detection_method="static",
            evidence=[],
            manifests=[],
            languages=["Python"] if framework_id else [],
            agent_fingerprint=("a" * 64) if framework_id else None,
            scores=[],
        )

    def _scan_result(self, agents, *, username="alice"):
        return ScanResult(
            device_id="dev-1",
            hostname="host-1",
            os="darwin",
            os_version="14",
            username=username,
            org_device_id="mdm-9",
            scan_duration_ms=1,
            collector_version="1.0.0",
            configurations=[],
            agents=agents,
        )

    def test_includes_device_context_and_agents(self):
        payload = self._scan_result([self._agent()]).to_agent_report_payload()
        assert payload["device_id"] == "dev-1"
        assert payload["hostname"] == "host-1"
        assert payload["os"] == "darwin"
        assert payload["username"] == "alice"
        assert payload["org_device_id"] == "mdm-9"
        assert [a["framework_id"] for a in payload["agents"]] == ["langchain"]
        # Redacted per-agent shape (path home-username scrubbed).
        assert payload["agents"][0]["root_path"] == "/Users/<redacted>/proj"

    def test_drops_non_agents(self):
        real = self._agent(framework_id="langchain")
        unknown = self._agent(framework_id=None, location="/Users/alice/other")
        payload = self._scan_result([real, unknown]).to_agent_report_payload()
        assert [a["framework_id"] for a in payload["agents"]] == ["langchain"]

    def test_empty_agents_yields_empty_list(self):
        payload = self._scan_result([]).to_agent_report_payload()
        assert payload["agents"] == []

    def test_caps_at_max_agents(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service

        agents = [
            self._agent(location=f"/Users/alice/p{i}") for i in range(MAX_AGENTS + 5)
        ]
        logger = mock.Mock()
        monkeypatch.setattr(scan_service, "logger", logger)

        payload = self._scan_result(agents).to_agent_report_payload()

        assert len(payload["agents"]) == MAX_AGENTS
        # Cap bit -> warn so an outlier host's clamp is visible, parity with the
        # time-budget walk's truncated signal.
        logger.warning.assert_called_once_with(
            "agent_report_truncated",
            detected=MAX_AGENTS + 5,
            sent=MAX_AGENTS,
        )

    def test_no_truncation_warning_under_cap(self, monkeypatch):
        from runlayer_cli.scan import service as scan_service

        agents = [self._agent(location=f"/Users/alice/p{i}") for i in range(MAX_AGENTS)]
        logger = mock.Mock()
        monkeypatch.setattr(scan_service, "logger", logger)

        payload = self._scan_result(agents).to_agent_report_payload()

        assert len(payload["agents"]) == MAX_AGENTS
        logger.warning.assert_not_called()

    def test_device_username_threaded_into_non_home_path(self):
        # The scan's own username is redacted even outside the home layout.
        agent = self._agent(location="/opt/work/alice/proj")
        payload = self._scan_result([agent], username="alice").to_agent_report_payload()
        assert payload["agents"][0]["root_path"] == "/opt/work/<redacted>/proj"

    def test_missing_username_leaves_non_home_path(self):
        # No device username -> only the home layout is scrubbed (no over-reach).
        agent = self._agent(location="/opt/work/alice/proj")
        payload = self._scan_result([agent], username=None).to_agent_report_payload()
        assert payload["agents"][0]["root_path"] == "/opt/work/alice/proj"


class TestMergeExtensionsWithConfig:
    """Tests for merge_extensions_with_config function."""

    def test_adds_new_extensions(self):
        """Extensions not in config are added."""
        from runlayer_cli.scan.config_parser import MCPClientConfig
        from runlayer_cli.scan.orchestrator import merge_extensions_with_config

        config = MCPClientConfig(
            client="zed",
            config_path=None,
            config_modified_at=None,
            servers=[],
            config_scope="global",
        )

        merge_extensions_with_config(config, ["mcp-server-foo", "mcp-server-bar"])

        assert len(config.servers) == 2
        names = [s.name for s in config.servers]
        assert "mcp-server-foo" in names
        assert "mcp-server-bar" in names

    def test_skips_existing_servers(self):
        """Extensions already in config are not duplicated."""
        from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig
        from runlayer_cli.scan.orchestrator import merge_extensions_with_config

        existing_server = MCPServerConfig(
            name="mcp-server-foo",
            type="stdio",
            command="node",
            args=["server.js"],
            url=None,
            env=None,
            headers=None,
        )
        config = MCPClientConfig(
            client="zed",
            config_path=None,
            config_modified_at=None,
            servers=[existing_server],
            config_scope="global",
        )

        merge_extensions_with_config(config, ["mcp-server-foo", "mcp-server-bar"])

        assert len(config.servers) == 2
        # The original server should be preserved (with command)
        foo_server = next(s for s in config.servers if s.name == "mcp-server-foo")
        assert foo_server.command == "node"

    def test_handles_duplicate_extension_names(self):
        """Duplicate names in extension_names are deduplicated.

        This tests a specific bug fix where duplicate extension names
        would result in duplicate server entries because existing_names
        was not updated during the loop.
        """
        from runlayer_cli.scan.config_parser import MCPClientConfig
        from runlayer_cli.scan.orchestrator import merge_extensions_with_config

        config = MCPClientConfig(
            client="zed",
            config_path=None,
            config_modified_at=None,
            servers=[],
            config_scope="global",
        )

        # Pass duplicate extension names
        merge_extensions_with_config(
            config, ["mcp-server-foo", "mcp-server-bar", "mcp-server-foo"]
        )

        # Should only have 2 servers, not 3
        assert len(config.servers) == 2
        names = [s.name for s in config.servers]
        assert names.count("mcp-server-foo") == 1
        assert names.count("mcp-server-bar") == 1

    def test_extension_servers_have_config_hash(self):
        """Extension servers get a config hash."""
        from runlayer_cli.scan.config_parser import MCPClientConfig
        from runlayer_cli.scan.orchestrator import merge_extensions_with_config

        config = MCPClientConfig(
            client="zed",
            config_path=None,
            config_modified_at=None,
            servers=[],
            config_scope="global",
        )

        merge_extensions_with_config(config, ["mcp-server-test"])

        assert len(config.servers) == 1
        assert config.servers[0].config_hash != ""
        assert len(config.servers[0].config_hash) == 64  # SHA-256 hex


class TestScanSubmissionResultExitCode:
    """Exit-code precedence policy — unit-testable without e2e monkeypatching."""

    def test_clean_run_exits_zero(self):
        assert ScanSubmissionResult().exit_code == 0

    def test_response_only_exits_zero(self):
        result = ScanSubmissionResult(response={"servers_processed": 1})
        assert result.exit_code == 0

    def test_unsupported_only_exits_unsupported(self):
        result = ScanSubmissionResult(unsupported=["Shadow Skill Detection"])
        assert result.exit_code == EXIT_UNSUPPORTED == 2

    def test_failed_only_exits_submit_failed(self):
        result = ScanSubmissionResult(failed_submissions=["servers"])
        assert result.exit_code == EXIT_SUBMIT_FAILED == 3

    def test_failed_outranks_unsupported(self):
        result = ScanSubmissionResult(
            unsupported=["Shadow Skill Detection"],
            failed_submissions=["plugins"],
        )
        assert result.exit_code == EXIT_SUBMIT_FAILED


def _submission_scan_result(
    *,
    os_name: str = "darwin",
    servers: int = 0,
    clients: int = 0,
    skills: int = 0,
    plugins: int = 0,
    agents: int = 0,
    agent_definitions: int = 0,
    processes: int = 0,
    containers: int = 0,
    container_scan_requested: bool = False,
    containers_scanned: bool = False,
    stopped_containers_scanned: bool = False,
    container_images_scanned: bool = False,
    wsl_distros: int = 0,
    wsl_scanned: bool = False,
    skill_crawl_complete: bool = False,
    project_scan_depth: int = 7,
    project_scan_home: str | None = "/home/alice",
    project_skill_candidate_paths: tuple[str, ...] = (),
    global_skill_candidate_paths: tuple[str, ...] = (),
    machine_scope: bool = True,
    project_scan_requested: bool = True,
    agent_discovery_complete: bool = True,
    client_discovery_complete: bool = True,
    process_scan_requested: bool = False,
    processes_scanned: bool = False,
    completeness: ScanCompleteness | None = None,
):
    """Minimal stand-in for ScanResult exposing only what the orchestrator reads."""
    agent_list = [
        SimpleNamespace(
            is_agent=True,
            to_api_payload=lambda i=i: {
                "framework_id": f"fw-{i}",
                "language": "Python",
            },
        )
        for i in range(agents)
    ]
    definition_list = [
        SimpleNamespace(
            name=f"agent-definition-{i}",
            to_api_payload=lambda i=i: {
                "client": "cursor",
                "name": f"agent-definition-{i}",
                "scope": "project",
                "path": f"/workspace/.cursor/agents/{i}.md",
                "content_hash": f"{i:064x}",
            },
        )
        for i in range(agent_definitions)
    ]
    scan_session_id = uuid.UUID("00000000-0000-4000-8000-000000000001")
    scan_started_at = datetime.datetime(
        2026,
        9,
        3,
        12,
        0,
        tzinfo=datetime.timezone.utc,
    )
    return SimpleNamespace(
        device_id="device-1",
        scan_session_id=scan_session_id,
        scan_started_at=scan_started_at,
        completeness=completeness or ScanCompleteness(),
        hostname="host",
        os=os_name,
        os_version="14",
        username="alex",
        org_device_id=None,
        serial_number=None,
        machine_scope=machine_scope,
        project_scan_requested=project_scan_requested,
        agent_discovery_complete=agent_discovery_complete,
        client_discovery_complete=client_discovery_complete,
        process_scan_requested=process_scan_requested,
        processes_scanned=processes_scanned,
        total_servers=servers,
        detected_clients=[
            SimpleNamespace(client=f"client-{i}") for i in range(clients)
        ],
        skills=[
            SimpleNamespace(
                name=f"skill-{i}",
                identifier=f"skill-{i}",
                container_id=None,
                wsl_distro=None,
            )
            for i in range(skills)
        ],
        plugins=[
            SimpleNamespace(
                name=f"plugin-{i}",
                identifier=f"plugin-{i}",
                container_id=None,
            )
            for i in range(plugins)
        ],
        agents=agent_list,
        agent_definitions=definition_list,
        processes=[SimpleNamespace(pid=1000 + i) for i in range(processes)],
        containers=[
            SimpleNamespace(container_id=f"container-{i}") for i in range(containers)
        ],
        container_scan_requested=container_scan_requested,
        containers_scanned=containers_scanned,
        stopped_containers_scanned=stopped_containers_scanned,
        container_images_scanned=container_images_scanned,
        wsl_distros=[SimpleNamespace(name=f"distro-{i}") for i in range(wsl_distros)],
        wsl_scanned=wsl_scanned,
        skill_crawl_complete=skill_crawl_complete,
        project_scan_depth=project_scan_depth,
        project_scan_home=project_scan_home,
        project_skill_candidate_paths=list(project_skill_candidate_paths),
        global_skill_candidate_paths=list(global_skill_candidate_paths),
        to_api_payload=lambda: {
            "device_id": "device-1",
            "scan_session_id": str(scan_session_id),
            "scan_started_at": scan_started_at.isoformat(),
        },
        to_agent_report_payload=lambda: {
            "device_id": "device-1",
            "scan_session_id": str(scan_session_id),
            "scan_started_at": scan_started_at.isoformat(),
            "agents": [a.to_api_payload() for a in agent_list],
        },
        to_agent_definition_report_payload=lambda: {
            "device_id": "device-1",
            "scan_session_id": str(scan_session_id),
            "scan_started_at": scan_started_at.isoformat(),
            "agent_definitions": [
                definition.to_api_payload() for definition in definition_list
            ],
        },
    )


class TestSubmitDiscoveredServers:
    """Server submission taxonomy — the per-category peer of skills/plugins."""

    def test_success_returns_status_and_response(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {
            "servers_processed": 3,
            "shadow_servers_found": 1,
            "managed_servers_matched": 0,
        }

        result = submit_discovered_servers(client, _submission_scan_result(servers=3))

        assert isinstance(result, ServerSubmission)
        assert result.status == "success"
        assert result.response == client.submit_mcp_watch_scan.return_value
        client.submit_mcp_watch_scan.assert_called_once_with(
            {
                "device_id": "device-1",
                "scan_session_id": "00000000-0000-4000-8000-000000000001",
                "scan_started_at": "2026-09-03T12:00:00+00:00",
            }
        )

    def test_unsupported_response_has_no_body(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"unsupported": True}

        result = submit_discovered_servers(client, _submission_scan_result(servers=1))

        assert result.status == "unsupported"
        assert result.response is None

    def test_transport_error_is_failed(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        client.submit_mcp_watch_scan.side_effect = httpx.ConnectError(
            "down", request=request
        )

        result = submit_discovered_servers(client, _submission_scan_result(servers=1))

        assert result.status == "failed"
        assert result.response is None

    def test_server_5xx_is_failed(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(500, request=request)
        client.submit_mcp_watch_scan.side_effect = httpx.HTTPStatusError(
            "boom", request=request, response=response
        )

        result = submit_discovered_servers(client, _submission_scan_result(servers=1))

        assert result.status == "failed"

    @pytest.mark.parametrize("status", [401, 403])
    def test_auth_error_propagates(self, status):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(status, request=request)
        client.submit_mcp_watch_scan.side_effect = httpx.HTTPStatusError(
            "unauthorized", request=request, response=response
        )

        with pytest.raises(httpx.HTTPStatusError):
            submit_discovered_servers(client, _submission_scan_result(servers=1))

    def test_422_captures_validation_detail_and_server_count(self):
        """ENG-4074: a 422 must be diagnosable — log the sanitized backend
        detail (loc/type/msg) plus how many servers were in the batch.
        """
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        detail = [
            {
                "loc": ["body", "configurations", 0, "servers", 0, "env", "PORT"],
                "type": "string_type",
                "msg": "Input should be a valid string",
            }
        ]
        response = httpx.Response(422, request=request, json={"detail": detail})
        client.submit_mcp_watch_scan.side_effect = httpx.HTTPStatusError(
            "unprocessable", request=request, response=response
        )

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            result = submit_discovered_servers(
                client, _submission_scan_result(servers=5)
            )

        assert result.status == "failed"
        warning_mock.assert_called_once()
        assert warning_mock.call_args.args == ("mcp_watch_scan_submission_failed",)
        kwargs = warning_mock.call_args.kwargs
        assert kwargs["status_code"] == 422
        assert kwargs["server_count"] == 5
        assert kwargs["validation_detail"] == detail

    def test_422_non_json_body_falls_back_to_text(self):
        """A 422 without a JSON body still captures a truncated text snippet."""
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(422, request=request, text="not json")
        client.submit_mcp_watch_scan.side_effect = httpx.HTTPStatusError(
            "unprocessable", request=request, response=response
        )

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            result = submit_discovered_servers(
                client, _submission_scan_result(servers=1)
            )

        assert result.status == "failed"
        warning_mock.assert_called_once()
        assert warning_mock.call_args.kwargs["validation_detail"] == "not json"

    def test_non_422_error_has_no_validation_detail(self):
        """5xx failures record server_count but no validation_detail."""
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(500, request=request)
        client.submit_mcp_watch_scan.side_effect = httpx.HTTPStatusError(
            "boom", request=request, response=response
        )

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            result = submit_discovered_servers(
                client, _submission_scan_result(servers=2)
            )

        assert result.status == "failed"
        warning_mock.assert_called_once()
        kwargs = warning_mock.call_args.kwargs
        assert kwargs["validation_detail"] is None
        assert kwargs["server_count"] == 2


class TestSubmitDiscoveredAgents:
    """Agent submission taxonomy — the per-category peer of servers/skills."""

    def test_no_agents_is_success_without_call(self):
        client = mock.MagicMock()

        result = submit_discovered_agents(client, _submission_scan_result(agents=0))

        assert result == "success"
        client.submit_agents.assert_not_called()

    def test_success(self):
        client = mock.MagicMock()
        client.submit_agents.return_value = {"agents_processed": 2}

        result = submit_discovered_agents(client, _submission_scan_result(agents=2))

        assert result == "success"
        client.submit_agents.assert_called_once()

    def test_unsupported_response(self):
        client = mock.MagicMock()
        client.submit_agents.return_value = {"unsupported": True}

        result = submit_discovered_agents(client, _submission_scan_result(agents=1))

        assert result == "unsupported"

    def test_transport_error_is_failed(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        client.submit_agents.side_effect = httpx.ConnectError("down", request=request)

        result = submit_discovered_agents(client, _submission_scan_result(agents=1))

        assert result == "failed"

    def test_server_5xx_is_failed(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(500, request=request)
        client.submit_agents.side_effect = httpx.HTTPStatusError(
            "boom", request=request, response=response
        )

        result = submit_discovered_agents(client, _submission_scan_result(agents=1))

        assert result == "failed"

    @pytest.mark.parametrize("status", [401, 403])
    def test_auth_error_propagates(self, status):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(status, request=request)
        client.submit_agents.side_effect = httpx.HTTPStatusError(
            "unauthorized", request=request, response=response
        )

        with pytest.raises(httpx.HTTPStatusError):
            submit_discovered_agents(client, _submission_scan_result(agents=1))


class TestSubmitDiscoveredAgentDefinitions:
    def test_success_submits_dedicated_report(self):
        client = mock.MagicMock()
        client.submit_agent_definitions.return_value = {
            "agent_definitions": [],
            "created_count": 1,
            "updated_count": 0,
        }

        result = submit_discovered_agent_definitions(
            client, _submission_scan_result(agent_definitions=1)
        )

        assert result == "success"
        client.submit_agent_definitions.assert_called_once()

    def test_unsupported_response(self):
        client = mock.MagicMock()
        client.submit_agent_definitions.return_value = {"unsupported": True}

        result = submit_discovered_agent_definitions(
            client, _submission_scan_result(agent_definitions=1)
        )

        assert result == "unsupported"


def _expected_presence_state(scan_result):
    return build_state(
        SkillPresenceParams(
            project_depth=scan_result.project_scan_depth,
            home=scan_result.project_scan_home,
        ),
        project_paths=scan_result.project_skill_candidate_paths,
        global_paths=scan_result.global_skill_candidate_paths,
    )


class TestReconcileSkillPresence:
    def test_first_complete_crawl_saves_baseline_without_submit(self, tmp_path):
        state_path = tmp_path / "presence.json"
        client = mock.MagicMock()
        scan_result = _submission_scan_result(
            skill_crawl_complete=True,
            project_skill_candidate_paths=("/project/current",),
            global_skill_candidate_paths=("/global/current",),
        )

        result = reconcile_skill_presence(
            client,
            scan_result,
            state_path=state_path,
        )

        assert result == "success"
        client.submit_skill_removals.assert_not_called()
        assert load_state(state_path) == _expected_presence_state(scan_result)

    def test_baseline_write_failure_is_best_effort(self, tmp_path, monkeypatch):
        client = mock.MagicMock()
        monkeypatch.setattr(
            "runlayer_cli.scan.service.save_presence_state",
            lambda *_args, **_kwargs: False,
        )

        result = reconcile_skill_presence(
            client,
            _submission_scan_result(skill_crawl_complete=True),
            state_path=tmp_path / "presence.json",
        )

        assert result == "success"
        client.submit_skill_removals.assert_not_called()

    def test_incomplete_crawl_neither_reads_writes_nor_submits(
        self, tmp_path, monkeypatch
    ):
        state_path = tmp_path / "presence.json"
        client = mock.MagicMock()
        load_mock = mock.Mock(side_effect=AssertionError("state read"))
        save_mock = mock.Mock(side_effect=AssertionError("state write"))
        monkeypatch.setattr("runlayer_cli.scan.service.load_presence_state", load_mock)
        monkeypatch.setattr("runlayer_cli.scan.service.save_presence_state", save_mock)

        result = reconcile_skill_presence(
            client,
            _submission_scan_result(
                skill_crawl_complete=False,
                project_skill_candidate_paths=("/project/current",),
            ),
            state_path=state_path,
        )

        assert result == "success"
        load_mock.assert_not_called()
        save_mock.assert_not_called()
        client.submit_skill_removals.assert_not_called()
        assert not state_path.exists()

    def test_changed_params_replace_baseline_without_submit(self, tmp_path):
        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            project_paths=("/project/removed",),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        scan_result = _submission_scan_result(
            skill_crawl_complete=True,
            project_scan_depth=8,
        )

        result = reconcile_skill_presence(
            client,
            scan_result,
            state_path=state_path,
        )

        assert result == "success"
        client.submit_skill_removals.assert_not_called()
        assert load_state(state_path) == _expected_presence_state(scan_result)

    def test_deleted_project_still_submits_its_skill_removals(self, tmp_path):
        """A deleted repo changes the discovered project set in the same scan
        that drops its skills; that must not reset the baseline."""
        state_path = tmp_path / "presence.json"
        deleted_repo_skill = "/home/alice/repo/.agents/skills/release"
        kept_skill = "/home/alice/other/.agents/skills/kept"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            project_paths=(deleted_repo_skill, kept_skill),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        client.submit_skill_removals.return_value = {"removed": 1}
        scan_result = _submission_scan_result(
            skill_crawl_complete=True,
            project_skill_candidate_paths=(kept_skill,),
        )

        result = reconcile_skill_presence(
            client,
            scan_result,
            state_path=state_path,
        )

        assert result == "success"
        assert client.submit_skill_removals.call_args.args[0] == [
            path_hash(deleted_repo_skill)
        ]
        assert load_state(state_path) == _expected_presence_state(scan_result)

    def test_successful_removal_advances_state(self, tmp_path):
        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            project_paths=("/project/removed", "/project/kept"),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        client.submit_skill_removals.return_value = {"removed": 1}
        scan_result = _submission_scan_result(
            skill_crawl_complete=True,
            project_skill_candidate_paths=("/project/kept",),
        )

        result = reconcile_skill_presence(
            client,
            scan_result,
            state_path=state_path,
        )

        assert result == "success"
        client.submit_skill_removals.assert_called_once()
        assert client.submit_skill_removals.call_args.args[0] == [
            path_hash("/project/removed")
        ]
        assert client.submit_skill_removals.call_args.args[1]["device_id"] == "device-1"
        assert load_state(state_path) == _expected_presence_state(scan_result)

    def test_removal_state_write_failure_is_best_effort(self, tmp_path, monkeypatch):
        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            project_paths=("/project/removed",),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        client.submit_skill_removals.return_value = {"removed": 1}
        monkeypatch.setattr(
            "runlayer_cli.scan.service.save_presence_state",
            lambda *_args, **_kwargs: False,
        )

        result = reconcile_skill_presence(
            client,
            _submission_scan_result(skill_crawl_complete=True),
            state_path=state_path,
        )

        assert result == "success"
        client.submit_skill_removals.assert_called_once()
        assert load_state(state_path) == previous

    def test_unsupported_removal_keeps_previous_state(self, tmp_path):
        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            project_paths=("/project/removed",),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        client.submit_skill_removals.return_value = {"unsupported": True}

        result = reconcile_skill_presence(
            client,
            _submission_scan_result(skill_crawl_complete=True),
            state_path=state_path,
        )

        assert result == "success"
        assert load_state(state_path) == previous

    def test_non_auth_failure_keeps_previous_state(self, tmp_path):
        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            project_paths=("/project/removed",),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        client.submit_skill_removals.side_effect = RuntimeError("backend unavailable")

        result = reconcile_skill_presence(
            client,
            _submission_scan_result(skill_crawl_complete=True),
            state_path=state_path,
        )

        assert result == "failed"
        assert load_state(state_path) == previous

    @pytest.mark.parametrize("status", [401, 403])
    def test_auth_failure_propagates(self, tmp_path, status):
        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            project_paths=("/project/removed",),
        )
        assert save_state(previous, state_path)
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(status, request=request)
        client = mock.MagicMock()
        client.submit_skill_removals.side_effect = httpx.HTTPStatusError(
            "unauthorized",
            request=request,
            response=response,
        )

        with pytest.raises(httpx.HTTPStatusError):
            reconcile_skill_presence(
                client,
                _submission_scan_result(skill_crawl_complete=True),
                state_path=state_path,
            )

        assert load_state(state_path) == previous


class TestSubmitScanResults:
    """Orchestrator maps each category's status into the result buckets."""

    def test_category_surface_contract_matches_backend_manifest_pairs(self):
        expected_pairs = {
            ("mcp", "host_static"),
            ("mcp", "host_runtime"),
            ("mcp", "container"),
            ("mcp", "wsl"),
            ("mcp", "wsl_runtime"),
            ("client", "host_static"),
            ("client", "host_runtime"),
            ("client", "container"),
            ("client", "wsl"),
            ("client", "wsl_runtime"),
            ("skill", "host_static"),
            ("skill", "container"),
            ("skill", "wsl"),
            ("plugin", "host_static"),
            ("plugin", "host_runtime"),
            ("plugin", "container"),
            ("plugin", "device"),
            ("agent", "host_static"),
            ("agent", "host_runtime"),
            ("agent", "wsl"),
            ("agent", "wsl_runtime"),
            ("agent_definition", "host_static"),
            ("agent_definition", "container"),
            ("agent_definition", "wsl"),
        }

        assert {
            (category, surface)
            for category, surfaces in CATEGORY_SURFACES.items()
            for surface in surfaces
        } == expected_pairs

    @pytest.mark.parametrize(("category", "surfaces"), CATEGORY_SURFACES.items())
    def test_category_surface_contract_drives_all_consumers(
        self,
        category,
        surfaces,
    ):
        from runlayer_cli.scan import service as scan_service

        submission = ScanSubmissionResult()
        entries = _scan_manifest_payload(
            _submission_scan_result(),
            submission,
        )["entries"]
        manifest_surfaces = tuple(
            entry["surface"] for entry in entries if entry["category"] == category
        )
        assert manifest_surfaces == surfaces
        assert {
            surface
            for outcome_category, surface in submission.surface_outcomes
            if outcome_category == category
        } == set(surfaces)

        recorded = ScanSubmissionResult()
        recorded.surface_outcomes.clear()
        scan_service._record_surface_outcomes(
            recorded,
            category=category,
            outcome="failed",
        )
        assert recorded.surface_outcomes == {
            (category, surface): "failed" for surface in surfaces
        }

        for surface in surfaces:
            consumed = ScanSubmissionResult()
            scan_service._consume_backend_surface_failures(
                consumed,
                {
                    "incomplete_surfaces": [
                        {
                            "category": category,
                            "surface": surface,
                            "reason": "backend_failure",
                        }
                    ]
                },
            )
            assert consumed.incomplete_surfaces[(category, surface)] == (
                "backend_failure"
            )

        invalid_surface = next(
            surface
            for valid_surfaces in CATEGORY_SURFACES.values()
            for surface in valid_surfaces
            if surface not in surfaces
        )
        rejected = ScanSubmissionResult()
        scan_service._consume_backend_surface_failures(
            rejected,
            {
                "incomplete_surfaces": [
                    {
                        "category": category,
                        "surface": invalid_surface,
                        "reason": "invalid_pair",
                    }
                ]
            },
        )
        assert rejected.incomplete_surfaces == {}

    @pytest.mark.parametrize(
        ("category", "surface"),
        [
            (category, surface)
            for category, surfaces in CATEGORY_SURFACES.items()
            for surface in surfaces
        ],
    )
    def test_missing_expected_surface_outcome_fails_loud(
        self,
        category,
        surface,
    ):
        submission = ScanSubmissionResult()
        del submission.surface_outcomes[(category, surface)]

        with pytest.raises(KeyError):
            _scan_manifest_payload(_submission_scan_result(), submission)

    def test_empty_scan_still_sends_authoritative_manifest(self):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}

        submission = submit_scan_results(client, _submission_scan_result())

        client.submit_mcp_watch_scan.assert_not_called()
        client.submit_scan_manifest.assert_called_once()
        payload = client.submit_scan_manifest.call_args.args[0]
        assert payload["scan_session_id"] == ("00000000-0000-4000-8000-000000000001")
        assert payload["scan_started_at"] == "2026-09-03T12:00:00+00:00"
        assert payload["device_id"] == "device-1"
        entries = {
            (entry["category"], entry["surface"]): entry for entry in payload["entries"]
        }
        assert all(
            entries[(category, "host_static")]["complete"]
            for category in (
                "mcp",
                "skill",
                "plugin",
                "agent",
                "agent_definition",
            )
        )
        assert entries[("client", "host_static")] == {
            "category": "client",
            "surface": "host_static",
            "complete": True,
        }
        assert entries[("client", "host_runtime")]["complete"] is False
        assert entries[("client", "container")]["complete"] is False
        assert submission.category_outcomes == {
            "mcp": "success",
            "client": "success",
            "skill": "success",
            "plugin": "success",
            "agent": "success",
            "agent_definition": "success",
        }

    @pytest.mark.parametrize(
        ("scan_flags", "expected_completeness"),
        [
            ({}, (True, False, False)),
            (
                {
                    "os_name": "windows",
                    "wsl_scanned": True,
                },
                (True, False, False),
            ),
            (
                {
                    "process_scan_requested": True,
                    "processes_scanned": True,
                },
                (True, True, False),
            ),
            (
                {
                    "process_scan_requested": True,
                    "processes_scanned": True,
                    "container_scan_requested": True,
                    "containers_scanned": True,
                },
                (True, True, True),
            ),
            (
                {
                    "container_scan_requested": True,
                    "containers_scanned": False,
                },
                (True, False, False),
            ),
            (
                {
                    "os_name": "windows",
                    "process_scan_requested": True,
                    "processes_scanned": True,
                    "container_scan_requested": True,
                    "containers_scanned": True,
                },
                (False, True, True),
            ),
            (
                {
                    "os_name": "windows",
                    "wsl_scanned": True,
                    "process_scan_requested": True,
                    "processes_scanned": True,
                    "container_scan_requested": True,
                    "containers_scanned": True,
                },
                (True, True, True),
            ),
        ],
        ids=[
            "darwin-static-only",
            "windows-static-only",
            "static-and-runtime",
            "all-channels",
            "container-runtime-unavailable",
            "windows-wsl-unavailable",
            "windows-wsl-complete",
        ],
    )
    def test_client_manifest_authority_tracks_each_evidence_surface(
        self,
        scan_flags,
        expected_completeness,
    ):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}
        client.submit_scan_manifest.return_value = {"reconciled": 0}

        submit_scan_results(client, _submission_scan_result(**scan_flags))

        client_entries = {
            entry["surface"]: entry["complete"]
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
            if entry["category"] == "client"
        }
        assert (
            tuple(
                client_entries[surface]
                for surface in ("host_static", "host_runtime", "container")
            )
            == expected_completeness
        )

    @pytest.mark.parametrize(
        ("scan_flags", "expected_complete"),
        [
            (
                {
                    "os_name": "windows",
                    "wsl_scanned": True,
                },
                False,
            ),
            (
                {
                    "os_name": "windows",
                    "process_scan_requested": True,
                    "processes_scanned": True,
                },
                False,
            ),
            (
                {
                    "os_name": "windows",
                    "wsl_scanned": True,
                    "process_scan_requested": True,
                    "processes_scanned": True,
                },
                True,
            ),
        ],
        ids=["wsl-only", "runtime-only", "wsl-runtime-complete"],
    )
    def test_client_wsl_runtime_manifest_requires_both_scans(
        self,
        scan_flags,
        expected_complete,
    ):
        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(
                _submission_scan_result(**scan_flags),
                ScanSubmissionResult(),
            )["entries"]
        }

        assert entries[("client", "wsl_runtime")]["complete"] is expected_complete

    def test_successful_empty_process_scan_submits_before_authoritative_manifest(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}
        client.submit_scan_manifest.return_value = {"reconciled": 0}

        submission = submit_scan_results(
            client,
            _submission_scan_result(
                process_scan_requested=True,
                processes_scanned=True,
            ),
        )

        assert [call[0] for call in client.method_calls] == [
            "submit_mcp_watch_scan",
            "submit_scan_manifest",
        ]
        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("mcp", "host_runtime")]["complete"] is True
        assert entries[("plugin", "host_runtime")]["complete"] is True
        assert entries[("agent", "host_runtime")]["complete"] is True
        assert submission.response == client.submit_mcp_watch_scan.return_value
        assert submission.category_outcomes["mcp"] == "success"
        assert submission.category_outcomes["client"] == "success"

    @pytest.mark.parametrize(
        ("processes_scanned", "runtime_incomplete"),
        [
            (False, False),
            (True, True),
        ],
    )
    def test_empty_incomplete_process_scan_does_not_submit_shared_inventory(
        self,
        processes_scanned,
        runtime_incomplete,
    ):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        completeness = ScanCompleteness()
        if runtime_incomplete:
            completeness.runtime.mark_incomplete("runtime_extension_root_capped")

        submit_scan_results(
            client,
            _submission_scan_result(
                process_scan_requested=True,
                processes_scanned=processes_scanned,
                completeness=completeness,
            ),
        )

        client.submit_mcp_watch_scan.assert_not_called()
        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("mcp", "host_runtime")]["complete"] is False

    def test_agent_wire_cap_suppresses_all_agent_surface_authority(self):
        result = _submission_scan_result(agents=MAX_AGENTS + 1)

        payload = _scan_manifest_payload(
            result,
            ScanSubmissionResult(),
        )
        agent_entries = [
            entry for entry in payload["entries"] if entry["category"] == "agent"
        ]

        assert agent_entries
        assert all(entry["complete"] is False for entry in agent_entries)
        assert {entry["reason"] for entry in agent_entries} == {
            "agent_payload_truncated"
        }

    def test_definition_wire_cap_suppresses_all_definition_surface_authority(self):
        result = _submission_scan_result(agent_definitions=MAX_AGENT_DEFINITIONS + 1)

        payload = _scan_manifest_payload(
            result,
            ScanSubmissionResult(),
        )
        definition_entries = [
            entry
            for entry in payload["entries"]
            if entry["category"] == "agent_definition"
        ]

        assert definition_entries
        assert all(entry["complete"] is False for entry in definition_entries)
        assert {entry["reason"] for entry in definition_entries} == {
            "agent_definition_payload_truncated"
        }

    def test_definition_host_failure_does_not_freeze_complete_container_surface(self):
        completeness = ScanCompleteness()
        completeness.agent_definition_host_static.mark_incomplete(
            "agent_definition_marker_read_failed"
        )
        result = _submission_scan_result(
            container_scan_requested=True,
            containers_scanned=True,
            completeness=completeness,
        )

        payload = _scan_manifest_payload(
            result,
            ScanSubmissionResult(),
        )
        entries = {
            (entry["category"], entry["surface"]): entry for entry in payload["entries"]
        }

        assert entries[("agent_definition", "host_static")]["complete"] is False
        assert entries[("agent_definition", "container")]["complete"] is True

    def test_fully_throttled_skill_scan_is_success_with_incomplete_surface(self):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}

        def throttle_everything(*_args, throttled_surfaces, **_kwargs):
            throttled_surfaces.add("host_static")
            return "success"

        with (
            mock.patch.object(
                scan_service,
                "submit_discovered_skills",
                side_effect=throttle_everything,
            ),
            mock.patch.object(
                scan_service, "reconcile_skill_presence", return_value="success"
            ) as presence,
        ):
            submission = submit_scan_results(
                client,
                _submission_scan_result(skills=2),
                artifact_cache=mock.MagicMock(),
            )

        assert submission.exit_code == 0
        assert submission.failed_submissions == []
        assert submission.unsupported == []
        assert submission.category_outcomes["skill"] == "success"
        presence.assert_called_once()
        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("skill", "host_static")] == {
            "category": "skill",
            "surface": "host_static",
            "complete": False,
            "reason": "resubmit_throttled",
        }
        assert entries[("mcp", "host_static")]["complete"] is True

    def test_skill_free_scan_resets_the_resubmit_baseline(self):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        cache = mock.MagicMock()

        submit_scan_results(client, _submission_scan_result(), artifact_cache=cache)

        cache.retain_submissions.assert_called_once_with(set(), kind="skill")

    def test_manifest_is_last_and_reuses_session_id_for_every_submit(self):
        client = mock.MagicMock()
        client.submit_agents.return_value = {"agents_processed": 1}
        client.submit_agent_definitions.return_value = {
            "agent_definitions": [],
            "created_count": 1,
            "updated_count": 0,
        }
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 1}
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        scan_result = _submission_scan_result(
            servers=1,
            agents=1,
            agent_definitions=1,
        )

        submit_scan_results(client, scan_result)

        expected_session_id = "00000000-0000-4000-8000-000000000001"
        assert client.submit_agents.call_args.args[0]["scan_session_id"] == (
            expected_session_id
        )
        assert (
            client.submit_agent_definitions.call_args.args[0]["scan_session_id"]
            == expected_session_id
        )
        assert (
            client.submit_mcp_watch_scan.call_args.args[0]["scan_session_id"]
            == expected_session_id
        )
        assert (
            client.submit_scan_manifest.call_args.args[0]["scan_session_id"]
            == expected_session_id
        )
        assert {
            client.submit_agents.call_args.args[0]["scan_started_at"],
            client.submit_agent_definitions.call_args.args[0]["scan_started_at"],
            client.submit_mcp_watch_scan.call_args.args[0]["scan_started_at"],
            client.submit_scan_manifest.call_args.args[0]["scan_started_at"],
        } == {"2026-09-03T12:00:00+00:00"}
        assert client.method_calls[-1][0] == "submit_scan_manifest"

    def test_unexpected_agent_endpoint_failure_still_submits_manifest(self):
        client = mock.MagicMock()
        client.submit_agents.side_effect = RuntimeError("invalid response")
        client.submit_scan_manifest.return_value = {"reconciled": 0}

        submission = submit_scan_results(
            client,
            _submission_scan_result(agents=1),
        )

        client.submit_scan_manifest.assert_called_once()
        client.submit_mcp_watch_scan.assert_not_called()
        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("agent", "host_static")]["reason"] == "submission_failed"
        assert entries[("agent", "host_runtime")]["reason"] == (
            "runtime_discovery_incomplete"
        )
        assert submission.failed_submissions == ["agents"]

    def test_failed_category_is_incomplete_without_poisoning_other_categories(self):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        scan_result = _submission_scan_result(plugins=1)

        with mock.patch(
            "runlayer_cli.scan.service.submit_discovered_plugins",
            return_value="failed",
        ):
            submission = submit_scan_results(client, scan_result)

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("plugin", "host_static")] == {
            "category": "plugin",
            "surface": "host_static",
            "complete": False,
            "reason": "submission_failed",
        }
        assert entries[("skill", "host_static")]["complete"] is True
        assert submission.category_outcomes["plugin"] == "failed"
        assert submission.category_outcomes["skill"] == "success"

    def test_partial_plugin_submission_gates_only_failed_surface(self):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        scan_result = _submission_scan_result(
            plugins=1,
            process_scan_requested=True,
            processes_scanned=True,
        )

        def partially_fail(*_args, failed_surfaces, **_kwargs):
            failed_surfaces.add("host_runtime")
            return "success"

        with mock.patch(
            "runlayer_cli.scan.service.submit_discovered_plugins",
            side_effect=partially_fail,
        ):
            submission = submit_scan_results(client, scan_result)

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("plugin", "host_runtime")]["complete"] is False
        assert entries[("plugin", "host_runtime")]["reason"] == "submission_failed"
        assert entries[("plugin", "host_static")]["complete"] is True
        assert submission.failed_submissions == ["plugins"]

    def test_failed_skill_before_unsupported_skill_remains_failed(self):
        from runlayer_cli.scan.skill_scanner import (
            ARTIFACT_SKILL_MD,
            DiscoveredSkillArtifact,
            SkillFile,
        )

        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}
        client.submit_skill_fingerprints.return_value = {"unsupported": True}
        client.submit_skill_fingerprint.side_effect = [
            {"known": False},
            {"unsupported": True},
        ]
        client.submit_skill.side_effect = httpx.ConnectError(
            "down",
            request=httpx.Request("POST", "https://example.com/skills"),
        )
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        scan_result = _submission_scan_result(
            container_scan_requested=True,
            containers_scanned=True,
        )
        scan_result.skills = [
            DiscoveredSkillArtifact(
                name="failed-container-skill",
                path="/container-skill",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="failed-container-skill",
                files=[SkillFile(title="SKILL.md", content="# container")],
                container_id="container-1",
            ),
            DiscoveredSkillArtifact(
                name="unsupported-static-skill",
                path="/static-skill",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="unsupported-static-skill",
                files=[SkillFile(title="SKILL.md", content="# static")],
            ),
        ]

        submission = submit_scan_results(client, scan_result)

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert submission.category_outcomes["skill"] == "failed"
        assert submission.failed_submissions == ["skills"]
        assert submission.unsupported == []
        assert submission.surface_outcomes[("skill", "container")] == "failed"
        assert submission.incomplete_surfaces[("skill", "container")] == (
            "submission_failed"
        )
        assert entries[("skill", "container")]["reason"] == "submission_failed"
        assert submission.exit_code == EXIT_SUBMIT_FAILED

    def test_pure_unsupported_skill_submission_remains_unsupported(self):
        from runlayer_cli.scan.skill_scanner import (
            ARTIFACT_SKILL_MD,
            DiscoveredSkillArtifact,
        )

        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {"unsupported": True}
        client.submit_skill_fingerprint.return_value = {"unsupported": True}
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        scan_result = _submission_scan_result()
        scan_result.skills = [
            DiscoveredSkillArtifact(
                name="unsupported-skill",
                path="/unsupported-skill",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="unsupported-skill",
            )
        ]

        submission = submit_scan_results(client, scan_result)

        assert submission.category_outcomes["skill"] == "unsupported"
        assert submission.failed_submissions == []
        assert submission.unsupported == ["Shadow Skill Detection"]
        assert all(
            submission.surface_outcomes[("skill", surface)] == "unsupported"
            for surface in CATEGORY_SURFACES["skill"]
        )
        assert submission.exit_code == EXIT_UNSUPPORTED

    def test_category_specific_incomplete_reason_does_not_poison_peers(self):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        completeness = ScanCompleteness()
        completeness.skill_host_static.mark_incomplete("project_skill_scan_capped")

        submit_scan_results(
            client,
            _submission_scan_result(completeness=completeness),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("skill", "host_static")]["reason"] == (
            "project_skill_scan_capped"
        )
        assert entries[("skill", "host_static")]["complete"] is False
        assert entries[("mcp", "host_static")]["complete"] is True
        assert entries[("plugin", "host_static")]["complete"] is True

    @pytest.mark.parametrize(
        ("surface", "scan_kwargs", "expected_reason"),
        [
            (
                "host_static",
                {"project_scan_requested": False},
                "static_discovery_incomplete",
            ),
            (
                "host_runtime",
                {},
                "runtime_discovery_incomplete",
            ),
        ],
    )
    def test_unrequested_plugin_host_channel_does_not_blame_wsl(
        self,
        surface,
        scan_kwargs,
        expected_reason,
    ):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}

        submit_scan_results(
            client,
            _submission_scan_result(**scan_kwargs),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("plugin", surface)]["complete"] is False
        assert entries[("plugin", surface)]["reason"] == expected_reason

    @pytest.mark.parametrize("surface", ["host_static", "host_runtime"])
    def test_windows_plugin_host_authority_requires_complete_wsl(
        self,
        surface,
    ):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        completeness = ScanCompleteness()
        completeness.plugin_host_static.mark_incomplete("wsl_home_discovery_capped")

        submit_scan_results(
            client,
            _submission_scan_result(
                os_name="windows",
                process_scan_requested=True,
                processes_scanned=True,
                wsl_scanned=True,
                completeness=completeness,
            ),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("plugin", surface)] == {
            "category": "plugin",
            "surface": surface,
            "complete": False,
            "reason": "wsl_home_discovery_capped",
        }

    @pytest.mark.parametrize("surface", ["host_static", "host_runtime"])
    def test_windows_plugin_host_authority_ignores_wsl_project_walk(
        self,
        surface,
    ):
        completeness = ScanCompleteness()
        completeness.wsl_static.mark_incomplete("wsl_project_scan_disabled")

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(
                _submission_scan_result(
                    os_name="windows",
                    process_scan_requested=True,
                    processes_scanned=True,
                    wsl_scanned=True,
                    completeness=completeness,
                ),
                ScanSubmissionResult(),
            )["entries"]
        }

        assert entries[("plugin", surface)]["complete"] is True

    def test_windows_client_host_authority_ignores_disabled_wsl_project_walk(self):
        completeness = ScanCompleteness()
        completeness.wsl_static.mark_incomplete("wsl_project_scan_disabled")

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(
                _submission_scan_result(
                    os_name="windows",
                    wsl_scanned=True,
                    completeness=completeness,
                ),
                ScanSubmissionResult(),
            )["entries"]
        }

        assert entries[("client", "host_static")] == {
            "category": "client",
            "surface": "host_static",
            "complete": True,
        }
        assert entries[("client", "wsl")] == {
            "category": "client",
            "surface": "wsl",
            "complete": False,
            "reason": "wsl_project_scan_disabled",
        }

    def test_windows_client_wsl_authority_requires_completed_project_walk(self):
        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(
                _submission_scan_result(
                    os_name="windows",
                    wsl_scanned=True,
                    container_scan_requested=True,
                ),
                ScanSubmissionResult(),
            )["entries"]
        }

        assert entries[("client", "wsl")] == {
            "category": "client",
            "surface": "wsl",
            "complete": True,
        }

    def test_client_wsl_authority_requires_client_discovery(self):
        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(
                _submission_scan_result(
                    os_name="windows",
                    wsl_scanned=True,
                    container_scan_requested=True,
                    client_discovery_complete=False,
                ),
                ScanSubmissionResult(),
            )["entries"]
        }

        assert entries[("client", "wsl")] == {
            "category": "client",
            "surface": "wsl",
            "complete": False,
            "reason": "client_discovery_incomplete",
        }

    def test_windows_client_host_authority_requires_requested_wsl_project_walk(
        self,
    ):
        completeness = ScanCompleteness()
        completeness.wsl_static.mark_incomplete("wsl_project_scan_timed_out")

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(
                _submission_scan_result(
                    os_name="windows",
                    wsl_scanned=True,
                    container_scan_requested=True,
                    completeness=completeness,
                ),
                ScanSubmissionResult(),
            )["entries"]
        }

        assert entries[("client", "host_static")] == {
            "category": "client",
            "surface": "host_static",
            "complete": False,
            "reason": "wsl_project_scan_timed_out",
        }

    def test_windows_client_host_authority_requires_wsl_inventory(self):
        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(
                _submission_scan_result(
                    os_name="windows",
                    wsl_scanned=False,
                ),
                ScanSubmissionResult(),
            )["entries"]
        }

        assert entries[("client", "host_static")] == {
            "category": "client",
            "surface": "host_static",
            "complete": False,
            "reason": "wsl_inventory_incomplete",
        }

    @pytest.mark.parametrize(
        ("surface", "scan_kwargs", "expected_reason"),
        [
            (
                "wsl",
                {
                    "os_name": "windows",
                    "project_scan_requested": False,
                    "wsl_scanned": True,
                },
                "agent_discovery_incomplete",
            ),
            (
                "wsl_runtime",
                {
                    "os_name": "windows",
                    "wsl_scanned": True,
                },
                "runtime_discovery_incomplete",
            ),
        ],
    )
    def test_agent_wsl_reason_respects_host_authority_gate(
        self,
        surface,
        scan_kwargs,
        expected_reason,
    ):
        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(
                _submission_scan_result(**scan_kwargs),
                ScanSubmissionResult(),
            )["entries"]
        }
        assert entries[("agent", surface)]["complete"] is False
        assert entries[("agent", surface)]["reason"] == expected_reason

    def test_agent_definition_wsl_reason_uses_completeness_reason(self):
        completeness = ScanCompleteness()
        completeness.wsl_static.mark_incomplete("wsl_home_discovery_capped")

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in _scan_manifest_payload(
                _submission_scan_result(
                    os_name="windows",
                    wsl_scanned=True,
                    completeness=completeness,
                ),
                ScanSubmissionResult(),
            )["entries"]
        }

        assert entries[("agent_definition", "wsl")] == {
            "category": "agent_definition",
            "surface": "wsl",
            "complete": False,
            "reason": "wsl_home_discovery_capped",
        }

    def test_windows_plugin_host_surfaces_complete_below_caps(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}
        client.submit_scan_manifest.return_value = {"reconciled": 0}

        submit_scan_results(
            client,
            _submission_scan_result(
                os_name="windows",
                process_scan_requested=True,
                processes_scanned=True,
                wsl_scanned=True,
            ),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("plugin", "host_static")]["complete"] is True
        assert entries[("plugin", "host_runtime")]["complete"] is True

    def test_container_artifact_truncation_blocks_container_authority(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        completeness = ScanCompleteness()
        completeness.container_artifacts.mark_incomplete(
            "container_artifact_walk_truncated"
        )

        submit_scan_results(
            client,
            _submission_scan_result(
                container_scan_requested=True,
                containers_scanned=True,
                completeness=completeness,
            ),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("mcp", "container")] == {
            "category": "mcp",
            "surface": "container",
            "complete": False,
            "reason": "container_artifact_walk_truncated",
        }

    def test_runtime_contributor_error_reaches_runtime_manifest(self):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        completeness = ScanCompleteness()
        completeness.runtime.mark_incomplete("runtime_extension_root_capped")

        submit_scan_results(
            client,
            _submission_scan_result(
                process_scan_requested=True,
                processes_scanned=True,
                completeness=completeness,
            ),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("plugin", "host_runtime")]["reason"] == (
            "runtime_extension_root_capped"
        )
        assert entries[("mcp", "host_runtime")]["complete"] is False

    @pytest.mark.parametrize(
        ("category", "surface", "artifact"),
        [
            (
                "skill",
                "wsl",
                SimpleNamespace(
                    identifier=None,
                    container_id=None,
                    wsl_distro="Ubuntu",
                    files=[],
                ),
            ),
            (
                "plugin",
                "container",
                SimpleNamespace(identifier=None, container_id="container-1"),
            ),
            (
                "plugin",
                "device",
                SimpleNamespace(
                    identifier=None,
                    container_id=None,
                    wsl_distro=None,
                    device_scope=True,
                    scope=None,
                ),
            ),
            (
                "plugin",
                "host_static",
                SimpleNamespace(
                    identifier=None,
                    container_id=None,
                    wsl_distro=None,
                    device_scope=False,
                    scope="user",
                ),
            ),
            (
                "plugin",
                "host_runtime",
                SimpleNamespace(
                    identifier=None,
                    container_id=None,
                    wsl_distro=None,
                    device_scope=False,
                    scope="process_override",
                ),
            ),
        ],
    )
    def test_unidentified_artifact_gates_its_surface_without_failing_run(
        self,
        category,
        surface,
        artifact,
    ):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        scan_result = _submission_scan_result()
        setattr(scan_result, f"{category}s", [artifact])

        submission = submit_scan_results(client, scan_result)

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[(category, surface)]["complete"] is False
        assert entries[(category, surface)]["reason"] == (
            f"{category}_identifier_missing"
        )
        identifier_missing_surfaces = {
            entry["surface"]
            for entry in entries.values()
            if entry["category"] == category
            and entry.get("reason") == f"{category}_identifier_missing"
        }
        assert identifier_missing_surfaces == {surface}
        assert submission.exit_code == 0

    def test_failed_empty_shared_upload_makes_mcp_and_client_incomplete(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        client.submit_mcp_watch_scan.side_effect = httpx.ConnectError(
            "down",
            request=request,
        )
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        scan_result = _submission_scan_result(
            container_scan_requested=True,
            containers_scanned=True,
        )

        submission = submit_scan_results(client, scan_result)

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("mcp", "host_static")]["reason"] == "submission_failed"
        assert entries[("mcp", "container")]["reason"] == "submission_failed"
        assert entries[("client", "host_static")]["reason"] == "submission_failed"
        assert submission.category_outcomes["mcp"] == "failed"
        assert submission.category_outcomes["client"] == "failed"
        assert submission.failed_submissions == ["scan inventory"]
        assert submission.exit_code == EXIT_SUBMIT_FAILED

    def test_runtime_agent_uses_shared_scan_outcome_not_static_agent_outcome(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        client.submit_agents.return_value = {"agents_processed": 1}
        client.submit_mcp_watch_scan.side_effect = httpx.ConnectError(
            "down",
            request=request,
        )
        client.submit_scan_manifest.return_value = {"reconciled": 0}

        submission = submit_scan_results(
            client,
            _submission_scan_result(
                agents=1,
                processes=1,
                process_scan_requested=True,
                processes_scanned=True,
            ),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("agent", "host_static")]["complete"] is True
        assert entries[("agent", "host_runtime")] == {
            "category": "agent",
            "surface": "host_runtime",
            "complete": False,
            "reason": "submission_failed",
        }
        assert submission.failed_submissions == ["servers"]

    def test_backend_partial_surface_failure_gates_only_reported_surface(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {
            "servers_processed": 1,
            "incomplete_surfaces": [
                {
                    "category": "mcp",
                    "surface": "container",
                    "reason": "container_inventory_ingest_failed",
                }
            ],
        }
        client.submit_scan_manifest.side_effect = httpx.ConnectError(
            "manifest down",
            request=httpx.Request("POST", "https://example.com/manifest"),
        )

        submission = submit_scan_results(
            client,
            _submission_scan_result(
                servers=1,
                container_scan_requested=True,
                containers_scanned=True,
            ),
        )

        payload = client.submit_scan_manifest.call_args.args[0]
        entries = {
            (entry["category"], entry["surface"]): entry for entry in payload["entries"]
        }
        assert entries[("mcp", "host_static")]["complete"] is True
        assert entries[("mcp", "container")] == {
            "category": "mcp",
            "surface": "container",
            "complete": False,
            "reason": "container_inventory_ingest_failed",
        }
        assert submission.failed_submissions == ["servers", "scan manifest"]
        assert submission.incomplete_surfaces[("mcp", "container")] == (
            "container_inventory_ingest_failed"
        )

    def test_container_image_backend_failure_is_nonzero_and_gates_container(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {
            "servers_processed": 1,
            "incomplete_surfaces": [
                {
                    "category": "mcp",
                    "surface": "container",
                    "reason": "container_image_inventory_ingest_failed",
                }
            ],
        }
        client.submit_scan_manifest.return_value = {"reconciled": 1}

        submission = submit_scan_results(
            client,
            _submission_scan_result(
                servers=1,
                container_scan_requested=True,
                containers_scanned=True,
            ),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("mcp", "host_static")]["complete"] is True
        assert entries[("mcp", "container")] == {
            "category": "mcp",
            "surface": "container",
            "complete": False,
            "reason": "container_image_inventory_ingest_failed",
        }
        assert submission.failed_submissions == ["servers"]
        assert submission.exit_code == EXIT_SUBMIT_FAILED

    def test_plugins_submit_before_plugin_dependents_and_manifest_is_last(self):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        order: list[str] = []

        def submit_plugins(*_args, **_kwargs):
            order.append("plugins")
            return "success"

        def submit_servers(*_args, **_kwargs):
            order.append("servers")
            return ServerSubmission(status="success", response={"servers_processed": 1})

        def submit_skills(*_args, **_kwargs):
            order.append("skills")
            return "success"

        with (
            mock.patch(
                "runlayer_cli.scan.service.submit_discovered_plugins",
                side_effect=submit_plugins,
            ),
            mock.patch(
                "runlayer_cli.scan.service.submit_discovered_servers",
                side_effect=submit_servers,
            ),
            mock.patch(
                "runlayer_cli.scan.service.submit_discovered_skills",
                side_effect=submit_skills,
            ),
        ):
            submit_scan_results(
                client,
                _submission_scan_result(servers=1, skills=1, plugins=1),
            )

        assert order == ["plugins", "servers", "skills"]
        assert client.method_calls[-1][0] == "submit_scan_manifest"

    def test_disabled_authority_surfaces_are_incomplete(self):
        client = mock.MagicMock()
        client.submit_scan_manifest.return_value = {"reconciled": 0}

        submit_scan_results(
            client,
            _submission_scan_result(
                machine_scope=False,
                process_scan_requested=False,
                container_scan_requested=False,
                wsl_scanned=False,
            ),
        )

        entries = {
            (entry["category"], entry["surface"]): entry
            for entry in client.submit_scan_manifest.call_args.args[0]["entries"]
        }
        assert entries[("plugin", "device")]["complete"] is False
        assert entries[("mcp", "container")]["complete"] is False
        assert entries[("mcp", "wsl")]["complete"] is False
        assert entries[("mcp", "host_runtime")]["complete"] is False

    def test_unsupported_manifest_is_fail_open_but_transport_failure_is_reported(self):
        unsupported_client = mock.MagicMock()
        unsupported_client.submit_scan_manifest.return_value = {"unsupported": True}

        unsupported = submit_scan_results(
            unsupported_client,
            _submission_scan_result(),
        )

        assert unsupported.failed_submissions == []
        assert "Scan Absence Reconciliation" not in unsupported.unsupported
        assert unsupported.exit_code == 0

        failed_client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        failed_client.submit_scan_manifest.side_effect = httpx.ConnectError(
            "down",
            request=request,
        )

        failed = submit_scan_results(failed_client, _submission_scan_result())

        assert failed.failed_submissions == ["scan manifest"]
        assert failed.exit_code == EXIT_SUBMIT_FAILED

    def test_all_success_records_response(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {
            "servers_processed": 2,
            "shadow_servers_found": 1,
            "managed_servers_matched": 0,
        }
        scan_result = _submission_scan_result(servers=2, skills=1, plugins=1)

        with (
            mock.patch(
                "runlayer_cli.scan.service.submit_discovered_skills",
                return_value="success",
            ),
            mock.patch(
                "runlayer_cli.scan.service.submit_discovered_plugins",
                return_value="success",
            ),
        ):
            submission = submit_scan_results(client, scan_result)

        assert submission.response == client.submit_mcp_watch_scan.return_value
        assert submission.unsupported == []
        assert submission.failed_submissions == []
        assert submission.exit_code == 0

    def test_server_unsupported_response_is_bucketed(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"unsupported": True}
        scan_result = _submission_scan_result(servers=1)

        submission = submit_scan_results(client, scan_result)

        assert submission.unsupported == ["Shadow MCP Detection"]
        assert submission.response is None
        assert submission.exit_code == EXIT_UNSUPPORTED

    def test_empty_inventory_unsupported_response_exits_unsupported(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"unsupported": True}
        scan_result = _submission_scan_result(container_scan_requested=True)

        submission = submit_scan_results(client, scan_result)

        assert submission.unsupported == ["Scan Inventory"]
        assert submission.exit_code == EXIT_UNSUPPORTED

    def test_agent_definition_unsupported_response_is_bucketed(self):
        client = mock.MagicMock()
        client.submit_agent_definitions.return_value = {"unsupported": True}

        submission = submit_scan_results(
            client,
            _submission_scan_result(agent_definitions=1),
        )

        client.submit_mcp_watch_scan.assert_not_called()
        client.submit_agents.assert_not_called()
        client.submit_skill.assert_not_called()
        client.submit_plugin.assert_not_called()
        client.submit_agent_definitions.assert_called_once()
        assert submission.unsupported == ["Agent Definition Detection"]
        assert submission.exit_code == EXIT_UNSUPPORTED

    def test_processes_only_scan_still_submits(self):
        """Runtime sightings ride the MCP payload; zero configured servers must
        not skip the POST (the runtime-only shadow headline scenario)."""
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}
        scan_result = _submission_scan_result(processes=1)

        submission = submit_scan_results(client, scan_result)

        client.submit_mcp_watch_scan.assert_called_once()
        assert submission.response == client.submit_mcp_watch_scan.return_value
        assert submission.exit_code == 0

    def test_detected_clients_only_scan_still_submits(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}

        submission = submit_scan_results(
            client,
            _submission_scan_result(clients=1),
        )

        client.submit_mcp_watch_scan.assert_called_once()
        assert submission.response == client.submit_mcp_watch_scan.return_value
        assert submission.exit_code == 0

    def test_container_inventory_submits_without_mcp_servers(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {
            "servers_processed": 0,
            "shadow_servers_found": 0,
            "managed_servers_matched": 0,
        }

        submission = submit_scan_results(
            client,
            _submission_scan_result(containers=1, containers_scanned=True),
        )

        client.submit_mcp_watch_scan.assert_called_once()
        assert submission.exit_code == 0

    def test_successful_empty_container_inventory_submits(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {
            "servers_processed": 0,
            "shadow_servers_found": 0,
            "managed_servers_matched": 0,
        }

        submission = submit_scan_results(
            client,
            _submission_scan_result(containers_scanned=True),
        )

        client.submit_mcp_watch_scan.assert_called_once()
        assert submission.exit_code == 0

    def test_failed_requested_container_inventory_submits(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {
            "servers_processed": 0,
            "shadow_servers_found": 0,
            "managed_servers_matched": 0,
        }

        submission = submit_scan_results(
            client,
            _submission_scan_result(container_scan_requested=True),
        )

        client.submit_mcp_watch_scan.assert_called_once()
        assert submission.exit_code == 0

    @pytest.mark.parametrize(
        "inventory_flag",
        ["stopped_containers_scanned", "container_images_scanned"],
    )
    def test_non_running_container_inventory_submits(self, inventory_flag: str):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}

        submission = submit_scan_results(
            client,
            _submission_scan_result(**{inventory_flag: True}),
        )

        client.submit_mcp_watch_scan.assert_called_once()
        assert submission.exit_code == 0

    def test_wsl_inventory_submits_without_mcp_servers(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}

        submission = submit_scan_results(
            client,
            _submission_scan_result(wsl_distros=1, wsl_scanned=True),
        )

        client.submit_mcp_watch_scan.assert_called_once()
        assert submission.exit_code == 0

    def test_successful_empty_wsl_inventory_submits(self):
        client = mock.MagicMock()
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}

        submission = submit_scan_results(
            client,
            _submission_scan_result(wsl_scanned=True),
        )

        client.submit_mcp_watch_scan.assert_called_once()
        assert submission.exit_code == 0

    def test_empty_scan_does_not_submit_servers(self):
        client = mock.MagicMock()
        scan_result = _submission_scan_result()

        submission = submit_scan_results(client, scan_result)

        client.submit_mcp_watch_scan.assert_not_called()
        assert submission.response is None

    def test_failed_skill_submit_skips_presence_reconcile(self, tmp_path):
        from runlayer_cli.scan.skill_scanner import (
            ARTIFACT_SKILL_MD,
            DiscoveredSkillArtifact,
            SkillFile,
        )

        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            project_paths=("/project/removed",),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {"unsupported": True}
        client.submit_skill_fingerprint.return_value = {"known": False}
        client.submit_skill.side_effect = httpx.ConnectError(
            "down",
            request=httpx.Request("POST", "https://example.com/skills"),
        )
        client.submit_scan_manifest.return_value = {"reconciled": 0}
        scan_result = _submission_scan_result(skill_crawl_complete=True)
        scan_result.skills = [
            DiscoveredSkillArtifact(
                name="failed-skill",
                path="/project/failed-skill",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="failed-skill",
                files=[SkillFile(title="SKILL.md", content="# failed")],
            )
        ]
        real_reconcile = reconcile_skill_presence

        with mock.patch(
            "runlayer_cli.scan.service.reconcile_skill_presence",
            side_effect=lambda api_client, result: real_reconcile(
                api_client,
                result,
                state_path=state_path,
            ),
        ) as reconcile_mock:
            submission = submit_scan_results(client, scan_result)

        # A failed skill POST is collected per-surface rather than failing the
        # whole submit, but presence must not advance the baseline or emit
        # removals for a scan the server never fully received.
        reconcile_mock.assert_not_called()
        client.submit_skill_removals.assert_not_called()
        assert load_state(state_path) == previous
        assert submission.failed_submissions == ["skills"]
        assert submission.exit_code == EXIT_SUBMIT_FAILED

    def test_removals_reconcile_when_current_skills_are_empty(self, tmp_path):
        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            project_paths=("/project/removed",),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        client.submit_skill_removals.return_value = {"removed": 1}
        scan_result = _submission_scan_result(skill_crawl_complete=True)
        real_reconcile = reconcile_skill_presence

        with mock.patch(
            "runlayer_cli.scan.service.reconcile_skill_presence",
            side_effect=lambda api_client, result: real_reconcile(
                api_client,
                result,
                state_path=state_path,
            ),
        ) as reconcile_mock:
            submission = submit_scan_results(client, scan_result)

        reconcile_mock.assert_called_once_with(client, scan_result)
        client.submit_skill_removals.assert_called_once()
        assert load_state(state_path) == _expected_presence_state(scan_result)
        assert submission.unsupported == []
        assert submission.failed_submissions == []

    def test_removal_404_keeps_state_and_is_not_unsupported(self, tmp_path):
        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            global_paths=("/global/removed",),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        client.submit_skill_removals.return_value = {"unsupported": True}
        scan_result = _submission_scan_result(skill_crawl_complete=True)
        real_reconcile = reconcile_skill_presence

        with mock.patch(
            "runlayer_cli.scan.service.reconcile_skill_presence",
            side_effect=lambda api_client, result: real_reconcile(
                api_client,
                result,
                state_path=state_path,
            ),
        ):
            submission = submit_scan_results(client, scan_result)

        assert load_state(state_path) == previous
        assert submission.unsupported == []
        assert submission.failed_submissions == []
        assert submission.exit_code == 0

    def test_removal_failure_keeps_state_and_marks_failed(self, tmp_path):
        state_path = tmp_path / "presence.json"
        previous = build_state(
            SkillPresenceParams(project_depth=7, home="/home/alice"),
            global_paths=("/global/removed",),
        )
        assert save_state(previous, state_path)
        client = mock.MagicMock()
        client.submit_skill_removals.side_effect = RuntimeError("network down")
        scan_result = _submission_scan_result(skill_crawl_complete=True)
        real_reconcile = reconcile_skill_presence

        with mock.patch(
            "runlayer_cli.scan.service.reconcile_skill_presence",
            side_effect=lambda api_client, result: real_reconcile(
                api_client,
                result,
                state_path=state_path,
            ),
        ):
            submission = submit_scan_results(client, scan_result)

        assert load_state(state_path) == previous
        assert submission.failed_submissions == ["skill removals"]
        assert submission.exit_code == EXIT_SUBMIT_FAILED

    @pytest.mark.parametrize(
        ("skill_status", "expected_unsupported", "expected_failed"),
        [
            ("unsupported", ["Shadow Skill Detection"], []),
            ("failed", [], ["skills"]),
        ],
    )
    def test_skill_submit_failure_suppresses_presence_reconciliation(
        self,
        skill_status,
        expected_unsupported,
        expected_failed,
    ):
        client = mock.MagicMock()
        scan_result = _submission_scan_result(
            skills=1,
            skill_crawl_complete=True,
            project_skill_candidate_paths=("/project/current",),
        )

        with (
            mock.patch(
                "runlayer_cli.scan.service.submit_discovered_skills",
                return_value=skill_status,
            ),
            mock.patch(
                "runlayer_cli.scan.service.reconcile_skill_presence"
            ) as reconcile_mock,
        ):
            submission = submit_scan_results(client, scan_result)

        reconcile_mock.assert_not_called()
        assert submission.unsupported == expected_unsupported
        assert submission.failed_submissions == expected_failed

    def test_successful_skill_submit_attempts_presence_reconciliation(self):
        client = mock.MagicMock()
        scan_result = _submission_scan_result(
            skills=1,
            skill_crawl_complete=True,
            project_skill_candidate_paths=("/project/current",),
        )

        with (
            mock.patch(
                "runlayer_cli.scan.service.submit_discovered_skills",
                return_value="success",
            ),
            mock.patch(
                "runlayer_cli.scan.service.reconcile_skill_presence",
                return_value="success",
            ) as reconcile_mock,
        ):
            submit_scan_results(client, scan_result)

        reconcile_mock.assert_called_once_with(client, scan_result)

    def test_skills_unsupported_bucketed(self):
        client = mock.MagicMock()
        scan_result = _submission_scan_result(skills=1)

        with mock.patch(
            "runlayer_cli.scan.service.submit_discovered_skills",
            return_value="unsupported",
        ):
            submission = submit_scan_results(client, scan_result)

        assert submission.unsupported == ["Shadow Skill Detection"]
        assert submission.exit_code == EXIT_UNSUPPORTED

    def test_plugins_failed_bucketed(self):
        client = mock.MagicMock()
        scan_result = _submission_scan_result(plugins=1)

        with mock.patch(
            "runlayer_cli.scan.service.submit_discovered_plugins",
            return_value="failed",
        ):
            submission = submit_scan_results(client, scan_result)

        assert submission.failed_submissions == ["plugins"]
        assert submission.exit_code == EXIT_SUBMIT_FAILED

    def test_agents_unsupported_bucketed(self):
        client = mock.MagicMock()
        scan_result = _submission_scan_result(agents=1)

        with mock.patch(
            "runlayer_cli.scan.service.submit_discovered_agents",
            return_value="unsupported",
        ):
            submission = submit_scan_results(client, scan_result)

        assert submission.unsupported == ["Shadow Agent Detection"]
        assert submission.exit_code == EXIT_UNSUPPORTED

    def test_agents_failed_bucketed(self):
        client = mock.MagicMock()
        scan_result = _submission_scan_result(agents=1)

        with mock.patch(
            "runlayer_cli.scan.service.submit_discovered_agents",
            return_value="failed",
        ):
            submission = submit_scan_results(client, scan_result)

        assert submission.failed_submissions == ["agents"]
        assert submission.exit_code == EXIT_SUBMIT_FAILED

    def test_agents_submitted_when_present(self):
        client = mock.MagicMock()
        client.submit_agents.return_value = {"agents_processed": 1}
        scan_result = _submission_scan_result(agents=1)

        submission = submit_scan_results(client, scan_result)

        client.submit_agents.assert_called_once()
        assert submission.unsupported == []
        assert submission.failed_submissions == []

    def test_agent_definitions_submitted_when_present(self):
        client = mock.MagicMock()
        client.submit_agent_definitions.return_value = {
            "agent_definitions": [],
            "created_count": 1,
            "updated_count": 0,
        }
        scan_result = _submission_scan_result(agent_definitions=1)

        submission = submit_scan_results(client, scan_result)

        client.submit_agent_definitions.assert_called_once()
        assert submission.unsupported == []
        assert submission.failed_submissions == []
        assert submission.exit_code == 0

    def test_agents_submit_before_correlated_process_sightings(self):
        client = mock.MagicMock()
        client.submit_agents.return_value = {"agents_processed": 1}
        client.submit_mcp_watch_scan.return_value = {"servers_processed": 0}
        scan_result = _submission_scan_result(agents=1, processes=1)

        submit_scan_results(client, scan_result)

        assert [call[0] for call in client.method_calls[:2]] == [
            "submit_agents",
            "submit_mcp_watch_scan",
        ]

    def test_failed_server_still_submits_skills_and_plugins(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(500, request=request)
        client.submit_mcp_watch_scan.side_effect = httpx.HTTPStatusError(
            "boom", request=request, response=response
        )
        scan_result = _submission_scan_result(servers=1, skills=1, plugins=1)

        with (
            mock.patch(
                "runlayer_cli.scan.service.submit_discovered_skills",
                return_value="success",
            ) as skills_mock,
            mock.patch(
                "runlayer_cli.scan.service.submit_discovered_plugins",
                return_value="success",
            ) as plugins_mock,
        ):
            submission = submit_scan_results(client, scan_result)

        assert submission.failed_submissions == ["servers"]
        assert submission.exit_code == EXIT_SUBMIT_FAILED
        skills_mock.assert_called_once()
        plugins_mock.assert_called_once()

    def test_server_network_error_is_failed(self):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        client.submit_mcp_watch_scan.side_effect = httpx.ConnectError(
            "down", request=request
        )
        scan_result = _submission_scan_result(servers=1)

        submission = submit_scan_results(client, scan_result)

        assert submission.failed_submissions == ["servers"]
        assert submission.exit_code == EXIT_SUBMIT_FAILED

    @pytest.mark.parametrize("status", [401, 403])
    def test_auth_error_propagates(self, status):
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(status, request=request)
        client.submit_mcp_watch_scan.side_effect = httpx.HTTPStatusError(
            "unauthorized", request=request, response=response
        )
        scan_result = _submission_scan_result(servers=1)

        with pytest.raises(httpx.HTTPStatusError):
            submit_scan_results(client, scan_result)


class TestPresenceGatedFilterRespectsProbeCompleteness:
    """Absence of presence evidence is not evidence of absence (ISS-23).

    When the install probes did not run to completion, dropping shared-path
    project configs (``.mcp.json`` for github_copilot_cli) silently loses real
    findings. The gate must only fire on a complete presence scan.
    """

    @staticmethod
    def _copilot_project_config() -> MCPClientConfig:
        return MCPClientConfig(
            client="github_copilot_cli",
            config_path="/work/app/.mcp.json",
            config_modified_at=None,
            servers=[MCPServerConfig(name="s", type="stdio", command="echo")],
            config_scope="project",
            project_path="/work/app",
        )

    def test_gate_drops_when_presence_scan_complete(self):
        status = ScanCompletionStatus()
        result = scan_service._filter_presence_gated_project_configurations(
            [self._copilot_project_config()],
            clients=get_all_clients(),
            probed_clients=[],
            presence_status=status,
        )
        assert result == []

    def test_gate_is_skipped_when_presence_scan_incomplete(self):
        status = ScanCompletionStatus()
        status.mark_incomplete("client_presence_scan_failed")
        config = self._copilot_project_config()
        result = scan_service._filter_presence_gated_project_configurations(
            [config],
            clients=get_all_clients(),
            probed_clients=[],
            presence_status=status,
        )
        assert result == [config]


class TestAssemblyStepsAreBestEffort:
    """A bug in one post-phase assembly step must not lose the whole scan (ISS-11).

    The phases are individually best-effort, but the dedupe / attribution /
    presence-merge steps that stitch their results together ran unguarded in
    ``scan_all_clients``; one exception there raised out of the scan and the
    device reported nothing.
    """

    @staticmethod
    def _run_with_failing_step(monkeypatch, step: str):
        claude = get_client_by_name("claude_code")
        assert claude is not None
        configurations = [
            MCPClientConfig(
                client=claude.name,
                config_path="/home/u/.claude.json",
                config_scope="global",
                servers=[MCPServerConfig(name="s", type="stdio", command="echo")],
            )
        ]
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [claude])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                configurations=configurations
            ),
        )
        monkeypatch.setattr(
            scan_service, "detect_client_presence", lambda _clients, **_kwargs: []
        )

        def explode(*_args, **_kwargs):
            raise RuntimeError(f"{step} bug")

        monkeypatch.setattr(scan_service, step, explode)
        return scan_all_clients(
            device_id="device", scan_projects=False, governor=mock.MagicMock()
        )

    @pytest.mark.parametrize(
        ("step", "surface"),
        [
            ("_attribute_wsl_artifacts", "mcp_host_static"),
            ("_dedupe_path_configurations", "mcp_host_static"),
            ("dedupe_host_container_configurations", "mcp_host_static"),
            ("strip_duplicate_skill_files", "skill_host_static"),
            ("dedupe_agent_definitions", "agent_definition_host_static"),
            ("_filter_presence_gated_project_configurations", "mcp_host_static"),
        ],
    )
    def test_failing_step_keeps_configurations_and_marks_incomplete(
        self, monkeypatch, step, surface
    ):
        result = self._run_with_failing_step(monkeypatch, step)

        assert [config.client for config in result.configurations] == ["claude_code"]
        status = getattr(result.completeness, surface)
        assert "assembly_step_failed" in status.reasons

    def test_failing_presence_merge_keeps_probed_clients(self, monkeypatch):
        result = self._run_with_failing_step(monkeypatch, "merge_client_presence")

        assert [config.client for config in result.configurations] == ["claude_code"]
        assert "assembly_step_failed" in result.completeness.client_presence.reasons


class _LatchedGovernor:
    """Fake governor with the real one's sticky abort latch."""

    cpu_cores = 2

    def __init__(self, *, tripped: bool = False, reason: str = "over budget"):
        self.tripped = tripped
        self.reason = reason

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False

    def trip(self) -> None:
        self.tripped = True

    def checkpoint(self) -> None:
        if self.tripped:
            raise scan_service.ScanResourceLimitExceeded(self.reason)


class TestGovernorAbortKeepsPartialResults:
    """A resource-cap abort must upload what was found, not discard it (ISS-09).

    The governor's abort latch is sticky: once one phase trips it, every later
    checkpoint raises. Before, the first raise escaped ``scan_all_clients`` and
    the device reported nothing; now each phase past the trip falls through to
    its incomplete default (``resource_limit_exceeded``) and the assembled
    partial manifest is returned for upload with absence authority withheld.
    """

    @staticmethod
    def _global_config() -> MCPClientConfig:
        claude = get_client_by_name("claude_code")
        assert claude is not None
        return MCPClientConfig(
            client=claude.name,
            config_path="/home/u/.claude.json",
            config_scope="global",
            servers=[MCPServerConfig(name="s", type="stdio", command="echo")],
        )

    def test_orchestrator_assembles_phases_finished_before_the_trip(self, monkeypatch):
        TestConcurrentScanPhases._stub_empty_phases(monkeypatch)
        governor = _LatchedGovernor()
        global_config = self._global_config()
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_global_configurations",
            lambda *_a, **_k: scan_orchestrator.GlobalPhaseResult(
                configurations=[global_config]
            ),
        )

        def crawl_trips_the_cap(**_kwargs):
            governor.trip()
            governor.checkpoint()
            raise AssertionError("unreachable")

        monkeypatch.setattr(
            scan_orchestrator, "_scan_project_phase", crawl_trips_the_cap
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=governor,
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=True,
            run_static_agents=True,
        )

        assert [config.client for config in result.configurations] == ["claude_code"]
        assert result.resource_limit_exceeded == "over budget"
        assert "resource_limit_exceeded" in result.completeness.mcp_host_static.reasons
        assert (
            "resource_limit_exceeded" in result.completeness.agent_host_static.reasons
        )

    def test_plugin_phase_abort_withholds_device_plugin_authority(self, monkeypatch):
        """The device plugin scan runs inside phase 10; an abort there covers it.

        The abort stamped ``plugin_artifacts`` only, and the bridge into
        ``plugin_device`` copied just the crash reason, so an aborted
        machine-scope scan still claimed device-plugin absence authority.
        """
        TestConcurrentScanPhases._stub_empty_phases(monkeypatch)
        governor = _LatchedGovernor()

        def plugin_phase_trips_the_cap(**_kwargs):
            governor.trip()
            governor.checkpoint()
            raise AssertionError("unreachable")

        monkeypatch.setattr(
            scan_orchestrator, "_scan_plugin_artifact_phase", plugin_phase_trips_the_cap
        )

        result = scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=governor,
            timer=PhaseTimer(),
            scan_projects=False,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
            machine_scope=True,
        )

        assert result.resource_limit_exceeded == "over budget"
        assert "resource_limit_exceeded" in result.completeness.plugin_device.reasons
        assert result.completeness.plugin_device.complete is False

    @staticmethod
    def _record_finalizers(monkeypatch) -> list[str]:
        calls: list[str] = []
        for name in ("finalize_skill_scan_state", "finalize_plugin_scan_state"):
            monkeypatch.setattr(
                scan_orchestrator,
                name,
                lambda *_a, _name=name, **_k: calls.append(_name),
            )
        return calls

    @staticmethod
    def _run_with_governor(governor):
        return scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=governor,
            timer=PhaseTimer(),
            scan_projects=False,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=False,
            run_static_agents=False,
            machine_scope=True,
        )

    def test_abort_skips_content_rotation_finalizers(self, monkeypatch):
        """An aborted scan must not advance the skill/plugin content cursors.

        The finalizers persist ``offset + admitted`` after a capped run. A
        skill or plugin phase can admit content and then abort, returning its
        empty default, so that content never reaches the partial manifest;
        advancing the cursor past it would skip that slice on the next run.
        """
        TestConcurrentScanPhases._stub_empty_phases(monkeypatch)
        calls = self._record_finalizers(monkeypatch)
        governor = _LatchedGovernor()

        def plugin_phase_trips_the_cap(**_kwargs):
            governor.trip()
            governor.checkpoint()
            raise AssertionError("unreachable")

        monkeypatch.setattr(
            scan_orchestrator, "_scan_plugin_artifact_phase", plugin_phase_trips_the_cap
        )

        result = self._run_with_governor(governor)

        assert result.resource_limit_exceeded == "over budget"
        assert calls == []

    def test_clean_run_still_advances_content_rotation(self, monkeypatch):
        TestConcurrentScanPhases._stub_empty_phases(monkeypatch)
        calls = self._record_finalizers(monkeypatch)

        result = self._run_with_governor(_LatchedGovernor())

        assert result.resource_limit_exceeded is None
        assert calls == ["finalize_skill_scan_state", "finalize_plugin_scan_state"]

    @staticmethod
    def _run_agent_phases(monkeypatch, governor, *, discover_agents):
        TestConcurrentScanPhases._stub_empty_phases(monkeypatch)
        monkeypatch.setattr(
            scan_orchestrator,
            "_scan_project_phase",
            lambda **_kwargs: scan_orchestrator.ProjectPhaseResult(),
        )
        monkeypatch.setattr(scan_orchestrator, "discover_agents", discover_agents)
        return scan_orchestrator.run_concurrent_scan_phases(
            clients=[],
            governor=governor,
            timer=PhaseTimer(),
            scan_projects=True,
            project_scan_timeout=60,
            project_scan_depth=7,
            detect_agents=True,
            run_static_agents=True,
        )

    def test_agent_phase_abort_is_stamped_resource_limit_exceeded(self, monkeypatch):
        """The agent surface carries the abort reason, like every other surface.

        The agent phases used to pass a throwaway status and an already-marked
        default, so a cap tripping *inside* them (after the crawl finished)
        stamped ``agent_static_scan_failed`` on ``agent_host_static`` instead.
        """
        governor = _LatchedGovernor()

        def agents_trip_the_cap(**kwargs):
            if kwargs.get("detect_static"):
                governor.trip()
                governor.checkpoint()
            return AgentScanResult()

        result = self._run_agent_phases(
            monkeypatch, governor, discover_agents=agents_trip_the_cap
        )

        assert result.resource_limit_exceeded == "over budget"
        assert result.completeness.agent_host_static.reasons == [
            "resource_limit_exceeded"
        ]

    def test_agent_phase_crash_keeps_its_phase_reason(self, monkeypatch):
        def install_probe_crashes(**kwargs):
            if kwargs.get("detect_install"):
                raise RuntimeError("probe blew up")
            return AgentScanResult()

        result = self._run_agent_phases(
            monkeypatch,
            SimpleNamespace(cpu_cores=2, checkpoint=lambda: None),
            discover_agents=install_probe_crashes,
        )

        assert result.resource_limit_exceeded is None
        assert result.completeness.agent_host_static.reasons == [
            "agent_install_scan_failed"
        ]

    def test_service_returns_partial_result_when_later_phases_abort(self, monkeypatch):
        global_config = self._global_config()
        claude = get_client_by_name("claude_code")
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [claude])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                configurations=[global_config]
            ),
        )
        monkeypatch.setattr(
            scan_service,
            "detect_client_presence",
            lambda *_a, **_k: pytest.fail("presence probe must not run after abort"),
        )
        monkeypatch.setattr(
            scan_service,
            "discover_processes",
            lambda *_a, **_k: pytest.fail("process scan must not run after abort"),
        )

        result = scan_all_clients(
            device_id="device",
            scan_projects=False,
            detect_processes=True,
            governor=_LatchedGovernor(tripped=True, reason="memory cap hit"),
        )

        assert [config.client for config in result.configurations] == ["claude_code"]
        assert result.resource_limit_exceeded == "memory cap hit"
        assert result.client_discovery_complete is False
        assert "resource_limit_exceeded" in result.completeness.runtime.reasons
        assert "resource_limit_exceeded" in result.completeness.client_presence.reasons

    def test_presence_probe_abort_keeps_presence_gated_project_configs(
        self, monkeypatch
    ):
        """An aborted probe is not a complete "nothing installed" answer.

        Phase 14 falls back to an empty probe list on abort. The presence gate
        must see that scan as incomplete, or the shared-path project config
        (``.mcp.json`` for github_copilot_cli) is dropped from the partial upload.
        """
        gated = (
            TestPresenceGatedFilterRespectsProbeCompleteness._copilot_project_config()
        )
        copilot = get_client_by_name("github_copilot_cli")
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [copilot])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                configurations=[gated]
            ),
        )
        governor = _LatchedGovernor(reason="memory cap hit")

        def probe_trips_the_cap(*_a, **_k):
            governor.trip()
            governor.checkpoint()
            raise AssertionError("unreachable")

        monkeypatch.setattr(scan_service, "detect_client_presence", probe_trips_the_cap)

        result = scan_all_clients(
            device_id="device", scan_projects=False, governor=governor
        )

        assert result.configurations == [gated]
        assert result.resource_limit_exceeded == "memory cap hit"
        assert result.client_discovery_complete is False
