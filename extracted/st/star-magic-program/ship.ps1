# ship.ps1 - Star-Magic-Program band ship (gate -> commit -> tag -> push)
# Regenerated 2026-07-29: parser-safe version extraction (no quote/bracket regex).

$ErrorActionPreference = "Stop"

Write-Host "=== ship.ps1 - Star-Magic-Program band ship ===" -ForegroundColor Cyan

# --- 0. Clear Windows git locks ---
Remove-Item -Force .git\index.lock -ErrorAction SilentlyContinue
Remove-Item -Force .git\COMMIT_EDITMSG -ErrorAction SilentlyContinue

# --- 1. Read version from pyproject.toml (parser-safe: split on quote char) ---
$DQ = [char]34
$verLine = Get-Content pyproject.toml | Where-Object { $_.StartsWith("version") } | Select-Object -First 1
if (-not $verLine) { Write-Error "Cannot read version from pyproject.toml"; exit 1 }
$version = $verLine.Split($DQ)[1]
$tag = "v$version"
Write-Host "Version: $version  (tag: $tag)"

# --- 2. Refuse existing tag ---
$existing = git tag -l $tag
if ($existing) { Write-Error "Tag $tag already exists locally. Bump version first."; exit 1 }

# --- 2b. TAG-CHAIN CONTINUITY pre-flight (v0.413.0 lesson, 2026-09-03) ---
# Every ledger version except the current prep must already have a tag.
$ledger = Get-Content UNIFIED_REGISTRY_VERSION.txt | Where-Object { $_.StartsWith("v") }
$prior = $ledger | Select-Object -SkipLast 1
$gapAuthorized = @("v0.413.0")  # THE USER MANUAL BAND - prepared, silent ship failure, published inside v0.414.0
foreach ($lv in $prior) {
    if (-not (git tag -l $lv) -and ($gapAuthorized -notcontains $lv)) {
        Write-Error "TAG-CHAIN GAP: ledger version $lv has no git tag. A prior ship failed silently. Refusing to ship on a broken chain."; exit 1
    }
}

# --- 3. Fidelity gate ---
Write-Host "=== Fidelity gate ===" -ForegroundColor Cyan
python uqff_fidelity_tests.py
if ($LASTEXITCODE -ne 0) { Write-Error "GATE RED - refusing to ship."; exit 1 }

# --- 4. Commit message from SHIP_MESSAGE.txt ---
if (-not (Test-Path SHIP_MESSAGE.txt)) { Write-Error "SHIP_MESSAGE.txt missing."; exit 1 }

# --- 5. Stage + commit ---
git add -A
$staged = git diff --cached --name-only
if (-not $staged) { Write-Error "Nothing staged - refusing empty ship."; exit 1 }
git commit -F SHIP_MESSAGE.txt

# --- 6. Verify HEAD advanced ---
$headMsg = git log -1 --format=%s
Write-Host "HEAD: $headMsg"
if (-not $headMsg.StartsWith($tag)) {
    Write-Error "COMMIT DID NOT LAND - HEAD subject does not start with $tag. Refusing to tag."; exit 1
}

# --- 7. Tag AFTER commit; verify tag == HEAD ---
git tag -a $tag -m $headMsg
$tagSha  = git rev-parse ($tag + "^0")
$headSha = git rev-parse HEAD
if ($tagSha -ne $headSha) { Write-Error "TAG/HEAD MISMATCH - aborting push."; exit 1 }

# --- 8. Push commit then tag ---
git push origin master
git push origin $tag

# --- 9. Verify the ship actually landed (v0.413.0 lesson) ---
$remoteTag = git ls-remote origin ("refs/tags/" + $tag)
if (-not $remoteTag) { Write-Error "REMOTE TAG MISSING after push - the ship did NOT land. Do not trust this run."; exit 1 }
$localHead = git rev-parse HEAD
if (-not ($remoteTag.StartsWith($localHead.Substring(0,7)) -or $remoteTag.Contains($localHead))) {
    Write-Host "WARNING: remote tag SHA does not obviously match local HEAD - verify manually." -ForegroundColor Yellow
}

Write-Host "=== SHIPPED $tag (remote tag verified) ===" -ForegroundColor Green
Write-Host "Watch: https://github.com/Daniel8Murphy0007/Star-Magic-Program/actions"
Write-Host "PyPI:  https://pypi.org/project/star-magic-program/$version/"
