from pathlib import Path
from typing import List

import tinycss2

from abstra_internals.repositories.linter.models import LinterIssue, LinterRule
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings


class CssSyntaxErrorsFound(LinterIssue):
    def __init__(self, file_path: Path, errors: List[str]):
        bullets = "\n".join(f"  - {err}" for err in errors)
        self.label = f"CSS errors in {file_path.name}:\n{bullets}"
        self.fixes = []


class CssSyntax(LinterRule):
    label = "CSS syntax errors"
    type = "bug"
    fix_with_ai = True

    def find_issues(self) -> List[LinterIssue]:
        issues: List[LinterIssue] = []
        root = Settings.root_path

        for css_file in FileSystemService.list_files(root, allowed_suffixes=[".css"]):
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
                issues.append(CssSyntaxErrorsFound(css_file, file_errors))

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
