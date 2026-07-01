# CVC installer — Windows
# Source of truth: ~/Projects/Portfolio-E/installers/install.ps1
# Mirrored to:    ~/Projects/cvc/scripts/install.ps1

$ErrorActionPreference = "Continue"
$ProgressPreference    = "SilentlyContinue"

# Force UTF-8 so ✓ ⚠ ✗ render correctly on every Windows console
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
    chcp 65001 > $null 2>&1
} catch {}

$PackageName  = "tm-ai[all]"
$PyPIName     = "tm-ai"
$UvInstallUrl = "https://astral.sh/uv/install.ps1"

if (-not $env:UV_HTTP_TIMEOUT) { $env:UV_HTTP_TIMEOUT = "300" }

# Pin a known-good Python. Python 3.14 ships Unicode 17 which breaks
# rich<14 ("No module named 'rich._unicode_data.unicode17_0_0'"), and
# our dep pins rich>=13 — so we lock the tool venv to 3.13 across all
# installs/retries to keep CVC importable on every box.
$CvcPinPy = "3.13"

# ── CVC branded colours (24-bit truecolor) ─────────────────────────────────
$ESC        = [char]27
$CVC_RED    = "$ESC[38;2;204;51;51m"
$CVC_BRIGHT = "$ESC[38;2;255;68;68m"
$CVC_DIM    = "$ESC[38;2;139;112;112m"
$CVC_GREEN  = "$ESC[38;2;80;200;120m"
$BOLD       = "$ESC[1m"
$RESET      = "$ESC[0m"

function Write-CvcInfo ($msg) { Write-Host "  ${CVC_DIM}$msg${RESET}" }
function Write-CvcOk   ($msg) { Write-Host "  ${CVC_GREEN}${BOLD}✓${RESET} $msg" }
function Write-CvcWarn ($msg) { Write-Host "  ${CVC_DIM}! $msg${RESET}" }
function Write-CvcErr  ($msg) { Write-Host "  ${CVC_RED}${BOLD}✗${RESET} $msg" }

# Clear the current line. When 'cvc update' runs, the parent cvc.exe
# exits and the user's shell prompt comes back (PS C:\Users\jk422> in
# the console) before the replacer (which downloaded this script)
# starts running it. Without this clear, the user sees the prompt
# still on the same line as our first install line, which looks like
# a corrupt terminal. Overwrite the prompt with spaces and re-position
# the cursor at column 0 before we print anything.
[Console]::Write("`r" + (" " * 120) + "`r")

Write-Host ""
Write-Host "$CVC_RED$BOLD* Installing ${CVC_BRIGHT}CVC${CVC_RED}...$RESET"

# ── Resolve uv (install if missing) ────────────────────────────────────────
function Resolve-UvExe {
    $cmd = Get-Command uv -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $candidates = @(
        (Join-Path $env:USERPROFILE ".local\bin\uv.exe"),
        (Join-Path $env:LOCALAPPDATA "uv\uv.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\uv\uv.exe")
    )
    foreach ($c in $candidates) { if (Test-Path $c) { return $c } }
    return $null
}

$Script:UvExe = Resolve-UvExe

if (-not $Script:UvExe) {
    Write-CvcInfo "Installing package manager..."
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13
        Set-ExecutionPolicy Bypass -Scope Process -Force -ErrorAction SilentlyContinue
        $uvInstaller = Invoke-RestMethod -Uri $UvInstallUrl
        $null = & ([scriptblock]::Create($uvInstaller)) *>&1
    } catch {
        Write-CvcWarn "Package manager installer exited with a warning (continuing)..."
    }
    $env:PATH = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")
    $Script:UvExe = Resolve-UvExe
}

if (-not $Script:UvExe) {
    Write-Host ""
    Write-CvcErr "Could not locate the package manager after install."
    Write-CvcInfo "Close & reopen your terminal, then re-run the install command."
    exit 1
}

function Invoke-Uv { param([Parameter(ValueFromRemainingArguments)]$a)
    & $Script:UvExe @a
}

# Ensure a Python is available (silent)
$pyOut = Invoke-Uv python list --only-installed 2>&1
if ($LASTEXITCODE -ne 0 -or -not ($pyOut -match '\d+\.\d+\.\d+')) {
    Write-CvcInfo "Installing Python runtime..."
    try { Invoke-Uv python install $CvcPinPy 2>&1 | Out-Null } catch {}
}

# ── Detect existing install ────────────────────────────────────────────────
$ExistingBefore = ""
try {
    $cvcCmd = Get-Command cvc -ErrorAction SilentlyContinue
    if ($cvcCmd) {
        $verOut = & cvc --version 2>$null
        if ($verOut -match '(\d+\.\d+\.\d+)') { $ExistingBefore = $Matches[1] }
    }
} catch {}

# ── Fetch latest version (CDN-staleness retry) ─────────────────────────────
function Get-LatestVersion {
    try {
        $nonce = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
        return (Invoke-RestMethod -Headers @{ "Cache-Control" = "no-cache" } "https://pypi.org/pypi/$PyPIName/json?_=$nonce").info.version
    } catch { return "" }
}
function Test-VersionGt($a, $b) {
    if (-not $a -or -not $b) { return $false }
    try { return ([version]$a -gt [version]$b) } catch { return $false }
}

$LatestVersion = Get-LatestVersion
if ($LatestVersion -and $ExistingBefore -and -not (Test-VersionGt $LatestVersion $ExistingBefore)) {
    Write-CvcInfo "Checking for latest version..."
    for ($i = 1; $i -le 6; $i++) {
        Start-Sleep -Seconds 5
        $newLatest = Get-LatestVersion
        if ($newLatest -and (Test-VersionGt $newLatest $ExistingBefore)) {
            $LatestVersion = $newLatest; break
        }
    }
}

# ── Status lines (parity with macOS) ───────────────────────────────────────
if ($ExistingBefore) {
    Write-CvcInfo "Found existing CVC v$ExistingBefore -> will replace"
} else {
    Write-CvcInfo "No existing CVC install found"
}
if ($LatestVersion) {
    Write-CvcInfo "Latest available: v$LatestVersion"
}

# Build the pinned spec. We use [string]::Format instead of double-quoted
# interpolation because "$PyPIName[all]" gets parsed by PowerShell as an
# array indexer (PS 5.1 evaluates "$var[all]" as $null since "all" is not
# an integer index). -f sidesteps that entirely.
$PinnedPackage = if ($LatestVersion) { ('{0}[all]=={1}' -f $PyPIName, $LatestVersion) } else { $PackageName }

# ── Purge old installs (silent) ────────────────────────────────────────────
$uvToolBinEarly = $null
try { $uvToolBinEarly = (Invoke-Uv tool dir --bin 2>&1).Trim() } catch {}
if (-not $uvToolBinEarly -or -not (Test-Path $uvToolBinEarly)) {
    $uvToolBinEarly = Join-Path $env:USERPROFILE ".local\bin"
}
$uvToolBinEarly = $uvToolBinEarly.TrimEnd("\").TrimEnd("/")

function Test-UvOwned ($path) {
    $norm = $path.TrimEnd("\").TrimEnd("/")
    return $norm.StartsWith($uvToolBinEarly, [System.StringComparison]::OrdinalIgnoreCase)
}

$seenPythons = @{}
$pathDirs = $env:PATH -split ";" | Where-Object { $_ -and (Test-Path $_ -ErrorAction SilentlyContinue) }
foreach ($dir in $pathDirs) {
    foreach ($exe in @("python.exe","python3.exe","python311.exe","python312.exe","python313.exe")) {
        $full = Join-Path $dir $exe
        if ((Test-Path $full) -and -not $seenPythons.ContainsKey($full)) {
            $seenPythons[$full] = $true
            try {
                $pkg = & $full -m pip show $PyPIName 2>&1 | Select-String "^Name"
                if ($pkg) { & $full -m pip uninstall $PyPIName -y 2>&1 | Out-Null }
            } catch {}
        }
    }
}

$condaExe = Get-Command conda -ErrorAction SilentlyContinue
if ($condaExe) {
    try { & conda run -n base pip uninstall $PyPIName -y 2>&1 | Out-Null } catch {}
    try { & conda remove -n base $PyPIName -y 2>&1 | Out-Null } catch {}
}

foreach ($dir in $pathDirs) {
    foreach ($stale in @("cvc.exe","cvc","cvc-script.py","cvc.cmd")) {
        $stalePath = Join-Path $dir $stale
        if ((Test-Path $stalePath) -and -not (Test-UvOwned $stalePath)) {
            try { Remove-Item $stalePath -Force -ErrorAction SilentlyContinue } catch {}
        }
    }
}

$condaRoots = @(
    "$env:USERPROFILE\miniconda3","$env:USERPROFILE\anaconda3",
    "$env:USERPROFILE\AppData\Local\miniconda3","$env:USERPROFILE\AppData\Local\anaconda3",
    "$env:ProgramData\miniconda3","$env:ProgramData\anaconda3",
    "C:\ProgramData\miniconda3","C:\ProgramData\anaconda3"
)
if ($env:CONDA_PREFIX) { $condaRoots += $env:CONDA_PREFIX }
foreach ($root in $condaRoots) {
    if (-not (Test-Path $root)) { continue }
    foreach ($subDir in @("Scripts","bin","envs\base\Scripts")) {
        foreach ($stale in @("cvc.exe","cvc","cvc-script.py","cvc.cmd")) {
            $stalePath = Join-Path (Join-Path $root $subDir) $stale
            if ((Test-Path $stalePath) -and (-not (Test-UvOwned $stalePath))) {
                try { Remove-Item $stalePath -Force -ErrorAction SilentlyContinue } catch {}
            }
        }
    }
}

try {
    Get-Command cvc -All -ErrorAction SilentlyContinue | ForEach-Object {
        $src = $_.Source
        if ($src -and (-not (Test-UvOwned $src)) -and (Test-Path $src)) {
            try { Remove-Item $src -Force -ErrorAction SilentlyContinue } catch {}
        }
    }
} catch {}

$toolList = (Invoke-Uv tool list 2>&1) | Out-String
$needsCleanup = $false
if ($toolList -match "(^|\s)$PyPIName(\s|@|$)") { $needsCleanup = $true }
if ($toolList -match "(?i)(malformed|invalid environment).*$PyPIName") { $needsCleanup = $true }
if ($toolList -match "(?i)$PyPIName.*(malformed|invalid environment)") { $needsCleanup = $true }

$uvToolRoot = $null
try { $uvToolRoot = (Invoke-Uv tool dir 2>&1 | Select-Object -First 1).Trim() } catch {}
if (-not $uvToolRoot -or -not (Test-Path $uvToolRoot)) {
    $uvToolRoot = Join-Path $env:APPDATA "uv\tools"
}
$toolDir = Join-Path $uvToolRoot $PyPIName
if (Test-Path $toolDir) { $needsCleanup = $true }

if ($needsCleanup) {
    try { Invoke-Uv tool uninstall $PyPIName 2>&1 | Out-Null } catch {}
    if (Test-Path $toolDir) {
        try { Remove-Item $toolDir -Recurse -Force -ErrorAction SilentlyContinue } catch {}
    }
}

# 1d-extra. Self-heal: if the uv tool venv is half-broken (pyvenv.cfg or
# entrypoint missing) the next install will fail with cryptic errors like
# "failed to locate pyvenv.cfg" or "No module named 'rich._unicode_data.*'".
# Detect that state and force-remove the tool dir with retry — uv's
# `tool uninstall` does NOT remove malformed venvs. This makes "cvc update"
# recoverable on Windows where the running cvc.exe holds a file lock.
#
# v2.92.10 — Two improvements over v2.92.8:
#   1. v2.92.8 retried Remove-Item 3× blind. If a parent cvc.exe or its
#      child python.exe was holding a file handle on Scripts\python.exe,
#      the retries just hammered the same handle and failed. v2.92.10
#      detects the lock-holder processes FIRST and stops them before
#      retrying.
#   2. If we still can't delete the dir, we recursively take ownership
#      and reset ACLs (icacls) so Remove-Item isn't blocked by inherited
#      deny ACEs from a previous install.
if (Test-Path $toolDir) {
    $pyvenvOnDisk   = Join-Path $toolDir "pyvenv.cfg"
    $entryExeOnDisk = Join-Path (Join-Path $toolDir "Scripts") "cvc.exe"
    $isBroken = $false
    if (-not (Test-Path $pyvenvOnDisk))   { $isBroken = $true }
    if (-not (Test-Path $entryExeOnDisk)) { $isBroken = $true }
    if ($isBroken) {
        Write-CvcInfo "Detected half-broken CVC install — cleaning up before reinstall"

        # ── v2.92.10 NEW: identify + stop lock-holder processes ──
        # If cvc.exe or any process whose exe lives under $toolDir is
        # running, Remove-Item on Scripts\ will fail with Access denied.
        $cvcExe = Join-Path $uvToolBinEarly "cvc.exe"
        $lockHolders = @()
        try {
            Get-Process -ErrorAction SilentlyContinue | Where-Object {
                $_.Path -and $_.Path.StartsWith($toolDir, [System.StringComparison]::OrdinalIgnoreCase)
            } | ForEach-Object { $lockHolders += $_ }
            Get-Process -ErrorAction SilentlyContinue | Where-Object {
                ($_.Path -and ($_.Path -ieq $cvcExe)) -or $_.ProcessName -ieq 'cvc'
            } | ForEach-Object {
                if ($lockHolders -notcontains $_) { $lockHolders += $_ }
            }
        } catch {}
        if ($lockHolders.Count -gt 0) {
            Write-CvcInfo "Stopping $($lockHolders.Count) lock-holder process(es) (graceful, then force-kill)…"
            foreach ($p in $lockHolders) {
                try { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue } catch {}
            }
            Start-Sleep -Seconds 3
            foreach ($p in $lockHolders) {
                if (Get-Process -Id $p.Id -ErrorAction SilentlyContinue) {
                    try { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue } catch {}
                }
            }
            Start-Sleep -Seconds 1
        }

        # ── v2.92.10 NEW: strip inherited deny ACLs ──
        # Sometimes a previous failed install leaves deny ACEs on
        # Scripts\ that block Remove-Item even after the process is
        # gone. Reset with icacls.
        try {
            & icacls.exe $toolDir /reset /T /C 2>&1 | Out-Null
        } catch {}

        # Retry up to 5 times — Windows file locks can hold for a moment
        # after the parent cvc.exe exits, and the OS can take a few
        # hundred ms to release the directory handle.
        $removed = $false
        for ($i = 0; $i -lt 5; $i++) {
            try {
                Remove-Item $toolDir -Recurse -Force -ErrorAction Stop
                $removed = $true
                break
            } catch {
                Start-Sleep -Milliseconds 800
            }
        }
        if (-not $removed) {
            Write-CvcWarn "Could not fully remove $toolDir — uv will overwrite what it can."
            Write-CvcInfo "If install still fails, run:  taskkill /F /IM cvc.exe /T"
        }
    }
}
# Clean up stale .old shims that previous failed installs left behind
foreach ($staleOld in @("cvc.exe.old","cvc-script.py.old")) {
    $p = Join-Path $uvToolBinEarly $staleOld
    if (Test-Path $p) {
        try { Remove-Item $p -Force -ErrorAction SilentlyContinue } catch {}
    }
}

# ── Install ────────────────────────────────────────────────────────────────
$cvcTarget = Join-Path $uvToolBinEarly "cvc.exe"
$cvcOld    = Join-Path $uvToolBinEarly "cvc.exe.old"
if (Test-Path $cvcTarget) {
    try {
        if (Test-Path $cvcOld) { Remove-Item $cvcOld -Force -ErrorAction SilentlyContinue }
        [System.IO.File]::Move($cvcTarget, $cvcOld)
    } catch {}
}

if ($LatestVersion) {
    Write-CvcInfo "Installing CVC v$LatestVersion..."
} else {
    Write-CvcInfo "Installing CVC (latest)..."
}

$installOut = Invoke-Uv tool install --force --refresh --python $CvcPinPy $PinnedPackage 2>&1
$uvExitCode = $LASTEXITCODE
$entrypointFail = $false
if ($uvExitCode -ne 0 -and $null -ne $uvExitCode) {
    $outStr = ($installOut | Out-String)
    if ($outStr -match "Failed to install entrypoint") {
        $entrypointFail = $true
    } else {
        Write-CvcInfo "Retrying with a clean cache..."
        try { Invoke-Uv cache clean $PyPIName 2>&1 | Out-Null } catch {}
        if (Test-Path $toolDir) {
            try { Remove-Item $toolDir -Recurse -Force -ErrorAction SilentlyContinue } catch {}
        }
        $installOut = Invoke-Uv tool install --force --refresh --python $CvcPinPy $PinnedPackage 2>&1
        $uvExitCode = $LASTEXITCODE
        if ($uvExitCode -ne 0 -and $null -ne $uvExitCode) {
            $outStr = ($installOut | Out-String)
            if ($outStr -match "Failed to install entrypoint") {
                $entrypointFail = $true
            } else {
                Write-CvcInfo "Retrying with latest version..."
                $installOut = Invoke-Uv tool install --force --refresh --python $CvcPinPy $PackageName 2>&1
                $uvExitCode = $LASTEXITCODE
            }
        }
    }
}
if ($uvExitCode -ne 0 -and $null -ne $uvExitCode -and -not $entrypointFail) {
    $outStr = ($installOut | Out-String)
    if ($outStr -match "Failed to install entrypoint") {
        $entrypointFail = $true
    } else {
        Write-Host ""
        Write-CvcErr "CVC installation failed."
        Write-CvcInfo "Open a new terminal and re-run the install command."
        # v2.92.10 - Surface the actual uv error so users can
        # diagnose without digging through logs. Without this,
        # the only feedback they got was "installation failed"
        # which is useless for anyone troubleshooting.
        Write-Host ""
        Write-Host "${CVC_DIM}  uv output (last 60 lines):${RESET}"
        $tail = ($installOut | Out-String) -split "`n"
        $tailShown = $tail | Select-Object -Last 60
        foreach ($line in $tailShown) {
            Write-Host "    ${CVC_DIM}${line}${RESET}"
        }
        # v2.92.10 NEW: actionable next-steps the user can run
        # without having to open a ticket.
        Write-Host ""
        Write-Host "${CVC_DIM}  Common causes:${RESET}"
        Write-Host "    ${CVC_DIM}- Antivirus / Defender is blocking uv from creating the tool venv${RESET}"
        Write-Host "    ${CVC_DIM}- A running cvc.exe / python.exe is holding a file lock on the tool dir${RESET}"
        Write-Host "    ${CVC_DIM}- PyPI is unreachable or rate-limiting (try again in 60s)${RESET}"
        Write-Host "    ${CVC_DIM}- Network proxy blocks astral.sh or pypi.org${RESET}"
        Write-Host ""
        Write-Host "${CVC_DIM}  Recovery commands:${RESET}"
        Write-Host "    ${CVC_DIM}taskkill /F /IM cvc.exe /T${RESET}"
        Write-Host "    ${CVC_DIM}taskkill /F /IM python.exe /T${RESET}"
        Write-Host "    ${CVC_DIM}irm https://jaimeena.com/cvc/install.ps1 | iex${RESET}"
        exit 1
    }
}
if (Test-Path $cvcOld) {
    try { Remove-Item $cvcOld -Force -ErrorAction SilentlyContinue } catch {}
}
if ($entrypointFail) {
    $srcExe = Join-Path (Join-Path $env:APPDATA "uv\tools\$PyPIName\Scripts") "cvc.exe"
    if (Test-Path $srcExe) {
        try { Copy-Item $srcExe $cvcTarget -Force -ErrorAction SilentlyContinue } catch {}
    }
}

Write-CvcOk "CVC installed"

# ── PATH wiring ────────────────────────────────────────────────────────────
$uvToolBin = $uvToolBinEarly
if (-not (Test-Path $uvToolBin)) {
    New-Item -ItemType Directory -Path $uvToolBin -Force | Out-Null
}
$userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if (-not $userPath) { $userPath = "" }
$pathParts = $userPath -split ";" | Where-Object { $_ -and $_ -ne $uvToolBin }
$newUserPath = ($uvToolBin + ";" + ($pathParts -join ";")).TrimEnd(";")
[System.Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
$env:PATH = $uvToolBin + ";" + (($env:PATH -split ";" | Where-Object { $_ -and $_ -ne $uvToolBin }) -join ";")
try { Invoke-Uv tool update-shell 2>&1 | Out-Null } catch {}

Write-CvcOk "PATH updated"

# ── Verify ─────────────────────────────────────────────────────────────────
$installedVersion = ""
$cvcExe = Get-Command cvc -ErrorAction SilentlyContinue
if (-not $cvcExe -and (Test-Path $cvcTarget)) { $cvcExe = @{ Source = $cvcTarget } }
if ($cvcExe) {
    try {
        $verLine = & $cvcExe.Source --version 2>&1 | Select-Object -First 1
        $installedVersion = ($verLine -replace '[^0-9.]','').Trim('.')
    } catch {}
}

Write-Host ""
$vStr = if ($installedVersion) { " v$installedVersion" } else { "" }
Write-Host "$CVC_RED$BOLD* ${CVC_BRIGHT}CVC${vStr}${CVC_RED} installed successfully.$RESET"

if ($LatestVersion -and $installedVersion -and ($installedVersion -ne $LatestVersion)) {
    Write-CvcWarn "Expected v$LatestVersion, got v$installedVersion."
    Write-CvcWarn "Open a new terminal — PATH changes take effect in new sessions."
}

Write-Host ""
Write-Host "${CVC_DIM}Run ${RESET}${CVC_BRIGHT}${BOLD}cvc${RESET}${CVC_DIM} to start. (If 'cvc' is not found, open a new terminal once.)${RESET}"
Write-Host ""
