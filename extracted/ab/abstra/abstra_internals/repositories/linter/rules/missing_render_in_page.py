import ast
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
)
from abstra_internals.repositories.project.project import PageStage
from abstra_internals.utils.ast_cache import ASTCache


class MissingRenderInPageFound(LinterIssue):
    def __init__(self, stage: PageStage):
        self.label = (
            f"The page '{stage.title}' ({stage.file}) does not define a __render__ function. "
            f"Every page stage must have a @register_function decorated function named __render__ "
            f"that returns the HTML content."
        )
        self.fixes = []


class MissingRenderInPage(PathScopedLinterRule):
    label = "Page stages must define a __render__ function"
    type = "error"
    fix_with_ai = True

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        issues = []

        pages = project.pages
        if path is not None:
            key = linter_path_key(path)
            pages = [p for p in pages if linter_path_key(p.file_path) == key]

        for page in pages:
            if not page.file_path.exists():
                continue

            try:
                tree = ASTCache.get(page.file_path)
                if not self._has_render_function(tree):
                    issue = MissingRenderInPageFound(page)
                    issue.path = linter_path_key(page.file_path)
                    issues.append(issue)
            except Exception:
                pass

        return issues

    def _has_render_function(self, tree: ast.AST) -> bool:
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            if node.name != "__render__":
                continue
            for decorator in node.decorator_list:
                if (
                    isinstance(decorator, ast.Name)
                    and decorator.id == "register_function"
                ):
                    return True
                if (
                    isinstance(decorator, ast.Attribute)
                    and decorator.attr == "register_function"
                ):
                    return True
        return False
