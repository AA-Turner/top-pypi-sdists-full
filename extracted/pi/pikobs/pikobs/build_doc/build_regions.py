"""Build the regionsobs.py module docstring, boxes read from its own code.

    python build_regions.py pikobs/configobs/regionsobs.py
"""
import os as _os_dw, sys as _sys_dw  # noqa: E401
_sys_dw.path.insert(0, _os_dw.path.dirname(_os_dw.path.abspath(__file__)))
from docwrite import write_docstring  # noqa: E402
import os
import re
import sys

# this page needs no wrapper: a region is not a module you launch
if len(sys.argv) < 2:
    sys.exit(__doc__)
MODULE = sys.argv[1]


def user_settings(path):
    txt = open(path).read()
    a = txt.index("# 1. USER SETTINGS")
    a = txt.index("\n", txt.index("# ====", a)) + 1
    b = txt.index("# ====", a)
    return "\n".join("   " + l if l else ""
                     for l in txt[a:b].strip("\n").splitlines())


def grid(headers, rows):
    cols = list(zip(*([headers] + rows)))
    widths = [max(len(c) for c in col) for col in cols]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def line(r):
        return "|" + "|".join(f" {c:<{w}} " for c, w in zip(r, widths)) + "|"

    out = [sep, line(headers), sep.replace("-", "=")]
    for r in rows:
        out += [line(r), sep]
    return "\n".join(out)


def image(name, alt, static="docs/source/_static"):
    """The figure, or nothing when the run that makes it has not been
    done yet: a page reads better without one image than with a broken
    link and a warning at every build."""
    if not os.path.isfile(os.path.join(static, name)):
        print(f"  (no {name} yet: left out of the page)")
        return ""
    return (f".. image:: _static/{name}\n   :alt: {alt}\n"
            f"   :align: center\n   :width: 100%")



import re


def box_table(path):
    """The RST table of every box, parsed from the chain of tests."""
    src = open(path).read()
    rows = []
    for name, values in re.findall(
            r"region\s*==\s*['\"]([^'\"]+)['\"]\s*:\s*\n\s*latlons\s*=\s*"
            r"\(([^)]*)\)", src):
        try:
            a, b, c, d = [float(v) for v in values.split(',')]
        except ValueError:
            continue
        rows.append([f"``{name}``", f"{a:g} to {b:g}", f"{c:g} to {d:g}"])
    return grid(["Region", "Latitude", "Longitude"], rows), len(rows)


def polygon_table():
    """What the package carries as polygons, if anything."""
    try:
        from pikobs.configobs import regionsobs as R
        names = sorted(R.list_polygons())
    except Exception:
        names = []
    if not names:
        return ("No polygon is in ``configobs/regions_data`` yet; see the "
                "section above to bring some in.", 0)
    # names only, three per row
    cells = [f"``{n}``" for n in names]
    out = [".. list-table::", "   :widths: 34 33 33", ""]
    for i in range(0, len(cells), 3):
        row = cells[i:i + 3] + [" "] * (3 - len(cells[i:i + 3]))
        out.append("   * - " + row[0])
        out += ["     - " + c for c in row[1:]]
    return "\n".join(out), len(names)


USING = grid(
    ["What you want", "What to write"],
    [
        ["the condition of a region in SQL", "``regionsobs.criteria(name, pathwork)``"],
        ["a polygon usable from SQLite", "``regionsobs.register(conn, regions, pathwork)`` once per connection"],
        ["is this one a polygon?", "``regionsobs.is_polygon(name)``"],
        ["every region there is", "``regionsobs.list_regions()``"],
        ["the four numbers of a box", "``regions(name)``, as always"],
    ])

TROUBLE = grid(
    ["Symptom", "Cause and fix"],
    [
        ["``region 'X' is not in ...``",
         "The name is neither a box of this file nor a polygon in regions_data. Check the spelling, or import the collection that holds it."],
        ["A polygon selects nothing",
         "Its vertices may be in 0 to 360 rather than -180 to 180. Draw it with --plot: a region in the wrong half of the world is obvious."],
        ["The maps have no coastline",
         "The land mask has not been built yet; the drawing never builds it, to stay light. Point --plot at a PATHWORK where zone or histogram has already run."],
        ["A box crosses the date line",
         "Written as lon 130 to -150, as Pacifique is. The selection handles it; the map draws the whole globe."],
    ])

DOC = r"""
================================================
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

__BOX_TABLE__

They are read from this file itself, so a region added to ``regions()``
appears here, in ``list_regions()`` and in the maps without being
written down twice.

A box that crosses the date line is written the way it reads:
``Pacifique`` goes from 130 to -150.

The EMET domains
================

__POLY_TABLE__

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

__IMG_BOX__

A polygon gets a window of its own, since its shape is the point, with
the number of vertices in the title:

__IMG_POLY__

The land comes from the mask pikobs already uses for the land / ocean
split, so this needs nothing else installed. All of them on one page:
`every region, side by side <_static/regions/regions.html>`__.

Pass names to draw only those:

.. code-block:: bash

   python pikobs/configobs/import_regions.py --plot /tmp/maps hrdps Boreal_CLIM Canada

How a region becomes a query
============================

__USING__

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


import re as _re

target = MODULE
boxes, n_boxes = box_table(target)
polys, n_polys = polygon_table()
def image(name, alt, static="docs/source/_static"):
    """The figure, or nothing when the run that makes it has not been
    done yet: a page is better without one image than with a broken
    link and a warning at every build."""
    if not os.path.isfile(os.path.join(static, name)):
        print(f"  (no {name} yet: the figure is left out of the page)")
        return ""
    return (f".. image:: _static/{name}\n   :alt: {alt}\n"
            f"   :align: center\n   :width: 100%\n")


doc = (DOC.replace("__IMG_BOX__", image("region_box.png",
                                        "A box region on the globe"))
          .replace("__IMG_POLY__", image("region_polygon.png",
                                         "A polygon region, zoomed"))
          .replace("__BOX_TABLE__", boxes)
          .replace("__POLY_TABLE__", polys)
          .replace("__USING__", USING)
          .replace("__TROUBLE__", TROUBLE))
assert not _re.findall(r"__[A-Z_]+__", doc), _re.findall(r"__[A-Z_]+__", doc)
assert '\"\"\"' not in doc

write_docstring(target, doc, __file__)
print(f"docstring written: {n_boxes} boxes, {n_polys} polygon(s), "
      f"{doc.count(chr(10))} lines")
