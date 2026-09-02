#Requires -Version 5.1

$ErrorActionPreference = "Stop"

$minPesterVersion = [version]"5.0.0"
$pester = Get-Module -Name Pester -ListAvailable |
    Sort-Object Version -Descending |
    Select-Object -First 1

if (-not $pester -or $pester.Version -lt $minPesterVersion) {
    Write-Host "Installing Pester 5.x..."
    Install-Module `
        -Name Pester `
        -MinimumVersion 5.0.0 `
        -Force `
        -Scope CurrentUser `
        -SkipPublisherCheck
}

Import-Module Pester -MinimumVersion 5.0.0

$config = [PesterConfiguration]::Default
$config.Run.Path = $PSScriptRoot
$config.Run.Exit = $true
$config.Output.Verbosity = "Detailed"

Invoke-Pester -Configuration $config
