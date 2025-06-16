from __future__ import annotations
from .general import MaleoMetadataGeneralParametersTransfers
from .service import MaleoMetadataServiceParametersTransfers
from .client import MaleoMetadataClientParametersTransfers

class MaleoMetadataParametersTransfers:
    General = MaleoMetadataGeneralParametersTransfers
    Service = MaleoMetadataServiceParametersTransfers
    Client = MaleoMetadataClientParametersTransfers