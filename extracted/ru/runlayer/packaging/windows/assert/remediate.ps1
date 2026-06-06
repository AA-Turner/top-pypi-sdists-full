# Intune Remediation — MDM Hook-Config Remediation. Run as SYSTEM.
# Pairs with assert/detect.ps1. Executes `aiwatch.exe setup hooks install
# --mdm` to write enterprise hook configs to:
#   C:\ProgramData\Cursor\hooks.json
#   %USERPROFILE%\.claude\settings.json (console user) — Claude Code's
#     enterprise managed-settings.json hooks regressed (ENG-3204), so its
#     hooks are written to the console user's settings.json instead.
# (Codex on Windows has no enterprise location; degrades to per-user.)
#
# Enable "Run this script using the logged-on credentials" set to **No** —
# the writes are to SYSTEM-scoped paths and must run as SYSTEM.
#
# Hard-fails with exit 4 when the console user hasn't run `aiwatch enroll`
# yet (the per-user credential lives in HKCU + the user keychain; SYSTEM
# can't bootstrap it). Operator must trigger packaging/windows/scripts/
# bootstrap.ps1 as the logged-on user — e.g. via SCCM / GPO logon script.
#
# Exit codes mirror `aiwatch setup hooks install`:
#   0 — every supported client has its enterprise hook config written
#   1 — at least one write failed
#   2 — missing host (MDM misconfig)
#   4 — missing console-user credential (run scripts/bootstrap.ps1 first)

$ErrorActionPreference = "SilentlyContinue"

# Scan-only fleets (no MDM-pushed EnrollmentKey) short-circuit silently here as
# belt-and-suspenders. detect.ps1 already gates, but a manual remediate.ps1
# run shouldn't fire either. Mirrors `runlayer_cli/mdm_config.py:_read_windows`.
$EnrollmentKey = (Get-ItemProperty -Path "HKLM:\Software\Runlayer\AIWatch" -Name "EnrollmentKey" -ErrorAction SilentlyContinue).EnrollmentKey
if ([string]::IsNullOrEmpty($EnrollmentKey)) {
    exit 0
}

$Identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $Identity.IsSystem) {
    Write-Output "aiwatch MDM hook remediate must run as SYSTEM, not the logged-on user. Disable 'Run this script using the logged-on credentials'."
    exit 2
}

$ExePath = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
if (-not (Test-Path $ExePath)) {
    Write-Output "aiwatch.exe not found at $ExePath; install the AI Watch MSI first."
    exit 2
}

cmd /c "`"$ExePath`" setup hooks install --mdm 2>&1"
exit $LASTEXITCODE
