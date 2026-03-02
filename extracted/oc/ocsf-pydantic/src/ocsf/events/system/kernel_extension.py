from enum import Enum

from ocsf.events.system import SystemActivity

from ocsf.objects.actor import Actor
from ocsf.objects.kernel_driver import KernelExtension


class KernelExtensionActivityActivityId(Enum):
    Load: int = 1 # A driver/extension was loaded into the kernel
    Unload: int = 2 # A driver/extension was unloaded (removed) from the kernel


class KernelExtensionActivity(SystemActivity):
    """
    Kernel Extension events report when a driver/extension is loaded or unloaded
    into the kernel
    """

    class_uid: int = 1002
    class_name: str = 'Kernel Extension Activity'

    actor: Actor # The actor process that loaded or unloaded the driver/extension.
    driver: KernelExtension

    # Optional:
    activity_id: KernelExtensionActivityActivityId | None = None
