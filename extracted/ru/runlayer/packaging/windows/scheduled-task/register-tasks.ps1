# AI Watch scheduled-task registration. Run as SYSTEM by the MSI deferred
# custom action on install / repair / major-upgrade.
#
# Replaces the Intune Remediations model: instead of the cloud driving the
# recurring scan + hook re-assert (P2 licensing, IME health, assignment
# cadence), the MSI registers device-local Scheduled Tasks at install time —
# mirroring the macOS LaunchAgent + LaunchDaemon bundle.
#
# Registers, under the \Runlayer Task Scheduler folder:
#   AIWatchHooks  SYSTEM, at-boot + hourly — runs `aiwatch setup hooks install
#                 --mdm` (writes / removes enterprise hook configs).
#   AIWatchScan   SYSTEM, at-boot + any-user logon + every 15 min — runs
#                 `aiwatch scan --all-users`, which enumerates every real
#                 profile and scans each AS the user (token-drop when logged on,
#                 incl. Entra; SYSTEM env-pointed when logged off).
#   AIWatchUpdate SYSTEM, hourly only — re-enters this script with
#                 -RunSelfUpdate, gates on the HKLM OrgApiKey, then repairs a
#                 missing executable or runs `aiwatch self-update`.
# Then removes the legacy per-user fan-out tasks (AIWatchScanManager and any
# AIWatchScan-<SID>) on upgrade, and kicks both tasks once (async) so hooks +
# scans land promptly rather than waiting for the first scheduled tick — without
# blocking the MSI. AIWatchUpdate is not kicked during install and has no
# at-boot trigger, so it cannot overlap the MSI transaction that created it.
#
# The task-scheduler foundation (SDDL, settings, triggers, folder init, per-task
# SDDL apply, the AIWatchHooks + AIWatchScan + AIWatchUpdate tasks) lives in
# RunlayerTaskCommon.ps1, dot-sourced below.
#
# Idempotent (-Force re-registration). Tasks are -Hidden and locked down with a
# protected DACL applied via the COM Schedule.Service API.
#
# Exit codes:
#   0 — tasks registered (or silent no-op on an unconfigured fleet / updater)
#   2 — misconfig (not SYSTEM, or aiwatch.exe missing)
#   1 — registration or updater invocation failed
#   -RunSelfUpdate preserves any other exit code returned by aiwatch.exe / MSI

[CmdletBinding()]
param([switch]$RunSelfUpdate)

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "RunlayerTaskCommon.ps1")
$script:RunlayerLogComponent = "register"
$script:AiWatchUpgradeCode = "{E3A2F1C0-7B4D-4E9A-8C6F-1D2E3F4A5B6C}"

function Get-AiWatchProductCode {
    $installer = New-Object -ComObject "WindowsInstaller.Installer"
    try {
        # RelatedProducts is a parameterized COM property, not a method.
        $relatedProducts = $installer.GetType().InvokeMember(
            "RelatedProducts",
            [System.Reflection.BindingFlags]::GetProperty,
            $null,
            $installer,
            $script:AiWatchUpgradeCode
        )
        foreach ($productCode in $relatedProducts) {
            if (-not [string]::IsNullOrEmpty($productCode)) {
                return [string]$productCode
            }
        }
        return $null
    } finally {
        if ([System.Runtime.InteropServices.Marshal]::IsComObject($installer)) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($installer)
        }
    }
}

function Invoke-AiWatchSelfUpdate {
    # Gate before starting aiwatch so an unconfigured / key-removed device does
    # no network, identity, staging, or installer work on the hourly tick.
    $OrgApiKey = (Get-ItemProperty -Path "HKLM:\Software\Runlayer\AIWatch" -Name "OrgApiKey" -ErrorAction SilentlyContinue).OrgApiKey
    if ([string]::IsNullOrEmpty($OrgApiKey)) {
        Write-RunlayerLog "no OrgApiKey; self-update skipped"
        return 0
    }

    if (-not (Test-Path $script:ExePath)) {
        try {
            $productCode = Get-AiWatchProductCode
        } catch {
            Write-RunlayerLog "aiwatch.exe missing; installed product lookup failed - $($_.Exception.Message)"
            return 2
        }
        if ([string]::IsNullOrEmpty($productCode)) {
            Write-RunlayerLog "aiwatch.exe missing; no installed AI Watch product found for repair"
            return 2
        }

        Write-RunlayerLog "aiwatch.exe missing; attempting MSI repair for product $productCode"
        try {
            $process = Start-Process -FilePath "msiexec.exe" `
                -ArgumentList @("/fa", $productCode, "/qn", "/norestart") `
                -NoNewWindow -Wait -PassThru
            $exitCode = [int]$process.ExitCode
            Write-RunlayerLog "MSI repair completed with exit code $exitCode"
            return $exitCode
        } catch {
            Write-RunlayerLog "MSI repair invocation failed - $($_.Exception.Message)"
            return 1
        }
    }

    try {
        $process = Start-Process -FilePath $script:ExePath -ArgumentList "self-update" `
            -NoNewWindow -Wait -PassThru
        return [int]$process.ExitCode
    } catch {
        Write-RunlayerLog "self-update invocation failed - $($_.Exception.Message)"
        return 1
    }
}

function Remove-LegacyScanTasks {
    # The single SYSTEM AIWatchScan task supersedes the legacy per-user fan-out:
    # the SYSTEM AIWatchScanManager that registered per-user Interactive
    # AIWatchScan-<SID> tasks (broken for Entra — Register-ScheduledTask
    # -LogonType Interactive can't map an S-1-12-1 SID, 0x80070534). Remove both
    # on upgrade so they don't linger and re-fan-out. The new AIWatchScan has no
    # trailing dash, so the "AIWatchScan-*" match never catches it.
    foreach ($task in (Get-ScheduledTask -TaskPath $script:TaskPath -ErrorAction SilentlyContinue)) {
        if ($task.TaskName -eq "AIWatchScanManager" -or $task.TaskName -like "AIWatchScan-*") {
            Unregister-ScheduledTask -TaskName $task.TaskName -TaskPath $script:TaskPath `
                -Confirm:$false -ErrorAction SilentlyContinue
            Write-RunlayerLog "removed legacy task $($task.TaskName)"
        }
    }
}

# ---------------------------------------------------------------------------
# Main — skipped when the script is dot-sourced (Pester loads the functions
# above without running the imperative body).
# ---------------------------------------------------------------------------
if ($MyInvocation.InvocationName -ne '.') {
    if ($RunSelfUpdate) {
        $script:RunlayerLogComponent = "update"
        exit (Invoke-AiWatchSelfUpdate)
    }

    Write-RunlayerLog "starting"

    # Unconfigured fleets (no MDM-pushed OrgApiKey) short-circuit silently so a
    # repair / reinstall on an unconfigured device is a clean no-op. Mirrors
    # runlayer_cli/mdm_config.py:_read_windows (HKLM hive).
    $OrgApiKey = (Get-ItemProperty -Path "HKLM:\Software\Runlayer\AIWatch" -Name "OrgApiKey" -ErrorAction SilentlyContinue).OrgApiKey
    if ([string]::IsNullOrEmpty($OrgApiKey)) {
        Write-RunlayerLog "no OrgApiKey; nothing to register"
        exit 0
    }

    # Deferred CA runs with Impersonate="no" ⇒ SYSTEM. Refuse anything else so a
    # mis-sequenced action can't register tasks under the wrong principal.
    $Identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    if (-not $Identity.IsSystem) {
        Write-Warning "register-tasks must run as SYSTEM (MSI deferred custom action)."
        exit 2
    }

    if (-not (Test-Path $script:ExePath)) {
        Write-RunlayerLog "aiwatch.exe not found at $script:ExePath; install the AI Watch MSI first."
        Write-Warning "aiwatch.exe not found at $script:ExePath; install the AI Watch MSI first."
        exit 2
    }

    $registerFailed = $false

    # Non-fatal: Register-ScheduledTask creates the \Runlayer path on demand, so a
    # folder-init hiccup must not block task registration below. The lockdown is
    # re-asserted on the next install/repair/upgrade.
    try {
        Initialize-RunlayerTaskFolder
    } catch {
        Write-RunlayerLog "folder init failed - $($_.Exception.Message)"
        Write-Warning $_
    }

    # Register the three SYSTEM tasks INDEPENDENTLY: one failing must not prevent
    # the others. detect-install.ps1 requires AIWatchScan + AIWatchUpdate, so
    # both mandatory tasks must always be attempted even if another task fails.
    try {
        Register-AiWatchHooksTask
    } catch {
        Write-RunlayerLog "AIWatchHooks registration failed - $($_.Exception.Message)"
        Write-Warning $_
        $registerFailed = $true
    }

    try {
        Register-AiWatchScanTask
    } catch {
        Write-RunlayerLog "AIWatchScan registration failed - $($_.Exception.Message)"
        Write-Warning $_
        $registerFailed = $true
    }

    try {
        Register-AiWatchUpdateTask
    } catch {
        Write-RunlayerLog "AIWatchUpdate registration failed - $($_.Exception.Message)"
        Write-Warning $_
        $registerFailed = $true
    }

    # Best-effort: clear the legacy per-user fan-out tasks on upgrade. Runs after
    # the new tasks are registered so a cleanup hiccup can't leave the device
    # task-less, and is non-fatal (it never sets $registerFailed).
    try {
        Remove-LegacyScanTasks
    } catch {
        Write-RunlayerLog "legacy task cleanup failed - $($_.Exception.Message)"
        Write-Warning $_
    }

    # Kick hooks + scan once, async (best-effort; a no-op for either task that
    # failed to register): hooks so enforcement configs land, and the scan so the
    # first all-users scan runs promptly (not at the next tick). AIWatchUpdate is
    # intentionally NOT kicked: it starts on its hourly trigger after this MSI
    # transaction is complete. Start-ScheduledTask returns immediately — the scan
    # fan-out runs under Task Scheduler (bounded by the task's 1h
    # ExecutionTimeLimit), NOT inline in this deferred MSI custom action. A
    # synchronous invocation here would extend install time by the full profile-
    # enumeration + per-profile scan and risk MSI-timeout warnings in enterprise
    # deploy tools.
    Start-ScheduledTask -TaskPath $script:TaskPath -TaskName $script:HooksTaskName -ErrorAction SilentlyContinue
    Start-ScheduledTask -TaskPath $script:TaskPath -TaskName $script:ScanTaskName -ErrorAction SilentlyContinue

    if ($registerFailed) {
        Write-RunlayerLog "done with errors"
        exit 1
    }

    Write-RunlayerLog "done"
    exit 0
}
