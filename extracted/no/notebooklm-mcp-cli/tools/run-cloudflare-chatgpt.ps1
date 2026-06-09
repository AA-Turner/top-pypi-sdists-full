#Requires -Version 7.0
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PublicHostname,
    [string]$HostName = '127.0.0.1',
    [int]$Port = 8811,
    [string]$Profile = 'default',
    [string]$Cloudflared = 'cloudflared',
    [switch]$SkipAuthCheck
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (-not $SkipAuthCheck) {
    Write-Host '== NotebookLM auth status (read-only) =='
    uv run nlm login --profile $Profile --check
}

$origin = "http://$HostName`:$Port"
Write-Host '== Starting Cloudflare named/quick tunnel helper =='
Write-Host "Public MCP URL: https://$PublicHostname/mcp"
Write-Host "Public artifacts URL: https://$PublicHostname/artifacts/<filename>"
Write-Host ''
Write-Host 'In another terminal, run the MCP server if it is not already running:'
Write-Host "  uv run notebooklm-mcp --transport http --host $HostName --port $Port --query-timeout 600"
Write-Host ''
Write-Host 'Starting cloudflared as a local reverse proxy. For production, prefer a named tunnel with ingress:'
Write-Host "  hostname: $PublicHostname"
Write-Host "  service: $origin"
Write-Host ''
& $Cloudflared tunnel --url $origin
