#!/usr/bin/python3
"""Bring regions into pikobs, once, and draw them.

    python import_regions.py <shapefile or directory> ... [--name collection]

Reads the polygons of dasVerif -- or of any other shapefile -- and writes
them into ``pikobs/configobs/regions_data/<collection>.npz``, one array
per ring, in plain lon/lat. From then on pikobs carries the domains
itself: no path to a shared filesystem, no pyshp at run time, and the
same regions on ppp7, ppp8 or a laptop.

    python import_regions.py \\
        /space/hall5/.../shapefiles/common_systems/hrdps.shp \\
        /space/hall5/.../shapefiles/arcad_dasVerif_domains \\
        --name dasverif

    python import_regions.py --list          # what pikobs carries now

A ring of thousands of vertices costs a few tens of kB, so a whole
collection stays well under a megabyte. Use --simplify to drop the
vertices that change the border by less than a given distance; 0.05
degrees is about 5 km, invisible at the 0.1-degree resolution of the
raster pikobs builds from them.
"""

import argparse
import os
import sys
from typing import Dict, List

import numpy as np

_NAME_FIELDS = ("dom_name", "domain_name", "domain", "name", "region", "id")


def _shapefiles(items) -> List[str]:
    out = []
    for item in items:
        if os.path.isdir(item):
            for root, _, files in os.walk(item):
                out += [os.path.join(root, f) for f in sorted(files)
                        if f.endswith(".shp")]
        elif os.path.isfile(item) and item.endswith(".shp"):
            out.append(item)
        else:
            print(f"[import_regions] not a shapefile, skipped: {item}",
                  file=sys.stderr)
    return out


def _name_of(record, fields) -> str:
    names = [f[0] for f in fields[1:]]                 # skip DeletionFlag
    for wanted in _NAME_FIELDS:
        for i, name in enumerate(names):
            if name.lower() == wanted:
                return str(record[i]).strip()
    return str(record[0]).strip()


def _rings(shape) -> List[np.ndarray]:
    pts = np.asarray(shape.points, float)
    parts = list(shape.parts) + [len(pts)]
    return [pts[parts[i]:parts[i + 1]] for i in range(len(parts) - 1)
            if parts[i + 1] - parts[i] >= 3]


def _simplify(ring: np.ndarray, tol: float) -> np.ndarray:
    """Douglas-Peucker, so a border of 50 000 points does not travel."""
    if tol <= 0 or len(ring) < 4:
        return ring
    keep = np.zeros(len(ring), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(ring) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, b = ring[i], ring[j]
        ab = b - a
        norm = np.hypot(*ab)
        seg = ring[i + 1:j]
        if norm == 0:
            d = np.hypot(*(seg - a).T)
        else:
            d = np.abs(np.cross(ab, seg - a)) / norm
        k = int(np.argmax(d))
        if d[k] > tol:
            keep[i + 1 + k] = True
            stack += [(i, i + 1 + k), (i + 1 + k, j)]
    return ring[keep]


def read_domains(paths: List[str], simplify: float = 0.0
                 ) -> Dict[str, List[np.ndarray]]:
    import shapefile                                   # pyshp, only here
    out: Dict[str, List[np.ndarray]] = {}
    for path in paths:
        with shapefile.Reader(path) as sf:
            fields = sf.fields
            for i, rec in enumerate(sf.records()):
                name = _name_of(rec, fields)
                if not name or name in out:
                    continue
                rings = [_simplify(r, simplify) for r in _rings(sf.shape(i))]
                rings = [r for r in rings if len(r) >= 3]
                if rings:
                    out[name] = rings
        print(f"[import_regions] {os.path.basename(path)}: "
              f"{len(out)} region(s) so far", flush=True)
    return out


def write_collection(domains: Dict[str, List[np.ndarray]], dest: str) -> str:
    arrays = {}
    for name, rings in domains.items():
        for i, ring in enumerate(rings):
            arrays[f"{name}|{i}"] = np.asarray(ring, np.float32)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    np.savez_compressed(dest, **arrays)
    return dest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument('sources', nargs='*',
                    help="shapefiles, or directories holding them")
    ap.add_argument('--name', default='emet',
                    help="name of the collection written in "
                         "configobs/regions_data (default dasverif)")
    ap.add_argument('--simplify', type=float, default=0.02,
                    help="drop vertices that move the border by less than "
                         "this many degrees (default 0.02, about 2 km); 0 "
                         "keeps every point")
    ap.add_argument('--list', action='store_true',
                    help="show the regions pikobs already carries")
    ap.add_argument('--plot', metavar='DIR',
                    help="draw one map per region into DIR, with an "
                         "index page: the quickest way to see what a name "
                         "really covers")
    args = ap.parse_args(argv)

    from pikobs.configobs import regionsobs as R
    if args.plot:
        written = R.plot_all(args.plot, args.sources or None)
        print(f"[import_regions] {len(written)} map(s) in {args.plot}; "
              f"open {os.path.join(args.plot, 'regions.html')}")
        return 0
    if args.list or not args.sources:
        known = R.list_polygons()
        print(f"[import_regions] {len(known)} region(s) in "
              f"{R.region_dir()}:")
        for name in sorted(known):
            n_rings = len(R.rings_of(name))
            print(f"    {name}  ({n_rings} ring(s))")
        return 0

    paths = _shapefiles(args.sources)
    if not paths:
        print("[import_regions] no shapefile found", file=sys.stderr)
        return 1
    domains = read_domains(paths, args.simplify)
    if not domains:
        print("[import_regions] no domain read", file=sys.stderr)
        return 1
    dest = os.path.join(R.region_dir(), f"{args.name}.npz")
    write_collection(domains, dest)
    size = os.path.getsize(dest) / 1024.0
    print(f"[import_regions] {len(domains)} region(s) written to {dest} "
          f"({size:.0f} kB). They are part of pikobs now: use their names "
          f"in REGION.", flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
