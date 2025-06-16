from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.schemas.user_type import MaleoMetadataUserTypeSchemas

class UserTypeTransfers(
    MaleoMetadataUserTypeSchemas.Name,
    MaleoMetadataUserTypeSchemas.Key,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass