from pathlib import Path
from typing import Dict, List, Optional

from abstra_internals.controllers.language_server import get_diagnostics
from abstra_internals.repositories.linter.models import (
    LinterIssue,
    PathScopedLinterRule,
    linter_path_key,
    normalize_linter_path,
)
from abstra_internals.repositories.project.project import LocalProjectRepository


class TypeCheckIssue(LinterIssue):
    def __init__(self, filename: str, messages: List[str]) -> None:
        super().__init__()
        count = len(messages)
        lines = [f"{filename}: {count} issue{'s' if count != 1 else ''}"]
        lines.extend(messages)
        self.label = "\n".join(lines)
        self.fixes = []


class TypeCheckingRule(PathScopedLinterRule):
    label = "Type checking"
    type = "info"
    fix_with_ai = True

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = LocalProjectRepository().load()
        issues: List[LinterIssue] = []

        # Dedupe by normalized path: stages may share the same file, and the
        # LSP diagnostics pass is the most expensive rule in the py group.
        entrypoints: Dict[str, Path] = {}
        for entrypoint in project.iter_entrypoints():
            entrypoints.setdefault(linter_path_key(entrypoint), entrypoint)

        if path is not None:
            key = linter_path_key(path)
            entrypoints = {key: entrypoints[key]} if key in entrypoints else {}

        for key, entrypoint in entrypoints.items():
            file = normalize_linter_path(entrypoint)
            if not file.is_file() or file.suffix != ".py":
                continue

            try:
                code = file.read_text(encoding="utf-8")
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
                issue = TypeCheckIssue(key, messages)
                issue.path = key
                issues.append(issue)

        return issues
