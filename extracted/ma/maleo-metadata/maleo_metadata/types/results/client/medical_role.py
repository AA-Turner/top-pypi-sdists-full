from typing import Union
from maleo_metadata.models.transfers.results.client.medical_role import MaleoMetadataMedicalRoleClientResultsTransfers

class MaleoMetadataMedicalRoleClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
        MaleoMetadataMedicalRoleClientResultsTransfers.NoData,
        MaleoMetadataMedicalRoleClientResultsTransfers.MultipleData
    ]

    GetStructuredMultiple = Union[
        MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
        MaleoMetadataMedicalRoleClientResultsTransfers.NoData,
        MaleoMetadataMedicalRoleClientResultsTransfers.MultipleStructured
    ]

    GetSingle = Union[
        MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
        MaleoMetadataMedicalRoleClientResultsTransfers.SingleData
    ]

    GetSingleStructured = Union[
        MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
        MaleoMetadataMedicalRoleClientResultsTransfers.SingleStructured
    ]