from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.schemas.token import MaleoFoundationTokenSchemas
from maleo_foundation.models.transfers.general.token import MaleoFoundationTokenGeneralTransfers

class MaleoFoundationTokenResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Encode(BaseServiceGeneralResultsTransfers.SingleData):
        data: MaleoFoundationTokenSchemas.Token

    class Decode(BaseServiceGeneralResultsTransfers.SingleData):
        data: MaleoFoundationTokenGeneralTransfers.DecodePayload