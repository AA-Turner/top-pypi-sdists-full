from typing import Union
from maleo_metadata.models.transfers.results.client.organization_type import MaleoMetadataOrganizationTypeClientResultsTransfers

class MaleoMetadataOrganizationTypeClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataOrganizationTypeClientResultsTransfers.Fail,
        MaleoMetadataOrganizationTypeClientResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataOrganizationTypeClientResultsTransfers.Fail,
        MaleoMetadataOrganizationTypeClientResultsTransfers.SingleData
    ]