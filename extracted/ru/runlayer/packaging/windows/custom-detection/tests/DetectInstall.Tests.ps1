#Requires -Version 5.1
# Pester tests for the AI Watch Intune Win32 custom detection script
# (detect-install.ps1). Behavioral tests (mock the cmdlets / spawn a Windows
# PowerShell host) are Windows-only and skip elsewhere.
#
# detect-install.ps1 is dot-sourced; its `if ($MyInvocation.InvocationName -ne '.')`
# guard means dot-sourcing loads Test-AiWatchInstalled without running the main body.

BeforeAll {
    $script:DetectDir = Split-Path -Parent $PSScriptRoot
    $script:DetectScriptPath = Join-Path $script:DetectDir "detect-install.ps1"
    $script:OnWindows = $PSVersionTable.PSEdition -eq 'Desktop' -or $IsWindows
}

Describe "detect-install.ps1" {
    BeforeAll { . $script:DetectScriptPath }

    Context "Test-AiWatchInstalled" -Skip:(-not $OnWindows) {
        BeforeEach {
            # Keep the breadcrumb side-log off disk during tests.
            Mock New-Item {}
            Mock Add-Content {}
        }

        It "is not installed when aiwatch.exe is missing" {
            Mock Test-Path { $false }
            Test-AiWatchInstalled | Should -BeFalse
        }

        It "is not installed when the AIWatchScan task is missing" {
            Mock Test-Path { $true }
            Mock Get-Item { [pscustomobject]@{ VersionInfo = [pscustomobject]@{ FileVersion = "1.2.3" } } }
            Mock Get-ScheduledTask { $null }
            Test-AiWatchInstalled -MinimumVersion "0.0.0" | Should -BeFalse
        }

        It "is not installed when AIWatchUpdate is missing" {
            Mock Test-Path { $true }
            Mock Get-Item { [pscustomobject]@{ VersionInfo = [pscustomobject]@{ FileVersion = "1.2.3" } } }
            Mock Get-ScheduledTask {
                if ($TaskName -eq "AIWatchScan") {
                    return [pscustomobject]@{ TaskName = $TaskName }
                }
                return $null
            }
            Test-AiWatchInstalled -MinimumVersion "0.0.0" | Should -BeFalse
        }

        It "is installed when exe, AIWatchScan, and AIWatchUpdate are present without AIWatchHooks" {
            Mock Test-Path { $true }
            Mock Get-Item { [pscustomobject]@{ VersionInfo = [pscustomobject]@{ FileVersion = "1.2.3" } } }
            Mock Get-ScheduledTask {
                if ($TaskName -in @("AIWatchScan", "AIWatchUpdate")) {
                    return [pscustomobject]@{ TaskName = $TaskName }
                }
                return $null
            }
            Test-AiWatchInstalled -MinimumVersion "0.0.0" | Should -BeTrue
            Should -Invoke Get-ScheduledTask -Times 0 -Exactly -ParameterFilter {
                $TaskName -eq "AIWatchHooks"
            }
        }

        It "is not installed when the installed version is below the minimum" {
            Mock Test-Path { $true }
            Mock Get-Item { [pscustomobject]@{ VersionInfo = [pscustomobject]@{ FileVersion = "1.2.3" } } }
            Mock Get-ScheduledTask { [pscustomobject]@{ TaskName = "AIWatchScan" } }
            Test-AiWatchInstalled -MinimumVersion "9.9.9" | Should -BeFalse
        }

        It "side-logs the failing branch as a breadcrumb" {
            Mock Test-Path { $false }
            Test-AiWatchInstalled | Out-Null
            Should -Invoke Add-Content -ParameterFilter {
                $Value -like "*not-installed*aiwatch.exe missing*"
            }
        }
    }

    # ENG-3770 regression. Intune's Win32 custom-detection contract treats ANY
    # byte on STDERR as not-installed, even with a non-empty STDOUT + exit 0.
    # PowerShell maps the Warning / Verbose / Progress / Debug / Information
    # streams onto the process's STDERR, so a stray record from a detection-path
    # cmdlet (here Get-ScheduledTask, which is exactly where the ScheduledTasks
    # module can emit one under a non-admin context) would flip a correctly
    # detected install to not-installed. Run the real script in a child host with
    # STDOUT / STDERR redirected to separate files — the same descriptors the
    # Intune Management Extension captures — and prove the success marker lands on
    # STDOUT while STDERR stays empty.
    #
    # Windows-only: relies on the Windows PowerShell host mapping the warning
    # stream to the process STDERR fd, and on the detection script's runtime path.
    Context "STDERR contract (ENG-3770)" -Skip:(-not $OnWindows) {
        BeforeAll {
            function Invoke-DetectChild {
                # Run $ScriptBody in a child host with the OS STDOUT / STDERR fds
                # redirected to separate files, then return both plus the exit
                # code. Spawn Windows PowerShell 5.1 (powershell.exe) explicitly:
                # that is the host the Intune Management Extension uses to run the
                # detection script, and it is the host that routes the
                # Warning/Verbose/Debug/Information streams onto the process STDERR
                # fd (PowerShell 7 / pwsh routes them to STDOUT, so spawning the
                # current host would not faithfully reproduce the IME's STDERR
                # contamination). Falls back to the current host if 5.1 is absent.
                param([string]$ScriptBody)
                $winPs = Join-Path $env:WINDIR "System32\WindowsPowerShell\v1.0\powershell.exe"
                $exe = if (Test-Path $winPs) { $winPs } else { (Get-Process -Id $PID).Path }
                $base = Join-Path ([System.IO.Path]::GetTempPath()) ("rl-detect-{0}" -f [guid]::NewGuid())
                $tmp = "$base.ps1"
                $outFile = "$base.out"
                $errFile = "$base.err"
                Set-Content -LiteralPath $tmp -Value $ScriptBody -Encoding UTF8
                try {
                    $proc = Start-Process -FilePath $exe `
                        -ArgumentList @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", $tmp) `
                        -RedirectStandardOutput $outFile -RedirectStandardError $errFile `
                        -NoNewWindow -Wait -PassThru
                    return [pscustomobject]@{
                        ExitCode = $proc.ExitCode
                        StdOut   = (Get-Content -LiteralPath $outFile -Raw)
                        StdErr   = (Get-Content -LiteralPath $errFile -Raw)
                    }
                } finally {
                    Remove-Item -LiteralPath $tmp, $outFile, $errFile -Force -ErrorAction SilentlyContinue
                }
            }
        }

        It "puts the success marker on STDOUT and nothing on STDERR when a detection cmdlet emits a warning" {
            # Shadow the detection cmdlets so the script takes the 'installed'
            # branch, but have Get-ScheduledTask emit a stray warning the way the
            # ScheduledTasks module can under a non-admin context. Pre-fix that
            # warning reaches STDERR (default $WarningPreference = Continue) and
            # Intune reports not-installed; the fix silences + redirects it.
            $body = @"
function Test-Path { `$true }
function Get-Item { [pscustomobject]@{ VersionInfo = [pscustomobject]@{ FileVersion = '9.9.9' } } }
function Get-ScheduledTask { Write-Warning 'stray ScheduledTasks autoload record'; [pscustomobject]@{ TaskName = 'AIWatchScan' } }
function New-Item { }
function Add-Content { }
& '$($script:DetectScriptPath)'
"@
            $result = Invoke-DetectChild -ScriptBody $body
            $result.StdOut | Should -Match 'AI Watch installed'
            [string]::IsNullOrWhiteSpace($result.StdErr) | Should -BeTrue
        }
    }
}
