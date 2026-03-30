from pathlib import Path
from typing import List

from abstra_internals.controllers.language_server import get_diagnostics
from abstra_internals.repositories.linter.models import LinterIssue, LinterRule
from abstra_internals.repositories.project.project import LocalProjectRepository


class TypeCheckIssue(LinterIssue):
    def __init__(self, filename: str, line: int, message: str) -> None:
        super().__init__()
        self.label = f"{filename}:{line} — {message}"
        self.fixes = []


class TypeCheckingRule(LinterRule):
    label = "Type checking"
    type = "bug"
    fix_with_ai = True

    def find_issues(self) -> List[LinterIssue]:
        project = LocalProjectRepository().load()
        issues: List[LinterIssue] = []

        for entrypoint in project.iter_entrypoints():
            path = Path(entrypoint)
            if not path.is_file() or path.suffix != ".py":
                continue

            try:
                code = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            diagnostics = get_diagnostics(code)
            for diag in diagnostics:
                severity = diag.get("severity", 1)
                # Only report errors (severity 1) and warnings (severity 2)
                if severity > 2:
                    continue
                line = diag.get("range", {}).get("start", {}).get("line", 0) + 1
                message = diag.get("message", "Type error")
                issues.append(TypeCheckIssue(str(path), line, message))

        return issues
