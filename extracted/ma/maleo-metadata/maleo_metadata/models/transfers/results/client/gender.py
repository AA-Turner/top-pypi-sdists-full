from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_metadata.models.transfers.general.gender import GenderTransfers

class MaleoMetadataGenderClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:GenderTransfers = Field(..., description="Single gender data")

    class MultipleData(BaseClientServiceResultsTransfers.UnpaginatedMultipleData):
        data:list[GenderTransfers] = Field(..., description="Multiple genders data")