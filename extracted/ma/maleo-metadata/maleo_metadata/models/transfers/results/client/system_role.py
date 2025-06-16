from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_metadata.models.transfers.general.system_role import SystemRoleTransfers

class MaleoMetadataSystemRoleClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:SystemRoleTransfers = Field(..., description="Single system role data")

    class MultipleData(BaseClientServiceResultsTransfers.UnpaginatedMultipleData):
        data:list[SystemRoleTransfers] = Field(..., description="Multiple system roles data")