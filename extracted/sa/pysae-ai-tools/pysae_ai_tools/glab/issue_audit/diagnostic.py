"""Internal data model and diagnostic dataclasses."""

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum


class DetectionMethod(StrEnum):
    """How a label/type suggestion was resolved, shared across the audit modules.

    Canonical vocabulary for the ``Violation.method`` detection signal. Rule-specific
    display descriptors (e.g. a template name or a workflow label) stay free-form
    strings — this enum only fixes the detection methods that used to be redeclared as
    loose ``str`` literals in ``classifiers.py``, ``diagnostic.py`` and ``models.py``.
    """

    PROJECT = "project"
    KEYWORDS = "keywords"
    CLAUDE = "claude"
    CACHE = "cache"
    API = "api"
    NONE = "none"


class ViolationFixType(StrEnum):
    STRIP_PREFIX = "strip_prefix"
    TRANSLATE = "translate"
    REPLACE_LABEL = "replace_label"
    REMOVE_LABEL = "remove_label"
    ADD_LABEL = "add_label"
    ADD_BOARD = "add_board"
    KEEP_BOARD = "keep_board"
    FIX_TEMPLATE = "fix_template"


@dataclass
class ViolationFix:
    type: ViolationFixType
    label: str  # human-readable description of the fix


@dataclass
class Violation:
    check: str  # "labels" | "required_labels" | "board" | "weight" | "assignee" | "spec" | "title" | "template"
    severity: str  # "error" | "warning"
    message: str
    fixable: bool | None = None  # None = not yet resolved by fix_plan
    fix: ViolationFix | None = None
    method: str = ""  # detection method: a DetectionMethod value, or a rule-specific descriptor


@dataclass
class IssueReport:
    iid: int
    project_id: int
    project_path: str
    title: str
    web_url: str
    labels: list[str]
    violations: list[Violation] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(v.severity == "error" for v in self.violations)

    @property
    def fixable_violations(self) -> list[Violation]:
        return [v for v in self.violations if v.fixable is True]


# ---------------------------------------------------------------------------
# Shared types
# ---------------------------------------------------------------------------

# Progress callback: (current, total, issue_key, detail)
ProgressCallback = Callable[[int, int, str, str], None]


@dataclass
class RuleContext:
    """Shared context passed to rule methods."""

    group_labels: set[str] = field(default_factory=set)
    project_labels_cache: dict[int, set[str]] = field(default_factory=dict)


@dataclass
class FixTiming:
    """Timing for a single fix resolution."""

    check: str
    fix_type: str
    issue_key: str
    duration_ms: float


@dataclass
class CheckTiming:
    """Timing for a single diagnostic check."""

    check: str
    issue_key: str
    duration_ms: float
