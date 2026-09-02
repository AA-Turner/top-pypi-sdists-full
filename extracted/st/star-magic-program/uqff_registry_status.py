"""uqff_registry_status — campaign registry census (Star-Magic-Program).

HONESTY NOTE (2026-08-03 repair):
This module previously shipped as a v0.2.0 SCAFFOLD STUB whose writer functions
emitted hardcoded "no rows wired yet" text, while the bundled report files
(UNIFIED_REGISTRY_STATUS_REPORT.md / _RESULTS_TABLE.md / _FALSIFIABILITY.md)
actually carried the *predecessor* Star-Magic R0-R5 physics results (9-primitive
-> 73-derived-constant table, 2,549-row registry). The stub therefore falsely
claimed to generate files it did not, and running it would have DELETED the
inherited physics results.

DOCTRINE SUPERSEDED (Daniel's order, 2026-09-01): the freeze was protection
against a destructive stub, not a claim the physics cannot be derived here.
This repo now carries the full compiled corpus, so the results table is
DERIVED LIVE by calculate_results_table():
  * The inherited physics baseline is preserved IMMUTABLY as
    UNIFIED_REGISTRY_RESULTS_TABLE_INHERITED.csv (copied once, never edited).
  * Every closed form is re-evaluated at generation time against
    uqff_registry_primitives; rows verify against the baseline value and are
    flagged VERIFIED_LIVE / INHERITED_CARRIED (form not evaluatable here) /
    LIVE_MISMATCH (both values reported, nothing silently replaced).
  * The old protection survives as an invariant: no baseline row is ever
    dropped or overwritten - the live table can only ADD verification.
  * calculate_status_report() computes an HONEST live census of THIS repo's
    paper-wiring campaign registry (UNIFIED_REGISTRY.csv), parsed with the csv
    module (quoted comma-bearing fields handled correctly).

The campaign's authoritative wired/not-wired ledger is WHITEPAPER_INDEX.md;
this surface is a programmatic cross-check of the campaign CSV, nothing more.
"""
from __future__ import annotations

import csv
from typing import Any


REGISTRY_CSV = "UNIFIED_REGISTRY.csv"
GRAPH_CSV = "UNIFIED_REGISTRY_GRAPH.csv"
CITATIONS_CSV = "UNIFIED_REGISTRY_CORPUS_CITATIONS.csv"
XGEO_QUEUE_CSV = "UNIFIED_REGISTRY_XGEO_QUEUE.csv"
XGEO_ROUTES_CSV = "UNIFIED_REGISTRY_XGEO_ROUTES.csv"
XGEO_CONFIRMATIONS_CSV = "UNIFIED_REGISTRY_XGEO_CONFIRMATIONS.csv"


def _load_registry_rows() -> list[dict[str, Any]]:
    try:
        with open(REGISTRY_CSV, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def _count_data_lines(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            n = sum(1 for _ in f)
        return max(0, n - 1)
    except FileNotFoundError:
        return 0


def calculate_status_report(dataset: dict | None = None) -> dict:
    """Honest live census of THIS repo's campaign registry (UNIFIED_REGISTRY.csv)."""
    rows = _load_registry_rows()
    statuses: dict[str, int] = {}
    papers: set[str] = set()
    for r in rows:
        st = (r.get("status") or "").strip()
        statuses[st] = statuses.get(st, 0) + 1
        src = (r.get("paper_source") or "").strip()
        if src.startswith("PAPER_"):
            papers.add(src.split()[0])
    return {
        "value": {
            "registry_rows": len(rows),
            "distinct_papers_in_registry": len(papers),
            "status_breakdown": statuses,
            "graph_edges": _count_data_lines(GRAPH_CSV),
            "corpus_citation_rows": _count_data_lines(CITATIONS_CSV),
            "xgeo_queue_tasks": _count_data_lines(XGEO_QUEUE_CSV),
            "xgeo_routes": _count_data_lines(XGEO_ROUTES_CSV),
            "xgeo_confirmations": _count_data_lines(XGEO_CONFIRMATIONS_CSV),
            "note": "campaign census; physics results table is a frozen inherited reference, not derived here",
        }
    }


if __name__ == "__main__":
    import json
    print(json.dumps(calculate_status_report()["value"], indent=2))


RESULTS_TABLE_CSV = "UNIFIED_REGISTRY_RESULTS_TABLE.csv"
RESULTS_TABLE_MD = "UNIFIED_REGISTRY_RESULTS_TABLE.md"
RESULTS_BASELINE_CSV = "UNIFIED_REGISTRY_RESULTS_TABLE_INHERITED.csv"


def _results_eval_namespace():
    import math
    import uqff_registry_primitives as P
    ns = {k: v for k, v in vars(P).items()
          if not k.startswith("_") and isinstance(v, (int, float))}
    ns.update({"pi": math.pi, "sqrt": math.sqrt, "exp": math.exp,
               "cos": math.cos, "sin": math.sin, "log": math.log,
               "log10": math.log10, "factorial": math.factorial, "e": math.e})
    for alias, target in (("D_crit", "D_CRIT"), ("D_phys", "D_PHYS"),
                          ("SSq", "SSQ"), ("rho_SCm", "RHO_SCM"),
                          ("rho_UA", "RHO_UA"), ("Phi_res", "PHI_RES_RESONANCE"),
                          ("omega_SCm", "OMEGA_SCM_HZ"), ("Lambda", "LAMBDA_SIMPLE"),
                          ("kappa", "KAPPA_PER_DAY"), ("k_spring", "K_SPRING"),
                          ("Mpc", "MPC_TO_M"), ("A_5", "A_5"), ("SO_5", "SO_5")):
        if target in ns:
            ns[alias] = ns[target]
    return ns


def _results_try_eval(form: str, ns: dict):
    expr = (form or "").replace("^", "**").replace("26!", "factorial(26)")
    expr = expr.replace("Phi_5/6", "PHI_RES_COUNTING")
    import warnings
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            v = eval(expr, {"__builtins__": {}}, dict(ns))  # restricted namespace
        return float(v)
    except Exception:
        return None


def calculate_results_table(dataset: dict | None = None, write: bool = True) -> dict:
    """Derive the physics results table LIVE (Daniel's order 2026-09-01).

    Baseline-preserving: the inherited table is copied once to
    RESULTS_BASELINE_CSV and never modified; live rows verify against it."""
    import os
    import shutil
    if not os.path.exists(RESULTS_BASELINE_CSV):
        shutil.copyfile(RESULTS_TABLE_CSV, RESULTS_BASELINE_CSV)
    with open(RESULTS_BASELINE_CSV, "r", encoding="utf-8", newline="") as f:
        base = list(csv.DictReader(f))
    ns = _results_eval_namespace()
    out_rows = []
    counts = {"VERIFIED_LIVE": 0, "INHERITED_CARRIED": 0, "LIVE_MISMATCH": 0}
    for r in base:
        live = _results_try_eval(r.get("closed_form", ""), ns)
        try:
            inherited = float(r.get("uqff_value", ""))
        except (TypeError, ValueError):
            inherited = None
        if live is None or inherited is None:
            status = "INHERITED_CARRIED"
            live_out = ""
        else:
            # verify at the baseline's own stated precision (the gate's
            # paper-precision rule): format the live value to the same
            # number of significant figures the inherited print carries.
            digits = len((r.get("uqff_value", "").split("e")[0].split("E")[0]
                          .replace("-", "").replace(".", "").lstrip("0")) or "1")
            digits = max(2, min(digits, 15))
            same = ("%.*g" % (digits, live)) == ("%.*g" % (digits, inherited))
            close = inherited != 0.0 and abs(live - inherited) / abs(inherited) < 1e-6
            exact_zero = inherited == 0.0 and abs(live) < 1e-12
            status = "VERIFIED_LIVE" if (same or close or exact_zero) else "LIVE_MISMATCH"
            live_out = repr(live)
        counts[status] += 1
        row = dict(r)
        row["live_value"] = live_out
        row["live_status"] = status
        out_rows.append(row)
    if write:
        fields = list(base[0].keys()) + ["live_value", "live_status"]
        with open(RESULTS_TABLE_CSV, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            w.writerows(out_rows)
        with open(RESULTS_TABLE_MD, "w", encoding="utf-8", newline="") as f:
            f.write("# UNIFIED_REGISTRY_RESULTS_TABLE.md — LIVE-DERIVED physics results table\n\n")
            f.write("**Derived live** (Daniel's order, 2026-09-01): every closed form is\n")
            f.write("re-evaluated at generation time from `uqff_registry_primitives`; each row\n")
            f.write("verifies against the immutable inherited baseline\n")
            f.write("(`UNIFIED_REGISTRY_RESULTS_TABLE_INHERITED.csv`, predecessor R0-R5 /\n")
            f.write("PAPER_2130 physics, preserved verbatim). Census: %d VERIFIED_LIVE, %d\n"
                    % (counts["VERIFIED_LIVE"], counts["INHERITED_CARRIED"]))
            f.write("INHERITED_CARRIED (form not evaluatable from primitives alone - carried,\n")
            f.write("never dropped), %d LIVE_MISMATCH (both values shown; nothing silently\n"
                    % counts["LIVE_MISMATCH"])
            f.write("replaced). Residuals are honest disclosures (Rule 7).\n\n")
            f.write("| Constant | Route | Closed form | Inherited value | Live value | Status | Reference | Residual % |\n")
            f.write("|---|---|---|---|---|---|---|:-:|\n")
            for r in out_rows:
                f.write("| %s | %s | `%s` | %s | %s | %s | %s | %s |\n" % (
                    r.get("constant", ""), r.get("canonical_route", ""),
                    r.get("closed_form", "").replace("|", "/"),
                    r.get("uqff_value", ""), r.get("live_value", ""),
                    r.get("live_status", ""),
                    r.get("reference", "").replace("|", "/"),
                    r.get("residual_pct", "")))
    return {"value": {"rows": len(out_rows), **counts},
            "source": "calculate_results_table (live, baseline-preserving)"}
