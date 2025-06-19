# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import sys
from types import CodeType
from typing import Any
from contrast.utils.assess.tracking_util import SUPPORTED_TYPES
from contrast.utils.decorators import fail_quietly
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

# sys.monitoring only allows "tools" with IDs 0-5, inclusive. The following are defined:
#
# sys.monitoring.DEBUGGER_ID = 0
# sys.monitoring.COVERAGE_ID = 1
# sys.monitoring.PROFILER_ID = 2
# sys.monitoring.OPTIMIZER_ID = 5
#
# However, any value from 0-5 may be used. To reduce the probability of conflict, and
# since we don't really fall into any of the above tool types, we use a different ID.
# See https://docs.python.org/3/library/sys.monitoring.html
MAX_TOOL_ID = 5
CONTRAST_TOOL_ID = 4
CONTRAST_TOOL_NAME = "contrast"
VALID_TOOL_IDS = range(MAX_TOOL_ID + 1)


@fail_quietly()
def enable() -> None:
    """
    Enable sys.monitoring events if possible. We currently use this as a workaround for
    string propagation loss that results from bytecode specialization introduced in
    python 3.12. Enabling sys.monitoring prevents bytecode specialization from occurring
    for the monitored instructions. See the related pytest fixture for more detail.

    This is a fairly blunt solution to this problem, and in the future it may not be
    necessary.

    Returns True if sys.monitoring is enabled successfully and False otherwise.
    """
    if sys.version_info[:2] < (3, 12):
        logger.debug("Pre-3.12 environment detected. Will not enable sys.monitoring.")
        return

    if is_enabled():
        logger.debug("sys.monitoring is already enabled.")
        return

    from sys import monitoring

    logger.debug("summarizing sys.monitoring tools already in use")
    for tool_id in VALID_TOOL_IDS:
        logger.debug(
            "sys.monitoring tool ID %s: %s", tool_id, monitoring.get_tool(tool_id)
        )

    if monitoring.get_tool(CONTRAST_TOOL_ID) is not None:
        logger.debug(
            "Cannot enable sys.monitoring - tool ID %s is already registered",
            CONTRAST_TOOL_ID,
        )
        return

    monitoring.use_tool_id(CONTRAST_TOOL_ID, CONTRAST_TOOL_NAME)
    monitoring.set_events(CONTRAST_TOOL_ID, monitoring.events.CALL)
    monitoring.register_callback(
        CONTRAST_TOOL_ID, monitoring.events.CALL, _strlike_call_specialization_disabler
    )

    logger.debug("Enabled contrast sys.monitoring tool")


def _strlike_call_specialization_disabler(
    code: CodeType, instruction_offset: int, callable: object, arg0: object
) -> Any:
    # We need to check SUPPORTED_TYPES is not None because this callback will
    # still be installed during interpreter shutdown, when global variables may be
    # set to None.
    if SUPPORTED_TYPES is not None and callable not in SUPPORTED_TYPES:
        return sys.monitoring.DISABLE


@fail_quietly(return_value=False)
def is_enabled() -> bool:
    if sys.version_info[:2] < (3, 12):
        return False
    from sys import monitoring

    return bool(
        monitoring.get_tool(CONTRAST_TOOL_ID) == CONTRAST_TOOL_NAME
        and monitoring.get_events(CONTRAST_TOOL_ID) & monitoring.events.CALL
    )


@fail_quietly()
def disable():
    if sys.version_info[:2] < (3, 12):
        return
    from sys import monitoring

    monitoring.set_events(CONTRAST_TOOL_ID, monitoring.events.NO_EVENTS)
    monitoring.free_tool_id(CONTRAST_TOOL_ID)
