# Intune Remediation — MDM Hook-Config Detection. Run as SYSTEM.
# Pairs with assert/remediate.ps1. Reports whether the AI Watch enterprise
# hook configs are current at C:\ProgramData\Cursor, the console user's
# %USERPROFILE%\.claude\settings.json (Claude Code managed-settings hooks
# regressed — ENG-3204), etc.:
#   exit 0  — hook configs current (compliant).
#   exit 1  — drift, missing files, or missing user credential — triggers remediate.
#   exit 2  — misconfig (refused user context or missing exe); Intune marks
#             "Failed" so it surfaces in the dashboard instead of churning.
#
# Enable "Run this script using the logged-on credentials" set to **No** in
# the Intune Remediation settings — this script writes/reads SYSTEM-scoped
# config dirs (Program Files, ProgramData) and must run as SYSTEM.
#
# Enrollment runs separately via packaging/windows/scripts/bootstrap.ps1 as
# the logged-on user (SCCM / GPO logon script). The credential gate here
# checks `C:\Users\<console>\.runlayer\.enrolled-<host_key>` — an empty marker
# file dropped only by enrollment success paths. The secret may live in the
# Credential Manager (SYSTEM can't read it); the marker is sufficient proof
# the user has enrolled.

$ErrorActionPreference = "SilentlyContinue"

# Scan-only fleets (no MDM-pushed EnrollmentKey) short-circuit silently here so
# Intune treats the device as compliant and never fires remediate.ps1. Path
# mirrors `runlayer_cli/mdm_config.py:_read_windows` (HKLM hive).
$EnrollmentKey = (Get-ItemProperty -Path "HKLM:\Software\Runlayer\AIWatch" -Name "EnrollmentKey" -ErrorAction SilentlyContinue).EnrollmentKey
if ([string]::IsNullOrEmpty($EnrollmentKey)) {
    exit 0
}

$Identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $Identity.IsSystem) {
    Write-Output "aiwatch MDM hook detect must run as SYSTEM, not the logged-on user. Disable 'Run this script using the logged-on credentials'."
    exit 2
}

$ExePath = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
if (-not (Test-Path $ExePath)) {
    Write-Output "aiwatch.exe not installed at $ExePath"
    exit 2
}

# `cmd /c ... 2>&1` keeps structlog stderr off PowerShell's error stream so
# Intune doesn't mark the run "Failed" when the binary writes informational
# diagnostics during a successful 0 exit.
cmd /c "`"$ExePath`" setup hooks check --mdm 2>&1"
$CheckExit = $LASTEXITCODE

# `aiwatch setup hooks check --mdm` exit codes:
#   0 — every supported client has a current Runlayer hook config (compliant).
#   1 — drift / missing files in at least one client.           → remediate.
#   2 — host not configured.                                    → surface as failed.
#   4 — no console-user credential for the host yet.            → remediate (which will exit 4 too, surfacing in dashboard).
switch ($CheckExit) {
    0 { exit 0 }
    1 { exit 1 }
    2 { exit 2 }
    4 { exit 1 }
    default { exit 1 }
}
