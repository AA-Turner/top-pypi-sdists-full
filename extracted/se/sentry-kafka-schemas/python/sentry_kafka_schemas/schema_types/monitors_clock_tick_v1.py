from typing import Union, Required, TypedDict


class ClockTick(TypedDict, total=False):
    """
    clock_tick.

    A message indicating that the ingest-monitor consumer has processed check-ins past the specified minute-bound timestamp.
    """

    ts: Required[Union[int, float]]
    """
    The timestamp the clock ticked at.

    Required property
    """

