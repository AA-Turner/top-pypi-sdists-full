import ast
from pathlib import Path
from typing import Dict, List, Optional

from abstra_internals.repositories.linter.models import (
    LinterIssue,
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.repositories.project.project import (
    LocalProjectRepository,
)
from abstra_internals.utils.ast_cache import ASTCache

DEPRECATED_FUNCTIONS = {
    "run": {"from": "abstra.tables", "new_function": "run_sql"},
}


class DeprecatedFunctionFound(LinterIssue):
    def __init__(
        self,
        function_name: str,
        new_function_name: str,
        stage_title: str,
        stage_file: str,
        module: str,
    ):
        self.label = f"The stage '{stage_title}' ({stage_file}) uses a deprecated function '{function_name}' from '{module}'. Please use '{new_function_name}' instead."
        self.fixes = []


class DeprecatedFunctionUsage(PathScopedLinterRule):
    label: str = "Deprecated function usage"
    type: str = "warning"
    fix_with_ai: bool = True

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        project = LocalProjectRepository().load()
        issues = []

        for entrypoint, stage in project.iter_scoped_entrypointed_stages(path):
            try:
                tree = ASTCache.get(entrypoint)
                import_map = self.track_imports(tree)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name):
                            function_name = node.func.id
                            if (
                                function_name in DEPRECATED_FUNCTIONS
                                and DEPRECATED_FUNCTIONS[function_name]["from"]
                                == import_map.get(function_name)
                            ):
                                new_function_name = DEPRECATED_FUNCTIONS[function_name][
                                    "new_function"
                                ]
                                module = DEPRECATED_FUNCTIONS[function_name]["from"]
                                issue = DeprecatedFunctionFound(
                                    function_name,
                                    new_function_name,
                                    stage_title=stage.title,
                                    stage_file=stage.file,
                                    module=module,
                                )
                                issue.path = linter_path_key(entrypoint)
                                issues.append(issue)

            except Exception as e:
                print(f"Error while processing {entrypoint}: {e}")

        return issues

    def track_imports(self, tree: ast.AST) -> Dict[str, str]:
        import_map = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_map[alias.asname or alias.name.split(".")[-1]] = alias.name

            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                for alias in node.names:
                    import_map[alias.asname or alias.name] = module_name

        return import_map
