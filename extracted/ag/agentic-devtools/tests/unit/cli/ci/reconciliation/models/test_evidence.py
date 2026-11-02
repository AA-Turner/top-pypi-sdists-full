"""Evidence identity binds provenance and payload, not its own identity."""

from dataclasses import replace


def test_digest_binds_all_content(foundation):
    proof = foundation().proof()
    assert proof.digest() == proof.evidence_id
    assert replace(proof, evidence_id="ignored").digest() == proof.evidence_id
    assert replace(proof, source_revision="changed").digest() != proof.evidence_id
