"""
Per-worker thread budgeting.

Model libraries default to one thread per core. Under ``do_parallel_ml`` the
pool is *already* running N fold-tasks concurrently, so each of those N
processes grabbing all C cores oversubscribes the node by a factor of N.
Measured on a 128-core gsapp18: 19 workers x 131 threads each produced a load
average of 940, which not only wastes time in context switching but starves
every other job sharing the host.

The fix is to give each worker ``floor(C / N)`` threads so the pool as a whole
fits inside the machine. Serial runs (``do_parallel_ml = False``) are left
alone — a single process should use the whole box.

Two mechanisms are needed, because neither covers everything:

1. ``threadpool_limits`` from threadpoolctl retunes OpenMP/BLAS pools that are
   *already loaded*. Environment variables cannot do this on their own: the
   pool forks from a parent that has long since imported numpy, so libgomp is
   initialised before the child ever sees a new ``OMP_NUM_THREADS``.
2. Libraries with private thread pools ignore both of the above and need to be
   told explicitly — CatBoost via ``thread_count``, torch via
   ``set_num_threads``, joblib estimators via ``n_jobs``. Those read the budget
   back through :func:`thread_count`.

Configure with ``[ML] threads_per_worker``: unset/``auto``/``0`` = automatic,
a positive integer pins it, and ``-1`` restores the old unlimited behaviour.
"""

import logging
import os

logger = logging.getLogger(__name__)

#: Environment variable carrying the budget to worker code (and to any
#: library that reads the standard OpenMP/BLAS variables at import time).
ENV_KEY = "GEOCIF_THREADS_PER_WORKER"

THREAD_ENV_VARS = (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
)

# threadpool_limits restores the previous limits when the object is garbage
# collected, so the controller has to outlive the call that created it.
_limiter = None


def resolve_threads_per_worker(n_workers, total_cores, parser=None):
    """
    Thread budget for a single pool worker.

    Args:
        n_workers: number of concurrent worker processes
        total_cores: cores on the machine (``mp.cpu_count()``)
        parser: config parser; ``[ML] threads_per_worker`` overrides the
            automatic value

    Returns:
        int threads per worker, or None for "do not limit"
    """
    configured = None
    if parser is not None:
        try:
            raw = parser.get("ML", "threads_per_worker", fallback="").strip()
            if raw and raw.lower() not in ("auto", "0"):
                configured = int(raw)
        except (ValueError, AttributeError):
            logger.warning(
                "[threads] could not parse [ML] threads_per_worker; using automatic budget"
            )

    if configured is not None:
        # Negative means the caller explicitly wants the old all-cores behaviour.
        return None if configured < 0 else max(1, configured)

    try:
        n_workers = int(n_workers)
        total_cores = int(total_cores)
    except (TypeError, ValueError):
        return None

    if n_workers <= 1 or total_cores <= 0:
        return None

    return max(1, total_cores // n_workers)


def apply_worker_limits(threads, log=None):
    """
    Pin this process to ``threads`` threads. Call once, inside each pool
    worker, before any model is built.
    """
    global _limiter
    log = log or logger
    if not threads:
        return

    os.environ[ENV_KEY] = str(threads)
    for var in THREAD_ENV_VARS:
        os.environ[var] = str(threads)

    try:
        from threadpoolctl import threadpool_limits

        _limiter = threadpool_limits(limits=threads)
    except Exception as e:
        log.warning(f"[threads] threadpoolctl unavailable ({e}); OpenMP/BLAS stay unlimited")

    try:
        import torch

        torch.set_num_threads(threads)
    except Exception:
        # torch is an optional extra; nothing to do when it is absent.
        pass


def thread_count(default=None):
    """
    Budget for a library with its own thread pool (CatBoost ``thread_count``,
    joblib ``n_jobs``, ...).

    Args:
        default: value to return when no budget is in force — pass the
            library's own "use everything" sentinel (usually -1)

    Returns:
        int budget, or ``default``
    """
    raw = os.environ.get(ENV_KEY)
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value > 0 else default
