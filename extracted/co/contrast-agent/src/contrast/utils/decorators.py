# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import os
import logging as stdlib_logging

import contrast
from contrast_vendor import structlog as logging
from contrast.agent.validator import ValidationException
from contrast_vendor.webob.request import DisconnectionError

logger = logging.getLogger("contrast")

DEBUG_LEVEL = stdlib_logging.DEBUG


def log_and_report_exception(
    log_message: str | None,
    error: Exception,
    original_func,
    args,
    kwargs,
    log_level="debug",
):
    """
    Log an exception at the given level and report it to telemetry if available.
    """
    TELEMETRY = contrast.TELEMETRY if not contrast.telemetry_disabled() else None

    try:
        full_msg = (
            (log_message or "Exception in Contrast machinery") + ": " + str(error)
        )
        getattr(logger, log_level)(full_msg, exc_info=error, stack_info=True)
        logger.debug("wrapped function args: %s", args)
        logger.debug("wrapped function kwargs: %s", kwargs)

        if TELEMETRY is not None:
            # omit the decorator wrapper function from the stacktrace
            error.__traceback__ = error.__traceback__.tb_next
            TELEMETRY.report_error(
                error=error,
                original_func=original_func,
                message=full_msg,
                # 1 to remove the current _report_exception frame
                skip_frames=1,
            )
    except ValidationException as val_ex:
        logger.debug(f"Cannot report error to Telemetry: {str(val_ex)}")
    except Exception:
        # For complete safety, we're not going to try to log the logging error
        # because sometimes the logging error is actually an error (such as a recursive
        # error) within the logging module itself!
        pass


SILENCED_EXCEPTIONS = (DisconnectionError, ConnectionResetError)


def _fail_safely(log_message, log_level, return_value):
    """
    Decorator that will run the decorated function/method and, if
    an exception is raised, return a safe value and log the error.

    Note that SecurityException will always be re-raised.

    :param log_message: message to log in case of failure
    :param log_level: level to log in case of failure
    :param return_value: safe value to return in case of failure
    :return: original func return or return_value
    """

    def wrap(original_func):
        def run_safely(*args, **kwargs):
            try:
                return original_func(*args, **kwargs)
            except contrast.SecurityException:
                raise
            except Exception as ex:
                TESTING = os.environ.get("CONTRAST_TESTING")
                if isinstance(ex, SILENCED_EXCEPTIONS) and not TESTING:
                    logger.debug("Silenced exception in fail_safely", exc_info=ex)
                    return return_value

                log_and_report_exception(
                    log_message, ex, original_func, args, kwargs, log_level
                )
                if TESTING:
                    logger.warn(
                        "Re-raising exception in fail_safely (CONTRAST_TESTING is set)"
                    )
                    raise

            return return_value

        return run_safely

    return wrap


def fail_loudly(log_message=None, log_level="exception", return_value=None):
    return _fail_safely(log_message, log_level, return_value)


def fail_quietly(log_message="fail_quietly caught an exception", return_value=None):
    """
    Similar to fail_loudly (see above)

    This decorator is intended to handle cases where an exception may occur but won't
    disrupt normal operation of the agent. This decorator should be used to protect
    against external exceptions we can't prevent but still want to handle.

    In these cases, we log an error message and the exception traceback, both at DEBUG
    level.
    """
    return _fail_safely(f"WARNING: {log_message}", "debug", return_value)
