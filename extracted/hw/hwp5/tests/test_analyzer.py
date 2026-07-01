from datetime import datetime

from hwp5.analyzer import CalendarEvent, find_hard_work_windows, load_ics_events


def test_find_hard_work_windows_filters_and_aggregates():
    events = [
        CalendarEvent(
            start=datetime(2026, 5, 1, 9, 0, 0),
            end=datetime(2026, 5, 1, 13, 0, 0),
            summary="Hard Work - backend",
        ),
        CalendarEvent(
            start=datetime(2026, 5, 2, 9, 0, 0),
            end=datetime(2026, 5, 2, 14, 0, 0),
            summary="Deep Work - docs",
        ),
        CalendarEvent(
            start=datetime(2026, 5, 3, 10, 0, 0),
            end=datetime(2026, 5, 3, 12, 0, 0),
            summary="Team sync",
        ),
        CalendarEvent(
            start=datetime(2026, 5, 4, 8, 0, 0),
            end=datetime(2026, 5, 4, 13, 0, 0),
            summary="Focus sprint",
        ),
        CalendarEvent(
            start=datetime(2026, 5, 5, 8, 0, 0),
            end=datetime(2026, 5, 5, 14, 0, 0),
            summary="Hard work - release",
        ),
    ]

    windows = find_hard_work_windows(events, window_days=5, min_hours=20)
    assert len(windows) == 1
    assert windows[0].total_hours == 20.0
    assert windows[0].event_count == 4


def test_load_ics_events_reads_basic_vevents(tmp_path):
    ics_content = """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20260501T090000
DTEND:20260501T110000
SUMMARY:Hard Work block
END:VEVENT
BEGIN:VEVENT
DTSTART:20260502T130000
DTEND:20260502T150000
SUMMARY:Lunch
END:VEVENT
END:VCALENDAR
"""
    test_file = tmp_path / "sample.ics"
    test_file.write_text(ics_content, encoding="utf-8")

    events = load_ics_events(test_file)
    assert len(events) == 2
    assert events[0].summary == "Hard Work block"
