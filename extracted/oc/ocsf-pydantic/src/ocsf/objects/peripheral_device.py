from ._entity import Entity

class PeripheralDevice(Entity):
    """
    The peripheral device object describes the identity, vendor and model of a
    peripheral device.
    """

    class_: str # The class of the peripheral device.
    name: str # The name of the peripheral device.

    # Recommended:
    model: str | None = None
    serial_number: str | None = None # The peripheral device serial number.
    uid: str | None = None # The unique identifier of the peripheral device.
    vendor_name: str | None = None # The peripheral device vendor.
