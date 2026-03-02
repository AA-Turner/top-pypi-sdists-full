from enum import Enum

from ocsf.events.network import Network

from ocsf.objects.dce_rpc import DCERPC
from ocsf.objects.file import File
from ocsf.objects.response import ResponseElements


class SMBActivityActivityId(Enum):
    File_Supersede: int = 1
    File_Open: int = 2
    File_Create: int = 3
    File_Open_If: int = 4
    File_Overwrite: int = 5
    File_Overwrite_If: int = 6


class SMBActivity(Network):
    """
    Server Message Block (SMB) Protocol Activity events report client/server
    connections sharing resources within the network.
    """

    class_uid: int = 4006
    class_name: str = 'SMB Activity'

    # Recommended:
    client_dialects: list[str] | None = None
    command: str | None = None # The command name (e.g. SMB2_COMMAND_CREATE, SMB1_COMMAND_WRITE_ANDX).
    dialect: str | None = None
    file: File | None = None # The file that is the target of the SMB activity.
    open_type: str | None = None # Indicates how the file was opened (e.g. normal, delete on close).
    response: ResponseElements | None = None # The server response in an SMB network connection.
    share: str | None = None # The SMB share name.
    share_type: str | None = None # The SMB share type, normalized to the caption of the share_type_id
                                  # value. In the case of 'Other', it is defined by the event source.
    share_type_id: int | None = None # The normalized identifier of the SMB share type.
    tree_uid: str | None = None

    # Optional:
    activity_id: SMBActivityActivityId | None = None
    dce_rpc: DCERPC | None = None
