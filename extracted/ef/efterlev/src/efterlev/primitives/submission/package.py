"""Build a submission package — zip (or directory) containing 3PAO-ready artifacts.

Picks the LATEST of each artifact type from `.efterlev/reports/` and
`.efterlev/manifests/` and bundles them with a README that explains
what's inside, when it was built, and how the 3PAO should read it.

The artifact set at v0.1.135:
- FRMR attestation JSON (Documentation Agent output)
- POA&M markdown (reviewer-ready punch list)
- OSCAL POA&M JSON (machine-readable, validated against NIST schema + FedRAMP rules + oscal-cli)
- OSCAL Component-Definition JSON
- HTML gap report (color-coded KSI status overview)
- HTML documentation report (FRMR-shaped narrative view)
- Evidence Manifests (procedural attestations the customer authored)
- README.md (the per-package narrative the 3PAO reads first)
- index.json (machine-readable manifest of what's in the package + their hashes)
"""

from __future__ import annotations

import hashlib
import io
import zipfile
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class SubmissionManifest:
    """Catalog of one artifact in the package."""

    archive_path: str
    """Path inside the archive (POSIX-style, no leading slash)."""
    source_path: Path
    """Source file on disk (absolute)."""
    description: str
    """One-line description for the README."""
    sha256: str
    """Content hash; reproducible verification on the 3PAO side."""
    size_bytes: int


@dataclass(frozen=True)
class SubmissionResult:
    """What `build_submission` returns."""

    output_path: Path
    """Where the archive (or directory) was written."""
    is_archive: bool
    """True if .zip; False if --no-archive directory."""
    package_version: str
    """The version string embedded in the README + filename."""
    artifacts: list[SubmissionManifest] = field(default_factory=list)
    """All artifacts included, in archive order."""
    missing: list[str] = field(default_factory=list)
    """Optional artifacts not present (e.g. no OSCAL CD yet) — informational, not fatal."""


def _sha256_of(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        while True:
            chunk = f.read(1 << 16)
            if not chunk:
                break
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def _latest_match(directory: Path, glob: str) -> Path | None:
    """Return the most recently modified file matching `glob` under `directory`, or None."""
    if not directory.is_dir():
        return None
    matches = list(directory.glob(glob))
    if not matches:
        return None
    return max(matches, key=lambda p: p.stat().st_mtime)


def _latest_match_across(directories: list[Path], glob: str) -> Path | None:
    """v0.1.161 / #366: pick the most-recent match across multiple dirs.
    Used to find artifacts that may live in either the new
    `efterlev-out/reports/` location or the legacy `.efterlev/reports/`
    location during the v0.1.160 path transition. Tied or empty → None.
    """
    candidates: list[Path] = []
    for d in directories:
        if d.is_dir():
            candidates.extend(d.glob(glob))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _collect_artifacts(root: Path) -> tuple[list[tuple[str, Path, str]], list[str]]:
    """Find the latest of each expected artifact type.

    Returns (found, missing). Each found is `(archive_path, source_path, description)`.
    Each missing is a one-line "<kind> not found at <path> — run <command>".

    v0.1.161 / #366: walks BOTH the new `efterlev-out/reports/` location
    (default for fresh writes since v0.1.160) and the legacy
    `.efterlev/reports/` location so upgraded workspaces with split
    artifacts still produce a complete submission zip. Previously hardcoded
    only the legacy path — fresh installs (the modal new user) produced
    an empty zip because every artifact landed in the new location while
    the collector looked in the old one.
    """
    from efterlev.paths import internal_root, iter_report_dirs

    report_dirs = iter_report_dirs(root)
    poam_dirs = [d / "poam" for d in report_dirs]
    oscal_dirs = [d / "oscal" for d in report_dirs]

    found: list[tuple[str, Path, str]] = []
    missing: list[str] = []

    # FRMR attestation
    p = _latest_match_across(report_dirs, "attestation-*.json")
    if p is not None:
        found.append(
            (
                "attestation/frmr-attestation.json",
                p,
                "FRMR-compatible attestation JSON (Documentation Agent output)",
            )
        )
    else:
        missing.append(
            "FRMR attestation not found under efterlev-out/reports/ "
            "(or legacy .efterlev/reports/) — run `efterlev agent document`"
        )

    # POA&M markdown
    p = _latest_match_across(poam_dirs, "poam-*.md")
    if p is not None:
        found.append(
            (
                "poam/poam.md",
                p,
                "Plan-of-Action-and-Milestones markdown (3PAO reads this first)",
            )
        )
    else:
        missing.append(
            "POA&M markdown not found under efterlev-out/reports/poam/ "
            "(or legacy .efterlev/reports/poam/) — run `efterlev poam`"
        )

    # OSCAL POA&M
    p = _latest_match_across(oscal_dirs, "poam-*.json")
    if p is not None:
        found.append(
            (
                "oscal/poam.json",
                p,
                "OSCAL 1.0.4 POA&M (NIST-schema + FedRAMP-rule + oscal-cli validated)",
            )
        )
    else:
        missing.append(
            "OSCAL POA&M not found under efterlev-out/reports/oscal/ "
            "(or legacy .efterlev/reports/oscal/) — "
            "run `efterlev oscal export --kind poam`"
        )

    # OSCAL Component-Definition
    p = _latest_match_across(oscal_dirs, "component-definition-*.json")
    if p is not None:
        found.append(
            (
                "oscal/component-definition.json",
                p,
                "OSCAL 1.0.4 Component-Definition (per-KSI implemented-requirements)",
            )
        )
    else:
        missing.append(
            "OSCAL Component-Definition not found — "
            "run `efterlev oscal export --kind component-definition`"
        )

    # VDR (Vulnerability Detection & Response) report — RFC-0012-shaped
    # artifact, v0.1.162 / #367. Both JSON (machine-readable) and
    # markdown (3PAO-readable) views. Missing is informational only —
    # VDR is an ahead-of-RFC-0012-finalization preview; the POA&M above
    # remains the program-current artifact until the RFC standardizes.
    vdr_dirs = [d / "vdr" for d in report_dirs]
    p = _latest_match_across(vdr_dirs, "vdr-*.json")
    if p is not None:
        found.append(
            (
                "vdr/vdr-report.json",
                p,
                "Vulnerability Detection & Response (RFC-0012-shaped, ahead-of-finalization)",
            )
        )
    p = _latest_match_across(vdr_dirs, "vdr-*.md")
    if p is not None:
        found.append(
            (
                "vdr/vdr-report.md",
                p,
                "Vulnerability Detection & Response markdown (human-readable)",
            )
        )

    # Consolidated resource inventory — v0.1.164 / #369 (RFC-0017
    # "consolidated resource inventory being validated" artifact).
    # Both JSON (machine) + HTML (3PAO-readable) views. Missing is
    # informational; the inventory is derivable from the scan output
    # if needed.
    inventory_dirs = [d / "inventory" for d in report_dirs]
    p = _latest_match_across(inventory_dirs, "inventory-*.json")
    if p is not None:
        found.append(
            (
                "inventory/inventory.json",
                p,
                "Consolidated resource inventory (RFC-0017 artifact, machine-readable)",
            )
        )
    p = _latest_match_across(inventory_dirs, "inventory-*.html")
    if p is not None:
        found.append(
            (
                "inventory/inventory.html",
                p,
                "Consolidated resource inventory HTML (one-page, 3PAO-readable)",
            )
        )

    # HTML gap report
    p = _latest_match_across(report_dirs, "gap-*.html")
    if p is not None:
        found.append(
            (
                "reports/gap-report.html",
                p,
                "Color-coded gap report (all 60 KSI classifications at a glance)",
            )
        )

    # HTML documentation report
    p = _latest_match_across(report_dirs, "documentation-*.html")
    if p is not None:
        found.append(
            (
                "reports/documentation.html",
                p,
                "Narrative-shaped FRMR view (per-theme breakdown for human reviewers)",
            )
        )

    # 3PAO inspector report — v0.1.168 / #374. Single-page assessor view
    # composing FRMR statements + attestation narratives + RFC-0017 gate
    # results into one HTML page. The primary 3PAO-handoff artifact.
    p = _latest_match_across(report_dirs, "inspector-*.html")
    if p is not None:
        found.append(
            (
                "reports/inspector.html",
                p,
                "3PAO inspector — single-page RFC-0017 per-KSI checklist (assessor view)",
            )
        )

    # Evidence Manifests (all of them) — these always live under
    # `.efterlev/manifests/`; they're customer-authored input, not output.
    manifests_dir = internal_root(root) / "manifests"
    if manifests_dir.is_dir():
        for mf in sorted(manifests_dir.glob("*.yml")):
            found.append(
                (
                    f"manifests/{mf.name}",
                    mf,
                    "Customer-authored Evidence Manifest (procedural attestation)",
                )
            )

    return found, missing


def _build_readme(
    *,
    package_version: str,
    built_at: datetime,
    artifacts: list[SubmissionManifest],
    missing: list[str],
    workspace_root: Path,
) -> str:
    lines: list[str] = []
    lines.append(f"# Efterlev submission package · {package_version}")
    lines.append("")
    lines.append(f"Built at {built_at.isoformat()} from workspace `{workspace_root}`.")
    lines.append("")
    lines.append("**DRAFT — requires 3PAO review.** Every claim in this package is")
    lines.append("auto-generated and carries a `requires_review` flag. The 3PAO is")
    lines.append("expected to evaluate the underlying evidence + the Efterlev pipeline")
    lines.append("itself, not just accept these artifacts at face value.")
    lines.append("")
    lines.append("## What's in this package")
    lines.append("")
    lines.append("| Path | Description | SHA-256 (first 16) |")
    lines.append("|---|---|---|")
    for a in artifacts:
        lines.append(f"| `{a.archive_path}` | {a.description} | `{a.sha256[:16]}…` |")
    lines.append("")
    lines.append("## Read order (suggested)")
    lines.append("")
    lines.append("1. `poam/poam.md` — the punch list. Start here for a quick scan.")
    lines.append("2. `reports/gap-report.html` — color-coded view of all 60 KSIs.")
    lines.append("3. `attestation/frmr-attestation.json` — the FRMR-shaped attestation.")
    lines.append(
        "4. `oscal/poam.json` + `oscal/component-definition.json` — machine-readable formats"
    )
    lines.append("   for downstream ingestion (GRC platforms, etc.).")
    lines.append("5. `manifests/*.yml` — customer-authored procedural attestations.")
    lines.append("")
    if missing:
        lines.append("## Missing pieces (informational, not blocking)")
        lines.append("")
        for m in missing:
            lines.append(f"- {m}")
        lines.append("")
    lines.append("## Reproducibility")
    lines.append("")
    lines.append("Every artifact in this package was produced by Efterlev — an")
    lines.append("open-source compliance scanner (Apache 2.0). The 3PAO can")
    lines.append("re-produce the same outputs from the customer's IaC by following")
    lines.append("the README at https://github.com/efterlev/efterlev. The Efterlev")
    lines.append("provenance store (`.efterlev/store.db` in the customer's repo,")
    lines.append("not included in this package) walks any cited evidence record")
    lines.append("back to a specific file and line range via")
    lines.append("`efterlev provenance show <record-id>`.")
    lines.append("")
    lines.append("Tamper-evidence: every record in the store is content-addressed")
    lines.append("(sha256); the receipts log is hash-chained. Run")
    lines.append("`efterlev provenance verify` against the customer's workspace")
    lines.append("to confirm the store is internally consistent.")
    return "\n".join(lines) + "\n"


def _build_index(
    artifacts: list[SubmissionManifest], package_version: str, built_at: datetime
) -> str:
    """Machine-readable counterpart to README.md — for automated 3PAO tools."""
    import json

    return (
        json.dumps(
            {
                "package_version": package_version,
                "built_at": built_at.isoformat(),
                "tool": "efterlev",
                "artifacts": [
                    {
                        "path": a.archive_path,
                        "description": a.description,
                        "sha256": a.sha256,
                        "size_bytes": a.size_bytes,
                    }
                    for a in artifacts
                ],
            },
            indent=2,
        )
        + "\n"
    )


def build_submission(
    root: Path,
    *,
    output: Path | None = None,
    archive: bool = True,
    package_version: str | None = None,
) -> SubmissionResult:
    """Build the submission package at `root`. Returns the path written.

    Args:
        root: Workspace root containing `.efterlev/`.
        output: Where to write the package. Defaults to
            `.efterlev/submissions/submission-<ts>.zip` (or directory if
            `archive=False`).
        archive: When True (default), write a zip; otherwise a directory.
        package_version: Version string embedded in the README + index.
            Defaults to a timestamp-based string.
    """
    built_at = datetime.now(UTC)
    if package_version is None:
        package_version = f"v{built_at.strftime('%Y%m%d-%H%M%S')}"

    found_raw, missing = _collect_artifacts(root)

    artifacts: list[SubmissionManifest] = []
    for archive_path, src, desc in found_raw:
        sha, size = _sha256_of(src)
        artifacts.append(
            SubmissionManifest(
                archive_path=archive_path,
                source_path=src,
                description=desc,
                sha256=sha,
                size_bytes=size,
            )
        )

    readme_body = _build_readme(
        package_version=package_version,
        built_at=built_at,
        artifacts=artifacts,
        missing=missing,
        workspace_root=root,
    )
    index_body = _build_index(artifacts, package_version, built_at)

    # v0.1.160 / #365: visible-output split. Submissions now land under
    # `<workspace>/efterlev-out/submissions/` so the zip a customer
    # actually attaches to 3PAO email is discoverable in Finder.
    from efterlev.paths import submissions_dir as _submissions_dir

    submissions_dir = _submissions_dir(root)
    submissions_dir.mkdir(parents=True, exist_ok=True)

    if archive:
        ts = built_at.strftime("%Y%m%d-%H%M%S")
        out = output or (submissions_dir / f"submission-{ts}.zip")
        _write_zip(out, artifacts, readme_body, index_body)
    else:
        ts = built_at.strftime("%Y%m%d-%H%M%S")
        out = output or (submissions_dir / f"submission-{ts}")
        _write_dir(out, artifacts, readme_body, index_body)

    return SubmissionResult(
        output_path=out,
        is_archive=archive,
        package_version=package_version,
        artifacts=artifacts,
        missing=missing,
    )


def _write_zip(
    out: Path, artifacts: list[SubmissionManifest], readme_body: str, index_body: str
) -> None:
    """Write the archive atomically via a temp file in the same dir."""
    import tempfile

    out.parent.mkdir(parents=True, exist_ok=True)
    # Build in-memory then atomic-write (small package; fits in RAM easily).
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.md", readme_body)
        z.writestr("index.json", index_body)
        for a in artifacts:
            with a.source_path.open("rb") as f:
                z.writestr(a.archive_path, f.read())

    fd, tmp_path_str = tempfile.mkstemp(dir=out.parent, prefix=".submission-", suffix=".tmp")
    import os

    tmp_path = Path(tmp_path_str)
    try:
        os.write(fd, buf.getvalue())
    finally:
        os.close(fd)
    os.replace(tmp_path, out)


def _write_dir(
    out: Path, artifacts: list[SubmissionManifest], readme_body: str, index_body: str
) -> None:
    """Write the package as a directory tree."""
    out.mkdir(parents=True, exist_ok=True)
    (out / "README.md").write_text(readme_body, encoding="utf-8")
    (out / "index.json").write_text(index_body, encoding="utf-8")
    for a in artifacts:
        target = out / a.archive_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(a.source_path.read_bytes())
