from dataclasses import dataclass

@dataclass(kw_only=True)
class SchedulerEventData:
    """
    Base data structure for events in the scheduler system.

    This class serves as a foundational data container for events triggered within the scheduler.
    It holds a numeric event code that uniquely identifies the event type. Subclasses can extend
    this class to include additional event-specific context.

    Parameters
    ----------
    code : int
        Numeric code that uniquely identifies the type of event within the scheduler system.

    Returns
    -------
    SchedulerEventData
        An instance of SchedulerEventData with the specified event code.
    """

    # Numeric code representing the type of event in the scheduler
    code: int
