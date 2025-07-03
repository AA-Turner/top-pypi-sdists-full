from typing import Union
from maleo_metadata.models.transfers.results.client.organization_type import MaleoMetadataOrganizationTypeClientResultsTransfers

class MaleoMetadataOrganizationTypeClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataOrganizationTypeClientResultsTransfers.MultipleData,
        MaleoMetadataOrganizationTypeClientResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeClientResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataOrganizationTypeClientResultsTransfers.SingleData,
        MaleoMetadataOrganizationTypeClientResultsTransfers.Fail
    ]