"""CLI handlers for local diagnostics exports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from ..services.diagnostics_bundle import BundleOptions, create_diagnostics_bundle, parse_since


def _run_diagnostics(config: Any, args: argparse.Namespace) -> None:
    action = getattr(args, "diagnostics_action", None)
    if action != "bundle":
        print("Usage: aroom diagnostics bundle [options]", file=sys.stderr)
        sys.exit(1)

    try:
        since = parse_since(getattr(args, "since", None))
    except ValueError as exc:
        print(f"Invalid --since: {exc}", file=sys.stderr)
        sys.exit(1)

    output_raw = getattr(args, "output", None)
    options = BundleOptions(
        conversation_id=getattr(args, "conversation_id", None),
        turn_id=getattr(args, "turn_id", None),
        request_id=getattr(args, "request_id", None),
        since=since,
        latest_failure=getattr(args, "latest_failure", False),
        output=Path(output_raw) if output_raw else None,
        bundle_format=getattr(args, "bundle_format", "directory"),
        max_files=getattr(args, "max_files", None),
        max_entries=getattr(args, "max_entries", None),
        max_source_bytes=getattr(args, "max_source_bytes", None),
        max_bundle_bytes=getattr(args, "max_bundle_bytes", None),
    )

    try:
        result = create_diagnostics_bundle(config, options)
    except FileExistsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error writing diagnostics bundle: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Diagnostics bundle: {result.path}")
    print(f"Format: {result.format}")
    print(f"Size: {result.size_bytes} bytes")
    print(f"Entries: {result.entries}")
    if result.warnings:
        print(f"Warnings: {len(result.warnings)}")
        for warning in result.warnings[:5]:
            print(f"  - {warning}")
        if len(result.warnings) > 5:
            print(f"  - ... {len(result.warnings) - 5} more warning(s) in manifest.json")
    print("Inspect the bundle before sharing. It is redacted by default and was not uploaded.")
