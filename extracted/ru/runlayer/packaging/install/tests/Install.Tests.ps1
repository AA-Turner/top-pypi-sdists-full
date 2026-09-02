#Requires -Version 5.1

BeforeAll {
    $script:InstallScriptPath = Join-Path (Split-Path -Parent $PSScriptRoot) "install.ps1"
    $script:FixturePath = Join-Path $PSScriptRoot "fixtures/targets.json"
    . $script:InstallScriptPath `
        -RunlayerHost "https://tenant.runlayer.com" `
        -OrgApiKey "rl_org_test"
    $script:InstallText = Get-Content -LiteralPath $script:InstallScriptPath -Raw
    $script:AiWatchSpec = Get-RunlayerPackageSpec -Package "ai-watch"
    $script:CliSpec = Get-RunlayerPackageSpec -Package "cli"
    $script:ValidSignature = [pscustomobject]@{
        Status = "Valid"
        SignerCertificate = [pscustomobject]@{
            Extensions = @(
                [pscustomobject]@{
                    Oid = [pscustomobject]@{ Value = "2.5.29.37" }
                    EnhancedKeyUsages = @(
                        [pscustomobject]@{ Value = "1.3.6.1.5.5.7.3.3" }
                        [pscustomobject]@{ Value = "1.3.6.1.4.1.311.97.321483706.169062785.441198005.491085472" }
                    )
                }
            )
        }
    }
}

Describe "install.ps1" {
    It "does not forward the organization key across HTTP redirects" {
        $script:InstallText | Should -Match (
            '(?s)\$request = \[System\.Net\.WebRequest\]::Create\(\$Uri\).*' +
            '\$request\.AllowAutoRedirect = \$false.*' +
            '\$request\.Headers\.Add\("x-runlayer-api-key", \$ApiKey\)'
        )
    }

    It "rejects a non-HTTPS tenant host before installation" {
        {
            & $script:InstallScriptPath `
                -RunlayerHost "http://tenant.runlayer.com" `
                -OrgApiKey "rl_org_test"
        } | Should -Throw
    }

    It "rejects a non-organization API key before installation" {
        {
            & $script:InstallScriptPath `
                -RunlayerHost "https://tenant.runlayer.com" `
                -OrgApiKey "rl_user_test"
        } | Should -Throw
    }

    It "rejects an unsupported package before installation" {
        {
            & $script:InstallScriptPath `
                -RunlayerHost "https://tenant.runlayer.com" `
                -OrgApiKey "rl_org_test" `
                -Package "desktop"
        } | Should -Throw
    }

    It "selects the one Windows x64 MSI from the AI Watch target" {
        $response = Get-Content -LiteralPath $script:FixturePath -Raw | ConvertFrom-Json

        $target = Select-RunlayerMsi -Response $response -Spec $script:AiWatchSpec

        $target.Version | Should -Be "0.29.15"
        $target.Filename | Should -Be "aiwatch-0.29.15-win-x64.msi"
        $target.Sha256 | Should -Be "4d9c5af680d7cd7d1781c5c0f9f306828fbba5b65e61f3c6f3a611c1496a1392"
        $target.SizeBytes | Should -Be 20
    }

    It "selects the one Windows x64 MSI from the CLI target" {
        $response = Get-Content -LiteralPath $script:FixturePath -Raw | ConvertFrom-Json

        $target = Select-RunlayerMsi -Response $response -Spec $script:CliSpec

        $target.Version | Should -Be "0.29.15"
        $target.Filename | Should -Be "runlayer-0.29.15-win-x64.msi"
        $target.Sha256 | Should -Be "4d9c5af680d7cd7d1781c5c0f9f306828fbba5b65e61f3c6f3a611c1496a1392"
        $target.SizeBytes | Should -Be 20
    }

    It "rejects an ambiguous Windows MSI target" {
        $response = Get-Content -LiteralPath $script:FixturePath -Raw | ConvertFrom-Json
        $windowsArtifact = $response.data[0].resolved_target.artifacts |
            Where-Object { $_.platform -eq "windows" }
        $response.data[0].resolved_target.artifacts += $windowsArtifact

        { Select-RunlayerMsi -Response $response -Spec $script:AiWatchSpec } |
            Should -Throw "*exactly one Windows x64 MSI*"
    }

    It "accepts CLI versions at or above the Windows setup minimum" {
        $minimum = [version]"0.30.7"
        Test-RunlayerVersionSupportsSetup -Version "0.30.7" -MinimumVersion $minimum |
            Should -BeTrue
        Test-RunlayerVersionSupportsSetup -Version "v0.30.7" -MinimumVersion $minimum |
            Should -BeTrue
        Test-RunlayerVersionSupportsSetup -Version "0.30.8" -MinimumVersion $minimum |
            Should -BeTrue
        Test-RunlayerVersionSupportsSetup -Version "0.31.0" -MinimumVersion $minimum |
            Should -BeTrue
        Test-RunlayerVersionSupportsSetup -Version "1.0.0" -MinimumVersion $minimum |
            Should -BeTrue
        Test-RunlayerVersionSupportsSetup -Version "0.30.8-rc.1" -MinimumVersion $minimum |
            Should -BeTrue
    }

    It "rejects CLI versions below the Windows setup minimum" {
        $minimum = [version]"0.30.7"
        Test-RunlayerVersionSupportsSetup -Version "0.30.6" -MinimumVersion $minimum |
            Should -BeFalse
        Test-RunlayerVersionSupportsSetup -Version "0.29.15" -MinimumVersion $minimum |
            Should -BeFalse
        Test-RunlayerVersionSupportsSetup -Version "0.30.7-rc.1" -MinimumVersion $minimum |
            Should -BeFalse
        Test-RunlayerVersionSupportsSetup -Version "bogus" -MinimumVersion $minimum |
            Should -BeFalse
        Test-RunlayerVersionSupportsSetup -Version "0.30" -MinimumVersion $minimum |
            Should -BeFalse
    }

    It "points a too-old CLI target at the manual MSI flow before download" {
        Mock Get-RunlayerMsiTarget {
            [pscustomobject]@{
                Version = "0.30.6"
                Filename = "runlayer-0.30.6-win-x64.msi"
                Sha256 = "4d9c5af680d7cd7d1781c5c0f9f306828fbba5b65e61f3c6f3a611c1496a1392"
                SizeBytes = 20
            }
        }
        Mock Save-RunlayerMsi {}

        {
            Install-RunlayerPackage `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Package "cli"
        } | Should -Throw "*manual MSI flow*"
        Should -Invoke Save-RunlayerMsi -Times 0 -Exactly
    }

    It "does not version-gate AI Watch installs" {
        Mock Get-RunlayerMsiTarget {
            [pscustomobject]@{
                Version = "0.29.15"
                Filename = "aiwatch-0.29.15-win-x64.msi"
                Sha256 = "4d9c5af680d7cd7d1781c5c0f9f306828fbba5b65e61f3c6f3a611c1496a1392"
                SizeBytes = 20
            }
        }
        Mock Save-RunlayerMsi {}
        Mock Invoke-RunlayerVerifiedMsiInstall {}

        {
            Install-RunlayerPackage `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Package "ai-watch"
        } | Should -Not -Throw
        Should -Invoke Invoke-RunlayerVerifiedMsiInstall -Times 1 -Exactly
    }

    It "does not kick CLIUpdate from the unelevated parent after msiexec" {
        # CLIUpdate's SDDL is SYSTEM + Administrators only. The documented Test
        # Device flow pastes this script into a normal PowerShell session and
        # only elevates msiexec via UAC, so Start-ScheduledTask here always
        # access-denies and used to print a failure on every typical install.
        $script:InstallText | Should -Not -Match 'Start-ScheduledTask'
        $script:InstallText | Should -Not -Match 'Start-RunlayerUpdateTask'
        $script:InstallText | Should -Not -Match 'Triggering the first update check'
    }

    It "finishes a CLI install without a parent-session update kick" {
        Mock Get-RunlayerMsiTarget {
            [pscustomobject]@{
                Version = "0.30.7"
                Filename = "runlayer-0.30.7-win-x64.msi"
                Sha256 = "4d9c5af680d7cd7d1781c5c0f9f306828fbba5b65e61f3c6f3a611c1496a1392"
                SizeBytes = 20
            }
        }
        Mock Save-RunlayerMsi {}
        Mock Invoke-RunlayerVerifiedMsiInstall {}

        $installOutput = @(
            Install-RunlayerPackage `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Package "cli"
        ) -join "`n"

        $installOutput | Should -Match "installed successfully"
        $installOutput | Should -Not -Match "Triggering the first update check"
        $installOutput | Should -Not -Match "Could not trigger"
    }

    It "stops streaming a response at its byte limit" {
        $inputBytes = [System.Text.Encoding]::UTF8.GetBytes("response-too-large")
        $inputStream = [System.IO.MemoryStream]::new($inputBytes)
        $outputStream = [System.IO.MemoryStream]::new()
        try {
            {
                Copy-RunlayerLimitedStream `
                    -InputStream $inputStream `
                    -OutputStream $outputStream `
                    -MaximumBytes 8
            } | Should -Throw "*maximum allowed size*"
            $outputStream.Length | Should -BeLessOrEqual 8
        } finally {
            $inputStream.Dispose()
            $outputStream.Dispose()
        }
    }

    It "locks and reverifies the MSI through Windows Installer startup" {
        $msiPath = Join-Path $TestDrive "aiwatch.msi"
        Set-Content -LiteralPath $msiPath -Value "signed-msi" -NoNewline
        $target = [pscustomobject]@{
            Version = "0.29.15"
            Sha256 = (Get-FileHash -LiteralPath $msiPath -Algorithm SHA256).Hash
            SizeBytes = (Get-Item -LiteralPath $msiPath).Length
        }
        Mock Get-RunlayerMsiSignature { $script:ValidSignature }
        Mock Get-RunlayerMsiIdentity {
            [pscustomobject]@{
                ProductName = "Runlayer AI Watch"
                ProductVersion = "0.29.15"
                UpgradeCode = "E3A2F1C0-7B4D-4E9A-8C6F-1D2E3F4A5B6C"
            }
        }
        Mock Invoke-RunlayerMsiInstall {
            {
                $writeHandle = [System.IO.File]::Open(
                    $MsiPath,
                    [System.IO.FileMode]::Open,
                    [System.IO.FileAccess]::Write,
                    [System.IO.FileShare]::None
                )
                $writeHandle.Dispose()
            } | Should -Throw
        }

        {
            Invoke-RunlayerVerifiedMsiInstall `
                -MsiPath $msiPath `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:AiWatchSpec `
                -Target $target
        } | Should -Not -Throw
        Should -Invoke Invoke-RunlayerMsiInstall -Times 1 -Exactly -ParameterFilter {
            $TargetVersion -eq "0.29.15"
        }
    }

    It "accepts the CLI MSI package identity" {
        $identity = [pscustomobject]@{
            ProductName = "Runlayer CLI"
            ProductVersion = "0.30.7"
            UpgradeCode = "9F4B2E71-3C8A-4D5E-A1B2-6E7F8091C2D3"
        }
        $target = [pscustomobject]@{ Version = "0.30.7" }

        {
            Assert-RunlayerMsiIdentity `
                -Identity $identity `
                -Spec $script:CliSpec `
                -Target $target
        } | Should -Not -Throw
    }

    It "rejects an AI Watch MSI offered as the CLI package" {
        $identity = [pscustomobject]@{
            ProductName = "Runlayer AI Watch"
            ProductVersion = "0.30.7"
            UpgradeCode = "E3A2F1C0-7B4D-4E9A-8C6F-1D2E3F4A5B6C"
        }
        $target = [pscustomobject]@{ Version = "0.30.7" }

        {
            Assert-RunlayerMsiIdentity `
                -Identity $identity `
                -Spec $script:CliSpec `
                -Target $target
        } | Should -Throw "*package identity*"
    }

    It "rejects an MSI with the wrong native package identity" {
        $msiPath = Join-Path $TestDrive "wrong-product.msi"
        Set-Content -LiteralPath $msiPath -Value "signed-msi" -NoNewline
        $target = [pscustomobject]@{
            Version = "0.29.15"
            Sha256 = (Get-FileHash -LiteralPath $msiPath -Algorithm SHA256).Hash
            SizeBytes = (Get-Item -LiteralPath $msiPath).Length
        }
        Mock Get-RunlayerMsiSignature { $script:ValidSignature }
        Mock Get-RunlayerMsiIdentity {
            [pscustomobject]@{
                ProductName = "Unrelated Product"
                ProductVersion = "0.29.15"
                UpgradeCode = "E3A2F1C0-7B4D-4E9A-8C6F-1D2E3F4A5B6C"
            }
        }
        Mock Invoke-RunlayerMsiInstall {}

        {
            Invoke-RunlayerVerifiedMsiInstall `
                -MsiPath $msiPath `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:AiWatchSpec `
                -Target $target
        } | Should -Throw "*package identity*"
        Should -Invoke Invoke-RunlayerMsiInstall -Times 0 -Exactly
    }

    It "rejects a valid code-signing certificate without the Runlayer signing identity" {
        $signature = [pscustomobject]@{
            Status = "Valid"
            SignerCertificate = [pscustomobject]@{
                Extensions = @(
                    [pscustomobject]@{
                        Oid = [pscustomobject]@{ Value = "2.5.29.37" }
                        EnhancedKeyUsages = @(
                            [pscustomobject]@{ Value = "1.3.6.1.5.5.7.3.3" }
                        )
                    }
                )
            }
        }

        { Assert-RunlayerMsiSignature -Signature $signature } |
            Should -Throw "*Runlayer signer*"
    }

    It "rejects an MSI without a valid code-signing signature" {
        $msiPath = Join-Path $TestDrive "unsigned.msi"
        Set-Content -LiteralPath $msiPath -Value "unsigned-msi" -NoNewline
        $target = [pscustomobject]@{
            Sha256 = (Get-FileHash -LiteralPath $msiPath -Algorithm SHA256).Hash
            SizeBytes = (Get-Item -LiteralPath $msiPath).Length
        }
        Mock Get-RunlayerMsiSignature {
            [pscustomobject]@{
                Status = "NotSigned"
                SignerCertificate = $null
            }
        }
        Mock Invoke-RunlayerMsiInstall {}

        {
            Invoke-RunlayerVerifiedMsiInstall `
                -MsiPath $msiPath `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:AiWatchSpec `
                -Target $target
        } | Should -Throw "*Authenticode*"
        Should -Invoke Invoke-RunlayerMsiInstall -Times 0 -Exactly
    }

    It "accepts Windows Installer exit code 0" {
        Mock Start-Process {
            [pscustomobject]@{ ExitCode = 0 }
        }

        { Invoke-RunlayerMsiInstall `
                -MsiPath "C:\Temp\aiwatch.msi" `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:AiWatchSpec } | Should -Not -Throw
    }

    It "accepts Windows Installer reboot-required exit code 3010" {
        Mock Start-Process {
            [pscustomobject]@{ ExitCode = 3010 }
        }

        { Invoke-RunlayerMsiInstall `
                -MsiPath "C:\Temp\aiwatch.msi" `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:AiWatchSpec } | Should -Not -Throw
    }

    It "passes the CLI tenant properties to msiexec" {
        Mock Start-Process {
            [pscustomobject]@{ ExitCode = 0 }
        }

        {
            Invoke-RunlayerMsiInstall `
                -MsiPath "C:\Temp\runlayer.msi" `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:CliSpec
        } | Should -Not -Throw

        $expectedArguments = (
            '/i "C:\Temp\runlayer.msi" /qb! ' +
            'CLI_HOST=https://tenant.runlayer.com ' +
            'CLI_ORG_API_KEY=rl_org_test'
        )
        Should -Invoke Start-Process -Times 1 -Exactly -ParameterFilter {
            ($ArgumentList -join " ") -eq $expectedArguments
        }
    }

    It "forces a full reinstall when bootstrap targets the installed version" {
        Mock Get-RunlayerInstalledProductVersion { "0.29.15" }
        Mock Start-Process {
            [pscustomobject]@{ ExitCode = 0 }
        }

        {
            Invoke-RunlayerMsiInstall `
                -MsiPath "C:\Temp\aiwatch.msi" `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:AiWatchSpec `
                -TargetVersion "0.29.15"
        } | Should -Not -Throw

        $expectedArguments = (
            '/i "C:\Temp\aiwatch.msi" /qb! ' +
            'AIWATCH_HOST=https://tenant.runlayer.com ' +
            'AIWATCH_ORG_API_KEY=rl_org_test ' +
            'REINSTALL=ALL REINSTALLMODE=amus'
        )
        Should -Invoke Start-Process -Times 1 -Exactly -ParameterFilter {
            ($ArgumentList -join " ") -eq $expectedArguments
        }
    }

    It "detects the installed product with the package upgrade code" {
        Mock Get-RunlayerInstalledProductVersion { "0.30.7" } -ParameterFilter {
            $Spec.Package -eq "cli"
        }
        Mock Start-Process {
            [pscustomobject]@{ ExitCode = 0 }
        }

        {
            Invoke-RunlayerMsiInstall `
                -MsiPath "C:\Temp\runlayer.msi" `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:CliSpec `
                -TargetVersion "0.30.7"
        } | Should -Not -Throw

        $expectedArguments = (
            '/i "C:\Temp\runlayer.msi" /qb! ' +
            'CLI_HOST=https://tenant.runlayer.com ' +
            'CLI_ORG_API_KEY=rl_org_test ' +
            'REINSTALL=ALL REINSTALLMODE=amus'
        )
        Should -Invoke Start-Process -Times 1 -Exactly -ParameterFilter {
            ($ArgumentList -join " ") -eq $expectedArguments
        }
    }

    It "keeps major upgrades on the normal install path" {
        Mock Get-RunlayerInstalledProductVersion { "0.29.14" }
        Mock Start-Process {
            [pscustomobject]@{ ExitCode = 0 }
        }

        {
            Invoke-RunlayerMsiInstall `
                -MsiPath "C:\Temp\aiwatch.msi" `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:AiWatchSpec `
                -TargetVersion "0.29.15"
        } | Should -Not -Throw

        $expectedArguments = (
            '/i "C:\Temp\aiwatch.msi" /qb! ' +
            'AIWATCH_HOST=https://tenant.runlayer.com ' +
            'AIWATCH_ORG_API_KEY=rl_org_test'
        )
        Should -Invoke Start-Process -Times 1 -Exactly -ParameterFilter {
            ($ArgumentList -join " ") -eq $expectedArguments
        }
    }

    It "reports a declined UAC prompt for exit code 1602" {
        Mock Start-Process {
            [pscustomobject]@{ ExitCode = 1602 }
        }

        { Invoke-RunlayerMsiInstall `
                -MsiPath "C:\Temp\aiwatch.msi" `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:AiWatchSpec } | Should -Throw "*cancelled*UAC*"
    }

    It "fails every other Windows Installer exit code" {
        Mock Start-Process {
            [pscustomobject]@{ ExitCode = 1603 }
        }

        { Invoke-RunlayerMsiInstall `
                -MsiPath "C:\Temp\aiwatch.msi" `
                -TenantHost "https://tenant.runlayer.com" `
                -ApiKey "rl_org_test" `
                -Spec $script:AiWatchSpec } | Should -Throw "*1603*"
    }
}
