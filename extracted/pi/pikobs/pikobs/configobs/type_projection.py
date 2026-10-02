"""
===========
Projections
===========

The maps :doc:`scatter` can draw, one per value of ``PROJECTION`` in its
wrappers. Case does not matter -- ``OrthoN`` and ``orthon`` are the same --
and several values give one series of maps each: ``PROJECTION=(cyl OrthoN)``.

**Used by:** :doc:`scatter`, the only module with a ``PROJECTION`` setting.
:doc:`mapobs` draws maps too, but takes the projection from the region it
shows; the other modules draw sections, profiles and time series.

.. list-table::
   :widths: 20 50 30
   :header-rows: 1

   * - ``PROJECTION``
     - What it shows
     - Cartopy projection
   * - ``cyl``
     - Global Cylindrical Equidistant
     - PlateCarree
   * - ``orthon``
     - Orthographic North Pole
     - Orthographic
   * - ``orthos``
     - Orthographic South Pole
     - Orthographic
   * - ``robinson``
     - Global Robinson Projection
     - Robinson
   * - ``europe``
     - North Polar Stereographic focused on Europe
     - NorthPolarStereo
   * - ``canada``
     - North Polar Stereographic focused on Canada
     - NorthPolarStereo
   * - ``ameriquenord``
     - North Polar Stereographic focused on North America
     - NorthPolarStereo
   * - ``npolar``
     - Northern Hemisphere
     - NorthPolarStereo
   * - ``spolar``
     - Southern Hemisphere
     - SouthPolarStereo
   * - ``hrdps``
     - High-Resolution Deterministic Prediction System domain
     - RotatedPole
   * - ``reg``
     - Custom Regional Rotated Pole domain
     - RotatedPole

What they look like
-------------------

Each projection on its own, set up the way scatter sets it up, with the
land in grey as on the maps of the regions: `every projection, side by
side <_static/projections/projections.html>`__.

Another projection
------------------

A projection you need is not here? Open an issue with its name and the
area it should show: `Pikobs issues <https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`__.
"""

import cartopy.crs as ccrs
import pylab as plt
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def type_projection(Proj):   
    """Figure and Cartopy axes for one projection; the list is in the module docstring."""

    Proj = Proj.lower()
    pc = ccrs.PlateCarree()
    
    if Proj == 'cyl':
        PROJ = ccrs.PlateCarree()
        fig = plt.figure(figsize=(14,7))
        ax = plt.axes(projection=PROJ)
        
        ax.set_extent([-180, 180, -90, 90], crs=PROJ)
        LATPOS = [-90,-60,-30,00,30,60,90]
        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)

    elif Proj == 'orthon':
        PROJ = ccrs.Orthographic(central_latitude=90.0, central_longitude=-80.0)
        fig = plt.figure(figsize=(14,14))
        ax = plt.axes(projection=PROJ)
        
        ax.set_global()
        ax.coastlines(resolution='110m')
        
        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)

    elif Proj == 'orthos':
        PROJ = ccrs.Orthographic(central_latitude=-90.0, central_longitude=-80.0)
        fig = plt.figure(figsize=(14,14))
        ax = plt.axes(projection=PROJ)
        
        ax.set_global()
        ax.coastlines(resolution='110m')
        
        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)

    elif Proj == 'robinson':
        PROJ = ccrs.Robinson()
        fig = plt.figure(figsize=(15,7))
        ax = plt.subplot(1, 1, 1, projection=PROJ)
        
        ax.set_extent([-180, 180, -90, 90], pc)
        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)

    elif Proj == 'europe':
        PROJ = ccrs.NorthPolarStereo()
        fig = plt.figure(figsize=[14, 14])
        ax = plt.subplot(1, 1, 1, projection=PROJ)
        
        ax.set_extent([-20, 50, 30, 90], crs=ccrs.PlateCarree()) 
        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)
        
    elif Proj == 'canada':
        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)
        PROJ = ccrs.NorthPolarStereo(central_longitude=-105.0)
        fig = plt.figure(figsize=[14, 14])
        ax = plt.subplot(1, 1, 1, projection=PROJ)
        
        # Ajusta el set_extent para la proyección polar
        ax.set_extent([-150, -53, 42, 90], crs=ccrs.PlateCarree())

    elif Proj == 'ameriquenord':
        PROJ = ccrs.NorthPolarStereo(central_longitude=-105.0)
        fig = plt.figure(figsize=[14, 7])
        ax = plt.subplot(1, 1, 1, projection=PROJ)
        
        ax.set_extent([-140,  -40, 20, 90], pc)
        ax.set_extent([-170,  -40, 20, 90], pc)
        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)
        
    elif Proj == 'npolar':
        PROJ = ccrs.NorthPolarStereo(central_longitude=-90.5)
        fig = plt.figure(figsize=[13, 7])
        ax = plt.subplot(1, 1, 1, projection=PROJ)
        
        ax.set_extent([-180, 180, 00, 90], pc)
        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)
        ax.coastlines(resolution='110m')

    elif Proj == 'spolar':
        PROJ = ccrs.SouthPolarStereo(central_longitude=-86)
        fig = plt.figure(figsize=[14, 14])
        ax = plt.subplot(1, 1, 1, projection=PROJ)
        
        ax.set_extent([-180, 180, -90, 00], pc)
        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)

    elif Proj == 'hrdps':
        pole_latitude = 35.7
        pole_longitude = 65.5

        PROJ = ccrs.RotatedPole(pole_latitude=pole_latitude, pole_longitude=pole_longitude)
        fig = plt.figure(figsize=[14, 7])
        ax = plt.subplot(1, 1, 1, projection=PROJ)
        
        lat_0 = 48.8
        delta_lat = 10.
        lon_0 = 266.00
        delta_lon = 40.
        ax.set_extent([lon_0 - delta_lon, lon_0 + delta_lon, lat_0 - delta_lat, lat_0 + delta_lat], pc)

        LATPOS = [-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
        LATPOS = range(-90, 91, 10)

    elif Proj == 'reg':
        Size_mapx = 10
        Size_mapy = 10
        pole_latitude = 31.758
        pole_longitude = 178.008 - 90.
        llcrnrlat = -7.74911
        llcrnrlon = -128.80635
        urcrnrlat = 57.88194
        urcrnrlon = 39.378404
        central_rotated_longitude = -90. - 1.991605
        
        PROJ = ccrs.RotatedPole(pole_longitude=pole_longitude, pole_latitude=pole_latitude,
                                central_rotated_longitude=central_rotated_longitude)
        fig = plt.figure(1, figsize=(Size_mapx, Size_mapy))
        ax = fig.add_subplot(1, 1, 1, projection=PROJ)
        
        mapExtent = [llcrnrlon, urcrnrlon, llcrnrlat, urcrnrlat]
        ax.set_extent(mapExtent)
        xs, ys, zs = PROJ.transform_points(pc,
                                           np.array([llcrnrlon, urcrnrlon]),
                                           np.array([llcrnrlat, urcrnrlat])).T
        
        ax.set_xlim(xs)
        ax.set_ylim(ys)
        LATPOS = [-60,-30,00,10.,20.,30.,40.,50.,60.,70.,80.,90.]
  
    # Global gridlines configuration
    gl = ax.gridlines(draw_labels=True, linewidth=0.7, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False              
    gl.right_labels = False            
    
    # Text styles
    gl.xlabel_style = {'size': 12}
    gl.ylabel_style = {'size': 12}
    gl.xformatter = LongitudeFormatter()
    gl.yformatter = LatitudeFormatter()
    
    # Grid intervals
    gl.xlocator = plt.FixedLocator(np.arange(-180, 181, 30))
    gl.ylocator = plt.FixedLocator(np.arange(-90, 91, 30))
    
    return ax, fig, LATPOS, PROJ, pc

def get_rectangular_extent(proj_name):
    """
    Devuelve siempre la proyección PlateCarree (plana) y los límites EXACTOS
    (lon_min, lon_max, lat_min, lat_max) para que los histogramas marginales
    y los cross-sections se alineen perfectamente con el mapa.
    """
    proj = ccrs.PlateCarree()
    name = proj_name.lower()
    
    if "npolar" in name:
        return proj, [-180, 180, 50, 90]
    elif "spolar" in name:
        return proj, [-180, 180, -90, -50]
    elif "ameriquenord" in name or "canada" in name:
        return proj, [-150, -40, 30, 85]
    elif "europe" in name:
        return proj, [-25, 45, 30, 75]
    else:
        # Por defecto (cyl, global, etc.)
        return proj, [-180, 180, -90, 90]    


# ─────────────────────────────────────────────────────────────────────────────
# The gallery: every projection drawn the way the regions are
# ─────────────────────────────────────────────────────────────────────────────

def _projection_rows():
    """(name, what it shows, Cartopy projection), read from the table of the
    module docstring, so the gallery and the page never disagree."""
    import re as _re
    rows = _re.findall(r"\* - ``(\w+)``\n\s+- ([^\n]+)\n\s+- ([^\n]+)",
                       __doc__ or "")
    return [r for r in rows if r[0] != "PROJECTION"]


def plot_projection(name, what, crs, out_dir, pathwork=None):
    """One projection, in the style of the region maps; returns the file.

    The axes are made by type_projection() itself, so the picture is the
    projection scatter uses. The land is the grey of the land mask, as on
    the maps of the regions: nothing to download.
    """
    import os
    import matplotlib as mpl
    mpl.use("Agg")
    import matplotlib.pyplot as _plt
    from pikobs.configobs import regionsobs

    ax, fig = type_projection(name)[:2]
    fig.set_facecolor("white")
    land = regionsobs._land_for((-90.0, 90.0, -180.0, 180.0), pathwork or out_dir)
    if land is not None:
        ax.imshow(land[0], origin="lower", cmap="Greys", vmin=0, vmax=3,
                  extent=land[1], interpolation="nearest", zorder=0,
                  transform=ccrs.PlateCarree())
    try:
        ax.gridlines(linestyle="--", linewidth=0.6, alpha=0.3)
    except Exception:
        pass
    ax.set_title(f"{name}   ({crs})\n{what}", fontsize=11)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"projection_{name}.png")
    fig.savefig(out, dpi=110, bbox_inches="tight")
    _plt.close(fig)
    return out


def plot_projections(out_dir, pathwork=None):
    """Every projection, and projections.html -- the template of regions.html."""
    import os
    written, names = [], []
    for name, what, crs in _projection_rows():
        try:
            written.append(plot_projection(name, what, crs, out_dir, pathwork))
            names.append(f"{name} -- {what}")
        except Exception as exc:                      # pragma: no cover
            print(f"[projections] {name}: {exc}")
    if written:
        cards = "".join(
            f"<figure style='margin:0'><a href='{os.path.basename(f)}'>"
            f"<img src='{os.path.basename(f)}' style='width:100%'></a>"
            f"<figcaption style='text-align:center;font-family:sans-serif;"
            f"font-size:13px'>{n}</figcaption></figure>"
            for n, f in zip(names, written))
        html = (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                f"<title>pikobs projections</title></head><body>"
                f"<h1 style='font-family:sans-serif'>Projections of pikobs "
                f"({len(written)})</h1>"
                f"<div style='display:grid;grid-template-columns:"
                f"repeat(auto-fill,minmax(360px,1fr));gap:14px'>{cards}"
                f"</div></body></html>")
        with open(os.path.join(out_dir, "projections.html"), "w") as fh:
            fh.write(html)
    return written


if __name__ == "__main__":
    import sys as _sys
    for _f in plot_projections(_sys.argv[1] if len(_sys.argv) > 1 else "projections"):
        print(_f)
