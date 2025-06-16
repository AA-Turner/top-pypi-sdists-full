from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_metadata.models.transfers.general.blood_type import BloodTypeTransfers

class MaleoMetadataBloodTypeClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:BloodTypeTransfers = Field(..., description="Single blood type data")

    class MultipleData(BaseClientServiceResultsTransfers.UnpaginatedMultipleData):
        data:list[BloodTypeTransfers] = Field(..., description="Multiple blood types data")