#!/usr/bin/env python
"""What scatter's map background costs, per map, in one process.

Draws N global maps in a row with the background scatter uses (ocean,
land, coastline and borders from Natural Earth at 50m), saves each and
closes it, and reports the time per map and how the memory of the process
grows. Three versions:

    A  as scatter draws it
    B  without the ocean polygon: the axes painted the colour of the sea
    C  B with every layer at 110m

    python pikobs/build_doc/scatter_background_timing.py [N]
"""
import gc
import os
import sys
import tempfile
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import psutil
import cartopy
import cartopy.crs as ccrs


def background(ax, res, ocean_polygon):
    if ocean_polygon:
        ax.add_feature(cartopy.feature.NaturalEarthFeature(
            'physical', 'ocean', res, edgecolor='#9aa5aa', facecolor='#e7f2f5'),
            zorder=0)
    else:
        ax.set_facecolor('#e7f2f5')
    ax.add_feature(cartopy.feature.NaturalEarthFeature(
        'physical', 'land', res, edgecolor='#c8c8c8', facecolor='#f4f3f0'), zorder=1)
    ax.add_feature(cartopy.feature.NaturalEarthFeature(
        'physical', 'coastline', res, edgecolor='#4a4a4a', facecolor='none',
        linewidth=0.7), zorder=10)
    ax.add_feature(cartopy.feature.NaturalEarthFeature(
        'cultural', 'admin_0_boundary_lines_land', res, edgecolor='#777777',
        facecolor='none', linewidth=0.4), zorder=10)


def run(label, res, ocean_polygon, n, out):
    proc = psutil.Process()
    rng = np.random.default_rng(0)
    times, rss = [], [proc.memory_info().rss]
    for i in range(n):
        t = time.time()
        fig = plt.figure(figsize=(12, 6.5))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()
        background(ax, res, ocean_polygon)
        lon, lat = rng.uniform(-180, 180, 5000), rng.uniform(-90, 90, 5000)
        ax.scatter(lon, lat, c=rng.normal(size=5000), s=4, transform=ccrs.PlateCarree(),
                   zorder=5)
        fig.savefig(os.path.join(out, f"{label}_{i}.png"), dpi=100)
        plt.close("all")
        gc.collect()
        times.append(time.time() - t)
        rss.append(proc.memory_info().rss)
    first = times[0]
    rest = sum(times[1:]) / max(1, len(times) - 1)
    print(f"  {label}  first map {first:5.2f} s, then {rest:5.2f} s per map;  "
          f"memory {rss[0] / 1e9:.2f} -> {rss[1] / 1e9:.2f} after one -> "
          f"{rss[-1] / 1e9:.2f} GB after {n}")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    out = tempfile.mkdtemp()
    print(f"{n} global maps each, cartopy {cartopy.__version__}, matplotlib "
          f"{matplotlib.__version__}")
    for label, res, ocean in (("A", "50m", True), ("B", "50m", False), ("C", "110m", False)):
        run(label, res, ocean, n, out)
    print(f"\nthe maps are in {out}: compare A_1.png and B_1.png by eye")


if __name__ == "__main__":
    main()
