# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import string
import cProfile
import threading
import contextlib

try:
    import viztracer
except ImportError:
    viztracer = None

from contrast.utils.decorators import fail_loudly
from contrast.agent import request_state

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


VIZTRACER_SAVE_THREAD_NAME = "ContrastViztracerSave"
POSIX_SAFE_MAX_LENGTH = 64
POSIX_SAFE_CHARS = "_" + string.ascii_letters + string.digits

# VizTracer issues a stern warning if two tracers are recording simultaneously. We use
# this lock as non-blocking and only attempt to trace a request if some other request
# is not already being traced. This means we won't necessarily get viztracer output for
# every request, but it ensures that any data we do get is uncorrupted.
TRACER_LOCK = threading.Lock()


def _posix_safe(s: str) -> str:
    """
    Transform a string into a safe representation for a posix system filename. This
    function is overly aggressive but fine for our purposes.
    """
    s = s[:POSIX_SAFE_MAX_LENGTH].strip("/").replace("/", "_") or "_"
    return "".join(c for c in s if c in POSIX_SAFE_CHARS)


class Profiler(cProfile.Profile):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def __enter__(self):
        self.enable()
        return self

    def __exit__(self, *exc_info):
        self.disable()
        self._save_profile_data()

    @fail_loudly("Unable to save profile data")
    def _save_profile_data(self):
        filename = (
            f"cprofile-{_posix_safe(self.path)}-{request_state.get_request_id()}.out"
        )
        logger.debug("writing cprofile data to %s", filename)
        self.dump_stats(filename)


@contextlib.contextmanager
def tracer(path: str, min_duration_ms: int = 0):
    if viztracer is not None:
        if TRACER_LOCK.acquire(blocking=False):
            min_duration_us = min_duration_ms * 1000
            try:
                request_tracer = viztracer.VizTracer(
                    verbose=0,
                    log_async=True,
                    min_duration=min_duration_us,
                )
                request_tracer.start()
                yield
                request_tracer.stop()
            finally:
                TRACER_LOCK.release()
            _save_trace_data(request_tracer, path)
            return
        else:
            logger.debug("Skipping viztracer for this request - already in use")
    else:
        logger.warning(
            "Attempted to enable tracing but couldn't import viztracer. "
            "Disable tracing or `pip install contrast-agent[debug]` extras."
        )
    yield


@fail_loudly("Unable to save trace data")
def _save_trace_data(request_tracer, path: str):
    filename = f"viztracer-{_posix_safe(path)}-{request_state.get_request_id()}.json.gz"
    logger.debug("writing viztracer data in a background thread", output_file=filename)
    threading.Thread(
        target=_do_save,
        args=(request_tracer, filename),
        name=VIZTRACER_SAVE_THREAD_NAME,
        daemon=True,
    ).start()


def _do_save(request_tracer, filename: str):
    request_tracer.save(output_file=filename)
    logger.debug("wrote viztracer data", output_file=filename)
