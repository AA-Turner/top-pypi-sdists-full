"""Figure conventions for the crop-calendar validation.

These assert the contract the house style sets, not the pixels: charts land in
``plots/``, choropleths in ``maps/``, every figure has a companion CSV in a
mirrored ``csvs/`` tree, and ``lookup_plots_csvs.csv`` ties them together. A
figure without its data is the thing this guards against -- it is how a plotted
number stops being checkable.

Map rendering needs the GMT C library, which is not present everywhere, so the
map assertions are on the CSV and the graceful-degradation path rather than on a
PNG existing.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif.cropcal import plots


# --------------------------------------------------------------------------
# Naming
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "slug,expected",
    [
        ("winter_wheat", "Winter Wheat"),
        ("spring_wheat", "Spring Wheat"),
        ("maize", "Maize"),
        ("midgreenup", "Mid Greenup"),
        ("midgreendown", "Mid Greendown"),
        ("admin_1", "Admin 1"),
    ],
)
def test_canvas_names_are_title_case_never_slugs(slug, expected):
    assert plots.display(slug) == expected


def test_every_scored_crop_has_a_display_name():
    """A crop reaching the canvas as `winter_wheat` is a style bug."""
    from geocif.cropcal import naming

    for crop in naming.CROP_PARAMS:
        assert plots.display(crop)[0].isupper()
        assert "_" not in plots.display(crop)


# --------------------------------------------------------------------------
# Output tree
# --------------------------------------------------------------------------
def test_figure_set_mirrors_plots_into_csvs(tmp_path):
    figures = plots.FigureSet(tmp_path)
    frame = pd.DataFrame({"a": [1, 2, 3]})
    figures.record("plots", "diagnostic_x", frame)
    figures.record("maps", "delta_midgreenup_world", frame)
    lookup = figures.write_lookup()

    assert (tmp_path / "csvs" / "plots" / "diagnostic_x.csv").is_file()
    assert (tmp_path / "csvs" / "maps" / "delta_midgreenup_world.csv").is_file()
    assert lookup is not None and lookup.name == "lookup_plots_csvs.csv"

    rows = pd.read_csv(lookup)
    assert set(rows["plot"]) == {"plots/diagnostic_x.png", "maps/delta_midgreenup_world.png"}
    for _, row in rows.iterrows():
        assert (tmp_path / row["csv"]).is_file()


def _scored_frame(n=12):
    rng = np.random.default_rng(0)
    crops = ["maize", "winter_wheat", "rice"]
    return pd.DataFrame(
        {
            "key": [f"Region{i} Country{i % 3}" for i in range(n)],
            "country": [f"Country{i % 3}" for i in range(n)],
            "region": [f"region{i}" for i in range(n)],
            "crop": [crops[i % 3] for i in range(n)],
            "season": 1,
            "cm_group": ["AMIS", "EW"] * (n // 2),
            "combined_delta": rng.uniform(0, 90, n),
            "delta_midgreenup_signed": rng.uniform(-60, 60, n),
            "delta_midgreendown_signed": rng.uniform(-60, 60, n),
        }
    )


def _summary_frame():
    return pd.DataFrame(
        {
            "crop": ["All", "maize", "winter_wheat", "rice"],
            "pct_works": [60.0, 58.0, 52.0, 55.0],
            "pct_works_subset": [70.0, 73.0, 50.0, 67.0],
        }
    )


def test_charts_render_with_companions(tmp_path):
    made = plots.render_all(
        tmp_path,
        _scored_frame(),
        diagnostics=[],
        summary=_summary_frame(),
        boundary_file=None,
    )
    assert made["plots"] == 2                      # agreement bar + distribution

    for stem in ("agreement_crop", "difference_distribution_crop"):
        assert (tmp_path / "plots" / f"{stem}.png").is_file()
        assert (tmp_path / "csvs" / "plots" / f"{stem}.csv").is_file()

    lookup = pd.read_csv(tmp_path / "lookup_plots_csvs.csv")
    assert len(lookup) >= 2


def test_map_csv_is_written_even_without_a_boundary_file(tmp_path):
    """A missing map must never cost the numbers behind it."""
    plots.render_all(
        tmp_path, _scored_frame(), diagnostics=[],
        summary=_summary_frame(), boundary_file=None,
    )
    world = tmp_path / "csvs" / "maps" / "delta_midgreenup_world.csv"
    assert world.is_file()
    table = pd.read_csv(world)
    assert {"key", "value"} <= set(table.columns)
    assert not (tmp_path / "maps" / "delta_midgreenup_world.png").exists()


def test_filenames_lead_with_the_figure_type(tmp_path):
    """House rule: `{type}_{identifiers}_{qualifier}`, no `_by_` infixes."""
    plots.render_all(
        tmp_path, _scored_frame(), diagnostics=[],
        summary=_summary_frame(), boundary_file=None,
    )
    names = [p.name for p in (tmp_path / "plots").glob("*.png")]
    names += [p.stem for p in (tmp_path / "csvs" / "maps").glob("*.csv")]
    assert names, "nothing rendered"
    for name in names:
        assert not name.startswith("_")
        assert "_by_" not in name and "_all_" not in name and "_with_" not in name
    assert any(n.startswith("agreement_") for n in names)
    assert any(n.startswith("delta_") for n in names)


def test_maps_use_the_signed_difference_not_the_legacy_delta(tmp_path):
    """The legacy column's wrap branch forces half the rows positive.

    Mapping its mean would read as a bias that is partly an artefact of the
    formula, so only the signed column is mapped.
    """
    import inspect

    source = inspect.getsource(plots.render_all)
    assert "delta_midgreenup_signed" in source
    assert '"delta_midgreenup"' not in source


# --------------------------------------------------------------------------
# Shared map code
# --------------------------------------------------------------------------
def test_world_extent_does_not_exceed_the_globe():
    """Regression: a global extent plus 5% padding is 396 degrees.

    GMT rejects a region wider than 360 with "Map region exceeds 360 degrees",
    and plot_map catches that and silently falls back to matplotlib -- so every
    world map in geocif was drawn by the fallback backend while the logs showed
    nothing unless logging happened to be configured. The padded bounds are now
    clamped to the globe.
    """
    import inspect

    from geocif.viz import plot as viz_plot

    source = inspect.getsource(viz_plot._plot_map_pygmt)
    assert 'max(minx - padx, -180.0)' in source
    assert 'min(maxx + padx, 180.0)' in source
    assert '"region": [west, east, south, north]' in source

    # And the arithmetic itself, on a genuinely global frame.
    minx, miny, maxx, maxy = -180.0, -55.98, 180.0, 83.11
    padx = max(0.5, (maxx - minx) * 0.05)
    pady = max(0.5, (maxy - miny) * 0.05)
    west, east = max(minx - padx, -180.0), min(maxx + padx, 180.0)
    south, north = max(miny - pady, -90.0), min(maxy + pady, 90.0)
    assert east - west <= 360.0
    assert north - south <= 180.0


def test_distribution_panels_share_an_axis():
    """Equal box widths must mean equal day spans across the two transitions."""
    import inspect

    assert "sharex=True" in inspect.getsource(plots.difference_distribution)
