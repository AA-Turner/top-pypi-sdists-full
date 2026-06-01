#!/usr/bin/env python3
"""Regenerate the labeled OSCAL POA&M fixture under evals/fixtures/csp-starter-cfn/oscal/.

Inputs are pinned in this script so re-runs produce byte-stable output. The
fixture is a 3PAO-inspectable artifact derived from the csp-starter-cfn
Phase 2 lite verdicts (6 representative open KSIs across CMT, CNA, IAM, SVC,
MLA, PIY themes). When the generator's output shape changes, run this script
and commit the updated fixture alongside the version bump.

Usage:
    uv run python scripts/regenerate_oscal_labeled_fixture.py
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from efterlev.models.indicator import Indicator
from efterlev.primitives.generate import (
    GeneratePoamOscalInput,
    PoamClassificationInput,
    generate_poam_oscal,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "evals/fixtures/csp-starter-cfn/oscal/labeled-poam-v0.1.106.json"

# Pinned timestamp so re-runs don't churn the file.
LAST_MODIFIED = datetime(2026, 5, 14, 0, 0, 0, tzinfo=UTC)

INDICATORS_DATA: list[tuple[str, list[str], str]] = [
    ("KSI-CMT-RMV", ["cm-3", "cm-4"], "Redeploy from clean state vs in-place modification."),
    (
        "KSI-CNA-RNT",
        ["ac-4", "sc-7"],
        "Restrict network traffic by default; allow-list explicitly.",
    ),
    ("KSI-IAM-MFA", ["ia-2"], "Enforce phishing-resistant MFA for all administrative access."),
    ("KSI-SVC-SNT", ["sc-8", "sc-13"], "Encrypt network traffic in transit."),
    ("KSI-MLA-LGS", ["au-2", "au-3", "au-12"], "Centralize logging across services."),
    ("KSI-PIY-IRP", ["ir-4", "ir-8"], "Maintain incident response plan with role assignments."),
]

CLASSIFICATIONS: list[PoamClassificationInput] = [
    PoamClassificationInput(
        ksi_id="KSI-CMT-RMV",
        status="not_implemented",
        rationale="No deployment-pipeline evidence for redeploy-on-change pattern.",
        evidence_ids=["cfn-stack-policy-001"],
    ),
    PoamClassificationInput(
        ksi_id="KSI-CNA-RNT",
        status="not_implemented",
        rationale="Security groups have 0.0.0.0/0 inbound for non-LB resources.",
        evidence_ids=["cfn-sg-002", "cfn-sg-003"],
    ),
    PoamClassificationInput(
        ksi_id="KSI-IAM-MFA",
        status="not_implemented",
        rationale="No MFA-enforcement IAM policy present in the CFN template.",
        evidence_ids=["cfn-iam-001"],
    ),
    PoamClassificationInput(
        ksi_id="KSI-SVC-SNT",
        status="partial",
        rationale="ALB listener uses HTTPS; some internal traffic remains on HTTP.",
        evidence_ids=["cfn-alb-001"],
    ),
    PoamClassificationInput(
        ksi_id="KSI-MLA-LGS",
        status="partial",
        rationale="CloudWatch log groups configured for some services; ALB access logs missing.",
        evidence_ids=["cfn-cw-001"],
    ),
    PoamClassificationInput(
        ksi_id="KSI-PIY-IRP",
        status="not_implemented",
        rationale="Procedural KSI; no manifest attestation present.",
        evidence_ids=[],
    ),
]


def main() -> None:
    indicators = {
        ksi_id: Indicator(
            id=ksi_id,
            theme=ksi_id.split("-")[1],
            name=f"Indicator {ksi_id}",
            statement=stmt,
            controls=controls,
        )
        for ksi_id, controls, stmt in INDICATORS_DATA
    }

    out = generate_poam_oscal(
        GeneratePoamOscalInput(
            classifications=CLASSIFICATIONS,
            indicators=indicators,
            baseline_id="fedramp-20x-moderate",
            frmr_version="0.9.43-beta",
            system_name="csp-starter-cfn (labeled fixture)",
            system_id="csp-starter-cfn-labeled-001",
            last_modified=LAST_MODIFIED,
        )
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w") as f:
        json.dump(out.oscal_document, f, indent=2, sort_keys=False)
        f.write("\n")

    poam = out.oscal_document["plan-of-action-and-milestones"]
    print(
        f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}: "
        f"{out.item_count} POA&M items, "
        f"{len(poam['risks'])} risks, "
        f"{len(poam['observations'])} observations"
    )


if __name__ == "__main__":
    main()
