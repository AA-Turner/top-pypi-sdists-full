# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime

from ..._models import BaseModel

__all__ = ["ModelUsage", "Data"]


class Data(BaseModel):
    date: datetime
    """The start date of the data point"""

    prompt_tokens: int
    """The number of prompt tokens used"""

    response_tokens: int
    """The number of response tokens used"""

    summary_tokens: int
    """The number of all the tokens used"""


class ModelUsage(BaseModel):
    data: List[Data]
    """The list of data points for the given period"""

    end_date: datetime
    """The end date of the data points. Equal to the last date in the data list"""

    start_date: datetime
    """The start date of the data points. Equal to the first date in the data list"""
