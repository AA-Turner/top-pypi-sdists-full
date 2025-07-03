from typing import Union
from maleo_metadata.models.transfers.results.service.system_role import MaleoMetadataSystemRoleServiceResultsTransfers

class MaleoMetadataSystemRoleServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataSystemRoleServiceResultsTransfers.MultipleData,
        MaleoMetadataSystemRoleServiceResultsTransfers.NoData,
        MaleoMetadataSystemRoleServiceResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataSystemRoleServiceResultsTransfers.SingleData,
        MaleoMetadataSystemRoleServiceResultsTransfers.NoData,
        MaleoMetadataSystemRoleServiceResultsTransfers.Fail
    ]