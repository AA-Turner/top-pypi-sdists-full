"""Deterministic, offline reconciliation fixtures."""

import base64
import hashlib
import json
from dataclasses import asdict

import pytest

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import (
    ReconciliationAttestation,
    ReconciliationCriterionVerdict,
    ReconciliationFileVerdict,
)


@pytest.fixture
def attestation():
    return ReconciliationAttestation(
        schema_version=1,
        repository="example-owner/repo",
        pr_number=42,
        pre_repair_sha="1" * 40,
        pinned_base_sha="2" * 40,
        repair_output_sha="3" * 40,
        reviewed_head_sha="4" * 40,
        changed_files=("a.py", "src/b.py"),
        file_verdicts=(
            ReconciliationFileVerdict("a.py", "a" * 64, "accepted", "Preserves the original behavior."),
            ReconciliationFileVerdict("src/b.py", "b" * 64, "accepted", "Retains both intended changes."),
        ),
        criteria_source="https://github.com/swai-factory/agentic-devtools/issues/4299#acceptance-and-safety-tests",
        criteria_source_sha256="c" * 64,
        criterion_verdicts=tuple(
            ReconciliationCriterionVerdict(f"AC{number}", "accepted", f"Criterion {number} remains satisfied.")
            for number in range(1, 8)
        ),
        provider_evidence_ref="github://example-owner/repo/pull/42/reviews",
        configured_approver_login="approver",
        reviewer_login="approver",
        repair_writer_login="writer",
    )


@pytest.fixture
def payload(attestation):
    return json.loads(json.dumps(asdict(attestation)))


@pytest.fixture
def envelope():
    def wrap(value, *, raw=None):
        data = (
            json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()
            if raw is None
            else raw
        )
        digest = hashlib.sha256(data).hexdigest()
        encoded = base64.urlsafe_b64encode(data).decode().rstrip("=")
        return f"<!-- agdt-reconciliation:v1 sha256={digest} -->\n{encoded}\n<!-- /agdt-reconciliation -->"

    return wrap
