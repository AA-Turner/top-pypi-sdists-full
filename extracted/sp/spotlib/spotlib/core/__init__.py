from spotlib._version import __version__ as version


__author__ = 'Blake Huber'
__version__ = version
__email__ = "blakeca00@gmail.com"


from spotlib.core.ancillary import session_selector
from spotlib.core.endpoints import DurationEndpoints
from spotlib.core.spotcore import EC2SpotPrices
from spotlib.core.utc import UtcConversion, utc_conversion
