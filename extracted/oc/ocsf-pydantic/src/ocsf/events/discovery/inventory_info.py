from ocsf.events.discovery import Discovery

from ocsf.objects.actor import Actor
from ocsf.objects.device import Device


class DeviceInventoryInfo(Discovery):
    """
    Device Inventory Info events report device inventory data that is either logged
    or proactively collected. For example, when collecting device information from a
    CMDB or running a network sweep of connected devices.
    """

    class_uid: int = 5001
    class_name: str = 'Device Inventory Info'

    device: Device # The device that is being discovered by an inventory process.

    # Optional:
    actor: Actor | None = None
