from enum import Enum

from ocsf.events.network import Network

from ocsf.objects.file import File


class FTPActivityActivityId(Enum):
    Put: int = 1 # File upload to the FTP or SFTP site.
    Get: int = 2 # File download from the FTP or SFTP site.
    Poll: int = 3 # Poll directory for specific file(s) or folder(s) at the FTP or SFTP site location.
    Delete: int = 4 # Delete file(s) from the FTP or SFTP site.
    Rename: int = 5 # Rename the file(s) in the FTP or SFTP site.
    List: int = 6 # List files in a specified directory.


class FTPActivity(Network):
    """
    File Transfer Protocol (FTP) Activity events report file transfers between a
    server and a client as seen on the network.
    """
    class_uid: int = 4008
    class_name: str = 'FTP Activity'

    # Recommended:
    codes: list[int] | None = None # The list of return codes to the FTP command.
    command: str | None = None # The FTP command.
    command_responses: list[str] | None = None # The list of responses to the FTP command.
    name: str | None = None # The name of the data affiliated with the command.
    port: int | None = None # The dynamic port established for impending data transfers.
    type: str | None = None # The type of FTP network connection (e.g. active, passive).

    # Optional:
    activity_id: FTPActivityActivityId | None = None
    file: File | None = None # The file that is the target of the FTP activity.
