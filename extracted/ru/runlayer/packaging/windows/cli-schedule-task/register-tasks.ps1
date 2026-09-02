# Register the full Runlayer CLI's managed skill-sync scheduler. The task runs
# as SYSTEM, then `schedule --all-users` drops to each logged-on user's token
# before the per-user scheduler writes that user's home.

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "RunlayerTaskCommon.ps1")

$script:ExePath = Join-Path (Split-Path -Parent $PSScriptRoot) "runlayer.exe"
$script:TaskPath = "\Runlayer\"
$script:ScheduleTaskName = "CLISchedule"
$script:RunlayerLogComponent = "cli-schedule-register"

function Register-CliScheduleTask {
    $action = New-ScheduledTaskAction -Execute $script:ExePath -Argument "schedule --all-users"
    $triggers = @(
        (New-ScheduledTaskTrigger -AtLogOn),
        (New-RunlayerRepeatingTrigger -IntervalMinutes 60)
    )
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    $settings = New-RunlayerTaskSettings
    Register-ScheduledTask -TaskName $script:ScheduleTaskName -TaskPath $script:TaskPath `
        -Action $action -Trigger $triggers -Principal $principal -Settings $settings -Force | Out-Null
    Set-RunlayerTaskSecurity -TaskName $script:ScheduleTaskName
}

if ($MyInvocation.InvocationName -ne '.') {
    $Identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    if (-not $Identity.IsSystem) {
        Write-Warning "Runlayer CLI schedule task registration must run as SYSTEM."
        exit 2
    }
    if (-not (Test-Path $script:ExePath)) {
        Write-Warning "runlayer.exe not found at $script:ExePath."
        exit 2
    }

    try {
        Initialize-RunlayerTaskFolder
        Register-CliScheduleTask
        Write-RunlayerLog "registered CLISchedule"
        exit 0
    } catch {
        Write-RunlayerLog "registration failed - $($_.Exception.Message)"
        Write-Warning $_
        exit 1
    }
}
