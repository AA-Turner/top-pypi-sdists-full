from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_metadata.models.transfers.general.system_role import SystemRoleTransfers

class MaleoMetadataSystemRoleServiceResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:SystemRoleTransfers = Field(..., description="Single system role data")

    class MultipleData(BaseServiceGeneralResultsTransfers.UnpaginatedMultipleData):
        data:list[SystemRoleTransfers] = Field(..., description="Multiple system roles data")