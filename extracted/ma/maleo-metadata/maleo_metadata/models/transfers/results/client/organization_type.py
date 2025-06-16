from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_metadata.models.transfers.general.organization_type import OrganizationTypeTransfers

class MaleoMetadataOrganizationTypeClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:OrganizationTypeTransfers = Field(..., description="Single organization type data")

    class MultipleData(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[OrganizationTypeTransfers] = Field(..., description="Multiple organization types data")