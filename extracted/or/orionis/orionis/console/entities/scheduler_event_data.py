from dataclasses import dataclass

@dataclass(kw_only=True)
class SchedulerEventData:
    """
    Base data structure for scheduler-related events.

    This class encapsulates information about events that occur within the scheduler system.
    It provides a numeric event code to identify the event type and can be extended for
    additional context as needed.

    Parameters
    ----------
    code : int
        Numeric code that uniquely identifies the type of event within the scheduler system.

    Returns
    -------
    SchedulerEventData
        An instance of SchedulerEventData containing the event code.
    """

    # Numeric code representing the type of event
    code: int
