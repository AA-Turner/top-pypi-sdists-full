#Requires -Version 5.1
# Pester coverage for the full CLI's package-owned Windows update task.

BeforeAll {
    $script:ScheduledTaskDir = Split-Path -Parent $PSScriptRoot
    $script:WindowsPackagingDir = Split-Path -Parent $script:ScheduledTaskDir
    $script:CliTaskSourceDir = Join-Path $script:WindowsPackagingDir "cli-update-task"
    $script:CliTaskDir = Join-Path $TestDrive "cli-update-task"
    New-Item -ItemType Directory -Path $script:CliTaskDir | Out-Null
    Copy-Item (Join-Path $script:CliTaskSourceDir "register-tasks.ps1") $script:CliTaskDir
    Copy-Item (Join-Path $script:CliTaskSourceDir "unregister-tasks.ps1") $script:CliTaskDir
    Copy-Item (Join-Path $script:ScheduledTaskDir "RunlayerTaskCommon.ps1") $script:CliTaskDir
    $script:CliRegisterPath = Join-Path $script:CliTaskDir "register-tasks.ps1"
    $script:CliUnregisterPath = Join-Path $script:CliTaskDir "unregister-tasks.ps1"
    $script:ExpectedUpdateSddl = "D:P(A;;GA;;;SY)(A;;GA;;;BA)"
    $script:OnWindows = $PSVersionTable.PSEdition -eq 'Desktop' -or $IsWindows

    . $script:CliRegisterPath
}

Describe "full CLI update task registration" {
    It "requires SYSTEM and never kicks the updater during MSI install" {
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

        It "registers a protected hourly SYSTEM task with no catch-up setting" {
            Register-CliUpdateTask
            $expectedExePath = Join-Path (Split-Path -Parent $script:CliTaskDir) "runlayer.exe"

            Should -Invoke New-ScheduledTaskAction -Times 1 -Exactly -ParameterFilter {
                $Execute -eq $expectedExePath -and
                $Argument -eq "__scheduled-update"
            }
            Should -Invoke New-ScheduledTaskPrincipal -Times 1 -Exactly -ParameterFilter {
                $UserId -eq "SYSTEM" -and
                $LogonType -eq "ServiceAccount" -and
                $RunLevel -eq "Highest"
            }
            Should -Invoke New-ScheduledTaskTrigger -Times 1 -Exactly -ParameterFilter {
                $Once -and
                $RepetitionInterval.TotalMinutes -eq 60 -and
                $At -gt (Get-Date).AddMinutes(1) -and
                $At -lt (Get-Date).AddMinutes(3)
            }
            Should -Invoke New-ScheduledTaskSettingsSet -Times 1 -Exactly -ParameterFilter {
                $Hidden -eq $true -and
                $MultipleInstances -eq "IgnoreNew" -and
                -not $StartWhenAvailable
            }
            Should -Invoke Register-ScheduledTask -Times 1 -Exactly -ParameterFilter {
                $TaskName -eq "CLIUpdate" -and
                $TaskPath -eq "\Runlayer\" -and
                $Force -eq $true
            }
            Should -Invoke Set-RunlayerTaskSecurity -Times 1 -Exactly -ParameterFilter {
                $TaskName -eq "CLIUpdate" -and
                $Sddl -eq $script:ExpectedUpdateSddl
            }
        }
    }
}

Describe "full CLI update task removal" {
    BeforeAll {
        . $script:CliUnregisterPath
    }

    It "owns only CLIUpdate and CLIUpdateHandoff" {
        $text = Get-Content $script:CliUnregisterPath -Raw

        $text | Should -Match '\$script:CliTaskNames = @\("CLIUpdate", "CLIUpdateHandoff"\)'
        $text | Should -Not -Match 'AIWatchUpdate'
        $text | Should -Match 'GetTasks\(1\)'
        $text | Should -Match 'preserved shared \\Runlayer task folder'
    }

    It "continues deleting CLI-owned tasks after one deletion fails" {
        $tasks = @(
            [pscustomobject]@{ Name = "CLIUpdate" },
            [pscustomobject]@{ Name = "CLIUpdateHandoff" }
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
            if ($TaskName -eq "CLIUpdate") {
                throw "simulated delete failure"
            }
            [void]$this.Deleted.Add($TaskName)
        }
        Mock Write-RunlayerLog {}

        Remove-CliUpdateTasksFromFolder -Folder $folder

        ($folder.Deleted -join ",") | Should -Be "CLIUpdateHandoff"
        Should -Invoke Write-RunlayerLog -Times 1 -Exactly -ParameterFilter {
            $Message -match 'failed to delete CLIUpdate'
        }
    }
}
