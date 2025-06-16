from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.schemas.service import MaleoMetadataServiceSchemas

class ServiceTransfers(
    MaleoMetadataServiceSchemas.Name,
    MaleoMetadataServiceSchemas.Key,
    MaleoMetadataServiceSchemas.Category,
    MaleoMetadataServiceSchemas.Type,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass