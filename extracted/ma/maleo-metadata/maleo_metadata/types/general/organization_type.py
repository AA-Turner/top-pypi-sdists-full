from typing import List, Optional
from maleo_metadata.enums.organization_type import MaleoMetadataOrganizationTypeEnums
from maleo_metadata.models.transfers.general.organization_type import OrganizationTypeTransfers

class MaleoMetadataOrganizationTypeGeneralTypes:
    #* Simple organization type
    SimpleOrganizationType = MaleoMetadataOrganizationTypeEnums.OrganizationType
    OptionalSimpleOrganizationType = Optional[SimpleOrganizationType]
    ListOfSimpleOrganizationTypes = List[SimpleOrganizationType]
    OptionalListOfSimpleOrganizationTypes = Optional[List[SimpleOrganizationType]]

    #* Expanded organization type
    ExpandedOrganizationType = OrganizationTypeTransfers
    OptionalExpandedOrganizationType = Optional[ExpandedOrganizationType]
    ListOfExpandedOrganizationTypes = List[ExpandedOrganizationType]
    OptionalListOfExpandedOrganizationTypes = Optional[List[ExpandedOrganizationType]]