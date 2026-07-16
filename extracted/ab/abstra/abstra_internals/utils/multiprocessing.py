import os
import sys
from multiprocessing import Queue

from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.multiprocessing import MPContext

SHM_DIR = "/dev/shm"
# Named-semaphore files created by multiprocessing (SemLock names are "mp-*").
STALE_SEMAPHORE_PREFIX = "sem.mp-"


def cleanup_stale_multiprocessing_semaphores(shm_dir: str = SHM_DIR) -> int:
    """Delete sem.mp-* files leaked by previous incarnations of this container.

    /dev/shm belongs to the pod sandbox, so it survives container restarts.
    When the container dies by SIGKILL (e.g. an OOM kill of PID 1), the
    multiprocessing resource tracker is killed with it and never gets to
    sem_unlink, leaking every live semaphore. Repeated kills eventually fill
    the 64Mi tmpfs and every Queue() then fails with ENOSPC (Errno 28).

    Only safe to call before this process creates any multiprocessing
    primitive, while nothing else in the pod uses python multiprocessing —
    at that point every sem.mp-* file is garbage from a dead process.
    Returns the number of files removed (best-effort, never raises).
    On platforms without /dev/shm the listdir fails and this is a no-op.
    """
    try:
        names = os.listdir(shm_dir)
    except OSError:
        return 0
    removed = 0
    for name in names:
        if not name.startswith(STALE_SEMAPHORE_PREFIX):
            continue
        try:
            os.unlink(os.path.join(shm_dir, name))
            removed += 1
        except OSError:
            continue
    return removed


def safe_multiprocessing_queue(mp_context: MPContext) -> Queue:
    try:
        return mp_context.Queue()
    except OSError as e:
        if e.errno == 28:  # ENOSPC
            if sys.platform == "darwin":
                message = (
                    "Failed to create multiprocessing queue: system limit for "
                    "semaphores reached (Errno 28). This is a common issue on "
                    "macOS when processes are not cleaned up properly. Try "
                    "restarting your computer to clear the system semaphores."
                )
            else:
                message = (
                    "Failed to create multiprocessing queue: ENOSPC (Errno 28). "
                    "/dev/shm is likely full (e.g. leaked semaphores). "
                    "Terminating."
                )
            AbstraLogger.error(message)
            AbstraLogger.capture_exception(e)
            # sys.exit here would only kill the calling thread (SystemExit is
            # swallowed when raised outside the main thread), leaving the
            # process alive but unable to ever spawn executors. Exit the whole
            # process instead, flushing first since os._exit skips atexit and
            # buffered output.
            sys.stdout.flush()
            sys.stderr.flush()
            os._exit(1)
        raise e
