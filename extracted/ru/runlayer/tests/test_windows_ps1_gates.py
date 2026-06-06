"""Static checks for shipped Windows .ps1 launcher scripts.

All three ps1 invocation paths (Intune Remediations `assert/{detect,remediate}`
+ standalone `scripts/bootstrap`) must silent-exit on scan-only fleets where
no MDM-pushed `EnrollmentKey` registry value exists. Without this gate,
scan-only deployments emit churn in the Intune dashboard / event log every
remediation cycle.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_PACKAGING_WINDOWS = Path(__file__).parent.parent / "packaging" / "windows"

_GATED_PS1_FILES: tuple[Path, ...] = (
    _PACKAGING_WINDOWS / "assert" / "detect.ps1",
    _PACKAGING_WINDOWS / "assert" / "remediate.ps1",
    _PACKAGING_WINDOWS / "scripts" / "bootstrap.ps1",
)


@pytest.mark.parametrize(
    "ps1_path", _GATED_PS1_FILES, ids=lambda p: str(p.relative_to(_PACKAGING_WINDOWS))
)
def test_ps1_short_circuits_when_enrollment_key_absent(ps1_path: Path) -> None:
    text = ps1_path.read_text()

    assert "HKLM:\\Software\\Runlayer\\AIWatch" in text
    assert '-Name "EnrollmentKey"' in text
    assert "[string]::IsNullOrEmpty($EnrollmentKey)" in text
    assert "exit 0" in text


@pytest.mark.parametrize(
    "ps1_path", _GATED_PS1_FILES, ids=lambda p: str(p.relative_to(_PACKAGING_WINDOWS))
)
def test_enrollment_key_gate_precedes_identity_check(ps1_path: Path) -> None:
    """Gate must short-circuit before SYSTEM identity / refusal logic so that
    scan-only fleets never produce identity-check stderr noise either."""
    text = ps1_path.read_text()

    gate_marker = "[string]::IsNullOrEmpty($EnrollmentKey)"
    identity_marker = "WindowsIdentity]::GetCurrent()"

    gate_index = text.find(gate_marker)
    identity_index = text.find(identity_marker)
    assert gate_index != -1, "missing EnrollmentKey gate"
    assert identity_index != -1, "missing identity check"
    assert gate_index < identity_index, (
        f"{ps1_path.name}: EnrollmentKey gate must precede WindowsIdentity check"
    )
