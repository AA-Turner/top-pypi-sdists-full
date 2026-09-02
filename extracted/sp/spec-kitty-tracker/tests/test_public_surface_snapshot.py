"""N19: contract drift detection via a committed public-surface snapshot.

TRK-M1-01 draft A1/N19: "__version__ ... remains the only public version
constant; contract drift is detected by the committed public-surface
snapshot fixture (sorted __all__, dataclass field names and defaults,
error MRO, capability flag names). No second version constant is added."
"__version__ must be bumped in the same commit that changes the fixture
(asserted by comparing fixture header to __version__)."

If this test fails because the live snapshot differs from the fixture,
that is contract drift: either the change was unintentional (revert it),
or it is an intentional additive change to the public surface, in which
case regenerate the fixture *and* bump __version__ in the same commit
(see the bottom of this file for the regeneration snippet).
"""

from __future__ import annotations

import json
from pathlib import Path

from public_surface_snapshot import compute_public_surface_snapshot

import spec_kitty_tracker as pkg

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "public_surface_snapshot.json"


def _load_fixture() -> dict[str, object]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as f:
        result: dict[str, object] = json.load(f)
        return result


def test_public_surface_snapshot_matches_committed_fixture() -> None:
    assert FIXTURE_PATH.is_file(), f"Missing committed fixture: {FIXTURE_PATH}"

    live = compute_public_surface_snapshot()
    fixture = _load_fixture()

    assert live == fixture, (
        "Public-surface snapshot drift detected (TRK-M1-01 draft N19). "
        "If this is an intentional additive change, regenerate "
        f"{FIXTURE_PATH} from compute_public_surface_snapshot() AND bump "
        "__version__ in the same commit (A1/A17)."
    )


def test_fixture_version_header_matches_runtime_version() -> None:
    """A1: '__version__ must be bumped in the same commit that changes the fixture'."""
    fixture = _load_fixture()
    assert fixture["version"] == pkg.__version__, (
        f"Fixture version header {fixture['version']!r} does not match runtime "
        f"__version__ {pkg.__version__!r}. Bump __version__ in the same commit "
        "that changes the public-surface snapshot fixture (A1)."
    )


# Regeneration snippet (run from the package root with the dev venv active):
#
#   .venv/bin/python -c "
#   import json, sys
#   sys.path.insert(0, 'tests')
#   from public_surface_snapshot import compute_public_surface_snapshot
#   json.dump(
#       compute_public_surface_snapshot(),
#       open('tests/fixtures/public_surface_snapshot.json', 'w'),
#       indent=2,
#       sort_keys=True,
#   )
#   open('tests/fixtures/public_surface_snapshot.json', 'a').write('\n')
#   "
