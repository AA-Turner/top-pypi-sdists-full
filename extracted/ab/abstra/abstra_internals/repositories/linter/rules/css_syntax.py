from pathlib import Path
from typing import List

import tinycss2

from abstra_internals.repositories.linter.models import LinterIssue, LinterRule
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings


class CssSyntaxErrorFound(LinterIssue):
    def __init__(self, error_message: str, file_path: Path):
        self.label = f"CSS error in {file_path.name}: {error_message}"
        self.fixes = []


class CssSyntax(LinterRule):
    label = "CSS syntax errors"
    type = "bug"
    fix_with_ai = True

    def find_issues(self) -> List[LinterIssue]:
        issues = []
        root = Settings.root_path

        for css_file in FileSystemService.list_files(root, allowed_suffixes=[".css"]):
            try:
                content = css_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            # Check stylesheet-level errors
            nodes = tinycss2.parse_stylesheet(content, skip_whitespace=True)
            for node in nodes:
                if node.type == "error":
                    msg = f"{node.message} at line {node.source_line}, col {node.source_column}"
                    issues.append(CssSyntaxErrorFound(msg, css_file))

            # Check declaration-level errors inside rule blocks
            self._check_nodes(nodes, css_file, issues)

        return issues

    def _check_nodes(
        self,
        nodes: list,
        css_file: Path,
        issues: List[LinterIssue],
    ) -> None:
        for node in nodes:
            if not hasattr(node, "content") or node.content is None:
                continue
            if node.type == "at-rule":
                # At-rules like @media contain nested rules, not declarations
                nested = tinycss2.parse_rule_list(node.content)
                for n in nested:
                    if n.type == "error":
                        msg = f"{n.message} at line {n.source_line}, col {n.source_column}"
                        issues.append(CssSyntaxErrorFound(msg, css_file))
                self._check_nodes(nested, css_file, issues)
            elif node.type == "qualified-rule":
                declarations = tinycss2.parse_declaration_list(node.content)
                for decl in declarations:
                    if decl.type == "error":
                        msg = f"{decl.message} at line {decl.source_line}, col {decl.source_column}"
                        issues.append(CssSyntaxErrorFound(msg, css_file))
