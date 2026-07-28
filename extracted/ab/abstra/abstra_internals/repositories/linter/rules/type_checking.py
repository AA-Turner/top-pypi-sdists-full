from pathlib import Path
from typing import Dict, List, Optional

from abstra_internals.controllers.language_server import get_diagnostics_checked
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.linter.context import (
    LintContext,
    current_lint_context,
)
from abstra_internals.repositories.linter.models import (
    LinterIssue,
    PathScopedLinterRule,
    linter_path_key,
    normalize_linter_path,
)


class TypeCheckIssue(LinterIssue):
    title = "Type checking"
    type = "warning"
    fix_with_ai = True

    def __init__(self, filename: str, messages: List[str]) -> None:
        super().__init__()
        count = len(messages)
        lines = [f"{filename}: {count} issue{'s' if count != 1 else ''}"]
        lines.extend(messages)
        self.label = "\n".join(lines)
        self.fixes = []


class TypeCheckingRule(PathScopedLinterRule):
    label = "Type checking"

    # If Pyrefly stays mute for this many consecutive files, stop the pass:
    # each unanswered file costs a full request timeout, so a dead/mute server
    # would otherwise burn timeout×entrypoints and blow the deploy/lint budget
    # (the original Windows report: 62 files × 5s ≈ 310s, past the 600s gate).
    _UNRESPONSIVE_LIMIT = 5

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        issues: List[LinterIssue] = []

        # Dedupe by normalized path: stages may share the same file, and the
        # LSP diagnostics pass is the most expensive rule in the py group.
        entrypoints: Dict[str, Path] = {}
        for entrypoint in project.iter_entrypoints():
            entrypoints.setdefault(linter_path_key(entrypoint), entrypoint)

        if path is not None:
            key = linter_path_key(path)
            entrypoints = {key: entrypoints[key]} if key in entrypoints else {}

        consecutive_unresponsive = 0
        for key, entrypoint in entrypoints.items():
            file = normalize_linter_path(entrypoint)
            if not file.is_file() or file.suffix != ".py":
                continue

            try:
                code = file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            diagnostics, responded = get_diagnostics_checked(code)
            if not responded:
                consecutive_unresponsive += 1
                if consecutive_unresponsive >= self._UNRESPONSIVE_LIMIT:
                    AbstraLogger.warning(
                        "[TypeChecking] Pyrefly unresponsive after %d files; "
                        "skipping type checking for the rest of this pass"
                        % consecutive_unresponsive
                    )
                    break
                continue
            consecutive_unresponsive = 0
            messages = []
            for diag in diagnostics:
                if diag.get("severity", 1) > 2:
                    continue
                line = diag.get("range", {}).get("start", {}).get("line", 0) + 1
                message = diag.get("message", "Type error")
                messages.append(f"  Line {line}: {message}")
            if messages:
                issue = TypeCheckIssue(key, messages)
                issue.path = key
                issues.append(issue)

        return issues
