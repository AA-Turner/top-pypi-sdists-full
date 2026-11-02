# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import sys
import time
from logging import INFO

from contrast.utils.loggers import (
    color_enabled,
    color_for_level,
    wrap_with_border,
)
from contrast_rewriter import LOG_FORMAT, LOG_TIME_FORMAT
from contrast_vendor import structlog


def basic_stringifier(logger, method_name, event_dict) -> str:
    # Use UTC to match agent JSON logs (which are UTC / Z).
    date_and_time = time.strftime(LOG_TIME_FORMAT, time.gmtime())
    line = LOG_FORMAT.format(
        date_and_time=date_and_time,
        logger_name="contrast-agent",
        msg=event_dict.get("event", "<logging error>"),
    )

    color = color_for_level(method_name)
    if color is None:
        return line

    if not color_enabled(sys.stderr):
        color = None

    return wrap_with_border(line, color)


structlog.configure(
    processors=[basic_stringifier],
    logger_factory=structlog.PrintLoggerFactory(sys.stderr),
    wrapper_class=structlog.make_filtering_bound_logger(INFO),
    cache_logger_on_first_use=False,
)

from typing import TYPE_CHECKING  # noqa: E402

if TYPE_CHECKING:
    from contrast.agent.context import ContrastContext, WebContext

import os  # noqa: E402
from contextvars import ContextVar  # noqa: E402

from contrast.agent.assess.string_tracker import StringTracker  # noqa: E402

# aliases
from contrast.agent.assess.utils import get_properties  # noqa: F401 E402
from contrast.version import __version__  # noqa: E402

# process globals
CONTEXT: ContextVar[ContrastContext | None] = ContextVar(
    "contrast_context", default=None
)
WEB_CONTEXT: ContextVar[WebContext | None] = ContextVar(
    "contrast_web_context", default=None
)
STRING_TRACKER = StringTracker()
TELEMETRY = None

# PERF: These values are constant for the lifetime of the agent,
# so we compute them only once instead of potentially computing
# them hundreds of times.
AGENT_CURR_WORKING_DIR = os.getcwd()


def telemetry_disabled() -> bool:
    return os.environ.get("CONTRAST_AGENT_TELEMETRY_OPTOUT", "").lower() in [
        "1",
        "true",
    ]


def get_canonical_version() -> str:
    return ".".join(__version__.split(".")[:3])


class SecurityException(Exception):
    """
    Exceptions raised by Contrast to block attacks.
    """


class AttackBlockedException(SecurityException):
    """
    Exception raised by Contrast Protect to block attacks. Full attack details are
    reported to the Contrast UI.
    """

    def __init__(self, *, rule_name: str) -> None:
        super().__init__(
            f"Contrast Protect blocked an attack for rule: {rule_name}. See Contrast UI"
            " for full details."
        )
