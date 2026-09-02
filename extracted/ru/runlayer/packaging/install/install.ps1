#Requires -Version 5.1

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^https://[^\s/]+(?:/[^\s]*)?$')]
    [string]$RunlayerHost,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^rl_org_[A-Za-z0-9_-]+$')]
    [string]$OrgApiKey,

    [ValidateSet("ai-watch", "cli")]
    [string]$Package = "ai-watch"
)

$ErrorActionPreference = "Stop"
$script:MaximumTargetBytes = 1048576
$script:MaximumInstallerBytes = 536870912
$script:AiWatchUpgradeCode = "{E3A2F1C0-7B4D-4E9A-8C6F-1D2E3F4A5B6C}"
$script:CliUpgradeCode = "{9F4B2E71-3C8A-4D5E-A1B2-6E7F8091C2D3}"
# First cli release whose MSI accepts the CLI_HOST / CLI_ORG_API_KEY tenant
# properties; older MSIs silently ignore them, leaving the device unconfigured.
$script:CliMinimumWindowsSetupVersion = [version]"0.30.7"
$script:ManualFlowDocsUrl = "https://docs.runlayer.com/shadow-ai/deploy/test-device#manual-installation-fallback"

function Get-RunlayerPackageSpec {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet("ai-watch", "cli")]
        [string]$Package
    )

    if ($Package -eq "cli") {
        return [pscustomobject]@{
            Package         = "cli"
            DisplayName     = "Runlayer CLI"
            ProductName     = "Runlayer CLI"
            UpgradeCode     = $script:CliUpgradeCode
            HostProperty    = "CLI_HOST"
            ApiKeyProperty  = "CLI_ORG_API_KEY"
            MinimumVersion  = $script:CliMinimumWindowsSetupVersion
            TempFilePrefix  = "runlayer-cli"
        }
    }
    return [pscustomobject]@{
        Package         = "ai-watch"
        DisplayName     = "Runlayer AI Watch"
        ProductName     = "Runlayer AI Watch"
        UpgradeCode     = $script:AiWatchUpgradeCode
        HostProperty    = "AIWATCH_HOST"
        ApiKeyProperty  = "AIWATCH_ORG_API_KEY"
        MinimumVersion  = $null
        TempFilePrefix  = "runlayer-aiwatch"
    }
}

function Test-RunlayerVersionSupportsSetup {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Version,

        [Parameter(Mandatory = $true)]
        [version]$MinimumVersion
    )

    $normalized = $Version.TrimStart([char[]]"v")
    $withoutBuild = ($normalized -split '\+', 2)[0]
    $core = ($withoutBuild -split '-', 2)[0]
    $isPrerelease = $withoutBuild -ne $core
    $parts = $core -split '\.'
    if ($parts.Count -ne 3) {
        return $false
    }
    foreach ($part in $parts) {
        if ($part -notmatch '^[0-9]+$') {
            return $false
        }
    }
    $parsed = [version]$core
    if ($parsed -gt $MinimumVersion) {
        return $true
    }
    if ($parsed -lt $MinimumVersion) {
        return $false
    }
    return -not $isPrerelease
}

function Get-RunlayerHttpStatusCode {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [System.Management.Automation.ErrorRecord]$ErrorRecord
    )

    $exception = $ErrorRecord.Exception
    $response = $exception.Response
    while ($null -eq $response -and $null -ne $exception.InnerException) {
        $exception = $exception.InnerException
        $response = $exception.Response
    }
    if ($null -eq $response -or $null -eq $response.StatusCode) {
        return $null
    }
    return [int]$response.StatusCode
}

function Copy-RunlayerLimitedStream {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [System.IO.Stream]$InputStream,

        [Parameter(Mandatory = $true)]
        [System.IO.Stream]$OutputStream,

        [Parameter(Mandatory = $true)]
        [long]$MaximumBytes
    )

    $buffer = [byte[]]::new(65536)
    $totalBytes = [long]0
    while (($bytesRead = $InputStream.Read($buffer, 0, $buffer.Length)) -gt 0) {
        if ($totalBytes + $bytesRead -gt $MaximumBytes) {
            throw "The response exceeds the maximum allowed size."
        }
        $OutputStream.Write($buffer, 0, $bytesRead)
        $totalBytes += $bytesRead
    }
    return $totalBytes
}

function Invoke-RunlayerLimitedDownload {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [uri]$Uri,

        [Parameter(Mandatory = $true)]
        [string]$ApiKey,

        [Parameter(Mandatory = $true)]
        [string]$Destination,

        [Parameter(Mandatory = $true)]
        [long]$MaximumBytes,

        [Parameter(Mandatory = $true)]
        [int]$TimeoutSeconds
    )

    $request = [System.Net.WebRequest]::Create($Uri)
    $request.Method = "GET"
    $request.AllowAutoRedirect = $false
    $request.Headers.Add("x-runlayer-api-key", $ApiKey)
    $request.Timeout = $TimeoutSeconds * 1000
    $request.ReadWriteTimeout = $TimeoutSeconds * 1000
    $response = $null
    $inputStream = $null
    $outputStream = $null
    try {
        $response = $request.GetResponse()
        if ($response.ContentLength -gt $MaximumBytes) {
            throw "The response exceeds the maximum allowed size."
        }

        $inputStream = $response.GetResponseStream()
        $outputStream = [System.IO.File]::Open(
            $Destination,
            [System.IO.FileMode]::Create,
            [System.IO.FileAccess]::Write,
            [System.IO.FileShare]::None
        )
        $bytesWritten = Copy-RunlayerLimitedStream `
            -InputStream $inputStream `
            -OutputStream $outputStream `
            -MaximumBytes $MaximumBytes
        $headers = @{}
        foreach ($headerName in $response.Headers.AllKeys) {
            $headers[$headerName] = $response.Headers[$headerName]
        }

        return [pscustomobject]@{
            BytesWritten = $bytesWritten
            Headers = $headers
            StatusCode = [int]$response.StatusCode
        }
    } finally {
        if ($null -ne $outputStream) {
            $outputStream.Dispose()
        }
        if ($null -ne $inputStream) {
            $inputStream.Dispose()
        }
        if ($null -ne $response) {
            $response.Dispose()
        }
    }
}

function Select-RunlayerMsi {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [object]$Response,

        [Parameter(Mandatory = $true)]
        [object]$Spec
    )

    $rows = @(
        $Response.data |
            Where-Object { $null -ne $_ -and $_.package -eq $Spec.Package }
    )
    if ($rows.Count -ne 1 -or $null -eq $rows[0].resolved_target) {
        throw "The backend returned no unambiguous $($Spec.DisplayName) target."
    }

    $target = $rows[0].resolved_target
    $artifactMatches = @(
        $target.artifacts |
            Where-Object {
                $null -ne $_ -and
                $_.platform -eq "windows" -and
                $_.arch -eq "x64" -and
                $_.format -eq "msi" -and
                $null -eq $_.variant
            }
    )
    if ($artifactMatches.Count -ne 1) {
        throw "Expected exactly one Windows x64 MSI; found $($artifactMatches.Count)."
    }

    $artifact = $artifactMatches[0]
    $version = [string]$target.version
    $filename = [string]$artifact.filename
    $sha256 = ([string]$artifact.sha256).ToLowerInvariant()
    $sizeBytes = [long]$artifact.size_bytes

    if ($version -notmatch '^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$') {
        throw "The backend returned an unsafe package version."
    }
    if (
        $filename -notmatch '^[A-Za-z0-9][A-Za-z0-9._+-]{0,254}$' -or
        $filename -in @(".", "..") -or
        $filename.Contains("/") -or
        $filename.Contains("\")
    ) {
        throw "The backend returned an unsafe installer filename."
    }
    if ($sha256 -notmatch '^[a-f0-9]{64}$') {
        throw "The backend returned an invalid installer checksum."
    }
    if ($sizeBytes -le 0 -or $sizeBytes -gt $script:MaximumInstallerBytes) {
        throw "The backend returned an invalid installer size."
    }

    return [pscustomobject]@{
        Version   = $version
        Filename  = $filename
        Sha256    = $sha256
        SizeBytes = $sizeBytes
    }
}

function Get-RunlayerMsiTarget {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$TenantHost,

        [Parameter(Mandatory = $true)]
        [string]$ApiKey,

        [Parameter(Mandatory = $true)]
        [object]$Spec
    )

    $uri = "$TenantHost/api/v1/binary-packages/targets"
    $targetPath = [System.IO.Path]::GetTempFileName()
    try {
        Invoke-RunlayerLimitedDownload `
            -Uri $uri `
            -ApiKey $ApiKey `
            -Destination $targetPath `
            -MaximumBytes $script:MaximumTargetBytes `
            -TimeoutSeconds 60 | Out-Null
        $response = Get-Content -LiteralPath $targetPath -Raw | ConvertFrom-Json
    } catch {
        $statusCode = Get-RunlayerHttpStatusCode -ErrorRecord $_
        if ($statusCode -in @(401, 403)) {
            throw "The organization API key is invalid or lacks the Shadow AI Scan role."
        }
        throw "Could not resolve the $($Spec.DisplayName) package from $TenantHost."
    } finally {
        Remove-Item -LiteralPath $targetPath -Force -ErrorAction SilentlyContinue
    }

    return Select-RunlayerMsi -Response $response -Spec $Spec
}

function Save-RunlayerMsi {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$TenantHost,

        [Parameter(Mandatory = $true)]
        [string]$ApiKey,

        [Parameter(Mandatory = $true)]
        [object]$Spec,

        [Parameter(Mandatory = $true)]
        [object]$Target,

        [Parameter(Mandatory = $true)]
        [string]$Destination
    )

    $encodedPackage = [uri]::EscapeDataString([string]$Spec.Package)
    $encodedVersion = [uri]::EscapeDataString([string]$Target.Version)
    $encodedFilename = [uri]::EscapeDataString([string]$Target.Filename)
    $uri = "$TenantHost/api/v1/binary-packages/$encodedPackage/$encodedVersion/$encodedFilename"
    try {
        $downloadResponse = Invoke-RunlayerLimitedDownload `
            -Uri $uri `
            -ApiKey $ApiKey `
            -Destination $Destination `
            -MaximumBytes $script:MaximumInstallerBytes `
            -TimeoutSeconds 900
    } catch {
        $statusCode = Get-RunlayerHttpStatusCode -ErrorRecord $_
        switch ($statusCode) {
            401 {
                throw "The organization API key is invalid."
            }
            403 {
                throw "The organization API key cannot download this package."
            }
            409 {
                throw "The selected installer is not cached yet; retry in a minute."
            }
            404 {
                throw "The selected installer is no longer available; refresh the setup guide."
            }
            503 {
                throw "Binary package downloads are not configured on this Runlayer instance."
            }
            default {
                throw "Could not download the selected $($Spec.DisplayName) installer."
            }
        }
    }

    $headerSha256 = [string]$downloadResponse.Headers["x-runlayer-sha256"]
    if ($headerSha256 -ine [string]$Target.Sha256) {
        throw "The installer checksum header does not match the selected target."
    }
    $download = Get-Item -LiteralPath $Destination
    if ($download.Length -ne [long]$Target.SizeBytes) {
        throw "The downloaded installer size does not match the selected target."
    }
    $actualSha256 = (Get-FileHash -LiteralPath $Destination -Algorithm SHA256).Hash
    if ($actualSha256 -ine [string]$Target.Sha256) {
        throw "The downloaded installer checksum does not match the selected target."
    }
}

function Get-RunlayerMsiSignature {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$MsiPath
    )

    return Get-AuthenticodeSignature -LiteralPath $MsiPath
}

function Assert-RunlayerMsiSignature {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [object]$Signature
    )

    if ([string]$Signature.Status -ne "Valid" -or $null -eq $Signature.SignerCertificate) {
        throw "The installer does not have a valid Authenticode signature."
    }

    $codeSigningOid = "1.3.6.1.5.5.7.3.3"
    # Keep in sync with WINDOWS_SIGNER_IDENTITY_EKU_OID in windows_installer_verifier.py.
    $runlayerSigningIdentityOid = "1.3.6.1.4.1.311.97.321483706.169062785.441198005.491085472"
    $ekuOids = @(
        foreach ($extension in @($Signature.SignerCertificate.Extensions)) {
            if ([string]$extension.Oid.Value -eq "2.5.29.37") {
                foreach ($enhancedKeyUsage in @($extension.EnhancedKeyUsages)) {
                    [string]$enhancedKeyUsage.Value
                }
            }
        }
    )
    if ($codeSigningOid -notin $ekuOids) {
        throw "The installer signing certificate is not valid for code signing."
    }
    if ($runlayerSigningIdentityOid -notin $ekuOids) {
        throw "The installer signing certificate does not match the expected Runlayer signer."
    }
}

function Get-RunlayerMsiIdentity {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$MsiPath
    )

    $installer = $null
    $database = $null
    $view = $null
    $record = $null
    try {
        $installer = New-Object -ComObject WindowsInstaller.Installer
        $database = $installer.GetType().InvokeMember(
            "OpenDatabase",
            [System.Reflection.BindingFlags]::InvokeMethod,
            $null,
            $installer,
            @($MsiPath, 0)
        )
        $view = $database.GetType().InvokeMember(
            "OpenView",
            [System.Reflection.BindingFlags]::InvokeMethod,
            $null,
            $database,
            @('SELECT `Property`, `Value` FROM `Property`')
        )
        $view.GetType().InvokeMember(
            "Execute",
            [System.Reflection.BindingFlags]::InvokeMethod,
            $null,
            $view,
            $null
        ) | Out-Null

        $properties = @{}
        while ($true) {
            $record = $view.GetType().InvokeMember(
                "Fetch",
                [System.Reflection.BindingFlags]::InvokeMethod,
                $null,
                $view,
                $null
            )
            if ($null -eq $record) {
                break
            }
            $propertyName = $record.GetType().InvokeMember(
                "StringData",
                [System.Reflection.BindingFlags]::GetProperty,
                $null,
                $record,
                @([int]1)
            )
            if ($propertyName -in @("ProductName", "ProductVersion", "UpgradeCode")) {
                $properties[$propertyName] = $record.GetType().InvokeMember(
                    "StringData",
                    [System.Reflection.BindingFlags]::GetProperty,
                    $null,
                    $record,
                    @([int]2)
                )
            }
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($record)
            $record = $null
        }

        return [pscustomobject]@{
            ProductName = [string]$properties.ProductName
            ProductVersion = [string]$properties.ProductVersion
            UpgradeCode = [string]$properties.UpgradeCode
        }
    } finally {
        if ($null -ne $record) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($record)
        }
        if ($null -ne $view) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($view)
        }
        if ($null -ne $database) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($database)
        }
        if ($null -ne $installer) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($installer)
        }
    }
}

function Assert-RunlayerMsiIdentity {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [object]$Identity,

        [Parameter(Mandatory = $true)]
        [object]$Spec,

        [Parameter(Mandatory = $true)]
        [object]$Target
    )

    $expectedVersion = ([string]$Target.Version).TrimStart([char[]]"v")
    $expectedUpgradeCode = ([string]$Spec.UpgradeCode).Trim([char[]]"{}")
    $actualUpgradeCode = ([string]$Identity.UpgradeCode).Trim([char[]]"{}")
    if (
        [string]$Identity.ProductName -ne [string]$Spec.ProductName -or
        [string]$Identity.ProductVersion -ne $expectedVersion -or
        $actualUpgradeCode -ine $expectedUpgradeCode
    ) {
        throw "The installer has an unexpected Windows package identity."
    }
}

function Get-RunlayerInstalledProductVersion {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [object]$Spec
    )

    $installer = New-Object -ComObject "WindowsInstaller.Installer"
    try {
        $relatedProducts = $installer.GetType().InvokeMember(
            "RelatedProducts",
            [System.Reflection.BindingFlags]::GetProperty,
            $null,
            $installer,
            [string]$Spec.UpgradeCode
        )
        $productCodes = @(
            foreach ($productCode in $relatedProducts) {
                if (-not [string]::IsNullOrEmpty([string]$productCode)) {
                    [string]$productCode
                }
            }
        )
        if ($productCodes.Count -eq 0) {
            return $null
        }
        if ($productCodes.Count -ne 1) {
            throw "Expected exactly one installed $($Spec.DisplayName) product."
        }

        $version = $installer.GetType().InvokeMember(
            "ProductInfo",
            [System.Reflection.BindingFlags]::GetProperty,
            $null,
            $installer,
            @($productCodes[0], "VersionString")
        )
        if ([string]::IsNullOrEmpty([string]$version)) {
            throw "The installed $($Spec.DisplayName) product version is unavailable."
        }
        return [string]$version
    } finally {
        if ([System.Runtime.InteropServices.Marshal]::IsComObject($installer)) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($installer)
        }
    }
}

function Invoke-RunlayerMsiInstall {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$MsiPath,

        [Parameter(Mandatory = $true)]
        [string]$TenantHost,

        [Parameter(Mandatory = $true)]
        [string]$ApiKey,

        [Parameter(Mandatory = $true)]
        [object]$Spec,

        [AllowNull()]
        [string]$TargetVersion
    )

    $arguments = @(
        "/i"
        "`"$MsiPath`""
        "/qb!"
        "$($Spec.HostProperty)=$TenantHost"
        "$($Spec.ApiKeyProperty)=$ApiKey"
    )
    if (-not [string]::IsNullOrEmpty($TargetVersion)) {
        $installedVersion = Get-RunlayerInstalledProductVersion -Spec $Spec
        if ($installedVersion -eq $TargetVersion) {
            $arguments += @("REINSTALL=ALL", "REINSTALLMODE=amus")
        }
    }
    $process = Start-Process `
        -FilePath "msiexec.exe" `
        -ArgumentList $arguments `
        -Wait `
        -PassThru

    if ($process.ExitCode -eq 1602) {
        throw "Installation was cancelled at the UAC prompt."
    }
    if ($process.ExitCode -notin @(0, 3010)) {
        throw "Windows Installer failed with exit code $($process.ExitCode)."
    }
}

function Invoke-RunlayerVerifiedMsiInstall {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$MsiPath,

        [Parameter(Mandatory = $true)]
        [string]$TenantHost,

        [Parameter(Mandatory = $true)]
        [string]$ApiKey,

        [Parameter(Mandatory = $true)]
        [object]$Spec,

        [Parameter(Mandatory = $true)]
        [object]$Target
    )

    $lockedMsi = [System.IO.File]::Open(
        $MsiPath,
        [System.IO.FileMode]::Open,
        [System.IO.FileAccess]::Read,
        [System.IO.FileShare]::Read
    )
    try {
        if ($lockedMsi.Length -ne [long]$Target.SizeBytes) {
            throw "The protected installer size does not match the selected target."
        }
        $actualSha256 = (Get-FileHash -InputStream $lockedMsi -Algorithm SHA256).Hash
        if ($actualSha256 -ine [string]$Target.Sha256) {
            throw "The protected installer checksum does not match the selected target."
        }
        $signature = Get-RunlayerMsiSignature -MsiPath $MsiPath
        Assert-RunlayerMsiSignature -Signature $signature
        $identity = Get-RunlayerMsiIdentity -MsiPath $MsiPath
        Assert-RunlayerMsiIdentity -Identity $identity -Spec $Spec -Target $Target

        Invoke-RunlayerMsiInstall `
            -MsiPath $MsiPath `
            -TenantHost $TenantHost `
            -ApiKey $ApiKey `
            -Spec $Spec `
            -TargetVersion ([string]$identity.ProductVersion)
    } finally {
        $lockedMsi.Dispose()
    }
}

function Install-RunlayerPackage {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$TenantHost,

        [Parameter(Mandatory = $true)]
        [string]$ApiKey,

        [Parameter(Mandatory = $true)]
        [ValidateSet("ai-watch", "cli")]
        [string]$Package
    )

    $spec = Get-RunlayerPackageSpec -Package $Package
    $normalizedHost = $TenantHost.TrimEnd("/")
    Write-Output "Resolving the $($spec.DisplayName) package selected by your Client Updates policy..."
    $target = Get-RunlayerMsiTarget `
        -TenantHost $normalizedHost `
        -ApiKey $ApiKey `
        -Spec $spec
    if (
        $null -ne $spec.MinimumVersion -and
        -not (Test-RunlayerVersionSupportsSetup `
            -Version ([string]$target.Version) `
            -MinimumVersion $spec.MinimumVersion)
    ) {
        throw (
            "One-command setup requires $($spec.DisplayName) version " +
            "$($spec.MinimumVersion) or newer; use the manual MSI flow at " +
            "$script:ManualFlowDocsUrl."
        )
    }
    $tempPath = Join-Path `
        ([System.IO.Path]::GetTempPath()) `
        ("{0}-{1}.msi" -f $spec.TempFilePrefix, [guid]::NewGuid())

    try {
        Write-Output "Downloading $($target.Filename)..."
        Save-RunlayerMsi `
            -TenantHost $normalizedHost `
            -ApiKey $ApiKey `
            -Spec $spec `
            -Target $target `
            -Destination $tempPath
        Write-Output "Starting Windows Installer..."
        Invoke-RunlayerVerifiedMsiInstall `
            -MsiPath $tempPath `
            -TenantHost $normalizedHost `
            -ApiKey $ApiKey `
            -Spec $spec `
            -Target $target
    } finally {
        Remove-Item -LiteralPath $tempPath -Force -ErrorAction SilentlyContinue
    }

    # The parent session stays unelevated after the msiexec UAC prompt, and
    # CLIUpdate's SDDL is SYSTEM + Administrators only, so this script cannot
    # start that task. The MSI registers a short delayed first trigger that
    # fires as SYSTEM once the install transaction has closed.

    Write-Output "$($spec.DisplayName) installed successfully."
}

if ($MyInvocation.InvocationName -ne ".") {
    try {
        Install-RunlayerPackage `
            -TenantHost $RunlayerHost `
            -ApiKey $OrgApiKey `
            -Package $Package
    } catch {
        Write-Error "Installation failed: $($_.Exception.Message)"
        exit 1
    }
}
