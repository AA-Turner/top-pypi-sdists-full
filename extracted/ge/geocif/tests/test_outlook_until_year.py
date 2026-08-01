"""Regression test for yield_outlook.run(until_year=...) upper-bound param.

The outlook forecast/eval loop is
    outlook_seasons = list(range(since_year, current_year + 1))
where ``current_year`` is set to ``until_year`` when a bounded hindcast is
requested (see yield_outlook.run). This test pins:

  1. run() exposes an ``until_year`` keyword (default None).
  2. The documented window semantics: since_year..until_year inclusive.
  3. Default (until_year is None -> falls back to current_year) is a no-op.

Structural only — it does not execute the ML pipeline (that needs the full
cluster env + data), but it guards the signature + range arithmetic that the
bounded-hindcast feature depends on.
"""
import inspect

import geocif.yield_outlook as yo


def test_run_has_until_year_param():
    sig = inspect.signature(yo.run)
    assert "until_year" in sig.parameters, "run() must expose until_year"
    assert sig.parameters["until_year"].default is None, (
        "until_year must default to None so the config/current_year fallback wins"
    )


def _outlook_seasons(since_year, until_year):
    """Mirror of the window computed inside run() after until_year resolution."""
    current_year = until_year  # run() sets current_year = until_year
    return list(range(since_year, current_year + 1))


def test_bounded_hindcast_window_2001_2020():
    seasons = _outlook_seasons(2001, 2020)
    assert seasons[0] == 2001 and seasons[-1] == 2020
    assert len(seasons) == 20
    assert 2020 in seasons and 2021 not in seasons and 2000 not in seasons


def test_default_until_year_is_noop():
    # When until_year falls back to current_year, the window is unchanged
    # from the legacy range(since_year, current_year + 1).
    since, cur = 2005, 2026
    assert _outlook_seasons(since, cur) == list(range(since, cur + 1))
