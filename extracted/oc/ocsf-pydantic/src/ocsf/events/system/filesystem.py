from enum import Enum

from ocsf.events.system import SystemActivity

from ocsf.objects.actor import Actor
from ocsf.objects.file import File


class FileSystemActivityActivityId(Enum):
    Create: int = 1
    Read: int = 2
    Update: int = 3
    Delete: int = 4
    Rename: int = 5
    Set_Attributes: int = 6
    Set_Security: int = 7
    Get_Attributes: int = 8
    Get_Security: int = 9
    Encrypt: int = 10
    Decrypt: int = 11
    Mount: int = 12
    Unmount: int = 13
    Open: int = 14

class FileSystemActivity(SystemActivity):
    """
    File System Activity events report when a process performs an action on a file
    or folder.
    """

    class_uid: int = 1001
    class_name: str = 'File System Activity'

    actor: Actor # The actor that performed the activity on the `file` object
    file: File # The file that is the target of the activity.

    # Recommended:
    component: str | None = None
    create_mask: str | None = None
    file_diff: str | None = None
    file_result: File | None = None # The resulting file object when the activity was allowed and
                                    # successful.

    # Optional:
    access_mask: int | None = None
    activity_id: FileSystemActivityActivityId | None = None
    connection_uid: str | None = None
