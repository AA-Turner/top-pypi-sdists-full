"""Constants and display mappings for the audit."""

from ...common.references.gitlab_labels import (
    BoardLabel,
    TypeLabel,
)
from .diagnostic import DetectionMethod

TEMPLATES_PROJECT = "pysae/issue-templates"

BOARD_LABELS: set[str] = set(BoardLabel)

TYPE_TO_TEMPLATE: dict[str, str] = {
    TypeLabel.BUG: "bug",
    TypeLabel.FEATURE: "feature",
    TypeLabel.TECHNICAL: "technical",
    TypeLabel.DEBT: "technical",  # debt uses the technical template
}

METHOD_DISPLAY: dict[DetectionMethod, str] = {
    DetectionMethod.PROJECT: "projet",
    DetectionMethod.KEYWORDS: "mots-clés",
    DetectionMethod.CLAUDE: "Claude",
}
