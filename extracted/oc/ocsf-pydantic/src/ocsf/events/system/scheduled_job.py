from enum import Enum

from ocsf.events.system import SystemActivity

from ocsf.objects.actor import Actor
from ocsf.objects.job import Job


class ScheduledJobActivityActivityId(Enum):
    Create: int = 1
    Update: int = 2
    Delete: int = 3
    Enable: int = 4
    Disable: int = 5
    Start: int = 6


class ScheduledJobActivity(SystemActivity):
    """
    Scheduled Job Activity events report activities related to scheduled jobs or
    tasks.
    """

    class_uid: int = 1006
    class_name: str = 'Scheduled Job Activity'

    job: Job

    # Optional:
    activity_id: ScheduledJobActivityActivityId | None = None
    actor: Actor | None = None # The actor that performed the activity on the `job` object.
