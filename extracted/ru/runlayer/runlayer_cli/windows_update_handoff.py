"""Detached Windows MSI self-update handoff."""

from __future__ import annotations

import base64
from collections.abc import Callable
from datetime import datetime, timedelta
from hashlib import sha256
import os
from pathlib import Path, PureWindowsPath
import shutil
import subprocess

from runlayer_cli.installer_common import (
    CommandRunner,
    InstallerExecutionError,
    InstallerVerificationError,
    default_command_runner,
    run_checked,
    validate_artifact,
    windows_installer_environment,
)
from runlayer_cli.updater import Artifact, InstallDisposition
from runlayer_cli.windows_installer_verifier import (
    WindowsMsiVerifier,
    WindowsSignerIdentity,
    default_windows_executable,
)


_DEFAULT_STAGING_DIRECTORY = Path(r"C:\Program Files\Runlayer\UpdateStaging")
_LOCK_STAGING_DIRECTORY_ACL_SCRIPT = (
    "$ErrorActionPreference = 'Stop'; "
    "$systemSid = 'S-1-5-18'; $adminsSid = 'S-1-5-32-544'; "
    "$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent(); "
    "$currentSid = $identity.User.Value; "
    "$principal = [System.Security.Principal.WindowsPrincipal]::new($identity); "
    "$isSystem = $currentSid -eq $systemSid; "
    "if (-not $isSystem -and -not $principal.IsInRole("
    "[System.Security.Principal.WindowsBuiltInRole]::Administrator)) { "
    "throw 'Windows update staging requires SYSTEM or an administrator' }; "
    "$trustedOwnerSid = if ($isSystem) { $systemSid } else { $adminsSid }; "
    "$trustedOwner = [System.Security.Principal.SecurityIdentifier]::new("
    "$trustedOwnerSid); "
    "$allowedOwners = @($systemSid, $adminsSid); "
    "if ($env:RUNLAYER_UPDATE_ALLOW_CURRENT_OWNER -eq '1') { "
    "$allowedOwners += $currentSid }; "
    "$directory = [System.IO.DirectoryInfo]::new("
    "$env:RUNLAYER_UPDATE_LOCK_PATH); "
    "$ownerSecurity = $directory.GetAccessControl("
    "[System.Security.AccessControl.AccessControlSections]::Owner); "
    "$ownerSid = $ownerSecurity.GetOwner("
    "[System.Security.Principal.SecurityIdentifier]).Value; "
    "if ($allowedOwners -notcontains $ownerSid) { "
    "throw 'Windows update staging directory has an untrusted owner' }; "
    "$directorySecurity = "
    "[System.Security.AccessControl.DirectorySecurity]::new(); "
    "$directorySecurity.SetSecurityDescriptorSddlForm("
    "'D:P(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)'); "
    "$directorySecurity.SetOwner($trustedOwner); "
    "$directory.SetAccessControl($directorySecurity)"
)
_LOCK_STAGED_FILE_ACL_SCRIPT = (
    "$ErrorActionPreference = 'Stop'; "
    "$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent(); "
    "$trustedOwnerSid = if ($identity.User.Value -eq 'S-1-5-18') { "
    "'S-1-5-18' } else { 'S-1-5-32-544' }; "
    "$trustedOwner = [System.Security.Principal.SecurityIdentifier]::new("
    "$trustedOwnerSid); "
    "$fileSecurity = [System.Security.AccessControl.FileSecurity]::new(); "
    "$fileSecurity.SetSecurityDescriptorSddlForm("
    "'D:P(A;;FA;;;SY)(A;;FA;;;BA)'); "
    "$fileSecurity.SetOwner($trustedOwner); "
    "$file = [System.IO.FileInfo]::new($env:RUNLAYER_UPDATE_LOCK_FILE); "
    "$file.SetAccessControl($fileSecurity)"
)
_REGISTER_HANDOFF_TASK_SCRIPT = (
    "$ErrorActionPreference = 'Stop'; "
    "$PSModuleAutoLoadingPreference = 'None'; "
    "$modulePath = [System.IO.Path]::Combine($PSHOME, 'Modules', "
    "'ScheduledTasks', 'ScheduledTasks.psd1'); "
    "Microsoft.PowerShell.Core\\Import-Module -Name $modulePath "
    "-Force -ErrorAction Stop; "
    "$culture = [System.Globalization.CultureInfo]::InvariantCulture; "
    "$runAt = [System.DateTime]::ParseExact("
    "$env:RUNLAYER_UPDATE_RUN_AT, 's', $culture, "
    "[System.Globalization.DateTimeStyles]::AssumeLocal); "
    "$action = ScheduledTasks\\New-ScheduledTaskAction "
    "-Execute $env:RUNLAYER_UPDATE_ACTION_EXECUTABLE "
    "-Argument $env:RUNLAYER_UPDATE_ACTION_ARGUMENTS; "
    "$trigger = ScheduledTasks\\New-ScheduledTaskTrigger -Once -At $runAt; "
    "$trigger.EndBoundary = $runAt.AddMinutes(10).ToString('s', $culture); "
    "$principal = ScheduledTasks\\New-ScheduledTaskPrincipal "
    "-UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest; "
    "$settings = ScheduledTasks\\New-ScheduledTaskSettingsSet "
    "-Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries "
    "-StartWhenAvailable -MultipleInstances IgnoreNew "
    "-ExecutionTimeLimit ([System.TimeSpan]::FromHours(1)) "
    "-DeleteExpiredTaskAfter ([System.TimeSpan]::FromMinutes(1)) "
    "-DisallowDemandStart; "
    "$serviceType = [type]::GetTypeFromProgID('Schedule.Service', $true); "
    "$service = [System.Activator]::CreateInstance($serviceType); "
    "$service.Connect(); $root = $service.GetFolder('\\'); "
    "$folderSddl = 'D:P(A;;GA;;;SY)(A;;GA;;;BA)(A;;GRGX;;;AU)'; "
    "try { $folder = $root.GetFolder('Runlayer') } "
    "catch { $folder = $root.CreateFolder('Runlayer', $folderSddl) }; "
    "$folder.SetSecurityDescriptor($folderSddl, 0); "
    "$null = ScheduledTasks\\Register-ScheduledTask "
    "-TaskName $env:RUNLAYER_UPDATE_TASK_NAME -TaskPath '\\Runlayer\\' "
    "-Action $action -Trigger $trigger -Principal $principal "
    "-Settings $settings -Force; "
    "$task = $folder.GetTask($env:RUNLAYER_UPDATE_TASK_NAME); "
    "$task.SetSecurityDescriptor("
    "'D:P(A;;GA;;;SY)(A;;GA;;;BA)', 0)"
)


def _encoded_utf8(value: str) -> str:
    return base64.b64encode(value.encode()).decode("ascii")


def _build_handoff_action_script(
    *,
    msiexec_argv: list[str],
    log_path: Path,
    process_name: str,
    product_install_directory: str,
    to_version: str,
    quiesce_task_names: tuple[str, ...],
    quiesce_service_names: tuple[str, ...],
    wait_seconds: int,
) -> str:
    decode = "Decode-RunlayerValue"
    encoded_tasks = ", ".join(
        f"({decode} '{_encoded_utf8(task_name)}')" for task_name in quiesce_task_names
    )
    task_array = f"@({encoded_tasks})" if encoded_tasks else "@()"
    encoded_services = ", ".join(
        f"({decode} '{_encoded_utf8(service_name)}')"
        for service_name in quiesce_service_names
    )
    service_array = f"@({encoded_services})" if encoded_services else "@()"
    values = {
        "msiexec": _encoded_utf8(msiexec_argv[0]),
        "arguments": _encoded_utf8(subprocess.list2cmdline(msiexec_argv[1:])),
        "log": _encoded_utf8(str(log_path)),
        "process": _encoded_utf8(process_name),
        "product_directory": _encoded_utf8(product_install_directory),
        "target_version": _encoded_utf8(to_version),
    }
    lines = [
        "$ErrorActionPreference = 'Stop'",
        "Add-Type -AssemblyName System.ServiceProcess",
        "function Decode-RunlayerValue {",
        "    param([string]$Value)",
        "    return [System.Text.Encoding]::UTF8.GetString(",
        "        [System.Convert]::FromBase64String($Value))",
        "}",
        f"$msiexecPath = {decode} '{values['msiexec']}'",
        f"$msiexecArguments = {decode} '{values['arguments']}'",
        f"$logPath = {decode} '{values['log']}'",
        f"$processName = {decode} '{values['process']}'",
        f"$productRoot = ({decode} '{values['product_directory']}').TrimEnd(",
        "    [char]'\\') + '\\'",
        f"$targetVersion = {decode} '{values['target_version']}'",
        f"$quiesceTaskNames = {task_array}",
        f"$quiesceServiceNames = {service_array}",
        "function Write-HandoffLog {",
        "    param([string]$Message)",
        "    try {",
        "        $timestamp = [System.DateTime]::UtcNow.ToString('o')",
        "        $line = $timestamp + ' [handoff] ' + $Message + ",
        "            [System.Environment]::NewLine",
        "        [System.IO.File]::AppendAllText(",
        "            $logPath, $line, [System.Text.Encoding]::UTF8)",
        "    } catch { }",
        "}",
        "function Get-RunlayerBusyProcessCount {",
        "    $count = 0",
        "    foreach ($process in ",
        "            [System.Diagnostics.Process]::GetProcessesByName($processName)) {",
        "        try {",
        "            try { $processPath = $process.MainModule.FileName }",
        "            catch { $processPath = $null }",
        "            if ([string]::IsNullOrEmpty($processPath) -or ",
        "                    $processPath.StartsWith(",
        "                        $productRoot, ",
        "                        [System.StringComparison]::OrdinalIgnoreCase)) {",
        "                $count += 1",
        "            }",
        "        } finally {",
        "            $process.Dispose()",
        "        }",
        "    }",
        "    return $count",
        "}",
        "$taskService = $null",
        "$taskStates = @{}",
        "$serviceStates = @{}",
        "$exitCode = 1",
        "try {",
        "    if ($quiesceTaskNames.Count -gt 0) {",
        "        $serviceType = [type]::GetTypeFromProgID(",
        "            'Schedule.Service', $true)",
        "        $taskService = [System.Activator]::CreateInstance($serviceType)",
        "        $taskService.Connect()",
        "        $taskFolder = $taskService.GetFolder('\\Runlayer')",
        "        foreach ($task in @($taskFolder.GetTasks(1))) {",
        "            if ($quiesceTaskNames -contains [string]$task.Name) {",
        "                $taskStates[[string]$task.Name] = [bool]$task.Enabled",
        "                $task.Enabled = $false",
        "                try { $task.Stop(0) } catch { }",
        "            }",
        "        }",
        "    }",
        # Persistent package services are themselves counted below. Stop them
        # before waiting; MSI ServiceControl cannot run until msiexec starts.
        "    foreach ($serviceName in $quiesceServiceNames) {",
        "        $service = [System.ServiceProcess.ServiceController]::new(",
        "            [string]$serviceName)",
        "        try {",
        "            try { $serviceStatus = $service.Status }",
        "            catch [System.InvalidOperationException] { continue }",
        "            $stopped = ",
        "                [System.ServiceProcess.ServiceControllerStatus]::Stopped",
        "            $stopPending = ",
        "                [System.ServiceProcess.ServiceControllerStatus]::StopPending",
        "            $wasRunning = $serviceStatus -ne $stopped",
        "            $serviceStates[[string]$serviceName] = $wasRunning",
        "            if ($wasRunning) {",
        "                if ($serviceStatus -ne $stopPending) { $service.Stop() }",
        "                $service.WaitForStatus(",
        "                    $stopped, [System.TimeSpan]::FromSeconds(30))",
        "            }",
        "        } finally {",
        "            $service.Dispose()",
        "        }",
        "    }",
        f"    $deadline = [System.DateTime]::UtcNow.AddSeconds({wait_seconds})",
        "    $busyCount = Get-RunlayerBusyProcessCount",
        "    while ($busyCount -gt 0 -and ",
        "            [System.DateTime]::UtcNow -lt $deadline) {",
        "        [System.Threading.Thread]::Sleep(1000)",
        "        $busyCount = Get-RunlayerBusyProcessCount",
        "    }",
        "    if ($busyCount -gt 0) {",
        "        Write-HandoffLog 'product processes remained busy; install deferred'",
        "        $exitCode = 1618",
        "    } else {",
        "        $startInfo = [System.Diagnostics.ProcessStartInfo]::new()",
        "        $startInfo.FileName = $msiexecPath",
        "        $startInfo.Arguments = $msiexecArguments",
        "        $startInfo.UseShellExecute = $false",
        "        $startInfo.CreateNoWindow = $true",
        "        $installerProcess = ",
        "            [System.Diagnostics.Process]::Start($startInfo)",
        "        if ($null -eq $installerProcess) {",
        "            throw 'Could not start Windows Installer'",
        "        }",
        "        try {",
        "            $installerProcess.WaitForExit()",
        "            $exitCode = [int]$installerProcess.ExitCode",
        "        } finally {",
        "            $installerProcess.Dispose()",
        "        }",
        "        if ($exitCode -eq 0) {",
        "            $versionInfo = [System.Diagnostics.ProcessStartInfo]::new()",
        "            $versionInfo.FileName = $productRoot + $processName + '.exe'",
        "            $versionInfo.Arguments = '--version'",
        "            $versionInfo.UseShellExecute = $false",
        "            $versionInfo.CreateNoWindow = $true",
        "            $versionInfo.RedirectStandardOutput = $true",
        "            $versionOutput = ''",
        "            $versionExitCode = 1",
        "            $versionProcess = $null",
        "            try {",
        "                $versionProcess = ",
        "                    [System.Diagnostics.Process]::Start($versionInfo)",
        "                if ($null -eq $versionProcess) {",
        "                    throw 'Could not start installed binary verification'",
        "                }",
        "                $versionOutput = ",
        "                    $versionProcess.StandardOutput.ReadToEnd().Trim()",
        "                $versionProcess.WaitForExit()",
        "                $versionExitCode = [int]$versionProcess.ExitCode",
        "            } catch {",
        "                $versionOutput = $_.Exception.Message",
        "            } finally {",
        "                if ($null -ne $versionProcess) {",
        "                    $versionProcess.Dispose()",
        "                }",
        "            }",
        "            $expectedVersionOutput = ",
        "                $processName + ' version ' + $targetVersion",
        "            if ($versionExitCode -ne 0 -or ",
        "                    $versionOutput -ne $expectedVersionOutput) {",
        "                Write-HandoffLog (",
        "                    'post-install verification failed: exit=' + ",
        "                    $versionExitCode + '; output=' + $versionOutput)",
        "                $exitCode = 1",
        "            } else {",
        "                Write-HandoffLog (",
        "                    'post-install verification passed: ' + $versionOutput)",
        "            }",
        "        }",
        "    }",
        "} catch {",
        "    Write-HandoffLog ('handoff failed: ' + $_.Exception.Message)",
        "    $exitCode = 1",
        "} finally {",
        "    foreach ($entry in $serviceStates.GetEnumerator()) {",
        "        if (-not [bool]$entry.Value) { continue }",
        "        $service = [System.ServiceProcess.ServiceController]::new(",
        "            [string]$entry.Key)",
        "        try {",
        "            try { $serviceStatus = $service.Status }",
        "            catch [System.InvalidOperationException] { continue }",
        "            $stopped = ",
        "                [System.ServiceProcess.ServiceControllerStatus]::Stopped",
        "            $running = ",
        "                [System.ServiceProcess.ServiceControllerStatus]::Running",
        "            if ($serviceStatus -eq $stopped) {",
        "                $service.Start()",
        "                $service.WaitForStatus(",
        "                    $running, [System.TimeSpan]::FromSeconds(30))",
        "            }",
        "        } catch {",
        "            Write-HandoffLog ('service restore failed: ' + ",
        "                $_.Exception.Message)",
        "        } finally {",
        "            $service.Dispose()",
        "        }",
        "    }",
        "    if ($null -ne $taskService -and $taskStates.Count -gt 0) {",
        "        try { $restoreFolder = $taskService.GetFolder('\\Runlayer') }",
        "        catch { $restoreFolder = $null }",
        "        if ($null -ne $restoreFolder) {",
        "            foreach ($entry in $taskStates.GetEnumerator()) {",
        "                try {",
        "                    $task = $restoreFolder.GetTask([string]$entry.Key)",
        "                    if ([bool]$entry.Value) { $task.Enabled = $true }",
        "                    else { $task.Enabled = $false }",
        "                } catch { }",
        "            }",
        "        }",
        "    }",
        "}",
        "exit $exitCode",
    ]
    return "\n".join(lines)


def windows_update_outcome_marker_path(
    staged_filename: str,
    *,
    staging_directory: Path | None = None,
) -> Path:
    directory = staging_directory or _DEFAULT_STAGING_DIRECTORY
    marker_filename = f"{PureWindowsPath(staged_filename).stem}-outcome.json"
    return directory / marker_filename


def _encoded_powershell_command(script: str) -> str:
    return base64.b64encode(script.encode("utf-16-le")).decode("ascii")


def _resolve_unredirected(path: Path, *, error_message: str) -> Path:
    try:
        resolved_path = path.resolve(strict=True)
    except OSError as exc:
        raise InstallerExecutionError(error_message) from exc
    if resolved_path != path:
        raise InstallerExecutionError(error_message)
    return resolved_path


class WindowsUpdateHandoffInstaller:
    """Verify an MSI before handing replacement to a detached SYSTEM task."""

    def __init__(
        self,
        *,
        upgrade_code: str,
        product_name: str,
        task_name: str,
        staged_filename: str,
        signer_identity: WindowsSignerIdentity | None = None,
        runner: CommandRunner = default_command_runner,
        powershell_executable: str | None = None,
        msiexec_executable: str | None = None,
        process_name: str,
        product_install_directory: str,
        quiesce_task_names: tuple[str, ...],
        quiesce_service_names: tuple[str, ...] = (),
        staging_directory: Path | None = None,
        now: Callable[[], datetime] = datetime.now,
        process_wait_seconds: int = 300,
    ) -> None:
        staged_windows_path = PureWindowsPath(staged_filename)
        if (
            staged_windows_path.name != staged_filename
            or staged_windows_path.suffix.casefold() != ".msi"
        ):
            raise ValueError(
                "Windows update staged MSI filename must be a basename ending in .msi"
            )
        task_windows_path = PureWindowsPath(task_name)
        if (
            not task_name.strip()
            or task_windows_path.name != task_name
            or task_name in {".", ".."}
        ):
            raise ValueError("Windows update handoff task name must be a leaf name")
        if (
            not process_name.strip()
            or PureWindowsPath(process_name).name != process_name
        ):
            raise ValueError("Windows update process name must be a leaf name")
        product_directory = PureWindowsPath(product_install_directory)
        if not product_directory.is_absolute() or ".." in product_directory.parts:
            raise ValueError("Windows update product directory must be absolute")
        for quiesce_task_name in quiesce_task_names:
            quiesce_path = PureWindowsPath(quiesce_task_name)
            if (
                not quiesce_task_name.strip()
                or quiesce_path.name != quiesce_task_name
                or quiesce_task_name in {".", ".."}
            ):
                raise ValueError("Windows update quiesce task name must be a leaf name")
        for service_name in quiesce_service_names:
            service_path = PureWindowsPath(service_name)
            if (
                not service_name.strip()
                or service_path.name != service_name
                or service_name in {".", ".."}
            ):
                raise ValueError("Windows update service name must be a leaf name")
        if not 1 <= process_wait_seconds <= 3600:
            raise ValueError("Windows update process wait must be between 1 and 3600s")
        self._runner = runner
        self._verifier = WindowsMsiVerifier(
            upgrade_code=upgrade_code,
            product_name=product_name,
            signer_identity=signer_identity,
            runner=runner,
            powershell_executable=powershell_executable,
        )
        self._task_name = task_name
        self._staged_filename = staged_filename
        self._powershell = self._verifier.powershell_command("")[0]
        self._msiexec = msiexec_executable or default_windows_executable("msiexec.exe")
        self._process_name = process_name
        self._product_install_directory = str(product_directory)
        self._quiesce_task_names = quiesce_task_names
        self._quiesce_service_names = quiesce_service_names
        self._process_wait_seconds = process_wait_seconds
        self._staging_directory = staging_directory or _DEFAULT_STAGING_DIRECTORY
        self._now = now

    @property
    def outcome_marker_path(self) -> Path:
        return windows_update_outcome_marker_path(
            self._staged_filename,
            staging_directory=self._staging_directory,
        )

    def _lock_directory(
        self,
        path: Path,
        *,
        allow_current_owner: bool,
    ) -> None:
        run_checked(
            self._runner,
            self._verifier.powershell_command(_LOCK_STAGING_DIRECTORY_ACL_SCRIPT),
            verification=False,
            env=windows_installer_environment(
                self._verifier.system_directory,
                RUNLAYER_UPDATE_ALLOW_CURRENT_OWNER=(
                    "1" if allow_current_owner else "0"
                ),
                RUNLAYER_UPDATE_LOCK_PATH=str(path),
            ),
        )

    def _lock_file(self, path: Path) -> None:
        run_checked(
            self._runner,
            self._verifier.powershell_command(_LOCK_STAGED_FILE_ACL_SCRIPT),
            verification=False,
            env=windows_installer_environment(
                self._verifier.system_directory,
                RUNLAYER_UPDATE_LOCK_FILE=str(path),
            ),
        )

    def verify_and_install(
        self,
        artifact_path: Path,
        *,
        artifact: Artifact,
        from_version: str,
        to_version: str,
    ) -> InstallDisposition:
        del from_version
        path = validate_artifact(
            artifact_path,
            artifact,
            platform="windows",
            formats=("msi",),
        )
        configured_staging_directory = self._staging_directory.absolute()
        staging_redirect_error = "Windows update staging directory was redirected"
        staging_preexisting = os.path.lexists(configured_staging_directory)
        if staging_preexisting:
            _resolve_unredirected(
                configured_staging_directory,
                error_message=staging_redirect_error,
            )
        configured_staging_directory.mkdir(parents=True, exist_ok=True)
        staging_directory = _resolve_unredirected(
            configured_staging_directory,
            error_message=staging_redirect_error,
        )
        self._lock_directory(
            staging_directory,
            allow_current_owner=not staging_preexisting,
        )
        staged_path = staging_directory / self._staged_filename
        log_path = staged_path.with_suffix(".log")
        try:
            staged_path.unlink(missing_ok=True)
            log_path.unlink(missing_ok=True)
            shutil.copyfile(path, staged_path)
        except OSError as exc:
            raise InstallerExecutionError(
                "Could not safely stage the verified Windows MSI"
            ) from exc
        staged_path = staged_path.resolve(strict=True)
        if staged_path.parent != staging_directory:
            raise InstallerExecutionError(
                "Staged Windows update file escaped the locked update directory"
            )
        try:
            self._lock_file(staged_path)
        except Exception:
            staged_path.unlink(missing_ok=True)
            raise
        digest = sha256()
        try:
            with staged_path.open("rb") as staged_file:
                for chunk in iter(lambda: staged_file.read(1024 * 1024), b""):
                    digest.update(chunk)
        except OSError as exc:
            staged_path.unlink(missing_ok=True)
            raise InstallerExecutionError(
                "Could not hash the staged Windows MSI"
            ) from exc
        if digest.hexdigest().casefold() != artifact.sha256.casefold():
            staged_path.unlink(missing_ok=True)
            raise InstallerVerificationError(
                "Staged Windows MSI SHA-256 does not match the update manifest"
            )
        try:
            self._verifier.verify(
                staged_path,
                expected_version=to_version,
                expected_arch=artifact.arch,
            )
            self._verifier.require_related_product()
        except Exception:
            staged_path.unlink(missing_ok=True)
            raise
        try:
            with log_path.open("xb"):
                pass
            log_path = log_path.resolve(strict=True)
            if log_path.parent != staging_directory:
                raise InstallerExecutionError(
                    "Staged Windows update log escaped the locked update directory"
                )
            self._lock_file(log_path)
        except Exception:
            staged_path.unlink(missing_ok=True)
            log_path.unlink(missing_ok=True)
            raise
        msiexec_argv = [
            self._msiexec,
            "/i",
            str(staged_path),
            "/qn",
            "/norestart",
            "REBOOT=ReallySuppress",
            "REINSTALLMODE=amus",
            "/l*v",
            str(log_path),
        ]
        handoff_script = _build_handoff_action_script(
            msiexec_argv=msiexec_argv,
            log_path=log_path,
            process_name=self._process_name,
            product_install_directory=self._product_install_directory,
            to_version=to_version,
            quiesce_task_names=self._quiesce_task_names,
            quiesce_service_names=self._quiesce_service_names,
            wait_seconds=self._process_wait_seconds,
        )
        action_arguments = (
            "-NoLogo -NoProfile -NonInteractive -EncodedCommand "
            + _encoded_powershell_command(handoff_script)
        )
        scheduled_at = self._now() + timedelta(minutes=1)
        if scheduled_at.second or scheduled_at.microsecond:
            scheduled_at = scheduled_at.replace(second=0, microsecond=0) + timedelta(
                minutes=1
            )
        run_checked(
            self._runner,
            self._verifier.powershell_command(_REGISTER_HANDOFF_TASK_SCRIPT),
            verification=False,
            env=windows_installer_environment(
                self._verifier.system_directory,
                RUNLAYER_UPDATE_ACTION_ARGUMENTS=action_arguments,
                RUNLAYER_UPDATE_ACTION_EXECUTABLE=self._powershell,
                RUNLAYER_UPDATE_RUN_AT=scheduled_at.strftime("%Y-%m-%dT%H:%M:%S"),
                RUNLAYER_UPDATE_TASK_NAME=self._task_name,
            ),
        )
        return InstallDisposition.SCHEDULED
