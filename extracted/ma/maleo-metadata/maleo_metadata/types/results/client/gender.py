from typing import Union
from maleo_metadata.models.transfers.results.client.gender import MaleoMetadataGenderClientResultsTransfers

class MaleoMetadataGenderClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataGenderClientResultsTransfers.MultipleData,
        MaleoMetadataGenderClientResultsTransfers.NoData,
        MaleoMetadataGenderClientResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataGenderClientResultsTransfers.SingleData,
        MaleoMetadataGenderClientResultsTransfers.Fail
    ]