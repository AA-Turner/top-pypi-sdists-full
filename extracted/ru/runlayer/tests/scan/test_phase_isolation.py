"""One misbehaving client, plugin scanner or container must not empty its phase (ISS-03).

``_best_effort_phase`` only isolates whole phases: before these guards an
exception from a single client's reader threw away every sibling client's
findings in phase 01 and returned an empty ``GlobalPhaseResult``.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from runlayer_cli.scan import orchestrator
from runlayer_cli.scan.clients import ConfigPath, MCPClientDefinition
from runlayer_cli.scan.containers import collect as containers_module
from runlayer_cli.scan.containers.inspect_parse import DiscoveredContainer
from runlayer_cli.scan.resource_governor import ScanResourceLimitExceeded


def _client(name: str, config_path: Path) -> MCPClientDefinition:
    return MCPClientDefinition(
        name=name,
        display_name=name,
        paths=[ConfigPath(path=str(config_path))],
        servers_key="mcpServers",
    )


def _write_config(path: Path, server: str) -> None:
    path.write_text(json.dumps({"mcpServers": {server: {"command": "echo"}}}))


@pytest.fixture
def governor():
    return SimpleNamespace(checkpoint=lambda: None)


def test_one_client_raising_keeps_sibling_clients(tmp_path, monkeypatch, governor):
    good_path = tmp_path / "good.json"
    bad_path = tmp_path / "bad.json"
    _write_config(good_path, "good-server")
    _write_config(bad_path, "bad-server")
    clients = [_client("bad", bad_path), _client("good", good_path)]

    real_parse = orchestrator.parse_config_file

    def exploding_parse(client_def, config_path, **kwargs):
        if client_def.name == "bad":
            raise RuntimeError("reader bug")
        return real_parse(client_def, config_path, **kwargs)

    monkeypatch.setattr(orchestrator, "parse_config_file", exploding_parse)
    monkeypatch.setattr(
        orchestrator, "enrich_configurations_with_warp_sqlite", lambda *a, **k: None
    )

    result = orchestrator._scan_global_configurations(clients, governor)

    assert [config.client for config in result.configurations] == ["good"]
    assert result.completion.complete is False
    assert "client_config_scan_failed" in result.completion.reasons


def test_governor_abort_still_propagates(tmp_path, monkeypatch, governor):
    path = tmp_path / "cfg.json"
    _write_config(path, "s")

    def aborting_parse(*args, **kwargs):
        raise ScanResourceLimitExceeded("budget")

    monkeypatch.setattr(orchestrator, "parse_config_file", aborting_parse)

    with pytest.raises(ScanResourceLimitExceeded):
        orchestrator._scan_global_configurations([_client("c", path)], governor)


def test_warp_enrichment_failure_keeps_file_configs(tmp_path, monkeypatch, governor):
    path = tmp_path / "cfg.json"
    _write_config(path, "s")

    def exploding_enrich(*args, **kwargs):
        raise RuntimeError("sqlite bug")

    monkeypatch.setattr(
        orchestrator, "enrich_configurations_with_warp_sqlite", exploding_enrich
    )

    result = orchestrator._scan_global_configurations([_client("c", path)], governor)

    assert [config.client for config in result.configurations] == ["c"]
    assert "warp_sqlite_enrichment_failed" in result.completion.reasons


def _stub_phase_10_scanners(monkeypatch, *, failing: str) -> None:
    def artifact(name: str):
        return SimpleNamespace(name=name)

    scanners = {
        "scan_cursor_native_plugins": "cursor_native",
        "scan_cursor_user_local_plugins": "cursor_user_local",
        "scan_claude_code_plugin_artifacts": "claude_code",
        "scan_claude_desktop_connectors": "claude_desktop",
        "scan_codex_plugin_artifacts": "codex",
        "scan_opencode_plugin_artifacts": "opencode",
        "scan_vscode_extensions": "vscode",
        "scan_jetbrains_plugins": "jetbrains",
    }
    for attr, label in scanners.items():

        def scanner(*_args, _label=label, **_kwargs):
            if _label == failing:
                raise RuntimeError(f"{_label} bug")
            return [artifact(_label)]

        monkeypatch.setattr(orchestrator, attr, scanner)


def test_phase_10_one_scanner_raising_keeps_the_rest(monkeypatch, governor):
    _stub_phase_10_scanners(monkeypatch, failing="claude_code")
    status = orchestrator.ScanCompletionStatus()

    artifacts = orchestrator._scan_plugin_artifact_phase(
        governor=governor, scan_status=status
    )

    assert sorted(a.name for a in artifacts) == [
        "claude_desktop",
        "codex",
        "cursor_native",
        "cursor_user_local",
        "jetbrains",
        "opencode",
        "vscode",
    ]
    assert status.reasons == ["plugin_scanner_failed"]


def test_phase_10_vscode_failure_marks_device_scope(monkeypatch, governor):
    _stub_phase_10_scanners(monkeypatch, failing="vscode")
    status = orchestrator.ScanCompletionStatus()
    device_status = orchestrator.ScanCompletionStatus()

    orchestrator._scan_plugin_artifact_phase(
        governor=governor, scan_status=status, device_scan_status=device_status
    )

    assert "plugin_scanner_failed" in status.reasons
    assert "plugin_scanner_failed" in device_status.reasons


def test_phase_10_governor_abort_propagates(monkeypatch, governor):
    _stub_phase_10_scanners(monkeypatch, failing="none")

    def abort(*_args, **_kwargs):
        raise ScanResourceLimitExceeded("budget")

    monkeypatch.setattr(orchestrator, "scan_codex_plugin_artifacts", abort)
    with pytest.raises(ScanResourceLimitExceeded):
        orchestrator._scan_plugin_artifact_phase(governor=governor)


def test_one_container_raising_keeps_sibling_containers(monkeypatch):
    visited: list[str] = []

    def configs(_ctx, container, _clients):
        if container.container_id == "container-0":
            raise RuntimeError("hostile labels")
        visited.append(container.container_id)

    monkeypatch.setattr(containers_module, "_collect_container_configs", configs)
    for phase in (
        "_collect_container_project_tree",
        "_collect_container_global_skills",
        "_collect_container_extensions",
        "_collect_container_user_definitions",
        "_collect_container_hidden_artifacts",
        "_collect_standard_container_npm_agents",
    ):
        monkeypatch.setattr(containers_module, phase, lambda *_a, **_k: None)

    containers = [
        DiscoveredContainer(
            container_id=f"container-{index}",
            name=None,
            image_ref=None,
            image_digest=None,
        )
        for index in range(2)
    ]

    artifacts = containers_module._collect_container_artifacts(
        collector=SimpleNamespace(),
        containers=containers,
        clients=[],
        deadline=10**12,
        subprocess_timeout=1,
        host_home=Path("/Users/alex"),
    )

    assert visited == ["container-1"]
    assert artifacts.complete is False
    assert artifacts.failure_reason == "container_artifact_collection_failed"


def test_extension_cap_survives_a_later_failure_in_the_same_container(monkeypatch):
    """The extension cap is scan-wide and must outlive one container's crash.

    When the cap was a loop local returned from ``_collect_one_container``, a
    later phase raising in the same container (swallowed by the isolation
    guard) lost the return value, so the next container re-walked extensions
    and overwrote ``container_artifact_collection_failed`` with the cap reason.
    """
    extension_walks: list[str] = []

    def extensions(_ctx, container):
        extension_walks.append(container.container_id)
        raise containers_module._ExtensionCollectionCapped

    def user_definitions(_ctx, container, _roots):
        if container.container_id == "container-0":
            raise RuntimeError("hostile agent definitions")

    monkeypatch.setattr(containers_module, "_collect_container_extensions", extensions)
    monkeypatch.setattr(
        containers_module, "_collect_container_user_definitions", user_definitions
    )
    for phase in (
        "_collect_container_configs",
        "_collect_container_project_tree",
        "_collect_container_global_skills",
        "_collect_container_hidden_artifacts",
        "_collect_standard_container_npm_agents",
    ):
        monkeypatch.setattr(containers_module, phase, lambda *_a, **_k: None)

    containers = [
        DiscoveredContainer(
            container_id=f"container-{index}",
            name=None,
            image_ref=None,
            image_digest=None,
        )
        for index in range(2)
    ]

    artifacts = containers_module._collect_container_artifacts(
        collector=SimpleNamespace(),
        containers=containers,
        clients=[],
        deadline=10**12,
        subprocess_timeout=1,
        host_home=Path("/Users/alex"),
    )

    assert extension_walks == ["container-0"]
    assert artifacts.complete is False
    assert artifacts.failure_reason == "container_artifact_collection_failed"


def test_container_budget_exhaustion_still_stops_the_loop(monkeypatch):
    def exhaust(*_a, **_k):
        raise containers_module._CollectionBudgetExhausted()

    monkeypatch.setattr(
        containers_module, "_collect_standard_container_npm_agents", exhaust
    )

    artifacts = containers_module._collect_container_artifacts(
        collector=SimpleNamespace(),
        containers=[
            DiscoveredContainer(
                container_id="c", name=None, image_ref=None, image_digest=None
            )
        ],
        clients=[],
        deadline=10**12,
        subprocess_timeout=1,
        host_home=Path("/Users/alex"),
    )

    assert artifacts.failure_reason == "container_artifact_budget_exhausted"
