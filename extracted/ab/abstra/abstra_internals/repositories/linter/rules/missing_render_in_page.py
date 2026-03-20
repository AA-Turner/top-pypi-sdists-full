import ast
from typing import List

from abstra_internals.repositories.linter.models import (
    LinterIssue,
    LinterRule,
)
from abstra_internals.repositories.project.project import (
    LocalProjectRepository,
    PageStage,
)
from abstra_internals.utils.ast_cache import ASTCache


class MissingRenderInPageFound(LinterIssue):
    def __init__(self, stage: PageStage):
        self.label = (
            f"The page '{stage.title}' ({stage.file}) does not define a __render__ function. "
            f"Every page stage must have a @register_function decorated function named __render__ "
            f"that returns the HTML content."
        )
        self.fixes = []


class MissingRenderInPage(LinterRule):
    label = "Page stages must define a __render__ function"
    type = "bug"
    fix_with_ai = True

    def find_issues(self) -> List[LinterIssue]:
        project = LocalProjectRepository().load()
        issues = []

        for page in project.pages:
            if not page.file_path.exists():
                continue

            try:
                tree = ASTCache.get(page.file_path)
                if not self._has_render_function(tree):
                    issues.append(MissingRenderInPageFound(page))
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
