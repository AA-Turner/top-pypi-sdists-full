from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_metadata.models.transfers.general.medical_role import MedicalRoleTransfers, StructuredMedicalRoleTransfers

class MaleoMetadataMedicalRoleServiceResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:MedicalRoleTransfers = Field(..., description="Single medical role data")

    class SingleStructured(BaseServiceGeneralResultsTransfers.SingleData):
        data:StructuredMedicalRoleTransfers = Field(..., description="Single structured medical role data")

    class MultipleData(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[MedicalRoleTransfers] = Field(..., description="Multiple medical roles data")

    class MultipleStructured(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[StructuredMedicalRoleTransfers] = Field(..., description="Multiple structured medical roles data")