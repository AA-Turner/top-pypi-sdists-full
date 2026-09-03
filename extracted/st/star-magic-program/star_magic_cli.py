"""star-magic - THE FRONT DOOR (v0.412.0). One installable command over both
products: the UQFF calculator and the downhole surveying simulator.

    star-magic calc PAPER_646            # dispatch + honesty flags
    star-magic calc --list               # wired papers
    star-magic gate                      # full fidelity gate, ANY layout
    star-magic well run --steps 200      # downhole simulator passthrough
    star-magic docs                      # where the corpus lives
    star-magic gui                       # Qt operator shell (gui extra)

DANIEL'S LOCK #1 (2026-09-01), honored here with no GUI required: every
`calc` result prints the results-table verification status for each physics
row that cites the paper - VERIFIED_LIVE (re-derived from primitives at
generation time), INHERITED_CARRIED (carried from the inherited baseline,
NOT re-derived), or LIVE_MISMATCH (both values shown). Yang-Mills 1.736 and
Page 0.99596 are INHERITED_CARRIED and the terminal says so; hiding it
would be a lie.
"""
from __future__ import annotations

import argparse
import csv
import sys

import uqff_paths


def _results_rows_for(paper_id: str):
    rows = []
    try:
        with open(uqff_paths.results_table(), encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                blob = " ".join(str(v) for v in r.values())
                if paper_id in blob:
                    rows.append(r)
    except FileNotFoundError:
        pass
    return rows


def cmd_calc(args) -> int:
    import uqff_calculator as C
    if args.list:
        for p in C.list_wired():
            print(p)
        print("-- %d wired papers (%d dispatch keys)" % (C.wired_count(), len(C.DISPATCH)))
        return 0
    pid = args.paper
    if pid not in C.DISPATCH:
        print("UNKNOWN PAPER: %s (try: star-magic calc --list)" % pid)
        return 2
    r = C.calc(pid)
    print("== %s" % pid)
    print("value:        %s" % r.get("value"))
    print("formula:      %s" % r.get("formula"))
    print("residual_pct: %s" % r.get("residual_pct"))
    print("status:       %s" % r.get("status", "WIRED"))
    for extra in ("ruling_batch2", "footer_ruling", "athz_ruling", "e_react_ruling",
                  "k4_ruling", "p_scaling_convention"):
        if extra in r:
            print("%s: %s" % (extra, r[extra]))
    rows = _results_rows_for(pid)
    print("-- results-table verification (LIVE vs INHERITED - the honesty flags):")
    if not rows:
        print("   no physics results-table row cites %s directly" % pid)
    for row in rows:
        print("   %-28s = %-18s [%s]%s" % (
            row.get("constant", "?"), row.get("uqff_value", "?"),
            row.get("live_status", "?"),
            ("  live=" + row["live_value"]) if row.get("live_value") else ""))
    print("   (VERIFIED_LIVE = re-derived from primitives at generation time;")
    print("    INHERITED_CARRIED = baseline value, NOT re-derived here;")
    print("    LIVE_MISMATCH = both values shown, nothing silently replaced)")
    return 0


def cmd_gate(_args) -> int:
    """Run the full fidelity gate from ANY cwd on ANY layout (Daniel's lock #2):
    the gate bootstraps itself through uqff_paths.data_root()."""
    import runpy
    try:
        runpy.run_path(str(uqff_paths.resolve("uqff_fidelity_tests.py")), run_name="__main__")
    except SystemExit as e:
        return int(e.code or 0)
    return 0


def cmd_well(args) -> int:
    from uqff_downhole_simulator import __main__ as dm
    sys.argv = ["uqff_downhole_simulator"] + args.rest
    return dm.main() if hasattr(dm, "main") else 0


def cmd_docs(_args) -> int:
    root = uqff_paths.data_root()
    print("corpus root:   %s" % root)
    print("whitepapers:   %s (%d files)" % (uqff_paths.corpus(),
          sum(1 for _ in uqff_paths.corpus().iterdir())))
    print("registry:      %s" % uqff_paths.registry())
    print("results table: %s" % uqff_paths.results_table())
    print("rulings:       %s" % uqff_paths.resolve("RULINGS_QUEUE.md"))
    return 0


def cmd_gui(_args) -> int:
    try:
        from star_magic_shell import main as shell_main
    except ImportError as e:
        print("GUI needs the gui extra:  pip install \"star-magic-program[gui]\"  (%s)" % e)
        return 3
    return shell_main()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="star-magic",
                                 description="Star-Magic UQFF: calculator + downhole surveying, one door.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_calc = sub.add_parser("calc", help="run a paper dispatch with honesty flags")
    p_calc.add_argument("paper", nargs="?", default="")
    p_calc.add_argument("--list", action="store_true")
    p_calc.set_defaults(fn=cmd_calc)
    p_gate = sub.add_parser("gate", help="full fidelity gate (works from site-packages)")
    p_gate.set_defaults(fn=cmd_gate)
    p_well = sub.add_parser("well", help="downhole simulator passthrough")
    p_well.add_argument("rest", nargs=argparse.REMAINDER)
    p_well.set_defaults(fn=cmd_well)
    p_docs = sub.add_parser("docs", help="where the corpus lives on this machine")
    p_docs.set_defaults(fn=cmd_docs)
    p_gui = sub.add_parser("gui", help="Qt operator shell (gui extra)")
    p_gui.set_defaults(fn=cmd_gui)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
