import logging
import math
import multiprocessing
import time
from typing import Optional

from workflow_server.config import CONCURRENCY, MEMORY_LIMIT_MB

logger = logging.getLogger(__name__)

WARN_MEMORY_PERCENT = 0.90
FORCE_GC_MEMORY_PERCENT = 0.75

_MAX_PROCESS_COUNT = math.ceil(CONCURRENCY * 1.7)
# Keep these under the 15s knative response start timeout or it may trigger odd behavior
_MEMORY_CHECK_INTERVAL_SECONDS = 2
_MAX_MEMORY_CHECK_ATTEMPTS = 3
_ACTIVE_PROCESS_COUNT = multiprocessing.Value("i", 0)
_ACTIVE_PROCESS_LOCK = multiprocessing.Lock()
_ACTIVE_SPAN_IDS = multiprocessing.Manager().list()


def increment_process_count(change: int) -> None:
    result = _ACTIVE_PROCESS_LOCK.acquire(timeout=5)
    try:
        if result:
            global _ACTIVE_PROCESS_COUNT
            _ACTIVE_PROCESS_COUNT.value += change
        else:
            logger.error("Failed to lock workflow server process count global.")
    finally:
        if result:
            _ACTIVE_PROCESS_LOCK.release()


def get_active_process_count() -> int:
    return _ACTIVE_PROCESS_COUNT.value


def get_active_span_ids() -> list[str]:
    """Get a copy of currently active span IDs"""
    with _ACTIVE_PROCESS_LOCK:
        return list(_ACTIVE_SPAN_IDS)


def add_active_span_id(span_id: str) -> None:
    """Add a span ID to the active tracking list"""
    result = _ACTIVE_PROCESS_LOCK.acquire(timeout=5)
    try:
        if result:
            _ACTIVE_SPAN_IDS.append(span_id)
        else:
            logger.error("Failed to lock workflow server span ID tracking.")
    finally:
        if result:
            _ACTIVE_PROCESS_LOCK.release()


def remove_active_span_id(span_id: str) -> None:
    """Remove a span ID from the active tracking list"""
    result = _ACTIVE_PROCESS_LOCK.acquire(timeout=5)
    try:
        if result and span_id in _ACTIVE_SPAN_IDS:
            _ACTIVE_SPAN_IDS.remove(span_id)
        else:
            if not result:
                logger.error("Failed to lock workflow server span ID tracking.")
    finally:
        if result:
            _ACTIVE_PROCESS_LOCK.release()


def get_memory_in_use_mb() -> Optional[float]:
    try:
        with open("/sys/fs/cgroup/memory/memory.usage_in_bytes", "r") as file:
            memory_bytes = file.read()
    except Exception:
        logger.error("Unable to get current memory.")
        return None

    if not memory_bytes:
        logger.error("Unable to get current memory.")
        return None

    return int(memory_bytes) / 1024 / 1024


def wait_for_available_process() -> bool:
    memory_loops = 0
    process_available = False

    while memory_loops < _MAX_MEMORY_CHECK_ATTEMPTS:
        memory_mb = get_memory_in_use_mb()

        exceeded_warn_limit = memory_mb and memory_mb > (MEMORY_LIMIT_MB * WARN_MEMORY_PERCENT)
        exceeded_process_limit = (
            get_active_process_count() > _MAX_PROCESS_COUNT
            and memory_mb
            and memory_mb > (MEMORY_LIMIT_MB * FORCE_GC_MEMORY_PERCENT)
        )

        if not exceeded_process_limit and not exceeded_warn_limit:
            process_available = True
            break

        memory_loops += 1
        time.sleep(_MEMORY_CHECK_INTERVAL_SECONDS)

    return process_available
