"""API for working with celery task queue."""

import concurrent.futures
import functools
import itertools
import json
from collections import defaultdict
from typing import List

import redis

from django.conf import settings

from allianceauth.services.hooks import get_extension_logger
from app_utils.logging import LoggerAddTag

from taskmonitor import __title__
from taskmonitor.app_settings import TASKMONITOR_QUEUED_TASKS_CACHE_TIMEOUT
from taskmonitor.helpers import memcached

from .tasks_cache import QueuedTasksCache, QueuedTaskShort

PRIORITY_SEP = "\x06\x16"
DEFAULT_PRIORITY_STEPS = range(10)
QUEUED_TASKS_CACHE_KEY = "queued-tasks-cache-key"

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


def _redis_client():
    """Fetch the Redis client for the celery broker."""
    return redis.from_url(settings.BROKER_URL)


def default_queue_name() -> str:
    """Default name of celery queue in AA."""
    return getattr(settings, "CELERY_DEFAULT_QUEUE", "celery")


def _redis_queue_names(queue_name: str = None) -> List[str]:
    """List of all queue names on Redis incl. the dedicated queue names for each priority."""
    if not queue_name:
        queue_name = default_queue_name()
    names = [
        f"{queue_name}{PRIORITY_SEP}{priority}" for priority in DEFAULT_PRIORITY_STEPS
    ]
    names = [queue_name] + names
    return names


def queue_length() -> int:
    """Length of the celery queue."""
    r = _redis_client()
    return sum(r.llen(name) for name in _redis_queue_names())


@memcached(timeout=10)
def queue_length_cached() -> int:
    """Current queue length, but cached for a couple seconds to reduce load on Redis."""
    return queue_length()


def fetch_tasks() -> List[QueuedTaskShort]:
    """Fetch tasks from queues
    and return as ordered list with oldest task in first position.
    """
    data = tasks_cache.get()
    if data is None:
        logger.debug("Cache is stale. Fetching new tasks from queue.")
        tasks = _fetch_task_from_all_queues()
        tasks_cache.set(tasks)
    else:
        tasks = data.tasks
        logger.debug("Returning tasks from cache.")
    return tasks


def _fetch_task_from_all_queues() -> List[QueuedTaskShort]:
    """Coordinate fetching tasks from all priority queues."""
    _fetch_func = functools.partial(_fetch_tasks_from_redis, _redis_client())
    redis_queue_names = _redis_queue_names()
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(redis_queue_names)
    ) as executor:
        tasks_raw = executor.map(_fetch_func, redis_queue_names)
    return list(itertools.chain(*tasks_raw))


def _fetch_tasks_from_redis(
    r: redis.Redis, redis_queue_name: str
) -> List[QueuedTaskShort]:
    """Fetch tasks from redis."""
    tasks = []
    for obj_encoded in r.lrange(redis_queue_name, 0, -1):
        try:
            tasks.append(QueuedTaskShort.from_binary_json(obj_encoded))
        except ValueError:
            pass
    return reversed(tasks)


def delete_task_by_id(task_id: str) -> int:
    """Delete task from queue by task ID. Returns count of deleted entries."""
    return _delete_task_by_condition("id", task_id)


def delete_task_by_name(task_name: str) -> int:
    """Delete task from queue by task name. Returns count of deleted entries."""
    return _delete_task_by_condition("name", task_name)


def delete_task_by_app_name(app_name: str) -> int:
    """Delete task from queue by app name. Returns count of deleted entries."""
    return _delete_task_by_condition("app_name", app_name)


def _delete_task_by_condition(field: str, value) -> int:
    """Delete task from queue which match the condition.
    Returns count of deleted entries.
    """
    r = _redis_client()
    deleted_count = 0
    for queue_name in _redis_queue_names():
        for obj_encoded in r.lrange(queue_name, 0, -1):
            try:
                task = QueuedTaskShort.from_binary_json(obj_encoded)
            except ValueError:
                continue
            if getattr(task, field) == value:
                r.lrem(queue_name, 1, obj_encoded)
                deleted_count += 1
    return deleted_count


def clear_tasks(queue_name: str = None):
    """Clear tasks from all queues."""
    r = _redis_client()
    for redis_queue_name in _redis_queue_names(queue_name):
        r.delete(redis_queue_name)
    tasks_cache.clear()


def add_tasks(queue_name: str, raw_tasks: list):
    """Push fake tasks to task queue."""
    r = _redis_client()
    if not queue_name:
        queue_name = default_queue_name()
    tasks_by_priority = defaultdict(list)
    for task in raw_tasks:
        priority = task["properties"]["priority"]
        tasks_by_priority[priority].append(task)
    for priority, tasks in tasks_by_priority.items():
        raw_tasks_str = [json.dumps(obj) for obj in tasks]
        queue_name_raw = f"{queue_name}{PRIORITY_SEP}{priority}"
        r.lpush(queue_name_raw, *raw_tasks_str)
    del tasks_by_priority


tasks_cache = QueuedTasksCache(
    cache_key=QUEUED_TASKS_CACHE_KEY, timeout=TASKMONITOR_QUEUED_TASKS_CACHE_TIMEOUT
)
