"""Constants and configuration for the Speckit Phase 0 workflow core.

Phase 0 is the label-triggered normalization stage that carves out a
deterministic branch for a source issue, seeds it with a canonical
``issue.md`` artifact, commits it, and opens a pull request (see spec #1799).

All naming is deterministic and derived solely from the bare GitHub issue
number (the ``{issue-key}``), so that independent trigger runs and recovery
runs agree on branch names, artifact paths, and provenance locations without
any shared state beyond the repository itself.
"""

from __future__ import annotations

# Branch naming convention (FR-010): ``speckit/{issue-key}/phase-0-normalize``.
BRANCH_NAME_TEMPLATE = "speckit/{issue_key}/phase-0-normalize"

# Canonical artifact path (FR-003): ``.speckit/issues/{issue-key}/issue.md``.
ARTIFACT_PATH_TEMPLATE = ".speckit/issues/{issue_key}/issue.md"

# Canonical provenance JSON path within the Phase 0 bootstrap commit
# (plan.md Phase B). Kept constant across bootstrap, amendment, and recovery
# reads so independent runs share one unambiguous read location.
PROVENANCE_PATH = ".speckit/phase0-provenance.json"

# Conventional commit type/description for the generated ``issue.md`` (FR-003).
COMMIT_TYPE = "chore"
COMMIT_DESCRIPTION = "add normalized issue.md for Phase 0"

# Maximum source-description size before truncation is applied (FR-002, FR-008).
# Descriptions larger than this are truncated at a markdown-safe boundary with a
# ``[CONTENT_TRUNCATED: ...]`` annotation; the provenance content hash still
# reflects the complete pre-truncation source content.
MAX_DESCRIPTION_BYTES = 102_400

# Phase marker label applied to the Phase 0 pull request (drives progression).
PHASE_0_PR_LABEL = "speckit:phase-0"

# Applied to the Phase 0 pull request once its merge advances progression (FR-006).
PHASE_0_COMPLETE_LABEL = "speckit:phase-0-complete"
