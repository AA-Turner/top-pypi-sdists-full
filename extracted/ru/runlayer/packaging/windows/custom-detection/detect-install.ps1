$ErrorActionPreference = "SilentlyContinue"
$WarningPreference = "SilentlyContinue"
$ProgressPreference = "SilentlyContinue"
$VerbosePreference = "SilentlyContinue"
$DebugPreference = "SilentlyContinue"
$InformationPreference = "SilentlyContinue"

$script:DetectLogFile = "C:\ProgramData\Runlayer\Logs\detect-install.log"

function Write-DetectLog {
    param([string]$Message)
    try {
        $dir = Split-Path -Parent $script:DetectLogFile
        if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
        $line = "{0} [detect] {1}" -f (Get-Date -Format "o"), $Message
        Add-Content -Path $script:DetectLogFile -Value $line -ErrorAction SilentlyContinue
    } catch {}
}

$script:RawVersion = "__AIWATCH_VERSION__"
$script:MinimumVersion = if ($script:RawVersion -match '^\d+\.\d+') { $script:RawVersion } else { "0.0.0" }

function Test-AiWatchInstalled {
    param(
        [string]$ExePath = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe",
        [string]$ScanTaskPath = "\Runlayer\",
        [string]$ScanTaskName = "AIWatchScan",
        [string]$UpdateTaskName = "AIWatchUpdate",
        [string]$MinimumVersion = $script:MinimumVersion
    )
    try {
        $id = [System.Security.Principal.WindowsIdentity]::GetCurrent()
        Write-DetectLog "run as $($id.Name) IsSystem=$($id.IsSystem) Is64BitProcess=$([Environment]::Is64BitProcess)"
    } catch {}

    if (-not (Test-Path $ExePath)) {
        Write-DetectLog "not-installed: aiwatch.exe missing at $ExePath"
        return $false
    }

    $installed = (Get-Item $ExePath).VersionInfo.FileVersion
    if ([string]::IsNullOrEmpty($installed)) {
        Write-DetectLog "not-installed: aiwatch.exe at $ExePath has no FileVersion"
        return $false
    }
    try {
        if ([version]$installed -lt [version]$MinimumVersion) {
            Write-DetectLog "not-installed: version $installed < minimum $MinimumVersion"
            return $false
        }
    } catch {}

    foreach ($taskName in @($ScanTaskName, $UpdateTaskName)) {
        $task = Get-ScheduledTask -TaskPath $ScanTaskPath -TaskName $taskName -ErrorAction SilentlyContinue
        if ($null -eq $task) {
            Write-DetectLog "not-installed: $taskName task missing (registration incomplete?)"
            return $false
        }
    }

    Write-DetectLog "installed: aiwatch.exe $installed (>= $MinimumVersion), $ScanTaskName + $UpdateTaskName present"
    return $true
}

if ($MyInvocation.InvocationName -ne '.') {
    $detected = Test-AiWatchInstalled 2>$null 3>$null 4>$null 5>$null 6>$null
    if ($detected) {
        Write-Output "AI Watch installed; AIWatchScan + AIWatchUpdate present"
    }
    exit 0
}
