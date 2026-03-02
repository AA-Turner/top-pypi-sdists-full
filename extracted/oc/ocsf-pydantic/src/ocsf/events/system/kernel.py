from enum import Enum
from ocsf.events.system import SystemActivity

from ocsf.objects.kernel import KernelResource


class KernelActivityActivityId(Enum):
    Create: int = 1
    Read: int = 2
    Delete: int = 3
    Invoke: int = 4

class KernelActivity(SystemActivity):
    """
    Kernel Activity events report when an process creates, reads, or deletes a
    kernel resource.
    """

    class_uid: int = 1003
    class_name: str = 'Kernel Activity'

    kernel: KernelResource # The target kernel resource.

    # Optional:
    activity_id: KernelActivityActivityId | None = None
