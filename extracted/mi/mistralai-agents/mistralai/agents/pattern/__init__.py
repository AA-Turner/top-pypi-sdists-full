import temporalio.workflow

from mistralai.agents import _silence

# Direct submodule imports (`from mistralai.agents.pattern.hook import ...`) bypass the parent
# package's lazy `__getattr__`, so apply the same Temporal passthrough and log quieting here.
with temporalio.workflow.unsafe.imports_passed_through():
    _silence.presilence()
    try:
        from mistralai.vibe_agents.sdk.quiet import quiet_local_sdk_logs

        quiet_local_sdk_logs()
        from . import hook, sandbox_hook
    finally:
        _silence.restore_runtime_warning_levels()

__all__ = ["hook", "sandbox_hook"]
