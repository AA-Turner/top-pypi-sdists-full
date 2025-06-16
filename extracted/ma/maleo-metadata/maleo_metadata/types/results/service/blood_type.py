from typing import Union
from maleo_metadata.models.transfers.results.service.blood_type import MaleoMetadataBloodTypeServiceResultsTransfers

class MaleoMetadataBloodTypeServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataBloodTypeServiceResultsTransfers.Fail,
        MaleoMetadataBloodTypeServiceResultsTransfers.NoData,
        MaleoMetadataBloodTypeServiceResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataBloodTypeServiceResultsTransfers.Fail,
        MaleoMetadataBloodTypeServiceResultsTransfers.NoData,
        MaleoMetadataBloodTypeServiceResultsTransfers.SingleData
    ]