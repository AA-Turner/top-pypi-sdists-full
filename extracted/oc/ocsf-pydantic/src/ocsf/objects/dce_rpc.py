
from .rpc_interface import RPCInterface

from pydantic import BaseModel

class DCERPC(BaseModel):
    """
    The DCE/RPC, or Distributed Computing Environment/Remote Procedure Call, object
    describes the remote procedure call system for distributed computing
    environments. Defined by D3FEND <a target='_blank' href='https://d3fend.mitre.or
    g/dao/artifact/d3f:RemoteProcedureCall/'>d3f:RemoteProcedureCall</a>.
    """

    flags: list[str] # The list of interface flags.
    rpc_interface: RPCInterface

    # Recommended:
    command: str | None = None # The request command (e.g. REQUEST, BIND).
    command_response: str | None = None # The reply to the request command (e.g. RESPONSE, BINDACK or
                                        # FAULT).
    opnum: int | None = None
