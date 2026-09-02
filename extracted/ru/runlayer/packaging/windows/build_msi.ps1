# Build AI Watch .msi installer via WiX v4+.
#
# Usage:
#   cd cli
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build_msi.ps1
#
# Prerequisites:
#   - PyInstaller-built dist\aiwatch\ directory (onedir) must exist
#   - WiX Toolset v4+ (dotnet tool install --global wix)

param(
    [string]$Version = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CliDir = Resolve-Path "$ScriptDir\..\.."
$DistDir = "$CliDir\dist"

if ([string]::IsNullOrWhiteSpace($Version)) {
    $Version = (Select-String -Path "$CliDir\pyproject.toml" -Pattern '^version = "(.+)"' |
        Select-Object -First 1).Matches.Groups[1].Value
}

if (-not $Version) {
    Write-Error "Failed to read version from pyproject.toml"
    exit 1
}

$BundleDir = "$DistDir\aiwatch"
$ExePath = "$BundleDir\aiwatch.exe"
if (-not (Test-Path $BundleDir -PathType Container) -or -not (Test-Path $ExePath)) {
    Write-Error "dist\aiwatch\aiwatch.exe not found. Run pyinstaller first."
    exit 1
}

Write-Host "Building AI Watch .msi v$Version..."

$MsiPath = "$DistDir\aiwatch-$Version-win-x64.msi"
$ExternalCabPattern = "$DistDir\cab*.cab"

# Remove stale cabinets so the post-build guard checks only this build.
Get-ChildItem -Path $ExternalCabPattern -File -ErrorAction SilentlyContinue |
    Remove-Item -Force

# The deferred SYSTEM register/unregister custom actions use WixQuietExec64 from
# the WiX Util extension. Add it globally (idempotent; pinned to the wix version
# CI installs). Native non-zero here doesn't halt under ErrorActionPreference.
Write-Host "Ensuring WiX Util extension is available..."
wix extension add -g WixToolset.Util.wixext/5.0.2 2>&1 | Out-Null

wix build `
    -src "$ScriptDir\aiwatch.wxs" `
    -out $MsiPath `
    -arch x64 `
    -ext WixToolset.Util.wixext `
    -bindpath "$ScriptDir" `
    -d Version=$Version

if ($LASTEXITCODE -ne 0) {
    Write-Error "WiX build failed"
    exit 1
}

$ExternalCabs = @(Get-ChildItem -Path $ExternalCabPattern -File -ErrorAction SilentlyContinue)
if ($ExternalCabs.Count -gt 0) {
    $CabNames = $ExternalCabs.Name -join ", "
    Write-Error "WiX emitted external cabinet(s): $CabNames. MSI must be self-contained."
    exit 1
}

$BundleSizeBytes = (Get-ChildItem -Path $BundleDir -File -Recurse |
    Measure-Object -Property Length -Sum).Sum
$MsiSizeBytes = (Get-Item $MsiPath).Length
if ($BundleSizeBytes -ge 20MB -and $MsiSizeBytes -lt 10MB) {
    Write-Error "Built MSI is unexpectedly small ($MsiSizeBytes bytes); payload may be missing."
    exit 1
}

Write-Host "Built: $MsiPath"
