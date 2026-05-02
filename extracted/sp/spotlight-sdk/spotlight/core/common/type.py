"""
Common types.
"""

from datetime import date, datetime
from typing import NewType, Union

from pandas import DataFrame

Datetime = NewType("Datetime", Union[date, datetime])
DataResponse = NewType("DataResponse", Union[DataFrame, float])
