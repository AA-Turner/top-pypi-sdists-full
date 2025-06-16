from typing import Union
from maleo_metadata.models.transfers.results.service.service import MaleoMetadataServiceServiceResultsTransfers

class MaleoMetadataServiceServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataServiceServiceResultsTransfers.Fail,
        MaleoMetadataServiceServiceResultsTransfers.NoData,
        MaleoMetadataServiceServiceResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataServiceServiceResultsTransfers.Fail,
        MaleoMetadataServiceServiceResultsTransfers.NoData,
        MaleoMetadataServiceServiceResultsTransfers.SingleData
    ]