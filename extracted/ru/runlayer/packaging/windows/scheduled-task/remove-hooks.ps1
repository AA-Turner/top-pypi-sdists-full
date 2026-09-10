#Requires -Version 5.1
# AI Watch hook cleanup for true MSI uninstall. Intended to run as LocalSystem.
# Every operation is best-effort and the script entrypoint always exits zero.

[CmdletBinding()]
param()

$script:RunlayerLogFile = "C:\ProgramData\Runlayer\Logs\scheduled-task.log"
$script:RunlayerBackupRoot = "C:\ProgramData\Runlayer\Logs\hook-backups"
$script:RunlayerBackupSessionRoot = $null
$script:RunlayerMaxFileBytes = 4 * 1024 * 1024
$script:RunlayerMaxJsonSpanNodes = 10000
$script:RunlayerOwnedClineMarker = (
    "# runlayer-owned Cline hook {0} safe to delete" -f ([char]0x2014)
)
$script:RunlayerIgnoreMarkerStart = "# >>> Runlayer managed - do not edit >>>"
$script:RunlayerIgnoreMarkerEnd = "# <<< Runlayer managed <<<"

function Set-RunlayerHookCleanupContext {
    param(
        [Parameter(Mandatory = $true)][string]$BackupRoot,
        [Parameter(Mandatory = $true)][string]$LogFile
    )

    $script:RunlayerBackupRoot = $BackupRoot
    $script:RunlayerBackupSessionRoot = $null
    $script:RunlayerLogFile = $LogFile
}

function Write-RunlayerHookCleanupLog {
    param([string]$Message)

    try {
        $directory = Split-Path -Parent $script:RunlayerLogFile
        if (-not (Test-Path -LiteralPath $directory)) {
            New-Item -ItemType Directory -Path $directory -Force | Out-Null
        }
        $line = "{0} [remove-hooks] {1}" -f (Get-Date -Format "o"), $Message
        Add-Content -LiteralPath $script:RunlayerLogFile -Value $line `
            -ErrorAction SilentlyContinue
    } catch {
        # Uninstall must not depend on logging.
    }
}

function Join-RunlayerPath {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string[]]$Parts
    )

    $result = $Root
    foreach ($part in $Parts) {
        $result = Join-Path $result $part
    }
    return $result
}

function Test-RunlayerPathSafe {
    param([Parameter(Mandatory = $true)][string]$Path)

    try {
        $current = [System.IO.Path]::GetFullPath($Path)
        while (-not [string]::IsNullOrEmpty($current)) {
            if (Test-Path -LiteralPath $current) {
                $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
                if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                    return $false
                }
                if ($item.PSObject.Properties["LinkType"] -and $null -ne $item.LinkType) {
                    return $false
                }
            }

            $parent = Split-Path -Parent $current
            if ([string]::IsNullOrEmpty($parent) -or $parent -eq $current) {
                break
            }
            $current = $parent
        }
        return $true
    } catch {
        return $false
    }
}

function ConvertFrom-RunlayerTextBytes {
    param([Parameter(Mandatory = $true)][byte[]]$Bytes)

    $offset = 0
    if (
        $Bytes.Length -ge 4 -and
        $Bytes[0] -eq 0x00 -and $Bytes[1] -eq 0x00 -and
        $Bytes[2] -eq 0xFE -and $Bytes[3] -eq 0xFF
    ) {
        $encoding = [System.Text.UTF32Encoding]::new($true, $true, $true)
        $offset = 4
    } elseif (
        $Bytes.Length -ge 4 -and
        $Bytes[0] -eq 0xFF -and $Bytes[1] -eq 0xFE -and
        $Bytes[2] -eq 0x00 -and $Bytes[3] -eq 0x00
    ) {
        $encoding = [System.Text.UTF32Encoding]::new($false, $true, $true)
        $offset = 4
    } elseif (
        $Bytes.Length -ge 3 -and
        $Bytes[0] -eq 0xEF -and $Bytes[1] -eq 0xBB -and
        $Bytes[2] -eq 0xBF
    ) {
        $encoding = [System.Text.UTF8Encoding]::new($true, $true)
        $offset = 3
    } elseif (
        $Bytes.Length -ge 2 -and
        $Bytes[0] -eq 0xFE -and $Bytes[1] -eq 0xFF
    ) {
        $encoding = [System.Text.UnicodeEncoding]::new($true, $true, $true)
        $offset = 2
    } elseif (
        $Bytes.Length -ge 2 -and
        $Bytes[0] -eq 0xFF -and $Bytes[1] -eq 0xFE
    ) {
        $encoding = [System.Text.UnicodeEncoding]::new($false, $true, $true)
        $offset = 2
    } else {
        $encoding = [System.Text.UTF8Encoding]::new($false, $true)
    }

    $text = $encoding.GetString($Bytes, $offset, $Bytes.Length - $offset)
    return [pscustomobject]@{
        Text = $text
        Encoding = $encoding
    }
}

function Test-RunlayerFileSnapshot {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][object]$Snapshot
    )

    try {
        if (-not (Test-RunlayerPathSafe -Path $Path)) {
            return $false
        }
        $item = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
        if (
            $item.PSIsContainer -or
            (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
        ) {
            return $false
        }
        $fullPath = [System.IO.Path]::GetFullPath($Path)
        if (
            -not $fullPath.Equals(
                [string]$Snapshot.FullPath,
                [StringComparison]::OrdinalIgnoreCase
            ) -or
            [int64]$item.Length -ne [int64]$Snapshot.Length -or
            $item.LastWriteTimeUtc.Ticks -ne [int64]$Snapshot.LastWriteTimeUtcTicks -or
            $item.CreationTimeUtc.Ticks -ne [int64]$Snapshot.CreationTimeUtcTicks
        ) {
            return $false
        }
        $bytes = [System.IO.File]::ReadAllBytes($Path)
        return (
            [Convert]::ToBase64String($bytes) -ceq
            [string]$Snapshot.BytesBase64
        )
    } catch {
        return $false
    }
}

function Get-RunlayerFileState {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return [pscustomobject]@{
            Exists = $false
            Readable = $false
            Text = $null
            Snapshot = $null
        }
    }
    if (-not (Test-RunlayerPathSafe -Path $Path)) {
        Write-RunlayerHookCleanupLog "skipped unsafe path $Path"
        return [pscustomobject]@{
            Exists = $true
            Readable = $false
            Text = $null
            Snapshot = $null
        }
    }

    try {
        $before = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
        if ([int64]$before.Length -gt $script:RunlayerMaxFileBytes) {
            throw "file exceeds cleanup size limit"
        }
        $bytes = [System.IO.File]::ReadAllBytes($Path)
        $decoded = ConvertFrom-RunlayerTextBytes -Bytes $bytes
        $after = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
        if (
            $before.PSIsContainer -or
            (($before.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) -or
            [int64]$before.Length -ne [int64]$after.Length -or
            $before.LastWriteTimeUtc.Ticks -ne $after.LastWriteTimeUtc.Ticks -or
            $before.CreationTimeUtc.Ticks -ne $after.CreationTimeUtc.Ticks
        ) {
            throw "file changed while reading"
        }
        $snapshot = [pscustomobject]@{
            FullPath = [System.IO.Path]::GetFullPath($Path)
            Length = [int64]$after.Length
            LastWriteTimeUtcTicks = [int64]$after.LastWriteTimeUtc.Ticks
            CreationTimeUtcTicks = [int64]$after.CreationTimeUtc.Ticks
            Text = $decoded.Text
            Encoding = $decoded.Encoding
            BytesBase64 = [Convert]::ToBase64String($bytes)
        }
        return [pscustomobject]@{
            Exists = $true
            Readable = $true
            Text = $decoded.Text
            Snapshot = $snapshot
        }
    } catch {
        Write-RunlayerHookCleanupLog "skipped unreadable file $Path"
        return [pscustomobject]@{
            Exists = $true
            Readable = $false
            Text = $null
            Snapshot = $null
        }
    }
}

function Get-RunlayerBackupRelativePath {
    param([Parameter(Mandatory = $true)][string]$SourcePath)

    $fullPath = [System.IO.Path]::GetFullPath($SourcePath)
    $parts = [System.Collections.Generic.List[string]]::new()
    if ($fullPath -match "^(?<drive>[A-Za-z]):[\\/](?<rest>.*)$") {
        [void]$parts.Add($Matches["drive"].ToUpperInvariant())
        $remaining = $Matches["rest"]
    } elseif ($fullPath -match "^[\\/]{2}(?<rest>.*)$") {
        [void]$parts.Add("UNC")
        $remaining = $Matches["rest"]
    } else {
        [void]$parts.Add("absolute")
        $remaining = $fullPath.TrimStart([char[]]@("/", "\"))
    }

    foreach ($part in ($remaining -split "[\\/]+")) {
        if ([string]::IsNullOrEmpty($part)) {
            continue
        }
        [void]$parts.Add(($part -replace '[<>:"|?*]', "_"))
    }
    return ($parts -join [System.IO.Path]::DirectorySeparatorChar)
}

function New-RunlayerProtectedBackupSessionDirectory {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (
        [Environment]::OSVersion.Platform -ne
        [System.PlatformID]::Win32NT
    ) {
        New-Item -ItemType Directory -Path $Path -ErrorAction Stop | Out-Null
        return
    }

    $security = New-Object System.Security.AccessControl.DirectorySecurity
    $security.SetAccessRuleProtection($true, $false)
    $inheritance = (
        [System.Security.AccessControl.InheritanceFlags]::ContainerInherit -bor
        [System.Security.AccessControl.InheritanceFlags]::ObjectInherit
    )
    $expectedSids = @("S-1-5-18", "S-1-5-32-544")
    foreach ($sidValue in $expectedSids) {
        $sid = New-Object System.Security.Principal.SecurityIdentifier(
            $sidValue
        )
        $rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
            $sid,
            [System.Security.AccessControl.FileSystemRights]::FullControl,
            $inheritance,
            [System.Security.AccessControl.PropagationFlags]::None,
            [System.Security.AccessControl.AccessControlType]::Allow
        )
        [void]$security.AddAccessRule($rule)
    }

    if ($PSVersionTable.PSEdition -eq "Core") {
        [void][System.IO.FileSystemAclExtensions]::CreateDirectory(
            $security,
            $Path
        )
    } else {
        [void][System.IO.Directory]::CreateDirectory($Path, $security)
    }
    $actual = Get-Acl -LiteralPath $Path -ErrorAction Stop
    if (-not $actual.AreAccessRulesProtected) {
        throw "backup session ACL inherits permissions"
    }

    $seen = New-Object "System.Collections.Generic.HashSet[string]"
    $rules = @(
        $actual.GetAccessRules(
            $true,
            $false,
            [System.Security.Principal.SecurityIdentifier]
        )
    )
    foreach ($rule in $rules) {
        $sidValue = $rule.IdentityReference.Value
        if (
            $rule.AccessControlType -ne
                [System.Security.AccessControl.AccessControlType]::Allow -or
            $expectedSids -notcontains $sidValue -or
            (
                $rule.FileSystemRights -band
                [System.Security.AccessControl.FileSystemRights]::FullControl
            ) -ne [System.Security.AccessControl.FileSystemRights]::FullControl -or
            ($rule.InheritanceFlags -band $inheritance) -ne $inheritance
        ) {
            throw "backup session ACL contains unexpected access"
        }
        [void]$seen.Add($sidValue)
    }
    if ($seen.Count -ne $expectedSids.Count) {
        throw "backup session ACL is missing a required principal"
    }
}

function Initialize-RunlayerBackupSession {
    if ($null -ne $script:RunlayerBackupSessionRoot) {
        return $true
    }

    try {
        if (-not (Test-RunlayerPathSafe -Path $script:RunlayerBackupRoot)) {
            throw "backup root crosses a reparse point"
        }
        if (-not (Test-Path -LiteralPath $script:RunlayerBackupRoot)) {
            New-Item -ItemType Directory -Path $script:RunlayerBackupRoot `
                -Force -ErrorAction Stop | Out-Null
        }
        if (-not (Test-RunlayerPathSafe -Path $script:RunlayerBackupRoot)) {
            throw "created backup root is unsafe"
        }

        $runId = "{0}-{1}-{2}" -f (
            Get-Date -Format "yyyyMMdd_HHmmss_fff"
        ), $PID, ([guid]::NewGuid().ToString("N").Substring(0, 8))
        $session = Join-Path $script:RunlayerBackupRoot $runId
        New-RunlayerProtectedBackupSessionDirectory -Path $session
        if (-not (Test-RunlayerPathSafe -Path $session)) {
            throw "protected backup session is unsafe"
        }
        $script:RunlayerBackupSessionRoot = $session
        return $true
    } catch {
        Write-RunlayerHookCleanupLog "backup initialization failed"
        return $false
    }
}

function Backup-RunlayerFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [AllowNull()][object]$ExpectedSnapshot
    )

    if ($null -eq $ExpectedSnapshot) {
        $state = Get-RunlayerFileState -Path $Path
        if (-not $state.Exists -or -not $state.Readable) {
            return $false
        }
        $ExpectedSnapshot = $state.Snapshot
    }
    if (-not (Initialize-RunlayerBackupSession)) {
        return $false
    }

    try {
        $relative = Get-RunlayerBackupRelativePath -SourcePath $Path
        $destination = Join-Path $script:RunlayerBackupSessionRoot $relative
        $parent = Split-Path -Parent $destination
        if (-not (Test-RunlayerPathSafe -Path $parent)) {
            throw "backup destination is unsafe"
        }
        New-Item -ItemType Directory -Path $parent -Force -ErrorAction Stop | Out-Null
        if (-not (Test-RunlayerPathSafe -Path $parent)) {
            throw "created backup destination is unsafe"
        }

        if (Test-Path -LiteralPath $destination) {
            $destination = "{0}.{1}" -f $destination, ([guid]::NewGuid().ToString("N"))
        }
        if (-not (Test-RunlayerFileSnapshot -Path $Path -Snapshot $ExpectedSnapshot)) {
            throw "source changed before backup"
        }
        Copy-Item -LiteralPath $Path -Destination $destination -ErrorAction Stop
        if (-not (Test-RunlayerFileSnapshot -Path $Path -Snapshot $ExpectedSnapshot)) {
            Remove-Item -LiteralPath $destination -Force -ErrorAction SilentlyContinue
            throw "source changed during backup"
        }
        return $true
    } catch {
        Write-RunlayerHookCleanupLog "backup failed for $Path"
        return $false
    }
}

function Write-RunlayerNewTextFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][AllowEmptyString()][string]$Text,
        [Parameter(Mandatory = $true)][System.Text.Encoding]$Encoding
    )

    $stream = [System.IO.File]::Open(
        $Path,
        [System.IO.FileMode]::CreateNew,
        [System.IO.FileAccess]::Write,
        [System.IO.FileShare]::None
    )
    try {
        $preamble = $Encoding.GetPreamble()
        if ($preamble.Length -gt 0) {
            $stream.Write($preamble, 0, $preamble.Length)
        }
        $bytes = $Encoding.GetBytes($Text)
        if ($bytes.Length -gt 0) {
            $stream.Write($bytes, 0, $bytes.Length)
        }
        $stream.Flush($true)
    } finally {
        $stream.Dispose()
    }
}

function Invoke-RunlayerFileReplace {
    param(
        [Parameter(Mandatory = $true)][string]$ReplacementPath,
        [Parameter(Mandatory = $true)][string]$DestinationPath,
        [Parameter(Mandatory = $true)][string]$RollbackPath
    )

    [System.IO.File]::Replace(
        $ReplacementPath,
        $DestinationPath,
        $RollbackPath
    )
}

function Set-RunlayerAtomicTextFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][AllowEmptyString()][string]$Text,
        [AllowNull()][object]$ExpectedSnapshot
    )

    $temporary = $null
    $rollback = $null
    try {
        if ($null -eq $ExpectedSnapshot) {
            $state = Get-RunlayerFileState -Path $Path
            if (-not $state.Exists -or -not $state.Readable) {
                throw "destination is missing or unreadable"
            }
            $ExpectedSnapshot = $state.Snapshot
        }
        if (-not (Test-RunlayerFileSnapshot -Path $Path -Snapshot $ExpectedSnapshot)) {
            throw "destination changed before replacement"
        }
        $parent = Split-Path -Parent $Path
        if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
            throw "destination parent is missing"
        }
        $temporary = Join-Path $parent (
            ".runlayer-remove-{0}.tmp" -f ([guid]::NewGuid().ToString("N"))
        )
        $encoding = $ExpectedSnapshot.Encoding
        if ($null -eq $encoding) {
            throw "destination encoding is unavailable"
        }
        Write-RunlayerNewTextFile -Path $temporary -Text $Text `
            -Encoding $encoding
        if (-not (Test-RunlayerPathSafe -Path $temporary)) {
            throw "temporary file is unsafe"
        }
        if (-not (Test-RunlayerFileSnapshot -Path $Path -Snapshot $ExpectedSnapshot)) {
            throw "destination changed before atomic replacement"
        }
        if ($PSVersionTable.PSEdition -eq "Core") {
            # File.Replace rejects a null backup path on .NET Core. The
            # overwrite Move overload maps to one same-filesystem replacement.
            [System.IO.File]::Move($temporary, $Path, $true)
        } else {
            # Windows PowerShell 5.1 lacks the overwrite Move overload.
            $rollback = Join-Path $parent (
                ".runlayer-rollback-{0}.tmp" -f (
                    [guid]::NewGuid().ToString("N")
                )
            )
            if (-not (Test-RunlayerPathSafe -Path $rollback)) {
                throw "rollback path is unsafe"
            }
            Invoke-RunlayerFileReplace -ReplacementPath $temporary `
                -DestinationPath $Path -RollbackPath $rollback
            Remove-Item -LiteralPath $rollback -Force `
                -ErrorAction SilentlyContinue
            $rollback = $null
        }
        $temporary = $null
        return $true
    } catch {
        if (
            $null -ne $rollback -and
            (Test-Path -LiteralPath $rollback -PathType Leaf) -and
            -not (Test-Path -LiteralPath $Path) -and
            (Test-RunlayerPathSafe -Path $rollback)
        ) {
            try {
                [System.IO.File]::Move($rollback, $Path)
                $rollback = $null
            } catch {
                Write-RunlayerHookCleanupLog (
                    "atomic replace rollback retained at $rollback"
                )
            }
        }
        Write-RunlayerHookCleanupLog "atomic replace failed for $Path"
        return $false
    } finally {
        if ($null -ne $temporary) {
            Remove-Item -LiteralPath $temporary -Force -ErrorAction SilentlyContinue
        }
    }
}

function Test-RunlayerJsonObject {
    param([AllowNull()][object]$Value)

    return $null -ne $Value -and (
        $Value -is [System.Collections.IDictionary] -or
        $Value.GetType().Name -eq "PSCustomObject"
    )
}

function Test-RunlayerCommand {
    param([AllowNull()][object]$Command)

    if ($Command -isnot [string] -or [string]::IsNullOrWhiteSpace($Command)) {
        return $false
    }

    $ownedShim = '(?i)(?:^|[\\/"''\s])(?:runlayer-hook\.sh|runlayer-cursor-hook\.sh|runlayer-claude-hook\.sh|aiwatch-hook(?:\.exe)?|aiwatch-enforce(?:\.exe)?|runlayer-hook(?:\.exe)?)(?:["''\s]|$)'
    $aiwatch = '(?i)(?:^|[\\/"''\s])aiwatch(?:\.exe)?["''\s]+hook(?:["''\s]|$)'
    $runlayer = '(?i)(?:^|[\\/"''\s])runlayer(?:\.exe)?["''\s]+hook(?:["''\s]|$)'
    $module = '(?i)(?:^|\s)-m\s+runlayer_cli\.hook(?:\s|$)'
    return (
        $Command -match $ownedShim -or
        $Command -match $aiwatch -or
        $Command -match $runlayer -or
        $Command -match $module
    )
}

function Move-RunlayerJsonStringEnd {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][ref]$Position
    )

    $start = [int]$Position.Value
    if ($start -ge $Text.Length -or $Text[$start] -ne '"') {
        throw "expected JSON string"
    }
    $Position.Value++
    while ($Position.Value -lt $Text.Length) {
        $character = $Text[$Position.Value]
        if ([int][char]$character -lt 0x20) {
            throw "control character in JSON string"
        }
        if ($character -eq "\") {
            $Position.Value++
            if ($Position.Value -ge $Text.Length) {
                throw "unterminated JSON escape"
            }
            $escaped = $Text[$Position.Value]
            if ($escaped -eq "u") {
                for ($digit = 1; $digit -le 4; $digit++) {
                    $escapePosition = $Position.Value + $digit
                    if (
                        $escapePosition -ge $Text.Length -or
                        $Text[$escapePosition] -notmatch "[0-9A-Fa-f]"
                    ) {
                        throw "invalid JSON unicode escape"
                    }
                }
                $Position.Value += 5
                continue
            }
            if ('"\/bfnrt'.IndexOf($escaped) -lt 0) {
                throw "invalid JSON escape"
            }
            $Position.Value++
            continue
        }
        if ($character -eq '"') {
            $Position.Value++
            return
        }
        $Position.Value++
    }
    throw "unterminated JSON string"
}

function ConvertTo-RunlayerJsoncScrubbedText {
    param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Text)

    $characters = $Text.ToCharArray()
    $comments = [System.Collections.Generic.List[object]]::new()
    $trailingCommas = [System.Collections.Generic.HashSet[int]]::new()
    $pendingComma = -1
    $index = 0
    while ($index -lt $characters.Length) {
        if ([char]::IsWhiteSpace($characters[$index])) {
            $index++
            continue
        }
        if ($characters[$index] -eq '"') {
            $pendingComma = -1
            $stringPosition = $index
            Move-RunlayerJsonStringEnd -Text $Text `
                -Position ([ref]$stringPosition)
            $index = $stringPosition
            continue
        }

        if (
            $characters[$index] -eq "/" -and
            $index + 1 -lt $characters.Length -and
            $characters[$index + 1] -eq "/"
        ) {
            $start = $index
            while (
                $index -lt $characters.Length -and
                $characters[$index] -ne "`r" -and
                $characters[$index] -ne "`n"
            ) {
                $characters[$index] = " "
                $index++
            }
            if ($index -lt $characters.Length -and $characters[$index] -eq "`r") {
                $index++
                if (
                    $index -lt $characters.Length -and
                    $characters[$index] -eq "`n"
                ) {
                    $index++
                }
            } elseif (
                $index -lt $characters.Length -and
                $characters[$index] -eq "`n"
            ) {
                $index++
            }
            [void]$comments.Add([pscustomobject]@{
                Start = $start
                End = $index
            })
            continue
        }

        if (
            $characters[$index] -eq "/" -and
            $index + 1 -lt $characters.Length -and
            $characters[$index + 1] -eq "*"
        ) {
            $start = $index
            $closed = $false
            while ($index -lt $characters.Length) {
                if (
                    $index + 1 -lt $characters.Length -and
                    $characters[$index] -eq "*" -and
                    $characters[$index + 1] -eq "/"
                ) {
                    $characters[$index] = " "
                    $characters[$index + 1] = " "
                    $index += 2
                    $closed = $true
                    break
                }
                if (
                    $characters[$index] -ne "`r" -and
                    $characters[$index] -ne "`n"
                ) {
                    $characters[$index] = " "
                }
                $index++
            }
            if (-not $closed) {
                throw "unterminated JSON block comment"
            }
            [void]$comments.Add([pscustomobject]@{
                Start = $start
                End = $index
            })
            continue
        }
        if ($characters[$index] -eq ",") {
            $pendingComma = $index
            $index++
            continue
        }
        if (
            $pendingComma -ge 0 -and
            $characters[$index] -in @("}", "]")
        ) {
            $characters[$pendingComma] = " "
            [void]$trailingCommas.Add($pendingComma)
        }
        $pendingComma = -1
        $index++
    }

    return [pscustomobject]@{
        Text = $characters -join ""
        Comments = [object[]]$comments.ToArray()
        TrailingCommas = $trailingCommas
    }
}

function Move-RunlayerJsonSpanWhitespace {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][ref]$Position
    )

    while ($Position.Value -lt $Text.Length) {
        $character = $Text[$Position.Value]
        if ($character -notin @(" ", "`t", "`r", "`n")) {
            break
        }
        $Position.Value++
    }
}

function Get-RunlayerJsonSpanId {
    param([Parameter(Mandatory = $true)][ref]$NextId)

    $id = [int]$NextId.Value
    if ($id -ge $script:RunlayerMaxJsonSpanNodes) {
        throw "JSON node count exceeds cleanup limit"
    }
    $NextId.Value = $id + 1
    return $id
}

function Get-RunlayerJsonTrailingComma {
    param(
        [Parameter(Mandatory = $true)][object]$TrailingCommas,
        [Parameter(Mandatory = $true)][int]$Start,
        [Parameter(Mandatory = $true)][int]$End
    )

    $found = -1
    for ($index = $Start; $index -lt $End; $index++) {
        if (-not $TrailingCommas.Contains($index)) {
            continue
        }
        if ($found -ge 0) {
            throw "multiple trailing commas"
        }
        $found = $index
    }
    return $found
}

function ConvertFrom-RunlayerJsonStringToken {
    param([Parameter(Mandatory = $true)][string]$Token)

    $builder = [System.Text.StringBuilder]::new()
    for ($index = 1; $index -lt $Token.Length - 1; $index++) {
        $character = $Token[$index]
        if ($character -ne "\") {
            [void]$builder.Append($character)
            continue
        }

        $index++
        $escaped = $Token[$index]
        if ($escaped -eq "u") {
            $codeUnit = [Convert]::ToInt32(
                $Token.Substring($index + 1, 4),
                16
            )
            [void]$builder.Append([char]$codeUnit)
            $index += 4
            continue
        }
        $decoded = switch ($escaped) {
            '"' { '"' }
            "\" { "\" }
            "/" { "/" }
            "b" { [char]0x08 }
            "f" { [char]0x0C }
            "n" { [char]0x0A }
            "r" { [char]0x0D }
            "t" { [char]0x09 }
        }
        [void]$builder.Append($decoded)
    }
    return $builder.ToString()
}

function Read-RunlayerJsonStringSpan {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][ref]$Position,
        [Parameter(Mandatory = $true)][ref]$NextId
    )

    $start = [int]$Position.Value
    Move-RunlayerJsonStringEnd -Text $Text -Position $Position
    $end = [int]$Position.Value
    $token = $Text.Substring($start, $end - $start)
    $decoded = ConvertFrom-RunlayerJsonStringToken -Token $token
    return [pscustomobject]@{
        Id = Get-RunlayerJsonSpanId -NextId $NextId
        Kind = "String"
        Start = $start
        End = $end
        Decoded = $decoded
        CommaAfter = -1
    }
}

function Read-RunlayerJsonObjectSpan {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][ref]$Position,
        [Parameter(Mandatory = $true)][ref]$NextId,
        [Parameter(Mandatory = $true)][object]$TrailingCommas,
        [Parameter(Mandatory = $true)][int]$Depth
    )

    $start = [int]$Position.Value
    $id = Get-RunlayerJsonSpanId -NextId $NextId
    $Position.Value++
    Move-RunlayerJsonSpanWhitespace -Text $Text -Position $Position
    $properties = [System.Collections.Generic.List[object]]::new()

    if ($Position.Value -lt $Text.Length -and $Text[$Position.Value] -eq "}") {
        $closeStart = [int]$Position.Value
        if (
            (Get-RunlayerJsonTrailingComma -TrailingCommas $TrailingCommas `
                -Start ($start + 1) -End $closeStart) -ge 0
        ) {
            throw "trailing comma without an object property"
        }
        $Position.Value++
        return [pscustomobject]@{
            Id = $id
            Kind = "Object"
            Start = $start
            End = [int]$Position.Value
            CloseStart = $closeStart
            Properties = [object[]]$properties.ToArray()
            TrailingComma = -1
            CommaAfter = -1
        }
    }

    while ($Position.Value -lt $Text.Length) {
        $key = Read-RunlayerJsonStringSpan -Text $Text -Position $Position `
            -NextId $NextId
        Move-RunlayerJsonSpanWhitespace -Text $Text -Position $Position
        if (
            $Position.Value -ge $Text.Length -or
            $Text[$Position.Value] -ne ":"
        ) {
            throw "expected JSON property colon"
        }
        $Position.Value++
        Move-RunlayerJsonSpanWhitespace -Text $Text -Position $Position
        $value = Read-RunlayerJsonValueSpan -Text $Text -Position $Position `
            -NextId $NextId -TrailingCommas $TrailingCommas `
            -Depth ($Depth + 1)
        $property = [pscustomobject]@{
            Id = Get-RunlayerJsonSpanId -NextId $NextId
            Name = [string]$key.Decoded
            Key = $key
            Value = $value
            Start = [int]$key.Start
            End = [int]$value.End
            CommaAfter = -1
        }
        [void]$properties.Add($property)
        Move-RunlayerJsonSpanWhitespace -Text $Text -Position $Position
        if ($Position.Value -ge $Text.Length) {
            throw "unterminated JSON object"
        }
        if ($Text[$Position.Value] -eq ",") {
            $property.CommaAfter = [int]$Position.Value
            $Position.Value++
            Move-RunlayerJsonSpanWhitespace -Text $Text -Position $Position
            if (
                $Position.Value -ge $Text.Length -or
                $Text[$Position.Value] -eq "}"
            ) {
                throw "missing JSON property after comma"
            }
            continue
        }
        if ($Text[$Position.Value] -eq "}") {
            break
        }
        throw "expected JSON object comma or close"
    }

    $closeStart = [int]$Position.Value
    $last = $properties[$properties.Count - 1]
    $trailingComma = Get-RunlayerJsonTrailingComma `
        -TrailingCommas $TrailingCommas -Start $last.End -End $closeStart
    $Position.Value++
    return [pscustomobject]@{
        Id = $id
        Kind = "Object"
        Start = $start
        End = [int]$Position.Value
        CloseStart = $closeStart
        Properties = [object[]]$properties.ToArray()
        TrailingComma = $trailingComma
        CommaAfter = -1
    }
}

function Read-RunlayerJsonArraySpan {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][ref]$Position,
        [Parameter(Mandatory = $true)][ref]$NextId,
        [Parameter(Mandatory = $true)][object]$TrailingCommas,
        [Parameter(Mandatory = $true)][int]$Depth
    )

    $start = [int]$Position.Value
    $id = Get-RunlayerJsonSpanId -NextId $NextId
    $Position.Value++
    Move-RunlayerJsonSpanWhitespace -Text $Text -Position $Position
    $items = [System.Collections.Generic.List[object]]::new()

    if ($Position.Value -lt $Text.Length -and $Text[$Position.Value] -eq "]") {
        $closeStart = [int]$Position.Value
        if (
            (Get-RunlayerJsonTrailingComma -TrailingCommas $TrailingCommas `
                -Start ($start + 1) -End $closeStart) -ge 0
        ) {
            throw "trailing comma without an array item"
        }
        $Position.Value++
        return [pscustomobject]@{
            Id = $id
            Kind = "Array"
            Start = $start
            End = [int]$Position.Value
            CloseStart = $closeStart
            Items = [object[]]$items.ToArray()
            TrailingComma = -1
            CommaAfter = -1
        }
    }

    while ($Position.Value -lt $Text.Length) {
        $item = Read-RunlayerJsonValueSpan -Text $Text -Position $Position `
            -NextId $NextId -TrailingCommas $TrailingCommas `
            -Depth ($Depth + 1)
        [void]$items.Add($item)
        Move-RunlayerJsonSpanWhitespace -Text $Text -Position $Position
        if ($Position.Value -ge $Text.Length) {
            throw "unterminated JSON array"
        }
        if ($Text[$Position.Value] -eq ",") {
            $item.CommaAfter = [int]$Position.Value
            $Position.Value++
            Move-RunlayerJsonSpanWhitespace -Text $Text -Position $Position
            if (
                $Position.Value -ge $Text.Length -or
                $Text[$Position.Value] -eq "]"
            ) {
                throw "missing JSON item after comma"
            }
            continue
        }
        if ($Text[$Position.Value] -eq "]") {
            break
        }
        throw "expected JSON array comma or close"
    }

    $closeStart = [int]$Position.Value
    $last = $items[$items.Count - 1]
    $trailingComma = Get-RunlayerJsonTrailingComma `
        -TrailingCommas $TrailingCommas -Start $last.End -End $closeStart
    $Position.Value++
    return [pscustomobject]@{
        Id = $id
        Kind = "Array"
        Start = $start
        End = [int]$Position.Value
        CloseStart = $closeStart
        Items = [object[]]$items.ToArray()
        TrailingComma = $trailingComma
        CommaAfter = -1
    }
}

function Read-RunlayerJsonValueSpan {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][ref]$Position,
        [Parameter(Mandatory = $true)][ref]$NextId,
        [Parameter(Mandatory = $true)][object]$TrailingCommas,
        [int]$Depth = 0
    )

    if ($Depth -gt 100) {
        throw "JSON nesting exceeds cleanup limit"
    }
    Move-RunlayerJsonSpanWhitespace -Text $Text -Position $Position
    if ($Position.Value -ge $Text.Length) {
        throw "expected JSON value"
    }
    $character = $Text[$Position.Value]
    if ($character -eq "{") {
        return Read-RunlayerJsonObjectSpan -Text $Text -Position $Position `
            -NextId $NextId -TrailingCommas $TrailingCommas -Depth $Depth
    }
    if ($character -eq "[") {
        return Read-RunlayerJsonArraySpan -Text $Text -Position $Position `
            -NextId $NextId -TrailingCommas $TrailingCommas -Depth $Depth
    }
    if ($character -eq '"') {
        return Read-RunlayerJsonStringSpan -Text $Text -Position $Position `
            -NextId $NextId
    }

    $start = [int]$Position.Value
    $end = $start
    while (
        $end -lt $Text.Length -and
        $Text[$end] -notin @(" ", "`t", "`r", "`n", ",", "]", "}")
    ) {
        $end++
    }
    $token = $Text.Substring($start, $end - $start)
    if (
        $token -notmatch
        '^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)$'
    ) {
        throw "invalid JSON value"
    }
    $Position.Value = $end
    $decoded = ConvertFrom-Json -InputObject $token -ErrorAction Stop
    return [pscustomobject]@{
        Id = Get-RunlayerJsonSpanId -NextId $NextId
        Kind = "Primitive"
        Start = $start
        End = [int]$Position.Value
        Decoded = $decoded
        CommaAfter = -1
    }
}

function Get-RunlayerJsonDocument {
    param([Parameter(Mandatory = $true)][string]$Path)

    $state = Get-RunlayerFileState -Path $Path
    if (-not $state.Exists -or -not $state.Readable) {
        return [pscustomobject]@{
            Success = $false
            Exists = $state.Exists
            Root = $null
            Snapshot = $null
        }
    }

    try {
        $scrubbed = ConvertTo-RunlayerJsoncScrubbedText -Text $state.Text
        $position = 0
        $nextId = 0
        $root = Read-RunlayerJsonValueSpan -Text $scrubbed.Text `
            -Position ([ref]$position) -NextId ([ref]$nextId) `
            -TrailingCommas $scrubbed.TrailingCommas
        Move-RunlayerJsonSpanWhitespace -Text $scrubbed.Text `
            -Position ([ref]$position)
        if ($position -ne $scrubbed.Text.Length -or $root.Kind -ne "Object") {
            throw "JSON root is not exactly one object"
        }
        # Cross-check the span parser against PowerShell's JSON parser.
        $document = ConvertFrom-Json -InputObject $scrubbed.Text -ErrorAction Stop
        if (-not (Test-RunlayerJsonObject -Value $document)) {
            throw "JSON root is not an object"
        }
        return [pscustomobject]@{
            Success = $true
            Exists = $true
            Root = $root
            Text = $state.Text
            ScrubbedText = $scrubbed.Text
            Comments = $scrubbed.Comments
            Snapshot = $state.Snapshot
        }
    } catch {
        Write-RunlayerHookCleanupLog "skipped malformed JSON or JSONC $Path"
        return [pscustomobject]@{
            Success = $false
            Exists = $true
            Root = $null
            Snapshot = $null
        }
    }
}

function Get-RunlayerJsonSpanProperty {
    param(
        [Parameter(Mandatory = $true)][object]$ObjectNode,
        [Parameter(Mandatory = $true)][string]$Name
    )

    if ($ObjectNode.Kind -ne "Object") {
        return $null
    }
    $found = $null
    foreach ($property in $ObjectNode.Properties) {
        if (
            [string]::Equals(
                [string]$property.Name,
                $Name,
                [System.StringComparison]::OrdinalIgnoreCase
            )
        ) {
            $found = $property
        }
    }
    return $found
}

function Get-RunlayerJsonSpanProperties {
    param(
        [Parameter(Mandatory = $true)][object]$ObjectNode,
        [Parameter(Mandatory = $true)][string]$Name
    )

    if ($ObjectNode.Kind -ne "Object") {
        return @()
    }
    return @(
        $ObjectNode.Properties | Where-Object {
            [string]::Equals(
                [string]$_.Name,
                $Name,
                [System.StringComparison]::OrdinalIgnoreCase
            )
        }
    )
}

function Test-RunlayerJsonSpanMarked {
    param(
        [Parameter(Mandatory = $true)][hashtable]$Marks,
        [Parameter(Mandatory = $true)][int]$Id
    )

    return $Marks.ContainsKey([string]$Id)
}

function Set-RunlayerJsonSpanMarked {
    param(
        [Parameter(Mandatory = $true)][hashtable]$Marks,
        [Parameter(Mandatory = $true)][int]$Id
    )

    $Marks[[string]$Id] = $true
}

function Get-RunlayerJsonProjectedPropertyCount {
    param(
        [Parameter(Mandatory = $true)][object]$ObjectNode,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties
    )

    $count = 0
    foreach ($property in $ObjectNode.Properties) {
        if (
            -not (
                Test-RunlayerJsonSpanMarked -Marks $RemovedProperties `
                    -Id $property.Id
            )
        ) {
            $count++
        }
    }
    return $count
}

function Get-RunlayerJsonProjectedItemCount {
    param(
        [Parameter(Mandatory = $true)][object]$ArrayNode,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems
    )

    $count = 0
    foreach ($item in $ArrayNode.Items) {
        if (
            -not (
                Test-RunlayerJsonSpanMarked -Marks $RemovedItems -Id $item.Id
            )
        ) {
            $count++
        }
    }
    return $count
}

function Test-RunlayerJsonSpanPropertyNamesUnique {
    param(
        [Parameter(Mandatory = $true)][object]$ObjectNode,
        [Parameter(Mandatory = $true)][string[]]$Names
    )

    foreach ($name in $Names) {
        if (
            @(
                Get-RunlayerJsonSpanProperties -ObjectNode $ObjectNode `
                    -Name $name
            ).Count -gt 1
        ) {
            return $false
        }
    }
    return $true
}

function Test-RunlayerHookArraySpanUnambiguous {
    param([Parameter(Mandatory = $true)][object]$ArrayNode)

    foreach ($entry in $ArrayNode.Items) {
        if ($entry.Kind -ne "Object") {
            continue
        }
        if (
            -not (
                Test-RunlayerJsonSpanPropertyNamesUnique `
                    -ObjectNode $entry `
                    -Names @("hooks", "command", "args", "bash", "powershell")
            )
        ) {
            return $false
        }
        $nested = Get-RunlayerJsonSpanProperty -ObjectNode $entry -Name "hooks"
        if (
            $null -ne $nested -and
            $nested.Value.Kind -eq "Array" -and
            -not (
                Test-RunlayerHookArraySpanUnambiguous `
                    -ArrayNode $nested.Value
            )
        ) {
            return $false
        }
    }
    return $true
}

function Test-RunlayerHooksObjectSpanUnambiguous {
    param([Parameter(Mandatory = $true)][object]$HooksNode)

    $eventNames = [System.Collections.Generic.HashSet[string]]::new(
        [System.StringComparer]::OrdinalIgnoreCase
    )
    foreach ($eventProperty in $HooksNode.Properties) {
        if (-not $eventNames.Add([string]$eventProperty.Name)) {
            return $false
        }
        if (
            $eventProperty.Value.Kind -eq "Array" -and
            -not (
                Test-RunlayerHookArraySpanUnambiguous `
                    -ArrayNode $eventProperty.Value
            )
        ) {
            return $false
        }
    }
    return $true
}

function Get-RunlayerHookEntrySpanCommand {
    param([Parameter(Mandatory = $true)][object]$EntryNode)

    $commandProperty = Get-RunlayerJsonSpanProperty -ObjectNode $EntryNode `
        -Name "command"
    if (
        $null -eq $commandProperty -or
        $commandProperty.Value.Kind -ne "String"
    ) {
        return ""
    }

    $command = [string]$commandProperty.Value.Decoded
    $argsProperty = Get-RunlayerJsonSpanProperty -ObjectNode $EntryNode `
        -Name "args"
    if ($null -eq $argsProperty -or $argsProperty.Value.Kind -ne "Array") {
        return $command
    }

    $arguments = [System.Collections.Generic.List[string]]::new()
    foreach ($argument in $argsProperty.Value.Items) {
        if ($argument.Kind -ne "String") {
            return $command
        }
        [void]$arguments.Add([string]$argument.Decoded)
    }
    if ($arguments.Count -eq 0) {
        return $command
    }
    return (@($command) + $arguments.ToArray()) -join " "
}

function Set-RunlayerHookArraySpanProjection {
    param(
        [Parameter(Mandatory = $true)][object]$ArrayNode,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems
    )

    $changed = $false
    foreach ($entry in $ArrayNode.Items) {
        if ($entry.Kind -ne "Object") {
            continue
        }
        $entryResult = Set-RunlayerHookEntrySpanProjection `
            -EntryNode $entry -RemovedProperties $RemovedProperties `
            -RemovedItems $RemovedItems
        if ($entryResult.Changed) {
            $changed = $true
        }
        if (-not $entryResult.Keep) {
            Set-RunlayerJsonSpanMarked -Marks $RemovedItems -Id $entry.Id
        }
    }
    return [pscustomobject]@{
        Changed = $changed
        ItemCount = Get-RunlayerJsonProjectedItemCount `
            -ArrayNode $ArrayNode -RemovedItems $RemovedItems
    }
}

function Set-RunlayerHookEntrySpanProjection {
    param(
        [Parameter(Mandatory = $true)][object]$EntryNode,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems
    )

    $changed = $false
    $hooksProperty = Get-RunlayerJsonSpanProperty -ObjectNode $EntryNode `
        -Name "hooks"
    if (
        $null -ne $hooksProperty -and
        $hooksProperty.Value.Kind -eq "Array"
    ) {
        $innerResult = Set-RunlayerHookArraySpanProjection `
            -ArrayNode $hooksProperty.Value `
            -RemovedProperties $RemovedProperties -RemovedItems $RemovedItems
        if ($innerResult.Changed) {
            $changed = $true
            if ($innerResult.ItemCount -eq 0) {
                Set-RunlayerJsonSpanMarked -Marks $RemovedProperties `
                    -Id $hooksProperty.Id
            }
        }
    }

    $commandProperty = Get-RunlayerJsonSpanProperty -ObjectNode $EntryNode `
        -Name "command"
    if (
        $null -ne $commandProperty -and
        (Test-RunlayerCommand -Command (
                Get-RunlayerHookEntrySpanCommand -EntryNode $EntryNode
            ))
    ) {
        Set-RunlayerJsonSpanMarked -Marks $RemovedProperties `
            -Id $commandProperty.Id
        $argsProperty = Get-RunlayerJsonSpanProperty -ObjectNode $EntryNode `
            -Name "args"
        if ($null -ne $argsProperty) {
            Set-RunlayerJsonSpanMarked -Marks $RemovedProperties `
                -Id $argsProperty.Id
        }
        $changed = $true
    }

    foreach ($field in @("bash", "powershell")) {
        $property = Get-RunlayerJsonSpanProperty -ObjectNode $EntryNode `
            -Name $field
        if (
            $null -ne $property -and
            $property.Value.Kind -eq "String" -and
            (Test-RunlayerCommand -Command $property.Value.Decoded)
        ) {
            Set-RunlayerJsonSpanMarked -Marks $RemovedProperties -Id $property.Id
            $changed = $true
        }
    }

    $hasCommand = $false
    foreach ($field in @("command", "bash", "powershell")) {
        $property = Get-RunlayerJsonSpanProperty -ObjectNode $EntryNode `
            -Name $field
        if (
            $null -ne $property -and
            -not (
                Test-RunlayerJsonSpanMarked -Marks $RemovedProperties `
                    -Id $property.Id
            ) -and
            $property.Value.Kind -eq "String" -and
            -not [string]::IsNullOrWhiteSpace($property.Value.Decoded)
        ) {
            $hasCommand = $true
            break
        }
    }
    $hasNested = (
        $null -ne $hooksProperty -and
        -not (
            Test-RunlayerJsonSpanMarked -Marks $RemovedProperties `
                -Id $hooksProperty.Id
        ) -and
        $hooksProperty.Value.Kind -eq "Array" -and
        (
            Get-RunlayerJsonProjectedItemCount `
                -ArrayNode $hooksProperty.Value -RemovedItems $RemovedItems
        ) -gt 0
    )

    return [pscustomobject]@{
        Changed = $changed
        Keep = -not ($changed -and -not $hasCommand -and -not $hasNested)
    }
}

function Set-RunlayerHooksObjectSpanProjection {
    param(
        [Parameter(Mandatory = $true)][object]$HooksNode,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems
    )

    $changed = $false
    foreach ($eventProperty in $HooksNode.Properties) {
        if ($eventProperty.Value.Kind -ne "Array") {
            continue
        }
        $result = Set-RunlayerHookArraySpanProjection `
            -ArrayNode $eventProperty.Value `
            -RemovedProperties $RemovedProperties -RemovedItems $RemovedItems
        if (-not $result.Changed) {
            continue
        }
        $changed = $true
        if ($result.ItemCount -eq 0) {
            Set-RunlayerJsonSpanMarked -Marks $RemovedProperties `
                -Id $eventProperty.Id
        }
    }
    return $changed
}

function ConvertTo-RunlayerProjectedStrictJson {
    param(
        [Parameter(Mandatory = $true)][object]$Node,
        [Parameter(Mandatory = $true)][string]$ScrubbedText,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems
    )

    if ($Node.Kind -eq "Object") {
        $parts = [System.Collections.Generic.List[string]]::new()
        foreach ($property in $Node.Properties) {
            if (
                Test-RunlayerJsonSpanMarked -Marks $RemovedProperties `
                    -Id $property.Id
            ) {
                continue
            }
            $key = $ScrubbedText.Substring(
                $property.Key.Start,
                $property.Key.End - $property.Key.Start
            )
            $value = ConvertTo-RunlayerProjectedStrictJson `
                -Node $property.Value -ScrubbedText $ScrubbedText `
                -RemovedProperties $RemovedProperties -RemovedItems $RemovedItems
            [void]$parts.Add($key + ":" + $value)
        }
        return "{" + ($parts.ToArray() -join ",") + "}"
    }
    if ($Node.Kind -eq "Array") {
        $parts = [System.Collections.Generic.List[string]]::new()
        foreach ($item in $Node.Items) {
            if (
                Test-RunlayerJsonSpanMarked -Marks $RemovedItems -Id $item.Id
            ) {
                continue
            }
            [void]$parts.Add((
                ConvertTo-RunlayerProjectedStrictJson `
                    -Node $item -ScrubbedText $ScrubbedText `
                    -RemovedProperties $RemovedProperties `
                    -RemovedItems $RemovedItems
            ))
        }
        return "[" + ($parts.ToArray() -join ",") + "]"
    }
    return $ScrubbedText.Substring($Node.Start, $Node.End - $Node.Start)
}

function Add-RunlayerUncommentedRemovalRange {
    param(
        [Parameter(Mandatory = $true)][object]$Ranges,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][object[]]$Comments,
        [Parameter(Mandatory = $true)][int]$Start,
        [Parameter(Mandatory = $true)][int]$End
    )

    $cursor = $Start
    $low = 0
    $high = $Comments.Count
    while ($low -lt $high) {
        $middle = ($low + $high) -shr 1
        if ([int]$Comments[$middle].End -le $Start) {
            $low = $middle + 1
        } else {
            $high = $middle
        }
    }
    for ($index = $low; $index -lt $Comments.Count; $index++) {
        $comment = $Comments[$index]
        if ($comment.End -le $cursor) {
            continue
        }
        if ($comment.Start -ge $End) {
            break
        }
        if ($comment.Start -gt $cursor) {
            [void]$Ranges.Add([pscustomobject]@{
                Start = $cursor
                End = [Math]::Min([int]$comment.Start, $End)
            })
        }
        $cursor = [Math]::Max($cursor, [int]$comment.End)
        if ($cursor -ge $End) {
            break
        }
    }
    if ($cursor -lt $End) {
        [void]$Ranges.Add([pscustomobject]@{
            Start = $cursor
            End = $End
        })
    }
}

function Get-RunlayerTextLayout {
    param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Text)

    $lineStarts = New-Object int[] ($Text.Length + 1)
    $prefixWhitespace = New-Object bool[] ($Text.Length + 1)
    $lineStart = 0
    $onlyWhitespace = $true
    for ($index = 0; $index -lt $Text.Length; $index++) {
        $lineStarts[$index] = $lineStart
        $prefixWhitespace[$index] = $onlyWhitespace
        $character = $Text[$index]
        if ($character -in @("`r", "`n")) {
            $lineStart = $index + 1
            $onlyWhitespace = $true
        } elseif ($character -notin @(" ", "`t")) {
            $onlyWhitespace = $false
        }
    }
    $lineStarts[$Text.Length] = $lineStart
    $prefixWhitespace[$Text.Length] = $onlyWhitespace
    return [pscustomobject]@{
        LineStarts = $lineStarts
        PrefixWhitespace = $prefixWhitespace
    }
}

function Get-RunlayerExpandedJsonElementRange {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][object]$Layout,
        [Parameter(Mandatory = $true)][object]$Element,
        [Parameter(Mandatory = $true)][hashtable]$RemovedCommas
    )

    $start = [int]$Element.Start
    # Full-line elements take their indentation and removed comma/newline tail.
    if ($Layout.PrefixWhitespace[$start]) {
        $start = $Layout.LineStarts[$start]
    }

    $end = [int]$Element.End
    $probe = $end
    while (
        $probe -lt $Text.Length -and
        $Text[$probe] -in @(" ", "`t")
    ) {
        $probe++
    }
    if ($RemovedCommas.ContainsKey([string]$probe)) {
        $probe++
        while (
            $probe -lt $Text.Length -and
            $Text[$probe] -in @(" ", "`t")
        ) {
            $probe++
        }
    }
    if ($probe -lt $Text.Length -and $Text[$probe] -eq "`r") {
        $probe++
        if ($probe -lt $Text.Length -and $Text[$probe] -eq "`n") {
            $probe++
        }
        $end = $probe
    } elseif ($probe -lt $Text.Length -and $Text[$probe] -eq "`n") {
        $end = $probe + 1
    }

    return [pscustomobject]@{
        Start = $start
        End = $end
    }
}

function Get-RunlayerRemovedCommaPositions {
    param(
        [Parameter(Mandatory = $true)][object]$Node,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][object[]]$Elements,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][bool[]]$Removed
    )

    # A removed element takes its following separator. If a removed tail had
    # no original trailing comma, its preceding kept separator also goes.
    # Otherwise that separator becomes trailing and the old trailing comma
    # goes with the removed last element.
    $removedCommas = @{}
    $laterKept = New-Object bool[] $Elements.Count
    $seenKept = $false
    for ($index = $Elements.Count - 1; $index -ge 0; $index--) {
        $laterKept[$index] = $seenKept
        if (-not $Removed[$index]) {
            $seenKept = $true
        }
    }
    for ($index = 0; $index -lt $Elements.Count; $index++) {
        $comma = [int]$Elements[$index].CommaAfter
        if ($comma -lt 0) {
            continue
        }
        if (
            $Removed[$index] -or
            (-not $laterKept[$index] -and [int]$Node.TrailingComma -lt 0)
        ) {
            $removedCommas[[string]$comma] = $true
        }
    }
    if (
        [int]$Node.TrailingComma -ge 0 -and
        $Removed[$Elements.Count - 1]
    ) {
        $removedCommas[[string][int]$Node.TrailingComma] = $true
    }
    return $removedCommas
}

function Add-RunlayerJsonContainerRemovalRanges {
    param(
        [Parameter(Mandatory = $true)][object]$Node,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][object[]]$Elements,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][bool[]]$Removed,
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][object]$Layout,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][object[]]$Comments,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems,
        [Parameter(Mandatory = $true)][object]$Ranges
    )

    if ($Elements.Count -eq 0) {
        return
    }
    $removedCommas = Get-RunlayerRemovedCommaPositions -Node $Node `
        -Elements $Elements -Removed $Removed

    for ($index = 0; $index -lt $Elements.Count; $index++) {
        if (-not $Removed[$index]) {
            continue
        }
        $expanded = Get-RunlayerExpandedJsonElementRange -Text $Text `
            -Layout $Layout -Element $Elements[$index] `
            -RemovedCommas $removedCommas
        Add-RunlayerUncommentedRemovalRange -Ranges $Ranges `
            -Comments $Comments -Start $expanded.Start -End $expanded.End
    }
    foreach ($position in $removedCommas.Keys) {
        Add-RunlayerUncommentedRemovalRange -Ranges $Ranges `
            -Comments $Comments -Start ([int]$position) -End ([int]$position + 1)
    }

    for ($index = 0; $index -lt $Elements.Count; $index++) {
        if ($Removed[$index]) {
            continue
        }
        if ($Node.Kind -eq "Object") {
            $child = $Elements[$index].Value
        } else {
            $child = $Elements[$index]
        }
        Add-RunlayerJsonNodeRemovalRanges -Node $child -Text $Text `
            -Layout $Layout `
            -Comments $Comments -RemovedProperties $RemovedProperties `
            -RemovedItems $RemovedItems -Ranges $Ranges
    }
}

function Add-RunlayerJsonNodeRemovalRanges {
    param(
        [Parameter(Mandatory = $true)][object]$Node,
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][object]$Layout,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][object[]]$Comments,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems,
        [Parameter(Mandatory = $true)][object]$Ranges
    )

    if ($Node.Kind -eq "Object") {
        $elements = [object[]]$Node.Properties
        $removed = New-Object bool[] $elements.Count
        for ($index = 0; $index -lt $elements.Count; $index++) {
            $removed[$index] = Test-RunlayerJsonSpanMarked `
                -Marks $RemovedProperties -Id $elements[$index].Id
        }
        Add-RunlayerJsonContainerRemovalRanges -Node $Node `
            -Elements $elements -Removed $removed -Text $Text `
            -Layout $Layout `
            -Comments $Comments -RemovedProperties $RemovedProperties `
            -RemovedItems $RemovedItems -Ranges $Ranges
        return
    }
    if ($Node.Kind -eq "Array") {
        $elements = [object[]]$Node.Items
        $removed = New-Object bool[] $elements.Count
        for ($index = 0; $index -lt $elements.Count; $index++) {
            $removed[$index] = Test-RunlayerJsonSpanMarked `
                -Marks $RemovedItems -Id $elements[$index].Id
        }
        Add-RunlayerJsonContainerRemovalRanges -Node $Node `
            -Elements $elements -Removed $removed -Text $Text `
            -Layout $Layout `
            -Comments $Comments -RemovedProperties $RemovedProperties `
            -RemovedItems $RemovedItems -Ranges $Ranges
    }
}

function Remove-RunlayerTextRanges {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyString()][string]$Text,
        [Parameter(Mandatory = $true)][object[]]$Ranges
    )

    $ordered = @($Ranges | Sort-Object Start, End)
    $merged = [System.Collections.Generic.List[object]]::new()
    foreach ($range in $ordered) {
        $start = [int]$range.Start
        $end = [int]$range.End
        if ($start -lt 0 -or $end -le $start -or $end -gt $Text.Length) {
            throw "invalid JSON removal range"
        }
        if (
            $merged.Count -gt 0 -and
            $start -le $merged[$merged.Count - 1].End
        ) {
            if ($end -gt $merged[$merged.Count - 1].End) {
                $merged[$merged.Count - 1].End = $end
            }
            continue
        }
        [void]$merged.Add([pscustomobject]@{
            Start = $start
            End = $end
        })
    }

    $builder = [System.Text.StringBuilder]::new()
    $cursor = 0
    foreach ($range in $merged) {
        [void]$builder.Append(
            $Text.Substring($cursor, $range.Start - $cursor)
        )
        $cursor = $range.End
    }
    [void]$builder.Append($Text.Substring($cursor))
    return $builder.ToString()
}

function Test-RunlayerJsonProjection {
    param(
        [Parameter(Mandatory = $true)][object]$Loaded,
        [Parameter(Mandatory = $true)][string]$Candidate,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems
    )

    try {
        $expectedText = ConvertTo-RunlayerProjectedStrictJson `
            -Node $Loaded.Root -ScrubbedText $Loaded.ScrubbedText `
            -RemovedProperties $RemovedProperties -RemovedItems $RemovedItems
        $expected = ConvertFrom-Json -InputObject $expectedText `
            -ErrorAction Stop
        $candidateScrubbed = ConvertTo-RunlayerJsoncScrubbedText `
            -Text $Candidate
        $actual = ConvertFrom-Json -InputObject $candidateScrubbed.Text `
            -ErrorAction Stop
        if (
            -not (Test-RunlayerJsonObject -Value $expected) -or
            -not (Test-RunlayerJsonObject -Value $actual)
        ) {
            return $false
        }
        $expectedCanonical = ConvertTo-Json -InputObject $expected `
            -Depth 100 -Compress
        $actualCanonical = ConvertTo-Json -InputObject $actual `
            -Depth 100 -Compress
        return $expectedCanonical -ceq $actualCanonical
    } catch {
        return $false
    }
}

function Get-RunlayerJsonProjectionCandidate {
    param(
        [Parameter(Mandatory = $true)][object]$Loaded,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems
    )

    $ranges = [System.Collections.Generic.List[object]]::new()
    $layout = Get-RunlayerTextLayout -Text $Loaded.Text
    Add-RunlayerJsonNodeRemovalRanges -Node $Loaded.Root -Text $Loaded.Text `
        -Layout $layout `
        -Comments $Loaded.Comments -RemovedProperties $RemovedProperties `
        -RemovedItems $RemovedItems -Ranges $ranges
    if ($ranges.Count -eq 0) {
        throw "projection changed without a textual removal"
    }
    return Remove-RunlayerTextRanges -Text $Loaded.Text `
        -Ranges ([object[]]$ranges.ToArray())
}

function Write-RunlayerJsonProjection {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][object]$Loaded,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties,
        [Parameter(Mandatory = $true)][hashtable]$RemovedItems
    )

    try {
        $candidate = Get-RunlayerJsonProjectionCandidate -Loaded $Loaded `
            -RemovedProperties $RemovedProperties -RemovedItems $RemovedItems
        if (
            $candidate -ceq $Loaded.Text -or
            -not (
                Test-RunlayerJsonProjection -Loaded $Loaded `
                    -Candidate $candidate `
                    -RemovedProperties $RemovedProperties `
                    -RemovedItems $RemovedItems
            )
        ) {
            throw "candidate does not match the projected JSON tree"
        }
    } catch {
        Write-RunlayerHookCleanupLog "JSON projection verification failed for $Path"
        return $false
    }

    if (
        -not (
            Backup-RunlayerFile -Path $Path `
                -ExpectedSnapshot $Loaded.Snapshot
        )
    ) {
        return $false
    }
    if (
        Set-RunlayerAtomicTextFile -Path $Path -Text $candidate `
            -ExpectedSnapshot $Loaded.Snapshot
    ) {
        Write-RunlayerHookCleanupLog "updated $Path"
        return $true
    }
    return $false
}

function Test-RunlayerJsonProjectionClean {
    param(
        [Parameter(Mandatory = $true)][object]$Root,
        [Parameter(Mandatory = $true)][hashtable]$RemovedProperties
    )

    foreach ($property in $Root.Properties) {
        if (
            Test-RunlayerJsonSpanMarked -Marks $RemovedProperties `
                -Id $property.Id
        ) {
            continue
        }
        if (
            [string]::Equals(
                [string]$property.Name,
                "version",
                [System.StringComparison]::OrdinalIgnoreCase
            )
        ) {
            continue
        }
        if (
            [string]::Equals(
                [string]$property.Name,
                "hooks",
                [System.StringComparison]::OrdinalIgnoreCase
            ) -and
            $property.Value.Kind -eq "Object" -and
            (
                Get-RunlayerJsonProjectedPropertyCount `
                    -ObjectNode $property.Value `
                    -RemovedProperties $RemovedProperties
            ) -eq 0
        ) {
            continue
        }
        return $false
    }
    return $true
}

function Remove-RunlayerBackedFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [string]$Outcome = "deleted",
        [AllowNull()][object]$ExpectedSnapshot
    )

    if ($null -eq $ExpectedSnapshot) {
        $state = Get-RunlayerFileState -Path $Path
        if (-not $state.Exists -or -not $state.Readable) {
            return $false
        }
        $ExpectedSnapshot = $state.Snapshot
    }
    if (-not (Test-RunlayerFileSnapshot -Path $Path -Snapshot $ExpectedSnapshot)) {
        Write-RunlayerHookCleanupLog "delete skipped changed or unsafe file $Path"
        return $false
    }
    if (-not (Backup-RunlayerFile -Path $Path -ExpectedSnapshot $ExpectedSnapshot)) {
        return $false
    }
    try {
        if (-not (Test-RunlayerFileSnapshot -Path $Path -Snapshot $ExpectedSnapshot)) {
            throw "file changed before deletion"
        }
        Remove-Item -LiteralPath $Path -Force -ErrorAction Stop
        Write-RunlayerHookCleanupLog "$Outcome $Path"
        return $true
    } catch {
        Write-RunlayerHookCleanupLog "delete failed for $Path"
        return $false
    }
}

function Remove-RunlayerJsonHooks {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [switch]$DeleteWhenClean
    )

    $loaded = Get-RunlayerJsonDocument -Path $Path
    if (-not $loaded.Success) {
        return $false
    }
    $hooksProperties = @(
        Get-RunlayerJsonSpanProperties -ObjectNode $loaded.Root -Name "hooks"
    )
    if ($hooksProperties.Count -eq 0) {
        return $false
    }
    if ($hooksProperties.Count -gt 1) {
        Write-RunlayerHookCleanupLog "skipped ambiguous hooks properties $Path"
        return $false
    }
    $hooksProperty = $hooksProperties[0]
    if ($hooksProperty.Value.Kind -ne "Object") {
        Write-RunlayerHookCleanupLog "skipped invalid hooks object $Path"
        return $false
    }
    if (
        -not (
            Test-RunlayerHooksObjectSpanUnambiguous `
                -HooksNode $hooksProperty.Value
        )
    ) {
        Write-RunlayerHookCleanupLog "skipped ambiguous hook entries $Path"
        return $false
    }

    $removedProperties = @{}
    $removedItems = @{}
    $changed = Set-RunlayerHooksObjectSpanProjection `
        -HooksNode $hooksProperty.Value `
        -RemovedProperties $removedProperties -RemovedItems $removedItems
    if (-not $changed) {
        return $false
    }
    if (
        (
            Get-RunlayerJsonProjectedPropertyCount `
                -ObjectNode $hooksProperty.Value `
                -RemovedProperties $removedProperties
        ) -eq 0
    ) {
        Set-RunlayerJsonSpanMarked -Marks $removedProperties `
            -Id $hooksProperty.Id
    }

    if (
        $DeleteWhenClean -and
        (
            Test-RunlayerJsonProjectionClean -Root $loaded.Root `
                -RemovedProperties $removedProperties
        )
    ) {
        return Remove-RunlayerBackedFile -Path $Path `
            -ExpectedSnapshot $loaded.Snapshot
    }
    return Write-RunlayerJsonProjection -Path $Path -Loaded $loaded `
        -RemovedProperties $removedProperties -RemovedItems $removedItems
}

function Remove-RunlayerVscodeLocations {
    param([Parameter(Mandatory = $true)][string]$Path)

    $loaded = Get-RunlayerJsonDocument -Path $Path
    if (-not $loaded.Success) {
        return $false
    }
    $locationsProperties = @(
        Get-RunlayerJsonSpanProperties -ObjectNode $loaded.Root `
            -Name "chat.hookFilesLocations"
    )
    if ($locationsProperties.Count -eq 0) {
        return $false
    }
    if ($locationsProperties.Count -gt 1) {
        Write-RunlayerHookCleanupLog "skipped ambiguous VS Code locations $Path"
        return $false
    }
    $locationsProperty = $locationsProperties[0]
    if ($locationsProperty.Value.Kind -ne "Object") {
        return $false
    }

    $expected = [ordered]@{
        "~/.copilot/hooks" = $true
        ".claude/settings.json" = $false
        ".claude/settings.local.json" = $false
        "~/.claude/settings.json" = $false
    }
    if (
        -not (
            Test-RunlayerJsonSpanPropertyNamesUnique `
                -ObjectNode $locationsProperty.Value `
                -Names ([string[]]$expected.Keys)
        )
    ) {
        Write-RunlayerHookCleanupLog "skipped ambiguous VS Code locations $Path"
        return $false
    }
    $removedProperties = @{}
    $removedItems = @{}
    $changed = $false
    foreach ($name in $expected.Keys) {
        $property = Get-RunlayerJsonSpanProperty `
            -ObjectNode $locationsProperty.Value -Name $name
        if (
            $null -eq $property -or
            $property.Value.Kind -ne "Primitive"
        ) {
            continue
        }
        $value = $property.Value.Decoded
        if ($value -is [bool] -and $value -eq $expected[$name]) {
            Set-RunlayerJsonSpanMarked -Marks $removedProperties `
                -Id $property.Id
            $changed = $true
        }
    }
    if (-not $changed) {
        return $false
    }
    if (
        (
            Get-RunlayerJsonProjectedPropertyCount `
                -ObjectNode $locationsProperty.Value `
                -RemovedProperties $removedProperties
        ) -eq 0
    ) {
        Set-RunlayerJsonSpanMarked -Marks $removedProperties `
            -Id $locationsProperty.Id
    }
    return Write-RunlayerJsonProjection -Path $Path -Loaded $loaded `
        -RemovedProperties $removedProperties -RemovedItems $removedItems
}

function Remove-RunlayerHermesYaml {
    param([Parameter(Mandatory = $true)][string]$Path)

    $state = Get-RunlayerFileState -Path $Path
    if (-not $state.Exists -or -not $state.Readable) {
        return $false
    }
    $newline = if ($state.Text.Contains("`r`n")) { "`r`n" } else { "`n" }
    $hadTrailingNewline = $state.Text.EndsWith("`n")
    $lines = [regex]::Split($state.Text, "\r?\n")
    if ($hadTrailingNewline -and $lines.Count -gt 0 -and $lines[-1] -eq "") {
        $lines = $lines[0..($lines.Count - 2)]
    }

    $hooksStart = -1
    $hooksIndent = 0
    for ($index = 0; $index -lt $lines.Count; $index++) {
        if ($lines[$index] -match "^(?<indent>\s*)hooks\s*:\s*(?:#.*)?$") {
            $hooksStart = $index
            $hooksIndent = $Matches["indent"].Length
            break
        }
    }
    if ($hooksStart -lt 0) {
        return $false
    }

    $hooksEnd = $lines.Count
    for ($index = $hooksStart + 1; $index -lt $lines.Count; $index++) {
        if ($lines[$index] -match "^\s*(?:#.*)?$") {
            continue
        }
        $indent = ([regex]::Match($lines[$index], "^\s*")).Value.Length
        if ($indent -le $hooksIndent) {
            $hooksEnd = $index
            break
        }
    }

    $remove = New-Object bool[] $lines.Count
    $changed = $false
    $index = $hooksStart + 1
    while ($index -lt $hooksEnd) {
        $itemMatch = [regex]::Match($lines[$index], "^(?<indent>\s*)-\s*(?<body>.*)$")
        if (-not $itemMatch.Success) {
            $index++
            continue
        }
        $itemIndent = $itemMatch.Groups["indent"].Value.Length
        $itemEnd = $index + 1
        while ($itemEnd -lt $hooksEnd) {
            $line = $lines[$itemEnd]
            if ($line -match "^\s*(?:#.*)?$") {
                $itemEnd++
                continue
            }
            $lineIndent = ([regex]::Match($line, "^\s*")).Value.Length
            if (
                $lineIndent -lt $itemIndent -or
                ($lineIndent -eq $itemIndent -and $line -match "^\s*(?:-|[^#\s][^:]*:)")
            ) {
                break
            }
            $itemEnd++
        }

        $owned = $false
        for ($probe = $index; $probe -lt $itemEnd; $probe++) {
            if (
                $lines[$probe] -match "^\s*(?:-\s*)?command\s*:\s*(?<command>.+?)\s*$" -and
                (Test-RunlayerCommand -Command $Matches["command"])
            ) {
                $owned = $true
                break
            }
        }
        if ($owned) {
            for ($probe = $index; $probe -lt $itemEnd; $probe++) {
                $remove[$probe] = $true
            }
            $changed = $true
        }
        $index = $itemEnd
    }
    if (-not $changed) {
        return $false
    }

    $kept = @()
    for ($index = 0; $index -lt $lines.Count; $index++) {
        if (-not $remove[$index]) {
            $kept += $lines[$index]
        }
    }

    # Remove event keys left with no sequence entries, then remove an empty
    # top-level hooks section. The generated Hermes shape has one command-only
    # sequence item per event; comments and unknown YAML are preserved.
    $lines = $kept
    $remove = New-Object bool[] $lines.Count
    $hooksStart = [array]::IndexOf(
        $lines,
        ($lines | Where-Object { $_ -match "^(?<indent>\s*)hooks\s*:\s*(?:#.*)?$" } |
            Select-Object -First 1)
    )
    if ($hooksStart -ge 0) {
        $hooksIndent = ([regex]::Match($lines[$hooksStart], "^\s*")).Value.Length
        $hooksEnd = $lines.Count
        for ($index = $hooksStart + 1; $index -lt $lines.Count; $index++) {
            if ($lines[$index] -match "^\s*(?:#.*)?$") {
                continue
            }
            $indent = ([regex]::Match($lines[$index], "^\s*")).Value.Length
            if ($indent -le $hooksIndent) {
                $hooksEnd = $index
                break
            }
        }

        $index = $hooksStart + 1
        while ($index -lt $hooksEnd) {
            if ($lines[$index] -notmatch "^(?<indent>\s*)[^#\s-][^:]*:\s*(?:#.*)?$") {
                $index++
                continue
            }
            $eventIndent = $Matches["indent"].Length
            $eventEnd = $index + 1
            while ($eventEnd -lt $hooksEnd) {
                if ($lines[$eventEnd] -match "^\s*(?:#.*)?$") {
                    $eventEnd++
                    continue
                }
                $eventLineIndent = (
                    [regex]::Match($lines[$eventEnd], "^\s*")
                ).Value.Length
                if (
                    $eventLineIndent -lt $eventIndent -or
                    (
                        $eventLineIndent -eq $eventIndent -and
                        $lines[$eventEnd] -notmatch "^\s*-"
                    )
                ) {
                    break
                }
                $eventEnd++
            }
            $hasContent = $false
            for ($probe = $index + 1; $probe -lt $eventEnd; $probe++) {
                if ($lines[$probe] -notmatch "^\s*$") {
                    $hasContent = $true
                    break
                }
            }
            if (-not $hasContent) {
                $remove[$index] = $true
            }
            $index = $eventEnd
        }

        $hasHooksContent = $false
        for ($probe = $hooksStart + 1; $probe -lt $hooksEnd; $probe++) {
            if (-not $remove[$probe] -and $lines[$probe] -notmatch "^\s*$") {
                $hasHooksContent = $true
                break
            }
        }
        if (-not $hasHooksContent) {
            $remove[$hooksStart] = $true
        }
    }

    $finalLines = @()
    for ($index = 0; $index -lt $lines.Count; $index++) {
        if (-not $remove[$index]) {
            $finalLines += $lines[$index]
        }
    }
    $rendered = $finalLines -join $newline
    if ($hadTrailingNewline -and -not $rendered.EndsWith($newline)) {
        $rendered += $newline
    }
    if ($rendered -eq $state.Text) {
        return $false
    }
    if (
        -not (
            Backup-RunlayerFile -Path $Path `
                -ExpectedSnapshot $state.Snapshot
        )
    ) {
        return $false
    }
    if (
        Set-RunlayerAtomicTextFile -Path $Path -Text $rendered `
            -ExpectedSnapshot $state.Snapshot
    ) {
        Write-RunlayerHookCleanupLog "updated $Path"
        return $true
    }
    return $false
}

function Remove-RunlayerIgnoreBlock {
    param([Parameter(Mandatory = $true)][string]$Path)

    $state = Get-RunlayerFileState -Path $Path
    if (-not $state.Exists -or -not $state.Readable) {
        return $false
    }
    $lines = @(
        [regex]::Matches($state.Text, "[^\r\n]*(?:\r\n|\n|\r|$)") |
            ForEach-Object {
                if ($_.Length -gt 0) {
                    $_.Value
                }
            }
    )
    $starts = @()
    $ends = @()
    for ($index = 0; $index -lt $lines.Count; $index++) {
        $content = $lines[$index].TrimEnd([char[]]"`r`n")
        if ($content -ceq $script:RunlayerIgnoreMarkerStart) {
            $starts += $index
        }
        if ($content -ceq $script:RunlayerIgnoreMarkerEnd) {
            $ends += $index
        }
    }
    if ($starts.Count -ne 1 -or $ends.Count -ne 1 -or $starts[0] -ge $ends[0]) {
        return $false
    }

    $newline = if ($state.Text.Contains("`r`n")) { "`r`n" } else { "`n" }
    $before = ""
    if ($starts[0] -gt 0) {
        $before = ($lines[0..($starts[0] - 1)] -join "").TrimEnd(
            [char[]]"`r`n"
        )
    }
    $after = ""
    if ($ends[0] -lt $lines.Count - 1) {
        $after = ($lines[($ends[0] + 1)..($lines.Count - 1)] -join "").TrimStart(
            [char[]]"`r`n"
        )
    }
    if ($before -and $after) {
        $rendered = $before + $newline + $newline + $after
    } else {
        $rendered = $before + $after
    }
    if (
        $rendered -and
        ($state.Text.EndsWith("`n") -or $state.Text.EndsWith("`r"))
    ) {
        $rendered = $rendered.TrimEnd([char[]]"`r`n") + $newline
    }
    if ([string]::IsNullOrEmpty($rendered)) {
        return Remove-RunlayerBackedFile -Path $Path `
            -ExpectedSnapshot $state.Snapshot
    }
    if ($rendered -eq $state.Text) {
        return $false
    }
    if (
        -not (
            Backup-RunlayerFile -Path $Path `
                -ExpectedSnapshot $state.Snapshot
        )
    ) {
        return $false
    }
    if (
        Set-RunlayerAtomicTextFile -Path $Path -Text $rendered `
            -ExpectedSnapshot $state.Snapshot
    ) {
        Write-RunlayerHookCleanupLog "updated $Path"
        return $true
    }
    return $false
}

function Test-RunlayerClineScriptOwned {
    param([Parameter(Mandatory = $true)][string]$Text)

    if ($Text.Contains($script:RunlayerOwnedClineMarker)) {
        return $true
    }

    $foundRunlayer = $false
    foreach ($rawLine in ($Text -split "\r?\n")) {
        $line = $rawLine.Trim()
        if (
            [string]::IsNullOrEmpty($line) -or
            $line.StartsWith("#")
        ) {
            continue
        }
        if (
            $line -match '^export\s+(?:HOOK_EVENT_NAME|RUNLAYER_HOOK_CLIENT)=(?:"[^"]*"|''[^'']*''|[A-Za-z0-9_.:-]+)\s*$' -or
            $line -match '^\$env:(?:HOOK_EVENT_NAME|RUNLAYER_HOOK_CLIENT)\s*=\s*(?:"[^"]*"|''[^'']*'')\s*$' -or
            $line -match '^set -(?:e|eu|euo pipefail)$' -or
            $line -match '^Set-StrictMode\s+-Version\s+(?:Latest|[0-9.]+)\s*$' -or
            $line -match '^\$(?:(?:global|script):)?ErrorActionPreference\s*=\s*(?:"Stop"|''Stop'')\s*$'
        ) {
            continue
        }
        if (Test-RunlayerCommand -Command $line) {
            $foundRunlayer = $true
            continue
        }
        return $false
    }
    return $foundRunlayer
}

function Remove-RunlayerClineScripts {
    param([Parameter(Mandatory = $true)][string]$HooksDirectory)

    if (-not (Test-Path -LiteralPath $HooksDirectory -PathType Container)) {
        return 0
    }
    if (-not (Test-RunlayerPathSafe -Path $HooksDirectory)) {
        Write-RunlayerHookCleanupLog "skipped unsafe Cline directory $HooksDirectory"
        return 0
    }

    $removed = 0
    try {
        $files = @(Get-ChildItem -LiteralPath $HooksDirectory -Force -File `
                -ErrorAction Stop)
    } catch {
        Write-RunlayerHookCleanupLog "skipped unreadable Cline directory $HooksDirectory"
        return 0
    }
    foreach ($file in $files) {
        $state = Get-RunlayerFileState -Path $file.FullName
        if (-not $state.Readable) {
            continue
        }
        $owned = Test-RunlayerClineScriptOwned -Text $state.Text
        if (
            $owned -and
            (
                Remove-RunlayerBackedFile -Path $file.FullName `
                    -ExpectedSnapshot $state.Snapshot
            )
        ) {
            $removed++
        }
    }
    return $removed
}

function Remove-RunlayerOwnedTree {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        return 0
    }
    if (-not (Test-RunlayerPathSafe -Path $Path)) {
        Write-RunlayerHookCleanupLog "skipped unsafe owned directory $Path"
        return 0
    }

    $removed = 0
    try {
        $children = @(Get-ChildItem -LiteralPath $Path -Force -ErrorAction Stop)
    } catch {
        Write-RunlayerHookCleanupLog "skipped unreadable owned directory $Path"
        return 0
    }
    foreach ($child in $children) {
        if (-not (Test-RunlayerPathSafe -Path $child.FullName)) {
            Write-RunlayerHookCleanupLog "skipped reparse point $($child.FullName)"
            continue
        }
        if ($child.PSIsContainer) {
            $removed += Remove-RunlayerOwnedTree -Path $child.FullName
        } elseif (Remove-RunlayerBackedFile -Path $child.FullName) {
            $removed++
        }
    }

    try {
        if (
            (Test-RunlayerPathSafe -Path $Path) -and
            @(Get-ChildItem -LiteralPath $Path -Force -ErrorAction Stop).Count -eq 0
        ) {
            Remove-Item -LiteralPath $Path -Force -ErrorAction Stop
        }
    } catch {
        # A skipped reparse point or concurrent writer leaves the directory.
    }
    return $removed
}

function Get-RunlayerProfileRoots {
    [CmdletBinding()]
    param(
        [string]$RegistryPath = (
            "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
        )
    )

    $roots = [System.Collections.Generic.List[string]]::new()
    $seen = New-Object "System.Collections.Generic.HashSet[string]" (
        [System.StringComparer]::OrdinalIgnoreCase
    )
    $skipNames = @(
        "Default",
        "Default User",
        "Public",
        "All Users",
        "systemprofile",
        "LocalService",
        "NetworkService"
    )

    try {
        $profiles = @(Get-ChildItem -LiteralPath $RegistryPath -ErrorAction Stop)
    } catch {
        Write-RunlayerHookCleanupLog "ProfileList enumeration failed"
        return @()
    }
    foreach ($profileKey in $profiles) {
        $sid = [string]$profileKey.PSChildName
        if ($sid -notmatch '^S-1-(?:5-21|12-1)(?:-\d+){4}$') {
            continue
        }
        try {
            $properties = Get-ItemProperty -LiteralPath $profileKey.PSPath `
                -Name "ProfileImagePath" -ErrorAction Stop
            $root = [Environment]::ExpandEnvironmentVariables(
                [string]$properties.ProfileImagePath
            )
            if ([string]::IsNullOrWhiteSpace($root)) {
                continue
            }
            $root = [System.IO.Path]::GetFullPath($root)
            if ($skipNames -contains (Split-Path -Leaf $root)) {
                continue
            }
            if (
                (Test-Path -LiteralPath $root -PathType Container) -and
                $seen.Add($root)
            ) {
                [void]$roots.Add($root)
            }
        } catch {
            Write-RunlayerHookCleanupLog "skipped unreadable profile $sid"
        }
    }
    return $roots.ToArray()
}

function Get-RunlayerManagedGrokHome {
    try {
        $value = (
            Get-ItemProperty -LiteralPath "HKLM:\Software\Runlayer\AIWatch" `
                -Name "GrokHome" -ErrorAction Stop
        ).GrokHome
        if ($value -is [string] -and -not [string]::IsNullOrWhiteSpace($value)) {
            return $value
        }
    } catch {
        # Optional and commonly absent (or already removed by MSI sequencing).
    }
    return $null
}

function Resolve-RunlayerManagedUserPath {
    param(
        [Parameter(Mandatory = $true)][string]$ProfileRoot,
        [Parameter(Mandatory = $true)][string]$ConfiguredPath
    )

    try {
        if ($ConfiguredPath -eq "~") {
            $candidate = $ProfileRoot
        } elseif ($ConfiguredPath.StartsWith("~\") -or $ConfiguredPath.StartsWith("~/")) {
            $candidate = Join-Path $ProfileRoot $ConfiguredPath.Substring(2)
        } elseif ($ConfiguredPath.StartsWith("~")) {
            return $null
        } elseif ([System.IO.Path]::IsPathRooted($ConfiguredPath)) {
            $candidate = $ConfiguredPath
        } else {
            $candidate = Join-Path $ProfileRoot $ConfiguredPath
        }

        $root = [System.IO.Path]::GetFullPath($ProfileRoot).TrimEnd("\", "/")
        $resolved = [System.IO.Path]::GetFullPath($candidate)
        if (
            $resolved.Equals($root, [StringComparison]::OrdinalIgnoreCase) -or
            $resolved.StartsWith(
                $root + [System.IO.Path]::DirectorySeparatorChar,
                [StringComparison]::OrdinalIgnoreCase
            )
        ) {
            return $resolved
        }
    } catch {
        return $null
    }
    return $null
}

function Invoke-RunlayerProfileHookCleanup {
    param(
        [Parameter(Mandatory = $true)][string]$ProfileRoot,
        [AllowNull()][string]$ManagedGrokHome
    )

    if (-not (Test-RunlayerPathSafe -Path $ProfileRoot)) {
        Write-RunlayerHookCleanupLog "skipped unsafe profile $ProfileRoot"
        return 0
    }

    $changed = 0
    $jsonFiles = @(
        @{ Parts = @(".cursor", "hooks.json"); OwnedName = $true },
        @{ Parts = @(".copilot", "hooks", "runlayer.json"); OwnedName = $true },
        @{ Parts = @(".claude", "settings.json"); OwnedName = $false },
        @{ Parts = @(".codex", "hooks.json"); OwnedName = $true },
        @{ Parts = @(".copilot", "settings.json"); OwnedName = $false },
        @{ Parts = @(".codeium", "windsurf", "hooks.json"); OwnedName = $true },
        @{ Parts = @(".qwen", "settings.json"); OwnedName = $false },
        @{ Parts = @(".gemini", "settings.json"); OwnedName = $false },
        @{ Parts = @(".grok", "hooks", "runlayer.json"); OwnedName = $true },
        @{ Parts = @("AppData", "Roaming", "devin", "config.json"); OwnedName = $false }
    )
    foreach ($spec in $jsonFiles) {
        $path = Join-RunlayerPath -Root $ProfileRoot -Parts $spec.Parts
        if (Remove-RunlayerJsonHooks -Path $path -DeleteWhenClean:$spec.OwnedName) {
            $changed++
        }
    }

    if (-not [string]::IsNullOrWhiteSpace($ManagedGrokHome)) {
        $grokHome = Resolve-RunlayerManagedUserPath -ProfileRoot $ProfileRoot `
            -ConfiguredPath $ManagedGrokHome
        if ($null -ne $grokHome) {
            $grokPath = Join-RunlayerPath -Root $grokHome `
                -Parts @("hooks", "runlayer.json")
            $defaultGrokPath = Join-RunlayerPath -Root $ProfileRoot `
                -Parts @(".grok", "hooks", "runlayer.json")
            if (
                -not $grokPath.Equals(
                    $defaultGrokPath,
                    [StringComparison]::OrdinalIgnoreCase
                ) -and
                (Remove-RunlayerJsonHooks -Path $grokPath -DeleteWhenClean)
            ) {
                $changed++
            }
        }
    }

    $vscodeSettings = Join-RunlayerPath -Root $ProfileRoot `
        -Parts @("AppData", "Roaming", "Code", "User", "settings.json")
    if (Remove-RunlayerVscodeLocations -Path $vscodeSettings) {
        $changed++
    }

    $hermes = Join-RunlayerPath -Root $ProfileRoot `
        -Parts @(".hermes", "config.yaml")
    if (Remove-RunlayerHermesYaml -Path $hermes) {
        $changed++
    }

    $goose = Join-RunlayerPath -Root $ProfileRoot `
        -Parts @(".agents", "plugins", "runlayer-hooks")
    $changed += Remove-RunlayerOwnedTree -Path $goose

    $cline = Join-RunlayerPath -Root $ProfileRoot -Parts @(".cline", "hooks")
    $changed += Remove-RunlayerClineScripts -HooksDirectory $cline

    foreach ($ignoreName in @(".cursorignore", ".claudeignore")) {
        $path = Join-RunlayerPath -Root $ProfileRoot -Parts @($ignoreName)
        if (Remove-RunlayerIgnoreBlock -Path $path) {
            $changed++
        }
    }

    $legacyFiles = @(
        @(".cursor", "hooks", "runlayer-hook.sh"),
        @(".cursor", "hooks", "runlayer-cursor-hook.sh"),
        @(".cursor", "hooks", "runlayer-config.json"),
        @(".copilot", "hooks", "hooks", "runlayer-hook.sh"),
        @(".copilot", "hooks", "hooks", "runlayer-config.json"),
        @(".claude", "hooks", "runlayer-hook.sh"),
        @(".claude", "hooks", "runlayer-claude-hook.sh"),
        @(".claude", "hooks", "runlayer-config.json"),
        @(".codex", "hooks", "runlayer-hook.sh"),
        @(".codex", "hooks", "runlayer-config.json"),
        @(".hermes", "agent-hooks", "runlayer-hook.sh"),
        @(".hermes", "agent-hooks", "runlayer-config.json"),
        @(".copilot", "hooks", "runlayer-hook.sh"),
        @(".copilot", "hooks", "runlayer-config.json"),
        @(".codeium", "windsurf", "hooks", "runlayer-hook.sh"),
        @(".codeium", "windsurf", "hooks", "runlayer-config.json"),
        @(".gemini", "hooks", "runlayer-hook.sh"),
        @(".gemini", "hooks", "runlayer-config.json"),
        @(".runlayer", "hooks", "runlayer-hook.sh"),
        @(".runlayer", "hooks", "runlayer-config.json")
    )
    foreach ($parts in $legacyFiles) {
        $path = Join-RunlayerPath -Root $ProfileRoot -Parts $parts
        if (Remove-RunlayerBackedFile -Path $path) {
            $changed++
        }
    }
    return $changed
}

function Invoke-RunlayerEnterpriseHookCleanup {
    param(
        [Parameter(Mandatory = $true)][string]$ProgramDataRoot,
        [Parameter(Mandatory = $true)][string]$ProgramFilesRoot
    )

    $changed = 0
    $jsonFiles = @(
        @{
            Root = $ProgramDataRoot
            Parts = @("Cursor", "hooks.json")
            OwnedName = $true
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("GitHub", "Copilot", "policy.d", "runlayer.json")
            OwnedName = $true
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("Windsurf", "hooks.json")
            OwnedName = $true
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("qwen-code", "settings.json")
            OwnedName = $false
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("gemini-cli", "settings.json")
            OwnedName = $false
        },
        @{
            Root = $ProgramFilesRoot
            Parts = @("ClaudeCode", "managed-settings.json")
            OwnedName = $false
        }
    )
    foreach ($spec in $jsonFiles) {
        $path = Join-RunlayerPath -Root $spec.Root -Parts $spec.Parts
        if (Remove-RunlayerJsonHooks -Path $path -DeleteWhenClean:$spec.OwnedName) {
            $changed++
        }
    }

    $legacyFiles = @(
        @{
            Root = $ProgramDataRoot
            Parts = @("Cursor", "hooks", "runlayer-hook.sh")
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("Cursor", "hooks", "runlayer-cursor-hook.sh")
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("Cursor", "hooks", "runlayer-config.json")
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("GitHub", "Copilot", "policy.d", "hooks", "runlayer-hook.sh")
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("GitHub", "Copilot", "policy.d", "hooks", "runlayer-config.json")
        },
        @{
            Root = $ProgramFilesRoot
            Parts = @("ClaudeCode", "hooks", "runlayer-hook.sh")
        },
        @{
            Root = $ProgramFilesRoot
            Parts = @("ClaudeCode", "hooks", "runlayer-claude-hook.sh")
        },
        @{
            Root = $ProgramFilesRoot
            Parts = @("ClaudeCode", "hooks", "runlayer-config.json")
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("Windsurf", "hooks", "runlayer-hook.sh")
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("Windsurf", "hooks", "runlayer-config.json")
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("gemini-cli", "hooks", "runlayer-hook.sh")
        },
        @{
            Root = $ProgramDataRoot
            Parts = @("gemini-cli", "hooks", "runlayer-config.json")
        }
    )
    foreach ($spec in $legacyFiles) {
        $path = Join-RunlayerPath -Root $spec.Root -Parts $spec.Parts
        if (Remove-RunlayerBackedFile -Path $path) {
            $changed++
        }
    }
    return $changed
}

function Invoke-RemoveHooks {
    [CmdletBinding()]
    param(
        [AllowEmptyCollection()][string[]]$ProfileRoots,
        [string]$ProgramDataRoot = $env:ProgramData,
        [string]$ProgramFilesRoot = $env:ProgramFiles,
        [string]$BackupRoot,
        [string]$LogFile
    )

    if ([string]::IsNullOrWhiteSpace($ProgramDataRoot)) {
        $ProgramDataRoot = "C:\ProgramData"
    }
    if ([string]::IsNullOrWhiteSpace($ProgramFilesRoot)) {
        $ProgramFilesRoot = "C:\Program Files"
    }
    if ([string]::IsNullOrWhiteSpace($BackupRoot)) {
        $BackupRoot = Join-RunlayerPath -Root $ProgramDataRoot `
            -Parts @("Runlayer", "Logs", "hook-backups")
    }
    if ([string]::IsNullOrWhiteSpace($LogFile)) {
        $LogFile = Join-RunlayerPath -Root $ProgramDataRoot `
            -Parts @("Runlayer", "Logs", "scheduled-task.log")
    }

    Set-RunlayerHookCleanupContext -BackupRoot $BackupRoot -LogFile $LogFile
    Write-RunlayerHookCleanupLog "starting"

    $changed = 0
    if ($PSBoundParameters.ContainsKey("ProfileRoots")) {
        $roots = @($ProfileRoots)
    } else {
        $roots = @(Get-RunlayerProfileRoots)
    }
    $managedGrokHome = Get-RunlayerManagedGrokHome
    $seen = New-Object "System.Collections.Generic.HashSet[string]" (
        [System.StringComparer]::OrdinalIgnoreCase
    )
    foreach ($profileRoot in $roots) {
        if (
            [string]::IsNullOrWhiteSpace($profileRoot) -or
            -not $seen.Add($profileRoot)
        ) {
            continue
        }
        try {
            $changed += Invoke-RunlayerProfileHookCleanup `
                -ProfileRoot $profileRoot -ManagedGrokHome $managedGrokHome
        } catch {
            Write-RunlayerHookCleanupLog "profile cleanup failed for $profileRoot"
        }
    }

    try {
        $changed += Invoke-RunlayerEnterpriseHookCleanup `
            -ProgramDataRoot $ProgramDataRoot `
            -ProgramFilesRoot $ProgramFilesRoot
    } catch {
        Write-RunlayerHookCleanupLog "enterprise cleanup failed"
    }
    Write-RunlayerHookCleanupLog "done; changed $changed files"
    return $changed
}

# Dot-sourcing loads functions for Pester without touching the machine.
if ($MyInvocation.InvocationName -ne '.') {
    try {
        Invoke-RemoveHooks | Out-Null
    } catch {
        Write-RunlayerHookCleanupLog "unexpected cleanup failure"
    }
    exit 0
}
