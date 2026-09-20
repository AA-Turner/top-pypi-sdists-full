#
#   Local Objects
#

from ..basetypes import PropertyIdentifier
from ..vendor import VendorInfo


class LocalPropertyIdentifier(PropertyIdentifier):
    settings = 512


local_vendor_info = VendorInfo(999, property_identifier=LocalPropertyIdentifier)

from . import (
    analog,
    binary,
    cmd,
    cov,
    device,
    event,
    fault,
    networkport,
    object,
    schedule,
)
