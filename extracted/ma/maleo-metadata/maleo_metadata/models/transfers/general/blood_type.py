from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.schemas.blood_type import MaleoMetadataBloodTypeSchemas

class BloodTypeTransfers(
    MaleoMetadataBloodTypeSchemas.Name,
    MaleoMetadataBloodTypeSchemas.Key,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass