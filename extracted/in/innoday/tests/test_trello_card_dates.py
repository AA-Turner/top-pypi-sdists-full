"""A malformed Trello card date costs one field, not the whole sync.

`TrelloAPI` built `Ticket.created_at` with
`datetime.fromisoformat(card.get("dateLastActivity", <now>.isoformat()))` — three
problems in one expression:

* **no error handling**, so one card with an unexpected `dateLastActivity` shape
  raised `ValueError` partway through building a board's tickets;
* the default built an ISO string on *every* card just to parse it straight
  back; and
* both branches produced an **aware** datetime for `Ticket.created_at`, which is
  a naive column — the mismatch CLAUDE.md now names as the convention.
"""

from __future__ import annotations

import pytest

from src.api.trello_api import TrelloAPI, _now_naive


class TestNowNaive:
    def test_is_naive(self):
        assert _now_naive().tzinfo is None


class TestCardDates:
    """Exercised through `_card_to_ticket`-shaped input, not the network."""

    @staticmethod
    def _api() -> TrelloAPI:
        api = TrelloAPI.__new__(TrelloAPI)
        api.api_key = "k"
        api.token = "t"
        return api

    @pytest.mark.parametrize(
        "value",
        [None, "", "garbage", "not-a-date", "2026-13-45T99:00:00"],
    )
    def test_an_unusable_date_falls_back_instead_of_raising(self, value):
        """The point of the change: one bad card must not kill the sync."""
        from src.utils.time_windows import parse_iso_naive

        assert parse_iso_naive(value) is None
        # ...and the call site's `or _now_naive()` turns that into a usable
        # timestamp rather than an exception.
        assert (parse_iso_naive(value) or _now_naive()).tzinfo is None

    def test_a_real_trello_stamp_parses_to_naive_utc(self):
        """Trello sends `...Z`; the column is naive."""
        from datetime import datetime

        from src.utils.time_windows import parse_iso_naive

        parsed = parse_iso_naive("2026-08-07T20:07:51.000Z")
        assert parsed == datetime(2026, 8, 7, 20, 7, 51)
        assert parsed.tzinfo is None

    def test_the_source_no_longer_parses_inline(self):
        """Guards the regression, not just the helper.

        The helper being correct means nothing if a future edit reintroduces a
        bare `fromisoformat` at the call site — which is how this survived the
        first pass over the file.
        """
        import inspect

        import src.api.trello_api as trello_module

        source = inspect.getsource(trello_module)
        assert "fromisoformat" not in source, (
            "trello_api parses ISO inline again; use parse_iso_naive"
        )
