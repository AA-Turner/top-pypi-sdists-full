# Wrap the Runlayer CLI .msi into an .intunewin package for Intune deployment.
#
# Usage:
#   cd cli
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build_intunewin_runlayer.ps1
#
# Intune Win32 LOB app settings (configure in the Intune portal):
#   Install command:   msiexec /i "runlayer-<version>-win-x64.msi" /qn
#   Uninstall command: msiexec /x "{ProductCode}" /qn
#   Detection rule:    MSI product code (or file Program Files\Runlayer\CLI\runlayer.exe)
#
# Prerequisites:
#   - The .msi must already exist in dist\ (run build_msi_runlayer.ps1 first)
#   - IntuneWinAppUtil.exe is downloaded automatically if not present

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CliDir = Resolve-Path "$ScriptDir\..\.."
$DistDir = "$CliDir\dist"
$ToolsDir = "$CliDir\build\tools"

$Version = (Select-String -Path "$CliDir\pyproject.toml" -Pattern '^version = "(.+)"' |
    Select-Object -First 1).Matches.Groups[1].Value

$MsiFile = "runlayer-$Version-win-x64.msi"
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

& $IntuneUtil `
    -c $DistDir `
    -s $MsiFile `
    -o $DistDir `
    -q

$IntunewinPath = "$DistDir\$($MsiFile -replace '\.msi$', '.intunewin')"
$FinalPath = "$DistDir\runlayer-$Version-win-x64.intunewin"

if (Test-Path $IntunewinPath) {
    if ($IntunewinPath -ne $FinalPath) {
        Move-Item -Force $IntunewinPath $FinalPath
    }
    Write-Host "Built: $FinalPath"
} else {
    Write-Error "IntuneWinAppUtil did not produce expected output"
    exit 1
}
