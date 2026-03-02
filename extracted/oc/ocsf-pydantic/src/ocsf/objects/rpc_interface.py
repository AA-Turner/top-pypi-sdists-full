from uuid import UUID
from pydantic import BaseModel

class RPCInterface(BaseModel):
    """
    The RPC Interface represents the remote procedure call interface used in the
    DCE/RPC session.
    """

    uuid: UUID # The unique identifier of the particular remote procedure or service.
    version: str # The version of the DCE/RPC protocol being used in the session.

    # Recommended:
    ack_reason: int | None = None
    ack_result: int | None = None
