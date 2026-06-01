"""`efterlev catalog` — browse the KSI catalog for a baseline (Stage 0).

Where `efterlev plan` gives the aggregate strategic view (how many KSIs,
where the human work concentrates), `catalog` is the detailed reference:
every KSI listed, grouped by theme, with how Efterlev evidences it
(scanner / manifest / hybrid) and its mapped NIST 800-53 controls. It
answers "show me exactly what I'll be measured against" — the companion
to plan's "how much work is this?".

Like `plan`, it runs with NOTHING — no workspace, no IaC, no API key —
reading only bundled package data (the vendored FRMR catalog + the
detector→KSI registry + the manifest-template set). It shares plan's
classification helpers so the two commands can never disagree about how a
KSI is evidenced. Deterministic; no LLM, no network, no writes.
"""

from __future__ import annotations

from dataclasses import dataclass

import typer

from efterlev.cli.plan import Category, classify_ksi, load_baseline_landscape

_DEFAULT_BASELINE = "fedramp-20x-moderate"

# One-word human label per evidence category, for the listing.
_CATEGORY_LABEL: dict[Category, str] = {
    "scanner": "scanner",
    "procedural": "manifest",
    "hybrid": "hybrid",
    "uncovered": "manual",
}


@dataclass(frozen=True)
class CatalogEntry:
    ksi_id: str
    name: str
    theme_id: str
    category: Category
    controls: list[str]
    statement: str


@dataclass(frozen=True)
class CatalogTheme:
    theme_id: str
    name: str
    entries: list[CatalogEntry]


@dataclass(frozen=True)
class CatalogResult:
    baseline: str
    themes: list[CatalogTheme]

    @property
    def total(self) -> int:
        return sum(len(t.entries) for t in self.themes)


def build_catalog(baseline: str = _DEFAULT_BASELINE, theme: str | None = None) -> CatalogResult:
    """Build the per-KSI catalog for a baseline. Deterministic, no workspace.

    `theme` (case-insensitive theme id like "AFR") filters to one theme;
    raises ValueError if it names no theme in the baseline.
    """
    doc, covered, procedural = load_baseline_landscape(baseline)

    theme_filter = theme.strip().upper() if theme else None
    if theme_filter is not None and theme_filter not in doc.themes:
        raise ValueError(
            f"unknown theme '{theme}'. Themes in this baseline: {', '.join(sorted(doc.themes))}."
        )

    entries_by_theme: dict[str, list[CatalogEntry]] = {tid: [] for tid in doc.themes}
    for kid, ind in doc.indicators.items():
        if theme_filter is not None and ind.theme != theme_filter:
            continue
        entries_by_theme.setdefault(ind.theme, []).append(
            CatalogEntry(
                ksi_id=kid,
                name=ind.name,
                theme_id=ind.theme,
                category=classify_ksi(kid, covered, procedural),
                controls=list(ind.controls),
                statement=ind.statement or "",
            )
        )

    themes: list[CatalogTheme] = []
    for tid in sorted(entries_by_theme):
        entries = entries_by_theme[tid]
        if not entries:
            continue  # filtered out, or a theme with no indicators
        entries.sort(key=lambda e: e.ksi_id)
        name = doc.themes[tid].name if tid in doc.themes else tid
        themes.append(CatalogTheme(theme_id=tid, name=name, entries=entries))

    return CatalogResult(baseline=baseline, themes=themes)


def _baseline_title(baseline: str) -> str:
    return "FedRAMP 20x Moderate" if baseline == "fedramp-20x-moderate" else baseline


def render_catalog(result: CatalogResult) -> str:
    """Render a CatalogResult as a grouped, human-readable listing. Pure function."""
    out: list[str] = []
    out.append(f"{_baseline_title(result.baseline)} — {result.total} Key Security Indicators")
    out.append("")
    out.append(
        "  Evidenced by: [scanner] your IaC/runtime · [manifest] an Evidence "
        "Manifest you author · [hybrid] both"
    )
    out.append("")
    for theme in result.themes:
        out.append(f"{theme.theme_id} — {theme.name}")
        for e in theme.entries:
            tag = _CATEGORY_LABEL[e.category]
            out.append(f"  {e.ksi_id:<14} [{tag:<8}] {e.name}")
            if e.controls:
                out.append(f"  {'':<14}  controls: {', '.join(e.controls)}")
        out.append("")
    out.append(
        "Next: `efterlev plan` for the work breakdown, or `efterlev manifests "
        "draft <KSI>` to author a procedural attestation."
    )
    return "\n".join(out)


def catalog_to_dict(result: CatalogResult) -> dict[str, object]:
    """JSON-serializable view of the catalog (for `--json`)."""
    return {
        "baseline": result.baseline,
        "total": result.total,
        "themes": [
            {
                "id": t.theme_id,
                "name": t.name,
                "ksis": [
                    {
                        "id": e.ksi_id,
                        "name": e.name,
                        "evidence": e.category,
                        "controls": e.controls,
                        "statement": e.statement,
                    }
                    for e in t.entries
                ],
            }
            for t in result.themes
        ],
    }


def run_catalog(
    baseline: str = _DEFAULT_BASELINE,
    theme: str | None = None,
    json_output: bool = False,
) -> int:
    """Build + print the catalog. Exit code (0 ok, 2 on bad baseline/theme)."""
    try:
        result = build_catalog(baseline=baseline, theme=theme)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        return 2

    if json_output:
        import json

        typer.echo(json.dumps(catalog_to_dict(result), indent=2))
        return 0

    typer.echo("")
    typer.echo(render_catalog(result))
    return 0
