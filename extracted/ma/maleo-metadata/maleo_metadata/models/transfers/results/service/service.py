from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_metadata.models.transfers.general.service import ServiceTransfers

class MaleoMetadataServiceServiceResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:ServiceTransfers = Field(..., description="Single service data")

    class MultipleData(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[ServiceTransfers] = Field(..., description="Multiple services data")