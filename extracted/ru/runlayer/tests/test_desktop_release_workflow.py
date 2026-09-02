import xml.etree.ElementTree as ET
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[2]
_DESKTOP_WORKFLOW = (
    _REPO_ROOT / ".github" / "workflows" / "release-runlayer-desktop.yml"
)
_CLI_RELEASE_WORKFLOW = (
    _REPO_ROOT / ".github" / "workflows" / "release-runlayer-cli.yml"
)
_CLI_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "cli.yml"
_MSI_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "test-windows-msi.yml"
_MACOS = _REPO_ROOT / "desktop" / "macos"
_MACOS_APP_DELEGATE = _MACOS / "Sources" / "RunlayerDesktop" / "AppDelegate.swift"
_WINDOWS = _REPO_ROOT / "desktop" / "windows"


def _workflow_step(workflow: str, name: str) -> str:
    marker = f"- name: {name}"
    start = workflow.index(marker)
    end = workflow.find("\n      - name:", start + len(marker))
    return workflow[start : end if end != -1 else None]


def test_release_builds_native_trays_before_signing_and_installers() -> None:
    workflow = _DESKTOP_WORKFLOW.read_text()

    assert workflow.index("Test macOS tray app") < workflow.index(
        "Build macOS tray app"
    )
    assert workflow.index("Build macOS tray app") < workflow.index("Build desktop .pkg")
    assert "actions/setup-dotnet@v5" in workflow
    assert workflow.index("Build Windows tray app") < workflow.index("Sign exes + dlls")
    assert workflow.index("Sign exes + dlls") < workflow.index("Build desktop .msi")
    assert "uses: ./.github/actions/sign-windows-payload" in workflow
    assert "files-folder: cli\\dist\\runlayer" in workflow
    assert 'INCLUDE_DESKTOP: "1"' in workflow
    assert "build_msi_runlayer.ps1 -IncludeDesktop" in workflow
    assert 'tag_name: "desktop-${{ steps.version.outputs.version }}"' in workflow
    assert "package: desktop" in workflow


def test_published_release_requires_complete_signing_configuration() -> None:
    workflow = _DESKTOP_WORKFLOW.read_text()
    cases = {
        "Require macOS release signing": (
            "APPLE_CERT_P12",
            "APPLE_CERT_PASSWORD",
            "APPLE_IDENTITY_APP",
            "APPLE_IDENTITY_INSTALLER",
            "APPLE_ID",
            "APPLE_TEAM_ID",
            "APPLE_NOTARY_PASSWORD",
        ),
        "Require Windows release signing": (
            "AZURE_CLIENT_ID",
            "AZURE_TENANT_ID",
            "AZURE_SUBSCRIPTION_ID",
            "AZURE_TRUSTED_SIGNING_ENDPOINT",
            "AZURE_TRUSTED_SIGNING_ACCOUNT",
            "AZURE_TRUSTED_SIGNING_PROFILE",
        ),
    }

    for step_name, required_secrets in cases.items():
        step = _workflow_step(workflow, step_name)
        assert "if: inputs.publish_release" in step
        for secret in required_secrets:
            assert f"{secret}: ${{{{ secrets.{secret} }}}}" in step
            assert secret in step.split("run:", 1)[1]


def test_cli_release_has_no_desktop_build_dependency() -> None:
    workflow = _CLI_RELEASE_WORKFLOW.read_text()

    for desktop_step in (
        "Test macOS tray app",
        "Build macOS tray app",
        "Build Windows tray app",
        "RunlayerTray.exe",
        "INCLUDE_DESKTOP",
        "-IncludeDesktop",
    ):
        assert desktop_step not in workflow
    assert "package: cli" in workflow


def test_pr_workflows_build_desktop_sources_and_windows_msi() -> None:
    cli_workflow = _CLI_WORKFLOW.read_text()
    msi_workflow = _MSI_WORKFLOW.read_text()

    assert cli_workflow.count("- 'desktop/**'") == 2
    assert msi_workflow.count("- 'desktop/windows/**'") == 2
    assert msi_workflow.count("- 'cli/packaging/windows/cli-update-task/**'") == 2
    assert "actions/setup-dotnet@v5" in msi_workflow
    assert msi_workflow.index("Build Runlayer CLI MSI") < msi_workflow.index(
        "Build Runlayer tray"
    )
    assert msi_workflow.index("Build Runlayer tray") < msi_workflow.index(
        "Build Runlayer desktop MSI"
    )
    assert "build_msi_runlayer.ps1 -IncludeDesktop" in msi_workflow
    assert r"desktop\windows\build.ps1" in msi_workflow


def test_macos_tray_rebuilds_menu_after_action_success_or_failure() -> None:
    source = _MACOS_APP_DELEGATE.read_text()
    # Login prompt also clears statusError on success so discovery failures
    # don't stale the menu after Sign In.
    cases = (
        (
            "private func dispatch(_ action: String)",
            "private func promptForHostAndLogin()",
            [
                "lastError = nil",
                "} catch {",
                "lastError = error.localizedDescription",
                "}",
                "rebuildMenu()",
            ],
        ),
        (
            "private func promptForHostAndLogin()",
            "@objc private func sync()",
            [
                "lastError = nil",
                "statusError = nil",
                "} catch {",
                "lastError = error.localizedDescription",
                "}",
                "rebuildMenu()",
            ],
        ),
        (
            "@objc private func checkForUpdates()",
            "@objc private func quit()",
            [
                "lastError = nil",
                "} catch {",
                "lastError = error.localizedDescription",
                "}",
                "rebuildMenu()",
            ],
        ),
    )

    for start_marker, end_marker, completion in cases:
        start = source.index(start_marker)
        method = source[start : source.index(end_marker, start)]
        lines = [line.strip() for line in method.splitlines()]
        assert any(
            lines[index : index + len(completion)] == completion
            for index in range(len(lines))
        )


def test_windows_tray_uses_same_user_ipc_and_argument_lists() -> None:
    single_instance = (_WINDOWS / "SingleInstance.cs").read_text()
    cli = (_WINDOWS / "RunlayerCli.cs").read_text()
    protocol = (_WINDOWS / "RunlayerProtocolUrl.cs").read_text()

    assert "PipeOptions.CurrentUserOnly" in single_instance
    assert r"Local\{instanceName}" in single_instance
    assert "WindowsIdentity.GetCurrent().User" in single_instance
    assert "startInfo.ArgumentList.Add(argument)" in cli
    assert "UseShellExecute = false" in cli
    for action in ("login", "sync", "dashboard"):
        assert f'"runlayer://{action}"' in protocol


def test_windows_tray_listens_during_slow_context_initialization() -> None:
    program = (_WINDOWS / "Program.cs").read_text()
    listener_start = program.index("singleInstance.StartListening")
    context_start = program.index("new(new RunlayerCli())")

    assert listener_start < context_start
    listener_registration = program[listener_start:context_start]
    assert "lock (protocolUrlGate)" in listener_registration
    assert "pendingProtocolUrls.Enqueue(rawUrl)" in listener_registration
    assert "context.HandleProtocolUrl(rawUrl)" in listener_registration

    context_initialization = program[
        context_start : program.index("Application.Run", context_start)
    ]
    assert "lock (protocolUrlGate)" in context_initialization
    assert "context = readyContext;" in context_initialization
    assert "pendingProtocolUrls.TryDequeue" in context_initialization
    assert (
        "readyContext.HandleProtocolUrl(pendingProtocolUrl)" in context_initialization
    )


def test_windows_tray_login_resolves_host_instead_of_failing_silently() -> None:
    """`runlayer login` in a detached process cannot prompt or report a missing
    host, so the tray owns that decision for the menu item and the protocol URL.
    """
    tray = (_WINDOWS / "TrayApplicationContext.cs").read_text()
    cli = (_WINDOWS / "RunlayerCli.cs").read_text()
    prompt = (_WINDOWS / "HostPrompt.cs").read_text()

    assert '"Log In", (_, _) => StartLogin()' in tray
    assert "RunlayerProtocolAction.Login" in tray
    assert "StartLoginAfterStatusAsync" in tray
    assert "HostPrompt.Show()" in tray
    # The prompted value becomes a `--host` argument, so it must be normalized
    # by the same gate as the macOS tray before it reaches the CLI.
    assert "RunlayerHostUrl.Normalize" in prompt
    assert "RunlayerHostUrl.Normalize(host) != host" in cli
    assert 'StartDetached(["login", "--host", host])' in cli


def test_desktop_tray_serializes_login_flow() -> None:
    macos = _MACOS_APP_DELEGATE.read_text()
    windows = (_WINDOWS / "TrayApplicationContext.cs").read_text()

    assert "private var isLoggingIn = false" in macos
    assert "guard !isLoggingIn else" in macos
    assert "isLoggingIn = true" in macos
    assert macos.count("isLoggingIn = false") >= 2

    assert "private int _loginInFlight;" in windows
    assert "Interlocked.Exchange(ref _loginInFlight, 1)" in windows
    assert windows.count("Interlocked.Exchange(ref _loginInFlight, 0)") >= 2


def test_desktop_tray_handles_pending_approval_notifications() -> None:
    macos = _MACOS_APP_DELEGATE.read_text()
    macos_cli = (_MACOS / "Sources/RunlayerDesktop" / "RunlayerCLI.swift").read_text()
    macos_status = (
        _MACOS / "Sources/RunlayerDesktopCore/StatusSnapshot.swift"
    ).read_text()
    macos_links = (
        _MACOS / "Sources/RunlayerDesktopCore/DashboardDeepLink.swift"
    ).read_text()
    package = (_MACOS / "Package.swift").read_text()
    windows = (_WINDOWS / "TrayApplicationContext.cs").read_text()
    windows_status = (_WINDOWS / "StatusSnapshot.cs").read_text()
    windows_links = (_WINDOWS / "DashboardDeepLink.cs").read_text()

    assert "UserNotifications" in package
    assert "UNUserNotificationCenterDelegate" in macos
    assert "runlayer.approval.approve" in macos
    assert "runlayer.approval.prevent" in macos
    assert "canDecideInline" in macos
    assert "approvalLedger.absorb" in macos
    assert "Review approval request" in macos
    assert "DashboardDeepLink.approvalRequest" in macos
    assert "submit_approval" not in macos.lower()
    assert '"__decide-approval"' in macos_cli
    assert 'approve ? "--approve" : "--prevent"' in macos_cli
    assert "approvalRequestsPending" in macos_status
    assert "approvalRequests" in macos_status
    assert "canDecideInline" in macos_status
    assert 'path: "approvals/\\(canonical)"' in macos_links

    assert "ShowBalloonTip" in windows
    assert "_notifiedApprovalRequestIds.Add(request.Id)" in windows
    assert "BalloonTipClicked" in windows
    assert "Review approval request" in windows
    assert "DashboardDeepLink.ApprovalRequest" in windows
    assert "submit_approval" not in windows.lower()
    assert "ApprovalRequestsPending" in windows_status
    assert "ApprovalRequests" in windows_status
    assert "CanDecideInline" in windows_status
    assert '$"approvals/{parsed:D}"' in windows_links


def test_desktop_tray_notification_decisions_are_macos_only_for_now() -> None:
    """Windows balloons cannot carry actions, so nothing there may decide.

    Real Windows buttons need WinRT toast activation plus a shortcut carrying
    an AppUserModelID. Until that lands the Windows tray must not ship a
    decision codepath at all — an unreachable one reads like the feature works.
    """
    windows_cli = (_WINDOWS / "RunlayerCli.cs").read_text()
    windows = (_WINDOWS / "TrayApplicationContext.cs").read_text()

    assert "__decide-approval" not in windows_cli
    assert "LaunchApprovalDecision" not in windows
    assert "--approve" not in windows_cli


def test_desktop_tray_error_balloons_do_not_open_approvals() -> None:
    """One NotifyIcon shares a click handler across every balloon it raises."""
    windows = (_WINDOWS / "TrayApplicationContext.cs").read_text()

    assert "BalloonKind" in windows
    assert "_balloonKind = BalloonKind.Error;" in windows
    assert "_balloonKind = BalloonKind.PendingApprovals;" in windows
    assert "if (_balloonKind != BalloonKind.PendingApprovals)" in windows


def test_macos_tray_never_absorbs_approvals_it_cannot_yet_notify_about() -> None:
    """Absorbing marks an id notified forever; authorization resolves async.

    If the first status poll wins the race against the permission prompt, an
    absorb-then-check order silently swallows the first approval for good.
    """
    macos = _MACOS_APP_DELEGATE.read_text()
    start = macos.index("private func notifyForPendingApprovals")
    body = macos[start : macos.index("\n    private func", start + 10)]

    # Absorbing happens only inside the authorized branch, in a separate method.
    assert "approvalLedger.absorb" not in body
    assert "getNotificationSettings" in body
    assert "deliverApprovalNotification" in body
    deliver = macos.index("private func deliverApprovalNotification")
    assert (
        "approvalLedger.absorb"
        in macos[deliver : macos.index("\n    private func", deliver + 10)]
    )
    # Read live settings per poll: a cached false would mute the tray for good
    # once someone enables notifications in System Settings.
    assert "notificationsAuthorized" not in macos
    # Granting has to re-poll, or the waiting approval sits out the interval.
    grant = macos.index("requestAuthorization")
    authorization = macos[grant : macos.index("\n    private func", grant)]
    assert "self.refreshStatus()" in authorization


def test_desktop_notifications_name_the_action_they_offer_to_approve() -> None:
    """A one-click Approve on an unlabelled request is theatre.

    The backend withholds the argument preview from api-key callers, so the
    `Approval needed: Server -> tool` title is the only exact-action context
    the tray gets — and macOS drops the action buttons without it.
    """
    macos = _MACOS_APP_DELEGATE.read_text()
    macos_status = (
        _MACOS / "Sources/RunlayerDesktopCore/StatusSnapshot.swift"
    ).read_text()
    windows = (_WINDOWS / "TrayApplicationContext.cs").read_text()
    windows_status = (_WINDOWS / "StatusSnapshot.cs").read_text()

    assert "case title" in macos_status
    assert "content.title = approvalTitle" in macos
    assert "single?.title.isEmpty == false" in macos
    assert '[JsonPropertyName("title")]' in windows_status
    assert "_notifyIcon.BalloonTipTitle = approvalTitle;" in windows


def test_desktop_tray_prunes_decided_approval_notification_ids() -> None:
    """A tray runs for weeks; the notified-id set must not grow forever."""
    macos_ledger = (
        _MACOS / "Sources/RunlayerDesktopCore/ApprovalNotificationLedger.swift"
    ).read_text()
    windows = (_WINDOWS / "TrayApplicationContext.cs").read_text()

    assert "notifiedIds.formIntersection(liveIds)" in macos_ledger
    assert "_notifiedApprovalRequestIds.IntersectWith(" in windows


def test_windows_tray_allows_http_only_for_exact_loopback_hosts() -> None:
    host_url = (_WINDOWS / "RunlayerHostUrl.cs").read_text()

    assert "uri.Scheme == Uri.UriSchemeHttps" in host_url
    assert "uri.Scheme == Uri.UriSchemeHttp && IsHttpLoopbackHost(uri.Host)" in host_url
    for host in ('"localhost"', '"127.0.0.1"', '"::1"', '"[::1]"'):
        assert host in host_url


def test_windows_tray_publish_is_self_contained_and_not_unsafely_trimmed() -> None:
    project = ET.fromstring((_WINDOWS / "RunlayerTray.csproj").read_text())
    properties = {
        child.tag: child.text
        for group in project.findall("PropertyGroup")
        for child in group
    }

    assert properties["TargetFramework"].startswith("net8.0-windows")
    assert properties["UseWindowsForms"] == "true"
    assert properties["SelfContained"] == "true"
    assert properties["PublishTrimmed"] == "false"
