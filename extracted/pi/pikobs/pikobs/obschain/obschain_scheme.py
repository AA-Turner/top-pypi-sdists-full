"""The files of a family from dbase to postalt: one column per stage, one
box per file with the observations it holds, lines to the files of the next
stage that come from it. It shows where files split (the dbase of ai into
one file per type in cutoff), where they merge again (the four of cutoff
into one ai in derialt), where the RARS files go, and the versions that do
not reach postalt."""
import os
import re
import sqlite3
from collections import defaultdict
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def _rars(name: str) -> bool:
    return "rars" in name.lower().split("_")


def scheme_data(path: str, region: str = "Monde") -> Dict:
    """{stages, files: {stage: [(name, n, kind)]}} of one family; kind is
    counted, version (another version, not counted) or copy."""
    with sqlite3.connect(path) as conn:
        stages = [r[0] for r in conn.execute("SELECT stage FROM stages ORDER BY position")]
        files = defaultdict(dict)
        versions = defaultdict(set)
        for stage, stream, names in conn.execute("SELECT DISTINCT stage, stream, files FROM files"):
            for n in names.split():
                files[stage].setdefault(n, None)
                if stream == "version":
                    versions[stage].add(n)
        if conn.execute("SELECT 1 FROM sqlite_master WHERE name = 'file_counts'").fetchone():
            per = defaultdict(int)
            for stage, stream, f, n in conn.execute(
                    "SELECT stage, stream, file, SUM(n) FROM file_counts WHERE region = ? "
                    "GROUP BY stage, stream, file", (region,)):
                per[(stage, f)] = max(per[(stage, f)], n)
            for stage in files:              # counted, and nothing in it
                for f in files[stage]:
                    files[stage][f] = per.get((stage, f), 0)
        extra = defaultdict(dict)
        for (note,) in conn.execute("SELECT note FROM notes"):
            m = re.match(r"\S+ \S+ (\S+): (.+?) -- (.+)$", note)
            if not m or m.group(1) not in stages:
                continue
            kind = ("version" if "another version" in m.group(3) else
                    "copy" if "copy" in m.group(3) else
                    "missing" if "missing" in m.group(3) else None)
            if kind:
                for n in m.group(2).split():
                    if n not in files[m.group(1)]:
                        extra[m.group(1)][n] = kind
    out = {}
    for st in stages:
        rows = [(n, files[st][n], "version" if n in versions[st] else "counted")
                for n in sorted(files[st], key=lambda x: (x in versions[st], _rars(x), x))]
        rows += [(n, None, k) for n, k in sorted(extra[st].items(), key=lambda x: (_rars(x[0]), x[0]))]
        out[st] = rows
    return dict(stages=stages, files=out)


COLORS = {"counted": ("#E8EEF4", "#52606D"), "rars": ("#FCEBD9", "#B25E09"),
          "version": ("#FFFFFF", "#9AA5B1"), "copy": ("#FFFFFF", "#9AA5B1"),
          "missing": ("#FDECEC", "#B42318")}


def draw_scheme(family: str, path: str, out_png: str, region: str = "Monde") -> str:
    d = scheme_data(path, region)
    stages, files = d["stages"], d["files"]
    rows = max((len(v) for v in files.values()), default=1)
    w, h = 2.9 * len(stages) + 0.6, 0.62 * rows + 1.6
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, len(stages)); ax.set_ylim(-rows - 0.2, 1.1); ax.axis("off")
    pos = {}
    for i, st in enumerate(stages):
        ax.text(i + 0.5, 0.75, st, ha="center", va="center", fontsize=11, fontweight="bold",
                color="#1F2933")
        for j, (name, n, kind) in enumerate(files[st]):
            y = -j - 0.1
            face, edge = COLORS["rars"] if kind == "counted" and _rars(name) else COLORS[kind]
            box = FancyBboxPatch((i + 0.08, y - 0.36), 0.84, 0.72,
                                 boxstyle="round,pad=0.01,rounding_size=0.06",
                                 facecolor=face, edgecolor=edge, lw=1.2,
                                 ls="--" if kind in ("version", "copy") else "-")
            ax.add_patch(box)
            ax.text(i + 0.5, y + 0.12, name, ha="center", va="center", fontsize=8.5,
                    color=edge if kind != "counted" else "#1F2933")
            sub = (f"{n:,d} rows, other version" if kind == "version" and n else
                   f"{n:,d} rows" if n else "empty" if n == 0 else
                   {"version": "other version, not counted", "copy": "copy, counted once",
                    "missing": "missing"}.get(kind, ""))
            if kind == "counted" and n is None:
                sub = ""
            ax.text(i + 0.5, y - 0.17, sub, ha="center", va="center", fontsize=7.5,
                    color="#7B8794")
            if kind == "counted":
                pos[(st, name)] = (i, y)
    # a file leads to the files of the next stage of its own stream (RARS
    # or not); a stage with no file of that stream ends its lines
    for i in range(len(stages) - 1):
        a, b = stages[i], stages[i + 1]
        src = [n for (st, n) in pos if st == a]
        for (st, name), (x0, y0) in pos.items():
            if st != a:
                continue
            for (st2, name2), (x1, y1) in pos.items():
                if st2 != b:
                    continue
                # derialt to evalalt: the trunk feeds both branches (mwhs2
                # comes as rars_mwhs2 and leaves as mwhs2_qc and mwhs2_rars_qc);
                # a stage with no file of the other stream feeds it too (the
                # one mwhs2_dbase holds the RARS of cutoff)
                if (a == "derialt" and b == "evalalt") or _rars(name2) == _rars(name) or \
                        not any(_rars(n) == _rars(name2) for n in src):
                    ax.annotate("", xy=(x1 + 0.08, y1), xytext=(x0 + 0.92, y0),
                                arrowprops=dict(arrowstyle="-|>", lw=0.9, shrinkA=0, shrinkB=0,
                                                color="#B25E09" if _rars(name) and _rars(name2) else "#7B8794",
                                                connectionstyle="arc3,rad=0"))
    ax.set_title(f"{family}  ·  the files from dbase to postalt  ·  {region}",
                 loc="left", fontsize=13, fontweight="bold", color="#1F2933")
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    fig.savefig(out_png, dpi=110, bbox_inches="tight")
    plt.close(fig)
    return out_png
