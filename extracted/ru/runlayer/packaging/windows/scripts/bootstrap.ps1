# One-shot AI Watch bootstrap wrapper for Windows. **User context.**
#
# Runs `aiwatch.exe bootstrap --user` (enroll → install user-level hooks) in
# the current user's context. Refuses to run as SYSTEM since enrollment writes
# to the user keychain / HKCU. SYSTEM context wants the assert/ Intune
# Remediations pair instead — that pair handles the MDM hook install.
#
# Idempotent: re-running on a fully-bootstrapped device is a fast no-op
# (`aiwatch bootstrap` short-circuits when already enrolled).
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File bootstrap.ps1
#
# Exit codes mirror `aiwatch bootstrap`:
#   0  fully bootstrapped (or already bootstrapped / scan-only no-op)
#   1  hooks-install reported a write failure
#   2  required input missing (host)
#   4  --check: missing credential / drift
#
# For automated SYSTEM-context MDM hook re-assertion use the Intune
# Remediations pair in `..\assert\detect.ps1` + `remediate.ps1`. This
# standalone wrapper is for manual one-shot user-context runs (e.g. SCCM
# logon script, GPO logon script, helpdesk).

$ErrorActionPreference = "SilentlyContinue"

# Unconfigured fleets (no MDM-pushed OrgApiKey) short-circuit silently here so
# admins can push this logon script to the whole fleet without per-device-class
# targeting. Whether hooks actually install is decided downstream by the
# Enforcement / Sessions managed-config keys. Mirrors
# `runlayer_cli/mdm_config.py:_read_windows` (HKLM hive).
$OrgApiKey = (Get-ItemProperty -Path "HKLM:\Software\Runlayer\AIWatch" -Name "OrgApiKey" -ErrorAction SilentlyContinue).OrgApiKey
if ([string]::IsNullOrEmpty($OrgApiKey)) {
    exit 0
}

# Hard-refuse SYSTEM context — bootstrap touches HKCU credentials and
# %APPDATA%; running as SYSTEM would write to the wrong profile and leave
# the user's AI client unenrolled.
$Identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
if ($Identity.IsSystem) {
    Write-Error "aiwatch bootstrap must run as the logged-on user, not SYSTEM. Use the assert/ Intune Remediations pair for SYSTEM-context MDM hook installs."
    exit 2
}

$ExePath = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
if (-not (Test-Path $ExePath)) {
    # Fall back to PATH lookup for non-default installs.
    $Resolved = Get-Command aiwatch.exe -ErrorAction SilentlyContinue
    if ($null -eq $Resolved) {
        Write-Error "aiwatch.exe not found at $ExePath or on PATH; install the AI Watch MSI first."
        exit 2
    }
    $ExePath = $Resolved.Source
}

# `cmd /c ... 2>&1` merges stderr into stdout so structlog output doesn't
# pollute PowerShell's error stream (Intune / SCCM treat any error-stream
# output as a failure regardless of $LASTEXITCODE).
cmd /c "`"$ExePath`" bootstrap --user 2>&1"
exit $LASTEXITCODE
