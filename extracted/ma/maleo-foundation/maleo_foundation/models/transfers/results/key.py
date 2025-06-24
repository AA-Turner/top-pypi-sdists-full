from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.transfers.general.key import MaleoFoundationKeyGeneralTransfers

class MaleoFoundationKeyResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class CreatePrivate(BaseServiceGeneralResultsTransfers.SingleData):
        data: MaleoFoundationKeyGeneralTransfers.PrivateKey = Field(..., description="Private key data")

    class CreatePublic(BaseServiceGeneralResultsTransfers.SingleData):
        data: MaleoFoundationKeyGeneralTransfers.PublicKey = Field(..., description="Private key data")

    class CreatePair(BaseServiceGeneralResultsTransfers.SingleData):
        data: MaleoFoundationKeyGeneralTransfers.KeyPair = Field(..., description="Key pair data")