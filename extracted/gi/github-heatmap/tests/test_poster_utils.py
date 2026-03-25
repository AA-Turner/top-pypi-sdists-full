from github_heatmap.config import GITHUB_LEVEL_COLORS
from github_heatmap.drawer import Drawer
from github_heatmap.poster import Poster
from github_heatmap.utils import (
    build_level_colors,
    interpolate_color,
    make_github_level_thresholds,
    make_key_times,
    parse_years,
    resolve_github_level,
)


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


def test_make_github_level_thresholds():
    assert make_github_level_thresholds([]) == ()
    assert make_github_level_thresholds([0, 1, 1, 2, 3, 5, 8, 13]) == (1, 3, 8)


def test_resolve_github_level():
    thresholds = (2, 5, 9)

    assert resolve_github_level(0, thresholds) == 0
    assert resolve_github_level(2, thresholds) == 1
    assert resolve_github_level(5, thresholds) == 2
    assert resolve_github_level(9, thresholds) == 3
    assert resolve_github_level(10, thresholds) == 4


def test_build_level_colors_uses_exact_palette_when_provided():
    assert list(GITHUB_LEVEL_COLORS) == [
        "#9BE9A8",
        "#40C463",
        "#30A14E",
        "#216E39",
    ]
    assert len(build_level_colors("#40C463")) == 4


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


def test_drawer_make_color_uses_github_levels():
    poster = Poster()
    poster.use_github_level_mapping = True
    poster.level_colors = list(GITHUB_LEVEL_COLORS)
    poster.level_thresholds = (2, 5, 9)
    poster.colors["dom"] = "#ebedf0"
    drawer = Drawer(poster)

    assert drawer.make_color(poster.length_range_by_date, 0) == "#ebedf0"
    assert drawer.make_color(poster.length_range_by_date, 2) == "#9BE9A8"
    assert drawer.make_color(poster.length_range_by_date, 5) == "#40C463"
    assert drawer.make_color(poster.length_range_by_date, 9) == "#30A14E"
    assert drawer.make_color(poster.length_range_by_date, 12) == "#216E39"
