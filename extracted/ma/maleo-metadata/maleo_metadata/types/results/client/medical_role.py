from typing import Union
from maleo_metadata.models.transfers.results.client.medical_role import MaleoMetadataMedicalRoleClientResultsTransfers

class MaleoMetadataMedicalRoleClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataMedicalRoleClientResultsTransfers.MultipleData,
        MaleoMetadataMedicalRoleClientResultsTransfers.NoData,
        MaleoMetadataMedicalRoleClientResultsTransfers.Fail
    ]

    GetStructuredMultiple = Union[
        MaleoMetadataMedicalRoleClientResultsTransfers.MultipleStructured,
        MaleoMetadataMedicalRoleClientResultsTransfers.NoData,
        MaleoMetadataMedicalRoleClientResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataMedicalRoleClientResultsTransfers.SingleData,
        MaleoMetadataMedicalRoleClientResultsTransfers.Fail
    ]

    GetSingleStructured = Union[
        MaleoMetadataMedicalRoleClientResultsTransfers.SingleStructured,
        MaleoMetadataMedicalRoleClientResultsTransfers.Fail
    ]