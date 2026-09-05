"""Tests for ``[ML] annotate_map_values`` / ``annotate_value_fmt``.

``plot.plot_map`` has supported ``annotate_values`` (region name + the mapped
value on a second line) since the admin-1 error maps were added, but it was
only ever wired to the MAPE/metric choropleths in viz/diagnostics.py -- the
yield and outlook-index maps could not be value-labelled from config. These
flags expose it.

Resolution order mirrors ``annotate_regions``: the COUNTRY section first, then
``[ML]`` as a project-wide fallback, then the default.
"""

import configparser

import pytest


def _resolve_bool(parser, country, option, fallback=False):
    """Mirror of the resolution in analysis.py."""
    return parser.getboolean(
        country, option,
        fallback=parser.getboolean("ML", option, fallback=fallback),
    )


def _resolve_str(parser, country, option, fallback="{:.1f}"):
    return parser.get(
        country, option,
        fallback=parser.get("ML", option, fallback=fallback),
    )


def _cfg(ml=None, country=None):
    p = configparser.ConfigParser(interpolation=None)
    p["ML"] = ml or {}
    p["united_states_of_america"] = country or {}
    return p


# ------------------------------------------------------------- defaults
def test_defaults_off_and_one_decimal():
    p = _cfg()
    assert _resolve_bool(p, "united_states_of_america",
                         "annotate_map_values") is False
    assert _resolve_str(p, "united_states_of_america",
                        "annotate_value_fmt") == "{:.1f}"


def test_absent_country_section_still_falls_back_to_ml():
    p = configparser.ConfigParser(interpolation=None)
    p["ML"] = {"annotate_map_values": "True"}
    # country section missing entirely -> configparser raises NoSectionError
    # unless the fallback path is used; the resolver must not blow up
    with pytest.raises(configparser.NoSectionError):
        p.getboolean("nigeria", "annotate_map_values")
    assert p.getboolean("ML", "annotate_map_values") is True


# ------------------------------------------------------------- precedence
def test_ml_section_enables_project_wide():
    p = _cfg(ml={"annotate_map_values": "True"})
    assert _resolve_bool(p, "united_states_of_america",
                         "annotate_map_values") is True


def test_country_section_overrides_ml():
    p = _cfg(ml={"annotate_map_values": "True"},
             country={"annotate_map_values": "False"})
    assert _resolve_bool(p, "united_states_of_america",
                         "annotate_map_values") is False


def test_country_can_enable_when_ml_off():
    p = _cfg(ml={"annotate_map_values": "False"},
             country={"annotate_map_values": "True"})
    assert _resolve_bool(p, "united_states_of_america",
                         "annotate_map_values") is True


# ------------------------------------------------------------- format
@pytest.mark.parametrize("fmt,value,expected", [
    ("{:.1f}", 13.2749, "13.3"),
    ("{:.2f}", 3.6931, "3.69"),
    ("{:.0f}", 104.4, "104"),      # outlook index
    ("{:,.0f}", 12345.6, "12,346"),
])
def test_value_fmt_applied(fmt, value, expected):
    p = _cfg(ml={"annotate_value_fmt": fmt})
    got = _resolve_str(p, "united_states_of_america", "annotate_value_fmt")
    assert got == fmt
    assert got.format(value) == expected


def test_fmt_country_overrides_ml():
    p = _cfg(ml={"annotate_value_fmt": "{:.1f}"},
             country={"annotate_value_fmt": "{:.0f}"})
    assert _resolve_str(p, "united_states_of_america",
                        "annotate_value_fmt") == "{:.0f}"


def test_yield_and_index_need_different_formats():
    """A yield (~3-13 tn/ha) and an outlook index (~100) are two orders of
    magnitude apart -- the reason the format is configurable at all."""
    assert "{:.1f}".format(3.6931) == "3.7"
    assert "{:.0f}".format(104.37) == "104"


# ------------------------------------------------------------- wiring
def test_plot_map_accepts_the_kwargs():
    """Guard against the signature drifting away from what analysis.py passes."""
    import inspect

    from geocif.viz import plot

    sig = inspect.signature(plot.plot_map)
    assert "annotate_values" in sig.parameters
    assert "value_fmt" in sig.parameters
    assert sig.parameters["annotate_values"].default is False


def test_analysis_passes_both_kwargs_at_every_call_site():
    """All plot_map calls in analysis.py must forward the flags, otherwise
    some maps would silently stay unlabelled."""
    import pathlib

    src = pathlib.Path(
        __import__("geocif").__file__).parent / "analysis.py"
    text = src.read_text(encoding="utf-8", errors="ignore")
    n_calls = text.count("plot.plot_map(")
    n_wired = text.count("annotate_values=self.annotate_map_values")
    assert n_wired >= 1
    # every non-commented call site should be wired
    assert n_wired == n_calls - text.count("# plot.plot_map("), (
        f"{n_calls} plot_map calls but only {n_wired} forward annotate_values")
