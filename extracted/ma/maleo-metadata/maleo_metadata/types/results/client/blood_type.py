from typing import Union
from maleo_metadata.models.transfers.results.client.blood_type import MaleoMetadataBloodTypeClientResultsTransfers

class MaleoMetadataBloodTypeClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataBloodTypeClientResultsTransfers.Fail,
        MaleoMetadataBloodTypeClientResultsTransfers.NoData,
        MaleoMetadataBloodTypeClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataBloodTypeClientResultsTransfers.Fail,
        MaleoMetadataBloodTypeClientResultsTransfers.SingleData
    ]