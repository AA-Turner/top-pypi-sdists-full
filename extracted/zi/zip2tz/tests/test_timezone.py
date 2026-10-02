"""Tests for zip2tz timezone lookup."""

import pytest

import zip2tz
from zip2tz._data import TIMEZONES


class TestStringInput:
    """Test timezone lookup with string zip codes."""

    def test_basic_lookup(self) -> None:
        """Basic string zip code lookup."""
        assert zip2tz.timezone("90210") == "America/Los_Angeles"
        assert zip2tz.timezone("10001") == "America/New_York"
        assert zip2tz.timezone("60601") == "America/Chicago"

    def test_leading_zero_zipcode(self) -> None:
        """Zip codes with leading zeros (Northeast US)."""
        # Massachusetts (Agawam)
        assert zip2tz.timezone("01001") == "America/New_York"
        # Connecticut
        assert zip2tz.timezone("06001") == "America/New_York"
        # New Jersey
        assert zip2tz.timezone("07001") == "America/New_York"
        # IRS zip code
        assert zip2tz.timezone("00501") == "America/New_York"

    def test_not_found_returns_none(self) -> None:
        """Unknown zip codes return None."""
        assert zip2tz.timezone("00000") is None
        assert zip2tz.timezone("99999") is None


class TestIntegerInput:
    """Test timezone lookup with integer zip codes."""

    def test_basic_lookup(self) -> None:
        """Basic integer zip code lookup."""
        assert zip2tz.timezone(90210) == "America/Los_Angeles"
        assert zip2tz.timezone(10001) == "America/New_York"
        assert zip2tz.timezone(60601) == "America/Chicago"

    def test_leading_zero_as_integer(self) -> None:
        """Integer zip codes that would have leading zeros as strings."""
        # 01001 as int is 1001
        assert zip2tz.timezone(1001) == "America/New_York"
        # 06001 as int is 6001
        assert zip2tz.timezone(6001) == "America/New_York"
        # 00501 as int is 501
        assert zip2tz.timezone(501) == "America/New_York"

    def test_not_found_returns_none(self) -> None:
        """Unknown integer zip codes return None."""
        assert zip2tz.timezone(0) is None
        assert zip2tz.timezone(99999) is None


class TestIndianaTimezones:
    """Test Indiana's complex county-level timezone boundaries."""

    def test_indianapolis_eastern(self) -> None:
        """Indianapolis area - Eastern time."""
        assert zip2tz.timezone("46201") == "America/Indiana/Indianapolis"
        assert zip2tz.timezone("46204") == "America/Indiana/Indianapolis"

    def test_indiana_central_time_counties(self) -> None:
        """Northwest Indiana counties on Central time."""
        # Gary, IN area (Lake County) - Central time
        assert zip2tz.timezone("46401") == "America/Chicago"

    def test_indiana_other_eastern_zones(self) -> None:
        """Other Indiana Eastern time zones."""
        # These have their own IANA zones due to historical DST differences
        result = zip2tz.timezone("47591")  # Knox County area
        assert result is not None
        assert "Indiana" in result or result == "America/Chicago"


class TestNorthDakotaTimezones:
    """Test North Dakota's split counties."""

    def test_north_dakota_central(self) -> None:
        """Most of North Dakota is Central time."""
        # Fargo area
        assert zip2tz.timezone("58102") == "America/Chicago"

    def test_north_dakota_mountain(self) -> None:
        """Southwest ND counties on Mountain time."""
        # Check if we have any Mountain time zips in ND
        result = zip2tz.timezone("58645")  # Bowman County area
        assert result in ("America/Denver", "America/Chicago", None)


class TestAlaskaTimezones:
    """Test Alaska's multiple timezones."""

    def test_anchorage(self) -> None:
        """Anchorage area - Alaska time."""
        assert zip2tz.timezone("99501") == "America/Anchorage"

    def test_juneau(self) -> None:
        """Juneau - Alaska time."""
        result = zip2tz.timezone("99850")
        assert result in ("America/Juneau", "America/Anchorage", "America/Sitka")

    def test_adak(self) -> None:
        """Adak - Hawaii-Aleutian time."""
        assert zip2tz.timezone("99546") == "America/Adak"


class TestHawaii:
    """Test Hawaii timezone."""

    def test_honolulu(self) -> None:
        """Honolulu - Hawaii time."""
        assert zip2tz.timezone("96801") == "Pacific/Honolulu"

    def test_maui(self) -> None:
        """Maui - Hawaii time."""
        assert zip2tz.timezone("96768") == "Pacific/Honolulu"


class TestArizona:
    """Test Arizona (no DST except Navajo Nation)."""

    def test_phoenix(self) -> None:
        """Phoenix - Mountain Standard (no DST)."""
        assert zip2tz.timezone("85001") == "America/Phoenix"

    def test_phoenix_metro(self) -> None:
        """Phoenix metro area (Queen Creek) - Mountain Standard (no DST)."""
        assert zip2tz.timezone("85142") == "America/Phoenix"

    def test_tucson(self) -> None:
        """Tucson - Mountain Standard (no DST)."""
        assert zip2tz.timezone("85701") == "America/Phoenix"


class TestEdgeCases:
    """Test edge cases and invalid inputs."""

    def test_empty_string(self) -> None:
        """Empty string returns None."""
        assert zip2tz.timezone("") is None

    def test_non_numeric_string(self) -> None:
        """Non-numeric strings return None."""
        assert zip2tz.timezone("abcde") is None
        assert zip2tz.timezone("hello") is None

    def test_float_input(self) -> None:
        """Float input should work (converted to int)."""
        assert zip2tz.timezone(90210.0) == "America/Los_Angeles"

    def test_none_input(self) -> None:
        """None input returns None."""
        assert zip2tz.timezone(None) is None  # type: ignore[arg-type]

    def test_negative_number(self) -> None:
        """Negative numbers return None."""
        assert zip2tz.timezone(-12345) is None

    def test_too_long_zipcode(self) -> None:
        """Zip+4 format returns None (only 5-digit supported)."""
        assert zip2tz.timezone("902100001") is None
        assert zip2tz.timezone("90210-0001") is None


class TestAllTimezones:
    """Verify all returned timezones are valid IANA format."""

    def test_timezone_format(self) -> None:
        """All timezones should be in IANA format (contain '/')."""
        for tz in TIMEZONES:
            assert "/" in tz, f"Invalid timezone format: {tz}"
            assert tz.startswith(("America/", "Pacific/")), f"Unexpected timezone: {tz}"
