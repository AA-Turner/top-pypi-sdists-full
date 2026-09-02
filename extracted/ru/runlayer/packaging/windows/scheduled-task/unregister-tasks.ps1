# AI Watch scheduled-task removal. Run as SYSTEM by the MSI deferred custom
# action on TRUE uninstall only (REMOVE=ALL) — NOT on major-upgrade, where the
# new package's register custom action re-registers the tasks.
#
# Deletes only AI Watch-owned tasks: AIWatchHooks, AIWatchScan, AIWatchUpdate,
# the pending AIWatchUpdateHandoff, and legacy per-user fan-out tasks
# (AIWatchScanManager / AIWatchScan-<SID>). The shared \Runlayer folder is
# removed only when no tasks owned by another Runlayer product remain.

[CmdletBinding()]
param()

$ErrorActionPreference = "SilentlyContinue"

$script:TaskPath = "\Runlayer\"
$script:LogFile = "C:\ProgramData\Runlayer\Logs\scheduled-task.log"
$script:AiWatchTaskNames = @(
    "AIWatchHooks",
    "AIWatchScan",
    "AIWatchUpdate",
    "AIWatchUpdateHandoff",
    "AIWatchScanManager"
)

function Write-RunlayerLog {
    param([string]$Message)
    try {
        $dir = Split-Path -Parent $script:LogFile
        if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
        $line = "{0} [unregister] {1}" -f (Get-Date -Format "o"), $Message
        Add-Content -Path $script:LogFile -Value $line -ErrorAction SilentlyContinue
    } catch {
        # Best-effort logging only.
    }
}

function Test-AiWatchOwnedTaskName {
    param([string]$TaskName)

    return $script:AiWatchTaskNames -contains $TaskName -or $TaskName -like "AIWatchScan-*"
}

function Remove-AiWatchTasksFromFolder {
    param([object]$Folder)

    # GetTasks(1) includes hidden tasks such as both update tasks. Never delete
    # an unknown/shared task merely because it lives under \Runlayer.
    foreach ($task in $Folder.GetTasks(1)) {
        if (-not (Test-AiWatchOwnedTaskName -TaskName $task.Name)) {
            continue
        }
        try {
            # A deleted registration does not necessarily stop its running
            # action. Stop first so a waiting handoff cannot reinstall after a
            # true uninstall has completed.
            try { $task.Stop(0) } catch { }
            $Folder.DeleteTask($task.Name, 0)
            Write-RunlayerLog "deleted $($task.Name)"
        } catch {
        }
    }
}

function Remove-RunlayerTaskFolderIfEmpty {
    param(
        [object]$Root,
        [object]$Folder
    )

    $remainingTasks = @($Folder.GetTasks(1))
    if ($remainingTasks.Count -ne 0) {
        Write-RunlayerLog "preserved shared \Runlayer task folder"
        return
    }
    $Root.DeleteFolder("Runlayer", 0)
    Write-RunlayerLog "removed \Runlayer task folder"
}

function Remove-RunlayerTaskFolder {
    # Delete only AI Watch-owned tasks via COM, then remove the shared folder
    # only if a second hidden-task enumeration proves it empty.
    try {
        $svc = New-Object -ComObject "Schedule.Service"
        $svc.Connect()
        $root = $svc.GetFolder("\")
        try {
            $folder = $root.GetFolder("Runlayer")
        } catch {
            # Folder already gone — nothing to do.
            return
        }
        Remove-AiWatchTasksFromFolder -Folder $folder
        Remove-RunlayerTaskFolderIfEmpty -Root $root -Folder $folder
    } catch {
        Write-RunlayerLog "removal error - $($_.Exception.Message)"
    }
}

# ---------------------------------------------------------------------------
# Main — skipped when dot-sourced (Pester loads the functions above only).
# ---------------------------------------------------------------------------
if ($MyInvocation.InvocationName -ne '.') {
    Write-RunlayerLog "starting"
    Remove-RunlayerTaskFolder
    Write-RunlayerLog "done"
    exit 0
}
