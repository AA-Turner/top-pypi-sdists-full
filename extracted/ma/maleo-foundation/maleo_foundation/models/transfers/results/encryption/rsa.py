from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.schemas.encryption import MaleoFoundationEncryptionSchemas

class MaleoFoundationRSAEncryptionResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Encrypt(BaseServiceGeneralResultsTransfers.SingleData):
        data: MaleoFoundationEncryptionSchemas.Ciphertext = Field(..., description="Single encryption data")

    class Decrypt(BaseServiceGeneralResultsTransfers.SingleData):
        data: MaleoFoundationEncryptionSchemas.Plaintext = Field(..., description="Single decryption data")