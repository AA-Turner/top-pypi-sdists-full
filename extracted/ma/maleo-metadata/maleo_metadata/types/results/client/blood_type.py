from typing import Union
from maleo_metadata.models.transfers.results.client.blood_type import MaleoMetadataBloodTypeClientResultsTransfers

class MaleoMetadataBloodTypeClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataBloodTypeClientResultsTransfers.MultipleData,
        MaleoMetadataBloodTypeClientResultsTransfers.NoData,
        MaleoMetadataBloodTypeClientResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataBloodTypeClientResultsTransfers.SingleData,
        MaleoMetadataBloodTypeClientResultsTransfers.Fail
    ]