"""Shared service/container probe tests."""

from unittest import mock

from runlayer_cli.scan.agents.install import AgentRuntimeSignature
from runlayer_cli.scan.device import DiscoveredWSLDistro
from runlayer_cli.scan.processes import discover_processes
from runlayer_cli.scan.processes.classify import ClassifierContext, classify_processes
from runlayer_cli.scan.processes.models import ProcessCandidate
from runlayer_cli.scan.processes.probes import (
    parse_launchctl_pid,
    parse_systemd_main_pid,
    probe_agent_runtime,
)


def _signature() -> AgentRuntimeSignature:
    return AgentRuntimeSignature(
        framework_id="openclaw",
        argv_markers=("openclaw",),
        gateway_ports=lambda: (18789,),
        launchd_labels=lambda: ("bot.molt.gateway",),
        systemd_units=lambda: ("openclaw-gateway.service",),
        docker_markers=("openclaw",),
    )


def test_parse_service_pids():
    assert parse_launchctl_pid("state = running\n\tpid = 4321\n") == 4321
    assert parse_launchctl_pid("state = running\n") is None
    assert parse_systemd_main_pid("9876\n") == 9876
    assert parse_systemd_main_pid("0\n") is None


@mock.patch(
    "runlayer_cli.scan.processes.probes._run_success",
    return_value="state = running\n\tpid = 42\n",
)
@mock.patch("runlayer_cli.scan.processes.probes.shutil.which", return_value=None)
@mock.patch("runlayer_cli.scan.processes.probes.os.getuid", return_value=501)
@mock.patch("runlayer_cli.scan.processes.probes.platform.system", return_value="Darwin")
def test_launchd_probe_annotates_enumerated_pid(
    mock_system, mock_uid, mock_which, mock_run
):
    candidate = ProcessCandidate(pid=42, argv=["node", "gateway.js"])

    result = probe_agent_runtime([candidate], [_signature()], timeout=5)

    assert result == [candidate]
    assert candidate.agent_runtime_signals == {"openclaw": ["service:launchd"]}
    mock_run.assert_called_once_with(
        ["launchctl", "print", "gui/501/bot.molt.gateway"],
        timeout=5,
    )


@mock.patch(
    "runlayer_cli.scan.processes.probes._run_success",
    return_value="state = running\n",
)
@mock.patch("runlayer_cli.scan.processes.probes.shutil.which", return_value=None)
@mock.patch("runlayer_cli.scan.processes.probes.os.getuid", return_value=501)
@mock.patch("runlayer_cli.scan.processes.probes.platform.system", return_value="Darwin")
def test_service_without_pid_emits_runtime_probe(
    mock_system, mock_uid, mock_which, mock_run
):
    result = probe_agent_runtime([], [_signature()], timeout=5)

    assert len(result) == 1
    assert result[0].pid < 0
    assert result[0].discovery_source == "runtime_probe"
    assert result[0].agent_runtime_signals == {"openclaw": ["service:launchd"]}


@mock.patch(
    "runlayer_cli.scan.processes.probes._run_success",
    return_value="state = not running\n",
)
@mock.patch("runlayer_cli.scan.processes.probes.shutil.which", return_value=None)
@mock.patch("runlayer_cli.scan.processes.probes.os.getuid", return_value=501)
@mock.patch("runlayer_cli.scan.processes.probes.platform.system", return_value="Darwin")
def test_loaded_but_stopped_launchd_job_is_not_running(
    mock_system, mock_uid, mock_which, mock_run
):
    assert probe_agent_runtime([], [_signature()], timeout=5) == []


@mock.patch(
    "runlayer_cli.scan.processes.probes._run_success",
    return_value="state = running\n",
)
@mock.patch("runlayer_cli.scan.processes.probes.shutil.which", return_value=None)
@mock.patch("runlayer_cli.scan.processes.probes.os.getuid", return_value=501)
@mock.patch("runlayer_cli.scan.processes.probes.platform.system", return_value="Darwin")
def test_service_profile_name_is_not_submitted(
    mock_system, mock_uid, mock_which, mock_run
):
    profile = "customer-project"
    signature = AgentRuntimeSignature(
        framework_id="openclaw",
        argv_markers=("openclaw",),
        gateway_ports=lambda: (),
        launchd_labels=lambda: (f"bot.molt.gateway.{profile}",),
        systemd_units=lambda: (),
        docker_markers=(),
    )

    candidates = probe_agent_runtime([], [signature], timeout=5)
    sightings = classify_processes(
        candidates,
        ClassifierContext(),
    )

    assert len(sightings) == 1
    assert profile not in " ".join(sightings[0].ai_signals)


@mock.patch(
    "runlayer_cli.scan.processes.probes._run_success",
    side_effect=["active\n", "123\n"],
)
@mock.patch("runlayer_cli.scan.processes.probes.shutil.which", return_value=None)
@mock.patch("runlayer_cli.scan.processes.probes.platform.system", return_value="Linux")
def test_systemd_probe_resolves_main_pid(mock_system, mock_which, mock_run):
    candidate = ProcessCandidate(pid=123, argv=["node", "gateway.js"])

    result = probe_agent_runtime([candidate], [_signature()], timeout=5)

    assert result == [candidate]
    assert candidate.agent_runtime_signals == {"openclaw": ["service:systemd"]}
    assert mock_run.call_count == 2


@mock.patch(
    "runlayer_cli.scan.processes.probes._run_success",
    return_value="abc\topenclaw-gw\topenclaw/gateway:latest\n",
)
@mock.patch(
    "runlayer_cli.scan.processes.probes.shutil.which", return_value="/bin/docker"
)
@mock.patch(
    "runlayer_cli.scan.processes.probes.platform.system", return_value="Windows"
)
def test_docker_is_enumerated_once_for_all_signatures(
    mock_system, mock_which, mock_run
):
    other = AgentRuntimeSignature(
        framework_id="other",
        argv_markers=("other",),
        gateway_ports=lambda: (),
        launchd_labels=lambda: (),
        systemd_units=lambda: (),
        docker_markers=("other-image",),
    )

    result = probe_agent_runtime([], [_signature(), other], timeout=7)

    assert len(result) == 1
    assert result[0].agent_runtime_signals == {"openclaw": ["docker"]}
    sightings = classify_processes(result, ClassifierContext())
    assert len(sightings) == 1
    assert sightings[0].confidence >= 0.7
    assert sightings[0].agent_root_path == "runtime:docker:openclaw"
    mock_run.assert_called_once_with(
        ["docker", "ps", "--format", "{{.ID}}\t{{.Names}}\t{{.Image}}"],
        timeout=7,
    )


@mock.patch(
    "runlayer_cli.scan.processes.probes._run_success",
    side_effect=[
        "state = running\n\tpid = 42\n",
        "abc\topenclaw-gw\topenclaw/gateway:latest\n",
    ],
)
@mock.patch(
    "runlayer_cli.scan.processes.probes.shutil.which", return_value="/bin/docker"
)
@mock.patch("runlayer_cli.scan.processes.probes.os.getuid", return_value=501)
@mock.patch("runlayer_cli.scan.processes.probes.platform.system", return_value="Darwin")
def test_host_service_and_docker_are_separate_installations(
    mock_system, mock_uid, mock_which, mock_run
):
    candidates = probe_agent_runtime(
        [ProcessCandidate(pid=42, argv=["node", "gateway.js"])],
        [_signature()],
        timeout=5,
    )
    sightings = classify_processes(candidates, ClassifierContext())

    assert len(candidates) == 2
    assert {sighting.agent_root_path for sighting in sightings} == {
        "runtime:openclaw",
        "runtime:docker:openclaw",
    }


@mock.patch("runlayer_cli.scan.processes.probe_agent_runtime")
@mock.patch(
    "runlayer_cli.scan.processes.enumerate_candidates",
    return_value=[ProcessCandidate(pid=42, argv=["openclaw", "serve"])],
)
def test_detect_agents_false_skips_runtime_agent_channel(mock_enumerate, mock_probe):
    result = discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
    )

    assert result.processes == []
    assert result.override_config_refs == []
    mock_probe.assert_not_called()


@mock.patch(
    "runlayer_cli.scan.processes.probe_agent_runtime",
    side_effect=RuntimeError("probe failed"),
)
@mock.patch(
    "runlayer_cli.scan.processes.enumerate_candidates",
    return_value=[
        ProcessCandidate(
            pid=42,
            argv=["npx", "@modelcontextprotocol/server-filesystem"],
        )
    ],
)
def test_probe_failure_preserves_primary_process_enumeration(
    mock_enumerate, mock_probe
):
    result = discover_processes(configurations=[], clients=[])

    assert len(result.processes) == 1
    assert result.processes[0].pid == 42


@mock.patch("runlayer_cli.scan.processes.enumerate_wsl_process_tables", return_value=[])
@mock.patch("runlayer_cli.scan.processes.enumerate_candidates", return_value=[])
def test_discovery_forwards_checkpoint_to_wsl_enumeration(
    mock_enumerate,
    mock_wsl_enumerate,
):
    checkpoint = mock.Mock()
    distro = DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)

    discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
        wsl_distros=[distro],
        checkpoint=checkpoint,
    )

    mock_wsl_enumerate.assert_called_once_with(
        [distro],
        timeout=5,
        checkpoint=checkpoint,
    )


@mock.patch("runlayer_cli.scan.processes.enumerate_wsl_process_tables", return_value=[])
@mock.patch(
    "runlayer_cli.scan.processes.enumerate_candidates",
    side_effect=RuntimeError("host enumeration failed"),
)
def test_host_enumeration_failure_still_scans_wsl(
    mock_enumerate,
    mock_wsl_enumerate,
):
    distro = DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)

    result = discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
        wsl_distros=[distro],
    )

    mock_enumerate.assert_called_once_with(timeout=5)
    mock_wsl_enumerate.assert_called_once()
    assert result.processes == []


@mock.patch(
    "runlayer_cli.scan.processes.classify_processes_with_overrides",
    side_effect=RuntimeError("classification failed"),
)
@mock.patch("runlayer_cli.scan.processes.enumerate_wsl_process_tables", return_value=[])
@mock.patch("runlayer_cli.scan.processes.enumerate_candidates", return_value=[])
def test_classification_failure_returns_empty_result(
    mock_enumerate,
    mock_wsl_enumerate,
    mock_classify,
):
    distro = DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)

    result = discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
        wsl_distros=[distro],
    )

    mock_enumerate.assert_called_once_with(timeout=5)
    mock_wsl_enumerate.assert_called_once()
    mock_classify.assert_called_once()
    assert result.processes == []
