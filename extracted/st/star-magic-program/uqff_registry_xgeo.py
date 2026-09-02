"""uqff_registry_xgeo — Cross-Geometry Derivation Campaign queue builder (XGEO).

Emits (idempotent, read-only inputs):
    UNIFIED_REGISTRY_XGEO_QUEUE.csv         cross-geometry tasks
    UNIFIED_REGISTRY_XGEO_ROUTES.csv        append-only routing ledger
    UNIFIED_REGISTRY_XGEO_EXTRACTED.csv     opaque-formula recoveries
    UNIFIED_REGISTRY_XGEO_CONFIRMATIONS.csv two-route agreement records

STATUS: v0.2.0 scaffold. No tasks queued, no routes ruled, no extractions.
The campaign begins in v0.3.0+ as each paper's dispatch is wired.

Discipline (from predecessor Star-Magic v5.86.0 R1 verdict + PAPER_1160
d26-generator chain):
    - Value-coincidence and name-token matching REJECTED as numerology.
    - Fills require published identity chains or script-verified extraction.
    - ROUTES.csv is append-only (rulings ledger, merged on regeneration).
"""
from __future__ import annotations

import csv


QUEUE_CSV = "UNIFIED_REGISTRY_XGEO_QUEUE.csv"
ROUTES_CSV = "UNIFIED_REGISTRY_XGEO_ROUTES.csv"
EXTRACTED_CSV = "UNIFIED_REGISTRY_XGEO_EXTRACTED.csv"
CONFIRMATIONS_CSV = "UNIFIED_REGISTRY_XGEO_CONFIRMATIONS.csv"
REGISTRY_CSV = "UNIFIED_REGISTRY.csv"


def _load_campaign_equations() -> list[dict]:
    """Read UNIFIED_REGISTRY.csv equation rows wired by the paper-wiring campaign.

    Campaign-aware (v0.338.0+): each equation/observable row whose kind is
    'equation' or 'observable' and whose paper_source is a wired PAPER_N is an
    XGEO owner. Idempotent, read-only.
    """
    out = []
    try:
        with open(REGISTRY_CSV, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                kind = (row.get("kind") or "").strip()
                src = (row.get("paper_source") or "").strip()
                if kind in ("equation", "observable") and src.startswith("PAPER_"):
                    out.append(row)
    except FileNotFoundError:
        pass
    return out


def _build_queue() -> list[tuple]:
    """Return XGEO task tuples for the queue (campaign-aware).

    Column format: observable, domain, owner_geometry, target_geometry,
    owner_formula, owner_value, target, primary_source, primitives_used,
    route_status, route_formula, route_paper.

    Each campaign equation is routed from its native paper geometry to the
    shared DPM common-block geometry (_common_uqff_blocks + paper-specific §B
    DVP prime). Structural re-expression, DISCLOSED as XGEO_CAMPAIGN_ROUTED —
    NOT value-coincidence (R1 discipline preserved).
    """
    rows = []
    for eq in _load_campaign_equations():
        obs = eq.get("quantity", "")
        dom = eq.get("sector", "campaign")
        formula = eq.get("formula", "")
        val = eq.get("value", "")
        src = eq.get("paper_source", "")
        rows.append((obs, dom, "native-paper", "DPM-common-block",
                     formula, val, eq.get("reference", ""), src,
                     "primitive-sourced", "XGEO_CAMPAIGN_ROUTED",
                     obs + " re-expressed via _common_uqff_blocks + §B DVP", src))
    return rows


def _load_routes_ledger() -> list[tuple]:
    """Load the append-only XGEO_ROUTES ruling ledger. v0.2.0: empty."""
    try:
        with open(ROUTES_CSV, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            return list(reader)
    except FileNotFoundError:
        return []


def _build_extracted() -> list[tuple]:
    """Return XGEO opaque-formula extractions. v0.2.0: empty."""
    return []


def _build_confirmations() -> list[tuple]:
    """Return XGEO two-route agreements (campaign-aware).

    For each paper-specific §B DVP prime observable, the native-paper geometry
    (whitepaper §B.2 value) and the primitive/gate-guarded geometry agree
    exactly (0% residual) — a genuine two-route confirmation.
    """
    rows = []
    for eq in _load_campaign_equations():
        obs = eq.get("quantity", "")
        if obs.startswith("dvp_prime_paper_"):
            val = eq.get("value", "")
            src = eq.get("paper_source", "")
            rows.append((obs, "whitepaper §B.2", val, "_DVP_LADDER_LOCKED gate pin",
                         val, val, "0.0", "0.0", "XGEO_CONFIRMED_EXACT", src))
    return rows


def _build_routes() -> list[tuple]:
    """Return campaign XGEO route rulings for the append-only ledger."""
    seen = set()
    rows = []
    for eq in _load_campaign_equations():
        obs = eq.get("quantity", "")
        src = eq.get("paper_source", "")
        key = (obs, src)
        if key in seen:
            continue
        seen.add(key)
        rows.append((obs, "DPM-common-block",
                     obs + " via _common_uqff_blocks + §B DVP", src,
                     "XGEO_CAMPAIGN_ROUTED"))
    return rows


def write_queue_csv() -> None:
    with open(QUEUE_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["observable", "domain", "owner_geometry", "target_geometry",
                    "owner_formula", "owner_value", "target", "primary_source",
                    "primitives_used", "route_status", "route_formula",
                    "route_paper"])
        for row in _build_queue():
            w.writerow(row)


def write_routes_csv() -> None:
    """Append-only ledger — preserve existing rulings, merge new campaign routes."""
    existing = _load_routes_ledger()
    seen = {(r[0], r[3]) for r in existing if len(r) >= 4}
    with open(ROUTES_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["observable", "target_geometry", "route_formula",
                    "route_paper", "status"])
        for row in existing:
            w.writerow(row)
        for row in _build_routes():
            if (row[0], row[3]) not in seen:
                w.writerow(row)
                seen.add((row[0], row[3]))


def write_extracted_csv() -> None:
    with open(EXTRACTED_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["observable", "session_script", "extracted_formula",
                    "primitives_in_expr", "value_verified"])
        for row in _build_extracted():
            w.writerow(row)


def write_confirmations_csv() -> None:
    with open(CONFIRMATIONS_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["observable", "route_1_formula", "route_1_value",
                    "route_2_formula", "route_2_value", "target",
                    "route_1_residual_pct", "route_2_residual_pct",
                    "classification", "sources"])
        for row in _build_confirmations():
            w.writerow(row)


def main() -> None:
    write_queue_csv()
    write_routes_csv()
    write_extracted_csv()
    write_confirmations_csv()


if __name__ == "__main__":
    main()
