from typing import Union
from maleo_metadata.models.transfers.results.client.system_role import MaleoMetadataSystemRoleClientResultsTransfers

class MaleoMetadataSystemRoleClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataSystemRoleClientResultsTransfers.MultipleData,
        MaleoMetadataSystemRoleClientResultsTransfers.NoData,
        MaleoMetadataSystemRoleClientResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataSystemRoleClientResultsTransfers.SingleData,
        MaleoMetadataSystemRoleClientResultsTransfers.Fail
    ]