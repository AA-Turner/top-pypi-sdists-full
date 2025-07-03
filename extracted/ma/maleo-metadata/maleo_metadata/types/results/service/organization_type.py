from typing import Union
from maleo_metadata.models.transfers.results.service.organization_type import MaleoMetadataOrganizationTypeServiceResultsTransfers

class MaleoMetadataOrganizationTypeServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataOrganizationTypeServiceResultsTransfers.MultipleData,
        MaleoMetadataOrganizationTypeServiceResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeServiceResultsTransfers.Fail
    ]

    GetSingle = Union[
        MaleoMetadataOrganizationTypeServiceResultsTransfers.SingleData,
        MaleoMetadataOrganizationTypeServiceResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeServiceResultsTransfers.Fail
    ]