from __future__ import annotations
from .general import MaleoMetadataGeneralTransfers
from .parameters import MaleoMetadataParametersTransfers
from .results import MaleoMetadataResultsTransfers

class MaleoMetadataTransfers:
    General = MaleoMetadataGeneralTransfers
    Parameters = MaleoMetadataParametersTransfers
    Results = MaleoMetadataResultsTransfers