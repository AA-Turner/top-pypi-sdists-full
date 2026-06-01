# Build aiwatch-enforce .msi installer via WiX v4+.
#
# Usage:
#   cd cli
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build_enforce_msi.ps1
#
# Prerequisites:
#   - PyInstaller-built dist\aiwatch-enforce\ directory (onedir) must exist
#   - WiX Toolset v4+ (dotnet tool install --global wix)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CliDir = Resolve-Path "$ScriptDir\..\.."
$DistDir = "$CliDir\dist"

$Version = (Select-String -Path "$CliDir\pyproject.toml" -Pattern '^version = "(.+)"' |
    Select-Object -First 1).Matches.Groups[1].Value

if (-not $Version) {
    Write-Error "Failed to read version from pyproject.toml"
    exit 1
}

$BundleDir = "$DistDir\aiwatch-enforce"
$ExePath = "$BundleDir\aiwatch-enforce.exe"
if (-not (Test-Path $BundleDir -PathType Container) -or -not (Test-Path $ExePath)) {
    Write-Error "dist\aiwatch-enforce\aiwatch-enforce.exe not found. Run pyinstaller first."
    exit 1
}

Write-Host "Building aiwatch-enforce .msi v$Version..."

$MsiPath = "$DistDir\aiwatch-enforce-$Version-win-x64.msi"

wix build `
    -src "$ScriptDir\aiwatch-enforce.wxs" `
    -out $MsiPath `
    -arch x64 `
    -d Version=$Version

if ($LASTEXITCODE -ne 0) {
    Write-Error "WiX build failed"
    exit 1
}

Write-Host "Built: $MsiPath"
