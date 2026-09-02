# Remove only the full CLI's recurring updater and pending detached handoff.
# Preserve AI Watch tasks and the shared \Runlayer folder when they remain.

[CmdletBinding()]
param()

$ErrorActionPreference = "SilentlyContinue"

$script:TaskPath = "\Runlayer\"
$script:LogFile = "C:\ProgramData\Runlayer\Logs\scheduled-task.log"
$script:CliTaskNames = @("CLIUpdate", "CLIUpdateHandoff")

function Write-RunlayerLog {
    param([string]$Message)
    try {
        $dir = Split-Path -Parent $script:LogFile
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
        $line = "{0} [cli-update-unregister] {1}" -f (Get-Date -Format "o"), $Message
        Add-Content -Path $script:LogFile -Value $line -ErrorAction SilentlyContinue
    } catch {
    }
}

function Remove-CliUpdateTasksFromFolder {
    param($Folder)

    foreach ($task in $Folder.GetTasks(1)) {
        if ($script:CliTaskNames -notcontains $task.Name) {
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

function Remove-CliUpdateTasks {
    try {
        $svc = New-Object -ComObject "Schedule.Service"
        $svc.Connect()
        $root = $svc.GetFolder("\")
        try {
            $folder = $root.GetFolder("Runlayer")
        } catch {
            return
        }

        Remove-CliUpdateTasksFromFolder -Folder $folder
        Remove-RunlayerTaskFolderIfEmpty -Root $root -Folder $folder
    } catch {
        Write-RunlayerLog "removal failed - $($_.Exception.Message)"
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    Remove-CliUpdateTasks
    exit 0
}
