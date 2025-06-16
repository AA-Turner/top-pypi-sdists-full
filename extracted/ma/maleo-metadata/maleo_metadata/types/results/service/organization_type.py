from typing import Union
from maleo_metadata.models.transfers.results.service.organization_type import MaleoMetadataOrganizationTypeServiceResultsTransfers

class MaleoMetadataOrganizationTypeServiceResultsTypes:
    GetMultiple = Union[
        MaleoMetadataOrganizationTypeServiceResultsTransfers.Fail,
        MaleoMetadataOrganizationTypeServiceResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeServiceResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataOrganizationTypeServiceResultsTransfers.Fail,
        MaleoMetadataOrganizationTypeServiceResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeServiceResultsTransfers.SingleData
    ]