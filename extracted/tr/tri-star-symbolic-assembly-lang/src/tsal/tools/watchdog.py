"""Minimal watchdog to trigger repair loops."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from tsal.tools.brian import analyze_and_repair
from tsal.tools.proactive_scanner import scan_todo_file, scan_typos_file


def _check_todo(path: Path) -> None:
    hits = scan_todo_file(path)
    if hits:
        print(f"[Watchdog] TODO found in {path}")


def _check_typos(path: Path) -> None:
    hits = scan_typos_file(path)
    if hits:
        print(f"[Watchdog] Typos found in {path}: {len(hits)}")


def watch(
    path: str = "src/tsal",
    interval: float = 30.0,
    cycles: int = 0,
    repair: bool = False,
    todo: bool = False,
    typos: bool = False,
) -> None:
    """Monitor ``path`` and run analyze_and_repair on changed files."""
    base = Path(path)
    seen = {f: f.stat().st_mtime for f in base.rglob("*.py")}
    count = 0
    while True:
        for file in base.rglob("*.py"):
            mtime = file.stat().st_mtime
            if file not in seen or mtime > seen[file]:
                analyze_and_repair(str(file), repair=repair)
                if todo:
                    _check_todo(file)
                if typos:
                    _check_typos(file)
                seen[file] = mtime
        count += 1
        if cycles and count >= cycles:
            break
        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Continuous repair watchdog")
    parser.add_argument("path", nargs="?", default="src/tsal")
    parser.add_argument("--repair", action="store_true")
    parser.add_argument("--interval", type=float, default=30.0)
    parser.add_argument("--cycles", type=int, default=0)
    parser.add_argument("--todo", action="store_true")
    parser.add_argument("--typos", action="store_true")
    args = parser.parse_args()
    watch(
        args.path,
        interval=args.interval,
        cycles=args.cycles,
        repair=args.repair,
        todo=args.todo,
        typos=args.typos,
    )


if __name__ == "__main__":
    main()
