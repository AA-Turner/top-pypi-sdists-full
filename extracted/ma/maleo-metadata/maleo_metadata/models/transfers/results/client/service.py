from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_metadata.models.transfers.general.service import ServiceTransfers

class MaleoMetadataServiceClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:ServiceTransfers = Field(..., description="Single service data")

    class MultipleData(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[ServiceTransfers] = Field(..., description="Multiple services data")