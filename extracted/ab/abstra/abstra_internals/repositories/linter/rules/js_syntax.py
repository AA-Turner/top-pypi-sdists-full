from pathlib import Path
from typing import List, Optional

import tree_sitter_javascript as tsjs
from tree_sitter import Language, Parser

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

# tree-sitter is a recovery parser designed for editors — it reports error
# locations but not descriptive messages (e.g. "Unexpected token ;").
# For richer error details we'd need Node.js + acorn in the web editor
# containers, which would make the images way bigger.
# In addition, tree-sitter is very fast and lightweight.
JS_LANGUAGE = Language(tsjs.language())


def _find_errors(node, errors=None):
    if errors is None:
        errors = []
    if node.type == "ERROR" or node.is_missing:
        errors.append(node.start_point)
    for child in node.children:
        _find_errors(child, errors)
    return errors


class JsSyntaxErrorsFound(LinterIssue):
    title = "JavaScript syntax errors"
    type = "error"
    fix_with_ai = True

    def __init__(self, file_path: Path, errors: List[str]):
        bullets = "\n".join(f"  - {err}" for err in errors)
        self.label = f"JS errors in {file_path.name}:\n{bullets}"
        self.fixes = []


class JsSyntax(PathScopedLinterRule):
    label = "JavaScript syntax errors"

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        issues: List[LinterIssue] = []
        parser = Parser(JS_LANGUAGE)

        if path is not None:
            if path.suffix != ".js" or project.is_ignored_path(path):
                return []
            files = [normalize_linter_path(path)]
        else:
            files = list(project.iter_project_files(allowed_suffixes=[".js"]))

        for js_file in files:
            try:
                content = js_file.read_bytes()
            except OSError:
                continue

            if not content.strip():
                continue

            tree = parser.parse(content)
            if not tree.root_node.has_error:
                continue

            file_errors = [
                f"syntax error at line {row + 1}, col {col}"
                for row, col in _find_errors(tree.root_node)
            ]
            if file_errors:
                issue = JsSyntaxErrorsFound(js_file, file_errors)
                issue.path = linter_path_key(js_file)
                issues.append(issue)

        return issues
