from typing import Union
from maleo_metadata.models.transfers.results.client.gender import MaleoMetadataGenderClientResultsTransfers

class MaleoMetadataGenderClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataGenderClientResultsTransfers.Fail,
        MaleoMetadataGenderClientResultsTransfers.NoData,
        MaleoMetadataGenderClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataGenderClientResultsTransfers.Fail,
        MaleoMetadataGenderClientResultsTransfers.SingleData
    ]