"""`scan_cdk_python` primitive — parse Python CDK source, run detectors with file:line.

Mirror of `scan_cloudformation` for CDK source-mode. Walks `.py` files
under `target_dir`, parses each via `efterlev.cdk_python.parser`,
adapts each construct to a `TerraformResource`-shape via
`efterlev.cdk_python.adapter` (preserving file:line, the source-mode
value proposition), and dispatches to the same `source="terraform"`
detector library that `scan_terraform` and `scan_cloudformation` use.

Behind `--allow-cdk-py` at the CLI layer (this primitive itself is
unconditional; the CLI is the opt-in surface — same pattern as the
pre-graduation `--allow-cfn` posture).

Stage 1 scope (v0.1.126): one supported construct (`s3.Bucket`).
Detectors that need deep nested HCL block syntax won't fire on raw CDK
kwargs — that gap is intentional and closes in Stage 2+ via
property-mapping batches modeled on the v0.1.74-93 CFN arc.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

import efterlev.detectors  # noqa: F401  (registration side-effect)
from efterlev.cdk_python import (
    CdkParseFailure,
    adapt_cdk_constructs,
    parse_cdk_python_tree,
)
from efterlev.detectors.base import Source, get_registry
from efterlev.models import Evidence
from efterlev.primitives.base import primitive
from efterlev.provenance.context import get_active_store


class ScanCdkPythonInput(BaseModel):
    """Input to `scan_cdk_python`."""

    model_config = ConfigDict(frozen=True)

    target_dir: Path


class CdkPyDetectorRunSummary(BaseModel):
    """One detector's contribution to a CDK Python scan."""

    model_config = ConfigDict(frozen=True)

    detector_id: str
    version: str
    evidence_count: int


class CdkPyParseFailureRecord(BaseModel):
    """One `.py` file the parser couldn't read."""

    model_config = ConfigDict(frozen=True)

    file: Path
    reason: str


class ScanCdkPythonOutput(BaseModel):
    """Structured summary of a CDK Python scan."""

    model_config = ConfigDict(frozen=True)

    files_scanned: int
    """Count of `.py` files inspected (incl. files without aws_cdk imports, which return empty)."""
    constructs_parsed: int
    """Count of supported CDK construct invocations parsed."""
    resources_adapted: int
    """Count of `TerraformResource` records produced (1:1 with constructs at Stage 1)."""
    detectors_run: int
    evidence: list[Evidence] = Field(default_factory=list)
    evidence_record_ids: list[str] = Field(default_factory=list)
    per_detector: list[CdkPyDetectorRunSummary] = Field(default_factory=list)
    parse_failures: list[CdkPyParseFailureRecord] = Field(default_factory=list)

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)


@primitive(capability="scan", side_effects=False, version="0.1.0", deterministic=True)
def scan_cdk_python(input: ScanCdkPythonInput) -> ScanCdkPythonOutput:
    """Parse the target Python CDK tree, adapt to TF shape, run detectors."""
    constructs, parse_failures = parse_cdk_python_tree(input.target_dir)

    # files_scanned counts the rglob iteration; cheaper to recompute than thread through.
    excluded = {".venv", "node_modules", ".git", "__pycache__", "cdk.out", ".pytest_cache"}
    files_scanned = sum(
        1 for p in input.target_dir.rglob("*.py") if not any(part in excluded for part in p.parts)
    )

    tf_resources = adapt_cdk_constructs(constructs, scan_root=input.target_dir)

    terraform_source: Source = "terraform"
    terraform_detectors = [
        spec for spec in get_registry().values() if spec.source == terraform_source
    ]

    store = get_active_store()
    pre_ids: set[str] = set(store.iter_records()) if store is not None else set()

    evidence: list[Evidence] = []
    per_detector: list[CdkPyDetectorRunSummary] = []
    for spec in terraform_detectors:
        produced = spec.callable(tf_resources)
        evidence.extend(produced)
        per_detector.append(
            CdkPyDetectorRunSummary(
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

    return ScanCdkPythonOutput(
        files_scanned=files_scanned,
        constructs_parsed=len(constructs),
        resources_adapted=len(tf_resources),
        detectors_run=len(terraform_detectors),
        evidence=evidence,
        evidence_record_ids=evidence_record_ids,
        per_detector=per_detector,
        parse_failures=[
            CdkPyParseFailureRecord(file=f.file, reason=f.reason) for f in parse_failures
        ],
    )


def _coerce_failure(f: CdkParseFailure) -> CdkPyParseFailureRecord:
    """Helper kept exported for tests that want to mock parse failures."""
    return CdkPyParseFailureRecord(file=f.file, reason=f.reason)
