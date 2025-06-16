from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.schemas.organization_type import MaleoMetadataOrganizationTypeSchemas

class OrganizationTypeTransfers(
    MaleoMetadataOrganizationTypeSchemas.Name,
    MaleoMetadataOrganizationTypeSchemas.Key,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass