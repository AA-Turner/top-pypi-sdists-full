from enum import Enum

from ocsf.events.system import SystemActivity

from ocsf.objects.actor import Actor
from ocsf.objects.module import Module


class ModuleActivityActivityId(Enum):
    Load: int = 1
    Unload: int = 2


class ModuleActivity(SystemActivity):
    """
    Module Activity events report when a process loads or unloads the
    module
    """

    class_uid: int = 1005
    class_name: str = 'Module Activity'

    actor: Actor # The actor that loaded or unloaded the `module`.
    module: Module # The module that was loaded or unloaded.


    # Optional:
    activity_id: ModuleActivityActivityId | None = None
