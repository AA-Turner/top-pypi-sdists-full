# Runlayer scheduled-task shared foundation. Dot-sourced by AI Watch's
# register-tasks.ps1 and the full CLI's cli-update-task/ + cli-schedule-task/
# register scripts so protected SDDL, task settings, repeating triggers,
# shared-folder init, and per-task SDDL application have one implementation.
# AI Watch's three SYSTEM task definitions also live here.
#
# All tasks run as SYSTEM: AIWatchHooks fetches settings and re-asserts hooks;
# AIWatchScan runs `aiwatch scan --all-users`, which itself drops privileges to
# each logged-on user (incl. Entra) and scans logged-off users as SYSTEM; and
# AIWatchUpdate runs the OrgApiKey-gated self-update entrypoint hourly. The
# single SYSTEM scan task replaced the per-user Interactive fan-out
# (AIWatchScanManager + AIWatchScan-<SID>), which couldn't register a task for
# Entra (S-1-12-1) accounts.
#
# Not bundled standalone with the Intune detection script: detect-install.ps1 is
# published separately and intentionally self-contained (it can't dot-source a
# file shipped only inside the MSI).
#
# Dot-source contract: each runtime script sets $script:RunlayerLogComponent
# after dot-sourcing so log lines are tagged with the calling script.

# --- AI Watch defaults (CLI registration overrides the applicable values) ---
$script:ExePath = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
$script:TaskPath = "\Runlayer\"
$script:HooksTaskName = "AIWatchHooks"
$script:ScanTaskName = "AIWatchScan"
$script:UpdateTaskName = "AIWatchUpdate"
$script:PowerShellPath = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
$script:RegisterTasksPath = Join-Path $PSScriptRoot "register-tasks.ps1"
$script:LogFile = "C:\ProgramData\Runlayer\Logs\scheduled-task.log"
$script:RunlayerLogMaxBytes = 10MB
$script:RunlayerLogRotationChecked = $false
# Overridden by each runtime script right after dot-sourcing (register/manage).
$script:RunlayerLogComponent = "task"

function Invoke-RunlayerLogRotation {
    if ($script:RunlayerLogRotationChecked) { return }
    $script:RunlayerLogRotationChecked = $true
    try {
        $log = Get-Item -LiteralPath $script:LogFile -ErrorAction Stop
        if ($log.Length -gt $script:RunlayerLogMaxBytes) {
            $backupPath = $script:LogFile + ".1"
            Move-Item -LiteralPath $script:LogFile -Destination $backupPath `
                -Force -ErrorAction Stop
        }
    } catch {
        # Another task may hold or rotate the shared file. Keep appending.
    }
}

function Write-RunlayerLog {
    param([string]$Message)
    try {
        $dir = Split-Path -Parent $script:LogFile
        if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
        Invoke-RunlayerLogRotation
        $line = "{0} [{1}] {2}" -f (Get-Date -Format "o"), $script:RunlayerLogComponent, $Message
        Add-Content -Path $script:LogFile -Value $line -ErrorAction SilentlyContinue
    } catch {
        # Best-effort logging only — never fail the caller on a log write.
    }
}

function Get-RunlayerTaskSddl {
    # Protected DACL (D:P → no inheritance from the parent folder):
    #   (A;;GA;;;SY)  Generic All  → Local System
    #   (A;;GA;;;BA)  Generic All  → Builtin Administrators
    #   (A;;GRGX;;;AU) Generic Read+Execute → Authenticated Users
    # SYSTEM + Administrators keep full control; standard (non-admin) users can
    # read/run but get "Access is denied" on modify/delete. Single source of
    # truth for the lockdown (enforced by tests/test_windows_ps1_gates.py).
    return "D:P(A;;GA;;;SY)(A;;GA;;;BA)(A;;GRGX;;;AU)"
}

function Get-RunlayerUpdateTaskSddl {
    # AIWatchUpdate runs an installer as SYSTEM. Unlike Hooks/Scan, standard
    # users must not be able to trigger it on demand, so omit Authenticated
    # Users entirely. D:P keeps the DACL protected from inherited ACEs.
    return "D:P(A;;GA;;;SY)(A;;GA;;;BA)"
}

function New-RunlayerTaskSettings {
    return New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries -StartWhenAvailable `
        -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 1)
}

function New-RunlayerUpdateTaskSettings {
    # Do not use StartWhenAvailable here. A missed hourly updater trigger must
    # wait for the next scheduled interval instead of catching up at boot/resume,
    # where it could collide with an MDM-driven install or repair.
    return New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 1)
}

function New-RunlayerRepeatingTrigger {
    param(
        [int]$IntervalMinutes,
        [int]$InitialDelayMinutes = 0
    )
    # Repeat indefinitely. Do NOT pass -RepetitionDuration ([TimeSpan]::MaxValue):
    # it serializes to "P99999999DT23H59M59S", which New-ScheduledTaskTrigger
    # accepts but Register-ScheduledTask rejects as out-of-range ("The task XML
    # contains a value which is incorrectly formatted or out of range"), aborting
    # task registration on install (ENG-3579). An omitted / empty duration is the
    # supported way to repeat forever, so build with the interval only and clear
    # the duration the cmdlet may have defaulted in.
    $startAt = (Get-Date).AddMinutes($InitialDelayMinutes)
    $trigger = New-ScheduledTaskTrigger -Once -At $startAt `
        -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes)
    if ($trigger.Repetition) {
        $trigger.Repetition.Duration = ""
    }
    return $trigger
}

function Initialize-RunlayerTaskFolder {
    # Ensure \Runlayer exists with the protected SDDL; (re)apply each run so the
    # folder lockdown self-heals if it was loosened.
    $sddl = Get-RunlayerTaskSddl
    $svc = New-Object -ComObject "Schedule.Service"
    $svc.Connect()
    $root = $svc.GetFolder("\")
    try {
        $folder = $root.GetFolder("Runlayer")
    } catch {
        $folder = $root.CreateFolder("Runlayer", $sddl)
    }
    $folder.SetSecurityDescriptor($sddl, 0)
}

function Set-RunlayerTaskSecurity {
    # Apply the protected SDDL to a single registered task (Register-ScheduledTask
    # can't set a security descriptor, so we do it over COM after registration).
    param(
        [string]$TaskName,
        [string]$Sddl = (Get-RunlayerTaskSddl)
    )
    $svc = New-Object -ComObject "Schedule.Service"
    $svc.Connect()
    $folder = $svc.GetFolder("\Runlayer")
    $task = $folder.GetTask($TaskName)
    $task.SetSecurityDescriptor($Sddl, 0)
}

function Register-AiWatchHooksTask {
    # SYSTEM settings fetch + hook re-assert — the local-task replacement for
    # the assert/Intune Remediations pair. Hourly + at-boot keeps desired
    # settings and hooks current. Registered at install by register-tasks.ps1.
    $action = New-ScheduledTaskAction -Execute $script:ExePath -Argument "setup hooks install --mdm"
    $triggers = @(
        (New-ScheduledTaskTrigger -AtStartup),
        (New-RunlayerRepeatingTrigger -IntervalMinutes 60)
    )
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    $settings = New-RunlayerTaskSettings
    Register-ScheduledTask -TaskName $script:HooksTaskName -TaskPath $script:TaskPath `
        -Action $action -Trigger $triggers -Principal $principal -Settings $settings -Force | Out-Null
    Set-RunlayerTaskSecurity -TaskName $script:HooksTaskName
}

function Register-AiWatchScanTask {
    # SYSTEM all-users scan — the single-task replacement for the per-user
    # Interactive scan fan-out (AIWatchScanManager + AIWatchScan-<SID>), which
    # could not register a task for Entra (S-1-12-1) accounts
    # (Register-ScheduledTask -LogonType Interactive => 0x80070534). Runs
    # `aiwatch scan --all-users`, which enumerates every real profile and scans
    # each AS the user: dropping privileges to the logged-on user (incl. Entra)
    # via a token launch, and falling back to a SYSTEM scan with paths pointed at
    # the profile's home when logged off. At boot, on any user's logon (catches
    # first logons after install), and every 15 min. Registered at install by
    # register-tasks.ps1.
    $action = New-ScheduledTaskAction -Execute $script:ExePath -Argument "scan --all-users"
    $triggers = @(
        (New-ScheduledTaskTrigger -AtStartup),
        (New-ScheduledTaskTrigger -AtLogOn),
        (New-RunlayerRepeatingTrigger -IntervalMinutes 15)
    )
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    $settings = New-RunlayerTaskSettings
    Register-ScheduledTask -TaskName $script:ScanTaskName -TaskPath $script:TaskPath `
        -Action $action -Trigger $triggers -Principal $principal -Settings $settings -Force | Out-Null
    Set-RunlayerTaskSecurity -TaskName $script:ScanTaskName
}

function Register-AiWatchUpdateTask {
    # SYSTEM self-update, hourly only. Deliberately no at-boot trigger: an MSI
    # install / repair must finish before a scheduled updater can stage another
    # MSI transaction. Its first tick is seven minutes past the scan task's
    # one-hour alignment so the two recurring jobs do not collide on every run.
    # The runner checks the machine-wide OrgApiKey before invoking self-update.
    $arguments = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$script:RegisterTasksPath`" -RunSelfUpdate"
    $action = New-ScheduledTaskAction -Execute $script:PowerShellPath -Argument $arguments
    $trigger = New-RunlayerRepeatingTrigger -IntervalMinutes 60 -InitialDelayMinutes 67
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    $settings = New-RunlayerUpdateTaskSettings
    Register-ScheduledTask -TaskName $script:UpdateTaskName -TaskPath $script:TaskPath `
        -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
    Set-RunlayerTaskSecurity -TaskName $script:UpdateTaskName -Sddl (Get-RunlayerUpdateTaskSddl)
}
