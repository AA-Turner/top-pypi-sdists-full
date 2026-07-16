from typing import Union, Required, TypedDict, Literal


class CheckIn(TypedDict, total=False):
    """
    check_in.

    A message that contains a monitor check-in payload.
    """

    message_type: Required[Literal['check_in']]
    """
    Discriminant marker identifying this as a check-in message.

    Required property
    """

    payload: Required[bytes]
    """
    bytes. JSON string of the wrapped monitor check-in event.

    $bytes: True

    Required property
    """

    start_time: Required[Union[int, float]]
    """
    The time relay received the envelope containing the check-in. In seconds.

    Required property
    """

    project_id: Required[int]
    """
    The project for which this check-in is being sent.

    minimum: 0
    maximum: 18446744073709551615

    Required property
    """

    sdk: Union[str, None]
    """ The originating SDK client identifier string. """

    retention_days: Required[int]
    """
    minimum: 0
    maximum: 65535

    Required property
    """



class ClockPulse(TypedDict, total=False):
    """
    clock_pulse.

    A message that is only used as a marker for minute boundaries.
    """

    message_type: Required[Literal['clock_pulse']]
    """
    Discriminant marker identifying this as a clock-pulse message.

    Required property
    """



IngestMonitorMessage = Union["ClockPulse", "CheckIn"]
"""
ingest_monitor_message.

Aggregation type: oneOf
"""

