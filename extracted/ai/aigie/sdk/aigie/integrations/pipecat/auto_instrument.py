"""
Pipecat auto-instrumentation.

Automatically patches Pipecat PipelineTask initialization to inject Aigie observer.
"""

import functools
import logging

logger = logging.getLogger(__name__)

_patched_classes: set[str] = set()
_original_pipeline_task_init = None


def patch_pipecat() -> bool:
    """
    Patch Pipecat for auto-instrumentation.

    This patches PipelineTask.__init__ to automatically register AigieObserver
    when pipeline tasks are created.

    Returns:
        True if patching was successful (or already patched)
    """
    global _original_pipeline_task_init

    try:
        from pipecat.pipeline.task import PipelineTask
    except ImportError:
        logger.warning("[AIGIE] Pipecat not available. Install with: pip install pipecat-ai")
        return False

    # Check if already patched
    if id(PipelineTask.__init__) in _patched_classes:
        logger.debug("[AIGIE] Pipecat already patched")
        return True

    # Store original __init__
    if _original_pipeline_task_init is None:
        _original_pipeline_task_init = PipelineTask.__init__

    # Create patched __init__
    @functools.wraps(_original_pipeline_task_init)
    def patched_init(self, pipeline, *, observers=None, **kwargs):
        """Patched PipelineTask.__init__ that auto-registers Aigie observer."""
        # Auto-register Aigie observer before calling original __init__
        try:
            from .config import PipecatConfig
            from .handler import AigieObserver

            # Convert observers to list if needed
            observers = [] if observers is None else list(observers)

            # Check if Aigie observer is already present
            has_aigie_observer = any(isinstance(obs, AigieObserver) for obs in observers)

            if not has_aigie_observer:
                # Create observer with default config
                config = PipecatConfig.from_env()
                if config.enabled:
                    observer = AigieObserver(config=config)
                    observers.append(observer)

                    logger.debug("[AIGIE] Auto-registering AigieObserver for PipelineTask")

        except Exception as e:
            logger.warning(f"[AIGIE] Failed to auto-register AigieObserver: {e}")

        # Call original __init__ with potentially modified observers
        _original_pipeline_task_init(self, pipeline, observers=observers, **kwargs)

    # Patch PipelineTask.__init__
    PipelineTask.__init__ = patched_init
    _patched_classes.add(id(PipelineTask.__init__))

    logger.info("[AIGIE] Pipecat patched for auto-instrumentation")
    return True


def unpatch_pipecat() -> None:
    """Remove Pipecat patches (for testing)."""
    global _original_pipeline_task_init

    try:
        from pipecat.pipeline.task import PipelineTask
    except ImportError:
        return

    if _original_pipeline_task_init is not None:
        PipelineTask.__init__ = _original_pipeline_task_init
        _original_pipeline_task_init = None
        _patched_classes.clear()
        logger.info("[AIGIE] Pipecat patches removed")


def is_pipecat_patched() -> bool:
    """
    Check if Pipecat is currently patched.

    Returns:
        True if patched, False otherwise
    """
    try:
        from pipecat.pipeline.task import PipelineTask

        return id(PipelineTask.__init__) in _patched_classes
    except ImportError:
        return False
