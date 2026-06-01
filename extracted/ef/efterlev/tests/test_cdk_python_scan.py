"""Tests for v0.1.126 — CDK Python scan primitive.

Validates that the parser → adapter → detector pipeline produces
`TerraformResource` records the existing detector library can fire on,
and that the source-mode value proposition (`.py` file:line in
SourceRef) actually flows end-to-end.
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from efterlev.cdk_python import adapt_cdk_constructs, parse_cdk_python_tree
from efterlev.primitives.scan import ScanCdkPythonInput, scan_cdk_python
from efterlev.provenance import ProvenanceStore, active_store

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = REPO_ROOT / "evals/fixtures/cdk-python-sample"


def test_adapter_produces_terraform_resources_with_line_citations() -> None:
    """The whole point of source-mode: SourceRef.line_start populated."""
    constructs, _ = parse_cdk_python_tree(SAMPLE_DIR)
    tf_resources = adapt_cdk_constructs(constructs, scan_root=SAMPLE_DIR)
    # Stage 1 (v0.1.126): 2 buckets; Stage 2 (v0.1.127): 4 security;
    # Stage 3 (v0.1.128): 4 compute; Stage 4 (v0.1.129): 18 services → 28 total.
    assert len(tf_resources) == 28
    tf_types = {r.type for r in tf_resources}
    assert "aws_s3_bucket" in tf_types
    assert "aws_kms_key" in tf_types
    assert "aws_ec2_securitygroup" in tf_types
    assert "aws_iam_role" in tf_types
    assert "aws_cloudtrail_trail" in tf_types
    for r in tf_resources:
        assert r.source_ref.line_start is not None
        assert r.source_ref.line_start > 0
        # Path should be relative to scan_root (not absolute).
        assert not r.source_ref.file.is_absolute()


def test_scan_primitive_runs_detectors_against_cdk_constructs() -> None:
    """End-to-end: scan_cdk_python returns a populated output object."""
    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        out = scan_cdk_python(ScanCdkPythonInput(target_dir=SAMPLE_DIR))
    # 2 + 4 + 4 + 18 = 28 total constructs across all 4 stacks.
    assert out.constructs_parsed == 28
    assert out.resources_adapted == 28
    assert out.detectors_run > 0  # some terraform detectors ran (most fired 0 evidence)
    assert out.parse_failures == []


def test_scan_primitive_with_no_cdk_files(tmp_path: Path) -> None:
    """Scanning a directory with no `.py` files returns zero constructs."""
    (tmp_path / "README.md").write_text("# nothing\n", encoding="utf-8")
    with ProvenanceStore(tmp_path) as store, active_store(store):
        out = scan_cdk_python(ScanCdkPythonInput(target_dir=tmp_path))
    assert out.constructs_parsed == 0
    assert out.resources_adapted == 0
    assert out.evidence_count == 0


def test_scan_primitive_with_non_cdk_python_files(tmp_path: Path) -> None:
    """`.py` files without `aws_cdk` imports return zero constructs (cheap content-sniff)."""
    (tmp_path / "ordinary.py").write_text("def foo():\n    return 1\n", encoding="utf-8")
    with ProvenanceStore(tmp_path) as store, active_store(store):
        out = scan_cdk_python(ScanCdkPythonInput(target_dir=tmp_path))
    assert out.files_scanned == 1
    assert out.constructs_parsed == 0
