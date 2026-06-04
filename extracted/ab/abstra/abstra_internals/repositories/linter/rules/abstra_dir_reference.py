import ast
import re
from pathlib import Path
from typing import Iterator, List, Tuple

from abstra_internals.repositories.linter.models import (
    LinterIssue,
    LinterRule,
)
from abstra_internals.repositories.project.project import (
    LocalProjectRepository,
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


class AbstraDirReference(LinterRule):
    label: str = "Avoid hardcoding '.abstra' internal paths"
    type: str = "warning"
    fix_with_ai: bool = True

    def find_issues(self) -> List[LinterIssue]:
        project = LocalProjectRepository().load()
        issues: List[LinterIssue] = []

        for py_file in project.iter_py_files():
            try:
                tree = ASTCache.get(py_file)
                for literal, line in self._find_abstra_refs(tree):
                    issues.append(
                        AbstraDirReferenceFound(
                            file=self._display_path(py_file),
                            line=line,
                            literal=literal,
                        )
                    )
            except Exception as e:
                print(f"Error while processing {py_file}: {e}")

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
