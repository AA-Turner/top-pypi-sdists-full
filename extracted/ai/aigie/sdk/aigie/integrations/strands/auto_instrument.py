"""
Strands Agents auto-instrumentation.

Automatically patches Strands Agent initialization to inject Aigie tracing.
"""

import functools
import logging

logger = logging.getLogger(__name__)

_patched_agents: set[str] = set()
_original_agent_init = None


def patch_strands() -> bool:
    """
    Patch Strands Agents for auto-instrumentation.

    This patches Agent.__init__ to automatically register StrandsHandler
    when agents are created.

    Returns:
        True if patching was successful (or already patched)
    """
    global _original_agent_init

    try:
        import strands
        from strands.agent.agent import Agent
    except ImportError:
        # Silently skip - Strands Agents not installed, which is fine
        logger.debug("[AIGIE] Strands Agents not installed, skipping auto-instrumentation")
        return False

    # Check if already patched
    if id(Agent.__init__) in _patched_agents:
        logger.debug("[AIGIE] Strands Agents already patched")
        return True

    # Store original __init__
    if _original_agent_init is None:
        _original_agent_init = Agent.__init__

    # Create patched __init__
    @functools.wraps(_original_agent_init)
    def patched_init(self, *args, **kwargs):
        """Patched Agent.__init__ that auto-registers Aigie handler."""
        # Auto-register Aigie handler before calling original __init__
        # This ensures it's added to the hooks list that gets processed
        try:
            from .config import StrandsConfig
            from .handler import StrandsHandler

            # Check if handler is already in hooks list
            hooks = kwargs.get("hooks", []) or []
            has_aigie_handler = any(isinstance(hook, StrandsHandler) for hook in hooks)

            if not has_aigie_handler:
                # Create handler with default config
                config = StrandsConfig.from_env()
                if config.enabled:
                    handler = StrandsHandler(config=config)
                    # Add to hooks list - Agent.__init__ will register it
                    if hooks is None:
                        hooks = []
                    hooks.append(handler)
                    kwargs["hooks"] = hooks

                    logger.debug("[AIGIE] Auto-registering StrandsHandler for agent")

        except Exception as e:
            logger.warning(f"[AIGIE] Failed to auto-register StrandsHandler: {e}")

        # Call original __init__ with potentially modified kwargs
        _original_agent_init(self, *args, **kwargs)

    # Patch Agent.__init__
    Agent.__init__ = patched_init
    _patched_agents.add(id(Agent.__init__))

    logger.info("[AIGIE] Strands Agents patched for auto-instrumentation")
    return True


def unpatch_strands() -> None:
    """Remove Strands Agents patches (for testing)."""
    global _original_agent_init

    try:
        import strands
        from strands.agent.agent import Agent
    except ImportError:
        return

    if _original_agent_init is not None:
        Agent.__init__ = _original_agent_init
        _original_agent_init = None
        _patched_agents.clear()
        logger.info("[AIGIE] Strands Agents patches removed")


def is_strands_patched() -> bool:
    """
    Check if Strands Agents is currently patched.

    Returns:
        True if patched, False otherwise
    """
    try:
        from strands.agent.agent import Agent

        return id(Agent.__init__) in _patched_agents
    except ImportError:
        return False
