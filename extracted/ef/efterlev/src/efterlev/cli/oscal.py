"""`efterlev oscal` subcommand — emit OSCAL 1.0.4 artifacts.

Supported kinds:
- v0.1.105: `poam` (Plan of Action and Milestones)
- v0.1.108: `component-definition` (system component implementation)
- v0.1.109+: `partial-ssp` (planned)

Why a dedicated subcommand (not a flag on `report run`):

  - OSCAL has multiple output kinds (POA&M, component-definition,
    partial-SSP). Each is a distinct schema with its own input
    requirements. Subcommand namespace lets us add `oscal validate`,
    `oscal export --kind component-definition`, etc. without
    overloading the top-level CLI.
  - `efterlev report run` users who don't care about OSCAL shouldn't
    pay the OSCAL emit cost (deterministic but still work).
  - Trestle (IBM) uses the subcommand pattern;
    this keeps the OSCAL-tool surface familiar to compliance users.

OSCAL version: 1.0.4 (FedRAMP-current). When FedRAMP publishes
1.1.0 guidance, add a `--oscal-version` flag.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import typer

oscal_app = typer.Typer(
    name="oscal",
    help="Emit OSCAL 1.0.4 artifacts (POA&M + component-definition; partial-SSP planned).",
    no_args_is_help=True,
)

_SUPPORTED_KINDS = ("poam", "component-definition")


@oscal_app.command("export")
def oscal_export(
    kind: str = typer.Option(
        ...,
        "--kind",
        help=(
            "OSCAL artifact to emit. Supported: `poam` (Plan of Action and "
            "Milestones, v0.1.105), `component-definition` (system component "
            "implementation, v0.1.108). `partial-ssp` planned for v0.1.109+."
        ),
    ),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the workspace whose `.efterlev/` store will be read.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Write the OSCAL JSON to this file. Defaults to "
            "`efterlev-out/reports/oscal/<kind>-<timestamp>.json` "
            "(v0.1.160+ visible-output split)."
        ),
    ),
    system_name: str = typer.Option(
        "Unnamed System (efterlev placeholder)",
        "--system-name",
        help=(
            "Human-readable system name for the OSCAL `metadata.title`. "
            "Override before submitting to a 3PAO; the default is a "
            "placeholder that flags the gap."
        ),
    ),
    system_id: str = typer.Option(
        "efterlev-system-default",
        "--system-id",
        help=(
            "OSCAL `system-id` value. Override with the system's authoritative "
            "identifier (FedRAMP-issued ID for FedRAMP submissions, internal "
            "system inventory ID otherwise)."
        ),
    ),
    narratives_from: Path | None = typer.Option(
        None,
        "--narratives-from",
        help=(
            "Path to a Documentation Agent `attestation-*.json` artifact. Used "
            "with `--kind component-definition` to populate per-control "
            "implemented-requirement.statements[] with the agent's narrative "
            "prose. Ignored for `--kind poam`."
        ),
    ),
) -> None:
    """Emit an OSCAL artifact (`poam` or `component-definition`).

    Reads the latest Gap Agent classifications from the workspace's
    provenance store, resolves each KSI against the loaded FRMR catalog,
    and writes an OSCAL 1.0.4 JSON document.

    Deterministic: same Gap Agent classifications + same FRMR + same
    `last-modified` timestamp produce byte-identical OSCAL JSON. UUIDs
    are derived via `uuid5` from a fixed namespace + the underlying
    KSI/control identifiers, so re-runs of the same scan produce
    stable diffs (important for tracking deltas across release cycles).
    """
    if kind not in _SUPPORTED_KINDS:
        typer.echo(
            f"error: --kind={kind!r} not supported. Choose from "
            f"{list(_SUPPORTED_KINDS)}. `partial-ssp` planned for v0.1.109+.",
            err=True,
        )
        raise typer.Exit(code=2)

    # Lazy imports keep the CLI startup fast for unrelated subcommands.
    from efterlev.agents import (
        count_duplicate_classification_runs,
        reconstruct_classifications_from_store,
    )
    from efterlev.frmr.loader import FrmrDocument
    from efterlev.primitives.generate import (
        GenerateComponentDefinitionOscalInput,
        GeneratePoamOscalInput,
        PoamClassificationInput,
        generate_component_definition_oscal,
        generate_poam_oscal,
    )
    from efterlev.provenance import ProvenanceStore, active_store

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Re-run `efterlev init`.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))

    with ProvenanceStore(root) as store, active_store(store):
        rows = store.iter_claims_by_metadata_kind("ksi_classification")
        duplicate_count = count_duplicate_classification_runs(rows)
        # v0.1.147 / #352: drop pre-v0.1.146 stale unknown-KSI records.
        classifications = reconstruct_classifications_from_store(
            rows, baseline_ksi_ids=set(frmr_doc.indicators.keys())
        )
        if duplicate_count > 0:
            typer.echo(
                f"note: deduped {duplicate_count} duplicate classification(s) "
                f"from prior `agent gap` runs (latest-wins).",
                err=True,
            )
        if not classifications:
            typer.echo(
                "error: 0 Gap Agent classifications in the store. The Gap Agent "
                "either hasn't run yet, or ran with no evidence to classify "
                "(check `efterlev scan` first if you skipped that stage).",
                err=True,
            )
            raise typer.Exit(code=1)

        poam_inputs = [
            PoamClassificationInput(
                ksi_id=c.ksi_id,
                status=c.status,
                rationale=c.rationale,
                evidence_ids=list(c.evidence_ids),
                claim_record_id=None,
            )
            for c in classifications
        ]

        timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
        last_modified = datetime.now(UTC)

        if kind == "poam":
            poam_result = generate_poam_oscal(
                GeneratePoamOscalInput(
                    classifications=poam_inputs,
                    indicators=frmr_doc.indicators,
                    baseline_id="fedramp-20x-moderate",
                    frmr_version=frmr_doc.version,
                    system_name=system_name,
                    system_id=system_id,
                    last_modified=last_modified,
                )
            )
            output_doc = poam_result.oscal_document
            summary_label = "OSCAL POA&M"
            summary_count = ("poam-items", poam_result.item_count)
            skipped = poam_result.skipped_unknown_ksi
            default_filename = f"poam-{timestamp}.json"
        else:  # component-definition
            narratives: dict[str, str] = {}
            if narratives_from is not None:
                # Load Documentation Agent attestation; extract per-KSI narratives.
                # AttestationArtifact shape: KSI[theme].indicators[ksi_id].narrative.
                from efterlev.models import AttestationArtifact

                artifact = AttestationArtifact.model_validate_json(
                    narratives_from.read_text(encoding="utf-8")
                )
                for theme in artifact.KSI.values():
                    for ksi_id, ind in theme.indicators.items():
                        if ind.narrative:
                            narratives[ksi_id] = ind.narrative

            cd_result = generate_component_definition_oscal(
                GenerateComponentDefinitionOscalInput(
                    classifications=poam_inputs,
                    indicators=frmr_doc.indicators,
                    baseline_id="fedramp-20x-moderate",
                    frmr_version=frmr_doc.version,
                    system_name=system_name,
                    system_id=system_id,
                    narratives=narratives,
                    last_modified=last_modified,
                )
            )
            output_doc = cd_result.oscal_document
            summary_label = "OSCAL Component-Definition"
            summary_count = (
                "implemented-requirements",
                cd_result.implemented_requirement_count,
            )
            skipped = cd_result.skipped_unknown_ksi
            default_filename = f"component-definition-{timestamp}.json"

    # v0.1.160 / #365: OSCAL emit lands in the visible output dir.
    from efterlev.paths import oscal_dir

    output_path = output or (oscal_dir(root) / default_filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output_doc, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )

    typer.echo(f"{summary_label}: {output_path.resolve()}")
    typer.echo("  oscal-version:    1.0.4")
    typer.echo(f"  {summary_count[0]}: {summary_count[1]}")
    if skipped:
        typer.echo(
            f"  skipped (unknown KSI in indicator dict): {', '.join(sorted(skipped))}",
            err=True,
        )
    typer.echo(
        "  reviewer:         override --system-name and --system-id with the "
        "authoritative values before submitting to a 3PAO",
        err=True,
    )
