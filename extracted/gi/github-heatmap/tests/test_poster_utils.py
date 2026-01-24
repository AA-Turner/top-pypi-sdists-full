from github_heatmap.drawer import Drawer
from github_heatmap.poster import Poster
from github_heatmap.utils import interpolate_color, make_key_times, parse_years


def test_interpolate_color():
    assert interpolate_color("#000000", "#ffffff", 0) == "#000000"
    assert interpolate_color("#000000", "#ffffff", 1) == "#ffffff"
    assert interpolate_color("#000000", "#ffffff", 0.5) == "#7f7f7f"
    assert interpolate_color("#000000", "#ffffff", -100) == "#000000"
    assert interpolate_color("#000000", "#ffffff", 12345) == "#ffffff"


def test_parse_years():
    assert parse_years("2012") == (2012, 2012)
    assert parse_years("2015-2021") == (2015, 2021)
    assert parse_years("2021-2015") == (2015, 2021)


def test_make_key_times():
    assert make_key_times(5) == ["0", "0.2", "0.4", "0.6", "0.8", "1"]


def test_drawer_tooltip_formatting():
    poster = Poster()
    poster.units = "XP"
    drawer = Drawer(poster)

    assert drawer._format_tooltip("2024-01-01", 10) == "2024-01-01 10 XP"
    assert drawer._format_tooltip("2024-01-01") == "2024-01-01"

    poster.tooltip_template = "{date}: {value}{unit}"
    assert drawer._format_tooltip("2024-01-01", 5) == "2024-01-01: 5XP"
    assert drawer._format_tooltip("2024-01-01") == "2024-01-01"

    poster.tooltip_template = "{date} {value} for {type}"
    assert (
        drawer._format_tooltip("2024-01-01", 7, "run")
        == "2024-01-01 7 for run"
    )

    poster.tooltip_by_date = {"2024-01-01": "Custom"}
    assert drawer._format_tooltip("2024-01-01", 5) == "Custom"

    poster.tooltip_by_date = {"2024-01-02": {"run": "Run note"}}
    assert drawer._format_tooltip("2024-01-02", 3, "run") == "Run note"
