from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.schemas.signature import MaleoFoundationSignatureSchemas

class MaleoFoundationSignatureResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Sign(BaseServiceGeneralResultsTransfers.SingleData):
        data: MaleoFoundationSignatureSchemas.Signature = Field(..., description="Single signature data")

    class Verify(BaseServiceGeneralResultsTransfers.SingleData):
        data: MaleoFoundationSignatureSchemas.IsValid = Field(..., description="Single verify data")