"""Public names whose shape is not settled yet.

A minor release may change or remove a name here, and its changelog entry starts with
"Experimental:". A patch release does not. Importing or using these names gives no warning.
"""

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mistralai.agents.experimental import session_protocol
    from mistralai.vibe_agents.sdk.transport.session_journal import JsonFileSessionJournal


__all__ = ["JsonFileSessionJournal", "session_protocol"]

_SUBMODULES = frozenset({"session_protocol"})


def __getattr__(name: str) -> object:
    # Load each name on first use, so `import mistralai.agents.experimental` stays cheap.
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    if name in _SUBMODULES:
        # The submodule applies the Temporal passthrough and the log quieting itself, since a
        # direct `import mistralai.agents.experimental.session_protocol` does not come through here.
        return importlib.import_module(f"{__name__}.{name}")
    import temporalio.workflow  # noqa: PLC0415

    from mistralai.agents import _silence  # noqa: PLC0415

    # The same Temporal passthrough and log quieting as the names of `mistralai.agents`.
    with temporalio.workflow.unsafe.imports_passed_through():
        _silence.presilence()
        try:
            from mistralai.vibe_agents.sdk.quiet import quiet_local_sdk_logs  # noqa: PLC0415

            quiet_local_sdk_logs()
            from mistralai.vibe_agents.sdk.transport import session_journal  # noqa: PLC0415
        finally:
            _silence.restore_runtime_warning_levels()
    value = getattr(session_journal, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
