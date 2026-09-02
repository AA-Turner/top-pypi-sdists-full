# Wrap the Runlayer CLI .msi into an .intunewin package for Intune deployment.
#
# Usage:
#   cd cli
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build_intunewin_runlayer.ps1
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build_intunewin_runlayer.ps1 -IncludeDesktop
#
# Intune Win32 LOB app settings (configure in the Intune portal):
#   Install command:   msiexec /i "runlayer-<version>-win-x64.msi" /qn
#   Uninstall command: msiexec /x "{ProductCode}" /qn
#   Detection rule:    MSI product code (or file Program Files\Runlayer\CLI\runlayer.exe).
#                      CLIUpdate registration failure fails the MSI, so either
#                      marker implies the managed updater was registered.
#
# Prerequisites:
#   - The .msi must already exist in dist\ (run build_msi_runlayer.ps1 first)
#   - IntuneWinAppUtil.exe is downloaded automatically if not present

param(
    [switch]$IncludeDesktop
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CliDir = Resolve-Path "$ScriptDir\..\.."
$DistDir = "$CliDir\dist"
$ToolsDir = "$CliDir\build\tools"

$Version = (Select-String -Path "$CliDir\pyproject.toml" -Pattern '^version = "(.+)"' |
    Select-Object -First 1).Matches.Groups[1].Value

$ArtifactPrefix = if ($IncludeDesktop) { "runlayer-desktop" } else { "runlayer" }
$MsiFile = "$ArtifactPrefix-$Version-win-x64.msi"
$MsiPath = "$DistDir\$MsiFile"

if (-not (Test-Path $MsiPath)) {
    Write-Error "$MsiFile not found in dist\. Run build_msi_runlayer.ps1 first."
    exit 1
}

$IntuneUtil = "$ToolsDir\IntuneWinAppUtil.exe"
if (-not (Test-Path $IntuneUtil)) {
    Write-Host "Downloading IntuneWinAppUtil.exe..."
    New-Item -ItemType Directory -Path $ToolsDir -Force | Out-Null
    $Url = "https://github.com/microsoft/Microsoft-Win32-Content-Prep-Tool/raw/master/IntuneWinAppUtil.exe"
    Invoke-WebRequest -Uri $Url -OutFile $IntuneUtil -UseBasicParsing
}

Write-Host "Building .intunewin from $MsiFile..."

$StagingDir = Join-Path ([System.IO.Path]::GetTempPath()) "runlayer-intunewin-$([Guid]::NewGuid())"
New-Item -ItemType Directory -Path $StagingDir | Out-Null

try {
    Copy-Item -LiteralPath $MsiPath -Destination (Join-Path $StagingDir $MsiFile)

    & $IntuneUtil `
        -c $StagingDir `
        -s $MsiFile `
        -o $DistDir `
        -q

    if ($LASTEXITCODE -ne 0) {
        throw "IntuneWinAppUtil failed with exit code $LASTEXITCODE"
    }
} finally {
    Remove-Item -LiteralPath $StagingDir -Recurse -Force -ErrorAction SilentlyContinue
}

$IntunewinPath = "$DistDir\$($MsiFile -replace '\.msi$', '.intunewin')"
$FinalPath = "$DistDir\$ArtifactPrefix-$Version-win-x64.intunewin"

if (Test-Path $IntunewinPath) {
    if ($IntunewinPath -ne $FinalPath) {
        Move-Item -Force $IntunewinPath $FinalPath
    }
    Write-Host "Built: $FinalPath"
} else {
    Write-Error "IntuneWinAppUtil did not produce expected output"
    exit 1
}
