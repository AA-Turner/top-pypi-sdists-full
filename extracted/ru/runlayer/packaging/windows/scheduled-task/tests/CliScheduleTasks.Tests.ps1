#Requires -Version 5.1
# Pester coverage for the full CLI's package-owned skill-sync schedule task.

BeforeAll {
    $script:ScheduledTaskDir = Split-Path -Parent $PSScriptRoot
    $script:WindowsPackagingDir = Split-Path -Parent $script:ScheduledTaskDir
    $script:CliTaskSourceDir = Join-Path $script:WindowsPackagingDir "cli-schedule-task"
    $script:CliTaskDir = Join-Path $TestDrive "cli-schedule-task"
    New-Item -ItemType Directory -Path $script:CliTaskDir | Out-Null
    Copy-Item (Join-Path $script:CliTaskSourceDir "register-tasks.ps1") $script:CliTaskDir
    Copy-Item (Join-Path $script:CliTaskSourceDir "unregister-tasks.ps1") $script:CliTaskDir
    Copy-Item (Join-Path $script:ScheduledTaskDir "RunlayerTaskCommon.ps1") $script:CliTaskDir
    $script:CliRegisterPath = Join-Path $script:CliTaskDir "register-tasks.ps1"
    $script:CliUnregisterPath = Join-Path $script:CliTaskDir "unregister-tasks.ps1"
    $script:OnWindows = $PSVersionTable.PSEdition -eq 'Desktop' -or $IsWindows

    . $script:CliRegisterPath
}

Describe "full CLI schedule task registration" {
    It "requires SYSTEM and does not kick the task during MSI install" {
        $text = Get-Content $script:CliRegisterPath -Raw

        $text | Should -Match 'WindowsIdentity\]::GetCurrent\(\)'
        $text | Should -Match '\.IsSystem'
        $text | Should -Not -Match 'Start-ScheduledTask'
    }

    Context "task definition" -Skip:(-not $OnWindows) {
        BeforeEach {
            Mock New-ScheduledTaskAction {
                [pscustomobject]@{ Execute = $Execute; Argument = $Argument }
            }
            Mock New-ScheduledTaskTrigger {
                [pscustomobject]@{
                    At = $At
                    AtLogOn = $AtLogOn
                    Repetition = [pscustomobject]@{ Duration = "" }
                }
            }
            Mock New-ScheduledTaskPrincipal {
                [pscustomobject]@{ UserId = $UserId; LogonType = $LogonType }
            }
            Mock New-ScheduledTaskSettingsSet {
                [pscustomobject]@{ Hidden = $Hidden }
            }
            Mock Register-ScheduledTask {}
            Mock Set-RunlayerTaskSecurity {}
        }

        It "registers protected hourly and at-logon SYSTEM triggers" {
            Register-CliScheduleTask
            $expectedExePath = Join-Path (Split-Path -Parent $script:CliTaskDir) "runlayer.exe"

            Should -Invoke New-ScheduledTaskAction -Times 1 -Exactly -ParameterFilter {
                $Execute -eq $expectedExePath -and
                $Argument -eq "schedule --all-users"
            }
            Should -Invoke New-ScheduledTaskPrincipal -Times 1 -Exactly -ParameterFilter {
                $UserId -eq "SYSTEM" -and
                $LogonType -eq "ServiceAccount" -and
                $RunLevel -eq "Highest"
            }
            Should -Invoke New-ScheduledTaskTrigger -Times 1 -Exactly -ParameterFilter {
                $AtLogOn
            }
            Should -Invoke New-ScheduledTaskTrigger -Times 1 -Exactly -ParameterFilter {
                $Once -and $RepetitionInterval.TotalMinutes -eq 60
            }
            Should -Invoke New-ScheduledTaskSettingsSet -Times 1 -Exactly -ParameterFilter {
                $Hidden -eq $true -and
                $MultipleInstances -eq "IgnoreNew" -and
                $StartWhenAvailable -eq $true
            }
            Should -Invoke Register-ScheduledTask -Times 1 -Exactly -ParameterFilter {
                $TaskName -eq "CLISchedule" -and
                $TaskPath -eq "\Runlayer\" -and
                $Force -eq $true
            }
            Should -Invoke Set-RunlayerTaskSecurity -Times 1 -Exactly -ParameterFilter {
                $TaskName -eq "CLISchedule"
            }
        }
    }
}

Describe "full CLI schedule task removal" {
    BeforeAll {
        . $script:CliUnregisterPath
    }

    It "owns only CLISchedule" {
        $text = Get-Content $script:CliUnregisterPath -Raw

        $text | Should -Match '\$script:CliScheduleTaskNames = @\("CLISchedule"\)'
        $text | Should -Not -Match '"CLIUpdate"'
        $text | Should -Not -Match '"AIWatchUpdate"'
        $text | Should -Match 'GetTasks\(1\)'
        $text | Should -Match 'preserved shared \\Runlayer task folder'
    }

    It "deletes CLISchedule while preserving unrelated tasks" {
        $tasks = @(
            [pscustomobject]@{ Name = "CLISchedule" },
            [pscustomobject]@{ Name = "CLIUpdate" }
        )
        foreach ($task in $tasks) {
            $task | Add-Member -MemberType ScriptMethod -Name Stop -Value {
                param($Flags)
            }
        }
        $folder = [pscustomobject]@{
            Tasks = $tasks
            Deleted = [System.Collections.Generic.List[string]]::new()
        }
        $folder | Add-Member -MemberType ScriptMethod -Name GetTasks -Value {
            param($Flags)
            return $this.Tasks
        }
        $folder | Add-Member -MemberType ScriptMethod -Name DeleteTask -Value {
            param($TaskName, $Flags)
            [void]$this.Deleted.Add($TaskName)
        }
        Mock Write-RunlayerLog {}

        Remove-CliScheduleTasksFromFolder -Folder $folder

        ($folder.Deleted -join ",") | Should -Be "CLISchedule"
    }
}
