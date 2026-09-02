"""
Setup module for agentic-devtools.

Provides commands for installing external CLI dependencies and verifying
the environment is correctly configured.
"""

from .commands import setup_certs_cmd, setup_check_cmd, setup_cmd, setup_copilot_cli_cmd, setup_gh_cli_cmd
from .exit_codes import (
    ALL_EXIT_CODES,
    EXIT_CODE_DESCRIPTIONS,
    ExitCode,
    code_for,
    get_exit_code_name,
    name_for,
)
from .expectations_specializer import (
    RepositoryConfiguration,
    SpecializationResult,
    resolve_general_doc_path,
    run_specialization,
    specialize_expectations,
)
from .fixloop import (
    MAX_ATTEMPTS_PER_CLASS,
    MAX_TOTAL_ITERATIONS,
    ErrorClass,
    FixAction,
    backoff_seconds,
    classify_outcome,
    next_action,
)
from .gitignore_negations import ensure_root_gitignore_negations
from .issue_type_discovery import check_provider_connectivity, discover_issue_types
from .phases import PHASES
from .report import REPORT_PATH, SCHEMA_VERSION, PhaseResult, SetupReport, make_report, write_report
from .version_guard import VersionGuardResult, check_version_guard, compare_versions

__all__ = [
    "ALL_EXIT_CODES",
    "EXIT_CODE_DESCRIPTIONS",
    "ErrorClass",
    "ExitCode",
    "FixAction",
    "MAX_ATTEMPTS_PER_CLASS",
    "MAX_TOTAL_ITERATIONS",
    "PHASES",
    "PhaseResult",
    "REPORT_PATH",
    "RepositoryConfiguration",
    "SCHEMA_VERSION",
    "SetupReport",
    "SpecializationResult",
    "VersionGuardResult",
    "backoff_seconds",
    "check_provider_connectivity",
    "check_version_guard",
    "classify_outcome",
    "code_for",
    "compare_versions",
    "discover_issue_types",
    "ensure_root_gitignore_negations",
    "get_exit_code_name",
    "make_report",
    "name_for",
    "next_action",
    "resolve_general_doc_path",
    "run_specialization",
    "setup_certs_cmd",
    "setup_check_cmd",
    "setup_cmd",
    "setup_copilot_cli_cmd",
    "setup_gh_cli_cmd",
    "specialize_expectations",
    "write_report",
]
