from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class SchedulerEventData:
    """
    Represents the data associated with scheduler-related events.

    This class serves as a base structure for encapsulating information about
    events occurring within the scheduler system. It includes a numeric event
    code to identify the type of event and an optional alias for additional
    context.

    Attributes
    ----------
    code : int
        A numeric code that uniquely identifies the type of event within the
        scheduler system.
    alias : str, optional
        An optional string providing additional context or identifying specific
        components (e.g., executors or job stores) related to the event.

    Returns
    -------
    SchedulerEventData
        An instance of the `SchedulerEventData` class containing the event code
        and optional alias.
    """
    # Numeric code representing the type of event
    code: int

    # Optional alias for additional context about the event
    alias: Optional[str] = None