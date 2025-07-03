from typing import Union
from maleo_metadata.models.transfers.results.service.service import MaleoMetadataServiceServiceResultsTransfers

class MaleoMetadataServiceServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataServiceServiceResultsTransfers.MultipleData,
        MaleoMetadataServiceServiceResultsTransfers.NoData,
        MaleoMetadataServiceServiceResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataServiceServiceResultsTransfers.SingleData,
        MaleoMetadataServiceServiceResultsTransfers.NoData,
        MaleoMetadataServiceServiceResultsTransfers.Fail
    ]