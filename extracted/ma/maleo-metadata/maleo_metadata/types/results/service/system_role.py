from typing import Union
from maleo_metadata.models.transfers.results.service.system_role import MaleoMetadataSystemRoleServiceResultsTransfers

class MaleoMetadataSystemRoleServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataSystemRoleServiceResultsTransfers.Fail,
        MaleoMetadataSystemRoleServiceResultsTransfers.NoData,
        MaleoMetadataSystemRoleServiceResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataSystemRoleServiceResultsTransfers.Fail,
        MaleoMetadataSystemRoleServiceResultsTransfers.NoData,
        MaleoMetadataSystemRoleServiceResultsTransfers.SingleData
    ]