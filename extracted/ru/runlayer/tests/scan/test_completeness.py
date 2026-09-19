from dataclasses import fields
import threading

import pytest

from runlayer_cli.scan.agent_scan import AgentScanResult
from runlayer_cli.scan.completeness import ScanCompleteness, ScanCompletionStatus
from runlayer_cli.scan.hidden_space_sweep import HiddenSpaceScanResult
from runlayer_cli.scan.orchestrator import (
    CompletenessPhaseStatuses,
    GlobalPhaseResult,
    ProjectPhaseResult,
    _assemble_completeness,
)


def _assemble(
    *,
    global_result: GlobalPhaseResult | None = None,
    project_result: ProjectPhaseResult | None = None,
    phase_statuses: CompletenessPhaseStatuses | None = None,
    hidden_space_result: HiddenSpaceScanResult | None = None,
    scan_projects: bool = True,
    detect_agents: bool = True,
    run_static_agents: bool = True,
    detect_disguised_skills: bool = True,
    machine_scope: bool = True,
    install_agent_result: AgentScanResult | None = None,
    static_agent_result: AgentScanResult | None = None,
) -> ScanCompleteness:
    return _assemble_completeness(
        scan_projects=scan_projects,
        detect_agents=detect_agents,
        run_static_agents=run_static_agents,
        detect_disguised_skills=detect_disguised_skills,
        machine_scope=machine_scope,
        global_result=global_result or GlobalPhaseResult(),
        project_result=project_result or ProjectPhaseResult(),
        hidden_space_result=hidden_space_result or HiddenSpaceScanResult(),
        phase_statuses=phase_statuses or CompletenessPhaseStatuses(),
        install_agent_result=install_agent_result,
        static_agent_result=static_agent_result,
    )


def _incomplete_surfaces(completeness: ScanCompleteness) -> set[str]:
    return {
        item.name
        for item in fields(ScanCompleteness)
        if not getattr(completeness, item.name).complete
    }


@pytest.mark.parametrize(
    ("source", "expected_surfaces"),
    [
        pytest.param(
            "global.completion",
            {"mcp_host_static", "wsl_static", "client_presence"},
            id="global-config-and-extension",
        ),
        pytest.param(
            "project.completion",
            {
                "mcp_host_static",
                "skill_host_static",
                "plugin_host_static",
                "agent_host_static",
                "agent_definition_host_static",
                "wsl_static",
                "client_presence",
            },
            id="project-crawl",
        ),
        pytest.param(
            "project.mcp_completion",
            {"mcp_host_static", "wsl_static", "client_presence"},
            id="project-config",
        ),
        pytest.param(
            "project.skill_completion",
            {
                "skill_host_static",
                "agent_host_static",
                "wsl_static",
                "client_presence",
            },
            id="project-skill",
        ),
        pytest.param(
            "project.definition_completion",
            {"agent_definition_host_static", "wsl_static", "client_presence"},
            id="project-agent-definition",
        ),
        pytest.param(
            "statuses.hidden_spaces",
            {"skill_host_static", "wsl_static", "client_presence"},
            id="hidden-space",
        ),
        pytest.param(
            "statuses.plugin_configurations",
            {
                "mcp_host_static",
                "plugin_host_static",
                "wsl_static",
                "client_presence",
            },
            id="plugin-config",
        ),
        pytest.param(
            "statuses.global_skills",
            {"skill_host_static", "wsl_static", "client_presence"},
            id="global-skill",
        ),
        pytest.param(
            "statuses.user_agent_definitions",
            {"agent_definition_host_static", "wsl_static", "client_presence"},
            id="user-agent-definition",
        ),
        pytest.param(
            "statuses.disguised_skills",
            {"skill_host_static", "wsl_static", "client_presence"},
            id="disguised-skill",
        ),
        pytest.param(
            "statuses.plugin_artifacts",
            {
                "mcp_host_static",
                "plugin_host_static",
                "wsl_static",
                "client_presence",
            },
            id="plugin-artifact",
        ),
        pytest.param(
            "statuses.plugin_device_artifacts",
            {"plugin_device", "client_presence"},
            id="device-plugin-artifact",
        ),
        pytest.param(
            "statuses.renamed_plugin_caches",
            {"plugin_host_static", "wsl_static", "client_presence"},
            id="renamed-plugin",
        ),
        pytest.param(
            "statuses.wsl_homes",
            {"plugin_host_static", "wsl_static", "client_presence"},
            id="wsl-home",
        ),
    ],
)
def test_assemble_completeness_maps_phase_status_to_dependent_surfaces(
    source: str,
    expected_surfaces: set[str],
) -> None:
    global_result = GlobalPhaseResult()
    project_result = ProjectPhaseResult()
    phase_statuses = CompletenessPhaseStatuses()
    owners = {
        "global": global_result,
        "project": project_result,
        "statuses": phase_statuses,
    }
    owner_name, status_name = source.split(".", maxsplit=1)
    reason = f"{owner_name}_{status_name}_incomplete"
    getattr(owners[owner_name], status_name).mark_incomplete(reason)

    completeness = _assemble(
        global_result=global_result,
        project_result=project_result,
        phase_statuses=phase_statuses,
    )

    assert _incomplete_surfaces(completeness) == expected_surfaces
    for surface in expected_surfaces:
        assert getattr(completeness, surface).reasons == [reason]


@pytest.mark.parametrize(
    ("detect_disguised_skills", "expected_surfaces"),
    [
        (False, {"wsl_static", "client_presence"}),
        (True, {"skill_host_static", "wsl_static", "client_presence"}),
    ],
)
def test_assemble_completeness_maps_hidden_space_truncation(
    detect_disguised_skills: bool,
    expected_surfaces: set[str],
) -> None:
    completeness = _assemble(
        hidden_space_result=HiddenSpaceScanResult(node_modules_paths_truncated=True),
        detect_disguised_skills=detect_disguised_skills,
    )

    assert _incomplete_surfaces(completeness) == expected_surfaces
    for surface in expected_surfaces:
        assert getattr(completeness, surface).reasons == ["hidden_space_scan_truncated"]


def test_assemble_completeness_keeps_agent_failures_out_of_client_presence() -> None:
    agent_completion = ScanCompletionStatus()
    agent_completion.mark_incomplete("agent_install_probe_failed")
    completeness = _assemble(
        install_agent_result=AgentScanResult(completion=agent_completion)
    )

    assert _incomplete_surfaces(completeness) == {"agent_host_static"}
    assert completeness.client_presence.complete is True


@pytest.mark.parametrize(
    ("detect_agents", "run_static_agents", "expected_reason"),
    [
        (False, False, "agent_detection_disabled"),
        (True, False, "agent_static_scan_disabled"),
    ],
)
def test_assemble_completeness_marks_skipped_agent_phases_incomplete(
    detect_agents: bool,
    run_static_agents: bool,
    expected_reason: str,
) -> None:
    completeness = _assemble(
        detect_agents=detect_agents,
        run_static_agents=run_static_agents,
    )

    assert _incomplete_surfaces(completeness) == {"agent_host_static"}
    assert completeness.agent_host_static.reasons == [expected_reason]


def test_assemble_completeness_marks_disabled_machine_scope_incomplete() -> None:
    completeness = _assemble(machine_scope=False)

    assert _incomplete_surfaces(completeness) == {
        "plugin_device",
        "client_presence",
    }
    assert completeness.plugin_device.reasons == ["machine_scope_scan_disabled"]
    assert completeness.client_presence.reasons == ["machine_scope_scan_disabled"]


def test_assemble_completeness_dedupes_source_reasons() -> None:
    global_result = GlobalPhaseResult()
    phase_statuses = CompletenessPhaseStatuses()
    global_result.completion.mark_incomplete("shared_read_failure")
    phase_statuses.plugin_configurations.mark_incomplete("shared_read_failure")

    completeness = _assemble(
        global_result=global_result,
        phase_statuses=phase_statuses,
    )

    assert completeness.client_presence.reasons == ["shared_read_failure"]


def test_assemble_completeness_maps_disabled_project_scan() -> None:
    completeness = _assemble(scan_projects=False)

    assert _incomplete_surfaces(completeness) == {
        "mcp_host_static",
        "skill_host_static",
        "plugin_host_static",
        "agent_host_static",
        "agent_definition_host_static",
        "wsl_static",
        "client_presence",
    }


def test_assemble_completeness_propagates_plugin_failure_to_device_scope() -> None:
    phase_statuses = CompletenessPhaseStatuses()
    phase_statuses.plugin_artifacts.mark_incomplete("plugin_artifact_scan_failed")

    completeness = _assemble(phase_statuses=phase_statuses)

    assert _incomplete_surfaces(completeness) == {
        "mcp_host_static",
        "plugin_host_static",
        "plugin_device",
        "wsl_static",
        "client_presence",
    }


def test_merge_preserves_incomplete_status_without_reasons() -> None:
    target = ScanCompletionStatus()
    source = ScanCompletionStatus(complete=False)

    target.merge(source)

    assert target.complete is False
    assert target.reasons == []


def test_merge_snapshots_source_under_lock() -> None:
    target = ScanCompletionStatus()
    source = ScanCompletionStatus()
    merge_started = threading.Event()
    merge_finished = threading.Event()

    def merge_source() -> None:
        merge_started.set()
        target.merge(source)
        merge_finished.set()

    with source._lock:
        thread = threading.Thread(target=merge_source, daemon=True)
        thread.start()
        assert merge_started.wait(timeout=1)
        assert not merge_finished.wait(timeout=0.1)
        source.complete = False
        source.reasons.extend(["shared", "new", "shared"])

    assert merge_finished.wait(timeout=1)
    thread.join(timeout=1)
    assert target.complete is False
    assert target.reasons == ["shared", "new"]


def test_merge_self_does_not_deadlock() -> None:
    status = ScanCompletionStatus(complete=False, reasons=["failure"])
    merge_finished = threading.Event()

    def merge_self() -> None:
        status.merge(status)
        merge_finished.set()

    thread = threading.Thread(target=merge_self, daemon=True)
    thread.start()

    assert merge_finished.wait(timeout=1)
    thread.join(timeout=1)
    assert status.complete is False
    assert status.reasons == ["failure"]
