#!/usr/bin/env python3
"""Regex-engine contract for the CLI (ENG-4056).

Runtime code must use RE2 via `runlayer_cli.regex_safe`, never the
backtracking engines: stdlib `re` or the third-party `regex` package.
Backtracking regex is superlinear on adversarial (or merely unlucky) input,
and RE2 is linear-time by construction. Mirrors
`backend/scripts/check_regex_engine.py` (the canonical copy).

Pre-existing importers live in `cli/regex-engine-allowlist.txt`. The
allowlist is a ratchet: it may only shrink as migration PRs land. New
imports of `re`/`regex` fail this check; import `runlayer_cli.regex_safe`
instead. Entries that no longer match a real import also fail, so the file
stays honest — delete them.

Permanent exemptions (never migrated, never allowlisted):
- `runlayer_cli/regex_safe.py` — the wrapper itself.
- Golden-corpus parity tests under `tests/` marked with
  `# regex-engine: stdlib-parity` in their first 5 lines — they run OLD
  patterns under stdlib `re` as the frozen behavior spec for the RE2
  rewrites. The marker is honored under `tests/` only, so runtime code
  cannot self-exempt.

Usage:
    uv run python scripts/check_regex_engine.py
    uv run python scripts/check_regex_engine.py --update-allowlist  # shrink only
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent.parent
SCAN_ROOTS = (
    CLI_DIR / "runlayer_cli",
    CLI_DIR / "tests",
    CLI_DIR / "hooks",
    CLI_DIR / "scripts",
)
TESTS_DIR = CLI_DIR / "tests"
ALLOWLIST_PATH = CLI_DIR / "regex-engine-allowlist.txt"

BANNED_MODULES = {"re", "regex"}
EXEMPT_FILES = {CLI_DIR / "runlayer_cli" / "regex_safe.py"}
PARITY_MARKER = "# regex-engine: stdlib-parity"

ALLOWLIST_HEADER = """\
# Regex-engine allowlist (see scripts/check_regex_engine.py, ENG-4056).
#
# Each line is a file still importing a backtracking regex engine (stdlib
# `re` or the `regex` package), grandfathered in when the RE2 migration
# started. This file is a RATCHET: it may only shrink.
#
# - New imports are NOT added here. Use runlayer_cli.regex_safe instead.
# - When you migrate a file, delete its line (the check fails on stale lines).
#
# Format: <path relative to cli/> -> <banned module>
"""


def iter_source_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if root.is_file():
            files.append(root)
            continue
        files.extend(
            p for p in sorted(root.rglob("*.py")) if "__pycache__" not in p.parts
        )
    return files


def banned_imports(path: Path) -> list[tuple[str, int]]:
    """Return (banned module, line) for each `re`/`regex` import in the file."""
    # encoding="utf-8": Python sources are UTF-8 by definition, but read_text()
    # defaults to the locale encoding — on a cp1252 Windows box that raises on
    # the non-Latin-1 bytes several of our modules contain.
    source = path.read_text(encoding="utf-8")
    head = "\n".join(source.splitlines()[:5])
    # The marker exempts golden-corpus parity tests, which run OLD patterns
    # under stdlib `re` as the frozen behavior spec. Honor it under tests/
    # only — otherwise a runtime module could self-exempt its whole import
    # list by pasting one comment, silently defeating the ratchet.
    if PARITY_MARKER in head and path.is_relative_to(TESTS_DIR):
        return []
    tree = ast.parse(source, filename=str(path))
    hits: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in BANNED_MODULES:
                    hits.append((root, node.lineno))
        elif isinstance(node, ast.ImportFrom) and not node.level and node.module:
            root = node.module.split(".")[0]
            if root in BANNED_MODULES:
                hits.append((root, node.lineno))
    return hits


def collect_violations() -> dict[str, tuple[Path, int]]:
    """Map '<relpath> -> <module>' to the first (file, line) seen."""
    violations: dict[str, tuple[Path, int]] = {}
    for path in iter_source_files():
        if path in EXEMPT_FILES:
            continue
        for module, lineno in banned_imports(path):
            # as_posix(): the allowlist is checked in with forward slashes, so
            # a native-Windows run must not key on backslashes — every entry
            # would read as both new and stale at once.
            key = f"{path.relative_to(CLI_DIR).as_posix()} -> {module}"
            violations.setdefault(key, (path, lineno))
    return violations


def load_allowlist() -> set[str]:
    if not ALLOWLIST_PATH.exists():
        return set()
    stripped = (
        line.strip()
        for line in ALLOWLIST_PATH.read_text(encoding="utf-8").splitlines()
    )
    return {line for line in stripped if line and not line.startswith("#")}


def write_allowlist(keys: set[str]) -> None:
    ALLOWLIST_PATH.write_text(
        ALLOWLIST_HEADER + "\n" + "\n".join(sorted(keys)) + "\n", encoding="utf-8"
    )


def main() -> int:
    update = "--update-allowlist" in sys.argv[1:]
    violations = collect_violations()
    allowlist = load_allowlist()

    new = {k: v for k, v in violations.items() if k not in allowlist}
    stale = allowlist - violations.keys()

    if update:
        if not ALLOWLIST_PATH.exists():
            write_allowlist(set(violations))
            print(f"Allowlist bootstrapped: {len(violations)} entries.")
            return 0
        if new:
            print("Refusing to ADD entries; the allowlist only shrinks. New imports:")
            for key, (path, lineno) in sorted(new.items()):
                print(f"  {path.relative_to(CLI_DIR)}:{lineno}  {key}")
            return 1
        write_allowlist(set(violations))
        print(
            f"Allowlist rewritten: {len(violations)} entries ({len(stale)} stale removed)."
        )
        return 0

    ok = True
    if new:
        ok = False
        print(f"NEW backtracking-regex imports ({len(new)}):")
        for key, (path, lineno) in sorted(new.items()):
            print(f"  {path.relative_to(CLI_DIR)}:{lineno}  {key}")
        print("\nUse runlayer_cli.regex_safe (RE2); never extend the allowlist.")
    if stale:
        ok = False
        print(
            f"STALE allowlist entries ({len(stale)}) — already migrated; delete from {ALLOWLIST_PATH.name}:"
        )
        for key in sorted(stale):
            print(f"  {key}")
    if ok:
        print(f"Regex-engine contract OK ({len(violations)} files awaiting migration).")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
