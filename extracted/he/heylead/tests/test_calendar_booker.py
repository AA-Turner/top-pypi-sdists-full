"""Tests for the calendar booking service."""

import pytest

from heylead.services.calendar_booker import (
    _extract_datetime_from_text,
    _parse_calendly_path,
    _parse_calcom_path,
    _pick_best_slot,
    detect_provider,
    format_booking_result,
)


class TestDetectProvider:
    def test_calendly(self):
        assert detect_provider("https://calendly.com/john/30min") == "calendly"

    def test_calendly_with_www(self):
        assert detect_provider("https://www.calendly.com/john/30min") == "calendly"

    def test_calcom(self):
        assert detect_provider("https://cal.com/john/30min") == "calcom"

    def test_unknown(self):
        assert detect_provider("https://example.com/book") == "unknown"

    def test_acuity(self):
        assert detect_provider("https://acuityscheduling.com/schedule") == "unknown"


class TestParseCalendlyPath:
    def test_standard(self):
        assert _parse_calendly_path("https://calendly.com/john/30min") == ("john", "30min")

    def test_no_event_slug(self):
        assert _parse_calendly_path("https://calendly.com/john") == ("john", "")

    def test_trailing_slash(self):
        assert _parse_calendly_path("https://calendly.com/john/30min/") == ("john", "30min")

    def test_empty(self):
        assert _parse_calendly_path("https://calendly.com/") == ("", "")


class TestParseCalcomPath:
    def test_standard(self):
        assert _parse_calcom_path("https://cal.com/jane/15min") == ("jane", "15min")

    def test_no_event(self):
        assert _parse_calcom_path("https://cal.com/jane") == ("jane", "")


class TestPickBestSlot:
    def test_prefers_midmorning(self):
        slots = [
            {"start": "2026-03-25T08:00:00+00:00"},  # 8 AM — too early (outside biz hours)
            {"start": "2026-03-25T10:00:00+00:00"},  # 10 AM — ideal
            {"start": "2026-03-25T16:00:00+00:00"},  # 4 PM — OK
        ]
        chosen = _pick_best_slot(slots)
        assert chosen is not None
        assert "10:00" in chosen["start"]

    def test_skips_weekends(self):
        # 2026-03-28 is a Saturday, 2026-03-30 is Monday
        slots = [
            {"start": "2026-03-28T10:00:00+00:00"},  # Saturday
            {"start": "2026-03-30T10:00:00+00:00"},  # Monday
        ]
        chosen = _pick_best_slot(slots)
        assert chosen is not None
        assert "03-30" in chosen["start"]

    def test_empty_slots(self):
        assert _pick_best_slot([]) is None

    def test_fallback_to_any(self):
        # Only a slot outside business hours — should still fall back
        slots = [
            {"start": "2026-03-25T20:00:00+00:00"},  # 8 PM
        ]
        chosen = _pick_best_slot(slots)
        assert chosen is not None  # Falls back to any slot


class TestFormatBookingResult:
    def test_success(self):
        result = {
            "success": True,
            "provider": "calendly",
            "booked_time": "2026-03-25T10:00:00+00:00",
            "duration_minutes": 30,
        }
        text = format_booking_result(result)
        assert "Meeting booked" in text
        assert "Calendly" in text
        assert "30 min" in text

    def test_failure(self):
        result = {
            "success": False,
            "error": "No slots available",
            "url": "https://calendly.com/john/30min",
        }
        text = format_booking_result(result)
        assert "Could not auto-book" in text
        assert "calendly.com" in text

    def test_failure_with_attempted_time(self):
        result = {
            "success": False,
            "error": "Booking failed (403)",
            "url": "https://cal.com/jane/15min",
            "attempted_time": "2026-03-25T14:00:00+00:00",
        }
        text = format_booking_result(result)
        assert "cal.com" in text
        assert "2026-03-25" in text


class TestExtractDatetime:
    def test_iso_with_offset(self):
        assert (
            _extract_datetime_from_text("Meeting booked for 2026-04-01T10:00:00+00:00")
            == "2026-04-01T10:00:00+00:00"
        )

    def test_iso_with_z(self):
        assert (
            _extract_datetime_from_text("Your slot is 2026-04-01T14:30:00Z confirmed")
            == "2026-04-01T14:30:00Z"
        )

    def test_iso_without_tz(self):
        assert (
            _extract_datetime_from_text("Confirmed: 2026-04-01T09:00:00")
            == "2026-04-01T09:00:00"
        )

    def test_no_datetime(self):
        assert _extract_datetime_from_text("No date here") is None


class TestBrowserAgentBooking:
    """Tests for the browser agent booking fallback."""

    @pytest.mark.asyncio
    async def test_unknown_provider_without_browser_use(self, monkeypatch):
        """Without browser-use installed, unknown providers return manual URL."""
        import heylead.services.calendar_booker as cb

        monkeypatch.setattr(cb, "_BROWSER_USE_AVAILABLE", False)

        result = await cb.book_meeting(
            "https://acuityscheduling.com/john/meeting",
            "Test User",
            "test@example.com",
            "UTC",
        )
        assert result["success"] is False
        assert result["provider"] == "unknown"
        assert "Book manually" in result["error"]

    @pytest.mark.asyncio
    async def test_browser_agent_success(self, monkeypatch):
        """Browser agent successfully books a meeting."""
        import heylead.services.calendar_booker as cb

        monkeypatch.setattr(cb, "_BROWSER_USE_AVAILABLE", True)

        async def mock_book_browser(url, name, email, tz):
            return {
                "success": True,
                "provider": "acuityscheduling",
                "booked_time": "2026-04-01T10:00:00+00:00",
                "duration_minutes": 30,
                "confirmation": {"agent_response": "Booked for April 1"},
            }

        monkeypatch.setattr(cb, "_book_browser_agent", mock_book_browser)

        result = await cb.book_meeting(
            "https://acuityscheduling.com/john/meeting",
            "Test User",
            "test@example.com",
            "UTC",
        )
        assert result["success"] is True
        assert result["provider"] == "acuityscheduling"
        assert "10:00" in result["booked_time"]

    @pytest.mark.asyncio
    async def test_browser_agent_failure_falls_back(self, monkeypatch):
        """When browser agent fails, still returns manual URL."""
        import heylead.services.calendar_booker as cb

        monkeypatch.setattr(cb, "_BROWSER_USE_AVAILABLE", True)

        async def mock_book_browser_fail(url, name, email, tz):
            return {
                "success": False,
                "provider": "hubspot",
                "error": "Could not find available slots",
                "url": url,
            }

        monkeypatch.setattr(cb, "_book_browser_agent", mock_book_browser_fail)

        result = await cb.book_meeting(
            "https://meetings.hubspot.com/jane/intro",
            "Test User",
            "test@example.com",
            "UTC",
        )
        assert result["success"] is False
        assert result["provider"] == "unknown"
        assert "Book manually" in result["error"]

    def test_check_browser_use_caches(self, monkeypatch):
        """_check_browser_use caches its result."""
        import heylead.services.calendar_booker as cb

        monkeypatch.setattr(cb, "_BROWSER_USE_AVAILABLE", None)
        result = cb._check_browser_use()
        assert isinstance(result, bool)
        # Second call returns cached value without re-importing
        assert cb._check_browser_use() == result
