import webbrowser
from pathlib import Path
from typing import List, Optional, Set

from abstra_internals.repositories.linter.context import (
    LintContext,
    current_lint_context,
)
from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.services.env_vars import EnvVarsRepository


class AddEnvToEnvFile(LinterFix):
    def __init__(self, env_var: str):
        self.label = "Add env_var to .env file"
        self.env_var = env_var

    def fix(self):
        EnvVarsRepository.set(self.env_var, value=">> REPLACE ME <<")
        env_uri = EnvVarsRepository.get_env_var_path().absolute().as_uri()
        webbrowser.open(env_uri)


class EnvInCodeNotInEnvFile(LinterIssue):
    title = "Missing env vars"
    type = "warning"

    def __init__(self, filename: Path, lineno: int, env_var: str):
        self.label = f"Env var {env_var} is used in {filename}:{lineno} but not defined in .env file"
        self.fixes = [AddEnvToEnvFile(env_var)]


class MissingEnv(PathScopedLinterRule):
    label: str = "Missing env vars"
    internal_envs: Set[str] = {
        "ABSTRA_RUNNING_IN_BUNDLED_APP",
        "ABSTRA_BUNDLED_APP_PACKAGES_FOLDER",
        "ABSTRA_BUNDLED_APP_ROOT_FOLDER",
        "ABSTRA_ENVIRONMENT",
        "ABSTRA_SELENIUM_URL",
    }

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        if path is not None:
            ctx = current_lint_context() or LintContext()
            key = linter_path_key(path)
            if key not in ctx.project_file_keys:
                return []
            env_vars_in_code_dict = EnvVarsRepository.get_env_vars_in_files([path])
        else:
            env_vars_in_code_dict = EnvVarsRepository.get_env_vars_in_code()

        env_vars_in_code: Set[str] = set(env_vars_in_code_dict.keys())
        env_vars_in_env_file: Set[str] = set(
            [ev.name for ev in EnvVarsRepository.list()]
        )
        missing_env_vars = env_vars_in_code - env_vars_in_env_file - self.internal_envs

        issues = []

        for missing_env_var in missing_env_vars:
            code_paths: Set[str] = set()
            for filename, expr in env_vars_in_code_dict[missing_env_var]:
                code_path = f"{filename}:{expr.lineno}"
                if code_path not in code_paths:
                    code_paths.add(code_path)
                    issue = EnvInCodeNotInEnvFile(
                        filename, expr.lineno, missing_env_var
                    )
                    issue.path = linter_path_key(filename)
                    issues.append(issue)

        return issues
