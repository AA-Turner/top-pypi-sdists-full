# Intune Remediation — Scan-on-detect
# Runs aiwatch.exe scan directly in the detection phase.
# Exit 0 = compliant (scan succeeded), Exit 1 = non-compliant (scan failed or binary missing).
# Run as logged-on user so scan sees per-user MCP client configs under %APPDATA%.
# `cmd /c ... 2>&1` merges streams below PowerShell so structlog stderr doesn't
# pollute PS error stream (Intune marks Failed otherwise).

$ExePath = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
if (-not (Test-Path $ExePath)) {
    Write-Output "aiwatch.exe not installed"
    exit 1
}

cmd /c "`"$ExePath`" scan 2>&1"
exit $LASTEXITCODE
