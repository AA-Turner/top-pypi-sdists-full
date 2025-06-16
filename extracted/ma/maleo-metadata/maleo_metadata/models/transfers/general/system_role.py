from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.schemas.system_role import MaleoMetadataSystemRoleSchemas

class SystemRoleTransfers(
    MaleoMetadataSystemRoleSchemas.Name,
    MaleoMetadataSystemRoleSchemas.Key,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass