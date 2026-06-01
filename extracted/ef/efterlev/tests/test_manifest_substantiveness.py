"""Tests for the procedural-manifest experience: substantiveness + scaffold stubs."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from efterlev.manifests.loader import load_manifest_file
from efterlev.manifests.scaffold import stub_yaml, template_questions
from efterlev.manifests.substantiveness import is_substantive, manifest_issues
from efterlev.models.manifest import EvidenceManifest, ManifestAttestation


def _att(**kw) -> ManifestAttestation:
    base = dict(
        statement="We run a 24/7 monitored security inbox per the runbook at runbooks/ir.md.",
        attested_by="vp-security@acme.gov",
        attested_at=date(2026, 5, 1),
        next_review=date(2026, 11, 1),
        supporting_docs=["./policies/ir.pdf"],
    )
    base.update(kw)
    return ManifestAttestation(**base)


def test_filled_manifest_is_substantive() -> None:
    m = EvidenceManifest(ksi="KSI-AFR-FSI", evidence=[_att()])
    assert is_substantive(m)
    assert manifest_issues(m) == []


def test_placeholder_attester_is_not_substantive() -> None:
    m = EvidenceManifest(ksi="KSI-AFR-FSI", evidence=[_att(attested_by="TODO: someone")])
    assert not is_substantive(m)
    assert any("named attester" in i for i in manifest_issues(m))


def test_draft_placeholder_statement_is_not_substantive() -> None:
    m = EvidenceManifest(ksi="KSI-AFR-FSI", evidence=[_att(statement="DRAFT — example text")])
    assert not is_substantive(m)


def test_missing_review_cadence_is_not_substantive() -> None:
    m = EvidenceManifest(ksi="KSI-AFR-FSI", evidence=[_att(next_review=None)])
    assert not is_substantive(m)
    assert any("review cadence" in i for i in manifest_issues(m))


def test_no_attestations_is_not_substantive() -> None:
    m = EvidenceManifest(ksi="KSI-AFR-FSI", evidence=[])
    assert not is_substantive(m)


def test_supporting_docs_is_recommended_not_core() -> None:
    # missing supporting docs → still "ready" (core bar met), but surfaced as an issue
    m = EvidenceManifest(ksi="KSI-AFR-FSI", evidence=[_att(supporting_docs=[])])
    assert is_substantive(m)
    assert any("supporting-doc" in i for i in manifest_issues(m))


def test_stub_loads_and_is_not_substantive(tmp_path: Path) -> None:
    # a scaffolded stub must be schema-valid (loads) but deliberately thin
    p = tmp_path / "KSI-AFR-ICP.yml"
    p.write_text(stub_yaml("KSI-AFR-ICP"))
    manifest = load_manifest_file(p)
    assert manifest.ksi == "KSI-AFR-ICP"
    assert not is_substantive(manifest)


def test_stub_embeds_template_questions() -> None:
    # KSI-AFR-ICP has a bundled starter-pack template; its questions appear inline
    name, questions = template_questions("KSI-AFR-ICP")
    assert questions, "expected bundled template questions for KSI-AFR-ICP"
    text = stub_yaml("KSI-AFR-ICP")
    assert questions[0] in text
    assert name and name in text


def test_stub_for_templateless_ksi_still_valid(tmp_path: Path) -> None:
    p = tmp_path / "KSI-INR-XYZ.yml"
    p.write_text(stub_yaml("KSI-INR-XYZ"))
    manifest = load_manifest_file(p)
    assert manifest.ksi == "KSI-INR-XYZ" and not is_substantive(manifest)
