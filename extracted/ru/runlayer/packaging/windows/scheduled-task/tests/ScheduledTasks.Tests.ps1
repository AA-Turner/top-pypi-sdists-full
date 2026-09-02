#Requires -Version 5.1
# Pester tests for the AI Watch device-local Scheduled Task scripts.
#
# Helper / SDDL / naming tests run anywhere (.NET only). The behavioral tests
# that mock the ScheduledTasks module (SYSTEM principal, registration, legacy
# cleanup) are Windows-only and skip elsewhere. The Intune custom detection
# script moved to ../../custom-detection/ — see that folder's DetectInstall.Tests.ps1.
#
# The per-user fan-out logic (real-profile SID filter, username resolution,
# orchestration, per-profile resilience) moved out of PowerShell into the
# testable `aiwatch scan --all-users` binary — see cli/tests/test_windows_scan_all_users.py.
#
# Each script is dot-sourced; its `if ($MyInvocation.InvocationName -ne '.')`
# guard means dot-sourcing loads the functions without running the main body.

BeforeAll {
    # NB: these path vars use a `...ScriptPath` suffix on purpose — the runtime
    # script defines its own `$script:...` constants, and dot-sourcing one would
    # otherwise clobber a same-named harness variable.
    $script:TaskDir = Split-Path -Parent $PSScriptRoot
    $script:CommonScriptPath = Join-Path $script:TaskDir "RunlayerTaskCommon.ps1"
    $script:RegisterScriptPath = Join-Path $script:TaskDir "register-tasks.ps1"
    $script:UnregisterScriptPath = Join-Path $script:TaskDir "unregister-tasks.ps1"
    $script:ExpectedSddl = "D:P(A;;GA;;;SY)(A;;GA;;;BA)(A;;GRGX;;;AU)"
    $script:ExpectedUpdateSddl = "D:P(A;;GA;;;SY)(A;;GA;;;BA)"

    # Well-known SIDs + generic-right masks for the tamper assertions.
    $script:SidSystem = "S-1-5-18"
    $script:SidAdmins = "S-1-5-32-544"
    $script:SidAuthUsers = "S-1-5-11"
    $script:GENERIC_READ = 0x80000000
    $script:GENERIC_WRITE = 0x40000000
    $script:GENERIC_EXECUTE = 0x20000000
    $script:GENERIC_ALL = 0x10000000
    $script:DELETE = 0x00010000
    $script:WRITE_DAC = 0x00040000
    $script:WRITE_OWNER = 0x00080000

    $script:OnWindows = $PSVersionTable.PSEdition -eq 'Desktop' -or $IsWindows
}

Describe "RunlayerTaskCommon.ps1 (shared foundation)" {
    BeforeAll { . $script:CommonScriptPath }

    It "is the single source of the locked-down protected DACL" {
        Get-RunlayerTaskSddl | Should -Be $script:ExpectedSddl
    }

    It "exposes the shared task-scheduler foundation functions" {
        foreach ($fn in @(
                "Invoke-RunlayerLogRotation",
                "Write-RunlayerLog",
                "Get-RunlayerTaskSddl",
                "Get-RunlayerUpdateTaskSddl",
                "New-RunlayerTaskSettings",
                "New-RunlayerUpdateTaskSettings",
                "New-RunlayerRepeatingTrigger",
                "Initialize-RunlayerTaskFolder",
                "Set-RunlayerTaskSecurity",
                "Register-AiWatchHooksTask",
                "Register-AiWatchScanTask",
                "Register-AiWatchUpdateTask"
            )) {
            Get-Command $fn -CommandType Function | Should -Not -BeNullOrEmpty
        }
    }

    Context "shared log rotation" {
        BeforeEach {
            $script:LogFile = Join-Path $TestDrive "scheduled-task.log"
            $script:RunlayerLogMaxBytes = 4
            $script:RunlayerLogRotationChecked = $false
            $script:RunlayerLogComponent = "test"
            Remove-Item -LiteralPath $script:LogFile -Force -ErrorAction SilentlyContinue
            Remove-Item -LiteralPath ($script:LogFile + ".1") -Force -ErrorAction SilentlyContinue
        }

        AfterEach {
            $script:LogFile = "C:\ProgramData\Runlayer\Logs\scheduled-task.log"
            $script:RunlayerLogMaxBytes = 10MB
            $script:RunlayerLogRotationChecked = $false
            $script:RunlayerLogComponent = "task"
        }

        It "replaces the single backup before the first append only" {
            [System.IO.File]::WriteAllText($script:LogFile, "oversized")
            [System.IO.File]::WriteAllText(($script:LogFile + ".1"), "stale")

            Write-RunlayerLog "first"

            [System.IO.File]::ReadAllText(($script:LogFile + ".1")) | Should -Be "oversized"
            [System.IO.File]::ReadAllText($script:LogFile) | Should -Match "first"

            [System.IO.File]::AppendAllText($script:LogFile, "oversized again")
            Write-RunlayerLog "second"

            [System.IO.File]::ReadAllText(($script:LogFile + ".1")) | Should -Be "oversized"
            [System.IO.File]::ReadAllText($script:LogFile) | Should -Match "second"
        }

        It "keeps a log at the size threshold in place" {
            [System.IO.File]::WriteAllText($script:LogFile, "1234")

            Write-RunlayerLog "appended"

            Test-Path ($script:LogFile + ".1") | Should -BeFalse
            [System.IO.File]::ReadAllText($script:LogFile) | Should -Match "^1234"
            [System.IO.File]::ReadAllText($script:LogFile) | Should -Match "appended"
        }

        It "keeps appending when a concurrent writer prevents rotation" {
            [System.IO.File]::WriteAllText($script:LogFile, "oversized")
            Mock Move-Item { throw "simulated open handle" }

            { Write-RunlayerLog "appended" } | Should -Not -Throw

            Should -Invoke Move-Item -Times 1 -Exactly
            [System.IO.File]::ReadAllText($script:LogFile) | Should -Match "^oversized"
            [System.IO.File]::ReadAllText($script:LogFile) | Should -Match "appended"
        }
    }

    It "denies standard users read and execute access to AIWatchUpdate" {
        $sddl = Get-RunlayerUpdateTaskSddl
        $sddl | Should -Be $script:ExpectedUpdateSddl
        $sddl | Should -Not -Match ';;;AU\)'
    }

    # ENG-3579 regression. The repeating trigger must NOT carry an out-of-range
    # repetition Duration: -RepetitionDuration [TimeSpan]::MaxValue serializes to
    # "P99999999DT23H59M59S", which Task Scheduler accepts at trigger-creation
    # time but rejects at Register-ScheduledTask time ("The task XML contains a
    # value which is incorrectly formatted or out of range"). On install that
    # aborted register-tasks.ps1 before AIWatchScan was registered, so the
    # \Runlayer folder was empty and detect-install.ps1 reported not-installed.
    # An empty Duration => repeat indefinitely, which is what we want.
    #
    # Windows-only: New-RunlayerRepeatingTrigger calls New-ScheduledTaskTrigger
    # from the Windows ScheduledTasks module (absent on macOS / Linux PowerShell).
    Context "New-RunlayerRepeatingTrigger (ENG-3579)" -Skip:(-not $OnWindows) {
        It "sets the requested repetition interval" {
            $trigger = New-RunlayerRepeatingTrigger -IntervalMinutes 60
            $trigger.Repetition.Interval | Should -Be "PT60M"
        }

        It "does not emit the out-of-range MaxValue duration" {
            $trigger = New-RunlayerRepeatingTrigger -IntervalMinutes 60
            $trigger.Repetition.Duration | Should -Not -Be "P99999999DT23H59M59S"
            [string]::IsNullOrEmpty($trigger.Repetition.Duration) | Should -BeTrue
        }

        # Real registration (no mocks) — this is the check that actually failed on
        # device. Register-ScheduledTask validates the trigger XML, so an
        # out-of-range Duration throws here. Registered under the current user (no
        # -Principal) so the assertion turns purely on the trigger XML, not on
        # SYSTEM-principal elevation (principal behavior is covered by the mocked
        # registration tests).
        It "registers a real task using the repeating trigger" {
            $testPath = "\RunlayerTest\"
            $testName = "RunlayerRepeatingTriggerTest"
            try {
                $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c exit 0"
                $trigger = New-RunlayerRepeatingTrigger -IntervalMinutes 60
                $settings = New-RunlayerTaskSettings
                { Register-ScheduledTask -TaskName $testName -TaskPath $testPath `
                        -Action $action -Trigger $trigger `
                        -Settings $settings -Force -ErrorAction Stop } | Should -Not -Throw
                Get-ScheduledTask -TaskPath $testPath -TaskName $testName -ErrorAction SilentlyContinue |
                    Should -Not -BeNullOrEmpty
            } finally {
                Unregister-ScheduledTask -TaskName $testName -TaskPath $testPath `
                    -Confirm:$false -ErrorAction SilentlyContinue
                try {
                    $svc = New-Object -ComObject "Schedule.Service"
                    $svc.Connect()
                    $svc.GetFolder("\").DeleteFolder("RunlayerTest", 0)
                } catch {
                    # Best-effort folder cleanup; an empty test folder is harmless.
                }
            }
        }
    }
}

Describe "register-tasks.ps1" {
    BeforeAll {
        . $script:RegisterScriptPath
        $script:RegisterText = Get-Content $script:RegisterScriptPath -Raw
    }

    Context "self-update runner OrgApiKey gate" {
        BeforeEach {
            Mock Write-RunlayerLog {}
            Mock Test-Path { $true }
            Mock Start-Process { [pscustomobject]@{ ExitCode = 0 } }
        }

        It "queries the parameterized RelatedProducts property for the AI Watch UpgradeCode" {
            $script:AiWatchUpgradeCode | Should -Be "{E3A2F1C0-7B4D-4E9A-8C6F-1D2E3F4A5B6C}"
            $script:RegisterText | Should -Match (
                'InvokeMember\(\s*"RelatedProducts",\s*' +
                '\[System\.Reflection\.BindingFlags\]::GetProperty'
            )
        }

        It "does not invoke aiwatch when HKLM OrgApiKey is absent" {
            Mock Get-ItemProperty { [pscustomobject]@{ OrgApiKey = "" } }

            Invoke-AiWatchSelfUpdate | Should -Be 0

            Should -Invoke Get-ItemProperty -Times 1 -Exactly -ParameterFilter {
                $Path -eq "HKLM:\Software\Runlayer\AIWatch" -and $Name -eq "OrgApiKey"
            }
            Should -Invoke Start-Process -Times 0 -Exactly
        }

        It "repairs the installed AI Watch product when aiwatch.exe is missing" {
            $productCode = "{AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE}"
            Mock Get-ItemProperty { [pscustomobject]@{ OrgApiKey = "rl_org_test" } }
            Mock Test-Path { $false }
            Mock Get-AiWatchProductCode { $productCode }
            Mock Start-Process { [pscustomobject]@{ ExitCode = 3010 } }

            Invoke-AiWatchSelfUpdate | Should -Be 3010

            Should -Invoke Get-AiWatchProductCode -Times 1 -Exactly
            Should -Invoke Start-Process -Times 1 -Exactly -ParameterFilter {
                $FilePath -eq "msiexec.exe" -and
                ($ArgumentList -join " ") -eq "/fa $productCode /qn /norestart" -and
                $Wait -and $PassThru
            }
            Should -Invoke Write-RunlayerLog -Times 1 -Exactly -ParameterFilter {
                $Message -eq "aiwatch.exe missing; attempting MSI repair for product $productCode"
            }
            Should -Invoke Write-RunlayerLog -Times 1 -Exactly -ParameterFilter {
                $Message -eq "MSI repair completed with exit code 3010"
            }
        }

        It "returns 2 and logs when aiwatch.exe and its installed product are missing" {
            Mock Get-ItemProperty { [pscustomobject]@{ OrgApiKey = "rl_org_test" } }
            Mock Test-Path { $false }
            Mock Get-AiWatchProductCode { $null }

            Invoke-AiWatchSelfUpdate | Should -Be 2

            Should -Invoke Get-AiWatchProductCode -Times 1 -Exactly
            Should -Invoke Start-Process -Times 0 -Exactly
            Should -Invoke Write-RunlayerLog -Times 1 -Exactly -ParameterFilter {
                $Message -eq "aiwatch.exe missing; no installed AI Watch product found for repair"
            }
        }

        It "keeps invoking aiwatch self-update when aiwatch.exe is present" {
            Mock Get-ItemProperty { [pscustomobject]@{ OrgApiKey = "rl_org_test" } }
            Mock Get-AiWatchProductCode { throw "product lookup must not run" }
            Mock Start-Process { [pscustomobject]@{ ExitCode = 23 } }

            Invoke-AiWatchSelfUpdate | Should -Be 23

            Should -Invoke Get-AiWatchProductCode -Times 0 -Exactly
            Should -Invoke Start-Process -Times 1 -Exactly -ParameterFilter {
                $FilePath -eq "C:\Program Files\Runlayer\AIWatch\aiwatch.exe" -and
                $ArgumentList -eq "self-update" -and $Wait -and $PassThru
            }
        }
    }

    Context "tamper-resistance SDDL" {
        It "uses the locked-down protected DACL (via the shared foundation)" {
            Get-RunlayerTaskSddl | Should -Be $script:ExpectedSddl
        }
    }

    # RawSecurityDescriptor (System.Security.AccessControl) is Windows-only in
    # .NET; the cross-platform SDDL-string content check lives in
    # test_windows_ps1_gates.py. These decode the access masks on Windows.
    Context "tamper-resistance SDDL (ACL decode)" -Skip:(-not $OnWindows) {
        It "grants full control only to SYSTEM and Administrators" {
            $sd = [System.Security.AccessControl.RawSecurityDescriptor]::new((Get-RunlayerTaskSddl))
            foreach ($sid in @($script:SidSystem, $script:SidAdmins)) {
                $ace = $sd.DiscretionaryAcl | Where-Object { $_.SecurityIdentifier.Value -eq $sid }
                $ace | Should -Not -BeNullOrEmpty
                ($ace.AccessMask -band $script:GENERIC_ALL) | Should -Be $script:GENERIC_ALL
            }
        }

        It "grants Authenticated Users read+execute but never write or delete" {
            $sd = [System.Security.AccessControl.RawSecurityDescriptor]::new((Get-RunlayerTaskSddl))
            $ace = $sd.DiscretionaryAcl | Where-Object { $_.SecurityIdentifier.Value -eq $script:SidAuthUsers }
            $ace | Should -Not -BeNullOrEmpty
            ($ace.AccessMask -band $script:GENERIC_READ) | Should -Be $script:GENERIC_READ
            ($ace.AccessMask -band $script:GENERIC_EXECUTE) | Should -Be $script:GENERIC_EXECUTE
            ($ace.AccessMask -band $script:GENERIC_WRITE) | Should -Be 0
            ($ace.AccessMask -band $script:GENERIC_ALL) | Should -Be 0
            ($ace.AccessMask -band $script:DELETE) | Should -Be 0
            ($ace.AccessMask -band $script:WRITE_DAC) | Should -Be 0
            ($ace.AccessMask -band $script:WRITE_OWNER) | Should -Be 0
        }

        It "is a protected DACL (no inheritance from the parent folder)" {
            $sd = [System.Security.AccessControl.RawSecurityDescriptor]::new((Get-RunlayerTaskSddl))
            ($sd.ControlFlags -band [System.Security.AccessControl.ControlFlags]::DiscretionaryAclProtected) |
                Should -Not -Be 0
        }

        It "gives only SYSTEM and Administrators access to AIWatchUpdate" {
            $sd = [System.Security.AccessControl.RawSecurityDescriptor]::new((Get-RunlayerUpdateTaskSddl))
            $sd.DiscretionaryAcl.Count | Should -Be 2
            foreach ($sid in @($script:SidSystem, $script:SidAdmins)) {
                $ace = $sd.DiscretionaryAcl | Where-Object { $_.SecurityIdentifier.Value -eq $sid }
                $ace | Should -Not -BeNullOrEmpty
                ($ace.AccessMask -band $script:GENERIC_ALL) | Should -Be $script:GENERIC_ALL
            }
            $sd.DiscretionaryAcl |
                Where-Object { $_.SecurityIdentifier.Value -eq $script:SidAuthUsers } |
                Should -BeNullOrEmpty
        }
    }

    Context "task registration" -Skip:(-not $OnWindows) {
        BeforeEach {
            Mock New-ScheduledTaskAction { [pscustomobject]@{ Execute = $Execute; Argument = $Argument } }
            Mock New-ScheduledTaskTrigger { [pscustomobject]@{ kind = "trigger" } }
            Mock New-ScheduledTaskPrincipal { [pscustomobject]@{ UserId = $UserId; LogonType = $LogonType } }
            Mock New-ScheduledTaskSettingsSet { [pscustomobject]@{ Hidden = $Hidden } }
            Mock Register-ScheduledTask {}
            Mock Set-RunlayerTaskSecurity {}
        }

        It "registers AIWatchHooks as SYSTEM running 'setup hooks install --mdm'" {
            Register-AiWatchHooksTask
            Should -Invoke New-ScheduledTaskAction -Times 1 -Exactly -ParameterFilter {
                $Argument -eq "setup hooks install --mdm"
            }
            Should -Invoke New-ScheduledTaskPrincipal -ParameterFilter {
                $UserId -eq "SYSTEM" -and $LogonType -eq "ServiceAccount"
            }
            Should -Invoke Register-ScheduledTask -ParameterFilter {
                $TaskName -eq "AIWatchHooks" -and $TaskPath -eq "\Runlayer\" -and $Force -eq $true
            }
            Should -Invoke Set-RunlayerTaskSecurity -ParameterFilter { $TaskName -eq "AIWatchHooks" }
        }

        It "registers AIWatchScan as SYSTEM running 'scan --all-users' (hidden)" {
            Register-AiWatchScanTask
            Should -Invoke New-ScheduledTaskAction -Times 1 -Exactly -ParameterFilter {
                $Argument -eq "scan --all-users"
            }
            Should -Invoke New-ScheduledTaskPrincipal -ParameterFilter {
                $UserId -eq "SYSTEM" -and $LogonType -eq "ServiceAccount"
            }
            Should -Invoke New-ScheduledTaskSettingsSet -ParameterFilter { $Hidden -eq $true }
            Should -Invoke Register-ScheduledTask -ParameterFilter {
                $TaskName -eq "AIWatchScan" -and $TaskPath -eq "\Runlayer\" -and $Force -eq $true
            }
            Should -Invoke Set-RunlayerTaskSecurity -ParameterFilter { $TaskName -eq "AIWatchScan" }
        }

        It "registers AIWatchUpdate as a hidden SYSTEM hourly-only task" {
            Register-AiWatchUpdateTask
            Should -Invoke New-ScheduledTaskAction -Times 1 -Exactly -ParameterFilter {
                $Execute -like "*powershell.exe" -and
                $Argument -match 'register-tasks\.ps1' -and
                $Argument -match '-RunSelfUpdate'
            }
            Should -Invoke New-ScheduledTaskPrincipal -ParameterFilter {
                $UserId -eq "SYSTEM" -and $LogonType -eq "ServiceAccount"
            }
            Should -Invoke New-ScheduledTaskSettingsSet -Times 1 -Exactly -ParameterFilter {
                $Hidden -eq $true -and
                $AllowStartIfOnBatteries -eq $true -and
                $DontStopIfGoingOnBatteries -eq $true -and
                $MultipleInstances -eq "IgnoreNew" -and
                $ExecutionTimeLimit.TotalHours -eq 1 -and
                -not $StartWhenAvailable
            }
            Should -Invoke New-ScheduledTaskTrigger -Times 1 -Exactly -ParameterFilter {
                $Once -and $RepetitionInterval.TotalMinutes -eq 60 -and
                $At -gt (Get-Date).AddMinutes(62) -and
                $At -lt (Get-Date).AddMinutes(72)
            }
            Should -Invoke Register-ScheduledTask -ParameterFilter {
                $TaskName -eq "AIWatchUpdate" -and $TaskPath -eq "\Runlayer\" -and $Force -eq $true
            }
            Should -Invoke Set-RunlayerTaskSecurity -ParameterFilter {
                $TaskName -eq "AIWatchUpdate" -and $Sddl -eq $script:ExpectedUpdateSddl
            }
        }
    }

    # The single SYSTEM AIWatchScan task supersedes the legacy per-user fan-out
    # (AIWatchScanManager + AIWatchScan-<SID>). On upgrade, register-tasks.ps1
    # must remove the legacy tasks WITHOUT touching the new AIWatchScan (no
    # trailing dash) or AIWatchHooks.
    Context "legacy task cleanup" -Skip:(-not $OnWindows) {
        BeforeEach {
            Mock Get-ScheduledTask {
                @(
                    [pscustomobject]@{ TaskName = "AIWatchScan" },
                    [pscustomobject]@{ TaskName = "AIWatchHooks" },
                    [pscustomobject]@{ TaskName = "AIWatchUpdate" },
                    [pscustomobject]@{ TaskName = "AIWatchScanManager" },
                    [pscustomobject]@{ TaskName = "AIWatchScan-S-1-5-21-1-2-3-1001" },
                    [pscustomobject]@{ TaskName = "AIWatchScan-S-1-12-1-1-2-3-4" }
                )
            }
            Mock Unregister-ScheduledTask {}
            Mock Write-RunlayerLog {}
        }

        It "removes the legacy AIWatchScanManager task" {
            Remove-LegacyScanTasks
            Should -Invoke Unregister-ScheduledTask -Times 1 -Exactly -ParameterFilter {
                $TaskName -eq "AIWatchScanManager"
            }
        }

        It "removes the legacy per-user AIWatchScan-<SID> tasks" {
            Remove-LegacyScanTasks
            Should -Invoke Unregister-ScheduledTask -Times 2 -Exactly -ParameterFilter {
                $TaskName -like "AIWatchScan-*"
            }
        }

        It "does NOT remove the new single AIWatchScan task" {
            Remove-LegacyScanTasks
            Should -Invoke Unregister-ScheduledTask -Times 0 -Exactly -ParameterFilter {
                $TaskName -eq "AIWatchScan"
            }
        }

        It "does NOT remove the AIWatchHooks task" {
            Remove-LegacyScanTasks
            Should -Invoke Unregister-ScheduledTask -Times 0 -Exactly -ParameterFilter {
                $TaskName -eq "AIWatchHooks"
            }
        }

        It "does NOT remove the AIWatchUpdate task" {
            Remove-LegacyScanTasks
            Should -Invoke Unregister-ScheduledTask -Times 0 -Exactly -ParameterFilter {
                $TaskName -eq "AIWatchUpdate"
            }
        }
    }

    Context "SDDL via the shared foundation" {
        It "applies the identical locked-down SDDL" {
            Get-RunlayerTaskSddl | Should -Be $script:ExpectedSddl
        }
    }

    It "registers AIWatchUpdate but never kicks it from the MSI custom action" {
        $script:RegisterText | Should -Match 'Register-AiWatchUpdateTask'
        $script:RegisterText | Should -Not -Match 'Start-ScheduledTask[^\r\n]+\$script:UpdateTaskName'
    }

    It "logs the main registration missing-executable guard before warning and exit" {
        $script:RegisterText | Should -Match (
            '(?s)if \(-not \(Test-Path \$script:ExePath\)\) \{\s*' +
            'Write-RunlayerLog "aiwatch\.exe not found at \$script:ExePath; install the AI Watch MSI first\."\s*' +
            'Write-Warning "aiwatch\.exe not found at \$script:ExePath; install the AI Watch MSI first\."\s*' +
            'exit 2'
        )
    }
}

Describe "unregister-tasks.ps1" {
    BeforeAll {
        . $script:UnregisterScriptPath
        $script:UnregisterText = Get-Content $script:UnregisterScriptPath -Raw
    }

    It "defines scoped cleanup functions" {
        foreach ($fn in @(
                "Test-AiWatchOwnedTaskName",
                "Remove-AiWatchTasksFromFolder",
                "Remove-RunlayerTaskFolderIfEmpty",
                "Remove-RunlayerTaskFolder"
            )) {
            Get-Command $fn -CommandType Function | Should -Not -BeNullOrEmpty
        }
    }

    It "deletes only AI Watch persistent, handoff, and legacy tasks" {
        $tasks = @(
                [pscustomobject]@{ Name = "AIWatchHooks" },
                [pscustomobject]@{ Name = "AIWatchScan" },
                [pscustomobject]@{ Name = "AIWatchUpdate" },
                [pscustomobject]@{ Name = "AIWatchUpdateHandoff" },
                [pscustomobject]@{ Name = "AIWatchScanManager" },
                [pscustomobject]@{ Name = "AIWatchScan-S-1-5-21-1-2-3-1001" },
                [pscustomobject]@{ Name = "CLIUpdateHandoff" },
                [pscustomobject]@{ Name = "UnrelatedTask" }
        )
        foreach ($task in $tasks) {
            $task | Add-Member -MemberType NoteProperty -Name Stopped -Value $false
            $task | Add-Member -MemberType ScriptMethod -Name Stop -Value {
                param($Flags)
                $this.Stopped = $true
            }
        }
        $folder = [pscustomobject]@{
            Tasks = $tasks
            Deleted = [System.Collections.Generic.List[string]]::new()
        }
        $folder | Add-Member -MemberType ScriptMethod -Name GetTasks -Value {
            param($Flags)
            if ($Flags -ne 1) { throw "hidden tasks were not requested" }
            return $this.Tasks
        }
        $folder | Add-Member -MemberType ScriptMethod -Name DeleteTask -Value {
            param($TaskName, $Flags)
            [void]$this.Deleted.Add($TaskName)
        }
        Mock Write-RunlayerLog {}

        Remove-AiWatchTasksFromFolder -Folder $folder

        ($folder.Deleted -join ",") | Should -Be (
            "AIWatchHooks,AIWatchScan,AIWatchUpdate,AIWatchUpdateHandoff," +
            "AIWatchScanManager,AIWatchScan-S-1-5-21-1-2-3-1001"
        )
        foreach ($task in $tasks) {
            $expectedStopped = $task.Name -notin @("CLIUpdateHandoff", "UnrelatedTask")
            $task.Stopped | Should -Be $expectedStopped
        }
    }

    It "preserves the shared folder while CLIUpdateHandoff remains" {
        $folder = [pscustomobject]@{
            Tasks = @([pscustomobject]@{ Name = "CLIUpdateHandoff" })
        }
        $folder | Add-Member -MemberType ScriptMethod -Name GetTasks -Value {
            param($Flags)
            if ($Flags -ne 1) { throw "hidden tasks were not requested" }
            return $this.Tasks
        }
        $root = [pscustomobject]@{
            Deleted = [System.Collections.Generic.List[string]]::new()
        }
        $root | Add-Member -MemberType ScriptMethod -Name DeleteFolder -Value {
            param($FolderName, $Flags)
            [void]$this.Deleted.Add($FolderName)
        }
        Mock Write-RunlayerLog {}

        Remove-RunlayerTaskFolderIfEmpty -Root $root -Folder $folder

        $root.Deleted.Count | Should -Be 0
    }

    It "deletes the shared folder after hidden-task enumeration proves it empty" {
        $folder = [pscustomobject]@{ Tasks = @() }
        $folder | Add-Member -MemberType ScriptMethod -Name GetTasks -Value {
            param($Flags)
            if ($Flags -ne 1) { throw "hidden tasks were not requested" }
            return $this.Tasks
        }
        $root = [pscustomobject]@{
            Deleted = [System.Collections.Generic.List[string]]::new()
        }
        $root | Add-Member -MemberType ScriptMethod -Name DeleteFolder -Value {
            param($FolderName, $Flags)
            [void]$this.Deleted.Add($FolderName)
        }
        Mock Write-RunlayerLog {}

        Remove-RunlayerTaskFolderIfEmpty -Root $root -Folder $folder

        ($root.Deleted -join ",") | Should -Be "Runlayer"
    }
}

Describe "guard exit codes survive ErrorActionPreference = Stop" {
    # Regression for the Write-Error footgun: under $ErrorActionPreference='Stop',
    # Write-Error promotes to a TERMINATING error, so a following `exit N` never
    # runs and the script collapses to exit 1 — masking the documented misconfig
    # code (2). The SYSTEM runtime script sets Stop, so its guard / catch sites
    # must emit a NON-terminating diagnostic (Write-Warning) before `exit`.

    BeforeAll {
        function Invoke-HostExitCode {
            # Run a snippet in a child of the current PowerShell host and return
            # its process exit code (proves the control-flow, not just intent).
            param([string]$ScriptBody)
            $exe = (Get-Process -Id $PID).Path
            $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("rl-guard-{0}.ps1" -f [guid]::NewGuid())
            Set-Content -LiteralPath $tmp -Value $ScriptBody -Encoding UTF8
            try {
                & $exe -NoProfile -NonInteractive -File $tmp *> $null
                return $LASTEXITCODE
            } finally {
                Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
            }
        }

        function Get-DeadCodeExitGuards {
            # Guard sites where a terminating Write-Error directly precedes `exit`
            # (the broken pattern). A Write-Error carrying a non-terminating
            # -ErrorAction is exempt (it would not throw under Stop).
            param([string]$Path)
            $lines = Get-Content -LiteralPath $Path
            $hits = @()
            for ($i = 0; $i -lt $lines.Count; $i++) {
                $line = $lines[$i]
                if ($line.TrimStart() -notlike "Write-Error*") { continue }
                if ($line -match '-ErrorAction\s+(Continue|SilentlyContinue|Ignore)') { continue }
                $j = $i + 1
                while ($j -lt $lines.Count -and ($lines[$j].Trim() -eq "" -or $lines[$j].TrimStart().StartsWith("#"))) {
                    $j++
                }
                if ($j -lt $lines.Count -and $lines[$j].TrimStart() -like "exit*") {
                    $hits += "line $($i + 1): $($line.Trim())"
                }
            }
            return $hits
        }
    }

    It "demonstrates the footgun: Write-Error before 'exit 2' collapses to exit 1" {
        $body = @'
$ErrorActionPreference = "Stop"
Write-Error "guard message"
exit 2
'@
        Invoke-HostExitCode -ScriptBody $body | Should -Be 1
    }

    It "Write-Warning is non-terminating, so 'exit 2' takes effect under Stop" {
        $body = @'
$ErrorActionPreference = "Stop"
Write-Warning "guard message"
exit 2
'@
        Invoke-HostExitCode -ScriptBody $body | Should -Be 2
    }

    It "register-tasks.ps1 has no terminating Write-Error before exit" {
        Get-DeadCodeExitGuards -Path $script:RegisterScriptPath | Should -BeNullOrEmpty
    }
}
