from typing import Union
from maleo_metadata.models.transfers.results.service.gender import MaleoMetadataGenderServiceResultsTransfers

class MaleoMetadataGenderServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataGenderServiceResultsTransfers.Fail,
        MaleoMetadataGenderServiceResultsTransfers.NoData,
        MaleoMetadataGenderServiceResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataGenderServiceResultsTransfers.Fail,
        MaleoMetadataGenderServiceResultsTransfers.NoData,
        MaleoMetadataGenderServiceResultsTransfers.SingleData
    ]