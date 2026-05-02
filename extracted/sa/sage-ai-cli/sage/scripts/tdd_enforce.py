#!/usr/bin/env python3
"""
TDD Enforcement Script for SAGE AI CLI.

NOTE: TDD is now automatically enforced during code writes via sage/core/tdd.py.
This script provides a CLI interface for manual TDD validation and configuration.

Usage:
    python -m sage.scripts.tdd_enforce [--check FILE] [--coverage THRESHOLD]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sage.core.tdd import configure_tdd, validate_code_write


def main() -> int:
    """Main entry point for manual TDD validation."""
    parser = argparse.ArgumentParser(
        description="TDD Enforcement for SAGE AI CLI (manual validation)"
    )
    parser.add_argument(
        "--check",
        type=str,
        metavar="FILE",
        help="Validate a specific file against TDD requirements",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=100.0,
        help="Coverage threshold percentage (default: 100)",
    )
    parser.add_argument(
        "--project-root",
        type=str,
        help="Project root directory",
    )
    parser.add_argument(
        "--lenient",
        action="store_true",
        help="Don't fail on missing test files",
    )

    args = parser.parse_args()

    # Configure TDD
    configure_tdd(
        enabled=True,
        coverage_threshold=args.threshold,
        strict=not args.lenient,
        project_root=Path(args.project_root) if args.project_root else None,
    )

    print("=" * 60)
    print("SAGE AI CLI - TDD Enforcement")
    print("=" * 60)

    if args.check:
        filepath = Path(args.check)
        if not filepath.exists():
            print(f"ERROR: File not found: {filepath}")
            return 1

        print(f"\nValidating: {filepath}")
        print(f"Coverage threshold: {args.threshold}%\n")

        content = filepath.read_text(encoding="utf-8", errors="replace")
        result = validate_code_write(filepath, content)

        print(result.summary())

        if result.output:
            print("\nTest output:")
            print("-" * 40)
            print(result.output)

        return 0 if result.passed else 1

    # Default: show info about automatic TDD enforcement
    print("\nTDD is automatically enforced during code writes.")
    print("Every Python file write triggers:")
    print("  1. Test file detection")
    print("  2. pytest execution with coverage")
    print("  3. 100% coverage validation")
    print("  4. Automatic rollback on failure")
    print("\nUse --check FILE to manually validate a file.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
