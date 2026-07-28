from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from abstra_internals.settings import Settings


def normalize_linter_path(path: Path) -> Path:
    if not path.is_absolute():
        path = Settings.root_path / path
    return path.resolve()


def linter_path_key(path: Path) -> str:
    """Stable string key used to scope issues to a file (LinterIssue.path).

    Root-relative posix path; falls back to the absolute posix path for
    files outside the project root (the file_outside_project case).
    """
    resolved = normalize_linter_path(path)
    try:
        return resolved.relative_to(Settings.root_path.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


class LinterFix:
    label: str

    def fix(self):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__

    def make_label(self):
        return self.label

    def to_dict(self):
        return dict(name=self.name, label=self.make_label())

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, LinterFix):
            return False
        return self.name == __value.name


class LinterIssue:
    title: str
    label: str
    fixes: List[LinterFix]
    type: str  # "error" | "warning"
    fix_with_ai: bool = False
    # File this issue is scoped to (linter_path_key format). None means
    # project-global (e.g. "abstra missing in requirements.txt"). Used by the
    # repository to merge path-scoped re-runs without dropping other files'
    # issues.
    path: Optional[str] = None

    def make_title(self):
        return self.title

    def make_label(self):
        return self.label

    def to_dict(self):
        return dict(
            title=self.make_title(),
            label=self.make_label(),
            type=self.type,
            fixes=[fix.to_dict() for fix in self.fixes],
            fixWithAi=self.fix_with_ai,
        )


class LinterCheck:
    name: str
    label: str
    issues: List[LinterIssue]
    # "failed" means the rule crashed and produced no verdict: the empty
    # issues list must not be read as a pass (UI reports partial coverage,
    # the deploy gate treats any failed check as blocking).
    status: str

    def __init__(
        self,
        name: str,
        label: str,
        issues: List[LinterIssue],
        status: str = "ok",
    ):
        self.name = name
        self.label = label
        self.issues = issues
        self.status = status

    def to_dict(self):
        return dict(
            name=self.name,
            label=self.label,
            issues=[issue.to_dict() for issue in self.issues],
            status=self.status,
        )


def deploy_gate_message(blocking: List["LinterCheck"]) -> str:
    """User-facing reason for a blocked deploy. Real issues take precedence
    (they must be fixed regardless); a could-not-verify message only shows
    when failed blocking rules are the sole reason for the block."""
    if any(check.issues for check in blocking):
        return "Please fix all linter issues before deploying your project."
    failed = ", ".join(
        check.label or check.name for check in blocking if check.status == "failed"
    )
    return (
        f"Could not verify before deploy: {failed}. Please try again. "
        "If the problem persists, contact support."
    )


class LinterContractError(Exception):
    """An issue has no button: no fix and fix_with_ai=False."""


def assert_actionable(rule_name: str, issues: Iterable[LinterIssue]) -> None:
    """Raise LinterContractError unless every issue is actionable.

    Mirrors the editor's button predicate: each issue must carry at least one
    fix or set fix_with_ai. Called by the ``actionability`` test (a CI check).
    """
    for issue in issues:
        if not issue.fixes and not issue.fix_with_ai:
            raise LinterContractError(
                f"Linter rule {rule_name!r} surfaced an issue with no fixes and "
                f"fix_with_ai=False, so the editor renders it with no button: "
                f"{issue.make_label()!r}. Give the issue a LinterFix, or set "
                f"fix_with_ai = True on it."
            )


class LinterRule:
    label: str

    def find_issues(self) -> Sequence[LinterIssue]:
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__

    def check(self) -> LinterCheck:
        return LinterCheck(
            name=self.name,
            label=self.label,
            issues=list(self.find_issues()),
        )


class PathScopedLinterRule(LinterRule):
    def find_issues(self, path: Optional[Path] = None) -> Sequence[LinterIssue]:
        raise NotImplementedError


rules = []
