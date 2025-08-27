# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
import sys
from logging import DEBUG

from contrast_vendor import structlog


structlog.configure(
    logger_factory=structlog.PrintLoggerFactory(sys.stderr),
    wrapper_class=structlog.make_filtering_bound_logger(DEBUG),
    cache_logger_on_first_use=False,
)

from typing import TYPE_CHECKING  # noqa: E402

if TYPE_CHECKING:
    from contrast.agent.request_context import RequestContext

import os  # noqa: E402
import contextlib  # noqa: E402
from contextvars import ContextVar  # noqa: E402
from contrast.agent.assess.string_tracker import StringTracker  # noqa: E402
from contrast.version import __version__  # noqa: E402

# aliases
from contrast.agent.assess.utils import get_properties  # noqa: F401 E402

# process globals
REQUEST_CONTEXT: ContextVar[RequestContext | None] = ContextVar(
    "contrast_request_context", default=None
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
    Exception raised by Contrast Protect to block attacks. Full attack details are
    reported to the Contrast UI.
    """

    def __init__(self, *, rule_name: str) -> None:
        super().__init__(
            f"Contrast Protect blocked an attack for rule: {rule_name}. See Contrast UI"
            " for full details."
        )


@contextlib.contextmanager
def lifespan(context: RequestContext):
    # py313 - this method will no longer be necessary when we drop 3.13 because
    # `set()` is a contextmanager in 3.14+
    token = REQUEST_CONTEXT.set(context)
    try:
        yield context
    finally:
        REQUEST_CONTEXT.reset(token)
