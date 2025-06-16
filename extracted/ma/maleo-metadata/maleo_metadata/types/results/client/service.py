from typing import Union
from maleo_metadata.models.transfers.results.client.service import MaleoMetadataServiceClientResultsTransfers

class MaleoMetadataServiceClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataServiceClientResultsTransfers.Fail,
        MaleoMetadataServiceClientResultsTransfers.NoData,
        MaleoMetadataServiceClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataServiceClientResultsTransfers.Fail,
        MaleoMetadataServiceClientResultsTransfers.SingleData
    ]