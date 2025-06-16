from __future__ import annotations
from .tables import MaleoMetadataTables
from .transfers import MaleoMetadataTransfers
from .responses import MaleoMetadataResponses
from .expanded_schemas import MaleoMetadataExpandedSchemas

class MaleoMetadataModels:
    Tables = MaleoMetadataTables
    Transfers = MaleoMetadataTransfers
    Responses = MaleoMetadataResponses
    ExpandedSchemas = MaleoMetadataExpandedSchemas