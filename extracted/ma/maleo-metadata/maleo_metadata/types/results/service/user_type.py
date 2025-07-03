from typing import Union
from maleo_metadata.models.transfers.results.service.user_type import MaleoMetadataUserTypeServiceResultsTransfers

class MaleoMetadataUserTypeServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataUserTypeServiceResultsTransfers.MultipleData,
        MaleoMetadataUserTypeServiceResultsTransfers.NoData,
        MaleoMetadataUserTypeServiceResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataUserTypeServiceResultsTransfers.SingleData,
        MaleoMetadataUserTypeServiceResultsTransfers.NoData,
        MaleoMetadataUserTypeServiceResultsTransfers.Fail
    ]