"""Shared CLI helpers for the ``ci`` command group.

These centralise boilerplate that was previously copied across the ``ci run``
and ``ci run-local`` entry points: emitting a JSON payload to stdout and parsing
repeatable ``KEY=VALUE`` options.
"""

import json
import sys
from typing import Any

import typer


def emit_json(obj: Any) -> None:
    """Write ``obj`` to stdout as indented JSON followed by a trailing newline."""
    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def parse_kv_pairs(pairs: list[str] | None, *, flag: str = "--var") -> dict[str, str]:
    """Parse repeatable ``KEY=VALUE`` CLI options into a dict.

    Exits with code 1 (via ``typer.Exit``) when an entry has no ``=``, echoing
    ``flag`` in the error so the message names the offending option.
    """
    out: dict[str, str] = {}
    for pair in pairs or []:
        if "=" not in pair:
            print(f"ERROR: {flag} must be KEY=VALUE, got: {pair}", file=sys.stderr)
            raise typer.Exit(code=1)
        key, value = pair.split("=", 1)
        out[key] = value
    return out
