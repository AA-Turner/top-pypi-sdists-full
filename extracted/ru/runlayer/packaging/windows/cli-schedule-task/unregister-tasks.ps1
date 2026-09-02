# Remove only the full CLI's managed skill-sync scheduler. Preserve update and
# AI Watch tasks, plus the shared \Runlayer folder when any of them remain.

[CmdletBinding()]
param()

$ErrorActionPreference = "SilentlyContinue"

$script:TaskPath = "\Runlayer\"
$script:LogFile = "C:\ProgramData\Runlayer\Logs\scheduled-task.log"
$script:CliScheduleTaskNames = @("CLISchedule")

function Write-RunlayerLog {
    param([string]$Message)
    try {
        $dir = Split-Path -Parent $script:LogFile
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
        $line = "{0} [cli-schedule-unregister] {1}" -f (Get-Date -Format "o"), $Message
        Add-Content -Path $script:LogFile -Value $line -ErrorAction SilentlyContinue
    } catch {
    }
}

function Remove-CliScheduleTasksFromFolder {
    param($Folder)

    foreach ($task in $Folder.GetTasks(1)) {
        if ($script:CliScheduleTaskNames -notcontains $task.Name) {
            continue
        }
        try { $task.Stop(0) } catch { }
        try {
            $Folder.DeleteTask($task.Name, 0)
            Write-RunlayerLog "deleted $($task.Name)"
        } catch {
            Write-RunlayerLog "failed to delete $($task.Name) - $($_.Exception.Message)"
        }
    }
}

function Remove-RunlayerTaskFolderIfEmpty {
    param($Root, $Folder)

    if (@($Folder.GetTasks(1)).Count -eq 0) {
        $Root.DeleteFolder("Runlayer", 0)
        Write-RunlayerLog "removed empty \Runlayer task folder"
    } else {
        Write-RunlayerLog "preserved shared \Runlayer task folder"
    }
}

function Remove-CliScheduleTasks {
    try {
        $svc = New-Object -ComObject "Schedule.Service"
        $svc.Connect()
        $root = $svc.GetFolder("\")
        try {
            $folder = $root.GetFolder("Runlayer")
        } catch {
            return
        }

        Remove-CliScheduleTasksFromFolder -Folder $folder
        Remove-RunlayerTaskFolderIfEmpty -Root $root -Folder $folder
    } catch {
        Write-RunlayerLog "removal failed - $($_.Exception.Message)"
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    Remove-CliScheduleTasks
    exit 0
}
