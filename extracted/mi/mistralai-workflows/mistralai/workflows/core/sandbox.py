import importlib.util
import pkgutil
import traceback
from functools import cache

import structlog
from temporalio.worker.workflow_sandbox import RestrictedWorkflowAccessError, SandboxRestrictions

import mistralai.workflows as _workflows_pkg
from mistralai.workflows.plugins._discovery import PLUGIN_NAMESPACE, list_plugins

logger = structlog.get_logger(__name__)

_EXCLUDED_PREFIXES = (
    "mistralai.workflows.plugins.webhook.examples",
    "mistralai.workflows.plugins.mistralai.connectors.examples",
    "mistralai.workflows.plugins.evaluation._orchestrator",
    "mistralai_workflow_tests",
)

_BASE_PASSTHROUGH_MODULES = (
    "mistralai.client.models",
    "mistralai.observability.models",
    "mistralai.observability.api_models",
    "mistralai.observability.statistics",
    "mistralai.observability.utils",
)


def _discover_workflow_modules() -> tuple[str, ...]:
    """Walk mistralai.workflows and return all submodules except excluded ones.

    Plugins are discovered dynamically via list_plugins() and their submodules
    are walked separately (without importing them) to avoid listing the plugin
    root packages as passthrough modules.
    """
    plugins = list_plugins()
    plugin_roots = [f"{PLUGIN_NAMESPACE}.{p.name}" for p in plugins]
    excluded = (*_EXCLUDED_PREFIXES, *plugin_roots)

    # Core workflow modules (excluding plugin roots and their submodules)
    modules = [
        modname
        for _importer, modname, _ispkg in pkgutil.walk_packages(_workflows_pkg.__path__, prefix="mistralai.workflows.")
        if not any(modname == ex or modname.startswith(ex + ".") for ex in excluded)
    ]

    # Plugin submodules (excluding examples)
    for root in plugin_roots:
        spec = importlib.util.find_spec(root)
        if spec is None or spec.submodule_search_locations is None:
            continue
        for _, modname, _ in pkgutil.walk_packages(spec.submodule_search_locations, prefix=root + "."):
            if not any(modname == ex or modname.startswith(ex + ".") for ex in _EXCLUDED_PREFIXES):
                modules.append(modname)

    return (*modules, *_BASE_PASSTHROUGH_MODULES)


@cache
def get_sandbox_restrictions() -> SandboxRestrictions:
    sandbox_passthrough_modules = _discover_workflow_modules()
    return SandboxRestrictions.default.with_passthrough_modules(*sandbox_passthrough_modules)


_SANDBOX_INTERNAL_MARKERS = (
    "temporalio/",
    "<frozen importlib",
    "<string>",
)

_THIRD_PARTY_MARKERS = (
    "site-packages/",
    ".venv/",
)


def _find_sandbox_restriction_error(exc: BaseException) -> RestrictedWorkflowAccessError | None:
    """Walk the exception chain to find a RestrictedWorkflowAccessError."""
    current: BaseException | None = exc
    while current is not None:
        if isinstance(current, RestrictedWorkflowAccessError):
            return current
        current = current.__cause__
    return None


def _format_sandbox_import_chain(exc: RestrictedWorkflowAccessError) -> str:
    """Build a human-readable import chain from the sandbox error traceback.

    Categorizes frames into "your code" vs "third-party library" and filters
    out temporal/sandbox internals, so the user can see exactly which import
    in their code triggers the violation and which library is responsible.
    """
    tb = traceback.extract_tb(exc.__traceback__)

    # Filter out sandbox/temporal internals
    relevant_frames = [frame for frame in tb if not any(m in frame.filename for m in _SANDBOX_INTERNAL_MARKERS)]
    if not relevant_frames:
        return ""

    lines: list[str] = ["  Import chain:"]
    for frame in relevant_frames:
        is_third_party = any(m in frame.filename for m in _THIRD_PARTY_MARKERS)
        label = "[third-party]" if is_third_party else "[your code]  "
        lines.append(f"    {label} {frame.filename}:{frame.lineno}: {frame.line}")
    return "\n".join(lines)


_SANDBOX_ERROR_GUIDANCE = (
    "This usually means your workflow code imports or uses a module "
    "that is not allowed inside the sandbox "
    "(e.g. file I/O, network calls, threading).\n"
    "To fix this, either:\n"
    "  - Move the import inside an activity instead of the workflow\n"
    "  - Use `with workflow.unsafe.imports_passed_through():` "
    "to bypass the sandbox for safe imports"
)


def log_if_sandbox_restriction_error(exc: BaseException, context: str) -> None:
    """If exc (or its cause chain) contains a RestrictedWorkflowAccessError,
    log a structured error with the import chain and actionable guidance."""
    sandbox_error = _find_sandbox_restriction_error(exc)
    if sandbox_error is None:
        return
    import_chain = _format_sandbox_import_chain(sandbox_error)
    parts = [
        f"Workflow sandbox {context} failed: {sandbox_error}",
        import_chain,
        _SANDBOX_ERROR_GUIDANCE,
    ]
    message = "\n".join(part for part in parts if part)
    logger.error(message)
