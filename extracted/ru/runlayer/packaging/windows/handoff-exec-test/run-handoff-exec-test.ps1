$ErrorActionPreference = "Stop"

$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$cliDirectory = (Resolve-Path (Join-Path $scriptDirectory "..\..\..")).Path
$testRoot = Join-Path $env:RUNNER_TEMP "runlayer-handoff-$PID"
$productDirectory = Join-Path $testRoot "product"
$msiexecPath = Join-Path $testRoot "msiexec.exe"
$markerPath = Join-Path $testRoot "msiexec-started.txt"
$logPath = Join-Path $testRoot "handoff.log"
$stagedMsiPath = Join-Path $testRoot "handoff.msi"
$aiwatchPath = Join-Path $productDirectory "aiwatch.exe"
$serviceName = "RunlayerHandoffTestSvc$PID"
$targetVersion = "9.9.9"
$serviceCreated = $false

New-Item -ItemType Directory -Force $productDirectory | Out-Null
Push-Location $cliDirectory
try {
    $escapedMarkerPath = $markerPath.Replace('"', '""')
    $msiexecSource = @"
using System;
using System.IO;

namespace Runlayer.HandoffExecTest.Msiexec
{
    public static class Program
    {
        public static int Main(string[] args)
        {
            File.WriteAllText(@"$escapedMarkerPath", string.Join(" ", args));
            return 0;
        }
    }
}
"@
    Add-Type `
        -TypeDefinition $msiexecSource `
        -Language CSharp `
        -OutputAssembly $msiexecPath `
        -OutputType ConsoleApplication

    $aiwatchSource = @"
using System;

namespace Runlayer.HandoffExecTest.AIWatch
{
    public static class Program
    {
        public static int Main(string[] args)
        {
            Console.WriteLine("aiwatch version $targetVersion");
            return 0;
        }
    }
}
"@
    Add-Type `
        -TypeDefinition $aiwatchSource `
        -Language CSharp `
        -OutputAssembly $aiwatchPath `
        -OutputType ConsoleApplication

    Set-Content -Path $stagedMsiPath -Value "stub"
    & "$env:WINDIR\System32\sc.exe" create $serviceName `
        binPath= "$env:WINDIR\System32\svchost.exe" `
        start= demand | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create test service: $serviceName"
    }
    $serviceCreated = $true

    $emitterPath = Join-Path $scriptDirectory "emit_handoff_script.py"
    $encodedCommand = & uv run --frozen python $emitterPath `
        --msiexec-path $msiexecPath `
        --log-path $logPath `
        --product-directory $productDirectory `
        --service-name $serviceName `
        --target-version $targetVersion
    if ($LASTEXITCODE -ne 0) {
        throw "Could not emit the handoff script"
    }
    $encodedCommand = ([string]$encodedCommand).Trim()

    $windowsPowerShell = Join-Path $env:WINDIR `
        "System32\WindowsPowerShell\v1.0\powershell.exe"
    & $windowsPowerShell `
        -NoLogo `
        -NoProfile `
        -NonInteractive `
        -EncodedCommand $encodedCommand
    $handoffExitCode = $LASTEXITCODE

    $handoffLog = ""
    if (Test-Path $logPath -PathType Leaf) {
        $handoffLog = Get-Content -Raw $logPath
    }
    if ($handoffExitCode -ne 0) {
        throw "Handoff exited $handoffExitCode. Log: $handoffLog"
    }
    if (-not (Test-Path $markerPath -PathType Leaf)) {
        throw "Handoff did not launch the installer stub"
    }
    if ($handoffLog -notmatch "post-install verification passed") {
        throw "Handoff did not verify the installed binary. Log: $handoffLog"
    }
    if ($handoffLog -match "handoff failed:") {
        throw "Handoff logged a failure: $handoffLog"
    }
}
finally {
    if ($serviceCreated) {
        & "$env:WINDIR\System32\sc.exe" delete $serviceName | Out-Null
    }
    Pop-Location
    Remove-Item -Recurse -Force $testRoot -ErrorAction SilentlyContinue
}
