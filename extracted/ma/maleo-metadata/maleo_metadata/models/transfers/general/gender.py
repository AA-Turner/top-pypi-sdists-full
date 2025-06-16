from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.schemas.gender import MaleoMetadataGenderSchemas

class GenderTransfers(
    MaleoMetadataGenderSchemas.Name,
    MaleoMetadataGenderSchemas.Key,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass