from enum import Enum
from datetime import datetime

from ocsf.events.network import Network

from ocsf.objects.actor import Actor
from ocsf.objects.file import File
from ocsf.objects.network_connection_info import NetworkConnectionInformation
from ocsf.objects.network_endpoint import NetworkEndpoint


class NetworkFileActivityActivityId(Enum):
    Upload: int = 1 # Upload a file.
    Download: int = 2 # Download a file.
    Update: int = 3 # Update a file.
    Delete: int = 4 # Delete a file.
    Rename: int = 5 # Rename a file.
    Copy: int = 6 # Copy a file.
    Move: int = 7 # Move a file.
    Restore: int = 8 # Restore a file.
    Preview: int = 9 # Preview a file.
    Lock: int = 10 # Lock a file.
    Unlock: int = 11 # Unlock a file.
    Share: int = 12 # Share a file.
    Unshare: int = 13 # Unshare a file.
    Open: int = 14 # Open a file.
    Sync: int = 15 # Mark a file or folder to sync with a computer.
    Unsync: int = 16 # Mark a file or folder to not sync with a computer.


class NetworkFileActivity(Network):
    """
    Network File Activity events report file activities traversing the network,
    including file storage services such as Box, MS OneDrive, or Google Drive.
    """

    class_uid: int = 4010
    class_name: str = 'Network File Activity'

    actor: Actor # The actor that performed the activity on the target file.
    file: File # The file that is the target of the activity.
    src_endpoint: NetworkEndpoint # The endpoint that performed the activity on the
                                  # target file.

    # Recommended:
    dst_endpoint: NetworkEndpoint | None = None # The endpoint that received the activity on the target
                                                # file.

    # Optional:
    activity_id: NetworkFileActivityActivityId | None = None
    connection_info: NetworkConnectionInformation | None = None
    expiration_time: datetime | None = None # The share expiration time.
