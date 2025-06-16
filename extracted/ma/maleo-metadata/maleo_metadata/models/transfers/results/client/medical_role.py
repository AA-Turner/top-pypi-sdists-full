from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_metadata.models.transfers.general.medical_role import MedicalRoleTransfers, StructuredMedicalRoleTransfers

class MaleoMetadataMedicalRoleClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:MedicalRoleTransfers = Field(..., description="Single medical role data")

    class SingleStructured(BaseClientServiceResultsTransfers.SingleData):
        data:StructuredMedicalRoleTransfers = Field(..., description="Single structured medical role data")

    class MultipleData(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[MedicalRoleTransfers] = Field(..., description="Multiple medical roles data")

    class MultipleStructured(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[StructuredMedicalRoleTransfers] = Field(..., description="Multiple structured medical roles data")