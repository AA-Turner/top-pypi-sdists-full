from typing import Union
from maleo_metadata.models.transfers.results.client.user_type import MaleoMetadataUserTypeClientResultsTransfers

class MaleoMetadataUserTypeClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataUserTypeClientResultsTransfers.Fail,
        MaleoMetadataUserTypeClientResultsTransfers.NoData,
        MaleoMetadataUserTypeClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataUserTypeClientResultsTransfers.Fail,
        MaleoMetadataUserTypeClientResultsTransfers.SingleData
    ]