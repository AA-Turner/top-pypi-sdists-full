from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.schemas.token import MaleoFoundationTokenSchemas
from maleo_foundation.models.transfers.general.token import MaleoFoundationTokenGeneralTransfers

class MaleoFoundationTokenParametersTransfers:
    class Encode(
        MaleoFoundationTokenSchemas.Password,
        MaleoFoundationTokenSchemas.Key
    ):
        payload: MaleoFoundationTokenGeneralTransfers.BaseEncodePayload = Field(..., description="Encode payload")

    class Decode(
        MaleoFoundationTokenSchemas.Token,
        MaleoFoundationTokenSchemas.Key
    ): pass