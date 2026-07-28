from typing import List

from abstra_internals.repositories.linter.models import LinterRule

from .abstra_dir_reference import AbstraDirReference
from .bundle_analyzer import BundleAnalyzer
from .conflicting_name import ConflictingName
from .css_syntax import CssSyntax
from .deprecated_functions import DeprecatedFunctionUsage
from .html_and_jinja2_syntax import HtmlAndJinja2Syntax
from .imports_analyzer import ImportsAnalyzer
from .internal_page_reference import InternalPageReference
from .invalid_package_in_requirements import InvalidPackageInRequirements
from .js_syntax import JsSyntax
from .main_block_in_stage import MainBlockInStage
from .missing_env import MissingEnv
from .missing_render_in_page import MissingRenderInPage
from .requirements_analyzer import RequirementsAnalyzer
from .send_task_without_transition import SendTaskWithoutTransition
from .stage_analyzer import StageAnalyzer
from .syntax_errors import SyntaxErrors
from .type_checking import TypeCheckingRule

# --- Rule instances (shared across groups) ---

_syntax_errors = SyntaxErrors()
_deprecated_functions = DeprecatedFunctionUsage()
_missing_env = MissingEnv()
_missing_render_in_page = MissingRenderInPage()
_main_block_in_stage = MainBlockInStage()
_send_task_without_transition = SendTaskWithoutTransition()
_conflicting_name = ConflictingName()
_type_checking = TypeCheckingRule()
_requirements_analyzer = RequirementsAnalyzer()
_invalid_package = InvalidPackageInRequirements()
_stage_analyzer = StageAnalyzer()
_bundle_analyzer = BundleAnalyzer()
_imports_analyzer = ImportsAnalyzer()
_html_and_jinja2_syntax = HtmlAndJinja2Syntax()
_css_syntax = CssSyntax()
_js_syntax = JsSyntax()
_abstra_dir_reference = AbstraDirReference()
_internal_page_reference = InternalPageReference()

# --- Trigger-based rule groups ---
# Instead of running all rules on every file change, run only the
# rules whose result can actually become stale for a given event.

run_after_py_change: List[LinterRule] = [
    _syntax_errors,
    _deprecated_functions,
    _missing_env,
    _missing_render_in_page,
    _main_block_in_stage,
    _send_task_without_transition,
    _conflicting_name,
    _type_checking,
    _stage_analyzer,
    _imports_analyzer,
    _abstra_dir_reference,
    _internal_page_reference,
]

run_after_requirements_change: List[LinterRule] = [
    _requirements_analyzer,
    _invalid_package,
]

run_after_abstra_json_change: List[LinterRule] = [
    _stage_analyzer,
    _send_task_without_transition,
]

run_after_env_or_gitignore_change: List[LinterRule] = [
    _bundle_analyzer,
    _missing_env,
]

run_after_package_install: List[LinterRule] = [
    _imports_analyzer,
    _conflicting_name,
    _requirements_analyzer,
]

run_after_html_change: List[LinterRule] = [
    _html_and_jinja2_syntax,
]

run_after_css_change: List[LinterRule] = [
    _css_syntax,
]

run_after_js_change: List[LinterRule] = [
    _js_syntax,
]

# All rules — used for full checks (deploy, initial load)
_all_groups = [
    run_after_py_change,
    run_after_requirements_change,
    run_after_abstra_json_change,
    run_after_env_or_gitignore_change,
    run_after_package_install,
    run_after_html_change,
    run_after_css_change,
    run_after_js_change,
]
_seen_names: set[str] = set()
rules: List[LinterRule] = []
for _group in _all_groups:
    for _rule in _group:
        if _rule.name not in _seen_names:
            _seen_names.add(_rule.name)
            rules.append(_rule)
