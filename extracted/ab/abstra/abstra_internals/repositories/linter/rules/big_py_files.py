from pathlib import Path
from typing import List, Optional

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

# Constant to make it easy to change the line limit
MAX_LINES_THRESHOLD = 1000


class BigPyFileFound(LinterIssue):
    def __init__(self, file_path: Path, line_count: int):
        self.label = f"File {file_path.name} has {line_count} lines (limit: {MAX_LINES_THRESHOLD}). Consider splitting this file into multiple smaller files organized by responsibilities to improve code maintainability."
        self.fixes = []  # No automatic fix available for this type of issue


class BigPyFiles(PathScopedLinterRule):
    label = "Large Python files"
    type = "info"
    fix_with_ai = True

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        issues = []

        for py_file in project.iter_scoped_py_files(path):
            try:
                file = normalize_linter_path(py_file)
                if file.exists() and file.is_file():
                    # Count the number of lines in the file
                    with open(file, "r", encoding="utf-8") as f:
                        line_count = sum(1 for _ in f)

                    # If it exceeds the limit, add an issue
                    if line_count > MAX_LINES_THRESHOLD:
                        issue = BigPyFileFound(py_file, line_count)
                        issue.path = linter_path_key(py_file)
                        issues.append(issue)
            except (UnicodeDecodeError, OSError):
                # Ignore files that cannot be read as text
                continue

        return issues
