# Register the full Runlayer CLI's package-owned update task. The task runs as
# SYSTEM, checks hourly, and lets the hidden CLI entrypoint read the existing
# AI Watch MDM Host / OrgApiKey / AutoUpdate policy directly.

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "RunlayerTaskCommon.ps1")

$script:ExePath = Join-Path (Split-Path -Parent $PSScriptRoot) "runlayer.exe"
$script:TaskPath = "\Runlayer\"
$script:UpdateTaskName = "CLIUpdate"
$script:RunlayerLogComponent = "cli-update-register"

function Register-CliUpdateTask {
    $action = New-ScheduledTaskAction -Execute $script:ExePath -Argument "__scheduled-update"
    # No install-time kick: a first fire mid-MSI could stage a nested
    # installer. Do not start the task from install.ps1 either — CLIUpdate's
    # SDDL is SYSTEM + Administrators only, and the documented Test Device
    # parent session stays unelevated after the msiexec UAC prompt. A
    # two-minute delay lets msiexec return, then SYSTEM runs the first check
    # without needing the parent to start the task. Hourly after that.
    $trigger = New-RunlayerRepeatingTrigger -IntervalMinutes 60 -InitialDelayMinutes 2
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    $settings = New-RunlayerUpdateTaskSettings
    Register-ScheduledTask -TaskName $script:UpdateTaskName -TaskPath $script:TaskPath `
        -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
    Set-RunlayerTaskSecurity -TaskName $script:UpdateTaskName -Sddl (Get-RunlayerUpdateTaskSddl)
}

if ($MyInvocation.InvocationName -ne '.') {
    $Identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    if (-not $Identity.IsSystem) {
        Write-Warning "Runlayer CLI update task registration must run as SYSTEM."
        exit 2
    }
    if (-not (Test-Path $script:ExePath)) {
        Write-Warning "runlayer.exe not found at $script:ExePath."
        exit 2
    }

    try {
        Initialize-RunlayerTaskFolder
        Register-CliUpdateTask
        Write-RunlayerLog "registered CLIUpdate"
        exit 0
    } catch {
        Write-RunlayerLog "registration failed - $($_.Exception.Message)"
        Write-Warning $_
        exit 1
    }
}
