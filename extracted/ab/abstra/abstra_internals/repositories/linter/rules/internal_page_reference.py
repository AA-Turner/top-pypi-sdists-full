import ast
import re
from pathlib import Path
from typing import Iterator, List, Optional, Tuple

from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.linter.context import (
    LintContext,
    current_lint_context,
)
from abstra_internals.repositories.linter.models import (
    LinterIssue,
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.settings import Settings
from abstra_internals.utils.ast_cache import ASTCache

# Matches the internal "/_page" / "/_pages" RPC route prefix inside a string
# literal (a redirect target, an inline HTML href, a JS navigation, etc.).
# These routes are internal runtime plumbing — the iframe source and the
# function-call POST endpoint — never a valid navigation target. The capture
# extends to the rest of the URL token so the reported literal is short even
# when it lives inside a large inline-HTML render string.
INTERNAL_PAGE_RE = re.compile(r"/_pages?[/-][^\s\"'<>)]*")


class InternalPageReferenceFound(LinterIssue):
    title = "Avoid linking to internal page addresses"
    type = "warning"
    fix_with_ai = True

    def __init__(self, file: str, line: int, literal: str):
        self.label = (
            f"{file}:{line}: the link '{literal}' points to an internal address "
            f"that opens a broken page for your visitors. Link to the page's "
            f"normal path instead, like '/other-page'."
        )
        self.fixes = []


class InternalPageReference(PathScopedLinterRule):
    label: str = "Avoid linking to internal page addresses"

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        issues: List[LinterIssue] = []

        for py_file in project.iter_scoped_py_files(path):
            try:
                tree = ASTCache.get(py_file)
                for literal, line in self._find_page_refs(tree):
                    issue = InternalPageReferenceFound(
                        file=self._display_path(py_file),
                        line=line,
                        literal=literal,
                    )
                    issue.path = linter_path_key(py_file)
                    issues.append(issue)
            except FileNotFoundError:
                # File deleted/renamed mid-pass — normal, skip silently.
                continue
            except SyntaxError:
                # Broken Python is the SyntaxErrors rule's concern, not ours.
                continue
            except Exception as e:
                AbstraLogger.error(
                    f"[{self.name}] Error while processing {py_file}: {e}"
                )

        return issues

    def _display_path(self, py_file: Path) -> str:
        try:
            return (
                py_file.resolve().relative_to(Settings.root_path.resolve()).as_posix()
            )
        except ValueError:
            return py_file.name

    def _find_page_refs(self, tree: ast.AST) -> Iterator[Tuple[str, int]]:
        # ast.walk reaches every string Constant directly, including the literal
        # chunks of f-strings (the JoinedStr's children) and the inline HTML that
        # a page's __render__ returns as a Python string — so a single Constant
        # scan covers redirect("/_page/x") and embedded <a href="/_page/x">.
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                for match in INTERNAL_PAGE_RE.finditer(node.value):
                    yield match.group(0), node.lineno
