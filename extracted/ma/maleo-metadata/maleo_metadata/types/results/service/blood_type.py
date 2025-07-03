from typing import Union
from maleo_metadata.models.transfers.results.service.blood_type import MaleoMetadataBloodTypeServiceResultsTransfers

class MaleoMetadataBloodTypeServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataBloodTypeServiceResultsTransfers.MultipleData,
        MaleoMetadataBloodTypeServiceResultsTransfers.NoData,
        MaleoMetadataBloodTypeServiceResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataBloodTypeServiceResultsTransfers.SingleData,
        MaleoMetadataBloodTypeServiceResultsTransfers.NoData,
        MaleoMetadataBloodTypeServiceResultsTransfers.Fail
    ]