from pathlib import Path
from typing import List

import tree_sitter_javascript as tsjs
from tree_sitter import Language, Parser

from abstra_internals.repositories.linter.models import LinterIssue, LinterRule
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings

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
    def __init__(self, file_path: Path, errors: List[str]):
        bullets = "\n".join(f"  - {err}" for err in errors)
        self.label = f"JS errors in {file_path.name}:\n{bullets}"
        self.fixes = []


class JsSyntax(LinterRule):
    label = "JavaScript syntax errors"
    type = "bug"
    fix_with_ai = True

    def find_issues(self) -> List[LinterIssue]:
        issues: List[LinterIssue] = []
        root = Settings.root_path
        parser = Parser(JS_LANGUAGE)

        for js_file in FileSystemService.list_files(root, allowed_suffixes=[".js"]):
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
                issues.append(JsSyntaxErrorsFound(js_file, file_errors))

        return issues
