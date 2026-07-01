"""Command-line interface for hwp5."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .analyzer import find_hard_work_windows, load_ics_events


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hwp5",
        description="Search calendar exports for hard-work intensity over 5-day windows.",
    )
    parser.add_argument("ics_file", type=Path, help="Path to the .ics calendar export")
    parser.add_argument(
        "--window-days",
        type=int,
        default=5,
        help="Rolling window size in days (default: 5)",
    )
    parser.add_argument(
        "--min-hours",
        type=float,
        default=20.0,
        help="Minimum hard-work hours per window (default: 20)",
    )
    parser.add_argument(
        "--keyword",
        action="append",
        dest="keywords",
        default=None,
        help="Keyword to treat as hard work in SUMMARY (repeatable)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    return parser


def _format_text(windows: Sequence) -> str:
    if not windows:
        return "No hard-work windows found."
    lines = ["Hard-work windows found:"]
    for item in windows:
        lines.append(
            (
                f"- {item.start_date} to {item.end_date}: "
                f"{item.total_hours}h across {item.event_count} events"
            )
        )
    return "\n".join(lines)


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if not args.ics_file.exists():
        parser.error(f"File not found: {args.ics_file}")

    events = load_ics_events(args.ics_file)
    keywords = tuple(args.keywords) if args.keywords else ("hard work", "deep work", "focus")
    windows = find_hard_work_windows(
        events,
        window_days=args.window_days,
        min_hours=args.min_hours,
        keywords=keywords,
    )

    if args.json:
        payload = [
            {
                "start_date": item.start_date.isoformat(),
                "end_date": item.end_date.isoformat(),
                "event_count": item.event_count,
                "total_hours": item.total_hours,
                "matching_summaries": list(item.matching_summaries),
            }
            for item in windows
        ]
        print(json.dumps(payload, indent=2))
    else:
        print(_format_text(windows))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
