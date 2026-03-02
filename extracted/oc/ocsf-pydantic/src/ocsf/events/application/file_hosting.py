from datetime import datetime
from enum import Enum

from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.file import File
from ocsf.objects.actor import Actor
from ocsf.objects.network_connection_info import NetworkConnectionInformation

from .application import Application


class FileHostingActivityActivityId(Enum):
    Upload: int = 1
    Download: int = 2
    Update: int = 3
    Delete: int = 4
    Rename: int = 5
    Copy: int = 6
    Move: int = 7
    Restore: int = 8
    Preview: int = 9
    Lock: int = 10
    Unlock: int = 11
    Share: int = 12
    Unshare: int = 13
    Open: int = 14
    Sync: int = 15
    Unsync: int = 16

class FileHostingActivity(Application):
    """
    File Hosting Activity events report the actions taken by file management
    applications, including file sharing servers like Sharepoint and services such
    as Box, MS OneDrive, or Google Drive.
    """

    class_uid: int = 6006
    class_name: str = 'File Hosting Activity'

    actor: Actor # The actor that performed the activity on the target file.
    file: File # The file that is the target of the activity.
    src_endpoint: NetworkEndpoint # The endpoint that performed the activity on the
                                  # target file.

    # Recommended:
    dst_endpoint: NetworkEndpoint | None = None # The endpoint that received the activity on the target
                                                # file.

    # Optional:
    activity_id: FileHostingActivityActivityId | None = None
    connection_info: NetworkConnectionInformation | None = None
    expiration_time: datetime | None = None # The share expiration time.
    file_result: File | None = None # The resulting file object when the activity was allowed and
                                    # successful.
