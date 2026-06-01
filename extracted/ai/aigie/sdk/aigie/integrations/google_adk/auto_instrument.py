"""
Google ADK auto-instrumentation.

Automatically patches Google ADK's Runner to inject AigiePlugin
for automatic tracing without requiring manual plugin registration.
Also patches tool execution with retry executor support for auto-fix remediation.
"""

import functools
import logging
from typing import Any

logger = logging.getLogger(__name__)

_patched_runners: set[int] = set()
_patched_tools: set[Any] = set()
_original_runner_init = None


def patch_google_adk() -> bool:
    """
    Patch Google ADK Runner for auto-instrumentation.

    This patches Runner.__init__ to automatically add AigiePlugin
    to the plugins list when Runners are created. Also patches
    tool execution for remediation with retry executor support.

    Returns:
        True if patching was successful (or already patched)

    Example:
        >>> import aigie
        >>> aigie.patch("google_adk")
        >>>
        >>> # All Runners are now automatically traced
        >>> from google.adk import Runner, LlmAgent
        >>> runner = Runner(agent=agent, session_service=...)
        >>> async for event in runner.run_async(...):
        ...     process(event)
    """
    global _original_runner_init

    try:
        from google.adk.runners import Runner
    except ImportError:
        try:
            from google.adk import Runner
        except ImportError:
            # Silently skip - Google ADK not installed, which is fine
            logger.debug("[AIGIE] Google ADK not installed, skipping auto-instrumentation")
            return False

    # Check if already patched
    if id(Runner.__init__) in _patched_runners:
        logger.debug("[AIGIE] Google ADK Runner already patched")
        return True

    # Store original __init__
    if _original_runner_init is None:
        _original_runner_init = Runner.__init__

    # Create patched __init__
    @functools.wraps(_original_runner_init)
    def patched_init(self, *args, plugins=None, **kwargs):
        """Patched Runner.__init__ that auto-injects AigiePlugin."""
        try:
            from .config import GoogleADKConfig
            from .plugin import AigiePlugin

            # Ensure plugins is a list
            plugins = [] if plugins is None else list(plugins)

            # Check if AigiePlugin is already in the list
            has_aigie_plugin = any(
                isinstance(p, AigiePlugin) or (hasattr(p, "name") and p.name == "aigie")
                for p in plugins
            )

            if not has_aigie_plugin:
                # Create plugin with default config from env
                config = GoogleADKConfig.from_env()
                if config.enabled:
                    aigie_plugin = AigiePlugin(config=config)
                    # Prepend to ensure it's called first
                    plugins = [aigie_plugin] + plugins

                    logger.debug("[AIGIE] Auto-injecting AigiePlugin into Runner")

        except Exception as e:
            logger.warning(f"[AIGIE] Failed to auto-inject AigiePlugin: {e}")

        # Call original __init__ with potentially modified plugins
        _original_runner_init(self, *args, plugins=plugins, **kwargs)

    # Patch Runner.__init__
    Runner.__init__ = patched_init
    _patched_runners.add(id(Runner.__init__))

    # Also patch tool execution for remediation support
    _patch_tool_execution()

    logger.info("[AIGIE] Google ADK Runner patched for auto-instrumentation")
    return True


def _patch_tool_execution() -> bool:
    """Patch Google ADK tool execution with remediation and retry executor.

    Wraps BaseTool.run_async (or equivalent) to add AutoFixApplicator
    with a retry executor, following the same pattern as the LangChain
    integration's _patch_tool_run.

    The patch is always applied, but the remediation engine and config
    are resolved lazily at call time (not patch time) because Aigie may
    not be initialized yet when auto-instrumentation runs.

    Returns:
        True if patching was successful
    """
    try:
        from google.adk.tools import BaseTool as ADKBaseTool
    except ImportError:
        try:
            from google.adk.tools.base_tool import BaseTool as ADKBaseTool
        except ImportError:
            logger.debug("[AIGIE] Google ADK BaseTool not found, skipping tool patch")
            return True  # Not an error if not installed

    if ADKBaseTool in _patched_tools:
        return True

    # Find the async run method - ADK tools use run_async or arun
    original_run_async = getattr(ADKBaseTool, "run_async", None)
    if original_run_async is None:
        original_run_async = getattr(ADKBaseTool, "arun", None)
    if original_run_async is None:
        logger.debug("[AIGIE] Google ADK BaseTool has no run_async/arun method, skipping")
        return True

    run_method_name = "run_async" if hasattr(ADKBaseTool, "run_async") else "arun"

    if getattr(original_run_async, "_aigie_patched", False):
        return True  # Already patched

    # Lazy-initialized engine holder
    _engine_holder: dict[str, Any] = {}

    def _get_engine():
        """Lazily create remediation engine on first use."""
        if "engine" in _engine_holder:
            return _engine_holder["engine"], _engine_holder.get("config")
        from ...client import get_aigie
        from .config import GoogleADKConfig

        config = GoogleADKConfig.from_env()
        if not (config.enable_realtime_remediation and config.remediation_mode == "autonomous"):
            _engine_holder["engine"] = None
            _engine_holder["config"] = config
            return None, config
        aigie = get_aigie()
        if not aigie or not aigie._initialized:
            return None, config
        api_url = getattr(aigie, "api_url", None) or getattr(aigie, "_api_url", None)
        if not api_url:
            _engine_holder["engine"] = None
            _engine_holder["config"] = config
            return None, config
        from ...realtime.remediation_engine import RemediationEngine

        api_key = getattr(aigie, "_api_key", None) or getattr(aigie, "api_key", None)
        engine = RemediationEngine(
            api_url=api_url,
            api_key=api_key or "",
            query_timeout=getattr(config, "remediation_query_timeout", 2.0),
        )
        _engine_holder["engine"] = engine
        _engine_holder["config"] = config
        return engine, config

    @functools.wraps(original_run_async)
    async def traced_run_async(self, *args, **kwargs):
        """Wrapped tool execution with remediation and retry executor."""
        engine, config = _get_engine()
        if not engine:
            return await original_run_async(self, *args, **kwargs)

        tool_name = getattr(self, "name", "unknown_tool")

        try:
            return await original_run_async(self, *args, **kwargs)
        except Exception as e:
            try:
                rem = await engine.evaluate(
                    str(e),
                    tool_name,
                    "",
                    "",
                    mode=config.remediation_mode,
                )
                if rem and config.remediation_mode == "autonomous":
                    applied_programmatic = False
                    if rem.action_type:
                        try:
                            fix_action = engine.to_fix_action(rem)
                            if fix_action:
                                from ...interceptor.protocols import InterceptionContext
                                from ...realtime.auto_fix import AutoFixApplicator

                                applicator = AutoFixApplicator()

                                async def _retry_fn(**kw2):
                                    return await original_run_async(self, *args, **kwargs)

                                applicator.set_retry_executor(_retry_fn)
                                ctx = InterceptionContext(
                                    provider="google_adk",
                                    model="",
                                    messages=[],
                                    response_content=str(e),
                                )
                                fix_result = await applicator.apply_fixes(ctx, [fix_action])
                                if fix_result.success:
                                    applied_programmatic = True
                                    engine.mark_applied(rem)
                                    if fix_result.modified_response is not None:
                                        return fix_result.modified_response
                        except Exception as fix_err:
                            logger.debug(f"[AIGIE] Programmatic fix failed: {fix_err}")

                    if not applied_programmatic and rem.guidance_text:
                        engine.mark_applied(rem)
                        raise type(e)(f"{e}\n\n{rem.guidance_text}") from e
            except type(e):
                raise
            except Exception:
                pass
            raise

    traced_run_async._aigie_patched = True
    setattr(ADKBaseTool, run_method_name, traced_run_async)
    _patched_tools.add(ADKBaseTool)

    logger.debug("[AIGIE] Patched Google ADK BaseTool for remediation with retry executor")
    return True


def unpatch_google_adk() -> None:
    """
    Remove Google ADK patches.

    Restores Runner.__init__ to its original implementation.
    """
    global _original_runner_init

    try:
        from google.adk.runners import Runner
    except ImportError:
        try:
            from google.adk import Runner
        except ImportError:
            return

    if _original_runner_init is not None:
        Runner.__init__ = _original_runner_init
        _original_runner_init = None
        _patched_runners.clear()
        logger.info("[AIGIE] Google ADK patches removed")


def is_google_adk_patched() -> bool:
    """
    Check if Google ADK is currently patched.

    Returns:
        True if patched, False otherwise
    """
    try:
        from google.adk.runners import Runner
    except ImportError:
        try:
            from google.adk import Runner
        except ImportError:
            return False

    return id(Runner.__init__) in _patched_runners
