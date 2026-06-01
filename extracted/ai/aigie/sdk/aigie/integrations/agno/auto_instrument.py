"""
Agno auto-instrumentation.

Automatically patches Agno Agent and Team initialization to inject Aigie tracing.
Includes tool hook injection for remediation engine and gateway intervention support.
"""

import functools
import logging
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes: set[int] = set()
_original_agent_init = None
_original_team_init = None


def _create_aigie_tool_hook():
    """Create an Aigie tool hook for remediation and gateway intervention.

    Agno tool_hooks are sync functions that receive
    (function_name, function_call, arguments, **kwargs)
    and MUST call function_call(**arguments) and return the result.
    """
    _engine_holder: dict[str, Any] = {}

    def _get_engine():
        """Lazily create remediation engine on first use."""
        if "engine" in _engine_holder:
            return _engine_holder["engine"], _engine_holder.get("config")
        from .config import AgnoConfig

        config = AgnoConfig.from_env()
        if not (config.enable_realtime_remediation and config.remediation_mode == "autonomous"):
            _engine_holder["engine"] = None
            _engine_holder["config"] = config
            return None, config
        from ...client import get_aigie

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

    def aigie_tool_hook(function_name, function_call, arguments, **kwargs):
        """Aigie tool hook with remediation and gateway intervention."""
        # Check gateway intervention before execution
        try:
            from ...client import get_aigie

            aigie_inst = get_aigie()
            if aigie_inst and hasattr(aigie_inst, "_intervention_dispatcher"):
                dispatcher = getattr(aigie_inst, "_intervention_dispatcher", None)
                if dispatcher:
                    agent = kwargs.get("agent")
                    trace_id = None
                    if agent:
                        for h in getattr(agent, "pre_hooks", None) or []:
                            hnd = getattr(h, "_aigie_handler", None)
                            if hnd and hasattr(hnd, "trace_id"):
                                trace_id = hnd.trace_id
                                break
                    if trace_id:
                        signal = dispatcher.pop_pending(trace_id)
                        if signal:
                            if signal.intervention_type == "delay":
                                import time

                                delay_ms = signal.payload.get("delay_ms", 1000)
                                time.sleep(delay_ms / 1000.0)
                            elif signal.intervention_type == "inject_correction":
                                corrections = signal.payload.get("corrections", {})
                                if corrections:
                                    arguments = {**arguments, **corrections}
                            elif signal.intervention_type == "break_loop":
                                raise RuntimeError(f"[Aigie] {signal.reason}")
        except RuntimeError:
            raise
        except Exception as e:
            logger.debug(f"[AIGIE] Gateway check failed (non-fatal): {e}")

        # Execute the tool
        try:
            return function_call(**arguments)
        except Exception as e:
            engine, config = _get_engine()
            if not engine:
                raise

            try:
                import asyncio

                try:
                    asyncio.get_running_loop()
                    import concurrent.futures

                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                        rem = executor.submit(
                            asyncio.run,
                            engine.evaluate(
                                str(e), function_name, "", "", mode=config.remediation_mode
                            ),
                        ).result(timeout=config.remediation_query_timeout + 1)
                except RuntimeError:
                    rem = asyncio.run(
                        engine.evaluate(str(e), function_name, "", "", mode=config.remediation_mode)
                    )

                if rem and config.remediation_mode == "autonomous":
                    applied = False
                    if rem.action_type:
                        try:
                            fix_action = engine.to_fix_action(rem)
                            if fix_action:
                                from ...interceptor.protocols import InterceptionContext
                                from ...realtime.auto_fix import AutoFixApplicator

                                applicator = AutoFixApplicator()

                                def _retry_fn(**kw2):
                                    return function_call(**arguments)

                                applicator.set_retry_executor(_retry_fn)
                                ctx = InterceptionContext(
                                    provider="agno",
                                    model="",
                                    messages=[],
                                    response_content=str(e),
                                )
                                try:
                                    fix_result = asyncio.run(
                                        applicator.apply_fixes(ctx, [fix_action])
                                    )
                                except RuntimeError:
                                    fix_result = None

                                if fix_result and fix_result.success:
                                    applied = True
                                    engine.mark_applied(rem)
                                    if fix_result.modified_response is not None:
                                        return fix_result.modified_response
                        except Exception as fix_err:
                            logger.debug(f"[AIGIE] Programmatic fix failed: {fix_err}")

                    if not applied and rem.guidance_text:
                        engine.mark_applied(rem)
                        raise type(e)(f"{e}\n\n{rem.guidance_text}") from e
            except type(e):
                raise
            except Exception:
                pass
            raise

    aigie_tool_hook._aigie_hook = True
    return aigie_tool_hook


def patch_agno() -> bool:
    """
    Patch Agno for auto-instrumentation.

    This patches Agent.__init__ and Team.__init__ to automatically register
    AgnoHandler when agents/teams are created.

    Returns:
        True if patching was successful (or already patched), False if agno is not installed.
    """
    global _original_agent_init, _original_team_init

    try:
        from agno.agent import Agent
    except ImportError:
        logger.debug("[AIGIE] Agno not installed, skipping auto-instrumentation")
        return False

    patched_any = False

    # Patch Agent
    if id(Agent.__init__) not in _patched_classes:
        _original_agent_init = Agent.__init__
        orig_agent_init = _original_agent_init

        @functools.wraps(orig_agent_init)
        def patched_agent_init(self, *args, **kwargs):
            """Patched Agent.__init__ that auto-registers Aigie handler."""
            # Call original __init__ first so the agent is fully constructed
            orig_agent_init(self, *args, **kwargs)

            try:
                from .config import AgnoConfig
                from .handler import AgnoHandler

                config = AgnoConfig.from_env()
                if config.enabled:
                    # Check if a handler is already registered
                    pre_hooks = getattr(self, "pre_hooks", None) or []
                    has_aigie = any(
                        getattr(h, "_aigie_handler", None) is not None for h in pre_hooks
                    )
                    if not has_aigie:
                        handler = AgnoHandler(config=config)
                        handler.register(self)
                        logger.debug("[AIGIE] Auto-registered AgnoHandler on Agent")

                    # Inject aigie tool hook for remediation
                    tool_hooks = getattr(self, "tool_hooks", None) or []
                    has_aigie_tool_hook = any(getattr(h, "_aigie_hook", False) for h in tool_hooks)
                    if not has_aigie_tool_hook:
                        aigie_hook = _create_aigie_tool_hook()
                        self.tool_hooks = list(tool_hooks) + [aigie_hook]
                        logger.debug("[AIGIE] Injected Aigie tool hook for remediation")
            except Exception as e:
                logger.warning(f"[AIGIE] Failed to auto-register AgnoHandler on Agent: {e}")

        Agent.__init__ = patched_agent_init
        _patched_classes.add(id(Agent.__init__))
        patched_any = True
        logger.debug("[AIGIE] Agno Agent patched for auto-instrumentation")

    # Patch Team (optional — may not be available in all agno versions)
    try:
        from agno.team import Team

        if id(Team.__init__) not in _patched_classes:
            _original_team_init = Team.__init__
            orig_team_init = _original_team_init

            @functools.wraps(orig_team_init)
            def patched_team_init(self, *args, **kwargs):
                """Patched Team.__init__ that auto-registers Aigie handler."""
                orig_team_init(self, *args, **kwargs)

                try:
                    from .config import AgnoConfig
                    from .handler import AgnoHandler

                    config = AgnoConfig.from_env()
                    if config.enabled and config.trace_teams:
                        pre_hooks = getattr(self, "pre_hooks", None) or []
                        has_aigie = any(
                            getattr(h, "_aigie_handler", None) is not None for h in pre_hooks
                        )
                        if not has_aigie:
                            handler = AgnoHandler(config=config)
                            handler.register(self)
                            logger.debug("[AIGIE] Auto-registered AgnoHandler on Team")
                except Exception as e:
                    logger.warning(f"[AIGIE] Failed to auto-register AgnoHandler on Team: {e}")

            Team.__init__ = patched_team_init
            _patched_classes.add(id(Team.__init__))
            patched_any = True
            logger.debug("[AIGIE] Agno Team patched for auto-instrumentation")

    except ImportError:
        logger.debug("[AIGIE] Agno Team not available, skipping Team patch")

    if patched_any:
        logger.info("[AIGIE] Agno patched for auto-instrumentation")

    return patched_any


def unpatch_agno() -> None:
    """Remove Agno patches (for testing)."""
    global _original_agent_init, _original_team_init

    try:
        from agno.agent import Agent

        if _original_agent_init is not None:
            Agent.__init__ = _original_agent_init
            _original_agent_init = None
    except ImportError:
        pass

    try:
        from agno.team import Team

        if _original_team_init is not None:
            Team.__init__ = _original_team_init
            _original_team_init = None
    except ImportError:
        pass

    _patched_classes.clear()
    logger.info("[AIGIE] Agno patches removed")


def is_agno_patched() -> bool:
    """
    Check if Agno is currently patched.

    Returns:
        True if patched, False otherwise.
    """
    try:
        from agno.agent import Agent

        return id(Agent.__init__) in _patched_classes
    except ImportError:
        return False
