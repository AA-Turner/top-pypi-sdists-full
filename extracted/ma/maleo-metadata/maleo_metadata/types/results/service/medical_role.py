from typing import Union
from maleo_metadata.models.transfers.results.service.medical_role import MaleoMetadataMedicalRoleServiceResultsTransfers

class MaleoMetadataMedicalRoleServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataMedicalRoleServiceResultsTransfers.Fail,
        MaleoMetadataMedicalRoleServiceResultsTransfers.NoData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.MultipleData
    ]

    GetStructuredMultiple = Union[
        MaleoMetadataMedicalRoleServiceResultsTransfers.Fail,
        MaleoMetadataMedicalRoleServiceResultsTransfers.NoData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.MultipleStructured
    ]

    GetSingle = Union[
        MaleoMetadataMedicalRoleServiceResultsTransfers.Fail,
        MaleoMetadataMedicalRoleServiceResultsTransfers.NoData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.SingleData
    ]

    GetSingleStructured = Union[
        MaleoMetadataMedicalRoleServiceResultsTransfers.Fail,
        MaleoMetadataMedicalRoleServiceResultsTransfers.NoData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.SingleStructured
    ]