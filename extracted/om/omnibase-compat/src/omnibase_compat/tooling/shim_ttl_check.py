# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""CI rule: flag shim files whose TTL has expired.

Scans Python source files for lines matching:
    # sunset: omnibase_core >= <ver> (<YYYY-MM-DD>)

Exits non-zero if today's date >= the sunset date on any shim.

Usage:
    python -m omnibase_compat.tooling.shim_ttl_check src/
"""

from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path

_SUNSET_PATTERN = re.compile(r"#\s*sunset:\s*\S+\s*>=\s*\S+\s*\((\d{4}-\d{2}-\d{2})\)")


def _check_file(path: Path, today: date) -> list[str]:
    violations: list[str] = []
    for lineno, line in enumerate(path.read_text().splitlines(), start=1):
        m = _SUNSET_PATTERN.search(line)
        if m:
            sunset = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            if today >= sunset:
                violations.append(
                    f"{path}:{lineno}: shim TTL expired ({m.group(1)}) — delete or extend"
                )
    return violations


def main(roots: list[str]) -> int:
    today = date.today()
    all_violations: list[str] = []
    for root in roots:
        for path in Path(root).rglob("*.py"):
            all_violations.extend(_check_file(path, today))

    if all_violations:
        for v in all_violations:
            print(f"ERROR: {v}", file=sys.stderr)
        return 1

    print(f"shim-ttl-check: no expired shims (checked as of {today})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["src"]))
