import ast
from pathlib import Path
from typing import Dict, List, Optional

from abstra_internals.repositories.linter.context import (
    LintContext,
    current_lint_context,
)
from abstra_internals.repositories.linter.models import (
    LinterIssue,
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.repositories.project.project import StageWithFile
from abstra_internals.utils.ast_cache import ASTCache


class SendTaskWithoutTransitionFound(LinterIssue):
    title = "send_task calls should have a matching transition"
    type = "warning"
    fix_with_ai = True

    def __init__(
        self,
        task_type: str,
        stage_title: str,
        stage_file: str,
        line_number: int,
    ):
        self.label = (
            f"The stage '{stage_title}' ({stage_file}:{line_number}) calls "
            f"send_task with type '{task_type}', but there is no transition "
            f"configured to receive this task type."
        )
        self.fixes = []


class SendTaskWithoutTransition(PathScopedLinterRule):
    label: str = "send_task calls should have a matching transition"

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        issues = []

        for entrypoint, stage in project.iter_scoped_entrypointed_stages(path):
            try:
                tree = ASTCache.get(entrypoint)
                send_task_calls = self._find_send_task_calls(tree)

                for task_type, line_number in send_task_calls:
                    if not self._has_matching_transition(stage, task_type):
                        issue = SendTaskWithoutTransitionFound(
                            task_type=task_type,
                            stage_title=stage.title,
                            stage_file=stage.file,
                            line_number=line_number,
                        )
                        issue.path = linter_path_key(entrypoint)
                        issues.append(issue)
            except Exception:
                pass

        return issues

    def _find_send_task_calls(self, tree: ast.AST) -> List[tuple[str, int]]:
        """Find all send_task calls with string literal first argument.

        Returns a list of tuples (task_type, line_number).
        """
        send_task_calls = []
        import_info = self._track_send_task_imports(tree)

        if not import_info["direct_import"] and not import_info["module_aliases"]:
            return send_task_calls

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            task_type = self._extract_task_type_from_call(node, import_info)
            if task_type is not None:
                send_task_calls.append((task_type, node.lineno))

        return send_task_calls

    def _track_send_task_imports(self, tree: ast.AST) -> Dict:
        """Track how send_task is imported in the file.

        Returns a dict with:
        - direct_import: Set of names that directly refer to send_task
          (e.g., from "from abstra.tasks import send_task" or
          "from abstra.tasks import send_task as st")
        - module_aliases: Set of module aliases for abstra.tasks
          (e.g., from "import abstra.tasks as at")
        """
        info: Dict = {
            "direct_import": set(),
            "module_aliases": set(),
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module in (
                    "abstra.tasks",
                    "abstra_internals.interface.sdk.tasks",
                ):
                    for alias in node.names:
                        if alias.name == "send_task":
                            info["direct_import"].add(alias.asname or "send_task")

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in (
                        "abstra.tasks",
                        "abstra_internals.interface.sdk.tasks",
                    ):
                        info["module_aliases"].add(alias.asname or alias.name)

        return info

    def _extract_task_type_from_call(
        self, node: ast.Call, import_info: Dict
    ) -> Optional[str]:
        """Extract the task type from a send_task call if it's a string literal.

        Returns None if:
        - The call is not a send_task call
        - The first argument is not a string literal
        """
        is_send_task_call = False

        if isinstance(node.func, ast.Name):
            if node.func.id in import_info["direct_import"]:
                is_send_task_call = True

        elif isinstance(node.func, ast.Attribute):
            if node.func.attr == "send_task":
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id in import_info["module_aliases"]:
                        is_send_task_call = True

        if not is_send_task_call:
            return None

        if not node.args:
            return None

        first_arg = node.args[0]

        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            return first_arg.value

        return None

    def _has_matching_transition(self, stage: StageWithFile, task_type: str) -> bool:
        """Check if the stage has a transition that matches the task type.

        A transition matches if:
        - Its task_type equals the given task_type, OR
        - Its task_type is None or empty (accepts any task type)
        """
        for transition in stage.workflow_transitions:
            if transition.matches(task_type):
                return True
        return False
