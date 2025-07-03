from typing import Union
from maleo_metadata.models.transfers.results.service.gender import MaleoMetadataGenderServiceResultsTransfers

class MaleoMetadataGenderServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataGenderServiceResultsTransfers.MultipleData,
        MaleoMetadataGenderServiceResultsTransfers.NoData,
        MaleoMetadataGenderServiceResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataGenderServiceResultsTransfers.SingleData,
        MaleoMetadataGenderServiceResultsTransfers.NoData,
        MaleoMetadataGenderServiceResultsTransfers.Fail
    ]