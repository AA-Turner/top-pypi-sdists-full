# Build the native AI Watch hook shim (aiwatch-hook.exe) into the onedir bundle.
#
# Usage:
#   cd cli
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build_hook_shim.ps1
#
# Prerequisites:
#   - PyInstaller-built dist\aiwatch\ directory (onedir) must exist; the freeze
#     replaces that directory, so this must run after it
#   - Go toolchain matching aiwatch-hook-shim\go.mod

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CliDir = Resolve-Path "$ScriptDir\..\.."
$ShimDir = Resolve-Path "$CliDir\..\aiwatch-hook-shim"
$BundleDir = "$CliDir\dist\aiwatch"
$ShimPath = "$BundleDir\aiwatch-hook.exe"

$Version = (Select-String -Path "$CliDir\pyproject.toml" -Pattern '^version = "(.+)"' |
    Select-Object -First 1).Matches.Groups[1].Value

if (-not $Version) {
    Write-Error "Failed to read version from pyproject.toml"
    exit 1
}

if (-not (Test-Path $BundleDir -PathType Container)) {
    Write-Error "dist\aiwatch not found. Run pyinstaller first."
    exit 1
}

Write-Host "Building aiwatch-hook.exe v$Version..."

Push-Location $ShimDir
try {
    $env:CGO_ENABLED = "0"
    $env:GOOS = "windows"
    $env:GOARCH = "amd64"
    go build -trimpath -ldflags "-X main.version=$Version" -o $ShimPath ./cmd/aiwatch-hook
    if ($LASTEXITCODE -ne 0) {
        Write-Error "go build failed"
        exit 1
    }
}
finally {
    Pop-Location
}

if (-not (Test-Path $ShimPath)) {
    Write-Error "Expected $ShimPath to exist after go build"
    exit 1
}

Write-Host "Built: $ShimPath"
