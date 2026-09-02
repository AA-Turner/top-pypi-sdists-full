[CmdletBinding()]
param(
  [Parameter(Mandatory)]
  [string]$ProductionScript,

  [switch]$FakeSigner,

  [ValidateSet("success", "failure", "hang", "orphan-output")]
  [string]$Scenario = "success",

  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$Files
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($FakeSigner) {
  [Console]::Out.WriteLine("fake signer processed $($Files.Count) files")
  [Console]::Error.WriteLine("fake signer stderr")

  if (
    $Scenario -eq "failure" -and
    @($Files | Where-Object { (Split-Path -Leaf $_) -eq "fail.exe" }).Count -gt 0
  ) {
    exit 23
  }
  if ($Scenario -eq "hang") {
    Start-Sleep -Seconds 30
    exit 0
  }
  if ($Scenario -eq "orphan-output") {
    $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = (Get-Process -Id $PID).Path
    $startInfo.UseShellExecute = $false
    [void]$startInfo.ArgumentList.Add("-NoLogo")
    [void]$startInfo.ArgumentList.Add("-NoProfile")
    [void]$startInfo.ArgumentList.Add("-Command")
    [void]$startInfo.ArgumentList.Add("Start-Sleep -Seconds 30")
    $child = [System.Diagnostics.Process]::Start($startInfo)
    Set-Content -LiteralPath $env:SIGN_SHARDS_TEST_ORPHAN_PID_FILE -Value $child.Id
    $child.Dispose()
    exit 0
  }
  exit 0
}

function Assert-FailureContains {
  param(
    [Parameter(Mandatory)]
    [string]$Expected,

    [Parameter(Mandatory)]
    [hashtable]$Parameters
  )

  $message = $null
  try {
    & $ProductionScript @Parameters *> $null
  } catch {
    $message = $_.Exception.Message
  }

  if (-not $message) {
    throw "Expected signing to fail with: $Expected"
  }
  if (-not $message.Contains($Expected)) {
    throw "Expected failure containing '$Expected', got: $message"
  }
}

function New-FakeFiles {
  param(
    [Parameter(Mandatory)]
    [string[]]$Names
  )

  return @(
    foreach ($name in $Names) {
      (New-Item -ItemType File -Path (Join-Path $script:testRoot $name)).FullName
    }
  )
}

function New-SigningParameters {
  param(
    [Parameter(Mandatory)]
    [string]$TestScenario,

    [Parameter(Mandatory)]
    [string[]]$TestFiles,

    [int]$TestShardCount = 2,

    [int]$TestTimeoutSeconds = 5,

    [int]$TestMaxCommandLineLength = 30000
  )

  return @{
    SignCommand = (Get-Process -Id $PID).Path
    CommonArguments = @(
      "-NoLogo"
      "-NoProfile"
      "-File"
      $PSCommandPath
      "-ProductionScript"
      $ProductionScript
      "-FakeSigner"
      "-Scenario"
      $TestScenario
    )
    Files = $TestFiles
    ShardCount = $TestShardCount
    TimeoutSeconds = $TestTimeoutSeconds
    ShardStartDelayMilliseconds = 0
    MaxCommandLineLength = $TestMaxCommandLineLength
  }
}

$script:testRoot = Join-Path (
  [System.IO.Path]::GetTempPath()
) "runlayer-sign-shards-$([Guid]::NewGuid())"
[void](New-Item -ItemType Directory -Path $script:testRoot)

try {
  $successFiles = New-FakeFiles -Names @("one.exe", "two.dll", "three.pyd")
  $successParameters = New-SigningParameters `
    -TestScenario "success" `
    -TestFiles $successFiles
  & $ProductionScript @successParameters *> $null

  $failureFiles = New-FakeFiles -Names @("ok.exe", "fail.exe")
  $failureParameters = New-SigningParameters `
    -TestScenario "failure" `
    -TestFiles $failureFiles
  Assert-FailureContains `
    -Expected "Artifact signing failed for shard(s): 2" `
    -Parameters $failureParameters

  $hangFiles = New-FakeFiles -Names @("hang.exe")
  $hangParameters = New-SigningParameters `
    -TestScenario "hang" `
    -TestFiles $hangFiles `
    -TestShardCount 1 `
    -TestTimeoutSeconds 1
  Assert-FailureContains `
    -Expected "Timed-out shard(s): 1" `
    -Parameters $hangParameters

  $orphanPidFile = Join-Path $script:testRoot "orphan.pid"
  $env:SIGN_SHARDS_TEST_ORPHAN_PID_FILE = $orphanPidFile
  try {
    $orphanFiles = New-FakeFiles -Names @("orphan.exe")
    $orphanParameters = New-SigningParameters `
      -TestScenario "orphan-output" `
      -TestFiles $orphanFiles `
      -TestShardCount 1 `
      -TestTimeoutSeconds 1
    Assert-FailureContains `
      -Expected "Timed-out shard(s): 1" `
      -Parameters $orphanParameters
  } finally {
    if (Test-Path -LiteralPath $orphanPidFile) {
      $orphanPid = [int](Get-Content -LiteralPath $orphanPidFile)
      Stop-Process -Id $orphanPid -Force -ErrorAction SilentlyContinue
    }
    Remove-Item Env:SIGN_SHARDS_TEST_ORPHAN_PID_FILE -ErrorAction SilentlyContinue
  }

  $longFile = New-FakeFiles -Names @("$("x" * 100).exe")
  $guardParameters = New-SigningParameters `
    -TestScenario "success" `
    -TestFiles $longFile `
    -TestShardCount 1 `
    -TestMaxCommandLineLength 100
  Assert-FailureContains `
    -Expected "increase shard-count" `
    -Parameters $guardParameters
} finally {
  Remove-Item -LiteralPath $script:testRoot -Recurse -Force
}
