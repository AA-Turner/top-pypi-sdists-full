# Intune Remediation — Remediation Script. Run as logged-on user.
# `cmd /c ... 2>&1` merges streams below PowerShell — structlog stderr would
# otherwise pollute PS error stream and Intune would mark Failed.

$ExePath = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"

if (-not (Test-Path $ExePath)) {
    Write-Output "aiwatch.exe not found at $ExePath"
    exit 1
}

cmd /c "`"$ExePath`" scan 2>&1"
$ScanExitCode = $LASTEXITCODE

# Marker only on success — failed scan must stay non-compliant so Intune retries.
if ($ScanExitCode -eq 0) {
    $MarkerDir = "$env:LOCALAPPDATA\Runlayer"
    if (-not (Test-Path $MarkerDir)) {
        New-Item -ItemType Directory -Path $MarkerDir -Force | Out-Null
    }
    (Get-Date -Format "o") | Set-Content "$MarkerDir\last_scan"
}

exit $ScanExitCode
