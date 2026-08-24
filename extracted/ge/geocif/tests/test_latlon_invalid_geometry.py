"""Regression test: one invalid boundary polygon must not kill the whole run.

_add_lat_lon_to_data reprojects every region to EPSG:6933 to compute centroids.
GEOS aborts the ENTIRE to_crs on a single malformed ring
("Points of LinearRing do not form a closed linestring"), which crashed the
usa_admin2 full-10-state county run at geocif.py:_add_lat_lon_to_data while the
3-state subset (no bad county) passed. Geometries must be repaired first.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "geocif"


def test_invalid_geometry_repaired_before_reprojection():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("def _add_lat_lon_to_data")
    body = src[i:i + 4000]
    # repair happens before the reprojection
    assert "is_valid" in body, "must detect invalid geometries"
    assert "make_valid" in body, "must repair invalid geometries"
    assert body.index("make_valid") < body.index("to_crs(epsg=6933)"), \
        "repair must precede reprojection"
    # older shapely fallback
    assert "buffer(0)" in body, "needs a shapely<2.1 fallback"


def test_centroid_reprojection_has_per_geometry_fallback():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("def _add_lat_lon_to_data")
    body = src[i:i + 4000]
    assert "per-geometry centroids" in body, \
        "a wholesale to_crs failure must degrade per-geometry, not kill the run"
    assert "centroid reprojection failed wholesale" in body


def test_geometry_repair_is_warned():
    """Silent repair would hide a corrupt boundary file."""
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("def _add_lat_lon_to_data")
    body = src[i:i + 4000]
    assert "repairing" in body and "invalid" in body
