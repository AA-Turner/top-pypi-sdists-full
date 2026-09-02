"""Tests for scan service orchestration."""

from contextlib import contextmanager
import getpass
import json
import os
from pathlib import Path
import threading
from types import SimpleNamespace
from unittest import mock

import httpx
import pytest
import structlog

from runlayer_cli.scan import orchestrator as scan_orchestrator
from runlayer_cli.scan.client_presence import DetectedClient
from runlayer_cli.scan.clients import get_client_by_name
from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig
from runlayer_cli.scan.processes.models import (
    DiscoveredProcess,
    OverrideConfigRef,
    ProcessDiscoveryResult,
)
from runlayer_cli.scan.timing import PhaseTimer
from runlayer_cli.scan.service import (
    EXIT_SUBMIT_FAILED,
    EXIT_UNSUPPORTED,
    MAX_AGENTS,
    ScanResult,
    ScanSubmissionResult,
    ServerSubmission,
    _attribute_wsl_artifacts,
    _dedupe_path_configurations,
    _parse_process_override_configurations,
    dedupe_host_container_configurations,
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


def test_container_config_dedupe_prefers_container_attribution():
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

    assert deduped == [different, container]


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
def test_process_override_skips_untrusted_process_owner(tmp_path, process_user):
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

    with structlog.testing.capture_logs() as logs:
        parsed = _parse_process_override_configurations(
            [ref],
            configurations=[],
            clients=[claude],
        )

    assert parsed == []
    [skip_log] = [
        log
        for log in logs
        if log["event"] == "process_override_config_skipped_untrusted_owner"
    ]
    assert skip_log["log_level"] == "debug"
    assert skip_log["owner_status"] == (
        "unknown" if process_user is None else "mismatch"
    )
    assert str(config_path) not in repr(skip_log)


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
    )

    assert parsed == []


def test_windows_process_owner_lookup_caps_unique_pids(monkeypatch):
    from runlayer_cli.scan import service as scan_service

    run = mock.Mock(return_value=SimpleNamespace(returncode=0, stdout="[]", stderr=""))
    monkeypatch.setattr(scan_service.subprocess, "run", run)
    refs = [
        SimpleNamespace(pid=pid, user=None)
        for pid in range(1, scan_service.MAX_OVERRIDE_OWNER_LOOKUPS + 2)
    ]

    assert scan_service._resolve_windows_process_owners(refs) == {}

    script = run.call_args.args[0][-1]
    assert f"ProcessId = {scan_service.MAX_OVERRIDE_OWNER_LOOKUPS}" in script
    assert f"ProcessId = {scan_service.MAX_OVERRIDE_OWNER_LOOKUPS + 1}" not in script


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="FIFO unsupported")
def test_process_override_skips_fifo_without_opening_it(tmp_path, monkeypatch):
    from runlayer_cli.scan import service as scan_service

    claude = get_client_by_name("claude_code")
    assert claude is not None
    config_path = tmp_path / "mcp.json"
    os.mkfifo(config_path)
    parse = mock.Mock()
    monkeypatch.setattr(scan_service, "parse_config_file", parse)

    with structlog.testing.capture_logs() as logs:
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
    [skip_log] = [
        log
        for log in logs
        if log["event"] == "process_override_config_skipped_unsafe_file"
    ]
    assert skip_log["file_status"] == "not_regular"
    assert str(config_path) not in repr(skip_log)


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

    with structlog.testing.capture_logs() as logs:
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
    [skip_log] = [
        log
        for log in logs
        if log["event"] == "process_override_config_skipped_unsafe_file"
    ]
    assert skip_log["file_status"] == "too_large"
    assert str(config_path) not in repr(skip_log)


class TestScanAllClients:
    def test_forwards_crawled_node_modules_to_presence(self, monkeypatch, tmp_path):
        from runlayer_cli.scan import service as scan_service

        node_modules = tmp_path / "renamed-prefix" / "node_modules"
        seen: dict[str, object] = {}
        monkeypatch.setattr(scan_service, "get_all_clients", lambda: [])
        monkeypatch.setattr(
            scan_service,
            "run_concurrent_scan_phases",
            lambda **_kwargs: scan_orchestrator.ConcurrentScanResult(
                node_modules_paths=[node_modules]
            ),
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
        monkeypatch.setattr(scan_service, "detect_client_presence", lambda _clients: [])

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
        monkeypatch.setattr(scan_service, "detect_client_presence", lambda _clients: [])

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
        monkeypatch.setattr(scan_service, "detect_client_presence", lambda _clients: [])

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
                )
            ],
        )
        result = scan_all_clients(detect_processes=True, scan_projects=False)
        mock_discover.assert_called_once()
        assert callable(mock_discover.call_args.kwargs["checkpoint"])
        assert result.processes == [proc]
        assert result.total_processes == 1
        [override_config] = [
            config
            for config in result.configurations
            if config.config_scope == "process_override"
        ]
        assert override_config.config_path == str(override_path)
        assert override_config.servers[0].name == "override"

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
        monkeypatch.setattr(scan_service, "detect_client_presence", lambda _clients: [])

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
        monkeypatch.setattr(scan_service, "detect_client_presence", lambda _clients: [])

        scan_all_clients(
            device_id="device",
            scan_projects=False,
            detect_renamed_plugin_caches=True,
            governor=mock.MagicMock(),
        )

        assert run_concurrent.call_args.kwargs["detect_renamed_plugin_caches"] is True

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
        monkeypatch.setattr(scan_service, "detect_client_presence", lambda _clients: [])
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
        payload = result.to_api_payload()
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
            "scan_global_skills": [],
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
        monkeypatch.setattr(scan_orchestrator, "_wsl_homes", lambda: [])

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
            scan_orchestrator, "scan_global_skills", lambda **kwargs: []
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
        monkeypatch.setattr(scan_orchestrator, "_wsl_homes", lambda: [])

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

        def global_skills(*, extra_home_roots=(), checkpoint=None):
            extra_roots["skills"] = list(extra_home_roots)
            return []

        def user_agent_definitions(*, extra_home_roots=()):
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
        monkeypatch.setattr(scan_orchestrator, "scan_global_skills", global_skills)
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

        wsl_homes_mock.assert_called_once_with()
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
            "scan_global_skills": [],
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
        monkeypatch.setattr(scan_orchestrator, "_wsl_homes", lambda: [])

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

    def test_wire_payload_carries_wsl_container_scan_authority(self):
        from runlayer_cli.scan.containers import DiscoveredContainer

        result = self._result_with_findings()
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

    def test_caps_at_max_agents(self):
        agents = [
            self._agent(location=f"/Users/alice/p{i}") for i in range(MAX_AGENTS + 5)
        ]
        with structlog.testing.capture_logs() as logs:
            payload = self._scan_result(agents).to_agent_report_payload()
        assert len(payload["agents"]) == MAX_AGENTS
        # Cap bit -> warn so an outlier host's clamp is visible, parity with the
        # time-budget walk's truncated signal.
        truncated = [e for e in logs if e["event"] == "agent_report_truncated"]
        assert truncated == [
            {
                "event": "agent_report_truncated",
                "log_level": "warning",
                "detected": MAX_AGENTS + 5,
                "sent": MAX_AGENTS,
            }
        ]

    def test_no_truncation_warning_under_cap(self):
        agents = [self._agent(location=f"/Users/alice/p{i}") for i in range(MAX_AGENTS)]
        with structlog.testing.capture_logs() as logs:
            payload = self._scan_result(agents).to_agent_report_payload()
        assert len(payload["agents"]) == MAX_AGENTS
        assert not [e for e in logs if e["event"] == "agent_report_truncated"]

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
    servers: int = 0,
    clients: int = 0,
    skills: int = 0,
    plugins: int = 0,
    agents: int = 0,
    agent_definitions: int = 0,
    processes: int = 0,
    containers: int = 0,
    containers_scanned: bool = False,
    stopped_containers_scanned: bool = False,
    container_images_scanned: bool = False,
    wsl_distros: int = 0,
    wsl_scanned: bool = False,
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
    return SimpleNamespace(
        total_servers=servers,
        detected_clients=[
            SimpleNamespace(client=f"client-{i}") for i in range(clients)
        ],
        skills=[SimpleNamespace(name=f"skill-{i}") for i in range(skills)],
        plugins=[SimpleNamespace(name=f"plugin-{i}") for i in range(plugins)],
        agents=agent_list,
        agent_definitions=definition_list,
        processes=[SimpleNamespace(pid=1000 + i) for i in range(processes)],
        containers=[
            SimpleNamespace(container_id=f"container-{i}") for i in range(containers)
        ],
        containers_scanned=containers_scanned,
        stopped_containers_scanned=stopped_containers_scanned,
        container_images_scanned=container_images_scanned,
        wsl_distros=[SimpleNamespace(name=f"distro-{i}") for i in range(wsl_distros)],
        wsl_scanned=wsl_scanned,
        to_api_payload=lambda: {"device_id": "device-1"},
        to_agent_report_payload=lambda: {
            "device_id": "device-1",
            "agents": [a.to_api_payload() for a in agent_list],
        },
        to_agent_definition_report_payload=lambda: {
            "device_id": "device-1",
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
        client.submit_mcp_watch_scan.assert_called_once_with({"device_id": "device-1"})

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


class TestSubmitScanResults:
    """Orchestrator maps each category's status into the result buckets."""

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
