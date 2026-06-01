"""`efterlev plan` — Stage 0 (Strategic) pre-scan orientation.

The ISV journey's first stage is *deciding* to pursue FedRAMP 20x and
*scoping* the work — before any infrastructure-as-code exists to scan.
Every other Efterlev command assumes you're past that point (you've run
`init`, you have a workspace, you're collecting evidence). `plan` is the
one command that runs with NOTHING — no `.efterlev/`, no IaC, no API key
— and answers the Stage 0 question: *what am I getting into?*

It reads only bundled package data (the vendored FRMR catalog, the
detector→KSI registry, the manifest-template set, the inheritance
profiles) and prints the KSI landscape for a baseline:

  - how many KSIs Efterlev evidences automatically (from IaC/runtime),
  - how many need a human-authored Evidence Manifest (the procedural
    ones — personnel, training, incident response),
  - how many are hybrid,
  - and, for a chosen architecture, which are commonly CSP-inherited.

Deterministic; no LLM, no network, no filesystem writes. It's a map, not
a scan. This fills the "🟡 partial" Stage 0 gap documented in
docs/isv-journey.md (no pre-scan strategic walkthrough).

Deliberately NOT here: calendar-time / "days to authorization"
estimates. Effort is expressed in KSI-work units only — Efterlev
measures tool scope, never an authorization timeline.
"""

from __future__ import annotations

import importlib.resources
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

import typer

if TYPE_CHECKING:
    from efterlev.frmr.loader import FrmrDocument

# How a KSI is evidenced: "scanner" (detector only), "procedural" (manifest
# template only), "hybrid" (both), "uncovered" (neither — none today, but
# kept so a future catalog/detector change surfaces honestly rather than
# silently dropping a KSI).
Category = Literal["scanner", "procedural", "hybrid", "uncovered"]

_TEMPLATE_PKG = "efterlev.manifest_templates"
_TEMPLATE_SUFFIX = ".template.yml"
_DEFAULT_BASELINE = "fedramp-20x-moderate"

# Friendly `--architecture` values → inheritance-profile id (scope_cli).
# Only profiles that actually ship resolve to a real overlay; the rest
# render a graceful "no profile yet" note rather than a fake one.
_ARCH_ALIASES = {
    "serverless": "aws-serverless",
    "aws-serverless": "aws-serverless",
    "containers": "aws-containers",
    "aws-containers": "aws-containers",
    "ec2": "aws-ec2",
    "aws-ec2": "aws-ec2",
    "hybrid": "hybrid",
}
# Offered at the interactive prompt (plus a "skip" sentinel).
_ARCH_CHOICES = ["serverless", "containers", "ec2", "hybrid", "skip"]


@dataclass(frozen=True)
class ThemeRow:
    theme_id: str
    name: str
    total: int
    automated_only: int
    procedural_only: int
    hybrid: int

    @property
    def needs_manifest(self) -> int:
        return self.procedural_only + self.hybrid


@dataclass(frozen=True)
class PlanResult:
    baseline: str
    total: int
    theme_count: int
    automated_only: int
    procedural_only: int
    hybrid: int
    uncovered: int
    themes: list[ThemeRow]
    fully_automated_themes: list[str]
    architecture: str | None = None
    inherited_profile: str | None = None
    inherited_ksis: list[str] = field(default_factory=list)
    inherited_profile_known: bool = False


def _template_ksis() -> set[str]:
    """KSI ids that ship a manifest starter template (the procedural set)."""
    pkg = importlib.resources.files(_TEMPLATE_PKG)
    return {
        e.name[: -len(_TEMPLATE_SUFFIX)]
        for e in pkg.iterdir()
        if e.is_file() and e.name.endswith(_TEMPLATE_SUFFIX)
    }


def _detector_covered_ksis() -> set[str]:
    """KSI ids reachable from at least one detector (the scanner set)."""
    import efterlev.detectors  # noqa: F401 — import populates the registry
    from efterlev.detectors.base import get_registry

    covered: set[str] = set()
    for spec in get_registry().values():
        covered.update(spec.ksis)
    return covered


def load_baseline_landscape(
    baseline: str = _DEFAULT_BASELINE,
) -> tuple[FrmrDocument, set[str], set[str]]:
    """Load the FRMR doc + (detector-covered, procedural) KSI id sets for a baseline.

    Everything comes from bundled package data, so this works with no
    workspace. The two sets are the inputs to `classify_ksi`. Shared by
    `efterlev plan` and `efterlev catalog` so their per-KSI classification
    can never drift apart. Raises ValueError on an unsupported baseline.
    """
    from efterlev.frmr import load_frmr
    from efterlev.paths import vendored_catalogs_dir, verify_catalog_hashes
    from efterlev.workspace import _BASELINE_LEVEL, SUPPORTED_BASELINES

    if baseline not in SUPPORTED_BASELINES:
        raise ValueError(
            f"unknown baseline '{baseline}'. Supported: {sorted(SUPPORTED_BASELINES)}."
        )

    catalogs_dir = vendored_catalogs_dir()
    verify_catalog_hashes(catalogs_dir)
    doc = load_frmr(
        catalogs_dir / "frmr" / "FRMR.documentation.json",
        schema_path=catalogs_dir / "frmr" / "FedRAMP.schema.json",
        level=_BASELINE_LEVEL[baseline],
    )
    ksis = set(doc.indicators)
    return doc, _detector_covered_ksis() & ksis, _template_ksis() & ksis


def classify_ksi(ksi_id: str, covered: set[str], procedural: set[str]) -> Category:
    """How a KSI is evidenced, given the covered + procedural id sets."""
    c, p = ksi_id in covered, ksi_id in procedural
    if c and p:
        return "hybrid"
    if c:
        return "scanner"
    if p:
        return "procedural"
    return "uncovered"


def build_plan(baseline: str = _DEFAULT_BASELINE, architecture: str | None = None) -> PlanResult:
    """Classify a baseline's KSIs by evidence approach. Deterministic, no I/O writes.

    Loads everything from bundled package data, so this works with no
    workspace. `architecture` (a friendly name like "serverless") overlays
    the CSP-inheritance profile when one ships for it.
    """
    doc, covered, procedural = load_baseline_landscape(baseline)
    ksis = set(doc.indicators)

    auto_only = pro_only = hybrid = uncovered = 0
    from collections import defaultdict

    per: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0])  # total, auto, pro, hybrid
    for kid, ind in doc.indicators.items():
        cat = classify_ksi(kid, covered, procedural)
        row = per[ind.theme]
        row[0] += 1
        if cat == "hybrid":
            hybrid += 1
            row[3] += 1
        elif cat == "scanner":
            auto_only += 1
            row[1] += 1
        elif cat == "procedural":
            pro_only += 1
            row[2] += 1
        else:
            uncovered += 1

    theme_rows = [
        ThemeRow(
            theme_id=tid,
            name=doc.themes[tid].name if tid in doc.themes else tid,
            total=v[0],
            automated_only=v[1],
            procedural_only=v[2],
            hybrid=v[3],
        )
        for tid, v in per.items()
    ]
    # Themes with human work first (most manifests needed), then by id.
    theme_rows.sort(key=lambda r: (-r.needs_manifest, r.theme_id))
    fully_automated = sorted(r.theme_id for r in theme_rows if r.needs_manifest == 0)

    inherited_profile: str | None = None
    inherited: list[str] = []
    profile_known = False
    if architecture:
        from efterlev.cli.scope_cli import INHERITANCE_PROFILES, profile_ksis

        inherited_profile = _ARCH_ALIASES.get(architecture.lower(), architecture)
        if inherited_profile in INHERITANCE_PROFILES:
            profile_known = True
            inherited = [k for k in profile_ksis(inherited_profile) if k in ksis]

    return PlanResult(
        baseline=baseline,
        total=len(ksis),
        theme_count=len(doc.themes),
        automated_only=auto_only,
        procedural_only=pro_only,
        hybrid=hybrid,
        uncovered=uncovered,
        themes=theme_rows,
        fully_automated_themes=fully_automated,
        architecture=architecture,
        inherited_profile=inherited_profile,
        inherited_ksis=inherited,
        inherited_profile_known=profile_known,
    )


def _baseline_title(baseline: str) -> str:
    if baseline == "fedramp-20x-moderate":
        return "FedRAMP 20x Moderate"
    return baseline


def render_plan(result: PlanResult) -> str:
    """Render a PlanResult as the human-readable Stage 0 map. Pure function."""
    out: list[str] = []
    out.append(f"{_baseline_title(result.baseline)} — your KSI landscape (before you scan)")
    out.append("")
    out.append(f"  {result.total} Key Security Indicators across {result.theme_count} themes.")
    out.append("")
    out.append("How Efterlev evidences each one:")
    out.append("")
    out.append(
        f"  Automated from your IaC / runtime ... {result.automated_only:>2}   "
        "scanner finds the evidence; you configure infra + run `efterlev scan`"
    )
    out.append(
        f"  You author an Evidence Manifest ..... {result.procedural_only:>2}   "
        "procedural KSIs (personnel, training, incident response) — "
        "`efterlev manifests draft <KSI>`"
    )
    out.append(
        f"  Hybrid (scanner + a manifest) ....... {result.hybrid:>2}   "
        "scanner gives partial evidence; an attestation completes it"
    )
    if result.uncovered:
        out.append(
            f"  Not yet automated (manual) .......... {result.uncovered:>2}   "
            "no detector or template yet — track manually for now"
        )
    out.append("")

    work_themes = [t for t in result.themes if t.needs_manifest > 0]
    if work_themes:
        out.append("Where the human work concentrates (KSIs needing a manifest):")
        out.append("")
        for t in work_themes:
            label = f"{t.theme_id}  {t.name}"
            out.append(f"  {label:<42} {t.needs_manifest:>2} of {t.total:>2} need a manifest")
        out.append("")
    if result.fully_automated_themes:
        out.append(
            "Fully automated themes (no manifests needed): "
            + ", ".join(result.fully_automated_themes)
        )
        out.append("")

    if result.architecture:
        out.append(f"Architecture: {result.architecture}")
        if result.inherited_profile_known and result.inherited_ksis:
            n = len(result.inherited_ksis)
            out.append(f"  {n} of your automated KSIs are commonly CSP-inherited under shared")
            out.append("  responsibility:")
            out.append("    " + ", ".join(result.inherited_ksis))
            out.append(
                f"  You may declare these via `efterlev scope --inherited "
                f"{result.inherited_profile}`"
            )
            out.append("  instead of implementing them yourself (requires CSP-authorization")
            out.append("  confirmation + 3PAO review).")
        else:
            out.append(
                f"  No CSP-inheritance profile ships for '{result.architecture}' yet — treat every"
            )
            out.append("  KSI as yours to implement or attest. You can still declare specific")
            out.append("  inherited controls manually with `efterlev scope --inherited`.")
        out.append("")
    else:
        out.append("Tip: pass `--architecture serverless` to see which KSIs you may be able to")
        out.append("  inherit from your cloud provider under shared responsibility.")
        out.append("")

    out.append("Realistic next steps:")
    out.append("  1. efterlev catalog               browse every KSI + its mapped controls")
    out.append("  2. efterlev init                  scaffold a workspace for this baseline")
    out.append("  3. efterlev scan                  collect the automated evidence")
    out.append("  4. efterlev manifests draft <KSI>  author the procedural attestations")
    out.append("  5. efterlev readiness             track how close you are to submission")
    out.append("")
    out.append("Still deciding 20x vs the Rev 5 process? See docs/choosing-20x.md.")
    out.append("This command touched nothing — no files written, no API calls. It's a map.")
    return "\n".join(out)


def run_plan(baseline: str = _DEFAULT_BASELINE, architecture: str | None = None) -> int:
    """Resolve architecture (flag, or interactive prompt), build, render. Exit code."""
    from efterlev.cli.first_run_wizard import is_interactive

    if architecture is None and is_interactive():
        typer.echo("")
        typer.echo("What's your primary architecture? This refines which KSIs you may inherit")
        typer.echo(f"  from your cloud provider. Choices: {', '.join(_ARCH_CHOICES)}")
        choice = typer.prompt("Architecture", default="skip", show_default=True).strip().lower()
        if choice and choice != "skip":
            architecture = choice

    try:
        result = build_plan(baseline=baseline, architecture=architecture)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        return 2

    typer.echo("")
    typer.echo(render_plan(result))
    return 0
