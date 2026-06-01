"""`scan_cloudformation` primitive — parse a CFN tree, adapt to TF shape, run detectors.

Per DECISIONS 2026-05-12 Tier 5 #1, this primitive is the CFN-side
companion to `scan_terraform`: it walks `*.yaml` / `*.yml` / `*.json`
files under `target_dir`, content-sniffs for CFN templates, parses
each, adapts the resources to `TerraformResource` shape via
`efterlev.cloudformation.adapter`, and dispatches to the same
`source="terraform"` detectors that `scan_terraform` uses.

Honest scope (PR beta v0.1.72 plumbing): the adapter does
resource-type translation + shallow snake_case key mirror only.
Existing detectors will SEE CFN resources (filter pass) but will
read empty / shallow body data. Per-detector property-mapping is
PR gamma work.

Behind the `--allow-cfn` flag at the CLI layer per DECISIONS 2026-05-12
Decision #5; this primitive itself is unconditional — the CLI is the
opt-in surface.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

import efterlev.detectors  # noqa: F401  (registration side-effect)
from efterlev.cloudformation import adapt_cfn_resources, parse_cfn_tree
from efterlev.cloudformation.parser import CfnParseFailure
from efterlev.detectors.base import Source, get_registry
from efterlev.models import Evidence
from efterlev.primitives.base import primitive
from efterlev.provenance.context import get_active_store


class ScanCloudFormationInput(BaseModel):
    """Input to `scan_cloudformation`."""

    model_config = ConfigDict(frozen=True)

    target_dir: Path


class CfnDetectorRunSummary(BaseModel):
    """One detector's contribution to a CFN scan."""

    model_config = ConfigDict(frozen=True)

    detector_id: str
    version: str
    evidence_count: int


class CfnParseFailureRecord(BaseModel):
    """One CFN file the parser couldn't read."""

    model_config = ConfigDict(frozen=True)

    file: Path
    reason: str


class ScanCloudFormationOutput(BaseModel):
    """Structured summary of a CFN scan."""

    model_config = ConfigDict(frozen=True)

    files_scanned: int
    """Count of YAML/JSON files inspected (incl. non-CFN files content-sniffed and skipped)."""
    cfn_templates_parsed: int
    """Count of files that passed the CFN content-sniff and were actually parsed."""
    resources_parsed: int
    nested_stack_refs: int = 0
    """Count of `AWS::CloudFormation::Stack` references the parser saw and
    adapted but DID NOT expand. Surfaced in the scan summary so the user
    knows to scan child templates directly. v0.x followup: actually follow
    TemplateURL to recursively parse nested stacks."""
    detectors_run: int
    evidence: list[Evidence] = Field(default_factory=list)
    evidence_record_ids: list[str] = Field(default_factory=list)
    per_detector: list[CfnDetectorRunSummary] = Field(default_factory=list)
    parse_failures: list[CfnParseFailureRecord] = Field(default_factory=list)

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)


@primitive(capability="scan", side_effects=False, version="0.1.0", deterministic=True)
def scan_cloudformation(input: ScanCloudFormationInput) -> ScanCloudFormationOutput:
    """Parse the target CFN tree, adapt to TF shape, run terraform-source detectors.

    Per DECISIONS 2026-05-12 Decision #2 — the adapter shim approach
    means the EXISTING `source="terraform"` detector library is what
    runs over CFN resources. There is no `source="cloudformation"`
    detector; v1 reuses the Terraform detector identity since the
    KSI/control mappings + emitted Evidence shapes are equivalent.
    """
    parse_result = parse_cfn_tree(input.target_dir)
    cfn_resources = parse_result.resources

    # Track which files actually had CFN-template shape (vs just being
    # YAML/JSON files that got content-sniffed and skipped).
    cfn_template_files = {r.file for r in cfn_resources}

    tf_resources = adapt_cfn_resources(cfn_resources, scan_root=input.target_dir)

    # Count nested-stack references for the scan summary. AWS::CloudFormation::Stack
    # → aws_cloudformation_stack via cfn_type_to_tf_type. Surfaced so users
    # know to scan child templates directly (TemplateURL expansion is a v0.x
    # followup; see CFN graduation arc step 5 deferred-to-v0.3+).
    nested_stack_refs = sum(1 for r in tf_resources if r.type == "aws_cloudformation_stack")

    terraform_source: Source = "terraform"
    terraform_detectors = [
        spec for spec in get_registry().values() if spec.source == terraform_source
    ]

    store = get_active_store()
    pre_ids: set[str] = set(store.iter_records()) if store is not None else set()

    evidence: list[Evidence] = []
    per_detector: list[CfnDetectorRunSummary] = []
    for spec in terraform_detectors:
        produced = spec.callable(tf_resources)
        evidence.extend(produced)
        per_detector.append(
            CfnDetectorRunSummary(
                detector_id=spec.id,
                version=spec.version,
                evidence_count=len(produced),
            )
        )

    evidence_record_ids: list[str] = []
    if store is not None:
        for rid in store.iter_records():
            if rid not in pre_ids:
                evidence_record_ids.append(rid)

    return ScanCloudFormationOutput(
        files_scanned=parse_result.files_scanned,
        cfn_templates_parsed=len(cfn_template_files),
        resources_parsed=len(tf_resources),
        nested_stack_refs=nested_stack_refs,
        detectors_run=len(terraform_detectors),
        evidence=evidence,
        evidence_record_ids=evidence_record_ids,
        per_detector=per_detector,
        parse_failures=[
            CfnParseFailureRecord(file=f.file, reason=f.reason) for f in parse_result.parse_failures
        ],
    )


def _coerce_failure(f: CfnParseFailure) -> CfnParseFailureRecord:
    """Helper kept exported for tests that want to mock parse failures."""
    return CfnParseFailureRecord(file=f.file, reason=f.reason)
