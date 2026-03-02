from ocsf.events.discovery import Discovery

from ocsf.objects.actor import Actor
from ocsf.objects.device import Device
from ocsf.objects.security_state import SecurityState


class DeviceConfigStateChange(Discovery):
    """
    Device Config State Change events report state changes that impact the security
    of the device.
    """

    class_uid: int = 5019
    class_name: str = 'Device Config State Change'

    device: Device # The device that is impacted by the state change.

    # Recommended:
    prev_security_level: str | None = None
    prev_security_level_id: int | None = None
    prev_security_states: list[SecurityState] | None = None # The previous security states of the
                                                            # device.
    security_level: str | None = None
    security_level_id: int | None = None
    security_states: list[SecurityState] | None = None # The current security states of the device.

    # Optional:
    actor: Actor | None = None
