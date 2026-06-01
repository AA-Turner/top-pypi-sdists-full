"""
LiveKit Agents auto-instrumentation.

Automatically patches AgentSession initialization to inject Aigie handler.
"""

import functools
import logging
import threading

logger = logging.getLogger(__name__)

_is_patched = False
_patch_lock = threading.Lock()
_original_session_init = None


def patch_livekit_agents() -> bool:
    """
    Patch LiveKit Agents for auto-instrumentation.

    This patches AgentSession.__init__ to automatically register
    LiveKitAgentsHandler when agent sessions are created.

    Returns:
        True if patching was successful (or already patched)
    """
    global _is_patched, _original_session_init

    with _patch_lock:
        if _is_patched:
            logger.debug("[AIGIE] LiveKit Agents already patched")
            return True

        try:
            from livekit.agents import AgentSession
        except ImportError:
            logger.debug("[AIGIE] LiveKit Agents not installed, skipping auto-instrumentation")
            return False

        # Store original __init__
        if _original_session_init is None:
            _original_session_init = AgentSession.__init__

        # Create patched __init__
        @functools.wraps(_original_session_init)
        def patched_init(self, *args, **kwargs):
            """Patched AgentSession.__init__ that auto-registers Aigie handler."""
            _original_session_init(self, *args, **kwargs)

            try:
                from .config import LiveKitAgentsConfig
                from .handler import LiveKitAgentsHandler

                config = LiveKitAgentsConfig.from_env()
                if config.enabled:
                    handler = LiveKitAgentsHandler(config=config)
                    handler.register(self)
                    logger.debug("[AIGIE] Auto-registered LiveKitAgentsHandler on AgentSession")
            except Exception as e:
                logger.warning(f"[AIGIE] Failed to register handler: {e}")

        # Patch AgentSession.__init__
        AgentSession.__init__ = patched_init
        _is_patched = True

        logger.info("[AIGIE] LiveKit Agents patched for auto-instrumentation")
        return True


def unpatch_livekit_agents() -> None:
    """Remove LiveKit Agents patches (for testing)."""
    global _is_patched, _original_session_init

    with _patch_lock:
        try:
            from livekit.agents import AgentSession
        except ImportError:
            return

        if _original_session_init is not None:
            AgentSession.__init__ = _original_session_init
            _original_session_init = None
            _is_patched = False
            logger.info("[AIGIE] LiveKit Agents patches removed")


def is_livekit_agents_patched() -> bool:
    """
    Check if LiveKit Agents is currently patched.

    Returns:
        True if patched, False otherwise
    """
    return _is_patched
