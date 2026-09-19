from __future__ import annotations

import ctypes
from types import SimpleNamespace
from unittest.mock import MagicMock

from runlayer_cli.scan import processes
from runlayer_cli.scan.processes.models import ProcessCandidate, ProcessDiscoveryResult
from runlayer_cli.scan.processes.windows_owner import windows_process_owner_sid


def _candidate(pid: int) -> ProcessCandidate:
    return ProcessCandidate(pid=pid, exe="cursor.exe", argv=["cursor.exe"])


def _install_discovery_seams(monkeypatch, owners: dict[int, str | None]) -> None:
    monkeypatch.setattr(
        processes,
        "enumerate_candidates",
        lambda **_kwargs: [_candidate(101), _candidate(202)],
    )
    monkeypatch.setattr(processes, "enumerate_wsl_process_tables", lambda *_a, **_k: [])
    monkeypatch.setattr(
        processes,
        "windows_process_owner_sid",
        lambda pid: owners[pid],
    )
    monkeypatch.setattr(processes, "build_context", lambda *_a, **_k: object())
    monkeypatch.setattr(
        processes,
        "classify_processes_with_overrides",
        lambda candidates, *_a, **_k: ProcessDiscoveryResult(
            processes=list(candidates),
        ),
    )


def test_profile_discovery_attributes_each_host_process_to_only_its_sid(
    monkeypatch,
) -> None:
    _install_discovery_seams(
        monkeypatch,
        {
            101: "S-1-5-21-1-2-3-1001",
            202: "S-1-5-21-1-2-3-1002",
        },
    )

    alice = processes.discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
        windows_user_sid="S-1-5-21-1-2-3-1001",
    )
    bob = processes.discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
        windows_user_sid="S-1-5-21-1-2-3-1002",
    )

    assert [process.pid for process in alice.processes] == [101]
    assert [process.pid for process in bob.processes] == [202]
    assert alice.processes[0].owner_sid == "S-1-5-21-1-2-3-1001"
    assert bob.processes[0].owner_sid == "S-1-5-21-1-2-3-1002"
    assert {process.pid for process in alice.processes}.isdisjoint(
        process.pid for process in bob.processes
    )


def test_profile_discovery_filters_candidates_added_by_agent_probes(
    monkeypatch,
) -> None:
    _install_discovery_seams(
        monkeypatch,
        {
            101: "S-1-5-21-1-2-3-1001",
            202: "S-1-5-21-1-2-3-1002",
            303: "S-1-5-21-1-2-3-1002",
        },
    )

    def probe_agent_runtime(candidates, *_args, **_kwargs):
        synthetic = ProcessCandidate(pid=-1, discovery_source="runtime_probe")
        synthetic.agent_runtime_signals = {"openclaw": ["docker"]}
        return [*candidates, _candidate(303), synthetic]

    monkeypatch.setattr(processes, "probe_agent_runtime", probe_agent_runtime)

    result = processes.discover_processes(
        configurations=[],
        clients=[],
        windows_user_sid="S-1-5-21-1-2-3-1001",
    )

    assert [process.pid for process in result.processes] == [101]
    assert result.complete is False
    assert result.incomplete_reasons == ["process_owner_lookup_failed"]


def test_profile_discovery_skips_unattributable_process_without_losing_authority(
    monkeypatch,
) -> None:
    _install_discovery_seams(
        monkeypatch,
        {
            101: "S-1-5-21-1-2-3-1001",
            202: None,
        },
    )
    classified_pids: list[int] = []

    def classify(candidates, *_args, **_kwargs):
        classified_pids.extend(candidate.pid for candidate in candidates)
        return ProcessDiscoveryResult(
            processes=[candidate for candidate in candidates if candidate.pid == 101],
        )

    monkeypatch.setattr(
        processes,
        "classify_processes_with_overrides",
        classify,
    )

    result = processes.discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
        windows_user_sid="S-1-5-21-1-2-3-1001",
    )

    assert classified_pids == [101, 202]
    assert [process.pid for process in result.processes] == [101]
    assert result.complete is True
    assert "process_owner_lookup_failed" not in result.incomplete_reasons


def test_profile_discovery_marks_reportable_owner_gap_incomplete(monkeypatch) -> None:
    _install_discovery_seams(
        monkeypatch,
        {
            101: "S-1-5-21-1-2-3-1001",
            202: None,
        },
    )

    result = processes.discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
        windows_user_sid="S-1-5-21-1-2-3-1001",
    )

    assert [process.pid for process in result.processes] == [101]
    assert result.complete is False
    assert result.incomplete_reasons == ["process_owner_lookup_failed"]


def test_profile_discovery_keeps_target_profiles_wsl_candidates(monkeypatch) -> None:
    _install_discovery_seams(
        monkeypatch,
        {
            101: "S-1-5-21-1-2-3-1001",
            202: "S-1-5-21-1-2-3-1002",
        },
    )
    wsl = _candidate(303)
    wsl.wsl_distro = "Ubuntu"
    monkeypatch.setattr(
        processes,
        "enumerate_wsl_process_tables",
        lambda *_a, **_k: [wsl],
    )

    result = processes.discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
        windows_user_sid="S-1-5-21-1-2-3-1001",
    )

    assert [process.pid for process in result.processes] == [101, 303]


def test_profile_discovery_distinguishes_host_and_wsl_with_same_pid(
    monkeypatch,
) -> None:
    _install_discovery_seams(
        monkeypatch,
        {
            101: "S-1-5-21-1-2-3-1001",
            202: None,
        },
    )
    wsl = _candidate(202)
    wsl.wsl_distro = "Ubuntu"
    monkeypatch.setattr(
        processes,
        "enumerate_wsl_process_tables",
        lambda *_a, **_k: [wsl],
    )

    result = processes.discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
        windows_user_sid="S-1-5-21-1-2-3-1001",
    )

    assert [
        (process.pid, process.wsl_distro, process.owner_sid)
        for process in result.processes
    ] == [
        (101, None, "S-1-5-21-1-2-3-1001"),
        (202, "Ubuntu", None),
    ]
    assert result.complete is False
    assert result.incomplete_reasons == ["process_owner_lookup_failed"]


def test_ordinary_discovery_does_not_filter_by_windows_owner(monkeypatch) -> None:
    _install_discovery_seams(
        monkeypatch,
        {
            101: "S-1-5-21-1-2-3-1001",
            202: "S-1-5-21-1-2-3-1002",
        },
    )
    owner_calls: list[int] = []
    monkeypatch.setattr(
        processes,
        "windows_process_owner_sid",
        lambda pid: owner_calls.append(pid) or None,
    )

    result = processes.discover_processes(
        configurations=[],
        clients=[],
        detect_agents=False,
    )

    assert [process.pid for process in result.processes] == [101, 202]
    assert result.complete is True
    assert owner_calls == []


def test_windows_owner_lookup_closes_process_and_token_on_metadata_failure(
    monkeypatch,
) -> None:
    kernel32 = MagicMock()
    advapi32 = MagicMock()
    kernel32.OpenProcess.return_value = 77

    def open_token(_process, _access, token_pointer):
        ctypes.cast(
            token_pointer,
            ctypes.POINTER(ctypes.c_void_p),
        ).contents.value = 88
        return True

    advapi32.OpenProcessToken.side_effect = open_token
    advapi32.GetTokenInformation.return_value = False
    monkeypatch.setattr(
        ctypes,
        "windll",
        SimpleNamespace(kernel32=kernel32, advapi32=advapi32),
        raising=False,
    )

    assert windows_process_owner_sid(101) is None
    closed = [
        getattr(call.args[0], "value", call.args[0])
        for call in kernel32.CloseHandle.call_args_list
    ]
    assert closed == [88, 77]
