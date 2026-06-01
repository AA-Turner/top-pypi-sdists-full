"""KSI-PIY-RSD: SDLC security-gates detector.

Reads `.github/workflows/*.yml` for the canonical SDLC security-gate
patterns: CodeQL, dependency review, secret scanning (TruffleHog,
Gitleaks). Emits one Evidence per workflow.

Per DECISIONS 2026-05-07 "Tier 1 #4 design": this is detector #6 of 6
(the final item in the Tier 1 #4 backlog). KSI-PIY-RSD classified
`partial` — this detector covers the configured-gate half; the
procedural review cadence ("persistently review the effectiveness")
is manifest territory.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.github_workflows import WorkflowFile
from efterlev.models import Evidence

# Substring patterns the detector looks for in step `uses:` fields.
# Each tuple is (gate_label, list_of_substrings_any_match).
_GATE_PATTERNS: dict[str, tuple[str, ...]] = {
    "codeql": (
        "github/codeql-action/init",
        "github/codeql-action/analyze",
        "github/codeql-action/autobuild",
    ),
    "dependency_review": ("actions/dependency-review-action",),
    "secret_scanning": (
        "trufflesecurity/trufflehog",
        "gitleaks/gitleaks-action",
        "zricethezav/gitleaks-action",
    ),
}


@detector(
    id="github.piy_sdlc_security_gates",
    ksis=["KSI-PIY-RSD"],
    controls=["SA-3", "SA-8"],
    source="github-workflows",
    version="0.1.0",
)
def detect(workflows: list[WorkflowFile]) -> list[Evidence]:
    """Emit security-gate Evidence per workflow file.

    Evidences (KSI):     KSI-PIY-RSD — IaC-declared SDLC security
                         gates (CodeQL, dependency review, secret
                         scanning).
    Evidences (800-53):  SA-3 (System Development Life Cycle),
                         SA-8 (Security and Privacy Engineering
                         Principles).
    Does NOT prove:      procedural review cadence (manifest
                         territory); branch-protection rules
                         (separate detector candidate); whether
                         gate findings are actually triaged.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for wf in workflows:
        out.append(_emit_workflow_evidence(wf, now))

    return out


def _emit_workflow_evidence(wf: WorkflowFile, now: datetime) -> Evidence:
    gates_present = _detect_gates(wf)

    if gates_present:
        content: dict[str, Any] = {
            "resource_type": "github_workflow",
            "resource_name": wf.name,
            "gate_state": "configured",
            "gates_present": gates_present,
        }
    else:
        content = {
            "resource_type": "github_workflow",
            "resource_name": wf.name,
            "gate_state": "absent",
            "gap": (
                "no SDLC security gate detected (looked for codeql + "
                "dependency_review + secret_scanning patterns in `uses:` fields)"
            ),
        }

    return Evidence.create(
        detector_id="github.piy_sdlc_security_gates",
        ksis_evidenced=["KSI-PIY-RSD"],
        controls_evidenced=["SA-3", "SA-8"],
        source_ref=wf.source_ref,
        content=content,
        timestamp=now,
    )


def _detect_gates(wf: WorkflowFile) -> list[str]:
    """Return the sorted list of gate labels found in this workflow."""
    found: set[str] = set()
    for step in _iter_steps(wf):
        uses = step.get("uses")
        if not isinstance(uses, str):
            continue
        for gate, patterns in _GATE_PATTERNS.items():
            if any(pattern in uses for pattern in patterns):
                found.add(gate)
    return sorted(found)


def _iter_steps(wf: WorkflowFile) -> list[dict[str, Any]]:
    """Flatten every step across every job in a workflow."""
    out: list[dict[str, Any]] = []
    jobs = wf.jobs if isinstance(wf.jobs, dict) else {}
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        for step in steps:
            if isinstance(step, dict):
                out.append(step)
    return out
