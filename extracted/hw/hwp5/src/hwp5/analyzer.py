"""Core calendar parsing and hard-work window analysis."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class CalendarEvent:
    """Single calendar event extracted from an ICS export."""

    start: datetime
    end: datetime
    summary: str

    @property
    def duration_hours(self) -> float:
        seconds = max((self.end - self.start).total_seconds(), 0.0)
        return seconds / 3600.0


@dataclass(frozen=True)
class HardWorkWindow:
    """Analysis result for one date window."""

    start_date: date
    end_date: date
    event_count: int
    total_hours: float
    matching_summaries: tuple[str, ...]


def _parse_ics_datetime(raw_value: str) -> datetime:
    value = raw_value.strip()
    if not value:
        raise ValueError("Empty date value in ICS file")

    # Handle all-day events.
    if len(value) == 8 and value.isdigit():
        return datetime.strptime(value, "%Y%m%d")

    # Keep parser intentionally strict for predictable behavior.
    if value.endswith("Z"):
        return datetime.strptime(value, "%Y%m%dT%H%M%SZ")
    return datetime.strptime(value, "%Y%m%dT%H%M%S")


def _extract_property(line: str, key: str) -> str | None:
    if not line.startswith(key):
        return None
    _, _, value = line.partition(":")
    return value.strip()


def load_ics_events(path: str | Path) -> list[CalendarEvent]:
    """Load events from an ICS calendar export."""

    file_path = Path(path)
    lines = file_path.read_text(encoding="utf-8").splitlines()

    events: list[CalendarEvent] = []
    in_event = False
    current: dict[str, str] = {}

    for raw_line in lines:
        line = raw_line.strip()
        if line == "BEGIN:VEVENT":
            in_event = True
            current = {}
            continue
        if line == "END:VEVENT":
            if in_event and "DTSTART" in current and "DTEND" in current:
                start = _parse_ics_datetime(current["DTSTART"])
                end = _parse_ics_datetime(current["DTEND"])
                summary = current.get("SUMMARY", "")
                events.append(CalendarEvent(start=start, end=end, summary=summary))
            in_event = False
            current = {}
            continue
        if not in_event:
            continue

        dtstart = _extract_property(line, "DTSTART")
        if dtstart is not None:
            current["DTSTART"] = dtstart
            continue

        dtend = _extract_property(line, "DTEND")
        if dtend is not None:
            current["DTEND"] = dtend
            continue

        summary = _extract_property(line, "SUMMARY")
        if summary is not None:
            current["SUMMARY"] = summary

    return events


def _matches_keywords(summary: str, keywords: Sequence[str]) -> bool:
    lowered = summary.lower()
    return any(token.lower() in lowered for token in keywords)


def find_hard_work_windows(
    events: Iterable[CalendarEvent],
    *,
    window_days: int = 5,
    min_hours: float = 20.0,
    keywords: Sequence[str] = ("hard work", "deep work", "focus"),
) -> list[HardWorkWindow]:
    """
    Find windows with significant hard work.

    A result window is included when total duration of matching events
    within the `window_days` period is >= `min_hours`.
    """

    if window_days <= 0:
        raise ValueError("window_days must be > 0")
    if min_hours < 0:
        raise ValueError("min_hours must be >= 0")

    normalized = sorted(events, key=lambda item: item.start)
    if not normalized:
        return []

    matching = [event for event in normalized if _matches_keywords(event.summary, keywords)]
    if not matching:
        return []

    first_day = matching[0].start.date()
    last_day = matching[-1].start.date()
    max_start = last_day - timedelta(days=window_days - 1)
    if max_start < first_day:
        max_start = first_day

    output: list[HardWorkWindow] = []
    current_day = first_day

    while current_day <= max_start:
        window_end = current_day + timedelta(days=window_days)
        selected = [
            event
            for event in matching
            if current_day <= event.start.date() < window_end
        ]
        total_hours = sum(event.duration_hours for event in selected)
        if total_hours >= min_hours:
            output.append(
                HardWorkWindow(
                    start_date=current_day,
                    end_date=window_end - timedelta(days=1),
                    event_count=len(selected),
                    total_hours=round(total_hours, 2),
                    matching_summaries=tuple(event.summary for event in selected),
                )
            )
        current_day += timedelta(days=1)

    return output
