"""FortiOS CMDB - Dlp category"""

from .data_type import DataType
from .dictionary import Dictionary
from .exact_data_match import ExactDataMatch
from .filepattern import Filepattern
from .label import Label
from .profile import Profile
from .sensor import Sensor
from .settings import Settings

__all__ = [
    "DataType",
    "Dictionary",
    "Dlp",
    "ExactDataMatch",
    "Filepattern",
    "Label",
    "Profile",
    "Sensor",
    "Settings",
]


class Dlp:
    """Dlp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Dlp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.data_type = DataType(client)
        self.dictionary = Dictionary(client)
        self.exact_data_match = ExactDataMatch(client)
        self.filepattern = Filepattern(client)
        self.label = Label(client)
        self.profile = Profile(client)
        self.sensor = Sensor(client)
        self.settings = Settings(client)
