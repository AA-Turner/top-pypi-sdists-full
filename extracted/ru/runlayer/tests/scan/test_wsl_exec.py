import io
import json
import sys
import time
from unittest import mock

import pytest

from runlayer_cli.scan import wsl_exec
from runlayer_cli.scan.device import DiscoveredWSLDistro
from runlayer_cli.scan.processes import enumerate as process_enumerate
from runlayer_cli.scan.processes.enumerate import enumerate_wsl_process_tables
from runlayer_cli.scan.wsl_exec import (
    WSLCommandResult,
    run_wsl_command,
    scan_wsl_containers,
)


class _FakeProcess:
    def __init__(self, stdout: bytes) -> None:
        self.stdout = io.BytesIO(stdout)
        self.returncode = 0

    def wait(self, timeout: float | None = None) -> int:
        return self.returncode

    def kill(self) -> None:
        self.returncode = -9


class _TimeoutProcess(_FakeProcess):
    def __init__(self) -> None:
        super().__init__(b"")
        self.wait_calls = 0
        self.killed = False

    def wait(self, timeout: float | None = None) -> int:
        self.wait_calls += 1
        if self.wait_calls == 1:
            raise wsl_exec.subprocess.TimeoutExpired("wsl.exe", timeout)
        return self.returncode

    def kill(self) -> None:
        self.killed = True
        super().kill()


def test_runner_uses_fixed_argv_and_utf8_environment(monkeypatch) -> None:
    captured: dict[str, object] = {}
    credential_names = (
        "runlayer_api_key",
        "RUNLAYER_ORG_API_KEY",
        "Runlayer_Enrollment_API_Key",
        "RUNLAYER_SKILL_SYNC_API_KEY",
        "runlayer_self_update_org_key",
    )
    for name in credential_names:
        monkeypatch.setenv(name, f"{name}-secret")
    monkeypatch.setenv("SYSTEMROOT", r"C:\Windows")
    monkeypatch.setenv("wsl_utf8", "0")
    monkeypatch.setenv(
        "WSLENV",
        (
            "PATH/l:RUNLAYER_API_KEY/u:runlayer_org_api_key/wp:"
            "RUNLAYER_ENROLLMENT_API_KEY:runlayer_skill_sync_api_key/pu:"
            "RUNLAYER_SELF_UPDATE_ORG_KEY/w:SAFE_SETTING/u"
        ),
    )

    def fake_popen(command, **kwargs):
        captured["command"] = command
        captured["environment"] = kwargs["env"]
        return _FakeProcess(b"")

    monkeypatch.setattr(wsl_exec.subprocess, "Popen", fake_popen)

    result = run_wsl_command(
        "Ubuntu 24.04",
        ("ps", *wsl_exec.WSL_PS_ARGS),
    )

    assert result == WSLCommandResult(stdout="")
    assert captured["command"] == [
        "wsl.exe",
        "--distribution",
        "Ubuntu 24.04",
        "--exec",
        "timeout",
        "-s",
        "KILL",
        "9",
        "ps",
        "-axww",
        "-o",
        "pid=,ppid=,user:32=,lstart=,args=",
    ]
    assert captured["environment"]["WSL_UTF8"] == "1"
    assert captured["environment"]["WSLENV"] == "PATH/l:SAFE_SETTING/u"
    assert captured["environment"]["SYSTEMROOT"] == r"C:\Windows"
    environment_names = {name.casefold() for name in captured["environment"]}
    assert environment_names.isdisjoint(name.casefold() for name in credential_names)
    assert sum(name == "wsl_utf8" for name in environment_names) == 1


def test_runner_rejects_non_allowlisted_command() -> None:
    with pytest.raises(ValueError, match="unsupported WSL command"):
        run_wsl_command("Ubuntu", ("sh", "-c", "id"))


def test_runner_uses_one_second_in_vm_deadline_for_short_timeout(
    monkeypatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_popen(command, **_kwargs):
        captured["command"] = command
        return _FakeProcess(b"")

    monkeypatch.setattr(wsl_exec.subprocess, "Popen", fake_popen)

    result = run_wsl_command(
        "Ubuntu",
        ("ps", *wsl_exec.WSL_PS_ARGS),
        timeout=0.1,
    )

    assert result == WSLCommandResult(stdout="")
    assert captured["command"] == [
        "wsl.exe",
        "--distribution",
        "Ubuntu",
        "--exec",
        "timeout",
        "-s",
        "KILL",
        "1",
        "ps",
        *wsl_exec.WSL_PS_ARGS,
    ]


@pytest.mark.parametrize(
    "timeout",
    [0, -1, float("nan"), float("inf"), -float("inf")],
)
def test_runner_isolates_invalid_timeout_without_spawning(
    monkeypatch,
    timeout: float,
) -> None:
    monkeypatch.setattr(
        wsl_exec.subprocess,
        "Popen",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("invalid timeout must not execute")
        ),
    )

    result = run_wsl_command(
        "Ubuntu",
        ("ps", *wsl_exec.WSL_PS_ARGS),
        timeout=timeout,
    )

    assert result is None


def test_runner_bounds_large_timeout_and_emits_plain_duration(monkeypatch) -> None:
    captured: dict[str, object] = {}
    wait_timeouts: list[float | None] = []

    class RecordingProcess(_FakeProcess):
        def wait(self, timeout: float | None = None) -> int:
            wait_timeouts.append(timeout)
            return super().wait(timeout)

    def fake_popen(command, **_kwargs):
        captured["command"] = command
        return RecordingProcess(b"")

    monkeypatch.setattr(wsl_exec.subprocess, "Popen", fake_popen)

    result = run_wsl_command(
        "Ubuntu",
        ("ps", *wsl_exec.WSL_PS_ARGS),
        timeout=sys.float_info.max,
    )

    assert result == WSLCommandResult(stdout="")
    assert captured["command"] == [
        "wsl.exe",
        "--distribution",
        "Ubuntu",
        "--exec",
        "timeout",
        "-s",
        "KILL",
        "299",
        "ps",
        *wsl_exec.WSL_PS_ARGS,
    ]
    assert wait_timeouts == [300.0]


def test_container_scan_uses_runtime_specific_allowlisted_commands(
    monkeypatch,
) -> None:
    commands: list[tuple[str, ...]] = []

    def fake_run(_distro: str, command, **_kwargs):
        commands.append(tuple(command))
        return WSLCommandResult(stdout="")

    monkeypatch.setattr(wsl_exec, "run_wsl_command", fake_run)

    scan_wsl_containers(
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)]
    )

    docker_command = (
        "docker",
        "ps",
        "--last",
        "65",
        "--no-trunc",
        "--filter",
        "status=running",
        "--filter",
        "status=paused",
        "--filter",
        "status=restarting",
        "--format",
        "{{json .}}",
    )
    podman_command = (
        "podman",
        "ps",
        "--last",
        "65",
        "--no-trunc",
        "--filter",
        "status=running",
        "--filter",
        "status=paused",
        "--format",
        "{{json .}}",
    )
    assert commands == [docker_command, podman_command]
    assert wsl_exec._command_is_allowed(docker_command) is True
    assert wsl_exec._command_is_allowed(podman_command) is True
    assert wsl_exec._command_is_allowed(("podman", *docker_command[1:])) is False
    assert wsl_exec._command_is_allowed(("docker", *podman_command[1:])) is False


def test_runner_kills_timed_out_command(monkeypatch) -> None:
    process = _TimeoutProcess()
    monkeypatch.setattr(wsl_exec.subprocess, "Popen", lambda *_args, **_kwargs: process)

    result = run_wsl_command(
        "Ubuntu",
        ("ps", *wsl_exec.WSL_PS_ARGS),
        timeout=0.01,
    )

    assert result is None
    assert process.killed is True
    assert process.wait_calls == 2


def test_runner_rejects_truncated_or_non_utf8_output(monkeypatch) -> None:
    processes = iter(
        [
            _FakeProcess(b"x" * 9),
            _FakeProcess(b"\xff"),
        ]
    )
    monkeypatch.setattr(
        wsl_exec.subprocess,
        "Popen",
        lambda *_args, **_kwargs: next(processes),
    )

    truncated = run_wsl_command(
        "Ubuntu",
        ("ps", *wsl_exec.WSL_PS_ARGS),
        max_output_bytes=8,
    )
    non_utf8 = run_wsl_command(
        "Ubuntu",
        ("ps", *wsl_exec.WSL_PS_ARGS),
    )

    assert truncated is None
    assert non_utf8 is None


def test_scans_docker_containers_and_attributes_distro(monkeypatch) -> None:
    output = json.dumps(
        {
            "ID": "a" * 64,
            "Names": "mcp-server",
            "Image": "example/mcp:latest",
        }
    )

    def fake_run(_distro: str, command, **_kwargs):
        if command[0] == "docker":
            return WSLCommandResult(stdout=f"{output}\n")
        return None

    monkeypatch.setattr(wsl_exec, "run_wsl_command", fake_run)

    result = scan_wsl_containers(
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)]
    )

    assert result.scanned_distros == ["Ubuntu"]
    assert len(result.containers) == 1
    assert result.containers[0].wsl_distro == "Ubuntu"
    assert result.containers[0].to_api_payload()["wsl_distro"] == "Ubuntu"


@pytest.mark.parametrize("bad_row_kind", ["malformed", "blank", "duplicate"])
def test_bad_row_keeps_valid_containers_non_authoritative(
    monkeypatch,
    bad_row_kind: str,
) -> None:
    valid_rows = [
        {
            "ID": "a" * 64,
            "Names": "first-mcp",
            "Image": "example/first:latest",
        },
        {
            "ID": "b" * 64,
            "Names": "second-mcp",
            "Image": "example/second:latest",
        },
    ]
    bad_row = {
        "malformed": "not-json",
        "blank": "",
        "duplicate": json.dumps(valid_rows[0]),
    }[bad_row_kind]
    output = "\n".join([json.dumps(valid_rows[0]), bad_row, json.dumps(valid_rows[1])])

    def fake_run(_distro: str, command, **_kwargs):
        if command[0] == "docker":
            return WSLCommandResult(stdout=output)
        return None

    monkeypatch.setattr(wsl_exec, "run_wsl_command", fake_run)

    result = scan_wsl_containers(
        [
            DiscoveredWSLDistro(
                name="Ubuntu",
                wsl_version=2,
                is_running=True,
                container_runtimes=("docker",),
            )
        ]
    )

    assert [container.container_id for container in result.containers] == [
        "a" * 64,
        "b" * 64,
    ]
    assert result.scanned_distros == []


def test_parses_podman_id_row_once_and_preserves_metadata(monkeypatch) -> None:
    output = json.dumps(
        {
            "Id": "b" * 64,
            "Names": ["podman-mcp"],
            "Image": "quay.io/example/mcp:latest",
        }
    )
    original_loads = json.loads
    parse_json = mock.Mock(wraps=original_loads)
    monkeypatch.setattr(wsl_exec.json, "loads", parse_json)

    containers, complete = wsl_exec._parse_container_rows(
        output,
        runtime="podman",
        distro="Fedora",
    )

    assert complete is True
    assert parse_json.call_count == 1
    assert [
        (
            container.container_id,
            container.name,
            container.image_ref,
            container.runtime,
            container.wsl_distro,
        )
        for container in containers
    ] == [
        (
            "b" * 64,
            "podman-mcp",
            "quay.io/example/mcp:latest",
            "podman",
            "Fedora",
        )
    ]


def test_expected_runtime_failure_keeps_distro_non_authoritative(monkeypatch) -> None:
    output = json.dumps(
        {
            "ID": "a" * 64,
            "Names": "mcp-server",
            "Image": "example/mcp:latest",
        }
    )

    def fake_run(_distro: str, command, **_kwargs):
        if command[0] == "docker":
            return WSLCommandResult(stdout=f"{output}\n")
        return None

    monkeypatch.setattr(wsl_exec, "run_wsl_command", fake_run)

    result = scan_wsl_containers(
        [
            DiscoveredWSLDistro(
                name="Ubuntu",
                wsl_version=2,
                is_running=True,
                container_runtimes=("docker", "podman"),
            )
        ]
    )

    assert len(result.containers) == 1
    assert result.scanned_distros == []


def test_docker_wins_for_duplicate_container_exposed_by_podman_shim(
    monkeypatch,
) -> None:
    container_id = "c" * 64

    def fake_run(_distro: str, command, **_kwargs):
        runtime = command[0]
        return WSLCommandResult(
            stdout=json.dumps(
                {
                    "ID" if runtime == "docker" else "Id": container_id,
                    "Names": f"{runtime}-name",
                    "Image": f"example/{runtime}:latest",
                }
            )
        )

    monkeypatch.setattr(wsl_exec, "run_wsl_command", fake_run)

    result = scan_wsl_containers(
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)]
    )

    assert [
        (container.runtime, container.name, container.image_ref)
        for container in result.containers
    ] == [("docker", "docker-name", "example/docker:latest")]


def test_container_checkpoint_runs_before_each_runtime_and_propagates(
    monkeypatch,
) -> None:
    commands: list[str] = []
    checkpoints = 0

    def fake_run(_distro: str, command, **_kwargs):
        commands.append(command[0])
        return WSLCommandResult(stdout="")

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1
        if checkpoints == 2:
            raise RuntimeError("scan stopped")

    monkeypatch.setattr(wsl_exec, "run_wsl_command", fake_run)

    with pytest.raises(RuntimeError, match="scan stopped"):
        scan_wsl_containers(
            [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)],
            checkpoint=checkpoint,
        )

    assert checkpoints == 2
    assert commands == ["docker"]


def test_container_scan_stops_at_aggregate_deadline(monkeypatch) -> None:
    clock = 0.0
    calls: list[tuple[str, str]] = []
    timeouts: list[float] = []

    def fake_run(distro: str, command, **kwargs):
        nonlocal clock
        calls.append((distro, command[0]))
        command_timeout = kwargs["timeout"]
        timeouts.append(command_timeout)
        clock += min(command_timeout, 0.6)
        return WSLCommandResult(stdout="")

    monkeypatch.setattr(time, "monotonic", lambda: clock)
    monkeypatch.setattr(
        wsl_exec,
        "WSL_CONTAINER_SCAN_TIME_BUDGET_S",
        1.0,
        raising=False,
    )
    monkeypatch.setattr(wsl_exec, "run_wsl_command", fake_run)

    result = scan_wsl_containers(
        [
            DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True),
            DiscoveredWSLDistro(name="Debian", wsl_version=2, is_running=True),
        ]
    )

    assert calls == [("Ubuntu", "docker"), ("Ubuntu", "podman")]
    assert timeouts == pytest.approx([1.0, 0.4])
    assert result.scanned_distros == ["Ubuntu"]


@pytest.mark.parametrize(
    ("container_runtimes", "expected_scanned_distros"),
    [
        (("docker",), ["Ubuntu"]),
        (("docker", "podman"), []),
    ],
)
def test_container_scan_deadline_only_invalidates_unprobed_expected_runtime(
    monkeypatch,
    container_runtimes: tuple[str, ...],
    expected_scanned_distros: list[str],
) -> None:
    clock = 0.0
    calls: list[str] = []

    def fake_run(_distro: str, command, **_kwargs):
        nonlocal clock
        calls.append(command[0])
        clock = 1.0
        return WSLCommandResult(stdout="")

    monkeypatch.setattr(time, "monotonic", lambda: clock)
    monkeypatch.setattr(
        wsl_exec,
        "WSL_CONTAINER_SCAN_TIME_BUDGET_S",
        1.0,
    )
    monkeypatch.setattr(wsl_exec, "run_wsl_command", fake_run)

    result = scan_wsl_containers(
        [
            DiscoveredWSLDistro(
                name="Ubuntu",
                wsl_version=2,
                is_running=True,
                container_runtimes=container_runtimes,
            )
        ]
    )

    assert calls == ["docker"]
    assert result.scanned_distros == expected_scanned_distros


def test_skips_stopped_and_docker_desktop_distros(monkeypatch) -> None:
    monkeypatch.setattr(
        wsl_exec,
        "run_wsl_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("skipped distro must not execute")
        ),
    )

    result = scan_wsl_containers(
        [
            DiscoveredWSLDistro(
                name="Ubuntu",
                wsl_version=2,
                is_running=False,
            ),
            DiscoveredWSLDistro(
                name="docker-desktop",
                wsl_version=2,
                is_running=True,
            ),
        ]
    )

    assert result.containers == []
    assert result.scanned_distros == []


def test_container_scan_respects_cross_distro_result_cap(monkeypatch) -> None:
    calls: list[str] = []

    def fake_run(distro: str, command, **_kwargs):
        calls.append(distro)
        if command[0] != "docker":
            return None
        return WSLCommandResult(
            stdout=json.dumps(
                {
                    "ID": distro.casefold(),
                    "Names": distro,
                    "Image": "example/mcp:latest",
                }
            )
        )

    monkeypatch.setattr(wsl_exec, "run_wsl_command", fake_run)

    result = scan_wsl_containers(
        [
            DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True),
            DiscoveredWSLDistro(name="Debian", wsl_version=2, is_running=True),
        ],
        max_containers=1,
    )

    assert [container.wsl_distro for container in result.containers] == ["Ubuntu"]
    assert result.scanned_distros == ["Ubuntu"]
    assert "Debian" not in calls


def test_enumerates_and_attributes_wsl_processes(monkeypatch) -> None:
    monkeypatch.setattr(
        "runlayer_cli.scan.processes.enumerate.run_wsl_command",
        lambda *_args, **_kwargs: WSLCommandResult(
            stdout=(
                "123 1 alice Wed Jul 15 09:27:01 2026 "
                "/usr/local/bin/claude --mcp-server\n"
            )
        ),
    )

    candidates = enumerate_wsl_process_tables(
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)],
    )

    assert len(candidates) == 1
    assert candidates[0].pid == 123
    assert candidates[0].argv == ["/usr/local/bin/claude", "--mcp-server"]
    assert candidates[0].wsl_distro == "Ubuntu"


def test_wsl_process_failure_isolated_per_distro(monkeypatch) -> None:
    def fake_run(distro: str, *_args, **_kwargs):
        if distro == "Ubuntu":
            return None
        return WSLCommandResult(
            stdout="321 1 bob Wed Jul 15 09:27:01 2026 /usr/bin/codex\n"
        )

    monkeypatch.setattr(
        "runlayer_cli.scan.processes.enumerate.run_wsl_command",
        fake_run,
    )

    candidates = enumerate_wsl_process_tables(
        [
            DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True),
            DiscoveredWSLDistro(name="Debian", wsl_version=2, is_running=True),
        ],
    )

    assert [(candidate.pid, candidate.wsl_distro) for candidate in candidates] == [
        (321, "Debian")
    ]


def test_wsl_process_enumeration_stops_at_aggregate_deadline(monkeypatch) -> None:
    clock = 0.0
    calls: list[str] = []
    timeouts: list[float] = []

    def fake_run(distro: str, *_args, **kwargs):
        nonlocal clock
        calls.append(distro)
        command_timeout = kwargs["timeout"]
        timeouts.append(command_timeout)
        clock += min(command_timeout, 0.6)
        return WSLCommandResult(stdout="")

    monkeypatch.setattr(time, "monotonic", lambda: clock)
    monkeypatch.setattr(
        process_enumerate,
        "WSL_PROCESS_SCAN_TIME_BUDGET_S",
        1.0,
        raising=False,
    )
    monkeypatch.setattr(process_enumerate, "run_wsl_command", fake_run)

    candidates = enumerate_wsl_process_tables(
        [
            DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True),
            DiscoveredWSLDistro(name="Debian", wsl_version=2, is_running=True),
            DiscoveredWSLDistro(name="Fedora", wsl_version=2, is_running=True),
        ],
    )

    assert calls == ["Ubuntu", "Debian"]
    assert timeouts == pytest.approx([1.0, 0.4])
    assert candidates == []


def test_wsl_process_checkpoint_runs_before_execution_and_propagates(
    monkeypatch,
) -> None:
    commands: list[str] = []
    checkpoints = 0

    def fake_run(distro: str, *_args, **_kwargs):
        commands.append(distro)
        return WSLCommandResult(stdout="")

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1
        if checkpoints == 2:
            raise RuntimeError("scan stopped")

    monkeypatch.setattr(
        "runlayer_cli.scan.processes.enumerate.run_wsl_command",
        fake_run,
    )

    with pytest.raises(RuntimeError, match="scan stopped"):
        enumerate_wsl_process_tables(
            [
                DiscoveredWSLDistro(
                    name="Ubuntu",
                    wsl_version=2,
                    is_running=True,
                ),
                DiscoveredWSLDistro(
                    name="Debian",
                    wsl_version=2,
                    is_running=True,
                ),
            ],
            checkpoint=checkpoint,
        )

    assert checkpoints == 2
    assert commands == ["Ubuntu"]
