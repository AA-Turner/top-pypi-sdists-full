"""GitLab label taxonomy for the Pysae group.

This module is the single source of truth for label constants used across scripts.
Keep in sync with the reference file: skills/references/gitlab-labels.md (edit both by hand).
"""

from enum import StrEnum

# NB: domain labels are NOT enumerated here — the vocabulary is the union of every repo's
# `project.labels` (see `project_config.domain_labels` / `pysae-ai-tools project domains`).
# This module keeps only the structured workflow labels (type/priority/board/review).


class TypeLabel(StrEnum):
    BUG = "type::bug"
    FEATURE = "type::feature"
    TECHNICAL = "type::technical"
    DEBT = "type::debt"


class PriorityLabel(StrEnum):
    P1 = "priority::P1"
    P2 = "priority::P2"
    P3 = "priority::P3"


class BoardLabel(StrEnum):
    REFINEMENT = "workflow::Refinement"
    READY = "workflow::Ready"
    TO_DO = "workflow::To Do"
    IN_PROGRESS = "workflow::In progress"
    UNDER_REVIEW = "workflow::Under review"
    TO_DEPLOY = "workflow::To deploy"


class ReviewLabel(StrEnum):
    # Applied by /code-review-pre-release to every ticket it spawns.
    RELEASE = "review::release"


def version_label(version: str) -> str:
    """Return the scoped ``version::vX.Y.Z`` label for a release.

    Normalises the input so the result always carries exactly one ``v`` prefix:
    ``"1.4.0"`` and ``"v1.4.0"`` both yield ``"version::v1.4.0"``.
    """
    return f"version::v{version.lstrip('v')}"


# There is NO hardcoded repo → domain mapping. A repo's domain is whatever its
# `.pysae-ai-tools.yaml` `project.labels` declares — read it directly off the config
# (`cfg.project.labels`), or use `project_config.domain_labels` for the group-wide
# vocabulary (also exposed as `pysae-ai-tools project domains`).

# Board labels ordered from least to most advanced in the workflow
BOARD_LABEL_ORDER: list[BoardLabel] = [
    BoardLabel.REFINEMENT,
    BoardLabel.READY,
    BoardLabel.TO_DO,
    BoardLabel.IN_PROGRESS,
    BoardLabel.UNDER_REVIEW,
    BoardLabel.TO_DEPLOY,
]

DEFAULT_BOARD_LABEL = BoardLabel.REFINEMENT
