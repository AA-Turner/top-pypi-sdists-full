"""`efterlev scope` — shared-responsibility / inherited-control declaration.

FedRAMP runs on a shared-responsibility model. A CSP customer inherits
some controls from the cloud provider: an AWS serverless shop, for
example, inherits the host/hypervisor/patching controls AWS manages.
For those KSIs the honest status is **implemented (inherited)** — they
DO apply, the CSP satisfies them — not "not applicable" and not "not
implemented."

This is the 20x-accurate replacement for the originally-planned
"architecture → not_applicable" scoping. 20x KSIs are outcome-based and
architecture-agnostic; almost none are genuinely inapplicable to
serverless. They're satisfied differently (managed platform) or
inherited. See design notes 2026-05-20.

## Workflow

  1. `efterlev scope declare --profile aws-serverless`  (or `--ksi KSI-X`)
     → writes `[scope] inherited = [...]` to config. Pure declaration.
  2. `efterlev scan`  → produces evidence as usual.
  3. `efterlev scope apply`  → for each declared KSI, a DETERMINISTIC
     evidence cross-check:
       - scanner evidence cites the KSI  → CONTRADICTION (the customer
         manages it themselves, it isn't fully inherited) → skip + warn.
       - no scanner evidence  → write an `implemented` claim + an
         inheritance-basis evidence record, both loudly marked
         `[INHERITED — requires CSP-authorization confirmation + 3PAO
         review]`.
  4. `efterlev agent gap`  → skips KSIs that already have an inherited
     claim (so the agent doesn't clobber the deterministic declaration).

`report run` sequences scan → scope apply → gap automatically.

## Why deterministic cross-check, not LLM

The safety guarantee is "won't silently mask a real gap." "Does any
scanner evidence cite this KSI?" answers that deterministically: if the
customer has their own config for a supposedly-inherited control, the
scanner found it, and we refuse to mark it inherited. No LLM needed —
more reliable, free, and unit-testable.

## Built-in profiles are STARTER SUGGESTIONS

A profile's KSI list is a starting point to review against your CSP's
published customer-responsibility matrix — NOT an authoritative
determination. Inheritance depends on the provider's FedRAMP
authorization and your own configuration. Every emitted record says so.
You can also declare KSIs explicitly with `--ksi` and skip profiles
entirely.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import typer

# Inheritance profiles: profile name -> list of (KSI id, rationale).
# CONSERVATIVE + STARTER-ONLY. Each entry is a candidate the customer
# confirms against their CSP customer-responsibility matrix; the apply
# step additionally cross-checks against scanner evidence.
INHERITANCE_PROFILES: dict[str, list[tuple[str, str]]] = {
    "aws-serverless": [
        (
            "KSI-CNA-IBP",
            "Serverless compute (Lambda) is immutable by AWS's deployment "
            "model — each version is a fresh, read-only artifact; there is no "
            "in-place host the customer mutates.",
        ),
        (
            "KSI-CNA-OFA",
            "AWS managed serverless services (Lambda, API Gateway, DynamoDB, "
            "S3) are multi-AZ and high-availability by default; the underlying "
            "availability engineering is AWS-operated.",
        ),
        (
            "KSI-CNA-MAT",
            "For a no-EC2/no-VPC serverless system, the host- and "
            "hypervisor-layer attack surface is managed entirely by AWS; the "
            "customer's surface is limited to function code + API config.",
        ),
        (
            "KSI-CNA-RVP",
            "AWS Shield Standard provides always-on L3/L4 DDoS protection for "
            "AWS-managed endpoints at no charge. (Application-layer/L7 "
            "protection remains a customer responsibility — confirm WAF "
            "coverage before relying on this as fully inherited.)",
        ),
    ],
}


def available_profiles() -> list[str]:
    return sorted(INHERITANCE_PROFILES.keys())


def profile_ksis(profile: str) -> list[str]:
    """Return the KSI ids a profile declares inherited, in table order."""
    return [ksi for ksi, _ in INHERITANCE_PROFILES.get(profile, [])]


def rationale_for(profile: str | None, ksi: str) -> str:
    """Per-KSI rationale from a profile, or a generic one for ad-hoc KSIs."""
    if profile is not None:
        for k, reason in INHERITANCE_PROFILES.get(profile, []):
            if k == ksi:
                return reason
    return (
        "Declared CSP-inherited by the operator. Confirm against your cloud "
        "provider's FedRAMP customer-responsibility matrix."
    )


# The loud marker that prefixes every inherited rationale in the store, so
# a reviewer can never mistake an inherited assertion for a verified one.
INHERITED_MARKER = (
    "[INHERITED — shared responsibility; requires CSP-authorization confirmation + 3PAO review]"
)

INHERITED_DETECTOR_ID = "scope_inherited"
INHERITED_CLAIM_KIND = "inherited_classification"


def partition_inherited(
    declared: list[str], evidenced_ksis: set[str]
) -> tuple[list[str], list[str]]:
    """Split declared-inherited KSIs into (clean, contradicted).

    Pure + deterministic. A KSI is *contradicted* when scanner evidence
    cites it — the customer has their own configuration for a control
    they declared inherited, so it isn't fully inherited and must not be
    auto-marked. Clean KSIs (no scanner evidence) are safe to mark
    inherited.
    """
    clean: list[str] = []
    contradicted: list[str] = []
    for ksi in declared:
        if ksi in evidenced_ksis:
            contradicted.append(ksi)
        else:
            clean.append(ksi)
    return clean, contradicted


# --- command entry points ---------------------------------------------


def _load_config_or_exit(root: Path):
    from efterlev.config import load_config
    from efterlev.errors import ConfigError

    config_path = root / ".efterlev" / "config.toml"
    if not config_path.is_file():
        typer.echo(
            f"error: no config at {config_path}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)
    try:
        return load_config(config_path)
    except ConfigError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e


def _load_catalog_ksis(root: Path) -> set[str]:
    """The baseline KSI ids, for validating declared ids are real."""
    from efterlev.frmr.loader import FrmrDocument

    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        return set()
    doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    return set(doc.indicators.keys())


def run_scope_declare(
    target: Path,
    *,
    profile: str | None,
    ksis: list[str],
) -> int:
    """Write the inherited-control declaration to config. No store writes."""
    from efterlev.config import ScopeConfig, save_config

    root = target.resolve()
    config = _load_config_or_exit(root)

    if profile is not None and profile not in INHERITANCE_PROFILES:
        typer.echo(
            f"error: unknown profile {profile!r}. Available: {', '.join(available_profiles())}.",
            err=True,
        )
        raise typer.Exit(code=2)

    declared: list[str] = []
    if profile is not None:
        declared.extend(profile_ksis(profile))
    declared.extend(ksis)
    # De-dup, preserve order.
    seen: set[str] = set()
    deduped: list[str] = []
    for k in declared:
        if k not in seen:
            seen.add(k)
            deduped.append(k)

    if not deduped:
        typer.echo(
            "error: nothing to declare. Pass --profile <name> and/or --ksi <KSI-ID> (repeatable).",
            err=True,
        )
        raise typer.Exit(code=2)

    # Validate against the catalog when available — a typo'd KSI id should
    # surface now, not silently no-op at apply time.
    catalog = _load_catalog_ksis(root)
    if catalog:
        unknown = [k for k in deduped if k not in catalog]
        if unknown:
            typer.echo(
                f"error: not real KSI ids: {', '.join(unknown)}. "
                "Check `efterlev scope` help or the FRMR catalog.",
                err=True,
            )
            raise typer.Exit(code=2)

    new_scope = ScopeConfig(inherited=deduped, inherited_profile=profile)
    updated = config.model_copy(update={"scope": new_scope})
    save_config(updated, root / ".efterlev" / "config.toml")

    typer.echo(f"Declared {len(deduped)} KSI(s) as CSP-inherited:")
    for k in deduped:
        typer.echo(f"  {k}")
    if profile is not None:
        typer.echo(f"  (profile: {profile} — a starter list; review against your CRM)")
    typer.echo("")
    typer.echo("These are declarations only. Next:")
    typer.echo("  1. `efterlev scan`         produce evidence")
    typer.echo("  2. `efterlev scope apply`  cross-check + record inherited status")
    return 0


def run_scope_show(target: Path) -> int:
    """Print the current inherited-control declaration + rationale."""
    root = target.resolve()
    config = _load_config_or_exit(root)
    scope = config.scope
    if not scope.inherited:
        typer.echo("No inherited controls declared.")
        typer.echo("")
        typer.echo("Declare some with:")
        typer.echo("  efterlev scope declare --profile aws-serverless")
        typer.echo(f"  (available profiles: {', '.join(available_profiles())})")
        return 0

    typer.echo(
        f"{len(scope.inherited)} KSI(s) declared CSP-inherited"
        + (f" (profile: {scope.inherited_profile})" if scope.inherited_profile else "")
        + ":"
    )
    typer.echo("")
    for ksi in scope.inherited:
        typer.echo(f"  {ksi}")
        typer.echo(f"    {rationale_for(scope.inherited_profile, ksi)}")
    typer.echo("")
    typer.echo(
        "Reminder: inheritance depends on your CSP's FedRAMP authorization and "
        "your configuration. `efterlev scope apply` cross-checks each against "
        "scanner evidence; a 3PAO confirms the basis."
    )
    return 0


def run_scope_clear(target: Path) -> int:
    """Remove the inherited-control declaration from config."""
    from efterlev.config import ScopeConfig, save_config

    root = target.resolve()
    config = _load_config_or_exit(root)
    if not config.scope.inherited:
        typer.echo("No inherited controls declared; nothing to clear.")
        return 0
    n = len(config.scope.inherited)
    updated = config.model_copy(update={"scope": ScopeConfig()})
    save_config(updated, root / ".efterlev" / "config.toml")
    typer.echo(f"Cleared {n} inherited-control declaration(s).")
    typer.echo(
        "Note: any inherited claims already written to the store remain. "
        "Re-run `efterlev agent gap` to reclassify those KSIs from evidence."
    )
    return 0


def run_scope_apply(target: Path) -> int:
    """Cross-check declared inherited KSIs against evidence + record status.

    Deterministic. For each declared KSI with no contradicting scanner
    evidence, write an inheritance-basis Evidence record (so the KSI
    passes the RFC-0017 gate's inventory item) and an `implemented`
    Claim (so it passes the current-status item), both loudly marked.
    KSIs the scanner DID find evidence for are flagged, not marked.
    """
    from efterlev.models import Evidence
    from efterlev.models.claim import Claim
    from efterlev.models.source_ref import SourceRef
    from efterlev.provenance import ProvenanceStore

    root = target.resolve()
    config = _load_config_or_exit(root)
    declared = list(config.scope.inherited)
    profile = config.scope.inherited_profile
    if not declared:
        typer.echo("No inherited controls declared; nothing to apply.")
        typer.echo("Declare some first: `efterlev scope declare --profile <name>`.")
        return 0

    if not (root / ".efterlev").is_dir():
        typer.echo(f"error: no `.efterlev/` under {root}. Run `efterlev init`.", err=True)
        raise typer.Exit(code=1)

    catalog_controls = _load_catalog_controls(root)

    with ProvenanceStore(root) as store:
        # Build the "scanner found customer config" set from existing
        # evidence — EXCLUDING our own prior inheritance records.
        evidenced: set[str] = set()
        existing_inherited: set[str] = set()
        for _rid, payload in store.iter_evidence():
            if payload.get("detector_id") == INHERITED_DETECTOR_ID:
                for k in payload.get("ksis_evidenced", []) or []:
                    if isinstance(k, str):
                        existing_inherited.add(k)
                continue
            for k in payload.get("ksis_evidenced", []) or []:
                if isinstance(k, str):
                    evidenced.add(k)

        clean, contradicted = partition_inherited(declared, evidenced)
        # Don't double-write KSIs already recorded inherited on a prior run.
        to_write = [k for k in clean if k not in existing_inherited]
        already = [k for k in clean if k in existing_inherited]

        now = datetime.now(UTC)
        written = 0
        for ksi in to_write:
            reason = rationale_for(profile, ksi)
            marked_reason = f"{INHERITED_MARKER} {reason}"
            controls = catalog_controls.get(ksi, [])
            evidence = Evidence.create(
                detector_id=INHERITED_DETECTOR_ID,
                source_ref=SourceRef(file=Path(".efterlev/config.toml")),
                ksis_evidenced=[ksi],
                controls_evidenced=controls,
                content={
                    "inherited": True,
                    "inherited_profile": profile,
                    "basis": "shared-responsibility / CSP-inherited",
                    "rationale": marked_reason,
                },
                timestamp=now,
            )
            ev_record = store.write_record(
                payload=evidence.model_dump(mode="json"),
                record_type="evidence",
                primitive="scope_apply@0.1.0",
                metadata={"kind": "inherited_basis", "ksi_id": ksi},
            )
            claim = Claim.create(
                claim_type="classification",
                content={
                    "ksi_id": ksi,
                    "status": "implemented",
                    "rationale": marked_reason,
                },
                confidence="medium",
                derived_from=[ev_record.record_id],
                model="deterministic:scope-inherited@0.1.0",
                prompt_hash="",
            )
            store.write_record(
                payload=claim.model_dump(mode="json"),
                record_type="claim",
                derived_from=[ev_record.record_id],
                primitive="scope_apply@0.1.0",
                metadata={
                    "kind": INHERITED_CLAIM_KIND,
                    "ksi_id": ksi,
                    "status": "implemented",
                    "inherited_profile": profile,
                },
            )
            written += 1

    # Report.
    typer.echo(f"Inherited-control apply ({len(declared)} declared):")
    if written:
        typer.echo(f"  ✓ {written} marked implemented (inherited)")
    if already:
        typer.echo(f"  • {len(already)} already recorded inherited (skipped)")
    if contradicted:
        typer.echo("")
        typer.echo(
            f"  ⚠ {len(contradicted)} NOT marked — scanner found customer-side "
            "evidence (these aren't fully inherited; review):"
        )
        for ksi in contradicted:
            typer.echo(f"      {ksi}")
        typer.echo("")
        typer.echo(
            "    The cross-check refused to mark these inherited because you "
            "have your own configuration for them. `efterlev agent gap` will "
            "classify them from that evidence."
        )
    typer.echo("")
    typer.echo(
        "Every inherited record is marked DRAFT and requires a 3PAO to confirm "
        "the CSP's authorization covers the control."
    )
    return 0


def _load_catalog_controls(root: Path) -> dict[str, list[str]]:
    """KSI id -> mapped 800-53 controls, for the inheritance evidence."""
    from efterlev.frmr.loader import FrmrDocument

    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        return {}
    doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    return {k: list(ind.controls) for k, ind in doc.indicators.items()}


def inherited_ksis_in_store(root: Path) -> set[str]:
    """KSI ids that have an inherited claim in the store.

    Used by `efterlev agent gap` to skip KSIs already recorded inherited,
    so the agent doesn't clobber the deterministic declaration with a
    newer evidence-based claim.
    """
    from efterlev.provenance import ProvenanceStore

    if not (root / ".efterlev" / "store.db").is_file():
        return set()
    out: set[str] = set()
    with ProvenanceStore(root) as store:
        for _rid, metadata, _payload in store.iter_claims_by_metadata_kind(INHERITED_CLAIM_KIND):
            ksi = metadata.get("ksi_id")
            if isinstance(ksi, str):
                out.add(ksi)
    return out
