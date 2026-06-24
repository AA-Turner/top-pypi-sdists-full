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

# Matches ".abstra" as a path segment inside a string literal: ".abstra/",
# ".abstra\" or a trailing ".abstra". Avoids matching things like
# "my.abstra.module" where ".abstra" is not followed by a path separator.
ABSTRA_PATH_RE = re.compile(r"(^|[\"'/\\\s])\.abstra([/\\]|$)")


class AbstraDirReferenceFound(LinterIssue):
    def __init__(self, file: str, line: int, literal: str):
        self.label = (
            f"{file}:{line} hardcodes an internal '.abstra' path: '{literal}'. "
            f"The '.abstra' directory location differs between local and cloud. "
            f"Use the SDK helpers instead: 'from abstra.common import "
            f"get_persistent_dir' and build paths from those."
        )
        self.fixes = []


class AbstraDirReference(PathScopedLinterRule):
    label: str = "Avoid hardcoding '.abstra' internal paths"
    type: str = "warning"
    fix_with_ai: bool = True

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        issues: List[LinterIssue] = []

        for py_file in project.iter_scoped_py_files(path):
            try:
                tree = ASTCache.get(py_file)
                for literal, line in self._find_abstra_refs(tree):
                    issue = AbstraDirReferenceFound(
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

    def _find_abstra_refs(self, tree: ast.AST) -> Iterator[Tuple[str, int]]:
        # ast.walk reaches every string Constant directly, including the
        # literal chunks of f-strings (the JoinedStr's children), so a single
        # Constant check covers both plain strings and f-strings.
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if ABSTRA_PATH_RE.search(node.value):
                    yield node.value, node.lineno
