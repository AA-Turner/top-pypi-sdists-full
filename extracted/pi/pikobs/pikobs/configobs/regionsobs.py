# GENERATED -- this docstring is written by pikobs/build_doc/build_regions.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""================================================
pikobs.configobs.regionsobs -- Where to look
================================================

Every module of pikobs asks the same question of every observation:
is it in the region I was asked about? For us, regions come in two
kinds: the classic ARCAD domains, boxes of latitude and longitude that
pikobs has always carried, and the EMET domains, polygons -- the grid of
a model, a climate area. Both are used the same way, and nothing outside
this file needs to know which kind a region is.

The ARCAD domains
=================

+-----------------------------+------------+---------------+
| Region                      | Latitude   | Longitude     |
+=============================+============+===============+
| ``PoleNord``                | 60 to 90   | -180 to 180   |
+-----------------------------+------------+---------------+
| ``PoleSud``                 | -90 to -60 | -180 to 180   |
+-----------------------------+------------+---------------+
| ``AmeriqueduNord``          | 25 to 60   | -145 to -50   |
+-----------------------------+------------+---------------+
| ``OuestAmeriqueduNord``     | 25 to 60   | -145 to -97.5 |
+-----------------------------+------------+---------------+
| ``AmeriqueDuNordPlus``      | 25 to 85   | -170 to -40   |
+-----------------------------+------------+---------------+
| ``Monde``                   | -90 to 90  | -180 to 180   |
+-----------------------------+------------+---------------+
| ``Global``                  | -90 to 90  | -180 to 180   |
+-----------------------------+------------+---------------+
| ``ExtratropiquesNord``      | 20 to 90   | -180 to 180   |
+-----------------------------+------------+---------------+
| ``ExtratropiquesSud``       | -90 to -20 | -180 to 180   |
+-----------------------------+------------+---------------+
| ``HemisphereNord``          | 0 to 90    | -180 to 180   |
+-----------------------------+------------+---------------+
| ``HemisphereSud``           | -90 to 0   | -180 to 180   |
+-----------------------------+------------+---------------+
| ``Asie``                    | 25 to 60   | 65 to 145     |
+-----------------------------+------------+---------------+
| ``Europe``                  | 25 to 70   | -10 to 28     |
+-----------------------------+------------+---------------+
| ``Mexique``                 | 15 to 30   | -130 to -60   |
+-----------------------------+------------+---------------+
| ``Canada``                  | 45 to 90   | -151 to -50   |
+-----------------------------+------------+---------------+
| ``BaieDhudson``             | 55 to 90   | -90 to -60    |
+-----------------------------+------------+---------------+
| ``Arctiquecanadien``        | 58 to 90   | -141 to -50   |
+-----------------------------+------------+---------------+
| ``EtatsUnis``               | 25 to 45   | -130 to -70   |
+-----------------------------+------------+---------------+
| ``SudestEtatsUnis``         | 25 to 40   | -100 to -70   |
+-----------------------------+------------+---------------+
| ``EstAmeriqueduNord``       | 25 to 60   | -97.5 to -50  |
+-----------------------------+------------+---------------+
| ``EstAmeriqueduNordPlus``   | 25 to 85   | -97.5 to -50  |
+-----------------------------+------------+---------------+
| ``OuestAmeriqueduNordPlus`` | 25 to 85   | -170 to -97.5 |
+-----------------------------+------------+---------------+
| ``Tropiques30``             | -30 to 30  | -180 to 180   |
+-----------------------------+------------+---------------+
| ``Tropiques``               | -20 to 20  | -180 to 180   |
+-----------------------------+------------+---------------+
| ``Australie``               | -55 to -10 | 90 to 180     |
+-----------------------------+------------+---------------+
| ``Pacifique``               | 20 to 65   | 130 to -150   |
+-----------------------------+------------+---------------+
| ``Atlantique``              | 20 to 65   | -80 to -1     |
+-----------------------------+------------+---------------+
| ``Alaska``                  | 50 to 75   | -180 to -140  |
+-----------------------------+------------+---------------+
| ``HIMAPEst``                | 35 to 65   | -105 to -50   |
+-----------------------------+------------+---------------+
| ``HIMAPOuest``              | 40 to 65   | -135 to -90   |
+-----------------------------+------------+---------------+
| ``ExtremeSud``              | -90 to -87 | -180 to 180   |
+-----------------------------+------------+---------------+
| ``ExtremeNord``             | 87 to 90   | -180 to 180   |
+-----------------------------+------------+---------------+
| ``TropiquesOuest``          | -20 to 0   | 180 to -90    |
+-----------------------------+------------+---------------+
| ``Bande60a90``              | 60 to 90   | -180 to 180   |
+-----------------------------+------------+---------------+
| ``Bande30a60``              | 30 to 60   | -180 to 180   |
+-----------------------------+------------+---------------+
| ``Bande00a30``              | 0 to 30    | -180 to 180   |
+-----------------------------+------------+---------------+
| ``BandeM30a00``             | -30 to 0   | -180 to 180   |
+-----------------------------+------------+---------------+
| ``BandeM60aM30``            | -60 to -30 | -180 to 180   |
+-----------------------------+------------+---------------+
| ``BandeM90aM60``            | -90 to -60 | -180 to 180   |
+-----------------------------+------------+---------------+
| ``Rapidscat``               | -55 to 55  | -180 to 180   |
+-----------------------------+------------+---------------+
| ``npstere``                 | 0 to 90    | -180 to 180   |
+-----------------------------+------------+---------------+
| ``spstere``                 | -90 to 0   | -180 to 180   |
+-----------------------------+------------+---------------+

They are read from this file itself, so a region added to ``regions()``
appears here, in ``list_regions()`` and in the maps without being
written down twice.

A box that crosses the date line is written the way it reads:
``Pacifique`` goes from 130 to -150.

The EMET domains
================

No polygon is in ``configobs/regions_data`` yet; see the section above to bring some in.

They live in ``configobs/regions_data`` as ``.npz`` files, a few tens of
kB each. Bring a collection in once from its shapefiles:

.. code-block:: bash

   python pikobs/configobs/import_regions.py /path/to/shapefiles/emet_domains --name emet
   python pikobs/configobs/import_regions.py --list

From then on the names are used like any other region:

.. code-block:: bash

   REGION=(Monde Canada hrdps Boreal_CLIM Great_Lakes_CLIM)

The importer simplifies a border with Douglas-Peucker, 0.02 degrees by
default: the grid of the HRDPS has 40 000 vertices and 126 of them draw
the same shape at the resolution anything here works at. ``--simplify 0``
keeps every point.

Seeing them
===========

A name in a list says little; the shape says everything. One command
draws every region pikobs knows, boxes and polygons, and writes an index
page with all of them:

.. code-block:: bash

   python pikobs/configobs/import_regions.py --plot $HOME/sites8/pikobs_regions

A box is drawn on the whole globe, plain cylindrical, because four
numbers mean little without the world around them and half of them are
bands that cross it:

.. image:: _static/region_box.png
   :alt: A box region on the globe
   :align: center
   :width: 100%


A polygon gets a window of its own, since its shape is the point, with
the number of vertices in the title:

.. image:: _static/region_polygon.png
   :alt: A polygon region, zoomed
   :align: center
   :width: 100%


The land comes from the mask pikobs already uses for the land / ocean
split, so this needs nothing else installed. All of them on one page:
`every region, side by side <_static/regions/regions.html>`__.

Pass names to draw only those:

.. code-block:: bash

   python pikobs/configobs/import_regions.py --plot /tmp/maps hrdps Boreal_CLIM Canada

How a region becomes a query
============================

+----------------------------------+----------------------------------------------------------------------+
| What you want                    | What to write                                                        |
+==================================+======================================================================+
| the condition of a region in SQL | ``regionsobs.criteria(name, pathwork)``                              |
+----------------------------------+----------------------------------------------------------------------+
| a polygon usable from SQLite     | ``regionsobs.register(conn, regions, pathwork)`` once per connection |
+----------------------------------+----------------------------------------------------------------------+
| is this one a polygon?           | ``regionsobs.is_polygon(name)``                                      |
+----------------------------------+----------------------------------------------------------------------+
| every region there is            | ``regionsobs.list_regions()``                                        |
+----------------------------------+----------------------------------------------------------------------+
| the four numbers of a box        | ``regions(name)``, as always                                         |
+----------------------------------+----------------------------------------------------------------------+

A box gives what it always gave:

.. code-block:: sql

   AND lat BETWEEN 45 AND 90 AND lon BETWEEN -151 AND -50

A polygon would be far too slow tested point by point -- tens of millions
of Python calls per file -- so it is rasterised once to a 0.1-degree grid
(about 11 km, finer than any thinning), cached in ``PATHWORK`` and
memory-mapped by every worker, the way the land mask is. The box that
contains it goes in front, and throws away most of the globe before the
mask is ever consulted:

.. code-block:: sql

   AND lat BETWEEN 39.0 AND 58.7 AND lon BETWEEN -142.0 AND -50.4
   AND in_region_sql_hrdps(lat, lon) = 1

Measured on a million rows: the box alone 0.04 s, the box with the mask
0.06 s, the mask without the box 0.55 s. The box in front is what makes
an irregular region cost nothing.

Adding a region to a module
===========================

Two lines, wherever the module builds its selections:

.. code-block:: python

   from pikobs.configobs import regionsobs

   regionsobs.register(conn, regions, pathwork)     # once per connection
   cond = regionsobs.criteria(region, pathwork)     # box or polygon

.. warning::

   A region selects on the position in the header. For families where
   that position is the instrument and not the observation -- radar,
   where the header holds the antenna -- a region selects radars, not
   beams.

Another region
==============

A region you need is not here? Open an issue with its name and its
limits -- four numbers for an ARCAD box, a shapefile for an EMET
domain: `Pikobs issues <https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`__.
"""

def regions(region):
    """
    Available Regions and Boundaries
    ================================

    The following geographic regions and their bounding boxes are available for analysis. 
    Latitudes (LAT) range from South (-90) to North (90), and Longitudes (LON) range from West (-180) to East (180).

    .. list-table:: Supported Geographic Regions
       :widths: 25 35 20 20
       :header-rows: 1
       :align: center

       * - Region Argument
         - Description
         - Latitude Range
         - Longitude Range

       * - ``PoleNord``
         - Northern polar region
         - 60 to 90
         - -180 to 180
       * - ``PoleSud``
         - Southern polar region
         - -90 to -60
         - -180 to 180
       * - ``AmeriqueduNord``
         - North America
         - 25 to 60
         - -145 to -50
       * - ``OuestAmeriqueduNord``
         - Western North America
         - 25 to 60
         - -145 to -97.5
       * - ``AmeriqueDuNordPlus``
         - Extended North America
         - 25 to 85
         - -170 to -40
       * - ``Monde`` / ``Global``
         - Global World
         - -90 to 90
         - -180 to 180
       * - ``ExtratropiquesNord``
         - Northern Extratropics
         - 20 to 90
         - -180 to 180
       * - ``ExtratropiquesSud``
         - Southern Extratropics
         - -90 to -20
         - -180 to 180
       * - ``HemisphereNord``
         - Northern Hemisphere
         - 0 to 90
         - -180 to 180
       * - ``HemisphereSud``
         - Southern Hemisphere
         - -90 to 0
         - -180 to 180
       * - ``Asie``
         - Asia
         - 25 to 60
         - 65 to 145
       * - ``Europe``
         - Europe
         - 25 to 70
         - -10 to 28
       * - ``Mexique``
         - Mexico
         - 15 to 30
         - -130 to -60
       * - ``Canada``
         - Canada
         - 45 to 90
         - -151 to -50
       * - ``BaieDhudson``
         - Hudson Bay
         - 55 to 90
         - -90 to -60
       * - ``Arctiquecanadien``
         - Canadian Arctic
         - 58 to 90
         - -141 to -50
       * - ``EtatsUnis``
         - United States
         - 25 to 45
         - -130 to -70
       * - ``SudestEtatsUnis``
         - Southeastern United States
         - 25 to 40
         - -100 to -70
       * - ``EstAmeriqueduNord``
         - Eastern North America
         - 25 to 60
         - -97.5 to -50
       * - ``EstAmeriqueduNordPlus``
         - Extended Eastern North America
         - 25 to 85
         - -97.5 to -50
       * - ``OuestAmeriqueduNordPlus``
         - Extended Western North America
         - 25 to 85
         - -170 to -97.5
       * - ``Tropiques30``
         - Tropics 30
         - -30 to 30
         - -180 to 180
       * - ``Tropiques``
         - Tropics
         - -20 to 20
         - -180 to 180
       * - ``Australie``
         - Australia
         - -55 to -10
         - 90 to 180
       * - ``Pacifique``
         - Pacific
         - 20 to 65
         - 130 to -150
       * - ``Atlantique``
         - Atlantic
         - 20 to 65
         - -80 to -1
       * - ``Alaska``
         - Alaska
         - 50 to 75
         - -180 to -140
       * - ``HIMAPEst``
         - HIMAP East
         - 35 to 65
         - -105 to -50
       * - ``HIMAPOuest``
         - HIMAP West
         - 40 to 65
         - -135 to -90
       * - ``ExtremeSud``
         - Extreme South
         - -90 to -87
         - -180 to 180
       * - ``ExtremeNord``
         - Extreme North
         - 87 to 90
         - -180 to 180
       * - ``TropiquesOuest``
         - Western Tropics
         - -20 to 0
         - 180 to -90
       * - ``Bande60a90``
         - Band from 60°N to 90°N
         - 60 to 90
         - -180 to 180
       * - ``Bande30a60``
         - Band from 30°N to 60°N
         - 30 to 60
         - -180 to 180
       * - ``Bande00a30``
         - Band from 0°N to 30°N
         - 0 to 30
         - -180 to 180
       * - ``BandeM30a00``
         - Band from 30°S to 0°N
         - -30 to 0
         - -180 to 180
       * - ``BandeM60aM30``
         - Band from 60°S to 30°S
         - -60 to -30
         - -180 to 180
       * - ``BandeM90aM60``
         - Band from 90°S to 60°S
         - -90 to -60
         - -180 to 180
       * - ``Rapidscat``
         - RapidScat coverage
         - -55 to 55
         - -180 to 180
       * - ``npstere``
         - North Polar Stereographic
         - 0 to 90
         - -180 to 180
       * - ``spstere``
         - South Polar Stereographic
         - -90 to 0
         - -180 to 180
    """
    
    if region == 'PoleNord':
        latlons = (60, 90, -180, 180)
    elif region == 'PoleSud':
        latlons = (-90, -60, -180, 180)
    elif region == 'AmeriqueduNord':
        latlons = (25, 60, -145, -50)
    elif region == 'OuestAmeriqueduNord':
        latlons = (25, 60, -145, -97.5)
    elif region == 'AmeriqueDuNordPlus':
        latlons = (25, 85, -170, -40)
    elif region == 'Monde':
        latlons = (-90, 90, -180, 180)
    elif region == 'Global':
        latlons = (-90, 90, -180, 180)
    elif region == 'ExtratropiquesNord':
        latlons = (20, 90, -180, 180)
    elif region == 'ExtratropiquesSud':
        latlons = (-90, -20, -180, 180)
    elif region == 'HemisphereNord':
        latlons = (0, 90, -180, 180)
    elif region == 'HemisphereSud':
        latlons = (-90, 0, -180, 180)
    elif region == 'Asie':
        latlons = (25, 60, 65, 145)
    elif region == 'Europe':
        latlons = (25, 70, -10, 28)
    elif region == 'Mexique':
        latlons = (15, 30, -130, -60)
    elif region == 'Canada':
        latlons = (45, 90, -151, -50)
    elif region == 'BaieDhudson':
        latlons = (55, 90, -90, -60)
    elif region == 'Arctiquecanadien':
        latlons = (58, 90, -141, -50)
    elif region == 'EtatsUnis':
        latlons = (25, 45, -130, -70)
    elif region == 'SudestEtatsUnis':
        latlons = (25, 40, -100, -70)
    elif region == 'EstAmeriqueduNord':
        latlons = (25, 60, -97.5, -50)
    elif region == 'EstAmeriqueduNordPlus':
        latlons = (25, 85, -97.5, -50)
    elif region == 'OuestAmeriqueduNordPlus':
        latlons = (25, 85, -170, -97.5)
    elif region == 'Tropiques30':
        latlons = (-30, 30, -180, 180)
    elif region == 'Tropiques':
        latlons = (-20, 20, -180, 180)
    elif region == 'Australie':
        latlons = (-55, -10, 90, 180)
    elif region == 'Pacifique':
        latlons = (20, 65, 130, -150)
    elif region == 'Atlantique':
        latlons = (20, 65, -80, -1)
    elif region == 'Alaska':
        latlons = (50, 75, -180, -140)
    elif region == 'HIMAPEst':
        latlons = (35, 65, -105, -50)
    elif region == 'HIMAPOuest':
        latlons = (40, 65, -135, -90)
    elif region == 'ExtremeSud':
        latlons = (-90, -87, -180, 180)
    elif region == 'ExtremeNord':
        latlons = (87, 90, -180, 180)
    elif region == 'TropiquesOuest':
        latlons = (-20, 0, 180, -90)
    elif region == 'Bande60a90':
        latlons = (60, 90, -180, 180)
    elif region == 'Bande30a60':
        latlons = (30, 60, -180, 180)
    elif region == 'Bande00a30':
        latlons = (0, 30, -180, 180)
    elif region == 'BandeM30a00':
        latlons = (-30, 0, -180, 180)
    elif region == 'BandeM60aM30':
        latlons = (-60, -30, -180, 180)
    elif region == 'BandeM90aM60':
        latlons = (-90, -60, -180, 180)
    elif region == 'Rapidscat':
        latlons = (-55, 55, -180, 180)
    elif region == 'npstere':
        latlons = (0, 90, -180, 180)
    elif region == 'spstere':
        latlons = (-90, 0, -180, 180)
    else:
        raise ValueError(f'not: {region}')
    
    return latlons

def generate_latlon_criteria(LAT1, LAT2, LON1, LON2):
    """
    This function generates a filtering criteria expression based on latitude and longitude coordinates.

    Arguments:
    LAT1 (float): The starting latitude.
    LAT2 (float): The ending latitude.
    LON1 (float): The starting longitude.
    LON2 (float): The ending longitude.

    Returns:
    str: A filtering criteria expression.
    """
    relatopLAT = '<=' if LAT2 == 90 else '<'
    relatopLON = '<=' if LON2 == 180 else '<'

    if LON1 >= LON2:
        LATLONCRIT = (
            f" and lat >= {LAT1} and lat {relatopLAT} {LAT2} "
            f" and (lon >= {LON1} or lon {relatopLON} {LON2})" 
        )
    else:
        LATLONCRIT = (
            f" and lat >= {LAT1} and lat {relatopLAT} {LAT2} "
            f" and lon >= {LON1} and lon {relatopLON} {LON2}"
        )

    return LATLONCRIT


# ═════════════════════════════════════════════════════════════════════════════
# Polygons: regions that are not boxes
# ═════════════════════════════════════════════════════════════════════════════
"""Some regions are not boxes.

The HRDPS grid, the climate areas of EMET, the coverage of a radar: their
border is a polygon, and four numbers cannot say it. They live in
``configobs/regions_data`` as ``.npz``, brought in once with
``import_regions.py``, so pikobs carries them itself and needs no path to
anyone's filesystem.

Testing a polygon per observation would call Python tens of millions of
times per file, so a region is rasterised once to a regular grid, cached
in PATHWORK and memory-mapped by every worker -- as the land mask is --
and the query keeps the box that contains it in front:

    AND lat BETWEEN 39.0 AND 58.7 AND lon BETWEEN -142.0 AND -50.4
    AND in_region_sql_hrdps(lat, lon) = 1

Every module asks :func:`criteria` for the condition of a region and does
not care which kind it is.
"""

import os as _os
import re as _re
from typing import Dict as _Dict, List as _List, Optional as _Optional
from typing import Sequence as _Sequence, Tuple as _Tuple

import numpy as _np

DEFAULT_RESOLUTION = 0.1          # about 11 km, finer than any thinning
DATA_SUBDIR = "regions_data"
CACHE_SUBDIR = ".region_cache"
LAND_BUILD_MIN_GB = 4.0


def box_regions() -> _Dict[str, tuple]:
    """Every box of :func:`regions`, read from its own code.

    The boxes are written as a chain of tests, which is fine to read and
    impossible to enumerate; this parses them once so the boxes and the
    polygons can be listed and drawn side by side.
    """
    src = ""
    try:                       # the file itself: the order of the parts
        with open(_os.path.abspath(__file__)) as fh:   # does not matter
            src = fh.read()
    except Exception:                                  # pragma: no cover
        try:
            import inspect
            src = inspect.getsource(regions)
        except Exception:
            return {}
    out = {}
    for name, values in _re.findall(
            r"region\s*==\s*['\"]([^'\"]+)['\"]\s*:\s*\n\s*latlons\s*=\s*"
            r"\(([^)]*)\)", src):
        try:
            out[name] = tuple(float(v) for v in values.split(','))
        except ValueError:                             # pragma: no cover
            continue
    return out


# Which polygons the conditions built so far need. A module asks for the
# condition of a region; the connection that runs it registers what the
# condition uses, so no module has to remember to do it.
_PENDING: set = set()


def cache_dir() -> str:
    """Where the rasters are kept when a module passes no PATHWORK.

    PIKOBS_REGION_CACHE if it is set, otherwise the temporary directory
    of the machine, which every worker of a node shares.
    """
    import tempfile as _tempfile
    return _os.environ.get(
        "PIKOBS_REGION_CACHE",
        _os.path.join(_tempfile.gettempdir(), "pikobs_region_cache"))


def register_pending(conn, pathwork: _Optional[str] = None) -> None:
    """Give a connection the functions the conditions so far need."""
    if _PENDING:
        register(conn, sorted(_PENDING), pathwork or cache_dir())


def region_dir() -> str:
    """Where the collections are: inside the package, or PIKOBS_REGION_DIR."""
    return _os.environ.get(
        "PIKOBS_REGION_DIR",
        _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                     DATA_SUBDIR))


def collections() -> _List[str]:
    """The .npz files holding domains, newest name last."""
    d = region_dir()
    if not _os.path.isdir(d):
        return []
    return [_os.path.join(d, f) for f in sorted(_os.listdir(d))
            if f.endswith(".npz")]


def list_polygons() -> _Dict[str, _Tuple[str, str]]:
    """{name: (collection, key)} of every region pikobs carries."""
    out: _Dict[str, _Tuple[str, str]] = {}
    for path in collections():
        try:
            with _np.load(path, allow_pickle=False) as data:
                for key in data.files:
                    if not key.endswith("|0"):
                        continue               # one entry per ring, ring 0
                    name = key[:-2]            # marks the domain
                    out.setdefault(name, (path, name))
        except Exception:                              # pragma: no cover
            continue
    return out


def is_polygon(name: str) -> bool:
    return str(name) in list_polygons()


def rings_of(name: str) -> _List[_np.ndarray]:
    """The rings of a domain, each an (n, 2) array of lon, lat."""
    found = list_polygons().get(str(name))
    if not found:
        raise KeyError(f"region '{name}' is not in {region_dir()}; import "
                       f"it with import_regions.py")
    path, key = found
    out = []
    with _np.load(path, allow_pickle=False) as data:
        i = 0
        while f"{key}|{i}" in data.files:
            out.append(_np.asarray(data[f"{key}|{i}"], float))
            i += 1
    return out


def build_mask(name: str, resolution: float = DEFAULT_RESOLUTION):
    """(mask, lat0, lon0, resolution) of a domain, rasterised.

    A cell counts as inside when its centre is inside an odd number of
    rings, which is what the even-odd rule of a shapefile means: outer
    rings fill, holes empty.
    """
    from matplotlib.path import Path
    rings = rings_of(name)
    if not rings:
        raise ValueError(f"region '{name}' has no usable polygon")
    lon_lo = max(-180.0, min(r[:, 0].min() for r in rings) - resolution)
    lon_hi = min(180.0, max(r[:, 0].max() for r in rings) + resolution)
    lat_lo = max(-90.0, min(r[:, 1].min() for r in rings) - resolution)
    lat_hi = min(90.0, max(r[:, 1].max() for r in rings) + resolution)
    lats = _np.arange(lat_lo, lat_hi + resolution, resolution)
    lons = _np.arange(lon_lo, lon_hi + resolution, resolution)
    grid_lon, grid_lat = _np.meshgrid(lons, lats)
    points = _np.column_stack([grid_lon.ravel(), grid_lat.ravel()])
    inside = _np.zeros(points.shape[0], bool)
    for ring in rings:
        inside ^= Path(ring).contains_points(points)
    return (inside.reshape(grid_lat.shape), float(lats[0]), float(lons[0]),
            float(resolution))


def mask_path(pathwork: str, name: str, resolution: float) -> str:
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in str(name))
    return _os.path.join(pathwork, CACHE_SUBDIR,
                        f"{safe}_{resolution:g}.npz")


def cached_mask(name: str, pathwork: str,
                resolution: float = DEFAULT_RESOLUTION):
    """The rasterised domain, built once and memory-mapped afterwards."""
    dest = mask_path(pathwork, name, resolution)
    if not _os.path.isfile(dest):
        _os.makedirs(_os.path.dirname(dest), exist_ok=True)
        mask, lat0, lon0, res = build_mask(name, resolution)
        tmp = f"{dest}.tmp{_os.getpid()}.npz"
        _np.savez(tmp, mask=mask, meta=_np.array([lat0, lon0, res]))
        _os.replace(tmp, dest)
    with _np.load(dest) as data:
        lat0, lon0, res = [float(v) for v in data["meta"]]
        return data["mask"], lat0, lon0, res


def bounds(name: str, pathwork: str,
           resolution: float = DEFAULT_RESOLUTION) -> _Tuple[float, ...]:
    """(lat1, lat2, lon1, lon2) around the domain, for the fast filter."""
    mask, lat0, lon0, res = cached_mask(name, pathwork, resolution)
    n_lat, n_lon = mask.shape
    return (lat0, lat0 + (n_lat - 1) * res, lon0, lon0 + (n_lon - 1) * res)


def in_polygon_function(name: str, pathwork: str,
                       resolution: float = DEFAULT_RESOLUTION):
    """A scalar (lat, lon) -> 0/1 for SQLite, nearest cell of the mask."""
    mask, lat0, lon0, res = cached_mask(name, pathwork, resolution)
    n_lat, n_lon = mask.shape

    def _inside(lat, lon):
        if lat is None or lon is None:
            return 0
        if lon > 180.0:
            lon -= 360.0
        i = int(round((lat - lat0) / res))
        j = int(round((lon - lon0) / res))
        if i < 0 or j < 0 or i >= n_lat or j >= n_lon:
            return 0
        return int(bool(mask[i, j]))

    return _inside


def criteria(name: str, pathwork: _Optional[str] = None,
             lat: str = 'lat', lon: str = 'lon',
             resolution: float = DEFAULT_RESOLUTION) -> str:
    """The SQL of a region, whichever kind it is.

    A box gives the plain comparison it always gave. A polygon gives the
    box that contains it -- cheap, and it throws away most of the globe
    -- and then its raster mask, which is only consulted for what could
    be inside.
    """
    pathwork = pathwork or cache_dir()
    if not is_polygon(name):
        import pikobs
        lat1, lat2, lon1, lon2 = regions(name)
        crit = pikobs.generate_latlon_criteria(lat1, lat2, lon1, lon2)
        return (crit if lat == 'lat' else
                crit.replace('lat', lat).replace('lon', lon))
    _PENDING.add(str(name))         # the next connection registers it
    lat1, lat2, lon1, lon2 = bounds(name, pathwork, resolution)
    return (f" AND {lat} BETWEEN {lat1:.4f} AND {lat2:.4f}"
            f" AND {lon} BETWEEN {lon1:.4f} AND {lon2:.4f}"
            f" AND in_region_sql_{_tag(name)}({lat}, {lon}) = 1")


def list_regions() -> _List[str]:
    """Every region pikobs knows: the boxes first, then the polygons."""
    return sorted(box_regions()) + sorted(list_polygons())


def _tag(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in str(name)).lower()


def register(conn, regions: _Sequence[str],
             pathwork: _Optional[str] = None,
             resolution: float = DEFAULT_RESOLUTION) -> _List[str]:
    """Give the connection one function per irregular region asked for.

    Returns the names it registered, so a module can tell which of its
    regions are polygons and which are the old boxes.
    """
    done = []
    pathwork = pathwork or cache_dir()
    known = list_polygons()
    for region in regions:
        if str(region) not in known:
            continue
        conn.create_function(f"in_region_sql_{_tag(region)}", 2,
                             in_polygon_function(region, pathwork, resolution))
        done.append(str(region))
    return done



# ═════════════════════════════════════════════════════════════════════════════
# One map per region
# ─────────────────────────────────────────────────────────────────────────────

_LAND_CACHE: dict = {}
# building the land cache reads a 0.9 GB array; worth it on a compute node,
# not on a laptop, and a region map is perfectly readable without it
LAND_BUILD_MIN_GB = 4.0


def _may_build_land(cache_dir: str) -> bool:
    try:
        pages = _os.sysconf('SC_PHYS_PAGES') * _os.sysconf('SC_PAGE_SIZE')
        return pages / 1e9 >= LAND_BUILD_MIN_GB
    except Exception:                                  # pragma: no cover
        return False


def _land_for(view, pathwork):
    """The land of a window, from the mask pikobs already uses.

    Read once per process and kept as a coarse copy: drawing every region
    of a collection would otherwise open the whole grid again and again.
    """
    try:
        if 'grid' not in _LAND_CACHE:
            from .landmask import (LAND_MASK_CACHE_SUBDIR,
                                   mmap_land_mask as _mmap_land_mask)
            cache = _os.path.join(pathwork, LAND_MASK_CACHE_SUBDIR)
            ready = all(_os.path.isfile(_os.path.join(cache, f"{n}.npy"))
                        for n in ("mask", "lat", "lon"))
            if not ready and not _may_build_land(cache):
                return None        # a map without land beats no map at all
            mask, lat_grid, lon_grid = _mmap_land_mask(pathwork)
            # the grid may run north to south, so take the step from the
            # size of the spacing, not its sign
            spacing = abs(float(lat_grid[1] - lat_grid[0])) or 0.25
            step = max(1, int(round(0.25 / spacing)))
            # a quarter of a degree is plenty for a picture, and it keeps
            # the whole globe in a few megabytes
            small = _np.asarray(mask[::step, ::step]) == 0
            lat_s = _np.asarray(lat_grid[::step], float)
            lon_s = _np.asarray(lon_grid[::step], float)
            if lat_s[0] > lat_s[-1]:          # searchsorted needs ascending
                small, lat_s = small[::-1], lat_s[::-1]
            if lon_s[0] > lon_s[-1]:
                small, lon_s = small[:, ::-1], lon_s[::-1]
            _LAND_CACHE['grid'] = (small, lat_s, lon_s)
        land, lat_grid, lon_grid = _LAND_CACHE['grid']
    except Exception:                                  # pragma: no cover
        return None
    n_lat, n_lon = land.shape
    i0, i1 = _np.searchsorted(lat_grid, [view[0], view[1]])
    j0, j1 = _np.searchsorted(lon_grid, [view[2], view[3]])
    i0, j0 = int(_np.clip(i0, 0, n_lat - 2)), int(_np.clip(j0, 0, n_lon - 2))
    i1 = int(_np.clip(max(i1, i0 + 2), i0 + 2, n_lat))
    j1 = int(_np.clip(max(j1, j0 + 2), j0 + 2, n_lon))
    return (land[i0:i1, j0:j1],
            [float(lon_grid[j0]), float(lon_grid[j1 - 1]),
             float(lat_grid[i0]), float(lat_grid[i1 - 1])])


def plot_region(name: str, out_dir: str, pathwork: _Optional[str] = None,
                resolution: float = DEFAULT_RESOLUTION) -> str:
    """Draw a region on a map and return the file written.

    A name in a list says little; the shape says everything. The land
    comes from the mask pikobs already uses for the land / ocean split,
    so this needs nothing else installed.
    """
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    
    pathwork = pathwork or out_dir
    polygon = is_polygon(name)
    if polygon:
        rings = rings_of(name)
        lat1, lat2, lon1, lon2 = bounds(name, pathwork, resolution)
    else:
        rings = []
        lat1, lat2, lon1, lon2 = regions(name)
        if lon1 > lon2:              # a box across the date line, as
            lon1, lon2 = -180.0, 180.0   # Pacifique is written

    # a box is drawn on the whole globe, plain cylindrical: four numbers
    # mean little without the world around them, and half of them are
    # bands that cover it anyway. A polygon gets a window around itself,
    # since its shape is the point.
    if polygon:
        pad_lat = max(4.0, (lat2 - lat1) * 0.25)
        pad_lon = max(6.0, (lon2 - lon1) * 0.25)
        view = (max(-90.0, lat1 - pad_lat), min(90.0, lat2 + pad_lat),
                max(-180.0, lon1 - pad_lon), min(180.0, lon2 + pad_lon))
    else:
        view = (-90.0, 90.0, -180.0, 180.0)

    fig, ax = plt.subplots(figsize=(7.2, 4.6) if polygon else (8.4, 4.4),
                           facecolor='white')
    land = _land_for(view, pathwork)
    if land is not None:
        ax.imshow(land[0], origin='lower', cmap='Greys', vmin=0, vmax=3,
                  extent=land[1], interpolation='nearest', zorder=0)
    if polygon:
        for ring in rings:
            ax.fill(ring[:, 0], ring[:, 1], color='#D62728', alpha=0.18,
                    zorder=2)
            ax.plot(ring[:, 0], ring[:, 1], color='#B2182B', lw=1.8,
                    zorder=3)
        kind = f"polygon, {sum(len(r) for r in rings)} vertices"
    else:
        ax.add_patch(mpl.patches.Rectangle(
            (lon1, lat1), lon2 - lon1, lat2 - lat1, facecolor='#2166AC',
            alpha=0.18, edgecolor='#2166AC', lw=1.8, zorder=2))
        kind = "box"
    ax.set_xlim(view[2], view[3])
    ax.set_ylim(view[0], view[1])
    ax.grid(True, ls='--', lw=0.6, alpha=0.3)
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    ax.set_title(f"{name}   ({kind})\n"
                 f"lat {lat1:.1f} to {lat2:.1f}, "
                 f"lon {lon1:.1f} to {lon2:.1f}", fontsize=11)
    if not polygon:
        ax.set_aspect('equal')                 # cylindrical, undistorted
        ax.set_xticks(_np.arange(-180, 181, 60))
        ax.set_yticks(_np.arange(-90, 91, 30))
    _os.makedirs(out_dir, exist_ok=True)
    out = _os.path.join(out_dir, f"region_{_tag(name)}.png")
    fig.tight_layout()
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out


def plot_all(out_dir: str, names: _Optional[_Sequence[str]] = None,
             pathwork: _Optional[str] = None) -> _List[str]:
    """One map per region, and an index page listing them."""
    names = list(names) if names else list_regions()
    written = []
    for name in names:
        try:
            written.append(plot_region(name, out_dir, pathwork))
        except Exception as exc:                      # pragma: no cover
            print(f"[regions] {name}: {exc}")
    if written:
        cards = "".join(
            f"<figure style='margin:0'><img src='{_os.path.basename(f)}' "
            f"style='width:100%'><figcaption style='text-align:center;"
            f"font-family:sans-serif;font-size:13px'>{n}</figcaption>"
            f"</figure>"
            for n, f in zip(names, written))
        html = (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                f"<title>pikobs regions</title></head><body>"
                f"<h1 style='font-family:sans-serif'>Regions of pikobs "
                f"({len(written)})</h1>"
                f"<div style='display:grid;grid-template-columns:"
                f"repeat(auto-fill,minmax(360px,1fr));gap:14px'>{cards}"
                f"</div></body></html>")
        with open(_os.path.join(out_dir, "regions.html"), "w") as fh:
            fh.write(html)
    return written
