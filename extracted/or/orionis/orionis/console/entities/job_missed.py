from dataclasses import dataclass
from datetime import datetime
from orionis.console.entities.job_event_data import JobEventData

@dataclass(kw_only=True)
class JobMissed(JobEventData):
    """
    Represents an event triggered when a scheduled job run is missed due to scheduler constraints.

    This class extends `JobEventData` and provides additional information about the missed job event, 
    specifically the time the job was originally scheduled to run.

    Attributes
    ----------
    scheduled_run_time : datetime
        The datetime when the job was originally scheduled to execute.

    Returns
    -------
    None
        This class does not return a value; it is used to encapsulate event data.
    """

    # The datetime when the job was supposed to run but was missed
    scheduled_run_time: datetime