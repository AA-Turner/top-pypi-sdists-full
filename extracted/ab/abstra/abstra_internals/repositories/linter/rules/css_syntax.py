from pathlib import Path
from typing import List, Optional

import tinycss2

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


class CssSyntaxErrorsFound(LinterIssue):
    def __init__(self, file_path: Path, errors: List[str]):
        bullets = "\n".join(f"  - {err}" for err in errors)
        self.label = f"CSS errors in {file_path.name}:\n{bullets}"
        self.fixes = []


class CssSyntax(PathScopedLinterRule):
    label = "CSS syntax errors"
    type = "error"
    fix_with_ai = True

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        issues: List[LinterIssue] = []

        if path is not None:
            if path.suffix != ".css" or project.is_ignored_path(path):
                return []
            files = [normalize_linter_path(path)]
        else:
            files = list(project.iter_project_files(allowed_suffixes=[".css"]))

        for css_file in files:
            try:
                content = css_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            file_errors: List[str] = []

            # Check stylesheet-level errors
            nodes = tinycss2.parse_stylesheet(content, skip_whitespace=True)
            for node in nodes:
                if node.type == "error":
                    file_errors.append(
                        f"{node.message} at line {node.source_line}, col {node.source_column}"
                    )

            # Check declaration-level errors inside rule blocks
            self._collect_nested_errors(nodes, file_errors)

            if file_errors:
                issue = CssSyntaxErrorsFound(css_file, file_errors)
                issue.path = linter_path_key(css_file)
                issues.append(issue)

        return issues

    def _collect_nested_errors(self, nodes: list, errors: List[str]) -> None:
        for node in nodes:
            if not hasattr(node, "content") or node.content is None:
                continue
            if node.type == "at-rule":
                # At-rules like @media contain nested rules, not declarations
                nested = tinycss2.parse_rule_list(node.content)
                for n in nested:
                    if n.type == "error":
                        errors.append(
                            f"{n.message} at line {n.source_line}, col {n.source_column}"
                        )
                self._collect_nested_errors(nested, errors)
            elif node.type == "qualified-rule":
                declarations = tinycss2.parse_declaration_list(node.content)
                for decl in declarations:
                    if decl.type == "error":
                        errors.append(
                            f"{decl.message} at line {decl.source_line}, col {decl.source_column}"
                        )
