# Build the Runlayer CLI .msi installer via WiX v4+.
#
# Usage:
#   cd cli
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build_msi_runlayer.ps1
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build_msi_runlayer.ps1 -IncludeDesktop
#
# Prerequisites:
#   - PyInstaller-built dist\runlayer\ directory (onedir) must exist
#   - WiX Toolset v4+ (dotnet tool install --global wix)

param(
    [switch]$IncludeDesktop
)

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
$TrayDir = "$BundleDir\tray"
$TrayExePath = "$TrayDir\RunlayerTray.exe"
if (-not (Test-Path $BundleDir -PathType Container) -or -not (Test-Path $ExePath)) {
    Write-Error "dist\runlayer\runlayer.exe not found. Run pyinstaller first."
    exit 1
}
if ($IncludeDesktop -and -not (Test-Path $TrayExePath -PathType Leaf)) {
    Write-Error "dist\runlayer\tray\RunlayerTray.exe not found. Run desktop\windows\build.ps1 first."
    exit 1
}
if (-not $IncludeDesktop -and (Test-Path $TrayDir)) {
    # WiX 5.0.2's Files harvesting cannot exclude subtrees, so the wxs picks
    # up everything under dist\runlayer. Keep the CLI-only MSI tray-free by
    # dropping the tray build output; desktop builds re-publish it.
    Write-Host "Removing dist\runlayer\tray from bundle for CLI-only build..."
    Remove-Item -Recurse -Force $TrayDir
}

$PackageName = if ($IncludeDesktop) { "Runlayer" } else { "Runlayer CLI" }
$PackageSlug = if ($IncludeDesktop) { "desktop" } else { "cli" }
$ArtifactPrefix = if ($IncludeDesktop) { "runlayer-desktop" } else { "runlayer" }
$IncludeDesktopValue = if ($IncludeDesktop) { "1" } else { "0" }

Write-Host "Building $PackageName .msi v$Version..."

$MsiPath = "$DistDir\$ArtifactPrefix-$Version-win-x64.msi"
$ExternalCabPattern = "$DistDir\cab*.cab"
$MarkerDir = "$CliDir\build\pkg-runlayer-$PackageSlug"
$MarkerPath = "$MarkerDir\product"
New-Item -ItemType Directory -Path $MarkerDir -Force | Out-Null
Set-Content -LiteralPath $MarkerPath -Value $PackageSlug -Encoding ascii

# Custom actions use the WiX Util extension's WixQuietExec64. Keep this exact
# version aligned with build_msi.ps1 and the release workflow toolchain.
Write-Host "Ensuring WiX Util extension is available..."
wix extension add -g WixToolset.Util.wixext/5.0.2 2>&1 | Out-Null

# Remove stale cabinets so the post-build guard checks only this build.
Get-ChildItem -Path $ExternalCabPattern -File -ErrorAction SilentlyContinue |
    Remove-Item -Force

wix build `
    -src "$ScriptDir\runlayer.wxs" `
    -out $MsiPath `
    -arch x64 `
    -ext WixToolset.Util.wixext `
    -bindpath "$ScriptDir" `
    -d Version=$Version `
    -d IncludeDesktop=$IncludeDesktopValue `
    -d "ProductName=$PackageName" `
    -d "ProductMarkerPath=$MarkerPath"

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
