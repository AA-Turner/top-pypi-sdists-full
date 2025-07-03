from typing import Union
from maleo_metadata.models.transfers.results.service.medical_role import MaleoMetadataMedicalRoleServiceResultsTransfers

class MaleoMetadataMedicalRoleServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataMedicalRoleServiceResultsTransfers.MultipleData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.NoData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.Fail
    ]

    GetStructuredMultiple = Union[
        MaleoMetadataMedicalRoleServiceResultsTransfers.MultipleStructured,
        MaleoMetadataMedicalRoleServiceResultsTransfers.NoData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataMedicalRoleServiceResultsTransfers.SingleData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.NoData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.Fail
    ]

    GetSingleStructured = Union[
        MaleoMetadataMedicalRoleServiceResultsTransfers.SingleStructured,
        MaleoMetadataMedicalRoleServiceResultsTransfers.NoData,
        MaleoMetadataMedicalRoleServiceResultsTransfers.Fail
    ]