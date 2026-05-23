import ast
from typing import List

from abstra_internals.repositories.linter.models import (
    LinterIssue,
    LinterRule,
)
from abstra_internals.repositories.project.project import (
    LocalProjectRepository,
)
from abstra_internals.utils.ast_cache import ASTCache


class MainBlockInStageFound(LinterIssue):
    def __init__(self, stage_title: str, stage_file: str):
        self.label = (
            f"The stage '{stage_title}' ({stage_file}) contains an "
            f"'if __name__ == \"__main__\":' block. Abstra stages are not "
            f"executed as __main__, so this block is dead code and should be removed."
        )
        self.fixes = []


class MainBlockInStage(LinterRule):
    label: str = "Stages should not contain 'if __name__ == \"__main__\":' blocks"
    type: str = "warning"
    fix_with_ai: bool = True

    def find_issues(self) -> List[LinterIssue]:
        project = LocalProjectRepository().load()
        issues: List[LinterIssue] = []

        for entrypoint, stage in project.iter_entrypointed_stages():
            try:
                tree = ASTCache.get(entrypoint)
                if self._has_main_block(tree):
                    issues.append(
                        MainBlockInStageFound(
                            stage_title=stage.title,
                            stage_file=stage.file,
                        )
                    )
            except Exception as e:
                print(f"Error while processing {entrypoint}: {e}")

        return issues

    def _has_main_block(self, tree: ast.AST) -> bool:
        for node in ast.walk(tree):
            if isinstance(node, ast.If) and self._is_main_check(node.test):
                return True
        return False

    def _is_main_check(self, test: ast.expr) -> bool:
        if not isinstance(test, ast.Compare):
            return False
        if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
            return False

        left = test.left
        right = test.comparators[0]

        if self._is_name_dunder(left) and self._is_main_constant(right):
            return True
        if self._is_main_constant(left) and self._is_name_dunder(right):
            return True
        return False

    def _is_name_dunder(self, node: ast.expr) -> bool:
        return isinstance(node, ast.Name) and node.id == "__name__"

    def _is_main_constant(self, node: ast.expr) -> bool:
        return isinstance(node, ast.Constant) and node.value == "__main__"
