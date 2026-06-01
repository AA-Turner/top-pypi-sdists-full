"""Lock `scripts/triage.sh`'s `EXPECTED_DETECTORS` constant against the
actual detector registry so the v0.1.28 → v0.1.29 drift can't recur.

v0.1.28 added `aws.cna_optimizing_for_availability` (registry: 45 → 46)
but missed bumping `EXPECTED_DETECTORS=45` in `scripts/triage.sh`. The
auto-triage's T3 check ran against the published v0.1.28 wheel,
compared the wheel's actual count (46) to the hardcoded expected (45),
and reported FAIL on the v0.1.28 release page.

This test is the structural fix: scan `scripts/triage.sh` for the
`EXPECTED_DETECTORS=N` line, parse N, and assert it equals the live
registry count. Future detector PRs that forget to bump the constant
fail this test at PR review — no Windows runner needed, no release
needed, just `pytest`.
"""

from __future__ import annotations

import re
from pathlib import Path

# Import the detector library so the registry is populated.
import efterlev.detectors  # noqa: F401
from efterlev.detectors.base import get_registry

TRIAGE_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "triage.sh"
EXPECTED_LINE_RE = re.compile(r"^EXPECTED_DETECTORS=(\d+)", re.MULTILINE)


def test_triage_expected_detectors_matches_registry() -> None:
    """`scripts/triage.sh`'s `EXPECTED_DETECTORS` must equal the live
    registry count. A failed assertion here means a detector add/remove
    skipped updating triage.sh — fix the script before merging or T3
    on the next release will FAIL on the GH Release page."""
    src = TRIAGE_SCRIPT.read_text(encoding="utf-8")
    matches = EXPECTED_LINE_RE.findall(src)
    assert len(matches) == 1, (
        f"expected exactly one `EXPECTED_DETECTORS=N` line in "
        f"{TRIAGE_SCRIPT}; found {len(matches)}: {matches!r}"
    )
    expected = int(matches[0])
    actual = len(get_registry())
    assert expected == actual, (
        f"scripts/triage.sh hardcodes EXPECTED_DETECTORS={expected} "
        f"but the live registry contains {actual} detectors. Bump the "
        f"constant when adding/removing a detector — auto-triage T3 "
        f"will FAIL on the next release page if these drift apart."
    )
