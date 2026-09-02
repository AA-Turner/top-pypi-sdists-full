#!/usr/bin/env pwsh
# Create a new feature
[CmdletBinding()]
param(
    [switch]$Json,
    [string]$ShortName,
    [int]$Issue = 0,
    [int]$Number = 0,
    [int]$Parent = 0,
    [switch]$Flat,
    [switch]$Help,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$FeatureDescription
)
$ErrorActionPreference = 'Stop'

# Show help if requested
if ($Help) {
    Write-Host "Usage: ./create-new-feature.ps1 [-Json] [-ShortName <name>] [-Issue N] [-Parent P] [-Flat] <feature description>"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Json               Output in JSON format"
    Write-Host "  -ShortName <name>   Provide a custom short name (2-4 words) for the branch"
    Write-Host "  -Issue N            GitHub issue number to use as directory/branch prefix"
    Write-Host "  -Number N           Deprecated alias for -Issue"
    Write-Host "  -Parent P           Explicit parent issue number (overrides hierarchy detection)"
    Write-Host "  -Flat               Force flat directory creation (ignore hierarchy)"
    Write-Host "  -Help               Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  ./create-new-feature.ps1 -Issue 1175 'Plan phase fails for large specs' -ShortName 'plan-phase-fails-large'"
    Write-Host "  ./create-new-feature.ps1 -Issue 42 'Add user authentication system'"
    Write-Host "  ./create-new-feature.ps1 -Issue 200 -Parent 100 'Child feature'"
    Write-Host "  ./create-new-feature.ps1 -Issue 200 -Flat 'Force flat layout'"
    exit 0
}

# Validate -Parent when -Flat is not set
if ($Parent -ne 0 -and -not $Flat) {
    if ($Parent -lt 1) {
        Write-Error "[specify] Error: -Parent requires a positive integer (got $Parent)"
        exit 1
    }
}

# Validate: -Parent requires -Issue when -Flat is not set
if ($Parent -ne 0 -and -not $explicitIssue -and -not $Flat) {
    # This will be checked after $explicitIssue is set below
    $parentRequiresIssueCheck = $true
} else {
    $parentRequiresIssueCheck = $false
}

# Check if feature description provided
if (-not $FeatureDescription -or $FeatureDescription.Count -eq 0) {
    Write-Error "Usage: ./create-new-feature.ps1 [-Json] [-ShortName <name>] [-Issue N] <feature description>"
    exit 1
}

$featureDesc = ($FeatureDescription -join ' ').Trim()

# Resolve repository root. Prefer git information when available, but fall back
# to searching for repository markers so the workflow still functions in repositories that
# were initialized with --no-git.
function Find-RepositoryRoot {
    param(
        [string]$StartDir,
        [string[]]$Markers = @('.git', '.specify')
    )
    $current = Resolve-Path $StartDir
    while ($true) {
        foreach ($marker in $Markers) {
            if (Test-Path (Join-Path $current $marker)) {
                return $current
            }
        }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current) {
            # Reached filesystem root without finding markers
            return $null
        }
        $current = $parent
    }
}

function Get-HighestNumberFromSpecs {
    param([string]$SpecsDir)
    
    $highest = 0
    if (Test-Path $SpecsDir) {
        Get-ChildItem -Path $SpecsDir -Directory | ForEach-Object {
            # Only match legacy 3-digit prefixed directories (e.g., 001-feature)
            # to avoid picking up issue-number dirs (e.g., 1175-feature)
            if ($_.Name -match '^\d{3}-') {
                $num = [int]($_.Name -replace '^(\d{3}).*', '$1')
                if ($num -gt $highest) { $highest = $num }
            }
        }
    }
    return $highest
}

function Get-HighestNumberFromBranches {
    param()
    
    $highest = 0
    try {
        $branches = git branch -a 2>$null
        if ($LASTEXITCODE -eq 0) {
            foreach ($branch in $branches) {
                # Clean branch name: remove leading markers and remote prefixes
                $cleanBranch = $branch.Trim() -replace '^\*?\s+', '' -replace '^remotes/[^/]+/', ''
                
                # Extract feature number if branch matches legacy pattern ###-*
                if ($cleanBranch -match '^\d{3}-') {
                    $num = [int]($cleanBranch -replace '^(\d{3}).*', '$1')
                    if ($num -gt $highest) { $highest = $num }
                }
            }
        }
    } catch {
        # If git command fails, return 0
        Write-Verbose "Could not check Git branches: $_"
    }
    return $highest
}

function Get-NextBranchNumber {
    param(
        [string]$SpecsDir
    )

    # Fetch all remotes to get latest branch info (suppress errors if no remotes)
    try {
        git fetch --all --prune 2>$null | Out-Null
    } catch {
        # Ignore fetch errors
    }

    # Get highest number from ALL branches (not just matching short name)
    $highestBranch = Get-HighestNumberFromBranches

    # Get highest number from ALL specs (not just matching short name)
    $highestSpec = Get-HighestNumberFromSpecs -SpecsDir $SpecsDir

    # Take the maximum of both
    $maxNum = [Math]::Max($highestBranch, $highestSpec)

    # Return next number
    return $maxNum + 1
}

function ConvertTo-CleanBranchName {
    param([string]$Name)
    
    return $Name.ToLower() -replace '[^a-z0-9]', '-' -replace '-{2,}', '-' -replace '^-', '' -replace '-$', ''
}
$fallbackRoot = (Find-RepositoryRoot -StartDir $PSScriptRoot)
if (-not $fallbackRoot) {
    Write-Error "Error: Could not determine repository root. Please run this script from within the repository."
    exit 1
}

try {
    $repoRoot = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0) {
        $hasGit = $true
    } else {
        throw "Git not available"
    }
} catch {
    $repoRoot = $fallbackRoot
    $hasGit = $false
}

Set-Location $repoRoot

$specsDir = Join-Path $repoRoot 'specs'
New-Item -ItemType Directory -Path $specsDir -Force | Out-Null

# Function to generate branch name with stop word filtering and length filtering
function Get-BranchName {
    param([string]$Description)
    
    # Common stop words to filter out
    $stopWords = @(
        'i', 'a', 'an', 'the', 'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with', 'from',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall',
        'this', 'that', 'these', 'those', 'my', 'your', 'our', 'their',
        'want', 'need', 'add', 'get', 'set'
    )
    
    # Convert to lowercase and extract words (alphanumeric only)
    $cleanName = $Description.ToLower() -replace '[^a-z0-9\s]', ' '
    $words = $cleanName -split '\s+' | Where-Object { $_ }
    
    # Filter words: remove stop words and words shorter than 3 chars (unless they're uppercase acronyms in original)
    $meaningfulWords = @()
    foreach ($word in $words) {
        # Skip stop words
        if ($stopWords -contains $word) { continue }
        
        # Keep words that are length >= 3 OR appear as uppercase in original (likely acronyms)
        if ($word.Length -ge 3) {
            $meaningfulWords += $word
        } elseif ($Description -match "\b$($word.ToUpper())\b") {
            # Keep short words if they appear as uppercase in original (likely acronyms)
            $meaningfulWords += $word
        }
    }
    
    # If we have meaningful words, use first 3-4 of them
    if ($meaningfulWords.Count -gt 0) {
        $maxWords = if ($meaningfulWords.Count -eq 4) { 4 } else { 3 }
        $result = ($meaningfulWords | Select-Object -First $maxWords) -join '-'
        return $result
    } else {
        # Fallback to original logic if no meaningful words found
        $result = ConvertTo-CleanBranchName -Name $Description
        $fallbackWords = ($result -split '-') | Where-Object { $_ } | Select-Object -First 3
        return [string]::Join('-', $fallbackWords)
    }
}

# Generate branch name
if ($ShortName) {
    # Use provided short name, just clean it up
    $branchSuffix = ConvertTo-CleanBranchName -Name $ShortName
} else {
    # Generate from description with smart filtering
    $branchSuffix = Get-BranchName -Description $featureDesc
}

# Determine feature number: -Issue takes priority, then -Number (deprecated), then auto-detect
$effectiveNumber = 0
$explicitIssue = $false
if ($Issue -ne 0) {
    if ($Issue -lt 1) {
        Write-Error "Error: -Issue requires a positive integer (got $Issue)"
        exit 1
    }
    $effectiveNumber = $Issue
    $explicitIssue = $true
} elseif ($Number -ne 0) {
    if ($Number -lt 1) {
        Write-Error "Error: -Number requires a positive integer (got $Number)"
        exit 1
    }
    $effectiveNumber = $Number
    $explicitIssue = $true
}

if ($effectiveNumber -eq 0) {
    if ($hasGit) {
        # Legacy fallback: auto-detect next sequential number
        $effectiveNumber = Get-NextBranchNumber -SpecsDir $specsDir
    } else {
        # Fall back to local directory check
        $effectiveNumber = (Get-HighestNumberFromSpecs -SpecsDir $specsDir) + 1
    }
}

# Validate: -Parent requires -Issue when -Flat is not set (deferred check)
if ($parentRequiresIssueCheck -and -not $explicitIssue) {
    Write-Error "[specify] Error: -Parent requires -Issue to be specified (hierarchy nesting requires an explicit issue number)"
    exit 1
}

# When -Issue was explicitly provided, use the number as-is (no zero-padding).
# When the number was auto-detected from legacy 3-digit dirs/branches, preserve
# the 3-digit zero-padded format so the new branch/dir will be picked up by
# subsequent legacy detection runs.
if ($explicitIssue) {
    $featureNum = "$effectiveNumber"
} else {
    $featureNum = "{0:D3}" -f $effectiveNumber
}
$branchName = "$featureNum-$branchSuffix"

# GitHub enforces a 244-byte limit on branch names
# Validate and truncate if necessary
$maxBranchLength = 244
if ($branchName.Length -gt $maxBranchLength) {
    # Calculate how much we need to trim from suffix
    # Account for: feature number (variable length) + hyphen (1)
    $prefixLength = $featureNum.Length + 1
    $maxSuffixLength = $maxBranchLength - $prefixLength
    
    # Truncate suffix
    $truncatedSuffix = $branchSuffix.Substring(0, [Math]::Min($branchSuffix.Length, $maxSuffixLength))
    # Remove trailing hyphen if truncation created one
    $truncatedSuffix = $truncatedSuffix -replace '-$', ''
    
    $originalBranchName = $branchName
    $branchName = "$featureNum-$truncatedSuffix"
    
    Write-Warning "[specify] Branch name exceeded GitHub's 244-byte limit"
    Write-Warning "[specify] Original: $originalBranchName ($($originalBranchName.Length) bytes)"
    Write-Warning "[specify] Truncated to: $branchName ($($branchName.Length) bytes)"
}

if ($hasGit) {
    try {
        git checkout -b $branchName | Out-Null
    } catch {
        Write-Warning "Failed to create git branch: $branchName"
    }
} else {
    Write-Warning "[specify] Warning: Git repository not detected; skipped branch creation for $branchName"
}

# ============================================================================
# Hierarchy-aware directory creation
# ============================================================================

function Find-PythonExe {
    # Returns the first available Python 3 executable name, or $null if none found.
    foreach ($candidate in @('python3', 'python', 'py')) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) {
            return $candidate
        }
    }
    return $null
}

function Resolve-RepoSlug {
    # Try gh CLI first
    try {
        $slug = gh repo view --json nameWithOwner -q '.nameWithOwner' 2>$null
        if ($slug -and $slug -match '/') {
            return $slug.Trim()
        }
    } catch {}
    # Fall back to parsing git remote
    if ($hasGit) {
        try {
            $remoteUrl = git remote get-url origin 2>$null
            if ($remoteUrl) {
                if ($remoteUrl -match '[:/]([^/]+/[^/]+?)(?:\.git)?$') {
                    return $Matches[1]
                }
            }
        } catch {}
    }
    return $null
}

function Invoke-HierarchyDetector {
    param([int]$IssueNum, [string]$RepoSlug)
    
    $result = @{ Status = 'error'; Parent = $null; Level = $null; Title = $null }
    
    if (-not $RepoSlug) { return $result }
    
    $pythonExe = Find-PythonExe
    if (-not $pythonExe) { return $result }
    
    try {
        $detectorStderr = [System.IO.Path]::GetTempFileName()
        $output = & $pythonExe -m agentic_devtools.cli.speckit.detect_parent_cli --issue $IssueNum --repo $RepoSlug --timeout 10 2>$detectorStderr
        if ($LASTEXITCODE -ne 0) {
            if (Test-Path $detectorStderr) {
                $errContent = Get-Content -Path $detectorStderr -Raw -ErrorAction SilentlyContinue
                if ($errContent) { Write-Warning "[specify] Hierarchy detector: $errContent" }
                Remove-Item $detectorStderr -Force -ErrorAction SilentlyContinue
            }
            return $result
        }
        Remove-Item $detectorStderr -Force -ErrorAction SilentlyContinue
        
        foreach ($line in $output) {
            if ($line -match '^status=(.+)$') { $result.Status = $Matches[1] }
            elseif ($line -match '^parent=(.+)$') { $val = $Matches[1]; if ($val -ne 'null') { $result.Parent = $val } }
            elseif ($line -match '^level=(.+)$') { $val = $Matches[1]; if ($val -ne 'null') { $result.Level = $val } }
            elseif ($line -match '^title=(.+)$') { $val = $Matches[1]; if ($val -ne 'null') { $result.Title = $val } }
        }
    } catch {
        # Detection failed
    }
    
    return $result
}

function Find-ParentDir {
    param([string]$SpecsDir, [string]$ParentKey)
    
    $matches = @()
    Get-ChildItem -Path $SpecsDir -Directory -Recurse | Where-Object {
        -not ($_.Attributes -band [System.IO.FileAttributes]::ReparsePoint)
    } | ForEach-Object {
        if ($_.Name -eq $ParentKey -or $_.Name -match "^${ParentKey}-") {
            $matches += $_.FullName
        }
    }
    
    if ($matches.Count -eq 0) { return @{ Path = $null; Code = 1 } }
    if ($matches.Count -eq 1) { return @{ Path = $matches[0]; Code = 0 } }
    
    Write-Error "[specify] Error: Multiple spec directories found matching parent '$ParentKey': $($matches -join ', ')"
    return @{ Path = $null; Code = 2 }
}

function Get-NestingDepth {
    param([string]$SpecsDir, [string]$TargetDir)
    
    $relPath = $TargetDir.Substring($SpecsDir.Length + 1)
    $depth = ($relPath.Split([System.IO.Path]::DirectorySeparatorChar) | Where-Object { $_ }).Count
    return $depth
}

# Initialize hierarchy output variables
$parentSpecDir = $null
$hierarchyLevel = $null
$nestedCreation = $false
$resolvedParent = ''
$detectedTitle = ''
$detectedLevel = ''

$template = Join-Path $repoRoot '.specify/presets/agdt-templates/templates/spec-template.md'

if ($explicitIssue -and -not $Flat) {
    $repoSlug = Resolve-RepoSlug
    
    if ($Parent -ne 0) {
        # Fail fast: explicit -Parent requires Python to update the parent
        # hierarchy.yml; there is no fallback for explicit nested mode.
        $pythonExeCheck = Find-PythonExe
        if (-not $pythonExeCheck) {
            Write-Error "[specify] Error: -Parent $Parent was specified but no Python executable was found on PATH. Install Python 3 or omit -Parent to use flat directory creation."
            exit 1
        }
        $resolvedParent = "$Parent"
        # Still invoke detector for level/title (but ignore parent result)
        $detection = Invoke-HierarchyDetector -IssueNum $effectiveNumber -RepoSlug $repoSlug
        if ($detection.Status -eq 'ok') {
            $detectedTitle = $detection.Title
            $detectedLevel = $detection.Level
        }
        $nestedCreation = $true
    } else {
        # Try hierarchy detection
        $detection = Invoke-HierarchyDetector -IssueNum $effectiveNumber -RepoSlug $repoSlug
        if ($detection.Status -eq 'ok') {
            if ($detection.Parent) {
                $resolvedParent = $detection.Parent
                $detectedTitle = $detection.Title
                $detectedLevel = $detection.Level
                $nestedCreation = $true
            }
        } else {
            Write-Warning "[specify] Warning: Hierarchy detection failed; falling back to flat directory creation"
        }
    }
    
    if ($detectedLevel) {
        $hierarchyLevel = $detectedLevel
    }
}

if ($nestedCreation -and $resolvedParent) {
    # Detect the *parent* issue's own title and level for directory naming and
    # hierarchy.yml creation.  $detectedTitle currently holds the child issue's
    # title from the earlier detection call, so we re-invoke the detector for the
    # parent issue number, save the results, then restore the child values.
    $parentDetectedTitle = ''
    $parentDetectedLevel = 'epic'
    if ($repoSlug) {
        $savedChildTitle = $detectedTitle
        $savedChildLevel = $detectedLevel
        $parentIssueNum = 0
        if ([int]::TryParse($resolvedParent, [ref]$parentIssueNum)) {
            $parentDetection = Invoke-HierarchyDetector -IssueNum $parentIssueNum -RepoSlug $repoSlug
            if ($parentDetection.Status -eq 'ok') {
                $parentDetectedTitle = $parentDetection.Title
                $parentDetectedLevel = if ($parentDetection.Level) { $parentDetection.Level } else { 'epic' }
            }
        }
        $detectedTitle = $savedChildTitle
        $detectedLevel = $savedChildLevel
    }

    # Find parent directory
    $parentResult = Find-ParentDir -SpecsDir $specsDir -ParentKey $resolvedParent
    
    if ($parentResult.Code -eq 2) {
        exit 1
    }
    
    $parentDir = $parentResult.Path
    
    if (-not $parentDir -or -not (Test-Path $parentDir)) {
        # Parent dir doesn't exist - create at top level using the parent's own title
        if ($parentDetectedTitle) {
            $parentSlug = ConvertTo-CleanBranchName -Name $parentDetectedTitle
            $parentDir = Join-Path $specsDir "${resolvedParent}-${parentSlug}"
        } else {
            $parentDir = Join-Path $specsDir $resolvedParent
        }
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
        if (Test-Path $template) {
            Copy-Item $template (Join-Path $parentDir 'spec.md') -Force
        } else {
            New-Item -ItemType File -Path (Join-Path $parentDir 'spec.md') | Out-Null
        }
    }
    
    # Check depth enforcement (max 3 levels)
    $depth = Get-NestingDepth -SpecsDir $specsDir -TargetDir $parentDir
    if ($depth -ge 3) {
        Write-Warning "[specify] Warning: Maximum nesting depth (3) would be exceeded; falling back to flat directory creation"
        $nestedCreation = $false
    }
}

if ($nestedCreation -and $resolvedParent) {
    # Create child directory with issue-key-only naming
    $featureDir = Join-Path $parentDir $featureNum
    New-Item -ItemType Directory -Path $featureDir -Force | Out-Null
    
    # Create spec.md
    $specFile = Join-Path $featureDir 'spec.md'
    if (Test-Path $template) {
        Copy-Item $template $specFile -Force
    } else {
        New-Item -ItemType File -Path $specFile | Out-Null
    }
    
    # Create child hierarchy.yml
    $childTitle = if ($detectedTitle) { $detectedTitle } else { $featureDesc }
    $childLevel = if ($detectedLevel) { $detectedLevel } else { 'task' }
    # Escape single quotes for YAML single-quoted scalars (' → '')
    $escapedChildTitle = $childTitle -replace "'", "''"
    $hierarchyContent = @"
title: '$escapedChildTitle'
level: $childLevel
parent: '$resolvedParent'
children: []
processed_at: null
"@
    Set-Content -Path (Join-Path $featureDir 'hierarchy.yml') -Value $hierarchyContent -Encoding utf8
    
    # Update parent hierarchy.yml
    $parentHierarchyFile = Join-Path $parentDir 'hierarchy.yml'
    $lockFile = Join-Path $parentDir '.hierarchy.yml.lock'
    
    # Attempt lock (simple retry with timeout for PowerShell)
    $lockAcquired = $false
    $lockStream = $null
    $startTime = Get-Date
    
    while (-not $lockAcquired) {
        try {
            $lockStream = [System.IO.File]::Open($lockFile, [System.IO.FileMode]::OpenOrCreate, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
            $lockAcquired = $true
        } catch {
            if (((Get-Date) - $startTime).TotalSeconds -ge 5) {
                Write-Error "[specify] Error: Could not acquire lock on $lockFile (timeout after 5s)"
                exit 1
            }
            Start-Sleep -Milliseconds 100
        }
    }
    
    try {
        # Create parent hierarchy.yml if missing, using the parent issue's own title/level
        if (-not (Test-Path $parentHierarchyFile)) {
            $pTitle = if ($parentDetectedTitle) { $parentDetectedTitle } else { "Issue $resolvedParent" }
            $pLevel = if ($parentDetectedLevel) { $parentDetectedLevel } else { 'epic' }
            # Escape single quotes for YAML single-quoted scalars (' → '')
            $escapedPTitle = $pTitle -replace "'", "''"
            $parentContent = @"
title: '$escapedPTitle'
level: $pLevel
parent: null
children: []
processed_at: null
"@
            Set-Content -Path $parentHierarchyFile -Value $parentContent -Encoding utf8
        }
        
        # Check idempotency and append child
        $content = Get-Content -Path $parentHierarchyFile -Raw -Encoding utf8
        if ($content -notmatch "key: '$featureNum'" -and $content -notmatch "key: `"$featureNum`"") {
            # Use Python for safe YAML update - pass values via env vars to avoid injection
            $pythonExe = Find-PythonExe
            if ($pythonExe) {
                $env:_HIER_FILE = $parentHierarchyFile
                $env:_CHILD_KEY = $featureNum
                $env:_CHILD_TITLE = $childTitle
                $pyScript = @"
import os, sys, yaml, tempfile
from pathlib import Path

hierarchy_file = Path(os.environ['_HIER_FILE'])
child_key = os.environ['_CHILD_KEY']
child_title = os.environ['_CHILD_TITLE']
child_order = int(child_key) if child_key.isdigit() else 0

data = yaml.safe_load(hierarchy_file.read_text(encoding='utf-8'))
if data is None:
    data = {}

if 'children' not in data or data['children'] is None:
    data['children'] = []

for child in data['children']:
    if str(child.get('key', '')) == child_key:
        sys.exit(0)

data['children'].append({'key': child_key, 'title': child_title, 'order': child_order})

tmp_fd, tmp_path = tempfile.mkstemp(dir=str(hierarchy_file.parent), suffix='.yml.tmp')
try:
    with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    os.replace(tmp_path, str(hierarchy_file))
except:
    os.unlink(tmp_path)
    raise
"@
                & $pythonExe -c $pyScript
                $pyExitCode = $LASTEXITCODE
                # Clean up env vars
                Remove-Item Env:\_HIER_FILE -ErrorAction SilentlyContinue
                Remove-Item Env:\_CHILD_KEY -ErrorAction SilentlyContinue
                Remove-Item Env:\_CHILD_TITLE -ErrorAction SilentlyContinue
                if ($pyExitCode -ne 0) {
                    Write-Error "[specify] Error: Python failed to update parent hierarchy.yml (exit code $pyExitCode); the child was created but the parent hierarchy.yml was not updated"
                    exit 1
                }
            } else {
                Write-Warning "[specify] Warning: No Python executable found; skipping parent hierarchy.yml child append"
            }
        }
    } finally {
        if ($lockStream) {
            $lockStream.Close()
            $lockStream.Dispose()
        }
    }
    
    $parentSpecDir = $parentDir
} else {
    # Flat directory creation (original behavior)
    $featureDir = Join-Path $specsDir $branchName
    New-Item -ItemType Directory -Path $featureDir -Force | Out-Null
    
    $specFile = Join-Path $featureDir 'spec.md'
    if (Test-Path $template) { 
        Copy-Item $template $specFile -Force 
    } else { 
        New-Item -ItemType File -Path $specFile | Out-Null 
    }
}

# Set the SPECIFY_FEATURE environment variable for the current session
$env:SPECIFY_FEATURE = $branchName

if ($Json) {
    $obj = [PSCustomObject]@{ 
        BRANCH_NAME = $branchName
        SPEC_FILE = $specFile
        FEATURE_NUM = $featureNum
        HAS_GIT = $hasGit
        PARENT_SPEC_DIR = $parentSpecDir
        HIERARCHY_LEVEL = $hierarchyLevel
    }
    $obj | ConvertTo-Json -Compress
} else {
    Write-Output "BRANCH_NAME: $branchName"
    Write-Output "SPEC_FILE: $specFile"
    Write-Output "FEATURE_NUM: $featureNum"
    Write-Output "HAS_GIT: $hasGit"
    Write-Output "PARENT_SPEC_DIR: $(if ($parentSpecDir) { $parentSpecDir } else { 'null' })"
    Write-Output "HIERARCHY_LEVEL: $(if ($hierarchyLevel) { $hierarchyLevel } else { 'null' })"
    Write-Output "SPECIFY_FEATURE environment variable set to: $branchName"
}
