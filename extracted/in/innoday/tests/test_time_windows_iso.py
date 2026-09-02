"""`parse_iso_naive` — the variant that unblocked the abandoned consolidation.

`parse_iso_utc` shipped with a docstring claiming it replaced "every one of the
copies". It had not: measured across `src/`, **4 files imported it and 31
hand-rolled `fromisoformat(...replace("Z", "+00:00"))` sites remained**. The
reason was not laziness — it returns an *aware* datetime, and most columns in
this schema are naive, so every caller with a naive column had to post-process
it and kept a private copy instead.

Those copies then drifted, and two ways of drifting are pinned here because both
were live:

* **The offset bug.** `board_sync_service._completed_at_from` did
  `fromisoformat(...).replace(tzinfo=None)` — stripping the offset rather than
  converting it. A Jira instance in a non-UTC timezone returns `resolutiondate`
  with a real offset, so completion times were stored hours wrong, silently, in
  the direction of the offset.
* **The missing guard.** Several copies had no `try` at all, so a malformed
  date from a third-party payload raised mid-sync instead of degrading.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.utils.time_windows import parse_iso_naive, parse_iso_utc


class TestParseIsoNaive:
    def test_z_suffix(self):
        assert parse_iso_naive("2026-08-07T20:07:51.167Z") == datetime(
            2026, 8, 7, 20, 7, 51, 167000
        )

    def test_an_offset_is_converted_not_stripped(self):
        """The bug that made Jira completion times wrong by the offset.

        `+02:00` is 18:07 UTC. Dropping the tzinfo without converting records
        20:07 — same digits, wrong instant, and nothing anywhere says so.
        """
        assert parse_iso_naive("2026-08-07T20:07:51+02:00") == datetime(
            2026, 8, 7, 18, 7, 51
        )

    def test_a_negative_offset_too(self):
        assert parse_iso_naive("2026-08-07T20:07:51-05:00") == datetime(
            2026, 8, 8, 1, 7, 51
        )

    def test_the_result_is_naive(self):
        """It exists to feed naive columns; an aware value defeats the point."""
        assert parse_iso_naive("2026-08-07T20:07:51Z").tzinfo is None

    @pytest.mark.parametrize("value", [None, "", "garbage", 42, "2026-13-45"])
    def test_unusable_input_is_none_not_an_exception(self, value):
        """Every caller is reading a third-party payload.

        "This field is junk today" must not take down a whole sync.
        """
        assert parse_iso_naive(value) is None

    def test_a_datetime_passes_through(self):
        aware = datetime(2026, 8, 7, 20, 7, 51, tzinfo=timezone.utc)
        assert parse_iso_naive(aware) == datetime(2026, 8, 7, 20, 7, 51)


class TestTheTwoVariantsAgreeOnTheInstant:
    """The only difference between them must be the tzinfo, never the moment."""

    @pytest.mark.parametrize(
        "value",
        [
            "2026-08-07T20:07:51Z",
            "2026-08-07T20:07:51+02:00",
            "2026-08-07T20:07:51-05:00",
            "2026-08-07T20:07:51",
        ],
    )
    def test_same_instant(self, value):
        aware = parse_iso_utc(value)
        naive = parse_iso_naive(value)
        assert aware is not None and naive is not None
        assert naive == aware.astimezone(timezone.utc).replace(tzinfo=None)
