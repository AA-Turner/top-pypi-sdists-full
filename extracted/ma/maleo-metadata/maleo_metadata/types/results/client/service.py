from typing import Union
from maleo_metadata.models.transfers.results.client.service import MaleoMetadataServiceClientResultsTransfers

class MaleoMetadataServiceClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataServiceClientResultsTransfers.MultipleData,
        MaleoMetadataServiceClientResultsTransfers.NoData,
        MaleoMetadataServiceClientResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataServiceClientResultsTransfers.SingleData,
        MaleoMetadataServiceClientResultsTransfers.Fail
    ]