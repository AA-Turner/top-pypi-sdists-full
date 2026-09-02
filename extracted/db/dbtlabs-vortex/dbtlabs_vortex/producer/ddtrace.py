import importlib.util
import io
import logging
import platform
import sys
from contextlib import contextmanager
from typing import Any, Generator, Optional


def has_ddtrace_dependency() -> bool:
    """
    Check if ddtrace dependency is installed.

    Returns:
        bool: True if ddtrace is installed, False otherwise
    """
    return importlib.util.find_spec("ddtrace") is not None


@contextmanager
def trace(name: str, **kwargs: Any) -> Generator[Optional[Any], None, None]:
    """
    Context manager that traces execution if ddtrace is installed, otherwise acts as a passthrough.

    Args:
        name: The name of the trace span
        **kwargs: Additional keyword arguments passed to ddtrace.tracer.trace

    Yields:
        The trace span if ddtrace is installed, otherwise None
    """
    _suppress_ddtrace_logs()

    if has_ddtrace_dependency():
        # defer loading ddtrace until we need it. if we include it at load time, it could
        # trigger the psutil traceback to end up in the log output.
        from ddtrace import tracer

        with tracer.trace(name, **kwargs) as span:
            yield span

    else:
        yield None


def _suppress_ddtrace_logs() -> None:
    """
    Suppress ddtrace logs by setting all ddtrace loggers to CRITICAL level and preventing
    them from propagating to parent loggers.
    """
    # List of loggers to suppress entirely
    loggers_to_suppress = [
        # Main ddtrace loggers
        "ddtrace",
        "ddtrace.settings.profiling",
        "ddtrace.internal.writer.writer",
        # Vendor package loggers
        "ddtrace.vendor",
        "ddtrace.vendor.psutil",
    ]

    # Add platform-specific loggers
    if platform.system() == "Linux":
        loggers_to_suppress.extend(
            [
                "ddtrace.vendor.psutil._pslinux",
                "ddtrace.vendor.psutil._common",
            ]
        )
    elif platform.system() == "Windows":
        loggers_to_suppress.extend(
            [
                "ddtrace.vendor.psutil._pswindows",
                "ddtrace.vendor.psutil._common",
            ]
        )
    elif platform.system() == "Darwin":
        loggers_to_suppress.extend(
            [
                "ddtrace.vendor.psutil._psosx",
                "ddtrace.vendor.psutil._common",
            ]
        )

    # Set all ddtrace loggers to CRITICAL level and add a NullHandler
    for logger_name in loggers_to_suppress:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.CRITICAL)
        logger.propagate = False  # Prevent propagation to parent loggers


def _preload_psutil_muted_traceback() -> None:
    """
    ddtrace's _pslinux module calls traceback.print_exc() _AT LOAD TIME_ when it encounters an
    error. See: https://github.com/DataDog/dd-trace-py/blob/v1.20.19/ddtrace/vendor/psutil/_pslinux.py#L311-L316

    This is a big problem in core and mantle where we want to carefully control the log output
    of the commands we run.

    This function is intended to be called at load time to circumvent the load time error.
    """
    if platform.system() != "Linux" or not has_ddtrace_dependency():
        return

    try:
        # Temporarily redirect stderr to suppress traceback printing that happens when we import
        # ddtrace.vendor.psutil._pslinux
        tmp_stderr = io.StringIO()
        sys.stderr = tmp_stderr
        sys.stdout = tmp_stderr

        import ddtrace.vendor.psutil._pslinux  # noqa

        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

    except (ImportError, AttributeError):
        # In case ddtrace vendor structure changes, just continue
        pass


if importlib.util.find_spec("ddtrace") is not None:
    # preload the psutil module here. this module can result in tracebacks being logged to stderr
    # at load time, which we don't want to do! we want to tightly control the log output of this
    # module.
    _suppress_ddtrace_logs()
    _preload_psutil_muted_traceback()
