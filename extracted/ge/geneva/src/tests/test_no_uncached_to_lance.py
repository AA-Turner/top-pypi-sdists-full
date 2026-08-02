# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Regression guard for un-cached ``Table.to_lance()`` callsites (GEN-574).

``Table.to_lance()`` opens a fresh ``LanceDataset`` (re-reading the manifest)
on every call. On a many-fragment backfill that turns into thousands of
redundant manifest reads — the GEN-571/GEN-574 slowdown. Read paths must go
through ``open_read_dataset`` (the process-global read cache in
``geneva.query``).

This test fails if a new direct ``.to_lance()`` callsite appears under
``src/geneva`` that neither routes through ``open_read_dataset`` nor carries an
explicit opt-out marker ``# to_lance: fresh — <reason>`` (for mutation-adjacent
paths that genuinely need a live manifest). The marker may sit on the call line
or the line directly above it.
"""

import pathlib

_GENEVA_SRC = pathlib.Path(__file__).resolve().parents[1] / "geneva"
_MARKER = "to_lance: fresh"


def _code_part(line: str) -> str:
    """Return the line with any trailing comment stripped.

    A ``.to_lance(`` that only appears inside a comment (e.g. prose or the
    opt-out marker itself) must not count as a callsite.
    """
    return line.split("#", 1)[0]


def test_no_uncached_to_lance_callsites() -> None:
    violations: list[str] = []
    for path in sorted(_GENEVA_SRC.rglob("*.py")):
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            if ".to_lance(" not in _code_part(line):
                continue
            prev = lines[i - 1] if i > 0 else ""
            if _MARKER in line or _MARKER in prev:
                continue
            rel = path.relative_to(_GENEVA_SRC.parent)
            violations.append(f"{rel}:{i + 1}: {line.strip()}")

    assert not violations, (
        "Direct Table.to_lance() callsite(s) must route through "
        "open_read_dataset (geneva.query) for read paths, or carry an opt-out "
        "comment '# to_lance: fresh — <reason>' for mutation-adjacent paths "
        "that need a live manifest:\n  " + "\n  ".join(violations)
    )
