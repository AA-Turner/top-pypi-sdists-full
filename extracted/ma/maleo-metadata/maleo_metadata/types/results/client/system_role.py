from typing import Union
from maleo_metadata.models.transfers.results.client.system_role import MaleoMetadataSystemRoleClientResultsTransfers

class MaleoMetadataSystemRoleClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataSystemRoleClientResultsTransfers.Fail,
        MaleoMetadataSystemRoleClientResultsTransfers.NoData,
        MaleoMetadataSystemRoleClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataSystemRoleClientResultsTransfers.Fail,
        MaleoMetadataSystemRoleClientResultsTransfers.SingleData
    ]