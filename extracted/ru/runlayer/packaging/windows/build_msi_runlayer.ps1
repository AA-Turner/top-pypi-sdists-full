# Build the Runlayer CLI .msi installer via WiX v4+.
#
# Usage:
#   cd cli
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build_msi_runlayer.ps1
#
# Prerequisites:
#   - PyInstaller-built dist\runlayer\ directory (onedir) must exist
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

$BundleDir = "$DistDir\runlayer"
$ExePath = "$BundleDir\runlayer.exe"
if (-not (Test-Path $BundleDir -PathType Container) -or -not (Test-Path $ExePath)) {
    Write-Error "dist\runlayer\runlayer.exe not found. Run pyinstaller first."
    exit 1
}

Write-Host "Building Runlayer CLI .msi v$Version..."

$MsiPath = "$DistDir\runlayer-$Version-win-x64.msi"

wix build `
    -src "$ScriptDir\runlayer.wxs" `
    -out $MsiPath `
    -arch x64 `
    -bindpath "$ScriptDir" `
    -d Version=$Version

if ($LASTEXITCODE -ne 0) {
    Write-Error "WiX build failed"
    exit 1
}

Write-Host "Built: $MsiPath"
