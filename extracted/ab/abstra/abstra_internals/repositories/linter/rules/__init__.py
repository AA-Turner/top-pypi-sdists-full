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
from .missing_task_schema_for_agent_target import MissingTaskSchemaForAgentTarget
from .new_version_of_abstra_available import NewVersionOfAbstraAvailable
from .psycopg2 import Psycopg2MustBeBinary
from .send_task_without_transition import SendTaskWithoutTransition
from .syntax_errors import SyntaxErrors
from .type_checking import TypeCheckingRule
from .venv_in_bundle import VenvInBundle

core_rules: List[LinterRule] = [
    EnvInBundle(),
    VenvInBundle(),
    SyntaxErrors(),
    MissingEntrypoint(),
    MissingAbstraInRequirements(),
    DuplicatePackagesInRequirements(),
    InvalidPackageInRequirements(),
    LocalPackageInRequirements(),
    ImportsRequirementsAnalyzer(),
    MissingEnv(),
    ConflictingPath(),
    Psycopg2MustBeBinary(),
    ConflictingName(),
    DeprecatedFunctionUsage(),
    BigPyFiles(),
    FileOutsideProjectRoot(),
    MissingTaskSchemaForAgentTarget(),
    SendTaskWithoutTransition(),
    MissingRenderInPage(),
    TypeCheckingRule(),
]

conditional_rules: List[LinterRule] = []

if not os.getenv("ABSTRA_RUNNING_IN_BUNDLED_APP"):
    conditional_rules = [NewVersionOfAbstraAvailable()]

rules: List[LinterRule] = core_rules + conditional_rules
