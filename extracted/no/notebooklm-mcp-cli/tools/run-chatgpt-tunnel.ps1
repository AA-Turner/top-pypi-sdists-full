#Requires -Version 7.0
[CmdletBinding()]
param(
    [string]$HostName = '127.0.0.1',
    [int]$Port = 8811,
    [string]$Profile = 'default',
    [switch]$SkipAuthCheck,
    [switch]$NoOpenAITunnel,
    [string]$OpenAITunnelCommand = 'openai'
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (-not $SkipAuthCheck) {
    Write-Host '== NotebookLM auth status (read-only) =='
    uv run nlm login --profile $Profile --check
}

Write-Host '== Starting NotebookLM MCP HTTP server =='
Write-Host "Local MCP: http://$HostName`:$Port/mcp"
Write-Host "Artifacts: http://$HostName`:$Port/artifacts/<filename>"
Write-Host ''

$env:PYTHONUNBUFFERED = '1'
$serverArgs = @('run', 'notebooklm-mcp', '--transport', 'http', '--host', $HostName, '--port', "$Port", '--query-timeout', '600')

if ($NoOpenAITunnel) {
    uv @serverArgs
    exit $LASTEXITCODE
}

Write-Host 'Start the OpenAI/ChatGPT secure tunnel in a second terminal if your OpenAI CLI does not support launching it inline.'
Write-Host 'Use target URL:'
Write-Host "  http://$HostName`:$Port/mcp"
Write-Host ''
uv @serverArgs
