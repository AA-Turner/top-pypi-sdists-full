import os
from typing import List

from abstra_internals.repositories.linter.models import LinterRule

from .big_py_files import BigPyFiles
from .conflicting_name import ConflictingName
from .conflicting_path import ConflictingPath
from .deprecated_functions import DeprecatedFunctionUsage
from .duplicate_package_in_requirements import DuplicatePackagesInRequirements
from .env_in_bundle import EnvInBundle
from .file_outside_project import FileOutsideProjectRoot
from .imports_requirements_analyzer import ImportsRequirementsAnalyzer
from .invalid_package_in_requirements import InvalidPackageInRequirements
from .local_package_in_requirements import LocalPackageInRequirements
from .missing_abstra_in_requirements import MissingAbstraInRequirements
from .missing_entrypoint import MissingEntrypoint
from .missing_env import MissingEnv
from .missing_render_in_page import MissingRenderInPage
from .new_version_of_abstra_available import NewVersionOfAbstraAvailable
from .psycopg2 import Psycopg2MustBeBinary
from .send_task_without_transition import SendTaskWithoutTransition
from .syntax_errors import SyntaxErrors
from .type_checking import TypeCheckingRule
from .venv_in_bundle import VenvInBundle

# --- Rule instances (shared across groups) ---

_syntax_errors = SyntaxErrors()
_deprecated_functions = DeprecatedFunctionUsage()
_missing_env = MissingEnv()
_missing_render_in_page = MissingRenderInPage()
_send_task_without_transition = SendTaskWithoutTransition()
_big_py_files = BigPyFiles()
_conflicting_name = ConflictingName()
_type_checking = TypeCheckingRule()
_duplicate_packages = DuplicatePackagesInRequirements()
_invalid_package = InvalidPackageInRequirements()
_local_package = LocalPackageInRequirements()
_missing_abstra = MissingAbstraInRequirements()
_psycopg2 = Psycopg2MustBeBinary()
_conflicting_path = ConflictingPath()
_file_outside_project = FileOutsideProjectRoot()
_missing_entrypoint = MissingEntrypoint()
_env_in_bundle = EnvInBundle()
_venv_in_bundle = VenvInBundle()
_imports_analyzer = ImportsRequirementsAnalyzer()

_new_version: List[LinterRule] = []
if not os.getenv("ABSTRA_RUNNING_IN_BUNDLED_APP"):
    _new_version = [NewVersionOfAbstraAvailable()]

# --- Trigger-based rule groups ---
# Instead of running all rules on every file change, run only the
# rules whose result can actually become stale for a given event.

run_after_py_change: List[LinterRule] = [
    _syntax_errors,
    _deprecated_functions,
    _missing_env,
    _missing_render_in_page,
    _send_task_without_transition,
    _big_py_files,
    _conflicting_name,
    _type_checking,
    _missing_entrypoint,
    _file_outside_project,
    _imports_analyzer,
]

run_after_requirements_change: List[LinterRule] = [
    _duplicate_packages,
    _invalid_package,
    _local_package,
    _missing_abstra,
    _psycopg2,
]

run_after_abstra_json_change: List[LinterRule] = [
    _conflicting_path,
    _file_outside_project,
    _missing_entrypoint,
    _send_task_without_transition,
]

run_after_env_or_gitignore_change: List[LinterRule] = [
    _env_in_bundle,
    _venv_in_bundle,
    _missing_env,
]

run_after_package_install: List[LinterRule] = [
    _imports_analyzer,
    _conflicting_name,
    _missing_abstra,
    *_new_version,
]

# All rules — used for full checks (deploy, initial load)
_all_groups = [
    run_after_py_change,
    run_after_requirements_change,
    run_after_abstra_json_change,
    run_after_env_or_gitignore_change,
    run_after_package_install,
]
_seen_names: set[str] = set()
rules: List[LinterRule] = []
for _group in _all_groups:
    for _rule in _group:
        if _rule.name not in _seen_names:
            _seen_names.add(_rule.name)
            rules.append(_rule)
