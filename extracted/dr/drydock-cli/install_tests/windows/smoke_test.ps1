# Drydock install smoke test — Windows PowerShell
# Mirrors the Linux smoke_test.py steps. Run from an Administrator PowerShell.

$ErrorActionPreference = "Continue"
$start = Get-Date

$LLAMACPP_URL = if ($env:LLAMACPP_URL) { $env:LLAMACPP_URL } else { "http://localhost:8001/v1" }
$LLAMACPP_MODEL = if ($env:LLAMACPP_MODEL) { $env:LLAMACPP_MODEL } else { "gemma4" }
$DRYDOCK_VERSION = if ($env:DRYDOCK_VERSION) { $env:DRYDOCK_VERSION } else { "" }
$SMOKE_TIMEOUT_S = if ($env:SMOKE_TIMEOUT_S) { [int]$env:SMOKE_TIMEOUT_S } else { 90 }

$results = @{}
function Log($msg) { Write-Host "[smoke] $msg" }

# Step 1: Python check
Log "Checking Python version..."
try {
    $pyver = (python --version 2>&1)
    if ($pyver -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]; $minor = [int]$Matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 12)) {
            $results.python = @{ok=$false; detail="found $pyver, need 3.12+"}
        } else {
            $results.python = @{ok=$true; detail=$pyver}
        }
    } else {
        $results.python = @{ok=$false; detail="couldn't parse: $pyver"}
    }
} catch {
    $results.python = @{ok=$false; detail="python not on PATH"}
}

if (-not $results.python.ok) {
    Write-Host "FATAL: $($results.python.detail)"
    exit 1
}

# Step 2: clean venv
Log "Creating clean venv..."
$venv = "$env:TEMP\drydock-smoke-venv"
if (Test-Path $venv) { Remove-Item -Recurse -Force $venv }
python -m venv $venv
& "$venv\Scripts\Activate.ps1"

# Step 3: install
Log "Installing drydock-cli..."
$pkg = "drydock-cli"
if ($DRYDOCK_VERSION) { $pkg = "drydock-cli==$DRYDOCK_VERSION" }
pip install --no-cache-dir $pkg 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    $results.install = @{ok=$false; detail="pip install failed"}
} else {
    $results.install = @{ok=$true; detail=$pkg}
}

# Step 4: version
Log "Verifying drydock --version..."
$verOut = drydock --version 2>&1
if ($LASTEXITCODE -eq 0) {
    $results.version = @{ok=$true; detail=$verOut}
} else {
    $results.version = @{ok=$false; detail="rc=$LASTEXITCODE"}
}

# Step 5: help
Log "Verifying drydock --help..."
$helpOut = drydock --help 2>&1
if ($LASTEXITCODE -eq 0 -and $helpOut -match "[Uu]sage") {
    $results.help = @{ok=$true; detail="help ok"}
} else {
    $results.help = @{ok=$false; detail="rc=$LASTEXITCODE"}
}

# Step 6: network reach
Log "Checking network reach to $LLAMACPP_URL/models..."
try {
    $resp = Invoke-RestMethod "$LLAMACPP_URL/models" -TimeoutSec 10
    $names = @()
    foreach ($m in $resp.data + $resp.models) { if ($m.id) { $names += $m.id } elseif ($m.name) { $names += $m.name } }
    if ($names -contains $LLAMACPP_MODEL) {
        $results.network = @{ok=$true; detail="reachable, models=$names"}
    } else {
        $results.network = @{ok=$false; detail="model $LLAMACPP_MODEL not found"}
    }
} catch {
    $results.network = @{ok=$false; detail="unreachable: $_"}
}

# Step 7: config
Log "Writing config..."
$cfgDir = "$env:USERPROFILE\.drydock"
New-Item -ItemType Directory -Force -Path $cfgDir | Out-Null
$cfgPath = "$cfgDir\config.toml"
@"
active_model = "local"
auto_approve = true
enable_telemetry = false
enable_update_checks = false
enable_auto_update = false
disable_welcome_banner_animation = true
api_timeout = 60.0

[[providers]]
name = "llamacpp"
api_base = "$LLAMACPP_URL"
api_key_env_var = ""
api_style = "openai"
backend = "generic"

[[models]]
name = "$LLAMACPP_MODEL"
provider = "llamacpp"
alias = "local"
"@ | Out-File -FilePath $cfgPath -Encoding utf8

$results.config = @{ok=$true; detail=$cfgPath}

# Step 8: smoke prompt (very basic on Windows — feeds via stdin pipe).
# Note: this exercises the install + first-run path. Full visual TUI
# verification needs a human run.
Log "Spawning drydock with a prompt..."
$cwd = $PWD.Path
$promptIn = "what is 2+2? Answer in one word.`r`n/exit`r`n"
try {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "drydock"
    $psi.WorkingDirectory = $cwd
    $psi.UseShellExecute = $false
    $psi.RedirectStandardInput = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $proc = [System.Diagnostics.Process]::Start($psi)
    $proc.StandardInput.WriteLine($promptIn)
    $proc.StandardInput.Close()
    if (-not $proc.WaitForExit(($SMOKE_TIMEOUT_S * 1000))) {
        $proc.Kill()
        $results.smoke = @{ok=$false; detail="timed out after $SMOKE_TIMEOUT_S s"}
    } else {
        $output = $proc.StandardOutput.ReadToEnd() + $proc.StandardError.ReadToEnd()
        if ($output -match "(?i)\b(4|four)\b") {
            $results.smoke = @{ok=$true; detail="response matched"}
        } else {
            $results.smoke = @{ok=$false; detail="no 4/four in response; tail: $($output.Substring([Math]::Max(0, $output.Length-300)))"}
        }
    }
} catch {
    $results.smoke = @{ok=$false; detail="spawn error: $_"}
}

# Emit result
$elapsed = (Get-Date) - $start
$allPass = $true
$parts = @()
foreach ($k in $results.Keys) {
    if ($results[$k].ok) {
        $parts += "$k=ok"
    } else {
        $allPass = $false
        $parts += "$k=FAIL"
    }
}
$status = if ($allPass) { "PASS" } else { "FAIL" }
$partsStr = $parts -join " "
Write-Host ""
Write-Host "[RESULT] windows $status  $partsStr  elapsed=$([int]$elapsed.TotalSeconds)s"
if (-not $allPass) {
    Write-Host ""
    Write-Host "=== failure details ==="
    foreach ($k in $results.Keys) {
        if (-not $results[$k].ok) {
            Write-Host "  $k`: $($results[$k].detail)"
        }
    }
}

if ($allPass) { exit 0 } else { exit 1 }
