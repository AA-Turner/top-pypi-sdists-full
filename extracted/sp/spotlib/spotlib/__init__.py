from spotlib._version import __version__ as version
from spotlib.statics import local_config


__author__ = 'Blake Huber'
__version__ = version
__email__ = "blakeca00@gmail.com"


try:


    from libtools import Colors
    from libtools import logd

    # global logger
    logd.local_config = local_config
    logger = logd.getLogger(__version__)

    from spotlib.core import EC2SpotPrices as SpotPrices
    from spotlib.core import DurationEndpoints
    from spotlib.core import UtcConversion, utc_conversion

except Exception:
    pass
