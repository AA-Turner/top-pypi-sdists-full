"""Agent-quality eval harness for Efterlev (v0.2 Phase 1).

Measures agent classification quality + narrative quality against
human-labeled ground-truth fixtures. See DECISIONS 2026-05-08
"v0.2 agent-quality eval harness: lock Phase 1 scope" for the
full design.

Public surface:

    from evals.ground_truth import load_ground_truth, GroundTruth
    from evals.metrics import status_precision, status_recall

CLI:

    python -m evals run --fixture evals/fixtures/govnotes-v1
    python -m evals report --fixture evals/fixtures/govnotes-v1

Cost: ~$0.04 per fixture run on Haiku 4.5 via Bedrock (the
maintainer's locked test-LLM default).
"""

from __future__ import annotations

__all__: list[str] = []
