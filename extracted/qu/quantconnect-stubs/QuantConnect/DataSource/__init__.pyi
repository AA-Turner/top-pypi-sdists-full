from typing import overload
from enum import IntEnum
import QuantConnect.Data
import QuantConnect.DataSource


class NullData(QuantConnect.Data.BaseData):
    """Represents a custom data type place holder"""


