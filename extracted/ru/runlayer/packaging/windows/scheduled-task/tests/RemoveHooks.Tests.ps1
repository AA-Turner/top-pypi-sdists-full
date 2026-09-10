#Requires -Version 5.1
# Pester tests for true-uninstall hook cleanup. All filesystem behavior uses
# TestDrive roots; no real profiles or enterprise directories are touched.

BeforeAll {
    $script:TaskDir = Split-Path -Parent $PSScriptRoot
    $script:RemoveHooksScriptPath = Join-Path $script:TaskDir "remove-hooks.ps1"
    . $script:RemoveHooksScriptPath

    function Write-TestJson {
        param(
            [Parameter(Mandatory = $true)][string]$Path,
            [Parameter(Mandatory = $true)][object]$Value
        )

        $parent = Split-Path -Parent $Path
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
        $text = ConvertTo-Json -InputObject $Value -Depth 100
        [System.IO.File]::WriteAllText($Path, $text + [Environment]::NewLine)
    }

    function Write-OwnedHookJson {
        param([Parameter(Mandatory = $true)][string]$Path)

        Write-TestJson -Path $Path -Value ([ordered]@{
            hooks = [ordered]@{
                PreToolUse = @(
                    [ordered]@{
                        command = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
                        args = @("hook", "--client", "test")
                    }
                )
            }
        })
    }

    function Read-TestJson {
        param([Parameter(Mandatory = $true)][string]$Path)

        return ConvertFrom-Json -InputObject (
            [System.IO.File]::ReadAllText($Path)
        )
    }

    function Reset-RemoveHooksTestState {
        $script:RunlayerBackupRoot = Join-Path $TestDrive "backups"
        $script:RunlayerLogFile = Join-Path $TestDrive "scheduled-task.log"
        Remove-Item -LiteralPath $script:RunlayerBackupRoot -Recurse -Force `
            -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $script:RunlayerLogFile -Force `
            -ErrorAction SilentlyContinue
        Set-RunlayerHookCleanupContext `
            -BackupRoot $script:RunlayerBackupRoot `
            -LogFile $script:RunlayerLogFile
    }
}

Describe "Runlayer command and JSON cleanup" {
    BeforeEach { Reset-RemoveHooksTestState }

    It "preserves third-party flat and nested hook entries" {
        $path = Join-Path $TestDrive "settings.json"
        Write-TestJson -Path $path -Value ([ordered]@{
            theme = "dark"
            hooks = [ordered]@{
                PreToolUse = @(
                    [ordered]@{
                        type = "command"
                        command = "C:\Acme\hook.exe"
                    },
                    [ordered]@{
                        type = "command"
                        command = "C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
                        args = @("hook", "--client", "claude_code")
                    },
                    [ordered]@{
                        matcher = ""
                        hooks = @(
                            [ordered]@{
                                type = "command"
                                command = "C:\Runlayer\aiwatch-hook.exe"
                                args = @("hook", "--client", "claude_code")
                            },
                            [ordered]@{
                                type = "command"
                                command = "C:\Acme\nested-hook.exe"
                            }
                        )
                    }
                )
                Stop = @(
                    [ordered]@{
                        type = "command"
                        bash = "/opt/acme/stop"
                        powershell = "& `"C:\Program Files\Runlayer\runlayer.exe`" hook"
                    }
                )
            }
        })

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        $cleaned = Read-TestJson -Path $path
        $cleaned.theme | Should -Be "dark"
        @($cleaned.hooks.PreToolUse).Count | Should -Be 2
        $cleaned.hooks.PreToolUse[0].command | Should -Be "C:\Acme\hook.exe"
        @($cleaned.hooks.PreToolUse[1].hooks).Count | Should -Be 1
        $cleaned.hooks.PreToolUse[1].hooks[0].command |
            Should -Be "C:\Acme\nested-hook.exe"
        @($cleaned.hooks.Stop).Count | Should -Be 1
        $cleaned.hooks.Stop[0].bash | Should -Be "/opt/acme/stop"
        $cleaned.hooks.Stop[0].PSObject.Properties["powershell"] |
            Should -BeNullOrEmpty
    }

    It "skips malformed JSON without a backup or write" {
        $path = Join-Path $TestDrive "malformed.json"
        $original = '{ "hooks": [not-json] }'
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeFalse

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $original
        Test-Path -LiteralPath $script:RunlayerBackupRoot | Should -BeFalse
    }

    It "skips an unterminated JSONC block comment without writing" {
        $path = Join-Path $TestDrive "malformed-comment.json"
        $original = (
            '{"hooks":{"PreToolUse":[' +
            '{"command":"C:\\Runlayer\\aiwatch-hook.exe"}]}} /* unterminated'
        )
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeFalse

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $original
        Test-Path -LiteralPath $script:RunlayerBackupRoot | Should -BeFalse
    }

    It "scrubs JSONC without changing offsets or comment-like strings" {
        $text = (
            "{`n" +
            "  // line comment`n" +
            "  `"url`": `"https://example.com/a//b/*literal*/`",`n" +
            "  `"value`": 1 /* block comment */,`n" +
            "}`n"
        )

        $scrubbed = ConvertTo-RunlayerJsoncScrubbedText -Text $text

        $scrubbed.Text.Length | Should -Be $text.Length
        $scrubbed.Text | Should -Match (
            [regex]::Escape('"https://example.com/a//b/*literal*/"')
        )
        $scrubbed.Text | Should -Not -Match "line comment"
        $scrubbed.Text | Should -Not -Match "block comment"
        $scrubbed.Comments.Count | Should -Be 2
        $scrubbed.TrailingCommas.Count | Should -Be 1
    }

    It "moves across validated JSON strings with escaped delimiters" {
        $text = '"literal \\ and \" and \u0061"tail'
        $position = 0

        Move-RunlayerJsonStringEnd -Text $text -Position ([ref]$position)

        $position | Should -Be $text.IndexOf("tail")
    }

    It "rejects invalid JSON string escapes in the shared scanner" {
        $position = 0

        {
            Move-RunlayerJsonStringEnd -Text '"bad \x escape"' `
                -Position ([ref]$position)
        } | Should -Throw "*invalid JSON escape*"
    }

    It "rejects unterminated JSON strings in the shared scanner" {
        $position = 0

        {
            Move-RunlayerJsonStringEnd -Text '"unterminated' `
                -Position ([ref]$position)
        } | Should -Throw "*unterminated JSON string*"
    }

    It "rejects short JSON unicode escapes in the shared scanner" {
        $position = 0

        {
            Move-RunlayerJsonStringEnd -Text '"short \u12"' `
                -Position ([ref]$position)
        } | Should -Throw "*invalid JSON unicode escape*"
    }

    It "rejects non-hex JSON unicode escapes in the shared scanner" {
        $position = 0

        {
            Move-RunlayerJsonStringEnd -Text '"bad \u12G4"' `
                -Position ([ref]$position)
        } | Should -Throw "*invalid JSON unicode escape*"
    }

    It "detects a trailing comma separated from its close by a comment" {
        $text = '{ "value": 1, /* trailing comment */ }'
        $comma = $text.IndexOf(",")

        $scrubbed = ConvertTo-RunlayerJsoncScrubbedText -Text $text

        $scrubbed.Text.Length | Should -Be $text.Length
        $scrubbed.Text[$comma] | Should -Be " "
        $scrubbed.TrailingCommas.Count | Should -Be 1
        $scrubbed.TrailingCommas.Contains($comma) | Should -BeTrue
        { ConvertFrom-Json -InputObject $scrubbed.Text } |
            Should -Not -Throw
    }

    It "preserves unicode escapes while removing hook entries" {
        $path = Join-Path $TestDrive "unicode-escape.json"
        $original = (
            '{"label":"\u0061","hooks":{"PreToolUse":[' +
            '{"command":"C:\\Runlayer\\aiwatch-hook.exe"},' +
            '{"command":"C:\\Acme\\hook.exe"}]}}'
        )
        $expected = (
            '{"label":"\u0061","hooks":{"PreToolUse":[' +
            '{"command":"C:\\Acme\\hook.exe"}]}}'
        )
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $expected
    }

    It "preserves date-like JSON strings while removing hook entries" {
        $path = Join-Path $TestDrive "date-strings.json"
        $original = (
            '{"legacy":"\/Date(0)\/",' +
            '"iso":"2026-09-03T00:00:00Z","hooks":{"PreToolUse":[' +
            '{"command":"C:\\Runlayer\\aiwatch-hook.exe"},' +
            '{"command":"C:\\Acme\\hook.exe"}]}}'
        )
        $expected = (
            '{"legacy":"\/Date(0)\/",' +
            '"iso":"2026-09-03T00:00:00Z","hooks":{"PreToolUse":[' +
            '{"command":"C:\\Acme\\hook.exe"}]}}'
        )
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $expected
    }

    It "preserves unrelated exact duplicate properties" {
        $path = Join-Path $TestDrive "duplicate-unrelated.json"
        $original = (
            '{"dup":1,"dup":2,"hooks":{"PreToolUse":[' +
            '{"command":"C:\\Runlayer\\aiwatch-hook.exe"}]}}'
        )
        $expected = '{"dup":1,"dup":2}'
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $expected
    }

    It "fails closed on duplicate cleanup-sensitive properties" {
        $path = Join-Path $TestDrive "duplicate-hooks.json"
        $original = (
            '{"hooks":{"PreToolUse":[' +
            '{"command":"C:\\Runlayer\\one.exe"}]},' +
            '"hooks":{"PreToolUse":[' +
            '{"command":"C:\\Runlayer\\two.exe"}]}}'
        )
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeFalse

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $original
        Test-Path -LiteralPath $script:RunlayerBackupRoot | Should -BeFalse
    }

    It "removes VS Code locations from JSONC without rewriting other bytes" {
        $path = Join-Path $TestDrive "settings.json"
        $original = (@(
            '{'
            '  // User formatting and values must survive cleanup.'
            '  "theme": "café <dark> & light",'
            '  "url": "https://example.com/a//b",'
            '  "note": "literal /* text */ stays a string",'
            '  "chat.hookFilesLocations": {'
            '    "~/.copilot/hooks": true,'
            '    /* An unrelated location. */'
            '    "~/acme/hooks": true,'
            '    ".claude/settings.json": false,'
            '  },'
            '}'
            ''
        ) -join "`r`n")
        $expected = (@(
            '{'
            '  // User formatting and values must survive cleanup.'
            '  "theme": "café <dark> & light",'
            '  "url": "https://example.com/a//b",'
            '  "note": "literal /* text */ stays a string",'
            '  "chat.hookFilesLocations": {'
            '    /* An unrelated location. */'
            '    "~/acme/hooks": true,'
            '  },'
            '}'
            ''
        ) -join "`r`n")
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerVscodeLocations -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $expected
    }

    It "removes shared JSONC hooks without reserializing untouched content" {
        $path = Join-Path $TestDrive "settings.json"
        $original = (@(
            '{'
            '  "title": "café <tag> & it''s unchanged",'
            '  /* Hook order is intentional. */'
            '  "hooks": {'
            '    "PreToolUse": ['
            '      { "command": "C:\\Acme\\hook.exe" },'
            '      { "command": "C:\\Runlayer\\aiwatch-hook.exe" },'
            '    ],'
            '  },'
            '  "tail": "https://example.com/a//b",'
            '}'
            ''
        ) -join "`n")
        $expected = (@(
            '{'
            '  "title": "café <tag> & it''s unchanged",'
            '  /* Hook order is intentional. */'
            '  "hooks": {'
            '    "PreToolUse": ['
            '      { "command": "C:\\Acme\\hook.exe" },'
            '    ],'
            '  },'
            '  "tail": "https://example.com/a//b",'
            '}'
            ''
        ) -join "`n")
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $expected
    }

    It "removes hooks from comment-rich JSONC without hanging" {
        $path = Join-Path $TestDrive "comment-rich.jsonc"
        $original = (@(
            '{'
            ' "literal": "quote=\" // /* slash=\\",'
            ' // before hooks'
            ' "hooks": {'
            ' /* before event */'
            ' "PreToolUse": ['
            ' // before owned'
            ' { /* inside */ "command": "C:\\Runlayer\\aiwatch-hook.exe" },'
            ' { "command": "C:\\Acme\\hook.exe" },'
            ' ],'
            ' },'
            '}'
            ''
        ) -join "`n")
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        $result = [System.IO.File]::ReadAllText($path)
        $result | Should -Not -Match "Runlayer"
        $result | Should -Match ([regex]::Escape("// before hooks"))
        $result | Should -Match ([regex]::Escape("/* before event */"))
        $result | Should -Match ([regex]::Escape("// before owned"))
        $result | Should -Match ([regex]::Escape("/* inside */"))
        $scrubbed = ConvertTo-RunlayerJsoncScrubbedText -Text $result
        { ConvertFrom-Json -InputObject $scrubbed.Text } |
            Should -Not -Throw
    }

    It "excises only an owned shell field from a shared hook entry" {
        $path = Join-Path $TestDrive "settings.json"
        $original = (@(
            '{'
            '  "hooks": {'
            '    "Stop": ['
            '      {'
            '        "bash": "/opt/acme/stop",'
            '        "powershell": "& \"C:\\Runlayer\\runlayer.exe\" hook",'
            '        "timeout": 5'
            '      }'
            '    ]'
            '  }'
            '}'
            ''
        ) -join "`n")
        $expected = (@(
            '{'
            '  "hooks": {'
            '    "Stop": ['
            '      {'
            '        "bash": "/opt/acme/stop",'
            '        "timeout": 5'
            '      }'
            '    ]'
            '  }'
            '}'
            ''
        ) -join "`n")
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $expected
    }

    It "preserves a UTF-8 BOM while excising a hook entry" {
        $path = Join-Path $TestDrive "settings.json"
        $original = (@(
            '{'
            '  "hooks": {'
            '    "PreToolUse": ['
            '      { "command": "C:\\Runlayer\\aiwatch-hook.exe" },'
            '      { "command": "C:\\Acme\\hook.exe" }'
            '    ]'
            '  }'
            '}'
            ''
        ) -join "`r`n")
        $expected = (@(
            '{'
            '  "hooks": {'
            '    "PreToolUse": ['
            '      { "command": "C:\\Acme\\hook.exe" }'
            '    ]'
            '  }'
            '}'
            ''
        ) -join "`r`n")
        $encoding = New-Object System.Text.UTF8Encoding($true)
        [System.IO.File]::WriteAllText($path, $original, $encoding)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        $expectedBytes = [byte[]]@(
            @($encoding.GetPreamble()) + @($encoding.GetBytes($expected))
        )
        [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($path)) |
            Should -BeExactly ([Convert]::ToBase64String($expectedBytes))
    }

    It "removes an event whose hook array has one entry" {
        $path = Join-Path $TestDrive "settings.json"
        $original = (@(
            '{'
            '  "owner": "acme",'
            '  "hooks": {'
            '    "PreToolUse": ['
            '      { "command": "C:\\Runlayer\\aiwatch-hook.exe" }'
            '    ]'
            '  }'
            '}'
            ''
        ) -join "`n")
        $expected = (@(
            '{'
            '  "owner": "acme"'
            '}'
            ''
        ) -join "`n")
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $expected
    }

    It "keeps case-insensitive matching from the PowerShell JSON model" {
        $path = Join-Path $TestDrive "settings.json"
        $original = (
            '{"owner":"acme","Hooks":{"PreToolUse":[' +
            '{"Command":"C:\\Runlayer\\aiwatch.exe","Args":["hook"]}]}}'
        )
        $expected = '{"owner":"acme"}'
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $expected
    }

    It "preserves the lack of a trailing newline" {
        $path = Join-Path $TestDrive "settings.json"
        $original = (
            '{"owner":"acme","hooks":{"PreToolUse":[' +
            '{"command":"C:\\Runlayer\\aiwatch-hook.exe"}]}}'
        )
        $expected = '{"owner":"acme"}'
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $expected
    }

    It "keeps compact arrays valid when removing first middle and last entries" {
        $runlayer = '{"command":"C:\\Runlayer\\aiwatch-hook.exe"}'
        $acme1 = '{"command":"C:\\Acme\\one.exe"}'
        $acme2 = '{"command":"C:\\Acme\\two.exe"}'
        $expected = (
            '{"hooks":{"PreToolUse":[' + $acme1 + "," + $acme2 + "]}}"
        )
        $cases = @(
            ("[" + $runlayer + "," + $acme1 + "," + $acme2 + "]")
            ("[" + $acme1 + "," + $runlayer + "," + $acme2 + "]")
            ("[" + $acme1 + "," + $acme2 + "," + $runlayer + "]")
        )

        foreach ($entries in $cases) {
            Reset-RemoveHooksTestState
            $path = Join-Path $TestDrive (
                "compact-{0}.json" -f ([guid]::NewGuid().ToString("N"))
            )
            [System.IO.File]::WriteAllText(
                $path,
                '{"hooks":{"PreToolUse":' + $entries + "}}"
            )

            Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

            [System.IO.File]::ReadAllText($path) |
                Should -BeExactly $expected
        }
    }

    It "fails closed when projection verification rejects the candidate" {
        $path = Join-Path $TestDrive "verification-failure.json"
        $original = (
            '{"owner":"acme","hooks":{"PreToolUse":[' +
            '{"command":"C:\\Runlayer\\aiwatch-hook.exe"}]}}'
        )
        [System.IO.File]::WriteAllText($path, $original)
        Mock Test-RunlayerJsonProjection { return $false }

        Remove-RunlayerJsonHooks -Path $path | Should -BeFalse

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $original
        Test-Path -LiteralPath $script:RunlayerBackupRoot | Should -BeFalse
        Should -Invoke Test-RunlayerJsonProjection -Times 1 -Exactly
    }

    It "backs up the exact original before changing a config" {
        $profileParent = Join-Path $TestDrive "Users"
        $path = Join-RunlayerPath -Root $profileParent `
            -Parts @("alice", ".claude", "settings.json")
        Write-OwnedHookJson -Path $path
        $original = [System.IO.File]::ReadAllText($path)

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue

        $backups = @(
            [System.IO.Directory]::GetFiles(
                $script:RunlayerBackupRoot,
                "*",
                [System.IO.SearchOption]::AllDirectories
            )
        )
        $backups.Count | Should -Be 1
        [System.IO.File]::ReadAllText($backups[0]) |
            Should -BeExactly $original
        $backups[0] | Should -Match "alice"
        $backups[0] | Should -Match "\.claude"
    }

    It "is idempotent and creates no backup for the second pass" {
        $path = Join-Path $TestDrive "hooks.json"
        Write-TestJson -Path $path -Value ([ordered]@{
            owner = "acme"
            hooks = [ordered]@{
                PreToolUse = @(
                    [ordered]@{
                        command = "C:\Program Files\Runlayer\AIWatch\aiwatch-hook.exe"
                    },
                    [ordered]@{ command = "C:\Acme\hook.exe" }
                )
            }
        })

        Remove-RunlayerJsonHooks -Path $path | Should -BeTrue
        $first = [System.IO.File]::ReadAllBytes($path)
        $backupCount = [System.IO.Directory]::GetFiles(
            $script:RunlayerBackupRoot,
            "*",
            [System.IO.SearchOption]::AllDirectories
        ).Count

        Remove-RunlayerJsonHooks -Path $path | Should -BeFalse

        [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($path)) |
            Should -Be ([Convert]::ToBase64String($first))
        [System.IO.Directory]::GetFiles(
            $script:RunlayerBackupRoot,
            "*",
            [System.IO.SearchOption]::AllDirectories
        ).Count | Should -Be $backupCount
    }

    It "deletes a clean Runlayer-named JSON file but preserves mixed content" {
        $owned = Join-Path $TestDrive "runlayer.json"
        Write-OwnedHookJson -Path $owned
        $mixed = Join-Path $TestDrive "mixed-runlayer.json"
        Write-TestJson -Path $mixed -Value ([ordered]@{
            hooks = [ordered]@{
                PreToolUse = @(
                    [ordered]@{ command = "C:\Runlayer\aiwatch-hook.exe" },
                    [ordered]@{ command = "C:\Acme\hook.exe" }
                )
            }
        })

        Remove-RunlayerJsonHooks -Path $owned -DeleteWhenClean |
            Should -BeTrue
        Remove-RunlayerJsonHooks -Path $mixed -DeleteWhenClean |
            Should -BeTrue

        Test-Path -LiteralPath $owned | Should -BeFalse
        (Read-TestJson -Path $mixed).hooks.PreToolUse.command |
            Should -Be "C:\Acme\hook.exe"
    }

    It "leaves unchanged clean files untouched with DeleteWhenClean" {
        $path = Join-Path $TestDrive "hooks.json"
        $original = "{`"version`": 1}`r`n"
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerJsonHooks -Path $path -DeleteWhenClean |
            Should -BeFalse

        Test-Path -LiteralPath $path | Should -BeTrue
        [System.IO.File]::ReadAllText($path) | Should -BeExactly $original
        Test-Path -LiteralPath $script:RunlayerBackupRoot | Should -BeFalse
    }

    It "preserves mixed-owner Cline scripts" {
        $hooks = Join-Path $TestDrive "cline-hooks"
        New-Item -ItemType Directory -Path $hooks | Out-Null
        $path = Join-Path $hooks "PreToolUse.ps1"
        $original = (
            "& `"C:\Acme\audit.exe`"`n" +
            "& `"C:\Program Files\Runlayer\AIWatch\aiwatch.exe`" hook`n"
        )
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerClineScripts -HooksDirectory $hooks | Should -Be 0

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $original
        Test-Path -LiteralPath $script:RunlayerBackupRoot | Should -BeFalse
    }

    It "preserves ignore-file bytes outside the managed block" {
        $path = Join-Path $TestDrive ".cursorignore"
        $original = (
            "  vendor/  `r`n" +
            "# >>> Runlayer managed - do not edit >>>`r`n" +
            ".env`r`n" +
            "# <<< Runlayer managed <<<`r`n" +
            "build/  `r`n"
        )
        [System.IO.File]::WriteAllText($path, $original)

        Remove-RunlayerIgnoreBlock -Path $path | Should -BeTrue

        [System.IO.File]::ReadAllText($path) |
            Should -BeExactly "  vendor/  `r`n`r`nbuild/  `r`n"
    }
}

Describe "backup session protection" {
    BeforeEach {
        Reset-RemoveHooksTestState
        $script:BackupOperationOrder = New-Object System.Collections.Generic.List[string]
    }

    It "protects the session before publication and copying" {
        $path = Join-Path $TestDrive "settings.json"
        [System.IO.File]::WriteAllText($path, "{}")

        Mock New-RunlayerProtectedBackupSessionDirectory {
            param([string]$Path)

            $script:RunlayerBackupSessionRoot | Should -BeNullOrEmpty
            [void]$script:BackupOperationOrder.Add("protect")
            New-Item -ItemType Directory -Path $Path -Force | Out-Null
        }
        Mock Copy-Item {
            [void]$script:BackupOperationOrder.Add("copy")
        }

        Backup-RunlayerFile -Path $path | Should -BeTrue

        $script:BackupOperationOrder.Count | Should -Be 2
        $script:BackupOperationOrder[0] | Should -Be "protect"
        $script:BackupOperationOrder[1] | Should -Be "copy"
        Should -Invoke New-RunlayerProtectedBackupSessionDirectory -Times 1 -Exactly
        Should -Invoke Copy-Item -Times 1 -Exactly
    }

    It "fails closed when backup ACL protection fails" {
        $deletePath = Join-Path $TestDrive "owned.json"
        Write-OwnedHookJson -Path $deletePath
        $deleteOriginal = [System.IO.File]::ReadAllText($deletePath)
        $writePath = Join-Path $TestDrive "mixed.json"
        Write-TestJson -Path $writePath -Value ([ordered]@{
            owner = "acme"
            hooks = [ordered]@{
                PreToolUse = @(
                    [ordered]@{ command = "C:\Runlayer\aiwatch-hook.exe" }
                )
            }
        })
        $writeOriginal = [System.IO.File]::ReadAllText($writePath)

        Mock New-RunlayerProtectedBackupSessionDirectory {
            throw "ACL protection failed"
        }
        Mock Copy-Item {}

        Remove-RunlayerJsonHooks -Path $deletePath -DeleteWhenClean |
            Should -BeFalse
        Remove-RunlayerJsonHooks -Path $writePath | Should -BeFalse

        $script:RunlayerBackupSessionRoot | Should -BeNullOrEmpty
        [System.IO.File]::ReadAllText($deletePath) |
            Should -BeExactly $deleteOriginal
        [System.IO.File]::ReadAllText($writePath) |
            Should -BeExactly $writeOriginal
        Should -Invoke Copy-Item -Times 0 -Exactly
    }

    It "uses protected locale-independent Windows backup ACLs" {
        $text = Get-Content -LiteralPath $script:RemoveHooksScriptPath -Raw

        $text | Should -Match ([regex]::Escape("S-1-5-18"))
        $text | Should -Match ([regex]::Escape("S-1-5-32-544"))
        $text | Should -Match 'SetAccessRuleProtection\(\$true,\s*\$false\)'
        $text | Should -Match '\[System\.IO\.Directory\]::CreateDirectory'
    }
}

Describe "file snapshot revalidation" {
    BeforeEach { Reset-RemoveHooksTestState }

    It "detects content changed after the initial read" {
        $path = Join-Path $TestDrive "settings.json"
        [System.IO.File]::WriteAllText($path, '{"owner":"original"}')
        $state = Get-RunlayerFileState -Path $path
        $state.Readable | Should -BeTrue

        [System.IO.File]::WriteAllText($path, '{"owner":"changed"}')

        Test-RunlayerFileSnapshot -Path $path -Snapshot $state.Snapshot |
            Should -BeFalse
    }

    It "does not delete a file changed after backup" {
        $path = Join-Path $TestDrive "settings.json"
        [System.IO.File]::WriteAllText($path, '{"owner":"original"}')
        $state = Get-RunlayerFileState -Path $path

        Mock Backup-RunlayerFile {
            param([string]$Path)

            [System.IO.File]::WriteAllText($Path, '{"owner":"changed"}')
            return $true
        }

        Remove-RunlayerBackedFile -Path $path `
            -ExpectedSnapshot $state.Snapshot | Should -BeFalse

        Test-Path -LiteralPath $path | Should -BeTrue
        [System.IO.File]::ReadAllText($path) |
            Should -BeExactly '{"owner":"changed"}'
    }

    It "restores the live file when Desktop replacement loses it" {
        $path = Join-Path $TestDrive "replace-failure.json"
        $original = '{"value":"original"}'
        [System.IO.File]::WriteAllText($path, $original)
        $state = Get-RunlayerFileState -Path $path
        Mock Invoke-RunlayerFileReplace {
            param($ReplacementPath, $DestinationPath, $RollbackPath)
            [System.IO.File]::Move($DestinationPath, $RollbackPath)
            throw "simulated partial ReplaceFile failure"
        }

        $edition = $PSVersionTable.PSEdition
        try {
            $PSVersionTable.PSEdition = "Desktop"
            Set-RunlayerAtomicTextFile -Path $path -Text '{"value":"new"}' `
                -ExpectedSnapshot $state.Snapshot | Should -BeFalse
        } finally {
            $PSVersionTable.PSEdition = $edition
        }

        [System.IO.File]::ReadAllText($path) | Should -BeExactly $original
        Assert-MockCalled Invoke-RunlayerFileReplace -Times 1 -Exactly
    }
}

Describe "profile discovery" {
    BeforeEach { Reset-RemoveHooksTestState }

    It "accepts local and Entra ProfileList users and skips service/default profiles" {
        $local = Join-Path $TestDrive "alice"
        $entra = Join-Path $TestDrive "entra"
        $default = Join-Path $TestDrive "Default"
        New-Item -ItemType Directory -Path $local, $entra, $default | Out-Null
        $registryPath = "HKLM:\Test\ProfileList"
        $profiles = @(
            [pscustomobject]@{
                PSChildName = "S-1-5-21-1-2-3-1001"
                PSPath = "local"
            },
            [pscustomobject]@{
                PSChildName = "S-1-12-1-1-2-3-4"
                PSPath = "entra"
            },
            [pscustomobject]@{
                PSChildName = "S-1-5-18"
                PSPath = "system"
            },
            [pscustomobject]@{
                PSChildName = "S-1-5-21-9-8-7-1002"
                PSPath = "default"
            }
        )
        Mock Get-ChildItem { $profiles } -ParameterFilter {
            $LiteralPath -eq $registryPath
        }
        Mock Get-ItemProperty {
            switch ($LiteralPath) {
                "local" { [pscustomobject]@{ ProfileImagePath = $local } }
                "entra" { [pscustomobject]@{ ProfileImagePath = $entra } }
                "default" { [pscustomobject]@{ ProfileImagePath = $default } }
                default { throw "service SID must not be read" }
            }
        }

        $roots = @(Get-RunlayerProfileRoots -RegistryPath $registryPath)

        $roots.Count | Should -Be 2
        $roots | Should -Contain ([System.IO.Path]::GetFullPath($local))
        $roots | Should -Contain ([System.IO.Path]::GetFullPath($entra))
        Should -Invoke Get-ItemProperty -Times 0 -Exactly -ParameterFilter {
            $LiteralPath -eq "system"
        }
    }
}

Describe "full profile and enterprise sweep" {
    BeforeEach { Reset-RemoveHooksTestState }

    It "covers all 13 clients, every supplied profile, and enterprise roots" {
        $programData = Join-Path $TestDrive "ProgramData"
        $programFiles = Join-Path $TestDrive "Program Files"
        $alice = Join-RunlayerPath -Root $TestDrive -Parts @("Users", "alice")
        $entra = Join-RunlayerPath -Root $TestDrive -Parts @("Users", "entra")
        New-Item -ItemType Directory -Path $programData, $programFiles, $alice, $entra `
            -Force | Out-Null

        # Cursor, VS Code, Claude Code, Codex, Copilot CLI, Windsurf, Qwen,
        # Gemini, Grok, and Devin JSON surfaces.
        $profileJson = @(
            @(".cursor", "hooks.json"),
            @(".copilot", "hooks", "runlayer.json"),
            @(".claude", "settings.json"),
            @(".codex", "hooks.json"),
            @(".copilot", "settings.json"),
            @(".codeium", "windsurf", "hooks.json"),
            @(".qwen", "settings.json"),
            @(".gemini", "settings.json"),
            @(".grok", "hooks", "runlayer.json"),
            @("AppData", "Roaming", "devin", "config.json")
        )
        $ownedProfileJson = @(
            ".cursor/hooks.json",
            ".copilot/hooks/runlayer.json",
            ".codex/hooks.json",
            ".codeium/windsurf/hooks.json",
            ".grok/hooks/runlayer.json"
        )
        foreach ($parts in $profileJson) {
            Write-OwnedHookJson -Path (
                Join-RunlayerPath -Root $alice -Parts $parts
            )
        }
        Write-OwnedHookJson -Path (
            Join-RunlayerPath -Root $entra -Parts @(".cursor", "hooks.json")
        )

        # Hermes YAML.
        $hermes = Join-RunlayerPath -Root $alice `
            -Parts @(".hermes", "config.yaml")
        New-Item -ItemType Directory -Path (Split-Path -Parent $hermes) `
            -Force | Out-Null
        [System.IO.File]::WriteAllText(
            $hermes,
            (
                "model: auto`n" +
                "hooks:`n" +
                "  pre_tool_call:`n" +
                "  - command: C:\Program Files\Runlayer\AIWatch\aiwatch.exe hook --client hermes`n" +
                "  - command: C:\Acme\hermes-hook.exe`n"
            )
        )

        # Goose's plugin tree is wholly owned.
        $goose = Join-RunlayerPath -Root $alice `
            -Parts @(".agents", "plugins", "runlayer-hooks")
        Write-TestJson -Path (Join-RunlayerPath -Root $goose -Parts @("plugin.json")) `
            -Value @{ name = "runlayer-hooks" }
        Write-OwnedHookJson -Path (
            Join-RunlayerPath -Root $goose -Parts @("hooks", "hooks.json")
        )

        # Cline's marker-owned script.
        $cline = Join-RunlayerPath -Root $alice `
            -Parts @(".cline", "hooks", "PreToolUse.ps1")
        New-Item -ItemType Directory -Path (Split-Path -Parent $cline) `
            -Force | Out-Null
        [System.IO.File]::WriteAllText(
            $cline,
            "# runlayer-owned Cline hook - safe to delete`n& aiwatch.exe hook`n"
        )

        $legacyShim = Join-RunlayerPath -Root $alice `
            -Parts @(".claude", "hooks", "runlayer-hook.sh")
        New-Item -ItemType Directory -Path (Split-Path -Parent $legacyShim) `
            -Force | Out-Null
        [System.IO.File]::WriteAllText($legacyShim, "# legacy Runlayer shim`n")

        # VS Code's managed hook-file location map.
        $vscodeSettings = Join-RunlayerPath -Root $alice `
            -Parts @("AppData", "Roaming", "Code", "User", "settings.json")
        Write-TestJson -Path $vscodeSettings -Value ([ordered]@{
            "chat.hookFilesLocations" = [ordered]@{
                "~/.copilot/hooks" = $true
                ".claude/settings.json" = $false
                "~/acme/hooks" = $true
            }
        })

        # Managed ignore blocks.
        foreach ($name in @(".cursorignore", ".claudeignore")) {
            $ignore = Join-RunlayerPath -Root $alice -Parts @($name)
            [System.IO.File]::WriteAllText(
                $ignore,
                "vendor/`n`n# >>> Runlayer managed - do not edit >>>`n.env`n# <<< Runlayer managed <<<`n"
            )
        }

        # Codex hook enablement belongs to the client and must remain.
        $codexToml = Join-RunlayerPath -Root $alice `
            -Parts @(".codex", "config.toml")
        [System.IO.File]::WriteAllText(
            $codexToml,
            "[features]`nhooks = true`n"
        )

        $enterpriseJson = @(
            @{
                Root = $programData
                Parts = @("Cursor", "hooks.json")
                OwnedName = $true
            },
            @{
                Root = $programData
                Parts = @("GitHub", "Copilot", "policy.d", "runlayer.json")
                OwnedName = $true
            },
            @{
                Root = $programData
                Parts = @("Windsurf", "hooks.json")
                OwnedName = $true
            },
            @{
                Root = $programData
                Parts = @("qwen-code", "settings.json")
                OwnedName = $false
            },
            @{
                Root = $programData
                Parts = @("gemini-cli", "settings.json")
                OwnedName = $false
            },
            @{
                Root = $programFiles
                Parts = @("ClaudeCode", "managed-settings.json")
                OwnedName = $false
            }
        )
        foreach ($spec in $enterpriseJson) {
            Write-OwnedHookJson -Path (
                Join-RunlayerPath -Root $spec.Root -Parts $spec.Parts
            )
        }

        $legacyFiles = @(
            @{ Root = $alice; Parts = @(".codeium", "windsurf", "hooks", "runlayer-hook.sh") },
            @{ Root = $alice; Parts = @(".gemini", "hooks", "runlayer-hook.sh") },
            @{ Root = $alice; Parts = @(".runlayer", "hooks", "runlayer-hook.sh") },
            @{ Root = $programData; Parts = @("Windsurf", "hooks", "runlayer-hook.sh") },
            @{ Root = $programData; Parts = @("gemini-cli", "hooks", "runlayer-hook.sh") }
        )
        foreach ($spec in $legacyFiles) {
            $path = Join-RunlayerPath -Root $spec.Root -Parts $spec.Parts
            New-Item -ItemType Directory -Path (Split-Path -Parent $path) `
                -Force | Out-Null
            [System.IO.File]::WriteAllText($path, "#!/bin/sh`naiwatch hook`n")
        }

        # Windows browser policy is intentionally out of scope.
        $browserPolicy = Join-RunlayerPath -Root $programData `
            -Parts @("Google", "Chrome", "policy.json")
        Write-OwnedHookJson -Path $browserPolicy
        $browserBefore = [System.IO.File]::ReadAllText($browserPolicy)

        Mock Get-RunlayerProfileRoots {
            throw "supplied roots must bypass real ProfileList"
        }
        $changed = Invoke-RemoveHooks -ProfileRoots @($alice, $entra) `
            -ProgramDataRoot $programData `
            -ProgramFilesRoot $programFiles `
            -BackupRoot (Join-Path $programData "RunlayerBackups") `
            -LogFile (Join-Path $programData "scheduled-task.log")

        $changed | Should -BeGreaterThan 15
        Should -Invoke Get-RunlayerProfileRoots -Times 0 -Exactly

        # All profile JSON files are clean; Runlayer-named files are removed.
        foreach ($parts in $profileJson) {
            $path = Join-RunlayerPath -Root $alice -Parts $parts
            if ($ownedProfileJson -contains ($parts -join "/")) {
                Test-Path -LiteralPath $path | Should -BeFalse
            } else {
                $document = Read-TestJson -Path $path
                $document.PSObject.Properties["hooks"] | Should -BeNullOrEmpty
            }
        }
        Test-Path -LiteralPath (
            Join-RunlayerPath -Root $entra -Parts @(".cursor", "hooks.json")
        ) | Should -BeFalse

        [System.IO.File]::ReadAllText($hermes) | Should -Not -Match "aiwatch"
        [System.IO.File]::ReadAllText($hermes) | Should -Match "C:\\Acme"
        Test-Path -LiteralPath $goose | Should -BeFalse
        Test-Path -LiteralPath $cline | Should -BeFalse
        Test-Path -LiteralPath $legacyShim | Should -BeFalse
        [System.IO.File]::ReadAllText($codexToml) |
            Should -BeExactly "[features]`nhooks = true`n"

        $locations = (Read-TestJson -Path $vscodeSettings)."chat.hookFilesLocations"
        $locations.PSObject.Properties["~/.copilot/hooks"] |
            Should -BeNullOrEmpty
        $locations."~/acme/hooks" | Should -BeTrue
        foreach ($name in @(".cursorignore", ".claudeignore")) {
            [System.IO.File]::ReadAllText(
                (Join-RunlayerPath -Root $alice -Parts @($name))
            ) | Should -BeExactly "vendor/`n"
        }

        foreach ($spec in $enterpriseJson) {
            $path = Join-RunlayerPath -Root $spec.Root -Parts $spec.Parts
            if ($spec.OwnedName) {
                Test-Path -LiteralPath $path | Should -BeFalse
            } else {
                (Read-TestJson -Path $path).PSObject.Properties["hooks"] |
                    Should -BeNullOrEmpty
            }
        }
        [System.IO.File]::ReadAllText($browserPolicy) |
            Should -BeExactly $browserBefore
        foreach ($spec in $legacyFiles) {
            $path = Join-RunlayerPath -Root $spec.Root -Parts $spec.Parts
            Test-Path -LiteralPath $path | Should -BeFalse
        }
        Test-Path -LiteralPath (Join-Path $programData "RunlayerBackups") |
            Should -BeTrue
    }
}

Describe "entrypoint contract" {
    BeforeEach { Reset-RemoveHooksTestState }

    It "does not auto-run when dot-sourced and ends the file entrypoint with exit 0" {
        $text = Get-Content -LiteralPath $script:RemoveHooksScriptPath -Raw
        $text | Should -Match '\$MyInvocation\.InvocationName -ne ''\.'''
        $text | Should -Match '(?s)if \(\$MyInvocation\.InvocationName -ne ''\.''\).*exit 0\s*\}\s*$'
        $text | Should -Not -Match "OrgApiKey"
    }
}
