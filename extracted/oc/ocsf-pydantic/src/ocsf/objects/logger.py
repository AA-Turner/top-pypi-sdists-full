from datetime import datetime

from ._entity import Entity

from .product import Product
from .device import Device


class Logger(Entity):
    """
    The Logger object represents the device and product where events are stored with
    times for receipt and transmission.  This may be at the source device where the
    event occurred, a remote scanning device, intermediate hops, or the ultimate
    destination.
    """

    # Recommended:
    device: Device | None = None # The device where the events are logged.
    log_name: str | None = None
    log_provider: str | None = None
    logged_time: datetime | None = None
    name: str | None = None # The name of the logging product instance.
    product: Product | None = None # The product logging the event.  This may be the event source
                                   # product, a management server product, a scanning product, a SIEM,
                                   # etc.
    uid: str | None = None # The unique identifier of the logging product instance.

    # Optional:
    log_level: str | None = None
    log_version: str | None = None
    transmit_time: datetime | None = None # The time when the event was transmitted from the logging
                                          # device to it's next destination.
    version: str | None = None # The version of the logging product.
