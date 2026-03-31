from pathlib import Path
from typing import List

from abstra_internals.controllers.language_server import get_diagnostics
from abstra_internals.repositories.linter.models import LinterIssue, LinterRule
from abstra_internals.repositories.project.project import LocalProjectRepository


class TypeCheckIssue(LinterIssue):
    def __init__(self, filename: str, messages: List[str]) -> None:
        super().__init__()
        count = len(messages)
        lines = [f"{filename}: {count} issue{'s' if count != 1 else ''}"]
        lines.extend(messages)
        self.label = "\n".join(lines)
        self.fixes = []


class TypeCheckingRule(LinterRule):
    label = "Type checking"
    type = "info"
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
            messages = []
            for diag in diagnostics:
                if diag.get("severity", 1) > 2:
                    continue
                line = diag.get("range", {}).get("start", {}).get("line", 0) + 1
                message = diag.get("message", "Type error")
                messages.append(f"  Line {line}: {message}")
            if messages:
                issues.append(TypeCheckIssue(str(path), messages))

        return issues
