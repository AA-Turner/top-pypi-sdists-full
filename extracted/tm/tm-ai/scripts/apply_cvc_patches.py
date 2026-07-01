#!/usr/bin/env python3
"""
Apply CVC's runtime override patches to the freshly-synced vendor tree.

This is the second half of the vendor-sync mechanism:
  1. scripts/sync_vendor.sh  — copy ref → vendor (wholesale)
  2. scripts/apply_cvc_patches.py — inject CVC's additive overrides (this)

The patches live in scripts/patches/ and are intentionally surgical —
each one is a small, well-anchored text transform that adds CVC-specific
behavior without wholesale replacing the ref's file. That way, when
the ref renames, removes, or adds functions in a file we override, the
rest of the file still works correctly.

Run order:
  ./scripts/sync_vendor.sh && ./scripts/apply_cvc_patches.py

Verification:
  After running, the smoke tests at the bottom of sync_vendor.sh will
  confirm both patches landed. Re-running is safe — every patch is
  idempotent.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PATCHES_DIR = SCRIPT_DIR / "patches"
VENDOR_DIR = (SCRIPT_DIR.parent / "cvc" / "agent" / "_vendor" / "hermes").resolve()

# Patch registry: (vendor_relative_path, patches_module_name, description)
PATCHES = [
    (
        "hermes_cli/platforms.py",
        "cvc_dashboard_platform",
        "Register cvc-dashboard platform so runtime recognizes CVC dashboard",
    ),
    (
        "agent/skill_utils.py",
        "cvc_bundled_skills",
        "Inject bundled_skills tree lookup into get_external_skills_dirs()",
    ),
]


def apply_all(dry_run: bool = False) -> int:
    """Apply every patch in the registry. Return the number of files patched."""
    if not VENDOR_DIR.exists():
        print(f"ERROR: vendor dir not found: {VENDOR_DIR}", file=sys.stderr)
        return -1

    sys.path.insert(0, str(PATCHES_DIR))

    applied = 0
    for rel_path, module_name, description in PATCHES:
        target = VENDOR_DIR / rel_path
        if not target.exists():
            print(f"  ✗ MISSING: {rel_path}  (skipping {module_name})")
            continue

        before = target.read_text()
        try:
            patch = importlib.import_module(module_name)
            after = patch.apply(before)
        except Exception as e:
            print(f"  ✗ FAILED: {module_name} → {rel_path}: {e}")
            return -1

        if after == before:
            print(f"  = unchanged: {rel_path}  ({module_name})")
            continue

        delta = len(after) - len(before)
        if dry_run:
            print(f"  + would patch: {rel_path}  (+{delta} bytes)  [{module_name}]")
            print(f"      {description}")
        else:
            target.write_text(after)
            print(f"  ✓ patched: {rel_path}  (+{delta} bytes)  [{module_name}]")
            print(f"      {description}")
            applied += 1

    return applied


def main():
    dry_run = "--dry-run" in sys.argv
    print(f"Applying CVC override patches to {VENDOR_DIR}")
    if dry_run:
        print("(dry run — no writes)")
    print()
    n = apply_all(dry_run=dry_run)
    if n < 0:
        sys.exit(1)
    print()
    if dry_run:
        print(f"Would patch {n} files. Re-run without --dry-run to apply.")
    else:
        print(f"Patched {n} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
