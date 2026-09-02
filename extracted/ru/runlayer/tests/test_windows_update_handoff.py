"""Detached Windows self-update handoff behavior."""

from __future__ import annotations

import base64
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import subprocess
from typing import cast

import pytest

from runlayer_cli import platform_installers
from runlayer_cli.installer_common import (
    InstallerExecutionError,
    InstallerVerificationError,
)
from runlayer_cli.platform_installers import NativePlatformInstaller
from runlayer_cli.updater import Artifact, InstallDisposition, InstallTarget
from runlayer_cli.windows_update_handoff import WindowsUpdateHandoffInstaller
from tests.platform_installer_helpers import (
    RecordingRunner,
    artifact,
    artifact_path,
    result,
)
from tests.windows_installer_helpers import (
    AIWATCH_PRODUCT_NAME,
    AIWATCH_UPGRADE_CODE,
    authenticode_payload,
)


_TASK_NAME = "AIWatchUpdateHandoff"
_FIXED_NOW = datetime(2026, 7, 20, 10, 30)


@dataclass(frozen=True)
class UpdateCase:
    artifact: Artifact
    source_path: Path
    staging_directory: Path

    @property
    def staged_path(self) -> Path:
        return self.staging_directory / "aiwatch-update.msi"


@pytest.fixture
def update_case(tmp_path: Path) -> UpdateCase:
    value = artifact("windows", "msi", "aiwatch-2.0.0-win-x64.msi")
    return UpdateCase(
        artifact=value,
        source_path=artifact_path(tmp_path, value),
        staging_directory=tmp_path / "program-files" / "Runlayer" / "UpdateStaging",
    )


def _fixed_now() -> datetime:
    return _FIXED_NOW


class HandoffRunner(RecordingRunner):
    def __init__(
        self,
        callback: Callable[
            [dict[str, str]], subprocess.CompletedProcess[str] | None
        ] = lambda _environment: None,
    ) -> None:
        super().__init__()
        self.callback = callback

    def __call__(self, argv: list[str], **kwargs: object):
        environment = cast(dict[str, str] | None, kwargs.get("env")) or {}
        self.calls.append((argv, kwargs))
        response = self.callback(environment)
        if response is not None:
            return response
        if "RUNLAYER_INSTALLER_PATH" in environment:
            return result(stdout=authenticode_payload())
        if "RUNLAYER_MSI_UPGRADE_CODE" in environment:
            return result(stdout='"{12345678-90AB-CDEF-1234-567890ABCDEF}"')
        return result()


def _installer(
    case: UpdateCase,
    runner: RecordingRunner,
    *,
    now: Callable[[], datetime] = _fixed_now,
) -> WindowsUpdateHandoffInstaller:
    return WindowsUpdateHandoffInstaller(
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        task_name=_TASK_NAME,
        staged_filename="aiwatch-update.msi",
        runner=runner,
        powershell_executable="powershell.exe",
        msiexec_executable="msiexec.exe",
        process_name="aiwatch",
        product_install_directory=r"C:\Program Files\Runlayer\AIWatch",
        quiesce_task_names=("AIWatchScan", "AIWatchHooks"),
        quiesce_service_names=("RunlayerAIWatch",),
        staging_directory=case.staging_directory,
        now=now,
    )


def _install(
    case: UpdateCase,
    runner: RecordingRunner,
    *,
    now: Callable[[], datetime] = _fixed_now,
) -> InstallDisposition:
    return _installer(case, runner, now=now).verify_and_install(
        case.source_path,
        artifact=case.artifact,
        from_version="1.0.0",
        to_version="2.0.0",
    )


def _environment(call: tuple[list[str], dict[str, object]]) -> dict[str, str]:
    return cast(dict[str, str], call[1]["env"])


def test_outcome_marker_lives_in_locked_staging_directory(
    update_case: UpdateCase,
) -> None:
    installer = _installer(update_case, HandoffRunner())

    assert installer.outcome_marker_path == (
        update_case.staging_directory / "aiwatch-update-outcome.json"
    )


@pytest.mark.parametrize(
    ("failure", "error_type", "message"),
    (
        ("hash", InstallerVerificationError, "SHA-256"),
        ("signature", InstallerVerificationError, "Authenticode"),
        ("installed_product", InstallerExecutionError, "exactly one"),
    ),
)
def test_invalid_staged_msi_is_removed_and_never_scheduled(
    update_case: UpdateCase,
    failure: str,
    error_type: type[Exception],
    message: str,
) -> None:
    def fail(environment: dict[str, str]) -> subprocess.CompletedProcess[str] | None:
        if failure == "hash" and environment.get("RUNLAYER_UPDATE_LOCK_PATH") == str(
            update_case.staging_directory.resolve()
        ):
            update_case.source_path.write_bytes(b"swapped-after-validation")
        if failure == "signature" and "RUNLAYER_INSTALLER_PATH" in environment:
            return result(stdout=authenticode_payload(status="NotSigned"))
        if (
            failure == "installed_product"
            and "RUNLAYER_MSI_UPGRADE_CODE" in environment
        ):
            return result(stdout="[]")
        return None

    runner = HandoffRunner(fail)

    with pytest.raises(error_type, match=message):
        _install(update_case, runner)

    environments = [_environment(call) for call in runner.calls]
    assert not update_case.staged_path.exists()
    assert not any("RUNLAYER_UPDATE_TASK_NAME" in env for env in environments)
    assert any("RUNLAYER_INSTALLER_PATH" in env for env in environments) is (
        failure != "hash"
    )


def test_secure_stage_verify_quiesce_and_schedule_order(
    update_case: UpdateCase,
) -> None:
    events: list[tuple[str, bool]] = []

    def observe(environment: dict[str, str]) -> None:
        lock_path = environment.get("RUNLAYER_UPDATE_LOCK_PATH")
        lock_file = environment.get("RUNLAYER_UPDATE_LOCK_FILE")
        if lock_path:
            events.append((Path(lock_path).name, update_case.staged_path.exists()))
        elif lock_file:
            event = "msi_acl" if lock_file.endswith(".msi") else "log_acl"
            events.append((event, update_case.staged_path.exists()))
        elif "RUNLAYER_INSTALLER_PATH" in environment:
            events.append(("verify", update_case.staged_path.exists()))
        elif "RUNLAYER_UPDATE_TASK_NAME" in environment:
            events.append(("schedule", update_case.staged_path.exists()))

    runner = HandoffRunner(observe)
    disposition = _install(update_case, runner)

    assert disposition is InstallDisposition.SCHEDULED
    assert update_case.staged_path.read_bytes() == b"installer"
    assert events == [
        ("UpdateStaging", False),
        ("msi_acl", True),
        ("verify", True),
        ("log_acl", True),
        ("schedule", True),
    ]

    staging_acl, msi_acl, verifier, _, log_acl, task = runner.calls
    assert _environment(staging_acl)["RUNLAYER_UPDATE_ALLOW_CURRENT_OWNER"] == "1"
    assert _environment(staging_acl)["RUNLAYER_UPDATE_LOCK_PATH"] == str(
        update_case.staging_directory.resolve()
    )
    assert _environment(msi_acl)["RUNLAYER_UPDATE_LOCK_FILE"] == str(
        update_case.staged_path.resolve()
    )
    assert _environment(verifier)["RUNLAYER_INSTALLER_PATH"] == str(
        update_case.staged_path.resolve()
    )
    assert _environment(log_acl)["RUNLAYER_UPDATE_LOCK_FILE"] == str(
        update_case.staged_path.with_suffix(".log").resolve()
    )
    assert "D:P(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)" in staging_acl[0][-1]
    assert (
        "GetOwner([System.Security.Principal.SecurityIdentifier])" in staging_acl[0][-1]
    )
    assert "$directorySecurity.SetOwner($trustedOwner)" in staging_acl[0][-1]
    assert "D:P(A;;FA;;;SY)(A;;FA;;;BA)" in msi_acl[0][-1]
    assert "D:P(A;;FA;;;SY)(A;;FA;;;BA)" in log_acl[0][-1]

    task_script = task[0][-1]
    task_environment = _environment(task)
    for token in (
        "ScheduledTasks\\New-ScheduledTaskAction",
        "ScheduledTasks\\New-ScheduledTaskTrigger",
        "-UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest",
        "DeleteExpiredTaskAfter",
        "EndBoundary",
        "'D:P(A;;GA;;;SY)(A;;GA;;;BA)', 0",
    ):
        assert token in task_script
    assert task_environment["RUNLAYER_UPDATE_TASK_NAME"] == _TASK_NAME
    assert task_environment["RUNLAYER_UPDATE_RUN_AT"] == "2026-07-20T10:31:00"
    assert task_environment["RUNLAYER_UPDATE_ACTION_EXECUTABLE"] == "powershell.exe"

    action_arguments = task_environment["RUNLAYER_UPDATE_ACTION_ARGUMENTS"]
    handoff_script = base64.b64decode(action_arguments.rsplit(" ", 1)[1]).decode(
        "utf-16-le"
    )
    staged_path = update_case.staged_path.resolve()
    msiexec_arguments = subprocess.list2cmdline(
        [
            "/i",
            str(staged_path),
            "/qn",
            "/norestart",
            "REBOOT=ReallySuppress",
            "REINSTALLMODE=amus",
            "/l*v",
            str(staged_path.with_suffix(".log")),
        ]
    )
    for value in (
        "msiexec.exe",
        msiexec_arguments,
        "aiwatch",
        r"C:\Program Files\Runlayer\AIWatch",
        "AIWatchScan",
        "AIWatchHooks",
        "RunlayerAIWatch",
        "2.0.0",
    ):
        assert base64.b64encode(value.encode()).decode() in handoff_script
    service_assembly_load = "Add-Type -AssemblyName System.ServiceProcess"
    first_service_controller_use = "[System.ServiceProcess.ServiceController]::new("
    assert service_assembly_load in handoff_script
    assert handoff_script.index(service_assembly_load) < handoff_script.index(
        first_service_controller_use
    )
    assert (
        handoff_script.index("$task.Enabled = $false")
        < handoff_script.index("$service.Stop()")
        < handoff_script.index("$busyCount = Get-RunlayerBusyProcessCount")
        < handoff_script.index("$installerProcess = ")
        < handoff_script.index("$versionProcess = ")
    )
    assert (
        handoff_script.count("catch [System.InvalidOperationException] { continue }")
        == 2
    )
    for token in (
        "$task.Stop(0)",
        "$exitCode = 1618",
        "[System.StringComparison]::OrdinalIgnoreCase",
        "$versionInfo.Arguments = '--version'",
        "$versionOutput -ne $expectedVersionOutput",
        "post-install verification failed",
        "post-install verification passed",
        "if ([bool]$entry.Value) { $task.Enabled = $true }",
        "else { $task.Enabled = $false }",
        "$service.WaitForStatus(",
        "$service.Start()",
    ):
        assert token in handoff_script
    assert str(staged_path) not in task_script
    assert str(staged_path) not in handoff_script
    assert "ORG_API_KEY" not in task_environment
    assert "ORG_API_KEY" not in handoff_script
    assert all(call[1]["shell"] is False for call in runner.calls)


@pytest.mark.parametrize(
    ("filename", "expected"),
    (("aiwatch-update.msi", b"installer"), ("aiwatch-update.log", b"")),
)
def test_staging_replaces_precreated_file_links_without_following_them(
    update_case: UpdateCase,
    tmp_path: Path,
    filename: str,
    expected: bytes,
) -> None:
    update_case.staging_directory.mkdir(parents=True)
    outside_path = tmp_path / f"outside-{filename}"
    outside_path.write_bytes(b"do-not-overwrite")
    linked_path = update_case.staging_directory / filename
    linked_path.symlink_to(outside_path)

    _install(update_case, HandoffRunner())

    assert outside_path.read_bytes() == b"do-not-overwrite"
    assert not linked_path.is_symlink()
    assert linked_path.read_bytes() == expected


def test_staging_rejects_redirected_update_directory(
    update_case: UpdateCase,
    tmp_path: Path,
) -> None:
    outside_directory = tmp_path / "redirect-target"
    outside_directory.mkdir()
    update_case.staging_directory.parent.mkdir(parents=True)
    update_case.staging_directory.symlink_to(
        outside_directory,
        target_is_directory=True,
    )
    runner = HandoffRunner()

    with pytest.raises(InstallerExecutionError, match="redirected"):
        _install(update_case, runner)

    assert not (outside_directory / "aiwatch-update.msi").exists()
    assert runner.calls == []


def test_staging_rejects_preexisting_untrusted_owner_before_copy(
    update_case: UpdateCase,
) -> None:
    update_case.staging_directory.mkdir(parents=True)
    runner = RecordingRunner(
        result(returncode=1, stderr="staging directory has an untrusted owner"),
    )

    with pytest.raises(InstallerExecutionError, match="untrusted owner"):
        _install(update_case, runner)

    assert not update_case.staged_path.exists()
    assert _environment(runner.calls[0])["RUNLAYER_UPDATE_ALLOW_CURRENT_OWNER"] == "0"
    assert len(runner.calls) == 1


@pytest.mark.parametrize(
    ("package", "expected"),
    (
        (
            "ai-watch",
            (
                "AIWatchUpdateHandoff",
                "aiwatch-update.msi",
                "aiwatch",
                r"C:\Program Files\Runlayer\AIWatch",
                ("AIWatchScan", "AIWatchHooks"),
                ("RunlayerAIWatch",),
            ),
        ),
        (
            "cli",
            (
                "CLIUpdateHandoff",
                "runlayer-update.msi",
                "runlayer",
                r"C:\Program Files\Runlayer\CLI",
                ("CLISchedule",),
                (),
            ),
        ),
    ),
)
def test_native_installer_wires_product_specific_handoff(
    monkeypatch: pytest.MonkeyPatch,
    package: str,
    expected: tuple[str, str, str, str, tuple[str, ...], tuple[str, ...]],
) -> None:
    captured: dict[str, object] = {}

    class RecordingHandoff:
        def __init__(self, **kwargs: object) -> None:
            captured.update(kwargs)

    monkeypatch.setattr(
        platform_installers,
        "WindowsUpdateHandoffInstaller",
        RecordingHandoff,
    )
    installer = NativePlatformInstaller(
        package, target=InstallTarget("windows", "x64", "msi")
    )

    assert (
        captured["task_name"],
        captured["staged_filename"],
        captured["process_name"],
        captured["product_install_directory"],
        captured["quiesce_task_names"],
        captured["quiesce_service_names"],
    ) == expected
    marker_filename = f"{Path(expected[1]).stem}-outcome.json"
    assert installer.outcome_marker_path == (
        Path(r"C:\Program Files\Runlayer\UpdateStaging") / marker_filename
    )
