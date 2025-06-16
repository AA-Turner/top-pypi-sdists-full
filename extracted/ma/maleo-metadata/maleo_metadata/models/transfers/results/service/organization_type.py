from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_metadata.models.transfers.general.organization_type import OrganizationTypeTransfers

class MaleoMetadataOrganizationTypeServiceResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:OrganizationTypeTransfers = Field(..., description="Single organization type data")

    class MultipleData(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[OrganizationTypeTransfers] = Field(..., description="Multiple organization types data")