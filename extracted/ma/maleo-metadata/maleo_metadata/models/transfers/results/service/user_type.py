from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_metadata.models.transfers.general.user_type import UserTypeTransfers

class MaleoMetadataUserTypeServiceResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:UserTypeTransfers = Field(..., description="Single user type data")

    class MultipleData(BaseServiceGeneralResultsTransfers.UnpaginatedMultipleData):
        data:list[UserTypeTransfers] = Field(..., description="Multiple user types data")