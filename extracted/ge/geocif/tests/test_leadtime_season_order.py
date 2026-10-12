"""Lead-time plots order issue months by season, not by calendar.

A season that crosses the new year (Afghanistan poppy: windows ending Oct..Aug)
used to plot Oct, Nov and Dec to the right of August.
"""

from geocif.viz.leadtime import _MONTHS, _season_order


def _labels(order):
    return [_MONTHS[(x - 1) % 12] for x in sorted(order.values())]


def test_season_crossing_the_new_year_starts_in_october():
    order = _season_order([1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12])
    assert _labels(order) == ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
    assert order[10] == 10 and order[1] == 13 and order[8] == 20


def test_season_within_one_year_keeps_calendar_order():
    order = _season_order([4, 5, 6, 7, 8, 9, 10])
    assert order == {m: m for m in range(4, 11)}


def test_all_twelve_months_and_single_month_unchanged():
    assert _season_order(range(1, 13)) == {m: m for m in range(1, 13)}
    assert _season_order([7]) == {7: 7}
