from typing import Union
from maleo_metadata.models.transfers.results.client.user_type import MaleoMetadataUserTypeClientResultsTransfers

class MaleoMetadataUserTypeClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataUserTypeClientResultsTransfers.MultipleData,
        MaleoMetadataUserTypeClientResultsTransfers.NoData,
        MaleoMetadataUserTypeClientResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataUserTypeClientResultsTransfers.SingleData,
        MaleoMetadataUserTypeClientResultsTransfers.Fail
    ]