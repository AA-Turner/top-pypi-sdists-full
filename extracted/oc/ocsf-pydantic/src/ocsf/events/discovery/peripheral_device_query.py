from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.peripheral_device import PeripheralDevice


class PeripheralDeviceQuery(DiscoveryResult):
    """
    Peripheral Device Query events report information about peripheral devices.
    """

    class_uid: int = 5014
    class_name: str = 'Peripheral Device Query'

    peripheral_device: PeripheralDevice
