from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_metadata.models.transfers.general.blood_type import BloodTypeTransfers

class MaleoMetadataBloodTypeServiceResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:BloodTypeTransfers = Field(..., description="Single blood type data")

    class MultipleData(BaseServiceGeneralResultsTransfers.UnpaginatedMultipleData):
        data:list[BloodTypeTransfers] = Field(..., description="Multiple blood types data")