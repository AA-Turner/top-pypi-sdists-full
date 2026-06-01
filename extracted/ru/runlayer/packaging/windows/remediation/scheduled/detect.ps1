# Intune Remediation — Detection Script
# Run as logged-on user. Exit 0 = compliant, Exit 1 = triggers remediate.ps1.

$ErrorActionPreference = "SilentlyContinue"

$ExePath = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
if (-not (Test-Path $ExePath)) {
    Write-Output "aiwatch.exe not installed"
    exit 1
}

$MarkerDir = "$env:LOCALAPPDATA\Runlayer"
$MarkerFile = "$MarkerDir\last_scan"

if (-not (Test-Path $MarkerFile)) {
    Write-Output "No previous scan recorded"
    exit 1
}

$LastRun = Get-Content $MarkerFile -Raw | ForEach-Object { [datetime]::Parse($_.Trim()) }
$Threshold = (Get-Date).AddMinutes(-30)

if ($LastRun -lt $Threshold) {
    Write-Output "Last scan too old: $LastRun"
    exit 1
}

Write-Output "Scan is current: $LastRun"
exit 0
