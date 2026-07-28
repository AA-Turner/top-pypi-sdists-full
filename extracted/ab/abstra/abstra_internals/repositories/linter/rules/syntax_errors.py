from pathlib import Path
from typing import Dict, List, Optional

from abstra_internals.repositories.linter.context import (
    LintContext,
    current_lint_context,
)
from abstra_internals.repositories.linter.models import (
    LinterIssue,
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.utils.ast_cache import ASTCache


class SyntaxErrorFound(LinterIssue):
    title = "Syntax errors"
    type = "error"
    fix_with_ai = True

    def __init__(self, error: SyntaxError) -> None:
        self.label = str(error)
        self.fixes = []


class SyntaxErrors(PathScopedLinterRule):
    label = "Syntax errors"

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        ctx = current_lint_context() or LintContext()

        files: Dict[str, Path] = {}

        if path is not None:
            key = linter_path_key(path)
            if key not in ctx.project_file_keys:
                return []
            files[linter_path_key(path)] = path
        else:
            for file in ctx.project_files:
                files.setdefault(linter_path_key(file), file)

        issues: List[LinterIssue] = []
        for key, file in files.items():
            try:
                ASTCache.get(file)
            except SyntaxError as e:
                # ast.parse is fed the raw content, so the error carries no
                # filename; stamp the project-relative one for the label.
                e.filename = key
                issue = SyntaxErrorFound(e)
                issue.path = key
                issues.append(issue)
            except Exception:
                # Unreadable/missing files are other rules' concern.
                continue

        return issues
