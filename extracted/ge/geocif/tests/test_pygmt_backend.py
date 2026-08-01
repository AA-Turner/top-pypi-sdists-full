"""PyGMT map backend: in-process rendering via the pixi-managed GMT.

Three layers, so the suite is useful with or without GMT installed:

1. Call-contract regression (no GMT needed): the in-process path must hand
   ``render()`` the params DICT. Until pixi added gmt to the env this path
   was unreachable, hiding a bug where the params JSON *path* was passed
   instead (``AttributeError: 'str' object has no attribute 'get'``).
2. Renderer hygiene (no GMT needed): the subprocess-bridge helper must stay
   importable in a bare pygmt env (no geocif imports), and must not embed
   shell-style quotes in GMT frame/label strings (they render literally).
3. End-to-end (skipped unless GMT loads in-process): a real two-region
   choropleth renders to a non-trivial PNG.
"""

import ast
from pathlib import Path

import pytest

VIZ_DIR = Path(__file__).resolve().parents[1] / "geocif" / "viz"
RENDERER = VIZ_DIR / "_pygmt_render.py"


def _make_test_frames():
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import box

    attribute_df = gpd.GeoDataFrame(
        {
            "Country Region": ["aa r1", "aa r2"],
            "geometry": [box(30, -20, 31, -19), box(31, -20, 32, -19)],
        },
        crs="EPSG:4326",
    )
    df = pd.DataFrame({"Country Region": ["aa r1", "aa r2"], "yield": [1.0, 2.0]})
    return attribute_df, df


def _call_pygmt_path(tmp_path, fname="m.png"):
    from geocif.viz import plot as vplot

    attribute_df, df = _make_test_frames()
    vplot._plot_map_pygmt(
        attribute_df, df, None, "Country Region", None, "yield",
        str(tmp_path), fname, "title", "t/ha", 1.0, 2.0,
        vplot._resolve_cmap(None, "sequential", 2.0), "sequential",
        True, False, "ADM1_NAME", True, "region", False, False,
    )


def test_in_process_render_receives_params_dict(tmp_path, monkeypatch):
    """Regression: the in-process call must pass the params dict, not the
    JSON file path (latent until an env could load GMT in-process)."""
    from geocif.viz import plot as vplot
    from geocif.viz import _pygmt_render

    captured = {}

    def fake_render(geojson_path, params):
        captured["geojson"] = geojson_path
        captured["params"] = params

    monkeypatch.setattr(_pygmt_render, "render", fake_render)
    monkeypatch.setattr(vplot, "_gmt_available", lambda: True)

    _call_pygmt_path(tmp_path)

    assert isinstance(captured["params"], dict), (
        "in-process path passed %r instead of the params dict"
        % type(captured.get("params"))
    )
    assert captured["params"]["out_path"].endswith("m.png")
    assert Path(captured["geojson"]).suffix == ".geojson"


def test_renderer_is_self_contained():
    """The bridge helper runs in a bare pygmt env: no geocif imports."""
    tree = ast.parse(RENDERER.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert "geocif" not in imported, "renderer must not import geocif"
    assert imported <= {"os", "sys", "json", "tempfile", "geopandas", "pygmt"}


def test_renderer_has_no_embedded_quotes():
    """Regression: shell-style quotes inside GMT frame/label strings render
    literally through the pygmt API ("my title" instead of my title)."""
    src = RENDERER.read_text(encoding="utf-8")
    for bad in ('+t"', '+L"', '+l"'):
        assert bad not in src, f"embedded quote in GMT arg: {bad}..."


def _gmt_loadable():
    try:
        from geocif.viz.plot import _gmt_available
        return _gmt_available()
    except Exception:
        return False


@pytest.mark.skipif(not _gmt_loadable(), reason="GMT not loadable in-process")
def test_in_process_render_end_to_end(tmp_path):
    """Full prep + in-process GMT render of a two-region choropleth."""
    _call_pygmt_path(tmp_path, fname="e2e.png")
    out = tmp_path / "e2e.png"
    assert out.exists()
    assert out.stat().st_size > 20_000
