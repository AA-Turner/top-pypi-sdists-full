from typing import Union
from maleo_metadata.models.transfers.results.service.user_type import MaleoMetadataUserTypeServiceResultsTransfers

class MaleoMetadataUserTypeServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataUserTypeServiceResultsTransfers.Fail,
        MaleoMetadataUserTypeServiceResultsTransfers.NoData,
        MaleoMetadataUserTypeServiceResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataUserTypeServiceResultsTransfers.Fail,
        MaleoMetadataUserTypeServiceResultsTransfers.NoData,
        MaleoMetadataUserTypeServiceResultsTransfers.SingleData
    ]