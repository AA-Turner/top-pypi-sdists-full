#!/usr/bin/env python
"""Check setup-expectations drift between source files and docs.

Thin CLI wrapper around the package drift-check helpers. Exit codes:
  0 — no drift detected (pass)
  1 — drift detected (details printed to stdout) or precondition failure
      (details printed to stderr)
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make package imports robust when invoked outside repo root.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Force UTF-8 stdout/stderr so emoji survive on Windows cp1252 terminals.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


def main() -> int:
    """Run the setup-expectations drift check."""
    from agentic_devtools.cli.checks.setup_drift import (
        _is_setup_doc,
        _is_setup_source,
        check_drift,
        ensure_placeholder_docs,
    )
    from agentic_devtools.cli.checks.setup_drift_changed_files import _build_drift_file_list

    _all_files, deleted_paths = _build_drift_file_list(_REPO_ROOT)
    files = sorted(f for f in _all_files if _is_setup_source(f) or _is_setup_doc(f))

    if not files:
        print("✅ Setup drift check skipped: no setup-relevant files changed.")
        return 0

    # FR-008 precondition: ensure placeholder docs exist
    docs_dir = _REPO_ROOT / "docs" / "setup-expectations"
    try:
        ensure_placeholder_docs(docs_dir, deleted_paths=deleted_paths)
    except (ValueError, OSError) as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1

    result = check_drift(files)
    if result.passed:
        print(f"✅ {result.message}")
        return 0

    print(f"❌ {result.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
