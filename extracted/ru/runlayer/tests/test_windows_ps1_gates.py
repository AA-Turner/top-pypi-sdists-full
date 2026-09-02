"""Static checks for shipped Windows .ps1 launcher scripts.

The SYSTEM scheduled-task script (``scheduled-task/register-tasks.ps1``) and the
standalone ``scripts/bootstrap.ps1`` must silent-exit on unconfigured fleets
where no MDM-pushed ``OrgApiKey`` registry value exists. Without this gate,
unconfigured / repaired devices emit churn (event log, EDR noise) every tick.
(Whether hooks / scans then run is decided downstream by the Enforcement /
Sessions keys; the per-user fan-out now lives in ``aiwatch scan --all-users``,
not a per-user scheduled task.)

Also pins the tamper-resistance SDDL. It is defined once, in the shared
RunlayerTaskCommon.ps1 foundation that register-tasks.ps1 dot-sources (so there
is nothing to drift): SYSTEM + Administrators get full control, Authenticated
Users get read+execute only (no write/delete for standard users).
"""

from __future__ import annotations

from pathlib import Path

import pytest

_PACKAGING_WINDOWS = Path(__file__).parent.parent / "packaging" / "windows"
_SCHEDULED_TASK = _PACKAGING_WINDOWS / "scheduled-task"
# The Intune Win32 custom detection script ships in its own folder (not the MSI),
# matching the layout of the built deployment package.
_CUSTOM_DETECTION = _PACKAGING_WINDOWS / "custom-detection"
_DETECT_INSTALL_PS1 = _CUSTOM_DETECTION / "detect-install.ps1"
_RELEASE_WORKFLOW = (
    Path(__file__).parents[2] / ".github" / "workflows" / "release-aiwatch.yml"
)

_GATED_PS1_FILES: tuple[Path, ...] = (
    _SCHEDULED_TASK / "register-tasks.ps1",
    _PACKAGING_WINDOWS / "scripts" / "bootstrap.ps1",
)

# SYSTEM + Builtin Administrators full control; Authenticated Users read+execute
# only. Defined once, in the shared foundation the runtime script dot-sources.
_EXPECTED_SDDL = "D:P(A;;GA;;;SY)(A;;GA;;;BA)(A;;GRGX;;;AU)"
_COMMON_PS1 = _SCHEDULED_TASK / "RunlayerTaskCommon.ps1"
_SDDL_PS1_FILES: tuple[Path, ...] = (_COMMON_PS1,)
# The runtime script must own no scheduled-task foundation of its own — it
# dot-sources the common module instead of re-inlining the SDDL.
_RUNTIME_PS1_FILES: tuple[Path, ...] = (_SCHEDULED_TASK / "register-tasks.ps1",)


@pytest.mark.parametrize(
    "ps1_path", _GATED_PS1_FILES, ids=lambda p: str(p.relative_to(_PACKAGING_WINDOWS))
)
def test_ps1_short_circuits_when_org_api_key_absent(ps1_path: Path) -> None:
    text = ps1_path.read_text()

    assert "HKLM:\\Software\\Runlayer\\AIWatch" in text
    assert '-Name "OrgApiKey"' in text
    assert "[string]::IsNullOrEmpty($OrgApiKey)" in text
    assert "exit 0" in text


@pytest.mark.parametrize(
    "ps1_path", _GATED_PS1_FILES, ids=lambda p: str(p.relative_to(_PACKAGING_WINDOWS))
)
def test_org_api_key_gate_precedes_identity_check(ps1_path: Path) -> None:
    """Gate must short-circuit before SYSTEM identity / refusal logic so that
    unconfigured fleets never produce identity-check stderr noise either."""
    text = ps1_path.read_text()

    gate_marker = "[string]::IsNullOrEmpty($OrgApiKey)"
    identity_marker = "WindowsIdentity]::GetCurrent()"

    gate_index = text.find(gate_marker)
    identity_index = text.find(identity_marker)
    assert gate_index != -1, "missing OrgApiKey gate"
    assert identity_index != -1, "missing identity check"
    assert gate_index < identity_index, (
        f"{ps1_path.name}: OrgApiKey gate must precede WindowsIdentity check"
    )


@pytest.mark.parametrize(
    "ps1_path", _SDDL_PS1_FILES, ids=lambda p: str(p.relative_to(_PACKAGING_WINDOWS))
)
def test_scheduled_task_sddl_is_locked_down(ps1_path: Path) -> None:
    """The tamper-resistance SDDL grants full control only to SYSTEM (SY) +
    Administrators (BA), and read+execute (GRGX) — never write/all — to
    Authenticated Users (AU). Denying SYSTEM would break the task entirely."""
    text = ps1_path.read_text()

    assert _EXPECTED_SDDL in text
    # Authenticated Users must never get full control (GA) or any write/delete.
    assert "(A;;GA;;;AU)" not in text
    assert "(A;;GWGX;;;AU)" not in text


def test_shared_scheduled_log_rotates_once_before_append() -> None:
    text = _COMMON_PS1.read_text()
    rotate_start = text.index("function Invoke-RunlayerLogRotation")
    write_start = text.index("function Write-RunlayerLog")
    rotate_block = text[rotate_start:write_start]
    write_end = text.index("function Get-RunlayerTaskSddl", write_start)
    write_block = text[write_start:write_end]

    assert "$script:RunlayerLogMaxBytes = 10MB" in text
    assert "$script:RunlayerLogRotationChecked = $false" in text
    assert "$script:RunlayerLogRotationChecked = $true" in rotate_block
    assert ".Length -gt $script:RunlayerLogMaxBytes" in rotate_block
    assert '".1"' in rotate_block
    assert "Move-Item -LiteralPath $script:LogFile" in rotate_block
    assert "-Force -ErrorAction Stop" in rotate_block
    assert "try {" in rotate_block
    assert "} catch {" in rotate_block
    assert write_block.index("Invoke-RunlayerLogRotation") < write_block.index(
        "Add-Content"
    )


@pytest.mark.parametrize(
    "ps1_path", _RUNTIME_PS1_FILES, ids=lambda p: str(p.relative_to(_PACKAGING_WINDOWS))
)
def test_no_terminating_write_error_before_exit(ps1_path: Path) -> None:
    """Under ``$ErrorActionPreference = 'Stop'`` a ``Write-Error`` promotes to a
    terminating error, so a following ``exit N`` never runs: the script collapses
    to exit 1 instead of the documented misconfig code (2). Guard / catch sites
    must emit a NON-terminating diagnostic (``Write-Warning`` /
    ``[Console]::Error.WriteLine``) so the explicit ``exit N`` actually takes
    effect. (A ``Write-Error`` carrying its own non-terminating ``-ErrorAction``
    is exempt — it would not throw under Stop.)"""
    text = ps1_path.read_text()
    assert '$ErrorActionPreference = "Stop"' in text, (
        f"{ps1_path.name}: this gate only matters when the script opts into Stop"
    )

    lines = text.splitlines()
    non_terminating = (
        "-ErrorAction Continue",
        "-ErrorAction SilentlyContinue",
        "-ErrorAction Ignore",
    )
    offenders: list[str] = []
    for idx, raw in enumerate(lines):
        if not raw.lstrip().startswith("Write-Error"):
            continue
        if any(opt in raw for opt in non_terminating):
            continue
        nxt = idx + 1
        while nxt < len(lines) and (
            not lines[nxt].strip() or lines[nxt].lstrip().startswith("#")
        ):
            nxt += 1
        if nxt < len(lines) and lines[nxt].lstrip().startswith("exit"):
            offenders.append(
                f"L{idx + 1}: {raw.strip()} -> L{nxt + 1}: {lines[nxt].strip()}"
            )
    assert not offenders, (
        f"{ps1_path.name}: terminating Write-Error directly precedes exit "
        f"(dead code under Stop, collapses to exit 1): {offenders}"
    )


@pytest.mark.parametrize(
    "ps1_path", _RUNTIME_PS1_FILES, ids=lambda p: str(p.relative_to(_PACKAGING_WINDOWS))
)
def test_runtime_scripts_dot_source_common_not_inline_sddl(ps1_path: Path) -> None:
    """The runtime scripts share one canonical foundation: they dot-source
    RunlayerTaskCommon.ps1 and must NOT re-inline the SDDL (shared ownership, so
    there is nothing to drift — replacing the prior byte-for-byte copy gate)."""
    text = ps1_path.read_text()

    assert "RunlayerTaskCommon.ps1" in text, (
        f"{ps1_path.name} must dot-source the shared RunlayerTaskCommon.ps1"
    )
    assert _EXPECTED_SDDL not in text, (
        f"{ps1_path.name} must not re-inline the SDDL; it lives in RunlayerTaskCommon.ps1"
    )


def test_register_kicks_scan_task_async_not_inline() -> None:
    """The install-time kick of the all-users scan task must be asynchronous.

    register-tasks.ps1 runs inside the MSI's deferred SYSTEM custom action. A
    synchronous inline ``& powershell.exe ...`` / ``& aiwatch.exe scan
    --all-users`` would block InstallFinalize for the whole profile-enumeration +
    per-profile scan fan-out, extending install time and risking MSI-timeout
    warnings in enterprise deployment tools (the task's 1h ExecutionTimeLimit
    does not bound an inline CA invocation). Kick the already-registered
    AIWatchScan task via Start-ScheduledTask instead (mirrors the AIWatchHooks
    kick): it returns immediately and the fan-out runs under Task Scheduler,
    bounded by the task's ExecutionTimeLimit.
    """
    text = (_SCHEDULED_TASK / "register-tasks.ps1").read_text()

    # No inline/synchronous subprocess in the deferred custom action.
    assert "& powershell.exe" not in text, (
        "register-tasks.ps1 must not synchronously invoke powershell inline in "
        "the deferred MSI custom action; kick the scan task asynchronously "
        "via Start-ScheduledTask instead"
    )

    # The scan task is still kicked once at install, just asynchronously.
    scan_kick = [
        line
        for line in text.splitlines()
        if "Start-ScheduledTask" in line and "$script:ScanTaskName" in line
    ]
    assert scan_kick, (
        "register-tasks.ps1 must kick the AIWatchScan task via "
        "Start-ScheduledTask so the all-users scan lands promptly"
    )


def test_register_cleans_up_legacy_scan_tasks() -> None:
    """On upgrade, register-tasks.ps1 must remove the legacy per-user fan-out
    tasks (AIWatchScanManager + AIWatchScan-<SID>) that the single AIWatchScan
    task supersedes — without matching the new AIWatchScan (no trailing dash)."""
    text = (_SCHEDULED_TASK / "register-tasks.ps1").read_text()

    assert "Unregister-ScheduledTask" in text
    assert '"AIWatchScanManager"' in text
    assert '"AIWatchScan-*"' in text


def test_detect_install_is_not_org_api_key_gated() -> None:
    """The Intune detection script must run regardless of MDM config (it decides
    installed/not-installed), and keys off aiwatch.exe + the AIWatchScan task so a
    wiped task folder triggers an Intune reinstall. It must NOT key off the
    removed AIWatchScanManager."""
    text = _DETECT_INSTALL_PS1.read_text()

    assert "[string]::IsNullOrEmpty($OrgApiKey)" not in text
    assert "AIWatchScan" in text
    assert "AIWatchScanManager" not in text
    assert "aiwatch.exe" in text


def test_published_detection_script_requires_valid_signature() -> None:
    """A publish run must fail before upload when the stamped script is unsigned.

    The workflow runs via workflow_dispatch or workflow_call (release-all.yml);
    both gate publishing on ``inputs.publish_release``, so the verify step must
    use the same gate as the ``release`` job."""
    text = _RELEASE_WORKFLOW.read_text()
    marker = "- name: Verify detect-install signature before release"
    start = text.index(marker)
    end = text.find("\n      - name:", start + len(marker))
    step = text[start : end if end != -1 else None]

    assert "if: inputs.publish_release" in step
    assert "Get-AuthenticodeSignature" in step
    assert "SignatureStatus]::Valid" in step
    assert "throw" in step

    # The publish job must share the exact gate, so verification covers every
    # path that uploads release assets.
    release_job = text[text.index("\n  release:") :]
    assert "if: inputs.publish_release" in release_job


def test_release_smoke_only_normalizes_quser_no_session_exit() -> None:
    """Only quser's known no-session message may turn exit 1 into a skip."""
    text = _RELEASE_WORKFLOW.read_text()
    quser_index = text.index("& quser.exe")
    capture_index = text.index("$quserExitCode = $LASTEXITCODE", quser_index)
    no_session_index = text.index("$noInteractiveSession =", capture_index)
    guard_index = text.index(
        "if ($quserExitCode -ne 0 -and -not $noInteractiveSession)",
        no_session_index,
    )
    throw_index = text.index("throw", guard_index)
    reset_index = text.index("$global:LASTEXITCODE = 0", quser_index)
    branch_index = text.index(
        "if ($interactiveSessions.Count -gt 0)",
        quser_index,
    )

    assert (
        quser_index
        < capture_index
        < no_session_index
        < guard_index
        < throw_index
        < reset_index
        < branch_index
    )
    assert "& quser.exe 2>&1" in text
    assert "No User exists for \\*" in text


def test_detect_install_logs_breadcrumb() -> None:
    """The detection script must side-log which branch decided not-installed (and
    the running identity) so an Intune execution-context failure is diagnosable
    on-device without re-deriving the logic."""
    text = _DETECT_INSTALL_PS1.read_text()

    assert "detect-install.log" in text
    assert "IsSystem" in text
    assert "Is64BitProcess" in text


def test_detect_install_suppresses_all_noisy_streams() -> None:
    """Intune's Win32 custom-detection contract treats ANY byte on STDERR as
    not-installed, even with a non-empty STDOUT + exit 0. PowerShell maps the
    Warning / Verbose / Progress / Debug / Information streams onto STDERR, so a
    stray record from any cmdlet in the detection path (e.g. Get-ScheduledTask
    auto-loading the ScheduledTasks module under a non-admin context) silently
    flips the app to not-installed. The script must (1) silence every non-error
    stream preference and (2) redirect all non-output streams of the detection
    call to $null so only the success marker can reach Intune. (ENG-3770.)"""
    text = _DETECT_INSTALL_PS1.read_text()

    for pref in (
        "$WarningPreference",
        "$ProgressPreference",
        "$VerbosePreference",
        "$DebugPreference",
        "$InformationPreference",
    ):
        assert f'{pref} = "SilentlyContinue"' in text, (
            f"detect-install.ps1 must set {pref} = SilentlyContinue so the "
            "stream never reaches STDERR"
        )

    assert "2>$null 3>$null 4>$null 5>$null 6>$null" in text, (
        "detect-install.ps1 must redirect every non-output stream of the "
        "detection call to $null so only the STDOUT success marker reaches Intune"
    )
