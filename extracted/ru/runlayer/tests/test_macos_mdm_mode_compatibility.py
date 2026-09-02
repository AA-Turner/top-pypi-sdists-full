"""Static contracts for mixed-version macOS Mode compatibility guidance.

The shipped profile artifacts are bootstrap-only (Host + OrgApiKey) and no
longer carry Mode/Enforcement, but operators can still push those keys via MDM
for fleets pinned to AI Watch builds that predate the backend settings sync.
The packaging docs must keep stating the legacy pairing rule for that path.
"""

from __future__ import annotations

from pathlib import Path

_PACKAGING = Path(__file__).parent.parent / "packaging"
_PAIRING = (
    "Protect and Enforce require legacy Enforcement=true; Monitor requires legacy "
    "Enforcement=false."
)


def test_packaging_docs_state_legacy_mode_pairing() -> None:
    paths = (
        _PACKAGING / "README.md",
        _PACKAGING / "DEPLOYMENT.md",
    )

    for path in paths:
        assert _PAIRING in path.read_text(), f"{path.name} hides Mode compatibility"
