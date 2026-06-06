# Intune Remediation — Scan-on-detect. Run as logged-on user.
# `cmd /c ... 2>&1` merges streams below PowerShell — structlog stderr would
# otherwise pollute PS error stream and Intune would mark the run Failed.

$ExePath = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
if (-not (Test-Path $ExePath)) {
    Write-Output "aiwatch.exe not installed"
    exit 1
}

cmd /c "`"$ExePath`" scan 2>&1"
exit $LASTEXITCODE
