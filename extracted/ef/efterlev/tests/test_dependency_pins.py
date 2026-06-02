"""Source-level pins on load-bearing runtime dependency constraints.

These guard against silently loosening a cap that the test suite cannot
otherwise catch, because CI runs against the pinned `uv.lock` — a fresh
`pip`/`uv`/`pipx` install resolves *newer* versions than the lock, and a
parser-output regression there is invisible to the locked lane.

The canonical case: `python-hcl2` 6.x+ changed its parsed-block output
shape and silently breaks every detector's resource matching (a fresh
install on 8.1.2 scanned ~1 evidence record instead of ~20). See
DECISIONS 2026-06-01.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"


def _constraint(dep_name: str) -> str:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    for spec in data["project"]["dependencies"]:
        if spec.replace(" ", "").startswith(dep_name):
            return spec
    raise AssertionError(f"{dep_name} not found in [project.dependencies]")


def test_python_hcl2_is_capped_below_6() -> None:
    """python-hcl2 must stay capped below 6 until a full fresh-install scan
    (not just the locked lane) is re-validated against the newer line.

    A/B: revert the cap to `<9` and a fresh `pip install efterlev` scans
    ~1 evidence record instead of ~20 — the exact prod failure mode.
    """
    spec = _constraint("python-hcl2")
    m = re.search(r"<\s*(\d+)", spec)
    assert m is not None, f"python-hcl2 spec has no upper bound: {spec!r}"
    upper_major = int(m.group(1))
    assert upper_major <= 6, (
        f"python-hcl2 upper bound is {spec!r}; it MUST stay < 6 — 6.x+ changed the "
        "parser output and silently breaks detector matching on fresh installs. "
        "Re-validate a full fresh-deps scan before widening this cap."
    )
