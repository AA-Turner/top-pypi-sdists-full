"""`efterlev manifests draft <KSI>` — interactive Evidence Manifest scaffolder.

Procedural KSIs (the AFR / CED / INR / PIY / RPL themes, plus a few like
CMT-RVP / MLA-RVL / SVC-EIS / SVC-PRR) classify as
`evidence_layer_inapplicable` until the customer authors an Evidence
Manifest — the Terraform/CFN/CDK scanner structurally can't see a
monitored security inbox, a training program, or an incident-review
cadence. The bundled starter templates (`efterlev manifests init
--starter-pack`) carry per-KSI guidance, but the customer still has to
hand-edit YAML: fill DRAFT placeholders, remove the `_template_help`
block, get the schema right. That blank-page-plus-YAML friction is the
#1 remaining Stage-1 step before a workspace is submission-ready.

`manifests draft` removes it: it reads the bundled template's per-KSI
questions, walks them as interactive prompts, then writes a CLEAN,
schema-valid `.efterlev/manifests/<ksi>.yml` (no DRAFT placeholders, no
help block, dates defaulted) ready for the next `efterlev scan` to load.

## Deliberate scope — guidance, not fabrication

The helper is **deterministic; no LLM**. It NEVER drafts the attestation
prose for you. An attestation is a compliance claim the customer must
legally own ("we operate a monitored security inbox with a 15-minute
SLA") — having an LLM invent that text would be worse than a blank page:
it would put words in the customer's mouth that may not be true. So the
helper provides STRUCTURE (the schema) and GUIDANCE (the KSI's
statement, mapped controls, and the specific questions to address); the
words are the customer's.
"""

from __future__ import annotations

import importlib.resources
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import typer
import yaml

# Bundled per-KSI templates live here; filenames are `<KSI-ID>.template.yml`.
_TEMPLATE_PKG = "efterlev.manifest_templates"
# Default human-review cadence for the next_review date (templates suggest 6mo).
_DEFAULT_REVIEW_MONTHS = 6


@dataclass(frozen=True)
class ManifestTemplate:
    """The bundled guidance for one KSI's manifest."""

    ksi_id: str
    name: str
    description: str
    questions: list[str] = field(default_factory=list)


def load_template(ksi_id: str) -> ManifestTemplate | None:
    """Return the bundled template guidance for `ksi_id`, or None if none ships.

    A template ships only for the procedural KSIs (the ones a manifest is
    meant for). A None return is the signal that `ksi_id` is either not a
    real KSI or is scanner-evidenceable rather than procedural.
    """
    fname = f"{ksi_id}.template.yml"
    try:
        pkg = importlib.resources.files(_TEMPLATE_PKG)
        entry = pkg / fname
        if not entry.is_file():
            return None
        raw = yaml.safe_load(entry.read_text(encoding="utf-8")) or {}
    except (FileNotFoundError, ModuleNotFoundError, yaml.YAMLError):
        return None
    if not isinstance(raw, dict):
        return None
    help_block = raw.get("_template_help") or {}
    questions = help_block.get("questions") if isinstance(help_block, dict) else None
    return ManifestTemplate(
        ksi_id=ksi_id,
        name=str(raw.get("name") or ksi_id),
        description=str(help_block.get("description", "")).strip()
        if isinstance(help_block, dict)
        else "",
        questions=[str(q) for q in questions] if isinstance(questions, list) else [],
    )


def render_manifest_yaml(
    *,
    ksi_id: str,
    name: str,
    statement: str,
    attested_by: str,
    attested_at: date,
    reviewed_at: date | None,
    next_review: date | None,
    supporting_docs: list[str],
) -> str:
    """Serialize a clean, schema-valid Evidence Manifest to YAML.

    Validates the content through the real `EvidenceManifest` /
    `ManifestAttestation` models before serializing, so the file this
    writes is guaranteed to load (the loader uses `extra="forbid"`; this
    output carries no `_template_help` and no DRAFT placeholders).
    """
    from efterlev.models.manifest import EvidenceManifest, ManifestAttestation

    attestation = ManifestAttestation(
        type="attestation",
        statement=statement,
        attested_by=attested_by,
        attested_at=attested_at,
        reviewed_at=reviewed_at,
        next_review=next_review,
        supporting_docs=supporting_docs,
    )
    manifest = EvidenceManifest(ksi=ksi_id, name=name, evidence=[attestation])
    # model_validate round-trips the dump back through validation as a
    # belt-and-suspenders guarantee the written file loads.
    EvidenceManifest.model_validate(manifest.model_dump())

    ev: dict[str, Any] = {
        "type": "attestation",
        "statement": statement,
        "attested_by": attested_by,
        "attested_at": attested_at.isoformat(),
    }
    if reviewed_at is not None:
        ev["reviewed_at"] = reviewed_at.isoformat()
    if next_review is not None:
        ev["next_review"] = next_review.isoformat()
    if supporting_docs:
        ev["supporting_docs"] = supporting_docs
    doc = {"ksi": ksi_id, "name": name, "evidence": [ev]}
    header = (
        f"# {ksi_id} — {name}\n"
        f"# Evidence Manifest authored via `efterlev manifests draft`.\n"
        f"# Review the statement before relying on it — it is a compliance\n"
        f"# attestation you own. Re-run `efterlev scan` to load it.\n"
    )
    body = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False)
    return header + body


# --- interactive runner -----------------------------------------------


def run_manifest_draft(target: Path, ksi_id: str, *, force: bool) -> int:
    """Walk the interactive draft for one KSI; write the manifest. Exit code."""
    from efterlev.cli.first_run_wizard import is_interactive

    ksi_id = ksi_id.strip().upper()
    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        return 1

    # The KSI must be a real catalog id (validate against the FRMR cache).
    catalog = _load_catalog(root)
    if catalog is not None and ksi_id not in catalog:
        typer.echo(
            f"error: {ksi_id} is not a KSI in this workspace's baseline. "
            "Check the id (e.g. KSI-AFR-ADS).",
            err=True,
        )
        return 2

    template = load_template(ksi_id)
    if template is None:
        typer.echo(
            f"error: no manifest template ships for {ksi_id}. Manifests are for "
            "PROCEDURAL KSIs (personnel, training, incident-response, review "
            "cadences — the AFR / CED / INR / PIY / RPL themes). If this KSI is "
            "scanner-evidenceable, it doesn't need a manifest; if you still want "
            "to hand-author one, see `efterlev manifests init --starter-pack`.",
            err=True,
        )
        return 2

    dest = root / ".efterlev" / "manifests" / f"{ksi_id.lower()}.yml"
    if dest.exists() and not force:
        typer.echo(
            f"error: {dest} already exists. Pass --force to overwrite, or edit it directly.",
            err=True,
        )
        return 2

    if not is_interactive():
        typer.echo(
            "error: `manifests draft` is interactive (it walks you through the "
            "attestation questions). Run it on a terminal. To get the template "
            "file to hand-edit instead, run `efterlev manifests init --starter-pack`.",
            err=True,
        )
        return 2

    # --- the guided walk ---
    ind = catalog.get(ksi_id) if catalog else None
    typer.echo("")
    typer.echo(f"Drafting Evidence Manifest for {ksi_id} — {template.name}")
    if ind is not None:
        if ind.get("statement"):
            typer.echo("")
            typer.echo(f"  KSI outcome: {ind['statement']}")
        if ind.get("controls"):
            typer.echo(f"  Mapped 800-53 controls: {', '.join(ind['controls'])}")
    if template.description:
        typer.echo("")
        typer.echo(f"  {template.description}")
    typer.echo("")
    typer.echo(
        "I'll ask the questions this KSI's attestation should address. Answer in "
        "your own words — these become YOUR signed statement, so describe what "
        "your organization ACTUALLY does (leave an answer blank to skip it)."
    )

    answers: list[str] = []
    for i, q in enumerate(template.questions, start=1):
        typer.echo("")
        typer.echo(f"  Q{i}. {q}")
        ans = typer.prompt("    >", default="", show_default=False).strip()
        if ans:
            answers.append(ans)

    if not answers:
        typer.echo(
            "\nerror: no answers given — nothing to attest. Re-run when you're "
            "ready to describe this control.",
            err=True,
        )
        return 1

    statement = " ".join(answers)
    typer.echo("")
    typer.echo("Assembled statement:")
    typer.echo(f"  {statement}")
    typer.echo("")

    attested_by = ""
    while not attested_by:
        attested_by = typer.prompt(
            "Who is attesting this? (email or name of the accountable owner)"
        ).strip()

    today = date.today()
    attested_at = _prompt_date("Attestation date", default=today)
    reviewed_at = _prompt_date("Last reviewed date", default=today)
    next_default = _add_months(today, _DEFAULT_REVIEW_MONTHS)
    next_review = _prompt_date(
        f"Next review date (default = +{_DEFAULT_REVIEW_MONTHS} months)", default=next_default
    )

    typer.echo("")
    typer.echo("Supporting docs (paths or URLs to runbooks/policies). Empty line to finish.")
    docs: list[str] = []
    while True:
        d = typer.prompt(f"  doc #{len(docs) + 1}", default="", show_default=False).strip()
        if not d:
            break
        docs.append(d)

    yaml_text = render_manifest_yaml(
        ksi_id=ksi_id,
        name=template.name,
        statement=statement,
        attested_by=attested_by,
        attested_at=attested_at,
        reviewed_at=reviewed_at,
        next_review=next_review,
        supporting_docs=docs,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(yaml_text, encoding="utf-8")

    typer.echo("")
    typer.echo(f"Wrote {dest}")
    typer.echo("  Review the statement once more — it's a compliance attestation you own.")
    typer.echo("  Then run `efterlev scan` to load it into the evidence store.")
    return 0


def _prompt_date(label: str, *, default: date) -> date:
    """Prompt for an ISO date; re-prompt on parse failure; Enter accepts default."""
    while True:
        raw = typer.prompt(f"{label} (YYYY-MM-DD)", default=default.isoformat()).strip()
        try:
            return date.fromisoformat(raw)
        except ValueError:
            typer.echo(f"  '{raw}' isn't a valid YYYY-MM-DD date. Try again.")


def _add_months(d: date, months: int) -> date:
    """Add `months` to a date, clamping the day to the target month's length."""
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    # Clamp day (e.g. Aug 31 + 6mo -> Feb 28/29).
    day = min(d.day, _days_in_month(year, month))
    return date(year, month, day)


def _days_in_month(year: int, month: int) -> int:
    import calendar

    return calendar.monthrange(year, month)[1]


def _load_catalog(root: Path) -> dict[str, dict[str, Any]] | None:
    """Return {ksi_id: {statement, controls, name}} from the FRMR cache, or None."""
    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        return None
    from efterlev.frmr.loader import FrmrDocument

    doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    return {
        k: {
            "statement": ind.statement or "",
            "controls": list(ind.controls),
            "name": ind.name,
        }
        for k, ind in doc.indicators.items()
    }
