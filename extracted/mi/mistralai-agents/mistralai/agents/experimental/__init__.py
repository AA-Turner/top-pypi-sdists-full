"""Public names whose shape is not settled yet.

A minor release may change or remove a name here, and its changelog entry starts with
"Experimental:". A patch release does not. Importing or using these names gives no warning.
"""

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mistralai.agents.experimental import session_protocol
    from mistralai.vibe.harness.runtime.hosts.workflows import (
        WorkflowSandboxExecuteRequest as CustomSandboxExecuteRequest,
    )
    from mistralai.vibe.harness.runtime.hosts.workflows import (
        WorkflowSandboxExecuteResult as CustomSandboxExecuteResult,
    )
    from mistralai.vibe.harness.runtime.hosts.workflows import (
        WorkflowSandboxReadFileRequest as CustomSandboxReadFileRequest,
    )
    from mistralai.vibe.harness.runtime.hosts.workflows import (
        WorkflowSandboxReadFileResult as CustomSandboxReadFileResult,
    )
    from mistralai.vibe.harness.runtime.hosts.workflows import (
        WorkflowSandboxWriteFilesRequest as CustomSandboxWriteFilesRequest,
    )
    from mistralai.vibe.harness.runtime.hosts.workflows import (
        WorkflowSandboxWriteFilesResult as CustomSandboxWriteFilesResult,
    )
    from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_files import resolve_file_source
    from mistralai.vibe_agents.sdk.authoring.contracts import CustomSandbox
    from mistralai.vibe_agents.sdk.transport.session_journal import JsonFileSessionJournal


__all__ = [
    "CustomSandbox",
    "CustomSandboxExecuteRequest",
    "CustomSandboxExecuteResult",
    "CustomSandboxReadFileRequest",
    "CustomSandboxReadFileResult",
    "CustomSandboxWriteFilesRequest",
    "CustomSandboxWriteFilesResult",
    "JsonFileSessionJournal",
    "resolve_file_source",
    "session_protocol",
]

_SUBMODULES = frozenset({"session_protocol"})

_HARNESS_WORKFLOWS = "mistralai.vibe.harness.runtime.hosts.workflows"

# The module and the name that define each name. The harness names the sandbox requests after its Workflow host.
_SOURCES = {
    "CustomSandbox": ("mistralai.vibe_agents.sdk.authoring.contracts", "CustomSandbox"),
    "CustomSandboxExecuteRequest": (_HARNESS_WORKFLOWS, "WorkflowSandboxExecuteRequest"),
    "CustomSandboxExecuteResult": (_HARNESS_WORKFLOWS, "WorkflowSandboxExecuteResult"),
    "CustomSandboxReadFileRequest": (_HARNESS_WORKFLOWS, "WorkflowSandboxReadFileRequest"),
    "CustomSandboxReadFileResult": (_HARNESS_WORKFLOWS, "WorkflowSandboxReadFileResult"),
    "CustomSandboxWriteFilesRequest": (_HARNESS_WORKFLOWS, "WorkflowSandboxWriteFilesRequest"),
    "CustomSandboxWriteFilesResult": (_HARNESS_WORKFLOWS, "WorkflowSandboxWriteFilesResult"),
    "JsonFileSessionJournal": ("mistralai.vibe_agents.sdk.transport.session_journal", "JsonFileSessionJournal"),
    "resolve_file_source": (f"{_HARNESS_WORKFLOWS}.sandbox_files", "resolve_file_source"),
}


def __getattr__(name: str) -> object:
    # Load each name on first use, so `import mistralai.agents.experimental` stays cheap.
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    if name in _SUBMODULES:
        # The submodule applies the Temporal passthrough and the log quieting itself, since a
        # direct `import mistralai.agents.experimental.session_protocol` does not come through here.
        return importlib.import_module(f"{__name__}.{name}")
    module_name, attribute = _SOURCES[name]
    import temporalio.workflow  # noqa: PLC0415

    from mistralai.agents import _silence  # noqa: PLC0415

    # The same Temporal passthrough and log quieting as the names of `mistralai.agents`.
    with temporalio.workflow.unsafe.imports_passed_through():
        _silence.presilence()
        try:
            from mistralai.vibe_agents.sdk.quiet import quiet_local_sdk_logs  # noqa: PLC0415

            quiet_local_sdk_logs()
            module = importlib.import_module(module_name)
        finally:
            _silence.restore_runtime_warning_levels()
    value = getattr(module, attribute)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
