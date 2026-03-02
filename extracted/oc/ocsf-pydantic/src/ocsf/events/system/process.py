from enum import Enum

from ocsf.events.system import SystemActivity

from ocsf.objects.actor import Actor
from ocsf.objects.module import Module
from ocsf.objects.process import Process


class ProcessActivityActivityId(Enum):
    Launch: int = 1
    Terminate: int = 2
    Open: int = 3
    Inject: int = 4
    Set_User_Id: int = 5


class ProcessActivity(SystemActivity):
    """
    Process Activity events report when a process launches, injects, opens or
    terminates another process, successful or otherwise.
    """

    class_uid: int = 1007
    class_name: str = 'Process Activity'

    process: Process # The process that was launched, injected into, opened, or
                     # terminated.

    # Recommended:
    actual_permissions: int | None = None
    exit_code: int | None = None
    injection_type: str | None = None
    injection_type_id: int | None = None
    module: Module | None = None # The module that was injected by the actor process.
    requested_permissions: int | None = None

    # Optional:
    activity_id: ProcessActivityActivityId | None = None
    actor: Actor | None = None # The actor that performed the activity on the target
                               # `process`. For example, the process that started a new
                               # process or injected code into another process.
