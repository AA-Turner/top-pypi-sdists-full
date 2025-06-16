from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_metadata.models.transfers.general.user_type import UserTypeTransfers

class MaleoMetadataUserTypeClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:UserTypeTransfers = Field(..., description="Single user type data")

    class MultipleData(BaseClientServiceResultsTransfers.UnpaginatedMultipleData):
        data:list[UserTypeTransfers] = Field(..., description="Multiple user types data")