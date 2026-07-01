"""Meta-test: verify spec_kitty_tracker source has no rollout/feature-flag patterns.

This is the test-side enforcement of FR-007 / C-001 from mission
006-hosted-discovery-contract-hardening: ``spec-kitty-tracker`` must remain
rollout-free. Rollout policy lives only in pinned downstream consumers
(``spec-kitty`` CLI, ``spec-kitty-saas``), never in the tracker package itself.

The post-merge mission review (RISK-2) flagged that this constraint was
verified by orchestrator-time grep but had no automated regression guard.
This test codifies the constraint as enforceable: if a future PR introduces
an env var read or feature-flag check in ``src/spec_kitty_tracker/``, the
test will fail and force the change to be either reverted or re-scoped to
a downstream consumer.

The patterns scanned for are deliberately narrow to avoid false positives:
``os.environ`` and ``os.getenv`` are the standard Python idioms for env-var
access, and a single pre-existing exception (the test-only ``BOUNDARY_*``
hint emitted by GlooCache instrumentation in some local environments) is
not part of the package source.
"""

from __future__ import annotations

import re
from pathlib import Path

# Patterns that indicate a rollout / feature-flag / env-var dependency in
# tracker source code. Each entry is a (compiled regex, human description) pair.
#
# Narrow patterns only — these must produce zero hits in src/spec_kitty_tracker/
# under FR-007 / C-001. Broader patterns (e.g. matching the bare word
# "rollout") are intentionally excluded because they false-positive on
# documentation, comments, and unrelated identifiers.
FORBIDDEN_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bos\.environ\b"), "os.environ access"),
    (re.compile(r"\bos\.getenv\b"), "os.getenv() call"),
    (re.compile(r"\bfrom os import\b[^\n]*\b(environ|getenv)\b"), "from os import environ/getenv"),
    (re.compile(r"\benviron\.get\("), "environ.get() call"),
]

TRACKER_SRC = Path(__file__).parent.parent / "src" / "spec_kitty_tracker"


def _is_comment_or_docstring_line(line: str) -> bool:
    """Best-effort detection of pure comment / docstring delimiter lines.

    A line that begins (after leading whitespace) with ``#`` is a comment.
    A line whose only non-whitespace content is ``\"\"\"`` or ``'''`` is a
    docstring delimiter. Both are skipped because they may legitimately
    mention env-var patterns in explanatory text without invoking the
    behavior.

    This is intentionally a heuristic, not a full Python parser. The patterns
    we scan for are uncommon enough that the heuristic is sufficient. If a
    future false positive bites, switch to AST-based scanning at that time.
    """
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("#"):
        return True
    if stripped in ('"""', "'''"):
        return True
    return False


def test_tracker_source_has_no_rollout_patterns() -> None:
    """``src/spec_kitty_tracker/`` must contain zero env-var / feature-flag patterns.

    Enforces FR-007 / C-001 from mission 006-hosted-discovery-contract-hardening:
    tracker stays rollout-free. Rollout policy belongs in pinned downstream
    consumers, not in the tracker package.
    """
    assert TRACKER_SRC.is_dir(), (
        f"Expected tracker source at {TRACKER_SRC} but the directory does not exist. "
        f"Has the package layout changed?"
    )

    violations: list[str] = []
    py_files = sorted(TRACKER_SRC.rglob("*.py"))
    assert py_files, f"No .py files found under {TRACKER_SRC} — package layout is broken"

    for py_file in py_files:
        content = py_file.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.splitlines(), start=1):
            if _is_comment_or_docstring_line(line):
                continue
            for pattern, description in FORBIDDEN_PATTERNS:
                if pattern.search(line):
                    rel = py_file.relative_to(TRACKER_SRC.parent.parent)
                    violations.append(
                        f"  {rel}:{line_num}: {description}: {line.strip()}"
                    )

    assert not violations, (
        "Forbidden rollout / feature-flag patterns found in tracker source:\n"
        + "\n".join(violations)
        + "\n\nFR-007 / C-001 from mission 006-hosted-discovery-contract-hardening "
        "requires spec-kitty-tracker to remain rollout-free. Env vars, feature "
        "flags, and rollout gates belong in pinned downstream consumers "
        "(spec-kitty CLI, spec-kitty-saas), not in the tracker package itself.\n"
        "\n"
        "If this is intentional, the constraint must be re-negotiated in a new "
        "mission spec — do not silence this test."
    )
