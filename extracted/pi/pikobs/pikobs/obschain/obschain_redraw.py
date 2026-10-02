"""Redraw the figures and the viewer of an obschain run from its databases,
without counting again.

    python obschain_redraw.py PATHWORK CYCLE_START CYCLE_END RUN REGION... [--id_stn join all]
"""
import glob
import os
import re
import sys

from pikobs.obschain.obschain import chain_table, is_radiance, is_rars
from pikobs.obschain.obschain_plot import make_figures, VIEWER, web_address

args = sys.argv[1:]
id_stn = ["join"]
if "--id_stn" in args:
    i = args.index("--id_stn")
    id_stn, args = args[i + 1:], args[:i]
pathwork, start, end, run, regions = args[0], args[1], args[2], args[3], args[4:]
table = chain_table()
when = (f"{start[:4]}-{start[4:6]}-{start[6:8]} {start[8:10]} UTC" if start == end
        else f"{start} .. {end}")


def key_of(family, branch):
    names = [n for n in table.get(family, {}).get("postalt", [])
             if is_rars(n) == (branch == "rars")] or [family]
    return re.sub(r"_rars$", "", names[0])


import sqlite3


def complete(path):
    """A database written by obschain: it has its counts and its stages (an
    empty file, made by opening a missing name with sqlite3, has neither)."""
    try:
        with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as c:
            names = {r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        return {"counts", "stages"} <= names
    except sqlite3.Error:
        return False


dbs = sorted(glob.glob(os.path.join(pathwork, "obschain_*.db")))
skipped = [d for d in dbs if not complete(d)]
for d in skipped:
    print(f"[obschain] skipped, not a database of obschain: {d} ({os.path.getsize(d)} bytes)")
dbs = [d for d in dbs if d not in skipped]
figs = make_figures(dbs, regions, pathwork, when, run,
                    lambda family: is_radiance(family, table), key_of, id_stn)
viewer = os.path.join(pathwork, VIEWER)
print(f"[obschain] {len(figs)} figure(s) redrawn from {len(dbs)} database(s)")
print(f"Viewer: {viewer}")
if web_address(viewer):
    print(f"Web:    {web_address(viewer)}")
