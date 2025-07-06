"""Proactive source checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

from .aletheia_checker import scan_file as _scan_file


def scan_todo_file(path: str | Path) -> List[Tuple[int, str]]:
    """Return TODO lines from ``path``."""
    file = Path(path)
    hits: List[Tuple[int, str]] = []
    with open(file, "r", encoding="utf-8", errors="ignore") as fh:
        for lineno, line in enumerate(fh, 1):
            if "TODO" in line:
                hits.append((lineno, line.strip()))
    return hits


def scan_typos_file(path: str | Path) -> List[Tuple[int, str]]:
    """Return probable typos from ``path``."""
    return _scan_file(Path(path))


def scan_todos(base: str = "src") -> Dict[str, List[Tuple[int, str]]]:
    """Return TODO comments grouped by file."""
    root = Path(base)
    results: Dict[str, List[Tuple[int, str]]] = {}
    for path in root.rglob("*.py"):
        hits = scan_todo_file(path)
        if hits:
            results[str(path)] = hits
    return results


def _scan_root(root: Path) -> Dict[str, List[Tuple[int, str]]]:
    typos: Dict[str, List[Tuple[int, str]]] = {}
    for file in root.rglob("*.py"):
        hits = scan_typos_file(file)
        if hits:
            typos[str(file)] = hits
    return typos


def scan_typos(base: str = "src") -> Dict[str, List[Tuple[int, str]]]:
    """Return probable typos grouped by file."""
    return _scan_root(Path(base))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run proactive code scans")
    parser.add_argument("--path", default="src/tsal")
    parser.add_argument("--todos", action="store_true")
    parser.add_argument("--typos", action="store_true")
    args = parser.parse_args()

    if not args.todos and not args.typos:
        args.todos = args.typos = True

    results = {}
    if args.todos:
        results["todos"] = scan_todos(args.path)
    if args.typos:
        results["typos"] = scan_typos(args.path)
    print(json.dumps(results))


if __name__ == "__main__":
    main()
