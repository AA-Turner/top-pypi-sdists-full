"""App Signals"""

# Standard Library
from importlib import import_module

# Third Party
from celery import signals

# Django
from django.core.cache import cache

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.helpers.core import get_redis_client
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


@signals.worker_ready.connect
def worker_ready_handler(sender, **kwargs):  # pylint: disable=unused-argument
    """Handle worker ready signal.

    This signal is sent when a Celery worker is fully started and ready to
    accept tasks. We use this signal to clear any existing shutdown flag in
    the cache, ensuring that the system is marked as active and ready to
    process tasks.
    """
    cache.delete(f"{__title__.upper()}_WORKER_SHUTDOWN")
    logger.debug("Worker ready signal successfully processed for %s", sender)


@signals.worker_shutting_down.connect
def worker_shutting_down_handler(sender, **kwargs):  # pylint: disable=unused-argument
    """Handle worker shutdown signal.

    Celery sends this signal when a worker is in the process of shutting down.
    We use this signal to set a shutdown flag in the cache, which can be checked
    by long-running tasks to gracefully stop processing new items. This helps
    ensure that tasks do not start new work when the worker is shutting down.
    """
    cache.set(f"{__title__.upper()}_WORKER_SHUTDOWN", True, timeout=120)
    logger.debug("Worker shutting down signal successfully processed for %s", sender)


@signals.worker_shutdown.connect
def worker_shutdown_handler(sender, **kwargs):  # pylint: disable=unused-argument
    """Handle worker shutdown signal.

    This signal is sent when a Celery worker has fully shut down. We use this
    signal to clear any existing QueueOnce locks for tasks that should only run
    once at a time. This ensures that when the worker restarts, tasks can be
    executed again without being blocked by stale locks.
    """
    # Only attempt to clear the lock if we have a redis/cache client
    redis = get_redis_client()
    if not redis:
        logger.debug("No redis client available; skipping QueueOnce lock clear")
        return

    try:
        # Import the tasks module lazily to avoid side effects at import time
        tasks_mod = import_module("killstats.tasks")
        run_zkb_task = getattr(tasks_mod, "run_zkb_r2z2", None)

        if run_zkb_task is None or not hasattr(run_zkb_task, "name"):
            logger.debug("run_zkb_r2z2 task not found or has no name attribute")
            return

        # The celery-once key format (used by celery_once/helpers.queue_once_key)
        # starts with 'qo_' + task name when there are no task kwargs.
        key = f"qo_{run_zkb_task.name}"

        deleted = cache.delete(key)
        logger.debug(
            "Cleared QueueOnce lock for %s on shutdown (key=%s, deleted=%s)",
            run_zkb_task.name,
            key,
            deleted,
        )
        logger.debug("Worker shutdown signal successfully processed for %s", sender)
    except Exception:  # pylint: disable=broad-exception-caught
        logger.exception("Failed to clear QueueOnce lock for run_zkb_r2z2")
